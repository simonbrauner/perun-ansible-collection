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
    API_CLIENT_ARGS,
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
    module = AnsibleModule(
        argument_spec=dict(
            **API_CLIENT_ARGS,
            vo_id=dict(type="str", required=False),
            group_id=dict(type="str", required=False),
        ),
        required_one_of=[['vo_id', 'group_id']],
        mutually_exclusive=[['vo_id', 'group_id']],
        supports_check_mode=False,
    )

    try:
        with configured_api_client(module.params) as api_client:
            module.exit_json(**get_content(module.params, api_client))

    except Exception as exception:
        module.fail_json(msg=f"{exception}")


if __name__ == "__main__":
    main()
