from . import exceptions
import os
import yaml
import argparse
import logging

def find_configuration_file_from(folder, filename):
    full_folder_path = os.path.abspath(folder)
    full_file_name = os.path.join(full_folder_path, filename)
    if os.path.isfile(full_file_name):
        return full_file_name
    parent_folder = os.path.dirname(full_folder_path)
    if parent_folder != folder:
        return find_configuration_file_from(parent_folder, filename)
    raise exceptions.FileNotFoundError(filename)

def read_configuration(file_path):
    file_path = os.path.realpath(file_path)
    with open(file_path, 'r') as f:
        raw_conf = yaml.load(f)
        parent_folder = os.path.dirname(file_path)
        conf = {
                'source': convert_path(parent_folder, raw_conf['source'], True),
                'decorator': convert_path(parent_folder, raw_conf['decorator'], True),
                'output': convert_path(parent_folder, raw_conf['output']),
        }
        if 'template' in raw_conf:
            conf['template'] = convert_path(parent_folder, raw_conf['template'], True)
        else:
            conf['template'] = convert_path(os.path.dirname(conf['decorator']), 'templates', True)
        if 'templatemap' in raw_conf:
            conf['templatemap'] = os.path.join(parent_folder, raw_conf['templatemap'])
        else:
            conf['templatemap'] = os.path.join(conf['template'], 'templates.yaml')
        return conf

def convert_path(folder, filename, check = False):
    full_path = os.path.join(folder, filename)
    if check:
        if os.path.isdir(full_path):
            return full_path
        else:
            raise FileNotFoundError(full_path)
    else:
        return full_path

def read():
    parser = argparse.ArgumentParser(description='Feni static site generator!', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--source', help='Source directory for articles')
    parser.add_argument('--decorator', help='Decorator directory')
    parser.add_argument('--output', help='Output directory')
    parser.add_argument('--template', help='Template directory')
    parser.add_argument('--templatemap', help='Template map file')
    parser.add_argument('--config', help='Use specified configuration file \n %s' % config_help)
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    arguments = parser.parse_args()
    if arguments.config:
        configuration = read_configuration(arguments.config)
    else:
        try:
            config_file = find_configuration_file_from('.', 'feni.yaml')
        except exceptions.FileNotFoundError:
            configuration = {}
        else:
            configuration = read_configuration(config_file)
    if arguments.source:
        configuration['source'] = os.path.abspath(arguments.source)
    if arguments.decorator:
        configuration['decorator'] = os.path.abspath(arguments.decorator)
    if arguments.output:
        configuration['output'] = os.path.abspath(arguments.output)
    if arguments.template:
        configuration['template'] = os.path.abspath(arguments.template)
    else:
        if 'template' not in configuration:
            configuration['template'] = convert_path(configuration['decorator'], 'templates', True)
    if arguments.templatemap:
        configuration['templatemap'] = os.path.abspath(arguments.templatemap)
    else:
        if 'templatemap' not in configuration:
            configuration['templatemap'] = os.path.join(configuration['template'], 'templates.yaml')
    if arguments.verbose:
        logging.basicConfig(level=logging.DEBUG)
    for k in ['source', 'decorator', 'output']:
        if k not in configuration:
            raise exceptions.RequiredValueMissing(k)
    if not os.path.isdir(configuration['source']):
        raise exceptions.FileNotFoundError(configuration['source'])
    if not os.path.isdir(configuration['decorator']):
        raise exceptions.FileNotFoundError(configuration['decorator'])
    if not os.path.isdir(configuration['template']):
        raise exceptions.FileNotFoundError(configuration['template'])
    if not os.path.isfile(configuration['templatemap']):
        raise exceptions.FileNotFoundError(configuration['templatemap'])
    return configuration

config_help = '''
Feni needs the following information to function, that it can read
from command line arguments or from a configuration file.

1. A source directory. This is where Feni looks for content. Right now it only
look for .md files. Each of this file should be of format as shown below.

    main: true
    type: post
    permalink: test-post.html
    data-title: My test post
    data-subtitle: This is as test post
    ---
    ###This is the content of the post in markdown format###

Every article needs to have a header in yaml format that contain information
regarding how the final html should be generated. The first one, the 'main'
attribute denotes if the article is intended to be a whole article or if it is
part of a bigger article. If it is a whole article, this attribute should be true.
If it is a sub article, then this should be false.

The next attribute, the 'type', as the name implies, denotes the type of the article.
This attribute is used to find a template that can be used to expand this article.

'permalink' attribute is the final location of the generated html file. This should be
relative path. The generated html is placed under this path relative to the output
directory. 

'publish' attribute is used to denote wether to generate an article or not. If the
'publish' status of an article is changed to false, then that article is removed
from it's permalink location in the target folder, if it already exists.

the data- attributes are custom fields that you can define, which will be available in
your template. This can be any valid yaml value. For example, you this can be a list
where each item is information about an article. This list can be used to display a
list of articles in the target template. If you define a value 'data-article_name', then
that value will be available in the template as 'article_name' key.

2. A destination directory. This is where the generated files will be put.

3. A decorator directory. This is where all the other files, like css files, js files,
background images come from. This folder will be mostly copied as such into the output
folder. If there are files matching the enabled file handlers, then those will be passed
through them. Right now only .less files will be processed into css files.

4. A path to a templates folder that should contain all the jinja templates.

5. Path to a template configuration file. This file has the following format.

about.html:
    types:
        - aboutme
post.html:
    types:
        - post

As you can see, this just lists the template files and declares the type of
articles it can handle. By default, Feni looks for this file in the templates folder
under the name templates.yaml. But you can change that using the --templatemap
option

Feni can read this from a configuration file in yaml format.

source: articles
destination: output
decorator: design

By default, Feni looks for the this file in the current folder and folders above it.
Paths read from it will be considers as relative to the directory where it is found.
Template paths in template.yaml will be taken relative to the template directory.

'''
