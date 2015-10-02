import os
import shutil
import linktastic

import lnkr
import term

from import_section import ImportSection, MODE_COPY, MODE_LINK, MODE_SYMLINK
from export_section import ExportSection

def do_link_app(app_config):
    term.info('\nStart Linking App: %s' % term.format_path(app_config.path))
    for section in app_config.import_sections:
        link_import_section('Import', app_config, section, [app_config])
    term.info('\nFinish Linking App: %s' % term.format_path(app_config.path))

def get_new_attribs_holders(attribs_holders, new_holder):
    if new_holder in attribs_holders:
        return attribs_holders
    else:
        new_attribs_holders = list(attribs_holders)
        new_attribs_holders.append(new_holder)
        return new_attribs_holders

def link_import_section(kind, app_config, import_section, attribs_holders):
    term.info('\nLoading %s Section: %s' % (kind, term.format_param(import_section.key)))
    import_section.load()
    if not import_section.loaded:
        return
    link_import_section_component(app_config, import_section, import_section.key, get_new_attribs_holders(attribs_holders, import_section))

def link_import_section_component(app_config, import_section, key, attribs_holders):
    if app_config.is_component_linked(key):
        #term.verbose('\nBypass Import Section: %s, Component: %s' % (term.format_param(import_section.key), term.format_param(key)))
        return
    term.info('\nLinking Component, Section: %s, Key: %s' % (term.format_param(import_section.key), term.format_param(key)))

    error = 'Component Not Found'
    component = import_section.get_component(key)
    if component is not None:
        if isinstance(component, ExportSection):
            export_section = component
            app_config.mark_linked_component(key, export_section)
            error = link_import_section_package_export(app_config, import_section, import_section.package_config, export_section, get_new_attribs_holders(attribs_holders, import_section.package_config))
        elif isinstance(component, ImportSection):
            wrapper_section = component
            error = link_import_section_wrapper_import(app_config, import_section, import_section.wrapper_config, wrapper_section, attribs_holders)

    if error is not None:
        term.error('\nLinking Component Failed, Section: %s, Key: %s, Reason: %s' % (term.format_param(import_section.key), term.format_param(key), error))

# GOCHA: it's a bit messy here, since want to put the dependencies' attribs inside the accessor
def update_required_attribs_holders(attribs_holders, import_section, require_key):
    component = import_section.get_component(require_key)
    if component is not None:
        if isinstance(component, ExportSection):
            attribs_holders = get_new_attribs_holders(attribs_holders, import_section.package_config)
            attribs_holders = get_new_attribs_holders(attribs_holders, component)
            attribs_holders = get_required_attribs_holders(attribs_holders, import_section, component.requires)
        elif isinstance(component, ImportSection):
            attribs_holders = get_new_attribs_holders(attribs_holders, import_section.wrapper_config)
            attribs_holders = update_required_attribs_holders(attribs_holders, component, require_key)
    return attribs_holders

def get_required_attribs_holders(attribs_holders, import_section, requires):
    for require_key in requires:
        attribs_holders = update_required_attribs_holders(attribs_holders, import_section, require_key)
    return attribs_holders

def link_import_section_package_export(app_config, import_section, package_config, export_section, attribs_holders):
    new_attribs_holders = get_new_attribs_holders(attribs_holders, export_section)

    for require_key in export_section.requires:
        link_import_section_component(app_config, import_section, require_key, new_attribs_holders)

    link_attribs_holders = get_required_attribs_holders(new_attribs_holders, import_section, export_section.requires)
    for folder in export_section.folders:
        ok, from_path, to_path = check_link_folder('Folder', export_section.key, package_config.root_path, app_config.root_path, folder, link_attribs_holders)
        if ok:
            do_link_folder(import_section.mode, export_section.key, from_path, to_path)
    for fc in export_section.files:
        ok, from_path, to_path = check_link_folder('File', export_section.key, package_config.root_path, app_config.root_path, fc, link_attribs_holders)
        if ok:
            files = fc.get_file_list(from_path)
            for f in files:
                do_link_file(import_section.mode, export_section.key, from_path, to_path, f)

def link_import_section_wrapper_import(app_config, import_section, wrapper_config, wrapper_section, attribs_holders):
    link_import_section('Wrapper', app_config, wrapper_section, get_new_attribs_holders(attribs_holders, wrapper_config))

def check_link_folder(kind, key, from_root_path, to_root_path, folder_config, attribs_holders):
    from_path = folder_config.get_from_path(from_root_path)
    to_path = folder_config.get_to_path(to_root_path, attribs_holders)
    ok = False
    if not from_path.startswith(from_root_path):
        term.error('Link %s Failed, Component: %s\n\tFrom Root: %s\n\tInvalid From: %s' %
                (kind, term.format_param(key), term.format_path(from_root_path), term.format_path(from_path)))
    elif not to_path.startswith(to_root_path):
        term.error('Link %s Failed, Component: %s\n\tTo Root: %s\n\tInvalid To: %s' %
                (kind, term.format_param(key), term.format_path(to_root_path), term.format_path(to_path)))
    elif not os.path.isdir(from_path):
        term.error('Link %s Failed, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
                (kind, term.format_param(key), term.format_error('From Folder Not Exist'), term.format_path(from_path), term.format_path(to_path)))
    else:
        ok = True
    return ok, from_path, to_path

def cleanup_path(to_path):
    if os.path.islink(to_path):
        term.info('Remove Link: %s' % term.format_path(to_path))
        os.remove(to_path)
    elif os.path.isdir(to_path):
        term.info('Remove Folder: %s' % term.format_path(to_path))
        shutil.rmtree(to_path)
    elif os.path.isfile(to_path):
        term.info('Remove File: %s' % term.format_path(to_path))
        os.remove(to_path)

