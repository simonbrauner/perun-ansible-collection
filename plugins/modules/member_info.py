#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: member_info

short_description: Get data about member
'''

EXAMPLES = r'''
- name: Get data about member
  simonbrauner.perun.member_info:
    rpc_url: "{{ rpc_url }}"
    auth:
      user: "{{ user }}"
      password: "{{ password }}"
    vo_id: "{{ vo1.id }}"
    user_id: "{{ user_id }}"
'''

from perun_openapi.api_client import ApiClient
from perun_openapi.configuration import Configuration
from perun_openapi.api.members_manager_api import MembersManagerApi

from ansible.module_utils.basic import AnsibleModule

from json import loads


def get_content(params):
    if params["auth"] is None:
        raise NotImplementedError("OAuth 2 is not implemented yed")

    config = Configuration(
        host=params["rpc_url"],
        username=params["auth"]["user"],
        password=params["auth"]["password"],
    )

    with ApiClient(config) as api_client:
        manager = MembersManagerApi(api_client)
        response = manager.get_member_by_user(params["vo_id"], params["user_id"], _preload_content=False)
        json_string = response.read().decode()

        return loads(json_string)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            rpc_url=dict(type='str', required=True),
            auth=dict(type='dict', required=False,
                      options=dict(
                          user=dict(type='str', required=True),
                          password=dict(type='str', required=True, no_log=True),
                      )),
            vo_id=dict(type='int', required=True),
            user_id=dict(type='int', required=True)
        ),
        supports_check_mode=False
    )

    try:
        module.exit_json(**get_content(module.params))

    except Exception as exception:
        module.fail_json(msg=f'{exception}')


if __name__ == '__main__':
    main()
