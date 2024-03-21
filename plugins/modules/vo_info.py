#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: vo_info

short_description: Get data about virtual organization
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url

from urllib.parse import urljoin
from json import loads


def get_content(params):
    url = urljoin(params['rpc_url'], '/ba/rpc/json/vosManager/getVoByShortName')
    url = url + f'?shortName={params["short_name"]}'
    response = open_url(url, url_username=params['user'], url_password=params['password'])
    json_string = response.read().decode()

    return loads(json_string)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            rpc_url=dict(type='str', required=True),
            user=dict(type='str', required=True),
            password=dict(type='str', required=True),
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
