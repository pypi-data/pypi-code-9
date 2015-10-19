import unittest
import os.path
import json
import inspect
import requests

import asposebarcodecloud
from asposebarcodecloud.BarcodeApi import BarcodeApi
from asposebarcodecloud.BarcodeApi import ApiException
from asposebarcodecloud.models import BarcodeResponseList
from asposebarcodecloud.models import SaaSposeResponse
from asposebarcodecloud.models import BarcodeReader

import asposestoragecloud 
from asposestoragecloud.StorageApi import StorageApi

class TestAsposeBarcodeCloud(unittest.TestCase):

    def setUp(self):

        with open('setup.json') as json_file:
            data = json.load(json_file)

        self.storageApiClient = asposestoragecloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.storageApi = StorageApi(self.storageApiClient)

        self.apiClient = asposebarcodecloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.barcodeApi = BarcodeApi(self.apiClient)

        self.output_path = str(data['output_location'])

    def testGetBarcodeGenerate(self):
        try:
            
            response = self.barcodeApi.GetBarcodeGenerate(text="NewBarCode",type="qr",format='png')
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetBarcodeRecognize(self):
        try:
            name = "sample-barcode.jpeg"
            response = self.storageApi.PutCreate(name,'./data/' + name)
    
            response = self.barcodeApi.GetBarcodeRecognize(name)
            
            self.assertIsInstance(response,BarcodeResponseList.BarcodeResponseList)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostBarcodeRecognizeFromUrlorContent(self):
        try:
            url = "http://www.barcoding.com/images/Barcodes/code93.gif"
            response = self.barcodeApi.PostBarcodeRecognizeFromUrlorContent(file = None, url=url)
            self.assertIsInstance(response,BarcodeResponseList.BarcodeResponseList)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostGenerateMultiple(self):
        try:
            
            #response = self.barcodeApi.PostGenerateMultiple(file = './data/sample.txt')
            #self.assertEqual(response.Code,200)
            print ""

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPutBarcodeGenerateFile(self):
        try:
            
            response = self.barcodeApi.PutBarcodeGenerateFile(name='testbar.png', file=None, type="qr", text="Aspose.Barcode for Cloud")
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPutBarcodeRecognizeFromBody(self):
        try:
            name = "sample-barcode.jpeg"
            
            body = BarcodeReader.BarcodeReader()
            body.StripFNC = True
            body.ChecksumValidation = "OFF"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.barcodeApi.PutBarcodeRecognizeFromBody(name, body)
            
            self.assertIsInstance(response,BarcodeResponseList.BarcodeResponseList)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPutGenerateMultiple(self):
        try:
            name = "newfile.jpg"
            file = "./data/sample.txt"
            
            response = self.barcodeApi.PutGenerateMultiple(name, file)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
if __name__ == '__main__':
    unittest.main()