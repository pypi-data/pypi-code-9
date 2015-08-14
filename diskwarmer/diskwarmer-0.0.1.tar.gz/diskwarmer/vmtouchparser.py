from pyparsing import nums as digits
from pyparsing import alphas, LineStart, LineEnd, Word, Literal, Regex, ZeroOrMore, OnlyOnce
from collections import namedtuple

whole_number = Word(digits)
whole_number_ratio = whole_number + Literal("/") + whole_number

rational_number = Regex("[0-9]+\.[0-9]+")

unit = Regex("[BKMGT]")
unit_ratio = whole_number + unit + Literal("/") + whole_number + unit

file_name = Regex("[^\n\r]+") #TODO IMPROVE THIS

mapped = Regex("[Oo ]*")
mapped_pic = Literal("[") + mapped + Literal("]")

fileline = file_name + LineEnd()
mapline = mapped_pic + whole_number_ratio + LineEnd()
record = fileline + mapline

files_stat     = Literal("Files:") + whole_number + LineEnd()
dirs_stat      = Literal("Directories:") + whole_number + LineEnd()
resident_stat  = Literal("Resident Pages:") + whole_number_ratio + unit_ratio + rational_number + Literal("%") + LineEnd()
elapsed_stat   = Literal("Elapsed:") + rational_number + Literal("seconds") + LineEnd()
all_stats      = files_stat + dirs_stat + resident_stat + elapsed_stat

vmtouch_parser = ZeroOrMore(record) + all_stats

VmtouchRecord = namedtuple('VmtouchRecord', "name,pic,resident,size,ratio".split(','))

def parse(file):
    records = []
    def parseRecord(str, loc, toks):
      parts = {'name':toks[0], 'pic':toks[3], 'resident':int(toks[5]), 'size':int(toks[7])}
      parts['ratio'] = float(parts['resident'])/parts['size']
      record = VmtouchRecord(**parts)
      records.append(record)
    record.setParseAction( parseRecord )
    vmtouch_parser.parseFile(file)
    return records

