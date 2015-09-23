import logging
import sys
from functools import partial
from io import BytesIO

from docker import Client
from docker.utils import kwargs_from_env

from .container import Container
from .parser import MissionFilesCompiler
from .utils import TemporaryDirectory

PY3 = sys.version_info[0] == 3
if PY3:
    basestring = str


class DockerClient(object):
    PREFIX_IMAGE = 'checkio'
    LINUX_SOCKET = 'unix://var/run/docker.sock'

    def __init__(self, connection_params=None):
        if connection_params is None:
            connection_params = kwargs_from_env(assert_hostname=False)
            if 'base_url' not in connection_params:
                connection_params['base_url'] = self.LINUX_SOCKET
        self._client = Client(**connection_params)

    def __getattr__(self, attr):
        return getattr(self._client, attr)

    def get_image_name(self, mission):
        return "{}/{}".format(self.PREFIX_IMAGE, mission)

    def run(self, mission, command, volumes=None, **kwargs):
        container = self.create_container(mission, command, volumes=volumes, **kwargs)
        container.start()
        return container

    def create_container(self, mission, command, volumes=None, **kwargs):
        logging.debug("Create container: {}".format(command))

        if volumes is not None:
            if 'host_config' not in kwargs:
                kwargs['host_config'] = {}
            kwargs['volumes'] = list(volumes.keys())
            kwargs['host_config']['Binds'] = ['{}:{}:ro'.format(t, f) for f, t in volumes.items()]

        container = self._client.create_container(
            image=self.get_image_name(mission),
            command=command,
            **kwargs
        )
        return Container(container=container, connection=self._client)

    def build(self, name_image, path=None, dockerfile_content=None):
        """
        Build new docker image
        :param name_image: name of new docker image
        :param path: path to dir with Dockerfile
        :param dockerfile_content: content of Dockerfile

        Must be passed one of this args: path or dockerfile_content
        :return: None
        """
        logging.debug("Build: {}, {}".format(name_image, path))

        file_obj = None
        if dockerfile_content is not None:
            file_obj = BytesIO(dockerfile_content.encode('utf-8'))

        build = partial(self._client.build, path=path, fileobj=file_obj, tag=name_image, rm=True,
                        forcerm=True, pull=True, encoding='utf-8')
        output = [line for line in build()]
        if output:
            logging.info(output)
        return name_image

    def build_mission(self, mission, repository=None, source_path=None, compiled_path=None):
        """
        Build new docker image
        :param mission: mission slug
        :param repository: repository of CheckiO mission
        :param compiled_path: path for store compiled mission
        :return:
        """
        assert repository or source_path

        image_name = self.get_image_name(mission)
        with TemporaryDirectory() as temp_path:
            if compiled_path is None:
                compiled_path = temp_path

            mission_source = MissionFilesCompiler(compiled_path)
            mission_source.compile(source_path=source_path, repository=repository)
            self.build(name_image=image_name, path=mission_source.path_verification)
