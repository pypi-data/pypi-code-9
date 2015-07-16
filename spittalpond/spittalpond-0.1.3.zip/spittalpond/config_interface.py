import argparse
import os
import logging
import time
import datetime

import pytoml
import spittalpond

logger = logging.getLogger('spittalpond')

def verify_config(config):
    """ Verifies the config dictionary-like object for correctness.

    Also creates any unspecified optional config key-value pairs. This ensures
    that every recognized key in the config dictionary is safe to use and will
    not raise a KeyError.

    Args:
        config (dict): A python dictionary containing the config data.

    Returns:
        bool: True if the config passes all "tests".
              If config does not pass all "tests" an exception will be raised.
    """

    def quick_msg(msg):
        return ' '.join([prefix, msg, suffix])

    if 'meta' in config.keys():
        prefix = "FATAL:"
        suffix = "not specified in the meta section!"
        if 'url' not in config['meta'].keys():
            raise Exception(quick_msg("URL"))
        # TODO: Handle "turning off" logging here if file unspecfied.
        if 'log_level' not in config['meta'].keys():
            config['meta']['log_level'] = "INFO"

    if 'login' not in config.keys():
        prefix = "FATAL:"
        suffix = "not specified in the login section!"
        if 'user' not in config['login'].keys():
            raise Exception(quick_msg("user"))
        elif 'password' not in config['login'].keys():
            raise Exception(quick_msg("password"))

    def validate_upload_sections(section, prefix="", suffix=""):
        def pre_ssn(string, sub):
            """ Prepends the subsection name to a string. """
            return sub + "." + string

        if 'do_timestamps' not in section.keys():
            section['do_timestamps'] = True
        if 'directory_path' not in section.keys():
            raise Exception(quick_msg('directory_path'))
        categories = {k: v for k, v in section.iteritems()\
                      if k in ['dict', 'version']}
        for cat_name, category in categories.iteritems():
            for name, value in category.iteritems():
                fuller_name = cat_name + "." + name
                if 'filename' not in value.iterkeys():
                    raise Exception(
                        quick_msg(pre_ssn('filename', fuller_name))
                    )
                if 'module_supplier_id' not in value.iterkeys():
                    raise Exception(
                        quick_msg(pre_ssn('module_supplier_id', fuller_name))
                    )

    if 'model' in config.keys():
        prefix = "FATAL:"
        suffix = "not specified in the model section!"
        # If user wants to select keys manually, else...
        if 'select_manually' in config['model'].keys():
            pass
        else:
            validate_upload_sections(config['model'], prefix, suffix)

    if 'exposure' in config.keys():
        prefix = "FATAL:"
        suffix = "not specified in the exposure section!"
        validate_upload_sections(config['exposure'], prefix, suffix)

    if 'benchmark' in config.keys():
        prefix = "FATAL:"
        suffix = "not specified in the benchmark section!"
        if 'name' not in config['benchmark'].keys():
            raise Exception(quick_msg('name'))
        if 'chunk_size' not in config['benchmark'].keys():
            raise Exception(quick_msg('chunk_size'))
        if 'min_chunk' not in config['benchmark'].keys():
            raise Exception(quick_msg('min_chunk'))
        if 'max_chunk' not in config['benchmark'].keys():
            raise Exception(quick_msg('max_chunk'))

    if 'gul' in config.keys():
        prefix = "FATAL:"
        suffix = "not specified in the gul section!"
        if 'name' not in config['gul'].keys():
            raise Exception(quick_msg('name'))

    if 'pubgul' in config.keys():
        prefix = "FATAL:"
        suffix = "not specified in the pubgul section!"
        if 'name' not in config['pubgul'].keys():
            raise Exception(quick_msg('name'))
        if 'filename' not in config['pubgul'].keys():
            raise Exception(quick_msg('filename'))
        if 'output_filepath' not in config['pubgul'].keys():
            raise Exception(quick_msg('output_filepath'))
        if 'module_supplier_id' not in config['pubgul'].keys():
            raise Exception(quick_msg('module_supplier_id'))

    return True


