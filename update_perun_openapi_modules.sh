#!/usr/bin/env sh

IMPORT_PREFIX="ansible_collections.simonbrauner.perun.plugins.module_utils."

PERUN_SOURCE="https://gitlab.ics.muni.cz/perun/perun-idm/perun.git"
PERUN_OPENAPI_DIR_NAME="perun_openapi"
PERUN_OPENAPI_README_NAME="perun_openapi_README.md"

PERUN_OPENAPI_DIR="$(pwd)/plugins/module_utils/$PERUN_OPENAPI_DIR_NAME"
TMP_DIR="$(mktemp -d /tmp/perun_openapi.XXXXXX)"

rm -rf "$PERUN_OPENAPI_DIR"

git clone --depth 1 "$PERUN_SOURCE" "$TMP_DIR"
cd "$TMP_DIR/perun-cli-python"

sh "generate.sh"

MATCH="^(from |import )$PERUN_OPENAPI_DIR_NAME"
find "$PERUN_OPENAPI_DIR_NAME" -name "*.py" -exec sed -E -i \
    "s/$MATCH/\1$IMPORT_PREFIX$PERUN_OPENAPI_DIR_NAME/" {} +

cp -r "$PERUN_OPENAPI_DIR_NAME" "$PERUN_OPENAPI_DIR"
cp "$PERUN_OPENAPI_README_NAME" "$PERUN_OPENAPI_DIR/README.md"

COPYRIGHT="Copyright (c) 2010-2024, CESNET, CERIT-SC, Masaryk University. All rights reserved."
sed -i "1i # $COPYRIGHT" "perun/oidc/__init__.py"
cp -r "perun/oidc" "$PERUN_OPENAPI_DIR"

rm -rf "$TMP_DIR"
