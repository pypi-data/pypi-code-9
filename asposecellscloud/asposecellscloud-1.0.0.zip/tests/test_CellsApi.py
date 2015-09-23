import unittest
import os.path
import json
import inspect
import requests

import asposecellscloud
from asposecellscloud.CellsApi import CellsApi
from asposecellscloud.CellsApi import ApiException
from asposecellscloud.models import CreatePivotTableRequest
from asposecellscloud.models import ColumnsResponse
from asposecellscloud.models import SaaSposeResponse
from asposecellscloud.models import CellResponse
from asposecellscloud.models import CellsResponse
from asposecellscloud.models import StyleResponse
from asposecellscloud.models import ColumnResponse
from asposecellscloud.models import ColumnsResponse
from asposecellscloud.models import RowResponse
from asposecellscloud.models import RowsResponse
from asposecellscloud.models import Style
from asposecellscloud.models import Font
from asposecellscloud.models import AutoShapeResponse
from asposecellscloud.models import AutoShapesResponse
from asposecellscloud.models import ResponseMessage
from asposecellscloud.models import BarcodeResponseList
from asposecellscloud.models import ChartAreaResponse
from asposecellscloud.models import LineResponse
from asposecellscloud.models import FillFormatResponse
from asposecellscloud.models import ChartsResponse
from asposecellscloud.models import ChartResponse
from asposecellscloud.models import LegendResponse
from asposecellscloud.models import Legend
from asposecellscloud.models import Title
from asposecellscloud.models import TitleResponse
from asposecellscloud.models import HyperlinkResponse
from asposecellscloud.models import HyperlinksResponse
from asposecellscloud.models import Hyperlink
from asposecellscloud.models import OleObjectResponse
from asposecellscloud.models import OleObjectsResponse
from asposecellscloud.models import OleObject
from asposecellscloud.models import PictureResponse
from asposecellscloud.models import PicturesResponse
from asposecellscloud.models import Picture
from asposecellscloud.models import PivotTableResponse
from asposecellscloud.models import PivotTablesResponse
from asposecellscloud.models import PivotTableFieldRequest
from asposecellscloud.models import CellsDocumentPropertiesResponse
from asposecellscloud.models import CellsDocumentPropertyResponse
from asposecellscloud.models import CellsDocumentProperty
from asposecellscloud.models import SaveOptions
from asposecellscloud.models import SaveResponse
from asposecellscloud.models import WorkbookEncryptionRequest
from asposecellscloud.models import WorkbookProtectionRequest
from asposecellscloud.models import WorkbookResponse
from asposecellscloud.models import NamesResponse
from asposecellscloud.models import NameResponse
from asposecellscloud.models import TextItemsResponse
from asposecellscloud.models import AutoFitterOptions
from asposecellscloud.models import ImportOption
from asposecellscloud.models import SmartMarkerResultResponse
from asposecellscloud.models import SplitResultResponse
from asposecellscloud.models import WorkbookReplaceResponse
from asposecellscloud.models import PasswordRequest
from asposecellscloud.models import ProtectSheetParameter
from asposecellscloud.models import WorksheetResponse
from asposecellscloud.models import WorksheetsResponse
from asposecellscloud.models import SingleValueResponse
from asposecellscloud.models import CommentResponse
from asposecellscloud.models import CommentsResponse
from asposecellscloud.models import MergedCellResponse
from asposecellscloud.models import MergedCellsResponse
from asposecellscloud.models import AutoFitterOptions
from asposecellscloud.models import WorksheetMovingRequest
from asposecellscloud.models import Worksheet
from asposecellscloud.models import Comment
from asposecellscloud.models import SortKey
from asposecellscloud.models import DataSorter
from asposecellscloud.models import WorksheetReplaceResponse
from asposecellscloud.models import ValidationResponse
from asposecellscloud.models import ValidationsResponse

import asposestoragecloud 
from asposestoragecloud.StorageApi import StorageApi

import random
import string

