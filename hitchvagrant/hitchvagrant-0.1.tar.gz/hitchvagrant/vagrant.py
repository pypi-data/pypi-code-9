from sys import argv, stdout, stderr, exit
from subprocess import call, PIPE
from os import path, chdir
import optparse
import time


def run():
    parser = optparse.OptionParser()
    parser.add_option("-d", "--directory", type="str", dest="directory", default=".",
                      help="Specify the directory that contains the Vagrantfile (default: current directory)")

    options, _ = parser.parse_args(argv[1:])
    directory = path.abspath(options.directory)

    if call(["which", "vagrant"], stdout=PIPE, stderr=PIPE) != 0:
        stderr.write("Vagrant not installed.\n")
        exit(1)

    if path.exists(directory):
        chdir(directory)
    else:
        stderr.write("Directory does not exist.\n")
        exit(1)

    if not path.exists(path.join(directory, "Vagrantfile")):
        stderr.write("Vagrantfile does not exist at '{}'.\n".format(directory))
        exit(1)

    try:
        call(["vagrant", "up"])
        stdout.write("Vagrant service ready\n")
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        stdout.write("Shutting down vagrant...\n")
        returncode = call(["vagrant", "halt"])

        if returncode != 0:
            subprocess.call(["vagrant", "halt", "--force"])
        exit(0)

if __name__=='__main__':
    run()
