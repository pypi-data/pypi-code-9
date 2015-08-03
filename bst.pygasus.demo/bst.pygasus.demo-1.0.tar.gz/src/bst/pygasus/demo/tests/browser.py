import unittest
from splinter import Browser


LOCALHOST = 'http://localhost:8080/mainapp'

MODULS = ('index',
          'bootstrap',
          'scaffolding/model/Card.js',
          'scaffolding/form/Card.js',
          'scaffolding/grid/Card.js',
          'scaffolding/editgrid/Card.js',
          'scaffolding/display/Card.js',
          'scaffolding/store/Card.js',
          'scaffolding/bufferedstore/Card.js',
          'fanstatic/extjs/ext-all.js',
          'i18n/bst.pygasus.demo',
          )


class BrowserTest(unittest.TestCase):

    def response_check(self):
        with Browser() as browser:
            for mod in MODULS:
                browser.visit('%s/%s' % (LOCALHOST, mod))
