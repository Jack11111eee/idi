#!/usr/bin/env python3
"""CHECK-02 — WCAG contrast verification for the design-token layer.

Zero-dependency: python3 standard library only. Read-only: it never writes a
file and never runs git.

Pairs are derived from the contrast manifest written as comments inside the
fenced `:root` block of frontend/style.css — the same diff that declares the
tokens, so a drift between the manifest and the tokens is visible in review.
A manifest entry naming a token that is not declared in the fence (or an
ordering entry naming a pair that is not listed) is a contract-drift signal
and fails loudly; it is never silently skipped.

Thresholds are the WCAG constants: 4.5:1 for TEXT, 3:1 for NON-TEXT. The
comparison is closed-interval and the ratio is never rounded to the threshold
first — 4.496 fails, 4.504 passes.

Exit status: 0 when no failures, 1 otherwise.
"""
import re
import sys

CSS_PATH = "frontend/style.css"
TEXT_MIN = 4.5
NON_TEXT_MIN = 3.0

DECL_RE = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")
PAIR_RE = re.compile(
    r"/\*\s*PAIR\s+(--[a-z0-9-]+)\s+ON\s+(--[a-z0-9-]+)\s+"
    r"(TEXT|NON-TEXT)(?:@([0-9.]+))?\s*\*/"
)
ORDER_RE = re.compile(
    r"/\*\s*ORDER\s+(--[a-z0-9-]+)\s+BEFORE\s+(--[a-z0-9-]+)\s+"
    r"ON\s+(--[a-z0-9-]+)\s*\*/"
)
HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
RGBA_RE = re.compile(
    r"^rgba?\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)"
    r"\s*(?:,\s*([0-9.]+)\s*)?\)$"
)
VAR_RE = re.compile(r"^var\(\s*(--[a-z0-9-]+)\s*\)$")


def read_fence(path):
    """Return the text between the two DESIGN TOKENS fence comments."""
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()

    starts = sum(1 for line in lines if "===== DESIGN TOKENS: START" in line)
    ends = sum(1 for line in lines if "===== DESIGN TOKENS: END" in line)
    if starts != 1 or ends != 1:
        print(
            "FAIL: expected exactly 1 fence START and 1 fence END, found %d/%d"
            % (starts, ends)
        )
        sys.exit(1)

    out = []
    inside = False
    for line in lines:
        if "===== DESIGN TOKENS: START" in line:
            inside = True
            continue
        if "===== DESIGN TOKENS: END" in line:
            inside = False
            continue
        if inside:
            out.append(line)
    return "\n".join(out)


def parse_decls(fence):
    """Map every declared custom property inside the fence to its raw value."""
    return {m.group(1): m.group(2).strip() for m in DECL_RE.finditer(fence)}


def resolve(name, decls, seen=()):
    """Resolve a token name to an (r, g, b, a) tuple, or fail loudly."""
    if name not in decls:
        print("FAIL: unknown token %s" % name)
        sys.exit(1)
    if name in seen:
        print("FAIL: circular var() chain at %s" % name)
        sys.exit(1)
    value = decls[name]

    chained = VAR_RE.match(value)
    if chained:
        return resolve(chained.group(1), decls, seen + (name,))

    hexed = HEX_RE.match(value)
    if hexed:
        digits = hexed.group(1)
        if len(digits) == 3:
            digits = "".join(c * 2 for c in digits)
        return (int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16), 1.0)

    rgba = RGBA_RE.match(value)
    if rgba:
        rgb = tuple(int(round(float(rgba.group(i)))) for i in (1, 2, 3))
        alpha = float(rgba.group(4)) if rgba.group(4) is not None else 1.0
        return rgb + (alpha,)

    print("FAIL: unparsable value for %s: %s" % (name, value))
    sys.exit(1)


def channel_luminance(channel):
    """sRGB inverse gamma for one 0-255 channel."""
    c = channel / 255.0
    if c <= 0.03928:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    r, g, b = rgb[:3]
    return (
        0.2126 * channel_luminance(r)
        + 0.7152 * channel_luminance(g)
        + 0.0722 * channel_luminance(b)
    )


def composite(fg, bg, alpha):
    """Composite fg over bg per channel in 8-bit sRGB."""
    return tuple(int(round(alpha * fg[i] + (1.0 - alpha) * bg[i])) for i in range(3))


