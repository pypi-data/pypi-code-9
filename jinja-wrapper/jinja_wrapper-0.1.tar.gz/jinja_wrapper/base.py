import glob
import os

from jinja_wrapper.helpers import *
from jinja_wrapper.settings import *

class JinjaWrapper(object):
    """
    jinja tasks
    """

    def __init__(self):
        """
        """

    def execute(self, args):
        """
        """
        search_path = JW_TEMPLATES_SEARCH_PATH
        template_path  = find_template(search_path, args.template)

        if not template_path:
            print("no template found")
            return

        exec_file_glob = glob.glob(join(template_path, JW_EXEC_PATTERN))
        if exec_file_glob:
            if len(exec_file_glob) == 1:
                exec_file = os.path.basename(exec_file_glob[0])
            else:
                print("ERROR: more than 1 exec file found: %s" %
                        exec_file_glob)
                return
            return write_file_template(exec_file, args.config, args.target,
                    {
                        'search_path':template_path
                        })
