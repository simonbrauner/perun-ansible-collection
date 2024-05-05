from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.registrar_manager_api import RegistrarManagerApi

from json import loads


def get_mails(params, api_client):
    manager = RegistrarManagerApi(api_client)

    if params["vo_id"] is not None:
        response = manager.get_application_mails_for_vo(int(params["vo_id"]), _preload_content=False)
    else:
        response = manager.get_application_mails_for_group(int(params["group_id"]), _preload_content=False)

    json_string = response.read().decode()

    return loads(json_string)
