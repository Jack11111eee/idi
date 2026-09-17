#!/usr/bin/env bash
# CHECK-04 — `!important` DECLARATION count guard: exactly one.
# Counts `!important;` (declarations), NOT `!important` (hits) — the latter
# returns 3 because two hits are the comment prose at style.css:13-16.
# Zero-dependency (grep). Read-only.
set -euo pipefail
cd "$(dirname "$0")/.."

n=$(grep -c '!important;' frontend/style.css || true)

if [ "$n" = "1" ]; then
  echo "PASS"
  exit 0
fi
echo "FAIL: expected 1 '!important;' declaration, found $n"
exit 1