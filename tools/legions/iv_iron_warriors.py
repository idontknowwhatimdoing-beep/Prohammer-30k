"""IV Legion - Iron Warriors (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, allegiance_only, option, upgrade, clone, retinue_links,
                            command_squad_for, named_character, primarch, primarch_retinue, required_choice,
                            add_group, add_entry, legion_units, LOW)
from bsx import PTS, uid, el, wrap, info_link, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, rule_ref, per_model, rules_links, unit_profile
from legiones2 import (slot, take, pool, transports, add_mods, add_to, foc, rite_id, rite, TROOPS, ELITES, FA, HQ,
                       HS, model_swaps, pa_armoury, _negate)
from legiones_wargear import ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR

LEGION = "IV - Iron Warriors"
LR = "Legiones Astartes (Iron Warriors)"

RULES = {
    LR: ("Models with this rule belong to the IV Legion and use the Iron Warriors Legion special rules: Siege Masters, "
         "An Army of Steel and Wrath, Stubborn Resolve and Preliminary Bombardment."),
    "Siege Masters": (
        "Non-vehicle models with the Legiones Astartes (Iron Warriors) special rule receive +1 to Armour Penetration rolls "
        "made against Fortifications, Buildings, Bunkers, Tank Traps and other immobile structures with an Armour Value. "
        "Iron Warriors models only trigger enemy Minefields on a roll of 6. An Iron Warriors unit occupying a friendly "
        "Fortification or Bunker gains the Stubborn special rule; this provides no benefit while occupying a "
        "Fortification belonging to the enemy at the beginning of the battle."),
    "An Army of Steel and Wrath": (
        "When constructing an Iron Warriors Detachment, the player may exchange two Fast Attack selections for one "
        "additional Heavy Support selection. This exchange may only be made once. With the Standard Force Organisation "
        "Chart the army may therefore include 0-1 Fast Attack and 0-4 Heavy Support choices; all other Force "
        "Organisation limits remain unchanged. The exchange is made automatically: as soon as the Detachment contains a "
        "fourth Heavy Support choice, it may include no more than one Fast Attack choice."),
    "Stubborn Resolve": (
        "If a mission uses a variable game length and the game would normally end, the opposing player may demand that "
        "one additional complete game turn be played. Roll a D6: on a 3+ one additional complete game turn is played. "
        "This roll may only be made once; after the additional game turn the battle ends automatically. No effect in a "
        "mission which ends immediately when a particular objective or action is completed once it has occurred."),
    "Preliminary Bombardment (Iron Warriors)": (
        "Only in missions which already use Preliminary Bombardment. The Iron Warriors player receives one additional "
        "Preliminary Bombardment roll for every full 500 points in the army. Before any Preliminary Bombardment rolls are "
        "made, each additional roll must be assigned to an eligible enemy unit or obstacle; several may be assigned to "
        "the same target, but all rolls assigned to a target are made together. Additional rolls may not be assigned "
        "after bombardment rolls have begun. Resolve them using the normal Preliminary Bombardment rules."),
    # Armoury
    "Shrapnel Bolts": (
        "5 points per unit. The following weapons carried by models in the unit gain the Pinning special rule: Bolt "
        "Pistols, Bolters, Combi-Bolters, Storm Bolters, Heavy Bolters, Twin-linked Bolters and the bolter component of "
        "Combi-Weapons. Any unit may purchase Shrapnel Bolts (including vehicles, Dreadnoughts, named characters and "
        "Primarchs) for the bolt weapons it carries. Shrapnel Bolts may not be combined with Special Issue Ammunition, "
        "Hellfire Rounds or another special ammunition type: a bolt weapon firing Shrapnel Bolts uses no other special "
        "ammunition for that attack, and a weapon firing another special ammunition type does not gain Pinning from "
        "Shrapnel Bolts for that attack."),
    "Shrapnel Bolts (The Hammer of Olympia)": (
        "The Hammer of Olympia: this unit has Shrapnel Bolts at no additional points cost (applied automatically; see "
        "Shrapnel Bolts)."),
    "Servo-Arm (Iron Warriors)": (
        "Any Iron Warriors model with access to the Space Marine Armoury may purchase a Servo-Arm for +30 points, even if "
        "it is not normally permitted to select Techmarine equipment. The Servo-Arm follows the normal rules of the "
        "Legiones Astartes Army List. A model equipped with a Jump Pack may not purchase a Servo-Arm."),
    "Bionics (Iron Warriors)": (
        "Any Iron Warriors model with access to the Space Marine Armoury may purchase Bionics for +5 points instead of "
        "the normal +10 points. Bionics otherwise follow the normal rules."),
    # Rites of War
    "The Hammer of Olympia": (
        "EFFECTS - The Iron Line: the army's compulsory Troops choices must be selected from Legion Tactical Squads and "
        "Legion Breacher Siege Squads; Legion Tactical Squads and Legion Breacher Siege Squads automatically gain "
        "Shrapnel Bolts at no additional points cost. "
        "Hail of Fire: Iron Warriors Tactical Squads and Breacher Siege Squads equipped with Shrapnel Bolts may declare a "
        "charge after firing Rapid Fire weapons during the Shooting phase; a unit which does so does not receive the "
        "normal +1 Attack bonus for charging that Assault phase. A unit which used Fury of the Legion during the same "
        "player turn may not benefit from this rule. Fury of Olympia: models equipped with Shrapnel Bolts may re-roll To "
        "Hit rolls of 1 when firing those weapons at an enemy unit within 12\" (not when firing Snap Shots). Armoured "
        "Resolve: Iron Warriors Legion Predator Strike Squadrons, Legion Vindicator Siege Tank Squadrons, Land Raiders "
        "(every Land Raider variant, including Achilles-Alpha Land Raiders and Land Raider Battle Squadrons) "
        "and Legion Spartan Assault Tanks ignore Crew Shaken and Crew Stunned results; other Vehicle Damage results apply "
        "normally. LIMITATIONS - The army's Warlord must possess the Master of the Legion special rule. The compulsory "
        "Troops choices must be Legion Tactical Squads or Legion Breacher Siege Squads. No Iron Warriors unit may deploy "
        "using Deep Strike; units which are required to enter play by Deep Strike (Drop Pods, Dreadclaws) may not be "
        "selected, and no Deep Strike wargear (Teleport Homers, Locator Beacons) may be taken."),
    "The Ironfire": (
        "EFFECTS - Artillery Column: one Legion Artillery Tank Squadron may be selected as a non-compulsory Troops choice; "
        "it does not occupy a Heavy Support choice, may not fulfil a compulsory Troops selection and does not count as a "
        "Scoring Unit unless it would normally do so for another reason. The normal 0-1 restriction on Legion Artillery "
        "Tank Squadrons still applies. Rolling Bombardment: when an Iron Warriors Barrage weapon fires at a point within "
        "12\" of a friendly Iron Warriors unit, an attack that would scatter 2D6\" scatters only D6\"; after resolving "
        "it, place an Ironfire Marker at the final centre point of the Blast marker. Walking the Fire: when another Iron "
        "Warriors Barrage weapon fires, it does not scatter if the initial target point is within 18\" of an Ironfire "
        "Marker AND within 6\" of a friendly Iron Warriors unit; afterwards place a new Ironfire Marker at the centre of "
        "the Blast marker. If an Iron Warriors Shooting phase ends without a new Ironfire Marker being placed, remove all "
        "Ironfire Markers. Ride the Ironfire: Iron Warriors Infantry units with at least one model within 6\" of an "
        "Ironfire Marker gain Fearless while at least one model remains within 6\" of a marker. LIMITATIONS - The army's "
        "Warlord must possess the Master of the Legion special rule. The army must contain at least one unit equipped "
        "with a Barrage weapon. If the mission designates an Attacker and a Defender, the Iron Warriors must be the "
        "Attacker. The army may not include a Fortification."),
    "Selected as Troops (Artillery Column)": (
        "The Ironfire: this Legion Artillery Tank Squadron is a non-compulsory Troops choice. It does not occupy a Heavy "
        "Support choice, may not fulfil a compulsory Troops selection and is not a Scoring Unit unless it would normally "
        "be one for another reason."),
    # units
    "Coordinated Bombardment": (
        "When the squad fires its Cyclone Missile Launchers, it may re-roll one failed To Hit roll made with a Cyclone "
        "Missile Launcher during that Shooting phase. A model equipped with a Cyclone Missile Launcher may fire it in "
        "addition to its Storm bolter or Foeblaster boltgun during the same Shooting phase; both weapons must target the "
        "same enemy unit."),
    "Enhanced Targeting": "Iron Havocs have Ballistic Skill 5, as shown in their profile.",
    "Hatred (Battle-Automata)": "This unit uses the normal ProHammer Hatred special rule when fighting enemy Battle-Automata.",
    "Those Once Honoured": (
        "One Dominator Cohort may be selected as Perturabo's personal retinue. If selected in this manner, the squad does "
        "not occupy an Elites choice and Perturabo and the Dominator Cohort count as a single HQ selection. (Select it "
        "in Perturabo's Primarch Retinue.)"),
    "Cybernetica Cortex": (
        "Battle-Automata controlled by a Cybernetica Cortex: use the Cybernetica Cortex rules of the ProHammer Mechanicum "
        "document. Perturabo carries a Cortex Controller for his Iron Circle retinue."),
    "Reactor Blast": "Use the Reactor Blast rule of the ProHammer Mechanicum document.",
    "Moving Bulwark": (
        "If a Domitar-Ferrum is in base contact with another friendly Domitar-Ferrum from the same unit, both models "
        "improve their Invulnerable Save from 5+ to 4+. The bonus is lost as soon as they are no longer in base contact."),
    "Iron Warriors Construct": (
        "The Iron Circle counts as an Iron Warriors unit for rules which specifically affect friendly Iron Warriors units. "
        "It does not possess the Legiones Astartes special rule. The Iron Circle may only be selected as Perturabo's "
        "Primarch Retinue."),
    # characters
    "Feel No Pain (5+)": "This model has the Feel No Pain special rule with a 5+ roll.",
    "Battlesmith (Dreygur)": (
        "During the Shooting phase, instead of firing a weapon, Dreygur may attempt to repair a friendly damaged Vehicle "
        "with which he is in base contact or embarked upon. On a roll of 5+, remove one Engine Damaged, Weapon Destroyed "
        "or Immobilised result."),
    "Master of Automata": (
        "Narik Dreygur may join a friendly unit of Battle-Automata despite the normal restrictions on Independent "
        "Characters joining Monstrous Creatures. While joined to such a unit, it may use his Leadership for any Leadership "
        "tests it is required to make."),
    "Cortex Controller (Iron Warriors)": (
        "Friendly Battle-Automata with a model within 6\" of this character automatically pass any Command Uplink or "
        "equivalent control test they are required to make."),
    "Terminator Attack": (
        "If Erasmus Golg is the army's Warlord, Legion Terminator Squads may be selected as Troops choices. Terminator "
        "Squads selected in this manner may not be used to fulfil the army's compulsory Troops selections. (Use the "
        "'Selected as Troops (Terminator Attack)' option on the Legion Terminator Squad.)"),
    "Command Retinue (Golg)": (
        "Golg may select a Legion Terminator Command Squad, Tyrant Siege Terminator Squad or Dominator Cohort as his "
        "retinue. The selected unit does not occupy a separate Force Organisation slot and Golg and his retinue count as "
        "a single HQ selection."),
    "Battlesmith (Vhalen)": (
        "During the Shooting phase, instead of firing a weapon, Vhalen may attempt to repair a friendly damaged Vehicle "
        "with which he is in base contact or embarked upon. Normally the repair succeeds on a 5+; Vhalen's Servo-Arm adds "
        "+1, so he normally succeeds on a 4+. On a success, remove one Engine Damaged, Weapon Destroyed or Immobilised "
        "result."),
    "Shatterblade": (
        "Kyr Vhalen's Feel No Pain save is already included in his profile and special rules. In addition, Vhalen and "
        "any unit he joins have the Stubborn special rule."),
    "Master of the First Grand Battalion": "Forrix and any Iron Warriors unit he has joined may re-roll failed Morale tests.",
    "Siege Commander": (
        "After deployment but before the first turn begins, nominate one non-Vehicle Iron Warriors Heavy Support unit. "
        "That unit gains the Tank Hunters special rule for the remainder of the battle."),
    "Command Retinue (Forrix)": (
        "Forrix may select either a Legion Terminator Command Squad or Tyrant Siege Terminator Squad as his retinue. The "
        "selected unit does not occupy a separate Force Organisation slot and Forrix and his retinue count as a single "
        "HQ selection."),
    "The Bloody-Handed": (
        "Kroeger has the Furious Charge special rule. Any Iron Warriors unit Kroeger has joined also gains Furious Charge "
        "while he remains part of the unit."),
    "No Surrender": (
        "Whenever Kroeger and his unit win a close combat and one or more defeated enemy units Retreat, Kroeger's unit "
        "must Pursue if it is legally permitted to do so; it may not choose to Consolidate instead. If no enemy unit "
        "Retreats, or if Kroeger's unit is not permitted to Pursue, it may Consolidate normally."),
    "Command Retinue (Kroeger)": (
        "Kroeger may select one Legion Command Squad as his retinue. The Command Squad does not occupy a separate Force "
        "Organisation slot and Kroeger and the squad count as a single HQ selection."),
    # Perturabo
    "Siege Specialists": (
        "A unit using Siege Specialists receives +1 to Armour Penetration rolls against Fortifications, Buildings, "
        "Bunkers and other immobile structures with an Armour Value. All other abilities use their normal ProHammer "
        "rules."),
    "Lord of Iron": (
        "Perturabo has the Tank Hunters and Siege Specialists special rules. Any unit Perturabo has joined gains Tank "
        "Hunters while he remains part of that unit."),
    "Calculated Destruction": (
        "Before deployment, nominate one enemy Vehicle, Fortification or Lord of War. Perturabo may re-roll failed Armour "
        "Penetration rolls made against the nominated model for the duration of the battle."),
    "Battlefield Calculation": (
        "After both armies have deployed but before the first turn begins, nominate one friendly Iron Warriors unit. That "
        "unit may immediately be repositioned up to 6\". Every model must remain entirely within its normal deployment "
        "zone, and this move may not be used to embark upon or disembark from a Transport."),
    "Siege Bombardments": (
        "After deployment zones have been determined, but before either army deploys, nominate two terrain features as "
        "Perturabo's plotted bombardment targets and select one bombardment profile for each (Lance Strike, Melta Torpedo "
        "or Barrage Bomb; the same or different). The Siege Bombardments begin the battle in Reserve as a single Reserve "
        "entry (the controlling player may choose not to make the Reserve roll). Once available, one of the two plotted "
        "bombardments may be resolved during each subsequent friendly Shooting phase: place the Blast marker anywhere "
        "within the nominated terrain feature and scatter normally - if an arrow is rolled, double the distance "
        "scattered; if a Hit is rolled, the marker still scatters the distance rolled in the direction of the small "
        "arrow on the Hit symbol. A Siege Bombardment counts as an Ordnance Barrage attack and causes Pinning."),
    "Primarch Retinue (Perturabo)": (
        "Perturabo may select one of the following as his Primarch Retinue: Legion Honour Guard Squad, Legion Terminator "
        "Command Squad, Dominator Cohort or Iron Circle Maniple. It does not occupy an additional Force Organisation "
        "selection and otherwise follows the normal Primarch Retinue rules."),
}

WEAPONS_ = {
    "Olympia-pattern Bolt Cannon": ('36"', "5", "4", "Heavy 5, Pinning"),
    "Graviton Maul": ("-", "10", "-", "Power Weapon, Concussive"),
    "Graviton Gauntlet": ("-", "8", "-", "Power Weapon, Unwieldy, Concussive"),
    "Master-crafted Bolt Pistol": ('12"', "4", "5", "Pistol, Master-crafted"),
    "Master-crafted Power Fist": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Master-crafted"),
    "Extricator": ("-", "10", "-", "Power Weapon, Master-crafted, Unwieldy, Armourbane"),
    "Aegeas": ("-", "User +2", "-", "Rending, Master-crafted, Blind"),
    "Forgebreaker": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Concussive, Master-crafted, "
                                    "Armourbane"),
    "Logos Array": ('30"', "6", "3", "Assault 6, Twin-linked, Shred, Pinning"),
}
MULTI = {
    "Siege Bombardments": {
        "Siege Bombardment - Lance Strike": ("Unlimited", "10", "1", "Ordnance 1, Blast, Barrage, Pinning"),
        "Siege Bombardment - Melta Torpedo": ("Unlimited", "8", "3", "Ordnance 1, Blast, Armourbane, Barrage, Pinning"),
        "Siege Bombardment - Barrage Bomb": ("Unlimited", "6", "4", "Ordnance 1, Blast, Barrage, Pinning"),
    },
}
WEAPON_RULES_ = {
    "Olympia-pattern Bolt Cannon": ["Pinning"],
    "Graviton Maul": ["Concussive"],
    "Graviton Gauntlet": ["Unwieldy", "Concussive"],
    "Master-crafted Bolt Pistol": ["Master-Crafted"],
    "Master-crafted Power Fist": ["Unwieldy", "Master-Crafted"],
    "Extricator": ["Master-Crafted", "Unwieldy", "Armourbane"],
    "Aegeas": ["Rending", "Master-Crafted", "Blind"],
    "Forgebreaker": ["Unwieldy", "Concussive", "Master-Crafted", "Armourbane"],
    "Logos Array": ["Twin-Linked", "Shred", "Pinning"],
    "Siege Bombardments": ["Siege Bombardments", "Pinning", "Armourbane"],
}
WARGEAR_ = {
    "Karceri Battle Shield": "Grants the Domitar-Ferrum its 5+ Invulnerable Save (already included in its profile).",
    "Iron Halo (Named Character)": (
        "Grants a 4+ Invulnerable Save. Part of this named character's own wargear; not counted towards the army's normal "
        "limit of one Iron Halo."),
    "The Logos": (
        "Counts as Primarch Armour and incorporates a Nuncio Vox. In addition, once during each friendly Shooting phase, "
        "one friendly Iron Warriors Heavy Support unit with at least one model within 12\" of Perturabo may re-roll one "
        "failed To Hit roll made with a shooting attack.", ["Primarch Armour"]),
}


def register():
    ARMY_RULES.update(RULES)
    register_data(weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_, multi_profile=MULTI)
    # The Hammer of Olympia: compulsory Troops only Tactical / Breacher Siege Squads
    L2.NOT_LINE_UNDER["Legion Assault Squad"].append("The Hammer of Olympia")


# ------------------------------------------------------------------ local helpers
def model(u, name, cost, mn, mx, utype, stats, kit, groups=(), rules_=()):
    mid = uid("model", u, name)
    return mid, entry(mid, name, typ="model", cost=cost,
                      constraints=[constraint(uid(mid, "min"), "min", mn), constraint(uid(mid, "max"), "max", mx)],
                      profiles=[unit_profile(u, name, utype, *stats)], links=[gear(mid, k) for k in kit],
                      groups=list(groups), infolinks=rules_links(list(rules_), key=mid))


def find_group(e, name):
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == name:
            return g
    return None


def per_model_rule(key, name, pts, unit_id, rules_):
    """'The entire squad may take <special rule> for +N points per model'."""
    eid = uid("squadwide", key, name)
    return entry(eid, name, mods=[modifier("increment", PTS, pts, repeats=[repeat("model", unit_id, 1)])],
                 constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                 infolinks=rules_links(list(rules_), key=eid))


def troops_toggle(e, key, label, visible_conds, rule_name, remove_cat):
    """An option that makes the unit a non-compulsory Troops choice while visible_conds hold."""
    u = e.get("id")
    tog = uid(u, "iw-troops", key)
    off = all_of(*[_negate(c) for c in visible_conds])
    add_to(e, "selectionEntries", [entry(
        tog, label, constraints=[constraint(uid(tog, "max"), "max", 1, auto=True)],
        mods=[modifier("set", "hidden", "true", groups=[off]),
              modifier("set", uid(tog, "max"), 0, groups=[all_of(*[_negate(c) for c in visible_conds])])],
        infolinks=rules_links([rule_name], key=tog))])
    on = [cond(tog, "self", "atLeast", 1)]
    add_mods(e, [modifier("set-primary", "category", TROOPS, conds=on),
                 modifier("remove", "category", remove_cat, conds=on),
                 modifier("remove", "category", gs.CAT_LINE, conds=on)])
    return tog


def is_vehicle(e):
    """No model in the unit has an ordinary (non-vehicle) Unit profile."""
    return not any(p.get("typeName") == "Unit" for p in e.iter("profile"))


# ------------------------------------------------------------------ units
# "Land Raider" for these squads means the Land Raider Spartan (author, Q13)
TDA_TRANSPORTS = ["Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"]


def tyrant_squad(key="Tyrant Siege Terminator Squad", root=True):
    name = "Tyrant Siege Terminator Squad"
    u = uid("unit", key)
    kit = ["Cataphractii Terminator Armour", "Storm Bolter", "Power Weapon", "Cyclone Missile Launcher"]
    tid, terms = model(u, "Tyrant Siege Terminator", 65, 4, 9, "Infantry", (4, 4, 4, 4, 1, 3, 2, 9, "2+/4+"), kit)
    mid = uid("model", u, "Tyrant Siege Master")
    ranged = [("Foeblaster Boltgun", 5)]
    cc = [("Power Fist", 5), ("Chainfist", 10)]
    _, master = model(u, "Tyrant Siege Master", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 3, 3, 9, "2+/4+"),
                      kit, groups=[slot(mid, "Replace Storm Bolter", "Storm Bolter", ranged),
                                   slot(mid, "Replace Power Weapon", "Power Weapon", cc),
                                   take(mid, "Tyrant Siege Master Wargear", [("Grenade Harness", 10)])])
    return entry(u, name, typ="unit", cost=325 - 4 * 65, cats=[foc(HS, "Heavy Support", u)] if root else [],
                 infolinks=rules_links([LR, "Coordinated Bombardment"] + ([] if root else ["Retinue"]), key=u),
                 entries=[master, terms],
                 groups=[model_swaps(u, "Tyrant Siege Terminators: replace Storm Bolter (any number)", u, [tid], ranged),
                         model_swaps(u, "Tyrant Siege Terminators: replace Power Weapon (any number)", u, [tid], cc),
                         transports(u, u, TDA_TRANSPORTS, orbital=False)])


def iron_havocs():
    name = "Iron Havoc Squad"
    u = uid("unit", name)
    kit = ["Power Armour", "Bolter", "Bolt Pistol", "Frag Grenades"]
    hid, havocs = model(u, "Iron Havoc", 25, 4, 9, "Infantry", (4, 5, 4, 4, 1, 4, 1, 8, "3+"), kit)
    sid = uid("model", u, "Iron Havoc Sergeant")
    _, sgt = model(u, "Iron Havoc Sergeant", 0, 1, 1, "Infantry (Character)", (4, 5, 4, 4, 1, 4, 2, 9, "3+"), kit,
                   groups=[take(sid, "Iron Havoc Sergeant Wargear", [("Signum", 15)]),
                           pa_armoury(sid, u, 10, slots=["Bolt Pistol", "Bolter"], skip=("Signum",))])
    heavy, _ = pool(u, "Heavy Weapons (up to four Iron Havocs, replace Bolter)", u,
                    [("Heavy Bolter", 10), ("Missile Launcher", 15), ("Autocannon", 20), ("Lascannon", 30)], 4)
    return entry(u, name, typ="unit", cost=140 - 4 * 25, cats=[foc(HS, "Heavy Support", u)],
                 infolinks=rules_links([LR, "Enhanced Targeting"], key=u),
                 entries=[sgt, havocs, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model_rule(u, "Tank Hunters (entire squad)", 3, u, ["Tank Hunters"])],
                 groups=[heavy])


def dominator_cohort(key="Dominator Cohort", root=True):
    name = "Dominator Cohort"
    u = uid("unit", key)
    kit = ["Cataphractii Terminator Armour", "Combi-Bolter", "Thunder Hammer"]
    did, doms = model(u, "Dominator", 50, 4, 9, "Infantry", (5, 4, 4, 4, 1, 3, 2, 9, "2+/4+"), kit)
    wid = uid("model", u, "Dominator Warden")
    ranged = [("Volkite Charger", 10), ("Combi-Flamer", 10), ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15)]
    cc = [("Chainfist", 0)]
    heavy_opts = [("Heavy Flamer", 10), ("Reaper Autocannon", 15), ("Multi-Melta", 15)]
    _, warden = model(u, "Dominator Warden", 0, 1, 1, "Infantry (Character)", (5, 4, 4, 4, 1, 3, 3, 9, "2+/4+"), kit,
                      groups=[slot(wid, "Replace Combi-bolter", "Combi-Bolter", ranged),
                              slot(wid, "Replace Thunder Hammer", "Thunder Hammer", cc),
                              take(wid, "Dominator Warden Wargear", [("Grenade Harness", 10)])])
    heavy, _ = pool(u, "Heavy Weapons (1 Dominator per 5 models, replace Combi-bolter)", u, heavy_opts, 0, every=5)
    rl = [LR, "Stubborn", "Hatred (Battle-Automata)", "Those Once Honoured"] + ([] if root else ["Retinue"])
    return entry(u, name, typ="unit", cost=250 - 4 * 50, cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links(rl, key=u), entries=[warden, doms],
                 groups=[model_swaps(u, "Dominators: replace Thunder Hammer (any number)", u, [did], cc),
                         model_swaps(u, "Dominators: replace Combi-bolter (any number)", u, [did], ranged,
                                     minus=[W(n) for n, _ in heavy_opts]),
                         heavy, transports(u, u, TDA_TRANSPORTS, orbital=False)])


def iron_circle(key="Iron Circle Domitar-Ferrum Maniple", root=True):
    name = "Iron Circle Domitar-Ferrum Maniple"
    u = uid("unit", key)
    _, dom = model(u, "Domitar-Ferrum", 205, 1, 6, "Monstrous Creature", (4, 4, 7, 7, 4, 3, 3, 8, "3+/5+"),
                   ["Olympia-pattern Bolt Cannon", "Graviton Maul", "Karceri Battle Shield"])
    rl = ["Cybernetica Cortex", "Reactor Blast", "Crusader", "Moving Bulwark", "Iron Warriors Construct"]
    return entry(u, name, typ="unit", cost=0, cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links(rl + ([] if root else ["Retinue"]), key=u), entries=[dom])


# ------------------------------------------------------------------ characters
DREYGUR = uid("unit", "Narik Dreygur")
GOLG = uid("unit", "Erasmus Golg")
VHALEN = uid("unit", "Kyr Vhalen")
FORRIX = uid("unit", "Forrix, First Captain of the Iron Warriors")
KROEGER = uid("unit", "Kroeger, the Bloody-Handed")
PERTURABO = uid("unit", "Perturabo, the Lord of Iron")


def characters():
    out = []
    out.append(named_character(
        LR, "Nârik Dreygur", 140, (5, 5, 4, 4, 3, 5, 3, 9, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Graviton Gauntlet", "Master-crafted Bolt Pistol", "Frag Grenades",
         "Cortex Controller"],
        ["Feel No Pain (5+)", "Battlesmith (Dreygur)", "Master of Automata", "Cortex Controller (Iron Warriors)"],
        master=False, compulsory=False, key="Narik Dreygur", profile_name="Narik Dreygur",
        extra_groups=[take(DREYGUR, "Wargear", [("Krak Grenades", 2)])]))
    out.append(named_character(
        LR, "Erasmus Golg", 175, (6, 5, 4, 4, 4, 4, 4, 10, "2+/4+"),
        ["Cataphractii Terminator Armour", "Extricator", "Combi-Meltagun", "Nuncio Vox"],
        ["Stubborn", "Terminator Attack", "Command Retinue (Golg)"],
        retinue=retinue_links("golg", [L2.terminator_command_squad("golg"), tyrant_squad("golg-tyrant", root=False),
                                       dominator_cohort("golg-dominator", root=False)])))
    out.append(named_character(
        LR, "Kyr Vhalen", 195, (6, 5, 4, 4, 4, 5, 4, 10, "2+/4+"),
        ["Artificer Armour", "Iron Halo (Named Character)", "Aegeas", "Volkite Charger", "Servo-Arm",
         "Cortex Controller", "Frag Grenades", "Melta Bombs"],
        ["Feel No Pain (5+)", "Battlesmith (Vhalen)", "Shatterblade", "Stubborn", "Cortex Controller (Iron Warriors)"],
        extra_groups=[take(VHALEN, "Wargear", [("Krak Grenades", 2)])]))
    out.append(named_character(
        LR, "Forrix, First Captain of the Iron Warriors", 190, (6, 5, 4, 4, 3, 5, 4, 10, "2+/4+"),
        ["Cataphractii Terminator Armour", "Master-crafted Power Fist", "Combi-Meltagun"],
        ["Master of the First Grand Battalion", "Siege Commander", "Command Retinue (Forrix)"], master=True,
        profile_name="Forrix",
        retinue=retinue_links("forrix", [L2.terminator_command_squad("forrix"),
                                         tyrant_squad("forrix-tyrant", root=False)])))
    out.append(named_character(
        LR, "Kroeger, the Bloody-Handed", 140, (6, 5, 4, 4, 2, 5, 4, 10, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Power Weapon", "Bolt Pistol", "Frag Grenades"],
        ["The Bloody-Handed", "Furious Charge", "No Surrender", "Command Retinue (Kroeger)"], master=False,
        profile_name="Kroeger",
        retinue=retinue_links("kroeger", [command_squad_for("kroeger", KROEGER)]),
        extra_groups=[take(KROEGER, "Wargear", [("Krak Grenades", 2)])]))
    return out


def perturabo():
    ret = primarch_retinue("perturabo", extra=[dominator_cohort("perturabo-dominator", root=False),
                                               iron_circle("perturabo-iron-circle", root=False)])
    return primarch(LR, "Perturabo, the Lord of Iron", 500, (7, 7, 6, 6, 6, 5, 4, 10, "1+"),
                    ["The Logos", "Forgebreaker", "Logos Array", "Siege Bombardments", "Cortex Controller"],
                    ["Primarch Armour", "Lord of Iron", "Tank Hunters", "Siege Specialists", "Calculated Destruction",
                     "Battlefield Calculation", "Siege Bombardments", "Primarch Retinue (Perturabo)"],
                    retinue=ret, profile_name="Perturabo")


# ------------------------------------------------------------------ Armoury
SHRAPNEL_WEAPONS = ["Bolt Pistol", "Bolter", "Combi-Bolter", "Storm Bolter", "Heavy Bolter", "Twin-linked Bolter",
                    "Combi-Flamer", "Combi-Meltagun", "Combi-Plasma Gun", "Combi-Grenade Launcher",
                    "Combi-Volkite Charger", "Combi-Weapon", "Heavy Bolter with Suspensor Web",
                    "Heavy Bolter with Suspensor and Hellfire Rounds", "Dreadnought Close Combat Weapon",
                    "Chainfist with built-in Twin-linked Bolter", "Space Marine Bike with Twin-linked Bolters",
                    "Attack Bike with Twin-linked Bolters", "Logos Array", "Master-crafted Bolt Pistol",
                    "Olympia-pattern Bolt Cannon"]


def add_shrapnel_bolts(ctx):
    """Shrapnel Bolts (+5 per unit) for every unit with a bolt weapon - vehicles, Dreadnoughts, named characters and
    Perturabo included (author, Q3). Special ammunition is exclusive per attack, not per unit (Q4), so nothing is
    blocked. Under The Hammer of Olympia, Tactical / Breacher Siege Squads get them automatically and free (Q7)."""
    targets = {W(n) for n in SHRAPNEL_WEAPONS if n in WEAPONS or n in WARGEAR}
    hammer_free = {"Legion Tactical Squad", "Legion Breacher Siege Squad"}
    free_tid, free_name = rule_ref("Shrapnel Bolts (The Hammer of Olympia)")
    n = 0
    done = set()
    for e in ctx.all_entries():
        if e.get("type") != "unit" or e.get("id") in done:
            continue
        done.add(e.get("id"))
        tids = {lk.get("targetId") for lk in e.iter("entryLink")}
        if not tids & targets:
            continue  # no bolt weapons
        u = e.get("id")
        eid = uid("iw-shrapnel", u)
        mods = []
        if e.get("name") in hammer_free:
            mods = [modifier("set", "hidden", "true", conds=[rite("The Hammer of Olympia")]),
                    modifier("set", uid(eid, "max"), 0, conds=[rite("The Hammer of Olympia")])]
            add_to(e, "infoLinks", [info_link(free_tid, free_name, "rule", key=uid(eid, "free"), mods=[
                modifier("set", "hidden", "true", conds=[_negate(rite("The Hammer of Olympia"))])])])
        add_to(e, "selectionEntries", [entry(eid, "Shrapnel Bolts (unit)", cost=5, mods=mods,
                                             constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                                             infolinks=rules_links(["Shrapnel Bolts"], key=eid))])
        n += 1
    return n


def add_servo_arm(ctx):
    """Servo-Arm (+30) for every model with access to the Space Marine Armoury, not with a Jump Pack."""
    seen = set()
    n = 0
    for e in ctx.all_entries():
        u = e.get("id")
        gs_ = [g for g in e.iter("selectionEntryGroup") if g.get("name") == "Space Marine Armoury (max 50 pts)"]
        if e.get("name") in ("Legion Praetor", "Legion Centurion"):
            arm = find_group(e, "Space Marine Armoury (max 100 pts)")
            gs_.append(find_group(arm, "Additional Wargear"))
        for g in gs_:
            if id(g) in seen:
                continue
            seen.add(id(g))
            links = g.find("entryLinks")
            if links is None:
                links = el("entryLinks")
                g.append(links)
            lid = uid("link", g.get("id"), "iw", "Servo-Arm")
            jp = [has(W("Jump Pack"), u)]
            links.append(link(lid, W("Servo-Arm"), "Servo-Arm", cost=30,
                              mods=[modifier("set", "hidden", "true", conds=jp),
                                    modifier("set", uid(lid, "max"), 0, conds=list(jp))],
                              constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
            n += 1
    return n


def cheap_bionics(ctx):
    bid = W("Bionics")
    n = 0
    done = set()
    for e in ctx.all_entries():
        if id(e) in done:
            continue
        done.add(id(e))
        for lk in e.iter("entryLink"):
            if lk.get("targetId") != bid:
                continue
            for c in lk.iter("cost"):
                if c.get("typeId") == PTS and float(c.get("value")) == 10:
                    c.set("value", "5")
                    n += 1
    return n


# ------------------------------------------------------------------ extend
BARRAGE = ["Quad Launcher", "Quad Launcher with Frag and Shatter Shells", "Whirlwind Launcher", "Earthshaker Cannon",
           "Medusa Siege Gun", "Scorpius Multi-launcher", "Phosphex Discharger", "Siege Bombardments"]


def extend(ctx):
    legion = ctx.unit("Legion")
    ctx.legion_rules([LR, "Siege Masters", "An Army of Steel and Wrath", "Stubborn Resolve",
                      "Preliminary Bombardment (Iron Warriors)", "Shrapnel Bolts", "Servo-Arm (Iron Warriors)",
                      "Bionics (Iron Warriors)"])

    # An Army of Steel and Wrath: automatic - 0-4 Heavy Support, but with a 4th HS choice only 0-1 Fast Attack (Q1)
    add_mods(legion, [
        modifier("add", "category", gs.FOC_PLUS["Heavy Support"]),
        modifier("add", "error", "An Army of Steel and Wrath: a Detachment with four Heavy Support choices may include "
                                 "no more than one Fast Attack choice.",
                 conds=[cond(HS, "force", "atLeast", 4), cond(FA, "force", "atLeast", 2)])])

    # units
    # Iron Circle: only as Perturabo's Primarch Retinue (author, Q19)
    ctx.add_units(tyrant_squad(), iron_havocs(), dominator_cohort(), *characters(), perturabo())

    # Erasmus Golg: Terminator Attack
    troops_toggle(ctx.unit("Legion Terminator Squad"), "golg", "Selected as Troops (Terminator Attack)",
                  [cond(GOLG, "force", "atLeast", 1)], "Terminator Attack", ELITES)
    # The Ironfire: Artillery Column
    troops_toggle(ctx.unit("0-1 Legion Artillery Tank Squadron"), "ironfire", "Selected as Troops (Artillery Column)",
                  [rite("The Ironfire")], "Selected as Troops (Artillery Column)", HS)

    # Armoury
    add_shrapnel_bolts(ctx)
    add_servo_arm(ctx)
    cheap_bionics(ctx)

    # Rites of War
    T = L.TRANSPORTS
    pods = [cond(T[n], "force", "atLeast", 1) for n in ["Legion Drop Pod", "Anvillus Pattern Dreadclaw Drop Pod",
                                                         "Legion Dreadnought Drop Pod"]]
    pods += [cond(W(n), "force", "atLeast", 1) for n in ["Teleport Homer", "Locator Beacon"]]
    hid = rite_id("The Hammer of Olympia")
    ctx.add_rite("The Hammer of Olympia", RULES["The Hammer of Olympia"], mods=[modifier(
        "add", "error", "The Hammer of Olympia: units which are required to enter play by Deep Strike (Drop Pods, "
                        "Dreadclaws) and Deep Strike wargear (Teleport Homers, Locator Beacons) may not be selected.",
        conds=[cond(hid, "force", "atLeast", 1)], groups=[any_of(*pods)])])
    iid = rite_id("The Ironfire")
    no_barrage = all_of(*[cond(W(n), "force", "lessThan", 1) for n in BARRAGE])
    ctx.add_rite("The Ironfire", RULES["The Ironfire"], mods=[modifier(
        "add", "error", "The Ironfire: the army must contain at least one unit equipped with a Barrage weapon.",
        conds=[cond(iid, "force", "atLeast", 1)], groups=[no_barrage])], errors=[
        ("the army may not include a Fortification.", [cond(gs.cat("Fortification"), "roster", "atLeast", 1)]),
    ])
