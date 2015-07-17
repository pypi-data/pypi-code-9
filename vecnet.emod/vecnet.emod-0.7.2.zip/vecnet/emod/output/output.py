#!/usr/bin/python
#
# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Functions and classes for working with EMOD output files
"""
import json
import os
import csv
from zipfile import ZipFile
import StringIO
from vecnet.emod.output.binnedreport import BinnedReport
import zipfile

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(base_dir, "..", "tests", "output", "1")

def convert_emod_output_to_csv(*files):
    """
    Covert EMOD output files to a csv file
    :param files: argument list of EMOD output files (open files, strings and dict are accepted)
    :return: contents of csv file
    :rtype: str
    """
    table = []
    field_names = ["Timestep"]

    for file_content in files:
        if file_content is None:
            # To simplify convert_to_csv function
            # if one or more outputs are missing, we will pass None instead of file contents
            continue
        if hasattr(file_content, "read"):
            file_content = json.load(file_content)
        if isinstance(file_content, (str, unicode)):
            file_content = json.loads(file_content)
        if not isinstance(file_content, dict):
            raise TypeError("Open file, string or dict arguments are accepted")

        if not table:
            # Add timesteps column
            timesteps = file_content["Header"]["Timesteps"]
            for i in range(0, timesteps):
                table.append({"Timestep": i})

        if "Subchannel_Metadata" in file_content["Header"]:
            # BinnedReport or VectorSpeciesReport
            binned_report = BinnedReport(data=file_content)
            for channel in binned_report.channels:
                assert len(binned_report.axis) == 1
                axis = binned_report.axis[0]
                for species in binned_report.get_meanings_per_axis(axis):
                        data = binned_report.get_data(channel, axis, species)
                        for i in range(0, len(data)):
                            table[i][channel + ": " + species] = data[i]
                        field_names.append(channel + ": " + species)
        else:
            # InsetChart or DemographicsSummary
            for channel in file_content["Channels"]:
                data = file_content["Channels"][channel]["Data"]
                for i in range(0, len(data)):
                    table[i][channel] = data[i]
                field_names.append(channel)

    # Write CSV file
    fp = StringIO.StringIO()
    writer = csv.DictWriter(fp, fieldnames=field_names)
    writer.writeheader()
    for row in table:
        writer.writerow(row)
    contents = fp.getvalue()
    fp.close()
    return contents

def convert_to_csv(output_dir):
    filename = os.path.join(output_dir, "InsetChart.json")
    output_filename = "output.csv"
    inset_chart = json.load(open(filename))
    try:
        with open(os.path.join(output_dir, "DemographicsSummary.json")) as fp:
            demographics_summary = json.load(fp)
    except IOError:
        # No DemographicsSummary.json
        demographics_summary = None

    table = []
    field_names = ["Timestep"]

    timesteps = inset_chart["Header"]["Timesteps"]
    for i in range(0, timesteps):
        table.append({"Timestep": i})

    # Add data from InsetCharts.json
    for channel in inset_chart["Channels"]:
        data = inset_chart["Channels"][channel]["Data"]
        for i in range(0, len(data)):
            table[i][channel] = data[i]
        field_names.append(channel)

    # Add data from DemographicsSummary.json
    if demographics_summary is not None:
        for channel in demographics_summary["Channels"]:
            data = demographics_summary["Channels"][channel]["Data"]
            for i in range(0, len(data)):
                table[i][channel] = data[i]
            field_names.append(channel)

    # Add data from VectorSpeciesReport.json
    try:
        vector_species_report = BinnedReport(os.path.join(output_dir, "VectorSpeciesReport.json"))
        for channel in vector_species_report.channels:
            for species in vector_species_report.get_meanings_per_axis("Vector Species"):
                    data = vector_species_report.get_data(channel, "Vector Species", species)
                    for i in range(0, len(data)):
                        table[i][channel + ": " + species] = data[i]
                    field_names.append(channel + ": " + species)
    except IOError:
        # No VectorSpeciesReport.json, move on
        pass

    # Add data from BinnedReport.json
    try:
        binned_report = BinnedReport(os.path.join(output_dir, "BinnedReport.json"))
        for channel in binned_report.channels:
            for species in binned_report.get_meanings_per_axis("Age"):
                    data = binned_report.get_data(channel, "Age", species)
                    for i in range(0, len(data)):
                        table[i][channel + ": " + species] = data[i]
                    field_names.append(channel + ": " + species)
    except IOError:
        # No BinnedReport.json, move on
        pass

    # Write CSV file
    with open(os.path.join(output_dir, output_filename), "wb") as fp:
        writer = csv.DictWriter(fp, fieldnames=field_names)
        writer.writeheader()
        for row in table:
            writer.writerow(row)

    # Zip and compress CSV file
    with ZipFile(os.path.join(output_dir, "%s.zip" % output_filename), 'w') as myzip:
        myzip.write(os.path.join(output_dir, output_filename), output_filename, zipfile.ZIP_DEFLATED)
    return table

if __name__ == "__main__":
    convert_to_csv(base_dir)
    fp = open(os.path.join(base_dir, "test.csv"), "wb")
    print >>fp, convert_emod_output_to_csv(open(os.path.join(base_dir, "InsetChart.json")),
                                           json.load(open(os.path.join(base_dir, "BinnedReport.json"))),
                                           None,
                                           open(os.path.join(base_dir, "DemographicsSummary.json")).read(),
                                           )
    fp.close()
