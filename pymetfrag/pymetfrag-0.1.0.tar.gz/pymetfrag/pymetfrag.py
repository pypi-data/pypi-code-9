# encoding: utf-8
from __future__ import print_function

import os
import sys
from operator import itemgetter

import multiprocessing
import subprocess
import tempfile

import pandas


class CallToMetfragFailed(Exception):
    pass


HERE = os.path.dirname(os.path.abspath(__file__))


def default_template():
    path = os.path.join(HERE, "parameter_file_template.txt")
    try:
        return open(path, "r").read()
    except IOError:
        raise RuntimeError("pymetfrag installation is broken, can not read %s" % path)


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
        precursor_setting = """NeutralPrecursorMolecularFormula = {}""".format(mf)

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
            "num_threads": multiprocessing.cpu_count() - 1,
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


def _run_metfrag(ms2_peaklist, m0, mf, adduct, positive_mode, settings, **kw):

    folder = tempfile.mkdtemp()
    peaklist_file_path = os.path.join(folder, "peaks.txt")
    with open(peaklist_file_path, "w") as fp:
        for (mz, ii) in ms2_peaklist:
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
            extra = "-DproxySet=true -DproxyHost=%s -DproxyPort=%s" % (host, port)
        else:
            extra = "-DproxySet=true -DproxyHost=%s" % proxy
    else:
        extra = ""

    extra += "-Djava.io.tmpdir=%s" % tempfile.mkdtemp()

    if sys.platform == "win32":
        with open(os.path.join(HERE, "metfrag22.l4j.ini"), "w") as fp:
            for line in extra.split(" "):
                print(line, file=fp)
        cmd_line = "%s/metfrag22.exe %s" % (HERE, parameter_file_path)
    else:
        cmd_line = "java %s -jar %s/MetFrag2.2-CL.jar %s" % (extra, HERE, parameter_file_path)

    return_code = subprocess.call(cmd_line.split(" "), shell=False)
    if return_code:
        raise CallToMetfragFailed("calling metfrag as %r failed" % cmd_line)

    result_path = os.path.join(folder, "result.csv")
    return result_path


def _run_in_parallel(function, args, n_threads):

    import threading
    import Queue

    def _run(func, qin, qout):
        while True:
            item = qin.get()
            if item is not None:
                idx, kw = item
                try:
                    result = func(**kw)
                except Exception, e:
                    result = e
                qout.put((idx, result))
            else:
                break

    qin = Queue.Queue()
    qout = Queue.Queue()

    for i, arg in enumerate(args):
        qin.put((i, arg))

    for _ in range(n_threads):
        qin.put(None)

    threads = []
    for _ in range(n_threads):
        t = threading.Thread(target=_run, args=(function, qin, qout))
        threads.append(t)
        t.start()

    results = []
    for _ in range(len(args)):
        results.append(qout.get())

    results.sort()
    return [item for (i, item) in results]


def run_metfrag_on_emzed_spectrum(ms2_spec, adduct="M+H", settings=None, **kw):
    import emzed
    __, dmz, mode = emzed.adducts.get(adduct).adducts[0]
    m0 = (ms2_spec.precursors[0][0] - dmz) / abs(mode)
    positive_mode = ms2_spec.polarity == "+"
    ms2_peaklist = ms2_spec.peaks.tolist()

    identifications = run_metfrag_on_peaklist(ms2_peaklist, m0, None, adduct, positive_mode,
                                              settings, **kw)

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


def run_metfrag_on_emzed_spectra(ms2_specs, adduct_or_adducts, num_workers=None, settings=None,
                                 **kw):

    # check arguments
    assert isinstance(ms2_specs, (list, tuple)), "ms2_specs should be list or tuple of strings"
    if not isinstance(adduct_or_adducts, (list, tuple)):
        adducts = [adduct_or_adducts] * len(ms2_specs)
    else:
        adducts = adduct_or_adducts
        assert len(adducts) == len(ms2_specs), ("need as many adducts as ms2_specs or single "
                                                "adduct for all spectra")
    assert isinstance(adducts, (list, tuple)), "adducts should be list or tuple of strings"

    # setup parameters for parallel calls
    if settings is None:
        settings = standard_settings()
    settings.update(kw)
    items = []
    for ms2_spec, adduct in zip(ms2_specs, adducts):
        items.append({"ms2_spec": ms2_spec, "adduct": adduct, "settings": settings})

    # run in parallel
    if num_workers is None:
        num_workers = min(len(items), 10)
    results = _run_in_parallel(run_metfrag_on_emzed_spectrum, items, num_workers)

    # check results
    import emzed

    tables = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            raise result
        if not isinstance(result, emzed.core.Table):
            raise RuntimeError("expected emzed.core.Table but got %r" % result)
        result.addColumn("spec_id", i, insertBefore=0)
        tables.append(result)

    return emzed.utils.stackTables(tables)


def run_metfrag_on_peaklist(ms2_peaklist, m0, mf=None, adduct="M+H", positive_mode=None, settings=None, **kw):

    allowed = available_adducts()
    assert adduct in allowed, "invalid adduct, allowed are %s" % ", ".join(
        allowed)

    for item in ms2_peaklist:
        assert isinstance(
            item, (list, tuple)), "ms2_peaklist is not a list/tuple of lists/tuples"
        assert len(
            item) == 2, "ms2_peaklist is not a list of tuples/lists of length 2"
    assert positive_mode in (
        True, False), "need boolean value for positive_mode argument"

    result_path = _run_metfrag(
        ms2_peaklist, m0, mf, adduct, positive_mode, settings, **kw)
    try:
        result = pandas.read_csv(result_path, sep="|")
    except Exception:
        open(result_path, "r").close()
        # file can be opened for reading but has no valid csv content:
        return _empty_data_frame()
    return result


def run_metfrag_on_peaklists(ms2_peak_lists, m0s, mfs=None, adducts="M+H", positive_mode=None,
                             num_workers=None, settings=None, **kw):

    n = len(ms2_peak_lists)
    if isinstance(adducts, basestring):
        adducts = n * [adducts]
    assert len(adducts) == n
    assert len(m0s) == n
    if mfs is not None:
        assert len(mfs) == n
    else:
        mfs = [None] * n

    # setup parameters for parallel calls
    if settings is None:
        settings = standard_settings()
    settings.update(kw)
    items = []
    for ms2_peaklist, m0, mf, adduct in zip(ms2_peak_lists, m0s, mfs, adducts):
        items.append({"ms2_peaklist": ms2_peaklist, "m0": m0, "mf": mf, "adduct": adduct,
                      "positive_mode": positive_mode, "settings": settings})

    # run in parallel
    if num_workers is None:
        num_workers = min(len(items), 10)
    results = _run_in_parallel(run_metfrag_on_peaklist, items, num_workers)

    data_frames = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            raise result
        if not isinstance(result, pandas.DataFrame):
            raise RuntimeError("expected pandas.DataFrame but got %r" % result)
        result.insert(0, "spec_id", i)
        data_frames.append(result)

    return pandas.concat(data_frames)
