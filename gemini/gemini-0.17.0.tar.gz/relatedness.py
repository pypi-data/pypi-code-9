import vcf
import sys
import re

def num_alt_alleles(gt):
    (a1, a2) = re.split('/|', gt)
    return (a1 != '0') + (a2 != '0')

def aaf(record):
    num_not_missing = 0
    num_alts = 0
    for sample in record.samples:
        gt = sample['GT']
        if gt is not None:
            num_alts += num_alt_alleles(gt)
            num_not_missing += 2
        else:
            num_unknown += 1

vcf_reader = vcf.Reader(filename=sys.argv[1])
for record in vcf_reader:
    print record
    aaf(record)
