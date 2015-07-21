import carboxylic

def add(cb, operand):
    cb.accumulator += cb.get_value(operand)

def bra(cb, operand):
    cb.counter = cb.branchpoints[operand]

def brp(cb, operand):
    if cb.accumulator > 0:
        cb.counter = cb.get_branch(operand)

def brz(cb, operand):
    if cb.accumulator == 0:
        cb.counter = cb.get_branch(operand)

def define(cb, operand):
    # We can't call this `def` since it's already a Python keyword.
    cb.branchpoints.update({operand : cb.counter})

def hlt(cb, operand):
    raise carboxylic.CarboxylicHalt()

def inp(cb, operand):
    cb.accumulator = int(raw_input(">>> "))

def lda(cb, operand):
    cb.accumulator = cb.get_value(operand)

def out(cb, operand):
    print "<<< %s" % cb.accumulator

def sta(cb, operand):
    cb.registers.update({operand : cb.accumulator})

def sub(cb, operand):
    cb.accumulator -= cb.get_value(operand)

commands = {
    "ADD" : add,
    "BRA" : bra,
    "BRP" : brp,
    "BRZ" : brz,
    "DEF" : define,
    "HLT" : hlt,
    "INP" : inp,
    "LDA" : lda,
    "OUT" : out,
    "STA" : sta,
    "SUB" : sub,
}
