from django.core.urlresolvers import reverse
from rapid.models import Application
from django.conf.urls import url
import inspect
import logging
from os import path

def _split_all_path(file_name):
    file_name = path.splitdrive(file_name)[1]
    p = 'a'
    while p:
        file_name, p = path.split(file_name)
        yield p

def _caller_urls_module():
    st = inspect.stack()
    for rec in st:
        file_name = rec[1]
        segments = list(_split_all_path(file_name))
        i = 0
        for i in xrange(0, len(segments) - 2):
            p = path.normcase(segments[i])
            p = path.splitext(p)[0]
            if p == "urls":
                return segments[i+1]
    return None

def _model_name(model):
    if hasattr(model, "url_name"):
        return model.url_name
    return model._meta.verbose_name

class MenuEntry:
    """
    The data that goes on a menu item.
    Model, permissions and url
    """
    def __init__(self, model, permission, url_name=None):
        self.url_name = url_name
        self.model = model
        self.permission = permission

    def get_url(self, instance=None):
        ats = [(x, getattr(instance, x)) for x in self.action.query_parameters]
        return reverse(self.url, kwargs=dict(ats))

    def __unicode__(self):
        return u"Menu entry: " + self.url_name + " -> " + unicode(self.action)

    def __str__(self):
        return str(unicode(self))


class ModuleEntry:
    """
    Module data used at menu construction
    """
    def __init__(self, python_name, menu_name):
        self.python_name = python_name
        self.menu_name = menu_name
        self.models = set()


class Action:
    """
    An action to be done over a model.
    Default actions are "list", "view", "edit", "add", "delete", and "select",
    those are defined at the views module.
    """
    def __init__(self, name, url_parameters, query_parameters, view_factory,
                 verbose_name=None, icon=None, visibility=None):
        self.name = name
        self.url_parameters = url_parameters
        self.query_parameters = query_parameters
        self.view_factory = view_factory
        self.verbose_name = verbose_name if verbose_name else name
        self.icon = icon
        self.visibility = self.Visibility.details if visibility is None else visibility

    def __unicode__(self):
        return u"Action: " + self.name

    def __str__(self):
        return str(unicode(self))

    class Visibility:
        hidden = 1
        details = 2
        list = 3


class _Registry:
    """
    Registry of URLs, models and views present on the menu

    The registry must:
        -- for the menu creation
        list registered modules
        list registered models
        list menu entries by module
        list actions by model
        reverse url of action and model
        -- for crud generation
        query if model is registered
        list actions by model
        reverse url of action and model
    """

    def __init__(self):
        """
        Populates the menu registry
        """
        self._modules = {}  # ModuleEntry by python_name
        self._models = {}  # {'action name': MenuEntry} by model class
        for a in Application.objects.filter(enabled=True):
            m = ModuleEntry(a.python_name, a.name)
            self._modules[a.python_name] = m

    def register_action(self, action, entry, **kwargs):
        """
        Registers an action at this registry, so it will appear on the menu
        and can be reversed at the cruds.
        :param action: Action type
        :param entry: The menu entry where it will appear
        :param kwargs: Arguments (besides model) that'll be passed to the view_factory of the action
        :return: A Django URL pattern that should be added to the patterns of a urls.py module
        """
        from django.contrib.auth.models import User
        module_name = _caller_urls_module()
        model = entry.model
        if not module_name:
            raise Exception("Unidentified python module registering " + str(model))
        if not registry._modules.has_key(module_name):
            logging.error("Module " + module_name + " is not set-up for registering cruds")
            return None

        module_entry = registry._modules[module_name]
        module_entry.models.add(model)

        if not entry.url_name:
            entry.url_name = _model_name(model)
        entry.action = action
        entry_url = module_entry.menu_name + '_' + entry.url_name + '_' + action.name
        entry.url = entry_url
        model_actions = self._models.get(model, {})
        if model_actions.has_key(action.name):
            raise Exception("Action " + action.name + " already registered for model " + str(model))
        model_actions[action.name] = entry
        self._models[model] = model_actions
        return url(r'^%s/%s/%s$' % (entry.url_name, action.name, action.url_parameters),
                   action.view_factory(model=entry.model, **kwargs), name=entry_url)


    def get_url_of_action(self, model, action_name, **kwargs):
        acts = self._models.get(model)
        if acts and acts.has_key(action_name):
            return reverse(acts[action_name].url, kwargs=kwargs)

    def modules(self):
        return self._modules.values()

    def entry_names(self):
        return [x.menu_name for x in self._modules.values()]

    def is_controlled(self, model):
        return self._models.has_key(model)

    def model_entry(self, model):
        return self._models.get(model)

    def module_models(self, module):
        return self._modules[module].models


registry = _Registry()
