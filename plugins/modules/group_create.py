#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: group_create

short_description: Create a new group
"""

EXAMPLES = r"""
- name: Add new group
  simonbrauner.perun.group_create:
    rpc_url: "{{ rpc_url }}"
    auth:
      user: "{{ user }}"
      password: "{{ password }}"
    vo_id: "{{ vo1.id }}"
    name: "{{ new_group_name }}"
    description: "{{ new_group_description }}"
"""

from ansible_collections.simonbrauner.perun.plugins.module_utils.api_client import (
    API_CLIENT_ARGS,
    configured_api_client,
)

from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.exceptions import ApiException
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.groups_manager_api import GroupsManagerApi

from ansible.module_utils.basic import AnsibleModule

from json import loads


def needs_change(params, api_client):
    manager = GroupsManagerApi(api_client)

    try:
        manager.get_group_by_name(
            params["vo_id"], params["name"], _preload_content=False
        )
    except ApiException:
        return True

    return False


def perform_changes(params, api_client):
    manager = GroupsManagerApi(api_client)
    response = manager.create_group_with_vo_name_description(
        params["vo_id"], params["name"], params["description"], _preload_content=False
    )
    json_string = response.read().decode()

    return loads(json_string)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            **API_CLIENT_ARGS,
            vo_id=dict(type="int", required=True),
            name=dict(type="str", required=True),
            description=dict(type="str", required=True),
        ),
        supports_check_mode=False,
    )

    try:
        with configured_api_client(module.params) as api_client:
            if not needs_change(module.params, api_client):
                module.exit_json()

            module.exit_json(changed=True, **perform_changes(module.params, api_client))

    except Exception as exception:
        module.fail_json(msg=f"{exception}")


if __name__ == "__main__":
    main()
