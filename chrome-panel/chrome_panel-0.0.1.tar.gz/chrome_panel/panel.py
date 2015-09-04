from collections import OrderedDict
from importlib import import_module
import json
import uuid

from django.conf.urls import url
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, resolve
from django.http import Http404

from chrome_panel import settings as cp_settings
from chrome_panel.utils import get_name_from_obj


class DebugPanel(object):
    def __init__(self, request, thread_id=None):
        self.request = request
        self.config = cp_settings.CONFIG.copy()
        self._panels = OrderedDict()
        for panel_class in self.get_panel_classes():
            panel_instance = panel_class(self)
            self._panels[panel_instance.panel_id] = panel_instance
        self.stats = {}
        self.store_id = None
        self.response_json = {
            'view_func': '<unknown>',
            'url': reverse('chrome_panels:panel_data', args=[thread_id]),
            'panels': [],
        }
        try:
            self.response_json['view_func'] = get_name_from_obj(resolve(request.path)[0])
        except Http404:
            pass

    @property
    def panels(self):
        """
        Get a list of all available panels.
        """
        return list(self._panels.values())

    @property
    def enabled_panels(self):
        """
        Get a list of panels enabled for the current request.
        """
        return [panel for panel in self._panels.values() if panel.enabled]

    def get_panel_by_id(self, panel_id):
        """
        Get the panel with the given id, which is the class name by default.
        """
        return self._panels[panel_id]

    def render_toolbar(self):
        """
        Renders the overall Toolbar with panels inside.
        """
        if not self.config['RENDER_PANELS']:
            self.store()

        for panel in self.panels:
            panel_data = {'t': str(panel.nav_title)}
            if not panel.enabled:
                continue
            subtitle = panel.nav_subtitle
            if subtitle:
                if not isinstance(subtitle, str):
                    subtitle = subtitle()
                panel_data['s'] = subtitle
            self.response_json['panels'].append(panel_data)

        return json.dumps(self.response_json)

    _store = OrderedDict()

    def store(self):
        self.store_id = uuid.uuid4().hex
        cls = type(self)
        cls._store[self.store_id] = self
        for _ in range(len(cls._store) - self.config['RESULTS_CACHE_SIZE']):
            cls._store.popitem(last=False)

    @classmethod
    def fetch(cls, store_id):
        return cls._store.get(store_id)

    _panel_classes = None

    @classmethod
    def get_panel_classes(cls):
        if cls._panel_classes is None:
            # Load panels in a temporary variable for thread safety.
            panel_classes = []
            for panel_path in cp_settings.PANELS:
                # This logic could be replaced with import_by_path in Django 1.6.
                try:
                    panel_module, panel_classname = panel_path.rsplit('.', 1)
                except ValueError:
                    raise ImproperlyConfigured(
                        "%s isn't a debug panel module" % panel_path)
                try:
                    mod = import_module(panel_module)
                except ImportError as e:
                    raise ImproperlyConfigured(
                        'Error importing debug panel %s: "%s"' %
                        (panel_module, e))
                try:
                    panel_class = getattr(mod, panel_classname)
                except AttributeError:
                    raise ImproperlyConfigured(
                        'Toolbar Panel module "%s" does not define a "%s" class' %
                        (panel_module, panel_classname))
                panel_classes.append(panel_class)
            cls._panel_classes = panel_classes
        return cls._panel_classes

    _urlpatterns = None

    @classmethod
    def get_urls(cls):
        if cls._urlpatterns is None:
            from . import views
            # Load URLs in a temporary variable for thread safety.
            # Global URLs
            urlpatterns = [
                url(r'^panel_data/([\w-]+)/$', views.panels, name='panel_data'),
            ]
            # Per-panel URLs
            for panel_class in cls.get_panel_classes():
                urlpatterns += panel_class.get_urls()
            cls._urlpatterns = urlpatterns
        return cls._urlpatterns


urlpatterns = DebugPanel.get_urls()
