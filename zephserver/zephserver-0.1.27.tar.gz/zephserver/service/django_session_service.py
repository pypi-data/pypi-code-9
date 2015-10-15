# -*- coding: utf-8 -*-
'''
Copyright 2015 
    Centre de données socio-politiques (CDSP)
    Fondation nationale des sciences politiques (FNSP)
    Centre national de la recherche scientifique (CNRS)
License
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
'''


# django settings must be called before importing models
try:
    import django.conf
    import django.contrib.auth
except:
    pass
import importlib
import logging
import json, sys
import traceback
from threading import Event
from zephserver.infra.service_manager import ServiceManager
from zephserver.service.service_interface import ServiceInterface
try:
    from zephserversettings import SAME_DOMAIN
except: 
    from zephserver.settings import SAME_DOMAIN

class DecorMethod(object):
    def __init__(self, decor, instance):
        self.decor = decor
        self.instance = instance

    def __call__(self, *args, **kw):
        return self.decor( self.instance, *args, **kw)

    def __getattr__(self, name):
        return getattr(self.decor, name)

    def __repr__(self):
        return '<bound method {} of {}>'.format(self.decor, type(self))
    
class ZephSession(ServiceInterface):
    
    _shutdown_event = Event()
    
    def main(self):
        logging.info('launching session service')
        self._shutdown_event.wait()
        self._shutdown_event.clear()
        
    def disable(self):
        logging.warning('asking to stop session service')
        self._shutdown_event.set()
        logging.info('session service stoped')
        
    def get_django_session(self, instance, message):
        logging.info('message %s' ,message)
        message_content = json.loads(message)
        logging.info(message_content)
        try:
            engine = importlib.import_module(django.conf.settings.SESSION_ENGINE)
        except:
            pass
        try:
            if SAME_DOMAIN == True :
                session_key = instance.get_cookie('sessionid')
            else:
                session_key = message_content['session_id']
            
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self._session = engine.SessionStore(session_key)
        logging.info('session %s'% self._session)
        return self._session
      
    def get_current_user(self, instance, message):
        # get_user needs a django request object, but only looks at the session
        class Dummy(object): pass
        django_request = Dummy()
        try:
            #on essaye de se recuperer la session
            django_request.session = self.get_django_session(instance, message)
            user = django.contrib.auth.get_user(django_request)
            logging.info('user session %s'% user.id)
        except:
            # en cas d'echec on reset la connexion a la db
            logging.info('db connection failed, trying reseting db')
            sm = ServiceManager.get_instance()
            db_service = sm.get_service('zephserver.service.db_service/DbService')
            db_service.reset_db()
            #on refait la requete
            django_request.session = self.get_django_session(instance, message)
            user = django.contrib.auth.get_user(django_request)
        try: 
            if user.is_authenticated():
                return user
            else:
                # try basic auth
                if not self.request.headers.has_key('Authorization'):
                    return None
                kind, data = self.request.headers['Authorization'].split(' ')
                if kind != 'Basic':
                    return None
                (username, _, password) = data.decode('base64').partition(':')
                user = django.contrib.auth.authenticate(username = username,
                                                        password = password)
                if user is not None and user.is_authenticated():
                    return user
                return None
        except Exception, e:
            logging.warning("authentification failed %s with exception %s" % (user, e))
