#!/usr/bin/env python3
# kate: word-wrap-column 80; word-wrap off;
"""
Print a report about a SAM/BAM file.
"""
__author__ = 'Marcel Martin'

import sys
from collections import Counter, namedtuple, defaultdict
from itertools import islice
from contextlib import ExitStack
from pysam import Samfile
from sqt import HelpfulArgumentParser, Cigar, cigar


Subalignment = namedtuple("Subalignment", ['length', 'pos', 'tid'])

class SupplementaryAlignment(namedtuple("SupplementaryAlignment",
	['rname', 'pos', 'strand', 'cigar', 'mapq', 'edit_distance'])):
	# TODO cigar attribute should be a Cigar object
	@property
	def reference_name(self):
		return self.rname

	@property
	def qstart(self):  # TODO rename to query_start
		return soft_clipping_length(self.cigar, 0)

	@property
	def qend(self):   # TODO rename to query_end
		return soft_clipping_length(self.cigar, 0) + cigar.aligned_bases(self.cigar)

	@property
	def qlength(self):
		return cigar.aligned_bases(self.cigar)

	@property
	def rstop(self):
		return self.pos + Cigar(self.cigar).reference_length()


def header(s):
	print(s)
	print('-' * len(s))
	print()


def soft_clipping_length(cig, where):
	"""
	Return length of soft-clipping at the ends of an alignment.

	where -- 0 stands for the beginning of alignment, -1 for the end.
	"""
	assert where in (0, -1)
	if not cig:
		return 0
	p = cig[where]
	if p[0] == cigar.S:
		return p[1]
	return 0



class AlignedRead:
	"""
	An AlignedRead describes all alignments that exist for a single read in a
	SAM/BAM file. Thus, it also includes all supplementary alignments (if they
	exist).
	"""
	def __init__(self, read, reference_name):
		"""
		The given read should be an AlignedSegment. The SA tag of the read is
		parsed.
		"""
		assert not read.is_secondary, "Read should not be secondary"
		assert not read.is_supplementary, "Read should not be supplementary"
		self.alignments = extract_supplementary_alignments(read, reference_name)
		self.query_name = read.query_name
		self._primary_read = read
		self._length = Cigar(read.cigar).query_length(count_clipped='hard')
		assert self._length == Cigar(read.cigar).query_length(count_clipped='soft'), "Shouldn't be hard-clipped"

	def __len__(self):
		return self._length

	def overall_aligned_bases(self):
		return overall_aligned_bases(self._primary_read, self.alignments)


def parse_supplementary(sa):
	"""
	Parse supplementary alignments given by the SA:Z: tag in a SAM record.

	Return a list of SupplementaryAlignment objects.
	"""
	fields = sa.split(';')
	assert fields[-1] == ''  # sa must end with a ';'
	alignments = []
	for field in fields[:-1]:
		ref, pos, strand, cig, mapq, edit_dist = field.split(',')
		pos = int(pos) - 1
		cig = Cigar.parse(cig)  # TODO should be Cigar(cig)
		mapq = int(mapq)
		edit_dist = int(edit_dist)
		assert strand in '+-'
		a = SupplementaryAlignment(ref, pos, strand, cig, mapq, edit_dist)
		alignments.append(a)
	return alignments


def extract_supplementary_alignments(read, rname):
	"""
	Given a single read that potentially has supplementary alignments specified
	by the SA tag, return a list of SupplementaryAlignment objects. The list
	includes at least the read itself.
	"""
	tags = dict(read.tags)
	alignments = [SupplementaryAlignment(rname, read.pos, '+-'[int(read.is_reverse)],
		read.cigar, read.mapq, tags['NM'])]
	if 'SA' in tags:
		alignments.extend(parse_supplementary(tags['SA']))
	return alignments


def print_coverage_report(aligned_read, report, minimum_cover_fraction=0.01):
	"""
	Print coverage report for a single read to the file-like object 'report'.
	"""
	read_length = len(aligned_read)
	alignments = aligned_read.alignments
	print('Read {} ({:.1f}kbp):'.format(aligned_read.query_name, read_length / 1000), file=report)
	for alignment in sorted(alignments, key=lambda a: (a.qstart, a.qend)):
		cigar = Cigar(alignment.cigar)
		alignment_length = cigar.query_length(count_clipped=None)
		if alignment_length / read_length < minimum_cover_fraction:
			continue
		print(
			'{:9} bp'.format(alignment_length),
			'{:6.1%}'.format(alignment_length / read_length),
			'{:6} ... {:6}  '.format(alignment.qstart+1, alignment.qend),
			'{} {:>2}:{}-{}'.format(alignment.strand,
				alignment.rname, alignment.pos+1, alignment.rstop),
			file=report)
	bases = aligned_read.overall_aligned_bases()
	print('{:.1%} aligned ({}/{})\n'.format(bases / read_length,
		bases, read_length),
		file=report)


