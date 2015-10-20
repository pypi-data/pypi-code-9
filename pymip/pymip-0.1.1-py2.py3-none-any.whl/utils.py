# -*- coding: utf-8 -*-
import itertools
import os
import subprocess


def fastq_name(lane, date, flowcell, sample, index, read):
    """Build a string representing FASTQ file name.

    The naming follows MIP conventions. The syntax is as follows:
        1_140818_H9FD3ADXX_000127T_GATCAG_1.fastq.gz
    """
    if read not in ('1', '2'):
        raise ValueError("'read' must be either of directions: '1' or '2'")

    elif '_' in sample:
        raise ValueError("'sample' must not contain any underscores")

    return ("{lane}_{date}_{flowcell}_{sample}_{index}_{read}.fastq.gz"
            .format(lane=lane, date=date, flowcell=flowcell, sample=sample,
                    index=index, read=read))


def crawl_files(root_path, end_patten='_qc_sampleInfo.yaml'):
    """Crawl for files matching a certain end pattern.

    Args:
        root_path (str): where to start crawling from and down
        end_patten (str, optional): pattern to match files against

    Yields:
        str: path to files matching the end pattern
    """
    # crawl all files in the directory tree, building full paths, nested
    all_files = ((os.path.join(root, a_file) for a_file in files)
                 for root, _, files in os.walk(root_path, followlinks=True))

    # un-nest the list of lists
    all_files_flat = itertools.chain.from_iterable(all_files)

    # match paths against the provided pattern
    return (a_file for a_file in all_files_flat if a_file.endswith(end_patten))


def start_analysis(family_id, clusterconstant_path, config_path,
                   gene_list=None, mip_path=None):
    """Lunch a new MIP analysis for a specific family.

    Args:
        family_id (str): unique id for the family to analyze
        clusterconstant_path (path): root path for the analysis
        config_path (path): absolute path to the MIP config file
        gene_list (str, optional): name of the gene list file
        mip_path (path, optional): path to MIP script file

    Rerurns:
        int: return code from the executed process
    """
    command = []

    # configure the executable
    if mip_path:
        command.append('perl')
        command.append(mip_path)
    else:
        command.append('mip.pl')

    # add the family option
    command.append('--familyID')
    command.append(family_id)

    # add YAML config file path
    command.append('--configFile')
    command.append(config_path)

    # configure the "cluster constant path"
    command.append('--clusterConstantPath')
    command.append(clusterconstant_path)

    if gene_list:
        command.append('--vcfParserSelectFile')
        command.append(gene_list)

    return subprocess.Popen(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
