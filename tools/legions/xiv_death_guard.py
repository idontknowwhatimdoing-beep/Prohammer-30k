"""XIV Legion - Death Guard (Forces of the Legions)."""
import copy

from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, allegiance_only, option, upgrade, clone, retinue_links,
                            command_squad_for, named_character, primarch, required_choice, add_group, add_entry,
                            add_armoury_items, add_weapon_variant, legion_units, LOW, TRAITOR, LOYALIST)
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile, has_tda, no_tda
from legiones2 import (slot, take, pool, choice, transports, add_mods, add_to, foc, rite_id, rite, TROOPS, ELITES,
                       HS, HQ, model_swaps, pa_armoury, tda_armoury, RETINUE_SHARED)
from legiones_wargear import ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR, ARMOURY

LEGION = "XIV - Death Guard"
LR = "Legiones Astartes (Death Guard)"

RULES = {
    LR: ("Models with this rule belong to the XIV Legion and use the Death Guard Legion special rules: Steady Assault, "
         "Resilience of Barbarus and Footslogging Killers."),
    "Steady Assault": "All Death Guard Infantry gain True Grit and Move Through Cover.",
    "True Grit": (
        "Models may count their bolter as a bolt pistol in close combat and may therefore gain an additional Attack if "
        "equipped with a second pistol or close combat weapon. However, a model using its bolter in this manner does not "
        "gain the bonus Attack for charging."),
    "Resilience of Barbarus": "All Death Guard models have Feel No Pain (4+) against wounds caused by Poisoned weapons.",
    "Footslogging Killers": (
        "A Death Guard army may take only 0-1 selection in total from the following units: Land Speeder Squadron, "
        "Attack Bike Squadron, Bike Squadron. Legion Sky Hunter Jetbike Squadrons and Legion Javelin Attack Speeder "
        "Squadrons also count towards this 0-1 limit."),
    # Armoury
    "Manreaper": (
        "A Two-Handed Power Weapon. At the beginning of each Assault phase in which the bearer is engaged in close combat, "
        "roll a D3: the bearer gains that many additional Attacks until the end of that Assault phase. If the bearer "
        "directs all of his attacks against a single enemy Independent Character or other separately targetable model, he "
        "gains only +1 Attack instead. The bearer receives no additional Attack for fighting with a second close-combat "
        "weapon. Any Death Guard Sergeant or Character permitted to select weapons from the Space Marine Armoury may "
        "purchase a Manreaper for 20 points. As an exception, Sergeants that could not normally select weapons from the "
        "Armoury may also purchase it."),
    "Alchem Flamer": (
        "A Death Guard model equipped with a Flamer or Heavy Flamer may replace it with an Alchem Flamer at no additional "
        "cost. A model permitted to select a Combi-flamer may instead select a Combi-Alchem Flamer for +4 points in "
        "addition to the normal cost of the Combi-flamer; the Alchem Flamer component follows the normal rules for "
        "Combi-weapons."),
    # Rites of War
    "The Reaping": (
        "EFFECTS - Superior Firepower: Legion Veteran Squads and Legion Heavy Support Squads may be selected as "
        "non-compulsory Troops choices; they may not fulfil compulsory Troops selections unless another rule specifically "
        "permits them to do so. Implacable: all Death Guard Infantry units gain Move Through Cover (including models "
        "wearing any form of Terminator Armour). Dark Arsenal: any Death Guard Character or Independent Character may "
        "purchase Rad Grenades for +10 points (this includes Sergeants; a Sergeant's Rad Grenades affect his whole unit "
        "until he is removed as a casualty).\n"
        "LIMITATIONS - Units in the Detachment may not make Advance Moves. Vehicles in the Detachment may not move Flat "
        "Out. Units in the Detachment may not deploy using Deep Strike; units which are required to deploy using Deep "
        "Strike may not be selected. The normal Death Guard restriction on Fast Attack choices from Footslogging Killers "
        "continues to apply."),
    "Creeping Death": (
        "TRAITOR ONLY.\nEFFECTS - Mist-clad: Death Guard Infantry models in open ground receive a 5+ Cover Save against "
        "shooting attacks provided there is no enemy model within 12\" (this does not improve an existing Cover Save). "
        "Bio-phage Bombardment: after both armies have deployed (including Scouts and Infiltrators), roll a D6 for every "
        "piece of terrain representing a wood or jungle; on a 4+ it becomes a fetid chemical mire for the rest of the "
        "battle: any Cover Save it provides is worsened by 1 (4+ becomes 5+, a 6+ is lost) and it counts as Dangerous "
        "Terrain to all models except models with the Legiones Astartes (Death Guard) special rule. Toxin Weapons: Frag "
        "Missiles fired by Death Guard models are resolved at Strength 5 instead of 4; Death Guard Frag Grenades used "
        "against Vehicles have Strength 5 + D6 Armour Penetration instead of 4 + D6. All other rules for Frag Grenades "
        "and Frag Missiles remain unchanged.\n"
        "LIMITATIONS - Only a Traitor Death Guard Detachment. The Detachment must include at least one Legion Heavy "
        "Support Squad whose Sergeant has been upgraded to a Siege Breaker. In missions with an Attacker and a Defender, "
        "the Death Guard must be the Attacker. The Detachment may not include a Fortification or an Allied Detachment."),
    # Units
    "Silent Retinue": (
        "A Death Guard character who would normally be permitted to select a Legion Terminator Command Squad may instead "
        "select one Deathshroud Terminator Squad as his retinue. The Deathshroud do not occupy a separate Force "
        "Organisation slot; the character and the Deathshroud count as a single HQ selection."),
    "Cataphractii (Deathshroud)": (
        "If the squad exchanges its Terminator Armour for Cataphractii Terminator Armour, it has a 2+/4+ Save and follows "
        "all normal rules and restrictions for Cataphractii Terminator Armour."),
    "Shrouded in Death": (
        "A Grave Warden Terminator Squad counts as being equipped with Defensive Grenades. All normal ProHammer rules for "
        "Defensive Grenades apply."),
    "Destroyer Cadre (Mortus Poisoners)": (
        "The Mortus Poisoners use the normal Destroyer Cadre rule from the Legiones Astartes Army List (only an "
        "Independent Character with the Moritat Consul upgrade - or Crysos Morturg - may join the squad)."),
    # Characters
    "Latent Psyker": (
        "Typhon is treated as a Psyker (Mastery Level 1) solely for the purpose of using Aura of Pestilence and suffering "
        "Perils of the Warp. He knows no other psychic powers. He takes the Psychic Test for Aura of Pestilence using "
        "Leadership 7 instead of the Leadership value shown in his profile."),
    "Aura of Pestilence": (
        "At the beginning of either player's Assault phase, Typhon may attempt to invoke Aura of Pestilence. If the "
        "Psychic Test is passed, every enemy model within 2\" of Typhon suffers -1 Attack (minimum 1) until the end of "
        "that Assault phase. If it is failed, every friendly model within 2\" of Typhon instead suffers -1 Attack "
        "(minimum 1) until the end of that Assault phase. Typhon may fight normally during an Assault phase in which Aura "
        "of Pestilence is used."),
    "Command Retinue (Typhon)": (
        "Typhon may select either a Deathshroud Terminator Squad or a Legion Terminator Command Squad as his retinue. The "
        "selected squad does not occupy a separate Force Organisation slot."),
    "Psychic Powers (Morturg)": (
        "Morturg selects one psychic power from the Telepathy ProHammer Psychic Power list. He follows all normal "
        "ProHammer rules for Psykers and Mastery Level 1."),
    "Master of Ambush": (
        "Morturg and one Death Guard Infantry unit he has joined before deployment may deploy using Infiltrate. Morturg "
        "must remain joined to that unit when it is deployed."),
    "Destroyer Officer": (
        "Morturg may join a Legion Destroyer Squad or Mortus Poisoner Squad despite the normal restrictions imposed by "
        "Destroyer Cadre."),
    "Command Retinue (Morturg)": (
        "Morturg may select one Mortus Poisoner Squad as his retinue. The selected squad does not occupy a separate Force "
        "Organisation slot."),
    "Force of Destruction": (
        "Durak Rask and any Death Guard Infantry unit he has joined have the Tank Hunters special rule."),
    "Command Retinue (Death Guard Captains)": (
        "The character may select one Legion Command Squad as his retinue. The selected squad does not occupy a separate "
        "Force Organisation slot."),
    "The Eater of Lives": (
        "The first time Grulgor is reduced to 0 Wounds, do not immediately remove him as a casualty. Roll a D6: on a 1-4 "
        "remove Grulgor normally; on a 5+ Grulgor remains in play with 1 Wound remaining and gains Daemon, Fearless and "
        "Feel No Pain (5+) for the remainder of the battle. This rule may only be used once per battle."),
    "Libertas": (
        "A Two-Handed, Master-crafted Power Weapon which grants Garro +2 Strength. Garro receives no additional Attack for "
        "fighting with a second close-combat weapon while using Libertas."),
    "Aquila Imperator": (
        "Grants Garro a 4+ Invulnerable Save (already included in his profile). Whenever Garro or a unit he has joined "
        "would be affected by an enemy psychic power, roll a D6: on a 5+ that psychic power is nullified and has no effect "
        "upon Garro or his unit. Only one Aquila Imperator nullification roll may be attempted against each psychic "
        "power."),
    # Mortarion
    "Barbaran Plate": "Barbaran Plate counts as Primarch Armour.",
    "Silence": (
        "Silence is a Two-Handed Power Weapon. Attacks made with Silence are resolved at +1 Strength and have the Rampage "
        "special rule. Any unsaved Wound inflicted by Silence against a model without the Primarch special rule becomes "
        "a Massive Wound and inflicts D3 Wounds instead of one Wound."),
    "Barbaran Endurance": "Mortarion has Feel No Pain (5+).",
    "Witch-Spite": (
        "Whenever Mortarion or a unit he has joined makes a Deny the Witch roll, a failed roll may be re-rolled. In "
        "addition, Mortarion's Adamantium Will grants a +2 bonus to Deny the Witch rolls instead of the normal +1."),
    "The Reaper's Advance": (
        "Friendly Death Guard Infantry within 12\" of Mortarion may fire Rapid Fire weapons as though they had remained "
        "stationary. In addition, they may re-roll failed Pinning tests."),
    "Toxic Miasma": (
        "Enemy non-Vehicle models in base contact with Mortarion suffer -1 Toughness. This penalty lasts only while the "
        "model remains in base contact with Mortarion."),
    "Poison Cannot Kill Death": (
        "Poisoned attacks made against Mortarion do not use their normal fixed To Wound value. Instead, resolve the attack "
        "using its Strength against Mortarion's Toughness normally. If a Poisoned attack has no Strength characteristic, "
        "it may only wound Mortarion on an unmodified roll of 6."),
    "Primarch Retinue (Mortarion)": (
        "Mortarion may select one Deathshroud Terminator Squad as his Primarch Retinue. He may not select a Legion Honour "
        "Guard Squad or Legion Terminator Command Squad. A Deathshroud Terminator Squad selected in this manner does not "
        "occupy an additional Force Organisation selection and otherwise follows the normal Primarch Retinue rules."),
    # Mortarion, Prince of Decay
    "Daemonic Barbaran Plate": (
        "Mortarion, Prince of Decay has a 2+ Armour Save and a 4+ Invulnerable Save (as shown in his profile). It has no "
        "further rules."),
    "Burdened Wings": (
        "Mortarion may move over intervening models and terrain as though using a Jump Pack, but may never move more than "
        "9\" during the Movement phase. Mortarion may never join another unit and no model may join him."),
    "Silence (Daemon Primarch)": (
        "Silence is a Two-Handed, Master-crafted Power Weapon which grants Mortarion +2 Strength. Instead of making his "
        "normal close-combat attacks, Mortarion may make one attack against every enemy model in base contact with him."),
    "The Reaper's Miasma": (
        "At the beginning of each enemy turn, every enemy unit within 18\" of Mortarion suffers: within 6\" - D3 S5 AP4 "
        "hits, Poisoned (3+); 6-12\" - D3 S4 AP4 hits, Poisoned (3+); 12-18\" - 1 S4 AP4 hit, Poisoned (3+). Death Guard "
        "models and Daemons of Nurgle are immune."),
    "Reluctant Sorcerer": (
        "Mortarion is a Mastery Level 2 Psyker, but always takes Psychic Tests using Leadership 8, regardless of his "
        "normal Leadership or modifiers which would increase it. He knows Miasma of Pestilence, Curse of Decay and "
        "Nurgle's Rot."),
    "Miasma of Pestilence": (
        "Phase: beginning of the enemy Assault phase. Range 12\". Choose one enemy unit within range and take a Psychic "
        "Test. If successful, the unit suffers -1 Initiative and -1 Attack (minimum 1) until the end of the Assault "
        "phase."),
    "Curse of Decay": (
        "Phase: Mortarion's Shooting phase. Range 18\". Choose one enemy unit within range and take a Psychic Test. If "
        "successful, the unit treats all terrain, including open ground, as Difficult Terrain until the beginning of "
        "Mortarion's next turn."),
    "Nurgle's Rot": (
        "Phase: Mortarion's Shooting phase. Range 12\". Choose one enemy unit within range and take a Psychic Test. If "
        "successful, the target suffers D6 Strength 4 AP4 hits with Poisoned (3+)."),
    "Sons of the Plague Father": (
        "If Daemon Primarch Mortarion is included in a Death Guard army, a Death Guard Infantry unit composed entirely of "
        "models wearing Power Armour or Artificer Armour may be upgraded to Plague Marines for +7 points per model. "
        "Models upgraded in this manner gain +1 Toughness, Feel No Pain (5+) and Slow and Purposeful. Models upgraded to "
        "Plague Marines may not benefit from Move Through Cover, regardless of its source. Their normal maximum charge "
        "distance is reduced from 6\" to 5\", and they may not benefit from rules which increase their Movement or charge "
        "distance. The Relentless component of Slow and Purposeful applies normally. Jump Infantry, Breacher Siege Squads "
        "(Hardened Power Armour) and Independent Characters in Power Armour or Artificer Armour may also be upgraded. An "
        "Independent Character may only join a Plague Marine unit if he has been upgraded to a Plague Marine as well."),
    "Only one Mortarion": ("Mortarion, Prince of Decay may only be selected for a Death Guard army. An army may not "
                           "include both Mortarion, Prince of Decay and Mortarion in his mortal form."),
}

