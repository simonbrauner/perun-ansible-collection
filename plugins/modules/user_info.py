#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: user_info

short_description: Get data about user
"""

EXAMPLES = r"""
- name: Get data about user with given id
  simonbrauner.perun.user_info:
    id: "{{ user_id }}"
"""

from ansible_collections.simonbrauner.perun.plugins.module_utils.api_client import (
    general_module_options,
    configured_api_client,
)

from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.users_manager_api import (
    UsersManagerApi,
)

from ansible.module_utils.basic import AnsibleModule

from json import loads


def get_content(params, api_client):
    manager = UsersManagerApi(api_client)
    response = manager.get_user_by_id(params["id"], _preload_content=False)
    json_string = response.read().decode()

    return loads(json_string)


def main():
    options = general_module_options()
    options["argument_spec"]["id"] = dict(type="int", required=True)
    module = AnsibleModule(**options)

    try:
        with configured_api_client(module.params) as api_client:
            module.exit_json(**get_content(module.params, api_client))

    except Exception as exception:
        module.fail_json(msg=f"{exception}")


if __name__ == "__main__":
    main()
