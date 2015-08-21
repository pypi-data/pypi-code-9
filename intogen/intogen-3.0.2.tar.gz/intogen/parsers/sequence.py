import os

__CB = {
    "A": "T",
    "T": "A",
    "G": "C",
    "C": "G"
}


def neutral_head_length(ref, alt):
    """
    returns index of first non-N(eutral) nucleotide
    :param ref: e.g NNNNA
    :param alt: e.g NNNNG
    :return:
    """
    i = 0
    while i < len(ref) and ref[i] == "N" and i < len(alt) and alt[i] == "N":
        i += 1
    return i


def neutral_tail_length(ref, alt):
    """
    returns index of last non-N(eutral) nucleotide
    :param ref:
    :param alt:
    :return:
    """
    i = len(ref) - 1
    j = len(alt) - 1
    while i >= 0 and ref[i] == "N" and j >= 0 and alt[j] == "N":
        i -= 1
        j -= 1
    return len(ref) - i - 1


def remove_neutral_caps(start, ref, alt):
    """
    Removes the part of the variant where the nucleotides are set to N (instead of A,C,G or T)
    :param start:
    :param ref:
    :param alt:
    :return:
    """
    head_len = neutral_head_length(ref, alt)
    ins_correction = 1 if len(ref) < len(alt) else 0
    start += max(0, head_len - ins_correction)
    alt = alt[head_len:]
    ref = ref[head_len:]

    tail_len = neutral_tail_length(ref, alt)
    if tail_len > 0:
        alt = alt[:-tail_len]
        ref = ref[:-tail_len]

    return start, ref, alt


def prefix_length(ref, alt):
    i = 0
    while i < len(ref) and i < len(alt) and ref[i] == alt[i]:
        i += 1
    return i


def suffix_length(ref, alt):
    i = len(ref) - 1
    j = len(alt) - 1
    while i >= 0 and j >= 0 and ref[i] == alt[j]:
        i -= 1
        j -= 1
    return len(ref) - i - 1


def remove_common(start, ref, alt):
    """
    Removes the bases that are repeated in both ref and alt and are therefore NOT variants
    :param start:
    :param ref:
    :param alt:
    :return:
    """
    prefix_len = prefix_length(ref, alt)
    ins_correction = 1 if len(ref) < len(alt) else 0
    start += max(0, prefix_len - ins_correction)
    alt = alt[prefix_len:]
    ref = ref[prefix_len:]

    suffix_len = suffix_length(ref, alt)
    if suffix_len > 0:
        alt = alt[:-suffix_len]
        ref = ref[:-suffix_len]

    return start, ref, alt


def complementary_sequence(seq):
    """
    returns the complementary sequence of given
    :param seq:
    :return:
    """
    return "".join([__CB[base] if base in __CB else base for base in seq.upper()])


def get_base(chr, start, chr_path=None):

    if chr_path is None:
        return None

    with open(os.path.join(chr_path, "chr{0}.txt".format(chr)), 'rb') as fd:
        fd.seek(start-1)
        return fd.read(1).decode().upper()


def strand_wizard(strand, variant=None, chr_path=None):
    """
    Tries to guess correct strand if strand data is missing
    :param strand:
    :param variant:
    :param chr_path:
    :return:
    """
    if strand == "1" or strand == "+1":
        return "+"
    elif strand == "-1":
        return "-"
    elif len(strand) == 0:
        if variant is None or chr_path is None:
            return None
        else:

            # Try to deduce from genome reference
            chr, start, ref = variant
            newbase = get_base(chr, start)

            if ref == newbase:
                return '+'
            if complementary_sequence(ref) == newbase:
                return '-'
            else:
                return None

    elif strand not in ["+", "-"]:
        return None

    return strand
