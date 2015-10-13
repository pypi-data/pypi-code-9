"""Facilitates the use of the SNAP aligner.

The module's core function is snap_call, which provides an enhanced
interface to SNAP correcting many of the shortcomings of the current version
(0.15) of SNAP.
snap_batch provides a user-friendly way to run several SNAP jobs
and to merge the results into a single output file organized in several read
groups. This function is used by the GALAXY interface of MiModD.
"""

import sys, os
import shlex
import signal
import shutil
import subprocess
import gzip
import platform

from collections import Counter

from . import config, catch_sigterm, __version__
from . import fasta, pysamtools, samheader, pysam, tmpfiles
from .decox import parachute, FuncInfo
from .auxparsers import SnapCLParser

from . import ArgumentParseError, ArgumentValidationError, ParseError, FormatParseError

tempfile_dir = config.tmpfiles_path
snap_exe = config.snap_exe

# raise an error on SIGTERM throughout this module
signal.signal(signal.SIGTERM, catch_sigterm)


def is_yosemite ():
    """Return True when called on OS X Yosemite."""

    platform_description = platform.uname()
    if platform_description[0] == 'Darwin' and platform_description[2].split('.')[0] == '14':
        # kernel version 14.x.x indicates Yosemite
        return True


def is_OS_X ():
    """Return True when called on any OS X version."""

    platform_description = platform.uname()
    if platform_description[0] == 'Darwin':
        return True


def select_parallelism (max_threads, snap_dest):
    """Select the optimal parallel processing mode for the platform.

    Returns a tuple of: threads to be used by SNAP and a boolean indicating
    whether snap_dest has been set up for use as a named pipe for more
    efficient coupling between the SNAP alignment process and postprocessing."""
    
    # Ideally, we want to run SNAP and output postprocessing jointly
    # using a named pipe.
    # If a named pipe cannot be set up or if the user limits max_threads
    # to 1, we run snap first, saving its output in a regular file,
    # which we then use as input for postprocessing.
    
    aln_threads = max_threads
    use_named_pipe = False
    if aln_threads > 1 and not is_OS_X():
        # Named pipes cannot be used on OS X
        # because of SNAP's simplistic OsxAsyncFile implementation.
        # TO DO: fix the SNAP source code to change this situation.
        try:
            os.mkfifo(snap_dest)
        except (OSError, AttributeError):
            pass
        else:
            aln_threads -= 1
            use_named_pipe = True
            
    # REMOVE this block once SNAP Yosemite bug is fixed!
    if is_yosemite():
        # for currently unknown reasons
        # SNAP produces corrupt output when run
        # under Yosemite with more than one thread
        aln_threads = 1
    # --------------------------------------------------------------
    return aln_threads, use_named_pipe

            
