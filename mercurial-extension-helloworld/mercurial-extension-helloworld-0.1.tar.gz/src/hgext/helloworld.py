"""Hello world extension
"""


def extsetup(ui):
    """setup extension
    """
    from mercurial import commands
    commands.norepo += ' hello'


def hello(ui, *opts):
    ui.write("Hello world!\n")

cmdtable = {
    'hello': (hello, [], 'Says "Hello world!"'),
}
