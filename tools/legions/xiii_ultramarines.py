"""XIII Legion - Ultramarines (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, allegiance_only, named_character, primarch, primarch_retinue,
                            retinue_links, command_squad_for, add_armoury_items, register_data)
from bsx import PTS, uid, cond, any_of, all_of, modifier, constraint, entry, link, group, category_link
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, gear, per_model, rules_links, unit_profile
from legiones2 import (slot, take, pool, transports, add_mods, add_to, walker_profile, foc, rite, model_swaps,
                       specials_decrement, tda_armoury)
from legiones2 import TROOPS, ELITES, FA, HQ, RETINUE_SHARED

LEGION = "XIII - Ultramarines"
LR = "Legiones Astartes (Ultramarines)"

RULES = {
    LR: ("Models with this special rule belong to the XIII Legion and use the Ultramarines Legion special rules: Codex "
         "Astartes and Flexible Command Structure."),
    "Codex Astartes": (
        "A Legion Tactical Squad of exactly ten models may be divided into two Combat Squads of five models before "
        "deployment. The Sergeant, specialist and heavy weapons, Legion Vexilla and Nuncio Vox may be divided as the "
        "Ultramarines player wishes. Each Combat Squad then counts as a separate unit for deployment, Morale, casualties, "
        "scoring and all other purposes. For Victory Points each is worth half the original unit's points (any fraction "
        "to the squad with the Sergeant). A Dedicated Transport must be assigned to one Combat Squad; only that squad may "
        "begin the battle embarked in it."),
    "Flexible Command Structure": (
        "An Ultramarines Detachment may include up to four HQ selections (the normal limit on models with Master of the "
        "Legion still applies). An Ultramarines army begins the battle with one additional Strategy Point (normal "
        "ProHammer rules)."),
    "Ultramarines Armoury": (
        "Legatine Axe (+20): any Ultramarines Independent Character with access to the Space Marine Armoury. Mantle of "
        "Ultramar (+20): an Ultramarines Praetor in Artificer Armour may exchange it for a Mantle of Ultramar. Breacher "
        "Power Weapons (+5 per model): any model in an Ultramarines Legion Breacher Siege Squad may replace its Bolter "
        "with a Power Weapon; such a model may not also take a Specialist Weapon that replaces its Bolter."),
    "Legatine Axe": ("A precisely balanced Power Weapon granting +1 Strength (Two-Handed). A model attacking with a "
                     "Legatine Axe does not receive the bonus Attack for fighting with two close-combat weapons."),
    "Mantle of Ultramar": ("Grants a 2+ Armour Save and Feel No Pain (5+). The bearer is immune to the Blind special "
                           "rule; this protection applies only to the bearer, not to a unit he has joined."),
    # Rites of War
    "The Logos Lectora": (
        "EFFECTS - Tactical Command: at the beginning of each Ultramarines player turn choose one command, active until "
        "the beginning of the next Ultramarines player turn: Full March (all Ultramarines non-Vehicle units may re-roll "
        "the Advance D6; the second result stands), Hold Fast (Ultramarines non-Vehicle units that remained stationary "
        "re-roll To Hit rolls of 1 for First Fire or Overwatch Fire and their Snap Fire hits on 5+; stationary "
        "Ultramarines Dreadnoughts also benefit) or Retribution Strike (all Ultramarines non-Vehicle units gain "
        "Counter-Attack; an Ultramarines Dreadnought not already engaged that is successfully charged gains +1 Attack "
        "that Assault phase).\n"
        "LIMITATIONS - One additional compulsory HQ choice, which must be a Legion Master of Signals Consul or a Damocles "
        "Command Rhino. One additional compulsory Troops choice. No more Vehicles with the Tank or Flyer type than "
        "Infantry units. Units may not deploy using Infiltrate or enter play by Deep Strike (normal Reserves allowed); "
        "units required to enter play by Deep Strike (e.g. Legion Drop Pods) may not be selected."),
    "Vigil Opertii Mission": (
        "EFFECTS - Vigil Auxilia: all Infantry units in the army's allied Imperialis Militia Detachment gain Infiltrate. "
        "Sacred Duty: they gain Implacable Advance and count as Scoring Units regardless of battlefield role. Overseers: "
        "Ultramarines Legion Reconnaissance Squads lose Support Squad and may fulfil compulsory Troops choices.\n"
        "LIMITATIONS - Loyalist Ultramarines Detachment only. The army must include an Allied Detachment from the "
        "Imperialis Militia & Cults Army List with both the Gene-crafted and Warrior Elite Provenances of War and no "
        "Inducted Levy Squads. The Ultramarines Detachment must include a Legion Vigilator Consul."),
    # units
    "Invictarus Honour Guard": (
        "One Invictarus Suzerain Squad may be selected as the retinue of an Ultramarines Praetor or a named Ultramarines "
        "Independent Character permitted to select a Command Squad. It does not occupy a separate Force Organisation "
        "slot; the character and the Suzerains count as a single HQ selection."),
    "Guided Warheads": (
        "When firing Frag missiles from their Cyclone Missile Launchers, Fulmentarus Terminators may fire at an enemy unit "
        "they cannot see if it is visible to a friendly model with a Nuncio Vox (not embarked, Falling Back, Pinned or in "
        "close combat). Such fire must use Frag missiles, counts as Barrage and follows the normal Barrage rules. Krak "
        "missiles may not use Guided Warheads."),
    "Coordinated Assault": ("If the Locutarus charge an enemy unit which suffered one or more hits from another friendly "
                            "Ultramarines unit in the preceding Shooting phase, they may re-roll To Hit rolls of 1 during "
                            "that Assault phase."),
    "Argean Power Sword": "An Argean Power Sword is a Master-crafted Power Weapon.",
    "Mortifier Bolter": "Mortifier Bolters are normal Bolters with the Poisoned (3+) and Pinning special rules.",
    "Hatred (Word Bearers)": "Hatred (see ProHammer Classic) against models with Legiones Astartes (Word Bearers).",
    # characters
    "First Master of the Legion": ("Friendly non-Vehicle Ultramarines units with at least one model within 12\" of "
                                   "Marius Gage may use his Leadership for Morale and Pinning tests."),
    "Master of Organisation": (
        "After both armies have deployed but before the first turn, select one Ultramarines Infantry unit which deployed "
        "normally; it may be redeployed anywhere wholly within the Ultramarines deployment zone (normal restrictions "
        "apply, not into Reserve). Independent Characters joined to it are redeployed with it."),
    "Calculated Response": "Marius Gage and any Ultramarines unit he has joined have Counter-Attack.",
    "Command Retinue (Gage)": ("Marius Gage may select a Legion Command Squad, Legion Terminator Command Squad or "
                               "Invictarus Suzerain Squad as his retinue (no separate Force Organisation slot)."),
    "The Saviour of Calth": ("Ventanus and any Ultramarines unit he has joined have Fearless while at least one model "
                             "from the unit is within 6\" of an objective."),
    "Practical Commander": ("After both armies have deployed but before the first turn, nominate one Legion Tactical "
                            "Squad; it gains Counter-Attack for the battle."),
    "Command Retinue (Ultramarines)": ("This character may select one Legion Command Squad (or an Invictarus Suzerain "
                                       "Squad, see Invictarus Honour Guard) as his retinue. It does not occupy a separate "
                                       "Force Organisation slot."),
    "Unorthodox Tactics": (
        "After deployment but before the first turn, choose Counter-Attack, Move Through Cover, Night Vision or Tank "
        "Hunters. Thiel and every model in his squad gain it for the battle, even if Thiel is later slain."),
    "Aeonid Thiel": (
        "One Legion Tactical Squad or Legion Veteran Squad may replace its Sergeant with Aeonid Thiel for +80 points. "
        "Thiel remains part of the squad for the entire battle; he is a Character but not an Independent Character. If "
        "the squad purchases Krak Grenades or Melta Bombs, Thiel receives the same upgrade at the normal squad cost. A "
        "Legion Tactical Squad led by Thiel may still be divided by Codex Astartes; Thiel joins one of the Combat Squads."),
    "Psychic Powers (Prayto)": ("Titus Prayto is a Psyker (Mastery Level 2) and selects two psychic powers from the normal "
                                "Psychic Power list, following all normal rules for Psykers and Disturbance in the Warp."),
    "Psychic Savant": ("Once during each Ultramarines player turn, Prayto may re-roll one failed Psychic Test (the second "
                       "result must be accepted)."),
    # Guilliman
    "Armour of Reason": "The Armour of Reason counts as Primarch Armour (1+ Armour Save, 4+ Invulnerable Save).",
    "Gladius Incandor": "A Master-crafted Power Weapon; attacks are resolved at +1 Strength and have Shred.",
    "Hand of Dominion": "A Master-crafted Power Fist with the Armourbane special rule.",
    "Master Strategist": ("Unless a rule states otherwise, the range of Roboute Guilliman's special rules which affect "
                          "friendly Ultramarines units is 18\"."),
    "Preternatural Strategy": (
        "After both armies have deployed but before the first turn, nominate one friendly Ultramarines unit. It may be "
        "redeployed anywhere it could legally have been deployed at the beginning of the battle (normal restrictions; "
        "not into Reserve unless it was already eligible)."),
    "Sire of Ultramar": ("Friendly Ultramarines units with at least one model within 12\" of Roboute Guilliman may "
                         "re-roll failed Morale tests (the second result must be accepted)."),
    "Theoretical / Practical": (
        "At the beginning of each Ultramarines turn choose a doctrine affecting friendly Ultramarines units with at least "
        "one model within 18\" of Guilliman until the beginning of the next Ultramarines turn: Advance (move up to 1\" "
        "further in the Movement phase), Fire (re-roll shooting To Hit rolls of 1) or Assault (re-roll close combat To Hit "
        "rolls of 1)."),
    "Primarch Retinue (Guilliman)": ("Roboute Guilliman may select a Legion Honour Guard Squad, Legion Terminator Command "
                                     "Squad or Invictarus Suzerain Squad as his Primarch Retinue."),
}

WEAPONS = {
    "Legatine Axe": ("-", "User +1", "-", "Power Weapon, Two-Handed"),
    "Argean Power Sword": ("-", "User", "-", "Power Weapon, Master-crafted"),
    "Mortifier Bolter": ('24"', "4", "5", "Rapid Fire, Poisoned (3+), Pinning"),
    "Gladius Incandor": ("-", "User +1", "-", "Power Weapon, Master-crafted, Shred"),
    "Hand of Dominion": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Master-crafted, Armourbane"),
    "Arbitrator": ('18"', "6", "3", "Assault 2, Rending, Master-crafted"),
}
WEAPON_RULES = {
    "Legatine Axe": ["Legatine Axe", "Two-Handed"],
    "Argean Power Sword": ["Master-Crafted"],
    "Mortifier Bolter": ["Mortifier Bolter", "Poison", "Pinning"],
    "Gladius Incandor": ["Master-Crafted", "Shred"],
    "Hand of Dominion": ["Master-Crafted", "Unwieldy", "Armourbane"],
    "Arbitrator": ["Rending", "Master-Crafted"],
}
WARGEAR = {
    "Mantle of Ultramar": (RULES["Mantle of Ultramar"], ["Feel No Pain"]),
    "Armour of Reason": (RULES["Armour of Reason"], []),
}


def register():
    register_data(rules=RULES, weapons=WEAPONS, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    # Land Raider Achilles as a Dedicated Transport (Fulmentarus Terminators may take any Land Raider pattern)
    L2.T.setdefault("Land Raider Achilles", uid("transport", "Land Raider Achilles"))


# ------------------------------------------------------------------ helpers
def model(u, name, mn, mx, cost, stats, kit, unit_type="Infantry", groups=(), mods=()):
    mid = uid("model", u, name)
    return mid, entry(mid, name, typ="model", cost=cost, mods=list(mods),
                      constraints=[constraint(uid(mid, "min"), "min", mn, auto=True),
                                   constraint(uid(mid, "max"), "max", mx, auto=True)],
                      profiles=[unit_profile(u, name, unit_type, *stats)],
                      links=[gear(mid, k) for k in kit], groups=list(groups))


def find_group(e, name):
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == name:
            return g
    raise KeyError(name)


# any Land Raider pattern (Phobos, Proteus, Achilles), a Dreadclaw or a Spartan
TDA_TRANSPORTS = ["Land Raider Phobos", "Land Raider Proteus", "Land Raider Achilles",
                  "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"]


# ------------------------------------------------------------------ units
SUZERAIN = uid("unit", "Invictarus Suzerain Squad")


def suzerain(key="Invictarus Suzerain Squad", root=True):
    u = uid("unit", key)
    kit = ["Artificer Armour", "Boarding Shield", "Bolt Pistol", "Legatine Axe"]
    lid = uid("model", u, "Suzerain Legate")
    sid = uid("model", u, "Invictarus Suzerain")
    smin, smax = uid(sid, "min"), uid(sid, "max")
    suz = entry(sid, "Invictarus Suzerain", typ="model", cost=45,
                mods=specials_decrement(sid, smin, smax, [lid], u),
                constraints=[constraint(smin, "min", 5, auto=True), constraint(smax, "max", 10, auto=True)],
                profiles=[unit_profile(u, "Invictarus Suzerain", "Infantry", 5, 4, 4, 4, 1, 4, 2, 9, "2+/5+")],
                links=[gear(sid, k) for k in kit])
    leg = entry(lid, "Suzerain Legate", typ="model", cost=65, constraints=[constraint(uid(lid, "max"), "max", 1)],
                profiles=[unit_profile(u, "Suzerain Legate", "Infantry (Character)", 5, 4, 4, 4, 1, 5, 3, 10, "2+/5+")],
                links=[gear(lid, k) for k in ["Artificer Armour", "Boarding Shield", "Legatine Axe"]],
                groups=[L2.pa_armoury(lid, u, 10, slots=["Bolt Pistol"], skip=("Artificer Armour",))])
    return entry(u, "Invictarus Suzerain Squad", typ="unit", cost=225 - 5 * 45,
                 cats=[foc(ELITES, "Elites", u)] if root else [],
                 constraints=[force_limit(u)] if root else [],
                 infolinks=rules_links([LR, "Stubborn", "Invictarus Honour Guard", "Legatine Axe"], key=u),
                 entries=[suz, leg, per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])])


def fulmentarus():
    u = uid("unit", "Fulmentarus Terminator Squad")
    kit = ["Cataphractii Terminator Armour", "Storm Bolter", "Power Fist", "Cyclone Missile Launcher"]
    did = uid("model", u, "Fulmentarus Decurion")
    tid = uid("model", u, "Fulmentarus Terminator")
    tmin, tmax = uid(tid, "min"), uid(tid, "max")
    terms = entry(tid, "Fulmentarus Terminator", typ="model", cost=65,
                  mods=specials_decrement(tid, tmin, tmax, [did], u),
                  constraints=[constraint(tmin, "min", 5, auto=True), constraint(tmax, "max", 10, auto=True)],
                  profiles=[unit_profile(u, "Fulmentarus Terminator", "Infantry", 4, 4, 4, 4, 1, 4, 2, 9, "2+/4+")],
                  links=[gear(tid, k) for k in kit])
    dec = entry(did, "Fulmentarus Decurion", typ="model", cost=85, constraints=[constraint(uid(did, "max"), "max", 1)],
                profiles=[unit_profile(u, "Fulmentarus Decurion", "Infantry (Character)", 4, 4, 4, 4, 1, 5, 3, 9,
                                       "2+/4+")],
                links=[gear(did, k) for k in kit],
                groups=[take(did, "Decurion Wargear", [("Grenade Harness", 10)]), tda_armoury(did)])
    return entry(u, "Fulmentarus Terminator Squad", typ="unit", cost=325 - 5 * 65, cats=[foc(ELITES, "Elites", u)],
                 constraints=[force_limit(u)],
                 infolinks=rules_links([LR, "Guided Warheads"], key=u),
                 entries=[terms, dec],
                 groups=[model_swaps(u, "Any model: replace Power Fist (any number)", u, [tid, did], [("Chainfist", 5)]),
                         transports(u, u, TDA_TRANSPORTS, orbital=False)])


def locutarus():
    u = uid("unit", "Locutarus Storm Squad")
    kit = ["Artificer Armour", "Jump Pack", "Bolt Pistol", "Argean Power Sword", "Frag Grenades"]
    lid, loc = model(u, "Locutarus", 4, 9, 35, (5, 4, 4, 4, 1, 4, 2, 9, "2+"), kit, unit_type="Jump Infantry")
    sid, sl = model(u, "Locutarus Strike Leader", 1, 1, 0, (5, 4, 4, 4, 1, 5, 3, 9, "2+"),
                    ["Artificer Armour", "Jump Pack", "Argean Power Sword", "Frag Grenades"],
                    unit_type="Jump Infantry (Character)",
                    groups=[L2.pa_armoury(uid(u, "leader"), u, 10, slots=["Bolt Pistol"], skip=("Artificer Armour",))])
    pistols, _ = pool(u, "Locutarus: replace Bolt Pistol (up to two)", u, [("Hand Flamer", 5), ("Plasma Pistol", 15)], 2)
    return entry(u, "Locutarus Storm Squad", typ="unit", cost=175 - 4 * 35, cats=[foc(FA, "Fast Attack", u)],
                 infolinks=rules_links([LR, "Coordinated Assault", "Argean Power Sword"], key=u),
                 entries=[sl, loc, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[pistols])


def nemesis_armoury(u):
    """Sergeant's 50-pt Armoury; his Artificer Armour and Phosphex Bombs count towards the cap (author, Q17)."""
    cap = L2.pa_armoury(uid(u, "sgt"), u, 10, skip=("Artificer Armour",))
    add_to(cap, "selectionEntryGroups", [take(uid(u, "sgt"), "Sergeant Wargear", [("Artificer Armour", 10),
                                                                               ("Phosphex Bomb", 10, 3)])])
    return cap


