# -*- coding: utf-8 -*-
# Copyright (C) 2006-2007 Søren Roug, European Environment Agency
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Contributor(s):
#

from namespaces import SVGNS
from element import Element
from draw import DrawElement

# Autogenerated
def DefinitionSrc(**args):
    args.setdefault('type', 'simple')
    return Element(qname = (SVGNS,'definition-src'), **args)

def Desc(**args):
    return Element(qname = (SVGNS,'desc'), **args)

def FontFaceFormat(**args):
    return Element(qname = (SVGNS,'font-face-format'), **args)

def FontFaceName(**args):
    return Element(qname = (SVGNS,'font-face-name'), **args)

def FontFaceSrc(**args):
    return Element(qname = (SVGNS,'font-face-src'), **args)

def FontFaceUri(**args):
    args.setdefault('type', 'simple')
    return Element(qname = (SVGNS,'font-face-uri'), **args)

def Lineargradient(**args):
    return DrawElement(qname = (SVGNS,'linearGradient'), **args)

def Radialgradient(**args):
    return DrawElement(qname = (SVGNS,'radialGradient'), **args)

def Stop(**args):
    return Element(qname = (SVGNS,'stop'), **args)

def Title(**args):
    return Element(qname = (SVGNS,'title'), **args)
