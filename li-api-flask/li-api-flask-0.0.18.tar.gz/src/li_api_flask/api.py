# -*- coding: utf-8 -*-

__author__ = 'renato'

from li_api_flask import settings
from li_common.helpers import pegar_versao_git

from flask import Flask, Blueprint
from flask_restful import Api
from flask_restful.utils import cors
from flask_restful import Resource

from raven.contrib.flask import Sentry
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware


class LIFlask():

    __application = None
    __prefix = '/loja/<int:loja_id>'
    def __init__(self):
        self.__application = Flask(__name__)
        self.__application.config.from_object(settings)
        self.__application.debug = settings.DEBUG

        self.__bp_main = Blueprint('main', __name__)
        self.__criar_resource_default()
        self.__application.register_blueprint(self.__bp_main)

        if settings.SENTRY_DSN_API:
            sentry = Sentry(dsn=settings.SENTRY_DSN_API)
            sentry.init_app(self.__application)


    def __criar_resource_default(self):
        self.__api_main = Api(self.__bp_main)
        self.__api_main.decorators = [cors.crossdomain(origin='*', headers=['Authorization', 'Content-Type', 'Accept'])]
        self.__api_main.add_resource(Home, '/')
        self.__api_main.add_resource(Healthcheck, '/healthcheck')

    
    def registrar_blueprint(self, blueprint, **options):

        if not options.get('ignore_prefix', False):
            if options.has_key('url_prefix'):
                options['url_prefix'] = self.__prefix + options.get('url_prefix')
            else:
                options['url_prefix'] = self.__prefix
        else:
            del options['ignore_prefix']

        self.__application.register_blueprint(blueprint, **options)

    def retorna_app_flask(self):
        return self.__application;

    def criar_dispatcher(self):
        return DispatcherMiddleware(self.__application, { })

    def run_develop(self):
        if(self.__application is None):
            raise ValueError("Nenhuma aplicação foi criada.\nUsar app=LIFlask()\napp.run_app()")

        self.app = self.criar_dispatcher()
        run_simple('0.0.0.0', 4000, self.app, use_reloader=True, use_debugger=settings.DEBUG)

    def run(self):
        if(self.__application is None):
            raise ValueError("Nenhuma aplicação foi criada.\nUsar app=LIFlask()\napp.run_app()")

        return self.criar_dispatcher()


class Home(Resource):
    def get(self):
        return '{}'

class Healthcheck(Resource):
    def get(self):
        return "Health Check OK - {}".format(pegar_versao_git())
