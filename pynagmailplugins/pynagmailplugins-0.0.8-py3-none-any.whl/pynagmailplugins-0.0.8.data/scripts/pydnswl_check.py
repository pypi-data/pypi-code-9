#!python
"""
You can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 2
of the License.

Copyright Andrea Briganti a.k.a 'Kbyte'
"""

import nagiosplugin
import socket

class DnswlStatus(nagiosplugin.Resource):
    name = 'DNSWL'

    def probe(self):
        try:
            socket.gethostbyname('2.0.0.127.list.dnswl.org')
        except OSError as e:
            return [nagiosplugin.Metric('dnswl', (False, str(e)), context='dnswl')]

        return [nagiosplugin.Metric('dnswl', (True, None), context='dnswl')]


class DnswlContext(nagiosplugin.Context):
    def __init__(self):
        super(DnswlContext, self).__init__('dnswl')

    def evaluate(self, metric, resource):
        value, output = metric.value
        if value:
            return self.result_cls(nagiosplugin.Ok, metric=metric)
        else:
            return self.result_cls(nagiosplugin.Critical, metric=metric, hint='error: %s' % output)


@nagiosplugin.guarded
def main():
    check = nagiosplugin.Check(
        DnswlStatus(),
        DnswlContext())

    check.main()


if __name__ == '__main__':
    main()
