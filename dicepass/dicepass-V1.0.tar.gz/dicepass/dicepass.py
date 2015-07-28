import argparse
import random

DEFAULT_WORDLIST = "/usr/share/dict/american-english"

def main():
    ap = argparse.ArgumentParser("dicepass",
            description="Generate diceware/xkcd style passwords.")

    ap.add_argument("n", type=int,
                help="The number of words to generate.")
    ap.add_argument("--wordlist", "-w", type=argparse.FileType("r"),
                default=DEFAULT_WORDLIST,
                help="A custom wordlist.")

    args = ap.parse_args()
    n = args.n

    r = random.SystemRandom() # uses /dev/urandom
    words = [i.strip() for i in args.wordlist.readlines()]
    print " ".join(r.sample(words, n)).lower()

if __name__ == "__main__":
    main()
