
import os
import os.path

_DEFAULT_SEGGER_ROOT_PATH = r'C:\Program Files (x86)\SEGGER'


def find_latest_dll():
    
    dir_list = [os.path.join(_DEFAULT_SEGGER_ROOT_PATH, folder) for folder in os.listdir(_DEFAULT_SEGGER_ROOT_PATH) if os.path.isdir(os.path.join(_DEFAULT_SEGGER_ROOT_PATH, folder))]
    if len(dir_list) == 0:
        return None
    
    versioned_list_dir = [(dir, _find_jlink_version_info(dir)) for dir in dir_list]
    sorted_versioned_list_dir = sorted(versioned_list_dir, key = lambda x: x[1])
    
    return os.path.join(sorted_versioned_list_dir[-1][0], 'JLinkARM.dll')
    
    
def _find_jlink_version_info(segger_dir):
    
    return segger_dir[segger_dir.index('V') + 1:]
    