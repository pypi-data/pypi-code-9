import unittest
import os.path
import json
import inspect
import requests

import asposeslidescloud
from asposeslidescloud.SlidesApi import SlidesApi
from asposeslidescloud.SlidesApi import ApiException
from asposeslidescloud.models import SplitDocumentResponse
from asposeslidescloud.models import DocumentResponse
from asposeslidescloud.models import ImagesResponse
from asposeslidescloud.models import PresentationsMergeRequest
from asposeslidescloud.models import OrderedMergeRequest
from asposeslidescloud.models import PlaceholderResponse
from asposeslidescloud.models import PlaceholdersResponse
from asposeslidescloud.models import DocumentPropertiesResponse
from asposeslidescloud.models import CommonResponse
from asposeslidescloud.models import DocumentProperties
from asposeslidescloud.models import DocumentProperty
from asposeslidescloud.models import DocumentPropertyResponse
from asposeslidescloud.models import ParagraphResponse
from asposeslidescloud.models import ParagraphsResponse
from asposeslidescloud.models import ShapeListResponse
from asposeslidescloud.models import ShapeResponse
from asposeslidescloud.models import PortionResponse
from asposeslidescloud.models import Portion
from asposeslidescloud.models import Shape
from asposeslidescloud.models import SlideListResponse
from asposeslidescloud.models import SlideBackgroundResponse
from asposeslidescloud.models import SlideResponse
from asposeslidescloud.models import SlideCommentsResponse
from asposeslidescloud.models import TextItemsResponse
from asposeslidescloud.models import PresentationStringReplaceResponse
from asposeslidescloud.models import SlideStringReplaceResponse
from asposeslidescloud.models import ThemeResponse
from asposeslidescloud.models import ColorSchemeResponse
from asposeslidescloud.models import FontSchemeResponse
from asposeslidescloud.models import FormatSchemeResponse
from asposeslidescloud.models import PdfExportOptions
from asposeslidescloud.models import TiffExportOptions
from asposeslidescloud.models import HtmlExportOptions

import asposestoragecloud 
from asposestoragecloud.StorageApi import StorageApi


import random
import string

