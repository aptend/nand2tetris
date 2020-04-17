import sys
import re
import os
import shutil
import tempfile
from enum import Enum
from warnings import warn
from collections import deque


class AssemblerError(Exception):
    def __str__(self):
        return "".join(self.args)


class UnkownCompError(AssemblerError):
    pass


class UnkownDestError(AssemblerError):
    pass


class UnkownJumpError(AssemblerError):
    pass


class KeyNotFoundError(AssemblerError):
    pass


class InvalidSymbolError(AssemblerError):
    pass


class MacroError(AssemblerError):
    pass


class Dumper:
    def __init__(self, file, encoder):
        (self.f, self.name) = tempfile.mkstemp()
        self.true_f = file
        self.encoder = encoder

    def dump_c_ins(self, dest, comp, jump):
        self.write_line(self.encoder.c_ins(dest, comp, jump))

    def dump_a_ins(self, address):
        self.write_line(self.encoder.a_ins(address))

    def write_line(self, content):
        bin_content = (content + '\n').encode('utf8')
        os.write(self.f, bin_content)

    def commit(self):
        os.fsync(self.f)
        os.close(self.f)
        shutil.move(self.name, self.true_f)

    def cancel(self):
        try:
            os.close(self.f)
            os.remove(self.name)
        except (IOError, OSError):
            pass


class Encoder:
    def __init__(self):
        self.jumps = {
            "": "000",
            "JMP": "111",
            "JEQ": "010",
            "JNE": "101",
            "JLT": "100",
            "JLE": "110",
            "JGT": "001",
            "JGE": "011",
        }
        self.comps = {
            "0": "101010",
            "1": "111111",
            "-1": "111010",
            "D": "001100",
            "A": "110000",
            "!D": "001101",
            "!A": "110001",
            "-D": "001111",
            "-A": "110011",
            "D+1": "011111",
            "A+1": "110111",
            "D-1": "001110",
            "A-1": "110010",
            "D+A": "000010",
            "D-A": "010011",
            "A-D": "000111",
            "D&A": "000000",
            "D|A": "010101",
        }

        self.dest_map = dict(A=4, D=2, M=1)

    def c_ins(self, dest, comp, jump):
        select_mem = "0"
        # compose an instruction for operation on Memery[A]
        _comp = comp
        if "M" in comp:
            select_mem = "1"
            _comp = comp.replace("M", "A")

        if (comp_bin := self.comps.get(_comp, None)) is None:
            raise UnkownCompError(repr(comp))

        if (jump_bin := self.jumps.get(jump, None)) is None:
            raise UnkownJumpError(repr(jump))

        dest_set = set(dest)
        if len(dest_set - set("ADM")) > 0:
            raise UnkownDestError(repr(dest))
        s = sum(self.dest_map[d] for d in dest_set)
        dest_bin = f"{s:03b}"

        return f"111{select_mem}{comp_bin}{dest_bin}{jump_bin}"

    def a_ins(self, address):
        assert isinstance(address, int)
        address_bin = f"{address:016b}"
        return f"0{address_bin[-15:]}"


class SymbolTable:
    def __init__(self):
        self.pos = 16
        self.variables = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576,
        }
        for i in range(16):
            self.variables[f"R{i}"] = i

        self.labels = {}

    def add_symbol_if_not_present(self, symbol):
        if symbol not in self.variables and symbol not in self.labels:
            self.variables[symbol] = self.pos
            self.pos += 1

    def add_label(self, lable, address):
        self.labels[lable] = address

    def address(self, key):
        if key in self.variables:
            return self.variables[key]
        elif key in self.labels:
            return self.labels[key]
        else:
            raise KeyNotFoundError(f"not found {key!r}")


class Statement(Enum):
    Label = 0
    AIns = 1
    CIns = 2


