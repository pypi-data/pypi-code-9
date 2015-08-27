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


def find_file_path(lookahead):
    print lookahead
    if lookahead == None:
        return None
    ctx = lookahead['text']
    items = ctx.split()
    if items[0] == 'edit':
        return items[1]


def editor_run(**kwargs):
    lookahead = kwargs['lookahead']
    code = kwargs['code']
    kv = kwargs['kv']

    file_path = find_file_path(kwargs['lookahead'])
    if file_path == None:
        msg = "[DEBUG] I don't know how to edit!"
        print msg
        return msg
    fp = open(file_path, 'w')
    rcode = replaceable(code, kv)
    fp.write(rcode)
    fp.close()
    return "[DEBUG] success to create : %s" % file_path


