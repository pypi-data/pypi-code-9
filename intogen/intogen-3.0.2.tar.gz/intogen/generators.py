import logging
from configobj import ConfigObj
import fnmatch
import numpy
from intogen.utils import get_nested, set_nested
import os
import pandas

PROJECT_FILE_EXTENSION = '.smconfig'

ANNOTATION = "annotation"

POOL_PREFIX = "POOL_"

ALL_PROJECTS = 'global'

PROJECTS_DIR = "project"


class ProjectGroups():
    def __init__(self, outputs):
        self._outputs = outputs


    def __iter__(self):
        for out in self._outputs:
            yield out


class ProjectGroupsGenerator():
    def __init__(self, project_confs, results_dir="output"):
        self._project_confs = project_confs
        self._results_dir = results_dir

    def generate_groups(self, grouping_keys, project_file, output_files):
        outputs = []

        if ALL_PROJECTS in grouping_keys and grouping_keys.index(ALL_PROJECTS) > 0:
            pos = grouping_keys.index(ALL_PROJECTS)
            grouping_keys.insert(0, grouping_keys.pop(pos))

        for grouping_key in grouping_keys:
            groups = {}
            for project, config in self._project_confs.items():
                if project.startswith(POOL_PREFIX):
                    continue
                if grouping_key == ALL_PROJECTS:
                    # aggregate all projects
                    group = ALL_PROJECTS
                else:
                    # aggregate by indicated grouping_key
                    try:
                        group = config[ANNOTATION][grouping_key]
                        if " " in group:
                            group = group.replace(" ", "_")
                            config[ANNOTATION][grouping_key] = group

                    except KeyError:
                        logging.warning("Project '{}' does not contain GROUPING KEY annotation '{}'".format(project, grouping_key))
                        continue

                if group not in groups:
                    groups[group] = []
                groups[group].append(project)

            if len(groups) > 0:
                grouping_dir = os.path.join(self._results_dir, grouping_key)
                for group, projects in groups.items():
                    # create directory for output
                    if grouping_key == ALL_PROJECTS:
                        group_dir = grouping_dir
                    else:
                        group_dir = os.path.join(grouping_dir, group)
                    if not os.path.exists(group_dir):
                        os.makedirs(group_dir)

                    # collect files wanted
                    gene_files = []
                    for project in projects:
                        gene_files.append(os.path.join(self._results_dir, PROJECTS_DIR, project, project_file))

                    # append new entry to generator
                    outputs.append([gene_files, [os.path.join(group_dir, f) for f in output_files], grouping_key, group])
        return ProjectGroups(outputs)