def nemesis():
    u = uid("unit", "Nemesis Destroyer Squad")
    kit = ["Power Armour", "Mortifier Bolter", "Bolt Pistol", "Chainsword", "Rad Grenades"]
    did, dests = model(u, "Nemesis Destroyer", 4, 9, 25, (4, 4, 4, 4, 1, 4, 1, 9, "3+"), kit)
    sid, sgt = model(u, "Nemesis Destroyer Sergeant", 1, 1, 0, (4, 4, 4, 4, 1, 4, 2, 9, "3+"), kit,
                     unit_type="Infantry (Character)",
                     groups=[slot(uid(u, "sgt"), "Replace Chainsword", "Chainsword",
                                  [("Rending Weapon", 5), ("Power Weapon", 10), ("Power Fist", 15),
                                   ("Thunder Hammer", 20)]),
                             nemesis_armoury(u)])
    heavy, _ = pool(u, "Nemesis Destroyers: replace Mortifier Bolter (1 per 5 models)", u,
                    [("Heavy Flamer", 10), ("Missile Launcher with Suspensor Web and Rad Missiles", 25)], 0, every=5)
    return entry(u, "Nemesis Destroyer Squad", typ="unit", cost=150 - 4 * 25, cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links([LR, "Counter-Attack", "Stubborn", "Destroyer Cadre", "Rad Grenades"], key=u),
                 entries=[sgt, dests, per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[heavy, L.one_each(u, "Squad Equipment (different models)",
                                           [("Legion Vexilla", 10), ("Nuncio Vox", 10)]),
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos",
                                           "Land Raider Proteus"])])


