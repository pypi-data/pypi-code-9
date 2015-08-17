#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

""" Script to generate a json CubicWeb configuration file containing
dependencies used by the CW environment installer cw_install.py.
To fill with the values corresponding to the CW version.
"""

# System import
import json

# Define the cw setup version
version = "3.19"


hg_cubes = {
    "http://hg.logilab.org/review/cubes/bootstrap":
        ("bootstrap", "cubicweb-bootstrap-version-0.6.3", ""),
    "http://hg.logilab.org/review/cubes/brainomics":
        ("brainomics", "cubicweb-brainomics-version-0.9.0", ""),
    "http://hg.logilab.org/review/cubes/card":
        ("card", "cubicweb-card-version-0.5.3", ""),
    "http://hg.logilab.org/review/cubes/comment":
        ("comment", "cubicweb-comment-version-1.10.0", ""),
    "http://hg.logilab.org/review/cubes/file":
        ("file", "cubicweb-file-version-1.16.0", ""),
    "http://hg.logilab.org/review/cubes/forgotpwd":
        ("forgotpwd", "cubicweb-forgotpwd-version-0.4.2", ""),
    "http://hg.logilab.org/review/cubes/genomics":
        ("genomics", "cubicweb-genomics-version-0.8.1", ""),
    "http://hg.logilab.org/review/cubes/jqplot":
        ("jqplot", "cubicweb-jqplot-version-0.4.0", ""),
    "http://hg.logilab.org/review/cubes/medicalexp":
        ("medicalexp", "cubicweb-medicalexp-version-0.10.0", ""),
    "http://hg.logilab.org/review/cubes/neuroimaging":
        ("neuroimaging", "cubicweb-neuroimaging-version-0.6.0", ""),
    "http://hg.logilab.org/review/cubes/preview":
        ("preview", "cubicweb-preview-version-1.1.0", ""),
    "http://hg.logilab.org/review/cubes/questionnaire":
        ("questionnaire", "cubicweb-questionnaire-version-0.6.0", ""),
    "http://hg.logilab.org/review/cubes/squareui":
        ("squareui", "cubicweb-squareui-version-0.3.3", ""),
    "http://hg.logilab.org/review/cubes/seo":
        ("seo", "cubicweb-seo-version-0.2.0", ""),
    "http://hg.logilab.org/review/cubes/trustedauth":
        ("trustedauth", "cubicweb-trustedauth-version-0.3.0", ""),
    "http://hg.logilab.org/review/cubes/dataio":
        ("dataio", "cubicweb-dataio-version-0.5.0", ""),
    "http://hg.logilab.org/review/cubes/container":
        ("container", "cubicweb-container-version-2.4.0", ""),
    "http://hg.logilab.org/review/cubes/rqlcontroller":
        ("rqlcontroller", "cubicweb-rqlcontroller-version-0.1.0", ""),
}

git_cubes = {
    "https://github.com/neurospin/rql_download.git":
        ("rql_download", None, "rql_download"),
    "https://github.com/neurospin/rql_upload.git":
        ("rql_upload", None, "rql_upload"),
    #"https://github.com/neurospin/piws.git":
    #    ("piws", None, "piws"),
}

pypi_tools = [
    "pyasn1"
]

json_data = {
    "version": version,
    "hg_cubes": hg_cubes,
    "git_cubes": git_cubes,
    "pypi_tools": pypi_tools
}

with open("{0}.conf".format(version), "w") as open_file:
    json.dump(json_data, open_file)
