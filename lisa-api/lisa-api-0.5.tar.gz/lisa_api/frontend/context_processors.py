from lisa_api import __version__


def version_processor(request):
    return {'version': __version__}