def snap_call (mode, refgenome_or_indexdir, inputfiles,
               iformat = 'fastq', oformat = 'sam',
               verbose = False, quiet = True, **other_options):
    """Functional interface to the SNAP aligner.

    Bundles calls to snap index and the SNAP aligner in one function call.
    Extends the useful input file spectrum of SNAP by decompressing gzipped
    fastq files and converting BAM to SAM files before calling the aligner.
    Removes the .sam file extension restriction of SNAP on SAM format input.
    Ensures the correct use of input header information and proper RG tags
    in aligned reads.
    Enables exclusion of overlapping mate pairs in paired-end mode.
    Extends SNAP's output file spectrum to include BAM.

    Arguments:
    mode: 'single' or 'paired'; used to specify the aligner call
    refgenome_or_indexdir: if a directory, it is used as the index-dir argument
                           in the underlying call to snap
                           if a filename, it is used in a call to snap index to
                           generate the index-dir at the location specified by
                           idx_out
    inputfiles: an iterable of input files; used as the inputfile(s) argument
                in the underlying call to snap
    outputfile: output destination
    iformat: 'fastq', 'sam' or 'bam' to specify the format of the input files;
             care is taken of format conversion and calling snap correctly
    oformat: 'sam' or 'bam' to specify the output format;
             the function takes care of format conversion
    idx_out: specifies the location for the index directory;
             used as the output-dir argument in an underlying call to
             snap index; default: config.tmpfiles_path/outfileprefix+'_index'
    idx_seedsize: the -s parameter for snap index
    idx_slack: the -h parameter for snap index
    idx_ofactor: the -O parameter for snap index
    """
    
    # snap_call_argcheck does basic argument validation and returns a flattened dictionary of all arguments for convenience
    args = snap_call_argcheck(FuncInfo(func = snap_call, innerscope = True), locals())
    
    # read defaults from config.py
    if 'threads' not in args:
        args['threads'] = config.multithreading_level

    input_header = args['header']
    # if the rg does not specify a sample name, reuse the ID
    # the previous call of snap_call_argcheck makes sure that
    # there is only one rg entry in the header
    if not 'SM' in input_header['RG'][0]:
        input_header['RG'][0]['SM'] = input_header['RG'][0]['ID']

    # args['outputfile'] specifies where snap output should go
    # get the file's name without extension
    outfileprefix = os.path.basename(args['outputfile']).split('.')[0]
    snap_output, sorted_output = (
            tmpfiles.unique_tmpfile_name(outfileprefix, '.tmp'),
            args['outputfile']
            )
    amended_output = snap_output+'_unsorted' \
                     if args.get('sort') \
                     else sorted_output
    args['outputfile'] = snap_output

    # PREPARE SNAP SUBPROCESS CALL

    # a maxmem argument is supported, but it is used only
    # to determine the memory usage during sorting
    sort_memory = args.get('maxmem') or config.max_memory

    # set default value for --spacing in paired-end mode
    if mode == 'paired' and 'spacing' not in args:
        args['spacing'] = [100, 10000]
        
    option_table = {'outputfile':'-o',
                    'maxseeds':'-n',
                    'maxhits':'-h',
                    'maxdist':'-d',
                    'confdiff':'-c',
                    'confadapt':'-a',
                    'selectivity':'-S',
                    'filter_output':'-F',
                    'gap_penalty':'-G'
                    }
    sticky_table = {'clipping':'-C'}
    bool_table = {'mmatch_notation':'-M',
                  'error_rep':'-e',
                  'no_prefetch':'-P',
                  'bind_threads':'-b',
                  'explore':'-x',
                  'stop_on_first':'-f',
                  'ignore': '-I'
                  }
    iter_table = {'spacing':'-s'}
    
    snap_args = []
    for option in option_table:
        if args.get(option):
            snap_args += [option_table[option], str(args[option])]
    for option in sticky_table:
        if args.get(option):
            snap_args.append(''.join([sticky_table[option],str(args[option])]))
    for option in bool_table:
        if args.get(option):
            snap_args.append(bool_table[option])
    for option in iter_table:
        if args.get(option):
            snap_args.append(iter_table[option])
            snap_args += [str(v) for v in args[option]]
            
    # this list keeps track whether any input file is a temporary file that needs to be removed before finishing
    inputfiles_remove = [False for file in inputfiles]

    # starting IO, make sure we clean up
    try:
        try:
            # EXTENSION OF SNAP INPUT FILE SPECTRUM
            # decompress .gz
            if verbose:
                print ('Preparing input files for alignment ..')
            if args.get("iformat") == "gz":
                for n, file in enumerate(inputfiles):
                    inputfiles[n] = tmpfiles.unique_tmpfile_name(outfileprefix, '.fastq')
                    inputfiles_remove[n] = True
                    with gzip.open(file, 'rb') as comp_data:
                        with open(inputfiles[n], 'wb') as uncomp_data:
                            shutil.copyfileobj(comp_data, uncomp_data)
                    if verbose:
                        print ('Decompressed input file {0} to {1}.'.format(file, inputfiles[n]))
            # convert BAM to SAM
            elif args.get('iformat') == 'bam':
                comp_file = inputfiles[0]
                inputfiles[0] = tmpfiles.unique_tmpfile_name(outfileprefix, '.sam')
                inputfiles_remove[0] = True
                pysamtools.view(comp_file, 'bam', inputfiles[0], 'sam')
                if verbose:
                    print ('Decompressed input file {0} to {1}.'.format(comp_file, inputfiles[0]))
            elif args.get("iformat") == "sam" and (inputfiles[0].split('.')[-1] != 'sam'):
                # .sam hard link for SAM files with wrong extension
                # SNAP relies on the .sam suffix to use sam files,
                # but we fool it with a hard link
                # SNAP cannot use symbolic links, so if no hard link
                # can be generated, we have to go for a copy of the file
                hard_link = tmpfiles.tmp_hardlink(inputfiles[0], outfileprefix, '.sam', fallback = 'copy')
                if verbose:
                    print ('Generated hard link {0} for input file {1}.'.format(hard_link, inputfiles[0]))
                inputfiles[0] = hard_link
                inputfiles_remove[0] = True
            if verbose:
                print ()

            # CALLING SNAP
            if os.path.isdir(refgenome_or_indexdir):
                ref_index = refgenome_or_indexdir
                idx_remove = False
            else:
                # build the call to snap index
                if args.get('idx_out'):
                    ref_index = args['idx_out']
                    idx_remove = False
                else:
                    ref_index = os.path.join(tempfile_dir, outfileprefix + '_index')
                    idx_remove = True
                call, results, errors = snap_index(
                                            refgenome_or_indexdir, ref_index,
                                            args.get('idx_seedsize'), args.get('idx_slack'),
                                            args.get('idx_ofactor'), args.get('threads'),
                                            verbose = verbose, quiet = quiet)
            # get the md5sums of all sequences just indexed
            with open(os.path.join(ref_index, 'md5sums'), 'r') as ifo:
                md5dict = {seqtitle: md5 for seqtitle, md5 in (line.strip().split('\t') for line in ifo)}

            aln_threads, pipe_to_postprocess = select_parallelism(
                                                max_threads=args['threads'],
                                                snap_dest=snap_output)
            snap_args += ['-t', str(aln_threads)]
            
            # build the call to snap single|paired
            snap_align = [snap_exe, mode, ref_index] + inputfiles + snap_args
            # put together the args dictionary for the postprocessing function
            post_proc_args = {'ifile': snap_output,
                              'ofile': amended_output,
                              'unaln_header': input_header,
                              'md5dict': md5dict,
                              'snap_mode': mode}
            if args.get('sort'):
                post_proc_args['oformat'] = 'bam'
                post_proc_args['ocomp'] = not pipe_to_postprocess
            else:
                post_proc_args['oformat'] = args['oformat']
                if args.get('bam_compression'):
                    post_proc_args['ocomp'] = args['bam_compression']
            if args.get('discard_overlapping'):
                post_proc_args['discard_overlapping'] = args['discard_overlapping']

            # aligning
            if verbose:
                print ("Calling SNAP with:")
                print (' '.join(snap_align))
                print ()

            align_proc = subprocess.Popen(snap_align, bufsize = -1,
                                          stdout = subprocess.PIPE,
                                          stderr = subprocess.PIPE)
            if pipe_to_postprocess:
                # postprocess alignment while it is generated
                # using a named pipe

                # TO DO:
                # This current implementation suffers from a cleanup
                # problem with snap errors:
                # if the snap subprocess terminates unexpectedly, then
                # pysam used in postprocess_alignment will crash the
                # interpreter and no temporary files will be deleted.
                if verbose:
                    print ('Starting alignment postprocessing ...')
                    print ()
                postprocess_alignment(**post_proc_args)
                
            results, errors = (s.decode() for s in align_proc.communicate())
            if not quiet:
                print (results)
            if align_proc.returncode or errors:
                msg = 'SNAP failed with:\n'
                msg += errors or 'no specific error message.'
                if 'Unmatched read IDs' in errors:
                    msg += '\nCheck if the input is really paired-end and sorted by read names (not coordinates)'
                raise RuntimeError(msg)
        finally:
            # make sure the snap subprocess is terminated
            try:
                align_proc.terminate()
            except:
                pass
            # remove flagged index and input files
            try:
                if idx_remove:
                    shutil.rmtree(ref_index) # remove the whole index directory
            except (UnboundLocalError, OSError, IOError):
                # error occurred before idx_remove was set
                # or the directory created
                pass
            finally:
                # remove any temporary input files
                for file, flag in zip(inputfiles, inputfiles_remove):
                    if flag:
                        try:
                            os.remove(file)
                        except:
                            pass
                        
        if not pipe_to_postprocess:
            # Named pipes are not supported or the user has requested
            # a single threaded run explicitly.
            # We do postprocessing now after the alignment is done.
            if verbose:
                print ('Starting alignment postprocessing ...')
                print ()
            postprocess_alignment(**post_proc_args)
        # optional coordinate sorting 
        if args.get('sort'):
            pysamtools.sort(amended_output, sorted_output,
                            oformat=args.get('oformat'), maxmem=sort_memory)
            
    finally: # we are done, now remove all temporary files
        try:
            os.remove(snap_output)   # remove the intermediate sam output
        except:
            pass
        if args.get('sort'):
            # with sorting the final output is in sorted_output
            # so we need to get rid of the amended_output file
            try:
                os.remove(amended_output)
            except:
                pass


