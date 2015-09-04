import tourney_inserter as cti
import sys

def main():
    if len(sys.argv) == 1:
        print("Usage: chessil_tourney_inserter.py *tournament name*")
        exit()
    cti.main();
    
if __name__ == "__main__":
    main()