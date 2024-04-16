from perun_openapi.api_client import ApiClient
from perun_openapi.configuration import Configuration

def configured_api_client(params):
    if params["auth"] is None:
        raise NotImplementedError("OAuth 2 is not implemented")

    config = Configuration(
        host=params["rpc_url"],
        username=params["auth"]["user"],
        password=params["auth"]["password"],
    )

    return ApiClient(config)
