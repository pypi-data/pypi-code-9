"""
Utility functions to access the entry points registry
"""

# Standard library modules.
from operator import attrgetter

# Third party modules.
import pkg_resources

# Local modules.

# Globals and constants variables.

def iter_entry_points(group, name=None):
    entry_points = list(pkg_resources.iter_entry_points(group, name)) #@UndefinedVariable
    entry_points.sort(key=attrgetter('name'))

    for entry_point in entry_points:
        yield entry_point.name, entry_point.load(require=False)

def iter_condition_widget_classes(name=None):
    return iter_entry_points('pyhmsa.gui.spec.condition', name)

def iter_condition_widgets(name=None, *args, **kwargs):
    for name, clasz in iter_condition_widget_classes(name):
        yield name, clasz(*args, **kwargs)

def iter_datum_widget_classes(name=None):
    return iter_entry_points('pyhmsa.gui.spec.datum', name)

def iter_datum_widgets(name=None, *args, **kwargs):
    for name, clasz in iter_datum_widget_classes(name):
        yield name, clasz(*args, **kwargs)

def iter_importer_classes(name=None):
    for name, clasz in iter_entry_points('pyhmsa.fileformat.importer', name):
        for ext in clasz.SUPPORTED_EXTENSIONS:
            yield name, ext, clasz

def iter_importers(name=None, *args, **kwargs):
    for name, ext, clasz in iter_importer_classes(name):
        yield name, ext, clasz(*args, **kwargs)

def iter_exporter_classes(name=None):
    return iter_entry_points('pyhmsa.fileformat.exporter', name)

def iter_exporters(name=None, *args, **kwargs):
    for name, clasz in iter_exporter_classes(name):
        yield name, clasz(*args, **kwargs)

def iter_preferences_widget_classes(name=None):
    return iter_entry_points('pyhmsa.viewer.preferences', name)