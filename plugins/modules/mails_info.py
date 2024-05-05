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
from ansible_collections.simonbrauner.perun.plugins.module_utils.get_mails import get_mails

from ansible.module_utils.basic import AnsibleModule


def get_content(params, api_client):
    return {"mails":get_mails(params, api_client)}


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
