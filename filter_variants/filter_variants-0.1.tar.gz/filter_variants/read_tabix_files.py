import logging
from tabix import TabixError

# def check_tabix_index(compressed_file, file_type='cadd', verbose=False):
#     """
#     Check if a compressed file have a tabix index, if not build one.
#
#     Args:
#         compressed_file (str): Path to a file that is assumed to be compressed.
#         file_type (str): The type of the file. ('cadd' or 'vcf')
#         verbose (bool): Increase output verbosity
#
#     Returns:
#         0 if everything went ok.
#
#     """
#     if file_type == 'cadd':
#         try:
#             tabix_index(compressed_file, seq_col=0, start_col=1, end_col=1, meta_char='#')
#         except IOError as e:
#             pass
#     elif file_type == 'vcf':
#         try:
#             tabix_index(compressed_file, preset='vcf')
#         except IOError as e:
#             pass
#     return 0


# def get_frequency(tabix_reader, chrom, start, alt):
#     """
#     Return the frequency from a tabix indexed vcf file.
#
#     Arguments:
#         tabix_reader (Tabix.reader): A Tabix object
#         chrom (str): The chromosome of the position
#         start (str): The start position of the variant
#         alt (str): The alternative sequence
#
#     Returns:
#         freq (str): The frequency for this position
#     """
#     logger = logging.getLogger(__name__)
#     freq = None
#     # CADD values are only for snps:
#     tabix_key = int(start)
#     try:
#         for record in tabix_reader.query(chrom, tabix_key-1, tabix_key):
#             i = 0
#             #We can get multiple rows so need to check each one
#             #We also need to check each one of the alternatives per row
#             for alternative in record[4].split(','):
#                 if alternative == alt:
#                     for info in record[7].split(';'):
#                         info = info.split('=')
#                         if info[0] == 'AF':
#                             frequencies = info[-1].split(',')
#                             return frequencies[i]
#                 i += 1
#     except TypeError:
#         for record in tabix_reader.query(str(chrom), tabix_key-1, tabix_key):
#             i = 0
#             #We can get multiple rows so need to check each one
#             #We also need to check each one of the alternatives per row
#             for alternative in record[4].split(','):
#                 if alternative == alt:
#                     for info in record[7].split(';'):
#                         info = info.split('=')
#                         if info[0] == 'AF':
#                             frequencies = info[-1].split(',')
#                             return frequencies[i]
#                 i += 1
#     except:
#         pass
#
#     return freq


def get_thousand_g_frequency(chrom, pos, alt, tabix_reader):
    """Return the frequency found for this variant
    
    
        Args:
            chrom (str): The chromosome that the variant resides on
            pos (int): The startposition for the variant
            alt (list): A list of strings with the alternatives
            thousand_g_handle (TabixHandle): A pytabix file handle
        
        Returns:
            thousand_g_freq (float): The frequency found
    """
    logger = logging.getLogger(__name__)
    logger.debug("Checking thousand genomes ferquency for variant on chromosome"\
                 " {0}, position {1}, alternative {2}".format(chrom, pos, ','.join(alt)))
    
    try:
        for record in tabix_reader.query(chrom, pos-1, pos):
            logger.debug("Found record {0}".format(record))
            i = 0
            #We can get multiple rows so need to check each one
            #We also need to check each one of the alternatives per row
            for i,alternative in enumerate(record[4].split(',')):
                if alternative in alt:
                    logger.debug("{0} matches alt".format(alternative))
                    for info in record[7].split(';'):
                        info = info.split('=')
                        if info[0] == 'AF':
                            frequencies = info[-1].split(',')
                            logger.debug("Returning allele frequency {0}".format(frequencies[i]))
                            return frequencies[i]
    except TabixError as e:
        logger.warning("Chromosome {0} does not exist in frequency file.".format(chrom))
    
    logger.debug("No frequency found. Returning None")
    
    return None
