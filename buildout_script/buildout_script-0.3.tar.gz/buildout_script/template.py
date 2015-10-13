## Copyright (c) 2006 Nathan R. Yergler, Creative Commons

## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the "Software"),
## to deal in the Software without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Software, and to permit persons to whom the
## Software is furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
## DEALINGS IN THE SOFTWARE.

"""zc.buildout recipe to copy a template file, filling in details with 
information from the buildout run."""

import os
import stat
import logging

import zc.buildout
import pkg_resources

class Template:

    def __init__(self, buildout, name, options):

        self.buildout = buildout
        self.name = name
        self.options = options

        self._template_name = self.options.get('template', None)
        self._target_name = self.options.get('target', None)
        self._output_dir = self.options.get('output_dir', '.')

        # make sure the template was specified
        if self._template_name is None:
            logging.getLogger(self.name).error("Missing template parameter")
            raise zc.buildout.UserError("A template must be specified.")

        # see if the target was specified
        if self._target_name is None:

            # none specified, use the default name
            # (the template with the extension split off
            self._target_name = self._template_name.rsplit('.', 1)[0]

        # make sure the template exists
        self._get_template(self._template_name)

    def _get_template(self, template_name):
        """Given a template name, attempt to resolve it and return the
        contents as a String."""

        if pkg_resources.resource_exists(__name__, 'templates/%s'
                                         % template_name):

            # loading from our recipe egg
            return pkg_resources.resource_string(__name__, 'templates/%s'
                                                 % template_name)

        else:
            # see if the user specified a templates directory
            template_dir = self.options.get('template_dir',
               os.path.join(self.buildout['buildout']['directory'],
                            'templates'))
            
            if os.path.exists(os.path.join(template_dir, template_name)):
                return file(os.path.join(template_dir, template_name)).read()

        # unable to find template, throw an error
        logging.getLogger(self.name).error("Template %s does not exist." %
                                           template_name)
        raise zc.buildout.UserError(
            "The specified template, %s, does not exist" % template_name)
        
    def install(self):
        """Duplicate the template script as the specified target, applying
        Python string formatting first.  The dictionary passed to string
        formatting is a flattened dictionary of buildout options and
        the part options."""

        script_template = self._get_template(self._template_name)

        info_dict = self.buildout['buildout'].copy()
        info_dict.update(self.options)
        info_dict.update({'part-name':self.name})

        # write the new script out
        script_fn = os.path.join(self.buildout['buildout']['directory'],
                                 self._output_dir, self._target_name)
        file(script_fn, 'w').write(script_template % info_dict)

        return [script_fn]

    update = install
    
