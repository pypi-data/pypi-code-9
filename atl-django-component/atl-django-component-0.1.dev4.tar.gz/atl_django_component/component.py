# coding=UTF-8
import json
import re
import uuid

class Component(object):
    ''' Component generic class 
    
    '''
    
    def __init__(self, data_provider=None, version=None):
        ''' 
          En template creamos un diccionario para definir los diferentes posibles template que se
        cargara a la hora de llamar al componente, por defecto se carga el template 'default'
        que apuntará siempre a 'vcl/nombre_del_componente.html'
        ''' 
        self.__template = {'default': 'atl_django_component/%s.html' % self.__class__.__name__.lower()}
        self.__styles = 'atl_django_component/%s/css/styles.css' % self.__class__.__name__.lower()
        self.__custom_styles = 'atl_django_component/%s/css/custom_styles.css' % self.__class__.__name__.lower()
        self.__data_provider = data_provider
        self.__version = version
        self.__config = {}
        self.__id = '%s' % uuid.uuid4()
        super(Component, self).__init__()

    @property
    def styles(self):
        return self.__styles

    @styles.setter
    def styles(self, value):
        self.__styles = value

    @property
    def custom_styles(self):
        return self.__custom_styles

    @custom_styles.setter
    def custom_styles(self, value):
        self.__custom_styles = value

    @property
    def data_provider(self):
        return self.__data_provider

    @data_provider.setter
    def data_provider(self, value):
        self.__data_provider = value

    @property
    def template(self):
        return self.__template

    @template.setter
    def template(self, value):
        self.__template = value

    @property
    def config(self):
        my_config = {}
        for i in self.__dict__.keys():
            if not re.match('_.', i):
                my_config[i] = self.__dict__[i]
        return json.dumps(my_config)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value