def postprocess_alignment(ifile, ofile, oformat,
                          unaln_header, md5dict, snap_mode,
                          discard_overlapping = [],
                          ocomp = True):
    # OUTPUT POSTPROCESSING
    # this section takes care of:
    # i)   reheadering the original SNAP output making sure that RG and other
    #      information is preserved from the input
    # ii)  retagging of all reads to correct their read group information
    # iii) filtering out overlapping mate pairs (if allow_mate_overlap is set to False)
    # iv)  optional BAM format output

    if oformat == 'bam':
        if ocomp:
            write_mode = 'wb'
        else:
            write_mode = 'wbu'
    else:
        write_mode = 'wh'

    # rewrite the data with new header information
    # filtering out overlapping mate pairs and
    # correcting read group information for each read
    with pysam.Samfile(ifile, "r") as tmp_data:
        # generate the new header object
        snap_header = samheader.Header(hdrdict=tmp_data.header)
        header = unaln_header               # mostly revert the header to what it was in the input file
        header['SQ'] = snap_header['SQ']    # SNAP gets the sequences right,
        for sq in header['SQ']:             # but we want to add MD5 tags to them
            sq['M5'] = md5dict[sq['SN']]
        # modify and add SNAP's PG header line
        for pg in snap_header['PG']:
            if pg['ID'] == 'SNAP':
                pg['PN'] = 'MiModD snap'
                pg['VN'] = str(__version__)
                pg['CL'] = ' '.join([snap_mode, pg['CL']])
        header['PG'].extend(snap_header['PG'])
            
        rg_id = header['RG'][0]['ID'] # we need the RG ID value to write it to each read's tag list below

        with pysam.Samfile(ofile, write_mode, header=header) as out_final:
            new_rg_info = ('RG', rg_id)
            if snap_mode == 'paired':
                tmp_data = purge_overlapping_factory(tmp_data,
                                                     discard_overlapping)
            for read in tmp_data:
                read.tags = [e if e[0]!='RG' else new_rg_info
                             for e in read.tags]
                out_final.write(read)


