"""XVIII Legion - Salamanders (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, allegiance_only, option, upgrade, retinue_links, command_squad_for,
                            named_character, primarch, primarch_retinue, add_group, add_entry, LOW, TRAITOR, LOYALIST)
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group, \
    info_link, costs
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile, has_tda, no_tda, rule_ref
from legiones2 import (slot, take, pool, transports, add_mods, add_to, foc, rite_id, rite, TROOPS, ELITES, FA, HQ, HS,
                       model_swaps, model_takes, pa_armoury, tda_armoury, walker_profile, SGT_CCW, _negate)
from legiones_wargear import (ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR, ARMOURY, TDA_SGT,
                              NOT_WITH_TDA)

LEGION = "XVIII - Salamanders"
LR = "Legiones Astartes (Salamanders)"

COVENANT = "The Covenant of Fire"
AWAKENING = "The Awakening Fire"

RULES = {
    LR: ("Models with this rule belong to the XVIII Legion and use the Salamanders Legion special rules: Promethean Cult, "
         "Sturdy and Never Give Up."),
    "Promethean Cult": (
        "Salamanders models may re-roll To Hit rolls of 1 when attacking with Thunder Hammers, Melta Bombs, Meltaguns, "
        "Multi-Meltas and other weapons with the Melta special rule. In addition, Salamanders models may re-roll To Wound "
        "rolls of 1 when firing Flame weapons."),
    "Sturdy": (
        "All Salamanders models with an Initiative characteristic, except Dreadnoughts, suffer -1 Initiative. This "
        "modifier applies after all other profile modifications (it is NOT already included in the printed profiles). "
        "Salamanders units also subtract 1\" from their Fall Back distance, to a minimum of 1\". The Initiative penalty "
        "applies normally when resolving Pursuit."),
    "Never Give Up": (
        "At the end of the final scheduled game turn, the Salamanders player may choose to play one additional complete "
        "game turn; both players take one additional turn. After this additional game turn the battle ends automatically. "
        "May only be used once per battle and does not extend a mission which has already ended because a specific "
        "objective or action was completed."),
    # Armoury
    "Salamanders Armoury": (
        "SALAMANDERS MANTLE (35): one Salamanders Independent Character in the army may purchase one; only one per army "
        "(a named Character whose entry includes one prevents any other model from purchasing one). "
        "ARTIFICER WEAPONS: Salamanders models purchase the Master-crafted Weapon upgrade for +10 points instead of +15 "
        "(normal restrictions apply). ARTIFICER ARMOUR: a Salamanders non-Independent Character with access to the Space "
        "Marine Armoury may purchase Artificer Armour for +15 points even if his unit entry would not normally allow it; "
        "if his own unit entry offers it for less, use that cost. FIRE-BASED WARFARE: Flamers and Heavy Flamers used by "
        "Salamanders models gain +1 Strength (Dragon's Breath flamers; already included in the profiles). Where a Legion "
        "Tactical Squad or Legion Veteran Squad may purchase a Flamer it may instead purchase a Heavy Flamer for +10 "
        "points; Legion Heavy Support Squads may select Heavy Flamers as a Heavy Weapon option for +10 points per model. "
        "INFERNO PISTOL (15): any Salamanders Independent Character or squad Sergeant with access to the Space Marine "
        "Armoury. REINFORCED CERAMITE: any Salamanders Vehicle or Dreadnought which may normally purchase Armoured Ceramite "
        "may purchase it for +10 points instead (Land Raiders and Spartans pay their normal cost). PROSCRIBED MUNITIONS: "
        "a Salamanders Detachment may not select Phosphex weapons or Phosphex ammunition unless a specific unit or "
        "Character entry explicitly states otherwise."),
    "Salamanders Mantle": (
        "If an unsaved Wound would become a Massive Wound solely because the attack's Strength is at least double the "
        "bearer's Toughness, it instead inflicts only one Wound. No protection against weapons or special rules which "
        "explicitly inflict Massive Wounds by another method. Only one Salamanders Mantle per army; a named Character "
        "whose entry includes one prevents another model from purchasing one."),
    "Proscribed Munitions": ("A Salamanders Detachment may not select Phosphex weapons or Phosphex ammunition unless a "
                             "specific unit or Character entry explicitly states otherwise."),
    # Rites of War
    COVENANT: (
        "EFFECTS - Disciples of the Flame: Pyroclast Squads and Salamanders Infernus Destroyer Squads may be selected as "
        "non-compulsory Troops choices (they may not fulfil compulsory Troops selections). Walk Through Fire: Salamanders "
        "Infantry units gain Move Through Cover. Veneration of Wrath: when a Salamanders model makes an Armour Penetration "
        "roll with a Melta weapon (or Melta Bombs), one individual Armour Penetration die which rolls a natural 1 may be "
        "re-rolled; the second result stands. Obsidian Forged: each time a Salamanders Vehicle or Dreadnought suffers a "
        "Glancing or Penetrating Hit from a Flame, Melta, Plasma or Volkite weapon (or Melta Bombs), roll a D6; on a 5+ "
        "the hit is ignored (roll before the Vehicle Damage table).\n"
        "LIMITATIONS - Units in the Detachment may not deploy using Deep Strike; units which must deploy using Deep Strike "
        "may not be selected. The combined number of Fast Attack and Heavy Support choices may not exceed the number of "
        "Troops choices in the Detachment. The Detachment may not include a Fortification."),
    AWAKENING: (
        "EFFECTS - Devils from the Dark: Salamanders Infantry units gain Fear. Unto the Fires: Never Give Up functions "
        "normally; during the additional game turn generated by Never Give Up all Salamanders Infantry units gain "
        "Fearless. Fury of the Salamander: Salamanders Librarians in the Detachment may select Fury of the Salamander as a "
        "Pyromancy psychic power.\n"
        "LIMITATIONS - The Detachment must include a Legion Chaplain Consul. The Detachment may include no more than one "
        "unit of each of the following types: Jump Infantry, Jetbike, Skimmer and Flyer. The Detachment may not include "
        "Vulkan. The Detachment may not include a Fortification or an Allied Detachment."),
    "Fury of the Salamander": (
        "Psychic Witchfire power (18\", S5, AP1, Beam, Assault 1, Elemental Horror). Salamanders Librarians in a "
        "Detachment using The Awakening Fire may select it as a Pyromancy power; Xiaphas Jurr always knows it."),
    "Elemental Horror": (
        "If an enemy unit suffers one or more unsaved Wounds from Fury of the Salamander, it must immediately take a Morale "
        "test regardless of how many casualties were caused, with a Leadership penalty equal to the number of unsaved "
        "Wounds caused by Fury of the Salamander."),
    # Units
    "Firedrake Retinue": (
        "A Firedrake Terminator Squad may be selected as the retinue of a Salamanders Praetor wearing Terminator Armour, "
        "Artellus Numeon or another Character whose rules specifically permit it. The squad does not occupy a separate "
        "Elites selection."),
    "Pyroclast Flame Projector": (
        "Each time it is fired choose: fire it as a Salamanders Heavy Flamer, or fire it as a Meltagun. The selected weapon "
        "uses all of its normal rules, and for Promethean Cult and Fire-based Warfare it counts as the weapon whose profile "
        "it is using."),
    "Guided by Prophecy": (
        "At the beginning of an Assault phase the squad may take a Leadership test using Leadership 7 regardless of the "
        "Leadership of any model in the unit. If passed, until the end of that Assault phase the squad has Weapon Skill 5 "
        "and Feel No Pain (6+). If failed there is no effect."),
    "Close-Quarters Arsenal": ("A Sanctifier equipped with two Pistol weapons has the Dual Pistols special rule. Both "
                               "Pistols must fire at the same target."),
    "Infernus Jump Packs": ("If every model is equipped with a Jump Pack, the unit becomes Jump Infantry and may not "
                            "select a Dedicated Transport."),
    "Destroyer Cadre (Infernus)": (
        "An Infernus Destroyer Squad may only be joined by a Legion Moritat or another Character specifically stated to be "
        "permitted to join Destroyer units."),
    # Named characters
    "Captain of the Pyre Guard": (
        "Numeon may select one Firedrake Terminator Squad as his personal retinue. One Firedrake in that unit may be "
        "upgraded to a Firedrake Master at no additional points cost. The squad does not occupy a separate Elites "
        "selection. Command Retinue: instead of a Firedrake Terminator Squad, Numeon may select a Legion Command Squad or "
        "Legion Terminator Command Squad."),
    "Vulkan's Heir": "Numeon and any Salamanders unit he has joined may re-roll failed Morale tests.",
    "Lord Chaplain": ("Nomus Rhy'tan counts as a Legion Chaplain Consul for all rules, army construction requirements and "
                      "Rites of War."),
    "Keeper of the Keys": (
        "One Legion Dreadnought or Legion Contemptor Dreadnought may be selected as a non-compulsory HQ choice. It may not "
        "fulfil the army's compulsory HQ selection and may not be the Warlord."),
    "Command Retinue (Nomus Rhy'tan)": ("Nomus may select a Legion Command Squad, Legion Terminator Command Squad or "
                                        "Firedrake Terminator Squad as his retinue."),
    "Darkstar Falling": (
        "A Two-Handed, Master-crafted Power Weapon. Attacks made with it are resolved at +2 Strength and have the "
        "Concussive special rule. Against Vehicles, attacks made with Darkstar Falling have Armourbane."),
    "Ignatus": ("A Master-crafted Power Weapon. During an Assault phase in which Jurr charges, attacks made with Ignatus "
                "are resolved at +1 Strength."),
    "Chaplain-Lieutenant": "Jurr counts as a Legion Chaplain Consul for army construction requirements and Rites of War.",
    "Prophet of Fire": ("Jurr is a Psyker (Mastery Level 1). He knows Fury of the Salamander. When Jurr takes a Psychic "
                        "test, he uses Leadership 7 instead of his normal Leadership characteristic."),
    "Dreadfire Cannon": "The Dreadfire Cannon counts as a Twin-linked Salamanders Heavy Flamer.",
    "Automatic Shielding": ("Whenever Cassian suffers a Glancing or Penetrating Hit from a shooting attack, roll a D6. On a "
                            "5+, the hit is ignored."),
    "Venerable Ancient": (
        "Whenever Cassian suffers a Glancing or Penetrating Hit which is not ignored by Automatic Shielding, the "
        "Salamanders player may force the opponent to re-roll the resulting Vehicle Damage roll. The second result must be "
        "accepted."),
    "Reinforced Ceramite (Cassian)": ("Cassian uses the normal Reinforced Ceramite rules (he is equipped with Armoured "
                                      "Ceramite)."),
    "The Last Warlord": (
        "Cassian may be the army's Warlord despite being a Vehicle. If Cassian is the Warlord, friendly Salamanders "
        "Infantry units with at least one model within 6\" of him gain Feel No Pain (6+)."),
    "Burning Wrath": ("Cassian may give up one of his Attacks during an Assault phase. If he does so, every enemy model in "
                      "base contact with him suffers one automatic Strength 6 AP4 hit. (Lost by Cassian Dracos Reborn.)"),
    "Cassian Dracos Reborn": (
        "Cassian Dracos may instead be fielded as Cassian Dracos Reborn for +25 points: replace the Dreadfire Cannon with a "
        "second Dreadnought Close Combat Weapon with built-in Pyroclast Flame Projector; Attacks become 4; gains It Will "
        "Not Die and Voice of the Machine; loses Burning Wrath. A built-in Pyroclast Flame Projector follows the normal "
        "Pyroclast Flame Projector rule."),
    "Voice of the Machine": (
        "Friendly Battle-Automata with at least one model within 6\" of Cassian Dracos Reborn may use Leadership 10 for "
        "Morale and Pinning tests. During the Shooting phase, Cassian may forgo shooting to make a Battlesmith attempt "
        "against one friendly Vehicle or Battle-Automata model within 6\". The attempt succeeds on a 4+."),
    "Master Artificer": (
        "After both armies have been selected but before deployment, choose one friendly Salamanders Character. One weapon "
        "carried by that Character becomes Master-crafted for the duration of the battle. Alternatively, one friendly "
        "Salamanders Vehicle or Dreadnought may receive Extra Armour at no additional points cost."),
    "Keeper of the Forge": (
        "One Salamanders Vehicle or Dreadnought eligible to purchase Reinforced Ceramite may receive that upgrade at no "
        "points cost. This may not be applied to a Land Raider or Spartan."),
    "Forgefather (T'Kell)": ("T'Kell receives +2 rather than +1 to Battlesmith attempts for his Servo-Arm. A Battlesmith "
                             "attempt may still never be improved beyond 3+."),
    # Vulkan
    "Dawnbringer": (
        "A Master-crafted, Two-Handed Power Weapon. Attacks are resolved at Strength 10 and have Armourbane and Concussive. "
        "Any unsaved Wound inflicted against a model without the Primarch special rule becomes a Massive Wound and "
        "inflicts D3 Wounds instead of one."),
    "The Forgefather": ("All ranged and close-combat weapons carried by Vulkan count as Master-crafted (already included "
                        "in the profiles where relevant)."),
    "Lord of Drakes": ("Vulkan may re-roll failed Armour and Invulnerable Saves made against attacks from Flame or Melta "
                       "weapons. The second result must be accepted."),
    "Sire of the Salamanders": (
        "Friendly Salamanders units with at least one model within 12\" of Vulkan may re-roll failed Morale tests. Such "
        "units may also re-roll Armour Save rolls of 1 made against attacks from Flame weapons (the second result stands)."),
    "Perpetual": (
        "The first time Vulkan is reduced to 0 Wounds, roll a D6 before removing him. On 4+ he is not removed: roll a D3 "
        "and restore him to that many Wounds; he stays exactly where he was (and remains engaged if in combat). On 1-3 he "
        "is removed normally. Once per battle. If it succeeds he is not considered slain for Victory Points, Warlord "
        "objectives or Price of Failure; those rewards are only awarded if Vulkan is ultimately removed as a casualty."),
    "Primarch Retinue (Vulkan)": (
        "Vulkan may select one Legion Honour Guard Squad, Legion Terminator Command Squad or Firedrake Terminator Squad as "
        "his Primarch Retinue. It does not occupy an additional Force Organisation selection and otherwise follows the "
        "normal Primarch Retinue rules."),
    "Vulkan Restrictions": "Vulkan may only be selected for a Loyalist Salamanders army.",
    "Selected as HQ (Keeper of the Keys)": (
        "With Nomus Rhy'tan in the army, this Dreadnought is a non-compulsory HQ choice. It may not fulfil the compulsory "
        "HQ selection and may not be the Warlord."),
}

WEAPONS_ = {
    "Inferno Pistol": ('6"', "8", "1", "Pistol, Melta"),
    "Master-crafted Thunder Hammer": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Concussive, "
                                                      "Master-crafted"),
    "Darkstar Falling": ("-", "User +2", "-", "Power Weapon, Two-Handed, Master-crafted, Concussive, Armourbane "
                                              "(vs Vehicles)"),
    "Ignatus": ("-", "User (+1 when charging)", "-", "Power Weapon, Master-crafted"),
    "Dreadfire Cannon": ("Template", "6", "4", "Assault 1, Twin-linked"),
    "Dawnbringer": ("-", "10", "-", "Power Weapon, Two-Handed, Master-crafted, Armourbane, Concussive, D3 Massive "
                                    "Wounds (non-Primarch)"),
    "Furnace's Heart": ('18"', "6", "2", "Assault 1, Rending, Master-crafted"),
    "Gauntlet of the Forge": ("Template", "6", "4", "Assault 1, Flame"),
    "Fury of the Salamander": ('18"', "5", "1", "Witchfire - Beam, Assault 1, Elemental Horror"),
}
MULTI = {
    "Pyroclast Flame Projector": {
        "Pyroclast Flame Projector - Heavy Flamer": ("Template", "6", "4", "Assault 1"),
        "Pyroclast Flame Projector - Meltagun": ('12"', "8", "1", "Assault 1, Melta")},
}
WEAPON_RULES_ = {
    "Inferno Pistol": ["Melta"],
    "Master-crafted Thunder Hammer": ["Unwieldy", "Concussive", "Master-Crafted"],
    "Darkstar Falling": ["Darkstar Falling", "Two-Handed", "Master-Crafted", "Concussive", "Armourbane"],
    "Ignatus": ["Ignatus", "Master-Crafted"],
    "Dreadfire Cannon": ["Dreadfire Cannon", "Twin-Linked"],
    "Dawnbringer": ["Dawnbringer", "Two-Handed", "Master-Crafted", "Armourbane", "Concussive"],
    "Furnace's Heart": ["Rending", "Master-Crafted"],
    "Fury of the Salamander": ["Fury of the Salamander", "Elemental Horror"],
    "Pyroclast Flame Projector": ["Pyroclast Flame Projector", "Melta"],
}
WARGEAR_ = {
    "Salamanders Mantle": RULES["Salamanders Mantle"],
    "Mantle of the Elder Drake": "Counts as a Salamanders Mantle. " + RULES["Salamanders Mantle"],
    "Dragonscale Storm Shield": (
        "The bearer has a 4+ Invulnerable Save in close combat and against shooting attacks made with Flame or Melta "
        "weapons. Against all other shooting attacks the shield provides a 5+ Invulnerable Save."),
    "The Burning Halo": (
        "Grants a 4+ Invulnerable Save. Each time Jurr successfully passes this save against a close-combat attack of "
        "Strength 5 or greater, the attacking model suffers one Strength 4 hit."),
    "Iron Halo (Named Character)": (
        "Grants a 4+ Invulnerable Save. Part of this named character's own wargear; not counted towards the army's normal "
        "limit of one Iron Halo."),
    "Draken Scale": ("Counts as Primarch Armour.", ["Primarch Armour"]),
    "Kesare's Mantle": ("When resolving an attack made with a Flame weapon against Vulkan, reduce the Strength of that "
                        "attack by 1, to a minimum of Strength 1."),
}
# Fire-based Warfare: +1 Strength to Flamers and Heavy Flamers used by Salamanders models
DRAGONS_BREATH = {
    "Flamer": ("Template", "5", "5", "Assault 1"),
    "Heavy Flamer": ("Template", "6", "4", "Assault 1"),
    "Twin-linked Flamer": ("Template", "5", "5", "Assault 1, Twin-linked"),
    "Twin-linked Heavy Flamer": ("Template", "6", "4", "Assault 1, Twin-linked"),
}
PHOSPHEX = ["Phosphex Bomb", "Phosphex Discharger", "Phosphex Canister Shot"]


def _patch_armoury():
    """Artificer Weapons (Master-crafted +10), Artificer Armour (+15 for non-IC characters), Inferno Pistol."""
    import legiones as Lm
    for lst in (ARMOURY, Lm.PA_SGT_WEAPONS, Lm.PA_SGT_WARGEAR):
        for i, r in enumerate(lst):
            if r[0] == "Master-crafted Weapon":
                lst[i] = (r[0], 10) + tuple(r[2:])
            if r[0] == "Artificer Armour":
                lst[i] = (r[0], 15) + tuple(r[2:])
    TDA_SGT["Master-crafted Weapon"] = 10
    row = ("Inferno Pistol", 15, 1, 1, 1, "weapon", "")
    # insert next to the Plasma Pistol
    idx = next(i for i, r in enumerate(ARMOURY) if r[0] == "Plasma Pistol") + 1
    ARMOURY.insert(idx, row)
    idx = next(i for i, r in enumerate(Lm.PA_SGT_WEAPONS) if r[0] == "Plasma Pistol") + 1
    Lm.PA_SGT_WEAPONS.insert(idx, row)
    NOT_WITH_TDA.add("Inferno Pistol")


def register():
    ARMY_RULES.update(RULES)
    register_data(weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_, multi_profile=MULTI)
    WEAPON_PROFILES.update(DRAGONS_BREATH)
    # aliases built from existing profiles
    WEAPONS["Two Hand Flamers"] = ["Hand Flamer"]
    WEAPONS["Two Volkite Serpentae"] = ["Volkite Serpenta"]
    WEAPON_RULES["Two Volkite Serpentae"] = ["Rending"]
    WEAPONS["Second Bolt Pistol"] = ["Bolt Pistol"]
    WEAPONS["Multi-Melta with Suspensor Web"] = ["Multi-Melta"]
    WEAPON_RULES["Multi-Melta with Suspensor Web"] = ["Melta", "Suspensor Web"]
    WEAPONS["Dreadnought Close Combat Weapon with built-in Heavy Flamer"] = ["Dreadnought Close Combat Weapon",
                                                                            "Heavy Flamer"]
    WEAPONS["Dreadnought Close Combat Weapon with built-in Pyroclast Flame Projector"] = [
        "Dreadnought Close Combat Weapon", "Pyroclast Flame Projector - Heavy Flamer",
        "Pyroclast Flame Projector - Meltagun"]
    WEAPON_RULES["Dreadnought Close Combat Weapon with built-in Pyroclast Flame Projector"] = [
        "Pyroclast Flame Projector", "Melta"]
    _patch_armoury()


# ------------------------------------------------------------------ local helpers
def find_group(e, name):
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == name:
            return g
    return None


def find_entry(e, name):
    for x in e.iter("selectionEntry"):
        if x.get("name") == name:
            return x
    return None


def link_cost(lk):
    cs = lk.find("costs")
    if cs is None or not len(cs):
        return 0
    return float(cs[0].get("value"))


def set_link_cost(lk, value):
    cs = lk.find("costs")
    if cs is not None:
        lk.remove(cs)
    lk.append(costs(value))


def hide_unless(eid, conds_hide):
    return [modifier("set", "hidden", "true", groups=[any_of(*conds_hide)]),
            modifier("set", uid(eid, "max"), 0, groups=[any_of(*conds_hide)])]


def model(u, name, cost, mn, mx, utype, stats, kit, groups=(), rules_=(), prof_mods=()):
    mid = uid("model", u, name)
    prof = unit_profile(u, name, utype, *stats)
    if prof_mods:
        prof.insert(0, wrap("modifiers", list(prof_mods)))
    return mid, entry(mid, name, typ="model", cost=cost,
                      constraints=[constraint(uid(mid, "min"), "min", mn), constraint(uid(mid, "max"), "max", mx)],
                      profiles=[prof], links=[gear(mid, k) for k in kit],
                      groups=list(groups), infolinks=rules_links(list(rules_), key=mid))


def unit_type_mod(new_type, conds):
    return modifier("set", gs.char_id("Unit", "Unit Type"), new_type, conds=conds)


def squad_gear(u):
    return [per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
            per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])]


# ------------------------------------------------------------------ units
FIREDRAKES = uid("unit", "Firedrake Terminator Squad")
PYROCLASTS = uid("unit", "Pyroclast Squad")
INFERNUS = uid("unit", "Salamanders Infernus Destroyer Squad")
ADHERENTS = uid("unit", "Adherent Squad")
SANCTIFIERS = uid("unit", "Sanctifier Squad")


def firedrakes(key="Firedrake Terminator Squad", root=True):
    u = uid("unit", key)
    kit = ["Terminator Armour", "Dragonscale Storm Shield"]
    fid, drakes = model(u, "Firedrake", 45, 4, 9, "Infantry", (5, 4, 4, 4, 1, 4, 2, 9, "2+/5+"),
                        kit + ["Thunder Hammer"])
    mid = uid("model", u, "Firedrake Master")
    _, master = model(u, "Firedrake Master", 0, 1, 1, "Infantry (Character)", (5, 4, 4, 4, 1, 4, 3, 10, "2+/5+"), kit,
                      groups=[slot(mid, "Replace Thunder Hammer", "Thunder Hammer",
                                   [("Master-crafted Thunder Hammer", 10)]),
                              tda_armoury(mid)])
    shields, mx = pool(u, "Firedrakes: replace Dragonscale Storm Shield (up to two per five models)", u,
                       [("Heavy Flamer", 10), ("Multi-Melta", 20)], 0, every=5)
    add_mods(shields, [modifier("increment", mx, 1, repeats=[repeat("model", u, 5)])])
    return entry(u, "Firedrake Terminator Squad", typ="unit", cost=285 - 4 * 45,
                 cats=[foc(ELITES, "Elites", u)] if root else [],
                 constraints=[force_limit(u, 1)] if root else [],
                 infolinks=rules_links([LR, "Stubborn", "Implacable Advance", "Firedrake Retinue"] +
                                       ([] if root else ["Retinue"]), key=u),
                 entries=[master, drakes],
                 groups=[model_swaps(u, "Firedrakes: upgrade Thunder Hammer (any number)", u, [fid],
                                     [("Master-crafted Thunder Hammer", 10)]),
                         shields,
                         transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                                    orbital=False)])


def covenant_troops(u):
    on = [rite(COVENANT)]
    return [modifier("set-primary", "category", TROOPS, conds=on), modifier("remove", "category", ELITES, conds=on)]


def pyroclasts():
    u = PYROCLASTS
    kit = ["Artificer Armour", "Pyroclast Flame Projector", "Frag Grenades"]
    _, pyros = model(u, "Pyroclast", 30, 4, 9, "Infantry", (4, 4, 4, 4, 1, 4, 1, 9, "2+"),
                     kit + ["Bolt Pistol", "Close Combat Weapon"])
    wid = uid("model", u, "Pyroclast Warden")
    _, warden = model(u, "Pyroclast Warden", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 2, 10, "2+"), kit,
                      groups=[slot(wid, "Replace Close Combat Weapon", "Close Combat Weapon",
                                   [("Rending Weapon", 5), ("Power Weapon", 10), ("Power Fist", 15),
                                    ("Thunder Hammer", 20)]),
                              pa_armoury(wid, u, 10, slots=["Bolt Pistol"], skip=("Artificer Armour",))])
    return entry(u, "Pyroclast Squad", typ="unit", cost=190 - 4 * 30, cats=[foc(ELITES, "Elites", u)],
                 mods=covenant_troops(u),
                 infolinks=rules_links([LR, "Stubborn", "Pyroclast Flame Projector"], key=u),
                 entries=[warden, pyros, *squad_gear(u)],
                 groups=[transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos",
                                           "Land Raider Proteus"])])


def infernus():
    u = INFERNUS
    jp_id = uid("squadwide", u, "Jump Packs (entire squad)")
    jp_on = [has(jp_id, u)]
    kit = ["Hardened Power Armour", "Frag Grenades"]
    did, dests = model(u, "Infernus Destroyer", 25, 4, 9, "Infantry", (4, 4, 4, 4, 1, 4, 2, 9, "3+"),
                       kit + ["Two Hand Flamers", "Chainsword"], prof_mods=[unit_type_mod("Jump Infantry", jp_on)])
    sid = uid("model", u, "Infernus Sergeant")
    pistols = [("Volkite Serpenta", 5), ("Plasma Pistol", 15), ("Inferno Pistol", 10)]
    _, sgt = model(u, "Infernus Sergeant", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 3, 9, "3+"), kit,
                   prof_mods=[unit_type_mod("Jump Infantry (Character)", jp_on)],
                   groups=[slot(sid, "Replace Chainsword", "Chainsword", SGT_CCW),
                           slot(sid, "Replace first Hand Flamer", "Hand Flamer", pistols),
                           slot(sid, "Replace second Hand Flamer", "Hand Flamer", pistols),
                           pa_armoury(sid, u, 10)])
    heavy_opts = [("Heavy Flamer with Suspensor Web", 10), ("Multi-Melta with Suspensor Web", 15)]
    heavy, _ = pool(u, "Infernus Destroyers: replace one Hand Flamer with a heavy weapon (1 per 5 models)", u,
                    heavy_opts, 0, every=5)
    # each Destroyer has two Hand Flamers; heavy weapons use up one of them
    hands = model_swaps(u, "Infernus Destroyers: replace either Hand Flamer (any number, two per model)", u,
                        [did, did], [("Volkite Serpenta", 5), ("Plasma Pistol", 15)],
                        minus=[W(n) for n, _ in heavy_opts])
    jp = per_model(u, "Jump Packs (entire squad)", 15, u, ["Jump Pack"])
    add_to(jp, "infoLinks", rules_links(["Infernus Jump Packs"], key=jp_id))
    return entry(u, "Salamanders Infernus Destroyer Squad", typ="unit", cost=150 - 4 * 25,
                 cats=[foc(ELITES, "Elites", u)], mods=covenant_troops(u),
                 infolinks=rules_links([LR, "Counter-Attack", "Hardened Armour", "Dual Pistols (Destroyers)",
                                        "Destroyer Cadre (Infernus)"], key=u),
                 entries=[sgt, dests, *squad_gear(u), jp],
                 groups=[heavy, hands,
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos",
                                           "Land Raider Proteus"],
                                    block_if=jp_on)])


def adherents():
    u = ADHERENTS
    kit = ["Power Armour", "Combi-Flamer", "Frag Grenades"]
    _, adh = model(u, "Adherent", 22, 4, 9, "Infantry", (4, 4, 4, 4, 1, 4, 2, 8, "3+"),
                   kit + ["Bolt Pistol", "Chainsword"])
    sid = uid("model", u, "Adherent Sergeant")
    _, sgt = model(u, "Adherent Sergeant", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 2, 9, "3+"), kit,
                   groups=[slot(sid, "Replace Chainsword", "Chainsword",
                                [("Rending Weapon", 5), ("Power Weapon", 10), ("Power Fist", 15),
                                 ("Thunder Hammer", 20)]),
                           take(sid, "Sergeant Wargear", [("Artificer Armour", 10)]),
                           pa_armoury(sid, u, 10, slots=["Bolt Pistol"], skip=("Artificer Armour",))])
    hf, _ = pool(u, "Adherents: replace Combi-flamer with Heavy Flamer (1 per 5 models)", u, [("Heavy Flamer", 10)],
                 0, every=5)
    return entry(u, "Adherent Squad", typ="unit", cost=120 - 4 * 22, cats=[foc(TROOPS, "Troops", u)],
                 infolinks=rules_links([LR, "Support Squad", "Guided by Prophecy"], key=u),
                 entries=[sgt, adh, *squad_gear(u)],
                 groups=[hf, transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                               "Anvillus Pattern Dreadclaw Drop Pod"])])


def sanctifiers():
    u = SANCTIFIERS
    kit = ["Power Armour", "Frag Grenades"]
    mid, sanc = model(u, "Sanctifier", 25, 4, 9, "Infantry", (5, 4, 4, 4, 1, 4, 2, 9, "3+"),
                      kit + ["Bolter", "Bolt Pistol", "Chainsword"])
    sid = uid("model", u, "Sanctifier Sergeant")
    _, sgt = model(u, "Sanctifier Sergeant", 0, 1, 1, "Infantry (Character)", (5, 4, 4, 4, 1, 4, 3, 9, "3+"),
                   kit + ["Bolter", "Bolt Pistol"],
                   groups=[slot(sid, "Replace Chainsword", "Chainsword", SGT_CCW),
                           take(sid, "Sergeant Wargear", [("Artificer Armour", 10)])])
    ccw, _ = pool(u, "Sanctifiers: replace Chainsword (1 per 5 models)", u,
                  [("Rending Weapon", 5), ("Power Weapon", 10)], 0, every=5)
    bolter = model_swaps(u, "Sanctifiers: replace Bolter (any number; the paired pistols also replace the Bolt Pistol)",
                         u, [mid], [("Second Bolt Pistol", 0), ("Rotor Cannon", 10), ("Two Hand Flamers", 10),
                                    ("Two Volkite Serpentae", 10)])
    return entry(u, "Sanctifier Squad", typ="unit", cost=150 - 4 * 25, cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links([LR, "Stubborn", "Close-Quarters Arsenal"], key=u),
                 entries=[sgt, sanc, *squad_gear(u)],
                 groups=[bolter, ccw,
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos",
                                           "Land Raider Proteus"])])


# ------------------------------------------------------------------ characters
NUMEON = uid("unit", "Artellus Numeon")
NOMUS = uid("unit", "Lord Chaplain Nomus Rhy'tan")
JURR = uid("unit", "Xiaphas Jurr, Prophet of Fire")
CASSIAN = uid("unit", "Cassian Dracos")
TKELL = uid("unit", "Forgefather T'Kell")
VULKAN = uid("unit", "Vulkan, the Forgefather")


def grenades(u, melta=True):
    return take(u, "Wargear", [("Krak Grenades", 2)] + ([("Melta Bombs", 5)] if melta else []))


def characters():
    out = []
    out.append(named_character(
        LR, "Artellus Numeon", 190, (6, 5, 4, 4, 3, 5, 3, 10, "2+/4+"),
        ["Artificer Armour", "Iron Halo (Named Character)", "Master-crafted Thunder Hammer", "Bolt Pistol",
         "Frag Grenades", "Salamanders Mantle"],
        ["Captain of the Pyre Guard", "Vulkan's Heir", "Salamanders Mantle"],
        retinue=retinue_links("numeon", [firedrakes("numeon-firedrakes", root=False),
                                         command_squad_for("numeon", NUMEON),
                                         L2.terminator_command_squad("numeon")]),
        extra_groups=[grenades(NUMEON)]))
    out.append(named_character(
        LR, "Lord Chaplain Nomus Rhy'tan", 205, (6, 4, 4, 4, 3, 5, 3, 10, "2+/4+"),
        ["Artificer Armour", "Iron Halo (Named Character)", "Darkstar Falling", "Combi-Flamer", "Bolt Pistol",
         "Frag Grenades", "Mantle of the Elder Drake"],
        ["Zealot", "Lord Chaplain", "Keeper of the Keys", "Command Retinue (Nomus Rhy'tan)", "Salamanders Mantle"],
        retinue=retinue_links("nomus", [command_squad_for("nomus", NOMUS), L2.terminator_command_squad("nomus"),
                                        firedrakes("nomus-firedrakes", root=False)]),
        extra_groups=[grenades(NOMUS)], profile_name="Nomus Rhy'tan"))
    out.append(named_character(
        LR, "Xiaphas Jurr, Prophet of Fire", 150, (5, 5, 4, 4, 2, 5, 3, 10, "2+/4+"),
        ["Artificer Armour", "The Burning Halo", "Dragonscale Storm Shield", "Ignatus", "Bolt Pistol",
         "Frag Grenades", "Fury of the Salamander"],
        ["Stubborn", "Chaplain-Lieutenant", "Prophet of Fire", "Psyker", "Fury of the Salamander"], master=False,
        extra_groups=[grenades(JURR)], profile_name="Xiaphas Jurr"))
    out.append(named_character(
        LR, "Forgefather T'Kell", 155, (5, 5, 4, 4, 2, 5, 2, 10, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Master-crafted Thunder Hammer", "Bolt Pistol", "Servo-Arm", "Signum",
         "Frag Grenades"],
        ["Battlesmith", "Bolster Defences", "Master Artificer", "Keeper of the Forge", "Forgefather (T'Kell)"],
        master=False, extra_groups=[grenades(TKELL)], profile_name="T'Kell"))
    out.append(cassian())
    return out


def cassian():
    u = CASSIAN
    prof = walker_profile(u, "Cassian Dracos", 6, 5, 6, 13, 12, 10, 4, 3, ut="Vehicle (Walker, Character)")
    rid = uid(u, "reborn")
    on = [has(rid, u)]
    prof.insert(0, wrap("modifiers", [modifier("set", gs.char_id("Walker", "A"), 4, conds=on)]))
    cannon = entry(uid(u, "cannon"), "Dreadfire Cannon", links=[gear(uid(u, "cannon"), "Dreadfire Cannon")])
    reborn = entry(rid, "Cassian Dracos Reborn (replaces the Dreadfire Cannon)", cost=25,
                   links=[gear(rid, "Dreadnought Close Combat Weapon with built-in Pyroclast Flame Projector")],
                   infolinks=rules_links(["Cassian Dracos Reborn", "It Will Not Die", "Voice of the Machine"], key=rid))
    form = slot(u, "Form", None, [(reborn, None)], default_is_entry=cannon)
    tid, tname = rule_ref("Burning Wrath")
    wrath = info_link(tid, tname, "rule", key=u + "wrath", mods=[modifier("set", "hidden", "true", conds=on)])
    return entry(u, "Cassian Dracos", typ="unit", cost=225, cats=[foc(ELITES, "Elites", u)],
                 constraints=[unique(u)], profiles=[prof],
                 mods=[modifier("set", "name", "Cassian Dracos Reborn", conds=on)],
                 infolinks=rules_links(["Automatic Shielding", "Venerable Ancient", "Reinforced Ceramite (Cassian)",
                                        "The Last Warlord", "Dreadfire Cannon"], key=u) + [wrath],
                 links=[gear(u, k) for k in ["Dreadnought Close Combat Weapon with built-in Heavy Flamer",
                                             "Extra Armour", "Armoured Ceramite", "Smoke Launchers", "Searchlight",
                                             "Nuncio Vox"]],
                 groups=[form])


def vulkan():
    ret = primarch_retinue("vulkan", extra=[firedrakes("vulkan-firedrakes", root=False)])
    return primarch(LR, "Vulkan, the Forgefather", 520, (7, 6, 7, 7, 7, 5, 5, 10, "1+"),
                    ["Draken Scale", "Kesare's Mantle", "Dawnbringer", "Furnace's Heart", "Gauntlet of the Forge",
                     "Frag Grenades"],
                    ["Primarch Armour", "The Forgefather", "Lord of Drakes", "Sire of the Salamanders", "Perpetual",
                     "Primarch Retinue (Vulkan)", "Vulkan Restrictions"],
                    retinue=ret, loyalist=True, profile_name="Vulkan")


# ------------------------------------------------------------------ Legion-wide changes
def legion_armoury(ctx):
    roots = ctx.all_entries()
    seen = set()
    # Fire-based Warfare: Heavy Flamer instead of a Flamer for Tactical / Veteran Squads
    tac = ctx.unit("Legion Tactical Squad")
    g = find_group(tac, "Special Weapons (1, 2 at 20 models)")
    g.find("entryLinks").append(link(uid("link", g.get("id"), "sal", "Heavy Flamer"), W("Heavy Flamer"),
                                     "Heavy Flamer (Fire-based Warfare)", cost=10))
    vet = ctx.unit("Legion Veteran Squad")
    g = find_group(vet, "Specialist Weapons (1 per 5 models)")
    g.find("entryLinks").append(link(uid("link", g.get("id"), "sal", "Heavy Flamer"), W("Heavy Flamer"),
                                     "Heavy Flamer (Fire-based Warfare)", cost=10))
    hs = ctx.unit("Legion Heavy Support Squad")
    g = find_group(hs, "Heavy Weapons (up to four models)")
    g.find("entryLinks").insert(0, link(uid("link", g.get("id"), "sal", "Heavy Flamer"), W("Heavy Flamer"),
                                        "Heavy Flamer", cost=10))

    targets = {W("Master-crafted Weapon"): (15, 10)}
    ceramite = W("Armoured Ceramite")
    phos = {W(n) for n in PHOSPHEX}
    for r in roots:
        if id(r) in seen:
            continue
        seen.add(id(r))
        rname = r.get("name") or ""
        lr_or_spartan = "Land Raider" in rname or "Spartan" in rname
        for lk in r.iter("entryLink"):
            t = lk.get("targetId")
            # Artificer Weapons
            if t in targets and link_cost(lk) == targets[t][0]:
                set_link_cost(lk, targets[t][1])
            # Reinforced Ceramite
            if t == ceramite and link_cost(lk) == 20 and not lr_or_spartan:
                set_link_cost(lk, 10)
                lk.set("name", "Armoured Ceramite (Reinforced Ceramite)")
            # Proscribed Munitions
            if t in phos:
                lk.set("hidden", "true")
                add_to(lk, "constraints", [constraint(uid(lk.get("id"), "sal-phosphex"), "max", 0)])
        for e in r.iter("selectionEntry"):
            if "Phosphex" in (e.get("name") or "") and e is not r:
                e.set("hidden", "true")
                add_to(e, "constraints", [constraint(uid(e.get("id"), "sal-phosphex"), "max", 0)])

    # Inferno Pistol for sergeants whose Armoury block has no pistol slot (only extra wargear)
    done = set()
    for r in roots:
        for g in r.iter("selectionEntryGroup"):
            if g.get("name") != "Space Marine Armoury (max 50 pts)" or id(g) in done:
                continue
            done.add(id(g))
            subs = g.find("selectionEntryGroups")
            if subs is None or not len(subs):
                continue  # Terminator column - no pistols
            if any((s.get("name") or "").startswith("Replace ") for s in subs):
                continue  # already offers the Inferno Pistol through the Armoury weapon slots
            extra = [s for s in subs if s.get("name") == "Additional Wargear"]
            if not extra:
                continue
            links = extra[0].find("entryLinks")
            lid = uid("link", extra[0].get("id"), "sal", "Inferno Pistol")
            links.append(link(lid, W("Inferno Pistol"), "Inferno Pistol", cost=15,
                              constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))

    # Salamanders Mantle for a Praetor / Centurion (counts towards the Armoury cap)
    add_armoury_items(ctx, [("Salamanders Mantle", 35)], who=("praetor", "centurion"))
    legion = ctx.unit("Legion")
    mantle = W("Salamanders Mantle")
    add_mods(legion, [
        modifier("add", "error", "Only one Salamanders Mantle may be included in the army (Artellus Numeon's own "
                                 "Mantle counts).", conds=[cond(mantle, "roster", "greaterThan", 1)]),
        modifier("add", "error", "Only one Salamanders Mantle may be included in the army (Nomus Rhy'tan's Mantle of "
                                 "the Elder Drake counts as one).",
                 conds=[cond(W("Mantle of the Elder Drake"), "roster", "atLeast", 1), cond(mantle, "roster", "atLeast", 1)]),
    ])


def firedrake_praetor_retinue(ctx):
    pr = ctx.unit("Legion Praetor")
    pid = pr.get("id")
    fd = firedrakes("praetor-firedrakes", root=False)
    L2.RETINUE_SHARED.append(fd)
    g = find_group(pr, "Retinue (no Force Organisation slot)")
    g.find("entryLinks").append(link(uid("link", g.get("id"), fd.get("id")), fd.get("id"), fd.get("name"),
                                     mods=[modifier("set", "hidden", "true", groups=[no_tda(pid)])]))
    add_mods(pr, [modifier("add", "error", "A Firedrake Terminator Squad retinue requires the Praetor to wear "
                                           "Terminator Armour.",
                           groups=[all_of(cond(fd.get("id"), pid, "atLeast", 1), *[lacks(W(n), pid) for n in L.TDA])])])


def keeper_of_the_keys(ctx):
    tid = uid("sal", "keeper-of-the-keys")
    fmax = uid(tid, "force")
    no_nomus = [cond(NOMUS, "force", "lessThan", 1)]
    tog = entry(tid, "Selected as HQ (Keeper of the Keys)",
                mods=[modifier("set", "hidden", "true", conds=no_nomus), modifier("set", fmax, 0, conds=no_nomus)],
                constraints=[constraint(fmax, "max", 1, scope="force", deep=True)],
                infolinks=rules_links(["Selected as HQ (Keeper of the Keys)"], key=tid))
    ctx.add_shared(tog)
    for n in ("Legion Dreadnought", "Legion Contemptor Dreadnought"):
        d = ctx.unit(n)
        lid = uid("link", d.get("id"), "sal-keeper")
        add_to(d, "entryLinks", [link(lid, tid, tog.get("name"),
                                      constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])])
        on = [cond(tid, "self", "atLeast", 1)]
        add_mods(d, [modifier("set-primary", "category", HQ, conds=on), modifier("remove", "category", ELITES, conds=on),
                     modifier("remove", "category", TROOPS, conds=on),
                     modifier("remove", "category", gs.CAT_LINE, conds=on)])


def fury_for_librarians(ctx):
    cen = ctx.unit("Legion Centurion")
    lib = L.consul_id("Librarian")
    for e in cen.iter("selectionEntry"):
        if e.get("id") == lib:
            fid = uid("sal", "fury-librarian")
            hide = [cond(rite_id(AWAKENING), "force", "lessThan", 1)]
            add_to(e, "selectionEntries", [entry(
                fid, "Fury of the Salamander (Pyromancy, The Awakening Fire)", mods=hide_unless(fid, hide),
                constraints=[constraint(uid(fid, "max"), "max", 1, auto=True)],
                links=[gear(fid, "Fury of the Salamander")])])


def rites(ctx):
    rites_e = ctx.unit("Rite of War")
    cov = ctx.add_rite(COVENANT, RULES[COVENANT])
    deep = [L.TRANSPORTS["Legion Drop Pod"], L.TRANSPORTS["Anvillus Pattern Dreadclaw Drop Pod"],
            L2.T["Legion Dreadnought Drop Pod"]]
    fort = gs.cat("Fortification")
    add_mods(rites_e, [
        modifier("add", "error", f"{COVENANT}: units which must deploy using Deep Strike (Drop Pods, Dreadclaws) may not "
                                 "be selected.", conds=[cond(cov, "self", "atLeast", 1)],
                 groups=[any_of(*[cond(d, "force", "atLeast", 1) for d in deep])]),
        modifier("add", "error", f"{COVENANT}: the Detachment may not include a Fortification.",
                 conds=[cond(cov, "self", "atLeast", 1), cond(fort, "force", "atLeast", 1)]),
    ])
    # combined Fast Attack + Heavy Support choices may not exceed the number of Troops choices
    limit = []
    for t in range(0, 16):
        over = el("conditionGroup", {"type": "or"}, [
            wrap("conditions", [cond(FA, "force", "greaterThan", t)]),
            wrap("conditionGroups", [all_of(cond(FA, "force", "equalTo", f), cond(HS, "force", "greaterThan", t - f))
                                     for f in range(0, t + 1)])])
        limit.append(modifier("add", "error", f"{COVENANT}: the combined number of Fast Attack and Heavy Support "
                                              "choices may not exceed the number of Troops choices.",
                              conds=[cond(cov, "self", "atLeast", 1), cond(TROOPS, "force", "equalTo", t)],
                              groups=[over]))
    add_mods(rites_e, limit)
    aw = ctx.add_rite(AWAKENING, RULES[AWAKENING])
    chaplains = [L.consul_id("Chaplain"), NOMUS, JURR]
    add_mods(rites_e, [
        modifier("add", "error", f"{AWAKENING}: the Detachment must include a Legion Chaplain Consul (Nomus Rhy'tan or "
                                 "Xiaphas Jurr count as one).",
                 conds=[cond(aw, "self", "atLeast", 1)] + [cond(c, "force", "lessThan", 1) for c in chaplains]),
        modifier("add", "error", f"{AWAKENING}: the Detachment may not include Vulkan.",
                 conds=[cond(aw, "self", "atLeast", 1), cond(VULKAN, "force", "atLeast", 1)]),
        modifier("add", "error", f"{AWAKENING}: the Detachment may not include a Fortification.",
                 conds=[cond(aw, "self", "atLeast", 1), cond(fort, "force", "atLeast", 1)]),
    ])


# ------------------------------------------------------------------ extend
def extend(ctx):
    ctx.legion_rules([LR, "Promethean Cult", "Sturdy", "Never Give Up", "Salamanders Armoury", "Proscribed Munitions"])

    # Legion-wide changes on the standard army list (before the new units are added)
    legion_armoury(ctx)
    firedrake_praetor_retinue(ctx)
    keeper_of_the_keys(ctx)
    fury_for_librarians(ctx)

    ctx.add_units(firedrakes(), pyroclasts(), infernus(), adherents(), sanctifiers(), *characters(), vulkan())
    ctx.finish()
    rites(ctx)
