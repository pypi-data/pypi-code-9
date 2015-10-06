# Copyright © 2015 STRG.AT GmbH, Vienna, Austria
#
# This file is part of the The SCORE Framework.
#
# The SCORE Framework and all its parts are free software: you can redistribute
# them and/or modify them under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation which is in the
# file named COPYING.LESSER.txt.
#
# The SCORE Framework and all its parts are distributed without any WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. For more details see the GNU Lesser General Public
# License.
#
# If you have not received a copy of the GNU Lesser General Public License see
# http://www.gnu.org/licenses/.
#
# The License-Agreement realised between you as Licensee and STRG.AT GmbH as
# Licenser including the issue of its valid conclusion and its pre- and
# post-contractual effects is governed by the laws of Austria. Any disputes
# concerning this License-Agreement including the issue of its valid conclusion
# and its pre- and post-contractual effects are exclusively decided by the
# competent court, in whose district STRG.AT GmbH has its registered seat, at
# the discretion of STRG.AT GmbH also the competent court, in whose district the
# Licensee has his registered seat, an establishment or assets.

from . import css
from pyramid.view import view_config
from pyramid.settings import asbool
from jinja2 import Markup
import io
import os
import subprocess
import strg.tpl as tpl
import xml.etree.ElementTree as ET

import logging
log = logging.getLogger(__name__)


def rootdir(request):
    """
    Returns the root directory of all icon files.
    """
    return os.path.join(tpl.rootdir(request), 'icon')


def pngresponse(request, png):
    """
    Returns a pyramid response object containing *png* bytes.
    """
    request.response.content_type = 'image/png'
    request.response.body = png
    return request.response


def svgresponse(request, svg):
    """
    Returns a pyramid response object containing an *svg* string.
    """
    request.response.content_encoding = 'UTF-8'
    request.response.content_type = 'image/svg+xml; charset=UTF-8'
    request.response.text = svg
    return request.response


def svg2pngresponse(request, svg):
    """
    Returns a pyramid response containing a png image from given *svg* string.
    """
    cmd = 'convert'
    try:
        cmd = request.registry.settings['cmd.%s' % cmd]
    except KeyError:
        pass
    args = [request, cmd, '-background', 'none', '-', '-']
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.stdin.write(svg.encode('UTF-8'))
    png = process.stdout.read()
    return pngresponse(request, png)


def svgfile2pngresponse(request, svg):
    """
    Returns a pyramid response containing a png image from given *svg* file.
    """
    try:
        cachedir = request.registry.settings['icons.cachedir']
    except KeyError:
        return svg2pngresponse(request, open(svg, 'r').read())
    pngpath = os.path.join(cachedir, os.path.basename(svg)[:-3] + 'png')
    if not os.path.isfile(pngpath) or os.path.getmtime(pngpath) < os.path.getmtime(svg):
        os.makedirs(os.path.dirname(pngpath), exist_ok=True)
        cmd = 'convert'
        try:
            cmd = request.registry.settings['cmd.%s' % cmd]
        except KeyError:
            pass
        subprocess.check_call(cmd, '-background', 'none', svg, pngpath)
    return pngresponse(request, open(pngpath, 'rb').read())


@view_config(route_name='icons/single/svg')
def icon_single_svg(request):
    path = os.path.join(rootdir(request), request.matchdict['path'])
    svg = open(path).read()
    return svgresponse(request, svg)


@view_config(route_name='icons/single/png')
def icon_single_png(request):
    path = request.matchdict['path']
    svgpath = os.path.join(rootdir(request), path[:-3] + 'svg')
    return svgfile2pngresponse(request, svgpath)


@view_config(route_name='icons/combined/svg')
def icon_multi_svg(request):
    isfile, svg = multisvg(request)
    if isfile:
        svg = open(svg, 'r').read()
    return svgresponse(request, svg)


@view_config(route_name='icons/combined/png')
def icon_multi_png(request):
    isfile, svg = multisvg(request)
    if isfile:
        return svgfile2pngresponse(request, svg)
    else:
        return svg2pngresponse(request, svg)


def combining(request):
    try:
        return asbool(request.registry.settings['icons.combine'])
    except KeyError:
        return True


def files(request):
    """
    Provides a list of all svg files found in the css root folder.
    """
    root = rootdir(request)
    svgfiles = []
    for parent, _, files in os.walk(root):
        for file in files:
            if file.endswith('.svg'):
                path = os.path.relpath(os.path.join(parent, file), root)
                svgfiles.append(path)
    return svgfiles