class Parser:
    def __init__(self, lines: "FileLike"):
        self._lines = iter(lines)
        self._expand_space = deque()
        self._current_line = None
        self._ins_addr = -1
        self._line_num = 0
        self.user_define_re = re.compile(r"[a-zA-Z_:$\.][a-zA-Z_:$0-9\.]*")
        self.eat()

    def eat(self):
        # read from expanded space first
        if self._expand_space:
            line = self._expand_space.popleft()
        else:
            try:
                line = next(self._lines).strip()
                # add line_num only when we read from files
                self._line_num += 1
            except StopIteration:
                # all lines are exhausted, return
                self._current_line = None
                return

        # find a line
        if (idx := line.find(r"//")) >= 0:
            line = line[:idx]

        if line == "":
            self.eat()
        elif self._try_macro_expand(line):
            self.eat()
        else:
            self._current_line = line
            if not self._is_lable(line):
                self._ins_addr += 1

    def _try_macro_expand(self, line):
        m_matches = re.findall(r'(M\[\s*(.*?)\s*\])', line)
        j_matches = re.findall(r'(J(EQ|NE|LT|LE|GT|GE|MP)\s*@(.*?)\s*)$', line)
        if not m_matches and not j_matches:
            return False
        if m_matches and j_matches:
            warn('It is dangerous! You are using M and jump in one instrucion')
        if m_matches:
            mmacro, var = m_matches[0]
            if not all(m[1] == var for m in m_matches):
                raise MacroError("bad macro expression: inconsistent M[..]")
            line = line.replace(mmacro, 'M')
            self._expand_space.append(f'@{var}')

        if j_matches:
            jmacro, jtyp, jdest = j_matches[0]
            line = line.replace(jmacro, jmacro[:3])
            self._expand_space.append(f'@{jdest}')

        self._expand_space.append(line)
        return True

    @property
    def ins_addr(self):
        return self._ins_addr

    @property
    def line_num(self):
        return self._line_num

    def has_next(self):
        return self._current_line is not None

    def _is_valid_user_defined(self, symbol):
        return self.user_define_re.fullmatch(symbol) is not None

    def _is_lable(self, token):
        return token[0] == "(" and token[-1] == ")"

    def _is_a_ins(self, token):
        return token[0] == "@"

    def statement_type(self):
        token = self._current_line
        if self._is_lable(token):
            typ = Statement.Label
        elif self._is_a_ins(token):
            typ = Statement.AIns
        else:
            typ = Statement.CIns
        return typ

    def parse_label(self):
        token = self._current_line[1:-1].strip()
        if self._is_valid_user_defined(token):
            return token
        else:
            raise InvalidSymbolError(f"bad name for label: {token!r}")

    def parse_a_ins(self):
        token = self._current_line[1:].strip()
        if token.isdigit() or self._is_valid_user_defined(token):
            return token
        else:
            raise InvalidSymbolError(f"bad symbol for a-instruction: {token!r}")

    def parse_c_ins(self):
        token = self._current_line
        *dest, rest = token.split("=", maxsplit=1)
        dest = dest[0].replace(" ", "") if dest else ""
        comp, *jump = rest.rsplit(";", maxsplit=1)
        jump = jump[0].replace(" ", "") if jump else ""
        comp = comp.replace(" ", "")
        return dest, comp, jump


def assemble(filepath):
    name, *ext = filename.rsplit(".", maxsplit=1)
    complied_filename = name + ".hack"

    dumper = Dumper(complied_filename, Encoder())
    symbol_table = SymbolTable()

    f = open(filename)
    parser = Parser(f)

    # first pass, collect labels
    try:
        while parser.has_next():
            if parser.statement_type() == Statement.Label:
                symbol_table.add_label(parser.parse_label(), parser.ins_addr + 1)
            parser.eat()

        # second pass, compile .asm
        f.seek(0)
        parser = Parser(f)
        while parser.has_next():
            typ = parser.statement_type()
            if typ == Statement.AIns:
                symbol = parser.parse_a_ins()
                if symbol.isdigit():
                    dumper.dump_a_ins(int(symbol))
                else:
                    symbol_table.add_symbol_if_not_present(symbol)
                    dumper.dump_a_ins(symbol_table.address(symbol))
            elif typ == Statement.CIns:
                dumper.dump_c_ins(*parser.parse_c_ins())
            parser.eat()
    except AssemblerError as e:
        dumper.cancel()
        raise e.__class__(
            f"{e.__class__.__name__} at {parser.line_num} line: ", *e.args
        ) from e
    else:
        dumper.commit()
    finally:
        f.close()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit(1)
    filename = sys.argv[1]
    try:
        assemble(filename)
    except AssemblerError as e:
        print(e)
