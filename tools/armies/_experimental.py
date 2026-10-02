"""Experimental Wargear and Units (the author's sandbox of optional / unofficial units and wargear).

Source: the author's document 'Experimental_Wargear_and_Units.txt'.
Questions: tools/questions/Experimental Wargear and Units.md

Built as its own catalogue. Every unit carries the 'Experimental (Unofficial)' rule. The catalogue also offers an
'Experimental Supplement' force type without compulsory selections, so these units can be added to a roster as a
second Detachment next to a Legiones Astartes Detachment.
"""
import copy

import legiones_wargear as LW
from armies.common import *  # noqa: F401,F403
from armies.common import (k, unit, model, upgrade, unique, error_if, catalogue, start, register_data, W, gear,
                           rules_links, unit_profile, transport_profile, vehicle_profile, slot, take, pool,
                           model_swaps, numbered, specials_decrement, HQ, ELITES, FA, HS)
from bsx import PTS, uid, el, wrap, cond, modifier, constraint, rule, entry, link, group, category_link
import gamesystem as gs

ARMY = "Experimental Wargear and Units"

# Snapshot of the Legiones Astartes data (start() empties these tables). Taken at import time.
_LW_PROFILES = copy.deepcopy(LW.WEAPON_PROFILES)
_LW_WEAPONS = copy.deepcopy(LW.WEAPONS)
_LW_WEAPON_RULES = copy.deepcopy(LW.WEAPON_RULES)
_LW_RULES = copy.deepcopy(LW.ARMY_RULES)
_LW_WARGEAR = copy.deepcopy(LW.WARGEAR)
_LW_TDA_SGT = dict(LW.TDA_SGT)

# ====================================================================== rules
EXPERIMENTAL = "Experimental (Unofficial)"

