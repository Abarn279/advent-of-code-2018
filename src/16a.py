from file_importer import FileImporter
import re

class Op:
    def __init__(self, op, a, b, c):
        self.op = op; self.a = a; self.b = b; self.c = c

# Addition
def addr(op, regs): regs[op.c] = regs[op.a] + regs[op.b]; return regs
def addi(op, regs): regs[op.c] = regs[op.a] + op.b; return regs

# Multiplication
def mulr(op, regs): regs[op.c] = regs[op.a] * regs[op.b]; return regs
def muli(op, regs): regs[op.c] = regs[op.a] * op.b; return regs

# Bitwise AND
def banr(op, regs): regs[op.c] = regs[op.a] & regs[op.b]; return regs
def bani(op, regs): regs[op.c] = regs[op.a] & op.b; return regs

# Bitwise OR
def borr(op, regs): regs[op.c] = regs[op.a] | regs[op.b]; return regs
def bori(op, regs): regs[op.c] = regs[op.a] | op.b; return regs

# Assignment
def setr(op, regs): regs[op.c] = regs[op.a]; return regs
def seti(op, regs): regs[op.c] = op.a; return regs

# Greater-than testing:
def gtir(op, regs): regs[op.c] = 1 if op.a > regs[op.b] else 0; return regs
def gtri(op, regs): regs[op.c] = 1 if regs[op.a] > op.b else 0; return regs
def gtrr(op, regs): regs[op.c] = 1 if regs[op.a] > regs[op.b] else 0; return regs

# Equality testing
def eqir(op, regs): regs[op.c] = 1 if op.a == regs[op.b] else 0; return regs
def eqri(op, regs): regs[op.c] = 1 if regs[op.a]  == op.b else 0; return regs
def eqrr(op, regs): regs[op.c] = 1 if regs[op.a] == regs[op.b] else 0; return regs

opcodes = { 
    'addr' : addr,
    'addi' : addi,
    'mulr' : mulr,
    'muli' : muli,
    'banr' : banr,
    'bani' : bani,
    'borr' : borr,
    'bori' : bori,
    'setr' : setr,
    'seti' : seti,
    'gtir' : gtir,
    'gtri' : gtri,
    'gtrr' : gtrr,
    'eqir' : eqir,
    'eqri' : eqri,
    'eqrr' : eqrr
}

inp = FileImporter.get_input("/../input/16.txt").split("\n\n\n")[0].split('\n')
count = 0
for i in range(0, len(inp), 4):
    registers_before = eval(re.match('Before: (\[.+\])', inp[i]).groups()[0])
    op = Op(*map(int, inp[i + 1].split(' ')))
    registers_after = eval(re.match('After:  (\[.+\])', inp[i + 2]).groups()[0]) 

    if sum(1 for opcode in opcodes if opcodes[opcode](op, registers_before[:]) == registers_after) >= 3:
        count += 1

print(count)
