#! /usr/bin/env python

"""Utilities for FASTR related functions"""

__version__ = '0.0.0.3'


def compress_fastr(sequence):
    """Eliminates repeats in a sequence and returns a string"""

    compressed_sequence = []
    if type(sequence) == str:
        sequence = sequence.split('-')
    last_read = None
    read_repeats = 0
    for read in enumerate(sequence):
        if read[1] == last_read:
            read_repeats += 1
        else:
            if read_repeats != 0:
                compressed_sequence.append(
                    '{0}x{1}'.format(str(read_repeats + 1), str(last_read)))
                read_repeats = 0
            elif read[0] != 0:
                compressed_sequence.append(str(last_read))
            last_read = read[1]
        if read[0] + 1 == len(sequence):
            if read_repeats != 0:
                compressed_sequence.append(
                    '{0}x{1}'.format(str(read_repeats + 1), str(last_read)))
            else:
                compressed_sequence.append(str(last_read))
            compressed_sequence = '-'.join(compressed_sequence)
    return compressed_sequence


def decompress_fastr(sequence):
    """Returns decompressed FASTR sequence"""

    depth_sequence = sequence.split('-')
    decompressed_sequence = []
    for base in depth_sequence:
        try:
            int(base)
            decompressed_sequence.append(int(base))
        except ValueError:
            sep = base.split('x')
            sep[1] = sep[1].rstrip('\n')
            decompressed_sequence += [int(sep[1]) for i in range(int(sep[0]))]
    decompressed_sequence = '-'.join([str(i) for i in decompressed_sequence])
    return decompressed_sequence


def write_fastr(sequence_ids, sequences, fastr_handle):
    """Writes the list of sequence ids and sequences to a FASTR file"""

    for sequence_id, sequence in zip(sequence_ids, sequences):
        fastr_entry = '+{0}\n{1}\n'.format(sequence_id, sequence)
        fastr_handle.write(fastr_entry)
