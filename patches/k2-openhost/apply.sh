#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

python3 "$ROOT/patches/k2-openhost/apply.py"

echo
echo "K2-OpenHost validated patchset applied successfully."
echo "Backups, when created, use the suffix .k2-openhost.orig"
