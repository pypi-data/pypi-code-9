import logging
import mothermayi.errors
import subprocess

LOGGER = logging.getLogger(__name__)

def plugin():
    return {
        'name'          : 'pylint',
        'pre-commit'    : pre_commit,
    }

def pre_commit(config, staged):
    pylint = config.get('pylint', {})
    args   = pylint.get('args', [])

    command = ['pylint'] + args
    command += staged
    LOGGER.debug("Executing %s", " ".join(command))
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise mothermayi.errors.FailHook(str(e.output.decode('utf-8')))
