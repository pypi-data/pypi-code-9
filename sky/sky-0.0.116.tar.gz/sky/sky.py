def get_args_parser():
    p = argparse.ArgumentParser(
        description='Discover where your sensitive data has been leaked.')
    p.add_argument('-user', '-u',
                   help='Provide a github username, only if also -repo')
    p.add_argument('-repo', '-r',
                   help='Provide a github repo, only if also -user')
    p.add_argument('-link', '-l',
                   help='Provide a link to clone')
    p.add_argument('-delete', '-d', action='store_true',
                   help='If cloned, remove the repo afterwards.')
    p.add_argument('--find-anything', '-a', action='store_true',
                   help='flag: If you want to find anything remotely suspicious.')
    p.add_argument('--case-sensitive', '-c', action='store_true',
                   help='flag: If you want to be specific about case matching.')
    p.add_argument('--excluding', '-e', nargs='+',
                   help='List of words that are ignored occurring as value.')
    p.add_argument('--verbose', '-v', action='store_true',
                   help='If flag given, print verbose matches.')
    p.add_argument('--no-banner', '-b', action='store_true',
                   help='Omit the banner at the start of a print statement')
    p.add_argument('--no-fancy-color', '-f', action='store_true',
                   help='Omit the banner at the start of a print statement')
    return p


def main():
    """ This is the function that is run from commandline with `gittyleaks` """
    args = get_args_parser().parse_args()
    gl = GittyLeak(args.__dict__)
    try:
        gl.run()
    except KeyboardInterrupt:
        print('sky interupted')
    gl.printer()
