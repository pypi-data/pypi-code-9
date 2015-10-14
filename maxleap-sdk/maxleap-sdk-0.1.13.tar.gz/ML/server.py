# coding: utf-8

import os
import ML
import json
import logging
import traceback
import functools
from flask import Flask, request, Response

__author__ = 'czhou <czhou@ilegendsoft.com>'

Port = 8080
Host = '127.0.0.1'

app = Flask(__name__)

def get_principal():
    if not ML.PRO:
        return None
    str_user_principal = request.headers.get('Las-User-Principal',None)
    if not str_user_principal:
        raise RuntimeError("You can't use server sdk without UserPrincipal")
    json_user_principal = json.loads(str_user_principal)
    session_token = None
    master_key = None
    client_key = None
    if json_user_principal.get('identityType') in ["ORG_USER", "APP_USER"]:
        session_token = json_user_principal.get('sessionToken')
    if json_user_principal.get('identityType') in ["MASTER_KEY"]:
        master_key = json_user_principal.get('key')
    if json_user_principal.get('identityType') in ["API_KEY"]:
        client_key = json_user_principal.get('key')
    return ML.UserPrincipal(ML.client.APP_ID, client_key=client_key, master_key=master_key, session_token=session_token)

@app.after_request
def after_request(response):
    ML.Log.debug("===========Request End===============")
    return response

@app.before_request
def before_request():
    ML.Log.debug("===========Request Start=============")
    ML.Log.debug("Method:{0}".format(request.method))
    ML.Log.info("Headers:\n{0}".format(request.headers))
    ML.Log.info("Body:{0}".format(request.data))

@app.errorhandler(500)
def custom_error(e):
    if isinstance(e, ML.MaxLeapError):
        ML.Log.error(e)
        return Response(
            json.dumps({"errorCode":e.code,"errorMessage":e.error}),
            status=545,
            mimetype='application/json'
        )
    traces_info = traceback.format_exc()
    ML.Log.error(traces_info)
    return Response(
        traces_info,
        status=545,
        mimetype='application/json'
        )

