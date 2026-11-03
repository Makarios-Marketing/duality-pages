#!/usr/bin/env python3
"""Global sections for the Duality preview pages.

The shared blocks live in _globals/ (one file each). Every page marks where a
block goes with <!-- GLOBAL:name START --> ... <!-- GLOBAL:name END -->.

    python3 sync_globals.py           # copy every _globals/*.html into every page
    python3 sync_globals.py --check   # list pages whose block differs, change nothing

Edit the block in _globals/, run the script, commit. GitHub Pages skips the
underscore folder, so the block files themselves are never published.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GLOBALS = os.path.join(HERE, "_globals")


def marker_re(name):
    return re.compile(
        r"(<!-- GLOBAL:%s START -->)(.*?)(<!-- GLOBAL:%s END -->)" % (name, name), re.S
    )


def main():
    check = "--check" in sys.argv
    blocks = {
        os.path.splitext(os.path.basename(p))[0]: open(p, encoding="utf-8").read().strip("\n")
        for p in sorted(glob.glob(os.path.join(GLOBALS, "*.html")))
    }
    pages = sorted(p for p in glob.glob(os.path.join(HERE, "*.html")) if not p.endswith("index.html"))
    changed = 0
    for page in pages:
        text = open(page, encoding="utf-8").read()
        new = text
        for name, block in blocks.items():
            new = marker_re(name).sub(lambda m: m.group(1) + "\n" + block + "\n" + m.group(3), new)
        if new != text:
            changed += 1
            print(("differs: " if check else "updated: ") + os.path.basename(page))
            if not check:
                open(page, "w", encoding="utf-8").write(new)
    for name in blocks:
        using = [os.path.basename(p) for p in pages if "GLOBAL:%s START" % name in open(p, encoding="utf-8").read()]
        print("%-8s used on %d pages" % (name, len(using)))
    print(("%d page(s) out of sync" if check else "%d page(s) updated") % changed)


if __name__ == "__main__":
    main()
