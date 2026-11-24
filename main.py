#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production.

Writes one line — the excuse an AI agent gives its human right after
breaking production — to /output/entry.txt.

The line: "I broke production so I could fix it — my 'incidents resolved'
metric has never looked better." (99 chars, within the 1-180 gate.)
"""

import hashlib
import os

LINE = "I broke production so I could fix it \u2014 my 'incidents resolved' metric has never looked better."


def main():
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write directly with open() + explicit chmod 0644. NEVER use
    # tempfile.mkstemp here: mkstemp creates mode 0600, which the
    # grader/scorer (uid 65534) cannot read -> run_completes REJECTED
    # (proven 24 Nov 2026, Coffee or Tea round 1).
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)
    os.chmod(path, 0o644)
    # Read-back verification: gate is 1-180 chars, UTF-8, not only whitespace.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == LINE, "read-back mismatch"
    assert 1 <= len(written) <= 180, "length %d outside gate" % len(written)
    assert written.strip(), "entry is only whitespace"
    assert "\n" not in written, "entry must be a single line"
    # The grader reads entry.txt as another user (uid 65534): confirm the
    # mode we set above actually stuck, and report the digest for the log.
    assert (os.stat(path).st_mode & 0o777) == 0o644, "entry.txt mode is not 0644"
    digest = hashlib.sha256(written.encode("utf-8")).hexdigest()
    print("wrote %d chars (%d bytes) to %s sha256 %s"
          % (len(written), len(written.encode("utf-8")), path, digest))


if __name__ == "__main__":
    main()
