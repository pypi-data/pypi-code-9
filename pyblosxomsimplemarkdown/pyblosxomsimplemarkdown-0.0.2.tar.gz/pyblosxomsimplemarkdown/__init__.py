__author__      = "Sean Hammond pyblosxomsimplemarkdown at seanh dot cc"
__version__     = "0.1"
__url__         = "https://github.com/seanh/pyblosxomsimplemarkdown"
__description__ = ("A Pyblosxom entryparser plugin that uses Markdown syntax "
                   "and parses the whole file as the entry body")


from Pyblosxom import tools


def verify_installation(request):
    try:
        import markdown
        return True
    except ImportError:
        print "Couldn't import markdown, is Python Markdown installed?"
        return False


def cb_entryparser(entryparsingdict):
    for extension in ('md', 'markdown'):
        entryparsingdict[extension] = parse
    return entryparsingdict


def cb_preformat(args):
    if args.get('parser') == 'simplemarkdown':
        import markdown
        return markdown.markdown(
            u''.join(args['story']),
            extensions=['extra', 'smarty'],
            output_format='html5'
        )


def parse(filename, request):
    # FIXME: We're assuming the file is UTF-8.
    lines = [line.decode('utf8') for line in open(filename, 'r').readlines()]

    # Call the preformat function, this should return us an HTML string for
    # the body of the entry.
    args = {'parser': 'simplemarkdown', 'story': lines, 'request': request}
    body = tools.run_callback(
        'preformat', args, donefunc=lambda x: x is not None,
        defaultfunc=lambda x: ''.join(x['story']))

    entry_data = {'body': body}  # No title!

    # Call the postformat callbacks.
    tools.run_callback(
        'postformat', {'request': request, 'entry_data': entry_data})

    return entry_data
