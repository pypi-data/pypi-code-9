import shutil


def clean():
    shutil.rmtree('build')


def main(args):
    clean()
