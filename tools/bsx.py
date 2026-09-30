"""Small helper library for writing BattleScribe / New Recruit XML (.gst / .cat).

IDs are derived from stable keys (md5), so re-running the build keeps every id
the same and players' saved rosters keep working after data updates.
"""
import hashlib
import xml.etree.ElementTree as ET

PTS = "pts0-0000-0000-0001"  # cost type id (set in the game system)
PTS_NAME = "pts"


def uid(*key):
    h = hashlib.md5("|".join(str(k) for k in key).encode("utf8")).hexdigest()
    return f"{h[0:4]}-{h[4:8]}-{h[8:12]}-{h[12:16]}"


def el(tag, attrs=None, children=None, text=None):
    e = ET.Element(tag, {k: str(v) for k, v in (attrs or {}).items() if v is not None})
    for c in children or []:
        if c is not None:
            e.append(c)
    if text is not None:
        e.text = text
    return e


def wrap(tag, items):
    items = [i for i in items if i is not None]
    return el(tag, children=items) if items else None


# ---------------------------------------------------------------- conditions
def cond(child, scope="parent", typ="atLeast", value=1, field="selections", deep=True):
    return el("condition", {
        "field": field, "scope": scope, "value": value, "percentValue": "false",
        "shared": "true", "includeChildSelections": "true" if deep else "false",
        "includeChildForces": "false", "childId": child, "type": typ})


def any_of(*conds):
    return el("conditionGroup", {"type": "or"}, [wrap("conditions", conds)])


def all_of(*conds):
    return el("conditionGroup", {"type": "and"}, [wrap("conditions", conds)])


def modifier(typ, field, value, conds=None, groups=None, repeats=None):
    return el("modifier", {"type": typ, "field": field, "value": value}, [
        wrap("repeats", repeats or []),
        wrap("conditions", conds or []),
        wrap("conditionGroups", groups or []),
    ])


def repeat(child, scope, every=1, field="selections", deep=True):
    return el("repeat", {
        "field": field, "scope": scope, "value": every, "percentValue": "false",
        "shared": "true", "includeChildSelections": "true" if deep else "false",
        "includeChildForces": "false", "childId": child, "repeats": "1", "roundUp": "false"})


def hide_if(*conds, mode="or"):
    """Hide an entry when any (mode='or') / all (mode='and') conditions are true."""
    if len(conds) == 1:
        return modifier("set", "hidden", "true", conds=list(conds))
    grp = any_of(*conds) if mode == "or" else all_of(*conds)
    return modifier("set", "hidden", "true", groups=[grp])


def show_if(*conds):
    """Entry is hidden by default and shown when any condition is true."""
    if len(conds) == 1:
        return modifier("set", "hidden", "false", conds=list(conds))
    return modifier("set", "hidden", "false", groups=[any_of(*conds)])


# --------------------------------------------------------------- constraints
def constraint(cid, typ, value, scope="parent", field="selections", deep=False, shared=True):
    return el("constraint", {
        "field": field, "scope": scope, "value": value, "percentValue": "false",
        "shared": "true" if shared else "false",
        "includeChildSelections": "true" if deep else "false",
        "includeChildForces": "false", "id": cid, "type": typ})


def costs(value):
    return wrap("costs", [el("cost", {"name": PTS_NAME, "typeId": PTS, "value": value})])


# ------------------------------------------------------------------- content
def rule(rid, name, text, hidden=False):
    return el("rule", {"id": rid, "name": name, "hidden": str(hidden).lower()},
              [el("description", text=text)])


def profile(pid, name, type_id, type_name, chars):
    """chars: list of (characteristic_type_id, name, value)."""
    return el("profile", {"id": pid, "name": name, "hidden": "false",
                          "typeId": type_id, "typeName": type_name},
              [wrap("characteristics", [
                  el("characteristic", {"name": n, "typeId": t}, text=str(v)) for t, n, v in chars])])


def info_link(target, name, typ="rule", key=None, mods=None):
    return el("infoLink", {"id": uid("il", key or "", target, name), "name": name,
                           "hidden": "false", "targetId": target, "type": typ},
              [wrap("modifiers", mods or [])])


def category_link(target, name, primary=False, key=""):
    return el("categoryLink", {"id": uid("cl", key, target), "name": name, "hidden": "false",
                               "targetId": target, "primary": str(primary).lower()})


def entry(eid, name, typ="upgrade", cost=0, hidden=False, collective=False, mods=None,
          constraints=None, profiles=None, rules=None, infolinks=None, cats=None,
          entries=None, groups=None, links=None):
    return el("selectionEntry", {
        "id": eid, "name": name, "hidden": str(hidden).lower(),
        "collective": str(collective).lower(), "import": "true", "type": typ}, [
        wrap("modifiers", mods or []),
        wrap("constraints", constraints or []),
        wrap("profiles", profiles or []),
        wrap("rules", rules or []),
        wrap("infoLinks", infolinks or []),
        wrap("categoryLinks", cats or []),
        wrap("selectionEntries", entries or []),
        wrap("selectionEntryGroups", groups or []),
        wrap("entryLinks", links or []),
        costs(cost),
    ])


def link(lid, target, name, cost=None, hidden=False, mods=None, constraints=None,
         typ="selectionEntry", collective=False):
    return el("entryLink", {
        "id": lid, "name": name, "hidden": str(hidden).lower(),
        "collective": str(collective).lower(), "import": "true",
        "targetId": target, "type": typ}, [
        wrap("modifiers", mods or []),
        wrap("constraints", constraints or []),
        costs(cost) if cost else None,
    ])


def group(gid, name, hidden=False, default=None, mods=None, constraints=None,
          entries=None, groups=None, links=None, collective=False):
    return el("selectionEntryGroup", {
        "id": gid, "name": name, "hidden": str(hidden).lower(),
        "collective": str(collective).lower(), "import": "true",
        "defaultSelectionEntryId": default}, [
        wrap("modifiers", mods or []),
        wrap("constraints", constraints or []),
        wrap("selectionEntries", entries or []),
        wrap("selectionEntryGroups", groups or []),
        wrap("entryLinks", links or []),
    ])


def write(root, path):
    ET.indent(root, space="  ")
    data = ET.tostring(root, encoding="unicode")
    with open(path, "w", encoding="utf8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        f.write(data)
        f.write("\n")
