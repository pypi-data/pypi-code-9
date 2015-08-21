import os.path
import re
import numpy as np

from intogen import so

SIMPLE_AA_CHANGE_RE = re.compile(r"^([\*A-Z])(?:/([\*A-Z]))?$", re.IGNORECASE)
COMPLEX_AA_CHANGE_RE = re.compile(r"^([\*\-A-Z]+)(?:/([\*\-A-Z]+))?$", re.IGNORECASE)


from math import log


class ReContext(object):
    def __init__(self):
        self.rematch = None

    def match(self, regexp, matchstring):
        self.rematch = re.match(regexp, matchstring)
        return bool(self.rematch)

    def group(self, i):
        return self.rematch.group(i)


class TransFIC(object):
    # Consequence group
    CT_SYNONYMOUS = 1
    CT_STOP = 2
    CT_FRAMESHIFT = 3
    CT_NON_SYNONYMOUS = 4

    # Impact class
    HIGH_IMPACT_CLASS = 1
    MEDIUM_IMPACT_CLASS = 2
    LOW_IMPACT_CLASS = 3
    UNKNOWN_IMPACT_CLASS = 4
    NONE_IMPACT_CLASS = 5

    IMPACT_CLASSES = {
        HIGH_IMPACT_CLASS,
        MEDIUM_IMPACT_CLASS,
        LOW_IMPACT_CLASS
    }

    CLASS_NAME = {
        HIGH_IMPACT_CLASS: "high",
        MEDIUM_IMPACT_CLASS: "medium",
        LOW_IMPACT_CLASS: "low",
        UNKNOWN_IMPACT_CLASS: "unknown",
        NONE_IMPACT_CLASS: "none"
    }

    CLASS_VALUE = {
        "high": HIGH_IMPACT_CLASS,
        "medium": MEDIUM_IMPACT_CLASS,
        "low": LOW_IMPACT_CLASS,
        "unknown": UNKNOWN_IMPACT_CLASS,
        "none": NONE_IMPACT_CLASS
    }

    @staticmethod
    def higher_impact(a, b):
        return min(a, b)

    @staticmethod
    def class_value(cls):

        if cls not in TransFIC.CLASS_VALUE:
            return np.nan

        return TransFIC.CLASS_VALUE[cls]

    @staticmethod
    def class_name(cls):

        if cls not in TransFIC.CLASS_NAME:
            return None

        return TransFIC.CLASS_NAME[cls]

    def __init__(self, data_path):
        self.data_path = data_path

        self.__partitions = {}

    def __load_partition(self, name):
        if name not in self.__partitions:
            self.__partitions[name] = {}

        part = self.__partitions[name]

        with open(os.path.join(self.data_path, name + ".genes"), "r") as f:
            f.readline()  # discard header
            for line in f:
                fields = line.rstrip("\n").split("\t")
                gene = fields[0]
                # sift_mean, sift_sd, pph2_mean, pph2_sd, ma_mean, ma_sd = [float(x) for x in fields[1:7]]
                part[gene] = tuple([float(x) for x in fields[1:7]])

        return part

    def __get_partition(self, name):
        if name not in self.__partitions:
            self.__load_partition(name)

        return self.__partitions[name]

    def __calculate(self, ct_type, score, mean, sd, class_thresholds, is_ma=False):
        if score is None:
            return (None, None)

        if ct_type == self.CT_SYNONYMOUS:
            tfic = mean - 2.0 * sd
        elif ct_type in [self.CT_FRAMESHIFT, self.CT_STOP]:
            tfic = mean + 2.0 * sd
        elif ct_type == self.CT_NON_SYNONYMOUS:
            if not is_ma:
                if score == 0.0:
                    score = 0.001
                elif score == 1.0:
                    score = 0.999

                tfic = log(score / (1 - score)) - (mean / sd)
            else:
                tfic = (score - mean) / sd

        if tfic < class_thresholds[0]:
            tfic_class = self.LOW_IMPACT_CLASS
        elif tfic < class_thresholds[1]:
            tfic_class = self.MEDIUM_IMPACT_CLASS
        else:
            tfic_class = self.HIGH_IMPACT_CLASS

        return tfic, tfic_class

    def calculate(self, part_name, gene, ct, sift_score, pph2_score, ma_score):
        part = self.__get_partition(part_name)

        if gene not in part:
            return (None, None, None, None, None, None)

        sift_mean, sift_sd, pph2_mean, pph2_sd, ma_mean, ma_sd = part[gene]

        sift_tfic, sift_class = self.__calculate(ct, sift_score, sift_mean, sift_sd, (0.0, 2.0))
        pph2_tfic, pph2_class = self.__calculate(ct, pph2_score, pph2_mean, pph2_sd, (0.0, 1.5))
        ma_tfic, ma_class = self.__calculate(ct, ma_score, ma_mean, ma_sd, (1.0, 3.0), is_ma=True)

        return sift_tfic, sift_class, pph2_tfic, pph2_class, ma_tfic, ma_class

    def run(self, gene, transcript, ct, protein_pos, aa_change, sift_score, pph2_score, uniprot, fi_score):
        # gene = vep.get('gene')
        #transcript = vep.get('transcript')
        #ct = vep.get('consequence')
        #protein_pos = vep.get('protein_pos')
        #aa_change = vep.get('aa_change')
        #sift_score = float(vep.get('sift')) if 'sift' in vep else None
        #pph2_score = float(vep.get('polyphen')) if 'polyphen' in vep else None

        # ct = (ct or "").split(",")  # Invert sift score
        if sift_score is not None:
            sift_score = 1.0 - sift_score

        ma_score = None

        #ma = values['ma'][0] if 'ma' in values else {}
        #uniprot = ma['uniprot'] if 'uniprot' in ma else None

        sift_impact = pph2_impact = ma_impact = None  # TransFIC.UNKNOWN_IMPACT_CLASS

        coding_region = 1 if so.match(ct, so.CODING_REGION) else 0

        sift_tfic, sift_class, pph2_tfic, pph2_class, ma_tfic, ma_class = (None, None, None, None, None, None)

        ct_type = None
        if so.match(ct, so.NON_SYNONYMOUS):  # missense
            ct_type = TransFIC.CT_NON_SYNONYMOUS
            ma_score = float(fi_score) if fi_score is not None else None

            (sift_tfic, sift_class,
             pph2_tfic, pph2_class,
             ma_tfic, ma_class) = self.calculate("gosmf", gene, ct_type, sift_score, pph2_score, ma_score)

            sift_impact = sift_class if sift_class in self.IMPACT_CLASSES else sift_impact
            pph2_impact = pph2_class if pph2_class in self.IMPACT_CLASSES else pph2_impact
            ma_impact = ma_class if ma_class in self.IMPACT_CLASSES else ma_impact
        elif so.match(ct, so.STOP):  # stop
            sift_impact = pph2_impact = ma_impact = TransFIC.HIGH_IMPACT_CLASS
            sift_score = pph2_score = 1.0
            ma_score = 3.5
        elif so.match(ct, so.FRAMESHIFT):  # frameshift
            sift_impact = pph2_impact = ma_impact = TransFIC.HIGH_IMPACT_CLASS
            sift_score = pph2_score = 1.0
            ma_score = 3.5
        elif so.match(ct, so.SPLICE_JUNCTION):  # splice junction
            sift_impact = pph2_impact = ma_impact = TransFIC.HIGH_IMPACT_CLASS
            sift_score = pph2_score = 1.0
            ma_score = 3.5
        elif so.match(ct, so.SPLICE_REGION):  # splice region
            sift_impact = pph2_impact = ma_impact = TransFIC.UNKNOWN_IMPACT_CLASS
            sift_score = pph2_score = 1.0
            ma_score = 3.5
        elif so.match(ct, so.SYNONYMOUS):  # synonymous
            sift_impact = pph2_impact = ma_impact = TransFIC.NONE_IMPACT_CLASS
            sift_score = pph2_score = 0.0
            ma_score = -2
        else:
            sift_impact = pph2_impact = ma_impact = TransFIC.NONE_IMPACT_CLASS

        # try to follow the convention http://www.hgvs.org/mutnomen/recs-prot.html
        prot_change = None
        if ct_type == TransFIC.CT_FRAMESHIFT:
            if protein_pos is None:
                prot_change = "fs"
            else:
                prot_change = "fs {0}".format(protein_pos)
        elif ct_type == "splice":
            prot_change = "r.spl?"
        elif protein_pos is not None and aa_change is not None:
            rc = ReContext()
            if rc.match(SIMPLE_AA_CHANGE_RE, aa_change):
                prot_change = "{ref}{pos}{alt}".format(pos=protein_pos, ref=rc.group(1), alt=rc.group(2) or "=")
            elif rc.match(COMPLEX_AA_CHANGE_RE, aa_change):
                prot_change = "{0} {1}".format(aa_change, protein_pos)

        tr_impact = ma_impact or pph2_impact or sift_impact or TransFIC.UNKNOWN_IMPACT_CLASS

        return (
            tr_impact, prot_change,
            sift_score, sift_tfic, sift_class, sift_impact,
            pph2_score, pph2_tfic, pph2_class, pph2_impact,
            ma_score, ma_tfic, ma_class, ma_impact,
            coding_region
        )
