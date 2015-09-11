# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

__doc__ = """
bioutils.symbols -- symbols for amino acids and nucleic acids
"""

from recordtype import recordtype


class _Molecule(recordtype('_Molecule', ['symbol', 'abbr', 'descr', 'name', 'mw'], default=None)):
    """Base type for AminoAcid and NucleicAcid"""
    pass


class AminoAcid(_Molecule):
    pass


class NucleicAcid(_Molecule):
    pass


aa_iupac = [ 
    AminoAcid(symbol='A', abbr='Ala', descr='Alanine'),
    AminoAcid(symbol='C', abbr='Cys', descr='Cysteine'),
    AminoAcid(symbol='D', abbr='Asp', descr='pAspartic acid'),
    AminoAcid(symbol='E', abbr='Glu', descr='Glutamic acid'),
    AminoAcid(symbol='F', abbr='Phe', descr='Phenylalanine'),
    AminoAcid(symbol='G', abbr='Gly', descr='Glycine'),
    AminoAcid(symbol='H', abbr='His', descr='Histidine'),
    AminoAcid(symbol='I', abbr='Ile', descr='Isoleucine'),
    AminoAcid(symbol='K', abbr='Lys', descr='Lysine'),
    AminoAcid(symbol='L', abbr='Leu', descr='Leucine'),
    AminoAcid(symbol='M', abbr='Met', descr='Methionine'),
    AminoAcid(symbol='N', abbr='Asn', descr='Asparagine'),
    AminoAcid(symbol='O', abbr='Pyl', descr='Pyrrolysine'),
    AminoAcid(symbol='P', abbr='Pro', descr='Proline'),
    AminoAcid(symbol='Q', abbr='Gln', descr='Glutamine'),
    AminoAcid(symbol='R', abbr='Arg', descr='Arginine'),
    AminoAcid(symbol='S', abbr='Ser', descr='Serine'),
    AminoAcid(symbol='T', abbr='Thr', descr='Threonine'),
    AminoAcid(symbol='U', abbr='Sec', descr='Selenocysteine'),
    AminoAcid(symbol='V', abbr='Val', descr='Valine'),
    AminoAcid(symbol='W', abbr='Trp', descr='Tryptophan'),
    AminoAcid(symbol='Y', abbr='Tyr', descr='Tyrosine'),
    ]

aa_ambiguity = [ 
    AminoAcid(symbol='B', abbr='Asx', descr='Asparagine or aspartic acid'),
    AminoAcid(symbol='J', abbr='Xle', descr='Leucine or Isoleucine'),
    AminoAcid(symbol='X', abbr='Xaa', descr='Unspecified or unknown amino acid'),
    AminoAcid(symbol='Z', abbr='Glx', descr='Glutamine or glutamic acid'),
    AminoAcid(symbol='*', abbr='Ter', descr='Stop'),
    ]

aa = aa_iupac + aa_ambiguity

aa_by_symbol = {_aa.symbol: _aa for _aa in aa}


na_iupac = [
    NucleicAcid(symbol='A', abbr='A', descr='Adenine'),
    NucleicAcid(symbol='C', abbr='C', descr='Cytosine'),
    NucleicAcid(symbol='G', abbr='G', descr='Guanine'),
    ]

dna_iupac = na_iupac + [
    NucleicAcid(symbol='T', abbr='T', descr='Thymine'),
    ]

rna_iupac = na_iupac + [
    NucleicAcid(symbol='U', abbr='U', descr='Uracil'),
    ]

na_ambiguity = [
    NucleicAcid(symbol='R', abbr='R', descr='Purine (A or G)'),
    NucleicAcid(symbol='Y', abbr='Y', descr='Pyrimidine (C, T, or U)'),
    NucleicAcid(symbol='M', abbr='M', descr='C or A'),
    NucleicAcid(symbol='K', abbr='K', descr='T, U, or G'),
    NucleicAcid(symbol='W', abbr='W', descr='T, U, or A'),
    NucleicAcid(symbol='S', abbr='S', descr='C or G'),
    NucleicAcid(symbol='B', abbr='B', descr='C, T, U, or G (not A)'),
    NucleicAcid(symbol='D', abbr='D', descr='A, T, U, or G (not C)'),
    NucleicAcid(symbol='H', abbr='H', descr='A, T, U, or C (not G)'),
    NucleicAcid(symbol='V', abbr='V', descr='A, C, or G (not T, not U)'),
    NucleicAcid(symbol='N', abbr='N', descr='Any base (A, C, G, T, or U)'),
    ]

na_by_symbol = {_na.symbol: _na for _na in na_iupac + dna_iupac + rna_iupac + na_ambiguity}
