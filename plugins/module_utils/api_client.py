from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api_client import ApiClient
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.configuration import Configuration


API_CLIENT_ARGS = dict(
    rpc_url=dict(type="str", required=True),
    auth=dict(
        type="dict",
        required=False,
        options=dict(
            user=dict(type="str", required=True),
            password=dict(type="str", required=True, no_log=True),
        ),
    ),
)


def configured_api_client(params):
    if params["auth"] is None:
        raise NotImplementedError("OAuth 2 is not implemented")

    config = Configuration(
        host=params["rpc_url"],
        username=params["auth"]["user"],
        password=params["auth"]["password"],
    )

    return ApiClient(config)
