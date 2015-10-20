# -*- coding: utf-8 -*-
import os
import glob
import shutil

from pybuilder.core import init, task

__author__ = u"Martin Grůber"

try:
    string_types = basestring
except NameError:
    string_types = str


@init
def init_smart_copy_plugin(project, logger):
    project.set_property_if_unset("smart_copy_resources", {})
    project.set_property_if_unset("smart_copy_resources_basedir", project.basedir)

@task("smart_copy_resources", "Copy additional resources to required destinations")
def smart_copy_resources(project, logger):

    logger.info(u"Copying additional resource files")

    # Get the properties
    copy_source_dir = project.expand_path(project.get_property("smart_copy_resources_basedir"))
    resources_to_copy = project.get_property("smart_copy_resources")

    # There are no resources to copy
    if not resources_to_copy:
        logger.warn(u"No resources to copy configured. Consider removing plugin.")
        return
    # Check if resources_to_copy is a dict-like object
    if not isinstance(resources_to_copy, dict):
        logger.warn(u"Invalid smart_copy_resources property, it shall be a dict-like object")

    for glob_to_copy, copy_settings in resources_to_copy.items():
        copy_as = None
        glob_to_copy = project.expand(glob_to_copy)

        # Handle dict-like copy settings
        if isinstance(copy_settings, dict):
            if "destination" not in copy_settings:
                logger.warn(u"Missing 'destination' for resource: {}".format(glob_to_copy))
                return
            destinations = copy_settings["destination"]
            if "copy_as" in copy_settings:
                copy_as = copy_settings["copy_as"]
        else:
            destinations = copy_settings

        # Make it a list to allow multiple destinations
        if isinstance(destinations, string_types):
            destinations = [destinations]
        elif isinstance(destinations, list) or isinstance(destinations, tuple):
            pass
        else:
            logger.warn(u"Invalid settings for resource: {}".format(glob_to_copy))
            return

        # Get all the files using glob
        all_files = glob.glob(os.path.join(copy_source_dir, glob_to_copy))
        if len(all_files) < 1:
            logger.warn(u"No files found to copy in smart_copy_resources for pattern: {}".format(glob_to_copy))
            continue

        # Copy all the files
        for file_to_copy in all_files:
            # to all the destinations
            for destination in destinations:
                destination = project.expand(destination)
                destination = os.path.abspath(destination)
                smart_copy_resource(file_to_copy, os.path.basename(file_to_copy) if copy_as is None else copy_as, destination, logger, verbose=project.get_property("verbose"))

def smart_copy_resource(absolute_filename, relative_filename, target_directory, logger, verbose=False):
    absolute_target_file_name = os.path.join(target_directory, relative_filename)
    if verbose:
        logger.info(u"Copying resource {} to {}".format(absolute_filename, absolute_target_file_name))
    parent = os.path.dirname(absolute_target_file_name)
    if not os.path.exists(parent):
        os.makedirs(parent)
    shutil.copy(absolute_filename, absolute_target_file_name)
