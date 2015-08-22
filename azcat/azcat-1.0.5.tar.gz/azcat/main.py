import os
import sys
import chardet
from subprocess import Popen, PIPE, check_output, STDOUT
from azcat.pretty_print import pretty_print

if sys.version_info[0] == 2:
    from __builtin__ import raw_input as input

def load_file (filepath):
    try:
        # detect & convert character encoding
        with open(filepath, "rb") as f:
            data = f.read()

        en = chardet.detect(data[0:1024])["encoding"]
        if en is None:
            s = data.decode("utf-8")
        else:
            s = data.decode(chardet.detect(data[0:1024])["encoding"])
    except IOError as e:
        sys.exit("azcat: cannot open '%s': %s" % (filepath, str(e)))
    except UnicodeDecodeError:
        sys.exit("azcat: file seems a binary file.")

    # confirm if file size is larger than 1MB
    if os.path.getsize(filepath) > 1024*1024:
        if input("file size is big; do you continue? [Y/n]: ") == "n":
            sys.exit()
    return s


def main (args):
    # GNU global
    if args["t"] is not None:
        args["with_pager"] = True
        try:
            output = check_output(["global", "-x", args["t"]]).decode("utf-8")
            if output == "":
                sys.exit("azcat: symbol ``{0}'' not found".format(args["t"]))
            line, file = list(filter(lambda x: x != "", output.split(" ")))[1:3]
            line = int(line)
        except Exception as e:
            sys.exit("azcat: error occurred in global(1)")
    # normal
    else:
        file = args["file"]
        line = 1

    s = load_file(file)
    ext = args.get("f")
    if ext == None:
        ext = os.path.splitext(file)[1][1:]

    if args["with_pager"]:
        p = Popen(["less", "-R", "+{0}g".format(line)], stdin=PIPE)
        try:
            pretty_print(file, s, p.stdin, args["with_formatter"], ext=ext)
            p.stdin = sys.stdin
            p.wait()
        except IOError: # this will raised after the pager existed
            pass
    else:
        pretty_print(file, s, sys.stdout.buffer,
                     args["with_formatter"], ext=ext)
