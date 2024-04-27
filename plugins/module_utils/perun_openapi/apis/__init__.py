
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from perun_openapi.api.attributes_manager_api import AttributesManagerApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.attributes_manager_api import AttributesManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.audit_messages_manager_api import AuditMessagesManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.authz_resolver_api import AuthzResolverApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.cabinet_manager_api import CabinetManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.consents_manager_api import ConsentsManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.database_manager_api import DatabaseManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.ext_sources_manager_api import ExtSourcesManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.facilities_manager_api import FacilitiesManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.groups_manager_api import GroupsManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.integration_manager_api import IntegrationManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.members_manager_api import MembersManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.owners_manager_api import OwnersManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.rt_messages_manager_api import RTMessagesManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.registrar_manager_api import RegistrarManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.resources_manager_api import ResourcesManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.searcher_api import SearcherApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.services_manager_api import ServicesManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.tasks_manager_api import TasksManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.users_manager_api import UsersManagerApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.utils_api import UtilsApi
from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.api.vos_manager_api import VosManagerApi
