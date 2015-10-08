import unittest
import os.path
import json
import inspect
import requests

import asposepdfcloud
from asposepdfcloud.PdfApi import PdfApi
from asposepdfcloud.PdfApi import ApiException
from asposepdfcloud.models import AnnotationResponse
from asposepdfcloud.models import AnnotationsResponse
from asposepdfcloud.models import AttachmentResponse
from asposepdfcloud.models import AttachmentsResponse
from asposepdfcloud.models import BarcodeResponseList
from asposepdfcloud.models import BookmarksResponse
from asposepdfcloud.models import Signature
from asposepdfcloud.models import Rectangle
from asposepdfcloud.models import SaaSposeResponse
from asposepdfcloud.models import SplitResultResponse
from asposepdfcloud.models import DocumentResponse
from asposepdfcloud.models import AppendDocument
from asposepdfcloud.models import MergeDocuments
from asposepdfcloud.models import TiffExportOptions
from asposepdfcloud.models import FieldResponse
from asposepdfcloud.models import FieldsResponse
from asposepdfcloud.models import Field
from asposepdfcloud.models import Fields
from asposepdfcloud.models import TextItemsResponse
from asposepdfcloud.models import TextFormatResponse
from asposepdfcloud.models import TextItemResponse
from asposepdfcloud.models import ImagesResponse
from asposepdfcloud.models import ImageResponse
from asposepdfcloud.models import LinkAnnotationResponse
from asposepdfcloud.models import LinkAnnotationsResponse
from asposepdfcloud.models import DocumentPagesResponse
from asposepdfcloud.models import WordCountResponse
from asposepdfcloud.models import Stamp
from asposepdfcloud.models import DocumentProperty
from asposepdfcloud.models import DocumentPropertyResponse
from asposepdfcloud.models import DocumentPropertiesResponse
from asposepdfcloud.models import DocumentTextReplaceResponse
from asposepdfcloud.models import TextReplace
from asposepdfcloud.models import TextReplaceListRequest
from asposepdfcloud.models import PageTextReplaceResponse
from asposepdfcloud.models import BookmarkResponse

import asposestoragecloud 
from asposestoragecloud.StorageApi import StorageApi

import random
import string

