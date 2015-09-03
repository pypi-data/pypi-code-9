
from setuptools import setup
from setuptools import find_packages

print(find_packages())

setup(
    name                    = 'ngl_utils',
    version                 = '1.3.1',
    description             = ( 'ngl_utils converting/generate code utilities for embedded NGL library'
                                'ngluic - console converter QtDesigner *.ui files'
                                'nglfec - ui convertor/generator util for fonts'
                                'nglfed - ui ngl font editor' ),
    author                  = 'Vladislav Kamenev',
    author_email            = 'wladkam@mail.com',
    url                     = '',
    package_data            = { 'ngl_utils': ['templates/*.ntp'],
                                'ngl_utils.nfont': ['qtres/*.ui'] },
    packages                = find_packages(),
    
    entry_points = {
        'console_scripts': [ 'ngluic = ngl_utils.ngluic : main',
                             'nglfcn = ngl_utils.nfont.converterwidget : nfontConverterGUIStart',
                             'nglfed = ngl_utils.nfont.editwidget : nfontEditGUIStart' ] },

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3'
        ],
)