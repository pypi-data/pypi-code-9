"""A collection of wrappers that provide a functional programming interface
to the csamtools software suite."""

import subprocess
import glob
import os
import signal
import tempfile
import gzip
from collections import namedtuple
from . import config, catch_sigterm, tmpfiles
from . import SamtoolsRuntimeError, ArgumentParseError, FormatParseError

SamtoolsReturnValue = namedtuple('SamtoolsReturnValue', ['call', 'results', 'errors'])

class Command (object):
    """Object representation of a samtools subcommand call.

    To be used by faidx, _iheader, index, reheader, sort, cat and view.
    Not yet ready for use."""

    def __init__ (self, subcommand, parameters, o_redirect = False, fatal_strings=[]):
        pass

    def execute (self):
        if o_redirect:
            proc = subprocess.Popen(self.call, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            results, errors = (s.decode() for s in proc.communicate())
        else:
            # output is going to stdout, so better don't PIPE it !!
            proc = subprocess.Popen(self.call, shell = True, stderr = subprocess.PIPE)
            results, errors = None, proc.communicate()[1].decode()            
        if proc.returncode or any([msg in errors for msg in self.fatal_strings]):
            # can't rely on return code alone here because some samtools subcommands, e.g. samtools sort, inappropriately
            # return 0 with some errors
            raise RuntimeError ('{0} failed with: {1}'.format(self.call, errors or 'no error message'))
        return SamtoolsReturnValue(self.call, results, errors)
    
def is_bam (ifile):
    with gzip.open(ifile) as i:
        try:
            return i.read(3) == b'BAM'
        except OSError:
            # this isn't even a gzipped file
            return False
            
def faidx (ref_genome):
    """Wrapper around samtools faidx."""
    
    call = [config.samtools_exe, 'faidx', ref_genome]
    results, errors = (s.decode() for s in subprocess.Popen(call, bufsize = -1, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate())

    if errors:
        msg = 'Failed to index file {0}.'.format(ref_genome)
        raise SamtoolsRuntimeError(msg, ' '.join(call), errors)

    return SamtoolsReturnValue(call, results, errors)

def header (inputfile, iformat):
    """Wrapper around samtools view -H.

    Yields an iterator over the header lines of a sam/bam file."""

    if iformat == "sam":
        call = [config.samtools_legacy_exe, 'view', '-H', '-S', inputfile]
    elif iformat == "bam":
        call = [config.samtools_legacy_exe, 'view', '-H', inputfile]
    else:
        raise ArgumentParseError(
            'Invalid input format "{0}". Must be "sam" or "bam".',
            iformat)
    
    results, errors = (s.decode() for s in subprocess.Popen(call, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate())

    if not results:
        if errors:
            msg = 'Could not obtain header information from the {0} input file.'.format(iformat.upper())
            raise SamtoolsRuntimeError(msg, ' '.join(call), errors)
        else:
            return
    
    for line in results.strip().split('\n'):
        yield line
    
def index (inputfile, reindex = False):
    """Wrapper around samtools index."""

    if os.path.exists(inputfile+'.bai') and not reindex:
        return SamtoolsReturnValue('', '', '')
    call = [config.samtools_legacy_exe, 'index', inputfile]
    results, errors = (s.decode() for s in subprocess.Popen(call, bufsize = -1, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate())
    if errors:
        msg = 'Failed to index file {0}.'.format(inputfile)
        raise SamtoolsRuntimeError(msg, ' '.join(call), errors)
    return SamtoolsReturnValue(call, results, errors)

def reheader (template, inputfile, outputfile = None, verbose = False):
    """Wrapper around samtools reheader."""

    if isinstance (template, str):        
        call = [config.samtools_legacy_exe, 'reheader', template, inputfile]
        stdin_pipe = None
        input_bytes = None
    elif isinstance (template, dict):
        call = [config.samtools_legacy_exe, 'reheader', '-', inputfile]
        stdin_pipe = subprocess.PIPE
        input_bytes = str(template).encode()
    if outputfile:
        stdout_pipe = open(outputfile, 'wb')
    else:
        stdout_pipe = None
    if verbose:
        print ('generating new bam from {0} with new header from template {1}'.format(inputfile, template))

    p = subprocess.Popen(call, stdout = stdout_pipe, stderr = subprocess.PIPE, stdin = stdin_pipe)
    results, errors = None, p.communicate(input = input_bytes)[1].decode()
    if outputfile:
        stdout_pipe.close()
    if errors:
        msg = 'Could not reheader input file {0}.'.format(inputfile)
        raise SamtoolsRuntimeError(msg, ' '.join(call), errors)
    return SamtoolsReturnValue(call, results, errors)

    
def sort (ifile, ofile = None, iformat = None, oformat = 'bam',
          maxmem = None, threads = None,
          by_read_name = False, compression_level = None):
    """Wrapper around samtools sort.

    Improvements over wrapped tool:
    - samtools sort adds an extra '.bam' to the final output file, here we don't;
    - ensures cleanup of temporary files upon unexpected termination of samtools,
      where samtools would leave them behind;
    - never pollutes the final output directory with temporary files;
    - treats errors more consistently than samtools;
    - enables output in SAM format;
    - simpler call signature.
    """

    # Define samtools sort stderr output signatures
    # that indicate an error despite a 0 return code.
    # With samtools 1.x we have not yet found any such signature.
    fatal_strings = []

    # sanitize parameters
    if oformat not in ('sam', 'bam'):
        raise ArgumentParseError(
            'Unknown output format "{0}". Valid formats are "bam" and "sam"',
            oformat)
    if iformat not in ('sam', 'bam', None):
        raise ArgumentParseError(
            'Unknown input format "{0}". Valid formats are "bam" and "sam"',
            iformat)
    # if no input format is specified, we let samtools autodetect it,
    # otherwise we do a fast precheck
    if iformat == 'sam' and is_bam(ifile):
        raise FormatParseError('The input looks like BAM format. Expected SAM.')
    if iformat == 'bam' and not is_bam(ifile):
        raise FormatParseError('The input is not in BAM format.')
    if not threads:
        threads = config.multithreading_level
    # Calculate per-thread memory allowance.
    # The fixed factor 2.5 is required because samtools sticks only losely
    # to the indication and overconsumes memory especially for large input
    # files. The chosen factor prevents overconsumption for files beyond
    # 150 GB (the actual limit is untested), but moderately reduces
    # performance for smaller files.
    maxmem = int((maxmem or config.max_memory)*10**9 / (threads * 2.5))
        
    # construct the call to samtools sort
    tmp_output = tmpfiles.unique_tmpfile_name ('MiModD_sort','')
    call = [config.samtools_exe, 'sort']
    if by_read_name:
        call.append('-n')
    if compression_level:
        call += ['-l', str(compression_level)]
    call += ['-@', str(threads),
             '-m', str(maxmem),
             '-O', oformat,
             '-T', tmp_output]
    if ofile:
        call += ['-o', ofile]
        call_stdout = subprocess.PIPE
    else:
        call_stdout = None
    call.append(ifile)

    # run samtools sort        
    signal.signal(signal.SIGTERM, catch_sigterm)
    try: # we may need to delete temporary files created by samtools
        proc = subprocess.Popen(call,
                                stdout=call_stdout, stderr=subprocess.PIPE)
        results, errors = (s if s is None else s.decode()
                           for s in proc.communicate())

        # check for errors with sort call
        if proc.returncode or any([msg in errors for msg in fatal_strings]):
            # can't rely on return code alone here
            # because samtools sort inappropriately returns 0 with
            # some errors
            msg = 'Failed to sort file {0}.'.format(ifile)
            raise SamtoolsRuntimeError(msg, ' '.join(call), errors)
    except:
        # make sure the subprocess is terminated
        try:
            proc.terminate()
        except:
            pass
        # try to remove temporary files created by samtools
        # that may have been left behind
        for file in glob.iglob(tmp_output + '.*.bam'):
            try:
                os.remove(file)
            except:
                pass
        raise
    return SamtoolsReturnValue(call, results, errors)


def cat (infiles, outfile, oformat, headerfile = None):
    """Wrapper around samtools cat, but with additional header management."""

    if oformat not in ('sam', 'bam'):
        raise ArgumentParseError('Unknown output format "{0}". Valid formats are bam and sam',
                                 oformat)

    if len(infiles) > 1:
        # calling samtools cat
        command_strings = ['cat']
        if headerfile:
            command_strings += ['-h "{0}"'.format(headerfile)]
        if oformat == 'bam':
            command_strings += ['-o "{0}"'.format(outfile)]
        for file in infiles:
            command_strings.append('"{0}"'.format(file))
        if oformat == 'sam':
            command_strings += ['| {0} view -h -o "{1}" -'.format(config.samtools_legacy_exe, outfile)]
        call = ' '.join(command_strings)
        call = '{0} {1}'.format(config.samtools_legacy_exe, call)
        results, errors = (s.decode() for s in subprocess.Popen(call, shell = True, bufsize = -1, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate())
        if errors:
            msg = 'Could not concatenate the input files.'
            raise SamtoolsRuntimeError(msg, call, errors)
        return SamtoolsReturnValue(call, results, errors)
    else:
        # with only one file just rewrite it using samtools view, but respect output format
        ret = view (infiles[0], 'bam', outfile, oformat)
        return ret

    
def view (infile, iformat, outfile = None, oformat = None, threads = None):
    """Simple wrapper around samtools view."""

    if not iformat in ('sam', 'bam'):
        raise ArgumentParseError(
            'Invalid input format "{0}". Expected "sam" or "bam".',
            iformat)
    if not oformat:
        if iformat == 'sam':
            oformat = 'bam'
        elif iformat == 'bam':
            oformat = 'sam'
    if not oformat in ('sam', 'bam'):
        raise ArgumentParseError(
            'Invalid output format "{0}". Expected "sam" or "bam".',
            oformat)

    if not threads:
        threads = config.multithreading_level
    fatal_strings = []
    call = [config.samtools_exe, 'view']
    if oformat == 'bam':
        call.append('-b')
        call.extend(['-@', str(threads)])
    elif oformat == 'sam':
        call.append('-h')
    if iformat == 'sam':
        call.append('-S')
    if outfile:
        call.extend(['-o', outfile])
    call.append(infile)

    if outfile:
        proc = subprocess.Popen(call, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        results, errors = (s.decode() for s in proc.communicate())
    else:
        # output is going to stdout, so better don't PIPE it !!
        proc = subprocess.Popen(call, stderr = subprocess.PIPE)
        results, errors = None, proc.communicate()[1].decode()            
    if proc.returncode or any([msg in errors for msg in fatal_strings]):
        # see sort() for rationale behind this
        msg = 'Conversion from {0} to {1} failed for file {2}.'.format(
            iformat.upper(), oformat.upper(), infile)
        raise SamtoolsRuntimeError(msg, ' '.join(call), errors)

    return SamtoolsReturnValue(call, results, errors)
