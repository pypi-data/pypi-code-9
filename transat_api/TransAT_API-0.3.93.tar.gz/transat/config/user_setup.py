import os
import ConfigParser


def load():
    user_file = os.path.join(os.getcwd(), 'user_config.ini')
    if os.path.exists(user_file):
        Config = ConfigParser.ConfigParser()
        Config.read(user_file)
        env = {}
        for section in Config.sections():
            env[section] = ConfigSectionMap(Config, section)
        return env
    else:
        return _load()


def _load():
    env = {  #

             'wd': {
                 'local': 'simulations'
             },
             'tmb_path': {
                 'local': '/home/metrailler/TransATSuite/transatMB/build_opt/bin'
             },
             'path':{
             'ui': '/home/metrailler/TransATSuite/transatUI/bin',
             'freecad': '/usr/lib/freecad/lib',
             'db': 'db.json'}
             }
    return env


def ConfigSectionMap(Config, section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
        except:
            dict1[option] = None
    return dict1

