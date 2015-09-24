#!/usr/bin/env python3
"""
Extract all reads from a BAM file that map to a certain location, but try hard
to extract them even if hard clipping is used.

TODO reverse-complementarity is ignored
"""
__author__ = 'Marcel Martin'

import sys
import logging
from pysam import Samfile
from sqt import HelpfulArgumentParser, FastqWriter
from sqt.region import Region
from sqt.reads import AlignedRead
from sqt.cigar import Cigar

logger = logging.getLogger(__name__)

def extract_read(aligned_read, aligned_segment, samfile):
	"""
	Return the primary AlignedSegment (the one that is not hard clipped) for
	the aligned read.
	"""
	def is_hard_clipped(segment):
		cig = Cigar(segment.cigar)
		return cig.hard_clipping_left != 0 or cig.hard_clipping_right != 0

	if not is_hard_clipped(aligned_segment):
		return aligned_segment
	for supplementary in aligned_read:
		refname, pos = supplementary.reference_name, supplementary.pos
		for segment in samfile.fetch(refname, pos, pos+1, multiple_iterators=True):
			if (segment.query_name == aligned_segment.query_name and
					not is_hard_clipped(segment)):
				return segment
	return None


def main():
	logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
	parser = HelpfulArgumentParser(description=__doc__)
	parser.add_argument("--missing-quality", type=int, default=40,
		help='Quality value to use if an entry does not have qualities '
			'(default: %(default)s)')
	parser.add_argument("bam", metavar="SAM/BAM", help="Name of a SAM or BAM file")
	parser.add_argument("region", help="Region")
	args = parser.parse_args()
	missing_quality = chr(args.missing_quality + 33)

	written_reads = set()
	region = Region(args.region)
	not_found = set()
	no_qualities = 0
	indirect = 0
	n_records = 0
	names = set()
	with FastqWriter(sys.stdout) as writer, Samfile(args.bam) as sf:
		for record in sf.fetch(region.reference, region.start, region.stop):
			n_records += 1
			names.add(record.query_name)
			if record.is_unmapped:
				assert False, 'shouldn’t happen'
				continue
			assert record.cigar is not None
			if record.query_name not in written_reads and record.query_name not in not_found:
				aligned_read = AlignedRead(record, sf.getrname(record.tid))
				segment = extract_read(aligned_read, record, sf)
				if segment is None:
					not_found.add(record.query_name)
					continue
				if segment is not record:
					indirect += 1
				assert segment.query_name == record.query_name
				if segment.query_qualities is not None:
					qualities = ''.join(chr(c+33) for c in segment.query_qualities)
				else:
					qualities = missing_quality * len(segment.query_sequence)
					no_qualities += 1
				writer.write(segment.query_name, segment.query_sequence, qualities)
				written_reads.add(record.query_name)
	logger.info('%s unique read names in region', len(names))
	logger.info('%s entries written (%s found indirectly)', len(written_reads), indirect)
	logger.info('%s without qualities', no_qualities)


if __name__ == '__main__':
	main()
