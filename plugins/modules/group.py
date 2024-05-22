#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: group

short_description: Create group or change its description

description: Create group or change its description.
"""

EXAMPLES = r"""
- name: Add new group
  simonbrauner.perun.group:
    vo_id: "{{ vo1.id }}"
    name: "{{ group_name }}"
    description: "{{ group_description }}"

- name: Change group description
  simonbrauner.perun.group:
    vo_id: "{{ vo1.id }}"
    name: "{{ group_name }}"
    description: "{{ new_group_description }}"
"""

from ansible_collections.simonbrauner.perun.plugins.module_utils.api_client import (
    general_module_options,
    configured_api_client,
)

from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.exceptions import (
    ApiException,
)
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.groups_manager_api import (
    GroupsManagerApi,
)
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.model.input_update_group import (
    InputUpdateGroup,
)

from ansible.module_utils.basic import AnsibleModule

from json import loads


def get_group(params, api_client):
    manager = GroupsManagerApi(api_client)

    try:
        return manager.get_group_by_name(params["vo_id"], params["name"])
    except Exception:
        return None


def set_group(found_group, params, api_client):
    manager = GroupsManagerApi(api_client)

    if found_group is None:
        manager.create_group_with_vo_name_description(
            params["vo_id"], params["name"], params["description"]
        )

        return True

    if found_group.description != params["description"]:
        found_group.description = params["description"]
        manager.update_group(InputUpdateGroup(found_group))

        return True

    return False


def main():
    options = general_module_options()
    options["argument_spec"]["vo_id"] = dict(type="int", required=True)
    options["argument_spec"]["name"] = dict(type="str", required=True)
    options["argument_spec"]["description"] = dict(type="str", required=True)
    module = AnsibleModule(**options)

    try:
        with configured_api_client(module.params) as api_client:
            found_group = get_group(module.params, api_client)

            module.exit_json(changed=set_group(found_group, module.params, api_client))

    except Exception as exception:
        module.fail_json(msg=f"{exception}")


if __name__ == "__main__":
    main()