class TestAsposeCellsCloud(unittest.TestCase):

    def setUp(self):

        with open('setup.json') as json_file:
            data = json.load(json_file)

        self.storageApiClient = asposestoragecloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.storageApi = StorageApi(self.storageApiClient)

        self.apiClient = asposecellscloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.cellsApi = CellsApi(self.apiClient)

        self.output_path = str(data['output_location'])

    def testDeleteWorksheetColumns(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1" 
            columnIndex = 1
            columns = 10
            updateReference = True
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.cellsApi.DeleteWorksheetColumns(name=name, sheetName=sheetName, columnIndex=columnIndex, columns=columns, updateReference=updateReference)            

            self.assertIsInstance(response,ColumnsResponse.ColumnsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
                    
    def testDeleteWorksheetRow(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1" 
            rowIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response = self.cellsApi.DeleteWorksheetRow(name=name, sheetName=sheetName, rowIndex=rowIndex)
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
            
    def testDeleteWorksheetRows(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1" 
            startrow = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorksheetRows(name=name, sheetName=sheetName, startrow=startrow)
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
            
    def testGetWorksheetCell(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1" 
            cellOrMethodName = "a1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetCell(name=name, sheetName=sheetName, cellOrMethodName=cellOrMethodName)
            self.assertIsInstance(response,CellResponse.CellResponse)
            self.assertEqual(response.Status,'OK')
            
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
    
    def testGetWorksheetCellProperty(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1" 
            cellOrMethodName = "maxcolumn"
           
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetCellProperty(name, sheetName, cellOrMethodName)
            self.assertIsInstance(response,int)
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

            
    def testGetWorksheetCells(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetCells(name=name, sheetName=sheetName)
            
            self.assertIsInstance(response,CellsResponse.CellsResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

            
    def testGetWorksheetCellStyle(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            cellName = "a1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetCellStyle(name=name, sheetName=sheetName, cellName=cellName)

            self.assertIsInstance(response,StyleResponse.StyleResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

            
    def testGetWorksheetColumn(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            columnIndex = 1
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetColumn(name=name, sheetName=sheetName, columnIndex=columnIndex)
            
            self.assertIsInstance(response,ColumnResponse.ColumnResponse)
            self.assertEqual(response.Status,'OK')
                        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

            
    def testGetWorksheetColumns(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetColumns(name=name, sheetName=sheetName)
            
            self.assertIsInstance(response,ColumnsResponse.ColumnsResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testGetWorksheetRow(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            rowIndex = 1
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetRow(name=name, sheetName=sheetName, rowIndex=rowIndex)
            
            self.assertIsInstance(response,RowResponse.RowResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetRows(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetRows(name=name, sheetName=sheetName)
            
            self.assertIsInstance(response,RowsResponse.RowsResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostClearContents(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            startRow = 1
            startColumn = 1
            endRow = 2
            endColumn = 2
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostClearContents(name=name, sheetName=sheetName, startRow=startRow, startColumn=startColumn, endRow=endRow, endColumn=endColumn)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostClearFormats(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            startRow = 1
            startColumn = 1
            endRow = 2
            endColumn = 2
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostClearFormats(name, sheetName, startRow=startRow, startColumn=startColumn, endRow=endRow, endColumn=endColumn)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostColumnStyle(self):
        try:
            #TODO FIX IT
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            columnIndex = 0
            
            body = Style.Style()
            font = Font.Font()
            font.Name = "Calibri"
            font.Size = 40
            body.Font = font
            body.Name ="TestStyle"
            #self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostColumnStyle(name=name, sheetName=sheetName, columnIndex=columnIndex, body=body)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostCopyCellIntoCell(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            worksheet =  "Sheet2"
            destCellName = "a1"
            row = 2
            column = 2
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostCopyCellIntoCell(name, destCellName, sheetName, worksheet, row=row, column=column);
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostCopyWorksheetColumns(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            sourceColumnIndex = 2
            destinationColumnIndex = 2
            columnNumber = 2
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostCopyWorksheetColumns(name=name, sheetName=sheetName, sourceColumnIndex=sourceColumnIndex, destinationColumnIndex=destinationColumnIndex, columnNumber=columnNumber)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostCopyWorksheetRows(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            sourceRowIndex = 2
            destinationRowIndex = 2
            rowNumber = 2
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostCopyWorksheetRows(name=name, sheetName=sheetName, sourceRowIndex=sourceRowIndex, destinationRowIndex=destinationRowIndex, rowNumber=rowNumber)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostGroupWorksheetColumns(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            firstIndex = 2
            lastIndex = 3
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostGroupWorksheetColumns(name=name, sheetName=sheetName, firstIndex=firstIndex, lastIndex=lastIndex)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostGroupWorksheetRows(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            firstIndex = 2
            lastIndex = 3
            
            self.storageApi.PutCreate(name,'./data/' + name)            
            response =self.cellsApi.PostGroupWorksheetRows(name=name, sheetName=sheetName, firstIndex=firstIndex, lastIndex=lastIndex)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostHideWorksheetColumns(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            startColumn = 1
            totalColumns = 1
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostHideWorksheetColumns(name=name, sheetName=sheetName, startColumn=startColumn, totalColumns=totalColumns)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostHideWorksheetRows(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            startrow = 1
            totalRows = 1
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostHideWorksheetRows(name=name, sheetName=sheetName, startrow=startrow, totalRows=totalRows)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostRowStyle(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            rowIndex = 1
            
            body = Style.Style()
            font = Font.Font()
            font.Name = "Calibri"
            font.Size = 40
            body.Font = font
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostRowStyle(name=name, sheetName=sheetName, rowIndex=rowIndex, body=body)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostSetCellHtmlString(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            cellName = "a1"
            file = './data/testfile.txt'
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostSetCellHtmlString(name=name, sheetName=sheetName, cellName=cellName, file=file)
            
            self.assertIsInstance(response,CellResponse.CellResponse)
            self.assertEqual(response.Status,'OK')
            
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostSetCellRangeValue(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            cellarea = "A10:B20"
            value = "1234"
            type = "int"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostSetCellRangeValue(name=name, sheetName=sheetName, cellarea=cellarea, type=type, value=value)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostSetWorksheetColumnWidth(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            columnIndex = "1"
            width = "20"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostSetWorksheetColumnWidth(name=name, sheetName=sheetName, columnIndex=columnIndex, width=width)
            
            self.assertIsInstance(response,ColumnResponse.ColumnResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostUngroupWorksheetColumns(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            firstIndex = 1
            lastIndex = 1
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostUngroupWorksheetColumns(name=name, sheetName=sheetName, firstIndex=firstIndex, lastIndex=lastIndex)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostUngroupWorksheetRows(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            firstIndex = 1
            lastIndex = 1
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostUngroupWorksheetRows(name=name, sheetName=sheetName, firstIndex=firstIndex, lastIndex=lastIndex)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostUnhideWorksheetColumns(self):
        try:
            
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            startcolumn = 1
            totalColumns = 1
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostUnhideWorksheetColumns(name=name, sheetName=sheetName, startcolumn=startcolumn, totalColumns=totalColumns)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostUnhideWorksheetRows(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName =  "Sheet1"
            startrow = 1
            totalRows = 1
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostUnhideWorksheetRows(name=name, sheetName=sheetName, startrow=startrow, totalRows=totalRows)
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostUpdateWorksheetCellStyle(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            cellName = "A2:B2"
            
            body = Style.Style()
            
            font = Font.Font()
            font.Name = "Calibri"
            font.Size = 40
            body.Font = font
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostUpdateWorksheetCellStyle(name=name, sheetName=sheetName, cellName=cellName, body=body)            
            self.assertIsInstance(response,StyleResponse.StyleResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostUpdateWorksheetRangeStyle(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            range = "A2"
            
            body = Style.Style()
            
            font = Font.Font()
            font.Name = "Calibri"
            font.Size = 40
            body.Font = font
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostUpdateWorksheetRangeStyle(name=name, sheetName=sheetName, range=range, body=body)            
            self.assertIsInstance(response,StyleResponse.StyleResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            

    def testPostUpdateWorksheetRow(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            rowIndex = 0            
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostUpdateWorksheetRow(name=name, sheetName=sheetName, rowIndex=rowIndex)
                        
            self.assertIsInstance(response,RowResponse.RowResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorksheetCellSetValue(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            cellName = "A1"            
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostWorksheetCellSetValue(name=name, sheetName=sheetName, cellName=cellName)
                        
            self.assertIsInstance(response,CellResponse.CellResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorksheetMerge(self):
        try:
            name = "Sample_Test_Book.xls"            
            sheetName = "Sheet2"
            startRow = 1
            startColumn = 1
            totalRows = 1
            totalColumns = 5
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostWorksheetMerge(name=name, sheetName=sheetName, startRow=startRow, startColumn=startColumn, totalRows=totalRows, totalColumns=totalColumns)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorksheetUnmerge(self):
        try:
            name = "MergeCell_Sample_Test_Book.xls"
            sheetName = "Sheet2"            
            startRow = 1
            startColumn = 1
            totalRows = 1
            totalColumns = 5
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostWorksheetUnmerge(name=name, sheetName=sheetName, startRow=startRow, startColumn=startColumn, totalRows=totalRows, totalColumns=totalColumns)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutInsertWorksheetColumns(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"            
            columnIndex = 1
            columns = 1
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PutInsertWorksheetColumns(name=name, sheetName=sheetName, columnIndex=columnIndex, columns=columns)
                        
            self.assertIsInstance(response,ColumnsResponse.ColumnsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutInsertWorksheetRow(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"            
            rowIndex = 0            
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PutInsertWorksheetRow(name=name, sheetName=sheetName, rowIndex=rowIndex)
                        
            self.assertIsInstance(response,RowResponse.RowResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutInsertWorksheetRows(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"            
            startrow = 0            
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PutInsertWorksheetRows(name=name, sheetName=sheetName, startrow=startrow)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetAutoshape(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet4"            
            autoshapeNumber = 1            
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetAutoshape(name=name, sheetName=sheetName, autoshapeNumber=autoshapeNumber)
                        
            self.assertIsInstance(response,AutoShapeResponse.AutoShapeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetAutoshapes(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet4"            
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetAutoshapes(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,AutoShapesResponse.AutoShapesResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetAutoshapeWithFormat(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet4"
            autoshapeNumber = 1            
            format = "png"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetAutoshapeWithFormat(name=name, sheetName=sheetName, autoshapeNumber=autoshapeNumber, format=format)
            
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetExtractBarcodes(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet6"
            pictureNumber = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetExtractBarcodes(name=name, sheetName=sheetName, pictureNumber=pictureNumber)
                        
            self.assertIsInstance(response,BarcodeResponseList.BarcodeResponseList)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetChartArea(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetChartArea(name=name, sheetName=sheetName, chartIndex=chartIndex)
                        
            self.assertIsInstance(response,ChartAreaResponse.ChartAreaResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetChartAreaBorder(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetChartAreaBorder(name=name, sheetName=sheetName, chartIndex=chartIndex)
                        
            self.assertIsInstance(response,LineResponse.LineResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetChartAreaFillFormat(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetChartAreaFillFormat(name=name, sheetName=sheetName, chartIndex=chartIndex)
                        
            self.assertIsInstance(response,FillFormatResponse.FillFormatResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorksheetChartLegend(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorksheetChartLegend(name=name, sheetName=sheetName, chartIndex=chartIndex)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testDeleteWorksheetClearCharts(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorksheetClearCharts(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorksheetDeleteChart(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorksheetDeleteChart(name=name, sheetName=sheetName, chartIndex=chartIndex)
                        
            self.assertIsInstance(response,ChartsResponse.ChartsResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetChart(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartNumber = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetChart(name=name, sheetName=sheetName, chartNumber=chartNumber)
                        
            self.assertIsInstance(response,ChartResponse.ChartResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetChartLegend(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetChartLegend(name=name, sheetName=sheetName, chartIndex=chartIndex)
                        
            self.assertIsInstance(response,LegendResponse.LegendResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetCharts(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetCharts(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,ChartsResponse.ChartsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetChartWithFormat(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartNumber = 0
            format = "png"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetChartWithFormat(name=name, sheetName=sheetName, chartNumber=chartNumber,format=format)
            
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorksheetChartLegend(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartIndex = 0
            
            body = Legend.Legend()
            body.Height = 200
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostWorksheetChartLegend(name=name, sheetName=sheetName, chartIndex=chartIndex, body=body)
                        
            self.assertIsInstance(response,LegendResponse.LegendResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorksheetChartTitle(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartIndex = 0
            
            body = Title.Title()
            body.Height = 200
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostWorksheetChartTitle(name=name, sheetName=sheetName, chartIndex=chartIndex, body=body)
                        
            self.assertIsInstance(response,TitleResponse.TitleResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorksheetAddChart(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartType = "bar"
            upperLeftRow = 12
            upperLeftColumn = 12
            lowerRightRow = 20
            lowerRightColumn = 20
            area = "A1:A3"
            isVertical = False
            isAutoGetSerialName = True
            title = "SalesState"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PutWorksheetAddChart(name=name, sheetName=sheetName, chartType=chartType, upperLeftRow=upperLeftRow, upperLeftColumn=upperLeftColumn, lowerRightColumn=lowerRightColumn, area=area, isVertical=isVertical, isAutoGetSerialName=isAutoGetSerialName, title=title)
                        
            self.assertIsInstance(response,ChartsResponse.ChartsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorksheetChartLegend(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PutWorksheetChartLegend(name=name, sheetName=sheetName, chartIndex=chartIndex)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorksheetChartTitle(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet5"
            chartIndex = 0
            
            body = Title.Title()
            body.Height = 200
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PutWorksheetChartTitle(name=name, sheetName=sheetName, chartIndex=chartIndex, body=body)
                        
            self.assertIsInstance(response,TitleResponse.TitleResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorkSheetHyperlink(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            hyperlinkIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorkSheetHyperlink(name=name, sheetName=sheetName, hyperlinkIndex=hyperlinkIndex)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorkSheetHyperlinks(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorkSheetHyperlinks(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheetHyperlink(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            hyperlinkIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorkSheetHyperlink(name=name, sheetName=sheetName, hyperlinkIndex=hyperlinkIndex)
                        
            self.assertIsInstance(response,HyperlinkResponse.HyperlinkResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheetHyperlinks(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorkSheetHyperlinks(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,HyperlinksResponse.HyperlinksResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkSheetHyperlink(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            hyperlinkIndex = 0
            
            body = Hyperlink.Hyperlink()
            body.Address ="http://www.aspose.com/cloud/total-api.aspx"
            body.TextToDisplay ="Aspose Cloud APIs"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostWorkSheetHyperlink(name=name, sheetName=sheetName, hyperlinkIndex=hyperlinkIndex, body=body)
                        
            self.assertIsInstance(response,HyperlinkResponse.HyperlinkResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorkSheetHyperlink(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            firstRow = 2
            firstColumn = 2
            totalRows = 2
            totalColumns = 2
            address = "http://www.aspose.com/cloud/total-api.aspx"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PutWorkSheetHyperlink(name=name, sheetName=sheetName, firstRow=firstRow, firstColumn=firstColumn, totalRows=totalRows, totalColumns=totalColumns, address=address)
                        
            self.assertIsInstance(response,HyperlinkResponse.HyperlinkResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorksheetOleObject(self):
        try:
            name = "Embeded_OleObject_Sample_Book1.xlsx"
            sheetName = "Sheet1"
            oleObjectIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorksheetOleObject(name=name, sheetName=sheetName, oleObjectIndex=oleObjectIndex)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorksheetOleObjects(self):
        try:
            name = "Embeded_OleObject_Sample_Book1.xlsx"
            sheetName = "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorksheetOleObjects(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetOleObject(self):
        try:
            name = "Embeded_OleObject_Sample_Book1.xlsx"
            sheetName = "Sheet1"
            objectNumber = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetOleObject(name=name, sheetName=sheetName, objectNumber=objectNumber)
                        
            self.assertIsInstance(response,OleObjectResponse.OleObjectResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetOleObjects(self):
        try:
            name = "Embeded_OleObject_Sample_Book1.xlsx"
            sheetName = "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetOleObjects(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,OleObjectsResponse.OleObjectsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetOleObjectWithFormat(self):
        try:
            name = "Embeded_OleObject_Sample_Book1.xlsx"
            sheetName = "Sheet1"
            objectNumber = 0
            format = "png"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetOleObjectWithFormat(name=name, sheetName=sheetName, objectNumber=objectNumber, format=format)
            
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostUpdateWorksheetOleObject(self):
        try:
            name = "Embeded_OleObject_Sample_Book1.xlsx"
            sheetName = "Sheet1"
            oleObjectIndex = 0
            sourceFileName = "Sample_Book2.xls"
            imageFileName = "aspose-logo.png"
            
            body  = OleObject.OleObject()
            body.SourceFullName = sourceFileName
            body.ImageSourceFullName = imageFileName
            body.UpperLeftRow = 15
            body.UpperLeftColumn = 5
            body.Top = 10
            body.Bottom = 10
            body.Left = 10
            body.Height = 400
            body.Width = 400
            body.IsAutoSize = True

            self.storageApi.PutCreate(name,'./data/' + name)
            self.storageApi.PutCreate(sourceFileName,'./data/' + sourceFileName)
            self.storageApi.PutCreate(imageFileName,'./data/' + imageFileName)
            
            response =self.cellsApi.PostUpdateWorksheetOleObject(name=name, sheetName=sheetName, oleObjectIndex=oleObjectIndex, body=body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorksheetOleObject(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            sourceFileName = "Sample_Book2.xls"
            imageFileName = "aspose-logo.png"
            
            body  = OleObject.OleObject()
            body.SourceFullName = sourceFileName
            body.ImageSourceFullName = imageFileName
            body.UpperLeftRow = 15
            body.UpperLeftColumn = 5
            body.Top = 10
            body.Bottom = 10
            body.Left = 10
            body.Height = 400
            body.Width = 400
            body.IsAutoSize = True

            self.storageApi.PutCreate(name,'./data/' + name)
            self.storageApi.PutCreate(sourceFileName,'./data/' + sourceFileName)
            self.storageApi.PutCreate(imageFileName,'./data/' + imageFileName)
            
            response =self.cellsApi.PutWorksheetOleObject(name=name, sheetName=sheetName, body=body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorksheetPicture(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet6"
            pictureIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorksheetPicture(name=name, sheetName=sheetName, pictureIndex=pictureIndex)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorkSheetPictures(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet6"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorkSheetPictures(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetPicture(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet6"
            pictureNumber = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetPicture(name=name, sheetName=sheetName, pictureNumber=pictureNumber)
                        
            self.assertIsInstance(response,PictureResponse.PictureResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetPictures(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet6"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetPictures(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,PicturesResponse.PicturesResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetPictureWithFormat(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet6"
            pictureNumber = 0
            format = "png"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetPictureWithFormat(name=name, sheetName=sheetName, pictureNumber=pictureNumber, format=format)
            
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkSheetPicture(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet6"
            pictureIndex = 0
            
            body = Picture.Picture()
            body.Name ="aspose-cloud-logo"
            body.RotationAngle = 90.0

            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostWorkSheetPicture(name=name, sheetName=sheetName, pictureIndex=pictureIndex, body=body)
                        
            self.assertIsInstance(response,PictureResponse.PictureResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorksheetAddPicture(self):
        try:            
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet6"            
            upperLeftRow = 5
            upperLeftColumn = 5
            lowerRightRow = 10
            lowerRightColumn = 10
            picturePath = "aspose-cloud.png"


            self.storageApi.PutCreate(name,'./data/' + name)
            self.storageApi.PutCreate(picturePath,'./data/' + picturePath)
            response =self.cellsApi.PutWorksheetAddPicture(name=name, sheetName=sheetName, file=None, picturePath=picturePath, upperLeftRow=upperLeftRow, upperLeftColumn=upperLeftColumn,lowerRightRow=lowerRightRow, lowerRightColumn=lowerRightColumn )
                        
            self.assertIsInstance(response,PicturesResponse.PicturesResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorksheetPivotTable(self):
        try:
            name = "Sample_Pivot_Table_Example.xls"
            sheetName = "Sheet2"
            pivotTableIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorksheetPivotTable(name=name, sheetName=sheetName, pivotTableIndex=pivotTableIndex)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorksheetPivotTables(self):
        try:
            name = "Sample_Pivot_Table_Example.xls"
            sheetName = "Sheet2"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteWorksheetPivotTables(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetPivotTable(self):
        try:
            name = "Sample_Pivot_Table_Example.xls"
            sheetName = "Sheet2"
            pivottableIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetPivotTable(name=name, sheetName=sheetName, pivottableIndex=pivottableIndex)
                        
            self.assertIsInstance(response,PivotTableResponse.PivotTableResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorksheetPivotTables(self):
        try:
            name = "Sample_Pivot_Table_Example.xls"
            sheetName = "Sheet2"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorksheetPivotTables(name=name, sheetName=sheetName)
                        
            self.assertIsInstance(response,PivotTablesResponse.PivotTablesResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostPivotTableCellStyle(self):
        try:
            name = "Sample_Pivot_Table_Example.xls"
            sheetName = "Sheet2"
            pivotTableIndex = 0
            column = 1
            row = 1
            
            body = Style.Style()
            
            font = Font.Font()
            font.Name = "Calibri"
            font.Size = 40
            body.Font = font
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostPivotTableCellStyle(name, sheetName, pivotTableIndex, column, row, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostPivotTableStyle(self):
        try:
            name = "Sample_Pivot_Table_Example.xls"
            sheetName = "Sheet2"
            pivotTableIndex = 0
            
            body = Style.Style()
            
            font = Font.Font()
            font.Name = "Calibri"
            font.Size = 40
            body.Font = font
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostPivotTableStyle(name, sheetName, pivotTableIndex, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutPivotTableField(self):
        try:
            name = "Sample_Pivot_Table_Example.xls"
            sheetName = "Sheet2"
            pivotTableIndex = 0
            pivotFieldType = "Row"
            
            body = PivotTableFieldRequest.PivotTableFieldRequest()
            body.Data = [1,2]
            
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PutPivotTableField(name, sheetName, pivotTableIndex, pivotFieldType, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorksheetPivotTable(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            body = CreatePivotTableRequest.CreatePivotTableRequest()
            body.Name = "MyPivot"
            body.SourceData = "A5:E10"
            body.DestCellName ="H20"
            body.UseSameSource = True
            body.PivotFieldRows = [1]
            body.PivotFieldColumns = [1]
            body.PivotFieldData = [1]

            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PutWorksheetPivotTable(name, sheetName, body)
                        
            self.assertIsInstance(response,PivotTableResponse.PivotTableResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteDocumentProperties(self):
        try:
            name = "Sample_Test_Book.xls"
           
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteDocumentProperties(name)
                        
            self.assertIsInstance(response,CellsDocumentPropertiesResponse.CellsDocumentPropertiesResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteDocumentProperty(self):
        try:
            name = "Sample_Book1.xlsx"
            propertyName = "AsposeAuthor"
           
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteDocumentProperty(name, propertyName)
                        
            self.assertIsInstance(response,CellsDocumentPropertiesResponse.CellsDocumentPropertiesResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetDocumentProperties(self):
        try:
            name = "Sample_Book1.xlsx"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetDocumentProperties(name)
                        
            self.assertIsInstance(response,CellsDocumentPropertiesResponse.CellsDocumentPropertiesResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetDocumentProperty(self):
        try:
            name = "Sample_Book1.xlsx"
            propertyName = "AsposeAuthor"
           
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetDocumentProperty(name, propertyName)
                        
            self.assertIsInstance(response,CellsDocumentPropertyResponse.CellsDocumentPropertyResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutDocumentProperty(self):
        try:
            name = "Sample_Book1.xlsx"
            propertyName = "AsposeAuthor"
           
            body = CellsDocumentProperty.CellsDocumentProperty()
            body.Name ="AsposeAuthor"
            body.Value ="Aspose Plugin Developer"
            body.BuiltIn = False
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PutDocumentProperty(name, propertyName, body)
                        
            self.assertIsInstance(response,CellsDocumentPropertyResponse.CellsDocumentPropertyResponse)
            self.assertEqual(response.Status,'Created')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostDocumentSaveAs(self):
        try:
            name = "Sample_Test_Book.xls"
            newfilename = "Sample_Test_Book.pdf" 
            
            body = SaveOptions.SaveOptions()
                        
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostDocumentSaveAs(name, body, newfilename=newfilename)
                        
            self.assertIsInstance(response,SaveResponse.SaveResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteDecryptDocument(self):
        try:
            name = "encrypted_Sample_Test_Book.xls"
                        
            body = WorkbookEncryptionRequest.WorkbookEncryptionRequest()
            body.EncryptionType = "XOR"
            body.Password = "aspose"
            body.KeyLength = 128
                        
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteDecryptDocument(name, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteDocumentUnProtectFromChanges(self):
        try:
            name = "Sample_Test_Book.xls"
                        
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteDocumentUnProtectFromChanges(name)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteUnProtectDocument(self):
        try:
            name = "Sample_Protected_Test_Book.xls"

            body = WorkbookProtectionRequest.WorkbookProtectionRequest()
            body.Password = "aspose"
            body.ProtectionType = "None"
                        
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.DeleteUnProtectDocument(name, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkBook(self):
        try:
            name = "Sample_Test_Book.xls"

            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorkBook(name)
                        
            self.assertIsInstance(response,WorkbookResponse.WorkbookResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkBookDefaultStyle(self):
        try:
            name = "Sample_Test_Book.xls"

            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorkBookDefaultStyle(name)
                        
            self.assertIsInstance(response,StyleResponse.StyleResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkBookName(self):
        try:
            name = "Sample_Test_Book.xls"
            nameName = "TestRange"

            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorkBookName(name, nameName)
                        
            self.assertIsInstance(response,NameResponse.NameResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkBookNames(self):
        try:
            name = "Sample_Test_Book.xls"

            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorkBookNames(name)
                        
            self.assertIsInstance(response,NamesResponse.NamesResponse)
            self.assertEqual(response.Status,'OK')
            

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkBookTextItems(self):
        try:
            name = "Sample_Test_Book.xls"

            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorkBookTextItems(name)
                        
            self.assertIsInstance(response,TextItemsResponse.TextItemsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkBookWithFormat(self):
        try:
            name = "Sample_Test_Book.xls"
            format = "pdf"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.GetWorkBookWithFormat(name, format)
            
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostAutofitWorkbookRows(self):
        try:
            name = "Sample_Test_Book.xls"
            
            body = AutoFitterOptions.AutoFitterOptions()
            body.IgnoreHidden = True
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostAutofitWorkbookRows(name, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostEncryptDocument(self):
        try:
            name = "Sample_Test_Book.xls"
            
            body = WorkbookEncryptionRequest.WorkbookEncryptionRequest()
            body.EncryptionType = "XOR"
            body.Password = "aspose"
            body.KeyLength = 128
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostEncryptDocument(name, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostImportData(self):
        try:
            name = "Sample_Test_Book.xls"
            
            body = ImportOption.ImportOption()
            body.IsInsert = True
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostImportData(name, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostProtectDocument(self):
        try:
            name = "Sample_Test_Book.xls"
            
            body = WorkbookProtectionRequest.WorkbookProtectionRequest()
            body.Password = "aspose"
            body.ProtectionType = "All"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostProtectDocument(name, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkbookCalculateFormula(self):
        try:
            name = "Sample_Test_Book.xls"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostWorkbookCalculateFormula(name)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkbookGetSmartMarkerResult(self):
        try:
            name = "Sample_SmartMarker.xlsx"
            datafile = "./data/Sample_SmartMarker_Data.xml"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            response =self.cellsApi.PostWorkbookGetSmartMarkerResult(name, file = datafile)
            self.assertIsInstance(response,SmartMarkerResultResponse.SmartMarkerResultResponse)            
            self.assertEqual(response.StatusCode,200)

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkbooksMerge(self):
        try:
            name = "Sample_Book1.xlsx"
            mergeWith = "Sample_Book2.xls"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            self.storageApi.PutCreate(mergeWith,'./data/' + mergeWith)
            
            response =self.cellsApi.PostWorkbooksMerge(name, mergeWith)
                        
            self.assertIsInstance(response,WorkbookResponse.WorkbookResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkbookSplit(self):
        try:
            name = "Sample_Test_Book.xls"
            format = "png"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostWorkbookSplit(name=name, format=format, ffrom=2, to=2)
                        
            self.assertIsInstance(response,SplitResultResponse.SplitResultResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkbooksTextReplace(self):
        try:
            name = "Sample_Test_Book.xls"
            oldValue = "aspose"
            newValue = "aspose.com"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostWorkbooksTextReplace(name, oldValue, newValue)
                        
            self.assertIsInstance(response,WorkbookReplaceResponse.WorkbookReplaceResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkbooksTextSearch(self):
        try:
            name = "Sample_Test_Book.xls"
            text = "aspose"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostWorkbooksTextSearch(name, text)
                        
            self.assertIsInstance(response,TextItemsResponse.TextItemsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutConvertWorkBook(self):
        try:
            name = "Sample_Test_Book.xls"            
            format = "pdf"            
            
            file = './data/' + name
            data = "./data/" + "Sample_SaveOption_Data.xml"
            
            response =self.cellsApi.PutConvertWorkBook(file, data, format=format)

            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutDocumentProtectFromChanges(self):
        try:
            name = "Sample_Test_Book.xls"
            
            body = PasswordRequest.PasswordRequest()
            body.Password = "aspose"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PutDocumentProtectFromChanges(name, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

            
    def testPutWorkbookCreate(self):
        try:
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            name = name + ".xlsx"
            
            response =self.cellsApi.PutWorkbookCreate(name, file = None)
                        
            self.assertIsInstance(response,WorkbookResponse.WorkbookResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteUnprotectWorksheet(self):
        try:
            
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            body = ProtectSheetParameter.ProtectSheetParameter()
            body.ProtectionType = "None"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.DeleteUnprotectWorksheet(name, sheetName, body)
                        
            self.assertIsInstance(response,WorksheetResponse.WorksheetResponse)
            self.assertEqual(response.Status,'OK')
    
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        

    def testDeleteWorksheet(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.DeleteWorksheet(name, sheetName)
                        
            self.assertIsInstance(response,WorksheetsResponse.WorksheetsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorkSheetBackground(self):
        try:
            name = "WorkSheetBackground_Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.DeleteWorkSheetBackground(name, sheetName)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorkSheetComment(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            cellName = "A4"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.DeleteWorkSheetComment(name, sheetName, cellName)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorksheetFreezePanes(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            row = 1
            column = 1
            freezedRows = 1
            freezedColumns = 1
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.DeleteWorksheetFreezePanes(name, sheetName, row, column, freezedRows, freezedColumns)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheet(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheet(name, sheetName)
                        
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheetCalculateFormula(self):

        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            formula = "SUM(A5:A10)"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheetCalculateFormula(name, sheetName, formula)
                        
            self.assertIsInstance(response,SingleValueResponse.SingleValueResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheetComment(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            cellName = "A4"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheetComment(name, sheetName, cellName)
                        
            self.assertIsInstance(response,CommentResponse.CommentResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

            
    def testGetWorkSheetComments(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheetComments(name, sheetName)
                        
            self.assertIsInstance(response,CommentsResponse.CommentsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheetMergedCell(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            mergedCellIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheetMergedCell(name, sheetName, mergedCellIndex)
                        
            self.assertIsInstance(response,MergedCellResponse.MergedCellResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheetMergedCells(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheetMergedCells(name, sheetName)
                        
            self.assertIsInstance(response,MergedCellsResponse.MergedCellsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheets(self):
        try:
            name = "Sample_Test_Book.xls"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheets(name)
                        
            self.assertIsInstance(response,WorksheetsResponse.WorksheetsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheetTextItems(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheetTextItems(name, sheetName)
                        
            self.assertIsInstance(response,TextItemsResponse.TextItemsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
            
    def testGetWorkSheetWithFormat(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheetWithFormat(name, sheetName, format="png")
            
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostAutofitWorksheetRows(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            body = AutoFitterOptions.AutoFitterOptions()
            body.IgnoreHidden = True
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostAutofitWorksheetRows(name, sheetName, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostCopyWorksheet(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet7"
            sourceSheet = "Sheet1"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostCopyWorksheet(name, sheetName, sourceSheet)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostMoveWorksheet(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            body = WorksheetMovingRequest.WorksheetMovingRequest()
            body.DestinationWorksheet = "Sheet5"
            body.Position = "after"

            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostMoveWorksheet(name, sheetName, body)
                        
            self.assertIsInstance(response,WorksheetsResponse.WorksheetsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostRenameWorksheet(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            newname = "newSheet"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostRenameWorksheet(name, sheetName, newname)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostUpdateWorksheetProperty(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            
            body = Worksheet.Worksheet()
            body.Type ="Worksheet"
            body.Name = "Sheet1"
            body.IsGridlinesVisible = True
            body.IsPageBreakPreview = True
            body.IsRulerVisible = True
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostUpdateWorksheetProperty(name, sheetName, body)
                        
            self.assertIsInstance(response,WorksheetResponse.WorksheetResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkSheetComment(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            cellName = "A4"
            
            body = Comment.Comment()
            body.AutoSize = True
            body.Note = "Aspose"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostWorkSheetComment(name, sheetName, cellName, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorksheetRangeSort(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1"
            cellArea = "A5:A10"
            
            sort = SortKey.SortKey()
            sort.Key = 0
            sort.SortOrder = "descending"
            
            body = DataSorter.DataSorter()
            body.CaseSensitive = "false"
            body.HasHeaders = "false" 
            body.SortLeftToRight = "false"
            body.KeyList = [sort] 
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostWorksheetRangeSort(name, sheetName, cellArea, body)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkSheetTextSearch(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            text = "aspose"
           
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostWorkSheetTextSearch(name, sheetName, text)
                        
            self.assertIsInstance(response,TextItemsResponse.TextItemsResponse)
            self.assertEqual(response.Status,'OK')
           
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorsheetTextReplace(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName="Sheet2"
            oldValue = "aspose"
            newValue = "aspose.com"           
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PostWorsheetTextReplace(name, sheetName, oldValue, newValue)
                        
            self.assertIsInstance(response,WorksheetReplaceResponse.WorksheetReplaceResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutAddNewWorksheet(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1-new" 
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PutAddNewWorksheet(name, sheetName)
                        
            self.assertIsInstance(response,WorksheetsResponse.WorksheetsResponse)
            self.assertEqual(response.Status,'Created')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutChangeVisibilityWorksheet(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1" 
            isVisible = False
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PutChangeVisibilityWorksheet(name, sheetName, isVisible)
                        
            self.assertIsInstance(response,WorksheetResponse.WorksheetResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutProtectWorksheet(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1" 
            
            body = ProtectSheetParameter.ProtectSheetParameter()
            body.ProtectionType = "None"

            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PutProtectWorksheet(name, sheetName, body)
                        
            self.assertIsInstance(response,WorksheetResponse.WorksheetResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorkSheetBackground(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1" 
            file = './data/' + 'aspose-cloud.png'
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PutWorkSheetBackground(name, sheetName, file)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorkSheetComment(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet2"
            cellName = "A4"
            
            body = Comment.Comment()
            body.AutoSize = True
            body.Note = "Aspose"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PutWorkSheetComment(name, sheetName, cellName, body)
                        
            self.assertIsInstance(response,CommentResponse.CommentResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorksheetFreezePanes(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet1" 
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.PutWorksheetFreezePanes(name, sheetName, row=1, column=1, freezedRows=1, freezedColumns=1)
                        
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testDeleteWorkSheetValidation(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet3"
            validationIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.DeleteWorkSheetValidation(name, sheetName, validationIndex)
                        
            self.assertIsInstance(response,ValidationResponse.ValidationResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheetValidation(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet3"
            validationIndex = 0
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheetValidation(name, sheetName, validationIndex)
                        
            self.assertIsInstance(response,ValidationResponse.ValidationResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testGetWorkSheetValidations(self):
        try:
            name = "Sample_Test_Book.xls"
            sheetName = "Sheet3"
            
            self.storageApi.PutCreate(name,'./data/' + name)
            
            response =self.cellsApi.GetWorkSheetValidations(name, sheetName)
                        
            self.assertIsInstance(response,ValidationsResponse.ValidationsResponse)
            self.assertEqual(response.Status,'OK')

        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPostWorkSheetValidation(self):
        try:
            print ""
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
    def testPutWorkSheetValidation(self):
        try:
            print ""
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
            
if __name__ == '__main__':
    unittest.main()