__author__ = 'jkingsbury'


def endpoint(e):
    """
    Get the URI path for common Isilon API endpoints
    Available endpoints:
        session
        nfs
        smb
        namespace
        quota
    :param e: endpoint name
    :return: URI
    """
    endpoints = {
        "session": '/session/1/session',
        "nfs": '/platform/1/protocols/nfs/exports',
        "smb": '/platform/1/protocols/smb/shares',
        "namespace": '/namespace/',
        "quota": '/platform/1/quota/quotas'
    }
    return endpoints[e]
