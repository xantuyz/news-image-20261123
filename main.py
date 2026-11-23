#!/usr/bin/env python3
"""news-image-20261123 entrypoint (Python 3.13, standard library only).

The image is rendered at build time by render.py and shipped in this
repository as entry.png. This program only copies that file to the output
directory and verifies its SHA-256, so it runs in the grader sandbox,
which installs nothing.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = (
    "dda2d81df2e933c4755b29eaa79f9a7d8af6b055ea9dea21d246554dac31a828"
)
SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    got = sha256_of(dest)
    if got != EXPECTED_SHA256:
        print("sha256 mismatch: %s != %s" % (got, EXPECTED_SHA256),
              file=sys.stderr)
        return 1
    print("entry.png written to %s sha256=%s" % (dest, got))
    return 0


if __name__ == "__main__":
    sys.exit(main())
