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

"""zc.buildout recipe to create a simple script with details filled in
(potentially) from the buildout.cfg."""

import os
import re
import stat
import logging

import zc.buildout
import pkg_resources


class Script:

    def __init__(self, buildout, name, options):

        self.buildout = buildout
        self.name = name
        self.options = options

        self._template_name = self.options.get('template', None)
        self._target_name = self.options.get('target', None)

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
                return open(os.path.join(template_dir, template_name)).read()

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
        # write the new script out
        script_fn = os.path.join(self.buildout['buildout']['bin-directory'],
                                 self._target_name)
        # add prefix to vars in our 'own' part, so options._sub can process them
        # borrowed from collective.recipe.template
        script_template = re.sub(r"\$\{([^:]+?)\}", r"${%s:\1}" % self.name, script_template)
        open(script_fn, 'w').write(self.options._sub(script_template, []))

        # set the permissions to allow execution
        os.chmod(script_fn, os.stat(script_fn).st_mode |
                 stat.S_IXOTH | stat.S_IXGRP | stat.S_IXUSR)

        return [script_fn]

    update = install
