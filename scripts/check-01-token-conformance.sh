#!/usr/bin/env bash
# CHECK-01 — token conformance: zero bare #hex outside the fenced :root block.
# Zero-dependency (awk + grep). Read-only. PASS: prints "PASS" and exits 0.
set -euo pipefail
cd "$(dirname "$0")/.."

# The awk state machine drops every line between the two fence comments, so the
# primitives' literals inside :root are not counted. grep -c counts matching
# LINES; note it exits 1 when the count is 0, so we read stdout, never $?.
n=$(awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css \
  | grep -c '#[0-9a-fA-F]\{3,6\}' || true)

if [ "$n" = "0" ]; then
  echo "PASS"
  exit 0
fi
echo "FAIL: $n bare hex outside the token block"
exit 1