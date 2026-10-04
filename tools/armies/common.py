"""Shared building blocks for the non-Legion army books (tools/armies/<army>.py).

Every army book is its own catalogue. An army module defines

    ARMY = "Solar Auxilia"                     # catalogue name (file: '<ARMY>.cat')

    def build():
        start(ARMY)                            # resets the shared data tables for this catalogue
        register_data(rules={...}, weapons={...}, weapon_rules={...}, wargear={...})
        units = [...]                          # root units (anything the player adds to the army)
        shared = [...]                         # non-root shared entries (transports, retinues ...)
        return catalogue(ARMY, units, shared)

Each catalogue is built in its own process, so start() can safely empty the data tables that the Legiones
Astartes helpers (legiones.py / legiones2.py) read from. After that, all of their unit helpers work for any
army: W(name), gear(), slot(), take(), pool(), choice(), model_swaps(), model_takes(), numbered(), ...
"""
import copy

from bsx import (PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group,
                 info_link, category_link, hide_if, show_if, profile)
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile, rule_ref, transport_profile
from legiones2 import (slot, take, pool, choice, add_mods, add_to, dedupe_kit, walker_profile, foc, _negate,
                       model_swaps, model_takes, model_pair_claws, numbered, specials_decrement, TROOPS, ELITES, FA,
                       HQ, HS)
from legiones_wargear import ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR

LOW = gs.cat("Lords of War")
FORT = gs.cat("Fortification")
COMMANDER = gs.CAT_COMMANDER          # counts towards the compulsory HQ choice
LINE = gs.CAT_LINE                    # counts towards the two compulsory Troops choices
vehicle_profile = L.vehicle_profile
sh_vehicle_profile = L.sh_vehicle_profile
sh_walker_profile = L.sh_walker_profile

ARMY_KEY = None


def start(army):
    """Empty the shared data tables (they hold the Legiones Astartes data by default)."""
    global ARMY_KEY
    ARMY_KEY = army
    for d in (ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR):
        d.clear()


def register_data(rules=None, weapons=None, weapon_rules=None, wargear=None, multi_profile=None):
    """rules:         {rule name: text}
    weapons:       {weapon name: (range, S, AP, type)}  - one profile, entry of the same name
    multi_profile: {entry name: {profile name: (range, S, AP, type)}} - e.g. a weapon with several modes
    weapon_rules:  {weapon name: [rule names]}  (army rules or core USRs)
    wargear:       {item name: text} or {item name: (text, [core rule names])}"""
    ARMY_RULES.update(rules or {})
    for n, prof in (weapons or {}).items():
        WEAPON_PROFILES[n] = prof
        WEAPONS[n] = [n]
    for n, profs in (multi_profile or {}).items():
        WEAPON_PROFILES.update(profs)
        WEAPONS[n] = list(profs)
    WEAPON_RULES.update(weapon_rules or {})
    for n, t in (wargear or {}).items():
        WARGEAR[n] = t if isinstance(t, tuple) else (t, [])


def k(*parts):
    """Stable id that is unique to this army (use it for every id you make)."""
    return uid(ARMY_KEY, *parts)


# ------------------------------------------------------------------ units
def unit(name, cost, slot_cat, slot_name, models=(), profiles=(), kit=(), rules_=(), groups=(), entries=(),
         mods=(), constraints=(), compulsory=True, extra_cats=(), typ="unit", key=None):
    """A root unit in a Force Organisation slot.
    compulsory=True: an HQ unit counts towards the compulsory HQ, a Troops unit towards compulsory Troops."""
    u = key or k("unit", name)
    cats = [foc(slot_cat, slot_name, u)]
    if compulsory and slot_name == "HQ":
        cats.append(category_link(COMMANDER, "Compulsory HQ Eligible", key=u))
    if compulsory and slot_name == "Troops":
        cats.append(category_link(LINE, "Compulsory Troops Eligible", key=u))
    cats += [category_link(c, n, key=u) for c, n in extra_cats]
    return entry(u, name, typ=typ, cost=cost, cats=cats, mods=list(mods), constraints=list(constraints),
                 profiles=list(profiles), infolinks=rules_links(list(rules_), key=u),
                 links=[gear(u, x) for x in kit], entries=list(models) + list(entries), groups=list(groups))


def model(unit_id, name, mn, mx, cost, prof, kit=(), groups=(), rules_=(), mods=(), entries=()):
    """A model entry inside a unit. cost is per model. prof = unit_profile(...)/vehicle_profile(...)/..."""
    mid = uid("model", unit_id, name)
    cons = [constraint(uid(mid, "max"), "max", mx)]
    if mn:
        cons.append(constraint(uid(mid, "min"), "min", mn))
    return entry(mid, name, typ="model", cost=cost, constraints=cons, profiles=[prof] if prof is not None else [],
                 links=[gear(mid, x) for x in kit], groups=list(groups), infolinks=rules_links(list(rules_), key=mid),
                 mods=list(mods), entries=list(entries))


