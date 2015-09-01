from jquerypluginbp.core import generate_files, BOILERPLATE
import os
import shutil
import unittest

class TestGenerateBoilerplateFiles(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        shutil.rmtree('pluginbuild')
        os.remove('sample.package.json')

    def test_file_generation(self):
        sample_config = """
            {
                "name": "vimeoplaylist",
                "title": "jQuery Vimeo Playlist Plugin",
                "description": "jQuery plugin for creating your playlist with Vimeo.",
                "version": "0.1.0dev",
                "author": {
                    "name": "Nephila"
                },
                "licenses": [
                    {
                        "type": "MIT",
                        "url": "https://github.com/nephila/jquery-vimeoplaylist/blob/master/LICENSE"
                    }
                ]
            }
        """
        open('sample.package.json', 'w').write(sample_config)
        generate_files('sample.package.json', 'pluginbuild')
        for boilerplate in BOILERPLATE:
            boilerplate = boilerplate.replace('{{plugin_name}}', 'vimeoplaylist')
            self.assertTrue(os.path.exists(os.path.join('pluginbuild', boilerplate)))

    def test_multiple_license_generation(self):
        sample_config = """
            {
                "name": "vimeoplaylist",
                "title": "jQuery Vimeo Playlist Plugin",
                "description": "jQuery plugin for creating your playlist with Vimeo.",
                "version": "0.1.0dev",
                "author": {
                    "name": "Nephila"
                },
                "licenses": [
                    {
                        "type": "MIT, GPL3",
                        "url": "https://github.com/nephila/jquery-vimeoplaylist/blob/master/LICENSE"
                    }
                ]
            }
        """
        open('sample.package.json', 'w').write(sample_config)
        generate_files('sample.package.json', 'pluginbuild')
        self.assertTrue(os.path.exists(os.path.join('pluginbuild', 'LICENSE')))
        self.assertTrue('The MIT License' in open(os.path.join('pluginbuild', 'LICENSE')).read())
        self.assertTrue('GNU GENERAL PUBLIC LICENSE' in open(os.path.join('pluginbuild', 'LICENSE')).read())

    def test_wrong_license_generation(self):
        sample_config = """
            {
                "name": "vimeoplaylist",
                "title": "jQuery Vimeo Playlist Plugin",
                "description": "jQuery plugin for creating your playlist with Vimeo.",
                "version": "0.1.0dev",
                "author": {
                    "name": "Nephila"
                },
                "licenses": [
                    {
                        "type": "MITZ",
                        "url": "https://github.com/nephila/jquery-vimeoplaylist/blob/master/LICENSE"
                    }
                ]
            }
        """
        open('sample.package.json', 'w').write(sample_config)
        generate_files('sample.package.json', 'pluginbuild')
        self.assertTrue(os.path.exists(os.path.join('pluginbuild', 'LICENSE')))
        self.assertEqual(open(os.path.join('pluginbuild', 'LICENSE')).read(), '')

