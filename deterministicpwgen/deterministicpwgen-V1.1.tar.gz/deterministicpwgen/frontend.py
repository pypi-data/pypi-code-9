"""This module handles the frontend aspects of deterministicpwgen -- the
things such as prompting the user, handling command line arguments, etc.
"""

from argparse import ArgumentParser
import getpass
import string

# deterministicpwgen imports.  
import backend
import config

def setup_charset(choice):
    """Sets up the charset based upon the user-given charset flags."""
    global charset
    charset = ""

    chars = {
        "A" : string.printable.strip(),
        "b" : "10",
        "l" : string.lowercase,
        "n" : string.digits,
        "o" : string.octdigits,
        "p" : string.punctuation,
        "u" : string.uppercase,
        "w" : " ",
        "x" : string.hexdigits,
    }

    for ch in set(choice):
        try:
            charset += chars[ch]
        except KeyError:
            # This will be reached when we encounter a bogus option.  
            print "Invalid charset flag %s -- ignoring it." % ch

    if not charset:
        # If all flags given were bogus, use chars["A"] as default.  
        charset = chars["A"]

def get_integer_input(prompt):
	"""Enforces integer input."""
	n = 0
	while 1:
		try:
			n = int(raw_input(prompt))
			break
		except ValueError:
			print "Enter an integer value."
			continue
	return n

def get_keyfile(choice):
    """Loads the keyfile data according to choice."""
    global keyfile_data

    if choice not in ("yes", "prompt"):
        keyfile_data = ""
        return

    if not backend.keyfile_exists():
        print "You don't currently have a keyfile."
        print "deterministicpwgen can create a keyfile for you."
        print "Keyfiles make the generator more secure, but less convenient."
        
        i = raw_input("Would you like to create a keyfile? <y/N> ").lower()
        if i.startswith("y"):
            print "\n",
            size = get_integer_input("Keyfile size (bytes): ")
            backend.create_keyfile(size=size)
        else:
            keyfile_data = ""
            print "\n",
            return

    if choice == "prompt":
        i = raw_input("Use your keyfile? <Y/n> ")
        if not i.startswith("n"):
            choice = "yes"
        else:
            keyfile_data = ""
            return

    if choice == "yes":
        keyfile_data = backend.load_keyfile_seed()
    else:
        print "\n",

def get_password(choice):
    """Assigns the user passwords according to choice."""
    global password

    if choice == "prompt":
        i = raw_input("Use a password? <Y/n> ").lower()
        if not i.startswith("n"):
            choice = "yes"

    if choice == "yes":
        password = backend.stretch_key(getpass.getpass("Password: "))
        print "\n",
    else:
        # We will reach this point if the user has chosen not to use
        # a password or if input was bogus -- so, assign password to
        # an empty string.  
        password = ""

def init():
    """Prepares deterministicpwgen for generating passwords."""

    if not config.config_file_exists():
        config.create_config_file()

    ap = ArgumentParser(description="Generate passwords with a seed.")

    ap.add_argument("--charset", "-c", default=config.read("charset"),
                    help="Define a custom charset for the generator.")
    ap.add_argument("--hide-seed", "-s", action="store_true",
                    default=bool(config.read("hide-seed")),
                    help="Hide the seed when it's being typed.")
    ap.add_argument("--length", "-l", default=config.read("length"), type=int,
                    help="The length of the generated password.") 

    ap.add_argument("--keyfile", "-k", default=config.read("keyfile"),
                    help="Use a keyfile?")
    ap.add_argument("--password", "-p", default=config.read("password"),
                    help="Use a password?")

    args = ap.parse_args()
    
    print "\n",

    # Perform various setup tasks.  
    setup_charset(args.charset)
    global hide_seed; hide_seed = args.hide_seed
    global length;    length = args.length
    get_keyfile(args.keyfile)
    get_password(args.password)

def begin_generating():
    """Allow the user to input the final component to their seed and
    generate a password using the backend.
    """
    global charset, hide_seed, length
    global keyfile_data, password

    inp = getpass.getpass if hide_seed else raw_input
    while 1:
        seed = inp("Seed: ")
        print backend.generate(password + keyfile_data + seed, length, charset)

def main():
    try:
        init()
        begin_generating()
    except (EOFError, KeyboardInterrupt):
        print "\nInterrupt caught; have a nice day!"
        exit(0)

if __name__ == "__main__":
	main()
