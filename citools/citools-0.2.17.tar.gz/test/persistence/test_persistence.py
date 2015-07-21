import os
import tempfile
from unittest import TestCase
from citools.persistence import Persistence


class PersistenceTest(TestCase):
    def test_with_block(self):
        output = tempfile.mkdtemp(prefix='persistence_test')
        persistence_file_name = os.path.join(output, 'name')
        with Persistence(persistence_file_name) as persistence:
            report = persistence.get_report()

    def test_with_block_with_non_existent_path(self):
        self.assertRaises(Exception, lambda: Persistence('/non/existent/path'))