def purge_overlapping_factory (reads, orientations):
    purge_these = set(orientations)
    KEEP_ALL = set()
    PURGE_ALL = {'RF', 'FR', 'RR', 'FF'}
    PURGE_FIRST_FORWARD = {'FR', 'FF'}
    PURGE_FIRST_REVERSE = {'RF', 'RR'}
    PURGE_SECOND_FORWARD = {'RF', 'FF'}
    PURGE_SECOND_REVERSE = {'FR', 'RR'}
    PURGE_UNIDIRECTIONAL = {'FF', 'RR'}
    PURGE_BIDIRECTIONAL = {'FR', 'RF'}
    PURGE_RF = {'RF'}
    PURGE_FR = {'FR'}
    PURGE_FF = {'FF'}
    PURGE_RR = {'RR'}
    KEEP_RF = PURGE_ALL - PURGE_RF
    KEEP_FR = PURGE_ALL - PURGE_FR
    KEEP_FF = PURGE_ALL - PURGE_FF
    KEEP_RR = PURGE_ALL - PURGE_RR
    
    if purge_these == KEEP_ALL:
        return reads
    if purge_these == PURGE_ALL:
        return purge_overlapping(reads, lambda flag: False)
    if purge_these == KEEP_RF:
        return purge_overlapping(reads, lambda flag: flag & 16 and not flag & 32)
    if purge_these == KEEP_FR:
        return purge_overlapping(reads, lambda flag: flag & 32 and not flag & 16)
    if purge_these == KEEP_FF:
        return purge_overlapping(reads, lambda flag: not flag & 16 and not flag & 32)
    if purge_these == KEEP_RR:
        return purge_overlapping(reads, lambda flag: flag & 16 and flag & 32)
    if purge_these == PURGE_FIRST_FORWARD:
        return purge_overlapping(reads, lambda flag: flag & 16)
    if purge_these == PURGE_FIRST_REVERSE:
        return purge_overlapping(reads, lambda flag: not flag & 16)
    if purge_these == PURGE_SECOND_FORWARD:
        return purge_overlapping(reads, lambda flag: flag & 32)
    if purge_these == PURGE_SECOND_REVERSE:
        return purge_overlapping(reads, lambda flag: not flag & 32)
    if purge_these == PURGE_UNIDIRECTIONAL:
        return purge_overlapping(reads, lambda flag: bool(flag & 16) != bool(flag & 32))
    if purge_these == PURGE_BIDIRECTIONAL:
        return purge_overlapping(reads, lambda flag: bool(flag & 16) == bool(flag & 32))
    if purge_these == PURGE_RF:
        return purge_overlapping(reads, lambda flag: flag & 32 or not flag & 16)
    if purge_these == PURGE_FR:
        return purge_overlapping(reads, lambda flag: flag & 16 or not flag & 32)
    if purge_these == PURGE_FF:
        return purge_overlapping(reads, lambda flag: flag & 16 or flag & 32)
    if purge_these == PURGE_RR:
        return purge_overlapping(reads, lambda flag: not flag & 16 or not flag & 32)