def prepare_files_in_section(spittal_sub_instance, section):
    """ Prepares all specified files in a section.

    Args:
        spittal_sub_instance (SpittalBase):
            Any object that inherits from SpittalBase.
        section (dict):
            Dict epresentation of model or exposure config section.
    """

    # With s being config section and p being Oasis profile type.
    for skey, sitems in section.iteritems():
        if skey in ['dict', 'version']:
            for pkey, pitems in sitems.iteritems():
                data_name = skey + "_" + pkey
                filepath = os.path.join(
                    section['directory_path'],
                    pitems['filename']
                )
                spittal_sub_instance.prepare_file(
                    data_name,
                    filepath,
                    pitems['module_supplier_id'],
                    section['do_timestamps']
                )


def run_model(spittal_instance, config):
    """ Run model section of the config.

    This method assumes that the config is already validated and we are logged
    in.

    Args:
        spittal_instance (SpittalPond): SpittalPond object to run with.
        config (dict): Contains specific details for running the model.
    """

    spit = spittal_instance
    prepare_files_in_section(spit.model, config['model'])
    spit.model.create_model_structures()
    spit.model.model_do_jobs()


def run_exposure(spittal_instance, config):
    """ Run exposure section of the config.

    This method assumes that the config is already validated and we are logged
    in.

    Args:
        spittal_instance (SpittalPond): SpittalPond object to run with.
        config (dict): Contains specific details for running the model.
    """

    spit = spittal_instance
    prepare_files_in_section(spit.exposure, config['exposure'])
    spit.exposure.create_exposure_structure(spit.model.data_dict)
    spit.exposure.exposure_do_jobs()


def runner(config_file):
    """ Parse config file and makes the appropriate Oasis API call as needed."""

    start_time = time.time()
    # Load the config file into a toml object.
    with open(config_file, 'rb') as f:
        config = pytoml.load(f)

    verify_config(config)

    # If the config verifies we can assume that it has a legit login section.
    spit = spittalpond.SpittalPond(
        config['meta']['url'],
        config['login']['user'],
        log_file=config['meta']['log_file'],
        log_level=config['meta']['log_level'],
    )

    spit.model.do_login(config['login']['password'])

    if 'model' in config.keys():
        # If user wants to select keys manually, else...
        if 'select_manually' in config['model'].keys():
            spit.model.select_manually()
        else:
            run_model(spit, config)

    if 'exposure' in config.keys():
        # TODO: We shouldn't have to log in twice. Instead share cookies.
        spit.exposure.do_login(config['login']['password'])
        run_exposure(spit, config)

    if 'benchmark' in config.keys():
        spit.exposure.create_benchmark_structure(
            config['benchmark']['name']
        )

    if 'gul' in config.keys():
        # TODO: We shouldn't have to log in twice. Instead share cookies.
        spit.run.do_login(config['login']['password'])
        spit.run.auto_create_random_numbers()
        spit.run.create_gul_data(
            config['gul']['name'],
            spit.exposure.data_dict['kernel_benchmark']['taskId'],
            spit.exposure.data_dict['instance_exposure']['taskId'],
        )

    if 'pubgul' in config.keys():
        # TODO: We shouldn't have to log in twice. Instead share cookies.
        spit.run.do_login(config['login']['password'])
        response = spit.run.get_gul_data(
            config['pubgul']['name'],
            config['pubgul']['filename'],
            config['pubgul']['module_supplier_id']
        )
        with open(config['pubgul']['output_filepath'], 'wb') as output_file:
            output_file.write(response.content)
        print "Saved Published GUL output to {filepath}.".format(
            filepath=config['pubgul']['output_filepath']
        )

    seconds_elapsed = time.time() - start_time
    print "Time taken to run config: {time_elapsed} ".format(
        time_elapsed=datetime.timedelta(seconds=seconds_elapsed)
    )
    return spit


if __name__ == "__main__":
    # Grab the first argument passed. This is the file name.
    parser = argparse.ArgumentParser(
        description="Makes Oasis API calls according to the TOML config file \
                     specified."
        )
    parser.add_argument(
        "config_file",
        metavar="file",
        type=str,
        help="the path to the TOML config file for Spittalpond to run."
    )
    args = parser.parse_args()

    spittalpond_instance = runner(args.config_file)
    logger.info("Succesfully finished running the config interface!")
