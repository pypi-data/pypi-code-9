import lesscpy
import pathlib
import os
import logging

class LessProcessor:
    def process_file(filename, destination):
        old_path = os.getcwd()
        try:
            os.chdir(os.path.dirname(filename))
            destination = str(pathlib.PurePath(destination).with_suffix('.css'))
            with open(destination, 'w') as d:
                d.write(lesscpy.compile(filename))
        except Exception as e:
            logging.warning("Exception %s" % str(e))
            os.chdir(old_path)
