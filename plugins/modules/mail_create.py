#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: mail_create

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
    general_module_options,
    configured_api_client,
)

from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.exceptions import ApiException
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.registrar_manager_api import RegistrarManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.model.app_type import AppType
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.model.mail_type import MailType
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.model.mail_text import MailText
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.model.application_mail import ApplicationMail

from ansible.module_utils.basic import AnsibleModule

from json import loads


def needs_change(params, api_client):
    return True


def perform_changes(params, api_client):
    manager = RegistrarManagerApi(api_client)
    input_data = {
        "mail": ApplicationMail(
            app_type=AppType(params["mail"]["app_type"]),
            mail_type=MailType(params["mail"]["mail_type"]),
            send=params["mail"]["send"],
            message={property: MailText(params["mail"]["message"][property])
                     for property in params["mail"]["message"]},
            html_message={property: MailText(params["mail"]["html_message"][property])
                     for property in params["mail"]["html_message"]}
        )
    }

    if params["vo_id"] is not None:
        input_data["vo"] = int(params["vo_id"])
        manager.add_application_mail_for_vo(input_data, _preload_content=False)
    else:
        input_data["group"] = int(params["group_id"])
        manager.add_application_mail_for_group(input_data, _preload_content=False)


def main():
    options = general_module_options()
    options["argument_spec"]["mail"] = dict(
        type="dict",
        required=True,
        options=dict(
            app_type=dict(type="str", required=True),
            mail_type=dict(type="str", required=True),
            send=dict(type="bool", required=False, default=True),
            message=dict(
                type="dict",
                required=False,
                additional_properties=dict(
                    type="dict",
                    options=dict(
                        locale=dict(type="str", required=False),
                        subject=dict(type="str", required=False),
                        text=dict(type="str", required=False),
                    )
                )
            ),
            html_message=dict(
                type="dict",
                required=False,
                additional_properties=dict(
                    type="dict",
                    options=dict(
                        locale=dict(type="str", required=False),
                        subject=dict(type="str", required=False),
                        text=dict(type="str", required=False),
                    )
                )
            )

        )
    )
    options["argument_spec"]["vo_id"] = dict(type="str", required=False)
    options["argument_spec"]["group_id"] = dict(type="str", required=False)
    options["required_one_of"].append(["vo_id", 'group_id'])
    options["mutually_exclusive"].append(["vo_id", 'group_id'])
    module = AnsibleModule(**options)

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
