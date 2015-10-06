import glob
import os
import re

import requests
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio.SeqIO import SeqRecord
from Bio import SeqIO

from .utils import is_fasta


class PrimerDesigner:
    """Class for designing primers from FASTA files.

    It will send a FASTA alignment to `primers4clades`_ in order to design
    degenerate primers. Input data needed is an alignment in FASTA format
    containing at least 4 sequences.
    It is recommended that the beginning of each FASTA sequence description
    contains the taxon name between square brackets.

    Parameters:
        folder (str):         path of folder containing the FASTA file alignments
        tm (str):             temperature
        min_amplength (str):  minimum amplicon length
        max_amplength (str):  maximum amplicon length
        gencode (str):        genetic code. See below for all available genetic
                              codes
        clustype (str):       cluster distance metric: ``dna``, ``protein``.
        amptype (str):        substitution model used to estimate phylogenetic
                              information
        email (str):          your email address so that primer4clades can send
                              you email with detailed results

    Example:
        >>> # The values shown are the default. Change them if needed.
        >>> from primer_designer import PrimerDesigner
        >>> pd = PrimerDesigner()
        >>> pd.folder = "alignments"   # folder containing the FASTA file alignments
        >>> pd.tm = "55"               # annealing temperature
        >>> pd.min_amplength = "250"   # minimum amplicon length
        >>> pd.max_amplength = "500"   # maximum amplicon length
        >>> pd.gencode = "universal"   # see below for all available genetic codes
        >>> pd.mode  = "primers"
        >>> pd.clustype = "dna"
        >>> pd.amptype = "dna_GTRG"    # substitution model used to estimate phylogenetic information
        >>> pd.email = "youremail@email.com"   # primer4clades will send you an email with very detailed results
        >>> pd.design_primers()

    The best primer pairs will be printed to your screen. Detailed results will
    be saved as HTML files in your alignments folder. But it is recommended if
    you also get the results by email. primers4clades_ will send you one email
    for each alignment.
    The genetic code table (variable ``gencode``) can be any of the following:
        * ``universal`` for standard
        * ``2`` for vertebrate mitochondrial
        * ``3`` for yeast mitochondrial
        * ``4`` for mold and protozoa mitochondrial
        * ``5`` for invertebrate mitochondrial
        * ``6`` for ciliate
        * ``9`` for echinoderm and flatworm
        * ``10`` for  euplotid nuclear
        * ``11`` for  bacterial and plastid
        * ``12`` for  alternative yeast nuclear
        * ``13`` for  ascidian mitochondrial
        * ``14`` for  flatworm mitochondrial
        * ``15`` for  Blepharisma nuclear
        * ``16`` for  Chlorophycean mitochondrial
        * ``21`` for  Trematode mitochondrial
        * ``22`` for  Scenedesmus obliquus mitochondrial
        * ``23`` for  Thraustochytrium mitochondrial

    The evolutionary substitution model can be any of the following (variable
    ``amptype``):
        * ``protein_WAGG``  for protein WAG+G
        * ``protein_JTTG``  for protein JTT+G
        * ``protein_Blosum62G``  for protein Blosum62+G
        * ``protein_VTG``  for protein VT+G
        * ``protein_DayhoffG``  for protein Dayhoff+G
        * ``protein_MtREVG``  for protein MtREV+G
        * ``dna_HKYG``  for dna HKY+G
        * ``dna_GTRG``  for dna GTR+G
        * ``dna_K80G``  for dna K80+G
        * ``dna_TrNG``  for dna TrN+G
        * ``dna_JC69G``  for dna JC69+G

    .. _primers4clades: http://floresta.eead.csic.es/primers4clades/#0
    """

    def __init__(self, folder=None, tm="55", min_amplength="100",
                 max_amplength="500", gencode="universal", mode="primers",
                 clustype="dna", amptype="dna_GTR", email=None):
        self.folder = folder
        self.tm = tm
        self.min_amplength = min_amplength
        self.max_amplength = max_amplength
        self.gencode = gencode
        self.mode = mode
        self.clustype = clustype
        self.amptype = amptype
        self.email = email

    def design_primers(self):
        if os.path.exists(self.folder):
            # are there alignments/files in that folder?
            all_files = os.path.join(self.folder, "*")
            alns = glob.glob(all_files)

            if len(alns) > 0:
                url = "http://floresta.eead.csic.es/primers4clades/primers4clades.cgi"
                params = {
                    'tm': self.tm, 'min_amplength': self.min_amplength,
                    'max_amplength': self.max_amplength, 'mode': self.mode,
                    'gencode': self.gencode, 'clustype': self.clustype,
                    'email': self.email,
                }

                primers = []
                for aln in alns:
                    if is_fasta(aln):
                        print("\nProcessing file \"%s\"" % aln)
                        files = {'sequencefile': open(aln, 'rb')}
                        r = requests.post(url, files=files, data=params)

                        this_file = os.path.split(aln)[1]
                        this_file = re.sub(".fas.*", "", this_file)

                        # Save result to file
                        to_print = "Writing detailed results as file \""
                        to_print += str(aln) + ".html\""
                        print(to_print)

                        f = open(str(aln) + ".html", "w")
                        f.write(r.text)
                        f.close()

                        # Show primer pair to user
                        html_file = r.text.split("\n")
                        i = 1
                        for line in html_file:
                            if "degen_corr" in line:
                                seq = line.split(" ")[0].strip()

                                description = line.split(" ")[2].strip()

                                this_id = this_file + "_" + line.split(" ")[1].strip()
                                this_id += "_" + str(i)

                                seq = Seq(seq, IUPAC.ambiguous_dna)
                                seq_record = SeqRecord(seq)
                                seq_record.id = this_id
                                seq_record.description = description
                                primers.append(seq_record)
                                i = int(i)
                                i = i + 1

                            if i == 3:
                                break

                # Write primers to alignment file
                SeqIO.write(primers, "primers.fasta", "fasta")
                print("\nDone.\nAll primers have been saved in the file \"primers.fasta\"")

            else:
                print("\nError! the folder {0} is empty.\n".format(self.folder))

        else:
            print("\nError! the folder {0} does not exist.\n".format(self.folder))
