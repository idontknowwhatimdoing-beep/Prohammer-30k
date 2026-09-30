"""Build the New Recruit data files and sanity-check them.

    python3 tools/build.py

Writes 'Prohammer 30k.gst' and 'Legiones Astartes.cat' to the repository root.
"""
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import bsx  # noqa: E402
import gamesystem  # noqa: E402
import legiones  # noqa: E402

OUTPUTS = [
    (gamesystem.build, "Prohammer 30k.gst"),
    (legiones.build, "Legiones Astartes.cat"),
]
SPECIAL_CHILD_IDS = {"model", "unit", "upgrade", "any"}
NON_ID_FIELDS = {"selections", "forces", "hidden", "name", "category", "defaultSelectionEntryId",
                 "annotation", "description", "error", "warning", "info", bsx.PTS}


def check(roots):
    ids, errors = {}, []
    for fname, r in roots:
        for e in r.iter():
            i = e.get("id")
            if i:
                if i in ids:
                    errors.append(f"duplicate id {i} ({e.tag} {e.get('name')}) in {fname} and {ids[i]}")
                ids[i] = fname
    for fname, r in roots:
        for e in r.iter():
            for attr in ("targetId", "typeId", "childId", "defaultSelectionEntryId"):
                v = e.get(attr)
                if v and v not in SPECIAL_CHILD_IDS and v not in ids:
                    errors.append(f"{fname}: {e.tag} {e.get('name', '')} -> unknown {attr} {v}")
            tag = e.tag.split("}")[-1]
            if tag in ("condition", "repeat", "constraint"):
                s = e.get("scope")
                if s not in ("self", "parent", "force", "roster", "ancestor") and s not in ids:
                    errors.append(f"{fname}: {e.tag} unknown scope {s}")
            if tag == "modifier":
                f = e.get("field")
                if f not in NON_ID_FIELDS and f not in ids:
                    errors.append(f"{fname}: modifier targets unknown field {f}")
                if f == "category" and e.get("value") not in ids:
                    errors.append(f"{fname}: modifier adds unknown category {e.get('value')}")
    return errors


def main():
    roots = []
    for fn, out in OUTPUTS:
        r = fn()
        bsx.write(r, os.path.join(ROOT, out))
        roots.append((out, ET.parse(os.path.join(ROOT, out)).getroot()))
    errors = check(roots)
    for fname, r in roots:
        n = sum(1 for _ in r.iter())
        print(f"{fname}: {n} elements, {os.path.getsize(os.path.join(ROOT, fname)) // 1024} KB")
    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors[:60]:
            print("  " + e)
        sys.exit(1)
    print("All references resolve.")


if __name__ == "__main__":
    main()
