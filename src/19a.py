from file_importer import FileImporter

class Op:
    def __init__(self, op, a, b, c):
        self.op = str(op); self.a = int(a); self.b = int(b); self.c = int(c)

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

program = FileImporter.get_input("/../input/19.txt").split("\n")
inst_pointer_reg = int(program.pop(0).split(' ')[1])
program = [Op(*i.split(' ')) for i in program]
inst_pointer = 0
registers = { i : 0 for i in range(0, 6) }

while True:
    if inst_pointer >= len(program):
        break

    registers[inst_pointer_reg] = inst_pointer
    op = program[inst_pointer]
    registers = opcodes[op.op](op, registers)
    inst_pointer = registers[inst_pointer_reg] + 1

print(registers[0])