def path2cssclass(filename):
    """
    Converts a file path (that must end with ``.svg`` or ``.png``) to a
    css class.
    """
    return filename.replace('/', '-')[:-4]


def multisvg(request):
    """
    Provides all icons combined as a single svg file or string. The return
    value is a 2-tuple where the first value is a boolean. If this value is
    `True`, the second value is the path to an svg file, otherwise the second
    value is an svg image as a string.
    """
    root = rootdir(request)
    paths = files(request)
    if 'icons.cachedir' not in request.registry.settings:
        with io.StringIO() as buf:
            _genmultisvg(request, paths, buf)
            return (False, buf.getvalue())
    svgfile = os.path.join(request.registry.settings['icons.cachedir'], '_combined.svg')
    try:
        svgmtime = os.path.getmtime(svgfile)
        for file in paths:
            if os.path.getmtime(os.path.join(root, file)) >= svgmtime:
                with open(svgfile, 'w') as f:
                    _genmultisvg(request, paths, f)
                break
    except FileNotFoundError:
        os.makedirs(os.path.dirname(svgfile), exist_ok=True)
        with open(svgfile, 'w') as f:
            _genmultisvg(request, paths, f)
    return (True, svgfile)


def _genmultisvg(request, files, file):
    """
    Generates an svg image sprite containing all given files.
    """
    result = ET.Element('svg', {
        'version': '1.1',
    })
    width = 0
    height = 0
    for i, path in enumerate(files(request)):
        svgfile = os.path.join(rootdir(request), path)
        xml = ET.parse(svgfile)
        root = xml.getroot()
        group = ET.SubElement(result, 'g', {
            'class': path2cssclass(path),
            'transform': 'translate(%d)' % width,
        })
        for node in root:
            group.append(node)
        w, h = _wh(xml)
        width += w
        height = max(height, h)
    result.set('width', str(width))
    result.set('height', str(height))
    result = ET.ElementTree(result)
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    file.write(
        '<?xml version="1.0" standalone="no"?>\n'\
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" \n'\
        '  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
    )
    result.write(file, encoding='unicode', xml_declaration=False)


def _wh(xml):
    """
    Reads the width and height of an xml node containing an svg image.
    """
    root = xml.getroot()
    width, height = root.attrib['width'], root.attrib['height']
    width = int(width.replace('px', ''))
    height = int(height.replace('px', ''))
    return width, height


def css_combined(request):
    """
    Generates css styles for the combined icons sprite.
    """
    result = '.icon{'
    result += 'display:inline-block;'
    result += 'background:url(%s)no-repeat;' % request.route_url('icons/combined/png')
    result += 'background-image:url(%s),none}\n' % request.route_url('icons/combined/svg')
    offset = 0
    for i, path in enumerate(files(request)):
        cls = path2cssclass(path)
        xml = ET.parse(os.path.join(rootdir(request), path))
        width, height = _wh(xml)
        result += '.icon-%s{' % cls
        result += 'background-position:%dpx 0;' % offset
        result += 'width:%dpx;height:%dpx}\n' % (width, height)
        offset -= width
    return result


def css_single(request):
    """
    Generates css styles for the icons.
    """
    result = '.icon{display:inline-block}\n'
    for path in files(request):
        cls = path2cssclass(path)
        xml = ET.parse(os.path.join(rootdir(request), path))
        width, height = _wh(xml)
        result += '.icon-%s{' % cls
        result += 'background:url(%s)no-repeat;' % request.route_url('icons/single/png', path=path[:-3] + 'png')
        result += 'background-image:url(%s),none;' % request.route_url('icons/single/svg', path=path)
        result += 'width:%dpx;height:%dpx}\n' % (width, height)
    return result


@css.virtcss('icons.css')
def css(request):
    if combining(request):
        return css_combined(request)
    return css_single(request)


class TagGenerator:
    """
    This is a helper class for use in jinja-templates. You can use it to
    generate an html tag displaying an image. The following line … ::

        {{ icon('form/success') }}

    … will render as::

        <span class="icon icon-form-success"></span>

    This tag will have all required styles associated to render as an
    inline-block element with correct width and height, having the icon as
    background image.
    """

    def __init__(self, request):
        self.request = request

    def __call__(self, path):
        """
        Renders the requested icon as jinja-Markup. Note that the *path* must
        not contain any extension.
        """
        return Markup('<span class="icon icon-%s"></span>' % path2cssclass(path + '.svg'))

