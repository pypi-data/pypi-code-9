import argparse
import logging
from intogen.tasks.intogen_task import IntogenTask
from os.path import dirname, exists
import os


class ConcatTask(IntogenTask):

    @staticmethod
    def get_configuration_definitions():
        return {}


    def run(self, input_files, output_file, has_header=True):

        logging.info("Concatenating {} files: {}".format(len(input_files), ",".join(input_files)))

        if not exists(dirname(output_file)):
            logging.info("creating {}".format(dirname(output_file)))
            os.makedirs(dirname(output_file))

        with open(output_file, "w") as output:

            if has_header:
                with open(input_files[0]) as data:
                    output.write(next(data))

            for file in input_files:
                with open(file, "r") as data:

                    if has_header:
                        next(data)

                    for line in data:
                        output.write(line)


def cmdline():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='append', dest='input_files', default=[])
    parser.add_argument('-o', dest='output_file')
    parser.add_argument('--has_header', dest='has_header', default=True, type=bool)
    options = parser.parse_args()

    # Run the command line
    task = ConcatTask()
    task.run(
        options.input_files,
        options.output_file,
        has_header=options.has_header
    )


if __name__ == "__main__":
    cmdline()