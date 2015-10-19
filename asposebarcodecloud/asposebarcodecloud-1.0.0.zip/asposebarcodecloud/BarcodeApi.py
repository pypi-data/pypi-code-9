#!/usr/bin/env python

import sys
import os
import urllib
import json
import re
from models import *
from ApiClient import ApiException


class BarcodeApi(object):

    def __init__(self, apiClient):
      self.apiClient = apiClient

    

    def GetBarcodeGenerate(self, **kwargs):
        """Generate barcode.
        Args:
            text (str): The code text. (optional)

            type (str): Barcode type. (optional)

            format (str): Result format. (optional)

            resolutionX (float): Horizontal resolution. (optional)

            resolutionY (float): Vertical resolution. (optional)

            dimensionX (float): Smallest width of barcode unit (bar or space). (optional)

            dimensionY (float): Smallest height of barcode unit (for 2D barcodes). (optional)

            enableChecksum (str): Sets if checksum will be generated. (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['text', 'type', 'format', 'resolutionX', 'resolutionY', 'dimensionX', 'dimensionY', 'enableChecksum'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetBarcodeGenerate" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/barcode/generate/?appSid={appSid}&amp;text={text}&amp;type={type}&amp;toFormat={toFormat}&amp;resolutionX={resolutionX}&amp;resolutionY={resolutionY}&amp;dimensionX={dimensionX}&amp;dimensionY={dimensionY}&amp;enableChecksum={enableChecksum}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'text' in allParams and allParams['text'] is not None:
            resourcePath = resourcePath.replace("{" + "text" + "}" , str(allParams['text']))
        else:
            resourcePath = re.sub("[&?]text.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'type' in allParams and allParams['type'] is not None:
            resourcePath = resourcePath.replace("{" + "type" + "}" , str(allParams['type']))
        else:
            resourcePath = re.sub("[&?]type.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'resolutionX' in allParams and allParams['resolutionX'] is not None:
            resourcePath = resourcePath.replace("{" + "resolutionX" + "}" , str(allParams['resolutionX']))
        else:
            resourcePath = re.sub("[&?]resolutionX.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'resolutionY' in allParams and allParams['resolutionY'] is not None:
            resourcePath = resourcePath.replace("{" + "resolutionY" + "}" , str(allParams['resolutionY']))
        else:
            resourcePath = re.sub("[&?]resolutionY.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'dimensionX' in allParams and allParams['dimensionX'] is not None:
            resourcePath = resourcePath.replace("{" + "dimensionX" + "}" , str(allParams['dimensionX']))
        else:
            resourcePath = re.sub("[&?]dimensionX.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'dimensionY' in allParams and allParams['dimensionY'] is not None:
            resourcePath = resourcePath.replace("{" + "dimensionY" + "}" , str(allParams['dimensionY']))
        else:
            resourcePath = re.sub("[&?]dimensionY.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'enableChecksum' in allParams and allParams['enableChecksum'] is not None:
            resourcePath = resourcePath.replace("{" + "enableChecksum" + "}" , str(allParams['enableChecksum']))
        else:
            resourcePath = re.sub("[&?]enableChecksum.*?(?=&|\\?|$)", "", resourcePath)
        

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

        

        

    def GetBarcodeRecognize(self, name, **kwargs):
        """Recognize barcode from a file on server.
        Args:
            name (str): The image name. (required)

            type (str): The barcode type. (optional)

            checksumValidation (str): Checksum validation parameter. (optional)

            stripFnc (bool): Allows to strip FNC symbol in recognition results. (optional)

            rotationAngle (int): Allows to correct angle of barcode. (optional)

            barcodesCount (int): Count of barcodes to recognize. (optional)

            rectX (int): Top left point X coordinate of  to recognize barcode inside. (optional)

            rectY (int): Top left point Y coordinate of  to recognize barcode inside. (optional)

            rectWidth (int): Width of  to recognize barcode inside. (optional)

            rectHeight (int): Height of  to recognize barcode inside. (optional)

            storage (str): The image storage. (optional)

            folder (str): The image folder. (optional)

            

        Returns: BarcodeResponseList
        """

        allParams = dict.fromkeys(['name', 'type', 'checksumValidation', 'stripFnc', 'rotationAngle', 'barcodesCount', 'rectX', 'rectY', 'rectWidth', 'rectHeight', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetBarcodeRecognize" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/barcode/{name}/recognize/?appSid={appSid}&amp;type={type}&amp;checksumValidation={checksumValidation}&amp;stripFnc={stripFnc}&amp;rotationAngle={rotationAngle}&amp;barcodesCount={barcodesCount}&amp;rectX={rectX}&amp;rectY={rectY}&amp;rectWidth={rectWidth}&amp;rectHeight={rectHeight}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'type' in allParams and allParams['type'] is not None:
            resourcePath = resourcePath.replace("{" + "type" + "}" , str(allParams['type']))
        else:
            resourcePath = re.sub("[&?]type.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'checksumValidation' in allParams and allParams['checksumValidation'] is not None:
            resourcePath = resourcePath.replace("{" + "checksumValidation" + "}" , str(allParams['checksumValidation']))
        else:
            resourcePath = re.sub("[&?]checksumValidation.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'stripFnc' in allParams and allParams['stripFnc'] is not None:
            resourcePath = resourcePath.replace("{" + "stripFnc" + "}" , str(allParams['stripFnc']))
        else:
            resourcePath = re.sub("[&?]stripFnc.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rotationAngle' in allParams and allParams['rotationAngle'] is not None:
            resourcePath = resourcePath.replace("{" + "rotationAngle" + "}" , str(allParams['rotationAngle']))
        else:
            resourcePath = re.sub("[&?]rotationAngle.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'barcodesCount' in allParams and allParams['barcodesCount'] is not None:
            resourcePath = resourcePath.replace("{" + "barcodesCount" + "}" , str(allParams['barcodesCount']))
        else:
            resourcePath = re.sub("[&?]barcodesCount.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectX' in allParams and allParams['rectX'] is not None:
            resourcePath = resourcePath.replace("{" + "rectX" + "}" , str(allParams['rectX']))
        else:
            resourcePath = re.sub("[&?]rectX.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectY' in allParams and allParams['rectY'] is not None:
            resourcePath = resourcePath.replace("{" + "rectY" + "}" , str(allParams['rectY']))
        else:
            resourcePath = re.sub("[&?]rectY.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectWidth' in allParams and allParams['rectWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "rectWidth" + "}" , str(allParams['rectWidth']))
        else:
            resourcePath = re.sub("[&?]rectWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectHeight' in allParams and allParams['rectHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "rectHeight" + "}" , str(allParams['rectHeight']))
        else:
            resourcePath = re.sub("[&?]rectHeight.*?(?=&|\\?|$)", "", resourcePath)
        

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

        

        

    def PostBarcodeRecognizeFromUrlorContent(self, file, **kwargs):
        """Recognize barcode from an url.
        Args:
            type (str): Barcode type. (optional)

            checksumValidation (str): Checksum validation parameter. (optional)

            stripFnc (bool): Allows to strip FNC symbol in recognition results. (optional)

            rotationAngle (int): Recognition of rotated barcode. Possible angles are 90, 180, 270, default is 0 (optional)

            url (str): The image file url. (optional)

            file (File):  (required)

            

        Returns: BarcodeResponseList
        """

        allParams = dict.fromkeys(['type', 'checksumValidation', 'stripFnc', 'rotationAngle', 'url', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostBarcodeRecognizeFromUrlorContent" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/barcode/recognize/?appSid={appSid}&amp;type={type}&amp;checksumValidation={checksumValidation}&amp;stripFnc={stripFnc}&amp;rotationAngle={rotationAngle}&amp;url={url}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'type' in allParams and allParams['type'] is not None:
            resourcePath = resourcePath.replace("{" + "type" + "}" , str(allParams['type']))
        else:
            resourcePath = re.sub("[&?]type.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'checksumValidation' in allParams and allParams['checksumValidation'] is not None:
            resourcePath = resourcePath.replace("{" + "checksumValidation" + "}" , str(allParams['checksumValidation']))
        else:
            resourcePath = re.sub("[&?]checksumValidation.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'stripFnc' in allParams and allParams['stripFnc'] is not None:
            resourcePath = resourcePath.replace("{" + "stripFnc" + "}" , str(allParams['stripFnc']))
        else:
            resourcePath = re.sub("[&?]stripFnc.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rotationAngle' in allParams and allParams['rotationAngle'] is not None:
            resourcePath = resourcePath.replace("{" + "rotationAngle" + "}" , str(allParams['rotationAngle']))
        else:
            resourcePath = re.sub("[&?]rotationAngle.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'url' in allParams and allParams['url'] is not None:
            resourcePath = resourcePath.replace("{" + "url" + "}" , str(allParams['url']))
        else:
            resourcePath = re.sub("[&?]url.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'BarcodeResponseList', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostGenerateMultiple(self, file, **kwargs):
        """Generate multiple barcodes and return in response stream
        Args:
            format (str): Format to return stream in (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['format', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostGenerateMultiple" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/barcode/generateMultiple/?appSid={appSid}&amp;toFormat={toFormat}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'dto':open(file, 'rb')}
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

        

        

    def PutBarcodeGenerateFile(self, name, file, **kwargs):
        """Generate barcode and save on server.
        Args:
            name (str): The image name. (required)

            text (str): Barcode's text. (optional)

            type (str): The barcode type. (optional)

            format (str): The image format. (optional)

            resolutionX (float): Horizontal resolution. (optional)

            resolutionY (float): Vertical resolution. (optional)

            dimensionX (float): Smallest width of barcode unit (bar or space). (optional)

            dimensionY (float): Smallest height of barcode unit (for 2D barcodes). (optional)

            codeLocation (str): property of the barcode. (optional)

            grUnit (str): Measurement of barcode properties. (optional)

            autoSize (str): Sets if barcode size will be updated automatically. (optional)

            barHeight (float): Height of the bar. (optional)

            imageHeight (float): Height of the image. (optional)

            imageWidth (float): Width of the image. (optional)

            imageQuality (str): Detepmines  of the barcode image. (optional)

            rotAngle (float): Angle of barcode orientation. (optional)

            topMargin (float): Top margin. (optional)

            bottomMargin (float): Bottom margin. (optional)

            leftMargin (float): Left margin. (optional)

            rightMargin (float): Right margin. (optional)

            enableChecksum (str): Sets if checksum will be generated. (optional)

            storage (str): Image's storage. (optional)

            folder (str): Image's folder. (optional)

            file (File):  (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'text', 'type', 'format', 'resolutionX', 'resolutionY', 'dimensionX', 'dimensionY', 'codeLocation', 'grUnit', 'autoSize', 'barHeight', 'imageHeight', 'imageWidth', 'imageQuality', 'rotAngle', 'topMargin', 'bottomMargin', 'leftMargin', 'rightMargin', 'enableChecksum', 'storage', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutBarcodeGenerateFile" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/barcode/{name}/generate/?appSid={appSid}&amp;text={text}&amp;type={type}&amp;toFormat={toFormat}&amp;resolutionX={resolutionX}&amp;resolutionY={resolutionY}&amp;dimensionX={dimensionX}&amp;dimensionY={dimensionY}&amp;codeLocation={codeLocation}&amp;grUnit={grUnit}&amp;autoSize={autoSize}&amp;barHeight={barHeight}&amp;imageHeight={imageHeight}&amp;imageWidth={imageWidth}&amp;imageQuality={imageQuality}&amp;rotAngle={rotAngle}&amp;topMargin={topMargin}&amp;bottomMargin={bottomMargin}&amp;leftMargin={leftMargin}&amp;rightMargin={rightMargin}&amp;enableChecksum={enableChecksum}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'text' in allParams and allParams['text'] is not None:
            resourcePath = resourcePath.replace("{" + "text" + "}" , str(allParams['text']))
        else:
            resourcePath = re.sub("[&?]text.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'type' in allParams and allParams['type'] is not None:
            resourcePath = resourcePath.replace("{" + "type" + "}" , str(allParams['type']))
        else:
            resourcePath = re.sub("[&?]type.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'resolutionX' in allParams and allParams['resolutionX'] is not None:
            resourcePath = resourcePath.replace("{" + "resolutionX" + "}" , str(allParams['resolutionX']))
        else:
            resourcePath = re.sub("[&?]resolutionX.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'resolutionY' in allParams and allParams['resolutionY'] is not None:
            resourcePath = resourcePath.replace("{" + "resolutionY" + "}" , str(allParams['resolutionY']))
        else:
            resourcePath = re.sub("[&?]resolutionY.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'dimensionX' in allParams and allParams['dimensionX'] is not None:
            resourcePath = resourcePath.replace("{" + "dimensionX" + "}" , str(allParams['dimensionX']))
        else:
            resourcePath = re.sub("[&?]dimensionX.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'dimensionY' in allParams and allParams['dimensionY'] is not None:
            resourcePath = resourcePath.replace("{" + "dimensionY" + "}" , str(allParams['dimensionY']))
        else:
            resourcePath = re.sub("[&?]dimensionY.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'codeLocation' in allParams and allParams['codeLocation'] is not None:
            resourcePath = resourcePath.replace("{" + "codeLocation" + "}" , str(allParams['codeLocation']))
        else:
            resourcePath = re.sub("[&?]codeLocation.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'grUnit' in allParams and allParams['grUnit'] is not None:
            resourcePath = resourcePath.replace("{" + "grUnit" + "}" , str(allParams['grUnit']))
        else:
            resourcePath = re.sub("[&?]grUnit.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'autoSize' in allParams and allParams['autoSize'] is not None:
            resourcePath = resourcePath.replace("{" + "autoSize" + "}" , str(allParams['autoSize']))
        else:
            resourcePath = re.sub("[&?]autoSize.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'barHeight' in allParams and allParams['barHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "barHeight" + "}" , str(allParams['barHeight']))
        else:
            resourcePath = re.sub("[&?]barHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'imageHeight' in allParams and allParams['imageHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "imageHeight" + "}" , str(allParams['imageHeight']))
        else:
            resourcePath = re.sub("[&?]imageHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'imageWidth' in allParams and allParams['imageWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "imageWidth" + "}" , str(allParams['imageWidth']))
        else:
            resourcePath = re.sub("[&?]imageWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'imageQuality' in allParams and allParams['imageQuality'] is not None:
            resourcePath = resourcePath.replace("{" + "imageQuality" + "}" , str(allParams['imageQuality']))
        else:
            resourcePath = re.sub("[&?]imageQuality.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rotAngle' in allParams and allParams['rotAngle'] is not None:
            resourcePath = resourcePath.replace("{" + "rotAngle" + "}" , str(allParams['rotAngle']))
        else:
            resourcePath = re.sub("[&?]rotAngle.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'topMargin' in allParams and allParams['topMargin'] is not None:
            resourcePath = resourcePath.replace("{" + "topMargin" + "}" , str(allParams['topMargin']))
        else:
            resourcePath = re.sub("[&?]topMargin.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'bottomMargin' in allParams and allParams['bottomMargin'] is not None:
            resourcePath = resourcePath.replace("{" + "bottomMargin" + "}" , str(allParams['bottomMargin']))
        else:
            resourcePath = re.sub("[&?]bottomMargin.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'leftMargin' in allParams and allParams['leftMargin'] is not None:
            resourcePath = resourcePath.replace("{" + "leftMargin" + "}" , str(allParams['leftMargin']))
        else:
            resourcePath = re.sub("[&?]leftMargin.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rightMargin' in allParams and allParams['rightMargin'] is not None:
            resourcePath = resourcePath.replace("{" + "rightMargin" + "}" , str(allParams['rightMargin']))
        else:
            resourcePath = re.sub("[&?]rightMargin.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'enableChecksum' in allParams and allParams['enableChecksum'] is not None:
            resourcePath = resourcePath.replace("{" + "enableChecksum" + "}" , str(allParams['enableChecksum']))
        else:
            resourcePath = re.sub("[&?]enableChecksum.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutBarcodeRecognizeFromBody(self, name, body, **kwargs):
        """Recognition of a barcode from file on server with parameters in body.
        Args:
            name (str): The image name. (required)

            type (str): The barcode type. (optional)

            folder (str): The image folder. (optional)

            body (BarcodeReader): BarcodeReader object with parameters. (required)

            

        Returns: BarcodeResponseList
        """

        allParams = dict.fromkeys(['name', 'type', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutBarcodeRecognizeFromBody" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/barcode/{name}/recognize/?appSid={appSid}&amp;type={type}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'type' in allParams and allParams['type'] is not None:
            resourcePath = resourcePath.replace("{" + "type" + "}" , str(allParams['type']))
        else:
            resourcePath = re.sub("[&?]type.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'BarcodeResponseList', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutGenerateMultiple(self, name, file, **kwargs):
        """Generate image with multiple barcodes and put new file on server
        Args:
            name (str): New filename (required)

            format (str): Format of file (optional)

            folder (str): Folder to place file to (optional)

            file (File):  (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'format', 'folder', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutGenerateMultiple" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/barcode/{name}/generateMultiple/?appSid={appSid}&amp;toFormat={toFormat}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'dto':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/json,application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['Content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    




