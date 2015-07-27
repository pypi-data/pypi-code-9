import os.path
import sys

from zsearch_definitions import search_pb2
from zsearch_definitions import rpc_pb2

class AdminService(object):
    TIMEOUT = 600 # second
    HOST = "localhost"
    PORT = 8080

    VALID_DATASTORES = [
        "IPV4",
        "DOMAIN",
        "CERTIFICATE",
        "KEY"
    ]
    
    def __init__(self, host=None, port=None):
        host = host or self.HOST
        port = port or self.PORT
        self._service = search_pb2.early_adopter_create_AdminService_stub(host, port).__enter__()

    def shutdown(self):
        return self._service.Shutdown(rpc_pb2.Command(), self.TIMEOUT)

    def status(self):
        return self._service.Status(rpc_pb2.Command(), self.TIMEOUT)

    def statistics(self, datastore):
        ds = rpc_pb2.Command.Datastore.Value(datastore)
        return self._service.Statistics(rpc_pb2.Command(datastore=ds), self.TIMEOUT)

    def dump_certificates(self, path, incremental=False, max_records=0):
        return self._service.DumpCertificatesToJSON(rpc_pb2.Command(filepath=path, 
                incremental_dump=incremental, max_records=max_records), 3600)

    def dump_ipv4(self, path, max_records=0):
        return self._service.DumpIPv4ToJSON(rpc_pb2.Command(filepath=path,
                max_records=max_records), 3600)

    def dump_domain(self, path, max_records=0):
        return self._service.DumpDomainToJSON(rpc_pb2.Command(filepath=path, 
                max_records=max_records), 3600)

    def prune(self, datastore, scan_ids):
        if datastore not in self.VALID_DATSTORES:
            sys.stderr.write("ERROR: invalid datastore. Valid datastores: %s\n" % self.VALID_DATASTORES)
        pb_scan_ids = []
        for (port, proto, subproto, min_id) in scan_ids:
            ak = rpc_pb2.AnonymousKey(port=port,proto=proto,subproto=subproto)
            pb_scan_ids.append(rpc_pb2.MinScanId(key=ak, min_scan_id=min_id))
        ds = rpc_pb2.Command.Value(datastore)
        c = rpc_pb2.Command(min_scan_ids=pb_scan_ids, datastore=ds)
        return self._service.Status(c, self.TIMEOUT)

    def __del__(self):
        if self._service:
            self._service.__exit__(None, None, None)