RULES = {
    EXPERIMENTAL: (
        "This unit or rule comes from the 'Experimental Wargear and Units' document - the author's place for optional "
        "and unofficial units and wargear that were not (or not yet) added to the official lists for thematic reasons "
        "or because they do not fit the vision of the ruleset. Use them only by agreement with your opponent; some "
        "may be added officially later on."),
    "Experimental Supplement": (
        "Experimental units have no Detachment of their own in the rules. Select them for a Legiones Astartes army as "
        "if they were part of that army's Detachment and its Force Organisation chart (Saturnine Terminator Squad: "
        "Elites; Sabre Strike Tank Squadron: Fast Attack; Arquitor Bombard Squadron: Heavy Support; Saturnine "
        "Terminator Command Squad: retinue of a Praetor or Centurion in Saturnine Exo-armour; Legion Rhino Advancer: "
        "transport). In New Recruit add them in an 'Experimental Supplement' Detachment of this catalogue; the "
        "slots it uses still count against the Legion Detachment's Force Organisation chart (not checked)."),
    "Legiones Astartes": _LW_RULES["Legiones Astartes"],
    # ------------------------------------------------------- Saturnine
    "Saturnine Exo-armour": (
        "Saturnine Exo-armour is an exceptionally massive form of Tactical Dreadnought Armour. A model equipped with it "
        "gains the following modifiers: S +1, T +1, W +1, I -1, A +1, Save 2+/4++ (already included in the Saturnine "
        "profiles).\nTerminator Armour: Saturnine Exo-armour counts as Terminator Armour for all rules, restrictions "
        "and wargear options.\nSlow and Purposeful: a model wearing Saturnine Exo-armour has the Slow and Purposeful "
        "special rule.\nMassive Exo-armour: see that rule.\nDeep Strike: models wearing Saturnine Exo-armour may deploy "
        "using the Deep Strike rules in missions where Deep Strike is normally permitted.\nCombi-Foeblaster: see that "
        "rule.\nCOST FOR CHARACTERS: the heading gives '65 ca' (about 65 points). A Legion Praetor or Centurion may "
        "take Saturnine Exo-armour for about +65 points (this is required for him to select a Saturnine Terminator "
        "Command Squad as a retinue). New Recruit cannot add this option to the characters of the Legiones Astartes "
        "catalogues; note it on the character."),
    "Massive Exo-armour": (
        "Models wearing Saturnine Exo-armour may never make a Sweeping Advance and may only Consolidate after winning a "
        "close combat. Each model counts as two models wearing Terminator Armour when determining Transport Capacity."),
    "Combi-Foeblaster": (
        "A Combi-Foeblaster follows the normal rules for combi-weapons, except that its primary weapon is a Foeblaster "
        "boltgun instead of a bolter: the Foeblaster boltgun may be fired normally throughout the battle, the secondary "
        "weapon may be fired once per battle, and both may not be fired in the same Shooting phase."),
    "Saturnine Retinue": (
        "A Saturnine Terminator Command Squad may only be selected as a retinue for a Legion Praetor or Legion "
        "Centurion equipped with Saturnine Exo-armour. The character and the Command Squad count as a single HQ "
        "choice (they do not occupy a separate Force Organisation slot)."),
    "Legion-specific Wargear (Saturnine)": (
        "Models in the squad may take Legion-specific weapons, relics or wargear where the relevant Legion rules "
        "permit that equipment to be taken by models in Terminator Armour (add them by hand; not listed here)."),
    "Space Marine Armoury (Saturnine Veteran)": (
        "The Saturnine Veteran Terminator may select up to 50 points of permitted weapons and wargear from the Space "
        "Marine Armoury (Terminator Armour column)."),
    # ------------------------------------------------------- vehicles
    "Sunder": "Failed Armour Penetration rolls made by this weapon may be re-rolled.",
    "Repair": (
        "If a Rhino Advancer is Immobilised, its crew may attempt to repair the vehicle. During the controlling "
        "player's Shooting phase, instead of firing any of the Rhino's weapons, roll a D6. On a roll of 6, remove one "
        "Immobilised result from the Rhino. The vehicle may move normally from the beginning of its following "
        "Movement phase."),
    "Auxiliary Drive": (
        "At the start of the controlling player's Movement phase, if a vehicle equipped with an Auxiliary Drive is "
        "Immobilised, roll a D6. On a 4+, remove one Immobilised result. The vehicle may move normally during that "
        "Movement phase."),
    "Open Topped": "The vehicle is Open-topped. Use the ProHammer Classic rules for Open-topped vehicles.",
    "Rhino Advancer Transport": (
        "Transport Capacity 15 models. Models in Terminator Armour, models equipped with Jump Packs, and models "
        "mounted on Bikes or Jetbikes may not embark upon a Rhino Advancer. Access Points: one on each side of the "
        "hull and one at the rear. Fire Points: up to two transported models may fire through the Rhino's top hatch."),
    "Crew: Space Marines": "The vehicle is crewed by Space Marines (it does not have the Legiones Astartes rule).",
    "Space Marine Armoury (Vehicles)": (
        "Any vehicle with this rule may take vehicle upgrades from the Space Marine Armoury as normally permitted."),
    # ------------------------------------------------------- army-wide
    "Focused Fire Configuration": (
        "During big assaults and Special Operations the Legions focus multiple heavy support squads into what some "
        "call a Focused Fire Configuration - more firepower and deadlier than the base configuration, these groups "
        "include a greater amount of heavy weapons.\nA Legion Heavy Support Squad that is part of an army of over "
        "2,000 points may be fully equipped with heavy weapons (every model may take one), instead of the usual four "
        "Marines which can do so. Only one unit may be upgraded like that. (The Heavy Support Squad is in the "
        "Legiones Astartes catalogue: New Recruit will still limit it to four heavy weapons - add the rest by hand.)"),
    "Planned Additions (design notes)": (
        "Not playable - the author's list of ideas still to be written up:\n"
        "Ultramarines: Logos Command Squad (several bonuses for reserves, artillery or morale).\n"
        "Dark Angels: Excindio class Battle-Automata.\n"
        "Corrupted Legions (general): Daemon Prince (5th edition version); Blessing of a god - general blessing free "
        "for Veterans, Terminators and characters, the rest pay 25 points (maybe like Icons); all Chaos gods share the "
        "same rules, Chaos Undivided becomes just Hatred (Loyalist), named 'Death to the False Emperor'; Daemon allies "
        "for all but from specific dominions; no allies between armies; vehicle Dirge Caster, Daemonic Possession and "
        "Daemonic steeds.\n"
        "Sons of Horus: Horus bonus with allied Daemons; may ally other Legions upgraded like this and Dark Mechanicum.\n"
        "Word Bearers: easier Daemon summoning (must take); access to more Chaos spells like the Thousand Sons; more "
        "access to Daemons and possible transfiguration tables for characters when they kill something; possibility "
        "to turn a unit into Possessed later in the game (global sacrifice points).\n"
        "Death Guard: Plague Marines; Librarians may take Death Guard style psychic powers; Blight grenades for all "
        "units for 2 points and Rad grenades for 5 points per model; Mortarion's upgrade for Plague Marines (maybe "
        "more expensive); less movement for everything, 'living hull' for weapons.\n"
        "Emperor's Children: sonic weapons for normal units with access to heavy weapons; Slaanesh blessing for all "
        "units for 25/10 points; may not charge units of lower Weapon Skill but must charge otherwise (try to resist); "
        "Lash of Submission and psyker upgrade for characters.\n"
        "World Eaters: units must take close-combat weapons where they can; must charge and must pursue if possible; "
        "cheap Khorne upgrade; anti-psyker collars for some units; overcharged Nails (+2 Attacks but might die on a 2).\n"
        "Thousand Sons: Tzeentch bonus applied to everything; better spellcasting but worse Perils; Bolt of Change, "
        "Wind of Chaos, Gift of Chaos and Doombolt; less wargear but a 50 point psyker upgrade on everything (Tactical "
        "Squads etc.); Daemons change; Sorcerer Consul.\n"
        "Iron Warriors: Chaos Undivided; Obliterators; Frenzied Dreadnought (Chaos Dreadnought rules); allied Dark "
        "Mechanicum more easily.\n"
        "Knights: smaller Knights; corrupted Knights (5 blessings); human auxiliary.\n"
        "Mechanicum: Weapons Platforms (Photon Thruster addition; Plasma Caster); Nemesis Warbringer Titan; Psychic "
        "Titan."),
}

