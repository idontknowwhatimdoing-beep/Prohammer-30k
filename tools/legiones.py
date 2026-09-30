"""Legiones Astartes catalogue (.cat) for Prohammer 30k.

Slice 1: army configuration (Legion, Allegiance), HQ (Praetor, Centurion + all
Consuls), Troops (Tactical, Assault, Breacher, Recon), Dedicated Transports
(Rhino, Drop Pod, Dreadclaw) and the Space Marine Armoury.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "data"))

from bsx import (PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, hide_if,
                 constraint, rule, profile, info_link, category_link, entry, link, group)
import gamesystem as gs
from legiones_wargear import (WEAPON_PROFILES, WEAPONS, WEAPON_RULES, ARMY_RULES, WARGEAR,
                              ARMOURY, LEGIONS)

CAT_ID = "p30k-0000-0000-0101"
CAT_NAME = "Legiones Astartes"
REVISION = 1

# ------------------------------------------------------------------ lookups
CORE_NAMES = {}


def _load_core():
    import json
    data = json.load(open(os.path.join(os.path.dirname(__file__), "data", "core_usr.json"), encoding="utf8"))
    for d in data:
        CORE_NAMES[d["name"].lower()] = d["name"]
    for n, _ in gs.EXTRA_CORE_RULES:
        CORE_NAMES[n.lower()] = n


_load_core()
ALIASES = {"scout": "Scouts", "and they shall know no fear": "And They Shall Know no Fear",
           "twin-linked": "Twin-Linked", "extra armour": "Extra Armor", "poisoned": "Poison"}


def rule_ref(name):
    """Return (target_id, display_name) for an army-book or core rule."""
    if name in ARMY_RULES:
        return uid("rule", name), name
    key = ALIASES.get(name.lower(), name).lower()
    if key in CORE_NAMES:
        real = CORE_NAMES[key]
        return gs.core_rule_id(real), real
    raise KeyError(f"Unknown rule: {name}")


def rules_links(names, key):
    out = []
    for n in names:
        tid, disp = rule_ref(n)
        out.append(info_link(tid, disp, "rule", key=key))
    return out


def W(name):
    """Shared selection entry id of a weapon or wargear item."""
    if name in WEAPONS:
        return uid("weapon", name)
    if name in WARGEAR:
        return uid("wargear", name)
    raise KeyError(name)


def unit_chars(ut, ws, bs, s, t, w, i, a, ld, sv):
    vals = [ut, ws, bs, s, t, w, i, a, ld, sv]
    return [(gs.char_id("Unit", c), c, v) for c, v in zip(gs.UNIT_CHARS, vals)]


def unit_profile(key, name, *stats):
    return profile(uid("prof-unit", key, name), name, gs.UNIT, "Unit", unit_chars(*stats))


def vehicle_profile(key, name, ut, bs, f, s, r):
    chars = [(gs.char_id("Vehicle", c), c, v) for c, v in zip(gs.VEHICLE_CHARS, [ut, bs, f, s, r])]
    return profile(uid("prof-veh", key, name), name, gs.VEHICLE, "Vehicle", chars)


def transport_profile(key, name, cap, access, fire):
    chars = [(gs.char_id("Transport", c), c, v) for c, v in zip(gs.TRANSPORT_CHARS, [cap, access, fire])]
    return profile(uid("prof-tr", key, name), name, gs.TRANSPORT, "Transport", chars)


# ------------------------------------------------------------ link helpers
def gear(key, name, fixed=True, cost=None, mods=None, constraints=None, hidden=False):
    """Link to a shared weapon/wargear entry. fixed=True means always included (1-1)."""
    lid = uid("link", key, name)
    cons = list(constraints or [])
    if fixed:
        cons += [constraint(uid(lid, "min"), "min", 1), constraint(uid(lid, "max"), "max", 1, auto=True)]
    return link(lid, W(name), name, cost=cost, mods=mods, constraints=cons, hidden=hidden)


def option(key, name, cost, forbid=None, max_=1, extra_mods=None, min_=0, min_mods=None):
    """Optional link (0..max_) with a points cost. forbid: list of conditions that forbid it."""
    lid = uid("link", key, name)
    max_id = uid(lid, "max")
    mods = list(extra_mods or [])
    cons = [constraint(max_id, "max", max_)] if max_ is not None else []
    if min_ or min_mods:
        min_id = uid(lid, "min")
        cons.append(constraint(min_id, "min", min_))
        for m in min_mods or []:
            m.set("field", min_id)
            mods.append(m)
    if forbid:
        grp = any_of(*forbid) if len(forbid) > 1 else None
        if grp is not None:
            mods += [modifier("set", "hidden", "true", groups=[grp]),
                     modifier("set", max_id, 0, groups=[any_of(*forbid)])]
        else:
            mods += [modifier("set", "hidden", "true", conds=list(forbid)),
                     modifier("set", max_id, 0, conds=list(forbid))]
    return link(lid, W(name), name, cost=cost, mods=mods, constraints=cons)


def has(item_id, scope, n=1):
    return cond(item_id, scope, "atLeast", n)


def lacks(item_id, scope):
    return cond(item_id, scope, "equalTo", 0)


TDA = ["Terminator Armour", "Tartaros Terminator Armour", "Cataphractii Terminator Armour"]


def has_tda(scope):
    return [has(W(n), scope) for n in TDA]


def no_tda(scope):
    """Condition group: none of the Terminator Armour patterns selected."""
    return all_of(*[lacks(W(n), scope) for n in TDA])


def per_model(key, name, per, unit_id, contains, rules_text=None, max_=1):
    """'The entire squad may take X for +N points per model'."""
    eid = uid("squadwide", key, name)
    kids = [gear(eid, c) for c in contains]
    return entry(eid, name, cost=0,
                 mods=[modifier("increment", PTS, per, repeats=[repeat("model", unit_id, 1)])],
                 constraints=[constraint(uid(eid, "max"), "max", max_)],
                 links=kids)


# ------------------------------------------------------------------- shared
def shared_rules():
    return [rule(uid("rule", n), n, t) for n, t in ARMY_RULES.items()]


def shared_profiles():
    out = []
    for n, (rng, s, ap, typ) in WEAPON_PROFILES.items():
        chars = [(gs.char_id("Weapon", c), c, v) for c, v in zip(gs.WEAPON_CHARS, [rng, s, ap, typ])]
        out.append(profile(uid("prof-weapon", n), n, gs.WEAPON, "Weapon", chars))
    return out


def shared_items():
    out = []
    for name, profs in WEAPONS.items():
        il = [info_link(uid("prof-weapon", p), p, "profile", key=name) for p in profs]
        il += rules_links(WEAPON_RULES.get(name, []), key=name)
        inline = []
        if name in WARGEAR and WARGEAR[name][0]:
            inline.append(rule(uid("gear-rule", name), name, WARGEAR[name][0]))
        cons = []
        out.append(entry(W(name), name, cost=0, infolinks=il, rules=inline, constraints=cons))
    for name, (text, core) in WARGEAR.items():
        if name in WEAPONS:
            continue
        cons = []
        if name == "Iron Halo":  # normally one per army
            cons.append(constraint(uid("ironhalo", "roster"), "max", 1, scope="roster", deep=True))
        inline = [rule(uid("gear-rule", name), name, text)] if text else []
        out.append(entry(W(name), name, cost=0, rules=inline, infolinks=rules_links(core, key=name),
                         constraints=cons))
    return out


# ------------------------------------------------------------ configuration
LEGION_ENTRY = uid("cfg", "Legion")
ALLEGIANCE_ENTRY = uid("cfg", "Allegiance")
LOYALIST = uid("cfg", "Loyalist")
TRAITOR = uid("cfg", "Traitor")


def config_entries():
    def cats(k):
        return [category_link(gs.CAT_CONFIG, "Configuration", primary=True, key=k)]
    legion_opts = [entry(uid("legion", n), n) for n in LEGIONS]
    legion = entry(LEGION_ENTRY, "Legion", cats=cats("legion"), constraints=[
        constraint(uid(LEGION_ENTRY, "min"), "min", 1, scope="force", deep=True),
        constraint(uid(LEGION_ENTRY, "max"), "max", 1, scope="force", deep=True)],
        rules=[rule(uid("cfg-rule", "legion"), "Choosing a Legion",
                    "Every Legiones Astartes Detachment must belong to one of the Space Marine Legions. All models with "
                    "the Legiones Astartes special rule gain the named version of that rule for this Legion.")],
        groups=[group(uid("grp", "legion"), "Legion", constraints=[
            constraint(uid("grp", "legion", "min"), "min", 1), constraint(uid("grp", "legion", "max"), "max", 1)],
            entries=legion_opts)])
    alleg = entry(ALLEGIANCE_ENTRY, "Allegiance", cats=cats("alleg"), constraints=[
        constraint(uid(ALLEGIANCE_ENTRY, "min"), "min", 1, scope="force", deep=True),
        constraint(uid(ALLEGIANCE_ENTRY, "max"), "max", 1, scope="force", deep=True)],
        rules=[rule(uid("cfg-rule", "alleg"), "Allegiance",
                    "The army's Allegiance determines which characters, units, wargear, Rites of War and other options "
                    "may be selected. A Legion is not inherently restricted to a particular Allegiance.")],
        groups=[group(uid("grp", "alleg"), "Allegiance", constraints=[
            constraint(uid("grp", "alleg", "min"), "min", 1), constraint(uid("grp", "alleg", "max"), "max", 1)],
            entries=[entry(LOYALIST, "Loyalist"), entry(TRAITOR, "Traitor")])])
    return [legion, alleg]


# ------------------------------------------------------ HQ: Praetor/Centurion
PRAETOR = uid("unit", "Legion Praetor")
CENTURION = uid("unit", "Legion Centurion")

CONSULS = ["Chaplain", "Librarian", "Moritat", "Delegatus", "Esoterist", "Forge Lord", "Herald",
           "Master of Signals", "Primus Medicae", "Primus Nullificator", "Vigilator", "Praevian"]


def consul_id(n):
    return uid("consul", n)


PSYKER_CONSULS = ["Librarian", "Esoterist", "Primus Nullificator"]
SUPPORT_OFFICERS = ["Librarian", "Esoterist", "Herald", "Master of Signals", "Primus Medicae",
                    "Primus Nullificator", "Praevian"]
REPLACES_CHAINSWORD = ["Chaplain", "Librarian", "Esoterist", "Primus Nullificator"]

COMBIS = ["Combi-Bolter", "Combi-Flamer", "Combi-Grenade Launcher", "Combi-Meltagun", "Combi-Plasma Gun",
          "Combi-Volkite Charger"]
# item -> consuls that may not take it
CONSUL_FORBIDS = {}


def _forbid(consul, items):
    for i in items:
        CONSUL_FORBIDS.setdefault(i, []).append(consul)


_forbid("Moritat", ["Bolter", *COMBIS, "Boarding Shield", "Power Fist", "Thunder Hammer", "Lightning Claw",
                    "Pair of Lightning Claws", "Space Marine Bike", *TDA])
_forbid("Herald", ["Jump Pack", "Space Marine Bike", *TDA, "Relic Blade"])
_forbid("Master of Signals", [*TDA, "Space Marine Bike"])
_forbid("Vigilator", ["Boarding Shield", "Power Fist", "Thunder Hammer", "Lightning Claw", "Pair of Lightning Claws",
                      "Space Marine Bike", *TDA])
_forbid("Praevian", ["Jump Pack", "Space Marine Bike", *TDA])
_forbid("Forge Lord", ["Jump Pack", "Artificer Armour"])
_forbid("Primus Nullificator", ["Artificer Armour", "Terminator Armour", "Tartaros Terminator Armour"])


def item_forbids(item, scope, note, is_centurion):
    """Conditions under which an Independent Character may NOT take `item`."""
    f = []
    if is_centurion:
        f += [has(consul_id(c), scope) for c in CONSUL_FORBIDS.get(item, [])]
    if note == "tda":
        # needs Terminator Armour: forbidden when no pattern is selected
        f.append(("group", no_tda(scope)))
    if note == "psyker":
        f.append(("group", all_of(*[lacks(consul_id(c), scope) for c in PSYKER_CONSULS])))
    if note == "apothecary":
        f.append(lacks(consul_id("Primus Medicae"), scope))
    save5 = has_tda(scope) + [has(W("Iron Halo"), scope), has(W("Boarding Shield"), scope),
                              has(W("Refractor Field"), scope)]
    if is_centurion:
        save5.append(has(consul_id("Chaplain"), scope))
    if note == "inv6":
        f += save5
    if note in ("inv5", "refractor"):
        f += [c for c in save5 if c.get("childId") != W(item)]
    if note == "ironhalo":
        f += [has(W("Cataphractii Terminator Armour"), scope)]
        if is_centurion:
            f.append(has(consul_id("Chaplain"), scope))
    return f


def forbid_mods(lid, forbids):
    """Turn a forbid list (conditions or ('group', conditionGroup)) into hide + max-0 modifiers."""
    if not forbids:
        return []
    conds = [c for c in forbids if not isinstance(c, tuple)]
    groups = [c[1] for c in forbids if isinstance(c, tuple)]
    grp = el("conditionGroup", {"type": "or"}, [wrap("conditions", conds), wrap("conditionGroups", groups)])
    max_id = uid(lid, "max")

    def g():
        return el("conditionGroup", {"type": "or"}, [wrap("conditions", [c for c in conds]),
                                                     wrap("conditionGroups", groups)])
    return [modifier("set", "hidden", "true", groups=[grp]), modifier("set", max_id, 0, groups=[g()])]


def ic_armoury(key, unit_id, praetor):
    """Weapon slots + additional wargear for a Praetor/Centurion, capped at 100 points."""
    col = 2 if praetor else 3
    is_cent = not praetor
    weapons = [r for r in ARMOURY if r[5] == "weapon" and r[col]]
    wargear = [r for r in ARMOURY if r[5] == "wargear" and r[col]]

    def slot(slot_name, default, allow_pair):
        gid = uid("slot", key, slot_name)
        links = []
        dl = uid("link", gid, default)
        links.append(link(dl, W(default), default, constraints=[constraint(uid(dl, "max"), "max", 1)]))
        for name, pts, *_rest in weapons:
            note = _rest[-1]
            if name == default or (note == "pair" and not allow_pair):
                continue
            lid = uid("link", gid, name)
            f = item_forbids(name, unit_id, note, is_cent)
            links.append(link(lid, W(name), name, cost=pts, mods=forbid_mods(lid, f),
                              constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
        mn, mx = uid(gid, "min"), uid(gid, "max")
        mods = []
        if not allow_pair:
            zero_when = [has(W("Pair of Lightning Claws"), unit_id)]
            if is_cent:
                zero_when += [has(consul_id(c), unit_id) for c in REPLACES_CHAINSWORD]
            mods = [modifier("set", mn, 0, groups=[any_of(*zero_when)]),
                    modifier("set", mx, 0, groups=[any_of(*zero_when)]),
                    modifier("set", "hidden", "true", groups=[any_of(*zero_when)])]
        return group(gid, f"Replace {default}", default=dl, mods=mods, links=links,
                     constraints=[constraint(mn, "min", 1, auto=True), constraint(mx, "max", 1, auto=True)])

    extra_links = []
    gid = uid("grp", key, "wargear")
    for name, pts, *_rest in wargear:
        note = _rest[-1]
        lid = uid("link", gid, name)
        f = item_forbids(name, unit_id, note, is_cent)
        extra_links.append(link(lid, W(name), name, cost=pts, mods=forbid_mods(lid, f),
                                constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    extra = group(gid, "Additional Wargear", links=extra_links)

    cap = uid("grp", key, "armoury")
    return group(cap, "Space Marine Armoury (max 100 pts)",
                 constraints=[constraint(uid(cap, "maxpts"), "max", 100, scope="self", field=PTS, deep=True)],
                 groups=[slot("Bolt Pistol", "Bolt Pistol", True), slot("Chainsword", "Chainsword", False), extra])


def ic_armour_mobility(key, unit_id, is_cent):
    gid = uid("grp", key, "armour")
    dl = uid("link", gid, "Power Armour")
    links = [link(dl, W("Power Armour"), "Power Armour", constraints=[constraint(uid(dl, "max"), "max", 1)])]
    for name, pts in [("Artificer Armour", 20), ("Terminator Armour", 25), ("Tartaros Terminator Armour", 25),
                      ("Cataphractii Terminator Armour", 25)]:
        lid = uid("link", gid, name)
        f = [has(consul_id(c), unit_id) for c in CONSUL_FORBIDS.get(name, [])] if is_cent else []
        cons = [constraint(uid(lid, "max"), "max", 1, auto=True)]
        mods = forbid_mods(lid, f)
        if is_cent and name == "Cataphractii Terminator Armour":
            min_id = uid(lid, "min")
            cons.append(constraint(min_id, "min", 0))
            mods.append(modifier("set", min_id, 1, conds=[has(consul_id("Primus Nullificator"), unit_id)]))
        links.append(link(lid, W(name), name, cost=pts, mods=mods, constraints=cons))
    mn, mx = uid(gid, "min"), uid(gid, "max")
    armour = group(gid, "Armour", default=dl, links=links,
                   constraints=[constraint(mn, "min", 1, auto=True), constraint(mx, "max", 1, auto=True)])

    mid = uid("grp", key, "mobility")
    mob_links = []
    for name, pts in [("Jump Pack", 20), ("Space Marine Bike", 35)]:
        lid = uid("link", mid, name)
        f = [has(consul_id(c), unit_id) for c in CONSUL_FORBIDS.get(name, [])] if is_cent else []
        f += has_tda(unit_id)  # "If not equipped with Terminator Armour"
        mob_links.append(link(lid, W(name), name, cost=pts, mods=forbid_mods(lid, f),
                              constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    mobility = group(mid, "Mobility", links=mob_links, constraints=[constraint(uid(mid, "max"), "max", 1)])
    return [armour, mobility]


def consul_group(unit_id):
    key = "consul"

    def ce(name, cost, rules_, kit=(), options=(), groups_=(), mods=()):
        eid = consul_id(name)
        return entry(eid, f"{name} Consul", cost=cost, mods=list(mods),
                     constraints=[constraint(uid(eid, "max"), "max", 1)],
                     infolinks=rules_links(rules_, key=eid),
                     links=[gear(eid, k) for k in kit], entries=list(options), groups=list(groups_))

    epistolary = entry(uid("consul-opt", "Epistolary"), "Epistolary", cost=25,
                       constraints=[constraint(uid("consul-opt", "Epistolary", "max"), "max", 1)],
                       infolinks=rules_links(["Epistolary"], key="epist"))
    cortex = entry(uid("consul-opt", "Cortex Controller"), "Cortex Controller", cost=15,
                   constraints=[constraint(uid("consul-opt", "cc", "max"), "max", 1)],
                   links=[gear("forgelord-cc", "Cortex Controller")])
    tmatrix = entry(uid("consul-opt", "Targeting Matrix"), "Targeting Matrix", cost=10,
                    constraints=[constraint(uid("consul-opt", "tm", "max"), "max", 1)],
                    links=[gear("mos-tm", "Targeting Matrix")])
    orb_gid = uid("grp", "orbital")
    orbital = group(orb_gid, "Orbital Bombardment", constraints=[constraint(uid(orb_gid, "max"), "max", 1)],
                    entries=[entry(uid("orbital", n), n, cost=c,
                                   infolinks=[info_link(uid("prof-weapon", n), n, "profile", key="orb"),
                                              *rules_links(["Orbital Bombardment"], key=n)])
                             for n, c in [("Lance Strike", 40), ("Melta Torpedo", 45), ("Barrage Bomb", 30)]])
    ban_gid = uid("grp", "banner")
    banner = group(ban_gid, "Legion Heraldic Banner", constraints=[
        constraint(uid(ban_gid, "min"), "min", 1), constraint(uid(ban_gid, "max"), "max", 1)],
        entries=[
            entry(uid("banner", "aquila"), "Banner of the Aquila (Loyalist)",
                  infolinks=rules_links(["Banner of the Aquila"], key="aq"),
                  mods=[hide_if(has(TRAITOR, "roster"))]),
            entry(uid("banner", "eye"), "Banner of the Eye (Traitor)",
                  infolinks=rules_links(["Banner of the Eye"], key="eye"),
                  mods=[hide_if(has(LOYALIST, "roster"))])])
    scout_armour = entry(uid("consul-opt", "Scout Armour"), "Scout Armour (replaces Power Armour)", cost=0,
                         constraints=[constraint(uid("consul-opt", "sa", "max"), "max", 1)],
                         links=[gear("vig-sa", "Scout Armour")])

    entries = [
        ce("Chaplain", 35, ["Honour of the Legion", "Liturgies of Battle"], kit=["Crozius Arcanum", "Rosarius"]),
        ce("Librarian", 25, ["Psyker", "Legion Support Officer", "Psychic Powers (Librarian)"],
           kit=["Force Weapon"], options=[epistolary]),
        ce("Moritat", 45, ["Scout", "Counter-Attack", "Dual Pistols", "Lone Killer", "Chain Fire"],
           kit=["Bolt Pistol"]),
        ce("Delegatus", 15, ["Master of the Legion", "Delegated Authority"],
           mods=[hide_if(has(PRAETOR, "force"))]),
        ce("Esoterist", 25, ["Psyker", "Legion Support Officer", "Forbidden Lore"], kit=["Force Weapon"]),
        ce("Forge Lord", 70, ["Battlesmith", "Lord of the Armoury"], kit=["Artificer Armour", "Servo-Arm"],
           options=[cortex]),
        ce("Herald", 40, ["Legion Support Officer", "Fallen Honour"], groups_=[banner]),
        ce("Master of Signals", 45, ["Legion Support Officer", "Cognis Signum"],
           kit=["Nuncio Vox", "Cognis Signum"], options=[tmatrix], groups_=[orbital]),
        ce("Primus Medicae", 35, ["Legion Support Officer", "Sacred Trust"], kit=["Narthecium"]),
        ce("Primus Nullificator", 25, ["Psyker", "Legion Support Officer", "Adamantium Will", "Hexagrammic Wards",
                                       "Credo Annihilato", "Psychic Powers (Nullificator)"],
           kit=["Aether-shock Maul"]),
        ce("Vigilator", 35, ["Scout", "Stealth", "Sabotage", "Special Issue Ammunition (Vigilator)"],
           kit=["Bolter", "Cameleoline"], options=[scout_armour]),
        ce("Praevian", 35, ["Legion Support Officer", "Master of Cybernetica", "Legion Inductees"],
           kit=["Cortex Controller", "Cortex Designator"]),
    ]
    gid = uid("grp", "consul")
    return group(gid, "Legion Consul (max one)", entries=entries,
                 constraints=[constraint(uid(gid, "max"), "max", 1)])


def praetor():
    uid_ = PRAETOR
    return entry(uid_, "Legion Praetor", typ="unit", cost=125,
                 cats=[category_link(gs.cat("HQ"), "HQ", primary=True, key=uid_),
                       category_link(gs.CAT_COMMANDER, "Compulsory HQ Eligible", key=uid_),
                       category_link(gs.CAT_MASTER, "Master of the Legion", key=uid_)],
                 profiles=[unit_profile("praetor", "Legion Praetor", "Infantry (Character)",
                                        6, 5, 4, 4, 3, 5, 3, 10, "3+")],
                 infolinks=rules_links(["Legiones Astartes", "Independent Character", "Master of the Legion",
                                        "Honour Guard"], key=uid_),
                 links=[gear(uid_, "Frag Grenades"), gear(uid_, "Iron Halo")],
                 groups=[ic_armoury("praetor", uid_, True), *ic_armour_mobility("praetor", uid_, False)])


def centurion():
    uid_ = CENTURION
    remove_cmd = modifier("remove", "category", gs.CAT_COMMANDER,
                          groups=[any_of(*[has(consul_id(c), uid_) for c in SUPPORT_OFFICERS + ["Moritat"]])])
    rename = [modifier("set", "name", f"Legion {c} Consul", conds=[has(consul_id(c), uid_)]) for c in CONSULS]
    return entry(uid_, "Legion Centurion", typ="unit", cost=50, mods=[remove_cmd, *rename],
                 cats=[category_link(gs.cat("HQ"), "HQ", primary=True, key=uid_),
                       category_link(gs.CAT_COMMANDER, "Compulsory HQ Eligible", key=uid_)],
                 profiles=[unit_profile("centurion", "Legion Centurion", "Infantry (Character)",
                                        5, 5, 4, 4, 2, 5, 3, 9, "3+")],
                 infolinks=rules_links(["Legiones Astartes", "Independent Character", "Legion Consuls",
                                        "Command Retinue"], key=uid_),
                 links=[gear(uid_, "Frag Grenades")],
                 groups=[consul_group(uid_), ic_armoury("centurion", uid_, False),
                         *ic_armour_mobility("centurion", uid_, True)])


# ------------------------------------------------------------ sergeants
PA_SGT_WEAPONS = [r for r in ARMOURY if r[5] == "weapon" and r[4]]
PA_SGT_WARGEAR = [r for r in ARMOURY if r[5] == "wargear" and r[4] and r[0] != "Frag Grenades"]


def sgt_extra_wargear(key, unit_id, max_size, skip=()):
    """Additional Armoury wargear for a Power Armour Sergeant (no weapons)."""
    gid = uid("grp", key, "sgt-wargear")
    links = []
    for name, pts, *_r in PA_SGT_WARGEAR:
        if name in skip:
            continue
        note = _r[-1]
        lid = uid("link", gid, name)
        f = []
        if note == "refractor":
            # only if the squad is at its maximum starting strength; no stacking with other invulnerable saves
            f.append(cond("model", unit_id, "lessThan", max_size))
            f.append(has(W("Combat Shield"), "parent"))
        if note == "inv6":
            f.append(has(W("Refractor Field"), "parent"))
        links.append(link(lid, W(name), name, cost=pts, mods=forbid_mods(lid, f),
                          constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    return group(gid, "Additional Wargear", links=links)


def sgt_armoury_capped(key, unit_id, max_size, slots, skip=()):
    """Up to 50 pts of Armoury weapons & wargear (for sergeants with no explicit option list)."""
    groups = []
    for i, default in enumerate(slots):
        gid = uid("slot", key, default)
        dl = uid("link", gid, default)
        links = [link(dl, W(default), default, constraints=[constraint(uid(dl, "max"), "max", 1)])]
        for name, pts, *_r in PA_SGT_WEAPONS:
            if name == default or (_r[-1] == "pair" and i > 0):
                continue
            lid = uid("link", gid, name)
            links.append(link(lid, W(name), name, cost=pts, constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
        mn, mx = uid(gid, "min"), uid(gid, "max")
        mods = []
        if i > 0:
            z = [has(W("Pair of Lightning Claws"), "parent")]
            mods = [modifier("set", mn, 0, conds=z), modifier("set", mx, 0, conds=z),
                    modifier("set", "hidden", "true", conds=z)]
        groups.append(group(gid, f"Replace {default}", default=dl, links=links, mods=mods,
                            constraints=[constraint(mn, "min", 1, auto=True), constraint(mx, "max", 1, auto=True)]))
    groups.append(sgt_extra_wargear(key, unit_id, max_size, skip))
    cap = uid("grp", key, "sgt-armoury")
    return group(cap, "Space Marine Armoury (max 50 pts)", groups=groups,
                 constraints=[constraint(uid(cap, "maxpts"), "max", 50, scope="self", field=PTS, deep=True)])


def sgt_slot(key, title, default, options, zero_if=None):
    """Explicit replacement list, e.g. 'may replace his Bolt pistol with: ...'."""
    gid = uid("slot", key, title)
    dl = uid("link", gid, default)
    links = [link(dl, W(default), default, constraints=[constraint(uid(dl, "max"), "max", 1)])]
    for name, pts in options:
        lid = uid("link", gid, name)
        links.append(link(lid, W(name), name, cost=pts or None,
                          constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    mn, mx = uid(gid, "min"), uid(gid, "max")
    mods = []
    if zero_if:
        mods = [modifier("set", mn, 0, conds=zero_if), modifier("set", mx, 0, conds=zero_if),
                modifier("set", "hidden", "true", conds=zero_if)]
    return group(gid, title, default=dl, links=links, mods=mods,
                 constraints=[constraint(mn, "min", 1, auto=True), constraint(mx, "max", 1, auto=True)])


def sgt_takes(key, options):
    gid = uid("grp", key, "sgt-takes")
    links = []
    for name, pts in options:
        lid = uid("link", gid, name)
        links.append(link(lid, W(name), name, cost=pts, constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    return group(gid, "Sergeant Wargear", links=links)


def sgt_extra_capped(key, unit_id, max_size, skip):
    grp = sgt_extra_wargear(key, unit_id, max_size, skip)
    cap = uid("grp", key, "sgt-extra-cap")
    return group(cap, "Space Marine Armoury (max 50 pts)", groups=[grp],
                 constraints=[constraint(uid(cap, "maxpts"), "max", 50, scope="self", field=PTS, deep=True)])


# ---------------------------------------------------------------- squads
def model(key, name, mn, mx, cost, prof, kit, groups=(), typ_rules=()):
    eid = uid("model", key, name)
    return eid, entry(eid, name, typ="model", cost=cost,
                      constraints=[constraint(uid(eid, "min"), "min", mn), constraint(uid(eid, "max"), "max", mx)],
                      profiles=[prof], links=[gear(eid, k) for k in kit], groups=list(groups),
                      infolinks=rules_links(typ_rules, key=eid))


def weapon_pool(key, title, unit_id, options, base_max, every=None, at20=False):
    """Squad-level pool of weapon swaps limited by model count."""
    gid = uid("grp", key, title)
    mx = uid(gid, "max")
    mods = []
    if every:
        mods.append(modifier("increment", mx, 1, repeats=[repeat("model", unit_id, every)]))
    if at20:
        mods.append(modifier("increment", mx, 1, conds=[cond("model", unit_id, "atLeast", 20)]))
    links = []
    for name, pts in options:
        lid = uid("link", gid, name)
        links.append(link(lid, W(name), name, cost=pts or None))
    return group(gid, title, mods=mods, links=links, constraints=[constraint(mx, "max", base_max)])


def one_each(key, title, items):
    gid = uid("grp", key, title)
    links = []
    for name, pts in items:
        lid = uid("link", gid, name)
        links.append(link(lid, W(name), name, cost=pts, constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    return group(gid, title, links=links)


def transport_group(key, unit_id, options, max_models=10):
    gid = uid("grp", key, "transport")
    mx = uid(gid, "max")
    too_big = [cond("model", unit_id, "greaterThan", max_models)]
    links = [link(uid("link", gid, n), TRANSPORTS[n], n) for n in options]
    return group(gid, "Dedicated Transport", links=links, constraints=[constraint(mx, "max", 1, auto=True)],
                 mods=[modifier("set", mx, 0, conds=too_big), modifier("set", "hidden", "true", conds=too_big)])


def squad(name, cost, cats, rules_, models, groups):
    uid_ = uid("unit", name)
    return entry(uid_, name, typ="unit", cost=cost, cats=cats, infolinks=rules_links(rules_, key=uid_),
                 entries=models, groups=groups)


def tactical():
    name = "Legion Tactical Squad"
    u = uid("unit", name)
    ut = ("Infantry",)
    _, sgt = model(u, "Legion Tactical Sergeant", 1, 1, 0,
                   unit_profile(u, "Legion Tactical Sergeant", "Infantry (Character)", 4, 4, 4, 4, 1, 4, 2, 9, "3+"),
                   ["Power Armour", "Frag Grenades"],
                   groups=[sgt_armoury_capped(u + "sgt", u, 20, ["Bolter", "Bolt Pistol"])])
    _, marines = model(u, "Legion Tactical Marine", 9, 19, 15,
                       unit_profile(u, "Legion Tactical Marine", *ut, 4, 4, 4, 4, 1, 4, 1, 8, "3+"),
                       ["Power Armour", "Bolter", "Bolt Pistol", "Frag Grenades"])
    cw_gid = uid("grp", u, "chainswords")
    chainswords = group(cw_gid, "Chainswords", constraints=[constraint(uid(cw_gid, "max"), "max", 1)], entries=[
        per_model(u, "Chainswords (entire squad)", 2, u, ["Chainsword"]),
        entry(uid("squadwide", u, "swap"), "Exchange Bolters for Chainswords (entire squad)",
              links=[gear(uid("squadwide", u, "swap"), "Chainsword")])])
    specials = [("Flamer", 5), ("Meltagun", 10), ("Plasma Gun", 15), ("Volkite Charger", 10),
                ("Volkite Caliver", 15), ("Rotor Cannon", 4)]
    heavies = [("Heavy Bolter", 5), ("Missile Launcher", 10), ("Autocannon", 10), ("Multi-Melta", 10),
               ("Plasma Cannon", 15), ("Lascannon", 15)]
    grp_eq = uid("grp", u, "equipment")
    return squad(name, 150 - 9 * 15,
                 [category_link(gs.cat("Troops"), "Troops", primary=True, key=u),
                  category_link(gs.CAT_LINE, "Compulsory Troops Eligible", key=u)],
                 ["Legiones Astartes", "Fury of the Legion"],
                 [sgt, marines, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
                 [chainswords,
                  weapon_pool(u, "Special Weapons (1, 2 at 20 models)", u, specials, 1, at20=True),
                  weapon_pool(u, "Heavy Weapons (1, 2 at 20 models)", u, heavies, 1, at20=True),
                  one_each(u, "Squad Equipment", [("Legion Vexilla", 10), ("Nuncio Vox", 10)]),
                  transport_group(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                         "Anvillus Pattern Dreadclaw Drop Pod"])])


PISTOL_SWAPS = [("Volkite Serpenta", 5), ("Hand Flamer", 5), ("Plasma Pistol", 15)]
COMBI_SWAPS = [("Combi-Flamer", 10), ("Combi-Volkite Charger", 10), ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15)]


def assault():
    name = "Legion Assault Squad"
    u = uid("unit", name)
    sk = u + "sgt"
    _, sgt = model(u, "Legion Assault Sergeant", 1, 1, 0,
                   unit_profile(u, "Legion Assault Sergeant", "Jump Infantry (Character)", 4, 4, 4, 4, 1, 4, 2, 9,
                                "3+"),
                   ["Power Armour", "Frag Grenades", "Jump Pack"],
                   groups=[
                       sgt_slot(sk, "Replace Bolt Pistol", "Bolt Pistol",
                                PISTOL_SWAPS + [("Pair of Lightning Claws", 20)]),
                       sgt_slot(sk, "Replace Chainsword", "Chainsword",
                                [("Rending Weapon", 5), ("Power Weapon", 10), ("Lightning Claw", 15),
                                 ("Power Fist", 15), ("Thunder Hammer", 20)],
                                zero_if=[has(W("Pair of Lightning Claws"), "parent")]),
                       sgt_takes(sk, [("Combat Shield", 5), ("Melta Bombs", 5)]),
                       sgt_extra_capped(sk, u, 20, skip=("Combat Shield", "Melta Bombs"))])
    _, marines = model(u, "Legion Assault Marine", 9, 19, 18,
                       unit_profile(u, "Legion Assault Marine", "Jump Infantry", 4, 4, 4, 4, 1, 4, 1, 8, "3+"),
                       ["Power Armour", "Bolt Pistol", "Chainsword", "Frag Grenades", "Jump Pack"])
    swaps = [("Rending Weapon", 5), ("Power Weapon", 10)] + PISTOL_SWAPS
    return squad(name, 180 - 9 * 18,
                 [category_link(gs.cat("Troops"), "Troops", primary=True, key=u),
                  category_link(gs.CAT_LINE, "Compulsory Troops Eligible", key=u)],
                 ["Legiones Astartes"],
                 [sgt, marines,
                  per_model(u, "Combat Shields (entire squad)", 5, u, ["Combat Shield"]),
                  per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]),
                  per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
                 [weapon_pool(u, "Assault Weapons (1 per 5 models)", u, swaps, 0, every=5),
                  one_each(u, "Squad Equipment", [("Legion Vexilla", 10), ("Nuncio Vox", 10)])])


def breacher():
    name = "Legion Breacher Siege Squad"
    u = uid("unit", name)
    sk = u + "sgt"
    _, sgt = model(u, "Legion Breacher Sergeant", 1, 1, 0,
                   unit_profile(u, "Legion Breacher Sergeant", "Infantry (Character)", 4, 4, 4, 4, 1, 4, 2, 9, "3+"),
                   ["Hardened Power Armour", "Boarding Shield", "Frag Grenades"],
                   groups=[sgt_slot(sk, "Replace Bolter", "Bolter", COMBI_SWAPS),
                           sgt_slot(sk, "Replace Bolt Pistol", "Bolt Pistol", PISTOL_SWAPS),
                           sgt_takes(sk, [("Breaching Charge", 10), ("Melta Bombs", 5)]),
                           sgt_extra_capped(sk, u, 20, skip=("Melta Bombs", "Combat Shield", "Refractor Field"))])
    _, marines = model(u, "Legion Breacher Marine", 9, 19, 15,
                       unit_profile(u, "Legion Breacher Marine", "Infantry", 4, 4, 4, 4, 1, 4, 1, 8, "3+"),
                       ["Hardened Power Armour", "Bolter", "Bolt Pistol", "Boarding Shield", "Frag Grenades"])
    specials = [("Volkite Charger", 5), ("Volkite Caliver", 15), ("Rotor Cannon", 4), ("Flamer", 5),
                ("Meltagun", 10), ("Plasma Gun", 15), ("Lascutter", 10), ("Graviton Gun", 15)]
    return squad(name, 200 - 9 * 15,
                 [category_link(gs.cat("Troops"), "Troops", primary=True, key=u),
                  category_link(gs.CAT_LINE, "Compulsory Troops Eligible", key=u)],
                 ["Legiones Astartes", "Hardened Armour"],
                 [sgt, marines,
                  per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]),
                  per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
                 [weapon_pool(u, "Specialist Weapons (1 per 5 models)", u, specials, 0, every=5),
                  one_each(u, "Squad Equipment", [("Legion Vexilla", 10), ("Nuncio Vox", 10)])])


def recon():
    name = "Legion Reconnaissance Squad"
    u = uid("unit", name)
    sk = u + "sgt"
    recon_swaps = [("Astartes Shotgun", 0), ("Chainsword", 0), ("Combat Blade", 0), ("Sniper Rifle", 5)]
    _, sgt = model(u, "Legion Recon Sergeant", 1, 1, 0,
                   unit_profile(u, "Legion Recon Sergeant", "Infantry (Character)", 4, 4, 4, 4, 1, 4, 2, 9, "4+"),
                   ["Recon Armour", "Frag Grenades"],
                   groups=[sgt_slot(sk, "Replace Bolter", "Bolter",
                                    recon_swaps + [("Combi-Flamer", 10), ("Combi-Volkite Charger", 10),
                                                   ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15)]),
                           sgt_slot(sk, "Replace Bolt Pistol", "Bolt Pistol", PISTOL_SWAPS),
                           sgt_takes(sk, [("Melta Bombs", 5)]),
                           sgt_extra_capped(sk, u, 10, skip=("Melta Bombs",))])
    mid, marines = model(u, "Legion Recon Marine", 4, 9, 14,
                         unit_profile(u, "Legion Recon Marine", "Infantry", 4, 4, 4, 4, 1, 4, 1, 8, "4+"),
                         ["Recon Armour", "Bolter", "Bolt Pistol", "Frag Grenades"])
    gid = uid("grp", u, "recon-weapons")
    mx = uid(gid, "max")
    weapons = group(gid, "Recon Marine weapons (replace Bolter, any model)",
                    mods=[modifier("increment", mx, 1, repeats=[repeat(mid, u, 1)])],
                    constraints=[constraint(mx, "max", 0)],
                    links=[link(uid("link", gid, n), W(n), n, cost=p or None) for n, p in recon_swaps])
    return squad(name, 70 - 4 * 14,
                 [category_link(gs.cat("Troops"), "Troops", primary=True, key=u)],
                 ["Legiones Astartes", "Support Squad", "Scout", "Infiltrate", "Move Through Cover", "Acute Senses"],
                 [sgt, marines,
                  per_model(u, "Cameleoline (entire squad)", 5, u, ["Cameleoline"]),
                  per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                  per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 [weapons, one_each(u, "Squad Equipment", [("Nuncio Vox", 10)]),
                  transport_group(u, u, ["Legion Rhino Armoured Carrier"])])


# ------------------------------------------------------------- transports
TRANSPORTS = {n: uid("transport", n) for n in [
    "Legion Rhino Armoured Carrier", "Legion Drop Pod", "Anvillus Pattern Dreadclaw Drop Pod"]}


def rhino():
    n = "Legion Rhino Armoured Carrier"
    t = TRANSPORTS[n]
    pintle = [("Twin-linked Bolter", 5), ("Combi-Weapon", 5), ("Heavy Bolter", 10), ("Heavy Flamer", 10),
              ("Multi-Melta", 15), ("Havoc Launcher", 15)]
    pg = uid("grp", t, "pintle")
    return entry(t, n, typ="unit", cost=50,
                 cats=[category_link(gs.CAT_TRANSPORT, "Dedicated Transport", primary=True, key=t)],
                 profiles=[vehicle_profile(t, n, "Vehicle (Tank, Transport)", 4, 11, 11, 10),
                           transport_profile(t, n, "10 models (no Terminator Armour, Jump Packs, Bikes or Jetbikes)",
                                             "One on each side, one at the rear",
                                             "Up to two models through the top hatch")],
                 infolinks=rules_links(["Repair"], key=t),
                 links=[gear(t, "Storm Bolter"), gear(t, "Smoke Launchers"), gear(t, "Searchlight")],
                 groups=[one_each(t, "Vehicle Upgrades", [("Dozer Blade", 5), ("Extra Armour", 5),
                                                          ("Hunter-Killer Missile", 5), ("Auxiliary Drive", 10)]),
                         group(pg, "Pintle-mounted Weapon", constraints=[constraint(uid(pg, "max"), "max", 1)],
                               links=[link(uid("link", pg, w), W(w), w, cost=c) for w, c in pintle])])


def drop_pod():
    n = "Legion Drop Pod"
    t = TRANSPORTS[n]
    return entry(t, n, typ="unit", cost=50,
                 cats=[category_link(gs.CAT_TRANSPORT, "Dedicated Transport", primary=True, key=t)],
                 profiles=[vehicle_profile(t, n, "Vehicle (Open-topped, Transport)", 4, 12, 12, 12),
                           transport_profile(t, n, "10 models (Terminator Armour counts as two; no Jump Packs, Bikes "
                                                   "or Jetbikes)", "-", "Open-topped")],
                 infolinks=rules_links(["Deep Strike", "Drop Pod Assault", "Immobile", "Inertial Guidance System",
                                        "Assault Vehicle"], key=t),
                 groups=[sgt_slot(t, "Replace Storm Bolter", "Storm Bolter", [("Deathwind Missile Launcher", 20)]),
                         one_each(t, "Upgrades", [("Locator Beacon", 10)])])


def dreadclaw():
    n = "Anvillus Pattern Dreadclaw Drop Pod"
    t = TRANSPORTS[n]
    return entry(t, n, typ="unit", cost=65,
                 cats=[category_link(gs.CAT_TRANSPORT, "Dedicated Transport", primary=True, key=t)],
                 profiles=[vehicle_profile(t, n, "Vehicle (Fast, Skimmer, Transport)", 4, 12, 12, 12),
                           transport_profile(t, n, "10 models in Power Armour, or 5 in Terminator Armour, or one "
                                                   "Dreadnought where permitted",
                                             "Passengers may disembark from any point around the hull", "-")],
                 infolinks=rules_links(["Deep Strike", "Dreadclaw Assault", "Inertial Guidance System",
                                        "Assault Pod", "Hover Jets"], key=t))


# ------------------------------------------------------------------ build
def build():
    root = el("catalogue", {
        "id": CAT_ID, "name": CAT_NAME, "revision": REVISION, "battleScribeVersion": "2.03",
        "authorName": "idontknowwhatimdoing-beep",
        "authorUrl": "https://github.com/idontknowwhatimdoing-beep/Prohammer-30k",
        "library": "false", "gameSystemId": gs.GST_ID, "gameSystemRevision": gs.REVISION,
        "type": "catalogue", "xmlns": "http://www.battlescribe.net/schema/catalogueSchema"})
    root.append(wrap("publications", [
        el("publication", {"id": uid("pub", "legiones"), "name": "Legiones Astartes Army List",
                           "shortName": "Legiones Astartes"})]))

    units = [*config_entries(), praetor(), centurion(), tactical(), assault(), breacher(), recon()]
    transports = [rhino(), drop_pod(), dreadclaw()]
    import legiones2
    more_units, more_shared = legiones2.extend({u.get("name"): u for u in units}, transports)
    units += more_units
    transports += more_shared
    import legion_ts
    by_name = {u.get("name"): u for u in units + transports}
    more_units, more_shared = legion_ts.extend(by_name, units, transports)
    units += more_units
    transports += more_shared
    root.append(wrap("entryLinks", [
        link(uid("root", u.get("id")), u.get("id"), u.get("name")) for u in units]))
    root.append(wrap("sharedSelectionEntries", units + transports + shared_items()))
    root.append(wrap("sharedRules", shared_rules()))
    root.append(wrap("sharedProfiles", shared_profiles()))
    return root
