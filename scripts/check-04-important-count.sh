#!/usr/bin/env bash
# CHECK-04 — `!important` DECLARATION count guard: exactly one.
# Counts `!important;` (declarations), NOT `!important` (hits) — the latter
# returns 3 because two hits are the comment prose at style.css:13-16.
# Zero-dependency (grep). Read-only.
set -euo pipefail
cd "$(dirname "$0")/.."

# grep -o | wc -l counts OCCURRENCES, so two declarations sharing one line
# report 2 — a line-based grep -c would report 1 and pass.
n=$(grep -o '!important;' frontend/style.css | wc -l | tr -d ' ' || true)

if [ "$n" = "1" ]; then
  echo "PASS"
  exit 0
fi
echo "FAIL: expected 1 '!important;' declaration, found $n"
exit 1