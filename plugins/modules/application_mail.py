#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r"""
---
module: application_mail

short_description: Create/update/delete application mail

description: Create/update/delete application mail.
"""

EXAMPLES = r"""
- name: Create a new application mail
  application_mail:
    mail:
      app_type: INITIAL
      mail_type: APP_CREATED_USER
      message:
        cs:
          locale: cs
          subject: "{{ cs_subject }}"
          text: "{{ cs_text }}"
      html_message:
        en:
          locale: en
          subject: "{{ en_subject }}"
          text: "{{ en_text }}"

- name: Set send to false in application mail
  application_mail:
    mail:
      app_type: INITIAL
      mail_type: APP_CREATED_USER
      send: false
      message:
        cs:
          locale: cs
          subject: "{{ cs_subject }}"
          text: "{{ cs_text }}"
      html_message:
        en:
          locale: en
          subject: "{{ en_subject }}"
          text: "{{ en_text }}"

- name: Delete the application mail
  application_mail:
    state: absent
    mail:
      app_type: INITIAL
      mail_type: APP_CREATED_USER
"""

from ansible_collections.simonbrauner.perun.plugins.module_utils.api_client import (
    general_module_options,
    configured_api_client,
)
from ansible_collections.simonbrauner.perun.plugins.module_utils.get_mails import (
    get_mails,
)

from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.exceptions import (
    ApiException,
)
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.registrar_manager_api import (
    RegistrarManagerApi,
)
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.model.app_type import (
    AppType,
)
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.model.mail_type import (
    MailType,
)
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.model.mail_text import (
    MailText,
)
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.model.application_mail import (
    ApplicationMail,
)

from ansible.module_utils.basic import AnsibleModule

from json import loads


def get_mail(params, api_client):
    mails = get_mails(params, api_client)

    for mail in mails:
        if mail["id"] == params["mail"]["id"] or (
            mail["appType"] == params["mail"]["app_type"]
            and mail["mailType"] == params["mail"]["mail_type"]
        ):
            return mail

    return None


def updated_mail(found_mail, params, api_client):
    manager = RegistrarManagerApi(api_client)

    mail_data = {
        "app_type": AppType(params["mail"]["app_type"]),
        "mail_type": MailType(params["mail"]["mail_type"]),
        "send": params["mail"]["send"],
        "message": {
            property: MailText(params["mail"]["message"][property])
            for property in params["mail"]["message"]
        },
        "html_message": {
            property: MailText(params["mail"]["html_message"][property])
            for property in params["mail"]["html_message"]
        },
    }

    if found_mail is not None:
        mail_data["id"] = found_mail["id"]
        mail_data["form_id"] = found_mail["formId"]

    return ApplicationMail(**mail_data)


def create_mail(mail_data, params, api_client):
    manager = RegistrarManagerApi(api_client)

    if params["vo_id"] is not None:
        mail_data["vo"] = params["vo_id"]
        manager.add_application_mail_for_vo(mail_data)
    else:
        mail_data["group"] = params["group_id"]
        manager.add_application_mail_for_group(mail_data)


def delete_mail(found_mail_id, params, api_client):
    manager = RegistrarManagerApi(api_client)

    if params["vo_id"] is not None:
        manager.delete_application_mail_for_vo(params["vo_id"], found_mail_id)
    else:
        manager.delete_application_mail_for_group(params["group_id"], found_mail_id)


def set_mail(found_mail, params, api_client):
    manager = RegistrarManagerApi(api_client)

    if params["state"] == "absent":
        if found_mail is None:
            return False

        delete_mail(found_mail["id"], params, api_client)
        return True

    mail_data = {"mail": updated_mail(found_mail, params, api_client)}

    if found_mail is None:
        create_mail(mail_data, params, api_client)
        return True

    manager.update_application_mail(mail_data)
    return True


def main():
    options = general_module_options()
    options["argument_spec"]["mail"] = dict(
        type="dict",
        required=True,
        options=dict(
            id=dict(type="int", required=False),
            app_type=dict(type="str", required=False),
            mail_type=dict(type="str", required=False),
            send=dict(type="bool", required=False, default=True),
            message=dict(
                type="dict",
                required=False,
                default=dict(),
                additional_properties=dict(
                    type="dict",
                    options=dict(
                        locale=dict(type="str", required=False),
                        subject=dict(type="str", required=False),
                        text=dict(type="str", required=False),
                    ),
                ),
            ),
            html_message=dict(
                type="dict",
                required=False,
                default=dict(),
                additional_properties=dict(
                    type="dict",
                    options=dict(
                        locale=dict(type="str", required=False),
                        subject=dict(type="str", required=False),
                        text=dict(type="str", required=False),
                    ),
                ),
            ),
        ),
        required_one_of=[["id", "app_type"], ["id", "mail_type"]],
        mutually_exclusive=[["id", "app_type"], ["id", "mail_type"]],
    )
    options["argument_spec"]["state"] = dict(
        type="str", choices=["present", "absent"], required=False, default="present"
    )
    options["argument_spec"]["vo_id"] = dict(type="int", required=False)
    options["argument_spec"]["group_id"] = dict(type="int", required=False)
    options["required_one_of"].append(["vo_id", "group_id"])
    options["mutually_exclusive"].append(["vo_id", "group_id"])
    module = AnsibleModule(**options)

    try:
        with configured_api_client(module.params) as api_client:
            found_mail = get_mail(module.params, api_client)

            module.exit_json(changed=set_mail(found_mail, module.params, api_client))

    except Exception as exception:
        module.fail_json(msg=f"{exception}")


if __name__ == "__main__":
    main()