def overall_aligned_bases(read, alignments):
	"""
	Given an AlignedRead and its corresponding list of SupplementaryAlignment
	objects, return how many of its bases are aligned,
	considering all supplementary alignments.
	"""
	events = []
	for alignment in alignments:
		events.append((alignment.qstart, 'start', None))
		events.append((alignment.qend, 'stop', alignment))

	depth = 0  # number of observed 'start' events
	bases = 0  # number of covered bases
	last_qstart = None
	for qpos, what, alignment in sorted(events, key=lambda x: x[0]):
		if what == 'start':
			if depth == 0:
				last_qstart = qpos
			depth += 1
		elif what == 'stop':
			depth -= 1
			if depth == 0:
				# interval (last_qstart, qpos) was covered
				bases += qpos - last_qstart
	return bases


def print_basics(aligned_reads, aligned_bases):
	header('Basic statistics')
	bases = sum(len(aligned_read) for aligned_read in aligned_reads)
	total_reads = len(aligned_reads)
	total_alignments = sum(len(aligned_read.alignments) for aligned_read in aligned_reads)
	print('Number of reads:     {:10,d}'.format(total_reads))
	#print('unfiltered+CIGAR:    {:10,d} ({:.2%})'.format(mapped_reads, mapped_reads / total_reads))
	print('Alignments per read: {:.3f} (only mapped reads)'.format(total_alignments / total_reads))  # TODO is this correct?
	print('bases:         {:15,d} ({:.2f} Gbp)'.format(bases, bases / 1E9))
	print('aligned bases: {:15,d} ({:.2f} Gbp) ({:.2%})'.format(aligned_bases, aligned_bases/1E9, aligned_bases/bases))
	print()


def print_subalignment_histogram(number_alignments):
	print('Histogram of number of subalignments')
	rest = 0
	for number, count in number_alignments.items():
		if number <= 10:
			print(' {:2} {:9}'.format(number, count))
		else:
			rest += count
	if rest > 0:
		print('>10 {:9}'.format(rest))
	print()


def print_subalignment_stats(aligned_reads, total_reads):
	header('Subalignment statistics')
	fully_aligned_95 = 0  # reads whose bases are 95% aligned within one subalignment
	fully_aligned_99 = 0  # reads whose bases are 99% aligned within one subalignment
	number_alignments = Counter()
	interesting = 0
	for aligned_read in aligned_reads:
		alignments = aligned_read.alignments
		lengths = sorted(alignment.qlength for alignment in alignments)
		refnames = set(alignment.reference_name for alignment in alignments)

		if len(lengths) >= 1 and lengths[-1] >= 0.95 * len(aligned_read):
			fully_aligned_95 += 1
		if len(lengths) >= 1 and lengths[-1] >= 0.99 * len(aligned_read):
			fully_aligned_99 += 1
		number_alignments[len(lengths)] += 1

		# is this an 'interesting' read? (arbitrary thresholds)
		if 2 <= len(lengths) <= 4 and len(set(refnames)) > 1:
			interesting += 1

	print_subalignment_histogram(number_alignments)
	print('fully aligned (95%):{:10,d} ({:.2%})'.format(fully_aligned_95, fully_aligned_95/total_reads))
	print('fully aligned (99%):{:10,d} ({:.2%})'.format(fully_aligned_99, fully_aligned_99/total_reads))
	print('no of interesting reads:', interesting)
	print()


def print_cigar_usage(counter):
	header("CIGAR operator usage")
	total_ops = sum(counter.values())
	ops = 'MIDNSHPX='
	for op_i, op in enumerate(ops):
		print("{:2} {:14,d} ({:7.2%})".format(op, counter[op_i], counter[op_i]/total_ops))
	print()