WEAPONS_ = {
    "Manreaper": ("-", "User", "-", "Power Weapon, Two-Handed, Manreaper (+D3 Attacks)"),
    "Alchem Flamer": ("Template", "2", "5", "Assault 1, Poisoned (3+)"),
    "Death Cloud Projector": ("Template", "1", "4", "Assault 1, Poisoned (3+), Ignores Cover"),
    "Libertas": ("-", "User +2", "-", "Power Weapon, Two-Handed, Master-crafted"),
    "Silence": ("-", "User +1", "-", "Power Weapon, Two-Handed, Rampage, Massive Wound (D3) vs non-Primarchs"),
    "Lantern": ('18"', "8", "2", "Assault 1, Armourbane, Master-crafted"),
    "Silence (Daemon Primarch)": ("-", "User +2", "-", "Power Weapon, Two-Handed, Master-crafted"),
    "Lantern (Daemon Primarch)": ('18"', "8", "2", "Assault 1, Master-crafted, Armourbane"),
}
MULTI = {
    "Assault Grenade Launcher": {
        "Assault Grenade Launcher - Krak": ('18"', "6", "4", "Assault 2"),
        "Assault Grenade Launcher - Toxin": ('18"', "1", "5", "Assault 4, Poisoned (3+), Ignores Cover")},
}
WEAPON_RULES_ = {
    "Manreaper": ["Manreaper", "Two-Handed"],
    "Alchem Flamer": ["Poisoned"],
    "Death Cloud Projector": ["Poisoned", "Ignores Cover"],
    "Assault Grenade Launcher": ["Poisoned", "Ignores Cover"],
    "Libertas": ["Libertas", "Two-Handed", "Master-Crafted"],
    "Silence": ["Silence", "Two-Handed", "Rampage"],
    "Lantern": ["Armourbane", "Master-Crafted"],
    "Silence (Daemon Primarch)": ["Silence (Daemon Primarch)", "Two-Handed", "Master-Crafted"],
    "Lantern (Daemon Primarch)": ["Armourbane", "Master-Crafted"],
}
WARGEAR_ = {
    "Barbaran Plate": ("Counts as Primarch Armour.", ["Primarch Armour"]),
    "Daemonic Barbaran Plate": RULES["Daemonic Barbaran Plate"],
    "Aquila Imperator": RULES["Aquila Imperator"],
}

