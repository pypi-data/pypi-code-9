import argparse
import sys
import bgconvert

MAP_FUNCTIONS = {
    ('ensembl', 'symbol'): bgconvert.ensembl_to_symbol,
    ('symbol', 'ensembl'): bgconvert.symbol_to_ensembl
}


def run():

    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='from_map', required=True, help='Input format (symbol, ensembl)')
    parser.add_argument('--to', dest='to_map', required=True, help='Output format (symbol, ensembl)')
    args = parser.parse_args()

    key = (args.from_map, args.to_map)
    if key not in MAP_FUNCTIONS:
        raise RuntimeError("Unknown mapping from '{}' to '{}'".format(args.from_map, args.to_map))

    for line in sys.stdin:
        print(MAP_FUNCTIONS[key](line))


if __name__ == "__main__":
    run()