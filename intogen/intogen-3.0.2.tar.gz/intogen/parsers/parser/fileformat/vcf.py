import re
from intogen.parsers.chromosome import parse_chromosome
from intogen.parsers.model import Variant, Sample
from intogen.parsers.parser.fileformat.variantparser import VariantParser


_REF_RE = re.compile(r"^([ACGTN]+)$", re.IGNORECASE)
_ALT_RE = re.compile(r"^([ACGTN]+(?:,[ACGTN]+)*)$", re.IGNORECASE)


class VcfParser(VariantParser):
    name = "VCF"

    def __init__(self, f, fname, default_sample_id, chromosome_path=None):
        VariantParser.__init__(self, f, fname, default_sample_id, chromosome_path)

        self.__format = None

        # Metadata and comments
        line = self._readline()
        while len(line) > 0 and line.startswith("#"):
            if line.startswith("##INDIVIDUAL="):
                self._default_sample_id = line[13:]
            elif line.startswith("##fileformat="):
                self.__format = line[13:]
            line = self._readline()

        if len(line) > 0:  # First line
            self._queue_line(line)

    def __next__(self):
        VariantParser.__next__(self)

        var = None
        while var is None:
            line = self._readline()
            while len(line) > 0 and line.lstrip().startswith("#"):
                if line.startswith("##INDIVIDUAL="):
                    self._default_sample_id = line[13:]
                line = self._readline()

            if len(line) == 0:
                raise StopIteration()

            fields = line.rstrip("\n").split("\t")

            if len(fields) < 5:
                self._discard_line('fields')
                continue

            chr, start, external_id, ref, alt = fields[0:5]

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

            # Check ref and alt
            if _REF_RE.match(ref) is None:
                self._discard_line('ref')
                continue

            if _ALT_RE.match(alt) is None:
                self._discard_line('alt')
                continue

            ref_len = len(ref)

            if "," in alt:
                vtype = None
                s = alt.split(",")
                for allele in s:
                    if ref_len == len(allele):
                        t = Variant.SUBST
                    else:
                        t = Variant.INDEL
                    if vtype is None:
                        vtype = t
                    elif vtype != t:
                        vtype = Variant.COMPLEX
                        break
            else:
                if ref_len == len(alt):
                    vtype = Variant.SUBST
                else:
                    vtype = Variant.INDEL

            var = Variant(type=vtype, chr=chr, start=start, ref=ref, alt=alt, strand="+",
                          samples=[Sample(name=self._default_sample_id)])

        return var