class flask_base_server(object):
    def __init__(self, app, host, port):
        """
        创建一个新的server

        :host: IP
        :port: 端口
        :return:
        """
        self._app = app
        self._host = host
        self._port = port
        self._function_map = {}
        self._job_map = {}
        self._hook_map = {}
        self._hook_classes = set()
        self.setup()

    def setup(self):
        self.before_save = functools.partial(self.Hook, hook_name='before_save')
        self.after_save = functools.partial(self.Hook, hook_name='after_save')
        self.after_update = functools.partial(self.Hook, hook_name='after_update')
        self.before_delete = functools.partial(self.Hook, hook_name='before_delete')
        self.after_delete = functools.partial(self.Hook, hook_name='after_delete')
        self._app.add_url_rule('/health', 'health', self.health)
        self._app.add_url_rule('/console/config', 'config', self.config, methods=['GET','POST'])
        self._app.add_url_rule('/console/functionNames', 'functionNames', self.functionNames, methods=['GET','POST'])
        self._app.add_url_rule('/console/jobNames', 'jobNames', self.jobNames, methods=['GET','POST'])
        self._app.add_url_rule('/console/threadStats', 'threadStats', self.threadStats, methods=['GET','POST'])

    def health(self):
        return "ok"

    def jobNames(self):
        return json.dumps(self._job_map.keys())

    def functionNames(self):
        return json.dumps(self._function_map.keys())

    def config(self):
        if os.path.exists("/home/leap/global.json"):
            return open("/home/leap/global.json").read()
        return "{}"

    def threadStats(self):
        return json.dumps({"queueSize":60,"rejectCount":0})

    def Function(self, func):
        def _deco():
            ML.by_hook(False)
            return func(request)

        self._function_map[func.__name__] = _deco
        self._app.add_url_rule(
            '/function/{}'.format(func.__name__),
            'function.{}'.format(func.__name__),
            _deco,
            methods=['POST']
        )
        return _deco

    def Job(self, func):
        def _deco():
            ML.by_hook(False)
            return func(request)

        self._job_map[func.__name__] = _deco
        self._app.add_url_rule(
            '/job/{}'.format(func.__name__),
            'job.{}'.format(func.__name__),
            _deco,
            methods=['POST']
        )
        return _deco

    def Hook(self, class_name, hook_name):
        hook_name = '{}_{}'.format(hook_name, class_name)
        def _deco(func):
            def __deco():
                ML.by_hook(True)
                method = request.json['method']
                params = request.json['params']
                res = self._handel_hook(class_name, method, params)
                ML.by_hook(False)
                return res

            self._hook_map[hook_name] = func

            if class_name not in self._hook_classes:
                self._app.add_url_rule(
                    '/entityManager/{}'.format(class_name),
                    'entityManager.{}'.format(class_name),
                    __deco,
                    methods=['POST']
                )
            self._hook_classes.add(class_name)
            return __deco
        return _deco

    def _handel_hook(self, class_name, method, params):

        if method == 'create':
            params['principal'] = get_principal()
            obj = ML.Object.create(class_name,**params)

            if 'before_save_{}'.format(class_name) in self._hook_map:
                hook_res = self._hook_map['before_save_{}'.format(class_name)](obj)
                if isinstance(hook_res, Response):return hook_res

            obj.save()
            res = Response(json.dumps({
                "createdAt":"{}.{}Z".format(obj.created_at.strftime('%Y-%m-%dT%H:%M:%S'),obj.created_at.microsecond/1000),
                "objectId":obj.id
                }),
                mimetype='application/json'
            )

            if 'after_save_{}'.format(class_name) in self._hook_map:
                hook_res = self._hook_map['after_save_{}'.format(class_name)](obj)
                if isinstance(hook_res, Response):return hook_res


        elif method == 'update':
            attrs = {}
            attrs['objectId'] = params['objectId']
            attrs.update(params['update'])
            attrs['principal'] = get_principal()
            obj = ML.Object.create(class_name,**attrs)
            obj.save()
            res = Response(json.dumps({
                "updatedAt":"{}.{}Z".format(obj.updated_at.strftime('%Y-%m-%dT%H:%M:%S'),obj.updated_at.microsecond/1000),
                "number":1
                }),
                mimetype='application/json'
            )

            if 'after_update_{}'.format(class_name) in self._hook_map:
                hook_res = self._hook_map['after_update_{}'.format(class_name)](obj)
                if isinstance(hook_res, Response):return hook_res

        elif method == 'delete':
            attrs = {}
            attrs['objectId'] = params
            attrs['principal'] = get_principal()
            obj = ML.Object.create(class_name,**attrs)
            if 'before_delete_{}'.format(class_name) in self._hook_map:
                hook_res = self._hook_map['before_delete_{}'.format(class_name)](obj)
                if isinstance(hook_res, Response): return hook_res

            obj.destroy()
            res = Response(json.dumps({
                "number":1
                }),
                mimetype='application/json'
            )

            if 'after_delete_{}'.format(class_name) in self._hook_map:
                hook_res = self._hook_map['after_delete_{}'.format(class_name)](obj)
                if isinstance(hook_res, Response): return hook_res
        else:
            raise ML.MaxLeapError(501, "Unknown method [{}]".format(method))
        if isinstance(res,Response):
            return res
        else:
            raise ML.MaxLeapError(510, "hook didn't return an Response Object")

    def run(self):
        if ML.DEBUG:
            self._app.run(host=self._host, port=self._port)
        else:
            raise Runtime('Not Debug Model')

    def callFunction(self, name, *args, **kwargs):
        client = self._app.test_client()
        path = '/function/{0}'.format(name)
        headers = {"Content-Type":"application/json"}
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        return client.post(path, *args, **kwargs)

    def callJob(self, name, *args, **kwargs):
        client = self._app.test_client()
        path = '/job/{0}'.format(name)
        headers = {"Content-Type":"application/json"}
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        return client.post(path, *args, **kwargs)

Server = flask_base_server(app, Host, Port)