for _r in ("Combi-Weapon", "Force", "Legion Standard", "Sacred Standard", "Crusade Relic"):
    RULES.setdefault(_r, _LW_RULES[_r])

WEAPONS = {
    "Anvillus Snub Autocannon": ('24"', "8", "4", "Heavy 2, Twin-linked, Sunder"),
    "Neutron Blaster": ('24"', "9", "2", "Heavy 1, Concussive"),
    "Volkite Saker": ('24"', "6", "5", "Heavy 6, Rending"),
    "Sabre Missile": ('36"', "6", "4", "Heavy 1, One Use, Rending"),
    "Morbus Heavy Bombard": ('24"', "9", "3", "Ordnance 1, Barrage, Large Blast, Pinning"),
    "Graviton-Charge Cannon": ('24"', "*", "4", "Ordnance 1, Barrage, Large Blast, Graviton, Concussive"),
    "Spicula Rocket System": ('48"', "7", "3", "Ordnance 1, Barrage, Large Blast, Pinning, Sunder"),
}
MULTI = {
    "Combi-Foeblaster (flamer)": {"Foeblaster Boltgun": _LW_PROFILES["Foeblaster Boltgun"],
                                  "Flamer": _LW_PROFILES["Flamer"]},
    "Combi-Foeblaster (melta)": {"Foeblaster Boltgun": _LW_PROFILES["Foeblaster Boltgun"],
                                 "Meltagun": _LW_PROFILES["Meltagun"]},
    "Combi-Foeblaster (plasma)": {"Foeblaster Boltgun": _LW_PROFILES["Foeblaster Boltgun"],
                                  "Plasma Gun": _LW_PROFILES["Plasma Gun"]},
    "Two Sponson-mounted Heavy Bolters": {"Heavy Bolter": _LW_PROFILES["Heavy Bolter"],
                                          "Heavy Bolter - Hellfire Round": _LW_PROFILES[
                                              "Heavy Bolter - Hellfire Round"]},
    "Two Sponson-mounted Autocannons": {"Autocannon": _LW_PROFILES["Autocannon"]},
}
WEAPON_RULES = {
    "Anvillus Snub Autocannon": ["Twin-Linked", "Sunder"],
    "Neutron Blaster": ["Concussive"],
    "Volkite Saker": ["Rending"],
    "Sabre Missile": ["Rending"],
    "Morbus Heavy Bombard": ["Pinning"],
    "Graviton-Charge Cannon": ["Graviton", "Concussive"],
    "Spicula Rocket System": ["Pinning", "Sunder"],
    "Combi-Foeblaster (flamer)": ["Combi-Foeblaster", "Twin-Linked"],
    "Combi-Foeblaster (melta)": ["Combi-Foeblaster", "Twin-Linked", "Melta"],
    "Combi-Foeblaster (plasma)": ["Combi-Foeblaster", "Twin-Linked", "Gets Hot"],
    "Two Sponson-mounted Heavy Bolters": ["Hellfire"],
}
RULES.setdefault("Hellfire", _LW_RULES["Hellfire"])

