__author__ = 'yue'
from conn import EhcConnection

class Cluster(object):
    def __init__(self):
        self.conn = EhcConnection("ehc.datacanvas.io", 4430)

    def build_body(self, ehc_setting):
        return ehc_setting.to_full_conf()

    def create(self, ehc_setting, token):
        body = self.build_body(ehc_setting)
        return self.conn.send_request(body=body, type='ehc', url="create", token=token, verb="POST")

    def terminate(self, ehc_id, token):
        return self.conn.send_request(body={}, type='ehc', url="terminate/%s" % ehc_id, token=token)

    def describe(self, ehc_setting, token):
        body = self.build_body(ehc_setting)
        return self.conn.send_request(body=body, type='ehc', url="describe", token=token, verb="POST")
if __name__ == "__main__":
    cluster = Cluster()
    from ehc_setting import EhcConf
#     full_conf = {
#   "ehc_setting":{
#     "name":"sdk0.1",
#     "cloud_setting":{
#       "type": "qingcloud",
#       "region": "pek2"
#     },
#     "hadoop_setting":{
#       "cluster_type": "cdh5",
#       "master_type": "c4m4",
#       "slave_type": "c4m4",
#       "slave_num": 0,
#       "build-in-metastore": "true"
#   	}
#   }
# }
    full_conf = {}
    token = '.eJyrVirIyM9LVbJSMrQwM7QwNjI3tzBT0lHKTAEKleoaGBglJSYaGqaaWpqbGgDF8xJzQYqzMvPSK0tTgQKpuYmZOQgRh6rUksrSPL3k_FylWgCuDBvZ.16K66tixlJCG8dquKD6BrNXK_mc'
    conf = EhcConf(full_conf)
    conf.ehc_id = "e-84350911e597b5"
    conf.ehc_name = "sdk0.1"
    conf.cloud_type = 'qingcloud'
    conf.cloud_region = "pek2"
    conf.cluster_type = 'cdh5'
    conf.master_type = 'c4m4'
    conf.slave_type = 'c4m4'
    conf.slave_num = 0
    #ret = cluster.create(conf, token)
    #ret = cluster.terminate(ehc_id="e-84350911e597b5", token=token)
    ret = cluster.describe(conf, token=token)

    print ret