DEATHSHROUD = uid("unit", "Deathshroud Terminator Squad")
GRAVE_WARDEN = uid("unit", "Grave Warden Terminator Squad")
MORTUS = uid("unit", "Mortus Poisoner Squad")
MORTARION = uid("unit", "Mortarion, the Reaper")
DAEMON_MORTARION = uid("unit", "Mortarion, Prince of Decay")
FOOTSLOG = ["Legion Land Speeder Squadron", "Legion Attack Bike Squadron", "Legion Bike Squadron",
            "Legion Sky Hunter Jetbike Squadron", "Legion Javelin Attack Speeder Squadron"]


def register():
    register_data(rules=RULES, weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_, multi_profile=MULTI)
    # Combi-Alchem Flamer: Bolter + Alchem Flamer
    WEAPONS["Combi-Alchem Flamer"] = ["Bolter", "Alchem Flamer"]
    WEAPON_RULES["Combi-Alchem Flamer"] = ["Combi-Weapon", "Poisoned"]
    # Legion Destroyer Company: Mortus Poisoner Squads count like Legion Destroyer Squads
    L2.TROOP_RITES["Mortus Poisoner Squad"] = ["Legion Destroyer Company"]
    L2.NORMAL_ROLE["Mortus Poisoner Squad"] = ELITES