WARGEAR = {
    "Saturnine Exo-armour": (RULES["Saturnine Exo-armour"], ["Slow and purposeful", "Deep Strike"]),
    "Saturnine Champion (+1 Attack)": "The Saturnine Champion has +1 Attack (included in his profile).",
}

# Legiones Astartes weapons and wargear used by these units (copied with their profiles and rules)
LEGION_ITEMS = ["Foeblaster Boltgun", "Power Weapon", "Power Fist", "Chainfist", "Thunder Hammer", "Heavy Flamer",
                "Plasma Blaster", "Multi-Melta", "Heavy Bolter", "Storm Bolter", "Twin-linked Bolter", "Combi-Weapon",
                "Havoc Launcher", "Hunter-Killer Missile", "Volkite Culverin", "Narthecium", "Reductor",
                "Legion Standard", "Smoke Launchers", "Searchlight", "Dozer Blade", "Extra Armour",
                "Auxiliary Drive", "Armoured Ceramite"] + [n for n in _LW_TDA_SGT if n != "Force Weapon"]


def _copy_legion_items():
    for n in LEGION_ITEMS:
        if n in _LW_WEAPONS:
            profs = _LW_WEAPONS[n]
            if profs == [n]:
                WEAPONS[n] = _LW_PROFILES[n]
            else:
                MULTI[n] = {p: _LW_PROFILES[p] for p in profs}
            if n in _LW_WEAPON_RULES:
                WEAPON_RULES[n] = list(_LW_WEAPON_RULES[n])
        if n in _LW_WARGEAR and n not in _LW_WEAPONS:
            WARGEAR[n] = _LW_WARGEAR[n]
    for rl in WEAPON_RULES.values():
        for r in rl:
            if r in _LW_RULES:
                RULES.setdefault(r, _LW_RULES[r])


_copy_legion_items()

