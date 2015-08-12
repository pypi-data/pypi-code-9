from intogen.parsers.parser.fileformat.maf import MafParser
from intogen.parsers.parser.fileformat.tab import TabParser
from intogen.parsers.parser.fileformat.vcf import VcfParser

_PARSERS = {
    "tab": TabParser,
    "vcf": VcfParser,
    "maf": MafParser
}


class VariantParserFactory:
    def __init__(self):
        pass

    @staticmethod
    def get(parser_type, f, fname, default_sample_id, chromsome_path=None):
        if parser_type not in _PARSERS:
            raise Exception("Unknown mutations parser type: {0}".format(parser_type))

        return _PARSERS[parser_type](f, fname, default_sample_id, chromsome_path)