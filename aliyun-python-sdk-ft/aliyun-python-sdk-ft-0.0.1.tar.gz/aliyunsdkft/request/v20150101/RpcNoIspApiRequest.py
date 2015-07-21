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
class RpcNoIspApiRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ft', '2015-01-01', 'RpcNoIspApi')

	def get_IntValue(self):
		return self.get_query_params().get('IntValue')

	def set_IntValue(self,IntValue):
		self.add_query_param('IntValue',IntValue)

	def get_NumberRange(self):
		return self.get_query_params().get('NumberRange')

	def set_NumberRange(self,NumberRange):
		self.add_query_param('NumberRange',NumberRange)