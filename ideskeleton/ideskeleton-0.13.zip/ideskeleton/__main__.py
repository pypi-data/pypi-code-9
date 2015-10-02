"""Build IDE required files from python folder structure from command line.
"""
import argparse
from ideskeleton import build

def main():
    """Build IDE files from python folder structure."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "source_path",
        help="path of the folder structure used to generate the IDE skeleton",
        type=str)
    parser.add_argument(
        "-f",
        "--force",
        help="force overwrite existing solution and project files",
        action="store_true")
    parser.add_argument(
        "-i",
        "--ide",
        help="choose IDE",
        type=str,
        choices=["vstudio"])

    args = parser.parse_args()

    if not args.ide:
        args.ide = "vstudio"

    build(args.source_path, args.force, args.ide)

main()


