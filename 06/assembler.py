import logging

class AssemblerError(Exception):
    pass

class UnkownCompError(AssemblerError):
    pass

class UnkownDestError(AssemblerError):
    pass

class UnkownJumpError(AssemblerError):
    pass

class KeyNotFoundError(AssemblerError):
    pass

class InvalidSymbol(AssemblerError):
    pass

class Dumper:
    def __init__(self, file, encoder):
        self.f = open(file, 'w')
        self.encoder = encoder
    
    def dump_c_ins(self, dest, comp, jump):
        self.f.write(self.encoder.c_ins(dest, comp, jump))
        self.f.write('\n')
    
    def dump_a_ins(self, address):
        self.f.write(self.encoder.a_ins(address))
        self.f.write('\n')
    
    def close(self):
        self.f.flush()
        self.f.close()

class Encoder:
    def __init__(self):
        self.jumps = {
            '': '000',
            'JMP': '111',
            'JEQ': '010',
            'JNE': '101',
            'JLT': '100',
            'JLE': '110',
            'JGT': '001',
            'JGE': '011'
        }
        self.dests = {
            '': '000',
            'A': '100',
            'D': '010',
            'M': '001',
            'AD': '110',
            'AM': '101',
            'DM': '011',
            'AMD': '111',
        }
        self.comps = {
            '0': '101010',
            '1': '111111',
            '-1': '111010',
            'D': '001100',
            'A': '110000',
            '!D': '001101',
            '!A': '110001',
            '-D': '001111',
            '-A': '110011',
            'D+1': '011111',
            'A+1': '110111',
            'D-1': '001110',
            'A-1': '110010',
            'D+A': '000010',
            'D-A': '010011',
            'A-D': '000111',
            'D&A': '000000',
            'D|A': '010101',
        }

    def c_ins(self, dest, comp, jump):
        select_mem = '0'
        # compose an instruction for operation on Memery[A]
        if 'M' in comp:
            select_mem = '1'
            comp = comp.replace('M', 'A')

        if (comp_bin := self.comps.get(comp, None)) is None:
            raise UnkownCompError(repr(comp))

        if (jump_bin := self.jumps.get(jump, None)) is None:
            raise UnkownJumpError(repr(jump))

        dest_set = set(dest)
        if len(dest_set - set('ADM')) > 0:
            raise UnkownDestError(repr(dest))
        dest_bin = ['0', '0', '0']
        dest_map = dict(A=0, D=1, M=2)
        for d in dest_set:
            dest_bin[dest_map[d]] = '1'
        dest_bin = ''.join(dest_bin)
        
        
        return f'111{select_mem}{comp_bin}{dest_bin}{jump_bin}'

    def a_ins(self, address):
        assert isinstance(address, int)
        address_bin = f'{address:016b}'
        return f'0{address_bin[-15:]}'


class SymbolTable:
    def __init__(self):
        self.pos = 16
        self.variables = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'SCREEN': 16384,
            'KBD': 24576,
        }
        for i in range(16):
            self.variables[f'R{i}'] = i

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
            raise KeyNotFoundError(f'not found {key:!r}')

from enum import Enum
import re

class Statement(Enum):
    Label = 0
    AIns = 1
    CIns = 2


class Parser:
    def __init__(self, lines: "FileLike"):
        self.lines = iter(lines)
        self.current_line = None
        self._ins_addr = -1
        self._line_num = -1
        self.user_define_re = re.compile(r'[a-zA-Z_:$\.][a-zA-Z_:$0-9\.]*')
        self.eat()

    def eat(self):
        try:
            line = next(self.lines).strip()
            if (idx := line.find(r'//')) >= 0:
                line = line[:idx]
            self._line_num += 1
        except StopIteration:
            self.current_line = None
            return
        if line == '':
            self.eat()
        else:
            self.current_line = line
            if not self._is_lable(line):
                self._ins_addr += 1
    
    @property
    def ins_addr(self):
        return self._ins_addr


    def has_next(self):
        return self.current_line is not None

    def _is_valid_user_defined(self, symbol):
        return self.user_define_re.fullmatch(symbol) is not None

    def _is_lable(self, token):
        return token[0] == '(' and token[-1] == ')'
    
    def _is_a_ins(self, token):
        return token[0] == '@'

    def statement_type(self):
        token = self.current_line
        if self._is_lable(token):
            typ = Statement.Label
        elif self._is_a_ins(token):
            typ = Statement.AIns
        else:
            typ = Statement.CIns
        return typ

    def parse_label(self):
        token = self.current_line[1:-1].strip()
        if self._is_valid_user_defined(token):
            return token
        else:
            raise InvalidSymbol(f'bad name for label: {token:!r}')

    def parse_a_ins(self):
        token = self.current_line[1:].strip()
        if token.isdigit() or self._is_valid_user_defined(token):
            return token
        else:
            raise InvalidSymbol(f'bad symbol for a-instruction: {token:!r}')

    def parse_c_ins(self):
        token = self.current_line
        *dest, rest = token.split('=', maxsplit=1)
        dest = dest[0].replace(' ', '') if dest else ''
        comp, *jump = rest.rsplit(';', maxsplit=1)
        jump = jump[0].replace(' ', '') if jump else ''
        comp = comp.replace(' ', '')
        return dest, comp, jump


import sys


def main():
    if len(sys.argv) <= 1:
        exit(1)
    filename = sys.argv[1]
    name, *ext = filename.rsplit('.', maxsplit=1)
    complied_filename = name + '.hack'
    
    encoder = Encoder()
    dumper = Dumper(complied_filename, encoder)

    f = open(filename)
    parser = Parser(f)
    symbol_table = SymbolTable()

    # first pass, collect labels
    while parser.has_next():
        if parser.statement_type() == Statement.Label:
            symbol_table.add_label(parser.parse_label(), parser.ins_addr+1)
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
    f.close()


if __name__ == '__main__':
    main()