SAT_RULES = ["Legiones Astartes", "Slow and purposeful", "Massive Exo-armour", "Deep Strike", EXPERIMENTAL]
SAT_KIT = ["Saturnine Exo-armour", "Foeblaster Boltgun"]
COMBI_FOE = [("Combi-Foeblaster (flamer)", 10), ("Combi-Foeblaster (melta)", 15), ("Combi-Foeblaster (plasma)", 15)]
SAT_HEAVY = [("Heavy Flamer", 5), ("Plasma Blaster", 15), ("Multi-Melta", 20)]
STD_UPGRADES = [("Hunter-Killer Missile", 5), ("Dozer Blade", 5), ("Extra Armour", 5), ("Auxiliary Drive", 10),
                ("Armoured Ceramite", 20)]
PINTLE = [("Twin-linked Bolter", 5), ("Combi-Weapon", 5), ("Heavy Bolter", 10), ("Heavy Flamer", 10),
          ("Multi-Melta", 15), ("Havoc Launcher", 15)]


def sat_profile(u, name, a, character=False):
    return unit_profile(u, name, "Infantry (Character)" if character else "Infantry",
                        4, 4, 5, 5, 2, 3, a, 9, "2+/4+")


def cc_slot(mid, hammer=False):
    """'Power weapon or power fist'; a power fist may become a chainfist (+5) or thunder hammer (+10)."""
    opts = [("Power Fist", 0), ("Chainfist", 5)] + ([("Thunder Hammer", 10)] if hammer else [])
    return slot(mid, "Power Weapon or Power Fist", "Power Weapon", opts)


def veteran_armoury(mid):
    gid = uid("grp", mid, "armoury")
    links = [link(uid("link", gid, n), W(n), n, cost=p,
                  constraints=[constraint(uid("link", gid, n, "max"), "max", 1, auto=True)])
             for n, p in _LW_TDA_SGT.items() if n != "Force Weapon"]
    return group(gid, "Space Marine Armoury (max 50 pts)", links=links,
                 constraints=[constraint(uid(gid, "maxpts"), "max", 50, scope="self", field=PTS, deep=True)])


# ====================================================================== units
def saturnine_squad():
    name = "Saturnine Terminator Squad"
    u = k("unit", name)
    vet = model(u, "Saturnine Veteran Terminator", 1, 1, 70,
                sat_profile(u, "Saturnine Veteran Terminator", 4, character=True), kit=SAT_KIT,
                groups=[slot(uid("model", u, "vet"), "Replace Foeblaster Boltgun", "Foeblaster Boltgun", COMBI_FOE),
                        cc_slot(uid("model", u, "vet")), veteran_armoury(uid("model", u, "vet"))],
                rules_=["Space Marine Armoury (Saturnine Veteran)", "Character"])
    tid = uid("model", u, "Saturnine Terminator")
    terms = model(u, "Saturnine Terminator", 2, 5, 70, sat_profile(u, "Saturnine Terminator", 3), kit=SAT_KIT)
    heavy, _ = pool(u, "Heavy Weapon (one Saturnine Terminator per three models in the squad)", u, SAT_HEAVY, 0,
                    every=3)
    swaps = [
        model_swaps(u, "Saturnine Terminators: replace Foeblaster Boltgun (any number)", u, [tid], COMBI_FOE,
                    minus=[W(n) for n, _ in SAT_HEAVY]),
        heavy,
        model_swaps(u, "Saturnine Terminators: Power Weapon or Power Fist (any number)", u, [tid],
                    [("Power Fist", 0), ("Chainfist", 5)]),
    ]
    return unit(name, 0, ELITES, "Elites", models=[vet, terms], rules_=SAT_RULES, groups=swaps, key=u)


