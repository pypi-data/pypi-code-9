#!/usr/bin/env python

import sys
import os
import urllib
import json
import re
from models import *
from ApiClient import ApiException


class SlidesApi(object):

    def __init__(self, apiClient):
      self.apiClient = apiClient

    

    def GetSlidesDocument(self, name, **kwargs):
        """Read presentation info.
        Args:
            name (str): The document name. (required)

            password (str): The document password. (optional)

            storage (str): Document's storage. (optional)

            folder (str): Document's folder. (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'password', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesDocument" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/?appSid={appSid}&amp;password={password}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

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

        

        

    def GetSlidesDocumentWithFormat(self, name, format, **kwargs):
        """Export presentation to some format.
        Args:
            name (str): The document name. (required)

            format (str): The conversion format. (required)

            jpegQuality (int): Quality of the JPEG images inside PDF document. (optional)

            password (str): The document password. (optional)

            storage (str): Document's storage. (optional)

            folder (str): Document's folder. (optional)

            outPath (str): Path to save result (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'format', 'jpegQuality', 'password', 'storage', 'folder', 'outPath'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesDocumentWithFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/?appSid={appSid}&amp;toFormat={toFormat}&amp;jpegQuality={jpegQuality}&amp;password={password}&amp;storage={storage}&amp;folder={folder}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'jpegQuality' in allParams and allParams['jpegQuality'] is not None:
            resourcePath = resourcePath.replace("{" + "jpegQuality" + "}" , str(allParams['jpegQuality']))
        else:
            resourcePath = re.sub("[&?]jpegQuality.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

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

        

        

    def PostSlidesDocument(self, name, templatePath, file, **kwargs):
        """Create presentation
        Args:
            name (str): The document name. (required)

            templatePath (str): Template file path. (required)

            templateStorage (str): Template storage name. (optional)

            isImageDataEmbeeded (bool): Is Image Data Embeeded (optional)

            password (str): The document password. (optional)

            storage (str): Document's storage. (optional)

            folder (str): Document's folder. (optional)

            file (File):  (required)

            

        Returns: DocumentResponse
        """

        allParams = dict.fromkeys(['name', 'templatePath', 'templateStorage', 'isImageDataEmbeeded', 'password', 'storage', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSlidesDocument" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/?appSid={appSid}&amp;templatePath={templatePath}&amp;templateStorage={templateStorage}&amp;isImageDataEmbeeded={isImageDataEmbeeded}&amp;password={password}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'templatePath' in allParams and allParams['templatePath'] is not None:
            resourcePath = resourcePath.replace("{" + "templatePath" + "}" , str(allParams['templatePath']))
        else:
            resourcePath = re.sub("[&?]templatePath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'templateStorage' in allParams and allParams['templateStorage'] is not None:
            resourcePath = resourcePath.replace("{" + "templateStorage" + "}" , str(allParams['templateStorage']))
        else:
            resourcePath = re.sub("[&?]templateStorage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isImageDataEmbeeded' in allParams and allParams['isImageDataEmbeeded'] is not None:
            resourcePath = resourcePath.replace("{" + "isImageDataEmbeeded" + "}" , str(allParams['isImageDataEmbeeded']))
        else:
            resourcePath = re.sub("[&?]isImageDataEmbeeded.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

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
        files = {}
        
        if file is not None:
            files = { 'file':open(file, 'rb')}
            
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostSlidesSplit(self, name, **kwargs):
        """Splitting presentations. Create one image per slide.
        Args:
            name (str): The document name. (required)

            width (int): The width of created images. (optional)

            height (int): The height of created images. (optional)

            to (int): The last slide number for splitting, if is not specified splitting ends at the last slide of the document. (optional)

            ffrom (int): The start slide number for splitting, if is not specified splitting starts from the first slide of the presentation. (optional)

            destFolder (str): Folder on storage where images are going to be uploaded. If not specified then images are uploaded to same folder as presentation. (optional)

            format (str): The format. Default value is jpeg. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SplitDocumentResponse
        """

        allParams = dict.fromkeys(['name', 'width', 'height', 'to', 'ffrom', 'destFolder', 'format', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSlidesSplit" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/split/?appSid={appSid}&amp;width={width}&amp;height={height}&amp;to={to}&amp;from={from}&amp;destFolder={destFolder}&amp;toFormat={toFormat}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'width' in allParams and allParams['width'] is not None:
            resourcePath = resourcePath.replace("{" + "width" + "}" , str(allParams['width']))
        else:
            resourcePath = re.sub("[&?]width.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'height' in allParams and allParams['height'] is not None:
            resourcePath = resourcePath.replace("{" + "height" + "}" , str(allParams['height']))
        else:
            resourcePath = re.sub("[&?]height.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'to' in allParams and allParams['to'] is not None:
            resourcePath = resourcePath.replace("{" + "to" + "}" , str(allParams['to']))
        else:
            resourcePath = re.sub("[&?]to.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'ffrom' in allParams and allParams['ffrom'] is not None:
            resourcePath = resourcePath.replace("{" + "from" + "}" , str(allParams['ffrom']))
        else:
            resourcePath = re.sub("[&?]from.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'destFolder' in allParams and allParams['destFolder'] is not None:
            resourcePath = resourcePath.replace("{" + "destFolder" + "}" , str(allParams['destFolder']))
        else:
            resourcePath = re.sub("[&?]destFolder.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SplitDocumentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutNewPresentation(self, name, file, **kwargs):
        """Create presentation
        Args:
            name (str): The document name. (required)

            password (str): The document password. (optional)

            storage (str): Document's storage. (optional)

            folder (str): Document's folder. (optional)

            file (File):  (required)

            

        Returns: DocumentResponse
        """

        allParams = dict.fromkeys(['name', 'password', 'storage', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutNewPresentation" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/?appSid={appSid}&amp;password={password}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutNewPresentationFromStoredTemplate(self, name, templatePath, file, **kwargs):
        """Create presentation from stored template
        Args:
            name (str): The document name. (required)

            templatePath (str): Template file path. (required)

            templateStorage (str): Template storage name. (optional)

            password (str): The document password. (optional)

            storage (str): Document's storage. (optional)

            folder (str): Document's folder. (optional)

            file (File):  (required)

            

        Returns: DocumentResponse
        """

        allParams = dict.fromkeys(['name', 'templatePath', 'templateStorage', 'password', 'storage', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutNewPresentationFromStoredTemplate" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/?appSid={appSid}&amp;templatePath={templatePath}&amp;templateStorage={templateStorage}&amp;password={password}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'templatePath' in allParams and allParams['templatePath'] is not None:
            resourcePath = resourcePath.replace("{" + "templatePath" + "}" , str(allParams['templatePath']))
        else:
            resourcePath = re.sub("[&?]templatePath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'templateStorage' in allParams and allParams['templateStorage'] is not None:
            resourcePath = resourcePath.replace("{" + "templateStorage" + "}" , str(allParams['templateStorage']))
        else:
            resourcePath = re.sub("[&?]templateStorage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutSlidesConvert(self, file, **kwargs):
        """Convert presentation from request content to format specified.
        Args:
            password (str): The document password. (optional)

            format (str): The format. (optional)

            outPath (str): Path to save result (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['password', 'format', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutSlidesConvert" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/convert/?appSid={appSid}&amp;password={password}&amp;toFormat={toFormat}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

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

        

        

    def PutSlidesDocumentFromHtml(self, name, file, **kwargs):
        """Create presentation document from html
        Args:
            name (str): The document name. (required)

            password (str): The document password. (optional)

            storage (str): Document's storage. (optional)

            folder (str): Document's folder. (optional)

            file (File):  (required)

            

        Returns: DocumentResponse
        """

        allParams = dict.fromkeys(['name', 'password', 'storage', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutSlidesDocumentFromHtml" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/fromHtml/?appSid={appSid}&amp;password={password}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesImages(self, name, **kwargs):
        """Read presentation images info.
        Args:
            name (str): The presentation name. (required)

            folder (str): The presentation folder. (optional)

            storage (str): Document's storage. (optional)

            

        Returns: ImagesResponse
        """

        allParams = dict.fromkeys(['name', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesImages" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/images/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ImagesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesSlideImages(self, name, slideIndex, **kwargs):
        """Read slide images info.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): The slide index. (required)

            folder (str): Presentation folder. (optional)

            storage (str): Document's storage. (optional)

            

        Returns: ImagesResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesSlideImages" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/images/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ImagesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostPresentationMerge(self, name, body, **kwargs):
        """Merge presentations.
        Args:
            name (str): Original presentation name. (required)

            storage (str): The storage. (optional)

            folder (str): The folder. (optional)

            body (PresentationsMergeRequest): with a list of presentations to merge. (required)

            

        Returns: DocumentResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostPresentationMerge" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/merge/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutPresentationMerge(self, name, body, **kwargs):
        """Merge presentations.
        Args:
            name (str): Original presentation name. (required)

            storage (str): The storage. (optional)

            folder (str): The folder. (optional)

            body (OrderedMergeRequest): with a list of presentations to merge. (required)

            

        Returns: DocumentResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutPresentationMerge" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/merge/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesPlaceholder(self, name, slideIndex, placeholderIndex, **kwargs):
        """Read slide placeholder info.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide index. (required)

            placeholderIndex (int): Pleceholder index. (required)

            folder (str): Presentation folder. (optional)

            storage (str): Document's storage. (optional)

            

        Returns: PlaceholderResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'placeholderIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesPlaceholder" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/placeholders/{placeholderIndex}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'placeholderIndex' in allParams and allParams['placeholderIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "placeholderIndex" + "}" , str(allParams['placeholderIndex']))
        else:
            resourcePath = re.sub("[&?]placeholderIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'PlaceholderResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesPlaceholders(self, name, slideIndex, **kwargs):
        """Read slide placeholders info.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide index. (required)

            folder (str): Presentation folder. (optional)

            storage (str): Document's storage. (optional)

            

        Returns: PlaceholdersResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesPlaceholders" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/placeholders/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'PlaceholdersResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteSlidesDocumentProperties(self, name, **kwargs):
        """Clean document properties.
        Args:
            name (str): The presentation name. (required)

            folder (str): The presentation folder. (optional)

            storage (str): Document's storage. (optional)

            

        Returns: DocumentPropertiesResponse
        """

        allParams = dict.fromkeys(['name', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteSlidesDocumentProperties" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/documentproperties/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentPropertiesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteSlidesDocumentProperty(self, name, propertyName, **kwargs):
        """Delete document property.
        Args:
            name (str): The presentation name. (required)

            propertyName (str): The property name. (required)

            folder (str): The presentation folder. (optional)

            storage (str): Document's storage. (optional)

            

        Returns: CommonResponse
        """

        allParams = dict.fromkeys(['name', 'propertyName', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteSlidesDocumentProperty" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/documentproperties/{propertyName}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'propertyName' in allParams and allParams['propertyName'] is not None:
            resourcePath = resourcePath.replace("{" + "propertyName" + "}" , str(allParams['propertyName']))
        else:
            resourcePath = re.sub("[&?]propertyName.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'CommonResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesDocumentProperties(self, name, **kwargs):
        """Read presentation document properties.
        Args:
            name (str): The document name. (required)

            folder (str): Document's folder. (optional)

            storage (str): Document's storage. (optional)

            

        Returns: DocumentPropertiesResponse
        """

        allParams = dict.fromkeys(['name', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesDocumentProperties" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/documentproperties/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentPropertiesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        


    def GetSlidesDocumentProperty(self, name, propertyName, **kwargs):
        """
        Args:
            name (str):  (required)

            propertyName (str):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: DocumentPropertyResponse
        """

        allParams = dict.fromkeys(['name', 'propertyName', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesDocumentProperty" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/documentproperties/{propertyName}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'propertyName' in allParams and allParams['propertyName'] is not None:
            resourcePath = resourcePath.replace("{" + "propertyName" + "}" , str(allParams['propertyName']))
        else:
            resourcePath = re.sub("[&?]propertyName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentPropertyResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

    def PostSlidesSetDocumentProperties(self, name, body, **kwargs):
        """Set document properties.
        Args:
            name (str): The document name. (required)

            folder (str): Document's folder. (optional)

            storage (str): Document's storage. (optional)

            body (DocumentProperties): New properties. (required)

            

        Returns: DocumentPropertiesResponse
        """

        allParams = dict.fromkeys(['name', 'folder', 'storage', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSlidesSetDocumentProperties" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/documentproperties/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentPropertiesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutSlidesSetDocumentProperty(self, name, propertyName, body, **kwargs):
        """Set document property.
        Args:
            name (str): The presentation name. (required)

            propertyName (str): The property name. (required)

            folder (str): Document's folder. (optional)

            storage (str): Document's storage. (optional)

            body (DocumentProperty): Property with the value. (required)

            

        Returns: DocumentPropertyResponse
        """

        allParams = dict.fromkeys(['name', 'propertyName', 'folder', 'storage', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutSlidesSetDocumentProperty" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/documentproperties/{propertyName}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'propertyName' in allParams and allParams['propertyName'] is not None:
            resourcePath = resourcePath.replace("{" + "propertyName" + "}" , str(allParams['propertyName']))
        else:
            resourcePath = re.sub("[&?]propertyName.*?(?=&|\\?|$)", "", resourcePath)
        

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
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentPropertyResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetParagraphPortion(self, name, slideIndex, shapeIndex, paragraphIndex, portionIndex, **kwargs):
        """Reads paragraph portion in shape's textBody.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Index of slide starting from 1 (required)

            shapeIndex (int): Index of shape starting from 1 (required)

            paragraphIndex (int): Index of paragraph starting from 1 (required)

            portionIndex (int): Index of portion starting from 1 (required)

            folder (str): Presentation folder. (optional)

            storage (str): Document's storage. (optional)

            

        Returns: PortionResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'shapeIndex', 'paragraphIndex', 'portionIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetParagraphPortion" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/shapes/{shapeIndex}/paragraphs/{paragraphIndex}/portions/{portionIndex}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'shapeIndex' in allParams and allParams['shapeIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "shapeIndex" + "}" , str(allParams['shapeIndex']))
        else:
            resourcePath = re.sub("[&?]shapeIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'paragraphIndex' in allParams and allParams['paragraphIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "paragraphIndex" + "}" , str(allParams['paragraphIndex']))
        else:
            resourcePath = re.sub("[&?]paragraphIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'portionIndex' in allParams and allParams['portionIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "portionIndex" + "}" , str(allParams['portionIndex']))
        else:
            resourcePath = re.sub("[&?]portionIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'PortionResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetShapeParagraph(self, name, slideIndex, shapeIndex, paragraphIndex, **kwargs):
        """Reads paragraph in shape's textBody.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Index of slide starting from 1 (required)

            shapeIndex (int): Index of shape starting from 1 (required)

            paragraphIndex (int): Index of paragraph starting from 1 (required)

            folder (str): Presentation folder. (optional)

            storage (str): Document's storage. (optional)

            

        Returns: ParagraphResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'shapeIndex', 'paragraphIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetShapeParagraph" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/shapes/{shapeIndex}/paragraphs/{paragraphIndex}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'shapeIndex' in allParams and allParams['shapeIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "shapeIndex" + "}" , str(allParams['shapeIndex']))
        else:
            resourcePath = re.sub("[&?]shapeIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'paragraphIndex' in allParams and allParams['paragraphIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "paragraphIndex" + "}" , str(allParams['paragraphIndex']))
        else:
            resourcePath = re.sub("[&?]paragraphIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ParagraphResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlideShapeParagraphs(self, name, slideIndex, shapeIndex, **kwargs):
        """Reads a list of paragraphs in shape's textBody.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Index of slide starting from 1 (required)

            shapeIndex (int): Index of shape starting from 1 (required)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: ParagraphsResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'shapeIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlideShapeParagraphs" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/shapes/{shapeIndex}/paragraphs/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'shapeIndex' in allParams and allParams['shapeIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "shapeIndex" + "}" , str(allParams['shapeIndex']))
        else:
            resourcePath = re.sub("[&?]shapeIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ParagraphsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesSlideShapes(self, name, slideIndex, **kwargs):
        """Read slides shapes info.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide index. (required)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: ShapeListResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesSlideShapes" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/shapes/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ShapeListResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesSlideShapesParent(self, name, slideIndex, shapePath, **kwargs):
        """Read slide shapes or shape info.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide index. (required)

            shapePath (str): Shape path. (required)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: ShapeResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'shapePath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesSlideShapesParent" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/shapes/{shapePath}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'shapePath' in allParams and allParams['shapePath'] is not None:
            resourcePath = resourcePath.replace("{" + "shapePath" + "}" , str(allParams['shapePath']))
        else:
            resourcePath = re.sub("[&?]shapePath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ShapeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutSetParagraphPortionProperties(self, name, slideIndex, shapeIndex, paragraphIndex, portionIndex, body, **kwargs):
        """Updates paragraph portion properties.
        Args:
            name (str):  (required)

            slideIndex (int):  (required)

            shapeIndex (int):  (required)

            paragraphIndex (int):  (required)

            portionIndex (int):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            body (Portion):  (required)

            

        Returns: PortionResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'shapeIndex', 'paragraphIndex', 'portionIndex', 'folder', 'storage', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutSetParagraphPortionProperties" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/shapes/{shapeIndex}/paragraphs/{paragraphIndex}/portions/{portionIndex}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'shapeIndex' in allParams and allParams['shapeIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "shapeIndex" + "}" , str(allParams['shapeIndex']))
        else:
            resourcePath = re.sub("[&?]shapeIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'paragraphIndex' in allParams and allParams['paragraphIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "paragraphIndex" + "}" , str(allParams['paragraphIndex']))
        else:
            resourcePath = re.sub("[&?]paragraphIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'portionIndex' in allParams and allParams['portionIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "portionIndex" + "}" , str(allParams['portionIndex']))
        else:
            resourcePath = re.sub("[&?]portionIndex.*?(?=&|\\?|$)", "", resourcePath)
        

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
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'PortionResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutSlideShapeInfo(self, name, slideIndex, shapePath, body, **kwargs):
        """Updates shape properties.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide index. (required)

            shapePath (str): Shape path. (required)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            body (Shape): Shape dto. (required)

            

        Returns: ShapeResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'shapePath', 'folder', 'storage', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutSlideShapeInfo" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/shapes/{shapePath}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'shapePath' in allParams and allParams['shapePath'] is not None:
            resourcePath = resourcePath.replace("{" + "shapePath" + "}" , str(allParams['shapePath']))
        else:
            resourcePath = re.sub("[&?]shapePath.*?(?=&|\\?|$)", "", resourcePath)
        

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
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ShapeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteSlideByIndex(self, name, slideIndex, **kwargs):
        """Delete presentation slide by its index.
        Args:
            name (str): The presentation name. (required)

            slideIndex (int): The slide index. (required)

            folder (str): The presentation folder. (optional)

            storage (str): The presentation storage. (optional)

            

        Returns: SlideListResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteSlideByIndex" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideListResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteSlidesCleanSlidesList(self, name, **kwargs):
        """Delete presentation slides.
        Args:
            name (str): The presentation name. (required)

            folder (str): The presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: SlideListResponse
        """

        allParams = dict.fromkeys(['name', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteSlidesCleanSlidesList" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideListResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteSlidesSlideBackground(self, name, slideIndex, **kwargs):
        """Remove presentation slide background color.
        Args:
            name (str):  (required)

            slideIndex (int):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: SlideBackgroundResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteSlidesSlideBackground" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/background/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideBackgroundResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesSlide(self, name, slideIndex, **kwargs):
        """Read slide info.
        Args:
            name (str):  (required)

            slideIndex (int):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: SlideResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesSlide" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesSlideBackground(self, name, slideIndex, **kwargs):
        """Read presentation slide background color type.
        Args:
            name (str):  (required)

            slideIndex (int):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: SlideBackgroundResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesSlideBackground" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/background/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideBackgroundResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesSlideComments(self, name, slideIndex, **kwargs):
        """Read presentation slide comments.
        Args:
            name (str):  (required)

            slideIndex (int):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: SlideCommentsResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesSlideComments" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/comments/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideCommentsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesSlidesList(self, name, **kwargs):
        """Read presentation slides info.
        Args:
            name (str): The presentation name. (required)

            folder (str): The presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: SlideListResponse
        """

        allParams = dict.fromkeys(['name', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesSlidesList" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideListResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlideWithFormat(self, name, slideIndex, format, **kwargs):
        """Convert slide to some format.
        Args:
            name (str):  (required)

            slideIndex (int):  (required)

            format (str):  (required)

            width (int):  (optional)

            height (int):  (optional)

            folder (str):  (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'format', 'width', 'height', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlideWithFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/?appSid={appSid}&amp;toFormat={toFormat}&amp;width={width}&amp;height={height}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'width' in allParams and allParams['width'] is not None:
            resourcePath = resourcePath.replace("{" + "width" + "}" , str(allParams['width']))
        else:
            resourcePath = re.sub("[&?]width.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'height' in allParams and allParams['height'] is not None:
            resourcePath = resourcePath.replace("{" + "height" + "}" , str(allParams['height']))
        else:
            resourcePath = re.sub("[&?]height.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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

        

        

    def PostAddEmptySlide(self, name, **kwargs):
        """Add empty slide to the end of presentation
        Args:
            name (str): The presentation name. (required)

            folder (str): The presentation folder. (optional)

            storage (str): The presentation storage. (optional)

            

        Returns: SlideListResponse
        """

        allParams = dict.fromkeys(['name', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostAddEmptySlide" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideListResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostAddEmptySlideAtPosition(self, name, position, **kwargs):
        """Add empty presentation slide to the end of presentation
        Args:
            name (str): The presentation name. (required)

            position (int): The presentation slide position. (required)

            folder (str): The presentation folder. (optional)

            storage (str): The presentation storage. (optional)

            

        Returns: SlideListResponse
        """

        allParams = dict.fromkeys(['name', 'position', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostAddEmptySlideAtPosition" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/?appSid={appSid}&amp;position={position}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'position' in allParams and allParams['position'] is not None:
            resourcePath = resourcePath.replace("{" + "position" + "}" , str(allParams['position']))
        else:
            resourcePath = re.sub("[&?]position.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideListResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostAddSlideCopy(self, name, slideToClone, **kwargs):
        """Add a copy of slide to the end of presentation
        Args:
            name (str): The presentation name. (required)

            slideToClone (int): The presentation slide to clone. (required)

            folder (str): The presentation folder. (optional)

            storage (str): The presentation storage. (optional)

            

        Returns: SlideListResponse
        """

        allParams = dict.fromkeys(['name', 'slideToClone', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostAddSlideCopy" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/?appSid={appSid}&amp;slideToClone={slideToClone}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideToClone' in allParams and allParams['slideToClone'] is not None:
            resourcePath = resourcePath.replace("{" + "slideToClone" + "}" , str(allParams['slideToClone']))
        else:
            resourcePath = re.sub("[&?]slideToClone.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideListResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostClonePresentationSlide(self, name, position, slideToClone, **kwargs):
        """Clone presentation slide
        Args:
            name (str): The presentation name. (required)

            position (int): The presentation slide position. (required)

            slideToClone (int): The presentation slide to clone. (required)

            folder (str): The presentation folder. (optional)

            storage (str): The presentation storage. (optional)

            

        Returns: SlideListResponse
        """

        allParams = dict.fromkeys(['name', 'position', 'slideToClone', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostClonePresentationSlide" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/?appSid={appSid}&amp;position={position}&amp;slideToClone={slideToClone}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'position' in allParams and allParams['position'] is not None:
            resourcePath = resourcePath.replace("{" + "position" + "}" , str(allParams['position']))
        else:
            resourcePath = re.sub("[&?]position.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideToClone' in allParams and allParams['slideToClone'] is not None:
            resourcePath = resourcePath.replace("{" + "slideToClone" + "}" , str(allParams['slideToClone']))
        else:
            resourcePath = re.sub("[&?]slideToClone.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideListResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostCopySlideFromSourcePresentation(self, name, slideToCopy, source, position, **kwargs):
        """Copy slide from source presentation
        Args:
            name (str): The presentation name. (required)

            slideToCopy (int): The presentation slide to copy. (required)

            source (str): The source presentation. (required)

            position (int): The presentation slide position. (required)

            folder (str): The presentation folder. (optional)

            storage (str): The presentation storage. (optional)

            

        Returns: SlideListResponse
        """

        allParams = dict.fromkeys(['name', 'slideToCopy', 'source', 'position', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostCopySlideFromSourcePresentation" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/?appSid={appSid}&amp;slideToCopy={slideToCopy}&amp;source={source}&amp;position={position}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideToCopy' in allParams and allParams['slideToCopy'] is not None:
            resourcePath = resourcePath.replace("{" + "slideToCopy" + "}" , str(allParams['slideToCopy']))
        else:
            resourcePath = re.sub("[&?]slideToCopy.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'source' in allParams and allParams['source'] is not None:
            resourcePath = resourcePath.replace("{" + "source" + "}" , str(allParams['source']))
        else:
            resourcePath = re.sub("[&?]source.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'position' in allParams and allParams['position'] is not None:
            resourcePath = resourcePath.replace("{" + "position" + "}" , str(allParams['position']))
        else:
            resourcePath = re.sub("[&?]position.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideListResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostSlidesReorderPosition(self, name, oldPosition, newPosition, **kwargs):
        """Reorder presentation slide position
        Args:
            name (str): The presentation name. (required)

            oldPosition (int): The new presentation slide position. (required)

            newPosition (int): The new presentation slide position. (required)

            folder (str): The presentation folder. (optional)

            storage (str): The presentation storage. (optional)

            

        Returns: SlideListResponse
        """

        allParams = dict.fromkeys(['name', 'oldPosition', 'newPosition', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSlidesReorderPosition" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/?appSid={appSid}&amp;oldPosition={oldPosition}&amp;newPosition={newPosition}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'oldPosition' in allParams and allParams['oldPosition'] is not None:
            resourcePath = resourcePath.replace("{" + "oldPosition" + "}" , str(allParams['oldPosition']))
        else:
            resourcePath = re.sub("[&?]oldPosition.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newPosition' in allParams and allParams['newPosition'] is not None:
            resourcePath = resourcePath.replace("{" + "newPosition" + "}" , str(allParams['newPosition']))
        else:
            resourcePath = re.sub("[&?]newPosition.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideListResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutSlidesSlideBackground(self, name, slideIndex, body, **kwargs):
        """Set presentation slide background color.
        Args:
            name (str):  (required)

            slideIndex (int):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            body (str):  (required)

            

        Returns: SlideBackgroundResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutSlidesSlideBackground" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/background/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

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
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideBackgroundResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesPresentationTextItems(self, name, **kwargs):
        """Extract presentation text items.
        Args:
            name (str): Presentation name. (required)

            withEmpty (bool): Incude empty items. (optional)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: TextItemsResponse
        """

        allParams = dict.fromkeys(['name', 'withEmpty', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesPresentationTextItems" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/textItems/?appSid={appSid}&amp;withEmpty={withEmpty}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'withEmpty' in allParams and allParams['withEmpty'] is not None:
            resourcePath = resourcePath.replace("{" + "withEmpty" + "}" , str(allParams['withEmpty']))
        else:
            resourcePath = re.sub("[&?]withEmpty.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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

        

        

    def GetSlidesSlideTextItems(self, name, slideIndex, **kwargs):
        """Extract slide text items.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide's index. (required)

            withEmpty (bool): Include empty items. (optional)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: TextItemsResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'withEmpty', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesSlideTextItems" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/textItems/?appSid={appSid}&amp;withEmpty={withEmpty}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'withEmpty' in allParams and allParams['withEmpty'] is not None:
            resourcePath = resourcePath.replace("{" + "withEmpty" + "}" , str(allParams['withEmpty']))
        else:
            resourcePath = re.sub("[&?]withEmpty.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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

        

        

    def PostSlidesPresentationReplaceText(self, name, oldValue, newValue, **kwargs):
        """Replace text by a new value.
        Args:
            name (str): The presentation name. (required)

            oldValue (str): Text value to replace. (required)

            newValue (str): The new text value. (required)

            ignoreCase (bool): Is case must be ignored. (optional)

            folder (str): The presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: PresentationStringReplaceResponse
        """

        allParams = dict.fromkeys(['name', 'oldValue', 'newValue', 'ignoreCase', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSlidesPresentationReplaceText" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/replaceText/?oldValue={oldValue}&amp;newValue={newValue}&amp;appSid={appSid}&amp;ignoreCase={ignoreCase}&amp;folder={folder}&amp;storage={storage}'
        
    
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
        

        if 'ignoreCase' in allParams and allParams['ignoreCase'] is not None:
            resourcePath = resourcePath.replace("{" + "ignoreCase" + "}" , str(allParams['ignoreCase']))
        else:
            resourcePath = re.sub("[&?]ignoreCase.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'PresentationStringReplaceResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostSlidesSlideReplaceText(self, name, slideIndex, oldValue, newValue, **kwargs):
        """Replace text by a new value.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide's index. (required)

            oldValue (str): Text to replace. (required)

            newValue (str): New text value. (required)

            ignoreCase (bool): Is case must be ignored. (optional)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: SlideStringReplaceResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'oldValue', 'newValue', 'ignoreCase', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSlidesSlideReplaceText" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/replaceText/?oldValue={oldValue}&amp;newValue={newValue}&amp;appSid={appSid}&amp;ignoreCase={ignoreCase}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'oldValue' in allParams and allParams['oldValue'] is not None:
            resourcePath = resourcePath.replace("{" + "oldValue" + "}" , str(allParams['oldValue']))
        else:
            resourcePath = re.sub("[&?]oldValue.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newValue' in allParams and allParams['newValue'] is not None:
            resourcePath = resourcePath.replace("{" + "newValue" + "}" , str(allParams['newValue']))
        else:
            resourcePath = re.sub("[&?]newValue.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'ignoreCase' in allParams and allParams['ignoreCase'] is not None:
            resourcePath = resourcePath.replace("{" + "ignoreCase" + "}" , str(allParams['ignoreCase']))
        else:
            resourcePath = re.sub("[&?]ignoreCase.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SlideStringReplaceResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesTheme(self, name, slideIndex, **kwargs):
        """Read slide theme info.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide's index. (required)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: ThemeResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesTheme" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/theme/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ThemeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesThemeColorScheme(self, name, slideIndex, **kwargs):
        """Read slide theme color scheme info.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide's index. (required)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: ColorSchemeResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesThemeColorScheme" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/theme/colorScheme/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ColorSchemeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesThemeFontScheme(self, name, slideIndex, **kwargs):
        """Read slide theme font scheme info.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide's index. (required)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: FontSchemeResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesThemeFontScheme" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/theme/fontScheme/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'FontSchemeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetSlidesThemeFormatScheme(self, name, slideIndex, **kwargs):
        """Read slide theme color scheme info.
        Args:
            name (str): Presentation name. (required)

            slideIndex (int): Slide's index. (required)

            folder (str): Presentation folder. (optional)

            storage (str): Presentation storage. (optional)

            

        Returns: FormatSchemeResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetSlidesThemeFormatScheme" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/theme/formatScheme/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'FormatSchemeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        
    def PostAddNewShape(self, name, slideIndex, body, **kwargs):
        """
        Args:
            name (str):  (required)

            slideIndex (int):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            body (Shape):  (required)

            

        Returns: ShapeResponse
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'folder', 'storage', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostAddNewShape" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/shapes/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ShapeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        
    def GetShapeWithFormat(self, name, slideIndex, shapeIndex, format, **kwargs):
        """
        Args:
            name (str):  (required)

            slideIndex (int):  (required)

            shapeIndex (int):  (required)

            format (str):  (required)

            folder (str):  (optional)

            storage (str):  (optional)

            scaleX (float):  (optional)

            scaleY (float):  (optional)

            bounds (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'slideIndex', 'shapeIndex', 'format', 'folder', 'storage', 'scaleX', 'scaleY', 'bounds'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetShapeWithFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/slides/{slideIndex}/shapes/{shapeIndex}/?toFormat={toFormat}&amp;appSid={appSid}&amp;folder={folder}&amp;storage={storage}&amp;scaleX={scaleX}&amp;scaleY={scaleY}&amp;bounds={bounds}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'slideIndex' in allParams and allParams['slideIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "slideIndex" + "}" , str(allParams['slideIndex']))
        else:
            resourcePath = re.sub("[&?]slideIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'shapeIndex' in allParams and allParams['shapeIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "shapeIndex" + "}" , str(allParams['shapeIndex']))
        else:
            resourcePath = re.sub("[&?]shapeIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'scaleX' in allParams and allParams['scaleX'] is not None:
            resourcePath = resourcePath.replace("{" + "scaleX" + "}" , str(allParams['scaleX']))
        else:
            resourcePath = re.sub("[&?]scaleX.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'scaleY' in allParams and allParams['scaleY'] is not None:
            resourcePath = resourcePath.replace("{" + "scaleY" + "}" , str(allParams['scaleY']))
        else:
            resourcePath = re.sub("[&?]scaleY.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'bounds' in allParams and allParams['bounds'] is not None:
            resourcePath = resourcePath.replace("{" + "bounds" + "}" , str(allParams['bounds']))
        else:
            resourcePath = re.sub("[&?]bounds.*?(?=&|\\?|$)", "", resourcePath)
        

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

        
    def PostSlidesSaveAsPdf(self, name, body, **kwargs):
        """
        Args:
            name (str):  (required)

            password (str):  (optional)

            storage (str):  (optional)

            folder (str):  (optional)

            outPath (str):  (optional)

            body (PdfExportOptions):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'password', 'storage', 'folder', 'outPath', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSlidesSaveAsPdf" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/saveAs/pdf/?appSid={appSid}&amp;password={password}&amp;storage={storage}&amp;folder={folder}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

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
        files = { }
        bodyParam = body

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


    
    def PostSlidesSaveAsTiff(self, name, body, **kwargs):
        """
        Args:
            name (str):  (required)

            password (str):  (optional)

            storage (str):  (optional)

            folder (str):  (optional)

            outPath (str):  (optional)

            body (TiffExportOptions):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'password', 'storage', 'folder', 'outPath', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSlidesSaveAsTiff" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/saveAs/tiff/?appSid={appSid}&amp;password={password}&amp;storage={storage}&amp;folder={folder}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

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
        files = { }
        bodyParam = body

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


    def PostSlidesSaveAsHtml(self, name, body, **kwargs):
        """
        Args:
            name (str):  (required)

            password (str):  (optional)

            storage (str):  (optional)

            folder (str):  (optional)

            outPath (str):  (optional)

            body (HtmlExportOptions):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'password', 'storage', 'folder', 'outPath', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostSlidesSaveAsHtml" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/slides/{name}/saveAs/html/?appSid={appSid}&amp;password={password}&amp;storage={storage}&amp;folder={folder}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'password' in allParams and allParams['password'] is not None:
            resourcePath = resourcePath.replace("{" + "password" + "}" , str(allParams['password']))
        else:
            resourcePath = re.sub("[&?]password.*?(?=&|\\?|$)", "", resourcePath)
        

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
        files = { }
        bodyParam = body

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


