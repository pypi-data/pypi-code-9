#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import tempfile
import os
from distutils.errors import DistutilsError

from setuptools import Command
from setuptools import package_index
from pkg_resources import Requirement


class deps_download(Command):

    user_options = [
        ('download-dir=', 'd', 'download directory (default: deps)'),
        ('dependency-type=', 't', 'dependency types (install, test or setup / default: install)'),  # noqa
    ]

    def initialize_options(self):
        self.download_dir = None
        self.dependency_type = None

    def finalize_options(self):
        self.download_dir = self.download_dir or 'deps'
        self.dependency_type = self.dependency_type or 'install'

        dependency_types = {
            'install': 'install_requires',
            'test': 'tests_require',
            'setup': 'setup_requires',
        }
        if self.dependency_type not in dependency_types:
            raise DistutilsError(
                'unknown dependency type: {dep_type}'.format(
                    dep_type=self.dependency_type,
                )
            )
        self.dependency_type = dependency_types.get(self.dependency_type)

    def run(self):
        requires = getattr(self.distribution, self.dependency_type) or []
        pypi = package_index.PackageIndex()

        if not os.path.exists(self.download_dir):
            os.mkdir(self.download_dir)

        if not os.path.isdir(self.download_dir):
            raise DistutilsError(
                'not a directory: {target}'.format(target=self.download_dir)
            )

        try:
            tmpdir = tempfile.mkdtemp(prefix='setuptools-depsutil-')
            for package_name in requires:
                spec = Requirement.parse(package_name)
                download = pypi.fetch_distribution(spec, tmpdir, source=True)

                src_filepath = download.location
                filename = os.path.basename(src_filepath)
                dst_filepath = os.path.join(self.download_dir, filename)
                shutil.copyfile(src_filepath, dst_filepath)
        finally:
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
