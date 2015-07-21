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
class SetUserBusinessStatusRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ubsms', '2015-06-23', 'SetUserBusinessStatus')

	def get_Uid(self):
		return self.get_query_params().get('Uid')

	def set_Uid(self,Uid):
		self.add_query_param('Uid',Uid)

	def get_Service(self):
		return self.get_query_params().get('Service')

	def set_Service(self,Service):
		self.add_query_param('Service',Service)

	def get_StatusKey(self):
		return self.get_query_params().get('StatusKey')

	def set_StatusKey(self,StatusKey):
		self.add_query_param('StatusKey',StatusKey)

	def get_StatusValue(self):
		return self.get_query_params().get('StatusValue')

	def set_StatusValue(self,StatusValue):
		self.add_query_param('StatusValue',StatusValue)