def print_reference_usage(reflengths, reference_hits, minimum_reference_length=1000):
	header('Scaffold/chromosome/references usage')

	long_refs = sum(1 for length in reflengths.values() if length >= minimum_reference_length)
	ref_hits_length = sum(reflengths[refname] for refname in reference_hits)
	total_ref_length = sum(reflengths.values())

	print('total length of references: {:,d} ({:.2f} Gbp)'.format(total_ref_length, total_ref_length/1E9))
	print('references:', len(reflengths))
	print('references hit by at least one alignment:', len(reference_hits))
	print('length of those references: {:,d} ({:.2%})'.format(ref_hits_length, ref_hits_length/total_ref_length))
	print('length of references not hit: {:,d}'.format(total_ref_length - ref_hits_length))
	#_refs = infile.references
	#assert infile.nreferences == len(_refs)
	#refname_to_length = dict(zip(_refs, infile.lengths))
	#for i in range(infile.nreferences):
		#assert refname_to_length[infile.getrname(i)] == reflengths[i]

	long_ref_hits = sum(1 for tid in reference_hits if reflengths[tid] >= minimum_reference_length)
	ref_hits_length = sum(reflengths[refname] for refname in reference_hits)
	print('references >= {} bp:'.format(minimum_reference_length), long_refs)
	print('references >= {} bp hit by at least one alignment:'.format(minimum_reference_length), long_ref_hits)


def main():
	parser = HelpfulArgumentParser(description=__doc__)
	parser.add_argument('--quality', '-q', type=int, default=0,
		help='Minimum mapping quality (default: %(default)s')
	parser.add_argument('--minimum-reference-length', metavar='N', type=int, default=0,
		help='For reference usage statistics, ignore references shorter than N.')
	parser.add_argument('--limit', metavar='N', type=int, default=None,
		help='Process only the first N entries in the input file.')
	parser.add_argument('--cover', metavar='FILE', default=None,
		help='Print report about "read coverage" (which sections are aligned) to FILE')
	parser.add_argument('--minimum-cover-fraction', metavar='FRACTION', type=float, default=0.01,
		help='Alignment must cover at least FRACTION of the read to appear in the cover report. (%(default)s)')
	parser.add_argument("bam", metavar="SAM/BAM", help="Name of a SAM or BAM file")
	args = parser.parse_args()

	# Count how often each CIGAR operator occurs
	cigar_counter = Counter()

	n_records = 0
	unmapped = 0
	unmapped_bases = 0
	aligned_reads = []
	with Samfile(args.bam) as sf:
		for record in islice(sf, 0, args.limit):
			n_records += 1
			if record.is_unmapped:
				unmapped += 1
				unmapped_bases += len(record.seq)
				continue
			if record.mapq < args.quality:
				continue
			assert record.cigar is not None
			for op_i, l in record.cigar:
				cigar_counter[op_i] += l

			if not record.is_secondary and not record.is_supplementary:
				aligned_read = AlignedRead(record, sf.getrname(record.tid))
				aligned_reads.append(aligned_read)

		reflengths = sf.lengths
		nreferences = sf.nreferences
		assert nreferences == len(reflengths)
		refnames_map = { tid: sf.getrname(tid) for tid in range(nreferences) }
		reference_lengths = dict(zip(sf.references, sf.lengths))

	total_aligned_bases = 0
	reference_hits = defaultdict(int)
	for aligned_read in aligned_reads:
		total_aligned_bases += aligned_read.overall_aligned_bases()
		for alignment in aligned_read.alignments:
			reference_hits[alignment.reference_name] += 1

	if args.cover is not None:
		with open(args.cover, 'wt') as cover:
			for aligned_read in aligned_reads:
				print_coverage_report(aligned_read, cover, args.minimum_cover_fraction)

	header('All entries in input file')
	print('Total entries:   {:10,d}'.format(n_records))
	print('Unmapped:        {:10,d}'.format(unmapped))
	print('Unmapped bases:  {:10,d}'.format(unmapped_bases))
	print()

	print_basics(aligned_reads, total_aligned_bases)
	print_subalignment_stats(aligned_reads, len(aligned_reads))  # TODO is len(aligned_reads) actually the number of unique reads?
	print_cigar_usage(cigar_counter)
	print_reference_usage(reference_lengths, reference_hits, minimum_reference_length=args.minimum_reference_length)


if __name__ == '__main__':
	main()



"""
Old code that used to be in bamstats:

parser.add_argument('--minimum-start', '-m', type=int, default=1,
	help='minimum start position (1-based). Reads starting earlier are ignored.')
parser.add_argument('--maximum-start', '-M', type=int, default=1E100,
	help='maximum start position (1-based). Reads starting later are ignored.')
parser.add_argument('--forward', action='store_true', default=False,
	help='count only reads mapped forward')


for read in samfile:
	if not (args.minimum_start <= read.pos + 1 <= args.maximum_start):
		continue
	counter[read.rname] += 1

	# TODO should qlen or alen be used?
	# qlen: no. of aligned bases in the read
	# alen: no. of aligned bases in the reference
	coverage[read.rname] += read.qlen
reference_names = samfile.references

for index, name in enumerate(reference_names):
	print(name, counter[index], coverage[index], sep='\t')
"""
