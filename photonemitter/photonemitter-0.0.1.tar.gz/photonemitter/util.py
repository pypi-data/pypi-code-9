import os
import xdg.DesktopEntry
import xdg.BaseDirectory
import xdg.IconTheme
import glob
import importlib


_desktop_file_search_paths = [os.path.join(x, 'applications', '*.desktop')
                              for x in xdg.BaseDirectory.xdg_data_dirs]
# all desktop files
desktop_files = []
for sp in _desktop_file_search_paths:
    for f in glob.glob(sp):
        if f not in desktop_files:
            desktop_files.append(os.path.join(sp, f))

# DesktopEntry classes for all desktop files
desktop_entries = []
for df in desktop_files:
    desktop_file = xdg.DesktopEntry.DesktopEntry(df)
    desktop_entries.append(desktop_file)


def get_module_attr(attr):
    """
    Gets an attribute from a module referred to with dot notation.
    Ex: get_class_module('email.message.Message') would return the class
    Message from the module email.message.

    Positional arguments:
    attr -- the dot-separated module and attribute to return

    Example:
    >>> get_module_attr('email.message.Message')
    <class 'email.message.Message'>
    """
    split_attr = attr.split('.')
    module_name = '.'.join(split_attr[:-1])
    attr_name = split_attr[-1]

    mod = importlib.import_module(module_name)
    return getattr(mod, attr_name)


def get_icon_file(icon, icon_theme=None):
    """
    Gets the png file for an app's icon

    Positional parameters:
    icon -- the icon to look for. Can be a path or an icon name to grab with
    an XDG icon theme

    Returns:
    A path to a png icon file.
    """
    return xdg.IconTheme.getIconPath(icon, theme=icon_theme,
                                     extensions=['png'])


if __name__ == '__main__':
    from . import test
    test._test()
