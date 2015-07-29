__author__ = 'yue'
import json


class EhcConf:
    def __init__(self, full_conf=None):
        if full_conf:
            ehc_setting = full_conf.get('ehc_setting', None)
            if ehc_setting:
                self.ehc_id = ehc_setting.get('id', None)
                self.ehc_name = ehc_setting.get('name', "")
                self.vpc_id = ehc_setting.get('vpc_id', None)
                self.ehc_status = ehc_setting.get('status', None)
                cloud_setting = ehc_setting.get('cloud_setting', None)
                self.cloud_setting = json.dumps(cloud_setting)
                if cloud_setting:
                    self.cloud_type = cloud_setting.get('type', None)
                    self.cloud_region = cloud_setting.get('region', None)
                #self.ehc_package = ehc_setting['ehc_package']

                hadoop_setting = ehc_setting.get('hadoop_setting', None)
                self.hadoop_setting = json.dumps(hadoop_setting)
                if hadoop_setting:
                    self.cluster_type = hadoop_setting.get('cluster_type', 'cdh5')
                    self.master_type = hadoop_setting.get('master_type', 'c4m4')
                    self.slave_type = hadoop_setting.get('slave_type', 'c4m4')
                    self.slave_num = hadoop_setting.get('slave_num', '0')

            command_setting = full_conf.get('command_setting', None)
            if command_setting:
                self.command_id = command_setting.get('id', None)
                self.command_name = command_setting.get('name', None)
                self.command_description = command_setting.get('description', None)
                self.command_type = command_setting.get('type', None)
                self.command_conf = command_setting.get('conf', None)
        else:
            self.ehc_id = None
            self.ehc_name = None
            self.ehc_status = None
            self.cloud_region = None
            self.cloud_type = None
            self.vpc_id = None
            self.cluster_type = None
            self.master_type = None
            self.slave_num = None
            self.slave_type = None


    def to_full_conf(self):
        full_conf = {}
        ehc_setting = {}
        if self.ehc_id:
            ehc_setting['id'] = self.ehc_id
        if self.ehc_name:
            ehc_setting['name'] = self.ehc_name
        if self.vpc_id:
            ehc_setting['vpc_id'] = self.vpc_id
        if self.ehc_status:
            ehc_setting['status'] = self.ehc_status
        ehc_setting['cloud_setting'] = {}
        if self.cloud_type:
            ehc_setting['cloud_setting']['type'] = self.cloud_type
        if self.cloud_region:
            ehc_setting['cloud_setting']['region'] = self.cloud_region

        ehc_setting['hadoop_setting'] = {}
        if self.cloud_type:
            ehc_setting['hadoop_setting']['cluster_type'] = self.cloud_type
        if self.master_type:
            ehc_setting['hadoop_setting']['master_type'] = self.master_type
        if self.slave_type:
            ehc_setting['hadoop_setting']['slave_type'] = self.slave_type
        if self.slave_num:
            ehc_setting['hadoop_setting']['slave_num'] = self.slave_num
        if ehc_setting:
            full_conf['ehc_setting'] = ehc_setting
        return full_conf

    def load_dict(self, **entries):
        self.__dict__.update(entries)

    def to_dict(self):
        d = {}
        for name, value in vars(self).items():
            d[name] = value
        return d

    def get_ehc_filter(self):
        filter = {}
        if self.ehc_id:
            filter['id'] = self.ehc_id
        elif self.user_id:
            filter['user_id'] = self.user_id
        elif self.ehc_status:
            filter['status'] = self.ehc_status
        return filter

    def set_ehc_id(self, ehc_id):
        self.ehc_id = ehc_id

    def set_user_id(self, user_id):
        self.user_id = user_id
