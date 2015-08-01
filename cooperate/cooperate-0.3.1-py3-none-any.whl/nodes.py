import asyncio

__all__ = ['Node', 'DockerNode', 'LocalNode', 'LxcNode', 'SSHNode']


class Result:

    def __init__(self, code=None, stdout=None, stderr=None, error=None):
        self.code = code
        self.stdout = stdout
        self.stderr = stderr
        self.error = error

    @property
    def succeeded(self):
        return self.code == 0 or not self.error

    def __repr__(self):
        return '<Result(code=%s, stdout...)>' % self.code


class Node:

    @asyncio.coroutine
    def run(self, command):
        raise NotImplemented


class DockerNode(Node):

    def __init__(self, container):
        self.container = container

    @property
    def name(self):
        return '%s' % self.container

    @asyncio.coroutine
    def run(self, command):
        args = {'stdout': asyncio.subprocess.PIPE,
                'stderr': asyncio.subprocess.PIPE}
        if isinstance(command, (list, tuple)):
            args = ['docker', 'exec', self.container]
            args.extend(command)
            create = asyncio.create_subprocess_exec(*command, **args)
        else:
            cmd = 'docker exec %s' % (self.container, command)
            create = asyncio.create_subprocess_shell(cmd, **args)
        proc = yield from create
        stdout, stderr = yield from proc.communicate()
        return Result(proc.returncode,
                      stdout=stdout.decode('utf-8').rstrip('\r\n'),
                      stderr=stderr.decode('utf-8').rstrip('\r\n'))


class LocalNode(Node):

    @property
    def name(self):
        return 'local'

    @asyncio.coroutine
    def run(self, command):
        args = {'stdout': asyncio.subprocess.PIPE,
                'stderr': asyncio.subprocess.PIPE}
        if isinstance(command, (list, tuple)):
            create = asyncio.create_subprocess_exec(*command, **args)
        else:
            create = asyncio.create_subprocess_shell(command, **args)
        proc = yield from create
        stdout, stderr = yield from proc.communicate()
        return Result(proc.returncode,
                      stdout=stdout.decode('utf-8').rstrip('\r\n'),
                      stderr=stderr.decode('utf-8').rstrip('\r\n'))


class LxcNode(Node):

    def __init__(self, container):
        self.container = container

    @property
    def name(self):
        return '%s' % self.container

    @asyncio.coroutine
    def run(self, command):
        args = {'stdout': asyncio.subprocess.PIPE,
                'stderr': asyncio.subprocess.PIPE}
        if isinstance(command, (list, tuple)):
            args = ['lxc-attach', '--name', self.container, '--']
            args.extend(command)
            create = asyncio.create_subprocess_exec(*command, **args)
        else:
            cmd = 'lxc-attach --name %s -- %s' % (self.container, command)
            create = asyncio.create_subprocess_shell(cmd, **args)
        proc = yield from create
        stdout, stderr = yield from proc.communicate()
        return Result(proc.returncode,
                      stdout=stdout.decode('utf-8').rstrip('\r\n'),
                      stderr=stderr.decode('utf-8').rstrip('\r\n'))


class SSHNode(Node):

    def __init__(self, connect):
        self.connect = connect

    @property
    def name(self):
        return '%s' % self.connect

    @asyncio.coroutine
    def run(self, command):
        args = ['ssh', self.connect]
        if isinstance(command, (list, tuple)):
            args.extend(command)
        else:
            args.append(command)
        create = asyncio.create_subprocess_exec(*args,
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)
        proc = yield from create
        stdout, stderr = yield from proc.communicate()
        return Result(proc.returncode,
                      stdout=stdout.decode('utf-8').rstrip('\r\n'),
                      stderr=stderr.decode('utf-8').rstrip('\r\n'))
