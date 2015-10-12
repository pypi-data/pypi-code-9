# -*- coding: utf-8 -*-
from datetime import datetime

import pytest

from cghq_common.utils import (build_sampledir, date_from_rundir, dateify,
                               extract_flowcell, modification_date,
                               prepare_json, split_fastq, sample_from_rundir)

FASTQ_PATH = ("150410_D00134_0189_BHF3GKADXX/Unaligned2/Project_600597/"
              "Sample_ADM992A10_XTB02/"
              "ADM992A10_XTB02_GAGCTGAA_L002_R1_001.fastq.gz")


def test_build_sampledir():
    demux_root = 'tests/fixtures/demux'
    run_folder = '150410_D00134_0189_BHF3GKADXX'
    true_sample_id = 'ADM992A9'
    false_sample_id = 'ADM992A9fake'

    # test with existing sample run dir
    sample_rundir = build_sampledir(demux_root, run_folder, true_sample_id)
    the_rundir = ("tests/fixtures/demux/150410_D00134_0189_BHF3GKADXX/"
                  "Unaligned2/Project_600597/Sample_ADM992A9_XTA02/")
    assert sample_rundir == the_rundir

    # test with non-existing sample run dir
    with pytest.raises(AttributeError):
        build_sampledir(demux_root, run_folder, false_sample_id)


def test_date_from_rundir():
    run_dir = 'tests/fixtures/demux/150410_D00134_0189_BHF3GKADXX'
    run_date = date_from_rundir(run_dir)
    assert run_date.year == 2015
    assert run_date.month == 4
    assert run_date.day == 10

    with pytest.raises(AttributeError):
        date_from_rundir('tests/D00134_0189_BHF3GKADXX')


def test_dateify():
    regular_date_str = '2015-02-17T19:31:24'
    regular_date = dateify(regular_date_str)
    assert regular_date.year == 2015
    assert regular_date.month == 2
    assert regular_date.day == 17
    assert regular_date.hour == 19
    assert regular_date.minute == 31
    assert regular_date.second == 24


def test_modification_date():
    test_file = 'tests/fixtures/timestamp-test.txt'
    mod_date = modification_date(test_file)

    expected_year = 2015
    expected_month = 8
    expected_day = 11
    assert expected_year == mod_date.year
    assert expected_month == mod_date.month
    assert expected_day == mod_date.day


def test_extract_flowcell():
    run_dir = 'tests/fixtures/demux/150410_D00134_0189_BHF3GKADXX'
    flowcell_id = extract_flowcell(run_dir)
    assert flowcell_id == 'HF3GKADXX'

    # test with trailing slash
    run_dir = 'tests/fixtures/demux/150410_D00134_0189_BHF3GKADXX/'
    flowcell_id = extract_flowcell(run_dir)
    assert flowcell_id == 'HF3GKADXX'


def test_split_fastq():
    parts = split_fastq(FASTQ_PATH)

    assert parts['sample'] == 'ADM992A10'
    assert parts['index'] == 'GAGCTGAA'
    assert parts['lane'] == 2
    assert parts['read'] == 1
    assert parts['segment'] == 1


def test_sample_from_rundir():
    sample_rundir = ("./DEMUX/140627_D00410_0080_AH9BVFADXX/Unaligned"
                     "/Project_331195/Sample_000107T_sureselect7")
    sample_id = sample_from_rundir(sample_rundir)
    assert sample_id == '000107T'

    # ... and with trailing slash:
    sample_id = sample_from_rundir(sample_rundir + '/')
    assert sample_id == '000107T'


def test_prepare_json():
    test_dict = {'date': datetime.now(), 'name': 'P.T. Anderson',
                 'nested': {'date': datetime.now()}}
    prepare_json(test_dict)

    assert isinstance(test_dict['date'], str)
    assert isinstance(test_dict['nested']['date'], str)
    assert test_dict['name'] == 'P.T. Anderson'
