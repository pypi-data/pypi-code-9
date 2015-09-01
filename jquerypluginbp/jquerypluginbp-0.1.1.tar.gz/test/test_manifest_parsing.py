# -*- coding: utf-8 -*-

from jquerypluginbp.core import parse_package_manifest, PackageManifestException
import unittest

class TestManifestParsing(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_package_manifest(self):
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
        parsed_manifest = parse_package_manifest(sample_config)
        self.assertEqual(parsed_manifest['plugin_name'], 'vimeoplaylist')
        self.assertEqual(parsed_manifest['plugin_description'], 'jQuery plugin for creating your playlist with Vimeo.')
        self.assertEqual(parsed_manifest['plugin_version'], '0.1.0dev')
        self.assertEqual(parsed_manifest['plugin_author'], 'Nephila')
        self.assertEqual(parsed_manifest['plugin_license'], 'MIT')

    def test_parse_wrong_author(self):
        sample_config = """
            {
                "name": "vimeoplaylist",
                "title": "jQuery Vimeo Playlist Plugin",
                "description": "jQuery plugin for creating your playlist with Vimeo.",
                "version": "0.1.0dev",
                "author": {
                },
                "licenses": [
                    {
                        "type": "MIT",
                        "url": "https://github.com/nephila/jquery-vimeoplaylist/blob/master/LICENSE"
                    }
                ]
            }
        """
        parsed_manifest = self.assertRaises(PackageManifestException, parse_package_manifest, sample_config)

    def test_parse_wrong_license(self):
        sample_config = """
            {
                "name": "vimeoplaylist",
                "title": "jQuery Vimeo Playlist Plugin",
                "description": "jQuery plugin for creating your playlist with Vimeo.",
                "version": "0.1.0dev",
                "author": {
                    "name": "Nephila"
                },
                "licenses": "MIT"
            }
        """
        parsed_manifest = self.assertRaises(PackageManifestException, parse_package_manifest, sample_config)

    def test_parse_wrong_license_without_type(self):
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
                        "url": "https://github.com/nephila/jquery-vimeoplaylist/blob/master/LICENSE"
                    }
                ]
            }
        """
        self.assertRaises(PackageManifestException, parse_package_manifest, sample_config)

    def test_parse_multi_licenses(self):
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
                    },
                    {
                        "type": "RAINBOW LICENSE",
                        "url": "https://github.com/nephila/jquery-vimeoplaylist/blob/master/RAINBOW_LICENSE"
                    }
                ]
            }
        """
        parsed_manifest = parse_package_manifest(sample_config)
        self.assertEqual(parsed_manifest['plugin_license'], 'MIT,RAINBOW LICENSE')

    def test_parse_wrong_package_manifest(self):
        sample_config = """
            wrong package manager
        """
        parsed_manifest = self.assertRaises(PackageManifestException, parse_package_manifest, sample_config)

    def test_parse_package_manifest_with_missing_parameters(self):
        sample_config = """
            {
                "title": "jQuery Vimeo Playlist Plugin",
                "description": "jQuery plugin for creating your playlist with Vimeo."
            }
        """
        parsed_manifest = self.assertRaises(PackageManifestException, parse_package_manifest, sample_config)
