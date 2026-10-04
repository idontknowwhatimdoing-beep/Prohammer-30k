"""Game system (.gst) for Prohammer 30k.

Holds everything shared by all army books: points, profile types, force
organisation, and the ProHammer Classic universal special rules.
"""
import json
import os
import xml.etree.ElementTree as ET

from bsx import (PTS, PTS_NAME, uid, el, wrap, rule, constraint, category_link,
                 modifier, repeat, cond)

HERE = os.path.dirname(__file__)
GST_ID = "p30k-0000-0000-0001"
GST_NAME = "Prohammer 30k"
REVISION = 1

# ---------------------------------------------------------------- profiles
UNIT = uid("pt", "Unit")
UNIT_CHARS = ["Unit Type", "WS", "BS", "S", "T", "W", "I", "A", "Ld", "Sv"]
VEHICLE = uid("pt", "Vehicle")
VEHICLE_CHARS = ["Unit Type", "BS", "Front", "Side", "Rear"]
WEAPON = uid("pt", "Weapon")
WEAPON_CHARS = ["Range", "S", "AP", "Type"]
WALKER = uid("pt", "Walker")
WALKER_CHARS = ["Unit Type", "WS", "BS", "S", "Front", "Side", "Rear", "I", "A"]
# Knights, super-heavy vehicles and Titans: Structure Points in their own column
SH_WALKER = uid("pt", "Super-heavy Walker")
SH_WALKER_CHARS = ["Unit Type", "WS", "BS", "S", "Front", "Side", "Rear", "I", "A", "Structure Points"]
SH_VEHICLE = uid("pt", "Super-heavy Vehicle")
SH_VEHICLE_CHARS = ["Unit Type", "BS", "Front", "Side", "Rear", "Structure Points"]
TRANSPORT = uid("pt", "Transport")
TRANSPORT_CHARS = ["Capacity", "Access Points", "Fire Points"]

PROFILE_TYPES = {"Unit": (UNIT, UNIT_CHARS), "Vehicle": (VEHICLE, VEHICLE_CHARS),
                 "Walker": (WALKER, WALKER_CHARS), "Weapon": (WEAPON, WEAPON_CHARS),
                 "Super-heavy Walker": (SH_WALKER, SH_WALKER_CHARS),
                 "Super-heavy Vehicle": (SH_VEHICLE, SH_VEHICLE_CHARS),
                 "Transport": (TRANSPORT, TRANSPORT_CHARS)}


def char_id(ptype, cname):
    return uid("ct", ptype, cname)


# -------------------------------------------------------------- categories
def cat(name):
    return uid("cat", name)


FOC = [  # name, min, max
    ("HQ", 1, 2), ("Troops", 2, 6), ("Elites", 0, 3), ("Fast Attack", 0, 3),
    ("Heavy Support", 0, 3), ("Lords of War", 0, 1), ("Fortification", 0, 1),
]
CAT_CONFIG = cat("Configuration")
CAT_COMMANDER = cat("Compulsory HQ Eligible")
CAT_LINE = cat("Compulsory Troops Eligible")
CAT_MASTER = cat("Master of the Legion")
CAT_TRANSPORT = cat("Dedicated Transport")
# Army-construction limits switched on by Rites of War (or similar rules) in any army book:
# a selection carrying one of these categories lowers the matching Force Organisation maximum to 1.
CAT_LIMIT_FA = cat("Limit: 0-1 Fast Attack")
CAT_LIMIT_HS = cat("Limit: 0-1 Heavy Support")
# Army-book changes to the Force Organisation Chart: any selection carrying one of these categories changes the
# Detachment's maximum for that slot (e.g. Thousand Sons "Price of Knowledge": +1 HQ, +1 Elites, -1 Fast Attack).
FOC_SLOTS = ["HQ", "Troops", "Elites", "Fast Attack", "Heavy Support", "Lords of War", "Fortification"]
FOC_PLUS = {n: cat(f"Force Org: +1 {n}") for n in FOC_SLOTS}
FOC_MINUS = {n: cat(f"Force Org: -1 {n}") for n in FOC_SLOTS}
CAT_HQ_PLUS1 = FOC_PLUS["HQ"]
CAT_EL_PLUS1 = FOC_PLUS["Elites"]
CAT_FA_MINUS1 = FOC_MINUS["Fast Attack"]
CAT_PRIMARCH = cat("Primarch")
CAT_HALO = cat("Iron Halo (one per army)")  # Iron Halos of Praetors and Centurions; named characters' own do not count
CAT_BROTHERHOOD = cat("Psychic Brotherhood")
EXTRA_CATS = [("Configuration", CAT_CONFIG), ("Dedicated Transport", CAT_TRANSPORT),
              ("Compulsory HQ Eligible", CAT_COMMANDER),
              ("Compulsory Troops Eligible", CAT_LINE),
              ("Master of the Legion", CAT_MASTER),
              ("Limit: 0-1 Fast Attack", CAT_LIMIT_FA), ("Limit: 0-1 Heavy Support", CAT_LIMIT_HS),
              ("Primarch", CAT_PRIMARCH), ("Iron Halo (one per army)", CAT_HALO), ("Psychic Brotherhood", CAT_BROTHERHOOD)]
EXTRA_CATS += [(f"Force Org: +1 {n}", FOC_PLUS[n]) for n in FOC_SLOTS]
EXTRA_CATS += [(f"Force Org: -1 {n}", FOC_MINUS[n]) for n in FOC_SLOTS]


# ------------------------------------------------------------------- rules
def core_rule_id(name):
    return uid("core-rule", name.lower())


