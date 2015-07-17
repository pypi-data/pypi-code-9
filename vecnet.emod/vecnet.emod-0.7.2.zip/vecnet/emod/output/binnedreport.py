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

import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(base_dir, "..", "tests", "output", "1")


class BinnedReport:
    def __init__(self, filename=None, data=None):
        if isinstance(filename, str):
            with open(filename) as fp:
                self.data = json.load(fp)
        elif isinstance(data, dict):
            self.data = data
        else:
            raise AttributeError("data should be a dict")

    @property
    def channels(self):
        """
        :return: List of channels in this BinnedReport
        :rtype: list
        """
        return [channel for channel in self.data["Channels"]]

    @property
    def axis(self):
        return [axis for axis in self.data["Header"]["Subchannel_Metadata"]["AxisLabels"]]

    def get_units(self, channel_name):
        if "ChannelUnits" in self.data:
            return self.data["ChannelUnits"][self.get_channel_number(channel_name)]
        else:
            # ChannelUnits is not available in EMOD v1.6 output
            return None

    def get_axis_number(self, axis_name):
        i = 0
        for axis in self.axis:
            if axis == axis_name:
                return i
            i += 1
        return None

    def get_meanings_per_axis(self, axis_name):
        axis_number = self.get_axis_number(axis_name)
        if axis_number is None:
            raise KeyError(axis_name)
        return self.data["Header"]["Subchannel_Metadata"]["MeaningPerAxis"][axis_number]

    def get_meaning_number(self, axis_name, meaning):
        i = 0
        for meaning_name in self.get_meanings_per_axis(axis_name):
            if meaning == meaning_name:
                return i
            i += 1
        return None

    def get_channel_number(self, name):
        i = 0
        for channel in self.data["ChannelTitles"]:
            if channel == name:
                return i
            i += 1
        return None

    def get_data(self, channel_name, axis_name, axis_meaning_name):
        meaning_number = self.get_meaning_number(axis_name, axis_meaning_name)
        if meaning_number is None:
            raise KeyError(axis_name + ": " + axis_meaning_name)
        return self.data["Channels"][channel_name]["Data"][meaning_number]

if __name__ == "__main__":
    # Usage examples
    binned_report = json.load(open(os.path.join(base_dir, "BinnedReport.json")))
    binned_report_obj = BinnedReport(binned_report)

    print binned_report_obj.get_channel_number("New Diagnostic Prevalence")
    print binned_report_obj.axis
    print binned_report_obj.channels[binned_report_obj.get_channel_number("New Diagnostic Prevalence")]

    print binned_report_obj.get_units(binned_report_obj.channels[binned_report_obj.get_channel_number("New Diagnostic Prevalence")])
    print binned_report_obj.get_meanings_per_axis("Age")
    print binned_report_obj.channels
    # channel[""]

    # print binned_report_obj.data["Population"]["Age"]["<1"]
    # print binned_report_obj.data
    print binned_report_obj.get_data("Population", "Age", "5-10")

    vector_species_report = BinnedReport(os.path.join(base_dir, "VectorSpeciesReport.json"))
    print vector_species_report.channels
    print vector_species_report.axis
    print vector_species_report.get_meanings_per_axis("Vector Species")
    print vector_species_report.get_data("Daily HBR", "Vector Species", "funestus")
    print vector_species_report.get_units("Daily HBR")

    vector_species_report = BinnedReport(os.path.join(base_dir, "VectorSpeciesReport.json"))
    print vector_species_report.get_data("Daily HBR", "Vector Species", "funestus")
