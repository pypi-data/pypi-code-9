#!/usr/bin/python

# CenturyLink Cloud Ansible Modules.
#
# These Ansible modules enable the CenturyLink Cloud v2 API to be called
# from an within Ansible Playbook.
#
# This file is part of CenturyLink Cloud, and is maintained
# by the Workflow as a Service Team
#
# Copyright 2015 CenturyLink
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# CenturyLink Cloud: http://www.CenturyLinkCloud.com
# API Documentation: https://www.centurylinkcloud.com/api-docs/v2/

DOCUMENTATION = '''
module: clc_aa_policy
short_descirption: Create or Delete Anti Affinity Policies at CenturyLink Cloud.
description:
  - An Ansible module to Create or Delete Anti Affinity Policies at CenturyLink Cloud.
options:
  name:
    description:
      - The name of the Anti Affinity Policy.
    required: True
  location:
    description:
      - Datacenter in which the policy lives/should live.
    required: True
  state:
    description:
      - Whether to create or delete the policy.
    required: False
    default: present
    choices: ['present','absent']
  wait:
    description:
      - Whether to wait for the provisioning tasks to finish before returning.
    default: True
    required: False
    choices: [ True, False]
    aliases: []
'''

EXAMPLES = '''
# Note - You must set the CLC_V2_API_USERNAME And CLC_V2_API_PASSWD Environment variables before running these examples

---
- name: Create AA Policy
  hosts: localhost
  gather_facts: False
  connection: local
  tasks:
    - name: Create an Anti Affinity Policy
      clc_aa_policy:
        name: 'Hammer Time'
        location: 'UK3'
        state: present
      register: policy

    - name: debug
      debug: var=policy

---
- name: Delete AA Policy
  hosts: localhost
  gather_facts: False
  connection: local
  tasks:
    - name: Delete an Anti Affinity Policy
      clc_aa_policy:
        name: 'Hammer Time'
        location: 'UK3'
        state: absent
      register: policy

    - name: debug
      debug: var=policy
'''

__version__ = '1.0.2'

import requests

#
#  Requires the clc-python-sdk.
#  sudo pip install clc-sdk
#
try:
    import clc as clc_sdk
    from clc import CLCException
except ImportError:
    clc_found = False
    clc_sdk = None
else:
    clc_found = True


class ClcAntiAffinityPolicy():

    clc = clc_sdk
    module = None

    def __init__(self, module):
        """
        Construct module
        """
        self.module = module
        self.policy_dict = {}

        if not clc_found:
            self.module.fail_json(
                msg='clc-python-sdk required for this module')

        self._set_user_agent(self.clc)

    @staticmethod
    def _define_module_argument_spec():
        """
        Define the argument spec for the ansible module
        :return: argument spec dictionary
        """
        argument_spec = dict(
            name=dict(required=True),
            location=dict(required=True),
            alias=dict(default=None),
            wait=dict(default=True),
            state=dict(default='present', choices=['present', 'absent']),
        )
        return argument_spec

    # Module Behavior Goodness
    def process_request(self):
        """
        Process the request - Main Code Path
        :return: Returns with either an exit_json or fail_json
        """
        p = self.module.params

        if not clc_found:
            self.module.fail_json(
                msg='clc-python-sdk required for this module')

        self._set_clc_credentials_from_env()
        self.policy_dict = self._get_policies_for_datacenter(p)

        if p['state'] == "absent":
            changed, policy = self._ensure_policy_is_absent(p)
        else:
            changed, policy = self._ensure_policy_is_present(p)

        if hasattr(policy, 'data'):
            policy = policy.data
        elif hasattr(policy, '__dict__'):
            policy = policy.__dict__

        self.module.exit_json(changed=changed, policy=policy)

    def _set_clc_credentials_from_env(self):
        """
        Set the CLC Credentials on the sdk by reading environment variables
        :return: none
        """
        env = os.environ
        v2_api_token = env.get('CLC_V2_API_TOKEN', False)
        v2_api_username = env.get('CLC_V2_API_USERNAME', False)
        v2_api_passwd = env.get('CLC_V2_API_PASSWD', False)
        clc_alias = env.get('CLC_ACCT_ALIAS', False)
        api_url = env.get('CLC_V2_API_URL', False)

        if api_url:
            self.clc.defaults.ENDPOINT_URL_V2 = api_url

        if v2_api_token and clc_alias:
            self.clc._LOGIN_TOKEN_V2 = v2_api_token
            self.clc._V2_ENABLED = True
            self.clc.ALIAS = clc_alias
        elif v2_api_username and v2_api_passwd:
            self.clc.v2.SetCredentials(
                api_username=v2_api_username,
                api_passwd=v2_api_passwd)
        else:
            return self.module.fail_json(
                msg="You must set the CLC_V2_API_USERNAME and CLC_V2_API_PASSWD "
                    "environment variables")

    def _get_policies_for_datacenter(self, p):
        """
        Get the Policies for a datacenter by calling the CLC API.
        :param p: datacenter to get policies from
        :return: policies in the datacenter
        """
        response = {}

        policies = self.clc.v2.AntiAffinity.GetAll(location=p['location'])

        for policy in policies:
            response[policy.name] = policy
        return response

    def _create_policy(self, p):
        """
        Create an Anti Affinnity Policy using the CLC API.
        :param p: datacenter to create policy in
        :return: response dictionary from the CLC API.
        """
        return self.clc.v2.AntiAffinity.Create(
            name=p['name'],
            location=p['location'])

    def _delete_policy(self, p):
        """
        Delete an Anti Affinity Policy using the CLC API.
        :param p: datacenter to delete a policy from
        :return: none
        """
        policy = self.policy_dict[p['name']]
        policy.Delete()

    def _policy_exists(self, policy_name):
        """
        Check to see if an Anti Affinity Policy exists
        :param policy_name: name of the policy
        :return: boolean of if the policy exists
        """
        if policy_name in self.policy_dict:
            return self.policy_dict.get(policy_name)

        return False

    def _ensure_policy_is_absent(self, p):
        """
        Makes sure that a policy is absent
        :param p: dictionary of policy name
        :return: tuple of if a deletion occurred and the name of the policy that was deleted
        """
        changed = False
        if self._policy_exists(policy_name=p['name']):
            changed = True
            if not self.module.check_mode:
                self._delete_policy(p)
        return changed, None

    def _ensure_policy_is_present(self, p):
        """
        Ensures that a policy is present
        :param p: dictonary of a policy name
        :return: tuple of if an addition occurred and the name of the policy that was added
        """
        changed = False
        policy = self._policy_exists(policy_name=p['name'])
        if not policy:
            changed = True
            policy = None
            if not self.module.check_mode:
                policy = self._create_policy(p)
        return changed, policy

    @staticmethod
    def _set_user_agent(clc):
        if hasattr(clc, 'SetRequestsSession'):
            agent_string = "ClcAnsibleModule/" + __version__
            ses = requests.Session()
            ses.headers.update({"Api-Client": agent_string})
            ses.headers['User-Agent'] += " " + agent_string
            clc.SetRequestsSession(ses)


def main():
    """
    The main function.  Instantiates the module and calls process_request.
    :return: none
    """
    module = AnsibleModule(
        argument_spec=ClcAntiAffinityPolicy._define_module_argument_spec(),
        supports_check_mode=True)
    clc_aa_policy = ClcAntiAffinityPolicy(module)
    clc_aa_policy.process_request()

from ansible.module_utils.basic import *  # pylint: disable=W0614
if __name__ == '__main__':
    main()
