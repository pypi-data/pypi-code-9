#!/usr/bin/env python3
"""
Print and optionally plot a read length histogram of one or more FASTA or FASTQ
files. If more than one file is given, a total is also printed.
"""
import sys
from collections import Counter
from sqt import SequenceReader, HelpfulArgumentParser

# Make potential import failures happen before we read in files
import matplotlib as mpl
mpl.use('pdf')  # enable matplotlib over an ssh connection without X
import matplotlib.pyplot as plt
import numpy as np

__author__ = "Marcel Martin"


def length_histogram(path):
	"""Return a list of lengths """
	lengths = []
	with SequenceReader(path) as reader:
		for record in reader:
			lengths.append(len(record.sequence))
	return lengths


def plot_histogram(lengths, path, title, max_y=None):
	"""Plot histogram of lengths to path"""
	lengths = np.array(lengths)
	histomax = int(np.percentile(lengths, 99.9) * 1.01)
	larger = sum(lengths > histomax)

	fig = plt.figure(figsize=(40/2.54, 20/2.54))
	ax = fig.gca()
	ax.set_xlabel('Read length')
	ax.set_ylabel('Frequency')
	ax.set_title(title)
	_, borders, _ = ax.hist(lengths, bins=100, range=(0, histomax))
	w = borders[1] - borders[0]
	ax.bar([histomax], [larger], width=w, color='red')
	ax.set_xlim(0, histomax + 1.5 * w)
	if max_y is not None:
		ax.set_ylim(0, max_y)
	fig.savefig(path)


def get_argument_parser():
	parser = HelpfulArgumentParser(description=__doc__)
	add = parser.add_argument
	add('--plot', default=None, help='Plot to this file (.pdf or .png). '
		'If multiple sequence files given, plot only total.')
	add('--maxy', default=None, type=float, help='Maximum y in plot')
	add('--zero', default=False, action='store_true', help='Print also rows with a count of zero')
	add("--title", default='Read length histogram of {}',
		help="Plot title. {} is replaced with the input file name (default: '%(default)s')")
	add('seqfiles', nargs='+', metavar='FASTA/FASTQ',
		help='Input FASTA/FASTQ file(s) (may be gzipped).')
	return parser


def main():
	parser = get_argument_parser()
	args = parser.parse_args()
	overall_lengths = []
	for path in args.seqfiles:
		print("## File:", path)
		print("length", "frequency", sep='\t')
		lengths = length_histogram(path)
		freqs = Counter(lengths)
		for length in range(0, max(freqs) + 1):
			freq = freqs[length]
			if args.zero or freq > 0:
				print(length, freq, sep='\t')
		overall_lengths.extend(lengths)

	if len(args.seqfiles) > 1:
		print("## Total")
		print("length", "frequency", sep='\t')
		freqs = Counter(overall_lengths)
		for length in range(0, max(freqs) + 1):
			freq = freqs[length]
			if args.zero or freq > 0:
				print(length, freq, sep='\t')
		title = args.title.format('{} input files'.format(len(args.seqfiles)))
	else:
		title = args.title.format(args.seqfiles[0])
	if args.plot:
		plot_histogram(overall_lengths, args.plot, title, args.maxy)


if __name__ == '__main__':
	main()
