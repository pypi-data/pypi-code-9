from os import environ


def pytest_addoption(parser):
    parser.addini("env_files",
                  type="linelist",
                  help="a line separated list of env files to parse",
                  default=[])


def pytest_load_initial_conftests(args, early_config, parser):
    for file in early_config.getini("env_files"):
        parse_env_file(file)


def parse_env_file(file):
    with open(file) as fh:
        for line in fh:
            # skip comments and blank lines
            if line.startswith('#') or line.strip().__len__() == 0:
                continue
            # otherwise treat lines as environment variables in a KEY=VALUE combo
            key, value = line.split('=')
            environ[key.strip()] = value.strip()
