"""Tests for coverage.data"""

import os

from coverage.backward import pickle
from coverage.data import CoverageData
from coverage.files import PathAliases, canonical_filename

from tests.coveragetest import CoverageTest


DATA_1 = {
    'a.py': {1: None, 2: None},
    'b.py': {3: None},
}
SUMMARY_1 = {'a.py': 2, 'b.py': 1}
MEASURED_FILES_1 = ['a.py', 'b.py']
A_PY_LINES_1 = [1, 2]
B_PY_LINES_1 = [3]

DATA_2 = {
    'a.py': {1: None, 5: None},
    'c.py': {17: None},
}
SUMMARY_1_2 = {'a.py': 3, 'b.py': 1, 'c.py': 1}
MEASURED_FILES_1_2 = ['a.py', 'b.py', 'c.py']

ARC_DATA_3 = {
    'x.py': {
        (1, 2): None,
        (2, 3): None,
    },
    'y.py': {
        (17, 23): None,
    },
}
X_PY_ARCS_3 = [(1, 2), (2, 3)]
Y_PY_ARCS_3 = [(17, 23)]


class DataTestHelpers(CoverageTest):
    """Test helpers for data tests."""

    def assert_summary(self, covdata, summary, fullpath=False):
        """Check that the summary of `covdata` is `summary`."""
        self.assertEqual(covdata.summary(fullpath), summary)

    def assert_measured_files(self, covdata, measured):
        """Check that `covdata`'s measured files are `measured`."""
        self.assertCountEqual(covdata.measured_files(), measured)


class DataTest(DataTestHelpers, CoverageTest):
    """Test cases for coverage.data."""

    run_in_temp_dir = False

    def test_reading_empty(self):
        covdata = CoverageData()
        covdata.read()
        self.assert_summary(covdata, {})

    def test_adding_data(self):
        covdata = CoverageData()
        covdata.add_line_data(DATA_1)
        self.assert_summary(covdata, SUMMARY_1)
        self.assert_measured_files(covdata, MEASURED_FILES_1)

    def test_touch_file(self):
        covdata = CoverageData()
        covdata.add_line_data(DATA_1)
        covdata.touch_file('x.py')
        self.assert_measured_files(covdata, MEASURED_FILES_1 + ['x.py'])

    def test_writing_and_reading(self):
        covdata1 = CoverageData()
        covdata1.add_line_data(DATA_1)
        covdata1.write()

        covdata2 = CoverageData()
        covdata2.read()
        self.assert_summary(covdata2, SUMMARY_1)

    def test_combining(self):
        covdata1 = CoverageData()
        covdata1.add_line_data(DATA_1)
        covdata1.write(suffix='1')

        covdata2 = CoverageData()
        covdata2.add_line_data(DATA_2)
        covdata2.write(suffix='2')

        covdata3 = CoverageData()
        covdata3.combine_parallel_data()
        self.assert_summary(covdata3, SUMMARY_1_2)
        self.assert_measured_files(covdata3, MEASURED_FILES_1_2)

    def test_erasing(self):
        covdata1 = CoverageData()
        covdata1.add_line_data(DATA_1)
        covdata1.write()
        covdata1.erase()
        self.assert_summary(covdata1, {})

        covdata2 = CoverageData()
        covdata2.read()
        self.assert_summary(covdata2, {})

    def test_file_format(self):
        # Write with CoverageData, then read the pickle explicitly.
        covdata = CoverageData()
        covdata.add_line_data(DATA_1)
        covdata.write()

        with open(".coverage", 'rb') as fdata:
            data = pickle.load(fdata)

        lines = data['lines']
        self.assertCountEqual(lines.keys(), MEASURED_FILES_1)
        self.assertCountEqual(lines['a.py'], A_PY_LINES_1)
        self.assertCountEqual(lines['b.py'], B_PY_LINES_1)
        # If not measuring branches, there's no arcs entry.
        self.assertEqual(data.get('arcs', 'not there'), 'not there')

    def test_file_format_with_arcs(self):
        # Write with CoverageData, then read the pickle explicitly.
        covdata = CoverageData()
        covdata.add_arc_data(ARC_DATA_3)
        covdata.write()

        with open(".coverage", 'rb') as fdata:
            data = pickle.load(fdata)

        self.assertCountEqual(data['lines'].keys(), [])
        arcs = data['arcs']
        self.assertCountEqual(arcs['x.py'], X_PY_ARCS_3)
        self.assertCountEqual(arcs['y.py'], Y_PY_ARCS_3)

    def test_combining_with_aliases(self):
        covdata1 = CoverageData()
        covdata1.add_line_data({
            '/home/ned/proj/src/a.py': {1: None, 2: None},
            '/home/ned/proj/src/sub/b.py': {3: None},
            })
        covdata1.write(suffix='1')

        covdata2 = CoverageData()
        covdata2.add_line_data({
            r'c:\ned\test\a.py': {4: None, 5: None},
            r'c:\ned\test\sub\b.py': {6: None},
            })
        covdata2.write(suffix='2')

        covdata3 = CoverageData()
        aliases = PathAliases()
        aliases.add("/home/ned/proj/src/", "./")
        aliases.add(r"c:\ned\test", "./")
        covdata3.combine_parallel_data(aliases=aliases)

        apy = canonical_filename('./a.py')
        sub_bpy = canonical_filename('./sub/b.py')

        self.assert_summary(
            covdata3, { apy: 4, sub_bpy: 2, }, fullpath=True
            )
        self.assert_measured_files(covdata3, [apy,sub_bpy])


class DataTestInTempDir(DataTestHelpers, CoverageTest):
    """Test cases for coverage.data."""

    no_files_in_temp_dir = True

    def test_combining_from_different_directories(self):
        covdata1 = CoverageData()
        covdata1.add_line_data(DATA_1)
        os.makedirs('cov1')
        covdata1.write_file('cov1/.coverage.1')

        covdata2 = CoverageData()
        covdata2.add_line_data(DATA_2)
        os.makedirs('cov2')
        covdata2.write_file('cov2/.coverage.2')

        covdata3 = CoverageData()
        covdata3.combine_parallel_data(data_dirs=[
            'cov1/',
            'cov2/',
            ])

        self.assert_summary(covdata3, SUMMARY_1_2)
        self.assert_measured_files(covdata3, MEASURED_FILES_1_2)
