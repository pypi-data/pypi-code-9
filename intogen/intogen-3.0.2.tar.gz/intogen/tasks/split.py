import argparse
from intogen.tasks.intogen_task import IntogenTask
import os


class SplitTask(IntogenTask):

    @staticmethod
    def get_configuration_definitions():
        return {}

    def run(self, input_file, output_files, pattern='*.part', max_rows=200, has_header=True):

        exec_config = self.get_exec_config()

        output_files = [] if output_files is None else output_files

        for output_file in output_files:
            os.unlink(output_file)

        output_files = []

        with open(input_file, "r") as data:

            if has_header:
                header = next(data)

            chunck_count = 0
            line_count = 0

            file_name = input_file + '.' + pattern.replace('*', "%05d" % chunck_count)
            out = open(file_name, 'w')
            output_files.append(file_name)

            if has_header:
                out.write(header)

            for line in data:
                if line_count < max_rows:
                    out.write(line)
                    line_count += 1
                else:

                    # Open next chunk
                    chunck_count += 1
                    line_count = 0
                    out.close()
                    file_name = input_file + '.' + pattern.replace('*', "%05d" % chunck_count)
                    out = open(file_name, 'w')
                    output_files.append(file_name)

                    if has_header:
                        out.write(header)

                    out.write(line)

            out.close()

        return output_files


def cmdline():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file')
    parser.add_argument('-o', action='append', dest='output_files')
    parser.add_argument('--pattern', dest='pattern', default='*.part')
    parser.add_argument('--max_rows', dest='max_rows', default=200, type=int)
    parser.add_argument('--has_header', dest='has_header', default=True, type=bool)
    options = parser.parse_args()

    # Run the command line
    task = SplitTask()
    task.run(
        options.input_file,
        options.output_files,
        pattern=options.pattern,
        max_rows=options.max_rows,
        has_header=options.has_header
    )


if __name__ == "__main__":
    cmdline()