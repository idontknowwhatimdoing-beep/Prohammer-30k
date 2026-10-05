"""Close combat weapons (and Legion-specific ranged weapons) are always exchanges, never extra weapons.

Author (5 Oct 2026): "all close combat weapons should always exchange a chainsword or any other weapon that the
model would carry; same with all the Legion-specific ranged weapons".

Run on a finished catalogue. For every model that has 'Replace <weapon>' choices, a weapon offered in one of its
add-on groups (an Armoury, 'Sergeant Wargear', a Legion wargear group ...) is moved into the matching Replace choice:
close combat weapons into the slot of its close combat weapon (else its pistol, else any slot), Legion ranged weapons
into the slot of a ranged weapon. If that Replace choice already offers the weapon, the add-on copy is dropped.
Grenades, bombs and charges stay add-ons, as do generic ranged weapons, squad-wide swaps and Techmarine weapons.
"""
import os
import runpy
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

_D = runpy.run_path(os.path.join(HERE, "data", "legiones_wargear.py"))
GENERIC = set(_D["WEAPON_PROFILES"]) | set(_D["WEAPONS"])
NOT_WEAPONS = ("Grenade", "Bomb", "Charge", "Harness", "Ammunition", "Rounds", "Shells", "Missiles")
KEEP_GROUPS = ("Additional Weapon", "Heavy Weapon", "Special Weapon", "Psychic", "Consul", "Servo-automata", ": replace",
               "(any number)", " per ", "(up to", "Retinue")
DONE = []  # (catalogue, model, weapon, action) for the report


def _t(e):
    return e.tag.split("}")[-1]


def _kids(e, tag):
    c = e.find(tag)
    return list(c) if c is not None else []


class Lib:
    def __init__(self, root):
        roots = [root]
        gst = os.path.join(ROOT, "Prohammer 30k.gst")
        if os.path.exists(gst):
            g = ET.parse(gst).getroot()
            for e in g.iter():
                e.tag = _t(e)
            roots.append(g)
        self.entries, self.profiles = {}, {}
        for r in roots:
            for e in r.iter():
                if _t(e) == "selectionEntry":
                    self.entries.setdefault(e.get("id"), e)
                elif _t(e) == "profile" and "Weapon" in (e.get("typeName") or ""):
                    self.profiles.setdefault(e.get("id"), e)

    def weapon_profiles(self, se):
        out = [p for p in _kids(se, "profiles") if "Weapon" in (p.get("typeName") or "")]
        out += [self.profiles[i.get("targetId")] for i in _kids(se, "infoLinks")
                if i.get("targetId") in self.profiles]
        return [p for p in out if "Psychic" not in (p.get("typeName") or "")]

    def weapon(self, item):
        """(target id, name, is_melee) when item (a link or an entry) is a weapon choice, else None."""
        if _t(item) == "entryLink":
            se = self.entries.get(item.get("targetId"))
            tid = item.get("targetId")
        else:
            se, tid = item, item.get("id")
            if not self.weapon_profiles(se):
                inner = _kids(se, "entryLinks")
                if len(inner) == 1 and not _kids(se, "selectionEntries"):
                    tid = inner[0].get("targetId")
                    se = self.entries.get(tid)
        if se is None:
            return None
        name = se.get("name") or ""
        if any(w in name for w in NOT_WEAPONS) and not (name.startswith("Combi-") or "Launcher" in name
                                                        or "Charger" in name):
            return None
        profs = self.weapon_profiles(se)
        if not profs:
            return None
        melee = True
        for p in profs:
            for c in p.iter():
                if _t(c) == "characteristic" and c.get("name") == "Range":
                    v = (c.text or "").strip()
                    if v not in ("-", "", "Melee"):
                        melee = False
        return tid, name, melee


def _is_vehicle(o, lib):
    """Vehicles and weapon batteries keep their own option structure."""
    for p in o.iter():
        if _t(p) == "profile" and any(k in (p.get("typeName") or "") for k in ("Vehicle", "Artillery")):
            return True
    for i in o.findall("infoLinks/infoLink"):
        if i.get("type") == "profile" and "Vehicle" in (i.get("name") or ""):
            return True
    return any(k in (o.get("name") or "") for k in ("Tank", "Battery", "Rhino", "Predator", "Land Raider",
                                                     "Dreadnought", "Speeder", "Gunship", "Javelin"))