def do_link_folder(mode, key, from_path, to_path):
    if lnkr.test_mode:
        term.info('Link Folder, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
                (term.format_param(key), term.format_error('Test Mode, NOT Doing Anything'), term.format_path(from_path), term.format_path(to_path)))
    elif not os.path.exists(to_path) or lnkr.confirm_change('Changes In Folder Will be Lost, Are You Sure?\n%s, %s' % (term.format_param(key), term.format_path(to_path))):
        cleanup_path(to_path)
        if mode == MODE_COPY:
            do_link_folder_copy(key, from_path, to_path)
        elif mode == MODE_LINK:
            do_link_folder_link(key, from_path, to_path)
        elif mode == MODE_SYMLINK:
            do_link_folder_symlink(key, from_path, to_path)
    else:
        term.info('Link Folder, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
                (term.format_param(key), term.format_error('Skipped'), term.format_path(from_path), term.format_path(to_path)))

def check_parent_folder(key, to_path):
    parent_path = os.path.dirname(to_path)
    if not os.path.exists(parent_path):
        os.makedirs(parent_path, 0755)
    elif os.path.isfile(parent_path):
        term.info('Link Folder, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
                (term.format_param(key), term.format_error('"symlink" Failed: Parent Path is Not a Folder'), term.format_path(from_path), term.format_path(to_path)))
        return False
    return True

def do_link_folder_copy(key, from_path, to_path):
    if not check_parent_folder(key, to_path):
        return
    #TODO: not using os.system to support Windows
    os.system('cp -r %s "%s" "%s"' % (term.verbose_mode and '-v' or '', from_path, to_path))
    term.info('Link Folder, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
            (term.format_param(key), term.format_param('"copy" Done'), term.format_path(from_path), term.format_path(to_path)))

def do_link_folder_link(key, from_path, to_path):
    term.info('Link Folder, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
            (term.format_param(key), term.format_error('"link" Mode Not Implemented'), term.format_path(from_path), term.format_path(to_path)))

def get_folder_rel_from_path(from_path, to_path):
    to_dir = os.path.dirname(to_path)
    prefix = os.path.dirname(os.path.commonprefix([from_path, to_path]))
    if prefix:
        old_from_path = from_path
        from_path = os.path.join(os.path.relpath(prefix, to_dir), os.path.relpath(from_path, prefix))
        term.verbose("get_folder_rel_from_path()\n\told_from_path: %s\n\tto_path: %s\n\tprefix: %s\n\tfrom_path: %s" %
                     (term.format_path(old_from_path), term.format_path(to_path), term.format_path(prefix), term.format_path(from_path)))
    return from_path

def do_link_folder_symlink(key, from_path, to_path):
    if not check_parent_folder(key, to_path):
        return
    from_path = get_folder_rel_from_path(from_path, to_path)
    linktastic.symlink(from_path, to_path)
    term.info('Link Folder, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
            (term.format_param(key), term.format_param('"symlink" Done'), term.format_path(from_path), term.format_path(to_path)))

def do_link_file(mode, key, from_path, to_path, file_path):
    from_path = os.path.join(from_path, file_path)
    to_path = os.path.join(to_path, file_path)
    if lnkr.test_mode:
        term.info('Link File, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
                (term.format_param(key), term.format_error('Test Mode, NOT Doing Anything'), term.format_path(from_path), term.format_path(to_path)))
    elif not os.path.exists(to_path) or lnkr.confirm_change('Change of File Will be Lost, Are You Sure?\n%s, %s' % (term.format_param(key), term.format_path(to_path))):
        if mode == MODE_COPY:
            do_link_file_copy(key, from_path, to_path)
        elif mode == MODE_LINK:
            do_link_file_link(key, from_path, to_path)
        elif mode == MODE_SYMLINK:
            do_link_file_symlink(key, from_path, to_path)
    else:
        term.info('Link File, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
                (term.format_param(key), term.format_error('Skipped'), term.format_path(from_path), term.format_path(to_path)))

def do_link_file_copy(key, from_path, to_path):
    if not check_parent_folder(key, to_path):
        return
    #TODO: not using os.system to support Windows
    os.system('cp %s "%s" "%s"' % (term.verbose_mode and '-v' or '', from_path, to_path))
    term.info('Link File, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
            (term.format_param(key), term.format_param('"copy" Done'), term.format_path(from_path), term.format_path(to_path)))

def do_link_file_link(key, from_path, to_path):
    term.info('Link File, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
            (term.format_param(key), term.format_error('"link" Mode Not Implemented'), term.format_path(from_path), term.format_path(to_path)))

def get_file_rel_from_path(from_path, to_path):
    from_dir = os.path.dirname(from_path)
    to_dir = os.path.dirname(to_path)
    prefix = os.path.dirname(os.path.commonprefix([from_dir, to_dir]))
    if prefix:
        old_from_path = from_path
        from_path = os.path.join(os.path.relpath(prefix, to_dir), os.path.relpath(from_dir, prefix), os.path.basename(from_path))
        term.verbose("get_file_rel_from_path()\n\told_from_path: %s\n\tto_path: %s\n\tprefix: %s\n\tfrom_path: %s" %
                     (term.format_path(old_from_path), term.format_path(to_path), term.format_path(prefix), term.format_path(from_path)))
    return from_path

def do_link_file_symlink(key, from_path, to_path):
    cleanup_path(to_path)
    if not check_parent_folder(key, to_path):
        return
    from_path = get_file_rel_from_path(from_path, to_path)
    linktastic.symlink(from_path, to_path)
    term.info('Link File, Component: %s -> %s\n\tFrom: %s\n\tTo: %s' %
            (term.format_param(key), term.format_param('"symlink" Done'), term.format_path(from_path), term.format_path(to_path)))


