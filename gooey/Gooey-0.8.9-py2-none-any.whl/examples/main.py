from gooey import Gooey, GooeyParser
import csv
import secondary


@Gooey(advanced=True, program_name="Test Code!", default_size=(800, 500), required_cols=2)
def get_gooey_arguments():
    parser = GooeyParser()
    parser.add_argument("--save_location", required=True, widget="DirChooser", help="Choose a location to save the CSV file.")
    parser.add_argument("--file_name", required=True, help="Name the file!")
    parser.add_argument("--width", required=True, help="Width of the images.")
    parser.add_argument("--height", required=True, help="Height of the images.")

    gooey_arguments = parser.parse_args()
    return gooey_arguments


# MAIN PROGRAM
def main(args):
    file_list = secondary.default_dict
    return file_list

# EXECUTE
if __name__ == "__main__":
    arguments = get_gooey_arguments()
    csv_file_list = main(arguments)
    print csv_file_list

