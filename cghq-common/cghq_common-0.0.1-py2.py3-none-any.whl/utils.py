# -*- coding: utf-8 -*-
from datetime import datetime, date
import os
import re

from bson import ObjectId
from path import path

from .compat import iteritems

FC_PATTERN = re.compile("[0-9]{6}_.*_[0-9]{4}_.H.*XX")
DATE_TEMPLATE = '%Y-%m-%dT%H:%M:%S'


def modification_date(filename):
    """Get modification date as a datetime object."""
    timestamp = os.path.getmtime(filename)
    return datetime.fromtimestamp(timestamp)


def split_fastq(fastq_file):
    """Split FASTQ-file name into parts."""
    file_name = path(fastq_file).normpath().basename()
    parts = file_name.split('_')

    lane = int(parts[3].replace('L', ''))
    read = int(parts[4].replace('R', ''))
    segment = int(parts[5].replace('.fastq.gz', ''))

    return {'sample': parts[0], 'index': parts[2], 'lane': lane,
            'read': read, 'segment': segment}


def extract_flowcell(run_dir):
    """Extract flowcell id from run dir path.

    Args:
        run_dir (path): path to run folder

    Returns:
        str: flowcell id
    """
    run_folder = path(run_dir).normpath().basename()
    folder_parts = run_folder.split('_')
    flowcell_part = folder_parts[-1]
    flowcell_id = flowcell_part[1:]

    return flowcell_id


def build_sampledir(demux_root, run_folder, sample_id):
    """Figure out the sample run dir."""
    demux_path = path(demux_root)
    sample_glob = "Unaligned*/Project_*/Sample_{}*".format(sample_id)
    sample_rundir = demux_path.joinpath(run_folder, sample_glob)

    # glob the specific directory
    sample_paths = sample_rundir.glob('')

    if len(sample_paths) == 1:
        return sample_paths[0]
    elif len(sample_paths) == 0:
        raise AttributeError('sample run directory not found')
    else:
        raise AttributeError('sample run directory not unique')


def date_from_rundir(run_dir):
    """Extract run date from (sample) run directory."""
    matches = FC_PATTERN.findall(run_dir)
    if len(matches) != 1:
        raise AttributeError('ambiguous run directory')

    run_folder = matches[0]
    raw_date = run_folder[:6]
    return datetime.strptime(raw_date, '%y%m%d').date()


def sample_from_rundir(sample_rundir):
    """Extract sample_id from sample run directory."""
    sample_path = path(sample_rundir)
    sample_folder = sample_path.realpath().basename()

    # extract sample id from folder name
    return sample_folder.split('_')[1]


def dateify(date_str, template=DATE_TEMPLATE):
    """Reverse stringified datetime object."""
    return datetime.strptime(date_str, template)


def stringify_date(date_obj, template=DATE_TEMPLATE):
    """Stringify a datetime object uniformely."""
    return date_obj.strftime(template)


def prepare_json(dict_obj):
    for key, value in iteritems(dict_obj):
        if isinstance(value, dict):
            prepare_json(value)
        elif isinstance(value, (datetime, date)):
            dict_obj[key] = stringify_date(value)
        elif isinstance(value, ObjectId):
            dict_obj[key] = str(value)
    return dict_obj