def purge_overlapping (reads, predicate):
    """Yield only non-overlapping mate pairs from pair-sorted SAM iterable.
    
    Used by snap_call (with allow_mate_overlap=False) to purify the original
    SNAP output from read pairs that provide duplicate information.
    """

    _abs = abs
    for r1 in reads:
        while True:
            r2 = next(reads)
            if r1.qname == r2.qname:
                if not r1.tlen or r1.alen+r2.alen <= _abs(r1.tlen) \
                               or predicate(r1.flag):
                    # reads with tlen = 0 are those where one mate is unmapped
                    # or where the two mates are mapped to different references
                    # the sum of alen criterion is true for all other reads
                    # that are non-overlapping
                    yield r1
                    yield r2
                break
            if r1.flag & 2:
                raise RuntimeError ('{0} and\n{1}\nnot sorted by read pairs'.format(r1,r2))
            yield r1
            r1 = r2


@parachute
def snap_call_argcheck(**args):
    """Checks if an argument dictionary is safe to use in a call to snap_call.

    The parachute wrapper does basic argument validation and returns
    a flattened dictionary of all arguments for convenience.
    The function itself performs further sanity checks on the arguments.
    If no errors are found, the verified args dictionary gets
    returned to the caller."""
    
    allowed_params = {'mode': ('single', 'paired'),
                      'input_formats': ('fastq', 'gz', 'sam',  'bam'),
                      'output_formats': ('sam', 'bam'),
                      'clipping': ('x+', '+x', '++', 'xx', '-+', '+-', '--', None),
                      'out_filter': ('a', 's', 'u', None)
                      }
        
    ref = args.get('refgenome_or_indexdir')
    if not ref:
        raise ArgumentParseError('A reference genome or index directory is required.')
    if not os.path.exists(ref):
        raise ArgumentValidationError(
            'Invalid reference genome or index directory: {0} does not exist.', ref)
    if os.path.isdir(ref) and any((args.get('idx_seedsize'), args.get('idx_slack'), args.get('idx_out'))):
        raise ArgumentValidationError('Indexing parameters cannot be used with existing index directory.')
    if not args.get('outputfile'):
        raise ArgumentParseError('An output file needs to be specified.')
    if args['iformat'] not in allowed_params['input_formats']:
        raise ArgumentValidationError(
            'Invalid input format; must be one of: {}', ', '.join(allowed_params['input_formats']))
    if args['oformat'] not in allowed_params['output_formats']:
        raise ArgumentValidationError(
            'Invalid output format; must be one of: {}', ', '.join(allowed_params['output_formats']))
    if args['mode'] not in allowed_params['mode']:
        raise ArgumentValidationError(
            'Invalid value for parameter "mode"; must be either "single" for single-end or "paired" for paired-end mode.')
    if args['mode'] == 'paired' and len(args['inputfiles'])>2:
        raise ArgumentValidationError('Maximally two input files are allowed in paired-end mode')
    if args['mode'] == 'single' and len(args['inputfiles'])>1:
        raise ArgumentValidationError('Only one input file is allowed in single-end mode')
    if args['mode'] == 'single' and 'spacing' in args:
        raise ArgumentValidationError('Parameter -s / --spacing is only allowed in paired-end mode')
    for file in args['inputfiles']:
        if not os.path.exists(file):
            raise ArgumentValidationError('Invalid input file: {0} does not exist.', file)
    if args.get('clipping') not in allowed_params['clipping']:
        raise ArgumentValidationError(
            'Invalid value for parameter "clipping"; must be one of: "x+" (back only), "+x" (front only), "++" (back and front) or "xx" (no clipping).')
    else:
        # MiModD uses "x" to indicate no clipping, while SNAP uses "-".
        # Transform the clipping string to the format SNAP understands.
        args['clipping'] = args['clipping'].replace('x', '-')
    if args.get('out_filter') not in allowed_params['out_filter']:
        raise ArgumentValidationError(
            'Invalid value for parameter "filter-output"; must be one of: "a" (aligned), "s" (single aligned), "u" (unaligned) to keep only reads of the respective type')
    if args.get('selectivity') is not None and args.get('selectivity') < 2:
        del args['selectivity']
    if args.get('threads') is not None and args['threads'] < 1:
        raise ArgumentValidationError('Expected a positive value for parameter "threads".')
    if args.get('discard_overlapping'):
        all_orientations = {'FR', 'RF', 'FF', 'RR'}
        if 'ALL' in args['discard_overlapping']:
            args['discard_overlapping'] = all_orientations
        else:
            args['discard_overlapping'] = set(args['discard_overlapping'])
            if not args['discard_overlapping'].issubset(all_orientations):
                raise ArgumentValidationError('Unknown mate pair orientation(s): "{0}".',
                                              ', '.join(args['discard_overlapping']
                                                        .difference(all_orientations)))
    else:
        args['discard_overlapping'] = set()

    # validate input headers and
    # make sure each job has its header as a Header instance in args['header']
    header = {}
    if args['iformat'] in ('sam', 'bam'):
        try:
            header = samheader.Header.fromfile(args['inputfiles'][0], args.get('iformat'))
        except RuntimeError:
            # this causes misleading errors with wrong iformat and
            # other general failures => improve !!
            pass
        if len(header.get('RG', [])) > 1:
            raise ArgumentValidationError(
                'Multiple read groups declared in input file {0}. Such input is not currently supported.',
                args['inputfiles'][0])
    if args.get('header'):
        custom_header = args['header']
        if not isinstance (custom_header, samheader.Header):
            try:
                custom_header = samheader.Header.fromsam(custom_header)
            except RuntimeError:
                raise ArgumentValidationError(
                    'Unable to get header information from custom header argument for file {0}.',
                    args['inputfiles'][0])
        if len(custom_header['RG']) != 1:
            raise ArgumentValidationError(
                'The header specified by the custom header argument must contain exactly one read group; {0} found.',
                len(custom_header['RG']))
        args['header'] = header or samheader.Header()
        args['header'].merge_rg(custom_header, 'replace')
    else:
        if not header:
            if args['iformat'] in ('sam', 'bam'):
                raise ArgumentValidationError(
                    'Could not get header information from input file {0}.\nYou may want to provide a separate header through the custom header parameter.',
                    args['inputfiles'][0])
            else:
                raise ArgumentValidationError(
                    'Missing header information for input file {0}. {1} files require custom header information.',
                    args['inputfiles'][0], args['iformat'])
        if len(header['RG']) == 0:
            raise ArgumentValidationError(
                'Could not find read group information in the header of the input file {0}.\nYou may want to provide a separate header through the custom header parameter.',
                args['inputfiles'][0])
        args['header'] = header
    
    return args

