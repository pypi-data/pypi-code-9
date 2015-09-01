import io
import json
import os
import pystache

from .boilerplate import BOILERPLATE
from .lice import core as lice

from datetime import date

class PackageManifestException(Exception):
    pass

def parse_package_manifest(package_manifest_json):
    manifest = {}
    parameters = {}
    try:
        manifest = json.loads(package_manifest_json)
    except ValueError:
        raise PackageManifestException('Invalid package manifest.')
    required_attributes = ['name', 'description', 'version', 'author', 'licenses']
    for required_attribute in required_attributes:
        if required_attribute not in manifest:
            raise PackageManifestException('Invalid package manifest. Missing {0} attribute.'.format(required_attribute))
    if 'name' not in manifest['author']:
        raise PackageManifestException('Missing field "name" in "author".')
    if not isinstance(manifest['licenses'], list):
        raise PackageManifestException('Field "license" is not a list.')

    parameters['plugin_name'] = manifest['name'] or ''
    parameters['plugin_name_cc'] = manifest['name'].title() or ''
    parameters['plugin_description'] = manifest['description'] or ''
    parameters['plugin_version'] = manifest['version'] or ''
    parameters['plugin_author'] = manifest['author']['name'] or ''
    parameters['plugin_license'] = ''
    for license in manifest['licenses']:
        if 'type' not in license:
            raise PackageManifestException('Missing field "type" in "license".')
        parameters['plugin_license'] += license['type'] + ','
    parameters['plugin_license'] = parameters['plugin_license'][:-1]
    return parameters

def substitute(content, parameters):
    return pystache.render(content, parameters)

def get_current_dir():
    return os.path.split(__file__)[0]

def generate_files(package_json_path, dest_path):
    package_manifest_content = io.open(package_json_path, encoding='utf-8').read()
    parameters = parse_package_manifest(package_manifest_content)
    boilerplate_dir = os.path.join(get_current_dir(), 'boilerplate')
    for boilerplate_file in BOILERPLATE:
        src_boilerplate_file = os.path.join(boilerplate_dir, boilerplate_file)
        dest_boilerplate_file = os.path.join(dest_path, substitute(boilerplate_file, parameters))
        if not os.path.exists(os.path.split(dest_boilerplate_file)[0]):
            os.makedirs(os.path.split(dest_boilerplate_file)[0])
        io.open(dest_boilerplate_file, 'w', encoding='utf-8').write(substitute(io.open(src_boilerplate_file, encoding='utf-8').read(), parameters))
    for license in parameters['plugin_license'].split(','):
        try:
            context = {}
            context['year'] = '{0}'.format(date.today().year)
            context['organization'] = parameters['plugin_author']
            context['project'] = parameters['plugin_name']
            template = lice.load_package_template(license.strip().lower())
            content = lice.generate_license(template, context)
            out = lice.format_license(content, 'txt')
            out.seek(0)
            with open(os.path.join(dest_path, 'LICENSE'), "a") as f:
                f.write(out.getvalue())
                f.write('\n\n')
            f.close()
        except IOError:
            pass

def install_dependencies(dest_path):
    os.system('cd {0} && bower install qunit'.format(dest_path))
    os.system('cd {0} && bower install jquery'.format(dest_path))
    os.system('cd {0} && npm install'.format(dest_path))