import socket
import os.path
import sys

from zsearch_definitions import search_pb2
from zsearch_definitions import rpc_pb2
from zsearch_definitions import hoststore_pb2 
from zsearch_definitions.protocols import Protocol, Subprotocol

class AdminService(object):
    TIMEOUT = 60*60*2 # second
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

    @property
    def service(self):
        return self._service

    def shutdown(self):
        return self._service.Shutdown(rpc_pb2.Command(), self.TIMEOUT)

    def status(self):
        return self._service.Status(rpc_pb2.Command(), self.TIMEOUT)

    def statistics(self, datastore):
        ds = rpc_pb2.Command.Datastore.Value(datastore)
        return self._service.Statistics(rpc_pb2.Command(datastore=ds), self.TIMEOUT)

    def dump_certificates(self, path, incremental=False, max_records=0):
        return self._service.DumpCertificatesToJSON(rpc_pb2.Command(filepath=path,
                incremental_dump=incremental, max_records=max_records), 60*60)

    def dump_ipv4(self, path, max_records=0):
        return self._service.DumpIPv4ToJSON(rpc_pb2.Command(filepath=path,
                max_records=max_records), 4*60*60)

    def dump_domain(self, path, max_records=0):
        return self._service.DumpDomainToJSON(rpc_pb2.Command(filepath=path,
                max_records=max_records), 60*60)

    def _make_prune_cmd(self, min_scan_ids):
        cmd = rpc_pb2.Command()
        for (host_port, pretty_protocol, pretty_subprotocol), min_scan_id in \
                min_scan_ids.iteritems():
            network_port = socket.htons(host_port)
            protocol = Protocol.from_pretty_name(pretty_protocol)
            subprotocol = Protocol.from_pretty_name(pretty_subprotocol)
            ak = hoststore_pb2.AnonymousKey(
                port=network_port,
                protocol=protocol.value, subprotocol=subprotocol.value,
            )
            min_id_obj = cmd.min_scan_ids.add()
            min_id_obj.key.CopyFrom(ak)
            min_id_obj.min_scan_id = min_scan_id
        return cmd

    def prune_domain(self, min_scan_ids):
        cmd = self._make_prune_cmd(min_scan_ids)
        return self._service.PruneDomain(cmd, self.TIMEOUT)

    def prune_ipv4(self, min_scan_ids):
        '''min_scan_ids is a dictionary of the tuple
        (host_order_port, pretty_protocol_name, pretty_subprotocol_name):min_id
        '''
        cmd = self._make_prune_cmd(min_scan_ids)
        return self._service.PruneIPv4(cmd, self.TIMEOUT)

    def __del__(self):
        if self._service:
            self._service.__exit__(None, None, None)
