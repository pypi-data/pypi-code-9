import re
from intogen.parsers.chromosome import parse_chromosome
from intogen.parsers.model import Variant, Sample
from intogen.parsers.parser.fileformat.variantparser import VariantParser, ParserException, SkipLine
from intogen.parsers.sequence import strand_wizard

_ALLELE_RE = re.compile(r"^(\-|[ACGT]+)$", re.IGNORECASE)

# MAF spec is not clear about heders case and mix it with values case sensitivity
# so I will treat all headers as lower case.

_COL_ALLELE1 = "tumor_seq_allele1"
_COL_ALLELE2 = "tumor_seq_allele2"

_COLUMNS = [
    "chrom",
    "start_position",
    "strand",
    "reference_allele",
    _COL_ALLELE1,
    _COL_ALLELE2,
    "tumor_sample_barcode"]

_COLUMN_SYNONYMOUS = {
    "chromosome": "chrom"
}


class MafParser(VariantParser):
    name = "MAF"

    def __init__(self, f, fname, default_sample_id, chromosome_path=None):
        VariantParser.__init__(self, f, fname, default_sample_id, chromosome_path)

        self.__format = None

        # Metadata and comments
        line = self._readline()
        while len(line) > 0 and line.startswith("#"):
            if line.startswith("##fileformat="):
                self.__format = line[13:]
            line = self._readline()

        if len(line) > 0:  # Header
            column_indices = {}
            columns = line.rstrip().split("\t")
            self._col_size = len(columns)
            for i, name in enumerate(columns):

                # Case insensitive
                name = name.lower()

                # Allow some synonymous
                if name in _COLUMN_SYNONYMOUS:
                    name = _COLUMN_SYNONYMOUS[name]

                # Check if it's a known column header
                if name in _COLUMNS:
                    column_indices[name] = i
            try:
                self._col_name_indices = column_indices
                self._col_indices = [column_indices[name] for name in _COLUMNS]
            except KeyError as ex:
                raise ParserException("Header column not found: {0}".format(ex.args[0]), self._location())
        else:
            raise ParserException("Header not found", (self._fname))

    def __next__(self):
        VariantParser.__next__(self)

        var = None
        while var is None:
            line = self._readline()

            if len(line) == 0:
                raise StopIteration()

            fields = line.rstrip("\n").split("\t")

            chr, start, strand, ref, alt1, alt2, sample = [
                fields[i] if i < self._col_size else None for i in self._col_indices]

            # Chromosome

            chr = parse_chromosome(chr)
            if chr is None:
                self._discard_line('chr')
                continue

            # Start

            try:
                start = int(start)
            except:
                self._discard_line('start-pos')
                continue

            # Ref & alt
            if ref is None or alt1 is None or alt2 is None:
                self._discard_line('allele')
                continue

            try:
                for i, x in enumerate([ref, alt1, alt2]):
                    if _ALLELE_RE.match(x) is None:
                        self._discard_line('nomatch')
                        raise SkipLine()
            except SkipLine:
                continue

            # Strand
            strand = strand_wizard(strand, (chr, start, ref), self._chromosome_path)
            if strand is None:
                strand = '+'
                ## currently maf only accepts '+', so if none, set to plus strand

            alt = alt1

            if ref == "-":
                # [1   2]  -->  [1 2] 3
                #  . - .         N
                #  . T .         N T
                ref = "N"
                alt = "N" + alt if alt != "-" else "N"
            elif alt == "-":
                # 1 [2] 3  -->  [1 2] 3
                # .  T  .        N T
                # .  -  .        N
                start -= 1
                ref = "N" + ref
                alt = "N"

            ref_len = len(ref)

            vtype = Variant.SUBST if ref_len == len(alt) else Variant.INDEL

            if len(sample) == 0:
                sample = self._default_sample_id

            if alt1 != alt2:
                fields[self._col_name_indices[_COL_ALLELE1]] = fields[self._col_name_indices[_COL_ALLELE2]]
                self._queue_line("\t".join(fields))

            if ref == alt:
                continue

            var = Variant(type=vtype, chr=chr, start=start, ref=ref, alt=alt, strand=strand,
                          samples=[Sample(name=sample)])
        return var