def saturnine_command_squad():
    name = "Saturnine Terminator Command Squad"
    u = k("unit", name)
    bid = uid("model", u, "Saturnine Bodyguard")
    bmin, bmax = uid(bid, "min"), uid(bid, "max")
    specials = []
    for n, extra, a, kit in [("Saturnine Apothecary", 25, 3, ["Narthecium", "Reductor"]),
                             ("Saturnine Standard Bearer", 15, 3, ["Legion Standard"]),
                             ("Saturnine Champion", 15, 4, ["Saturnine Champion (+1 Attack)"])]:
        sid = uid("model", u, n)
        smods = []
        if "Standard" in n:
            smods = [error_if("A Legion Standard may only be included in an army of 2,000 points or more.",
                              [cond("any", "roster", "lessThan", 2000, field=PTS, deep=False)])]
        specials.append(entry(sid, n, typ="model", cost=70 + extra, mods=smods,
                              constraints=[constraint(uid(sid, "max"), "max", 1)],
                              profiles=[sat_profile(u, n, a)],
                              links=[gear(sid, x) for x in SAT_KIT + kit],
                              groups=[slot(sid, "Replace Foeblaster Boltgun", "Foeblaster Boltgun", COMBI_FOE),
                                      cc_slot(sid, hammer=True)]))
    spec_ids = [s.get("id") for s in specials]
    body = entry(bid, "Saturnine Bodyguard", typ="model", cost=70,
                 mods=specials_decrement(bid, bmin, bmax, spec_ids, u),
                 constraints=[constraint(bmin, "min", 2), constraint(bmax, "max", 5)],
                 profiles=[sat_profile(u, "Saturnine Bodyguard", 3)], links=[gear(bid, x) for x in SAT_KIT])
    swaps = [
        model_swaps(u, "Saturnine Bodyguards: replace Foeblaster Boltgun (any number)", u, [bid], COMBI_FOE),
        model_swaps(u, "Saturnine Bodyguards: Power Weapon or Power Fist (any number)", u, [bid],
                    [("Power Fist", 0), ("Chainfist", 5), ("Thunder Hammer", 10)]),
    ]
    mods = [error_if("A Saturnine Terminator Command Squad has 2-5 models.",
                     [cond("model", u, "lessThan", 2), cond("model", u, "greaterThan", 5)])]
    return unit(name, 0, HQ, "HQ", models=[body, *specials], groups=swaps, key=u, compulsory=False, mods=mods,
                rules_=SAT_RULES + ["Saturnine Retinue", "Legion-specific Wargear (Saturnine)"])


def vehicle_squadron(name, per, model_name, prof, slot_cat, slot_name, kit, groups_fn, rules_):
    u = k("unit", name)
    mid = uid("model", u, model_name)
    m = model(u, model_name, 1, 3, per, prof(u, model_name), kit=kit, groups=groups_fn(mid))
    return unit(name, 0, slot_cat, slot_name, models=numbered(m, 3, 1), rules_=rules_ + [EXPERIMENTAL], key=u)


def sabre():
    def groups(mid):
        return [slot(mid, "Replace Anvillus Snub Autocannon", "Anvillus Snub Autocannon",
                     [("Volkite Saker", 0), ("Neutron Blaster", 20)]),
                slot(mid, "Replace Hull-mounted Heavy Bolter", "Heavy Bolter",
                     [("Heavy Flamer", 0), ("Volkite Culverin", 15), ("Multi-Melta", 20)]),
                take(mid, "Sabre Missiles", [("Sabre Missile", 5, 4)]),
                take(mid, "Vehicle Upgrades", STD_UPGRADES),
                take(mid, "Pintle-mounted Weapon", PINTLE, max_total=1)]
    return vehicle_squadron("Sabre Strike Tank Squadron", 80, "Sabre Strike Tank",
                            lambda u, n: vehicle_profile(u, n, "Vehicle (Tank, Fast)", 4, 12, 11, 10), FA,
                            "Fast Attack", ["Smoke Launchers", "Searchlight"], groups,
                            ["Crew: Space Marines", "Space Marine Armoury (Vehicles)"])