class TestAsposePdfCloud(unittest.TestCase):

    def setUp(self):

        with open('setup.json') as json_file:
            data = json.load(json_file)

        self.storageApiClient = asposestoragecloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.storageApi = StorageApi(self.storageApiClient)

        self.apiClient = asposepdfcloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.pdfApi = PdfApi(self.apiClient)

        self.output_path = str(data['output_location'])

    def testGetPageAnnotation(self):    
        try:
            name = "Sample-Annotation.pdf"
            pageNumber =  1 
            annotationNumber = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetPageAnnotation(name, pageNumber, annotationNumber)            

            self.assertIsInstance(response,AnnotationResponse.AnnotationResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
    
    def testGetPageAnnotations(self):
        try:
            name = "Sample-Annotation.pdf"
            pageNumber =  1 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetPageAnnotations(name, pageNumber)            

            self.assertIsInstance(response,AnnotationsResponse.AnnotationsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDocumentAttachmentByIndex(self):
        try:
            name = "SampleAttachment.pdf"            
            attachmentIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetDocumentAttachmentByIndex(name, attachmentIndex)            

            self.assertIsInstance(response,AttachmentResponse.AttachmentResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDocumentAttachments(self):
        try:
            name = "SampleAttachment.pdf"
            pageNumber =  1 
            annotationNumber = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetDocumentAttachments(name)            

            self.assertIsInstance(response,AttachmentsResponse.AttachmentsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDownloadDocumentAttachmentByIndex(self):

        try:
            name = "SampleAttachment.pdf"
            attachmentIndex =  1 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetDownloadDocumentAttachmentByIndex(name, attachmentIndex)            
         
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetExtractBarcodes(self):

        try:
            name = "SampleBarCodeImage.pdf"
            pageNumber =  2 
            imageNumber = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetExtractBarcodes(name, pageNumber, imageNumber)            

            self.assertIsInstance(response,BarcodeResponseList.BarcodeResponseList)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDocumentBookmarks(self):

        try:
            name = "Sample-Bookmark.pdf"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetDocumentBookmarks(name)            

            self.assertIsInstance(response,BookmarksResponse.BookmarksResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDocumentBookmarksChildren(self):

        try:
            name = "Sample-Bookmark.pdf"
            
            #response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetDocumentBookmarksChildren(name, bookmarkPath="1")            
            
            self.assertIsInstance(response,BookmarkResponse.BookmarkResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDocument(self):

        try:
            name = "Sample.pdf"
            pageNumber =  1 
            annotationNumber = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetDocument(name)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDocumentWithFormat(self):

        try:
            name = "Sample.pdf"
            format =  "DOC"
            
            #response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetDocumentWithFormat(name, format)
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex   
   
   
    def testPostSignDocument(self):

        try:
            name = "sample-input.pdf"
            signatureFileName = "pkc7-sample.pfx";
            pageNumber = 1
            
            body = Signature.Signature()
            body.Authority =  "Farooq Sheikh"
            body.Location = "Rawalpindi"
            body.Contact =  "farooq.sheikh@aspose.com"
            body.Date =  "06/24/2015 2:00:00.000 AM"     
            body.FormFieldName = "Signature1"     
            body.Password = "aspose"
            
            rect = Rectangle.Rectangle();
            rect.X = 100
            rect.Y = 100
            rect.Height = 100
            rect.Width = 200
            body.Rectangle = rect
            body.SignaturePath = signatureFileName
            body.SignatureType = "PKCS7"
            body.Visible = True 

            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.storageApi.PutCreate(signatureFileName,'./data/' + signatureFileName)
            
            response = self.pdfApi.PostSignPage(name, pageNumber, body)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testPostSplitDocument(self):

        try:
            name = "sample-input.pdf"
            format = "pdf"
            ffrom = 1
            to = 2
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PostSplitDocument(name, format=format, ffrom=ffrom, to=to)            

            self.assertIsInstance(response,SplitResultResponse.SplitResultResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testPutConvertDocument(self):

        try:
            name = "Sample.pdf"             
            format = "TIFF"
            
            response = self.pdfApi.PutConvertDocument(file ='./data/' + name , format=format)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testPutCreateDocument(self):

        try:
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            name = name + ".pdf"
            
            response = self.pdfApi.PutCreateDocument(name)            

            self.assertIsInstance(response,DocumentResponse.DocumentResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testPostAppendDocument(self):

        try:
            name = "Sample.pdf"
            startPage = 2
            endPage = 3
            
            appendFileName = "sample-input.pdf"
            
            body = AppendDocument.AppendDocument()
            body.Document = appendFileName
            body.StartPage = startPage
            body.EndPage = endPage
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.storageApi.PutCreate(appendFileName,'./data/' + appendFileName)
            
            response = self.pdfApi.PostAppendDocument(name, body, startPage=startPage, endPage=endPage)            

            self.assertIsInstance(response,DocumentResponse.DocumentResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutMergeDocuments(self):

        try:
            name = "sample-merged.pdf"
            
            body = MergeDocuments.MergeDocuments()
            body.List = ["Sample.pdf", "sample-input.pdf"]
            
            response = self.storageApi.PutCreate('Sample.pdf','./data/' + 'Sample.pdf')
            response = self.storageApi.PutCreate('sample-input.pdf','./data/' + 'sample-input.pdf')
            
            response = self.pdfApi.PutMergeDocuments(name, body)            

            self.assertIsInstance(response,DocumentResponse.DocumentResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testPutDocumentSaveAsTiff(self):       

        try:
            name = "Sample.pdf"
            
            body = TiffExportOptions.TiffExportOptions()
            body.ResultFile = "Sample.tiff"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PutDocumentSaveAsTiff(name, body)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetField(self):

        try:
            name = "sample-field.pdf"
            fieldName =  "textbox1" 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetField(name, fieldName)            

            self.assertIsInstance(response,FieldResponse.FieldResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
    
    def testGetFields(self):

        try:
            name = "sample-field.pdf"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetFields(name)            

            self.assertIsInstance(response,FieldsResponse.FieldsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostCreateField(self):

        try:
            name = "sample-field.pdf"
            page = 1
            
            body = Field.Field()
            body.Name = "checkBoxField2"
            body.Values = ['1']
            body.Type = "Boolean"
            
            rect = Rectangle.Rectangle();
            rect.X = 100
            rect.Y = 100
            rect.Height = 100
            rect.Width = 200
            body.Rect = rect
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PostCreateField(name, page, body)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutUpdateField(self):

        try:
            name = "sample-field.pdf"
            fieldName = "textbox1"
            
            body = Field.Field()
            body.Name = "textbox1"
            body.Values = ['Aspose']
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PutUpdateField(name, fieldName, body)            

            self.assertIsInstance(response,FieldResponse.FieldResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testPutUpdateFields(self):

        try:
            name = "sample-field.pdf"
            page = 1
            
            field1 = Field.Field()
            field1.Name = "textbox1"
            field1.Values = ['Aspose']

            body = Fields.Fields()
            body.List = [field1]
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PutUpdateFields(name, body)            

            self.assertIsInstance(response,FieldsResponse.FieldsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetFragment(self):

        try:
            name = "sample-input.pdf"
            pageNumber =  1 
            fragmentNumber = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetFragment(name, pageNumber, fragmentNumber)            

            self.assertIsInstance(response,TextItemsResponse.TextItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetFragments(self):

        try:
            name = "sample-input.pdf"
            pageNumber =  1 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetFragments(name, pageNumber)            

            self.assertIsInstance(response,TextItemsResponse.TextItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetFragmentTextFormat(self):

        try:
            name = "sample-input.pdf"
            pageNumber =  1 
            fragmentNumber = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetFragmentTextFormat(name, pageNumber, fragmentNumber)            

            self.assertIsInstance(response,TextFormatResponse.TextFormatResponse)
            self.assertEqual(response.Status,'OK')
                    
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSegment(self):

        try:
            name = "sample-input.pdf"
            pageNumber =  1 
            fragmentNumber = 1
            segmentNumber = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetSegment(name, pageNumber, fragmentNumber, segmentNumber)            

            self.assertIsInstance(response,TextItemResponse.TextItemResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testGetSegments(self):

        try:
            name = "sample-input.pdf"
            pageNumber =  1 
            fragmentNumber = 1
            
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetSegments(name, pageNumber, fragmentNumber)            

            self.assertIsInstance(response,TextItemResponse.TextItemResponse)
            self.assertEqual(response.Status,'OK')

        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSegmentTextFormat(self):

        try:
            name = "sample-input.pdf"
            pageNumber =  1 
            fragmentNumber = 1
            segmentNumber = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetSegmentTextFormat(name, pageNumber, fragmentNumber, segmentNumber)            

            self.assertIsInstance(response,TextFormatResponse.TextFormatResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testGetImage(self):

        try:
            name = "SampleImage.pdf"
            pageNumber =  1 
            imageNumber = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetImage(name, pageNumber, imageNumber)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetImages(self):

        try:
            name = "SampleImage.pdf"
            pageNumber =  1 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetImages(name, pageNumber)            
            
            self.assertIsInstance(response,ImagesResponse.ImagesResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetImageWithFormat(self):

        try:
            name = "SampleImage.pdf"
            pageNumber =  1 
            imageNumber = 1
            format = "jpeg"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetImageWithFormat(name, pageNumber, imageNumber, format)            
            
            self.assertEqual(response.Status,'OK')

        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testPostReplaceImage(self):

        try:
            name = "SampleImage.pdf"
            pageNumber =  1 
            imageNumber = 1
            
            imageFile = "aspose-cloud.png"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            
            response = self.pdfApi.PostReplaceImage(name, pageNumber, imageNumber, file = './data/' + imageFile)            

            self.assertIsInstance(response,ImageResponse.ImageResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testGetPageLinkAnnotationByIndex(self):

        try:
            name = "Sample-Bookmark.pdf"
            pageNumber =  1 
            linkIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetPageLinkAnnotationByIndex(name, pageNumber, linkIndex)            

            self.assertIsInstance(response,LinkAnnotationResponse.LinkAnnotationResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetPageLinkAnnotations(self):

        try:
            name = "Sample-Bookmark.pdf"
            pageNumber =  1 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetPageLinkAnnotations(name, pageNumber)            

            self.assertIsInstance(response,LinkAnnotationsResponse.LinkAnnotationsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testDeletePage(self):

        try:
            name = "sample-input.pdf"
            pageNumber =  1 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.DeletePage(name, pageNumber)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetPage(self):        

        try:
            name = "sample-input.pdf"
            pageNumber =  1 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetPage(name, pageNumber)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetPages(self):

        try:
            name = "Sample-Annotation.pdf"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetPages(name)            

            self.assertIsInstance(response,DocumentPagesResponse.DocumentPagesResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetPageWithFormat(self):

        try:
            name = "Sample-Annotation.pdf"
            pageNumber =  1 
            format = "png"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetPageWithFormat(name, pageNumber, format)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetWordsPerPage(self):

        try:
            name = "Sample-Annotation.pdf"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetWordsPerPage(name)            

            self.assertIsInstance(response,WordCountResponse.WordCountResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostMovePage(self):
   
        try:
            name = "sample-merged.pdf"
            pageNumber =  1 
            newIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PostMovePage(name, pageNumber, newIndex)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex   
   
    def testPostSignPage(self):

        try:
            name = "Sample-Annotation.pdf"
            pageNumber =  1 
            
            name = "sample-input.pdf"
            signatureFileName = "pkc7-sample.pfx";
            pageNumber = 1
            
            body = Signature.Signature()
            body.Authority =  "Farooq Sheikh"
            body.Location = "Rawalpindi"
            body.Contact =  "farooq.sheikh@aspose.com"
            body.Date =  "06/24/2015 2:00:00.000 AM"     
            body.FormFieldName = "Signature1"     
            body.Password = "aspose"
            
            rect = Rectangle.Rectangle();
            rect.X = 100
            rect.Y = 100
            rect.Height = 100
            rect.Width = 200
            body.Rectangle = rect
            body.SignaturePath = signatureFileName
            body.SignatureType = "PKCS7"
            body.Visible = True 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PostSignPage(name, pageNumber, body)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testPutAddNewPage(self):

        try:
            name = "sample-input.pdf"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PutAddNewPage(name)            

            self.assertIsInstance(response,DocumentPagesResponse.DocumentPagesResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutPageAddStamp(self):

        try:
            name = "sample-input.pdf"
            pageNumber =  1 
            
            body = Stamp.Stamp()
            body.Value = "Aspose"
            body.Background = True
            body.Type = "Text"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PutPageAddStamp(name, pageNumber, body)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testDeleteProperties(self):

        try:
            name = "Sample-Annotation.pdf"
            pageNumber =  1 
            annotationNumber = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.DeleteProperties(name)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testDeleteProperty(self):

        try:
            name = "Sample-Annotation-Property.pdf"
            propertyName = "AsposeDev" 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.DeleteProperty(name, propertyName)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDocumentProperties(self):

        try:
            name = "Sample-Annotation.pdf"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetDocumentProperties(name)            

            self.assertIsInstance(response,DocumentPropertiesResponse.DocumentPropertiesResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetDocumentProperty(self):

        try:
            name = "Sample-Annotation.pdf"
            propertyName = "author";
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetDocumentProperty(name, propertyName)            

            self.assertIsInstance(response,DocumentPropertyResponse.DocumentPropertyResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testPutSetProperty(self):

        try:
            name = "Sample-Annotation.pdf"
            propertyName = "AsposeDev" 
            
            body = DocumentProperty.DocumentProperty()
            body.Name = "AsposeDev"
            body.Value = "Farooq Sheikh"
            body.BuiltIn = False
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PutSetProperty(name, propertyName, body)            

            self.assertIsInstance(response,DocumentPropertyResponse.DocumentPropertyResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
   
    def testGetPageTextItems(self):

        try:
            name = "Sample-Annotation.pdf"
            pageNumber =  1 
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetPageTextItems(name, pageNumber)            

            self.assertIsInstance(response,TextItemsResponse.TextItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetTextItems(self):

        try:
            name = "Sample-Annotation.pdf"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.GetTextItems(name)            

            self.assertIsInstance(response,TextItemsResponse.TextItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostDocumentReplaceText(self):

        try:
            name = "sample-input.pdf"
            
            body = TextReplace.TextReplace()
            body.OldValue = "Sample PDF"
            body.NewValue = "Sample Aspose PDF"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PostDocumentReplaceText(name, body)            

            self.assertIsInstance(response,DocumentTextReplaceResponse.DocumentTextReplaceResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostDocumentReplaceTextList(self):

        try:
            name = "Sample-Annotation.pdf"
            
            body = TextReplaceListRequest.TextReplaceListRequest()
            
            tr1 = TextReplace.TextReplace()
            tr1.OldValue = "Sample"
            tr1.NewValue = "Sample Aspose"
            
            tr2 = TextReplace.TextReplace()
            tr2.OldValue = "PDF"
            tr2.NewValue = "PDF Document"
            
            body.TextReplaces = [tr1, tr2]
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PostDocumentReplaceTextList(name, body)            

            self.assertIsInstance(response,DocumentTextReplaceResponse.DocumentTextReplaceResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostPageReplaceText(self):

        try:
            name = "sample-input.pdf"
            pageNumber =  1 
            
            body = TextReplace.TextReplace()
            body.OldValue = "Sample PDF"
            body.NewValue = "Sample Aspose PDF"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PostPageReplaceText(name, pageNumber, body)            

            self.assertIsInstance(response,PageTextReplaceResponse.PageTextReplaceResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostPageReplaceTextList(self):

        try:
            name = "sample-input.pdf"
            pageNumber = 1
            
            body = TextReplaceListRequest.TextReplaceListRequest()
            
            tr1 = TextReplace.TextReplace()
            tr1.OldValue = "Sample"
            tr1.NewValue = "Sample Aspose"
            
            tr2 = TextReplace.TextReplace()
            tr2.OldValue = "PDF"
            tr2.NewValue = "PDF Document"
            
            body.TextReplaces = [tr1, tr2]
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.pdfApi.PostPageReplaceTextList(name, pageNumber, body)            

            self.assertIsInstance(response,PageTextReplaceResponse.PageTextReplaceResponse)
            self.assertEqual(response.Status,'OK')

        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
if __name__ == '__main__':
    unittest.main()