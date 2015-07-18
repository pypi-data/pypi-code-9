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

import csv
import json
import itertools
import os
import sys
import datetime


def main():
    if len(sys.argv) < 2:
        print "Usage: generate_sweeps <ExperimentSpecification.json>"
        # exit() does not seem to be supported by embedded python library, so using sys.exit() instead
        sys.exit(0)
    filename = sys.argv[1]

    try:
        generate_scenarios(filename)
    except KeyError as e:
        print "Sweep generation failed"
        print "Can't find parameter %s" % e
        raw_input("Press Enter to continue ...")


def generate_scenarios(filename, base_dir=None):
    with open(filename) as fp:
        experiment_specification = json.load(fp)
    exp = ExperimentSpecification(experiment_specification)
    print "Number of scenarios to be generated: %s" % len(exp)
    if len(exp) > 1000:
        print "WARNING: experiments of size more that 1000 are not recommended"
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(filename))
    timestamp = datetime.datetime.now()
    number = exp.generate_scenarios(base_dir)
    print "%s scenarios generated in %s" % (number, datetime.datetime.now() - timestamp)
    raw_input("Press Enter to continue...")


def delete_emod_parameter(config, *parameter_path):
    # There is no syntax to delete a parameter in a sweep currently
    # But this piece of code seems to work
    sub_section_of_config = config
    prev_sub_section_of_config = sub_section_of_config

    if len(parameter_path) == 0:
        raise TypeError
    param = parameter_path[-1]  # Last parameter in the parameter_path

    for param in parameter_path:
        if ']' in param:
            # 0] , 1] etc  - index in array
            param = int(param[:-1])
        prev_sub_section_of_config = sub_section_of_config
        sub_section_of_config = sub_section_of_config[param]
    if isinstance(prev_sub_section_of_config, dict):
        prev_sub_section_of_config.pop(param)
    elif isinstance(prev_sub_section_of_config, list):
        prev_sub_section_of_config.pop(int(param))

    return config


def update_emod_parameter(config, *parameter_path, **kwargs):
    # Consider this a prototype of jsonpath parser implementation (with no eval, unlike jsonpath lib!)
    sub_section_of_config = config
    prev_sub_section_of_config = sub_section_of_config

    if len(parameter_path) == 0:
        raise TypeError
    param = parameter_path[-1]  # Last parameter in the parameter_path

    for param in parameter_path:
        if ']' in param:
            # 0] , 1] etc  - index in array
            param = int(param[:-1])
        prev_sub_section_of_config = sub_section_of_config
        sub_section_of_config = sub_section_of_config[param]
    prev_sub_section_of_config[param] = kwargs["value"]
    return config


def updated_input_file(parameter, replacement, input_files):
    filename = parameter.split("/")[0]
    if filename not in input_files:
        # Assume config.json.
        # Warning - danger zone if there is a typo in filename
        filename = "config.json"
        jsonpath = parameter.replace('[', '/').split("/")
        jsonpath.insert(0, "parameters")
    else:
        jsonpath = parameter.replace('[', '/').split("/")[1:]

    if isinstance(input_files[filename], dict):
        contents = update_emod_parameter(input_files[filename],
                                         *jsonpath,
                                         value=replacement)
    else:
        raise TypeError("%s is not a valid JSON file or is a compiled demographics files, "
                        "can't sweep on it" % filename)

    return filename, contents


class ExperimentArm(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name


class ExperimentSpecification(object):
    def __init__(self, experiment_specification):
        if isinstance(experiment_specification, str):
            experiment_specification = json.loads(experiment_specification)
        if hasattr(experiment_specification, "read"):
            experiment_specification = json.load(experiment_specification)
        if not isinstance(experiment_specification, dict):
            raise TypeError("experiment_specification should be a string, open file or a dict")
        self.experiment_specification = experiment_specification

    @property
    def number_of_combinations(self):
        n = 1
        for parameter, values in self.experiment_specification["simple_sweep"].iteritems():
            if not isinstance(values, (dict, list)):
                values = [values]
            n *= len(values)
        return n

    def __len__(self):
        return self.number_of_combinations

    def combinations(self):
        sweeps = []
        sweep_names = []
        for parameter, value in self.experiment_specification["simple_sweep"].iteritems():
            if isinstance(value, dict):
                value = [ExperimentArm(item_name, value=item) for item_name, item in value.iteritems()]
            if not isinstance(value, list):
                value = [value]
            sweeps.append(value)
            sweep_names.append(parameter)
        for sweep in itertools.product(*sweeps):
            yield dict(zip(sweep_names, sweep))

    def generate_scenarios(self, base_dir=None):
        cwd = os.getcwd()
        if base_dir is not None and base_dir != '':
            os.chdir(base_dir)
        try:
            input_files = {}

            for filename in self.experiment_specification["input_files"]:
                if "/" in filename or "\\" in filename:
                    # Files in subdirectory are not supported yet
                    raise ValueError("Input files should reside in the same folder as experiment specification")
                with open(filename, "rb") as fp:
                    content = fp.read()
                    try:
                        input_files[filename] = json.loads(content)
                        if "StringTable" in input_files[filename]:
                            # This may be a compiled demographics file, skipping
                            raise ValueError("%s is a compiled demographics file" % filename)
                    except ValueError:
                        # Not a valid JSON file or compiled demographics file - copy only
                        input_files[filename] = content

            try:
                os.mkdir("scenarios")
                os.chdir("scenarios")
            except WindowsError:
                raise TypeError("ERROR: scenarios directory already exists, "
                                "cowardly refusing to clobber existing directory")

            number_of_scenarios_generated = 0
            scenario_csv = []
            for combination in self.combinations():
                number_of_scenarios_generated += 1

                for parameter in combination:
                    replacement = combination[parameter]
                    if isinstance(replacement, ExperimentArm):
                        for arm in replacement.value:
                            # Apply each arm to input files
                            filename, contents = updated_input_file(arm, replacement.value[arm], input_files)
                            input_files[filename] = contents
                    else:
                        filename, contents = updated_input_file(parameter, replacement, input_files)
                        input_files[filename] = contents
                # save files to a subdirectory
                try:
                    # Make a subdirectory
                    os.mkdir(str(number_of_scenarios_generated))
                except OSError:
                    pass

                for filename in input_files:
                    with open(os.path.join(str(number_of_scenarios_generated), filename), "wb") as fp:
                        if isinstance(input_files[filename], dict):
                            json.dump(input_files[filename], fp=fp, indent=4, sort_keys=True)
                        else:
                            fp.write(input_files[filename])
                combination["scenario"] = number_of_scenarios_generated
                scenario_csv.append(combination)

            try:
                os.chdir("..")
                fp = open("scenarios.csv", "wb")
                fieldnames = [parameter for parameter in self.experiment_specification["simple_sweep"]]
                fieldnames.insert(0, "scenario")
                writer = csv.DictWriter(fp, fieldnames=fieldnames)
                writer.writeheader()
                for row in scenario_csv:
                    writer.writerow(row)
                fp.close()
            except IOError as e:
                print "Can't save scenarios.csv: %s" % e
                print "Check if it is open in Excel."
            os.chdir(cwd)
            return number_of_scenarios_generated
        except:
            os.chdir(cwd)
            raise

if __name__ == "__main__":
    main()
