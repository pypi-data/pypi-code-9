import argparse
from file_parser import FileParser

class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
                      description="enables student entrance to a given room")


def main():
    parser = Parser().parser
    parser.add_argument("file_path", help="path to text file to parse student data from")
    parser.add_argument("room_number", type=int, help="target room number")
    args = parser.parse_args()

    file_parser = FileParser(args.file_path)
    file_parser.create_room_auth_file(args.room_number)
    if file_parser.found_errors:
        print("Parsing errors in input file, see errors.log for further details")


if __name__ == '__main__':
    main()
