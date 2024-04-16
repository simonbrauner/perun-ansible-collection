#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: vo_info

short_description: Get data about virtual organization
"""

EXAMPLES = r"""
- name: Get data about given virtual organization
  simonbrauner.perun.vo_info:
    rpc_url: "{{ rpc_url }}"
    auth:
      user: "{{ user }}"
      password: "{{ password }}"
    short_name: "{{ vo_name }}"
"""

from ansible_collections.simonbrauner.perun.plugins.module_utils.api_client import (
    API_CLIENT_ARGS,
    configured_api_client,
)

from perun_openapi.api.vos_manager_api import VosManagerApi

from ansible.module_utils.basic import AnsibleModule

from json import loads


def get_content(params, api_client):
    manager = VosManagerApi(api_client)
    response = manager.get_vo_by_short_name(
        params["short_name"], _preload_content=False
    )
    json_string = response.read().decode()

    return loads(json_string)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            **API_CLIENT_ARGS, short_name=dict(type="str", required=True)
        ),
        supports_check_mode=False,
    )

    try:
        with configured_api_client(module.params) as api_client:
            module.exit_json(**get_content(module.params, api_client))

    except Exception as exception:
        module.fail_json(msg=f"{exception}")


if __name__ == "__main__":
    main()
