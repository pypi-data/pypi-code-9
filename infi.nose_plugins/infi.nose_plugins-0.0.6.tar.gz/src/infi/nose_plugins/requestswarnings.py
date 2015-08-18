from nose.plugins import Plugin


class RequestsSuppressWarningPlugin(Plugin):  # pragma: no cover
    """suppress requests warnings"""
    name = 'requests-no-warning'

    def help(self):
        return 'suppress requests warnings'

    def startContext(self, context):
        import requests
        requests.packages.urllib3.disable_warnings()
    
    def stopContext(self, context):
        pass
