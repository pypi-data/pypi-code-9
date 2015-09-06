#! /usr/bin/env python
# coding: utf-8

from __future__ import print_function

import sys
import os
from textwrap import dedent

name_space = 'ruamel'
package_name = 'venvgtk'
full_package_name = name_space + '.' + package_name

exclude_files = [
    'setup.py',
]

version_str = "0.4.1"

if __name__ == '__main__':
    # put here so setup.py can be imported more easily
    from setuptools import setup, find_packages, Extension
    from setuptools.command import install_lib


class MyInstallLib(install_lib.install_lib):
    def install(self):
        fpp = full_package_name.split('.')  # full package path
        full_exclude_files = [os.path.join(*(fpp + [x]))
                              for x in exclude_files]
        alt_files = []
        outfiles = install_lib.install_lib.install(self)
        for x in outfiles:
            for full_exclude_file in full_exclude_files:
                if full_exclude_file in x:
                    os.remove(x)
                    break
            else:
                alt_files.append(x)
        return alt_files


def main():
    install_requires = [
        'ruamel.base>=1.0',
    ]
    # if sys.version_info < (3, 4):
    #     install_requires.append("")
    packages = [full_package_name] + [(full_package_name + '.' + x) for x
                                      in find_packages(exclude=['tests'])]
    setup(
        name=full_package_name,
        version=version_str,
        description="link gtk (py27) / gi (py3.4) modules into virtualenv for "
        "tox/virtualenv on Debian derived systems",
        install_requires=install_requires,
        long_description=open(__file__.replace('setup.py', 'README.rst')).read(),
        url='https://bitbucket.org/ruamel/' + package_name,
        author='Anthon van der Neut',
        author_email='a.van.der.neut@ruamel.eu',
        license="MIT license",
        package_dir={full_package_name: '.'},
        namespace_packages=[name_space],
        packages=packages,
        cmdclass={'install_lib': MyInstallLib},
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
        ]
    )


if __name__ == '__main__':
    verbose = 1
    if not '--version' in sys.argv and \
       not 'check' in sys.argv and \
       not 'sdist' in sys.argv and \
       not sys.executable.startswith('/usr/bin/python'):
        import subprocess
        imps = []
        try:
            if sys.version_info < (3,):
                import gtk
        except ImportError:
            imps.append((
                [
                    'pygtk.pth',
                    'pygtk.py',
                    'gtk-2.0',
                    'gobject',
                    'glib',
                    'cairo',
                ],
                 'import os, pygtk; print(os.path.dirname(pygtk.__file__))'))
        try:
            import gi
        except ImportError:
            imps.append((
                ['gi',],
                'import os, gi; print(os.path.dirname(os.path.dirname(gi.__file__)))'))
        for dirs, imp in imps:
            src_dir = subprocess.check_output([
                '/usr/bin/{}'.format(os.path.basename(sys.executable)),
                '-c',
                imp,
            ]).strip().decode('unicode_escape')
            for x in sys.path:
                if not x.strip():
                    continue
                if os.path.isfile(x): # zipfile e.g.
                    continue
                if os.path.islink(x):
                    continue
                dst_base = x
            if verbose > 0:
                print('src_dir', src_dir)
                print('dst_dir', dst_base)
            for d in dirs:
                src = os.path.join(src_dir, d)
                dst = os.path.join(dst_base, d)
                if verbose > 1:
                    print('src', src)
                    print('dst', dst)
                if os.path.exists(src) and not os.path.exists(dst):
                    if verbose > 0:
                        print('linking', d, 'to', dst_base)
                    os.symlink(src, dst)
    if len(sys.argv) > 1:
        main()
