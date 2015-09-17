import bgdata
import re


class BgDataInterpolation(object):
    """
    This class will replace values following this schema:

        %(bgdata://project/dataset/version?build)

    with the bgdata path of the given data package
    """

    # compiled regexp to use in self.interpolate()
    _KEYCRE = re.compile(r"%\(bgdata://([^/)]*)/([^/)]*)/([^/)]*)\)")
    _cookie = '%'

    def __init__(self, section):
        # the Section instance that "owns" this engine
        self.section = section

    def interpolate(self, key, value):

        # short-cut
        if self._cookie not in value:
            return value

        match = self._KEYCRE.search(value)
        while match:
            project = match.group(1)
            dataset = match.group(2)
            version_and_build = match.group(3).split('?')
            version = version_and_build[0]
            build = version_and_build[1] if len(version_and_build) > 1 else bgdata.LATEST

            start, end = match.span()
            path = bgdata.get_path(project, dataset, version, build=build)

            value = value[:start] + path + value[end:]
            match = self._KEYCRE.search(value, start + len(path))

        return value