def upgrade(key, name, cost, rules_=(), text=None, links=(), max_=1, hide=None):
    """Simple optional upgrade with its own rule text and/or rule links."""
    eid = uid(key, "upgrade", name)
    mods = [modifier("set", "hidden", "true", groups=[any_of(*hide)]),
            modifier("set", uid(eid, "max"), 0, groups=[any_of(*hide)])] if hide else []
    return entry(eid, name, cost=cost, mods=mods, constraints=[constraint(uid(eid, "max"), "max", max_, auto=True)],
                 rules=[rule(uid(eid, "rule"), name, text)] if text else [],
                 infolinks=rules_links(list(rules_), key=eid), links=[gear(eid, x) for x in links])


def unique(eid, n=1, scope="roster"):
    """0-n per army (scope='roster') or per Detachment (scope='force')."""
    return constraint(uid(eid, "unique", scope), "max", n, scope=scope, deep=True)


def config(key, name, options, required=True, default=None):
    """Army-wide configuration entry (e.g. Allegiance, a Household/Cohort/Legio choice).
    options: [(name, [rule names]) ...]. Returns (entry, {option name: id})."""
    eid = k("cfg", key)
    gid = uid(eid, "grp")
    ents, ids = [], {}
    for n, rls in options:
        oid = uid(eid, n)
        ids[n] = oid
        ents.append(entry(oid, n, infolinks=rules_links(list(rls), key=oid),
                          constraints=[constraint(uid(oid, "max"), "max", 1, auto=True)]))
    cons = [constraint(uid(gid, "max"), "max", 1, auto=True)]
    if required:
        cons.append(constraint(uid(gid, "min"), "min", 1, auto=True))
    g = group(gid, name, entries=ents, constraints=cons, default=ids.get(default))
    e = entry(eid, name, typ="upgrade", cats=[category_link(gs.CAT_CONFIG, "Configuration", primary=True, key=eid)],
              constraints=[constraint(uid(eid, "min"), "min", 1, scope="force", deep=True),
                           constraint(uid(eid, "max"), "max", 1, scope="force", deep=True)],
              groups=[g])
    return e, ids


def allegiance(loyalist_ok=True, traitor_ok=True):
    """Standard Allegiance configuration (Loyalist / Traitor). Reuses the Legiones Astartes ids so rules that
    check allegiance (L.LOYALIST / L.TRAITOR) work across catalogues."""
    eid = uid("cfg", "Allegiance")
    gid = uid(eid, "grp")
    opts = []
    if loyalist_ok:
        opts.append(entry(L.LOYALIST, "Loyalist", constraints=[constraint(uid(L.LOYALIST, "max"), "max", 1, auto=True)]))
    if traitor_ok:
        opts.append(entry(L.TRAITOR, "Traitor", constraints=[constraint(uid(L.TRAITOR, "max"), "max", 1, auto=True)]))
    g = group(gid, "Allegiance", entries=opts, default=opts[0].get("id") if len(opts) == 1 else None,
              constraints=[constraint(uid(gid, "min"), "min", 1, auto=True),
                           constraint(uid(gid, "max"), "max", 1, auto=True)])
    return entry(eid, "Allegiance", cats=[category_link(gs.CAT_CONFIG, "Configuration", primary=True, key=eid)],
                 constraints=[constraint(uid(eid, "min"), "min", 1, scope="force", deep=True),
                              constraint(uid(eid, "max"), "max", 1, scope="force", deep=True)],
                 groups=[g])


def error_if(text, conds, mode="or"):
    grp = any_of(*conds) if mode == "or" else all_of(*conds)
    return modifier("add", "error", text, groups=[grp])


def clone(e, salt, new_name=None):
    """Deep copy of an entry with every id inside it remapped (for an entry used in two places)."""
    c = copy.deepcopy(e)
    ids = {x.get("id") for x in c.iter() if x.get("id")}
    remap = {i: uid(i, "clone", salt) for i in ids}
    for x in c.iter():
        for attr in ("id", "childId", "scope", "field", "defaultSelectionEntryId"):
            v = x.get(attr)
            if v in remap:
                x.set(attr, remap[v])
    if new_name:
        c.set("name", new_name)
    return c


# -------------------------------------------------------------- catalogue
def catalogue(name, units, shared=(), publication=None, force_entries=()):
    """Assemble the catalogue: root entry links for `units`, shared entries, weapons, wargear, rules, profiles."""
    cid = k("catalogue")
    root = el("catalogue", {
        "id": cid, "name": name, "revision": L.REVISION, "battleScribeVersion": "2.03",
        "authorName": "idontknowwhatimdoing-beep",
        "authorUrl": "https://github.com/idontknowwhatimdoing-beep/Prohammer-30k",
        "library": "false", "gameSystemId": gs.GST_ID, "gameSystemRevision": gs.REVISION,
        "type": "catalogue", "xmlns": "http://www.battlescribe.net/schema/catalogueSchema"})
    root.append(wrap("publications", [el("publication", {"id": k("pub"), "name": publication or name,
                                                         "shortName": name})]))
    if force_entries:
        root.append(wrap("forceEntries", list(force_entries)))
    units = list(units)
    root.append(wrap("entryLinks", [link(uid("root", u.get("id")), u.get("id"), u.get("name")) for u in units]))
    root.append(wrap("sharedSelectionEntries", units + list(shared) + L.shared_items()))
    root.append(wrap("sharedRules", L.shared_rules()))
    root.append(wrap("sharedProfiles", L.shared_profiles()))
    for u in units + list(shared):
        dedupe_kit(u)
        L2.unclash(u)
        L2.hide_when_zero(u)
    return root
