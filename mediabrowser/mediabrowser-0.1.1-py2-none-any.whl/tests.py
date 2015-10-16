from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image

import os



IMAGE_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testsite', 'img')


class AuthenticatedUserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("testuser", password="s3kret")
        user.is_staff = True
        user.save()
        self.uploaded = []
    
    def tearDown(self):
        for f in self.uploaded:
            os.remove(f)
    

    def get_client(self):
        c = Client()
        c.login(username="testuser", password="s3kret")
        return c

    
class FileBrowsingTestCase(AuthenticatedUserTestCase):
    
    def test_sticky_params_in_links(self):
        """ Test that file browser links contains the original GET params. """
        params = {
            "type": "Images",
            "CKEditor": "editor2",
            "CKEditorFuncNum": "2",
            "langCode": "en",
        }
        url = '/images/add/'
        c = self.get_client()
        response = c.get(url, params)
        # we should really parse HTML and extract links instad of this:
        for k,v in params.items():
            self.assertContains(response, k+"="+v)


class FileUploadTestCase(AuthenticatedUserTestCase):
    
    def test_image_upload(self):
        from mediabrowser.constants import MEDIABROWSER_MAX_IMAGE_SIZE
        c = self.get_client()
        filepath =  os.path.join(IMAGE_ROOT, 'test.png')
        with open(filepath) as fp:
            response = c.post('/images/add/?type=Images&CKEditor=editor2&CKEditorFuncNum=2&langCode=de', {"file":fp})
        self.assertTrue("asset" in response.context)
        self.uploaded.append(response.context["asset"].file.path)
        self.assertTrue("MEDIABROWSER.insertFile" in response.content, "Missing MEDIABROWSER.insertFile call in response")
        
        # test.png should not be resized, it's small
        orig_img = Image.open(filepath)
        uploaded_img = Image.open(response.context["asset"].file.path)
        self.assertEqual(orig_img.size[0], uploaded_img.size[0])
        self.assertEqual(orig_img.size[1], uploaded_img.size[1])
        
        filepath =  os.path.join(IMAGE_ROOT, 'user.png')
        with open(filepath) as fp:
            response = c.post('/images/add/?type=Images', {"file":fp})
        # user should be resized to 500 x 500 because it's larger then MEDIABROWSER_MAX_IMAGE_SIZE
        uploaded_img = Image.open(response.context["asset"].file)
        self.uploaded.append(response.context["asset"].file.path)
        self.assertEqual(MEDIABROWSER_MAX_IMAGE_SIZE[0], uploaded_img.size[0])
        self.assertEqual(MEDIABROWSER_MAX_IMAGE_SIZE[1], uploaded_img.size[1])
        
    
    # TODO: autoresize on upload

class AutoresizeImageTest(TestCase):
    
    def setUp(self):
        self.to_path = os.path.join(IMAGE_ROOT, 'user-resized.png')
    
    def tearDown(self):
        if os.path.exists(self.to_path):
            os.remove(self.to_path)
    
    def test_fit_image(self):
        from mediabrowser.utils import fit_image
        
        sizes = (
            # (max_size, expected_size)
            ((300, 300), (300, 300)),
            ((100, 300), (100, 100)),
            ((300, 200), (200, 200)),
        )
        from_path = os.path.join(IMAGE_ROOT, 'user.png')
        for size in sizes:
            fit_image(from_path, *size[0], save_to=self.to_path)
            img = Image.open(self.to_path)
            self.assertEqual(img.size[0], size[1][0], "Wrong image width: extected %d but got %d"%(img.size[0], size[1][0]))
            self.assertEqual(img.size[1], size[1][1], "Wrong image height: extected %d but got %d"%(img.size[1], size[1][1]))