"""Build the New Recruit data files and sanity-check them.

    python3 tools/build.py                 # everything
    python3 tools/build.py "XV - Thousand Sons" solar_auxilia   # only these catalogues (plus the .gst)

Writes 'Prohammer 30k.gst', one 'Legiones Astartes - <Legion>.cat' per Legion and one .cat per other army
(tools/armies/*.py) to the repository root. Every catalogue is built in its own process, so modules can change
shared data freely.
"""
import glob
import importlib
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "data"))

import bsx  # noqa: E402

SPECIAL_CHILD_IDS = {"model", "unit", "upgrade", "any"}
NON_ID_FIELDS = {"selections", "forces", "hidden", "name", "category", "defaultSelectionEntryId",
                 "annotation", "description", "error", "warning", "info", bsx.PTS}


def legion_modules():
    """{legion name: module name} for every module in tools/legions/."""
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, "legions", "*.py"))):
        name = os.path.basename(f)[:-3]
        if name in ("__init__", "common"):
            continue
        m = importlib.import_module("legions." + name)
        out[m.LEGION] = "legions." + name
    return out


def army_modules():
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, "armies", "*.py"))):
        name = os.path.basename(f)[:-3]
        if name.startswith("_") or name == "common":
            continue
        out[name] = "armies." + name
    return out


def check(roots):
    ids, errors = {}, []
    for fname, r in roots:
        seen = set()
        for e in r.iter():
            i = e.get("id")
            if i:
                if i in seen:
                    errors.append(f"duplicate id {i} ({e.tag.split('}')[-1]} {e.get('name')}) in {fname}")
                seen.add(i)
                ids.setdefault(i, fname)
    for fname, r in roots[1:]:
        for e in r.iter():
            for attr in ("targetId", "typeId", "childId", "defaultSelectionEntryId"):
                v = e.get(attr)
                if v and v not in SPECIAL_CHILD_IDS and v not in ids:
                    errors.append(f"{fname}: {e.tag.split('}')[-1]} {e.get('name', '')} -> unknown {attr} {v}")
            tag = e.tag.split("}")[-1]
            if tag in ("condition", "repeat", "constraint"):
                s = e.get("scope")
                if s not in ("self", "parent", "force", "roster", "ancestor", "primary-catalogue") and s not in ids:
                    errors.append(f"{fname}: {tag} unknown scope {s}")
            if tag == "modifier":
                f = e.get("field")
                if f not in NON_ID_FIELDS and f not in ids:
                    errors.append(f"{fname}: modifier targets unknown field {f}")
                if f == "category" and e.get("value") not in ids:
                    errors.append(f"{fname}: modifier adds unknown category {e.get('value')}")
    return errors


def build_one(kind, name):
    """Runs in a child process: build one catalogue, write it, check it against the .gst."""
    import gamesystem
    if kind == "legion":
        import legiones
        mods = legion_modules()
        module = importlib.import_module(mods[name]) if name in mods else None
        root = legiones.build(name, module)
        out = root.get("name") + ".cat"
    else:
        module = importlib.import_module(army_modules()[name])
        root = module.build()
        out = root.get("name") + ".cat"
    path = os.path.join(ROOT, out)
    bsx.write(root, path)
    gst = ET.parse(os.path.join(ROOT, "Prohammer 30k.gst")).getroot()
    cat = ET.parse(path).getroot()
    errors = check([("Prohammer 30k.gst", gst), (out, cat)])
    n = sum(1 for _ in cat.iter())
    print(f"{out}: {n} elements, {os.path.getsize(path) // 1024} KB")
    for e in errors[:40]:
        print("  " + e)
    if len(errors) > 40:
        print(f"  ... {len(errors) - 40} more")
    return 1 if errors else 0


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--one":
        sys.exit(build_one(sys.argv[2], sys.argv[3]))
    import gamesystem
    from legiones_wargear import LEGIONS
    bsx.write(gamesystem.build(), os.path.join(ROOT, "Prohammer 30k.gst"))
    wanted = sys.argv[1:]
    jobs = [("legion", l) for l in LEGIONS] + [("army", a) for a in army_modules()]
    if wanted:
        jobs = [j for j in jobs if j[1] in wanted]

    def run(job):
        p = subprocess.run([sys.executable, __file__, "--one", *job], capture_output=True, text=True)
        return job, p.returncode, p.stdout + p.stderr

    failed = 0
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        for job, rc, out in ex.map(run, jobs):
            print(out.rstrip())
            failed += rc != 0
    if failed:
        print(f"\n{failed} catalogue(s) with problems.")
        sys.exit(1)
    print("\nAll references resolve.")


if __name__ == "__main__":
    main()
