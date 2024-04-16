#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: vo_info

short_description: Get data about virtual organization
'''

EXAMPLES = r'''
- name: Get data about given virtual organization
  vo_info:
    rpc_url: "{{ rpc_url }}"
    auth:
      user: "{{ user }}"
      password: "{{ password }}"
    short_name: "{{ vo_name }}"
'''

from perun_openapi.api_client import ApiClient
from perun_openapi.configuration import Configuration
from perun_openapi.api.vos_manager_api import VosManagerApi

from ansible.module_utils.basic import AnsibleModule

from json import loads


def get_content(params):
    if params["auth"] is None:
        raise NotImplementedError("OAuth 2 is not implemented yed")

    config = Configuration(
        host=params["rpc_url"],
        username=params["auth"]["user"],
        password=params["auth"]["password"],
    )

    with ApiClient(config) as api_client:
        manager = VosManagerApi(api_client)
        response = manager.get_vo_by_short_name(params["short_name"], _preload_content=False)
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
            short_name=dict(type='str', required=True)
        ),
        supports_check_mode=False
    )

    try:
        module.exit_json(**get_content(module.params))

    except Exception as exception:
        module.fail_json(msg=f'{exception}')


if __name__ == '__main__':
    main()
