import sys

from decimal import Decimal
from collections import OrderedDict, Counter, namedtuple

from . import pyvcf, plotters
from . import ArgumentParseError, ArgumentValidationError, FormatParseError, DependencyError


class BinnedCounts (dict):
    def __init__ (self, bins, contigs):
        self.contigs = contigs
        for xbase in bins:
            # Initialize bin counters and
            # prepopulate each marker bin with one pseudocount
            # to avoid division-by-zero errors and
            # skipping of empty bins when calculating
            # histogram data.
            self[xbase] = {contig: {'markers': Counter(x for x in range(1, length//xbase + 2)),
                                    'non_segregating': Counter()}
                                    for contig, length in contigs.items()}
        
    def get_histogram_bins (self, xbase, normalize_bins = False):
        # if not self.exhausted:
        #     raise RuntimeError('Cannot calculate statistics during an ongoing mapping analysis.')
        hdata = OrderedDict()
        for contig in self.contigs:
            raw_counts = self[xbase][contig]
            # Throughout the method, we iterate over the keys in 'markers'.
            # Some of these may be missing in 'non_segregating', but since
            # we are dealing with Counters, we can still access them directly.
            if not normalize_bins:
                hdata[contig] = {bin: raw_counts['non_segregating'][bin]
                                 for bin in raw_counts['markers']}
            else:
                if len(raw_counts['non_segregating']) > 0:
                    mean_non_seg_count_on_contig = Decimal(
                        sum(raw_counts['non_segregating'].values())
                        ) / len(raw_counts['markers'])
                    hdata[contig] = {bin: (Decimal(raw_counts['non_segregating'][bin]) /
                                     (raw_counts['markers'][bin] -
                                      raw_counts['non_segregating'][bin])
                                     ) * mean_non_seg_count_on_contig
                                     for bin in raw_counts['markers']}
                else:
                    # avoid accidental division-by-zero
                    # if no non-segregating variants exist
                    hdata[contig] = {bin: 0 for bin in raw_counts['markers']}
        return hdata

    def get_histogram_series (self, normalize_bins = False):
        hdata = OrderedDict((contig, {}) for contig in self.contigs)
        for xbase in self:
            data = self.get_histogram_bins(xbase, normalize_bins)
            for contig, data_series in data.items():
                hdata[contig][xbase] = data_series
        return hdata

    def get_markers_per_bin (self, xbase, normalize_bins = False):
        hdata = OrderedDict()
        for contig in self.contigs:
            # remember to subtract the one pseudocount from the markers
            if normalize_bins:
                scaling = Decimal(max(self)) / xbase
                hdata[contig] = {bin: (counts - 1) * scaling 
                                 for bin, counts in
                                 self[xbase][contig]['markers'].items()}
            else:
                hdata[contig] = {bin: counts - 1
                                 for bin, counts in
                                 self[xbase][contig]['markers'].items()}
        return hdata
    
    def get_marker_series (self, normalize_bins = False):
        hdata = OrderedDict((contig, {}) for contig in self.contigs)
        for xbase in self:
            data = self.get_markers_per_bin(xbase, normalize_bins)
            for contig, data_series in data.items():
                hdata[contig][xbase] = data_series
        return hdata

            
class NacreousMap (object):
    def __init__ (self, vcfreader, mapping_sample,
                  related_parent = None, unrelated_parent = None,
                  infer_missing_parent = False,
                  stats_bins = []):
        self.reader = vcfreader
        self.mapping_sample = mapping_sample
        self.related_parent = related_parent
        self.unrelated_parent = unrelated_parent
        self.infer_missing_parent = infer_missing_parent
        self.exhausted = False
        # initialize the per-contig stats dictionaries
        self.binned_counts = BinnedCounts(stats_bins,
                                          contig_dict_from_vcf(self.reader))

    def __iter__ (self):
        try:
            for record in self.reader:
                # parse the related and unrelated parent samples' GT field
                # if no genotype is available (GT is ./.) pretend that the
                # corresponding sample is not available for this position
                if self.related_parent:
                    related_parent_gt_allele_nos = {
                        int(n) for n in
                        record.sampleinfo['GT'][self.related_parent].split('/')
                        if n !='.'
                        } or {None}
                else:
                    related_parent_gt_allele_nos = {None}
                if self.unrelated_parent:
                    unrelated_parent_gt_allele_nos = {
                        int(n) for n in
                        record.sampleinfo['GT'][self.unrelated_parent].split('/')
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
                    if related_gt_allele_no or unrelated_gt_allele_no or self.infer_missing_parent:
                        # parse the DPR field of the mapping_sample
                        dpr_counts = [int(count) for count in record.sampleinfo['DPR'][self.mapping_sample].split(',')]
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
                            if self.infer_missing_parent:
                                related_like_counts = total_counts - dpr_counts[unrelated_gt_allele_no]
                            else:
                                related_like_counts = dpr_counts[0]
                        else:
                            related_like_counts = dpr_counts[related_gt_allele_no]
                        if unrelated_gt_allele_no is None:
                            if self.infer_missing_parent:
                                unrelated_like_counts = total_counts - dpr_counts[related_gt_allele_no]
                            else:
                                unrelated_like_counts = dpr_counts[0]
                        else:
                            unrelated_like_counts = dpr_counts[unrelated_gt_allele_no]
                        if related_like_counts + unrelated_like_counts > 0:
                            record.linkage_data = [unrelated_like_counts, related_like_counts, total_counts]
                            yield record.sample_slice([self.mapping_sample])

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
            # ----------------------------------------------------------------
            
        finally:
            # signal that the generator has returned
            self.exhausted = True


SimpleRecord = namedtuple('SimpleRecord',
                          ['chrom',
                           'pos',
                           'linkage_data']
                          )


def vaf_mapping (ifo, bin_sizes, normalize = True,
                 mapping_sample = None,
                 related_parent = None, unrelated_parent = None,
                 infer_missing_parent = None,
                 text_out = sys.stdout, cloudmap_mode = False,
                 plot_file = None,
                 **plot_options):
    contigs = ifo.info.contigs
    if isinstance(ifo, pyvcf.VCFReader):
        if not mapping_sample:
            raise ArgumentParseError(
                'A mapping sample must be specified in "{0}" mode.',
                'VAF'
                )        
        if not (related_parent or unrelated_parent):
            raise ArgumentParseError(
                'At least one parent sample must be specified in "{0}" mode.',
                'VAF'
                )
        if related_parent and unrelated_parent and infer_missing_parent:
            raise ArgumentParseError(
                '"infer_missing_parent" cannot be used with both parent samples specified.'
                )

        mapper = NacreousMap(ifo, mapping_sample,
                             related_parent, unrelated_parent,
                             infer_missing_parent,
                             stats_bins=bin_sizes)
        binned_counts = mapper.binned_counts
    else:
        if mapping_sample or related_parent or unrelated_parent:
            raise ArgumentParseError(
                'Sample information cannot be used when replotting from a per-variant report file.'
                )

        mapper = ifo
        binned_counts = BinnedCounts(bin_sizes, contigs)
    if text_out:
        if cloudmap_mode:
            # In cloudmap_mode we want to write a CloudMap compatibility file,
            # which is, essentially, vcf.
            report_writer = write_vcf_records(text_out, ifo.info, mapping_sample)
        else:
            # In standard mode, we write a simple TAB-separated format
            # with read counts and ratios.
            colnames = ['#Chr',
                        'Pos',
                        'Alt Count',
                        'Ref Count',
                        'Read Depth',
                        'Ratio']
            report_writer = write_per_variant_report(text_out, contigs, colnames)
        next(report_writer) # prime the coroutine, now waiting for records

    if plot_file:
        # set up the plotting device
        plotter = plotters.contig_plotter(plot_file,
                                          xlab='Location (Mb)',
                                          major_tick_unit=bin_sizes[0],
                                          xlim=max(contigs.values())
                                               if not plot_options.get('fit_width')
                                               else None
                                          )
        next(plotter) # prime the coroutine, now waiting for data to plot
        if plot_options.get('no_scatter'):
            with_scatter = False
        else:
            with_scatter = True
            scatter_params = {
                'loess_span': plot_options.get('loess_span') or 0.1,
                'ylim': plot_options.get('ylim_scatter') or 1,
                'points_color': plot_options.get('points_color') or 'gray27',
                'loess_color': plot_options.get('loess_color') or 'red',
                'no_warnings': plot_options.get('no_warnings')
                }
        if plot_options.get('no_hist'):
            with_hist = False
        else:
            with_hist = True
    # Set up and start the main loop
    # obtaining and plotting data for each contig
    # in the input.
    for contig, linkage_data in linkage_reader(mapper, binned_counts, report_writer if text_out else None):
        if plot_file and with_scatter and linkage_data:
            scatter_params.update(title=contig)
            plotter.send([plotters.plot_scatter, linkage_data, scatter_params])
    # During the iteration above the linkage_reader
    # has stored binned stats per chromosome.
    # Now we use this information to plot histograms
    hdata = binned_counts.get_histogram_series(normalize)
    if plot_file and with_hist:
        if not plot_options.get('ylim_hist'):
            # scale all histogram y-axes to the largest value overall
            max_observed_y = max(value
                                 for data in hdata.values()
                                 for series in data.values()
                                 for value in series.values())
            # this scaling is retained from the original CloudMap code
            plot_options['ylim_hist'] = myround(max_observed_y + \
                                        int(round(round(max_observed_y)/10)))
        # plot histograms one per contig
        for contig, data in hdata.items():
            plotter.send([plotters.plot_histogram,
                          data,
                          {'title': contig,
                           'ylim': plot_options['ylim_hist'],
                           'ylab': '{0} of variants with apparent total linkage'
                           .format('normalized frequency'
                                   if normalize
                                   else 'number'),
                           'hist_colors': plot_options.get('hist_colors')
                          }]
                         )
    if plot_file:
        plotter.close()
    return hdata


def svd_mapping (ifo, bin_sizes, normalize = True,
                 mapping_sample = None,
                 related_parent = None, unrelated_parent = None,
                 infer_missing_parent = None,
                 text_out = sys.stdout, cloudmap_mode = False,
                 plot_file = None,
                 **plot_options):
    #argument validation
    if mapping_sample or related_parent or unrelated_parent:
        raise ArgumentParseError(
            'Sample information cannot be used in mode "{0}".',
            'SVD'
            )
    
    contigs = ifo.info.contigs
    if text_out:
        if cloudmap_mode:
            # In cloudmap_mode we want to write a CloudMap compatibility file,
            # which is, essentially, vcf.
            report_writer = write_simple_vcf_records(text_out,
                                                     ifo.info,
                                                     mapping_sample
                                                     )
        else:
            # In standard mode, we write a simple TAB-separated
            # 2-column format.
            colnames = ['#Chr',
                        'Pos']

            report_writer = write_svd_report(text_out,
                                             contigs,
                                             colnames,
                                             mapping_sample
                                             )
        next(report_writer) # prime the coroutine, now waiting for records

    if plot_file:
        # set up the plotting device
        plotter = plotters.contig_plotter(plot_file,
                                          xlab='Location (Mb)',
                                          major_tick_unit=bin_sizes[0],
                                          xlim=max(contigs.values())
                                               if not plot_options.get('fit_width')
                                               else None
                                          )
        next(plotter) # prime the coroutine, now waiting for data to plot
        # no scatter plots from this tool
        with_scatter = False
        if plot_options.get('no_hist'):
            with_hist = False
        else:
            with_hist = True

    # in current 'SVD' mode, we simply strip collect every variant
    # found in the input file
    def svd_parser (ifo):
        # mock something to fit in our framework!
        # ugly, but works
        for record in ifo:
            record.linkage_data = [1, 1, 2]
            yield record
            
    if isinstance(ifo, pyvcf.VCFReader):
        mapper = svd_parser(ifo)
    else:
        mapper = ifo
    binned_counts = BinnedCounts(bin_sizes, contigs)
    for contig, linkage_data in linkage_reader(mapper, binned_counts,
                                               report_writer
                                               if text_out else None
                                               ):
        pass
    # treat binned counts
    hdata = binned_counts.get_marker_series(normalize)
    if plot_file and with_hist:
        if not plot_options.get('ylim_hist'):
            # scale all histogram y-axes to the largest value overall
            max_observed_y = max(value
                                 for data in hdata.values()
                                 for series in data.values()
                                 for value in series.values())
            # this scaling is retained from the original CloudMap code
            plot_options['ylim_hist'] = myround(max_observed_y + \
                                        int(round(round(max_observed_y)/10)))
        # plot histograms one per contig
        for contig, data in hdata.items():
            plotter.send([plotters.plot_histogram,
                          data,
                          {'title': contig,
                           'ylim': plot_options['ylim_hist'],
                           'ylab': '{0} of variants'
                                   .format('frequency'
                                           if normalize
                                           else 'number'),
                           'hist_colors': plot_options.get('hist_colors')
                          }]
                         )
    if plot_file:
        plotter.close()
    return hdata


def linkage_reader (mapper, binner = None, report_writer = None):
    current_contig = None
    while True:
        for record in mapper:
            # Each record has a linkage_data list of [unrelated_like_counts, related_like_counts, total_counts].
            # Here, we append the ratio of unrelated_like_counts/total_counts to it.
            record.linkage_data.append(record.linkage_data[0] / record.linkage_data[2])
            if report_writer:
                report_writer.send(record)
            if binner:
                for xbase in binner:
                    this_bin = record.pos//xbase + 1
                    binner[xbase][record.chrom]['markers'][this_bin] += 1
                    if record.linkage_data[0] == 0:
                        binner[xbase][record.chrom]['non_segregating'][this_bin] += 1
            if record.chrom != current_contig:
                if current_contig is not None:
                    yield current_contig, ratios
                current_contig = record.chrom
                break
            ratios.append((record.pos, record.linkage_data[3]))
        else:
            # the mapper is exhausted
            # yield data for last contig, then return
            yield current_contig, ratios
            return
        ratios = [(record.pos, record.linkage_data[3])]


def delegate (mode, ifile, mapping_sample = None,
              related_parent = None, unrelated_parent = None,
              ofile = None,
              bin_sizes = None,
              normalize_hist = True,
              text_file = None,
              seqdict_file = None,
              cloudmap_mode = False,
              plot_file = None,
              quiet = False,
              **plot_options):
    """Module entry function delegating work to dedicated analysis functions."""

    # general argument validation
    mode = mode.upper()
    try:
        func = {'VAF': vaf_mapping,
                'SVD': svd_mapping
                }[mode]
    except KeyError:
        raise ArgumentParseError(
            'Unknown mode "{0}". Expected "SVD" or "VAF".',
            mode
            )
    if cloudmap_mode and not text_file:
        raise ArgumentParseError(
            'CloudMap compatibility mode requires an additional text output file specified through the "-t" option'
            )
    if not plot_file and plot_options:
        raise ArgumentParseError(
            'Any plot options require a specified plot output file.'
            )
    if plot_file:
        if plot_options.get('no_hist') and mode == 'SVD':
            raise ArgumentParseError(
                'Conflicting plot settings. A plot output file is specified, but histogram plotting is turned off and there is nothing else to plot in SVD mode.'
                )
        if plot_options.get('no_hist') and plot_options.get('no_scatter'):
            raise ArgumentParseError(
                'Conflicting plot settings. A plot output file is specified, but both histogram and scatter plotting are turned off so there is nothing to plot.'
                )
        if not plotters.RPY_OK:
            # upon import plotters sets this to False
            # if rpy2 is not installed
            raise DependencyError(
                'Graphical output requires the third-party module rpy.'
                )
        if quiet:
            plot_options['no_warnings'] = True
    if not bin_sizes:
        bin_sizes = [10**6, 5*10**5]
    else:
        bin_sizes = parse_bin_sizes(bin_sizes)

    # open input file and detect its format
    try:
        ifo = pyvcf.open(ifile)
    except FormatParseError:
        try:
            if mode == 'SVD':
                ifo = PerVariantSvdFileReader(open(ifile))
            else:
                ifo = PerVariantVafFileReader(open(ifile))
        except FormatParseError:
            raise ArgumentValidationError(
                'Expected vcf or per-variant report file'
                )
    if seqdict_file:
        # User-provided seqdicts always overwrite contig information
        # found in the input file.
        # To achieve this we clear the preparsed contig information and
        # add the seqdict info because for some readers the info structure
        # is an immutable tuple
        ifo.info.contigs.clear()
        ifo.info.contigs.update(read_cloudmap_seqdict(seqdict_file))
    elif not ifo.info.contigs:
        raise ArgumentValidationError(
            'Could not obtain contig information from the input file. You may have to provide an additional CloudMap-style seqdict file.'
            )

    if not ofile:
        out = sys.stdout
    else:
        out = open(ofile, 'w')
        
    # TO DO: close IO streams upon errors from here on
    
    # input file format dependent argument validation
    if isinstance(ifo, PerVariantFileReader):
        if cloudmap_mode:
            raise ArgumentParseError(
                'CloudMap compatibility mode is not available when remapping from a per-variant report file.'
                )
        if text_file:
            raise ArgumentParseError(
                'Additional per-variant site output ("-t" option) is not supported when remapping from a per-variant report file.'
                )
    elif isinstance(ifo, pyvcf.VCFReader):
        if seqdict_file:
            # TO DO: a seqdict file if specified should simply overwrite
            # the contig information found in the input file
            raise ArgumentParseError(
                'A CloudMap-style sequence dictionary file can only be used when remapping from a per-variant report file.'
                )
        # validate all sample names
        verify_samples_exist(ifo, (mapping_sample, related_parent, unrelated_parent))
    else:
        raise AssertionError(
            'Oh, oh, this looks like a bug')

    if not text_file:
        text_out = None
    else:
        text_out = open(text_file, 'w')
    try:
        # call mapping function
        result = func(ifo=ifo,
                      mapping_sample=mapping_sample,
                      related_parent=related_parent,
                      unrelated_parent=unrelated_parent,
                      bin_sizes=bin_sizes,
                      normalize=normalize_hist,
                      text_out=text_out,
                      cloudmap_mode=cloudmap_mode,
                      plot_file=plot_file,
                      **plot_options
                      )
        # internally the plotting functions may decide to do this:
        #        result = replot(ifo, seqdict_file=seqdict_file,
        #                        bin_sizes=bin_sizes,
        #                        normalize=normalize_hist,
        #                        plot_file=plot_file,
        #                        **plot_options)
    finally:
        if text_out:
            try:
                text_out.close()
            except:
                pass
    try:
        # print the binned linkage data returned by the delegates
        for contig, data_series in result.items():
            print('Histogram data for LG: ' + contig, file=out)
            for xbase, series_data in data_series.items():
                print('Data based on bin-width ' + str(xbase), file=out)
                for column, counts in series_data.items():
                    print('{0}\t{1:.2f}'.format(column, counts), file=out)
                print(file=out)
            print(file=out)
    finally:
        if out is not sys.stdout:
            try:
                out.close()
            except:
                pass


def verify_samples_exist (ivcf, samples):
    for sample in samples:
        if sample and sample not in ivcf.info.sample_names:
            raise ArgumentValidationError(
                'Sample {0}: no such sample name in the vcf file.',
                sample
                )


def parse_per_variant_report_meta (ifo):
    """Parse the info section (meta data and header) of a per-variant report input stream."""

    # essentially, this is a copy of pyvcf.parse_info
    # TO DO: unify the two readers

    
    # read the Meta section into a list of lines
    meta_lines = []
    while True:
        line = ifo.readline()
        if line[0:2] != '##':
            break
        meta_lines.append(line)
    # parse the Meta list
    meta = pyvcf.parse_meta_lines(meta_lines)
    # parse the header line
    header_fields = None
    if line:
        if line[0] == '#':
            header_fields = line[1:].rstrip('\t\r\n').split('\t')
        elif line.startswith('"#Chr'):
            # probably a CloudMap-corrupted header line
            # don't bother reading it
            header_fields = ['Chr', 'Pos',
                             'Alt Count', 'Ref Count',
                             'Read Depth', 'Ratio'
                             ]
    if header_fields is None:
        raise FormatParseError(
            'Could not parse header line.',
            help='A header line starting with a single "#" must precede the body of a per-variant report file.'
            )
    return header_fields, meta


SimpleInfo = namedtuple('SimpleInfo',
                        ['meta',
                         'contigs',
                         'header_fields'])
                        
class PerVariantFileReader (object):
    def __init__ (self, ifo):
        try:
            ifo.seek(0)
        except:
            self.ifo_isseekable = False
        else:
            self.ifo_isseekable = True
        header_fields, meta = parse_per_variant_report_meta(ifo)
        contigs = OrderedDict((ID, int(contig_info['length']))
                              for ID, contig_info in
                              meta.get('contig', {}).items()
                              )
        self.info = SimpleInfo(meta, contigs, header_fields)
        if self.ifo_isseekable:
            self.body_start = ifo.tell()
        self.ifo = ifo

    def __iter__ (self):
        return self
    

class PerVariantSvdFileReader (PerVariantFileReader):
    colnames = ['Chr', 'Pos']

    def __init__ (self, ifo):
        PerVariantFileReader.__init__(self, ifo)
        if self.info.header_fields[:2] != self.colnames:
            raise FormatParseError(
                'Invalid per-variant file file'
                )
        
    def __next__ (self):
        fields = next(self.ifo).rstrip('\t\r\n').split('\t')
        if len(fields) >= 2:
            return SimpleRecord(chrom=fields[0],
                                pos=int(fields[1]),
                                linkage_data=[1,1,2]
                                )
        else:
            raise FormatParseError('Invalid per-variant report file. Expected 2 columns per line.')

    
class PerVariantVafFileReader (PerVariantFileReader):
    colnames = ['Chr', 'Pos', 'Alt Count', 'Ref Count', 'Read Depth', 'Ratio']
    
    def __init__ (self, ifo):
        PerVariantFileReader.__init__(self, ifo)
        if self.info.header_fields[:6] != self.colnames:
            raise FormatParseError(
                'Invalid per-variant file file'
                )

    def __next__(self):
        fields = next(self.ifo).rstrip('\t\r\n').split('\t')
        if len(fields) == 6:
            return SimpleRecord(chrom=fields[0],
                                pos=int(fields[1]),
                                linkage_data=[int(n) for n in fields[2:5]]
                                )
        else:
            raise FormatParseError('Invalid per-variant report file. Expected 6 columns per line.')


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
    

def read_cloudmap_seqdict (dict_file):
    with open(dict_file) as i_file:
        contig_dict = OrderedDict()
        for line in i_file:
            # allow empty lines
            line = line.strip('\t\r\n')
            if line:
                try:
                    chrom, length = line.split('\t')
                except ValueError:
                    raise FormatParseError('CloudMap Sequence Dictionary files must be TAB-separated with two columns.')
                try:
                    contig_dict[chrom] = int(length) * 10**6
                except ValueError:
                    raise FormatParseError('The second column of a CloudMap Sequence Dictionary file must consist of numeric values specifying chromosome lengths.')
    return contig_dict


def contig_dict_from_vcf (ivcf):
    # likely to change in future versions
    return ivcf.info.contigs


def sanitize_contig_names_for_cloudmap (ori_names):
    """Return a mapping of contig names to their CloudMap-compatible versions."""

    # CloudMap does not work correctly with contig names containing colons
    # so we replace ":" with "_".

    compat_map = {contig_name: contig_name.replace(':', '_') for contig_name in ori_names}
    return compat_map


def parse_bin_sizes (bin_sizes):
    factors = {'K': 10**3,
               'M': 10**6
               }
    sizes = []
    for size_str in bin_sizes:
        # ensure size_str has a minimal length of two
        size_str = '00' + size_str.strip()
        if size_str[-1] == 'b':
            try:
                factor = factors[size_str[-2]]
                size_int = int(size_str[:-2]) * factor
            except (KeyError, ValueError):
                raise ArgumentParseError(
                    'Could not parse bin-size value "{0}". Expected format INT[Kb|Mb].',
                    size_str
                    )
        else:
            try:
                size_int = int(size_str)
            except ValueError:
                raise ArgumentParseError(
                    'Could not parse bin-size value "{0}". Expected format INT[Kb|Mb].',
                    size_str
                    )
        sizes.append(size_int)
    return sizes


def myround (x, base=10):
    return int(base * round(float(x)/base))


def write_per_variant_report(out, contigs, colnames):
    w = 0
    for ID, length in contigs.items():
        w += out.write('##contig=<ID={0},length={1}>\n'.format(ID, length))
    w += out.write('\t'.join(colnames) + '\n')
    # return the number of bytes just written,
    # receive first vcf record in exchange
    record = yield w
    while True:
        data = [record.chrom, record.pos] + record.linkage_data
        if len(data) != len(colnames):
            raise RuntimeError('Number of columns to be written to TAB-separated file does not match the number of column names written earlier.')
        # write records as they come in
        w = out.write('\t'.join(str(d) for d in data) + '\n')
        record = yield w


def write_svd_report(out, contigs, colnames, sample = None):
    w = 0
    for ID, length in contigs.items():
        w += out.write('##contig=<ID={0},length={1}>\n'.format(ID, length))
    w += out.write('\t'.join(colnames) + '\n')
    # return the number of bytes just written,
    # receive first vcf record in exchange
    record = yield w
    while True:
        data = [record.chrom,
                record.pos
               ]
        if len(data) != len(colnames):
            raise RuntimeError('Number of columns to be written to TAB-separated file does not match the number of column names written earlier.')
        # write records as they come in
        w = out.write('\t'.join(str(d) for d in data) + '\n')
        record = yield w


def write_vcf_records(out, header, sample):
    compat_contig_names = sanitize_contig_names_for_cloudmap(
                          header.contigs)
    new_contigs = OrderedDict()
    for contig_ID, contig_data in header.meta['contig'].items():
        new_contigs[compat_contig_names[contig_ID]] = contig_data
    header.meta['contig'] = new_contigs

    w = out.write(str(header.sample_slice([sample])) + '\n')
    record = yield w
    while True:
        record.sampleinfo['AD'] = {}
        record.sampleinfo['AD'][sample] = '{0},{1}'.format(record.linkage_data[1], record.linkage_data[0])
        # cloudmap calculates linkage as:
        # second value of AD field / read depth from DP field
        # so we need to adjust DP to equal the sum of the two
        # AD field values
        record.sampleinfo['DP'][sample] = '{0}'.format(record.linkage_data[1] + record.linkage_data[0])
        # CloudMap is not inspecting the INFO field
        # and does not know about the DPR field
        record.info = OrderedDict()
        del record.sampleinfo['DPR']
        # trim the record to just the mapping sample
        record = record.sample_slice([sample])
        # to think about: do we want to adjust REF and ALT and delete DPR ?
        # turn chromosome names into their CloudMap
        # compatible versions before writing
        record.chrom = compat_contig_names[record.chrom]
        w = out.write(str(record) + '\n')
        record = yield w


def write_simple_vcf_records(out, header, sample = None):
    compat_contig_names = sanitize_contig_names_for_cloudmap(
                          header.contigs)
    new_contigs = OrderedDict()
    for contig_ID, contig_data in header.meta['contig'].items():
        new_contigs[compat_contig_names[contig_ID]] = contig_data
    header.meta['contig'] = new_contigs
    if sample == None:
        sample = []
    else:
        sample = [sample]

    w = out.write(str(header.sample_slice(sample)) + '\n')
    record = yield w
    while True:
        # trim the record to just the mapping sample
        record = record.sample_slice(sample)
        # CloudMap is not inspecting the INFO field
        record.info = OrderedDict()
        # to think about: do we want to adjust REF and ALT and delete DPR ?
        # turn chromosome names into their CloudMap
        # compatible versions before writing
        record.chrom = compat_contig_names[record.chrom]
        w = out.write(str(record) + '\n')
        record = yield w
