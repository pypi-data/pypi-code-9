__version__ = '0.4.9'

from .args import HelpfulArgumentParser
from .io.fasta import (
	SequenceReader, FastaReader, FastqReader, FastaWriter, FastqWriter,
	IndexedFasta, guess_quality_base )
from .io.gtf import GtfReader
from .io.xopen import xopen
from .cigar import Cigar

#from .align import multialign, consensus
