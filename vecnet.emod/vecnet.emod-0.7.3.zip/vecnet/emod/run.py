import os
import json
import subprocess
import sys


def run_emod(emod_executable,
             input_dir,
             config=None,
             emod_input_files_dir=None):

    if emod_input_files_dir is None:
        emod_input_files_dir = input_dir

    if config is not None:
        with open(os.path.join(input_dir, "config.json"), "w") as fp:
            json.dump(config, fp, indent=4, sort_keys=True)

    command = [emod_executable,
               "-C", os.path.join(input_dir, "config.json"),
               "-I", emod_input_files_dir,
               "-O", os.path.join(input_dir, "output")
               ]

    with open(os.path.join(input_dir, "stdout.txt"), 'w') as stdout:
        # EMOD standard output will be saved to stdout.txt
        print >>stdout, "Command executed: %s" % command
        print >>stdout
        stdout.flush()
        exitcode = subprocess.call(command,
                                   cwd=input_dir,
                                   stdout=stdout,
                                   stderr=stdout,
                                   )
    return exitcode


def run_emod_in_background(emod_executable, input_dir, config=None, emod_input_files_dir=None):
    if emod_input_files_dir is None:
        emod_input_files_dir = input_dir

    if config is not None:
        with open(os.path.join(input_dir, "config.json"), "w") as fp:
            json.dump(config, fp, indent=4, sort_keys=True)

    command = [emod_executable,
               "-C", os.path.join(input_dir, "config.json"),
               "-I", emod_input_files_dir,
               "-O", os.path.join(input_dir, "output")
               ]

    with open(os.path.join(input_dir, "stdout.txt"), 'w') as stdout:
        # EMOD standard output will be saved to stdout.txt
        print >>stdout, "Command executed: %s" % command
        print >>stdout
        stdout.flush()
        p = subprocess.Popen(command,
                             cwd=input_dir,
                             stdout=stdout,
                             stderr=stdout,
                             )
    return p

if __name__ == "__main__":
    if len(sys.argv) > 1:
        exe = sys.argv[1]
    else:
        exe = "D:\\bin\\EMOD\\v1.8.1\\Eradication.exe"

    print "retcode: %s" % run_emod(exe,
                                   input_dir=os.getcwd(),
                                   config=None)
