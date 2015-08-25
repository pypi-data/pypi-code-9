###########################################
# This is very naive replacement algorithm
# TODO
############################################
import string

def replaceable(code, kv):
    # change keyword to value
    keys = kv.keys()
    # find keyword which is ${keyword}
    # replace value ${keyword} <- kv[keyword]
    for key in keys:
        nkey = "${%s}" % key
        code = string.replace(code, nkey, kv[key])
    print '#' * 40
    print code
    print '#' * 40
    return code

def bash_run(**kwargs):
    code = kwargs['code']
    kv = kwargs['kv']

    import os
    # call replaceable
    rcode = replaceable(code, kv)

    os.system("bash -c '%s'" % rcode)
    return "Bash executed"