def contrast_ratio(fg, bg):
    lf, lb = relative_luminance(fg), relative_luminance(bg)
    light, dark = max(lf, lb), min(lf, lb)
    return (light + 0.05) / (dark + 0.05)


def main():
    fence = read_fence(CSS_PATH)
    decls = parse_decls(fence)

    failures = 0
    text_pairs = {}  # (fg, bg) -> ratio, for non-alpha TEXT pairs (ORDER operands)
    order_lines = []

    # Coverage floor: an empty or truncated manifest would otherwise satisfy
    # "failures == 0" trivially. Floors are >=24 pairs, >=20 TEXT, >=4 NON-TEXT.
    pairs = list(PAIR_RE.finditer(fence))
    orders = list(ORDER_RE.finditer(fence))
    text_n = sum(1 for m in pairs if m.group(3) == "TEXT")
    nontext_n = len(pairs) - text_n
    if len(pairs) < 24 or text_n < 20 or nontext_n < 4:
        print(
            "FAIL: manifest coverage %d pairs (%d TEXT / %d NON-TEXT) below floor 24/20/4"
            % (len(pairs), text_n, nontext_n)
        )
        sys.exit(1)

    # Every "/* PAIR" / "/* ORDER" marker must parse. An entry the regex cannot
    # match would otherwise be dropped silently, so the docstring's "never
    # silently skipped" promise only holds if the raw marker count equals the
    # parsed count.
    raw_pairs = fence.count("/* PAIR")
    if raw_pairs != len(pairs):
        print(
            "FAIL: %d '/* PAIR' markers but only %d parsed — malformed manifest entry"
            % (raw_pairs, len(pairs))
        )
        sys.exit(1)

    raw_orders = fence.count("/* ORDER")
    if raw_orders != len(orders):
        print(
            "FAIL: %d '/* ORDER' markers but only %d parsed — malformed manifest entry"
            % (raw_orders, len(orders))
        )
        sys.exit(1)

    for match in pairs:
        fg_name, bg_name, kind, alpha = match.groups()
        fg = resolve(fg_name, decls)
        bg = resolve(bg_name, decls)
        # Composite whenever the foreground carries alpha — either from the
        # token's own value or from the entry's @<alpha> suffix. contrast_ratio
        # reads only rgb[:3], so skipping this would score rgba(0,0,0,0.45) as
        # fully opaque (21.00 instead of the true 3.36).
        token_alpha = fg[3]
        fg_alpha = token_alpha * float(alpha) if alpha is not None else token_alpha
        if fg_alpha < 1.0:
            fg = composite(fg, bg, fg_alpha)

        value = contrast_ratio(fg, bg)
        threshold = TEXT_MIN if kind == "TEXT" else NON_TEXT_MIN
        label = "%s on %s" % (fg_name, bg_name)
        if alpha is not None:
            label += "@%s" % alpha
        elif token_alpha < 1.0:
            label += "@%s" % token_alpha

        if value >= threshold:
            print("PASS  %.2f  %s" % (value, label))
        else:
            print("FAIL  %.2f  %s  (need >= %.1f)" % (value, label, threshold))
            failures += 1

        if kind == "TEXT" and alpha is None:
            text_pairs[(fg_name, bg_name)] = value

    for match in orders:
        quieter, louder, bg = match.groups()
        missing = [n for n in (quieter, louder) if (n, bg) not in text_pairs]
        if missing:
            for name in missing:
                print("FAIL: unknown pair %s ON %s" % (name, bg))
            sys.exit(1)

        q, l = text_pairs[(quieter, bg)], text_pairs[(louder, bg)]
        metric = q / l
        if q < l:
            order_lines.append(
                "ORDER %.3f  %s before %s on %s" % (metric, quieter, louder, bg)
            )
        else:
            order_lines.append(
                "FAIL: hierarchy inverted  %.3f  %s not before %s on %s  "
                "(need < 1.000)" % (metric, quieter, louder, bg)
            )
            failures += 1

    for line in order_lines:
        print(line)

    if failures:
        print("FAIL: %d failures" % failures)
        sys.exit(1)

    print("PASS: 0 failures")
    sys.exit(0)


if __name__ == "__main__":
    main()