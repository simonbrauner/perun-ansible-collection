from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api_client import ApiClient
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.configuration import Configuration
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.oidc import DeviceCodeOAuth


def general_module_options():
    return dict(
        argument_spec=dict(
            oauth=dict(
                type="dict",
                required=False,
                options=dict(
                    perun_instance=dict(type="str", required=True)
                )
            ),
            ba=dict(
                type="dict",
                required=False,
                options=dict(
                    rpc_url=dict(type="str", required=True),
                    user=dict(type="str", required=True),
                    password=dict(type="str", required=True, no_log=True),
                )
            )
        ),
        required_one_of=[['oauth', 'ba']],
        mutually_exclusive=[['oauth', 'ba']],
        supports_check_mode=False,
    )

def configured_api_client(params):
    if params["oauth"] is not None:
        dca = DeviceCodeOAuth(
            params["oauth"]["perun_instance"],
            "s3cr3t",
            False,
            8 * 60,
            False
        )
        config = Configuration(
            access_token=dca.get_access_token(),
            host=dca.get_perun_api_url(),
        )
    else:
        config = Configuration(
            host=params["ba"]["rpc_url"],
            username=params["ba"]["user"],
            password=params["ba"]["password"],
        )

    return ApiClient(config)
