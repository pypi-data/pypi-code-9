# encoding: utf-8
from __future__ import print_function

import os
import sys
from operator import itemgetter
import tempfile

import pandas


HERE = os.path.dirname(os.path.abspath(__file__))


def default_template():
    path = os.path.join(HERE, "parameter_file_template.txt")
    try:
        return open(path, "r").read()
    except IOError:
        raise RuntimeError(
            "pymetfrag installation is broken, can not read %s" % path)


def _create_template_file(peaklist_file_path, chemspider_token, dmz_m0_ppm, m0, mf,
                          dmz_ms2_absolute, dmz_ms2_ppm, precursor_ion_mode, is_positive_mode,
                          result_file_name, result_folder, num_threads,
                          score_types=None, score_weights=None,
                          template=None):

    if template is None:
        template = default_template()

    if mf is None:
        precursor_setting = """DatabaseSearchRelativeMassDeviation = {dmz_m0_ppm}""".format(
            dmz_m0_ppm=dmz_m0_ppm)
    else:
        precursor_setting = """NeutralPrecursorMolecularFormula = {}""".format(
            mf)

    precursor_setting += """\nNeutralPrecursorMass = {m0}""".format(m0=m0)

    database_setting = """MetFragDatabaseType = PubChem"""
    if score_types is None:
        score_types = ["FragmenterScore"]
    else:
        assert isinstance(
            score_types, (list, tuple)), "invalid parameter score_types"
    if score_weights is None:
        score_weights = [1.0]
    else:
        assert isinstance(
            score_weights, (list, tuple)), "invalid parameter score_weights"
    assert len(score_types) == len(score_weights),\
        "score types and score weights are not consistent"

    score_weights = ",".join(map(str, score_weights))
    score_types = ",".join(score_types)

    return template.format(**locals())


def standard_settings():
    return {"dmz_m0_ppm": 5.0,
            "num_threads": 2,
            "dmz_ms2_absolute": 0.001,
            "dmz_ms2_ppm": 5.0,
            "precursor_ion_mode": 1,
            "is_positive_mode": True,
            "proxy": None,
            }

_adduct_encodings = [("M", 0),
                     ("M+H", 1),
                     ("M-H", -1),
                     ("M+NH4", 18),
                     ("M+Na", 23),
                     ("M+K", 39),
                     ("M+Cl", 35),
                     ("M+Fa-H", 45),
                     ("M+Hac-H", 59),
                     ]


def available_adducts():
    return map(itemgetter(0), _adduct_encodings)


def _table_colums():
    col_names = ["Score", "PubChemXlogP", "InChI", "IUPACName", "FragmenterScore_Values",
                 "MaximumTreeDepth", "MonoisotopicMass", "Identifier", "MolecularFormula",
                 "SMILES", "FormulasOfExplPeaks", "InChIKey2", "InChIKey1", "FragmenterScore",
                 "ExplPeaks", "NoExplPeaks", "NumberPeaksUsed"]
    col_types = [float, float, str, float, float, int, float, int, str, str, str, str, str, float,
                 str, int, int]
    col_formats = ["%%%s" % f for f in "ffsffdfdsssssfsdd"]

    return col_names, col_types, col_formats


def _empty_table():
    import emzed
    col_names, col_types, col_formats = _table_colums()
    return emzed.core.Table(col_names, col_types, col_formats, rows=[])


def _empty_data_frame():
    col_names, col_types, __ = _table_colums()
    df = pandas.DataFrame()
    for col_name, col_type in zip(col_names, col_types):
        df[col_name] = pandas.Series((), dtype=col_type)
    return df


def run_metfrag_on_emzed_spectrum(ms2_spec, adduct="M+H", settings=None, **kw):
    import emzed
    __, dmz, mode = emzed.adducts.get(adduct).adducts[0]
    m0 = (ms2_spec.precursors[0][0] - dmz) / abs(mode)
    positive_mode = ms2_spec.polarity == "+"
    ms2_peaks = ms2_spec.peaks.tolist()
    identifications = run_metfrag_on_peaklist(
        ms2_peaks, m0, None, adduct, positive_mode, settings, **kw)
    if identifications is None:
        return _empty_table()

    result = emzed.core.Table.from_pandas(identifications)

    for name in result.getColNames():
        if "Score" in name and "Values" not in name:
            result.setColType(name, float)
        elif name in ("PubChemXlogP", "MonoisotopicMass"):
            result.setColType(name, float)
        elif name in ("NoExplPeaks", "NumberPeaksUsed"):
            result.setColType(name, int)
        else:
            result.setColType(name, str)
    return result


def run_metfrag_on_peaklist(ms2_peaks, m0, mf=None, adduct="M+H", positive_mode=None, settings=None, **kw):

    allowed = available_adducts()
    assert adduct in allowed, "invalid adduct, allowed are %s" % ", ".join(
        allowed)

    for item in ms2_peaks:
        assert isinstance(
            item, (list, tuple)), "ms2_peaks is not a list/tuple of lists/tuples"
        assert len(
            item) == 2, "ms2_peaks is not a list of tuples/lists of length 2"
    assert positive_mode in (
        True, False), "need boolean value for positive_mode argument"

    result_path = _run_metfrag(
        ms2_peaks, m0, mf, adduct, positive_mode, settings, **kw)
    try:
        result = pandas.read_csv(result_path, sep="|")
    except:
        open(result_path, "r").close()
        # file can be opened for reading but has no valid csv content:
        return _empty_data_frame()
    return result


def _run_metfrag(ms2_peaks, m0, mf, adduct, positive_mode, settings, **kw):

    folder = tempfile.mkdtemp()
    peaklist_file_path = os.path.join(folder, "peaks.txt")
    with open(peaklist_file_path, "w") as fp:
        for (mz, ii) in ms2_peaks:
            print(mz, ii, file=fp)

    if settings is None:
        settings = standard_settings()
    settings.update(kw)
    settings["m0"] = m0
    settings["mf"] = mf
    settings["peaklist_file_path"] = peaklist_file_path
    settings["chemspider_token"] = None
    settings["result_file_name"] = "result"   # without .csv !
    settings["result_folder"] = folder
    settings["precursor_ion_mode"] = dict(_adduct_encodings)[adduct]
    settings["is_positive_mode"] = positive_mode

    if "proxy" in settings:
        proxy = settings.pop("proxy")
    else:
        proxy = None

    parameter_file = _create_template_file(**settings)

    parameter_file_path = os.path.join(folder, "parameter_file.txt")
    with open(parameter_file_path, "w") as fp:
        fp.write(parameter_file)

    if proxy is not None:
        if ":" in proxy:
            host, __, port = proxy.partition(":")
            extra = "-DproxySet=true -DproxyHost=%s -DproxyPort=%s" % (
                host, port)
        else:
            extra = "-DproxySet=true -DproxyHost=%s" % proxy
    else:
        extra = ""

    if sys.platform == "win32":
        with open(os.path.join(HERE, "metfrag22.l4j.ini"), "w") as fp:
            for line in extra.split(" "):
                print(line, file=fp)
        cmd_line = "%s/metfrag22.exe %s" % (HERE, parameter_file_path)
    else:
        cmd_line = "java %s -jar %s/MetFrag2.2-CL.jar %s" % (
            extra, HERE, parameter_file_path)
    return_code = os.system(cmd_line)
    if return_code:
        raise RuntimeError("calling metfrag as %r failed" % cmd_line)

    result_path = os.path.join(folder, "result.csv")
    return result_path
