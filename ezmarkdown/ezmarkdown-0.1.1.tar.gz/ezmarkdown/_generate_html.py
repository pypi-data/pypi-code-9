## -*- coding: utf-8 -*-

import os
import base64
from copy import deepcopy 

from bs4 import BeautifulSoup

import requests
requests.packages.urllib3.disable_warnings()

import jinja2

import IPython.nbformat as nb
from IPython.config import Config
from IPython.nbconvert import HTMLExporter

from template import TEMPLATE_DIR


def read_notebook(fname):
    with open(fname) as obj:
        return nb.reader.read(obj)


def is_html_output(cell):
    if not cell['outputs']:
        return False
    if 'text/html' in cell['outputs'][0]['data'].keys():
        return True
    return False
 

def html_cell_output(cell):
    return cell['outputs'][0]['data']['text/html']


def all_images(html):
    soup = BeautifulSoup(html)
    imgs = soup.find_all('img')
    return list({t.attrs['src'] for t in imgs})

def is_http_url(img_path):
    img_path = img_path.lower()
    return (img_path.startswith("http://") or
            img_path.startswith("https://"))

def image_content(img_path):
    """Get the image content according to its path

    Different case:
      - PNG,JPEG: convert it to base64
      - SVG: open it and read it
      - HTTP URL: get the content via requests.get
    """
    if is_http_url(img_path):
        content = requests.get(img_path, verify=False).content
        if img_path.endswith(".svg"):
            return content
        return base64.b64encode(content)
    if img_path.endswith(".svg"):
        return open(img_path).read()
    return image_base64(img_path)

def replace_imgpath_by_content(html, image_path):
    for path in image_path:
        content = image_content(path)
        if path.endswith(".svg"):
            html = html.replace('<img alt="alt text" src="{}" />'.format(path),
                                '{}'.format(content))
        else:
            html = html.replace('src="{}"'.format(path),
                                'src="data:image/png;base64,{}"'.format(content))
    return html


def gen_html_cell(nbjson):
    """Yield index,cell for every cell with a HTML output.
    """
    for idx, cell in enumerate(nbjson['cells']):
        if is_html_output(cell):
            yield idx, cell


def put_image_content_in_cell(nbjson):
    nbjson = deepcopy(nbjson)
    for idx, cell in gen_html_cell(nbjson):
        html = html_cell_output(cell)
        image_paths = all_images(html)
        nbjson['cells'][idx]['outputs'][0]['data']['text/html'] = replace_imgpath_by_content(html, image_paths)
    return nbjson


def cell_filter(nbjson, included):
    """included: int or list of ints, for the cells to keep"""
    if isinstance(included, int):
        included = [included]
    nbjson = deepcopy(nbjson)
    cells = nbjson.pop('cells')
    nbjson['cells'] = []
    for idx in included:
        nbjson['cells'].append(cells[idx])
    return nbjson


def image_base64(imgpath):
    with open(imgpath, 'rb') as obj:
        return base64.b64encode(obj.read())


def html_conversion(nbjson, template=None):
    """
    Input template file .tpl as string.
    Provisionnally use the templates in class ezmarkdown.template.
    e.g. 'ezmarkdown.template.TEMPLATE_OUTPUT_CELLS_ONLY'.
    """
    tpl_loader = jinja2.FileSystemLoader(TEMPLATE_DIR)
    html_config = Config({"HTMLExporter": {"default_template": 'full'}})
    if template:
        html_config = Config({"HTMLExporter": {"template_file": template}})
    html_exporter = HTMLExporter(config=html_config, extra_loaders=[tpl_loader])
    html, resources = html_exporter.from_notebook_node(nbjson)
    return html


def write_html_doc(fname, output, cells, template=None):
    """
    Input cells to publish as a list of integers.
    Output file is saved in subdirectory 'saved'.
     """
    nbjson = read_notebook(fname)
    nbjson = cell_filter(nbjson, cells)
    nbjson = put_image_content_in_cell(nbjson)
    html = html_conversion(nbjson, template=template)
    if not os.path.exists('saved'):
        os.makedirs('saved')
    with open(output, 'w') as obj:
        obj.write(html.encode('utf-8'))