class TestAsposeSlidesCloud(unittest.TestCase):

    def setUp(self):

        with open('setup.json') as json_file:
            data = json.load(json_file)

        self.storageApiClient = asposestoragecloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.storageApi = StorageApi(self.storageApiClient)

        self.apiClient = asposeslidescloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.slidesApi = SlidesApi(self.apiClient)

        self.output_path = str(data['output_location'])

    def testGetSlidesDocument(self):
        try:
            name = "sample.pptx"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesDocument(name)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesDocumentWithFormat(self):
        try:
            name = "sample.pptx"
            format = "tiff"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesDocumentWithFormat(name, format)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostSlidesDocument(self):
        try:
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            name = name  + '.pptx'
            templatePath = "sample.pptx"
            
            response = self.storageApi.PutCreate(templatePath,'./data/' + templatePath)
            response = self.slidesApi.PostSlidesDocument(name, templatePath=templatePath, file = './data/Test.html')            

            self.assertIsInstance(response,DocumentResponse.DocumentResponse)
            self.assertEqual(response.Status,'Created')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostSlidesSplit(self):
        try:
            name = "sample-input.pptx"
            ffrom = 2 
            to = 3
            format = "png"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostSlidesSplit(name, ffrom=ffrom, to=to, format=format)            

            self.assertIsInstance(response,SplitDocumentResponse.SplitDocumentResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutNewPresentation(self):
        try:
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            name = name  + '.pptx'
            
            templatePath = "sample.pptx"
            
            response = self.slidesApi.PutNewPresentation(name, file = './data/' + templatePath)            
            
            self.assertIsInstance(response,DocumentResponse.DocumentResponse)
            self.assertEqual(response.Status,'Created')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutNewPresentationFromStoredTemplate(self):
        try:
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            name = name  + '.pptx'
            
            templatePath = "sample.pptx"
            
            response = self.storageApi.PutCreate(templatePath,'./data/' + templatePath)
            
            response = self.slidesApi.PutNewPresentationFromStoredTemplate(name, templatePath, file=None)            

            self.assertIsInstance(response,DocumentResponse.DocumentResponse)
            self.assertEqual(response.Status,'Created')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutSlidesConvert(self):
        try:
            name = "sample.pptx"
            format = "pdf"
            
            response = self.slidesApi.PutSlidesConvert(file = './data/' + name, format=format)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutSlidesDocumentFromHtml(self):
        try:
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            name = name  + '.pptx'
            
            response = self.slidesApi.PutSlidesDocumentFromHtml(name, file = './data/ReadMe.html')            

            self.assertIsInstance(response,DocumentResponse.DocumentResponse)
            self.assertEqual(response.Status,'Created')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSlidesImages(self):
        try:
            name = "sample-input.pptx"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesImages(name)            

            self.assertIsInstance(response,ImagesResponse.ImagesResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSlidesSlideImages(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesSlideImages(name, slideIndex)            

            self.assertIsInstance(response,ImagesResponse.ImagesResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostPresentationMerge(self):
        try:
            name = "sample.pptx"
            mergeFile1 = "welcome.pptx"
            mergeFile2 = "demo.pptx"
            
            body = PresentationsMergeRequest.PresentationsMergeRequest()
            body.PresentationPaths = [mergeFile1, mergeFile2]
            
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.storageApi.PutCreate(mergeFile1,'./data/' + mergeFile1)
            response = self.storageApi.PutCreate(mergeFile2,'./data/' + mergeFile2)
            
            response = self.slidesApi.PostPresentationMerge(name, body)            

            self.assertIsInstance(response,DocumentResponse.DocumentResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutPresentationMerge(self):
        try:
            name = "sample.pptx"
            mergeFile1 = "welcome.pptx"
            mergeFile2 = "demo.pptx"
            
            body = OrderedMergeRequest.OrderedMergeRequest()
            body.Presentations = [mergeFile1, mergeFile2]
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.storageApi.PutCreate(mergeFile1,'./data/' + mergeFile1)
            response = self.storageApi.PutCreate(mergeFile2,'./data/' + mergeFile2)
            
            response = self.slidesApi.PutPresentationMerge(name, body)            

            self.assertIsInstance(response,DocumentResponse.DocumentResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSlidesPlaceholder(self):
        try:
            name = "sample-input.pptx"
            slideIndex = 1
            placeholderIndex = 0
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesPlaceholder(name, slideIndex, placeholderIndex)            

            self.assertIsInstance(response,PlaceholderResponse.PlaceholderResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSlidesPlaceholders(self):
        try:
            name = "sample-input.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesPlaceholders(name, slideIndex)            

            self.assertIsInstance(response,PlaceholdersResponse.PlaceholdersResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testDeleteSlidesDocumentProperties(self):
        try:
            name = "sample-input.pptx"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.DeleteSlidesDocumentProperties(name)            

            self.assertIsInstance(response,DocumentPropertiesResponse.DocumentPropertiesResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testDeleteSlidesDocumentProperty(self):
        try:
            name = "sample-input.pptx"
            propertyName = "AsposeAuthor"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.DeleteSlidesDocumentProperty(name, propertyName)            

            self.assertIsInstance(response,CommonResponse.CommonResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSlidesDocumentProperties(self):
        try:
            name = "sample-input.pptx"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesDocumentProperties(name)            

            self.assertIsInstance(response,DocumentPropertiesResponse.DocumentPropertiesResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostSlidesSetDocumentProperties(self):
        try:
            name = "sample-input.pptx"
            
            body = DocumentProperties.DocumentProperties()
            
            docprop1 = DocumentProperty.DocumentProperty()
            docprop1.Name = "Author"
            docprop1.Value = "Farooq Sheikh"
            
            
            body.List = [docprop1]
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostSlidesSetDocumentProperties(name, body)            

            self.assertIsInstance(response,DocumentPropertiesResponse.DocumentPropertiesResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutSlidesSetDocumentProperty(self):
        try:
            name = "sample-input.pptx"
            propertyName = "Author"
            
            body = DocumentProperty.DocumentProperty()
            body.Name = "Author"
            body.Value = "Farooq Sheikh"
        
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PutSlidesSetDocumentProperty(name, propertyName, body)            

            self.assertIsInstance(response,DocumentPropertyResponse.DocumentPropertyResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetParagraphPortion(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            shapeIndex = 1
            paragraphIndex = 1
            portionIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetParagraphPortion(name, slideIndex, shapeIndex, paragraphIndex, portionIndex)            

            self.assertIsInstance(response,PortionResponse.PortionResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetShapeParagraph(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            shapeIndex = 1
            paragraphIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetShapeParagraph(name, slideIndex, shapeIndex, paragraphIndex)            

            self.assertIsInstance(response,ParagraphResponse.ParagraphResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSlideShapeParagraphs(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            shapeIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlideShapeParagraphs(name, slideIndex, shapeIndex)            

            self.assertIsInstance(response,ParagraphsResponse.ParagraphsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSlidesSlideShapes(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesSlideShapes(name, slideIndex)            

            self.assertIsInstance(response,ShapeListResponse.ShapeListResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesSlideShapesParent(self):
        try:
            name = "sample-input.pptx"
            slideIndex = 1
            shapePath = "1"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesSlideShapesParent(name, slideIndex, shapePath)            

            self.assertIsInstance(response,ShapeResponse.ShapeResponse)
            self.assertEqual(response.Status,'OK')
            
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPutSetParagraphPortionProperties(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            shapeIndex = 1
            paragraphIndex = 1
            portionIndex = 1

            body = Portion.Portion()
            body.Text = "Aspose.Slides for Python"
            body.FontColor = "#FFFF0000"
            
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PutSetParagraphPortionProperties(name, slideIndex, shapeIndex, paragraphIndex, portionIndex, body)            

            self.assertIsInstance(response,PortionResponse.PortionResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPutSlideShapeInfo(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            shapePath = 1
            
            body = Shape.Shape()
            body.AlternativeText = "Aspose"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PutSlideShapeInfo(name, slideIndex, shapePath, body)            

            self.assertIsInstance(response,ShapeResponse.ShapeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testDeleteSlideByIndex(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.DeleteSlideByIndex(name, slideIndex)            

            self.assertIsInstance(response,SlideListResponse.SlideListResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testDeleteSlidesCleanSlidesList(self):
        try:
            name = "sample.pptx"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.DeleteSlidesCleanSlidesList(name)            

            self.assertIsInstance(response,SlideListResponse.SlideListResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testDeleteSlidesSlideBackground(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.DeleteSlidesSlideBackground(name, slideIndex)            

            self.assertIsInstance(response,SlideBackgroundResponse.SlideBackgroundResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesSlide(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesSlide(name, slideIndex)            

            self.assertIsInstance(response,SlideResponse.SlideResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesSlideBackground(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesSlideBackground(name, slideIndex)            

            self.assertIsInstance(response,SlideBackgroundResponse.SlideBackgroundResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesSlideComments(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesSlideComments(name, slideIndex)            

            self.assertIsInstance(response,SlideCommentsResponse.SlideCommentsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesSlidesList(self):
        try:
            name = "sample.pptx"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesSlidesList(name)            

            self.assertIsInstance(response,SlideListResponse.SlideListResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlideWithFormat(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            format = "pdf"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlideWithFormat(name, slideIndex, format)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPostAddEmptySlide(self):
        try:
            name = "sample.pptx"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostAddEmptySlide(name)            

            self.assertIsInstance(response,SlideListResponse.SlideListResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPostAddEmptySlideAtPosition(self):
        try:
            name = "sample.pptx"
            position = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostAddEmptySlideAtPosition(name, position)            

            self.assertIsInstance(response,SlideListResponse.SlideListResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPostAddSlideCopy(self):
        try:
            name = "sample.pptx"
            slideToClone = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostAddSlideCopy(name, slideToClone)            

            self.assertIsInstance(response,SlideListResponse.SlideListResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPostClonePresentationSlide(self):
        try:
            name = "sample.pptx"
            position = 1
            slideToClone = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostClonePresentationSlide(name, position, slideToClone)            

            self.assertIsInstance(response,SlideListResponse.SlideListResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPostCopySlideFromSourcePresentation(self):
        try:
            name = "sample.pptx"
            slideToCopy = 1
            source = "sample-input.pptx"
            position = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.storageApi.PutCreate(source,'./data/' + source)
            response = self.slidesApi.PostCopySlideFromSourcePresentation(name, slideToCopy, source, position)            

            self.assertIsInstance(response,SlideListResponse.SlideListResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPostSlidesReorderPosition(self):
        try:
            name = "sample-input.pptx"
            oldPosition = 1
            newPosition = 2
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostSlidesReorderPosition(name, oldPosition, newPosition)            

            self.assertIsInstance(response,SlideListResponse.SlideListResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPutSlidesSlideBackground(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PutSlidesSlideBackground(name, slideIndex, body = "#FFFF0000")            

            self.assertIsInstance(response,SlideBackgroundResponse.SlideBackgroundResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesPresentationTextItems(self):
        try:
            name = "sample.pptx"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesPresentationTextItems(name)            

            self.assertIsInstance(response,TextItemsResponse.TextItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesSlideTextItems(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesSlideTextItems(name, slideIndex)            

            self.assertIsInstance(response,TextItemsResponse.TextItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPostSlidesPresentationReplaceText(self):
        try:
            name = "sample.pptx"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostSlidesPresentationReplaceText(name, oldValue = "aspose", newValue = "aspose2")            

            self.assertIsInstance(response,PresentationStringReplaceResponse.PresentationStringReplaceResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPostSlidesSlideReplaceText(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostSlidesSlideReplaceText(name, slideIndex, oldValue = "aspose", newValue = "aspose2")            

            self.assertIsInstance(response,SlideStringReplaceResponse.SlideStringReplaceResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesTheme(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesTheme(name, slideIndex)            

            self.assertIsInstance(response,ThemeResponse.ThemeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesThemeColorScheme(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesThemeColorScheme(name, slideIndex)            

            self.assertIsInstance(response,ColorSchemeResponse.ColorSchemeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetSlidesThemeFontScheme(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesThemeFontScheme(name, slideIndex)            

            self.assertIsInstance(response,FontSchemeResponse.FontSchemeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSlidesThemeFormatScheme(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesThemeFormatScheme(name, slideIndex)            

            self.assertIsInstance(response,FormatSchemeResponse.FormatSchemeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPostAddNewShape(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            
            body = Shape.Shape()
            body.AlternativeText = "Aspose" 
            body.ShapeType = "Line"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostAddNewShape(name, slideIndex, body)            

            self.assertIsInstance(response,ShapeResponse.ShapeResponse)
            self.assertEqual(response.Status,'Created')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetShapeWithFormat(self):
        try:
            name = "sample.pptx"
            slideIndex = 1
            shapeIndex = 1
            format = "png"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetShapeWithFormat(name, slideIndex, shapeIndex, format)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostSlidesSaveAsPdf(self):
        try:
            name = "sample.pptx"
            
            body = PdfExportOptions.PdfExportOptions()
            body.JpegQuality = 50
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostSlidesSaveAsPdf(name, body)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostSlidesSaveAsTiff(self):
        try:
            name = "sample.pptx"
            
            body = TiffExportOptions.TiffExportOptions()
            body.ExportFormat = "tiff"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostSlidesSaveAsTiff(name, body)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostSlidesSaveAsHtml(self):
        try:
            name = "sample.pptx"
            
            body = HtmlExportOptions.HtmlExportOptions()
            body.SaveAsZip = True
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.PostSlidesSaveAsHtml(name, body)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetSlidesDocumentProperty(self):
        try:
            name = "sample.pptx"
            propertyName = "Author"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.slidesApi.GetSlidesDocumentProperty(name, propertyName)            

            self.assertIsInstance(response,DocumentPropertyResponse.DocumentPropertyResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
if __name__ == '__main__':
    unittest.main()