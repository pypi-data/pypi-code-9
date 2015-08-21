from intogen.parsers.sequence import remove_neutral_caps, remove_common, complementary_sequence
from collections import namedtuple

# Sample

SampleBase = namedtuple("Sample", "id, name")


class Sample(SampleBase):
    def __new__(cls, id=None, name=None):
        return super(Sample, cls).__new__(cls, id, name)

# Variant
VariantBase = namedtuple("Variant", """id, type, chr, start, ref, alt, strand, samples, xrefs, extrainfo""")


class Variant(object):
    SUBST = "SUBST"
    INDEL = "INDEL"
    COMPLEX = "COMPLEX"

    def __init__(self, id=None, type=None, chr=None, start=None, ref=None, alt=None, strand=None, samples=None,
                xrefs=None, extrainfo=None):

        self.id = id
        self.type = type
        self.chr = chr
        self.start = start
        self.end = None
        self.ref = ref
        self.alt = alt
        self.strand = strand
        self.samples = samples
        self.xrefs = xrefs
        self.extrainfo = extrainfo

        if self.type is None:
            ref_len = self.seq_length(ref)
            alt_len = self.seq_length(alt)
            if ref_len == alt_len:
                self.type = Variant.SUBST
            else:
                self.type = Variant.INDEL

    @staticmethod
    def seq_length(seq):
        return len(seq.replace("-", "")) if seq is not None else 0

    def compute_end(self, remove_neutral_bases=True, remove_common_bases=True, force_strand=None):

        if remove_neutral_bases:
            self.start, self.ref, self.alt = remove_neutral_caps(self.start, self.ref, self.alt )

        if remove_common_bases:
            self.start, self.ref, self.alt = remove_common(self.start, self.ref, self.alt )

        ref_len = self.seq_length(self.ref)
        alt_len = self.seq_length(self.alt)

        if alt_len > ref_len:  # Insertion
            self.end = self.start
            self.start += 1
        elif alt_len < ref_len:  # Deletion
            self.end = self.start + ref_len - 1
        else:  # Substitution
            self.end = self.start + alt_len - 1

        if ref_len == 0 and self.ref == "":
            self.ref = "-"
        if alt_len == 0 and self.alt == "":
            self.alt = "-"

        if force_strand is not None and force_strand != self.strand:
            self.ref = complementary_sequence(self.ref)
            self.alt = complementary_sequence(self.alt)
