from __future__ import print_function


__author__ = 'Loris Mularoni'


# Import modules
import logging
import sys
from . import utils
from . import cli
from multiprocessing import Pool


def save(results, output_file, flanks):
    """Write the result to the output file.
    :param results:
    :param output_file:
    :param flanks:
    :return:
    """
    header = ["CHROMOSOME", "START", "END", "SEED", "MICROSATELLITE"]
    if flanks > 0:
        header += ['SEQUENCE_UPSTREAM', 'SEQUENCE_DOWNSTREAM']
    with open(output_file, 'w') as out:
        out.write("{}\n".format("\t".join(header)))
        for chromosome in results:
            for line in chromosome:
                #out.write("{}\t{}\t{}\t{}\t{}\n".format(*line))
                out.write("{}\n".format("\t".join([str(i) for i in line])))


def report(results, flanks):
    """Write the result to the standard output.
    :param results:
    :param flanks:
    :return:
    """
    header = ["CHROMOSOME", "START", "END", "SEED", "MICROSATELLITE"]
    if flanks > 0:
        header += ['SEQUENCE_UPSTREAM', 'SEQUENCE_DOWNSTREAM']
    sys.stdout.write("{}\n".format("\t".join(header)))
    for chromosome in results:
        for line in chromosome:
            sys.stdout.write("{}\n".format("\t".join([str(i) for i in line])))


def run(fasta_file, length, min_repetitions, alphabet, cores,
        imperfect, strict, flanks, progress=False):
    """Start the search of microsatellites.
    :param fasta_file:
    :param length:
    :param min_repetitions:
    :param alphabet:
    :param cores:
    :param imperfect:
    :param strict:
    :param flanks:
    :param progress:
    :return:
    """
    if progress:
        logging.info('Calculating the size of the genome')
        total = utils.get_number_of_chromosomes(fasta_file)
        # Initialize the progress bar
        _progress = utils.ProgressBar(total)

    # Create an instance of the class Microsatellite
    micro = utils.Microsatellite(length, min_repetitions, imperfect,
                                 strict, flanks, alphabet=alphabet)

    results = []
    with Pool(cores) as p:
        for matches in p.imap(micro.find_microsatellites, utils.read_fasta(fasta_file)):
            results.append(matches)
            # Update the progress bar
            if progress:
                _progress.update()

    # Close the progress bar
    if progress:
        _progress.close()

    return results


def main():
    """Execute the program"""
    # Configure the logger
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    # Check if the python version is 3
    if not utils.PYTHON_3:
        logging.error('Invalid version of Python.')
        sys.exit()

    # Read the command line argument
    args = cli.run()

    # Search for the microsatellites
    results = run(fasta_file=args.input_fasta,
                  length=args.length,
                  min_repetitions=args.min_repetitions,
                  alphabet=args.alphabet,
                  imperfect=args.imperfect,
                  strict=args.strict,
                  flanks=args.flanks,
                  cores=args.cores,
                  progress=args.progress)

    # Save or print the results to the output file
    if args.output_file is not None:
        save(results, args.output_file, args.flanks)
    else:
        report(results, args.flanks)


if __name__ == '__main__':
    main()
