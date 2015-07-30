#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import time
import urllib
import requests
from tencentyun import conf
from .auth import Auth

class ImageV2(object):

    def __init__(self, appid, secret_id, secret_key):
        self.IMAGE_FILE_NOT_EXISTS = -1
        self.IMAGE_NETWORK_ERROR = -2
        self.IMAGE_PARAMS_ERROR = -3

        self.EXPIRED_SECONDS = 2592000
        self._secret_id,self._secret_key = secret_id,secret_key
        conf.set_app_info(appid, secret_id, secret_key)
    
    def upload_impl(self, file_obj, bucket, fileid, userid, magic_context, params):
        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url_v2(bucket, userid, fileid)
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign_v2(url, expired)
        # It seems size is never used
        # size = os.path.getsize(filepath)

        data = {}
        if magic_context:
            data['MagicContext'] = magic_context

        headers = {
            'Authorization': 'QCloud '+sign,
            'User-Agent': conf.get_ua(),
        }

        files = {'FileContent': file_obj}

        if 'get' in params:
            query_str = urllib.parse.urlencode(params['get']);
            url = url + '?' + query_str

        r = {}
        try:
            r = requests.post(url, data=data, headers=headers, files=files)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode': r.status_code, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(e), 'data': {}}
            else:
                return {'httpcode': 0, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(e), 'data': {}}
        
        if 'code' in ret:
            if 0 == ret['code']:
                data = {
                    'url': ret['data']['url'],
                    'download_url': ret['data']['download_url'],
                    'fileid': ret['data']['fileid'],
                }
                if 'is_fuzzy' in ret['data']:
                    data['is_fuzzy'] = ret['data']['is_fuzzy']
                if 'is_food' in ret['data']:
                    data['is_food'] = ret['data']['is_food']                   
                return {
                    'httpcode': r.status_code, 
                    'code': ret['code'], 
                    'message': ret['message'], 
                    'data': data
                }
            else:
                return {
                    'httpcode': r.status_code, 
                    'code': ret['code'], 
                    'message': ret['message'], 
                    'data': {}
                }
        else:
            return {'httpcode': r.status_code, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(r.raw), 'data': {}}


    def upload(self, image_file, bucket, fileid = '', userid = '0', magic_context = '', params = {}):
        # if image file is provided as a filepath
        if isinstance(image_file, str):
            filepath = os.path.abspath(image_file)
            if os.path.exists(filepath):
                return self.upload_impl(open(filepath, 'rb'), bucket, fileid, userid, magic_context, params)
            else:
                return {'httpcode': 0, 'code': self.IMAGE_FILE_NOT_EXISTS, 'message': 'file not exists', 'data': {}}
        # if image file is provided as in-memory binary
        elif isinstance(image_file, bytes):
            return self.upload_impl(image_file, bucket, fileid, userid, magic_context, params)
        else:
            return {'httpcode': 0, 'code': self.IMAGE_PARAMS_ERROR, 'message': 'Unrecognized file format', 'data': {}}

    # In fact, u can upload an in-memory binary image by calling both upload and upload_binary in Python 3
    # 'cause in Python 3, str and bytes are two different types
    # The only reason why this function exists is to keep up with Python 2
    def upload_binary(self, image_file, bucket, fileid = '', userid = '0', magic_context = '', params = {}):
        return self.upload_impl(image_file, bucket, fileid, userid, magic_context, params)
 

            
    def stat(self, bucket, fileid, userid = '0'):
        if not fileid:
            return {'httpcode': 0, 'code': self.IMAGE_PARAMS_ERROR, 'message': 'params error', 'data': {}}

        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url_v2(bucket, userid, fileid)
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign_v2(url, expired)

        headers = {
            'Authorization': 'QCloud '+sign,
            'User-Agent': conf.get_ua(),
        }

        r = {}
        try:
            r = requests.get(url, headers=headers)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode': r.status_code, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(e), 'data': {}}
            else:
                return {'httpcode': 0, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(e), 'data': {}}

        if 'code' in ret:
            if 0 == ret['code']:
                return {
                    'httpcode': r.status_code, 
                    'code': ret['code'], 
                    'message': ret['message'], 
                    'data': {
                        'download_url': ret['data']['file_url'],
                        'fileid': ret['data']['file_fileid'],
                        'upload_time': ret['data']['file_upload_time'],
                        'size': ret['data']['file_size'],
                        'md5': ret['data']['file_md5'],
                        'width': ret['data']['photo_width'],
                        'height': ret['data']['photo_height'],
                    }
                }
            else:
                return {
                    'httpcode': r.status_code, 
                    'code': ret['code'], 
                    'message': ret['message'], 
                    'data':{ }
                }
        else:
            return {'httpcode': r.status_code, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(r.raw), 'data': {}}

    def copy(self, bucket, fileid, userid='0'):
        if not fileid:
            return {'httpcode': 0, 'code': self.IMAGE_PARAMS_ERROR, 'message': 'params error', 'data': {}}

        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url_v2(bucket, userid, fileid, 'copy')
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign_v2(url, expired)

        headers = {
            'Authorization': 'QCloud '+sign,
            'User-Agent': conf.get_ua(),
        }

        r = {}
        try:
            r = requests.post(url, headers = headers)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode': r.status_code, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(e), 'data': {}}
            else:
                return {'httpcode': 0, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(e), 'data': {}}

        if 'code' in ret:
            if 0 == ret['code']:
                return {
                    'httpcode': r.status_code, 
                    'code': ret['code'], 
                    'message': ret['message'], 
                    'data': {
                        'url': ret['data']['url'],
                        'download_url': ret['data']['download_url'],
                    },
                }
            else:
                return {
                    'httpcode': r.status_code, 
                    'code': ret['code'], 
                    'message': ret['message'], 
                    'data': {},
                }
        else:
            return {'httpcode': r.status_code, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(r.raw), 'data': {}}


    def delete(self, bucket, fileid, userid = '0'):
        if not fileid:
            return {'httpcode': 0, 'code': self.IMAGE_PARAMS_ERROR, 'message': 'params error', 'data': {}}

        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url_v2(bucket, userid, fileid, 'del')
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign_v2(url, expired)

        headers = {
            'Authorization': sign,
            'User-Agent': conf.get_ua(),
        }

        r = {}
        try:
            r = requests.post(url, headers = headers)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode': r.status_code, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(e), 'data': {}}
            else:
                return {'httpcode': 0, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(e), 'data': {}}

        if 'code' in ret:
            if 0 == ret['code']:
                return {
                    'httpcode': r.status_code, 
                    'code': ret['code'], 
                    'message': ret['message'], 
                    'data': {},
                }
            else:
                return {
                    'httpcode': r.status_code, 
                    'code': ret['code'], 
                    'message': ret['message'], 
                    'data': {},
                }
        else:
            return {'httpcode': r.status_code, 'code': self.IMAGE_NETWORK_ERROR, 'message': str(r.raw), 'data': {}}


    def generate_res_url(self, userid = '0', fileid = '', oper = ''):
        app_info = conf.get_app_info()
        if fileid:
            if oper:
                return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid) + '/' + str(fileid) + '/' + oper
            else:
                return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid) + '/' + str(fileid)
        else:
            return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid)


    def generate_res_url_v2(self, bucket, userid='0', fileid='', oper=''):
        app_info = conf.get_app_info()
        if fileid:
            if oper:
                return app_info['end_point_v2'] + str(app_info['appid']) + '/' + str(bucket) + '/' + str(userid) + '/' + str(fileid) + '/' + oper
            else:
                return app_info['end_point_v2'] + str(app_info['appid']) + '/' + str(bucket) + '/' + str(userid) + '/' + str(fileid)
        else:
            return app_info['end_point_v2'] + str(app_info['appid']) + '/' + str(bucket) + '/' + str(userid)