EXTRA_CORE_RULES = [
    ("Independent Character", "Independent Characters may join and leave friendly units, may not join units "
     "containing vehicles or monstrous creatures, and may only be targeted when unattached under the "
     "conditions given in ProHammer Classic (Unit Type Details - Independent Characters)."),
    ("Character", "See ProHammer Classic, Unit Type Details."),
    ("Deep Strike", "The unit may be held in reserve and arrive by deep strike. Models arriving by deep strike "
     "may not take a normal move that turn but may shoot, advance D6\" or assault; units charging on the turn "
     "they arrived gain no charge bonus attacks and no assault grenade benefits. Vehicles count as having moved "
     "at cruising speed. See ProHammer Classic, Movement Phase."),
    ("Psyker", "The model is a Psyker of the Mastery Level shown and uses the ProHammer Classic psychic rules."),
]


def core_rules():
    data = json.load(open(os.path.join(HERE, "data", "core_usr.json"), encoding="utf8"))
    import allies
    out = [(d["name"], d["text"]) for d in data] + EXTRA_CORE_RULES + allies.EXTRA_RULES
    return [rule(core_rule_id(n), n, t) for n, t in out]


def foc_links(variant=None):
    """Category links of the Standard Force Organisation Chart. variant None keeps the ids of the first releases."""
    def k(*p):
        return uid(*p) if variant is None else uid(*p, variant)
    key = "foc" if variant is None else "foc-" + variant
    links = [category_link(CAT_CONFIG, "Configuration", key=key)]
    limits = {"Fast Attack": CAT_LIMIT_FA, "Heavy Support": CAT_LIMIT_HS}
    for name, mn, mx in FOC:
        cl = category_link(cat(name), name, key=key)
        mods = []
        if name in limits:
            mods.append(modifier("set", k("foc-max", name), 1, conds=[cond(limits[name], "force", "atLeast", 1)]))
        # +1 / -1 per selection carrying the category (a Rite's 0-1 limit already caps FA/HS, so -1 only without it)
        mods.append(modifier("increment", k("foc-max", name), 1,
                             repeats=[repeat(FOC_PLUS[name], "force", 1, deep=True)]))
        minus_conds = [cond(limits[name], "force", "lessThan", 1)] if name in limits else None
        mods.append(modifier("decrement", k("foc-max", name), 1, conds=minus_conds,
                             repeats=[repeat(FOC_MINUS[name], "force", 1, deep=True)]))
        cl.append(wrap("modifiers", mods))
        cl.append(wrap("constraints", [
            constraint(k("foc-min", name), "min", mn),
            constraint(k("foc-max", name), "max", mx)]))
        links.append(cl)
    links.append(category_link(CAT_TRANSPORT, "Dedicated Transport", key=key))

    commander = category_link(CAT_COMMANDER, "Compulsory HQ Eligible", key=key)
    commander.append(wrap("constraints", [constraint(k("foc-min", "commander"), "min", 1)]))
    links.append(commander)

    line = category_link(CAT_LINE, "Compulsory Troops Eligible", key=key)
    line.append(wrap("constraints", [constraint(k("foc-min", "line"), "min", 2)]))
    links.append(line)

    # Master of the Legion: one per FULL 1,000 points in the army.
    master = category_link(CAT_MASTER, "Master of the Legion", key=key)
    mcid = k("foc-max", "master")
    master.append(wrap("modifiers", [modifier(
        "increment", mcid, 1, repeats=[repeat("any", "roster", 1000, field=PTS, deep=False)])]))
    master.append(wrap("constraints", [constraint(mcid, "max", 0)]))
    links.append(master)
    return links


def build():
    root = el("gameSystem", {
        "id": GST_ID, "name": GST_NAME, "revision": REVISION, "battleScribeVersion": "2.03",
        "authorName": "idontknowwhatimdoing-beep",
        "authorUrl": "https://github.com/idontknowwhatimdoing-beep/Prohammer-30k",
        "type": "gameSystem", "xmlns": "http://www.battlescribe.net/schema/gameSystemSchema"})

    root.append(wrap("publications", [
        el("publication", {"id": uid("pub", "core"), "name": "ProHammer Classic Core Rules v2.4",
                           "shortName": "ProHammer Classic"}),
        el("publication", {"id": uid("pub", "github"), "name": "github",
                           "publisherUrl": "https://github.com/idontknowwhatimdoing-beep/Prohammer-30k"}),
    ]))
    root.append(wrap("costTypes", [
        el("costType", {"id": PTS, "name": PTS_NAME, "defaultCostLimit": "-1", "hidden": "false"})]))

    root.append(wrap("profileTypes", [
        el("profileType", {"id": pid, "name": name}, [wrap("characteristicTypes", [
            el("characteristicType", {"id": char_id(name, c), "name": c}) for c in chars])])
        for name, (pid, chars) in PROFILE_TYPES.items()]))

    cats = [el("categoryEntry", {"id": cat(n), "name": n, "hidden": "false"}) for n, _, _ in FOC]
    cats += [el("categoryEntry", {"id": cid, "name": n, "hidden": "false"}) for n, cid in EXTRA_CATS]
    import allies
    cats += [el("categoryEntry", {"id": cid, "name": n, "hidden": "false"}) for n, cid in allies.army_categories()]
    root.append(wrap("categoryEntries", cats))

    # Primary Detachment (the Standard Force Organisation Chart; id kept from the first releases) and the Allied
    # Detachment (the same chart, its own ids) - see allies.py
    import allies
    primary = el("forceEntry", {"id": uid("force", "standard"), "name": "Primary Detachment", "hidden": "false"},
                 [wrap("categoryLinks", foc_links())])
    root.append(wrap("forceEntries", [primary, allies.allied_force_entry(foc_links("allied"))]))
    root.append(wrap("sharedRules", core_rules()))
    return root
