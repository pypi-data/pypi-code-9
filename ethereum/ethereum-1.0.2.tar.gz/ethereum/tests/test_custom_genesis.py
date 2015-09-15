import os
import ethereum.testutils as testutils
from ethereum.slogging import get_logger
import ethereum.blocks as blocks
logger = get_logger()

# SETUP TESTS IN GLOBAL NAME SPACE
def gen_func(filename, testname, testdata):
    return lambda: do_test_state(filename, testname, testdata)

def do_test_state(filename, testname=None, testdata=None, limit=99999999):
    logger.debug('running test:%r in %r' % (testname, filename))
    testutils.check_genesis_test(testutils.fixture_to_bytes(testdata))

fixtures = testutils.get_tests_from_file_or_dir(
    os.path.join(testutils.fixture_path, 'GenesisTests'))

filenames = sorted(list(fixtures.keys()))
for filename in filenames:
    tests = fixtures[filename]
    for testname, testdata in list(tests.items()):
        func_name = 'test_%s_%s' % (filename, testname)
        globals()[func_name] = gen_func(filename, testname, testdata)
