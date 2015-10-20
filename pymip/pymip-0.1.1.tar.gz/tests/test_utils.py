# -*- coding: utf-8 -*-
from pymip.utils import fastq_name


def test_fastq_name():
    """Test FASTQ file name generator."""
    name = fastq_name('1', '140127', 'H8A7MADXX', '0002P021', 'ACTTGA', '2')
    expected = '1_140127_H8A7MADXX_0002P021_ACTTGA_2.fastq.gz'

    assert name == expected
