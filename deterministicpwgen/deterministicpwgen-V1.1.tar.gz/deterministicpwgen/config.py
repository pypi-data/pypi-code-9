"""Module handling the configuration of deterministicpwgen."""

import ConfigParser
import backend
import os

config = ConfigParser.ConfigParser()

def config_file_exists(name="config"):
    """Checks if the config file for deterministicpwgen exists."""
    return os.path.isfile(backend.DIRECTORY + name)

def create_config_file(name="config"):
    backend.create_directory()

    config_file = open(backend.DIRECTORY + name, "w")

    config.add_section("deterministicpwgen")
    config.set("deterministicpwgen", "charset", "A")
    config.set("deterministicpwgen", "hide-seed", "")
    config.set("deterministicpwgen", "length", 16)

    config.set("deterministicpwgen", "keyfile", "prompt")
    config.set("deterministicpwgen", "password", "prompt")

    config.write(config_file)

def read(key, name="config"):
    config.read(backend.DIRECTORY + name)
    return config.get("deterministicpwgen", key)
