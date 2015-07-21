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
class ProductBindBsnRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Bsn', '2015-05-12', 'ProductBindBsn')

	def get_num(self):
		return self.get_query_params().get('num')

	def set_num(self,num):
		self.add_query_param('num',num)

	def get_resourceType(self):
		return self.get_query_params().get('resourceType')

	def set_resourceType(self,resourceType):
		self.add_query_param('resourceType',resourceType)

	def get_resourceId(self):
		return self.get_query_params().get('resourceId')

	def set_resourceId(self,resourceId):
		self.add_query_param('resourceId',resourceId)

	def get_aliuid(self):
		return self.get_query_params().get('aliuid')

	def set_aliuid(self,aliuid):
		self.add_query_param('aliuid',aliuid)