def snap_batch (job_arglist):
    """Run several snap alignment jobs and merge the results into a single SAM/BAM file.

    Takes a list of snap_call argument dictionaries (as generated, e.g.,
    by make_snap_argdictlist) and acts as a wrapper around the corresponding
    calls to snap_call, essentially treating the individual results files as
    temporary data to be merged into a single SAM/BAM file.
    Note: in the current version, the first argument dictionary in the list
    determines sorting, format (SAM or BAM) and name of the merged file."""

    # first job's parameters determine whether the final output should be
    # sorted, the output file name and the output format
    if job_arglist[0].get('sort'):
        this_batch_sort = True
        sort_memory = job_arglist[0].get('maxmem') or config.max_memory
    else:
        this_batch_sort = False
    this_batch_output = job_arglist[0]['outputfile']
    this_batch_oformat = job_arglist[0]['oformat']

    # get and secure (by creating an empty base file) a unique file prefix for this entire batch
    unique_output_prefix = tmpfiles.unique_tmpfile_name('batch_'+os.path.basename(this_batch_output).split('.')[0])
    with open(unique_output_prefix, 'w'):
        pass
            
    tmp_files = []
    refgenomes = Counter()
    
    # examine the reference genomes passed to the different jobs
    for job_args in job_arglist:
        if not os.path.isdir(job_args['refgenome_or_indexdir']):
            # check the reference genome sequence titles for compatibility
            # raise a FormatParseError if incompatible
            with open(job_args['refgenome_or_indexdir'], 'r') as ifo:
                try:
                    fasta.assert_valid_ids(fasta.FastaReader(ifo).identifiers())
                except FormatParseError as e:
                    e.token = job_args['refgenome_or_indexdir']
                    raise
            # determine the indexing action required for the job
            idx_settings = (job_args['refgenome_or_indexdir'], job_args.get('idx_out'), job_args.get('idx_seedsize'), job_args.get('idx_slack'))
            refgenomes[(idx_settings[0], idx_settings[1] or '_'.join((unique_output_prefix, os.path.basename(idx_settings[0]).split('.')[0], str(idx_settings[2] or 0), str(idx_settings[3] or 0))),
                        idx_settings[2], idx_settings[3], False if idx_settings[1] else True)] += 1
    try:
        for job_no, job_args in enumerate(job_arglist, 1):
            # overwrite some parameters in the argument dictionary
            if 'sort' in job_args:
                del job_args['sort']
            job_args['oformat'] = 'bam'
            job_args['outputfile'] = os.path.join(tempfile_dir, unique_output_prefix + str(job_no)) # create a temporary output file for each job
            # index reference genomes only if necessary
            if not os.path.isdir(job_args['refgenome_or_indexdir']):
                idx_settings = (job_args['refgenome_or_indexdir'], job_args.get('idx_out'), job_args.get('idx_seedsize'), job_args.get('idx_slack'))
                idx_key = (idx_settings[0], idx_settings[1] or '_'.join((unique_output_prefix, os.path.basename(idx_settings[0]).split('.')[0], str(idx_settings[2] or 0), str(idx_settings[3] or 0))),
                           idx_settings[2], idx_settings[3], False if idx_settings[1] else True)
                if not os.path.exists(idx_key[1]):
                    call, results, errors = snap_index(*idx_key[:-1], ofactor = job_args.get('idx_ofactor'), threads = job_args.get('threads'), verbose = job_args["verbose"], quiet = job_args["quiet"])
                refgenomes[idx_key] -= 1
                job_args['refgenome_or_indexdir'] = idx_key[1]
                for param in ('idx_out', 'idx_seedsize', 'idx_slack', 'idx_ofactor'):
                    if param in job_args:
                        del job_args[param]
            # keep track of temporary files generated
            tmp_files.append(job_args['outputfile'])
            # do the alignment for this job
            snap_call(**job_args)
            # remove index directories that are not used anymore
            if idx_key[4] and refgenomes[idx_key] == 0:
                shutil.rmtree(idx_key[1])
    
    # combining individual temporary files to one output file
        if this_batch_sort:
            if len(tmp_files) > 1:
                tmpcatfile = os.path.join(tempfile_dir, unique_output_prefix+'_unsorted')
                samheader.cat(tmp_files, tmpcatfile, 'bam')
                for file in tmp_files:
                    try:
                        os.remove(file)
                    except:
                        pass                
            else:
                tmpcatfile = tmp_files[0]
            pysamtools.sort(tmpcatfile, this_batch_output,
                            oformat=this_batch_oformat, maxmem=sort_memory)
        else:
            samheader.cat(tmp_files, this_batch_output, this_batch_oformat)

    finally:
        # make sure temporary index directories are always removed
        for idx_key in refgenomes:
            if idx_key[4]:
                try:
                    shutil.rmtree(idx_key[1])
                except:
                    pass

        #deleting temporary files
        for file in tmp_files:
            try:
                os.remove(file)
            except:
                pass
        try:
            os.remove(tmpcatfile)
        except:
            pass
        try:
            os.remove(unique_output_prefix) # remove the base file we generated as a lock for the temporary file names of this batch
        except:
            pass


