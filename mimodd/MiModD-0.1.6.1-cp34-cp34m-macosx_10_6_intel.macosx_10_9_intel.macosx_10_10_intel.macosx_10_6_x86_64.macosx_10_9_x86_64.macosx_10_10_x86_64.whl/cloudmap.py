import sys

from collections import OrderedDict

from . import pyvcf

def vcf_to_cloudmap (mode, ifile, mapping_sample,
                     related_parent = None, unrelated_parent = None,
                     infer_missing_parent = False, seqdict_file = None,
                     ofile = None, verbose = False):
    # argument validation
    mode = mode.upper()
    if mode == 'VAF':
        if not (related_parent or unrelated_parent):
            raise RuntimeError('At least one parent sample must be specified in "{0}" mode.'
                                .format(mode))
        if related_parent and unrelated_parent and infer_missing_parent:
            raise RuntimeError('infer_missing_parent cannot be used with both parent samples specified.')
    elif mode == "SVD":
        if related_parent or unrelated_parent:
            raise RuntimeError('Parent information cannot be used in mode "{0}".'
                                .format(mode))
    else:
        raise ValueError ('Expected one of "SVD", "VAF" for mode.')

    # optional generation of a sequence dictionary file for cloudmap        
    if seqdict_file:
        cloudmap_seqdict_from_vcf(ifile, seqdict_file)

    # vcf file conversion for cloudmap tools
    with pyvcf.open(ifile) as vcf:
        # validate all sample names
        for sample in (mapping_sample, related_parent, unrelated_parent):
            if sample and sample not in vcf.info.sample_names:
                raise RuntimeError('Sample {0}: no such sample name in the vcf file.'.format(sample))
        if not ofile:
            out = sys.stdout
        else:
            out = open(ofile, 'w')
        try:
            # write vcf header for a single sample
            # ensure contig names are CloudMap compatible
            compat_contig_names = sanitize_contig_names_for_cloudmap(
                                  vcf.info.contigs)
            new_contigs = OrderedDict()
            for contig_ID, contig_data in vcf.info.meta['contig'].items():
                new_contigs[compat_contig_names[contig_ID]] = contig_data
            vcf.info.meta['contig'] = new_contigs
            out.write(str(vcf.info.sample_slice([mapping_sample])) + '\n')

            if mode == 'SVD':
                # in 'SVD' mode, we simply strip away any additional samples
                # writing only mapping_sample information to the new vcf
                for record in vcf:
                    record.chrom = compat_contig_names[record.chrom]
                    out.write(str(record.sample_slice([mapping_sample])) + '\n')
            elif mode == 'VAF':
                # things are more complicated in 'VAF' mode
                # desired behaviour (not currently fully implemented):
                # always set record.ref to the (inferred) related parent allele or (lacking that) the reference allele
                # set record.alt to the predominant non-related parent allele
                # if there is no non-related parent allele, set record.alt to None
                # remove DPR field from output

                for record in vcf:
                    # parse the related and unrelated parent samples' GT field
                    # if no genotype is available (GT is ./.) pretend that the
                    # corresponding sample is not available for this position
                    if related_parent:
                        related_parent_gt_allele_nos = {
                            int(n) for n in
                            record.sampleinfo['GT'][related_parent].split('/')
                            if n !='.'
                            } or {None}
                    else:
                        related_parent_gt_allele_nos = {None}
                    if unrelated_parent:
                        unrelated_parent_gt_allele_nos = {
                            int(n) for n in
                            record.sampleinfo['GT'][unrelated_parent].split('/')
                            if n !='.'
                            } or {None}
                    else:
                        unrelated_parent_gt_allele_nos = {None}
                    # include only sites where all parents have a homozygous genotype call
                    # and where that call is different for the parents if two are provided
                    if len(related_parent_gt_allele_nos) == 1 and \
                     len(unrelated_parent_gt_allele_nos) == 1 and \
                     related_parent_gt_allele_nos != unrelated_parent_gt_allele_nos:
                        related_gt_allele_no = related_parent_gt_allele_nos.pop()
                        unrelated_gt_allele_no = unrelated_parent_gt_allele_nos.pop()
                        # include a site only if at least one parent has a non-reference (>0) genotype
                        # or if, with one parent, infer_missing_parent is True
                        if related_gt_allele_no or unrelated_gt_allele_no or infer_missing_parent:
                            # parse the DPR field of the mapping_sample
                            dpr_counts = [int(count) for count in record.sampleinfo['DPR'][mapping_sample].split(',')]
                            total_counts = sum(dpr_counts)
                            # Calculate the AD field with respect to recombination
                            # frequency (dip towards zero indicates close linkage).
                            # For a sample trio (mapping sample, related and
                            # unrelated parent), AD is:
                            # "related parent's allele count,
                            # unrelated parent's allele count".
                            # For a pair of samples (mapping sample and related or
                            # unrelated parent), the default is to assume a
                            # homozygous REF genotype for the missing sample.
                            # If infer_missing_parent is True, the missing
                            # parent's allele count is the sum of all counts
                            # except those of the other parent's genotype.
                            if related_gt_allele_no is None:
                                if infer_missing_parent:
                                    related_like_counts = total_counts - dpr_counts[unrelated_gt_allele_no]
                                else:
                                    related_like_counts = dpr_counts[0]
                            else:
                                related_like_counts = dpr_counts[related_gt_allele_no]
                            if unrelated_gt_allele_no is None:
                                if infer_missing_parent:
                                    unrelated_like_counts = total_counts - dpr_counts[related_gt_allele_no]
                                else:
                                    unrelated_like_counts = dpr_counts[0]
                            else:
                                unrelated_like_counts = dpr_counts[unrelated_gt_allele_no]
                            if related_like_counts + unrelated_like_counts > 0:
                                record.sampleinfo['AD'] = {}
                                record.sampleinfo['AD'][mapping_sample] = '{0},{1}'.format(related_like_counts, unrelated_like_counts)
                                # cloudmap calculates linkage as:
                                # second value of AD field / read depth from DP field
                                # so we need to adjust DP to equal the sum of the two
                                # AD field values
                                record.sampleinfo['DP'][mapping_sample] = '{0}'.format(related_like_counts + unrelated_like_counts)
                                # trim the record to just the mapping sample
                                record = record.sample_slice([mapping_sample])
                                # to think about: do we want to adjust REF and ALT and delete DPR ?

                                # turn chromosome names into their CloudMap
                                # compatible versions before writing
                                record.chrom = compat_contig_names[record.chrom]
                                out.write(str(record) + '\n')

                            # some thoughts on the algorithm:
                            #
                            # sample and related parent:
                            # looking for variants inherited in the F2
                            # all-like-related-parent sites in sample are evidence for close linkage
                            # sources of errors:
                            # a) counting sites with related-parent and sample = reference allele would give lots of false linkage when there was no mutation in any parent
                            # b) counting sites with related-parent = reference and sample something else would give false non-linkage if the sample allele was not introduced by the cross,
                            #    but results from another difference between the (possibly distantly related) parent and the sample
                            # c) false linkage if the (not included) unrelated parent carried, by chance, the same mutant allele as the related-parent
                            #
                            # a) is UNACCEPTABLE,
                            # the impact of b) depends on the relatedness between the strains and COULD BE ACCEPTABLE
                            # c) is UNAVOIDABLE with just two samples and should be ACCEPTED
                            #
                            # sample and non-related parent:
                            # looking for non-related parent variants NOT inherited in the F2
                            # all-not-like-non-related-parent sites in sample are evidence for close linkage
                            # sources of errors:
                            # a) as above
                            # b) as above (often less severe since mapping strain is typically used directly)
                            # c) as above
                            #
                            # consequences as above, but further supporting OPTIONAL ACCEPTANCE of type b) errors
                            # HOWEVER: question of reasonable cut-off (problem non-ref sample reads at very low levels would likely be artefacts that carry no information,
                            # but would be interpreted as strong linkage/non-linkage
                            #
                            # three-sample analysis with sample, related and non-related parent:
                            # eliminates all above sources of errors -> preferred
                            #
                            # in sample trio case adjust DP to related parent counts + non-related parent counts
            else:
                raise AssertionError('Oh oh, this looks like a bug')            
        finally:
            if out is not sys.stdout:
                try:
                    out.close()
                except:
                    pass

            
def cloudmap_seqdict_from_vcf (ifile, ofile = None):
    try:
        vcf = pyvcf.open(ifile)
        if not ofile:
            out = sys.stdout
        else:
            out = open(ofile, 'w')

        compat_contig_names = sanitize_contig_names_for_cloudmap(
                              vcf.info.contigs)
        for ident, length in vcf.info.contigs.items():
            out.write('{0}\t{1}\n'.format(compat_contig_names[ident],
                                          int(length)//10**6+1))
    finally:
        try:
            vcf.close()
        except:
            pass
        if out is not sys.stdout:
            try:
                out.close()
            except:
                pass
    

def sanitize_contig_names_for_cloudmap (ori_names):
    """Return a mapping of contig names to their CloudMap-compatible versions."""

    # CloudMap does not work correctly with contig names containing colons
    # so we replace ":" with "_".

    compat_map = {contig_name: contig_name.replace(':', '_') for contig_name in ori_names}
    return compat_map
