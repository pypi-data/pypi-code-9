# -*- coding: utf-8 -*-

import os
from unittest import TestCase

from noseapp_workspace import WorkSpace
from noseapp_workspace import Permissions


BASE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
    ),
)


def create_ws_path(case):
    return os.path.join(
        BASE_PATH,
        case.__class__.__name__.lower(),
    )


class BaseTests(TestCase):

    def setUp(self):
        self.ws = WorkSpace(
            create_ws_path(self),
            permissions=(
                Permissions.CREATE_FILE,
                Permissions.REMOVE_FILE,
                Permissions.CREATE_DIRECTORY,
                Permissions.REMOVE_DIRECTORY,
            ),
            create_if_not_exist=True,
        )

    def tearDown(self):
        self.ws.delete()

    def test_file_not_exist(self):
        file_name = 'file_not_exist.txt'
        self.assertFalse(self.ws.is_file(file_name))

    def test_dir_not_exist(self):
        dir_name = 'dir_not_exist'
        self.assertFalse(self.ws.is_dir(dir_name))

    def test_create_and_delete_file(self):
        file_name = 'test_create_file.txt'
        self.assertRaises(OSError, self.ws.delete_file, file_name)

        self.ws.create_file(file_name)
        self.assertTrue(self.ws.is_file(file_name))

        self.ws.delete_file(file_name)
        self.assertFalse(self.ws.is_file(file_name))

    def test_create_and_delete_dir(self):
        dir_name = 'test_create_dir'
        self.ws.create_dir(dir_name)
        self.assertTrue(self.ws.is_dir(dir_name))

        self.ws.delete_dir(dir_name)
        self.assertFalse(self.ws.is_dir(dir_name))

    def test_create_and_delete_log_file(self):
        file_name = 'test_log_file'
        full_file_name = lambda name: name + '.log'
        self.ws.create_log_file(file_name)
        self.assertTrue(self.ws.is_file(full_file_name(file_name)))

        self.ws.delete_file(full_file_name(file_name))
        self.assertFalse(self.ws.is_file(full_file_name(file_name)))

    def test_child_of_workspace(self):
        dir_name = 'new_workspace'
        self.assertFalse(self.ws.is_dir(dir_name))

        new_ws = self.ws.child_of_workspace(dir_name)
        self.assertTrue(self.ws.is_dir(dir_name))
        self.assertIsInstance(new_ws, WorkSpace)

        new_ws = self.ws.child_of_workspace(dir_name)
        self.assertIsInstance(new_ws, WorkSpace)

    def test_permission_property(self):
        permissions = (
            Permissions.CREATE_FILE,
            Permissions.REMOVE_FILE,
            Permissions.CREATE_DIRECTORY,
            Permissions.REMOVE_DIRECTORY,
        )
        self.assertEqual(permissions, self.ws.permissions)

    def test_is_permission(self):
        self.assertFalse(self.ws.is_permission(100))
        self.assertTrue(self.ws.is_permission(Permissions.CREATE_FILE))

    def test_go_to(self):
        dir_name = 'test_go_to'
        self.assertRaises(OSError, self.ws.go_to, dir_name)

        self.ws.create_dir(dir_name)
        cd = self.ws.go_to(dir_name)
        self.assertIsInstance(cd, WorkSpace)

    def test_go_to_bin(self):
        bin_name = 'test_bin_name'
        self.assertRaises(LookupError, self.ws.path_to_bin, bin_name)
        # TODO: test of real bin

    def test_create_file_if_not_exist(self):
        file_name = 'create_file_if_not_exist.txt'
        self.assertFalse(self.ws.is_file(file_name))

        self.ws.create_file_if_not_exist(file_name)
        self.assertTrue(self.ws.is_file(file_name))

        self.ws.create_file_if_not_exist(file_name)

    def test_create_dir_if_not_exist(self):
        dir_name = 'create_dir_if_not_exist.txt'
        self.assertFalse(self.ws.is_dir(dir_name))

        self.ws.create_dir_if_not_exist(dir_name)
        self.assertTrue(self.ws.is_dir(dir_name))

        self.ws.create_dir_if_not_exist(dir_name)

    def test_copy_file(self):
        orig_file_name = 'test_copy_file.txt'
        copy_file_name = 'test_copy_file2.txt'

        self.ws.create_file(orig_file_name)
        self.assertTrue(self.ws.is_file(orig_file_name))

        self.ws.copy_file(self.ws.path_to(orig_file_name), copy_file_name)
        self.assertTrue(self.ws.is_file(copy_file_name))

    def test_copy_dir(self):
        orig_dir_name = 'test_copy_dir'
        copy_dir_name = 'test_copy_dir2'

        self.ws.create_dir(orig_dir_name)
        self.assertTrue(self.ws.is_dir(orig_dir_name))

        self.ws.copy_dir(self.ws.path_to(orig_dir_name), copy_dir_name)
        self.assertTrue(self.ws.is_dir(copy_dir_name))
