import argparse
import sys
import prang


def prang_command():
    parser = argparse.ArgumentParser(
        description='Validate and XML document against a RELAX NG schema.')
    parser.add_argument(
        'schema_file', type=open, help='a RELAX NG XML schema file')
    parser.add_argument(
        'xml_file', type=open, help='the XML file to validate')

    args = parser.parse_args()
    try:
        schema = prang.Schema(schema_file=args.schema_file)
        schema.validate(doc_file=args.xml_file)
    except prang.PrangException as e:
        print(e)
        sys.exit(1)
