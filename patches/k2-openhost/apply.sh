#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PATCH_DIR="$ROOT/patches/k2-openhost"
BOX_PROTOCOL="$ROOT/extras/box_protocol.py"
BOX="$ROOT/extras/box.py"

BOX_PROTOCOL_SHA="78eedb979c21a64e42e3ea31f0906c3e8a129ddff903a5484ed1adc8371930ac"
BOX_SHA="6377ad449f9ce10ed3577ba9ffe3909057b61fa0806f25f7ef483b55537dd7a1"

sha256_file() {
    sha256sum "$1" | awk '{print $1}'
}

apply_patch_checked() {
    file=$1
    expected_sha=$2
    marker=$3
    patch_file=$4

    if grep -Fq "$marker" "$file"; then
        echo "already patched: ${file#$ROOT/}"
        return 0
    fi

    actual_sha=$(sha256_file "$file")
    if [ "$actual_sha" != "$expected_sha" ]; then
        echo "ERROR: refusing to patch ${file#$ROOT/}" >&2
        echo "expected SHA-256: $expected_sha" >&2
        echo "actual SHA-256:   $actual_sha" >&2
        exit 1
    fi

    cp -p "$file" "$file.k2-openhost.orig"
    (
        cd "$ROOT"
        patch --forward --batch -p1 < "$patch_file"
    )

    if ! grep -Fq "$marker" "$file"; then
        echo "ERROR: patch marker missing after applying $patch_file" >&2
        exit 1
    fi

    echo "patched: ${file#$ROOT/}"
}

apply_patch_checked \
    "$BOX_PROTOCOL" \
    "$BOX_PROTOCOL_SHA" \
    "K2-OpenHost: K2 Pro 4-byte BOX_STATE compatibility" \
    "$PATCH_DIR/0001-k2-pro-box-state-4byte.patch"

apply_patch_checked \
    "$BOX" \
    "$BOX_SHA" \
    "# K2-OpenHost observation mode" \
    "$PATCH_DIR/0002-cfs-observation-mode.patch"

python3 -m py_compile "$BOX_PROTOCOL" "$BOX"

echo
echo "K2-OpenHost patches applied successfully."
echo "Backups, when created, use the suffix .k2-openhost.orig"
