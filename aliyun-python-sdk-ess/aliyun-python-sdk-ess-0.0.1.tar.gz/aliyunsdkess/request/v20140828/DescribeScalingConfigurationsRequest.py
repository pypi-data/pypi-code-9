# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
class DescribeScalingConfigurationsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ess', '2014-08-28', 'DescribeScalingConfigurations')

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_PageNumber(self):
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self,PageNumber):
		self.add_query_param('PageNumber',PageNumber)

	def get_PageSize(self):
		return self.get_query_params().get('PageSize')

	def set_PageSize(self,PageSize):
		self.add_query_param('PageSize',PageSize)

	def get_ScalingGroupId(self):
		return self.get_query_params().get('ScalingGroupId')

	def set_ScalingGroupId(self,ScalingGroupId):
		self.add_query_param('ScalingGroupId',ScalingGroupId)

	def get_ScalingConfigurationId1(self):
		return self.get_query_params().get('ScalingConfigurationId1')

	def set_ScalingConfigurationId1(self,ScalingConfigurationId1):
		self.add_query_param('ScalingConfigurationId1',ScalingConfigurationId1)

	def get_ScalingConfigurationId2(self):
		return self.get_query_params().get('ScalingConfigurationId2')

	def set_ScalingConfigurationId2(self,ScalingConfigurationId2):
		self.add_query_param('ScalingConfigurationId2',ScalingConfigurationId2)

	def get_ScalingConfigurationId3(self):
		return self.get_query_params().get('ScalingConfigurationId3')

	def set_ScalingConfigurationId3(self,ScalingConfigurationId3):
		self.add_query_param('ScalingConfigurationId3',ScalingConfigurationId3)

	def get_ScalingConfigurationId4(self):
		return self.get_query_params().get('ScalingConfigurationId4')

	def set_ScalingConfigurationId4(self,ScalingConfigurationId4):
		self.add_query_param('ScalingConfigurationId4',ScalingConfigurationId4)

	def get_ScalingConfigurationId5(self):
		return self.get_query_params().get('ScalingConfigurationId5')

	def set_ScalingConfigurationId5(self,ScalingConfigurationId5):
		self.add_query_param('ScalingConfigurationId5',ScalingConfigurationId5)

	def get_ScalingConfigurationId6(self):
		return self.get_query_params().get('ScalingConfigurationId6')

	def set_ScalingConfigurationId6(self,ScalingConfigurationId6):
		self.add_query_param('ScalingConfigurationId6',ScalingConfigurationId6)

	def get_ScalingConfigurationId7(self):
		return self.get_query_params().get('ScalingConfigurationId7')

	def set_ScalingConfigurationId7(self,ScalingConfigurationId7):
		self.add_query_param('ScalingConfigurationId7',ScalingConfigurationId7)

	def get_ScalingConfigurationId8(self):
		return self.get_query_params().get('ScalingConfigurationId8')

	def set_ScalingConfigurationId8(self,ScalingConfigurationId8):
		self.add_query_param('ScalingConfigurationId8',ScalingConfigurationId8)

	def get_ScalingConfigurationId9(self):
		return self.get_query_params().get('ScalingConfigurationId9')

	def set_ScalingConfigurationId9(self,ScalingConfigurationId9):
		self.add_query_param('ScalingConfigurationId9',ScalingConfigurationId9)

	def get_ScalingConfigurationId10(self):
		return self.get_query_params().get('ScalingConfigurationId10')

	def set_ScalingConfigurationId10(self,ScalingConfigurationId10):
		self.add_query_param('ScalingConfigurationId10',ScalingConfigurationId10)

	def get_ScalingConfigurationName1(self):
		return self.get_query_params().get('ScalingConfigurationName1')

	def set_ScalingConfigurationName1(self,ScalingConfigurationName1):
		self.add_query_param('ScalingConfigurationName1',ScalingConfigurationName1)

	def get_ScalingConfigurationName2(self):
		return self.get_query_params().get('ScalingConfigurationName2')

	def set_ScalingConfigurationName2(self,ScalingConfigurationName2):
		self.add_query_param('ScalingConfigurationName2',ScalingConfigurationName2)

	def get_ScalingConfigurationName3(self):
		return self.get_query_params().get('ScalingConfigurationName3')

	def set_ScalingConfigurationName3(self,ScalingConfigurationName3):
		self.add_query_param('ScalingConfigurationName3',ScalingConfigurationName3)

	def get_ScalingConfigurationName4(self):
		return self.get_query_params().get('ScalingConfigurationName4')

	def set_ScalingConfigurationName4(self,ScalingConfigurationName4):
		self.add_query_param('ScalingConfigurationName4',ScalingConfigurationName4)

	def get_ScalingConfigurationName5(self):
		return self.get_query_params().get('ScalingConfigurationName5')

	def set_ScalingConfigurationName5(self,ScalingConfigurationName5):
		self.add_query_param('ScalingConfigurationName5',ScalingConfigurationName5)

	def get_ScalingConfigurationName6(self):
		return self.get_query_params().get('ScalingConfigurationName6')

	def set_ScalingConfigurationName6(self,ScalingConfigurationName6):
		self.add_query_param('ScalingConfigurationName6',ScalingConfigurationName6)

	def get_ScalingConfigurationName7(self):
		return self.get_query_params().get('ScalingConfigurationName7')

	def set_ScalingConfigurationName7(self,ScalingConfigurationName7):
		self.add_query_param('ScalingConfigurationName7',ScalingConfigurationName7)

	def get_ScalingConfigurationName8(self):
		return self.get_query_params().get('ScalingConfigurationName8')

	def set_ScalingConfigurationName8(self,ScalingConfigurationName8):
		self.add_query_param('ScalingConfigurationName8',ScalingConfigurationName8)

	def get_ScalingConfigurationName9(self):
		return self.get_query_params().get('ScalingConfigurationName9')

	def set_ScalingConfigurationName9(self,ScalingConfigurationName9):
		self.add_query_param('ScalingConfigurationName9',ScalingConfigurationName9)

	def get_ScalingConfigurationName10(self):
		return self.get_query_params().get('ScalingConfigurationName10')

	def set_ScalingConfigurationName10(self,ScalingConfigurationName10):
		self.add_query_param('ScalingConfigurationName10',ScalingConfigurationName10)

	def get_OwnerAccount(self):
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self,OwnerAccount):
		self.add_query_param('OwnerAccount',OwnerAccount)