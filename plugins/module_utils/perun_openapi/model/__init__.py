# we can not import model classes here because that would create a circular
# reference which would not work in python2
# do not import all models into this module because that uses a lot of memory and stack frames
# if you need the ability to import all models from one package, import them with
# from ansible_collections.simonbrauner.perun.plugins.module_utils.perun_openapi.models import ModelA, ModelB
