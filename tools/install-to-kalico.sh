#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SOURCE_EXTRAS="$ROOT/extras"
TARGET="${1:-/home/alfio/kalico}"
TARGET_EXTRAS="$TARGET/klippy/extras"
DRY_RUN=0

if [[ "${2:-}" == "--dry-run" || "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
  if [[ "${1:-}" == "--dry-run" ]]; then
    TARGET="/home/alfio/kalico"
    TARGET_EXTRAS="$TARGET/klippy/extras"
  fi
fi

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

[[ -f "$TARGET/klippy/klippy.py" ]] || fail "Kalico clone not found at $TARGET"
[[ -d "$TARGET_EXTRAS" ]] || fail "Kalico extras directory not found: $TARGET_EXTRAS"
[[ -f "$SOURCE_EXTRAS/manifest.json" ]] || fail "K2 extras manifest missing"
[[ -f "$SOURCE_EXTRAS/box.py" ]] || fail "K2 box.py missing"
[[ -f "$SOURCE_EXTRAS/box_protocol.py" ]] || fail "K2 box_protocol.py missing"

grep -Fq "# K2-OpenHost observation mode" "$SOURCE_EXTRAS/box.py" \
  || fail "source box.py is not the validated K2-OpenHost version"

grep -Fq "K2-OpenHost: K2 Pro 4-byte BOX_STATE compatibility" "$SOURCE_EXTRAS/box_protocol.py" \
  || fail "source box_protocol.py is not the validated K2-OpenHost version"

SOURCE_COMMIT="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
SOURCE_BRANCH="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
KALICO_COMMIT="$(git -C "$TARGET" rev-parse HEAD 2>/dev/null || echo unknown)"

if [[ "$SOURCE_BRANCH" != "k2-openhost" && "$SOURCE_BRANCH" != "HEAD" ]]; then
  echo "WARNING: source branch is '$SOURCE_BRANCH', expected 'k2-openhost'."
fi

mapfile -t FILES < <(
  python3 - "$SOURCE_EXTRAS/manifest.json" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
for name in sorted(data.get('files', {})):
    print(name)
PY
)

[[ ${#FILES[@]} -gt 0 ]] || fail "manifest contains no files"

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$TARGET/.k2-openhost-backups/$STAMP"
RECEIPT="$TARGET/.k2-openhost-install.txt"

copy_one() {
  local name="$1"
  local src="$SOURCE_EXTRAS/$name"
  local dst="$TARGET_EXTRAS/$name"

  [[ -f "$src" ]] || fail "manifest entry missing from source: $name"

  if [[ -f "$dst" ]] && cmp -s "$src" "$dst"; then
    echo "unchanged: klippy/extras/$name"
    return 0
  fi

  if [[ -e "$dst" ]]; then
    echo "replace:   klippy/extras/$name"
    if [[ $DRY_RUN -eq 0 ]]; then
      mkdir -p "$BACKUP_DIR"
      cp -a "$dst" "$BACKUP_DIR/$name"
    fi
  else
    echo "install:   klippy/extras/$name"
  fi

  if [[ $DRY_RUN -eq 0 ]]; then
    cp -a "$src" "$dst"
  fi
}

echo "=== K2-OpenHost -> Kalico overlay ==="
echo "source:       $ROOT"
echo "source branch:$SOURCE_BRANCH"
echo "source commit:$SOURCE_COMMIT"
echo "kalico:       $TARGET"
echo "kalico commit:$KALICO_COMMIT"
echo "files:        ${#FILES[@]}"
echo "dry-run:      $DRY_RUN"
echo

for name in "${FILES[@]}"; do
  copy_one "$name"
done

if [[ $DRY_RUN -eq 1 ]]; then
  echo
  echo "DRY RUN complete. No files were changed."
  exit 0
fi

mapfile -t PYFILES < <(
  for name in "${FILES[@]}"; do
    [[ "$name" == *.py ]] && printf '%s\n' "$TARGET_EXTRAS/$name"
  done
)

python3 -m py_compile "${PYFILES[@]}"

{
  echo "K2-OpenHost overlay installation"
  echo "installed_at=$STAMP"
  echo "source_repo=MzTechnology97/k2-pro-custom-firmware"
  echo "source_branch=$SOURCE_BRANCH"
  echo "source_commit=$SOURCE_COMMIT"
  echo "kalico_path=$TARGET"
  echo "kalico_commit=$KALICO_COMMIT"
  echo "backup_dir=$BACKUP_DIR"
  echo "files=${#FILES[@]}"
  printf 'file=%s\n' "${FILES[@]}"
} > "$RECEIPT"

echo
echo "Overlay installed successfully."
echo "Receipt: $RECEIPT"
if [[ -d "$BACKUP_DIR" ]]; then
  echo "Backups: $BACKUP_DIR"
else
  echo "Backups: none required"
fi
