# -*- coding: utf-8 -*-


import os
import unicodecsv
from StringIO import StringIO


class ResultsWriter():

    ROBOT_LISTENER_API_VERSION = 2

    def start_suite(self, name, attributes):

        # Only if the testsuite contains testcases
        if len(attributes['tests']):

            # Output filename is composed of the current PID and the testsuite name
            self.__output_file = "output/{}-{}.csv".format(os.getpid(), name.lower().replace(" ", "_"))
            print self.__output_file

            # Create a memory file and write the csv header to it
            self.__output_memory = StringIO()
            csv_writer = unicodecsv.writer(self.__output_memory, delimiter='|', encoding='utf-8')
            csv_writer.writerow([
                "uri",
                "base_url",
                "environment",
                "type",
                "pattern",
                "searched",
                "expected",
                "found",
                "criticality",
                "release",
                "status",
                "message"])
        else:
            self.__output_file = None
            self.__output_memory = None

    def end_test(self, name, attributes):

        if self.__output_memory:

            # Parse test case tags in a dictionary
            tags = dict(tag.split(':', 1) for tag in attributes["tags"])

            # Write test case record in the current memory file
            csv_writer = unicodecsv.writer(self.__output_memory, delimiter='|', encoding='utf-8')
            csv_writer.writerow([
                tags["uri"] if ("uri" in tags) else "n.a.",
                tags["base_url"] if ("base_url" in tags) else "n.a.",
                tags["environment"] if ("environment" in tags) else "n.a.",
                tags["type"] if ("type" in tags) else "n.a.",
                tags["pattern"] if ("pattern" in tags) else "n.a.",
                tags["searched"] if ("searched" in tags) else "n.a.",
                tags["expected"] if ("expected" in tags) else "n.a.",
                tags["found"] if ("found" in tags) else "n.a.",
                tags["criticality"] if ("criticality" in tags) else "n.a.",
                tags["release"] if ("release" in tags) else "n.a.",
                attributes["status"],
                attributes["message"]])

    def end_suite(self, name, attributes):

        if self.__output_file and self.__output_memory:

            # Write the memory file on disk
            with open(self.__output_file, "a") as output_file:
                output_file.write(self.__output_memory.getvalue())
                self.__output_file = None

            self.__output_memory.close()
            self.__output_memory = None