def make_snap_argdictlist (commands=None, ifile=None):
    """Populate snap_call() argument dictionaries from command lines.

    Takes an iterator over command line calls to snap_call and parses the
    arguments into a list of verified argument dictionaries, each of which
    can be used in a simple snap_call(**argdict) function call. The list can
    be used as the argument to snap_batch.
    Uses clparse and snap_call_argcheck for parsing and verifying that the
    argument dictionaries are safe to use with snap_call."""
    
    job_arglist = []
    try:
        if not commands:
            if not ifile:
                raise ValueError(
                    'Either the commands or the ifile argument MUST be specified.')
            commands = (line for line in open(ifile) if line.strip())
        for line_no, command in enumerate(commands, 1):
            try:
                # here we transform the command line to function call parameters,
                # validate these parameters and map them to snap_caller arguments !!
                args = clparse(shlex.split(command)[1:])
                job_arglist.append(snap_call_argcheck(FuncInfo(func=snap_call, innerscope = False), **args))
            except SystemExit:
                break    # somewhat complicated construct to reduce traceback
        else:
            # check all headers for compatibility
            # currently, the only requirement is that if a read group is
            # found more than once, its associated sample names have to match
            all_headers = [job['header'] for job in job_arglist]
            rg_sm_mapping = {}
            for hdr in all_headers:
                for rg in hdr['RG']:
                    if rg['ID'] in rg_sm_mapping:
                         if rg_sm_mapping[rg['ID']] != rg['SM']:
                             raise ArgumentValidationError('The input files declare the read group {0} more than once with different sample names.'.format(rg['ID']))
                    else:
                        rg_sm_mapping[rg['ID']] = rg['SM']
            return job_arglist
        
        raise ParseError(
            'Error parsing command line {0}: "{1}" is not a valid snap call.',
            line_no, command)
    finally:
        try:
            commands.close()
        except:
            pass
    return job_arglist

