# Perun Ansible Collection

Ansible collection for managing [Perun](https://perun-aai.org/) systems, developed as a part of a [bachelor's thesis](https://is.muni.cz/th/vhcyr/).

## External Code

This collection contains [Python modules generated from Perun's API](https://gitlab.ics.muni.cz/perun/perun-idm/perun/-/tree/48cbaf46474ca82d221815ca70919fdcd5dcd073/perun-cli-python) in the folder `plugins/module_utils/perun_openapi/`. The imports are downloaded and modified by the script `generate_perun_openapi_modules.sh` to make the modules accessible to Ansible.

The file `plugins/module_utils/oidc/__init__.py` is directly copied from the [Perun GitLab repository](https://gitlab.ics.muni.cz/perun/perun-idm/perun/-/blob/48cbaf46474ca82d221815ca70919fdcd5dcd073/perun-cli-python/perun/oidc/__init__.py) and modified to work better with Ansible and to remove unnecessary dependencies.

## Dependencies

The collection depends on the dependencies of the [previously mentioned generated modules](https://gitlab.ics.muni.cz/perun/perun-idm/perun/-/tree/48cbaf46474ca82d221815ca70919fdcd5dcd073/perun-cli-python#installation), with the exceptions of `openjdk-17-jdk-headless`, `qrencode`, and `python3-typer`.
