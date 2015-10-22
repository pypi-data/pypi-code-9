import os


NEEDS_ENVIRONMENT = True


def add_command_line_arguments(parser, _environ):
    parser.add_argument('source',
        help='Path of the executable in the container')
    parser.add_argument('dest',
        help='Name of the destination executable')


def run_command(options):
    install_program_link(options.bin_dir, options.dest, options.source)

    #config = Config(options.config_file)
    #config['link'][options.dest] = options.source
    #config.write()


def install_program_link(bin_dir, dest, source):
    if dest[0] in ('.', '/'):
        raise Exception('Destination must be a base filename. No path is allowed.')

    out = """\
#!/bin/sh
if [ -z "$CLEAN_ENV" ]; then
    export CLEAN_ENV=`readlink -f $(dirname $0)/..`
fi

exec $CLEAN_ENV/.env/bin/inenv -- %s $@
""" % source

    path = os.path.join(bin_dir, dest)
    open(path, 'w').write(out)
    os.chmod(path, 0o755)


def install_program_links(bin_dir, config):
    for dest, source in config['link'].items():
        install_program_link(bin_dir, dest, source)