def arquitor():
    def groups(mid):
        return [slot(mid, "Replace Morbus Heavy Bombard", "Morbus Heavy Bombard",
                     [("Graviton-Charge Cannon", 0), ("Spicula Rocket System", 0)]),
                slot(mid, "Sponson-mounted Weapons", "Two Sponson-mounted Heavy Bolters",
                     [("Two Sponson-mounted Autocannons", 10)]),
                take(mid, "Vehicle Upgrades", STD_UPGRADES),
                take(mid, "Pintle-mounted Weapon", PINTLE, max_total=1)]
    return vehicle_squadron("Arquitor Bombard Squadron", 140, "Arquitor Bombard",
                            lambda u, n: vehicle_profile(u, n, "Vehicle (Tank)", 4, 12, 12, 10), HS,
                            "Heavy Support", ["Smoke Launchers", "Searchlight"], groups,
                            ["Crew: Space Marines", "Space Marine Armoury (Vehicles)"])


def rhino_advancer():
    name = "Legion Rhino Advancer"
    u = k("unit", name)
    m = model(u, name, 1, 1, 0, vehicle_profile(u, name, "Vehicle (Tank, Transport)", 4, 11, 11, 10),
              kit=["Storm Bolter", "Smoke Launchers", "Searchlight"])
    tr = transport_profile(u, name, "15 models (no Terminator Armour, Jump Packs, Bikes or Jetbikes)",
                           "One on each side of the hull, one at the rear", "Up to two models (top hatch)")
    cats = [category_link(gs.CAT_TRANSPORT, "Dedicated Transport", primary=True, key=u)]
    return entry(u, name, typ="unit", cost=65, cats=cats, profiles=[tr], entries=[m],
                 infolinks=rules_links(["Repair", "Open Topped", "Rhino Advancer Transport", EXPERIMENTAL], key=u),
                 groups=[take(u, "Vehicle Upgrades", STD_UPGRADES[:4]),
                         take(u, "Pintle-mounted Weapon", PINTLE, max_total=1)])


def experimental_config():
    eid = k("cfg", "Experimental")
    ff = k("focused-fire")
    small = [cond("any", "roster", "atMost", 2000, field=PTS, deep=False)]
    focused = entry(ff, "Focused Fire Configuration (one Legion Heavy Support Squad)",
                    constraints=[constraint(uid(ff, "max"), "max", 1, auto=True), unique(ff, 1, "roster")],
                    mods=[error_if("Focused Fire Configuration: only in an army of over 2,000 points.", small)],
                    infolinks=rules_links(["Focused Fire Configuration"], key=ff))
    return entry(eid, "Experimental Wargear and Units", cats=[
        category_link(gs.CAT_CONFIG, "Configuration", primary=True, key=eid)],
        constraints=[constraint(uid(eid, "max"), "max", 1, scope="force", deep=True)],
        infolinks=rules_links([EXPERIMENTAL, "Experimental Supplement", "Saturnine Exo-armour",
                               "Planned Additions (design notes)"], key=eid),
        entries=[focused])


def supplement_force():
    fid = k("force", "Experimental Supplement")

    def cl(cat_id, name, mx=None):
        c = category_link(cat_id, name, key=fid)
        if mx is not None:
            c.append(wrap("constraints", [constraint(uid(fid, name, "max"), "max", mx)]))
        return c
    links = [cl(gs.CAT_CONFIG, "Configuration"), cl(HQ, "HQ", 2), cl(ELITES, "Elites", 3),
             cl(FA, "Fast Attack", 3), cl(HS, "Heavy Support", 3), cl(gs.CAT_TRANSPORT, "Dedicated Transport")]
    return el("forceEntry", {"id": fid, "name": "Experimental Supplement (no compulsory selections)",
                             "hidden": "false"}, [wrap("categoryLinks", links)])


# ====================================================================== build
def build():
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS, multi_profile=MULTI, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    units = [experimental_config(), saturnine_command_squad(), saturnine_squad(), sabre(), arquitor(),
             rhino_advancer()]
    return catalogue(ARMY, units, [], force_entries=[supplement_force()])
