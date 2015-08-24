import string

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
    fp.write(code)
    fp.close()
    return "[DEBUG] success to create : %s" % file_path


