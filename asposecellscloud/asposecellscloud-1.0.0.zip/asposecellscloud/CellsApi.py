#!/usr/bin/env python

import sys
import os
import urllib
import json
import re
from models import *
from ApiClient import ApiException


class CellsApi(object):

    def __init__(self, apiClient):
      self.apiClient = apiClient

    

    def DeleteWorksheetColumns(self, name, sheetName, columnIndex, columns, updateReference, **kwargs):
        """Delete worksheet columns.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            columnIndex (int): The column index. (required)

            columns (int): The columns. (required)

            updateReference (bool): The update reference. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: ColumnsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'columnIndex', 'columns', 'updateReference', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetColumns" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/{columnIndex}/?columns={columns}&amp;updateReference={updateReference}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'columnIndex' in allParams and allParams['columnIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "columnIndex" + "}" , str(allParams['columnIndex']))
        else:
            resourcePath = re.sub("[&?]columnIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'columns' in allParams and allParams['columns'] is not None:
            resourcePath = resourcePath.replace("{" + "columns" + "}" , str(allParams['columns']))
        else:
            resourcePath = re.sub("[&?]columns.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'updateReference' in allParams and allParams['updateReference'] is not None:
            resourcePath = resourcePath.replace("{" + "updateReference" + "}" , str(allParams['updateReference']))
        else:
            resourcePath = re.sub("[&?]updateReference.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ColumnsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetRow(self, name, sheetName, rowIndex, **kwargs):
        """Delete worksheet row.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet bame. (required)

            rowIndex (int): The row index. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'rowIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetRow" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/{rowIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rowIndex' in allParams and allParams['rowIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "rowIndex" + "}" , str(allParams['rowIndex']))
        else:
            resourcePath = re.sub("[&?]rowIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetRows(self, name, sheetName, startrow, **kwargs):
        """Delete several worksheet rows.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet bame. (required)

            startrow (int): The begin row index to be operated. (required)

            totalRows (int): Number of rows to be operated. (optional)

            updateReference (bool): Indicates if update references in other worksheets. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'startrow', 'totalRows', 'updateReference', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetRows" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/?startrow={startrow}&amp;appSid={appSid}&amp;totalRows={totalRows}&amp;updateReference={updateReference}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startrow' in allParams and allParams['startrow'] is not None:
            resourcePath = resourcePath.replace("{" + "startrow" + "}" , str(allParams['startrow']))
        else:
            resourcePath = re.sub("[&?]startrow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalRows' in allParams and allParams['totalRows'] is not None:
            resourcePath = resourcePath.replace("{" + "totalRows" + "}" , str(allParams['totalRows']))
        else:
            resourcePath = re.sub("[&?]totalRows.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'updateReference' in allParams and allParams['updateReference'] is not None:
            resourcePath = resourcePath.replace("{" + "updateReference" + "}" , str(allParams['updateReference']))
        else:
            resourcePath = re.sub("[&?]updateReference.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetCell(self, name, sheetName, cellOrMethodName, **kwargs):
        """Read cell data by cell's name.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            cellOrMethodName (str): The cell's or method name. (Method name like firstcell, endcell etc.) (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: CellResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellOrMethodName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetCell" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/{cellOrMethodName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellOrMethodName' in allParams and allParams['cellOrMethodName'] is not None:
            resourcePath = resourcePath.replace("{" + "cellOrMethodName" + "}" , str(allParams['cellOrMethodName']))
        else:
            resourcePath = re.sub("[&?]cellOrMethodName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CellResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)


    def GetWorksheetCellProperty(self, name, sheetName, cellOrMethodName, **kwargs):
        """Read cell data by cell's name.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            cellOrMethodName (str): The cell's or method name. (Method name like firstcell, endcell etc.) (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: int
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellOrMethodName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetCell" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/{cellOrMethodName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellOrMethodName' in allParams and allParams['cellOrMethodName'] is not None:
            resourcePath = resourcePath.replace("{" + "cellOrMethodName" + "}" , str(allParams['cellOrMethodName']))
        else:
            resourcePath = re.sub("[&?]cellOrMethodName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'int', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)
        

    def GetWorksheetCells(self, name, sheetName, **kwargs):
        """Get cells info.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            offest (int): Begginig offset. (optional)

            count (int): Maximum amount of cells in the response. (optional)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder name. (optional)

            

        Returns: CellsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'offest', 'count', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetCells" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/?appSid={appSid}&amp;offest={offest}&amp;count={count}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'offest' in allParams and allParams['offest'] is not None:
            resourcePath = resourcePath.replace("{" + "offest" + "}" , str(allParams['offest']))
        else:
            resourcePath = re.sub("[&?]offest.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'count' in allParams and allParams['count'] is not None:
            resourcePath = resourcePath.replace("{" + "count" + "}" , str(allParams['count']))
        else:
            resourcePath = re.sub("[&?]count.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CellsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetCellStyle(self, name, sheetName, cellName, **kwargs):
        """Read cell's style info.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            cellName (str): Cell's name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: StyleResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetCellStyle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/{cellName}/style/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellName' in allParams and allParams['cellName'] is not None:
            resourcePath = resourcePath.replace("{" + "cellName" + "}" , str(allParams['cellName']))
        else:
            resourcePath = re.sub("[&?]cellName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'StyleResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetColumn(self, name, sheetName, columnIndex, **kwargs):
        """Read worksheet column data by column's index.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            columnIndex (int): The column index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: ColumnResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'columnIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetColumn" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/{columnIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'columnIndex' in allParams and allParams['columnIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "columnIndex" + "}" , str(allParams['columnIndex']))
        else:
            resourcePath = re.sub("[&?]columnIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ColumnResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetColumns(self, **kwargs):
        """Read worksheet columns info.
        Args:
            name (str): The workbook name. (optional)

            sheetName (str): The worksheet name. (optional)

            storage (str): Workbook storage. (optional)

            folder (str): The workdook folder. (optional)

            

        Returns: ColumnsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetColumns" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ColumnsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetRow(self, name, sheetName, rowIndex, **kwargs):
        """Read worksheet row data by row's index.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            rowIndex (int): The row index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: RowResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'rowIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetRow" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/{rowIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rowIndex' in allParams and allParams['rowIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "rowIndex" + "}" , str(allParams['rowIndex']))
        else:
            resourcePath = re.sub("[&?]rowIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'RowResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetRows(self, name, sheetName, **kwargs):
        """Read worksheet rows info.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workdook folder. (optional)

            

        Returns: RowsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetRows" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'RowsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostClearContents(self, name, sheetName, **kwargs):
        """Clear cells contents.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            range (str): The range. (optional)

            startRow (int): The start row. (optional)

            startColumn (int): The start column. (optional)

            endRow (int): The end row. (optional)

            endColumn (int): The end column. (optional)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'range', 'startRow', 'startColumn', 'endRow', 'endColumn', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostClearContents" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/clearcontents/?appSid={appSid}&amp;range={range}&amp;startRow={startRow}&amp;startColumn={startColumn}&amp;endRow={endRow}&amp;endColumn={endColumn}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'range' in allParams and allParams['range'] is not None:
            resourcePath = resourcePath.replace("{" + "range" + "}" , str(allParams['range']))
        else:
            resourcePath = re.sub("[&?]range.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startRow' in allParams and allParams['startRow'] is not None:
            resourcePath = resourcePath.replace("{" + "startRow" + "}" , str(allParams['startRow']))
        else:
            resourcePath = re.sub("[&?]startRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startColumn' in allParams and allParams['startColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "startColumn" + "}" , str(allParams['startColumn']))
        else:
            resourcePath = re.sub("[&?]startColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'endRow' in allParams and allParams['endRow'] is not None:
            resourcePath = resourcePath.replace("{" + "endRow" + "}" , str(allParams['endRow']))
        else:
            resourcePath = re.sub("[&?]endRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'endColumn' in allParams and allParams['endColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "endColumn" + "}" , str(allParams['endColumn']))
        else:
            resourcePath = re.sub("[&?]endColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostClearFormats(self, name, sheetName, **kwargs):
        """Clear cells contents.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            range (str): The range. (optional)

            startRow (int): The start row. (optional)

            startColumn (int): The start column. (optional)

            endRow (int): The end row. (optional)

            endColumn (int): The end column. (optional)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'range', 'startRow', 'startColumn', 'endRow', 'endColumn', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostClearFormats" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/clearformats/?appSid={appSid}&amp;range={range}&amp;startRow={startRow}&amp;startColumn={startColumn}&amp;endRow={endRow}&amp;endColumn={endColumn}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'range' in allParams and allParams['range'] is not None:
            resourcePath = resourcePath.replace("{" + "range" + "}" , str(allParams['range']))
        else:
            resourcePath = re.sub("[&?]range.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startRow' in allParams and allParams['startRow'] is not None:
            resourcePath = resourcePath.replace("{" + "startRow" + "}" , str(allParams['startRow']))
        else:
            resourcePath = re.sub("[&?]startRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startColumn' in allParams and allParams['startColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "startColumn" + "}" , str(allParams['startColumn']))
        else:
            resourcePath = re.sub("[&?]startColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'endRow' in allParams and allParams['endRow'] is not None:
            resourcePath = resourcePath.replace("{" + "endRow" + "}" , str(allParams['endRow']))
        else:
            resourcePath = re.sub("[&?]endRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'endColumn' in allParams and allParams['endColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "endColumn" + "}" , str(allParams['endColumn']))
        else:
            resourcePath = re.sub("[&?]endColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostColumnStyle(self, name, sheetName, columnIndex, body, **kwargs):
        """Set column style
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            columnIndex (int): The column index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            body (Style): Style dto (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'columnIndex', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostColumnStyle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/{columnIndex}/style/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'columnIndex' in allParams and allParams['columnIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "columnIndex" + "}" , str(allParams['columnIndex']))
        else:
            resourcePath = re.sub("[&?]columnIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostCopyCellIntoCell(self, name, destCellName, sheetName, worksheet, **kwargs):
        """Copy cell into cell
        Args:
            name (str): Workbook name. (required)

            destCellName (str): Destination cell name (required)

            sheetName (str): Destination worksheet name. (required)

            worksheet (str): Source worksheet name. (required)

            cellname (str): Source cell name (optional)

            row (int): Source row (optional)

            column (int): Source column (optional)

            storage (str): Storage name (optional)

            folder (str): Folder name (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'destCellName', 'sheetName', 'worksheet', 'cellname', 'row', 'column', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostCopyCellIntoCell" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/{destCellName}/copy/?worksheet={worksheet}&amp;appSid={appSid}&amp;cellname={cellname}&amp;row={row}&amp;column={column}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'destCellName' in allParams and allParams['destCellName'] is not None:
            resourcePath = resourcePath.replace("{" + "destCellName" + "}" , str(allParams['destCellName']))
        else:
            resourcePath = re.sub("[&?]destCellName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'worksheet' in allParams and allParams['worksheet'] is not None:
            resourcePath = resourcePath.replace("{" + "worksheet" + "}" , str(allParams['worksheet']))
        else:
            resourcePath = re.sub("[&?]worksheet.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellname' in allParams and allParams['cellname'] is not None:
            resourcePath = resourcePath.replace("{" + "cellname" + "}" , str(allParams['cellname']))
        else:
            resourcePath = re.sub("[&?]cellname.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'row' in allParams and allParams['row'] is not None:
            resourcePath = resourcePath.replace("{" + "row" + "}" , str(allParams['row']))
        else:
            resourcePath = re.sub("[&?]row.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'column' in allParams and allParams['column'] is not None:
            resourcePath = resourcePath.replace("{" + "column" + "}" , str(allParams['column']))
        else:
            resourcePath = re.sub("[&?]column.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostCopyWorksheetColumns(self, name, sheetName, sourceColumnIndex, destinationColumnIndex, columnNumber, **kwargs):
        """Copy worksheet columns.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            sourceColumnIndex (int): Source column index (required)

            destinationColumnIndex (int): Destination column index (required)

            columnNumber (int): The copied column number (required)

            worksheet (str): The Worksheet (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'sourceColumnIndex', 'destinationColumnIndex', 'columnNumber', 'worksheet', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostCopyWorksheetColumns" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/copy/?sourceColumnIndex={sourceColumnIndex}&amp;destinationColumnIndex={destinationColumnIndex}&amp;columnNumber={columnNumber}&amp;appSid={appSid}&amp;worksheet={worksheet}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sourceColumnIndex' in allParams and allParams['sourceColumnIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "sourceColumnIndex" + "}" , str(allParams['sourceColumnIndex']))
        else:
            resourcePath = re.sub("[&?]sourceColumnIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'destinationColumnIndex' in allParams and allParams['destinationColumnIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "destinationColumnIndex" + "}" , str(allParams['destinationColumnIndex']))
        else:
            resourcePath = re.sub("[&?]destinationColumnIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'columnNumber' in allParams and allParams['columnNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "columnNumber" + "}" , str(allParams['columnNumber']))
        else:
            resourcePath = re.sub("[&?]columnNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'worksheet' in allParams and allParams['worksheet'] is not None:
            resourcePath = resourcePath.replace("{" + "worksheet" + "}" , str(allParams['worksheet']))
        else:
            resourcePath = re.sub("[&?]worksheet.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostCopyWorksheetRows(self, name, sheetName, sourceRowIndex, destinationRowIndex, rowNumber, **kwargs):
        """Copy worksheet rows.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            sourceRowIndex (int): Source row index (required)

            destinationRowIndex (int): Destination row index (required)

            rowNumber (int): The copied row number (required)

            worksheet (str): worksheet (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'sourceRowIndex', 'destinationRowIndex', 'rowNumber', 'worksheet', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostCopyWorksheetRows" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/copy/?sourceRowIndex={sourceRowIndex}&amp;destinationRowIndex={destinationRowIndex}&amp;rowNumber={rowNumber}&amp;appSid={appSid}&amp;worksheet={worksheet}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sourceRowIndex' in allParams and allParams['sourceRowIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "sourceRowIndex" + "}" , str(allParams['sourceRowIndex']))
        else:
            resourcePath = re.sub("[&?]sourceRowIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'destinationRowIndex' in allParams and allParams['destinationRowIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "destinationRowIndex" + "}" , str(allParams['destinationRowIndex']))
        else:
            resourcePath = re.sub("[&?]destinationRowIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rowNumber' in allParams and allParams['rowNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "rowNumber" + "}" , str(allParams['rowNumber']))
        else:
            resourcePath = re.sub("[&?]rowNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'worksheet' in allParams and allParams['worksheet'] is not None:
            resourcePath = resourcePath.replace("{" + "worksheet" + "}" , str(allParams['worksheet']))
        else:
            resourcePath = re.sub("[&?]worksheet.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostGroupWorksheetColumns(self, name, sheetName, firstIndex, lastIndex, **kwargs):
        """Group worksheet columns.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            firstIndex (int): The first column index to be operated. (required)

            lastIndex (int): The last column index to be operated. (required)

            hide (bool): columns visible state (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'firstIndex', 'lastIndex', 'hide', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostGroupWorksheetColumns" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/group/?firstIndex={firstIndex}&amp;lastIndex={lastIndex}&amp;appSid={appSid}&amp;hide={hide}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'firstIndex' in allParams and allParams['firstIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "firstIndex" + "}" , str(allParams['firstIndex']))
        else:
            resourcePath = re.sub("[&?]firstIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'lastIndex' in allParams and allParams['lastIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "lastIndex" + "}" , str(allParams['lastIndex']))
        else:
            resourcePath = re.sub("[&?]lastIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'hide' in allParams and allParams['hide'] is not None:
            resourcePath = resourcePath.replace("{" + "hide" + "}" , str(allParams['hide']))
        else:
            resourcePath = re.sub("[&?]hide.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostGroupWorksheetRows(self, name, sheetName, firstIndex, lastIndex, **kwargs):
        """Group worksheet rows.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            firstIndex (int): The first row index to be operated. (required)

            lastIndex (int): The last row index to be operated. (required)

            hide (bool): rows visible state (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'firstIndex', 'lastIndex', 'hide', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostGroupWorksheetRows" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/group/?firstIndex={firstIndex}&amp;lastIndex={lastIndex}&amp;appSid={appSid}&amp;hide={hide}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'firstIndex' in allParams and allParams['firstIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "firstIndex" + "}" , str(allParams['firstIndex']))
        else:
            resourcePath = re.sub("[&?]firstIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'lastIndex' in allParams and allParams['lastIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "lastIndex" + "}" , str(allParams['lastIndex']))
        else:
            resourcePath = re.sub("[&?]lastIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'hide' in allParams and allParams['hide'] is not None:
            resourcePath = resourcePath.replace("{" + "hide" + "}" , str(allParams['hide']))
        else:
            resourcePath = re.sub("[&?]hide.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostHideWorksheetColumns(self, name, sheetName, startColumn, totalColumns, **kwargs):
        """Hide worksheet columns.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            startColumn (int): The begin column index to be operated. (required)

            totalColumns (int): Number of columns to be operated. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'startColumn', 'totalColumns', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostHideWorksheetColumns" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/hide/?startColumn={startColumn}&amp;totalColumns={totalColumns}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startColumn' in allParams and allParams['startColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "startColumn" + "}" , str(allParams['startColumn']))
        else:
            resourcePath = re.sub("[&?]startColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalColumns' in allParams and allParams['totalColumns'] is not None:
            resourcePath = resourcePath.replace("{" + "totalColumns" + "}" , str(allParams['totalColumns']))
        else:
            resourcePath = re.sub("[&?]totalColumns.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostHideWorksheetRows(self, name, sheetName, startrow, totalRows, **kwargs):
        """Hide worksheet rows.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            startrow (int): The begin row index to be operated. (required)

            totalRows (int): Number of rows to be operated. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'startrow', 'totalRows', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostHideWorksheetRows" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/hide/?startrow={startrow}&amp;totalRows={totalRows}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startrow' in allParams and allParams['startrow'] is not None:
            resourcePath = resourcePath.replace("{" + "startrow" + "}" , str(allParams['startrow']))
        else:
            resourcePath = re.sub("[&?]startrow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalRows' in allParams and allParams['totalRows'] is not None:
            resourcePath = resourcePath.replace("{" + "totalRows" + "}" , str(allParams['totalRows']))
        else:
            resourcePath = re.sub("[&?]totalRows.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostRowStyle(self, name, sheetName, rowIndex, body, **kwargs):
        """Set row style.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            rowIndex (int): The row index. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (Style): Style dto (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'rowIndex', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostRowStyle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/{rowIndex}/style/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rowIndex' in allParams and allParams['rowIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "rowIndex" + "}" , str(allParams['rowIndex']))
        else:
            resourcePath = re.sub("[&?]rowIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostSetCellHtmlString(self, name, sheetName, cellName, file, **kwargs):
        """Set htmlstring value into cell
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            cellName (str): The cell name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            file (File):  (required)

            

        Returns: CellResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellName', 'storage', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSetCellHtmlString" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/{cellName}/htmlstring/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellName' in allParams and allParams['cellName'] is not None:
            resourcePath = resourcePath.replace("{" + "cellName" + "}" , str(allParams['cellName']))
        else:
            resourcePath = re.sub("[&?]cellName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CellResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostSetCellRangeValue(self, name, sheetName, cellarea, value, type, **kwargs):
        """Set cell range value
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            cellarea (str): Cell area (like A1:C2) (required)

            value (str): Range value (required)

            type (str): Value data type (like int) (required)

            storage (str): Storage name (optional)

            folder (str): Folder name (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellarea', 'value', 'type', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSetCellRangeValue" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/?cellarea={cellarea}&amp;value={value}&amp;type={type}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellarea' in allParams and allParams['cellarea'] is not None:
            resourcePath = resourcePath.replace("{" + "cellarea" + "}" , str(allParams['cellarea']))
        else:
            resourcePath = re.sub("[&?]cellarea.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'value' in allParams and allParams['value'] is not None:
            resourcePath = resourcePath.replace("{" + "value" + "}" , str(allParams['value']))
        else:
            resourcePath = re.sub("[&?]value.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'type' in allParams and allParams['type'] is not None:
            resourcePath = resourcePath.replace("{" + "type" + "}" , str(allParams['type']))
        else:
            resourcePath = re.sub("[&?]type.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostSetWorksheetColumnWidth(self, name, sheetName, columnIndex, width, **kwargs):
        """Set worksheet column width.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            columnIndex (int): The column index. (required)

            width (float): The width. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: ColumnResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'columnIndex', 'width', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSetWorksheetColumnWidth" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/{columnIndex}/?width={width}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'columnIndex' in allParams and allParams['columnIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "columnIndex" + "}" , str(allParams['columnIndex']))
        else:
            resourcePath = re.sub("[&?]columnIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'width' in allParams and allParams['width'] is not None:
            resourcePath = resourcePath.replace("{" + "width" + "}" , str(allParams['width']))
        else:
            resourcePath = re.sub("[&?]width.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ColumnResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostUngroupWorksheetColumns(self, name, sheetName, firstIndex, lastIndex, **kwargs):
        """Ungroup worksheet columns.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            firstIndex (int): The first column index to be operated. (required)

            lastIndex (int): The last column index to be operated. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'firstIndex', 'lastIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostUngroupWorksheetColumns" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/ungroup/?firstIndex={firstIndex}&amp;lastIndex={lastIndex}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'firstIndex' in allParams and allParams['firstIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "firstIndex" + "}" , str(allParams['firstIndex']))
        else:
            resourcePath = re.sub("[&?]firstIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'lastIndex' in allParams and allParams['lastIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "lastIndex" + "}" , str(allParams['lastIndex']))
        else:
            resourcePath = re.sub("[&?]lastIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostUngroupWorksheetRows(self, name, sheetName, firstIndex, lastIndex, **kwargs):
        """Ungroup worksheet rows.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            firstIndex (int): The first row index to be operated. (required)

            lastIndex (int): The last row index to be operated. (required)

            isAll (bool): Is all row to be operated (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'firstIndex', 'lastIndex', 'isAll', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostUngroupWorksheetRows" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/ungroup/?firstIndex={firstIndex}&amp;lastIndex={lastIndex}&amp;appSid={appSid}&amp;isAll={isAll}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'firstIndex' in allParams and allParams['firstIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "firstIndex" + "}" , str(allParams['firstIndex']))
        else:
            resourcePath = re.sub("[&?]firstIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'lastIndex' in allParams and allParams['lastIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "lastIndex" + "}" , str(allParams['lastIndex']))
        else:
            resourcePath = re.sub("[&?]lastIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isAll' in allParams and allParams['isAll'] is not None:
            resourcePath = resourcePath.replace("{" + "isAll" + "}" , str(allParams['isAll']))
        else:
            resourcePath = re.sub("[&?]isAll.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostUnhideWorksheetColumns(self, name, sheetName, startcolumn, totalColumns, **kwargs):
        """Unhide worksheet columns.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            startcolumn (int): The begin column index to be operated. (required)

            totalColumns (int): Number of columns to be operated. (required)

            width (float): The new column width. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'startcolumn', 'totalColumns', 'width', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostUnhideWorksheetColumns" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/unhide/?startcolumn={startcolumn}&amp;totalColumns={totalColumns}&amp;appSid={appSid}&amp;width={width}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startcolumn' in allParams and allParams['startcolumn'] is not None:
            resourcePath = resourcePath.replace("{" + "startcolumn" + "}" , str(allParams['startcolumn']))
        else:
            resourcePath = re.sub("[&?]startcolumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalColumns' in allParams and allParams['totalColumns'] is not None:
            resourcePath = resourcePath.replace("{" + "totalColumns" + "}" , str(allParams['totalColumns']))
        else:
            resourcePath = re.sub("[&?]totalColumns.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'width' in allParams and allParams['width'] is not None:
            resourcePath = resourcePath.replace("{" + "width" + "}" , str(allParams['width']))
        else:
            resourcePath = re.sub("[&?]width.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostUnhideWorksheetRows(self, name, sheetName, startrow, totalRows, **kwargs):
        """Unhide worksheet rows.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            startrow (int): The begin row index to be operated. (required)

            totalRows (int): Number of rows to be operated. (required)

            height (float): The new row height. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'startrow', 'totalRows', 'height', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostUnhideWorksheetRows" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/unhide/?startrow={startrow}&amp;totalRows={totalRows}&amp;appSid={appSid}&amp;height={height}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startrow' in allParams and allParams['startrow'] is not None:
            resourcePath = resourcePath.replace("{" + "startrow" + "}" , str(allParams['startrow']))
        else:
            resourcePath = re.sub("[&?]startrow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalRows' in allParams and allParams['totalRows'] is not None:
            resourcePath = resourcePath.replace("{" + "totalRows" + "}" , str(allParams['totalRows']))
        else:
            resourcePath = re.sub("[&?]totalRows.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'height' in allParams and allParams['height'] is not None:
            resourcePath = resourcePath.replace("{" + "height" + "}" , str(allParams['height']))
        else:
            resourcePath = re.sub("[&?]height.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostUpdateWorksheetCellStyle(self, name, sheetName, cellName, body, **kwargs):
        """Update cell's style.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            cellName (str): The cell name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            body (Style): with update style settings. (required)

            

        Returns: StyleResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellName', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostUpdateWorksheetCellStyle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/{cellName}/style/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellName' in allParams and allParams['cellName'] is not None:
            resourcePath = resourcePath.replace("{" + "cellName" + "}" , str(allParams['cellName']))
        else:
            resourcePath = re.sub("[&?]cellName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'StyleResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostUpdateWorksheetRangeStyle(self, name, sheetName, range, body, **kwargs):
        """Update cell's range style.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            range (str): The range. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            body (Style): with update style settings. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'range', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostUpdateWorksheetRangeStyle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/style/?range={range}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'range' in allParams and allParams['range'] is not None:
            resourcePath = resourcePath.replace("{" + "range" + "}" , str(allParams['range']))
        else:
            resourcePath = re.sub("[&?]range.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostUpdateWorksheetRow(self, name, sheetName, rowIndex, **kwargs):
        """Update worksheet row.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            rowIndex (int): The row index. (required)

            height (float): The new row height. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: RowResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'rowIndex', 'height', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostUpdateWorksheetRow" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/{rowIndex}/?appSid={appSid}&amp;height={height}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rowIndex' in allParams and allParams['rowIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "rowIndex" + "}" , str(allParams['rowIndex']))
        else:
            resourcePath = re.sub("[&?]rowIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'height' in allParams and allParams['height'] is not None:
            resourcePath = resourcePath.replace("{" + "height" + "}" , str(allParams['height']))
        else:
            resourcePath = re.sub("[&?]height.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'RowResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorksheetCellSetValue(self, name, sheetName, cellName, **kwargs):
        """Set cell value.
        Args:
            name (str): The document name. (required)

            sheetName (str): The worksheet name. (required)

            cellName (str): The cell name. (required)

            value (str): The cell value. (optional)

            type (str): The value type. (optional)

            formula (str): Formula for cell (optional)

            storage (str): Workbook storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: CellResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellName', 'value', 'type', 'formula', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorksheetCellSetValue" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/{cellName}/?appSid={appSid}&amp;value={value}&amp;type={type}&amp;formula={formula}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellName' in allParams and allParams['cellName'] is not None:
            resourcePath = resourcePath.replace("{" + "cellName" + "}" , str(allParams['cellName']))
        else:
            resourcePath = re.sub("[&?]cellName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'value' in allParams and allParams['value'] is not None:
            resourcePath = resourcePath.replace("{" + "value" + "}" , str(allParams['value']))
        else:
            resourcePath = re.sub("[&?]value.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'type' in allParams and allParams['type'] is not None:
            resourcePath = resourcePath.replace("{" + "type" + "}" , str(allParams['type']))
        else:
            resourcePath = re.sub("[&?]type.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'formula' in allParams and allParams['formula'] is not None:
            resourcePath = resourcePath.replace("{" + "formula" + "}" , str(allParams['formula']))
        else:
            resourcePath = re.sub("[&?]formula.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CellResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorksheetMerge(self, name, sheetName, startRow, startColumn, totalRows, totalColumns, **kwargs):
        """Merge cells.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            startRow (int): The start row. (required)

            startColumn (int): The start column. (required)

            totalRows (int): The total rows (required)

            totalColumns (int): The total columns. (required)

            storage (str): The document storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'startRow', 'startColumn', 'totalRows', 'totalColumns', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorksheetMerge" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/merge/?startRow={startRow}&amp;startColumn={startColumn}&amp;totalRows={totalRows}&amp;totalColumns={totalColumns}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startRow' in allParams and allParams['startRow'] is not None:
            resourcePath = resourcePath.replace("{" + "startRow" + "}" , str(allParams['startRow']))
        else:
            resourcePath = re.sub("[&?]startRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startColumn' in allParams and allParams['startColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "startColumn" + "}" , str(allParams['startColumn']))
        else:
            resourcePath = re.sub("[&?]startColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalRows' in allParams and allParams['totalRows'] is not None:
            resourcePath = resourcePath.replace("{" + "totalRows" + "}" , str(allParams['totalRows']))
        else:
            resourcePath = re.sub("[&?]totalRows.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalColumns' in allParams and allParams['totalColumns'] is not None:
            resourcePath = resourcePath.replace("{" + "totalColumns" + "}" , str(allParams['totalColumns']))
        else:
            resourcePath = re.sub("[&?]totalColumns.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorksheetUnmerge(self, name, sheetName, startRow, startColumn, totalRows, totalColumns, **kwargs):
        """Unmerge cells.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            startRow (int): The start row. (required)

            startColumn (int): The start column. (required)

            totalRows (int): The total rows (required)

            totalColumns (int): The total columns. (required)

            storage (str): The document storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'startRow', 'startColumn', 'totalRows', 'totalColumns', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorksheetUnmerge" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/unmerge/?startRow={startRow}&amp;startColumn={startColumn}&amp;totalRows={totalRows}&amp;totalColumns={totalColumns}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startRow' in allParams and allParams['startRow'] is not None:
            resourcePath = resourcePath.replace("{" + "startRow" + "}" , str(allParams['startRow']))
        else:
            resourcePath = re.sub("[&?]startRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startColumn' in allParams and allParams['startColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "startColumn" + "}" , str(allParams['startColumn']))
        else:
            resourcePath = re.sub("[&?]startColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalRows' in allParams and allParams['totalRows'] is not None:
            resourcePath = resourcePath.replace("{" + "totalRows" + "}" , str(allParams['totalRows']))
        else:
            resourcePath = re.sub("[&?]totalRows.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalColumns' in allParams and allParams['totalColumns'] is not None:
            resourcePath = resourcePath.replace("{" + "totalColumns" + "}" , str(allParams['totalColumns']))
        else:
            resourcePath = re.sub("[&?]totalColumns.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutInsertWorksheetColumns(self, name, sheetName, columnIndex, columns, **kwargs):
        """Insert worksheet columns.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            columnIndex (int): The column index. (required)

            columns (int): The columns. (required)

            updateReference (bool): The update reference. (optional)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: ColumnsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'columnIndex', 'columns', 'updateReference', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutInsertWorksheetColumns" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/columns/{columnIndex}/?columns={columns}&amp;appSid={appSid}&amp;updateReference={updateReference}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'columnIndex' in allParams and allParams['columnIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "columnIndex" + "}" , str(allParams['columnIndex']))
        else:
            resourcePath = re.sub("[&?]columnIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'columns' in allParams and allParams['columns'] is not None:
            resourcePath = resourcePath.replace("{" + "columns" + "}" , str(allParams['columns']))
        else:
            resourcePath = re.sub("[&?]columns.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'updateReference' in allParams and allParams['updateReference'] is not None:
            resourcePath = resourcePath.replace("{" + "updateReference" + "}" , str(allParams['updateReference']))
        else:
            resourcePath = re.sub("[&?]updateReference.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ColumnsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutInsertWorksheetRow(self, name, sheetName, rowIndex, **kwargs):
        """Insert new worksheet row.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            rowIndex (int): The new row index. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: RowResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'rowIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutInsertWorksheetRow" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/{rowIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rowIndex' in allParams and allParams['rowIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "rowIndex" + "}" , str(allParams['rowIndex']))
        else:
            resourcePath = re.sub("[&?]rowIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'RowResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutInsertWorksheetRows(self, name, sheetName, startrow, **kwargs):
        """Insert several new worksheet rows.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            startrow (int): The begin row index to be operated. (required)

            totalRows (int): Number of rows to be operated. (optional)

            updateReference (bool): Indicates if update references in other worksheets. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'startrow', 'totalRows', 'updateReference', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutInsertWorksheetRows" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/cells/rows/?startrow={startrow}&amp;appSid={appSid}&amp;totalRows={totalRows}&amp;updateReference={updateReference}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startrow' in allParams and allParams['startrow'] is not None:
            resourcePath = resourcePath.replace("{" + "startrow" + "}" , str(allParams['startrow']))
        else:
            resourcePath = re.sub("[&?]startrow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalRows' in allParams and allParams['totalRows'] is not None:
            resourcePath = resourcePath.replace("{" + "totalRows" + "}" , str(allParams['totalRows']))
        else:
            resourcePath = re.sub("[&?]totalRows.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'updateReference' in allParams and allParams['updateReference'] is not None:
            resourcePath = resourcePath.replace("{" + "updateReference" + "}" , str(allParams['updateReference']))
        else:
            resourcePath = re.sub("[&?]updateReference.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetAutoshape(self, name, sheetName, autoshapeNumber, **kwargs):
        """Get autoshape info.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            autoshapeNumber (int): The autoshape number. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: AutoShapeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'autoshapeNumber', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetAutoshape" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/autoshapes/{autoshapeNumber}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'autoshapeNumber' in allParams and allParams['autoshapeNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "autoshapeNumber" + "}" , str(allParams['autoshapeNumber']))
        else:
            resourcePath = re.sub("[&?]autoshapeNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'AutoShapeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetAutoshapes(self, name, sheetName, **kwargs):
        """Get worksheet autoshapes info.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: AutoShapesResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetAutoshapes" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/autoshapes/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'AutoShapesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetAutoshapeWithFormat(self, name, sheetName, autoshapeNumber, format, **kwargs):
        """Get autoshape info in some format.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            autoshapeNumber (int): The autoshape number. (required)

            format (str): Autoshape conversion format. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'autoshapeNumber', 'format', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetAutoshapeWithFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/autoshapes/{autoshapeNumber}/?appSid={appSid}&amp;toFormat={toFormat}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'autoshapeNumber' in allParams and allParams['autoshapeNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "autoshapeNumber" + "}" , str(allParams['autoshapeNumber']))
        else:
            resourcePath = re.sub("[&?]autoshapeNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetExtractBarcodes(self, name, sheetName, pictureNumber, **kwargs):
        """Extract barcodes from worksheet picture.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            pictureNumber (int): Picture index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Workbook folder. (optional)

            

        Returns: BarcodeResponseList
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'pictureNumber', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetExtractBarcodes" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pictures/{pictureNumber}/recognize/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pictureNumber' in allParams and allParams['pictureNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "pictureNumber" + "}" , str(allParams['pictureNumber']))
        else:
            resourcePath = re.sub("[&?]pictureNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'BarcodeResponseList', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetChartArea(self, name, sheetName, chartIndex, **kwargs):
        """Get chart area info.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Workbook folder. (optional)

            

        Returns: ChartAreaResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetChartArea" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/chartArea/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ChartAreaResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetChartAreaBorder(self, name, sheetName, chartIndex, **kwargs):
        """Get chart area border info.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Workbook folder. (optional)

            

        Returns: LineResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetChartAreaBorder" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/chartArea/border/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'LineResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetChartAreaFillFormat(self, name, sheetName, chartIndex, **kwargs):
        """Get chart area fill format info.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Workbook folder. (optional)

            

        Returns: FillFormatResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetChartAreaFillFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/chartArea/fillFormat/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'FillFormatResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetChartLegend(self, name, sheetName, chartIndex, **kwargs):
        """Hide legend in chart
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetChartLegend" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/legend/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetChartTitle(self, name, sheetName, chartIndex, **kwargs):
        """Hide title in chart
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetChartTitle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/title/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetClearCharts(self, name, sheetName, **kwargs):
        """Clear the charts.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetClearCharts" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetDeleteChart(self, name, sheetName, chartIndex, **kwargs):
        """Delete worksheet chart by index.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: ChartsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetDeleteChart" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ChartsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetChart(self, name, sheetName, chartNumber, **kwargs):
        """Get chart info.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            chartNumber (int): The chart number. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The document folder. (optional)
            

        Returns: ChartResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartNumber', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetChart" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartNumber}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartNumber' in allParams and allParams['chartNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "chartNumber" + "}" , str(allParams['chartNumber']))
        else:
            resourcePath = re.sub("[&?]chartNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = {}
        bodyParam = None

        headerParams['Accept'] = 'application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ChartResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetChartLegend(self, name, sheetName, chartIndex, **kwargs):
        """Get chart legend
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: LegendResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetChartLegend" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/legend/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'LegendResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetCharts(self, name, sheetName, **kwargs):
        """Get worksheet charts info.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: ChartsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetCharts" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ChartsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetChartWithFormat(self, name, sheetName, chartNumber, format, **kwargs):
        """Get chart in some format.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            chartNumber (int): The chart number. (required)

            format (str): Chart conversion format. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartNumber', 'format', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetChartWithFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartNumber}/?appSid={appSid}&amp;toFormat={toFormat}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartNumber' in allParams and allParams['chartNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "chartNumber" + "}" , str(allParams['chartNumber']))
        else:
            resourcePath = re.sub("[&?]chartNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorksheetChartLegend(self, name, sheetName, chartIndex, body, **kwargs):
        """Update chart legend
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            body (Legend):  (required)

            

        Returns: LegendResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorksheetChartLegend" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/legend/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'LegendResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorksheetChartTitle(self, name, sheetName, chartIndex, body, **kwargs):
        """Update chart title
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            body (Title): Chart title (required)

            

        Returns: TitleResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorksheetChartTitle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/title/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'TitleResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorksheetAddChart(self, name, sheetName, chartType, **kwargs):
        """Add new chart to worksheet.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): The worksheet name. (required)

            chartType (str): Chart type, please refer property Type in chart resource. (required)

            upperLeftRow (int): New chart upper left row. (optional)

            upperLeftColumn (int): New chart upperleft column. (optional)

            lowerRightRow (int): New chart lower right row. (optional)

            lowerRightColumn (int): New chart lower right column. (optional)

            area (str): Specifies values from which to plot the data series. (optional)

            isVertical (bool): Specifies whether to plot the series from a range of cell values by row or by column. (optional)

            categoryData (str): Gets or sets the range of category Axis values. It can be a range of cells (such as, d1:e10). (optional)

            isAutoGetSerialName (bool): Specifies whether auto update serial name. (optional)

            title (str): Specifies chart title name. (optional)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: ChartsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartType', 'upperLeftRow', 'upperLeftColumn', 'lowerRightRow', 'lowerRightColumn', 'area', 'isVertical', 'categoryData', 'isAutoGetSerialName', 'title', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorksheetAddChart" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/?chartType={chartType}&amp;appSid={appSid}&amp;upperLeftRow={upperLeftRow}&amp;upperLeftColumn={upperLeftColumn}&amp;lowerRightRow={lowerRightRow}&amp;lowerRightColumn={lowerRightColumn}&amp;area={area}&amp;isVertical={isVertical}&amp;categoryData={categoryData}&amp;isAutoGetSerialName={isAutoGetSerialName}&amp;title={title}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartType' in allParams and allParams['chartType'] is not None:
            resourcePath = resourcePath.replace("{" + "chartType" + "}" , str(allParams['chartType']))
        else:
            resourcePath = re.sub("[&?]chartType.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'upperLeftRow' in allParams and allParams['upperLeftRow'] is not None:
            resourcePath = resourcePath.replace("{" + "upperLeftRow" + "}" , str(allParams['upperLeftRow']))
        else:
            resourcePath = re.sub("[&?]upperLeftRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'upperLeftColumn' in allParams and allParams['upperLeftColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "upperLeftColumn" + "}" , str(allParams['upperLeftColumn']))
        else:
            resourcePath = re.sub("[&?]upperLeftColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'lowerRightRow' in allParams and allParams['lowerRightRow'] is not None:
            resourcePath = resourcePath.replace("{" + "lowerRightRow" + "}" , str(allParams['lowerRightRow']))
        else:
            resourcePath = re.sub("[&?]lowerRightRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'lowerRightColumn' in allParams and allParams['lowerRightColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "lowerRightColumn" + "}" , str(allParams['lowerRightColumn']))
        else:
            resourcePath = re.sub("[&?]lowerRightColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'area' in allParams and allParams['area'] is not None:
            resourcePath = resourcePath.replace("{" + "area" + "}" , str(allParams['area']))
        else:
            resourcePath = re.sub("[&?]area.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isVertical' in allParams and allParams['isVertical'] is not None:
            resourcePath = resourcePath.replace("{" + "isVertical" + "}" , str(allParams['isVertical']))
        else:
            resourcePath = re.sub("[&?]isVertical.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'categoryData' in allParams and allParams['categoryData'] is not None:
            resourcePath = resourcePath.replace("{" + "categoryData" + "}" , str(allParams['categoryData']))
        else:
            resourcePath = re.sub("[&?]categoryData.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isAutoGetSerialName' in allParams and allParams['isAutoGetSerialName'] is not None:
            resourcePath = resourcePath.replace("{" + "isAutoGetSerialName" + "}" , str(allParams['isAutoGetSerialName']))
        else:
            resourcePath = re.sub("[&?]isAutoGetSerialName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'title' in allParams and allParams['title'] is not None:
            resourcePath = resourcePath.replace("{" + "title" + "}" , str(allParams['title']))
        else:
            resourcePath = re.sub("[&?]title.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ChartsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorksheetChartLegend(self, name, sheetName, chartIndex, **kwargs):
        """Show legend in chart
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorksheetChartLegend" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/legend/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorksheetChartTitle(self, name, sheetName, chartIndex, body, **kwargs):
        """Add chart title / Set chart title visible
        Args:
            name (str): Workbook name. (required)

            sheetName (str): Worksheet name. (required)

            chartIndex (int): The chart index. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            body (Title): Chart title. (required)

            

        Returns: TitleResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'chartIndex', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorksheetChartTitle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/charts/{chartIndex}/title/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'chartIndex' in allParams and allParams['chartIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "chartIndex" + "}" , str(allParams['chartIndex']))
        else:
            resourcePath = re.sub("[&?]chartIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'TitleResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorkSheetHyperlink(self, name, sheetName, hyperlinkIndex, **kwargs):
        """Delete worksheet hyperlink by index.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            hyperlinkIndex (int): The hyperlink's index. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'hyperlinkIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorkSheetHyperlink" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/hyperlinks/{hyperlinkIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'hyperlinkIndex' in allParams and allParams['hyperlinkIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "hyperlinkIndex" + "}" , str(allParams['hyperlinkIndex']))
        else:
            resourcePath = re.sub("[&?]hyperlinkIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorkSheetHyperlinks(self, name, sheetName, **kwargs):
        """Delete all hyperlinks in worksheet.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorkSheetHyperlinks" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/hyperlinks/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetHyperlink(self, name, sheetName, hyperlinkIndex, **kwargs):
        """Get worksheet hyperlink by index.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            hyperlinkIndex (int): The hyperlink's index. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: HyperlinkResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'hyperlinkIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetHyperlink" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/hyperlinks/{hyperlinkIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'hyperlinkIndex' in allParams and allParams['hyperlinkIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "hyperlinkIndex" + "}" , str(allParams['hyperlinkIndex']))
        else:
            resourcePath = re.sub("[&?]hyperlinkIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'HyperlinkResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetHyperlinks(self, name, sheetName, **kwargs):
        """Get worksheet hyperlinks.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: HyperlinksResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetHyperlinks" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/hyperlinks/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'HyperlinksResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkSheetHyperlink(self, name, sheetName, hyperlinkIndex, body, **kwargs):
        """Update worksheet hyperlink by index.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            hyperlinkIndex (int): The hyperlink's index. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (Hyperlink): Hyperlink object (required)

            

        Returns: HyperlinkResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'hyperlinkIndex', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkSheetHyperlink" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/hyperlinks/{hyperlinkIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'hyperlinkIndex' in allParams and allParams['hyperlinkIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "hyperlinkIndex" + "}" , str(allParams['hyperlinkIndex']))
        else:
            resourcePath = re.sub("[&?]hyperlinkIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'HyperlinkResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorkSheetHyperlink(self, name, sheetName, firstRow, firstColumn, totalRows, totalColumns, address, **kwargs):
        """Add worksheet hyperlink.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            firstRow (int):  (required)

            firstColumn (int):  (required)

            totalRows (int):  (required)

            totalColumns (int):  (required)

            address (str):  (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: HyperlinkResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'firstRow', 'firstColumn', 'totalRows', 'totalColumns', 'address', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorkSheetHyperlink" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/hyperlinks/?appSid={appSid}&amp;firstRow={firstRow}&amp;firstColumn={firstColumn}&amp;totalRows={totalRows}&amp;totalColumns={totalColumns}&amp;address={address}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'firstRow' in allParams and allParams['firstRow'] is not None:
            resourcePath = resourcePath.replace("{" + "firstRow" + "}" , str(allParams['firstRow']))
        else:
            resourcePath = re.sub("[&?]firstRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'firstColumn' in allParams and allParams['firstColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "firstColumn" + "}" , str(allParams['firstColumn']))
        else:
            resourcePath = re.sub("[&?]firstColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalRows' in allParams and allParams['totalRows'] is not None:
            resourcePath = resourcePath.replace("{" + "totalRows" + "}" , str(allParams['totalRows']))
        else:
            resourcePath = re.sub("[&?]totalRows.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'totalColumns' in allParams and allParams['totalColumns'] is not None:
            resourcePath = resourcePath.replace("{" + "totalColumns" + "}" , str(allParams['totalColumns']))
        else:
            resourcePath = re.sub("[&?]totalColumns.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'address' in allParams and allParams['address'] is not None:
            resourcePath = resourcePath.replace("{" + "address" + "}" , str(allParams['address']))
        else:
            resourcePath = re.sub("[&?]address.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'HyperlinkResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetOleObject(self, name, sheetName, oleObjectIndex, **kwargs):
        """Delete OLE object.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worsheet name. (required)

            oleObjectIndex (int): Ole object index (required)

            storage (str): The workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'oleObjectIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetOleObject" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/oleobjects/{oleObjectIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'oleObjectIndex' in allParams and allParams['oleObjectIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "oleObjectIndex" + "}" , str(allParams['oleObjectIndex']))
        else:
            resourcePath = re.sub("[&?]oleObjectIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetOleObjects(self, name, sheetName, **kwargs):
        """Delete all OLE objects.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worsheet name. (required)

            storage (str): The workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetOleObjects" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/oleobjects/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetOleObject(self, name, sheetName, objectNumber, **kwargs):
        """Get OLE object info.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            objectNumber (int): The object number. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: OleObjectResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'objectNumber', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetOleObject" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/oleobjects/{objectNumber}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'objectNumber' in allParams and allParams['objectNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "objectNumber" + "}" , str(allParams['objectNumber']))
        else:
            resourcePath = re.sub("[&?]objectNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'OleObjectResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetOleObjects(self, name, sheetName, **kwargs):
        """Get worksheet OLE objects info.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: OleObjectsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetOleObjects" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/oleobjects/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'OleObjectsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetOleObjectWithFormat(self, name, sheetName, objectNumber, format, **kwargs):
        """Get OLE object info or get the OLE object in some format.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            objectNumber (int): The object number. (required)

            format (str): Object conversion format. (required)

            storage (str): Workbook storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'objectNumber', 'format', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetOleObjectWithFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/oleobjects/{objectNumber}/?appSid={appSid}&amp;toFormat={toFormat}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'objectNumber' in allParams and allParams['objectNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "objectNumber" + "}" , str(allParams['objectNumber']))
        else:
            resourcePath = re.sub("[&?]objectNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostUpdateWorksheetOleObject(self, name, sheetName, oleObjectIndex, body, **kwargs):
        """Update OLE object.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worsheet name. (required)

            oleObjectIndex (int): Ole object index (required)

            storage (str): The workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            body (OleObject): Ole Object (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'oleObjectIndex', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostUpdateWorksheetOleObject" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/oleobjects/{oleObjectIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'oleObjectIndex' in allParams and allParams['oleObjectIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "oleObjectIndex" + "}" , str(allParams['oleObjectIndex']))
        else:
            resourcePath = re.sub("[&?]oleObjectIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorksheetOleObject(self, name, sheetName, body, **kwargs):
        """Add OLE object
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worsheet name. (required)

            upperLeftRow (int): Upper left row index (optional)

            upperLeftColumn (int): Upper left column index (optional)

            height (int): Height of oleObject, in unit of pixel (optional)

            width (int): Width of oleObject, in unit of pixel (optional)

            oleFile (str): OLE filename (optional)

            imageFile (str): Image filename (optional)

            storage (str): The workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            body (OleObject): Ole Object (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'upperLeftRow', 'upperLeftColumn', 'height', 'width', 'oleFile', 'imageFile', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorksheetOleObject" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/oleobjects/?appSid={appSid}&amp;upperLeftRow={upperLeftRow}&amp;upperLeftColumn={upperLeftColumn}&amp;height={height}&amp;width={width}&amp;oleFile={oleFile}&amp;imageFile={imageFile}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'upperLeftRow' in allParams and allParams['upperLeftRow'] is not None:
            resourcePath = resourcePath.replace("{" + "upperLeftRow" + "}" , str(allParams['upperLeftRow']))
        else:
            resourcePath = re.sub("[&?]upperLeftRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'upperLeftColumn' in allParams and allParams['upperLeftColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "upperLeftColumn" + "}" , str(allParams['upperLeftColumn']))
        else:
            resourcePath = re.sub("[&?]upperLeftColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'height' in allParams and allParams['height'] is not None:
            resourcePath = resourcePath.replace("{" + "height" + "}" , str(allParams['height']))
        else:
            resourcePath = re.sub("[&?]height.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'width' in allParams and allParams['width'] is not None:
            resourcePath = resourcePath.replace("{" + "width" + "}" , str(allParams['width']))
        else:
            resourcePath = re.sub("[&?]width.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'oleFile' in allParams and allParams['oleFile'] is not None:
            resourcePath = resourcePath.replace("{" + "oleFile" + "}" , str(allParams['oleFile']))
        else:
            resourcePath = re.sub("[&?]oleFile.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'imageFile' in allParams and allParams['imageFile'] is not None:
            resourcePath = resourcePath.replace("{" + "imageFile" + "}" , str(allParams['imageFile']))
        else:
            resourcePath = re.sub("[&?]imageFile.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetPicture(self, name, sheetName, pictureIndex, **kwargs):
        """Delete a picture object in worksheet
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worsheet name. (required)

            pictureIndex (int): Picture index (required)

            storage (str): The workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'pictureIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetPicture" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pictures/{pictureIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pictureIndex' in allParams and allParams['pictureIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "pictureIndex" + "}" , str(allParams['pictureIndex']))
        else:
            resourcePath = re.sub("[&?]pictureIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorkSheetPictures(self, name, sheetName, **kwargs):
        """Delete all pictures in worksheet.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorkSheetPictures" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pictures/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetPicture(self, name, sheetName, pictureNumber, **kwargs):
        """GRead worksheet picture by number.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            pictureNumber (int): The picture number. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: PictureResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'pictureNumber', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetPicture" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pictures/{pictureNumber}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pictureNumber' in allParams and allParams['pictureNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "pictureNumber" + "}" , str(allParams['pictureNumber']))
        else:
            resourcePath = re.sub("[&?]pictureNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'PictureResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetPictures(self, name, sheetName, **kwargs):
        """Read worksheet pictures.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: PicturesResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetPictures" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pictures/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'PicturesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetPictureWithFormat(self, name, sheetName, pictureNumber, format, **kwargs):
        """GRead worksheet picture by number.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            pictureNumber (int): The picture number. (required)

            format (str): Picture conversion format. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'pictureNumber', 'format', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetPictureWithFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pictures/{pictureNumber}/?appSid={appSid}&amp;toFormat={toFormat}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pictureNumber' in allParams and allParams['pictureNumber'] is not None:
            resourcePath = resourcePath.replace("{" + "pictureNumber" + "}" , str(allParams['pictureNumber']))
        else:
            resourcePath = re.sub("[&?]pictureNumber.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkSheetPicture(self, name, sheetName, pictureIndex, body, **kwargs):
        """Update worksheet picture by index.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            pictureIndex (int): The picture's index. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (Picture): Picture object (required)

            

        Returns: PictureResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'pictureIndex', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkSheetPicture" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pictures/{pictureIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pictureIndex' in allParams and allParams['pictureIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "pictureIndex" + "}" , str(allParams['pictureIndex']))
        else:
            resourcePath = re.sub("[&?]pictureIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'PictureResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorksheetAddPicture(self, name, sheetName, file, **kwargs):
        """Add a new worksheet picture.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worsheet name. (required)

            upperLeftRow (int): The image upper left row. (optional)

            upperLeftColumn (int): The image upper left column. (optional)

            lowerRightRow (int): The image low right row. (optional)

            lowerRightColumn (int): The image low right column. (optional)

            picturePath (str): The picture path, if not provided the picture data is inspected in the request body. (optional)

            storage (str): The workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            file (File):  (required)

            

        Returns: PicturesResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'upperLeftRow', 'upperLeftColumn', 'lowerRightRow', 'lowerRightColumn', 'picturePath', 'storage', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorksheetAddPicture" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pictures/?appSid={appSid}&amp;upperLeftRow={upperLeftRow}&amp;upperLeftColumn={upperLeftColumn}&amp;lowerRightRow={lowerRightRow}&amp;lowerRightColumn={lowerRightColumn}&amp;picturePath={picturePath}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'upperLeftRow' in allParams and allParams['upperLeftRow'] is not None:
            resourcePath = resourcePath.replace("{" + "upperLeftRow" + "}" , str(allParams['upperLeftRow']))
        else:
            resourcePath = re.sub("[&?]upperLeftRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'upperLeftColumn' in allParams and allParams['upperLeftColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "upperLeftColumn" + "}" , str(allParams['upperLeftColumn']))
        else:
            resourcePath = re.sub("[&?]upperLeftColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'lowerRightRow' in allParams and allParams['lowerRightRow'] is not None:
            resourcePath = resourcePath.replace("{" + "lowerRightRow" + "}" , str(allParams['lowerRightRow']))
        else:
            resourcePath = re.sub("[&?]lowerRightRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'lowerRightColumn' in allParams and allParams['lowerRightColumn'] is not None:
            resourcePath = resourcePath.replace("{" + "lowerRightColumn" + "}" , str(allParams['lowerRightColumn']))
        else:
            resourcePath = re.sub("[&?]lowerRightColumn.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'picturePath' in allParams and allParams['picturePath'] is not None:
            resourcePath = resourcePath.replace("{" + "picturePath" + "}" , str(allParams['picturePath']))
        else:
            resourcePath = re.sub("[&?]picturePath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = {}
        
        if file is not None:
            files = { 'file':open(file, 'rb')}
            
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'PicturesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetPivotTable(self, name, sheetName, pivotTableIndex, **kwargs):
        """Delete worksheet pivot table by index
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            pivotTableIndex (int): Pivot table index (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'pivotTableIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetPivotTable" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pivottables/{pivotTableIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pivotTableIndex' in allParams and allParams['pivotTableIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "pivotTableIndex" + "}" , str(allParams['pivotTableIndex']))
        else:
            resourcePath = re.sub("[&?]pivotTableIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetPivotTables(self, name, sheetName, **kwargs):
        """Delete worksheet pivot tables
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetPivotTables" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pivottables/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetPivotTable(self, name, sheetName, pivottableIndex, **kwargs):
        """Get worksheet pivottable info by index.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            pivottableIndex (int):  (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: PivotTableResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'pivottableIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetPivotTable" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pivottables/{pivottableIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pivottableIndex' in allParams and allParams['pivottableIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "pivottableIndex" + "}" , str(allParams['pivottableIndex']))
        else:
            resourcePath = re.sub("[&?]pivottableIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'PivotTableResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorksheetPivotTables(self, name, sheetName, **kwargs):
        """Get worksheet pivottables info.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: PivotTablesResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorksheetPivotTables" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pivottables/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'PivotTablesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostPivotTableCellStyle(self, name, sheetName, pivotTableIndex, column, row, body, **kwargs):
        """Update cell style for pivot table
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            pivotTableIndex (int): Pivot table index (required)

            column (int):  (required)

            row (int):  (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            body (Style): Style dto in request body. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'pivotTableIndex', 'column', 'row', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostPivotTableCellStyle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pivottables/{pivotTableIndex}/Format/?column={column}&amp;row={row}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pivotTableIndex' in allParams and allParams['pivotTableIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "pivotTableIndex" + "}" , str(allParams['pivotTableIndex']))
        else:
            resourcePath = re.sub("[&?]pivotTableIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'column' in allParams and allParams['column'] is not None:
            resourcePath = resourcePath.replace("{" + "column" + "}" , str(allParams['column']))
        else:
            resourcePath = re.sub("[&?]column.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'row' in allParams and allParams['row'] is not None:
            resourcePath = resourcePath.replace("{" + "row" + "}" , str(allParams['row']))
        else:
            resourcePath = re.sub("[&?]row.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostPivotTableStyle(self, name, sheetName, pivotTableIndex, body, **kwargs):
        """Update style for pivot table
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            pivotTableIndex (int): Pivot table index (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            body (Style): Style dto in request body. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'pivotTableIndex', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostPivotTableStyle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pivottables/{pivotTableIndex}/FormatAll/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pivotTableIndex' in allParams and allParams['pivotTableIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "pivotTableIndex" + "}" , str(allParams['pivotTableIndex']))
        else:
            resourcePath = re.sub("[&?]pivotTableIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutPivotTableField(self, name, sheetName, pivotTableIndex, pivotFieldType, body, **kwargs):
        """Add pivot field into into pivot table
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            pivotTableIndex (int): Pivot table index (required)

            pivotFieldType (str):  (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            body (PivotTableFieldRequest): Dto that conrains field indexes (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'pivotTableIndex', 'pivotFieldType', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutPivotTableField" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pivottables/{pivotTableIndex}/PivotField/?pivotFieldType={pivotFieldType}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pivotTableIndex' in allParams and allParams['pivotTableIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "pivotTableIndex" + "}" , str(allParams['pivotTableIndex']))
        else:
            resourcePath = re.sub("[&?]pivotTableIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pivotFieldType' in allParams and allParams['pivotFieldType'] is not None:
            resourcePath = resourcePath.replace("{" + "pivotFieldType" + "}" , str(allParams['pivotFieldType']))
        else:
            resourcePath = re.sub("[&?]pivotFieldType.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorksheetPivotTable(self, name, sheetName, body, **kwargs):
        """Add a pivot table into worksheet.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): Workbook storage. (optional)

            folder (str): Document's folder. (optional)

            sourceData (str): The data for the new PivotTable cache. (optional)

            destCellName (str): The cell in the upper-left corner of the PivotTable report's destination range. (optional)

            tableName (str): The name of the new PivotTable report. (optional)

            useSameSource (bool): Indicates whether using same data source when another existing pivot table has used this data source. If the property is true, it will save memory. (optional)

            body (CreatePivotTableRequest): CreatePivotTableRequest dto in request body. (required)

            

        Returns: PivotTableResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder', 'sourceData', 'destCellName', 'tableName', 'useSameSource', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorksheetPivotTable" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/pivottables/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;sourceData={sourceData}&amp;destCellName={destCellName}&amp;tableName={tableName}&amp;useSameSource={useSameSource}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sourceData' in allParams and allParams['sourceData'] is not None:
            resourcePath = resourcePath.replace("{" + "sourceData" + "}" , str(allParams['sourceData']))
        else:
            resourcePath = re.sub("[&?]sourceData.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'destCellName' in allParams and allParams['destCellName'] is not None:
            resourcePath = resourcePath.replace("{" + "destCellName" + "}" , str(allParams['destCellName']))
        else:
            resourcePath = re.sub("[&?]destCellName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'tableName' in allParams and allParams['tableName'] is not None:
            resourcePath = resourcePath.replace("{" + "tableName" + "}" , str(allParams['tableName']))
        else:
            resourcePath = re.sub("[&?]tableName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'useSameSource' in allParams and allParams['useSameSource'] is not None:
            resourcePath = resourcePath.replace("{" + "useSameSource" + "}" , str(allParams['useSameSource']))
        else:
            resourcePath = re.sub("[&?]useSameSource.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'PivotTableResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteDocumentProperties(self, name, **kwargs):
        """Delete all custom document properties and clean built-in ones.
        Args:
            name (str): The document name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: CellsDocumentPropertiesResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteDocumentProperties" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/documentproperties/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CellsDocumentPropertiesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteDocumentProperty(self, name, propertyName, **kwargs):
        """Delete document property.
        Args:
            name (str): The document name. (required)

            propertyName (str): The property name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: CellsDocumentPropertiesResponse
        """

        allParams = dict.fromkeys(['name', 'propertyName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteDocumentProperty" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/documentproperties/{propertyName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'propertyName' in allParams and allParams['propertyName'] is not None:
            resourcePath = resourcePath.replace("{" + "propertyName" + "}" , str(allParams['propertyName']))
        else:
            resourcePath = re.sub("[&?]propertyName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CellsDocumentPropertiesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetDocumentProperties(self, name, **kwargs):
        """Read document properties.
        Args:
            name (str): The document name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: CellsDocumentPropertiesResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetDocumentProperties" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/documentproperties/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CellsDocumentPropertiesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetDocumentProperty(self, name, propertyName, **kwargs):
        """Read document property by name.
        Args:
            name (str): The document name. (required)

            propertyName (str): The property name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: CellsDocumentPropertyResponse
        """

        allParams = dict.fromkeys(['name', 'propertyName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetDocumentProperty" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/documentproperties/{propertyName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'propertyName' in allParams and allParams['propertyName'] is not None:
            resourcePath = resourcePath.replace("{" + "propertyName" + "}" , str(allParams['propertyName']))
        else:
            resourcePath = re.sub("[&?]propertyName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CellsDocumentPropertyResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutDocumentProperty(self, name, propertyName, body, **kwargs):
        """Set/create document property.
        Args:
            name (str): The document name. (required)

            propertyName (str): The property name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (CellsDocumentProperty): with new property value. (required)

            

        Returns: CellsDocumentPropertyResponse
        """

        allParams = dict.fromkeys(['name', 'propertyName', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutDocumentProperty" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/documentproperties/{propertyName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'propertyName' in allParams and allParams['propertyName'] is not None:
            resourcePath = resourcePath.replace("{" + "propertyName" + "}" , str(allParams['propertyName']))
        else:
            resourcePath = re.sub("[&?]propertyName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CellsDocumentPropertyResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostDocumentSaveAs(self, name, body, **kwargs):
        """Convert document and save result to storage.
        Args:
            name (str): The document name. (required)

            newfilename (str): The new file name. (optional)

            isAutoFitRows (bool): Autofit rows. (optional)

            isAutoFitColumns (bool): Autofit columns. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (SaveOptions): Save options. (required)

            

        Returns: SaveResponse
        """

        allParams = dict.fromkeys(['name', 'newfilename', 'isAutoFitRows', 'isAutoFitColumns', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostDocumentSaveAs" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/SaveAs/?appSid={appSid}&amp;newfilename={newfilename}&amp;isAutoFitRows={isAutoFitRows}&amp;isAutoFitColumns={isAutoFitColumns}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newfilename' in allParams and allParams['newfilename'] is not None:
            resourcePath = resourcePath.replace("{" + "newfilename" + "}" , str(allParams['newfilename']))
        else:
            resourcePath = re.sub("[&?]newfilename.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isAutoFitRows' in allParams and allParams['isAutoFitRows'] is not None:
            resourcePath = resourcePath.replace("{" + "isAutoFitRows" + "}" , str(allParams['isAutoFitRows']))
        else:
            resourcePath = re.sub("[&?]isAutoFitRows.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isAutoFitColumns' in allParams and allParams['isAutoFitColumns'] is not None:
            resourcePath = resourcePath.replace("{" + "isAutoFitColumns" + "}" , str(allParams['isAutoFitColumns']))
        else:
            resourcePath = re.sub("[&?]isAutoFitColumns.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaveResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteDecryptDocument(self, name, body, **kwargs):
        """Decrypt document.
        Args:
            name (str): The document name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (WorkbookEncryptionRequest): Encryption settings, only password can be specified. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteDecryptDocument" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/encryption/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteDocumentUnProtectFromChanges(self, name, **kwargs):
        """Unprotect document from changes.
        Args:
            name (str): The document name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteDocumentUnProtectFromChanges" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/writeProtection/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteUnProtectDocument(self, name, body, **kwargs):
        """Unprotect document.
        Args:
            name (str): The document name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (WorkbookProtectionRequest): Protection settings, only password can be specified. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteUnProtectDocument" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/protection/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkBook(self, name, **kwargs):
        """Read workbook info or export.
        Args:
            name (str): The document name. (required)

            password (str): The document password. (optional)

            isAutoFit (bool): Set document rows to be autofit. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: WorkbookResponse
        """

        allParams = dict.fromkeys(['name', 'password', 'isAutoFit', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkBook" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/?appSid={appSid}&amp;password={password}&amp;isAutoFit={isAutoFit}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isAutoFit' in allParams and allParams['isAutoFit'] is not None:
            resourcePath = resourcePath.replace("{" + "isAutoFit" + "}" , str(allParams['isAutoFit']))
        else:
            resourcePath = re.sub("[&?]isAutoFit.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorkbookResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkBookDefaultStyle(self, name, **kwargs):
        """Read workbook default style info.
        Args:
            name (str): The workbook name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document's folder. (optional)

            

        Returns: StyleResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkBookDefaultStyle" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/defaultstyle/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'StyleResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkBookName(self, name, nameName, **kwargs):
        """Read workbook's name.
        Args:
            name (str): The workbook name. (required)

            nameName (str): The name. (required)

            storage (str): The document storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: NameResponse
        """

        allParams = dict.fromkeys(['name', 'nameName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkBookName" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/names/{nameName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'nameName' in allParams and allParams['nameName'] is not None:
            resourcePath = resourcePath.replace("{" + "nameName" + "}" , str(allParams['nameName']))
        else:
            resourcePath = re.sub("[&?]nameName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'NameResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkBookNames(self, name, **kwargs):
        """Read workbook's names.
        Args:
            name (str): The workbook name. (required)

            storage (str): The document storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: NamesResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkBookNames" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/names/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'NamesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkBookTextItems(self, name, **kwargs):
        """Read workbook's text items.
        Args:
            name (str): The workbook name. (required)

            storage (str): The document storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: TextItemsResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkBookTextItems" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/textItems/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'TextItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkBookWithFormat(self, name, format, **kwargs):
        """EExport workbook to some format.
        Args:
            name (str): The document name. (required)

            format (str): The conversion format. (required)

            password (str): The document password. (optional)

            isAutoFit (bool): Set document rows to be autofit. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            outPath (str): Path to save result (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'format', 'password', 'isAutoFit', 'storage', 'folder', 'outPath'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkBookWithFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/?appSid={appSid}&amp;toFormat={toFormat}&amp;password={password}&amp;isAutoFit={isAutoFit}&amp;storage={storage}&amp;folder={folder}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isAutoFit' in allParams and allParams['isAutoFit'] is not None:
            resourcePath = resourcePath.replace("{" + "isAutoFit" + "}" , str(allParams['isAutoFit']))
        else:
            resourcePath = re.sub("[&?]isAutoFit.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostAutofitWorkbookRows(self, name, body, **kwargs):
        """Autofit workbook rows.
        Args:
            name (str): Document name. (required)

            startRow (int): Start row. (optional)

            endRow (int): End row. (optional)

            onlyAuto (bool): Only auto. (optional)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            body (AutoFitterOptions): Auto Fitter Options. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'startRow', 'endRow', 'onlyAuto', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostAutofitWorkbookRows" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/autofitrows/?appSid={appSid}&amp;startRow={startRow}&amp;endRow={endRow}&amp;onlyAuto={onlyAuto}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startRow' in allParams and allParams['startRow'] is not None:
            resourcePath = resourcePath.replace("{" + "startRow" + "}" , str(allParams['startRow']))
        else:
            resourcePath = re.sub("[&?]startRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'endRow' in allParams and allParams['endRow'] is not None:
            resourcePath = resourcePath.replace("{" + "endRow" + "}" , str(allParams['endRow']))
        else:
            resourcePath = re.sub("[&?]endRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'onlyAuto' in allParams and allParams['onlyAuto'] is not None:
            resourcePath = resourcePath.replace("{" + "onlyAuto" + "}" , str(allParams['onlyAuto']))
        else:
            resourcePath = re.sub("[&?]onlyAuto.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostEncryptDocument(self, name, body, **kwargs):
        """Encript document.
        Args:
            name (str): The document name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (WorkbookEncryptionRequest): Encryption parameters. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostEncryptDocument" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/encryption/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostImportData(self, name, body, **kwargs):
        """Import data to workbook.
        Args:
            name (str): The workbook name. (required)

            storage (str): The workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            body (ImportOption): The import option. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostImportData" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/importdata/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostProtectDocument(self, name, body, **kwargs):
        """Protect document.
        Args:
            name (str): The document name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (WorkbookProtectionRequest): The protection settings. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostProtectDocument" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/protection/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkbookCalculateFormula(self, name, **kwargs):
        """Calculate all formulas in workbook.
        Args:
            name (str): Document name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkbookCalculateFormula" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/calculateformula/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkbookGetSmartMarkerResult(self, name, file, **kwargs):
        """Smart marker processing result.
        Args:
            name (str): The workbook name. (required)

            xmlFile (str): The xml file full path, if empty the data is read from request body. (optional)

            storage (str): The document storage. (optional)

            folder (str): The workbook folder full path. (optional)

            outPath (str): Path to save result (optional)

            file (File):  (required)

            

        Returns: SmartMarkerResultResponse
        """

        allParams = dict.fromkeys(['name', 'xmlFile', 'storage', 'folder', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkbookGetSmartMarkerResult" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/smartmarker/?appSid={appSid}&amp;xmlFile={xmlFile}&amp;storage={storage}&amp;folder={folder}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'xmlFile' in allParams and allParams['xmlFile'] is not None:
            resourcePath = resourcePath.replace("{" + "xmlFile" + "}" , str(allParams['xmlFile']))
        else:
            resourcePath = re.sub("[&?]xmlFile.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/json,application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SmartMarkerResultResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkbooksMerge(self, name, mergeWith, **kwargs):
        """Merge workbooks.
        Args:
            name (str): Workbook name. (required)

            mergeWith (str): The workbook to merge with. (required)

            storage (str): The document storage. (optional)

            folder (str): Source workbook folder. (optional)

            

        Returns: WorkbookResponse
        """

        allParams = dict.fromkeys(['name', 'mergeWith', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkbooksMerge" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/merge/?mergeWith={mergeWith}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'mergeWith' in allParams and allParams['mergeWith'] is not None:
            resourcePath = resourcePath.replace("{" + "mergeWith" + "}" , str(allParams['mergeWith']))
        else:
            resourcePath = re.sub("[&?]mergeWith.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorkbookResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkbookSplit(self, name, **kwargs):
        """Split workbook.
        Args:
            name (str): The workbook name. (required)

            format (str): Split format. (optional)

            ffrom (int): Start worksheet index. (optional)

            to (int): End worksheet index. (optional)

            horizontalResolution (int): Image horizontal resolution. (optional)

            verticalResolution (int): Image vertical resolution. (optional)

            storage (str): The workbook storage. (optional)

            folder (str): The workbook folder. (optional)

            

        Returns: SplitResultResponse
        """

        allParams = dict.fromkeys(['name', 'format', 'ffrom', 'to', 'horizontalResolution', 'verticalResolution', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkbookSplit" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/split/?appSid={appSid}&amp;toFormat={toFormat}&amp;from={from}&amp;to={to}&amp;horizontalResolution={horizontalResolution}&amp;verticalResolution={verticalResolution}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'ffrom' in allParams and allParams['ffrom'] is not None:
            resourcePath = resourcePath.replace("{" + "from" + "}" , str(allParams['ffrom']))
        else:
            resourcePath = re.sub("[&?]from.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'to' in allParams and allParams['to'] is not None:
            resourcePath = resourcePath.replace("{" + "to" + "}" , str(allParams['to']))
        else:
            resourcePath = re.sub("[&?]to.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'horizontalResolution' in allParams and allParams['horizontalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "horizontalResolution" + "}" , str(allParams['horizontalResolution']))
        else:
            resourcePath = re.sub("[&?]horizontalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'verticalResolution' in allParams and allParams['verticalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "verticalResolution" + "}" , str(allParams['verticalResolution']))
        else:
            resourcePath = re.sub("[&?]verticalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SplitResultResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkbooksTextReplace(self, name, oldValue, newValue, **kwargs):
        """Replace text.
        Args:
            name (str): Document name. (required)

            oldValue (str): The old value. (required)

            newValue (str): The new value. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: WorkbookReplaceResponse
        """

        allParams = dict.fromkeys(['name', 'oldValue', 'newValue', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkbooksTextReplace" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/replaceText/?oldValue={oldValue}&amp;newValue={newValue}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'oldValue' in allParams and allParams['oldValue'] is not None:
            resourcePath = resourcePath.replace("{" + "oldValue" + "}" , str(allParams['oldValue']))
        else:
            resourcePath = re.sub("[&?]oldValue.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newValue' in allParams and allParams['newValue'] is not None:
            resourcePath = resourcePath.replace("{" + "newValue" + "}" , str(allParams['newValue']))
        else:
            resourcePath = re.sub("[&?]newValue.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorkbookReplaceResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkbooksTextSearch(self, name, text, **kwargs):
        """Search text.
        Args:
            name (str): Document name. (required)

            text (str): Text sample. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: TextItemsResponse
        """

        allParams = dict.fromkeys(['name', 'text', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkbooksTextSearch" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/findText/?text={text}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'text' in allParams and allParams['text'] is not None:
            resourcePath = resourcePath.replace("{" + "text" + "}" , str(allParams['text']))
        else:
            resourcePath = re.sub("[&?]text.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'TextItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutConvertWorkBook(self, file, data, **kwargs):
        """Convert workbook from request content to some format.
        Args:
            format (str): The format to convert. (optional)

            password (str): The workbook password. (optional)

            outPath (str): Path to save result (optional)

            file (File):  (required)
            
            data (File):  (required)
                        

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['format', 'password', 'outPath', 'file', 'data'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutConvertWorkBook" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/convert/?appSid={appSid}&amp;toFormat={toFormat}&amp;password={password}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = [
                ('file', (os.path.basename(file), open(file, 'rb'), 'application/octet-stream')),
                ('data', (os.path.basename(data), open(data, 'rb'), 'application/xml'))
            ]
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = None

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutDocumentProtectFromChanges(self, name, body, **kwargs):
        """Protect document from changes.
        Args:
            name (str): Document name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            body (PasswordRequest): Modification password. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutDocumentProtectFromChanges" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/writeProtection/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorkbookCreate(self, name, file, **kwargs):
        """Create new workbook using deferent methods.
        Args:
            name (str): The new document name. (required)

            templateFile (str): The template file, if the data not provided default workbook is created. (optional)

            dataFile (str): Smart marker data file, if the data not provided the request content is checked for the data. (optional)

            storage (str): The document storage. (optional)

            folder (str): The new document folder. (optional)

            file (File):  (required)

            

        Returns: WorkbookResponse
        """

        allParams = dict.fromkeys(['name', 'templateFile', 'dataFile', 'storage', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorkbookCreate" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/?appSid={appSid}&amp;templateFile={templateFile}&amp;dataFile={dataFile}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'templateFile' in allParams and allParams['templateFile'] is not None:
            resourcePath = resourcePath.replace("{" + "templateFile" + "}" , str(allParams['templateFile']))
        else:
            resourcePath = re.sub("[&?]templateFile.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'dataFile' in allParams and allParams['dataFile'] is not None:
            resourcePath = resourcePath.replace("{" + "dataFile" + "}" , str(allParams['dataFile']))
        else:
            resourcePath = re.sub("[&?]dataFile.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = {}
        
        if(file is not None):
            files = { 'file':open(file, 'rb')}
            
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorkbookResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteUnprotectWorksheet(self, name, sheetName, body, **kwargs):
        """Unprotect worksheet.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document folder. (optional)

            body (ProtectSheetParameter): with protection settings. Only password is used here. (required)

            

        Returns: WorksheetResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteUnprotectWorksheet" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/protection/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorksheetResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheet(self, name, sheetName, **kwargs):
        """Delete worksheet.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: WorksheetsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheet" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorksheetsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorkSheetBackground(self, name, sheetName, **kwargs):
        """Set worksheet background image.
        Args:
            name (str):  (required)

            sheetName (str):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorkSheetBackground" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/background/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorkSheetComment(self, name, sheetName, cellName, **kwargs):
        """Delete worksheet's cell comment.
        Args:
            name (str): The document name. (required)

            sheetName (str): The worksheet name. (required)

            cellName (str): The cell name (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorkSheetComment" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/comments/{cellName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellName' in allParams and allParams['cellName'] is not None:
            resourcePath = resourcePath.replace("{" + "cellName" + "}" , str(allParams['cellName']))
        else:
            resourcePath = re.sub("[&?]cellName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorksheetFreezePanes(self, name, sheetName, row, column, freezedRows, freezedColumns, **kwargs):
        """Unfreeze panes
        Args:
            name (str):  (required)

            sheetName (str):  (required)

            row (int):  (required)

            column (int):  (required)

            freezedRows (int):  (required)

            freezedColumns (int):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'row', 'column', 'freezedRows', 'freezedColumns', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorksheetFreezePanes" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/freezepanes/?appSid={appSid}&amp;row={row}&amp;column={column}&amp;freezedRows={freezedRows}&amp;freezedColumns={freezedColumns}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'row' in allParams and allParams['row'] is not None:
            resourcePath = resourcePath.replace("{" + "row" + "}" , str(allParams['row']))
        else:
            resourcePath = re.sub("[&?]row.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'column' in allParams and allParams['column'] is not None:
            resourcePath = resourcePath.replace("{" + "column" + "}" , str(allParams['column']))
        else:
            resourcePath = re.sub("[&?]column.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'freezedRows' in allParams and allParams['freezedRows'] is not None:
            resourcePath = resourcePath.replace("{" + "freezedRows" + "}" , str(allParams['freezedRows']))
        else:
            resourcePath = re.sub("[&?]freezedRows.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'freezedColumns' in allParams and allParams['freezedColumns'] is not None:
            resourcePath = resourcePath.replace("{" + "freezedColumns" + "}" , str(allParams['freezedColumns']))
        else:
            resourcePath = re.sub("[&?]freezedColumns.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheet(self, name, sheetName, **kwargs):
        """Read worksheet info or export.
        Args:
            name (str): The document name. (required)

            sheetName (str): The worksheet name. (required)

            verticalResolution (int): Image vertical resolution. (optional)

            horizontalResolution (int): Image horizontal resolution. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'verticalResolution', 'horizontalResolution', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheet" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/?appSid={appSid}&amp;verticalResolution={verticalResolution}&amp;horizontalResolution={horizontalResolution}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'verticalResolution' in allParams and allParams['verticalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "verticalResolution" + "}" , str(allParams['verticalResolution']))
        else:
            resourcePath = re.sub("[&?]verticalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'horizontalResolution' in allParams and allParams['horizontalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "horizontalResolution" + "}" , str(allParams['horizontalResolution']))
        else:
            resourcePath = re.sub("[&?]horizontalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetCalculateFormula(self, name, sheetName, formula, **kwargs):
        """Calculate formula value.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            formula (str): The formula. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: SingleValueResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'formula', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetCalculateFormula" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/formulaResult/?formula={formula}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'formula' in allParams and allParams['formula'] is not None:
            resourcePath = resourcePath.replace("{" + "formula" + "}" , str(allParams['formula']))
        else:
            resourcePath = re.sub("[&?]formula.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SingleValueResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetComment(self, name, sheetName, cellName, **kwargs):
        """Get worksheet comment by cell name.
        Args:
            name (str): The document name. (required)

            sheetName (str): The worksheet name. (required)

            cellName (str): The cell name (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: CommentResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetComment" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/comments/{cellName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellName' in allParams and allParams['cellName'] is not None:
            resourcePath = resourcePath.replace("{" + "cellName" + "}" , str(allParams['cellName']))
        else:
            resourcePath = re.sub("[&?]cellName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CommentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetComments(self, name, sheetName, **kwargs):
        """Get worksheet comments.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: CommentsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetComments" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/comments/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CommentsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetMergedCell(self, name, sheetName, mergedCellIndex, **kwargs):
        """Get worksheet merged cell by its index.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            mergedCellIndex (int): Merged cell index. (required)

            storage (str): The document storage. (optional)

            folder (str): Document folder. (optional)

            

        Returns: MergedCellResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'mergedCellIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetMergedCell" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/mergedCells/{mergedCellIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'mergedCellIndex' in allParams and allParams['mergedCellIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "mergedCellIndex" + "}" , str(allParams['mergedCellIndex']))
        else:
            resourcePath = re.sub("[&?]mergedCellIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'MergedCellResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetMergedCells(self, name, sheetName, **kwargs):
        """Get worksheet merged cells.
        Args:
            name (str): Document name. (required)

            sheetName (str): The workseet name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document folder. (optional)

            

        Returns: MergedCellsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetMergedCells" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/mergedCells/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'MergedCellsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheets(self, name, **kwargs):
        """Read worksheets info.
        Args:
            name (str): Document name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document folder. (optional)

            

        Returns: WorksheetsResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheets" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorksheetsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetTextItems(self, name, sheetName, **kwargs):
        """Get worksheet text items.
        Args:
            name (str): Workbook name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): The workbook's folder. (optional)

            

        Returns: TextItemsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetTextItems" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/textItems/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'TextItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetWithFormat(self, name, sheetName, format, **kwargs):
        """Read worksheet info or export.
        Args:
            name (str): The document name. (required)

            sheetName (str): The worksheet name. (required)

            format (str): Export format. (required)

            verticalResolution (int): Image vertical resolution. (optional)

            horizontalResolution (int): Image horizontal resolution. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'format', 'verticalResolution', 'horizontalResolution', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetWithFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/?appSid={appSid}&amp;toFormat={toFormat}&amp;verticalResolution={verticalResolution}&amp;horizontalResolution={horizontalResolution}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'verticalResolution' in allParams and allParams['verticalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "verticalResolution" + "}" , str(allParams['verticalResolution']))
        else:
            resourcePath = re.sub("[&?]verticalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'horizontalResolution' in allParams and allParams['horizontalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "horizontalResolution" + "}" , str(allParams['horizontalResolution']))
        else:
            resourcePath = re.sub("[&?]horizontalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostAutofitWorksheetRows(self, name, sheetName, body, **kwargs):
        """Autofit worksheet rows.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            startRow (int): Start row. (optional)

            endRow (int): End row. (optional)

            onlyAuto (bool): Only auto. (optional)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            body (AutoFitterOptions): Auto Fitter Options. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'startRow', 'endRow', 'onlyAuto', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostAutofitWorksheetRows" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/autofitrows/?appSid={appSid}&amp;startRow={startRow}&amp;endRow={endRow}&amp;onlyAuto={onlyAuto}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'startRow' in allParams and allParams['startRow'] is not None:
            resourcePath = resourcePath.replace("{" + "startRow" + "}" , str(allParams['startRow']))
        else:
            resourcePath = re.sub("[&?]startRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'endRow' in allParams and allParams['endRow'] is not None:
            resourcePath = resourcePath.replace("{" + "endRow" + "}" , str(allParams['endRow']))
        else:
            resourcePath = re.sub("[&?]endRow.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'onlyAuto' in allParams and allParams['onlyAuto'] is not None:
            resourcePath = resourcePath.replace("{" + "onlyAuto" + "}" , str(allParams['onlyAuto']))
        else:
            resourcePath = re.sub("[&?]onlyAuto.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostCopyWorksheet(self, name, sheetName, sourceSheet, **kwargs):
        """Copy worksheet
        Args:
            name (str):  (required)

            sheetName (str):  (required)

            sourceSheet (str):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'sourceSheet', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostCopyWorksheet" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/copy/?sourceSheet={sourceSheet}&amp;appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sourceSheet' in allParams and allParams['sourceSheet'] is not None:
            resourcePath = resourcePath.replace("{" + "sourceSheet" + "}" , str(allParams['sourceSheet']))
        else:
            resourcePath = re.sub("[&?]sourceSheet.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostMoveWorksheet(self, name, sheetName, body, **kwargs):
        """Move worksheet.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (WorksheetMovingRequest): with moving parameters. (required)

            

        Returns: WorksheetsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostMoveWorksheet" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/position/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorksheetsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostRenameWorksheet(self, name, sheetName, newname, **kwargs):
        """Rename worksheet
        Args:
            name (str):  (required)

            sheetName (str):  (required)

            newname (str):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'newname', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostRenameWorksheet" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/rename/?newname={newname}&amp;appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newname' in allParams and allParams['newname'] is not None:
            resourcePath = resourcePath.replace("{" + "newname" + "}" , str(allParams['newname']))
        else:
            resourcePath = re.sub("[&?]newname.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostUpdateWorksheetProperty(self, name, sheetName, body, **kwargs):
        """Update worksheet property
        Args:
            name (str):  (required)

            sheetName (str):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            body (Worksheet):  (required)

            

        Returns: WorksheetResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'folder', 'storage', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostUpdateWorksheetProperty" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorksheetResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkSheetComment(self, name, sheetName, cellName, body, **kwargs):
        """Update worksheet's cell comment.
        Args:
            name (str): The document name. (required)

            sheetName (str): The worksheet name. (required)

            cellName (str): The cell name (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (Comment): Comment object (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellName', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkSheetComment" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/comments/{cellName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellName' in allParams and allParams['cellName'] is not None:
            resourcePath = resourcePath.replace("{" + "cellName" + "}" , str(allParams['cellName']))
        else:
            resourcePath = re.sub("[&?]cellName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorksheetRangeSort(self, name, sheetName, cellArea, body, **kwargs):
        """Sort worksheet range.
        Args:
            name (str): The workbook name. (required)

            sheetName (str): The worksheet name. (required)

            cellArea (str): The range to sort. (required)

            storage (str): The document storage. (optional)

            folder (str): The workbook folder. (optional)

            body (DataSorter): with sorting settings. (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellArea', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorksheetRangeSort" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/sort/?cellArea={cellArea}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellArea' in allParams and allParams['cellArea'] is not None:
            resourcePath = resourcePath.replace("{" + "cellArea" + "}" , str(allParams['cellArea']))
        else:
            resourcePath = re.sub("[&?]cellArea.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkSheetTextSearch(self, name, sheetName, text, **kwargs):
        """Search text.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            text (str): Text to search. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: TextItemsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'text', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkSheetTextSearch" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/findText/?text={text}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'text' in allParams and allParams['text'] is not None:
            resourcePath = resourcePath.replace("{" + "text" + "}" , str(allParams['text']))
        else:
            resourcePath = re.sub("[&?]text.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'TextItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorsheetTextReplace(self, name, sheetName, oldValue, newValue, **kwargs):
        """Replace text.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            oldValue (str): The old text to replace. (required)

            newValue (str): The new text to replace by. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: WorksheetReplaceResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'oldValue', 'newValue', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorsheetTextReplace" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/replaceText/?oldValue={oldValue}&amp;newValue={newValue}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'oldValue' in allParams and allParams['oldValue'] is not None:
            resourcePath = resourcePath.replace("{" + "oldValue" + "}" , str(allParams['oldValue']))
        else:
            resourcePath = re.sub("[&?]oldValue.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newValue' in allParams and allParams['newValue'] is not None:
            resourcePath = resourcePath.replace("{" + "newValue" + "}" , str(allParams['newValue']))
        else:
            resourcePath = re.sub("[&?]newValue.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorksheetReplaceResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutAddNewWorksheet(self, name, sheetName, **kwargs):
        """Add new worksheet.
        Args:
            name (str): Document name. (required)

            sheetName (str): The new sheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document folder. (optional)

            

        Returns: WorksheetsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutAddNewWorksheet" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorksheetsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutChangeVisibilityWorksheet(self, name, sheetName, isVisible, **kwargs):
        """Change worksheet visibility.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            isVisible (bool): New worksheet visibility value. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: WorksheetResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'isVisible', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutChangeVisibilityWorksheet" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/visible/?isVisible={isVisible}&amp;appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isVisible' in allParams and allParams['isVisible'] is not None:
            resourcePath = resourcePath.replace("{" + "isVisible" + "}" , str(allParams['isVisible']))
        else:
            resourcePath = re.sub("[&?]isVisible.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorksheetResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutProtectWorksheet(self, name, sheetName, body, **kwargs):
        """Protect worksheet.
        Args:
            name (str): Document name. (required)

            sheetName (str): The worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document folder. (optional)

            body (ProtectSheetParameter): with protection settings. (required)

            

        Returns: WorksheetResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutProtectWorksheet" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/protection/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WorksheetResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorkSheetBackground(self, name, sheetName, file, **kwargs):
        """Set worksheet background image.
        Args:
            name (str):  (required)

            sheetName (str):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            file (File):  (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'folder', 'storage', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorkSheetBackground" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/background/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorkSheetComment(self, name, sheetName, cellName, body, **kwargs):
        """Add worksheet's cell comment.
        Args:
            name (str): The document name. (required)

            sheetName (str): The worksheet name. (required)

            cellName (str): The cell name (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (Comment): Comment object (required)

            

        Returns: CommentResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'cellName', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorkSheetComment" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/comments/{cellName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'cellName' in allParams and allParams['cellName'] is not None:
            resourcePath = resourcePath.replace("{" + "cellName" + "}" , str(allParams['cellName']))
        else:
            resourcePath = re.sub("[&?]cellName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CommentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorksheetFreezePanes(self, name, sheetName, row, column, freezedRows, freezedColumns, **kwargs):
        """Set freeze panes
        Args:
            name (str):  (required)

            sheetName (str):  (required)

            row (int):  (required)

            column (int):  (required)

            freezedRows (int):  (required)

            freezedColumns (int):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'row', 'column', 'freezedRows', 'freezedColumns', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorksheetFreezePanes" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/freezepanes/?appSid={appSid}&amp;row={row}&amp;column={column}&amp;freezedRows={freezedRows}&amp;freezedColumns={freezedColumns}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'row' in allParams and allParams['row'] is not None:
            resourcePath = resourcePath.replace("{" + "row" + "}" , str(allParams['row']))
        else:
            resourcePath = re.sub("[&?]row.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'column' in allParams and allParams['column'] is not None:
            resourcePath = resourcePath.replace("{" + "column" + "}" , str(allParams['column']))
        else:
            resourcePath = re.sub("[&?]column.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'freezedRows' in allParams and allParams['freezedRows'] is not None:
            resourcePath = resourcePath.replace("{" + "freezedRows" + "}" , str(allParams['freezedRows']))
        else:
            resourcePath = re.sub("[&?]freezedRows.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'freezedColumns' in allParams and allParams['freezedColumns'] is not None:
            resourcePath = resourcePath.replace("{" + "freezedColumns" + "}" , str(allParams['freezedColumns']))
        else:
            resourcePath = re.sub("[&?]freezedColumns.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteWorkSheetValidation(self, name, sheetName, validationIndex, **kwargs):
        """Delete worksheet validation by index.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            validationIndex (int): The validation index. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: ValidationResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'validationIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteWorkSheetValidation" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/validations/{validationIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'validationIndex' in allParams and allParams['validationIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "validationIndex" + "}" , str(allParams['validationIndex']))
        else:
            resourcePath = re.sub("[&?]validationIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ValidationResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetValidation(self, name, sheetName, validationIndex, **kwargs):
        """Get worksheet validation by index.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            validationIndex (int): The validation index. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: ValidationResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'validationIndex', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetValidation" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/validations/{validationIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'validationIndex' in allParams and allParams['validationIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "validationIndex" + "}" , str(allParams['validationIndex']))
        else:
            resourcePath = re.sub("[&?]validationIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ValidationResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetWorkSheetValidations(self, name, sheetName, **kwargs):
        """Get worksheet validations.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            storage (str): The document storage. (optional)

            folder (str): Document folder. (optional)

            

        Returns: ValidationsResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetWorkSheetValidations" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/validations/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ValidationsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostWorkSheetValidation(self, name, sheetName, validationIndex, file, **kwargs):
        """Update worksheet validation by index.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            validationIndex (int): The validation index. (required)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            file (File):  (required)

            

        Returns: ValidationResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'validationIndex', 'storage', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostWorkSheetValidation" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/validations/{validationIndex}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'validationIndex' in allParams and allParams['validationIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "validationIndex" + "}" , str(allParams['validationIndex']))
        else:
            resourcePath = re.sub("[&?]validationIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ValidationResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutWorkSheetValidation(self, name, sheetName, file, **kwargs):
        """Add worksheet validation at index.
        Args:
            name (str): Document name. (required)

            sheetName (str): Worksheet name. (required)

            range (str): Specified cells area (optional)

            storage (str): The document storage. (optional)

            folder (str): Document's folder. (optional)

            file (File):  (required)

            

        Returns: ValidationResponse
        """

        allParams = dict.fromkeys(['name', 'sheetName', 'range', 'storage', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutWorkSheetValidation" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/cells/{name}/worksheets/{sheetName}/validations/?appSid={appSid}&amp;range={range}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'sheetName' in allParams and allParams['sheetName'] is not None:
            resourcePath = resourcePath.replace("{" + "sheetName" + "}" , str(allParams['sheetName']))
        else:
            resourcePath = re.sub("[&?]sheetName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'range' in allParams and allParams['range'] is not None:
            resourcePath = resourcePath.replace("{" + "range" + "}" , str(allParams['range']))
        else:
            resourcePath = re.sub("[&?]range.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ValidationResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    




