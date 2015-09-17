import argparse
import csv
from intogen import so

from intogen.ma.local import MaLocal
from intogen.tasks.intogen_task import IntogenTask
from intogen.vep.local import VepLocal
from intogen.transfic import TransFIC
from intogen.constants.data_headers import *
from pandas import DataFrame


class FunctionalImpactTask(IntogenTask):

    @staticmethod
    def get_configuration_definitions():
        return {
            "ma_db": "file",
            "transfic_path": "dir",
            "consequence_rankings": "file",
            "perl_path": "string",
            "perl_lib": "string",
            "vep_path": "file",
            "vep_cache": "dir",
            "temporal_dir": "string"
        }

    def run(self, variants_file, output_file):

        exec_config = self.get_exec_config()

        # Read variants file and create a dictionary indexed by variant id.
        all_variants = []
        with open(variants_file, "r") as input_file:
            reader = csv.DictReader(input_file, delimiter='\t')

            for row in reader:
                variant_key = ":".join([row[f] for f in [CHR, START, STRAND, REF, ALT, SAMPLE]])
                all_variants.append((variant_key, row))

        if len(all_variants) == 0:
            raise RuntimeWarning("File '{}' is empyt.".format(variants_file))

        # Create MA service
        ma = MaLocal(exec_config["ma_db"])

        # Create TRANSFIC service
        tfic = TransFIC(data_path=exec_config["transfic_path"])

        consequence_ranking = DataFrame.from_csv(exec_config["consequence_rankings"], sep="\t")

        # Store results
        with open(output_file, "w") as output:
            writer = csv.writer(output, delimiter='\t')

            # Write header
            writer.writerow([
                # Variants
                SAMPLE, CHR, STRAND, START, REF, ALT,

                # VEP
                GENE, TRANSCRIPT, CONSEQUENCE, MOST_SEVERE_CONSEQUENCE, PROTEIN_POS, AA_CHANGE, PROTEIN,

                # MA
                UNIPROT,

                # Transfic
                SIFT_SCORE, SIFT_TRANSFIC, SIFT_CLASS,
                PPH2_SCORE, PPH2_TRANSFIC, PPH2_CLASS,
                MA_SCORE, MA_TRANSFIC, MA_CLASS,

                # Impact
                TRANSCRIPT_IMPACT,
                TRANSCRIPT_IMPACT_CLASS
            ])

            size = len(all_variants)
            step = 100
            start_variant = 0
            end_variant = min(start_variant + step, size)

            # Calculate max_variants at once
            while start_variant < size:

                # Select a variants subset of size 'step'
                variants = all_variants[start_variant:end_variant]
                start_variant += step
                end_variant = min(end_variant + step, size)

                # Create and run VEP
                vep = VepLocal(
                    perl_path=exec_config["perl_path"],
                    lib_path=exec_config["perl_lib"],
                    script_path=exec_config["vep_path"],
                    cache_path=exec_config["vep_cache"],
                    temp_path=exec_config["temporal_dir"]
                )
                vep.load(variants)

                # Iterate Variants
                for variant_key, var in variants:

                    # Get Mutation Assessor
                    uniprot, fi_score = ma.get(var[CHR], var[STRAND], int(var[START]), var[REF], var[ALT])

                    # Get VEP data
                    vep_results = vep.get(variant_key)

                    # Get VEP data
                    for v in vep_results:

                        # Check if the variant is Non-synonymous
                        missense = so.match(v.consequences, so.NON_SYNONYMOUS)
                        oncodrivefm = so.match(v.consequences, so.ONCODRIVEFM)

                        protein_pos = v.protein_pos
                        aa_change = v.aa_change
                        v_fi_score = fi_score
                        v_uniprot = uniprot
                        protein = v.protein

                        # get most sever consequence
                        most_severe = ""
                        try:
                            ranking = consequence_ranking[consequence_ranking[CONSEQUENCE].isin(v.consequences)]
                            most_severe = ranking[CONSEQUENCE].irow(0)
                        except:
                            pass

                        # Run Transfic if the variant is Non-synonymous
                        (
                            tr_impact, prot_change,
                            sift_score, sift_tfic, sift_class, sift_impact,
                            pph2_score, pph2_tfic, pph2_class, pph2_impact,
                            ma_score, ma_tfic, ma_class, ma_impact, coding_region
                        ) = tfic.run(
                            v.gene,
                            v.transcript,
                            v.consequences,
                            protein_pos,
                            aa_change,
                            v.sift,
                            v.polyphen,
                            v_uniprot,
                            v_fi_score
                        )

                        if not missense:
                             sift_tfic, sift_class, sift_impact = None, None, None
                             pph2_tfic, pph2_class, pph2_impact = None, None, None
                             ma_tfic, ma_class, ma_impact = None, None, None

                        # Store results
                        writer.writerow([

                            # Variant results
                            var[SAMPLE],
                            var[CHR], var[STRAND], var[START],
                            var[REF], var[ALT],

                            # VEP results
                            v.gene, v.transcript,
                            ",".join(v.consequences),
                            most_severe,
                            protein_pos,
                            aa_change,
                            protein,

                            # MA results
                            v_uniprot,

                            # TRANSFIC
                            sift_score, sift_tfic, TransFIC.class_name(sift_class),
                            pph2_score, pph2_tfic, TransFIC.class_name(pph2_class),
                            ma_score, ma_tfic, TransFIC.class_name(ma_class),

                            # Impact
                            tr_impact, TransFIC.class_name(tr_impact)
                        ])


def cmdline():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file')
    parser.add_argument('-o', dest='output_file')
    options = parser.parse_args()

    # Run the command line
    task = FunctionalImpactTask()
    task.run(
        options.input_file,
        options.output_file
    )


if __name__ == "__main__":
    cmdline()




