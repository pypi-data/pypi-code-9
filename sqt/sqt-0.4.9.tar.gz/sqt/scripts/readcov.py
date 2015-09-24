#!/usr/bin/env python3
# kate: word-wrap-column 80; word-wrap off;
"""
Print a report for individual reads in a SAM/BAM file.
"""
__author__ = 'Marcel Martin'

import sys
from collections import Counter, namedtuple, defaultdict
from itertools import islice
from contextlib import ExitStack
from pysam import Samfile
from sqt import HelpfulArgumentParser, Cigar, cigar
from sqt.region import Region

from .bamstats import AlignedRead, print_coverage_report


def main():
	parser = HelpfulArgumentParser(description=__doc__)
	parser.add_argument('--quality', '-q', type=int, default=0,
		help='Minimum mapping quality (default: %(default)s')
	parser.add_argument('--minimum-cover-fraction', metavar='FRACTION', type=float, default=0.01,
		help='Alignment must cover at least FRACTION of the read to appear in the cover report. (%(default)s)')
	parser.add_argument("bam", metavar="SAM/BAM", help="Name of a SAM or BAM file")
	parser.add_argument("region", help="Region")
	args = parser.parse_args()

	region = Region(args.region)
	n_records = 0
	seen_reads = set()
	with Samfile(args.bam) as sf:
		for record in sf.fetch(region.reference, region.start, region.stop):
			n_records += 1
			if record.is_unmapped:
				unmapped += 1
				unmapped_bases += len(record.seq)
				continue
			if record.mapq < args.quality:
				continue
			assert record.cigar is not None

			if not record.query_name in seen_reads:
				aligned_read = AlignedRead(record, sf.getrname(record.tid))
				print_coverage_report(aligned_read, minimum_cover_fraction=args.minimum_cover_fraction)
				seen_reads.add(record.query_name)


if __name__ == '__main__':
	main()
