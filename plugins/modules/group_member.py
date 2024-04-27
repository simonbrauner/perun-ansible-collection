#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: group_member

short_description: Manage membership in group
"""

EXAMPLES = r"""
- name: Add member to group
  simonbrauner.perun.group_member:
    rpc_url: "{{ rpc_url }}"
    auth:
      user: "{{ user }}"
      password: "{{ password }}"
    member_id: "{{ member1.id }}"
    group_id: "{{ group1.id }}"
    member_of_group: true

- name: Remove member from group
  simonbrauner.perun.group_member:
    rpc_url: "{{ rpc_url }}"
    auth:
      user: "{{ user }}"
      password: "{{ password }}"
    member_id: "{{ member1.id }}"
    group_id: "{{ group1.id }}"
    member_of_group: false
"""

from ansible_collections.simonbrauner.perun.plugins.module_utils.api_client import (
    API_CLIENT_ARGS,
    configured_api_client,
)

from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.groups_manager_api import GroupsManagerApi

from ansible.module_utils.basic import AnsibleModule

from json import loads


def needs_change(params, api_client):
    manager = GroupsManagerApi(api_client)
    is_member = manager.is_group_member(params["member_id"], params["group_id"])

    return is_member != params["member_of_group"]


def perform_changes(params, api_client):
    manager = GroupsManagerApi(api_client)
    member_function_args = ([params["group_id"]], params["member_id"])

    if params["member_of_group"]:
        manager.add_member(*member_function_args)
    else:
        manager.remove_member(*member_function_args)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            **API_CLIENT_ARGS,
            member_id=dict(type="int", required=True),
            group_id=dict(type="int", required=True),
            member_of_group=dict(type="bool", required=True),
        ),
        supports_check_mode=False,
    )

    try:
        with configured_api_client(module.params) as api_client:
            if not needs_change(module.params, api_client):
                module.exit_json()

            perform_changes(module.params, api_client)
            module.exit_json(changed=True)

    except Exception as exception:
        module.fail_json(msg=f"{exception}")


if __name__ == "__main__":
    main()