# ------------------------------------------------------------------ local helpers
def _unit_type(e):
    ps = e.find("profiles")
    if ps is None:
        return None
    for p in ps:
        if p.get("typeName") == "Unit":
            for c in p.iter("characteristic"):
                if c.get("name") == "Unit Type":
                    return c.text or ""
    return None


def all_unique(ctx):
    out, seen = [], set()
    for e in ctx.all_entries():
        if id(e) not in seen:
            seen.add(id(e))
            out.append(e)
    return out


def _is_vehicle_root(e):
    profs = [p.get("typeName") for p in e.iter("profile")]
    return bool(profs) and all(t in ("Vehicle", "Walker", "Weapon", "Transport") for t in profs)


def model(u, name, cost, mn, mx, utype, stats, kit, groups=(), mods=(), rules_=(), prof_mods=(), auto=False):
    mid = uid("model", u, name)
    prof = unit_profile(u, name, utype, *stats)
    if prof_mods:
        prof.insert(0, wrap("modifiers", list(prof_mods)))
    return mid, entry(mid, name, typ="model", cost=cost, mods=list(mods),
                      constraints=[constraint(uid(mid, "min"), "min", mn, auto=auto),
                                   constraint(uid(mid, "max"), "max", mx, auto=auto)],
                      profiles=[prof], links=[gear(mid, k) for k in kit],
                      groups=list(groups), infolinks=rules_links(list(rules_), key=mid))


def sv_mod(value, conds):
    return modifier("set", gs.char_id("Unit", "Sv"), value, conds=conds)


TERMINATOR_TRANSPORTS = ["Land Raider Phobos", "Land Raider Proteus", "Anvillus Pattern Dreadclaw Drop Pod",
                         "Legion Spartan Assault Tank"]


