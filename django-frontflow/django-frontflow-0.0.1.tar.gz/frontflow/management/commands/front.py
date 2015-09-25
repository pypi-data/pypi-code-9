from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import subprocess
import os
from os.path import dirname
import shutil


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            self.src_dir = settings.FRONT_SRC_DIR
        except AttributeError:
            self.src_dir = 'front'

        try:
            self.build_dir = settings.FRONT_BUILD_DIR
        except AttributeError:
            raise CommandError("Missing FRONT_BUILD_DIR setting")

        if not os.path.isabs(self.src_dir):
            self.src_dir = os.path.join(
                settings.PROJECT_DIR,
                settings.PROJECT_NAME,
                self.src_dir
            )

        if not os.path.isabs(self.build_dir):
            self.build_dir = os.path.join(
                settings.PROJECT_DIR,
                settings.PROJECT_NAME,
                self.build_dir
            )

        if not os.path.isdir(self.src_dir):
            print('Front source dir: {} does not exist. Initializing.'.format(
                self.src_dir
            ))
            self.initialize_src()

        succeeded = self.run()
        if not succeeded:
            install = subprocess.call(
                ['npm install'],
                shell=True,
                stdout=self.stdout,
                stderr=self.stderr,
                cwd=self.src_dir
            )
            if install == 0:
                self.run()
            else:
                raise CommandError(
                    "Could not install grunt in: {}".format(self.src_dir)
                )

    def initialize_src(self):
        template_dir = os.path.join(
            dirname(dirname(dirname(os.path.realpath(__file__)))),
            "front-template"
        )
        try:
            os.makedirs(dirname(self.src_dir))
        except FileExistsError:
            pass
        print("Copying {} to {}".format(template_dir, self.src_dir))
        shutil.copytree(template_dir, self.src_dir)
        assert os.path.isdir(self.src_dir)

    def run(self):
        single_run = subprocess.call(
            [self.cmd()],
            shell=True,
            stdout=self.stdout,
            stderr=self.stderr,
            cwd=self.src_dir
        )
        if single_run == 0:
            subprocess.call(
                [self.cmd('watch')],
                shell=True,
                stdout=self.stdout,
                stderr=self.stderr,
                cwd=self.src_dir
            )
            return True
        else:
            return False

    def cmd(self, *args):
        cmd = 'grunt {} --buildDir={}'.format(
            ' '.join(args),
            self.build_dir
        )
        print(cmd)
        return cmd