def clparse(args = None):
    """Command line parsing to make snap_call() usable from the terminal."""
    
    return vars(SnapCLParser.parse_args(args)).copy()


def snap_index (ref_genome, index_out, seedsize = None, slack = None, ofactor = None, threads = None, verbose = False, quiet = True):
    """A simple wrapper around SNAP index."""

    # REMOVE this block once SNAP Yosemite bug is fixed!
    if is_yosemite():
        # for currently unknown reasons
        # SNAP produces corrupt output when run
        # under Yosemite with more than one thread
        threads = 1
    # --------------------------------------------------------------

    if not threads:
        threads = config.multithreading_level
    if ofactor is not None:
        if ofactor < 1:
            ofactor = 1
        elif ofactor > 1000:
            ofactor = 1000
    with open(ref_genome, 'r') as ifo:
        # generate a list of seq_title, md5sum tuples
        md5sums = [md5 for md5 in fasta.FastaReader(ifo).md5sums()]
        # check the seq_titles for compatibility
        # raise a FormatParseError if incompatible titles are found
        fasta.assert_valid_ids(seq_title for seq_title, md5sum in md5sums)
        
    call = [snap_exe, "index", ref_genome, index_out, '-t{0}'.format(threads)]
    if seedsize:
        call += ['-s', str(seedsize)]
    if slack:
        call += ['-h', str(slack)]
    if ofactor:
        call += ['-O{0}'.format(ofactor)]
    if verbose:
        print('Calling snap index with:')
        print(' '.join(call))
        print()
    idx_proc = subprocess.Popen(call, bufsize = -1,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE)
    results, errors = (s.decode() for s in idx_proc.communicate())

    if not quiet:
        print ('\n'.join(n for n in results.split('\n') if not n.startswith('HashTable[')))
    if not idx_proc.returncode and not errors:
        with open(os.path.join(index_out, 'md5sums'), 'w') as md5_out:
            for seqtitle, md5 in md5sums:
                # replace spaces with underscores just like SNAP
                seqtitle = '_'.join(seqtitle.split(' '))
                md5_out.write('{0}\t{1}\n'.format(seqtitle, md5))
    else:
        raise RuntimeError ("SNAP index failed with:\n" + (errors or 'no error message available.'))

    return call, results, errors

