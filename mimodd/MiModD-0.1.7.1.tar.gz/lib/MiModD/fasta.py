import hashlib
from .iterx import SepIter

from . import FormatParseError

ILLEGAL_ID_CHARS = set('<>[]*;=,')


def is_valid_char (c):
    return 32 < ord(c) < 127 and c not in ILLEGAL_ID_CHARS


def is_valid_id (identifier):
    return all(32 < ord(c) < 127 and c not in ILLEGAL_ID_CHARS
               for c in identifier)


def assert_valid_ids (identifiers):
    for title in identifiers:
        if not is_valid_id(title):
            raise FormatParseError(
                'Invalid reference genome file {token}: Some sequence names contain characters that are not allowed in MiModD.',
                token='', # to be filled in by caller
                help='Whitespace, non-printable characters and any of the characters "{0}" are disallowed in sequence names.\nYou may manually clean up the file or run "python3 -m MiModD.sanitize" to replace invalid characters automatically.'
                     .format(''.join(sorted(ILLEGAL_ID_CHARS)))
                )
    

def sanitize_id (identifier, replacement_str = None):
    amended_chars = []
    for c in identifier:
        if is_valid_char(c):
            amended_chars.append(c)
        elif replacement_str:
            # a fixed replacement string has been specified
            # => use it to replace any invalid character
            amended_chars.append(replacement_str)
        else:
            # use the capitalized percent encoding of invalid characters
            amended_chars.append('%')
            amended_chars.append(hex(ord(c))[2:].upper().zfill(2))
    return ''.join(amended_chars)


class FastaReader (SepIter):

    RECORD_SEP = '>'
    
    def __init__ (self, iterable):
        self.super = super(FastaReader, self) # set this for fast access by next()
        self.super.__init__(iterable, self.RECORD_SEP)
        
    def identifiers (self):
        for header, seq_iter in self:
            yield header
            
    def sequences (self):
        for header, seq_iter in self:
            yield (header, ''.join(s.strip() for s in seq_iter))

    def md5sums (self):
        for header, seq_iter in self:
            md5 = hashlib.md5()
            for seqline in seq_iter:
                md5.update(seqline.strip().upper().encode())
            yield (header, md5.hexdigest())


def get_fasta_info (ifile):
    dna_strings = 'ACGTNKSYMWRBDHV'
    dna_strings += dna_strings.lower()
    IUPAC_DNA_codes = set(dna_strings)

    seqinfo = []
    with open(ifile, 'r') as ifo:
        for header, seq_iter in FastaReader(ifo):
            if header is None:
                raise RuntimeError('Expected ">" at start of file')
            seqlen = 0
            md5 = hashlib.md5()
            for seqline in seq_iter:
                seqline = seqline.strip().upper()
                if any(c not in IUPAC_DNA_codes for c in seqline):
                    raise RuntimeError('Invalid nucleotide code in sequence ' + header)
                seqlen += len(seqline)
                md5.update(seqline.encode())
            if seqlen == 0:
                raise RuntimeError('No nucleotide information found for sequence ' + header)
            seqinfo.append({'SN': header, 'LN': seqlen, 'M5': md5.hexdigest()})
    return seqinfo
