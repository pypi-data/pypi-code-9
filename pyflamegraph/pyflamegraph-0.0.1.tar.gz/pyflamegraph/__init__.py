import os.path
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile


class FlamegraphException(Exception):
    pass

class GenerationFailed(FlamegraphException):
    pass


def generate(input_source):
    with NamedTemporaryFile() as fh:
        fh.write(input_source)
        fh.flush()

        flamegraph_path = os.path.join(os.path.dirname(__file__), "flamegraph", "flamegraph.pl")
        proc = Popen([flamegraph_path, fh.name], stdout=PIPE, stderr=PIPE)

        stdout, stderr = proc.communicate()

        if proc.returncode:
            # fail
            raise GenerationFailed(stderr=stderr)

        return stdout
