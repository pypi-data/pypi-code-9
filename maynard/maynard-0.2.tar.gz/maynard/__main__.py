from maynard import *

disassemble(disassemble)

source_code = """

def f:
    arg operand

    global print

    const fred 88
    const none None

    local barney

    load print
    load fred
    call_function positional=1

    load print
    load fred
    store barney
    load barney
    here:
    load operand

    binary_add
    call_function p=1 kw=0
    pop_top
    jump_absolute beyond

    load fred
    return_value

    beyond:
    load print
    return_value

    end

def g:
    arg operand
    arg operand2

    load operand
    load operand2
    binary_add
    return_value

    end

class H:
    local a
    const three 3
    load three
    store a
    end


def outer:
    arg arg

    def inner:
        arg arg

        const three 3

        load arg
        load three
        binary_add
        return_value
        end

    load inner
    load arg
    call_function positional=1 kwonly=0
    return_value
    end

def with_defaults:
    arg a
    arg b 50
    kwonly c 100

    load a
    load b
    binary_add
    load c
    binary_add
    return_value
    end

def r_args:
    args foo

    load foo
    return_value
    end

def r_kwargs:
    kwargs foo

    load foo
    return_value
    end

"""

a = Assembler('module', type='module')
a.assemble(source_code.split('\n'))
module = a.make_module()

f = module.f
# disassemble(f)
# disassemble(foo)
# from colorsys import rgb_to_hls
f(5)

disassemble(module.with_defaults)
print("module.with_defaults.__code__.co_consts", module.with_defaults.__code__.co_consts)
print("module.with_defaults.__defaults__", module.with_defaults.__defaults__)
print("module.with_defaults.__kwdefaults__", module.with_defaults.__kwdefaults__)
print(module.with_defaults(1, 2, c=4))
print(module.with_defaults(1, 2))
print(module.with_defaults(1))

def xyz(x): return x ** 5
xyz(3)

print('f(3) returned:', module.f(3))
print('g(3, 6) returned:', module.g(3, 6))

# h = H()

# help(a.module.g)
