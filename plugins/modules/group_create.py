#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: group_create

short_description: Create a new group
'''

EXAMPLES = r'''
- name: Add new group
  simonbrauner.perun.group_create:
    rpc_url: "{{ rpc_url }}"
    auth:
      user: "{{ user }}"
      password: "{{ password }}"
    vo_id: "{{ vo1.id }}"
    name: "{{ new_group_name }}"
    description: "{{ new_group_description }}"
'''

from perun_openapi.api_client import ApiClient
from perun_openapi.configuration import Configuration
from perun_openapi.api.groups_manager_api import GroupsManagerApi

from ansible.module_utils.basic import AnsibleModule

from json import loads


def client_config(params):
    if params["auth"] is None:
        raise NotImplementedError("OAuth 2 is not implemented yed")

    return Configuration(
        host=params["rpc_url"],
        username=params["auth"]["user"],
        password=params["auth"]["password"],
    )


def needs_change(params):
    return True


def perform_changes(params):
    with ApiClient(client_config(params)) as api_client:
        manager = GroupsManagerApi(api_client)
        response = manager.create_group_with_vo_name_description(params["vo_id"],
                    params["name"], params["description"], _preload_content=False)
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
            name=dict(type='str', required=True),
            description=dict(type='str', required=True)
        ),
        supports_check_mode=True
    )

    try:
        if not needs_change(module.params):
            module.exit_json()

        module.exit_json(changed=True, **perform_changes(module.params))

    except Exception as exception:
        module.fail_json(msg=f'{exception}')


if __name__ == '__main__':
    main()
