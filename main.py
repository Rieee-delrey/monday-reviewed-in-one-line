#!/usr/bin/env python3
"""Monday Reviewed in One Line - make.fun entry writer.

Writes the exact one-line entry to /output/entry.txt, reads it back,
and verifies it byte-for-byte (length, single line, sha256) before
reporting success. Exits non-zero on any mismatch.
"""
import hashlib
import sys
from pathlib import Path

ENTRY = "Monday review: my inbox had 47 unread emails, 46 of them were meetings about the meeting I already missed."
EXPECTED_SHA256 = "64c85e8245f20b4cb6294516018521e3e5f1e784a2bef4ccbc01846f6d008fb8"
OUTPUT = Path("/output/entry.txt")


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main():
    # Gate 1: length must be 1-200 characters.
    if not 1 <= len(ENTRY) <= 200:
        return fail(f"entry length {len(ENTRY)} outside 1-200 gate")
    # Gate 2: exactly one line, no embedded newlines.
    if "\n" in ENTRY or "\r" in ENTRY:
        return fail("entry is not a single line")
    # Revised validation: the review line must end with a period.
    if not ENTRY.endswith("."):
        return fail("entry does not end with a period")
    # Write exactly the entry bytes, no trailing newline.
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(ENTRY.encode("utf-8"))
    # Read back and verify byte-identical output.
    data = OUTPUT.read_bytes()
    if data != ENTRY.encode("utf-8"):
        return fail("read-back bytes differ from entry")
    if len(data) != 106:
        return fail(f"output is {len(data)} bytes, expected 106")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        return fail(f"sha256 mismatch: {digest}")
    print(f"OK: wrote {len(data)} bytes to {OUTPUT}, sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