# ------------------------------------------------------------------ units
def deathshroud(key="Deathshroud Terminator Squad", root=True):
    u = uid("unit", key)
    arm_title = "Terminator Armour Pattern (entire squad)"
    cata = uid("choice", u, arm_title, "Cataphractii Terminator Armour")
    armour = choice(u, arm_title, [("Terminator Armour", 0, False, ["Terminator Armour"], []),
                                   ("Cataphractii Terminator Armour", 0, False, ["Cataphractii Terminator Armour"],
                                    ["Cataphractii (Deathshroud)"])],
                    required=True, default="Terminator Armour")
    mid, m = model(u, "Deathshroud Terminator", 55, 2, 7, "Infantry", (5, 4, 4, 4, 2, 4, 2, 9, "2+/5+"),
                   ["Manreaper", "Alchem Flamer"], prof_mods=[sv_mod("2+/4+", [has(cata, u)])])
    m.find("profiles")[0].set("name", "Deathshroud")
    rl = [LR, "Fearless", "Silent Retinue"] + ([] if root else ["Retinue"])
    return entry(u, "Deathshroud Terminator Squad", typ="unit", cost=110 - 2 * 55,
                 cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links(rl, key=u),
                 entries=[m, per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[armour, transports(u, u, TERMINATOR_TRANSPORTS, orbital=False)])


def grave_wardens():
    u = GRAVE_WARDEN
    kit = ["Cataphractii Terminator Armour", "Assault Grenade Launcher", "Death Cloud Projector", "Power Fist"]
    gid, gw = model(u, "Grave Warden", 50, 4, 9, "Infantry", (4, 4, 4, 4, 1, 4, 2, 9, "2+/4+"), kit)
    cid = uid("model", u, "Chem-master")
    _, cm = model(u, "Chem-master", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 3, 9, "2+/4+"), kit,
                  groups=[take(cid, "Chem-master Wargear", [("Grenade Harness", 10)]), tda_armoury(cid)])
    return entry(u, "Grave Warden Terminator Squad", typ="unit", cost=250 - 4 * 50, cats=[foc(HS, "Heavy Support", u)],
                 infolinks=rules_links([LR, "Shrouded in Death"], key=u),
                 entries=[cm, gw],
                 groups=[model_swaps(u, "Any model: replace Power Fist (any number)", u, [gid, cid], [("Chainfist", 5)]),
                         transports(u, u, TERMINATOR_TRANSPORTS, orbital=False)])


def mortus_poisoners(key="Mortus Poisoner Squad", root=True):
    u = uid("unit", key)
    kit = ["Power Armour", "Alchem Flamer", "Bolt Pistol", "Chainsword", "Frag Grenades", "Rad Grenades"]
    _, mp = model(u, "Mortus Poisoner", 20, 4, 9, "Infantry", (4, 4, 4, 4, 1, 4, 1, 9, "3+"), kit)
    pid = uid("model", u, "Poison-master")
    _, pm = model(u, "Poison-master", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 2, 9, "3+"), kit,
                  groups=[slot(pid, "Replace Chainsword", "Chainsword",
                               [("Rending Weapon", 5), ("Power Weapon", 10), ("Power Fist", 15)]),
                          take(pid, "Poison-master Wargear", [("Artificer Armour", 10), ("Phosphex Bomb", 10, 3)]),
                          pa_armoury(pid, u, 10, slots=["Bolt Pistol"], skip=("Artificer Armour",))])
    phos, _ = pool(u, "Phosphex Bomb (one Mortus Poisoner per five models)", u, [("Phosphex Bomb", 10)], 0, every=5)
    # Legion Destroyer Company (Forbidden Arsenal): up to two per five models
    rad, rad_mx = pool(u, "Legion Destroyer Company: Missile Launcher (up to 2 per 5 models)", u,
                       [("Missile Launcher with Suspensor Web and Rad Missiles", 25)], 0)
    no_dc = [cond(rite_id("Legion Destroyer Company"), "force", "lessThan", 1)]
    add_mods(rad, [modifier("increment", rad_mx, 2, conds=[rite("Legion Destroyer Company")],
                            repeats=[repeat("model", u, 5)]),
                   modifier("set", "hidden", "true", conds=no_dc)])
    rl = [LR, "Counter-Attack", "Destroyer Cadre", "Destroyer Cadre (Mortus Poisoners)"] + ([] if root else ["Retinue"])
    return entry(u, "Mortus Poisoner Squad", typ="unit", cost=150 - 4 * 20,
                 mods=L2.troop_role_mods("Mortus Poisoner Squad") if root else [],
                 cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links(rl, key=u),
                 entries=[pm, mp, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[phos, rad, transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                                      "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos"])])


# ------------------------------------------------------------------ characters
DS_RETINUE = None


def ds_retinue():
    global DS_RETINUE
    if DS_RETINUE is None:
        DS_RETINUE = deathshroud("Deathshroud Terminator Squad (Retinue)", root=False)
    return DS_RETINUE


