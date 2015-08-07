import argparse
import functools
import logging
import os
import numpy as np
import csv
import re

import bgscripts.utils.loaddata as loaddata
import bgscripts.utils.referencegenome as refgen

from multiprocessing import Pool


def randomize_mutation(regions, window_size, mutations):

    muts = []
    for mut in mutations:
    
        # Mutation signature
        signature = refgen.get_ref_triplet(mut['CHROMOSOME'], mut['POSITION']).upper()

        # Sequence window
        window_start = int(mut['POSITION'] - (window_size / 2))
        window_start = 0 if window_start < 0 else window_start
        sequence = refgen.get_ref(mut['CHROMOSOME'], window_start, size=window_size)

        # Find all positions with the same signature
        positions = [window_start + m.start() + 1 for m in re.finditer(signature, sequence)]
        positions = [p for p in positions if p != mut['POSITION']]

        # Remove positions outside our regions
        if regions is not None:
            positions = [p for p in positions if len(regions[mut['CHROMOSOME']][p]) > 0]

        if len(positions) == 0:
            logging.error("No positions with same signature at {}:{}".format(mut['CHROMOSOME'], mut['POSITION']))
            continue

        if len(positions) < 10:
            logging.warning("Only {} positions with same signature at {}:{}".format(len(positions), mut['CHROMOSOME'], mut['POSITION']))

        # Get a random position
        random_position = np.random.choice(positions, 1)[0]

        mut['POSITION'] = random_position
        muts.append(mut)

    return muts


def randomize_dataset(input_file, output_file, regions=None, cores=1, window_size=50000, quite=False):

    if output_file is None:
        output_file = "{}.rand".format(os.path.basename(input_file))

    # Load regions
    if regions is not None:
        logging.info("Loading regions...")
        regions_tree = loaddata.build_regions_tree(loaddata.load_regions(regions))
    else:
        regions_tree = None

    # Load mutations
    core = 0
    mutations = [list() for core in range(cores)]
    logging.info("Loading mutations...")
    for i, mut in enumerate(loaddata.load_mutations(input_file)):

        # Skip mutations outside our regions
        if regions_tree is not None and len(regions_tree[mut['CHROMOSOME']][mut['POSITION']]) == 0:
            continue

        mutations[core].append(mut)

        # Assign to another core
        core = core+1 if core < cores-1 else 0

    logging.info("Randomizing mutations...")
    with Pool(processes=cores) as pool:
        with open(output_file, 'wt') as fd:
            writer = csv.DictWriter(fd, delimiter='\t', fieldnames=loaddata.MUTATIONS_HEADER)
            writer.writerow({fn: fn for fn in loaddata.MUTATIONS_HEADER})

            randomize_mutation_partial = functools.partial(randomize_mutation, regions_tree, window_size)
            for muts in pool.imap(randomize_mutation_partial, mutations):
                for mut in muts:
                    writer.writerow(mut)

    logging.info("Randomization [done]")


def cmdline():

    # Parse the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", dest="input_file", required=True, help="Input dataset to randomize")
    parser.add_argument("-o", "--output", dest="output_file", default=None, help="Output randomizated dataset")
    parser.add_argument("-r", "--regions", dest="regions", default=None, help="Randomize only mutations in this regions and keep the random positions inside")
    parser.add_argument("--window", dest="window_size", type=int, default=50000, help="Randomization total window size (default 50k), half at each side of the mutation.")
    parser.add_argument("--cores", dest="cores", type=int, default=os.cpu_count(), help="Maximum CPU cores to use (default 1)")
    parser.add_argument('--quite', dest='quite', default=False, action='store_true', help="Hide any progress")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO if not args.quite else logging.ERROR)

    randomize_dataset(args.input_file, args.output_file,
                      regions=args.regions,
                      cores=args.cores,
                      window_size=args.window_size,
                      quite=args.quite)

if __name__ == "__main__":
    cmdline()
