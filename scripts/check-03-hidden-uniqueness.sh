#!/usr/bin/env bash
# CHECK-03 — `.hidden` uniqueness guard: exactly one global `.hidden {` rule.
# `.hidden { display: none !important }` is a mechanism, not styling: five
# elements are hidden only by it. Zero-dependency (grep). Read-only.
set -euo pipefail
cd "$(dirname "$0")/.."

# Match the selector anywhere on the line: a duplicate indented inside a future
# @media / @layer would win the cascade just as surely as a column-0 one, and an
# anchored-to-column-0 pattern would not see it.
n=$(grep -cE '^[[:space:]]*\.hidden[[:space:]]*\{' frontend/style.css || true)

if [ "$n" = "1" ]; then
  echo "PASS"
  exit 0
fi
echo "FAIL: expected 1 '.hidden {' rule, found $n"
exit 1