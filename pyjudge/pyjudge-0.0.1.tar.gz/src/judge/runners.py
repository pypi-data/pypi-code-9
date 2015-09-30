'''
Runner functions are responsible for running some specific interaction example
and gathering input, ouput and prompt strings.
'''

from judge import errors
from judge import builtins
from judge import util
from judge.util import timeout as run_with_timeout
from judge.parsers import Example, IOTemplate


def run_unsafe_python(example: Example, src: str, *,
                      namespace=None,
                      exec=exec,  # @ReservedAssignmenth
                      timeout=None):
    '''Run a string of Python code and return the Example() object for this
    interaction.

    Parameters
    ----------

    example : Example or template string
        The example object describing the interaction.
    src : str
        A string of Python source code or a code object that is passed to
        the exec() function.
    namespace : dict
        A namespace dictionary that is passed to the exec function.
    exec : callable
        A function that is executed as exec(src, namespace) in order to run
        the code in the given namespace. The function do not need to return
        anything, but rather must execute the correct `print` and `input`
        statements in order to recriate the correct Example() output.
    '''
    if isinstance(example, str):
        example = Example(example)

    # Prepare list of inputs and interactions
    interaction = []
    inputs = list(example.get_inputs())
    namespace = namespace if namespace is not None else {}

    # Prepare overrides for the builtin functions
    print_func = util.make_interaction_print(interaction)
    input_func = util.make_interaction_input(interaction, inputs)

    # Run code and return interactions. All errors that are not related to
    # code giving wrong answers will be captured at this stage
    builtins.update(print=print_func, input=input_func)
    try:
        if timeout:
            run_with_timeout(exec, args=(src, namespace), timeout=timeout)
        else:
            exec(src, namespace)

    # Execution exceeded timeout
    except TimeoutError:
        ex = errors.TimeExceededError()
        out = Example(interaction, error=ex, validate=False)

    # Program asked for a non-existing input
    except errors.MissingInputError as ex:
        out = Example(interaction, error=ex, validate=False)

    # Bad syntax in code
    except SyntaxError as ex:
        tb = ex.__traceback__
        ex = errors.BuildError(src, ex.with_traceback(tb))
        out = Example(interaction, error=ex, validate=False)

    # Some generic runtime error happened
    except Exception as ex:
        tb = ex.__traceback__
        ex = errors.UnexpectedError(ex.with_traceback(tb))
        out = Example(interaction, error=ex, validate=False)

    # Execution terminated
    else:
        # ... but did not used all necessary inputs
        if inputs:
            ex = errors.UnusedInputError(inputs)
            out = Example(interaction, error=ex, validate=False)
        else:
            out = Example(interaction, value=example.value,
                          feedback=example.feedback)

    finally:
        builtins.restore()
    return out


def run_python(example, src, **kwds):
    '''Safe sandboxed version of run_unsafe_python().

    This function has the overhead of starting another Python interpreter with
    reduced permissions.'''

    return run_unsafe_python(example, src, **kwds)


def run_unsafe_file(example: Example, path):
    '''Run executable file in the given path through shell and obtain the
    correct interactions'''

    raise NotImplementedError


def run_file(example: Example, path, **kwds):
    '''Safe sandboxed version of run_unsafe_file().

    This function runs the file with reduced permissions.'''

    return run_unsafe_file(example, path, **kwds)


def run_template_python(template, src, *,
                        stop_at_error=True,
                        check_value=True,
                        is_safe=False, **kwds):
    '''Run all examples in template and return the corresponding IOTemplate'''

    if isinstance(template, str):
        template = IOTemplate(template)

    # Choose runner function
    runner_func = run_unsafe_python if is_safe else run_python

    def runner(ex):
        result = runner_func(ex, src, **kwds)
        if isinstance(check_value, dict):
            return result.with_grades(ex, **check_value)
        elif check_value:
            return result.with_grades(ex)
        else:
            return result

    # Run examples and grade
    if stop_at_error:
        max_value = 1
        out = []
        for example in template:
            result = runner(example)
            out.append(result)
            if result.error:
                break
        return IOTemplate(out, value=max_value)
    else:
        return IOTemplate([runner(example) for example in template])


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    code1 = "x=input('x'); y=input('y'); print(x + y)"
    code1 = "x=input('x'); y=input('y'); print('ab')"
    code2 = "x=input('x'); print('abc')"
    code3 = "x=input('x'); y=input('y'); z=input('z'); print(x + y)"
    tmpl1 = "x: a; y: b --> ab"
    tmpl2 = "x: 1; y: 2 --> 12"
    tmpl3 = "x: x; y: y --> xy"
    template = '\n\n'.join([tmpl1, tmpl2, tmpl3])

    print(run_python(tmpl1, code1))

    from judge.parsers import parse_io_template
    print(parse_io_template(template))

    out = run_template_python(template, code1)
    print(out)