def _owner_map(root):
    parent = {c: p for p in root.iter() for c in p}

    def owner(n):
        p = parent.get(n)
        while p is not None and _t(p) != "selectionEntry":
            p = parent.get(p)
        return p
    return parent, owner


def _targets_in(g, lib):
    """Ids and names of everything a slot offers."""
    out = set()
    for e in g.iter():
        if _t(e) in ("entryLink", "selectionEntry"):
            out.add("name:" + (e.get("name") or ""))
        if _t(e) == "entryLink":
            out.add(e.get("targetId"))
        elif _t(e) == "selectionEntry":
            out.add(e.get("id"))
            w = lib.weapon(e)
            if w:
                out.add(w[0])
    return out


def apply(root):
    lib = Lib(root)
    parent, owner = _owner_map(root)
    groups = [g for g in root.iter() if _t(g) == "selectionEntryGroup"]
    by_owner = {}
    for g in groups:
        o = owner(g)
        if o is not None:
            by_owner.setdefault(id(o), (o, []))[1].append(g)
    cat = root.get("name")
    for o, gs in by_owner.values():
        def is_slot(g):
            return g.get("defaultSelectionEntryId") is not None or (g.get("name") or "").startswith("Replace ")
        slots = []
        for g in gs:
            if not is_slot(g):
                continue
            # skip slots nested in other slots (e.g. the pair of claws)
            p, nested = parent.get(g), False
            while p is not None and p is not o:
                if _t(p) == "selectionEntryGroup" and is_slot(p):
                    nested = True
                p = parent.get(p)
            if nested:
                continue
            dflt = g.get("defaultSelectionEntryId")
            d = next((x for x in g.iter() if x.get("id") == dflt), None) if dflt else None
            w = lib.weapon(d) if d is not None else None
            slots.append((g, w))
        if not any(w for _, w in slots) or _is_vehicle(o, lib):
            continue
        melee_slots = [g for g, w in slots if w and w[2]]
        pistol_slots = [g for g, w in slots if w and not w[2] and "Pistol" in w[1]]
        ranged_slots = [g for g, w in slots if w and not w[2] and "Pistol" not in w[1]]
        offered = set()
        for g, _ in slots:
            offered |= _targets_in(g, lib)
        slot_ids = {id(g) for g, _ in slots}
        for g in gs:
            if id(g) in slot_ids or any(k in (g.get("name") or "") for k in KEEP_GROUPS):
                continue
            # an add-on group must not sit inside a slot
            p, inside = parent.get(g), False
            while p is not None and p is not o:
                if id(p) in slot_ids:
                    inside = True
                p = parent.get(p)
            if inside:
                continue
            for cont in ("entryLinks", "selectionEntries"):
                c = g.find(cont)
                if c is None:
                    continue
                for item in list(c):
                    w = lib.weapon(item)
                    if not w:
                        continue
                    tid, name, melee = w
                    if melee:
                        dest = (melee_slots or pistol_slots or ranged_slots or [None])[0]
                    elif name not in GENERIC and "Pistol" in name:
                        dest = (pistol_slots or ranged_slots or [None])[0]
                    elif name not in GENERIC:
                        dest = (ranged_slots or pistol_slots or [None])[0]
                    elif tid in offered or "name:" + name in offered:
                        dest = "dup"  # a generic ranged weapon the model can already take as an exchange
                    else:
                        dest = None
                    if dest is None:
                        continue
                    c.remove(item)
                    if dest == "dup" or tid in offered or "name:" + name in offered:
                        DONE.append((cat, o.get("name"), name, "dropped (already offered as an exchange)", g.get("name")))
                        continue
                    dc = dest.find(cont)
                    if dc is None:
                        dc = ET.SubElement(dest, cont)
                    dc.append(item)
                    offered |= {tid, "name:" + name}
                    DONE.append((cat, o.get("name"), name, f"moved into {dest.get('name')}", g.get("name")))
    # drop add-on groups left empty
    parent, _ = _owner_map(root)
    for g in [g for g in root.iter() if _t(g) == "selectionEntryGroup"]:
        if not any(_kids(g, k) for k in ("entryLinks", "selectionEntries", "selectionEntryGroups")):
            holder = parent.get(g)
            if holder is not None:
                holder.remove(g)
    return root
