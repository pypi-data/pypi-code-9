import logging
from random import sample
import re

logger = logging.getLogger(__name__)

def count(fp, n = 100, pattern = b'\n', page_size = 2**16, regex = False):
    '''
    Estimate how many times a particular pattern appears in a file.

    If data are appended to the file during the function call,
    the appended data are ignored for the sampling.
    Sampling is without replacement

    :param int n: Number of samples
    :type fp: File-like object
    :param fp: The file to estimate line lengths of
    :type pattern: Bytes or compiled regex
    :param pattern: The pattern to match
    :rtype: dict
    :returns: Stats results
    '''
    if n < 0:
        raise ValueError('Sample size must be greater than zero.')

    file_start = fp.tell()
    fp.seek(0, 2)
    file_end = fp.tell()

    # Population size
    # Ignore the last page for now.
    # To do: Weight the last page lower, proportional to its size.
    N = int((file_end - file_start) / page_size)

    if file_end <= file_start:
        raise ValueError('The file is empty, or you have seeked to a strange part of it.')
    elif N <= n:
        raise ValueError('File is too small; just use "wc -l".')

    if regex:
        actual_page_size = page_size
        def f(i):
            fp.seek(file_start + i * page_size)
            return sum(1 for _ in re.finditer(pattern, fp.read(page_size)))
    else:
        actual_page_size = page_size + 1 - len(pattern)
        def f(i):
            fp.seek(file_start + i * page_size)
            return fp.read(page_size).count(pattern)

    ts = list(map(f, sorted(sample(range(0, N), n))))
    E_t_sample = sum(ts) / n
    Var_t_sample = sum((t - E_t_sample) ** 2 for t in ts) / (n - 1)

    # 99% gaussian confidence interval
    z = 2.575829

    # Levy & Lemeshow, page 51
    fpc = (N - n) / N
    E_t_population = N * E_t_sample * (page_size / actual_page_size)
    Var_t_population = (N ** 2) * fpc * Var_t_sample / n
    SE_t_population = Var_t_population ** 0.5

    return {
        'ml': E_t_population,
        'radius': z * SE_t_population,
    }