def telemechrus():
    u = uid("unit", "Honoured Telemechrus")
    e = entry(u, "Honoured Telemechrus", typ="unit", cost=215, cats=[foc(ELITES, "Elites", u)],
              constraints=[unique(u)],
              profiles=[walker_profile(u, "Honoured Telemechrus", 6, 5, 7, 13, 12, 10, 4, 4)],
              infolinks=rules_links(["Atomantic Shielding", "Fleet", "Hatred (Word Bearers)"], key=u),
              links=[gear(u, k) for k in ["Kheres Assault Cannon", "Dreadnought Close Combat Weapon",
                                          "Twin-linked Bolter", "Smoke Launchers", "Searchlight"]])
    return allegiance_only(e, loyalist=True)


# ------------------------------------------------------------------ characters
def characters():
    out = []
    g = uid("unit", "Marius Gage, First Master")
    out.append(named_character(LR, "Marius Gage, First Master", 190, (6, 5, 4, 4, 3, 5, 4, 10, "2+/4+"),
                               ["Artificer Armour", "Iron Halo", "Power Weapon", "Master-crafted Weapon", "Bolt Pistol",
                                "Frag Grenades"],
                               ["First Master of the Legion", "Master of Organisation", "Calculated Response",
                                "Command Retinue (Gage)"],
                               retinue=retinue_links("gage", [command_squad_for("gage", g),
                                                              L2.terminator_command_squad("gage"),
                                                              suzerain("gage-suzerains", root=False)]),
                               extra_groups=[take(g, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])],
                               profile_name="Marius Gage"))
    v = uid("unit", "Remus Ventanus")
    out.append(named_character(LR, "Remus Ventanus", 145, (5, 5, 4, 4, 2, 5, 3, 10, "2+/5+"),
                               ["Artificer Armour", "Refractor Field", "Power Weapon", "Bolt Pistol", "Nuncio Vox",
                                "Frag Grenades", "Legion Standard"],
                               ["The Saviour of Calth", "Practical Commander", "Command Retinue (Ultramarines)"],
                               retinue=retinue_links("ventanus", [command_squad_for("ventanus", v),
                                                                  suzerain("ventanus-suzerains", root=False)]),
                               master=False,
                               extra_groups=[take(v, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]))
    p = uid("unit", "Titus Prayto")
    out.append(named_character(LR, "Titus Prayto", 170, (5, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
                               ["Artificer Armour", "Refractor Field", "Force Weapon", "Psychic Hood", "Bolt Pistol",
                                "Frag Grenades"],
                               ["Psyker", "Psychic Powers (Prayto)", "Legion Support Officer", "Psychic Savant",
                                "Command Retinue (Ultramarines)"],
                               retinue=retinue_links("prayto", [command_squad_for("prayto", p),
                                                                suzerain("prayto-suzerains", root=False)]),
                               master=False, compulsory=False,
                               extra_groups=[take(p, "Wargear", [("Krak Grenades", 2)]),
                                             # "two psychic powers from the normal Psychic Power list" (Librarian list)
                                             psychic_powers(p, p, 2, PSY.LIBRARIAN)]))
    out.append(telemechrus())
    return out


GUILLIMAN = uid("unit", "Roboute Guilliman, the Avenging Son")


def guilliman():
    return primarch(LR, "Roboute Guilliman, the Avenging Son", 500, (7, 6, 6, 6, 6, 6, 5, 10, "1+/4+"),
                    ["Armour of Reason", "Gladius Incandor", "Hand of Dominion", "Arbitrator", "Frag Grenades"],
                    ["Primarch Armour", "Master Strategist", "Preternatural Strategy", "Sire of Ultramar",
                     "Theoretical / Practical", "Primarch Retinue (Guilliman)"],
                    retinue=primarch_retinue("guilliman", extra=[suzerain("guilliman-suzerains", root=False)]),
                    loyalist=True, profile_name="Roboute Guilliman")


# ------------------------------------------------------------------ Aeonid Thiel (replaces a Sergeant)
THIEL_IDS = []


def add_thiel(squad, sgt_name):
    u = squad.get("id")
    sgt_id = uid("model", u, sgt_name)
    tid = uid("thiel", u)
    THIEL_IDS.append(tid)
    thiel = entry(tid, "Aeonid Thiel (replaces the Sergeant)", typ="model", cost=80,
                  constraints=[constraint(uid(tid, "max"), "max", 1, auto=True), unique(tid)],
                  profiles=[unit_profile(tid, "Aeonid Thiel", "Infantry (Character)", 5, 5, 4, 4, 2, 5, 3, 10,
                                         "3+/5+")],
                  infolinks=rules_links([LR, "Aeonid Thiel", "Unorthodox Tactics"], key=tid),
                  links=[gear(tid, k) for k in ["Power Armour", "Refractor Field", "Power Weapon", "Bolt Pistol",
                                                "Purity Seals", "Frag Grenades"]])
    add_to(squad, "selectionEntries", [thiel])
    for e in squad.iter("selectionEntry"):
        if e.get("id") == sgt_id:
            add_mods(e, [modifier("decrement", uid(sgt_id, "min"), 1, conds=[has(tid, u)]),
                         modifier("decrement", uid(sgt_id, "max"), 1, conds=[has(tid, u)])])
            break
    else:
        raise KeyError(sgt_name)


# ------------------------------------------------------------------ extend
def extend(ctx):
    # Flexible Command Structure: up to four HQ (+2). Each +1 must sit on a different selection, so the second one is
    # carried by the (always present) Allegiance entry.
    ctx.legion_rules([LR, "Codex Astartes", "Flexible Command Structure", "Ultramarines Armoury"],
                     force_org=[gs.FOC_PLUS["HQ"]])
    add_mods(ctx.unit("Allegiance"), [modifier("add", "category", gs.FOC_PLUS["HQ"])])

    # Armoury
    add_armoury_items(ctx, [("Legatine Axe", 20)], who=("praetor", "centurion"))
    praetor = ctx.unit("Legion Praetor")
    armour = find_group(praetor, "Armour")
    mid = uid("link", armour.get("id"), "Mantle of Ultramar")
    add_to(armour, "entryLinks", [link(mid, W("Mantle of Ultramar"), "Mantle of Ultramar (replaces Artificer Armour)",
                                       cost=40, constraints=[constraint(uid(mid, "max"), "max", 1, auto=True)])])
    breacher = ctx.unit("Legion Breacher Siege Squad")
    bu = breacher.get("id")
    specials = ["Volkite Charger", "Volkite Caliver", "Rotor Cannon", "Flamer", "Meltagun", "Plasma Gun", "Lascutter",
                "Graviton Gun"]
    add_to(breacher, "selectionEntryGroups", [model_swaps(
        bu + "ultramarines", "Breacher Power Weapons: replace Bolter with Power Weapon (any number)", bu,
        [uid("model", bu, "Legion Breacher Marine")], [("Power Weapon", 5)], minus=[W(n) for n in specials])])
    rb = find_group(breacher, "Replace Bolter")
    add_to(rb, "entryLinks", [link(uid("link", rb.get("id"), "um-pw"), W("Power Weapon"), "Power Weapon", cost=5,
                                   constraints=[constraint(uid("link", rb.get("id"), "um-pw", "max"), "max", 1,
                                                           auto=True)])])

    # Aeonid Thiel
    add_thiel(ctx.unit("Legion Tactical Squad"), "Legion Tactical Sergeant")
    add_thiel(ctx.unit("Legion Veteran Squad"), "Legion Veteran Sergeant")
    add_mods(ctx.unit("Legion Tactical Squad"), [modifier(
        "add", "error", "Aeonid Thiel is unique: only one Legion Tactical or Veteran Squad may include him.",
        groups=[all_of(*[cond(t, "roster", "atLeast", 1) for t in THIEL_IDS])])])

    # new units
    roots = [suzerain(), fulmentarus(), locutarus(), nemesis(), *characters(), guilliman()]
    ctx.add_units(*roots)
    ctx.add_shared(L2.land_raider("Land Raider Achilles"))

    # Invictarus Suzerains as the retinue of a Praetor
    rg = find_group(praetor, "Retinue (no Force Organisation slot)")
    suz = suzerain("praetor-suzerains", root=False)
    RETINUE_SHARED.append(suz)
    add_to(rg, "entryLinks", [link(uid("link", rg.get("id"), suz.get("id")), suz.get("id"), suz.get("name"))])

    # Vigil Opertii: Recon Squads may fulfil compulsory Troops
    add_mods(ctx.unit("Legion Reconnaissance Squad"),
             [modifier("add", "category", gs.CAT_LINE, conds=[rite("Vigil Opertii Mission")])])

    # Rites of War
    deep = [L.TRANSPORTS["Legion Drop Pod"], L.TRANSPORTS["Anvillus Pattern Dreadclaw Drop Pod"],
            L2.T["Legion Dreadnought Drop Pod"]]
    ctx.add_rite("The Logos Lectora", RULES["The Logos Lectora"], errors=[
        ("the additional compulsory HQ choice must be a Legion Master of Signals Consul or a Damocles Command Rhino.",
         [cond(L.consul_id("Master of Signals"), "force", "lessThan", 1),
          cond(uid("unit", "Damocles Command Rhino"), "force", "lessThan", 1)]),
        ("the Detachment must include at least two HQ choices (one additional compulsory HQ).",
         [cond(HQ, "force", "lessThan", 2)]),
        ("the Detachment must include at least three compulsory Troops choices.",
         [cond(gs.CAT_LINE, "force", "lessThan", 3)]),
        ("units required to enter play by Deep Strike (Drop Pods, Dreadclaws) may not be selected.",
         [any_of(*[cond(d, "force", "atLeast", 1) for d in deep])]),
    ])
    ctx.add_rite("Vigil Opertii Mission", RULES["Vigil Opertii Mission"], errors=[
        ("only a Loyalist Ultramarines Detachment may use this Rite of War.", [cond(L.TRAITOR, "roster", "atLeast", 1)]),
        ("the Detachment must include a Legion Vigilator Consul.",
         [cond(L.consul_id("Vigilator"), "force", "lessThan", 1)]),
    ])
