from bpython import embed

def bpython_shell_runner(env, help):
    return embed(locals_=env, banner=help + '\n')
