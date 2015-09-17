import argparse
import csv
import logging
import sys
from intogen.parsers.parser.factory import VariantParserFactory
from intogen.parsers.parser.fileformat.variantparser import ParserException

from intogen.tasks.intogen_task import IntogenTask
import os
from intogen.constants.assembly import DEFAULT_INPUT_ASSEMBLY, DEFAULT_OUTPUT_ASSEMBLY
from intogen.constants.qc import ENTITY_VARIANTS
from intogen.constants.data_headers import *
from pyliftover import LiftOver

fieldnames = [CHR, START, STOP, REF, ALT, STRAND, SAMPLE]

_SUPPORTED_EXTENSIONS = [".tab", ".vcf", ".maf"]


class VariantsTask(IntogenTask):

    @staticmethod
    def get_configuration_definitions():
        return {
            'liftover_path': 'dir',
            'mutsig_hg19_path': 'dir'
        }

    def run(self, input_files, output_file, input_assembly=DEFAULT_INPUT_ASSEMBLY, output_assembly=DEFAULT_OUTPUT_ASSEMBLY, skip_indels=False):

        exec_config = self.get_exec_config()

        liftover = None
        if input_assembly != output_assembly:
            liftover_discarded = []
            logging.info("Using liftover from %s to %s", input_assembly, output_assembly)
            liftover = LiftOver(input_assembly, output_assembly, cache_dir=exec_config["liftover_path"])
        else:
            logging.info("Supplied variants already in %s", input_assembly)


        with open(output_file, "w") as output:

            writer = csv.writer(output, delimiter='\t')
            writer.writerow(fieldnames)

            count_match = 0
            count_mismatch = 0

            for input_file in input_files:

                with open(input_file, "r") as input:

                    filename = os.path.splitext(os.path.basename(input_file))
                    if filename[1].lower() in _SUPPORTED_EXTENSIONS:
                        parser_type = filename[1][1:]
                    else:
                        parser_type = "tab"

                    chr_path = exec_config["mutsig_hg19_path"]
                    variant_parser = VariantParserFactory.get(parser_type, input, filename[0], filename[0], chr_path)

                    logging.info("Parsing {} using {}".format(input_file, variant_parser.name))

                    for variant in variant_parser:

                        if skip_indels and (len(variant.ref) > 1 or len(variant.alt) > 1):
                            continue

                        if liftover is not None:

                            results = liftover.convert_coordinate("chr"+variant.chr, variant.start-1, variant.strand)

                            if results is None:
                                logging.warning("Liftover unrecognized chromosome chr%s at '%s'", variant.chr, input_file)
                                liftover_discarded.append(variant_parser._line_num)
                                continue

                            if len(results) == 0:
                                logging.warning("Liftover deleted locus chr%s:%s:%s at '%s'", variant.chr, variant.start, variant.strand, input_file)
                                liftover_discarded.append(variant_parser._line_num)
                                continue

                            if len(results) > 1:
                                logging.warning("Liftover multiple matching coordinates chr%s:%s:%s using first at '%s'", variant.chr, variant.start, variant.strand, input_file)

                            variant.chr = results[0][0].replace("chr", "")
                            variant.start = results[0][1]+1
                            variant.strand = results[0][2]

                        if chr_path is not None and variant_parser.is_reference_match(variant, logging):
                            count_match += 1
                        else:
                            count_mismatch += 1

                        variant.compute_end()

                        writer.writerow([
                            variant.chr,
                            variant.start, variant.end, variant.ref, variant.alt,
                            variant.strand,
                            variant.samples[0].name
                        ])

                    self.quality_control(ENTITY_VARIANTS, "variant_parser-discard", len(variant_parser.discarded_lines()), lines=variant_parser.discarded_lines())

                    if liftover is not None:
                        self.quality_control(ENTITY_VARIANTS, "liftover-discard", len(liftover_discarded), lines=liftover_discarded)

            total_variants = count_mismatch + count_match
            if total_variants > 0:
                match_ratio = count_match / total_variants
                if match_ratio < 0.9:

                    logging.warning("Important mismatch ratio with the reference genome {}/{} = {}".format(
                        count_match, count_mismatch + count_match, match_ratio)
                    )

                self.quality_control(ENTITY_VARIANTS, "reference_genome_match_ratio", match_ratio,
                          count_match=count_match,
                          count_mismatch=count_mismatch
                )


def cmdline():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='append', dest='input_files', default=[])
    parser.add_argument('-o', dest='output_file')
    parser.add_argument('--input_assembly', dest='input_assembly', default=DEFAULT_INPUT_ASSEMBLY)
    parser.add_argument('--output_assembly', dest='output_assembly', default=DEFAULT_OUTPUT_ASSEMBLY)
    parser.add_argument('--skip_indels', dest='skip_indels', default=False, action="store_true")
    options = parser.parse_args()

    # Run the command lin
    task = VariantsTask()

    try:
        task.run(
            options.input_files,
            options.output_file,
            input_assembly=options.input_assembly,
            output_assembly=options.output_assembly,
            skip_indels=options.skip_indels
        )
    except ParserException as e:
        logging.error(e)
        sys.exit(-1)


if __name__ == "__main__":
    cmdline()