class ProjectsGenerator():

    def complete_project_config(self, project_key, smconfig):
        # add annotations from annotations_file to smproject dict
        if self.annotations is not None:
            if project_key in self.annotations.index:
                smconfig = self.fill_in_annotations(project_key, smconfig)
            else:
                logging.info("No annotation found for '{}'".format(project_key))
        self._project_confs[project_key] = smconfig
        # add project-specific configuration from configuration files
        if self.configurations is not None and len(self.configurations) > 0:
            for config_table in self.configurations:
                if project_key in config_table.index:
                    smconfig = self.fill_in_configuration(project_key, smconfig, config_table)
        return smconfig

    def __init__(self, files, results_dir, annotation_file, config_files=[], pool_name=None):

        self.projects = []
        self._project_confs = {}
        self.results_path = os.path.join(results_dir, PROJECTS_DIR)
        self.config = {}
        self.outputs = []
        self.annotations = None

        # Read annotation table, if avilable
        if annotation_file is not None:
            if os.path.isfile(annotation_file):
                anndf = pandas.DataFrame.from_csv(annotation_file, sep="\t", index_col=0)
                self.annotations = anndf.where(pandas.notnull(anndf), other=None)
            else:
                logging.warning("Annotation file not a valid file: " + annotation_file)

        # Read configuration tables, if avilable
        self.configurations = None
        if len(config_files) > 0:
            self.configurations = []
            for f in config_files:
                confdf = pandas.read_csv(f, sep="\t", index_col=0, dtype=object)
                self.configurations.append(confdf.where(pandas.notnull(confdf), other=None))

        # Expand folders searching *.smconfig files
        for file in files:
            if os.path.isdir(file):
                for f in self.find_projects(file):
                    self.projects.append(f)
            else:
                self.projects.append(file)
        # add POOL project
        if pool_name is not None:
            self.projects.append(pool_name)

        # Create the output folder
        if not os.path.exists(self.results_path):
            os.makedirs(self.results_path)

        # Use absolutes paths always
        if not os.path.isabs(self.results_path):
            self.results_path = os.path.join(os.getcwd(), self.results_path)

        for file in self.projects:

            file_name = os.path.splitext(os.path.basename(file))
            extension = file_name[1]
            smconfig = ConfigObj()

            # Load project config
            if extension == PROJECT_FILE_EXTENSION:
                # smproject = json.load(open(file, 'r'))
                smconfig = ConfigObj(open(file), interpolation='intogen')
                project_key = smconfig.get('id', file_name[0])
                smconfig = self.complete_project_config(project_key, smconfig)

            elif file == pool_name:
                smconfig['id'] = project_key = POOL_PREFIX + pool_name
                smconfig = self.complete_project_config(pool_name, smconfig)

            else:
                # Manually create a smproject ConfigObj from inputfile
                project_key = file_name[0]
                smconfig['id'] = project_key
                smconfig['files'] = [file]
                smconfig = self.complete_project_config(project_key, smconfig)

            self.config[project_key] = self.absolute_file_paths(file, project_key, smconfig)

            # Create a folder for the project
            project_folder = os.path.join(self.results_path, project_key)
            if not os.path.exists(project_folder):
                os.mkdir(project_folder)

            # Create temporal folder
            temp_folder = os.path.join(project_folder, "temp")
            if not os.path.exists(temp_folder):
                os.mkdir(temp_folder)

            # Create input folder
            input_folder = os.path.join(project_folder, "variants")
            if not os.path.exists(input_folder):
                os.mkdir(input_folder)

            # Write smproject configuration file to the output-folder
            outfile_path = os.path.join(project_folder, project_key + PROJECT_FILE_EXTENSION)
            smconfig.filename = outfile_path
            smconfig.write()

            # The output file if not pool
            if file != pool_name:
                output_file = os.path.join(input_folder, 'variants')
                self.outputs.append([self.config[project_key]['files'], output_file, project_key])

    def absolute_file_paths(self, file, project_key, smproject):
        # Make relative path absolute
        smproject['files'] = [self.to_absolute(file, f) for f in smproject.get('files', [])]
        try:
            absolute = self.to_absolute(file, get_nested(smproject, ['oncodrivefm', 'genes_filter_file']))
            if absolute is not None:
                smproject = set_nested(smproject, ['oncodrivefm', 'genes_filter_file'], absolute)
        except KeyError:
            pass
        try:
            absolute = self.to_absolute(file, get_nested(smproject, ['oncodriveclust', 'genes_filter_file']))
            if absolute is not None:
                smproject = set_nested(smproject, ['oncodriveclust', 'genes_filter_file'], absolute)
        except KeyError:
            pass
        try:
            absolute = self.to_absolute(file, get_nested(smproject, ['mutsig', 'genes_filter_file']))
            if absolute is not None:
                smproject = set_nested(smproject, ['mutsig', 'genes_filter_file'], absolute)
        except KeyError:
            pass

        return smproject


    @staticmethod
    def to_absolute(basefile: str, path: str):
        if path is None:
            return None
        if not os.path.isabs(path):
            return os.path.join(os.path.dirname(basefile), path)
        else:
            return path

    def __iter__(self):

        for out in self.outputs:
            yield out

    def get_project_confs(self):
        return self._project_confs

    def fill_in_annotations(self, project_key, smproject):
        project_annotation = self.annotations.loc[project_key]

        if ANNOTATION not in smproject:
            smproject[ANNOTATION] = {}

        for ann_key in project_annotation.index:
            old = None
            if ann_key in smproject[ANNOTATION].keys():
                old = smproject[ANNOTATION][ann_key]
            new = project_annotation[ann_key]

            if new is not None and not (new is float and numpy.isnan(new)):
                smproject[ANNOTATION][ann_key] = new
                if old is not None and old != new:
                    logging.debug("Overwriting .smconfig annotation from annotation_file: project: '{}', "
                                  "old value: '{}', new value: '{}'".format(project_key, old, new))
        return smproject

    @staticmethod
    def find_projects(file, extension="*.smconfig"):
        matches = []
        for root, dirnames, filenames in os.walk(file):
            for filename in fnmatch.filter(filenames, extension):
                matches.append(os.path.join(root, filename))
        return matches


    @staticmethod
    def fill_in_configuration(project_key: str, smproject: ConfigObj, config_table: pandas.DataFrame):

        project_configuration = config_table.loc[project_key]

        for key in project_configuration.index:

            new = project_configuration[key]
            old = get_nested(smproject, key.split("."))

            if new is not None and not (new is float and numpy.isnan(new)):
                smproject = set_nested(smproject, key.split("."), new)

                if old is not None:
                    logging.info("Overwriting .smconfig configuration in '{}'. Config-Key: '{}'; "
                                 "Value (old/new): '{}' / '{}'".format(project_key, key, old, new))

        return smproject


