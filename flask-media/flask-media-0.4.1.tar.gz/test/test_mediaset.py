# coding: utf-8
import os
import shutil
import unittest
from tempfile import mkdtemp
from flask import Flask, url_for
from flask.ext.media import Media


__author__ = 'vadim'


class MediaSetTestCase(unittest.TestCase):
    def setUp(self):
        self.instance_path = mkdtemp()
        self.app = Flask(__name__, instance_path=self.instance_path)
        self.app.config['SERVER_NAME'] = 'localhost'
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        shutil.rmtree(self.instance_path)

    def test_create_media(self):
        media = Media()
        self.assertEqual(media.folder_level, 3)
        self.assertEqual(media.use_folder_date, False)
        self.assertEqual(media.app, None)

    def test_create_custom_media(self):
        media = Media(folder_level=5, use_folder_date=True)
        self.assertEqual(media.folder_level, 5)
        self.assertEqual(media.use_folder_date, True)

    def test_default_config(self):
        media = Media(self.app)

        self.assertTrue('media' in self.app.extensions)

        self.assertTrue(hasattr(self.app.extensions['media'], 'media'))
        self.assertTrue(hasattr(self.app.extensions['media'], 'app'))

        self.assertEqual(self.app.config.get('MEDIA_SETS'), '')
        self.assertEqual(self.app.config.get('MEDIA_HANDLER'), True)
        self.assertEqual(self.app.config.get('MEDIA_URL'), '/media')
        self.assertEqual(self.app.config.get('MEDIA_PATH'), 'media')
        self.assertEqual(self.app.config.get('MEDIA_ALLOW'), [])
        self.assertEqual(self.app.config.get('MEDIA_DENY'), [])
        self.assertEqual(self.app.config.get('MEDIA_SPLIT'), 0)
        self.assertEqual(self.app.config.get('MEDIA_THUMB_PATH'), 'thumb')

        self.assertEqual(len(media.sets), 0)
        self.assertIsInstance(url_for('uploaded_file', setname='set0', filename='filename1'), basestring)

    def test_custom_config(self):
        self.app.config['MEDIA_SETS'] = 'pic'
        self.app.config['MEDIA_ALLOW_PIC'] = 'gif bmp'
        media = Media(self.app)

        self.assertEqual(len(media.sets), 1)
        self.assertIsInstance(media['pic'], Media.MediaSet)
        self.assertEqual(media['pic'].name, 'pic')
        self.assertEqual(media['pic'].url, os.path.join(self.app.config['MEDIA_URL'], 'pic'))
        self.assertEqual(media['pic'].allow, tuple(self.app.config['MEDIA_ALLOW_PIC'].split()))