#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: group_info

short_description: Get data about group in virtual organization
'''

EXAMPLES = r'''
- name: Get data about given group
  simonbrauner.perun.group_info:
    rpc_url: "{{ rpc_url }}"
    auth:
      user: "{{ user }}"
      password: "{{ password }}"
    vo_id: "{{ vo1.id }}"
    name: "{{ group_name }}"
'''

from ansible_collections.simonbrauner.perun.plugins.module_utils.api_client import configured_api_client

from perun_openapi.api.groups_manager_api import GroupsManagerApi

from ansible.module_utils.basic import AnsibleModule

from json import loads


def get_content(params, api_client):
    manager = GroupsManagerApi(api_client)
    response = manager.get_group_by_name(params["vo_id"], params["name"], _preload_content=False)
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
            name=dict(type='str', required=True)
        ),
        supports_check_mode=False
    )

    try:
        with configured_api_client(module.params) as api_client:
            module.exit_json(**get_content(module.params, api_client))

    except Exception as exception:
        module.fail_json(msg=f'{exception}')


if __name__ == '__main__':
    main()
