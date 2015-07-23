import inspect

from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from django.conf import settings

from optparse import make_option

from cloudantdb.ext.django.document import Document

    
BASEDOC_STRING = 'cloudantdb.ext.django.document.Document'

def is_document(klass):
    try:
        if issubclass(klass,Document):
            try:
                abstract = klass.Meta.abstract
            except AttributeError:
                abstract = False
            if abstract == True:
                return False
            return True
    except TypeError:
        pass
    return False

 
class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--silent', default=False, dest='silent',
            help='Specifies whether there is output.'),
                                             )
    can_import_settings = True

    def handle(self, *args, **options):
        module = 'models'
        models_list = list()
        silent = options.get('silent') 
        for app in settings.INSTALLED_APPS:
            try:
                models_list.extend(inspect.getmembers(
                    import_module(".%s" % module, app),is_document))
            except ImportError:
                if module_has_submodule(import_module(app), module):
                    raise
                continue
        
        unique_models_list = list(set(models_list))
        for class_name,doc_class in unique_models_list:
            try:
                if not silent:
                    print "Syncing Indexes for {0}".format(class_name)
                doc_class.register_indexes()
            except AttributeError:
                pass
            