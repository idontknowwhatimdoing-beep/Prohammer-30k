"""Static check of the allied-detachment data in the generated files.

    python3 tools/check_allies.py
"""
import glob
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "data"))
import allies  # noqa: E402

NS = "{http://www.battlescribe.net/schema/catalogueSchema}"


def main():
    problems = []
    gst = ET.parse(os.path.join(ROOT, "Prohammer 30k.gst")).getroot()
    forces = {f.get("id"): f.get("name") for f in gst.iter() if f.tag.endswith("forceEntry")}
    for fid in (allies.PRIMARY_FORCE, allies.ALLIED_FORCE):
        if fid not in forces:
            problems.append(f"game system: force entry {fid} missing")
    cats = {c.get("id") for c in gst.iter() if c.tag.endswith("categoryEntry")}
    for n, cid in allies.army_categories():
        if cid not in cats:
            problems.append(f"game system: category {n} missing")

    sworn_expected = 0
    pairs = allies.sworn_pairs()
    sworn_found = 0
    rite_errors = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "*.cat"))):
        r = ET.parse(path).getroot()
        name = r.get("name")
        if name not in allies.CATALOGUES:
            problems.append(f"{name}: not in allies.CATALOGUES")
            continue
        alleg = [e for e in r.iter(NS + "selectionEntry") if e.get("id") == allies.ALLEGIANCE_ENTRY]
        if len(alleg) != 1:
            problems.append(f"{name}: {len(alleg)} Allegiance entries")
            continue
        a = alleg[0]
        cons = [c for c in a.iter(NS + "constraint") if c.get("type") == "min" and c.get("scope") == "force"]
        if not cons:
            problems.append(f"{name}: Allegiance entry not mandatory in a force")
        links = [c.get("targetId") for c in a.iter(NS + "categoryLink")]
        if allies.army_cat(name) not in links:
            problems.append(f"{name}: army marker missing")
        errs = [m.get("value") for m in a.iter(NS + "modifier") if m.get("field") == "error"]
        found = sum(1 for e in errs if e.startswith("Sworn Enemies"))
        me = allies.CATALOGUES[name]
        exp = 0
        if me:
            for p in pairs:
                if me in p:
                    exp += sum(1 for c, ab in allies.CATALOGUES.items() if ab == (p[1] if p[0] == me else p[0]))
        sworn_expected += exp
        sworn_found += found
        if found != exp:
            problems.append(f"{name}: {found} Sworn-Enemy errors, expected {exp}")
        n_rite = sum(1 for m in r.iter(NS + "modifier") if m.get("field") == "error" and
                     "Allied Detachment" in (m.get("value") or "") and ("may not include" in m.get("value")) and
                     m.get("value").split(":")[0] not in ("Sworn Enemies",))
        rite_errors += n_rite
        print(f"{name}: marker ok, {found} Sworn-Enemy errors, {n_rite} allied-restriction errors")
    print(f"\nSworn-Enemy pairs (symmetric union): {len(pairs)}; errors {sworn_found} (expected {sworn_expected})")
    if problems:
        print("\nPROBLEMS:\n" + "\n".join(problems))
        sys.exit(1)
    print("Allies data OK.")


if __name__ == "__main__":
    main()