def characters():
    out = []
    t = uid("unit", "Calas Typhon, First Captain")
    out.append(named_character(
        LR, "Calas Typhon, First Captain", 195, (6, 5, 4, 4, 3, 5, 3, 9, "2+/4+"),
        ["Cataphractii Terminator Armour", "Manreaper", "Alchem Flamer"],
        ["Latent Psyker", "Command Retinue (Typhon)"],
        retinue=retinue_links("typhon", [ds_retinue(), L2.terminator_command_squad("typhon")]),
        extra_groups=[psychic_powers(t, t, fixed=["Aura of Pestilence"])],
        min_points=1500, loyalist=False, profile_name="Calas Typhon"))
    m = uid("unit", "Crysos Morturg")
    out.append(named_character(
        LR, "Crysos Morturg", 175, (5, 5, 4, 4, 3, 5, 3, 9, "3+/5+"),
        ["Power Armour", "Refractor Field", "Power Weapon", "Combi-Alchem Flamer", "Bolt Pistol", "Frag Grenades",
         "Rad Grenades"],
        ["Stubborn", "Psyker", "Psychic Powers (Morturg)", "Master of Ambush", "Destroyer Officer",
         "Command Retinue (Morturg)"],
        retinue=retinue_links("morturg", [mortus_poisoners("morturg-poisoners", root=False)]),
        master=False, loyalist=True,
        extra_groups=[take(m, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)]),
                      psychic_powers(m, m, 1, ["Telepathy"])]))
    r = uid("unit", "Durak Rask")
    out.append(named_character(
        LR, "Durak Rask", 165, (5, 5, 4, 4, 3, 4, 3, 9, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Thunder Hammer", "Volkite Serpenta", "Nuncio Vox", "Phosphex Bomb",
         "Frag Grenades"],
        ["Force of Destruction", "Command Retinue (Death Guard Captains)"],
        retinue=retinue_links("rask", [command_squad_for("rask", r)]), loyalist=False,
        extra_groups=[take(r, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]))
    g = uid("unit", "Ignatius Grulgor")
    out.append(named_character(
        LR, "Ignatius Grulgor", 165, (6, 5, 4, 4, 3, 5, 3, 10, "3+/5+"),
        ["Power Armour", "Refractor Field", "Power Weapon", "Bolter", "Bolt Pistol", "Frag Grenades"],
        ["The Eater of Lives", "Command Retinue (Death Guard Captains)"],
        retinue=retinue_links("grulgor", [command_squad_for("grulgor", g)]), loyalist=False,
        extra_groups=[take(g, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]))
    n = uid("unit", "Nathaniel Garro")
    out.append(named_character(
        LR, "Nathaniel Garro", 165, (6, 5, 4, 4, 3, 5, 3, 9, "2+/4+"),
        ["Artificer Armour", "Aquila Imperator", "Libertas", "Bolt Pistol", "Frag Grenades"],
        ["Command Retinue (Death Guard Captains)"],
        retinue=retinue_links("garro", [command_squad_for("garro", n)]), master=False, loyalist=True,
        extra_groups=[take(n, "Wargear", [("Krak Grenades", 2)])]))
    return out


def mortarion():
    return primarch(LR, "Mortarion, the Reaper", 500, (7, 6, 6, 7, 6, 5, 4, 10, "1+"),
                    ["Barbaran Plate", "Silence", "Lantern", "Phosphex Bomb", "Frag Grenades"],
                    ["Primarch Armour", "Barbaran Endurance", "Witch-Spite", "The Reaper's Advance", "Toxic Miasma",
                     "Poison Cannot Kill Death", "Primarch Retinue (Mortarion)"],
                    retinue=retinue_links("mortarion", [ds_retinue()], title="Primarch Retinue"),
                    other=DAEMON_MORTARION, profile_name="Mortarion")


def daemon_mortarion():
    return primarch("Daemon Primarchs", "Mortarion, Prince of Decay", 650, (7, 6, 7, 8, 8, 4, 5, 10, "2+/4++"),
                    ["Silence (Daemon Primarch)", "Lantern (Daemon Primarch)", "Daemonic Barbaran Plate"],
                    ["Daemon", "Fear", "Fearless", "Eternal Warrior", "Feel No Pain", "Adamantium Will",
                     "Poison Cannot Kill Death", "Master of the Legion", "Psyker", "Burdened Wings", "The Reaper's Miasma",
                     "Reluctant Sorcerer", "Sons of the Plague Father", "Only one Mortarion"],
                    other=MORTARION, unit_type="Monstrous Creature (Character)", loyalist=False,
                    extra_groups=[psychic_powers(DAEMON_MORTARION, DAEMON_MORTARION,
                                                 fixed=["Miasma of Pestilence", "Curse of Decay", "Nurgle's Rot"])])


# ------------------------------------------------------------------ Legion-wide changes


def add_manreaper(ctx):
    """Manreaper (+20): Praetor/Centurion Armoury and every Sergeant/Champion 50-pt Armoury, including the wargear-only
    ones (author: Sergeants that could not normally select weapons may take it as an exception)."""
    add_armoury_items(ctx, [("Manreaper", 20)])


def alchem_variants(roots, bases, new_name, extra):
    """Next to every Flamer-type option in a choice group, offer new_name once per group for the cheapest
    replaced weapon's cost + extra."""
    base_ids = {W(b) for b in bases}
    new_id = W(new_name)
    seen = set()
    for r in roots:
        for g in r.iter("selectionEntryGroup"):
            if id(g) in seen:
                continue
            seen.add(id(g))
            links = g.find("entryLinks")
            if links is None or any(lk.get("targetId") == new_id for lk in links):
                continue
            found = [lk for lk in links if lk.get("targetId") in base_ids]
            if not found:
                continue

            def cost_of(lk):
                cs = lk.find("costs")
                return float(cs[0].get("value")) if cs is not None and len(cs) else 0
            best = min(found, key=cost_of)
            cons = []
            if any(c.get("type") == "max" for c in best.iter("constraint")):
                cons = [constraint(uid(best.get("id"), "dg-variant", new_name, "max"), "max", 1, auto=True)]
            new = link(uid(best.get("id"), "dg-variant", new_name), new_id, new_name,
                       cost=int(cost_of(best) + extra) or None, constraints=cons)
            if g.get("defaultSelectionEntryId") is not None:
                new.set("sortIndex", str(int(best.get("sortIndex") or 1) + 100))
            links.append(new)


def add_alchem(ctx):
    """Alchem Flamer for Flamers / Heavy Flamers (same cost), Combi-Alchem Flamer for Combi-flamers (+4), on all
    entries (vehicles and Dreadnoughts included). Model-count modifiers that count a replaced weapon also count its Alchem version."""
    roots = all_unique(ctx)
    alchem_variants(roots, ["Flamer", "Heavy Flamer", "Heavy Flamer with Suspensor Web"], "Alchem Flamer", 0)
    alchem_variants(roots, ["Combi-Flamer"], "Combi-Alchem Flamer", 4)
    mapping = {W("Flamer"): W("Alchem Flamer"), W("Heavy Flamer"): W("Alchem Flamer"),
               W("Heavy Flamer with Suspensor Web"): W("Alchem Flamer"), W("Combi-Flamer"): W("Combi-Alchem Flamer")}
    for r in roots:
        for ms in list(r.iter("modifiers")):
            for m in list(ms):
                reps = m.find("repeats")
                if reps is None or len(reps) != 1 or reps[0].get("childId") not in mapping:
                    continue
                c = copy.deepcopy(m)
                c.find("repeats")[0].set("childId", mapping[reps[0].get("childId")])
                # avoid double counting if the same modifier already exists for the variant
                if not any(x.find("repeats") is not None and len(x.find("repeats")) == 1 and
                           x.find("repeats")[0].get("childId") == c.find("repeats")[0].get("childId") and
                           x.get("field") == c.get("field") for x in ms):
                    ms.append(c)


def add_dark_arsenal(ctx):
    """The Reaping - Dark Arsenal: any Death Guard Character / Independent Character may buy Rad Grenades (+10)."""
    no_rite = [cond(rite_id("The Reaping"), "force", "lessThan", 1)]
    rad = W("Rad Grenades")
    seen = set()
    for r in ctx.all_entries():
        if _is_vehicle_root(r):
            continue
        cats = {c.get("targetId") for c in r.iter("categoryLink")}
        if gs.CAT_PRIMARCH in cats:
            continue
        for e in [r] + list(r.iter("selectionEntry")):
            if id(e) in seen:
                continue
            seen.add(id(e))
            t = _unit_type(e)
            if not t or "Character" not in t:
                continue
            own = e.find("entryLinks")
            if own is not None and any(lk.get("targetId") == rad for lk in own):
                continue
            eid = uid("dg-dark-arsenal", e.get("id"))
            add_to(e, "selectionEntries", [entry(
                eid, "Rad Grenades (The Reaping: Dark Arsenal)", cost=10, links=[gear(eid, "Rad Grenades")],
                constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                mods=[modifier("set", "hidden", "true", conds=no_rite), modifier("set", uid(eid, "max"), 0,
                                                                                conds=no_rite)])])


PM_ARMOUR = ["Power Armour", "Artificer Armour", "Hardened Power Armour"]


def _t_mod(p, eid, scope):
    tval = None
    for c in p.iter("characteristic"):
        if c.get("name") == "T":
            tval = c.text
    if tval and tval.isdigit():
        mod = modifier("set", gs.char_id("Unit", "T"), str(int(tval) + 1), conds=[has(eid, scope)])
        ms = p.find("modifiers")
        if ms is None:
            p.insert(0, wrap("modifiers", [mod]))
        else:
            ms.append(mod)


def add_plague_marines(ctx):
    """Sons of the Plague Father: Infantry / Jump Infantry units made only of Power, Artificer or Hardened Power Armour
    models, and Independent Characters in Power / Artificer Armour, may become Plague Marines (+7 per model) while
    Mortarion, Prince of Decay is in the army."""
    pa = {W(n) for n in PM_ARMOUR}
    no_daemon = [cond(DAEMON_MORTARION, "roster", "lessThan", 1)]
    hide = [modifier("set", "hidden", "true", conds=no_daemon)]
    rl = ["Sons of the Plague Father", "Feel No Pain", "Slow and Purposeful"]
    done = []
    for u in all_unique(ctx):
        if u.get("type") != "unit":
            continue
        cats = {c.get("targetId") for c in u.iter("categoryLink")}
        if gs.CAT_PRIMARCH in cats:
            continue
        uid_ = u.get("id")
        eid = uid("dg-plague-marines", uid_)
        models = [m for m in u.iter("selectionEntry") if m.get("type") == "model"]
        if models:
            ok = True
            for m in models:
                t = _unit_type(m) or ""
                links = m.find("entryLinks")
                if (not t.startswith(("Infantry", "Jump Infantry")) or links is None
                        or not any(lk.get("targetId") in pa for lk in links)):
                    ok = False
                    break
            if not ok:
                continue
            add_to(u, "selectionEntries", [entry(
                eid, "Plague Marines (entire unit, Sons of the Plague Father)", cost=0,
                constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                mods=[modifier("increment", PTS, 7, repeats=[repeat("model", uid_, 1)]),
                      modifier("set", uid(eid, "max"), 0, conds=no_daemon)] + hide,
                infolinks=rules_links(rl, key=eid))])
            for m in models:
                for p in m.iter("profile"):
                    if p.get("typeName") == "Unit":
                        _t_mod(p, eid, uid_)
            done.append(u.get("name"))
            continue
        # single-model characters (Praetor, Centurion, named characters): Infantry (Character) with Power / Artificer
        # Armour available; not while wearing Terminator Armour or riding a Bike / Jetbike
        t = _unit_type(u) or ""
        if not t.startswith(("Infantry", "Jump Infantry")) or "Character" not in t:
            continue
        own = u.find("entryLinks")
        fixed = own is not None and any(lk.get("targetId") in pa for lk in own)
        chosen = any(lk.get("targetId") in pa for g in u.iter("selectionEntryGroup") for lk in g.iter("entryLink")
                     if g.get("name") == "Armour")
        if not (fixed or chosen):
            continue
        bad = has_tda(uid_, deep=False) + [has(W("Space Marine Bike"), uid_, deep=False)]
        add_to(u, "selectionEntries", [entry(
            eid, "Plague Marine (Sons of the Plague Father)", cost=7,
            constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
            mods=[modifier("set", uid(eid, "max"), 0, conds=no_daemon),
                  modifier("add", "error", "Plague Marine: only a model in Power Armour or Artificer Armour (not on a "
                                           "Bike) may be upgraded.", groups=[any_of(*bad)])] + hide,
            infolinks=rules_links(rl, key=eid))])
        for p in u.findall("profiles/profile"):
            if p.get("typeName") == "Unit":
                _t_mod(p, eid, uid_)
        done.append(u.get("name"))
    return done


def footslogging_error(ctx):
    ids = [uid("unit", n) for n in FOOTSLOG]
    groups = [cond(i, "roster", "atLeast", 2) for i in ids]
    pairs = []
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            pairs.append(all_of(cond(ids[a], "roster", "atLeast", 1), cond(ids[b], "roster", "atLeast", 1)))
    grp = el("conditionGroup", {"type": "or"}, [wrap("conditions", groups), wrap("conditionGroups", pairs)])
    add_mods(ctx.unit("Legion"), [modifier("add", "error", "Footslogging Killers: a Death Guard army may take only 0-1 "
                                                           "selection in total from Land Speeder Squadrons, Attack Bike "
                                                           "Squadrons and Bike Squadrons.", groups=[grp])])


def silent_retinue(ctx):
    """Praetor / Centurion: a Deathshroud Terminator Squad as retinue (any armour, author's answer)."""
    ds = ds_retinue()
    for name in ["Legion Praetor", "Legion Centurion"]:
        for g in ctx.unit(name).iter("selectionEntryGroup"):
            if g.get("name") == "Retinue (no Force Organisation slot)":
                lid = uid("link", g.get("id"), "dg-deathshroud")
                add_to(g, "entryLinks", [link(lid, ds.get("id"), ds.get("name"))])
    if ds not in RETINUE_SHARED:
        RETINUE_SHARED.append(ds)


def reaping_troops(ctx):
    on = [rite("The Reaping")]
    for n, normal in [("Legion Veteran Squad", ELITES), ("Legion Heavy Support Squad", HS)]:
        add_mods(ctx.unit(n), [modifier("set-primary", "category", TROOPS, conds=on),
                               modifier("remove", "category", normal, conds=on),
                               modifier("remove", "category", gs.CAT_LINE, conds=on)])


# ------------------------------------------------------------------ extend
def extend(ctx):
    ctx.legion_rules([LR, "Steady Assault", "True Grit", "Move Through Cover", "Resilience of Barbarus",
                      "Footslogging Killers", "Manreaper", "Alchem Flamer"])
    footslogging_error(ctx)

    ctx.add_units(deathshroud(), grave_wardens(), mortus_poisoners(), *characters(), mortarion(), daemon_mortarion())
    silent_retinue(ctx)
    ctx.finish()  # new retinues become shared entries before the Legion-wide changes below

    # Armoury
    add_manreaper(ctx)
    add_alchem(ctx)

    # Rites of War
    reaping_troops(ctx)
    deep = [L.TRANSPORTS["Legion Drop Pod"], L.TRANSPORTS["Anvillus Pattern Dreadclaw Drop Pod"],
            L2.T["Legion Dreadnought Drop Pod"]]
    ctx.add_rite("The Reaping", RULES["The Reaping"], errors=[
        ("units may not deploy using Deep Strike, and units required to Deep Strike (Drop Pods, Dreadclaws) may not be "
         "selected.", [any_of(*[cond(i, "force", "atLeast", 1) for i in deep])])])
    ctx.add_rite("Creeping Death", RULES["Creeping Death"], errors=[
        ("only a Traitor Death Guard Detachment may use this Rite.", [cond(LOYALIST, "roster", "atLeast", 1)]),
        ("the Detachment must include a Legion Heavy Support Squad whose Sergeant is a Siege Breaker.",
         [cond(L2.SIEGE_BREAKER, "force", "lessThan", 1)]),
        ("the Detachment may not include a Fortification.", [cond(gs.cat("Fortification"), "force", "atLeast", 1)]),
    ])
    add_dark_arsenal(ctx)
    add_plague_marines(ctx)
