#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: mails_info

short_description: Get mails of given vo/group
"""

EXAMPLES = r"""
- name: Get mails of given vo
  simonbrauner.perun.mails_info:
    rpc_url: "{{ rpc_url }}"
    auth:
      user: "{{ user }}"
      password: "{{ password }}"
    vo_id: "{{ vo1.id }}"

- name: Get mails of given group
  simonbrauner.perun.mails_info:
    rpc_url: "{{ rpc_url }}"
    auth:
      user: "{{ user }}"
      password: "{{ password }}"
    group_id: "{{ group1.id }}"
"""

from ansible_collections.simonbrauner.perun.plugins.module_utils.api_client import (
    general_module_options,
    configured_api_client,
)

from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.registrar_manager_api import RegistrarManagerApi

from ansible.module_utils.basic import AnsibleModule

from json import loads


def get_content(params, api_client):
    manager = RegistrarManagerApi(api_client)

    if params["vo_id"] is not None:
        response = manager.get_application_mails_for_vo(int(params["vo_id"]), _preload_content=False)
    else:
        response = manager.get_application_mails_for_group(int(params["group_id"]), _preload_content=False)

    json_string = response.read().decode()

    return {"mails":loads(json_string)}


def main():
    options = general_module_options()
    options["argument_spec"]["vo_id"] = dict(type="str", required=False)
    options["argument_spec"]["group_id"] = dict(type="str", required=False)
    options["required_one_of"].append(["vo_id", 'group_id'])
    options["mutually_exclusive"].append(["vo_id", 'group_id'])
    module = AnsibleModule(**options)

    try:
        with configured_api_client(module.params) as api_client:
            module.exit_json(**get_content(module.params, api_client))

    except Exception as exception:
        module.fail_json(msg=f"{exception}")


if __name__ == "__main__":
    main()
