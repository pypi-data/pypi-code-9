import unittest
import os.path
import json

from asposestoragecloud.ApiClient import ApiClient
from asposestoragecloud.StorageApi import StorageApi
from asposestoragecloud.ApiClient import ApiException
from asposestoragecloud.models import ResponseMessage
from asposestoragecloud.models import DiscUsageResponse
from asposestoragecloud.models import FileExistResponse
from asposestoragecloud.models import MoveFileResponse
from asposestoragecloud.models import MoveFolderResponse
from asposestoragecloud.models import StorageExistResponse
from asposestoragecloud.models import FileVersionsResponse
from asposestoragecloud.models import RemoveFolderResponse
from asposestoragecloud.models import RemoveFileResponse

class TestAsposeStorage(unittest.TestCase):

    def setUp(self):

        with open('setup.json') as json_file:
            data = json.load(json_file)

        self.apiClient = ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.storageApi = StorageApi(self.apiClient)

        self.output_path = str(data['output_location'])

    def testGetListFiles(self):
        
        try:
            response = self.storageApi.PutCreateFolder('list_test_folder')
            response = self.storageApi.PutCreate('list_test_folder/SampleWordDocument.docx','./data/SampleWordDocument.docx')
            response = self.storageApi.PutCreate('list_test_folder/testfile.txt','./data/testfile.txt')
            response = self.storageApi.PutCreateFolder('list_test_folder/sub_folder')
            response = self.storageApi.GetListFiles(Path='list_test_folder')
            self.assertEqual(len(response.Files),3)
            self.assertEqual(response.Status,'OK')
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDiscUsage(self):
        try:
            response = self.storageApi.GetDiscUsage()

            self.assertIsInstance(response,DiscUsageResponse.DiscUsageResponse)
            self.assertEqual(response.Status,'OK')
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutCreate(self):
        try:
            response = self.storageApi.PutCreate('SampleWordDocument.docx','./data/SampleWordDocument.docx')

            self.assertIsInstance(response,ResponseMessage.ResponseMessage)
            self.assertEqual(response.Status,'OK')
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDownload(self):
        try:
            response = self.storageApi.GetDownload('SampleWordDocument.docx')

            self.assertEqual(response.Status,'OK')

            with open("./output/" + 'SampleWordDocument.docx', 'wb') as f:
                for chunk in response.InputStream:
                    f.write(chunk)


            self.assertTrue(True, os.path.exists("./output/" + 'SampleWordDocument.docx'))

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetIsExist(self):
        try:
            response = self.storageApi.GetIsExist('testfile.txt')

            self.assertIsInstance(response,FileExistResponse.FileExistResponse)
            self.assertEqual(response.Status,'OK')
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutCreateFolder(self):
        try:
            response = self.storageApi.PutCreateFolder('mytestfolder')

            self.assertIsInstance(response,ResponseMessage.ResponseMessage)
            self.assertEqual(response.Status,'OK')
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostMoveFile(self):
        try:
            response = self.storageApi.PutCreate('testfile.txt','./data/testfile.txt')
            response = self.storageApi.PostMoveFile('testfile.txt','mytestfolder/testfile.txt')

            self.assertIsInstance(response,MoveFileResponse.MoveFileResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostMoveFolder(self):
        try:
            response = self.storageApi.PostMoveFolder('mytestfolder','mytestfolder_new')

            self.assertIsInstance(response,MoveFolderResponse.MoveFolderResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutCopy(self):
        try:
            response = self.storageApi.PutCreate('testfile.txt','./data/testfile.txt')
            response = self.storageApi.PutCopy('testfile.txt','new_testfile.txt','./data/testfile.txt')

            self.assertIsInstance(response,ResponseMessage.ResponseMessage)
            self.assertEqual(response.Status,'OK')
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutCopyFolder(self):
        try:
            response = self.storageApi.PutCreateFolder('mytestfolder')
            response = self.storageApi.PutCopyFolder('mytestfolder','mytestfolder1')
            self.assertIsInstance(response,ResponseMessage.ResponseMessage)
            self.assertEqual(response.Status,'OK')
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetIsStorageExist(self):
        try:
            response = self.storageApi.GetIsStorageExist('Aspose123')
            self.assertIsInstance(response,StorageExistResponse.StorageExistResponse)
            self.assertEqual(response.Status,'OK')
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetListFileVersions(self):
        try:
            response = self.storageApi.PutCreate('testfile.txt','./data/testfile.txt')
            response = self.storageApi.GetListFileVersions('testfile.txt')

            self.assertIsInstance(response,FileVersionsResponse.FileVersionsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testDeleteFolder(self):
        try:
            response = self.storageApi.DeleteFolder('mytestfolder')
            self.assertIsInstance(response,RemoveFolderResponse.RemoveFolderResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testDeleteFile(self):
        try:
            response = self.storageApi.DeleteFile('testfile.txt')

            self.assertIsInstance(response,RemoveFileResponse.RemoveFileResponse)
            self.assertEqual(response.Status,'OK')
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

