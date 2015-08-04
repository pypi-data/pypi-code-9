# -*- coding: utf-8 -*-

import os
import shutil
import logging

from noseapp.core import ExtensionInstaller


__all__ = (
    'WorkSpace',
    'Permissions',
    'create_workspace_config',
)


logger = logging.getLogger(__name__)


def create_workspace_config(path, permissions=None, check_exist=True, create_if_not_exist=False):
    """
    Create configuration for auto install extension from app instance

    :param path: path to workspace
    :param permissions: permission list
    :param check_exist: check exist directory flag at create workspace
    :param create_if_not_exist: try to create directory if not exist

    :return: dict
    """
    return {
        'path': path,
        'check_exist': check_exist,
        'permissions': permissions,
        'create_if_not_exist': create_if_not_exist,
    }


class Permissions(object):
    """
    Permissions must be...
    """

    CREATE_FILE = 0
    REMOVE_FILE = 1
    CREATE_DIRECTORY = 2
    REMOVE_DIRECTORY = 3

    class Error(BaseException):
        """
        Will be raised at Illegal operation
        """

        def __init__(self, operation, path):
            msg = 'Illegal operation: {} "{}"'.format(operation, path)

            super(Permissions.Error, self).__init__(msg)


class WorkSpace(object):
    """
    Class implemented interface for work
    at file system within your application
    """

    name = 'workspace'
    config_key = 'WORKSPACE_EX'

    PERMISSIONS = tuple()

    def __init__(self, path, permissions=None, check_exist=True, create_if_not_exist=False):
        """
        :param path: entry point at file system. absolute path only.
        :type path: str
        :param permissions: list of permissions
        :type permissions: list, tuple
        :param check_exist: will be check exist path?
        :type check_exist: bool
        :param create_if_not_exist: flat to create directory if not exist
        :type create_if_not_exist: bool

        :raises: OSError
        """
        if create_if_not_exist and not os.path.exists(path):
            os.mkdir(path)

        if check_exist and not os.path.exists(path):
            raise OSError(
                'Directory "{}" does not exist'.format(
                    self.__path,
                ),
            )

        self.__path = path
        self.__permissions = permissions or tuple()

        logger.debug('Init new workspace at path "%s"', path)

    def __repr__(self):
        return '<WorkSpace: {}>'.format(self.__path)

    def __str__(self):
        return str(self.__path)

    def __unicode__(self):
        return unicode(self.__path)

    @classmethod
    def install(cls, app):
        """
        Auto install like extension from application

        :param app: instance of your application
        :type app: noseapp.app.NoseApp
        """
        options = app.config.get(cls.config_key, {})
        installer = ExtensionInstaller(cls, tuple(), options)
        app.shared_extension(cls=installer)

        return installer

    @property
    def path(self):
        """
        Path to workspace.

        :return: str
        """
        return self.__path

    @property
    def exist(self):
        """
        To return True if self path exist else False.

        :return: bool
        """
        return os.path.exists(self.__path)

    @property
    def permissions(self):
        """
        List of permissions.

        :return: tuple
        """
        permissions = list(self.PERMISSIONS)
        permissions.extend(self.__permissions)
        return tuple(set(permissions))

    def is_permission(self, permission):
        """
        Check permission in list of permission.

        :param permission: permission from Permissions class

        :return: bool
        """
        return permission in self.__permissions or permission in self.PERMISSIONS

    def is_file(self, file_name):
        """
        Check file exist.

        :param file_name: name of file

        :return: bool
        """
        logger.debug('Check exist file "%s", at path "%s"', file_name, self.__path)

        return os.path.isfile(
            self.path_to(file_name),
        )

    def is_dir(self, dir_name):
        """
        Check directory exist.

        :param dir_name: name of directory

        :return: bool
        """
        logger.debug('Check exist directory "%s" at path "%s"', dir_name, self.__path)

        return os.path.isdir(
            self.path_to(dir_name),
        )

    def path_to(self, *args):
        """
        Create path relative of self path.

        :param args: os join args

        :return: str
        """
        return os.path.realpath(
            os.path.join(
                self.__path,
                *args
            ),
        )

    def path_to_bin(self, bin_name):
        """
        Like path_to method with the exception of check is bin.

        :param bin_name: name of bin file

        :raises: LookupError
        :return: str
        """
        path = self.path_to(bin_name)

        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

        raise LookupError(
            'Bin file "{}" does not exist at path "{}"'.format(
                bin_name, self.__path
            ),
        )

    def go_to(self, dir_name):
        """
        Go to directory.
        Will be created new instance of self class on base path of dir_name.

        :param dir_name: name of directory

        :raises: OSError
        :return: WorkSpace
        """
        if self.is_dir(dir_name):
            return self.__class__(self.path_to(dir_name), permissions=self.__permissions)

        raise OSError(
            'Directory "{}" does not exist at path "{}"'.format(
                dir_name, self.__path,
            ),
        )

    def create_dir(self, dir_name):
        """
        Create new directory at self path.

        :param dir_name: name of dir

        :raises: OSError, Permissions.Error
        """
        if not self.is_permission(Permissions.CREATE_DIRECTORY):
            raise Permissions.Error('create directory', self.path_to(dir_name))

        logger.debug('Create new directory "%s" at path "%s"', dir_name, self.__path)

        dir_path = self.path_to(dir_name)

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            return self.__class__(dir_path, permissions=self.__permissions)

        raise OSError(
            'Directory "{}" already exist at path "{}"'.format(
                dir_name, self.__path
            ),
        )

    def create_dir_if_not_exist(self, dir_name):
        """
        Create new directory if not exist.

        :param dir_name: name of dir

        :return: WorkSpace
        """
        if not self.is_dir(dir_name):
            return self.create_dir(dir_name)

        return self.go_to(dir_name)

    def child_workspace(self, dir_name, permissions=None):
        """
        Create child workspace at self path.
        If not exist will be try to create.

        :param dir_name: name of directory
        :param permissions: new list of permissions for child workspace instance

        :return: WorkSpace
        """
        logger.debug('New child of workspace "%s" at path "%s"', dir_name, self.__path)

        if self.is_dir(dir_name):
            return self.__class__(
                self.path_to(dir_name),
                permissions=permissions or self.__permissions,
            )
        return self.create_dir(dir_name)

    def create_file(self, file_name, content=None):
        """
        Create new file at self path.

        :param file_name: name of file
        :param content: content will be written to file

        :raises: OSError, Permissions.Error
        :return: str
        """
        if not self.is_permission(Permissions.CREATE_FILE):
            raise Permissions.Error('create file', self.path_to(file_name))

        logger.debug('Create new file "%s" at path "%s"', file_name, self.__path)

        file_path = self.path_to(file_name)

        if not self.is_file(file_name):
            f = open(file_path, 'w')
            if content:
                f.write(content)
            f.close()
            return file_path

        raise OSError(
            'File "{}" already exist at path "{}"'.format(
                file_name, self.__path
            ),
        )

    def create_file_if_not_exist(self, file_name):
        """
        Create new file if not exist.

        :param file_name: name of file

        :return: str
        """
        if not self.is_file(file_name):
            return self.create_file(file_name)

        return self.path_to(file_name)

    def create_log_file(self, file_name):
        """
        Create file by '<file_name>.log' pattern.

        :param file_name: name of file without ext

        :return: str
        """
        file_name = '{}.log'.format(file_name)

        logger.debug('Create new log file "%s" at path "%s"', file_name, self.__path)

        return self.create_file(file_name)

    def copy_file(self, src, file_name):
        """
        Create copy of file

        :param src: absolute path to origin file
        :param file_name: name of file for copy

        :raises: Permissions.Error
        :return: str
        """
        if not self.is_permission(Permissions.CREATE_FILE):
            raise Permissions.Error('create file', self.path_to(file_name))

        file_path = self.path_to(file_name)
        shutil.copyfile(src, file_path)

        return file_path

    def copy_dir(self, src, dir_name):
        """

        :param src: absolute path to origin dir
        :param dir_name: name of dir for copy

        :raises: Permissions.Error
        :return: WorkSpace
        """
        if not self.is_permission(Permissions.CREATE_DIRECTORY):
            raise Permissions.Error('create directory', self.path_to(dir_name))

        dir_path = self.path_to(dir_name)
        shutil.copytree(src.path if isinstance(src, WorkSpace) else src, dir_path)

        return self.go_to(dir_name)

    def delete_file(self, file_name):
        """
        To delete file from self directory.

        :param file_name: name of file

        :raises: Permissions.Error
        """
        if not self.is_permission(Permissions.REMOVE_FILE):
            raise Permissions.Error('remove file', self.path_to(file_name))

        logger.debug('Delete file "%s" at path "%s"', file_name, self.__path)

        if self.is_file(file_name):
            os.remove(self.path_to(file_name))
        else:
            raise OSError(
                'File "{}" does not exist at path "{}"'.format(file_name, self.__path),
            )

    def delete_file_if_exist(self, file_name):
        """
        Delete file if exist.

        :param file_name: name of file
        """
        if self.is_file(file_name):
            self.delete_file(file_name)

    def delete_dir(self, dir_name):
        """
        Delete directory.

        :param dir_name: name of directory

        :raises: OSError
        """
        if not self.is_permission(Permissions.REMOVE_DIRECTORY):
            raise Permissions.Error('remove directory', self.__path)

        logger.debug('Delete directory "%s" at path "%s"', dir_name, self.__path)

        path_to_dir = self.path_to(dir_name)

        if os.path.exists(path_to_dir):
            shutil.rmtree(path_to_dir)
        else:
            raise OSError(
                'Directory "{}" does not exist'.format(path_to_dir),
            )

    def delete_dir_if_exist(self, dir_name):
        """
        Delete directory if exist.

        :param dir_name: name of dir
        """
        if self.is_dir(dir_name):
            self.delete_dir(dir_name)

    def delete(self):
        """
        To delete self directory.

        :raises: Permissions.Error
        """
        if not self.is_permission(Permissions.REMOVE_DIRECTORY):
            raise Permissions.Error('remove directory', self.__path)

        logger.debug('Delete workspace at path "%s"', self.__path)

        if os.path.exists(self.__path):
            shutil.rmtree(self.__path)
        else:
            raise OSError(
                'Directory "{}" does not exist'.format(self.__path),
            )

    def delete_if_exist(self):
        """
        Delete self directory if exist.
        """
        if self.exist:
            self.delete()
