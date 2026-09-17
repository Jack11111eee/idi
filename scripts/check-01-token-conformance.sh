#!/usr/bin/env bash
# CHECK-01 — token conformance: zero bare #hex outside the fenced :root block.
# Zero-dependency (awk + grep). Read-only. PASS: prints "PASS" and exits 0.
set -euo pipefail
cd "$(dirname "$0")/.."

# Assert the input before counting: a missing/unreadable file must FAIL loudly.
# Without this, awk's diagnostic goes to stderr, grep reads empty input and
# reports 0, and the guard prints PASS for a file it never read.
[ -f frontend/style.css ] || { echo "FAIL: frontend/style.css not found"; exit 1; }

# The fence is a pair of free-text comment markers; assert the pair before
# trusting it. Without this, a removed/renamed END marker leaves awk's `f` at 1
# to EOF, the whole tail counts as "inside the fence", and the guard goes
# vacuous. (check-02-contrast.py asserts the same pair.)
starts=$(grep -c '===== DESIGN TOKENS: START' frontend/style.css || true)
ends=$(grep -c '===== DESIGN TOKENS: END' frontend/style.css || true)
[ "$starts" = "1" ] && [ "$ends" = "1" ] \
  || { echo "FAIL: expected exactly 1 fence START and 1 fence END, found $starts/$ends"; exit 1; }

# The awk state machine drops every line between the two fence comments, so the
# primitives' literals inside :root are not counted. awk runs as its own command
# so its failure status aborts the script (set -e) instead of masquerading as a
# count. grep -o | wc -l counts OCCURRENCES, not lines, so a line carrying two
# hexes reports 2. grep exits 1 on a zero count, hence the || true.
outside=$(awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css)
n=$(printf '%s\n' "$outside" | grep -o '#[0-9a-fA-F]\{3,6\}' | wc -l | tr -d ' ' || true)

if [ "$n" = "0" ]; then
  echo "PASS"
  exit 0
fi
echo "FAIL: $n bare hex outside the token block"
exit 1