from replay_parser import ReplayParser

import os
import struct
import unittest


class TestReplayParser(unittest.TestCase):

    folder_path = '{}/example_replays/'.format(
        os.path.dirname(os.path.realpath(__file__))
    )

    def test_104_replay(self):
        """
        A replay from version 1.04.
        """

        parser = ReplayParser()

        with open(self.folder_path + '1.04.replay') as f:
            response = parser.parse(f)
            self.assertIsInstance(response, dict)
            self.assertEqual(response['header']['Id'], '0AB18BAB4CCE97201B7753A84B358D48')

    def test_105_replay(self):
        """
        A replay from version 1.05.
        """

        parser = ReplayParser()

        with open(self.folder_path + '1.05.replay') as f:
            response = parser.parse(f)
            self.assertIsInstance(response, dict)
            self.assertEqual(response['header']['Id'], '56E7708C45ED1CF3B9E51EBF1ADF4431')

    def test_broken_replay(self):
        """
        This replay file was purposefully broken by deleting a large portion
        of the data.
        """

        parser = ReplayParser()

        with open(self.folder_path + 'broken.replay') as f:
            with self.assertRaises(struct.error):
                parser.parse(f)

    def test_keyframes_missing_replay(self):
        """
        For some reason, this replay is missing the key frames from when goals
        were scored, so that data is not available to a parser. This is a good
        test to ensure the parser can handle odd scenarios.
        """

        parser = ReplayParser()

        with open(self.folder_path + 'keyframes_missing.replay') as f:
            response = parser.parse(f)
            self.assertIsInstance(response, dict)
            self.assertEqual(response['header']['Id'], '50D5031342FF90D9F25BE5A0152E56B8')

if __name__ == '__main__':
    unittest.main()
