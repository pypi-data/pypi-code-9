#!/usr/bin/env python
import os
import sys
from collections import Counter, defaultdict, OrderedDict
import numpy as np

import GeminiQuery
from gemini_constants import *
import gemini_subjects as subjects
import gemini_bcolz as bc

def _get_sample_sex(args):
    "Return a map of sample name to reported sex"
    gq = GeminiQuery.GeminiQuery(args.db)
    query = """SELECT name, sex FROM samples order by sample_id"""
    sample_sex = OrderedDict()
    gq.run(query)
    for row in gq:
        if row['sex'] == '1':
            sex = 'male'
        elif row['sex'] == '2':
            sex = 'female'
        else:
            sex = 'unknown'
        sample_sex[row['name']] = sex
    return sample_sex

def _get_variant_range(args):
    "Return the starting and ending variant id for a given chromosome"
    gq = GeminiQuery.GeminiQuery(args.db)
    query = """SELECT min(variant_id) as cmin, max(variant_id) as cmax
               FROM   variants
               WHERE  chrom = '%s'
               AND start > 2699520 and start < 154931044
            """ % args.chrom
    gq.run(query)
    start, end = None, None
    for row in gq:
        start, end = row['cmin'], row['cmax']
    print start, end
    return start, end

def check_sex(args):
    """
    Test to see if the number and type of genotype calls on the
    X chromosome make sense given the sex of the
    individual that is stated in the samples table (PED).

    Example:

    sample  sex     X_homref  X_het  X_homalt  het_homref_ratio
    SMS173  male    7265      1975   8010      0.271851342051
    SMS254  male    5440      1316   3846      0.241911764706
    SMS255  female  6275      3188   5423      0.508047808765
    SMS253  male    5536      1355   3582      0.244761560694
    SMS243  male    6181      1506   4479      0.243649894839
    SMS242  male    6365      1437   4200      0.225765907306
    SMS193  male    6667      1864   5829      0.279586020699
    SMS238  male    6263      1638   4891      0.261536005109
    SMS239  female  6755      3669   7618      0.543153219837
    SMS244  female  6489      2953   5140      0.45507782401
    SMS230  male    7209      1784   7146      0.247468442225
    SMS231  female  7306      4659   9332      0.637695045168
    """

    # what are the reported sexes of each sample?
    sample_sex = _get_sample_sex(args)
    # where do the chrX variants start and end?
    chr_start, chr_end = _get_variant_range(args)

    if chr_start is None or chr_end is None:
        sys.exit("ERROR: cannot find variant offsets for chrom %s\n" % args.chrom)

    bcpath = bc.get_bcolz_dir(args.db)
    print '\t'.join(['sample', 'sex',
        args.chrom + '_homref', args.chrom + '_het',
        args.chrom + '_homalt', args.chrom + '_unknown',
        'mean_depth'])
    for sample in sample_sex:
    #for sample in ["100630-100630"]:
        gt_types_path = "%s/%s/%s" % (bcpath, sample, 'gt_types')
        if os.path.exists(gt_types_path):
            gt_types_carray = bc.bcolz.open(gt_types_path, mode="r")
        else:
            sys.exit("ERROR: cannot find bcolz indices for sample %s\n" % sample)

        gt_depths_path = "%s/%s/%s" % (bcpath, sample, 'gt_depths')
        if os.path.exists(gt_depths_path):
            gt_depths_carray = bc.bcolz.open(gt_depths_path, mode="r")
        else:
            sys.exit("ERROR: cannot find bcolz indices for sample %s\n" % sample)

        # retrieve the subset of genotype types for this sample
        # that are from the X chromosome
        #print gt_types_carray[0:20]
        chr_gt_types = gt_types_carray[chr_start-1:chr_end]
        #print chr_gt_types[0:10]
        #print len(chr_gt_types)
        chr_gt_depths = gt_depths_carray[chr_start-1:chr_end]
        #print chr_gt_depths[0:10]
        # tally the frequency of each genotype type
        chr_gt_counts = Counter(gt_types_carray[chr_start-1:chr_end])
        #print sample, chr_gt_counts

        het_homref_ratio = float(chr_gt_counts[HET])/float(chr_gt_counts[HOM_REF])
        print '\t'.join(str(s) for s in [sample, sample_sex[sample],
            chr_gt_counts[HOM_REF], chr_gt_counts[HET],
            chr_gt_counts[HOM_ALT], chr_gt_counts[UNKNOWN]])
            #np.mean([d for d in chr_gt_depths if d > -1]), np.std(chr_gt_depths)])

def check_sex2(args):
    gq = GeminiQuery.GeminiQuery(args.db, include_gt_cols=True)
    query = """SELECT gt_types
               FROM   variants
               WHERE  chrom = '%s'
               AND start > 2699520 and start < 154931044
               AND call_rate > 0.90
               AND depth > 1000
               AND filter is NULL
               ORDER BY random()
               LIMIT 10000
            """ % args.chrom
    gq.run(query)
    sample_gt_types = Counter()
    cnt = 0
    for row in gq:
        cnt += 1
        #gt_types = row['gt_types']
        sample_gt_types.update((idx, gt) for idx, gt in enumerate(row['gt_types']))
        # for idx, gt in enumerate(gt_types):
        #     sample_gt_types[(idx, gt)] += 1
        if cnt % 1000 == 0:
            print str(cnt) + " seen"
    # what are the reported sexes of each sample?
    sample_sex = _get_sample_sex(args)

    print '\t'.join(['sample', 'sex',
        args.chrom + '_homref', args.chrom + '_het',
        args.chrom + '_homalt', args.chrom + '_unknown'])
    for idx, sample in enumerate(sample_sex):
        #print idx, sample
        print '\t'.join(str(s) for s in [sample, sample_sex[sample],
            sample_gt_types[(idx, HOM_REF)], sample_gt_types[(idx, HET)],
            sample_gt_types[(idx, HOM_ALT)], sample_gt_types[(idx, UNKNOWN)]])


def run(parser, args):
    if os.path.exists(args.db):
        if args.mode == "sex":
            check_sex2(args)
