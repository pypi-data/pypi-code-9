from ucloudclient import uexceptions
from ucloudclient.utils import base


class UnetManager(base.Manager):
    '''
    net manager class
    '''

    def eip_create(self, region, operator_name, bandwidth, charge_type=None,
                   quantity=None):
        '''
        create an eip
        :param region:
        :param operator_name:
        :param bandwidth:
        :param charge_type:
        :param quantity:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'AllocateEIP'
        body['OperatorName'] = operator_name
        body['Bandwidth'] = bandwidth
        if charge_type:
            body['ChargeType'] = charge_type
        if quantity:
            body['Quantity'] = quantity

        return self._get(body)

    def eip_list(self, region, offset=None, limit=None):
        '''
        query eip in given id
        :param region:
        :param uhostids:
        :param offset:
        :param limit:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = "DescribeEIP"
        if offset:
            body['Offset'] = offset
        if limit:
            body['Limit'] = limit
        return self._get(body)

    def eip_get(self, region, eipid):
        '''
        query eip in given id
        :param region:
        :param uhostids:
        :param offset:
        :param limit:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = "DescribeEIP"
        body['EIPId'] = eipid

        return self._get(body)

    def eip_update(self, region, eipid, name=None, tag=None, remark=None):
        '''
        update an eip
        :param region:
        :param eipid:
        :param name:
        :param tag:
        :param remark:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'UpdateEIPAttribute'
        body['EIPId'] = eipid
        if not name and not tag and remark:
            raise uexceptions.BadParameters
        if name:
            body['Name'] = name
        if tag:
            body['Tag'] = tag
        if remark:
            body['Remark'] = tag

        return self._get(body)

    def eip_release(self, region, eipid):
        '''
        release an eip
        :param region:
        :param eipid:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'ReleaseEIP'
        body['EIPId'] = eipid

        return self._get(body)

    def eip_bind(self, region, eipid, resource_type, resourceid):
        '''
        bind ip to given resource
        :param region:
        :param eipid:
        :param resource_type:
        :param resourceid:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'BindEIP'
        body['EIPId'] = eipid
        body['ResourceType'] = resource_type
        body['ResourceId'] = resourceid

        return self._get(body)

    def eip_unbind(self, region, eipid, resource_type, resourceid):
        '''
        unbind ip to given resource
        :param region:
        :param eipid:
        :param resource_type:
        :param resourceid:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'UnBindEIP'
        body['EIPId'] = eipid
        body['ResourceType'] = resource_type
        body['ResourceId'] = resourceid

        return self._get(body)

    def eip_bandwidth_modify(self, region, eipid, bandwidth):
        '''
        modify bandwidth of a given eip
        :param region:
        :param eipid:
        :param bandwidth:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'ModifyEIPBandwidth'
        body['EIPId'] = eipid
        body['Bandwidth'] = bandwidth

        return self._get(body)

    def eip_weight_modify(self, region, eipid, weight):
        '''
        modify weight of a given eip
        :param region:
        :param eipid:
        :param weight:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'ModifyEIPWeight'
        body['EIPId'] = eipid
        body['Weight'] = weight

        return self._get(body)

    def eip_price_get(self, region, operator_name, bandwidth,
                      charge_type=None):
        '''
        get eip price
        :param region:
        :param operator_name:
        :param bandwidth:
        :param charge_type:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'GetEIPPrice'
        body['OperatorName'] = operator_name
        body['Bandwidth'] = bandwidth
        if charge_type:
            body['ChargeType'] = charge_type

        return self._get(body)

    def vip_allocate(self, region, count=None):
        '''
        allocate a vip
        :param region:
        :param count:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'AllocateVIP'
        if count:
            body['Count'] = count

        return self._get(body)

    def vip_get(self, region):
        '''
        list all vip
        :param region:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'DescribeVIP'

        return self._get(body)

    def vip_release(self, region, vip):
        '''
        release a vip
        :param region:
        :param vip:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'ReleaseVIP'
        body['VIP'] = vip

        return self._get(body)

    def sec_get(self, region, resourcetype=None, resourceid=None,
                groupid=None):
        '''
        get security group info
        :param region:
        :param resourcetype:
        :param resourceid:
        :param groupid:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'DescribeSecurityGroup'
        if resourcetype:
            body['ResourceType'] = resourcetype
        if resourceid:
            body['ResourceId'] = resourceid
        if groupid:
            body['GroupId'] = groupid

        return self._get(body)

    def sec_reource_get(self, region, groupid=None):
        '''
        get resource attached to given security group
        :param region:
        :param groupid:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'DescribeSecurityGroupResource'
        if groupid:
            body['GroupId'] = groupid

        return self._get(body)

    def sec_creat(self, region, group_name, rules, description=None):
        '''
        create security group
        :param region:
        :param group_name:
        :param rule: [],must be a list, even if only one rule
        :param description:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'CreateSecurityGroup'
        body['GroupName'] = group_name
        if rules:
            for i in range(len(rules)):
                body['Rule.' + str(i)] = rules[i]
        if description:
            body['Description'] = description

        return self._get(body)

    def sec_update(self, region, groupid, rules):
        '''
        update given security group
        :param region:
        :param groupid:
        :param rules: [],must be a list, even if only one rule
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'UpdateSecurityGroup'
        body['GroupId'] = groupid
        if rules:
            for i in range(len(rules)):
                body['Rule.' + str(i)] = rules[i]

        return self._get(body)

    def sec_grant(self, region, groupid, resource_type, resourceid):
        '''
        grant given security group to specified resource
        :param region:
        :param groupid:
        :param resource_type:
        :param resourceid:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'GrantSecurityGroup'
        body['GroupId'] = groupid
        body['ResourceType'] = resource_type
        body['ResourceId'] = resourceid

        return self._get(body)

    def sec_delete(self, region, groupid):
        '''
        delete given security group
        :param region:
        :param groupip:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'DeleteSecurityGroup'
        body['GroupId'] = groupid

        return self._get(body)
