from file_importer import FileImporter

inp = FileImporter.get_input("/../input/16.txt").split("\n")

class Op:
    def __init__(self, op, a, b, c):
        self.op = op; self.a = a; self.b = b; self.c = c

opcodes = { 
    # Addition
    'addr' : lambda op, regs: regs[op.c] = regs[op.a] + regs[op.b],
    'addi' : lambda op, regs: regs[op.c] = regs[op.a] + op.b,

    # Multiplication
    'mulr' : lambda op, regs: regs[op.c] = regs[op.a] * regs[op.b],
    'muli' : lambda op, regs: regs[op.c] = regs[op.a] * op.b,

    # Bitwise AND
    'banr' : lambda op, regs: regs[op.c] = regs[op.a] & regs[op.b]
    'bani' : lambda op, regs: regs[op.c] = regs[op.a] & op.b

    # Bitwise OR
    'borr' : lambda op, regs: regs[op.c] = regs[op.a] | regs[op.b]
    'bori' : lambda op, regs: regs[op.c] = regs[op.a] | op.b

    # Assignment
    'setr' : lambda op, regs: regs[op.c] = regs[op.a]
    'seti' : lambda op, regs: regs[op.c] = op.addi

    # Greater-than testing:
    'gtir' : lambda op, regs: regs[op.c] = 1 if op.a > regs[op.b] else 0
    'gtri' : lambda op, regs: regs[op.c] = 1 if regs[op.a] > op.b else 0
    'gtrr' : lambda op, regs: regs[op.c] = 1 if regs[op.a] > regs[op.b] else 0

    # Equality testing: 
    'eqir' : lambda op, regs: regs[op.c] = 1 if op.a == regs[op.b] else 0
    'eqri' : lambda op, regs: regs[op.c] = 1 if regs[op.a]  == op.b else 0
    'eqrr' : lambda op, regs: regs[op.c] = 1 if regs[op.a] == regs[op.b] else 0
}


