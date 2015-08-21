
def bash_run(**kwargs):
    code = kwargs['code']
    import os
    os.system("bash -c '%s'" % code)
    return "Bash executed"


