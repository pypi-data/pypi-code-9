import csv
import intogen
import os
import re
import tempfile
import subprocess
from intogen.config import get_config

from .model import VepException, VepResult
from intogen.constants.data_headers import *


_SIFT_POLYPHEN_RE = re.compile(r"^.+\((.+)\)$")


class VepLocal(object):
    def __init__(self, perl_path, lib_path, script_path, cache_path, temp_path):
        self.perl_path = perl_path
        self.lib_path = lib_path
        self.script_path = script_path
        self.cache_path = cache_path
        self.temp_path = temp_path

        self.results_path = None
        self.cmd = None
        self.retcode = None

        self.values = {}

    def run(self, variants_path):
        """
        Run the VEP script and save results in a temporary file.
        :param variants_path: File with variants. In BED format. http://www.ensembl.org/info/docs/variation/vep/vep_script.html#custom_formats
        :return: True if success or False otherwise
        """

        if self.results_path is None:
            self.results_path = intogen.utils.get_temp_file(self.temp_path)[1]

        self.cmd = " ".join([
            self.perl_path,
            self.script_path,
            "-i", variants_path,
            "-o", self.results_path,
            "--no_progress --compress 'gunzip -c'",
            "--force_overwrite --format=ensembl",
            "--cache --offline --dir={0}".format(self.cache_path),
            "--no_intergenic",
            "--protein --sift=b --polyphen=b"])

        self.retcode = subprocess.call(self.cmd, shell=True,
                                       env={"PERL5LIB": self.lib_path, "COLUMNS": "20", "LINES": "10"})

        if self.retcode != 0:
            raise VepException("Error while running VEP:\n{0}".format(self.cmd))

    def results(self):
        """
        Iterator that parses the results temporary file and yields VepResult's
        """

        with open(self.results_path, "r") as f:
            for line in f:
                if line.startswith("#"):
                    continue

                fields = line.rstrip("\n").split("\t")

                var_id, location, allele, gene, feature, feature_type, consequences = fields[0:7]

                if feature_type != "Transcript":
                    continue

                chr, start = location.split(":")

                consequences = sorted(consequences.split(","))

                protein_pos, aa_change = [x if x != "-" else None for x in fields[9:11]]

                extra = fields[13]

                protein, sift, polyphen = (None, None, None)

                if len(extra) > 0:
                    for var in extra.split(";"):
                        key, value = var.split("=")
                        if key == "ENSP":
                            protein = value
                        elif key == "SIFT":
                            m = _SIFT_POLYPHEN_RE.match(value)
                            if m is not None:
                                sift = float(m.group(1))
                        elif key == "PolyPhen":
                            m = _SIFT_POLYPHEN_RE.match(value)
                            if m is not None:
                                polyphen = float(m.group(1))

                yield VepResult(var_id=var_id, chr=chr, start=start, allele=allele,
                                gene=gene, transcript=feature, consequences=consequences,
                                protein_pos=protein_pos, aa_change=aa_change, protein=protein,
                                sift=sift, polyphen=polyphen)

    def close(self):
        """
        Removes temporary files
        """

        if self.results_path is not None:
            os.remove(self.results_path)
            self.results_path = None

    def load(self, variants):

         # Create ENSEMBL file format
        ensembl_file = tempfile.mkstemp()[1]
        with open(ensembl_file, "w") as output:
            writer = csv.writer(output, delimiter='\t')

            for variant_key, values in variants:
                writer.writerow([
                    values[CHR], values[START], values[STOP],
                    values[REF] + '/' + values[ALT],
                    values[STRAND], variant_key
                ])

        self.run(ensembl_file)

        for vep_result in self.results():

            if vep_result.var_id in self.values:
                self.values[vep_result.var_id].append(vep_result)
            else:
                self.values[vep_result.var_id] = [vep_result]

        self.close()

    def get(self, variant_key):
        if variant_key in self.values:
            return self.values.get(variant_key)
        else:
            return []




