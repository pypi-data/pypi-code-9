import filesystem


class NetworkExport(dict):
    def __init__(self, request, data):
        self.update(data)

        # Replace path with a FileSystemContainer object
        if 'path' in data:
            self['path'] = filesystem.FileSystemContainer(request, data['path'])
        if 'paths' in data:
            for i, p in enumerate(data['paths']):
                data['paths'][i] = filesystem.FileSystemContainer(request, p)


class Share(NetworkExport):
    def __init__(self, request, data):
        NetworkExport.__init__(self, request, data)


class Export(NetworkExport):
    def __init__(self, request, data):
        NetworkExport.__init__(self, request, data)


class Quota(NetworkExport):
    def __init__(self, request, data):
        NetworkExport.__init__(self, request, data)
