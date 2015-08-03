import unittest
import os.path
import json

from asposebarcode.ApiClient import ApiClient
from asposebarcode.BarcodeApi import BarcodeApi
from asposestorage.StorageApi import StorageApi




class TestAsposeBarcode(unittest.TestCase):

    def setUp(self):

        with open('setup.json') as json_file:
            data = json.load(json_file)

        self.apiClient = ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),apiServer=str(data['product_uri']))
        self.storageApi = StorageApi(self.apiClient)
        self.barcodeApi = BarcodeApi(self.apiClient)

        self.output_path = str(data['output_location'])

    def testGetBarcodeGenerate(self):

        response = self.barcodeApi.GetBarcodeGenerate(text="NewBarCode",type="qr",format='png')
        self.assertEqual(response.status_code,200)

    def testGetBarcodeRecognize(self):
        response = self.storageApi.PutCreate('qrcode.jpg','./data/qrcode.jpg')
        self.assertEqual(response.status_code,200)

        response = self.barcodeApi.GetBarcodeRecognize('qrcode.jpg')
        self.assertEqual(response.status_code,200)

    def testPostBarcodeRecognizeFromUrlorContent(self):
        response = self.barcodeApi.PostBarcodeRecognizeFromUrlorContent('./data/qrcode.jpg',url='http://www.calm9.com/qrcode/Calm9-QRCode-Bookmark.png')
        self.assertEqual(response.status_code,200)

    def testPostGenerateMultiple(self):
        response = self.barcodeApi.PostGenerateMultiple('./data/sample.txt')
        self.assertEqual(response.status_code,200)

    def testPutBarcodeGenerateFile(self):
        response = self.barcodeApi.PutBarcodeGenerateFile('testbar.png','./data/qrcode.jpg',text="Hello My World")
        self.assertEqual(response.status_code,200)

    def testPutBarcodeRecognizeFromBody(self):
        body_str = '{"ChecksumValidation": "string","StripFNC": true,"BarcodesCount": 0,"RotationAngle": 0,"BinarizationHints": "string"}'
        response = self.barcodeApi.PutBarcodeRecognizeFromBody('testbar.png',body_str)
        self.assertEqual(response.status_code,200)


    def testPutGenerateMultiple(self):
        response = self.barcodeApi.PutGenerateMultiple('newfile.jpg','./data/sample.txt')
        self.assertEqual(response.status_code,200)


