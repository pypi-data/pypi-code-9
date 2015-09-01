import argparse
from .core import generate_files, install_dependencies, PackageManifestException

def generate(package_json_path='jquery.json', dest_path='.'):
    generate_files(package_json_path, dest_path)
    install_dependencies(dest_path)

def main():
    parser = argparse.ArgumentParser(description='Generate Jquery plugin boilerplate')
    parser.add_argument('manifest', help='Jquery package manifest.')
    parser.add_argument('-d', '--dest', default='./', help='Destination plugin folder path.')
    args = parser.parse_args()
    try:
        generate(args.manifest, args.dest)
    except OSError as osex:
        print (osex)
    except PackageManifestException as pmex:
        print (pmex)

if __name__ == '__main__':
    main()