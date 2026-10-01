"""I Legion - Dark Angels (Forces of the Legions).

Source: /home/claude/src/legions/I_Dark_Angels.txt. Open points are listed in tools/questions/I - Dark Angels.md.
"""
import copy

from legions.common import *  # noqa: F401,F403
from legions.common import (ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR, required_choice, choice_id,
                            legion_units, retinue_links, primarch, primarch_retinue, named_character, command_squad_for,
                            clone, option, add_group, add_entry, register_data, LOW, LOYALIST, TRAITOR)
from bsx import (PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group,
                 category_link)
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, TDA, gear, per_model, rules_links, unit_profile
from legiones2 import (slot, take, pool, transports, add_mods, add_to, dedupe_kit, walker_profile, foc, rite_id, rite,
                       TROOPS, ELITES, FA, HQ, HS, model_swaps, model_takes, model_pair_claws, T)

LEGION = "I - Dark Angels"
LR = "Legiones Astartes (Dark Angels)"
WING = "Hexagrammaton Wing"
WINGS = ["Stormwing", "Deathwing", "Dreadwing", "Ironwing", "Firewing", "Ravenwing"]

# ---------------------------------------------------------------- rules
RULES = {
    LR: ("Models with this rule belong to the I Legion and use the Dark Angels Legion special rules: Mastery of the "
         "Blade and The Hexagrammaton (every Dark Angels unit is assigned to one Wing)."),
    "Mastery of the Blade": (
        "When a Dark Angels model fights in close combat using a sword-type weapon against an enemy model with an equal "
        "Weapon Skill, it hits on a 3+ instead of 4+. Sword-type weapons: Chainswords, Power Weapons, Force Weapons, Rending "
        "Weapons and any Dark Angels weapon stated to count as a sword - not Power Fists, Thunder Hammers, Lightning Claws "
        "or other weapons which are clearly not swords."),
    "The Hexagrammaton": (
        "Every Dark Angels unit must be assigned to one Wing when the army is selected: Stormwing, Deathwing, Dreadwing, "
        "Ironwing, Firewing or Ravenwing. A unit normally belongs to only one Wing. A Dedicated Transport belongs to the "
        "Wing of the unit for which it was purchased. Units and named characters with a predetermined Wing may not select "
        "another. Independent Characters keep their own Wing when joining another unit; a Wing rule is not conferred "
        "between an Independent Character and a unit unless stated otherwise."),
    "Stormwing": ("When the unit resolves a First Fire or Overwatch shooting attack, models may re-roll To Hit rolls of 1 "
                  "with Bolters, Bolt Pistols, Storm Bolters, Foeblaster Boltguns and the bolter component of "
                  "Combi-weapons."),
    "Deathwing": ("Models with this Wing may re-roll To Hit rolls of 1 with sword-type weapons when fighting an enemy "
                  "whose Weapon Skill is higher than their own."),
    "Dreadwing": ("Attacks against a Dreadwing model made with a Flame, Plasma or Volkite weapon are at -1 Strength (min "
                  "1). Against Dreadwing Vehicles and Dreadnoughts this also applies when determining Armour "
                  "Penetration."),
    "Ironwing": ("Re-roll Armour Penetration rolls of 1 against enemy Vehicles. An Ironwing Vehicle firing Snap Shots hits "
                 "on a 5+ instead of 6+."),
    "Firewing": ("Re-roll To Hit rolls of 1 (shooting and close combat) when attacking an enemy unit containing an "
                 "Independent Character. If the Independent Character leaves the unit, the bonus no longer applies "
                 "against that unit."),
    "Ravenwing": ("Dark Angels Bikes and Jetbikes belonging to the Ravenwing gain Skilled Rider. Dark Angels Land Speeders "
                  "belonging to the Ravenwing gain Jink."),
    "Calibanite Warblade": "Counts as a sword-type weapon for Mastery of the Blade and Deathwing.",
    "Murderous Strike": ("A natural To Wound roll of 6 made with a Terranic Greatsword causes Instant Death. The Terranic "
                         "Greatsword counts as a sword-type weapon for Mastery of the Blade and Deathwing."),
    "Plasma Flame": ("Plasma Burners, Plasma Incinerators and Plasma-casters may re-roll failed To Hit rolls when firing "
                     "Overwatch. Roll once for the number of shots of a Plasma Burner or Plasma Incinerator; when several "
                     "identical weapons of that type in a unit fire, the one roll is used for all of them."),
    "Stasis Anomaly": ("If a unit is hit by one or more weapons with Stasis Anomaly, all models in it have Initiative 1 "
                       "until the end of the current player turn. Multiple Stasis Anomalies have no additional effect."),
    "Molecular Acid Shells": ("When firing a Heavy Bolter or Twin-linked Heavy Bolter with Molecular Acid Shells, choose "
                              "normal ammunition or Molecular Acid Shells. A Twin-linked Heavy Bolter firing Molecular "
                              "Acid Shells remains Twin-linked."),
    # units
    "Death-sworn Companions": (
        "While an eligible Dark Angels Independent Character is joined to this unit, once per phase when that Character "
        "suffers an unsaved Wound, one Companion of the unit within 2\" of him may be removed as a casualty instead and the "
        "original Wound is ignored. Against a Massive Wound this is used before rolling the D3 Wounds."),
    "Deathwing Retinue": (
        "A Deathwing Companion Detachment may be selected instead of a Legion Command Squad or Legion Honour Guard Squad for "
        "a Dark Angels Praetor or an appropriate named Dark Angels Character. It does not occupy a separate Force "
        "Organisation slot; the Character and the Detachment count as a single HQ selection."),
    "Deathwing Retinue (Terminators)": (
        "A Deathwing Terminator Companion Detachment may be selected instead of a Legion Terminator Command Squad for an "
        "eligible Dark Angels Character wearing the same pattern of Terminator Armour. It does not occupy a separate Force "
        "Organisation slot; the Character and the Terminator Companions count as a single HQ selection."),
    "Inner Circle": ("Knights Cenobium belong to the Orders of the Hekatonystika, not to the Hexagrammaton: they may not "
                     "select a Wing. Their Order Exemplars rule replaces the normal Wing benefit."),
    "Uncompromising Discipline": ("Knights Cenobium may enter and fire Overwatch despite wearing Cataphractii Terminator "
                                  "Armour. All other restrictions of Cataphractii Terminator Armour apply."),
    "Order Exemplars": "When the unit is selected, choose one Order; its benefit lasts for the entire battle.",
    "Augurs of Weakness": "+1 Strength for Armour Penetration rolls against vehicles with Armour Value 11 or higher.",
    "Icons of Resolve": "If the unit is charged, each model gains +1 Attack during that Assault phase.",
    "Guardians of Sanctity": ("Deny the Witch: roll 2D6 and use the highest result before applying any normal "
                              "modifiers."),
    "Slayers of Kings": ("Re-roll close-combat To Hit rolls of 1 against an enemy unit whose majority Weapon Skill is 5 "
                         "or higher."),
    "Hunters of Beasts": ("Re-roll To Wound rolls of 1 against Toughness 5; re-roll all failed To Wound rolls against "
                          "Toughness 6 or higher."),
    "Reapers of Hosts": ("A model which begins its Initiative step in base contact with more than one enemy model gains "
                         "+1 Attack for that Assault phase."),
    "Breakers of Witches": ("Re-roll failed close-combat To Hit and To Wound rolls against Psykers, Brotherhoods of "
                            "Psykers and models with the Daemon special rule."),
    "Bitter Duty": ("Only a Dark Angels Independent Character assigned to the Dreadwing may join a Dreadwing Interemptor "
                    "Squad. Rad Missiles, Stasis Missiles, Phosphex Bombs and Suspensor Webs use their normal rules."),
    "Supercharged Blades": (
        "At the beginning of an Assault phase in which the Cabal is engaged it may supercharge its Charge-blades: until the "
        "end of that phase they also count as Power Weapons. For each Enigmatus rolling one or more natural 1s To Hit with a "
        "supercharged blade, resolve one Strength 4 hit against that model after its attacks (Armour Saves allowed)."),
    "Hatred (Characters)": ("The unit has the Hatred special rule against enemy units containing one or more Characters "
                            "or Independent Characters."),
    # named characters
    "Paladin of Glory": (
        "When Corswain directs his attacks against an enemy Character or Independent Character he always hits on a 3+ "
        "unless he would need a better result. A natural To Wound roll of 6 with The Blade against a Character or "
        "Independent Character inflicts a Massive Wound (D3) instead of one Wound."),
    "Seneschal of the First Legion": (
        "Corswain may select a Deathwing Companion Detachment as his retinue; it may increase the Weapon Skill of every "
        "Deathwing Companion and its Oathbearer by +1 (max WS6) for +5 points per model. Corswain and his retinue count as "
        "a single HQ selection."),
    "The Blade": ("Chosen at the beginning of each Assault phase: one-handed +1 Strength (Corswain may use his Bolt Pistol "
                  "as a second close-combat weapon); two-handed Strength 6 but no bonus Attack for two close-combat "
                  "weapons."),
    "Ancient of War": (
        "After deployment but before the first turn, nominate one enemy faction in the opposing army. Marduk Sedras and "
        "friendly Dark Angels units with a model within 6\" of him may re-roll To Hit and To Wound rolls of 1 against "
        "models of that faction (Shooting and Assault phases)."),
    "Eskaton": ("Marduk Sedras is always assigned to the Dreadwing. Sedras and any Dark Angels unit he joins gain the "
                "Siege Specialists Veteran Skill."),
    "Siege Specialists": ("Veteran Skill: a unit using Siege Specialists receives +1 to Armour Penetration rolls against "
                          "Fortifications, Buildings, Bunkers and other immobile structures with an Armour Value. All other "
                          "abilities use their normal ProHammer rules."),
    "Cenobium Retinue": ("One Inner Circle Knights Cenobium unit may be selected as Marduk Sedras' personal retinue. It "
                         "does not occupy a separate Force Organisation slot; Sedras and the Cenobium count as a single HQ "
                         "selection."),
    "Murderous Strike (5+)": ("Any natural To Wound roll of 5 or 6 made with Death of Worlds inflicts a Massive Wound (D3) "
                              "instead of one Wound."),
    "Voted-Lieutenant of the Dreadwing": (
        "Farith Redloss is always assigned to the Dreadwing. One Dreadwing Interemptor Squad may be selected as his retinue "
        "(no separate Elites choice) and he may join it despite Bitter Duty. Redloss and the squad count as a single HQ "
        "selection."),
    "Extermination Protocol": (
        "Once per battle, at the beginning of the Dark Angels Shooting phase: Redloss' own unit or one friendly Dreadwing "
        "unit with a model within 12\" may re-roll To Wound rolls of 1 and Armour Penetration rolls of 1 made with Flame, "
        "Plasma or Volkite weapons until the end of that phase. The second result must be accepted."),
    "Voted-Lieutenant of the Deathwing": (
        "Holguin is always assigned to the Deathwing. He may select a Deathwing Terminator Companion Detachment as his "
        "personal retinue (no separate Force Organisation slot; a single HQ selection)."),
    "Unbroken Line": (
        "While Holguin is joined to a friendly Dark Angels unit, it gains Counter-Attack (no extra benefit if it already has "
        "it). If Holguin and his unit are charged while controlling an Objective or occupying a fortification, ruin or "
        "building, Holguin may re-roll To Hit rolls of 1 during that Assault phase."),
    # Lion
    "An Absolute Focus": ("Lion El'Jonson never needs worse than a 4+ To Hit in close combat, regardless of the enemy's "
                          "Weapon Skill or any modifiers."),
    "The Point of the Blade": ("Lion El'Jonson and any unit he has joined may declare charges against enemy units up to "
                               "8\" away instead of 6\". Difficult Terrain does not reduce this distance; Dangerous "
                               "Terrain is resolved normally."),
    "The Lion's Choler": ("While the Lion has 4 Wounds or fewer remaining, +1 Attack; while he has 2 Wounds or fewer, +2 "
                          "Attacks instead (not cumulative)."),
    "Knight of Knights": ("During each Assault phase in which the Lion directs attacks against an enemy Independent "
                          "Character or Primarch, he may re-roll one failed To Hit roll OR one failed To Wound roll against "
                          "such a model. The second result must be accepted."),
    "Primarch Retinue (Lion El'Jonson)": (
        "The Lion may select a Legion Honour Guard Squad, Legion Terminator Command Squad, Deathwing Companion Detachment or "
        "Deathwing Terminator Companion Detachment as his Primarch Retinue. A Terminator Companion Detachment may be taken "
        "although he does not wear Terminator Armour."),
}

RITE_TEXT = {
    "The Storm of War": (
        "EFFECTS - Masters of the Storm of War: a Legion Tactical Squad or Legion Assault Squad of 20 models may include one "
        "Legion Centurion (normal cost, may buy weapons and wargear normally). He does not occupy an HQ selection, becomes "
        "part of the squad and may not voluntarily leave it, may not select a Consul upgrade, may not be the Warlord and "
        "must belong to the Stormwing. Disciplined Volleys: the Stormwing bonus also applies in the Dark Angels Shooting "
        "phase if the unit remained stationary. Officers of the Storm: a Stormwing Infantry unit containing a Stormwing "
        "Character gains Stubborn.\nLIMITATIONS - The Warlord must belong to the Stormwing. The compulsory Troops must be "
        "Stormwing Legion Tactical Squads or Legion Assault Squads of 20 models each and may not select Dedicated "
        "Transports."),
    "The Unbroken Vow": (
        "EFFECTS - The Hammer of Caliban: Legion Veteran Squads and Legion Terminator Squads may be selected as Troops and "
        "may fulfil compulsory Troops. Death is not the End: a Deathwing unit with a model within 6\" of an Objective gains "
        "Feel No Pain (6+), or improves it by one step (max 4+). Marshal of the Unbroken Vow: a Deathwing Independent "
        "Character gains +1 Attack within 12\" of an Objective. The Oath: after deployment zones are determined, place an "
        "additional Objective as close as possible to the centre of the battlefield.\nLIMITATIONS - The Warlord must belong "
        "to the Deathwing. The compulsory Troops must be Deathwing Legion Veteran Squads or Legion Terminator Squads. At the "
        "end of the battle (Victory Point missions): if the Dark Angels do not control the Oath Objective the enemy gains "
        "+150 Victory Points; if the enemy controls it, +300 instead."),
    "The Eskaton Imperative": (
        "EFFECTS - Dread Legion: Legion Destroyer Squads may be Troops and fulfil compulsory Troops; Dreadwing Interemptor "
        "Squads also count as Troops. Masters of the Blackened Earth: open ground outside both deployment zones is Difficult "
        "Terrain; before deployment place up to three Eskaton Markers (outside deployment zones, 6\" from table edges, 12\" "
        "apart) - within 6\" of a marker is Dangerous Terrain. Walkers in Ash: Dreadwing Infantry gain Move Through Cover; "
        "Dreadwing models re-roll failed Dangerous Terrain tests. Marshal of the Eskaton: enemy units with a model within "
        "12\" and line of sight of the Dark Angels Warlord suffer -1 Leadership (not Fearless units, not cumulative).\n"
        "LIMITATIONS - The Warlord must belong to the Dreadwing. The compulsory Troops must be Dreadwing Legion Destroyer "
        "Squads or Dreadwing Interemptor Squads. At the end of the battle, if the enemy has a unit neither Falling Back nor "
        "Pinned wholly or partially within its own deployment zone it gains +150 Victory Points (+300 if that unit is "
        "Scoring); Victory Point missions only."),
    "The Steel Fist": (
        "EFFECTS - Iron Brethren: Legion Predator Strike Squadrons may be Troops and fulfil compulsory Troops. Armoured "
        "Assault: an Ironwing Infantry unit of 10 models or fewer may buy a Land Raider Phobos or Proteus as a Dedicated "
        "Transport at normal cost; one of 11-20 models may buy a Legion Spartan Assault Tank (normal Transport Capacity "
        "applies). Marshal of the Steel Fist: a Transport carrying an Ironwing Independent Character gains a 6+ "
        "Invulnerable Save against shooting (or +1 to an existing one, max 4+) while he is embarked.\nLIMITATIONS - The "
        "Warlord must belong to the Ironwing. The compulsory Troops must be Ironwing Legion Predator Strike Squadrons. Every "
        "Infantry unit which can be transported must begin embarked aboard a Transport Vehicle. No more than one Fast "
        "Attack choice."),
    "The Seeker's Arrow": (
        "EFFECTS - Ravenwing Host: Legion Bike Squadrons and Legion Sky Hunter Jetbike Squadrons may be Troops and fulfil "
        "compulsory Troops. Encirclement: Ravenwing Infantry, Bike and Jetbike units gain Outflank. Lightning Assault: "
        "Ravenwing Bike and Jetbike units gain Hit & Run. The Seeker's Arrow: at the beginning of each Dark Angels turn "
        "choose +2\" to Turbo-Boost and Advance moves, +2\" to Charge distances or +2\" to Consolidation moves for all "
        "Ravenwing units until the next Dark Angels turn.\nLIMITATIONS - The Warlord must belong to the Ravenwing. The "
        "compulsory Troops must be Ravenwing Legion Bike Squadrons or Sky Hunter Jetbike Squadrons. No more than one Heavy "
        "Support choice. No Vehicle unless it is Fast and/or a Skimmer."),
    "The Serpent's Bane": (
        "EFFECTS - The Serpent's Heads: after both armies are selected, nominate three enemy HQ, Elites or Lord of War units "
        "as Priority Targets (as many as possible if fewer). Execution Protocols: Firewing models re-roll To Hit and To "
        "Wound rolls of 1 (Armour Penetration against Vehicles) against Priority Targets, shooting and close combat. Marshal "
        "of the Firewing: a Firewing Independent Character gains +1 Attack while engaged with a Priority Target. Forward "
        "Deployment: up to three Firewing Troops units may gain Infiltrate. Seeker Formations: Legion Seeker Squads may be "
        "Troops and fulfil compulsory Troops.\nLIMITATIONS - The Warlord must belong to the Firewing. The compulsory Troops "
        "must be Firewing Legion Seeker Squads or Legion Assault Squads. For each Priority Target still on the battlefield "
        "at the end, the enemy gains +150 Victory Points (Victory Point missions only)."),
}

WEAPONS_ = {
    "Calibanite Warblade": ("-", "User +1", "-", "Power Weapon"),
    "Terranic Greatsword": ("-", "User +2", "-", "Power Weapon, Two-Handed, Murderous Strike"),
    "Master-crafted Terranic Greatsword": ("-", "User +2", "-", "Power Weapon, Two-Handed, Murderous Strike, "
                                                                 "Master-crafted"),
    "Calibanite Plasma Pistol": ('12"', "6", "2", "Pistol"),
    "Calibanite Plasma Gun": ('24"', "6", "2", "Rapid Fire"),
    "Calibanite Plasma Cannon": ('36"', "6", "2", "Heavy 1, Blast"),
    "Plasma Repeater": ('12"', "6", "2", "Salvo 2/3, Twin-linked, Gets Hot"),
    "Plasma Burner": ('12"', "4", "2", "Assault D3+1, Ignores Cover, Plasma Flame"),
    "Stasis Shell - Grenade": ('24"', "2", "-", "Assault 1, Blast, Stasis Anomaly"),
    "Stasis Shell - Missile": ('48"', "4", "6", "Heavy 1, Blast, Stasis Anomaly"),
    "Molecular Acid Heavy Bolter": ('36"', "5", "4", "Heavy 3, Fleshbane"),
    "Plasma-caster": ('12"', "4", "2", "Assault 2, Ignores Cover, Plasma Flame"),
    "Plasma Incinerator with Suspensor Web": ('18"', "4", "2", "Heavy D3+4, Ignores Cover, Plasma Flame"),
    "Needle Pistol": ('12"', "2", "5", "Pistol, Poisoned, Rending"),
    "Calibanite Charge-blade": ("-", "User +1", "-", "Rending"),
    "Death of Worlds": ("-", "6", "-", "Power Weapon, Two-Handed, Murderous Strike (5+)"),
    "The Lion Sword": ("-", "User +1", "-", "Power Weapon, Two-Handed, Master-crafted, Fleshbane, Lance"),
    "The Wolf Blade": ("-", "User +3", "-", "Power Weapon, Two-Handed, Shred"),
    "Fusil Actinaeus": ('18"', "7", "2", "Salvo 2/4, Twin-linked, Blind"),
}
MULTI = {
    "The Blade": {"The Blade (one-handed)": ("-", "User +1", "-", "Power Weapon, Master-crafted"),
                  "The Blade (two-handed)": ("-", "6", "-", "Power Weapon, Master-crafted, no bonus Attack for two "
                                                            "close-combat weapons")},
    "Missile Launcher with Suspensor Web, Rad Missiles and Stasis Missiles": {
        "Missile Launcher - Frag": ('48"', "4", "6", "Heavy 1, Blast"),
        "Missile Launcher - Krak": ('48"', "8", "3", "Heavy 1"),
        "Rad Missile": ('48"', "4", "3", "Heavy 1, Blast, Fleshbane, Rad-phage"),
        "Stasis Shell - Missile": ('48"', "4", "6", "Heavy 1, Blast, Stasis Anomaly")},
    "Grenade Launcher with Frag, Krak and Stasis Grenades": {
        "Grenade Launcher - Frag": ('24"', "3", "6", "Assault 1, Blast"),
        "Grenade Launcher - Krak": ('24"', "6", "4", "Assault 1"),
        "Stasis Shell - Grenade": ('24"', "2", "-", "Assault 1, Blast, Stasis Anomaly")},
}
WEAPON_RULES_ = {
    "Calibanite Warblade": ["Calibanite Warblade"], "Terranic Greatsword": ["Two-Handed", "Murderous Strike"],
    "Master-crafted Terranic Greatsword": ["Two-Handed", "Murderous Strike", "Master-Crafted"],
    "Plasma Repeater": ["Twin-Linked", "Gets Hot"], "Plasma Burner": ["Ignores Cover", "Plasma Flame"],
    "Stasis Shell - Grenade": ["Stasis Anomaly"], "Stasis Shell - Missile": ["Stasis Anomaly"],
    "Molecular Acid Heavy Bolter": ["Fleshbane", "Molecular Acid Shells"],
    "Plasma-caster": ["Ignores Cover", "Plasma Flame"],
    "Plasma Incinerator with Suspensor Web": ["Ignores Cover", "Plasma Flame", "Suspensor Web"],
    "Needle Pistol": ["Poisoned", "Rending"], "Calibanite Charge-blade": ["Rending", "Supercharged Blades"],
    "Death of Worlds": ["Two-Handed", "Murderous Strike (5+)"], "The Blade": ["The Blade", "Master-Crafted"],
    "The Lion Sword": ["Two-Handed", "Master-Crafted", "Fleshbane", "Lance"], "The Wolf Blade": ["Two-Handed", "Shred"],
    "Fusil Actinaeus": ["Twin-Linked", "Blind"],
    "Missile Launcher with Suspensor Web, Rad Missiles and Stasis Missiles": ["Suspensor Web", "Rad-phage", "Fleshbane",
                                                                              "Stasis Anomaly"],
    "Grenade Launcher with Frag, Krak and Stasis Grenades": ["Stasis Anomaly"],
}
WARGEAR_ = {
    "Teleportation Transponders": (
        "A model or unit with Teleportation Transponders may deploy using Deep Strike even if the mission would not normally "
        "permit it. An Independent Character intending to Deep Strike as part of a unit must purchase them separately. "
        "(Units entirely in Terminator Armour +15 points per unit; Independent Characters in Terminator Armour +10.)"),
    "Cytheron-pattern Aegis": (
        "4+ Invulnerable Save against shooting and 5+ in close combat. Occupies one hand: no bonus Attack for two "
        "close-combat weapons. If at least two models in the unit carry one, the unit may deploy its shields at the "
        "beginning of any Assault phase: until its next Movement phase the entire unit has a 4+ Invulnerable Save against "
        "shooting and 5+ in close combat, and engaged enemy models suffer -1 Initiative; models with deployed Aegises may "
        "not make close-combat attacks. The effect ends if fewer than two Aegis bearers remain."),
    "Shroud Bombs": ("Count as Defensive Grenades. An enemy non-vehicle unit attempting to charge the Cabal must first pass "
                     "a Leadership test or may not charge it that Assault phase (Night Vision and Daemons ignore this)."),
    "Enigmatus-pattern Jump Pack": (
        "The bearer is Jump Infantry. If the Cabal moved with its Jump Packs in its preceding Movement phase it has a 5+ "
        "Cover Save against shooting (unless better). When the Cabal charges after moving with its Jump Packs, the target "
        "may not Stand & Shoot (Overwatch established earlier is not prevented)."),
    "Armour of the Forest": ("Corswain's armour: 2+ Armour Save and 4+ Invulnerable Save as shown in his profile (no "
                             "further rules are given in the army book)."),
    "Regalia of the Shattered Sceptre": ("A suit of Cataphractii Terminator Armour; follows all normal rules and "
                                         "restrictions for that armour."),
    "Leonine Panoply": ("Counts as Primarch Armour. The first failed Invulnerable Save made by Lion El'Jonson during each "
                        "player turn may be re-rolled."),
    "Stasis Grenades": (
        "If Lion El'Jonson and a unit he has joined successfully charge an enemy unit, or are successfully charged, all "
        "enemy units engaged with his unit as a result of that charge are reduced to Initiative 1 until the end of the "
        "current player turn. Neither Assault nor Defensive Grenades."),
    "Molecular Acid Shells": RULES["Molecular Acid Shells"],
}


def register():
    # Rites of War that change the compulsory Troops (the base rites already handle their own units)
    for r in ["The Unbroken Vow"]:
        L2.TROOP_RITES["Legion Veteran Squad"].append(r)
        L2.TROOP_RITES["Legion Terminator Squad"].append(r)
    L2.TROOP_RITES["Legion Destroyer Squad"].append("The Eskaton Imperative")
    L2.TROOP_RITES["Legion Sky Hunter Jetbike Squadron"].append("The Seeker's Arrow")
    L2.NOT_LINE_UNDER["Legion Tactical Squad"] += ["The Unbroken Vow", "The Eskaton Imperative", "The Steel Fist",
                                                   "The Seeker's Arrow", "The Serpent's Bane"]
    L2.NOT_LINE_UNDER["Legion Assault Squad"] += ["The Unbroken Vow", "The Eskaton Imperative", "The Steel Fist",
                                                  "The Seeker's Arrow"]
    L2.NOT_LINE_UNDER["Legion Breacher Siege Squad"] += list(RITE_TEXT)
    register_data(rules=RULES, weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_, multi_profile=MULTI)
    for n, profs in MULTI.items():
        WEAPON_RULES.setdefault(n, WEAPON_RULES_.get(n, []))


# ---------------------------------------------------------------- local helpers
def is_char(e):
    ps = e.find("profiles")
    if ps is None:
        return False
    for p in ps:
        for c in p.iter("characteristic"):
            if c.get("name") == "Unit Type" and "Character" in (c.text or ""):
                return True
    return False


def link_cost(lk):
    cs = lk.find("costs")
    if cs is not None and len(cs):
        return float(cs[0].get("value"))
    return 0


def unique_entries(entries):
    seen, out = set(), []
    for e in entries:
        if id(e) not in seen:
            seen.add(id(e))
            out.append(e)
    return out


def owner_entry(parents, g):
    o = parents.get(g)
    while o is not None and o.tag != "selectionEntry":
        o = parents.get(o)
    return o


def copy_link_variant(lk, new_name, cost):
    """A link to new_name with the same constraints/modifiers (hide/forbid) as the base link lk."""
    nid = uid(lk.get("id"), "variant", new_name)
    cons, remap = [], {}
    for c in lk.findall("constraints/constraint"):
        c2 = copy.deepcopy(c)
        remap[c.get("id")] = uid(c.get("id"), new_name)
        c2.set("id", remap[c.get("id")])
        cons.append(c2)
    mods = []
    for m in lk.findall("modifiers/modifier"):
        m2 = copy.deepcopy(m)
        if m2.get("field") in remap:
            m2.set("field", remap[m2.get("field")])
        if m2.get("field") in remap.values() or m2.get("field") == "hidden":
            mods.append(m2)
    return link(nid, W(new_name), new_name, cost=int(cost) or None, mods=mods, constraints=cons)


def add_variants(entries, base, variants, chars_only=False, fixed_exchange=None):
    """Wherever `base` can be selected, also offer each variant [(name, extra_cost or callable(cost, is_default))].
    chars_only: only in groups belonging to a Character model / Independent Character.
    fixed_exchange: [(name, cost)] - Character models with `base` as fixed wargear get a 'Replace base' choice."""
    base_id = W(base)
    done = set()
    for r in unique_entries(entries):
        parents = {c: p for p in r.iter() for c in p}
        for g in list(r.iter("selectionEntryGroup")):
            links = g.find("entryLinks")
            if links is None:
                continue
            for lk in list(links):
                if lk.get("targetId") != base_id or id(lk) in done:
                    continue
                done.add(id(lk))
                if chars_only:
                    o = owner_entry(parents, g)
                    if o is None or not is_char(o):
                        continue
                is_default = g.get("defaultSelectionEntryId") == lk.get("id")
                existing = {x.get("targetId") for x in links}
                for new, extra in variants:
                    if W(new) in existing:
                        continue
                    c = extra(link_cost(lk), is_default) if callable(extra) else link_cost(lk) + extra
                    nl = copy_link_variant(lk, new, c)
                    if g.get("defaultSelectionEntryId") is not None:
                        nl.set("sortIndex", str(int(lk.get("sortIndex") or 1) + 100))
                    links.append(nl)
        # squad-level limits counting the base weapon also count the variants
        for m in list(r.iter("modifier")):
            reps = m.findall("repeats/repeat")
            if any(rp.get("childId") == base_id for rp in reps):
                parent = parents.get(m)
                if parent is None:
                    continue
                for new, _x in variants:
                    m2 = copy.deepcopy(m)
                    for rp in m2.iter("repeat"):
                        if rp.get("childId") == base_id:
                            rp.set("childId", W(new))
                    parent.append(m2)
        if fixed_exchange:
            for e in list(r.iter("selectionEntry")):
                if not is_char(e):
                    continue
                el_links = e.find("entryLinks")
                if el_links is None:
                    continue
                for lk in list(el_links):
                    if lk.get("targetId") == base_id:
                        el_links.remove(lk)
                        add_to(e, "selectionEntryGroups",
                               [slot(uid(e.get("id"), "exchange", base), f"Replace {base}", base, list(fixed_exchange))])
                        break


def ammo_upgrade(root, title, cost, item, weapons, per_model_cost=False):
    """'A model equipped with <weapon> may purchase <ammo>': one upgrade per such weapon in the unit."""
    ids = [W(w) for w in weapons if w in WEAPONS]
    eid = uid("da-ammo", root.get("id"), title)
    mx = uid(eid, "max")
    mods = [modifier("increment", mx, 1, repeats=[repeat(i, root.get("id"), 1)]) for i in ids]
    mods.append(modifier("set", "hidden", "true", groups=[all_of(*[cond(i, root.get("id"), "lessThan", 1)
                                                                    for i in ids])]))
    add_to(root, "selectionEntries", [entry(eid, title, cost=cost, mods=mods, constraints=[constraint(mx, "max", 0)],
                                            links=[gear(eid, item)])])


def has_link_to(root, ids):
    return any(lk.get("targetId") in ids for lk in root.iter("entryLink"))


def profile_types(root):
    out = []
    for p in root.iter("profile"):
        ut = None
        for c in p.iter("characteristic"):
            if c.get("name") == "Unit Type":
                ut = c.text
        out.append((p.get("typeName"), ut or ""))
    return out


def make_troops(unit, old_cat, conds_any, line=True):
    """Unit becomes a Troops choice (and compulsory-Troops eligible) while any of conds_any is true."""
    g = lambda: any_of(*conds_any)
    mods = [modifier("set-primary", "category", TROOPS, groups=[g()]),
            modifier("remove", "category", old_cat, groups=[g()])]
    if line:
        mods.append(modifier("add", "category", gs.CAT_LINE, groups=[g()]))
    add_mods(unit, mods)


def wing_id(unit_id, wing):
    return choice_id(unit_id, WING, wing)


def wing_group(unit_id, fixed=None):
    return required_choice(unit_id, WING, [(w, [w]) for w in WINGS], fixed=fixed)


def need_wing(unit, rite_name, wings):
    """Under the rite, the unit only counts for the compulsory Troops if it belongs to one of `wings`."""
    u = unit.get("id")
    add_mods(unit, [modifier("remove", "category", gs.CAT_LINE,
                             groups=[all_of(rite(rite_name), *[cond(wing_id(u, w), u, "lessThan", 1) for w in wings])])])


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


def transponders(key, cost, hide=None):
    e = option(key, "Teleportation Transponders", cost, hide=hide)
    return e


# ---------------------------------------------------------------- units
BLADE_OPTS = [("Terranic Greatsword", 10), ("Power Fist", 5)]
BOLTER_OPTS = [("Combi-Flamer", 10), ("Combi-Volkite Charger", 10), ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15),
               ("Plasma Pistol", 15), ("Cytheron-pattern Aegis", 10)]


def companions(key="Deathwing Companion Detachment", root=True, jump_char=None, ws_upgrade=False):
    name = "Deathwing Companion Detachment"
    u = uid("unit", key)
    cid, oid = uid("model", u, "Deathwing Companion"), uid("model", u, "Oathbearer")
    kit = ["Artificer Armour", "Calibanite Warblade", "Bolter", "Bolt Pistol", "Frag Grenades"]
    comp_prof = unit_profile(u, "Deathwing Companion", "Infantry", 5, 4, 4, 4, 1, 4, 2, 9, "2+")
    oath_prof = unit_profile(u, "Oathbearer", "Infantry (Character)", 5, 4, 4, 4, 2, 4, 2, 10, "2+/5+")
    oath = entry(oid, "Oathbearer", typ="model", cost=0,
                 constraints=[constraint(uid(oid, "min"), "min", 1), constraint(uid(oid, "max"), "max", 1)],
                 profiles=[oath_prof], links=[gear(oid, k) for k in kit + ["Refractor Field"]],
                 groups=[slot(oid, "Replace Calibanite Warblade", "Calibanite Warblade", BLADE_OPTS),
                         slot(oid, "Replace Bolter", "Bolter", BOLTER_OPTS)])
    comps = entry(cid, "Deathwing Companion", typ="model", cost=35,
                  constraints=[constraint(uid(cid, "min"), "min", 4), constraint(uid(cid, "max"), "max", 9)],
                  profiles=[comp_prof], links=[gear(cid, k) for k in kit])
    swaps = [model_swaps(u, "Deathwing Companions: replace Calibanite Warblade (any number)", u, [cid], BLADE_OPTS),
             model_swaps(u, "Deathwing Companions: replace Bolter (any number)", u, [cid], BOLTER_OPTS)]
    ents = [oath, comps, per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]),
            per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])]
    block = []
    if jump_char:
        jp_id = uid("squadwide", u, "Jump Packs (entire squad)")
        jp = per_model(u, "Jump Packs (entire squad)", 15, u, ["Jump Pack"])
        add_mods(jp, [modifier("set", "hidden", "true", conds=[lacks(W("Jump Pack"), jump_char)]),
                      modifier("set", uid(jp_id, "max"), 0, conds=[lacks(W("Jump Pack"), jump_char)])])
        ents.append(jp)
        block = [has(jp_id, u)]
    if ws_upgrade:
        upg = per_model(u, "Seneschal of the First Legion: +1 Weapon Skill (entire squad)", 5, u, [])
        uid_upg = uid("squadwide", u, "Seneschal of the First Legion: +1 Weapon Skill (entire squad)")
        ents.append(upg)
        for p in (comp_prof, oath_prof):
            p.insert(0, wrap("modifiers", [modifier("set", gs.char_id("Unit", "WS"), 6,
                                                    conds=[cond(uid_upg, u, "atLeast", 1)])]))
    tr = transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod", "Anvillus Pattern Dreadclaw Drop Pod",
                           "Land Raider Phobos", "Land Raider Proteus"], block_if=block)
    return entry(u, name, typ="unit", cost=175 - 4 * 35, cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links([LR, "Deathwing", "Stubborn", "Death-sworn Companions", "Deathwing Retinue",
                                        "Mastery of the Blade"], key=u),
                 entries=ents, groups=[wing_group(u, "Deathwing"), *swaps, tr])


TERM_BLADE = [("Terranic Greatsword", 10), ("Power Fist", 5), ("Thunder Hammer", 10)]
TERM_COMBI = [("Combi-Grenade Launcher", 10), ("Combi-Flamer", 10), ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15),
              ("Combi-Volkite Charger", 10)]
PATTERNS = ["Tartaros Terminator Armour", "Cataphractii Terminator Armour"]


def pattern_choice(u, fixed=None):
    g = required_choice(u, "Terminator Armour Pattern (entire squad)", [(p, []) for p in PATTERNS], fixed=fixed)
    for e in g.find("selectionEntries"):
        add_to(e, "entryLinks", [gear(e.get("id"), e.get("name"))])
    return g


def term_companions(key="Deathwing Terminator Companions", root=True, fixed_pattern=None):
    name = "Deathwing Terminator Companions"
    u = uid("unit", key)
    tid, oid = uid("model", u, "Deathwing Terminator Companion"), uid("model", u, "Terminator Oathbearer")
    pair = entry(uid(oid, "pair"), "Pair of Lightning Claws (replaces both)", cost=15,
                 links=[gear(uid(oid, "pair"), "Pair of Lightning Claws")])
    oath = entry(oid, "Terminator Oathbearer", typ="model", cost=0,
                 constraints=[constraint(uid(oid, "min"), "min", 1), constraint(uid(oid, "max"), "max", 1)],
                 profiles=[unit_profile(u, "Terminator Oathbearer", "Infantry (Character)", 5, 4, 4, 4, 2, 4, 2, 10,
                                        "2+")],
                 groups=[slot(oid, "Replace Combi-bolter", "Combi-Bolter", TERM_COMBI + [(pair, None)]),
                         slot(oid, "Replace Calibanite Warblade", "Calibanite Warblade", TERM_BLADE,
                              zero_if=[has(uid(oid, "pair"), "parent")]),
                         take(oid, "Oathbearer Wargear", [("Grenade Harness", 10)])])
    terms = entry(tid, "Deathwing Terminator Companion", typ="model", cost=40,
                  constraints=[constraint(uid(tid, "min"), "min", 4), constraint(uid(tid, "max"), "max", 9)],
                  profiles=[unit_profile(u, "Terminator Companion", "Infantry", 5, 4, 4, 4, 1, 4, 2, 9, "2+")],
                  links=[gear(tid, "Combi-Bolter"), gear(tid, "Calibanite Warblade")])
    pid, pair_all = model_pair_claws(u, "Pair of Lightning Claws (replaces Combi-bolter and Calibanite Warblade)", u,
                                     [tid], 15)
    swaps = [model_swaps(u, "Terminator Companions: replace Combi-bolter (any number)", u, [tid], TERM_COMBI,
                         entries=[pair_all]),
             model_swaps(u, "Terminator Companions: replace Calibanite Warblade (any number)", u, [tid], TERM_BLADE,
                         minus=[pid])]
    tp = option(u, "Teleportation Transponders (entire squad)", 15, item="Teleportation Transponders")
    tr = transports(u, u, ["Land Raider Phobos", "Land Raider Proteus", "Anvillus Pattern Dreadclaw Drop Pod",
                           "Legion Spartan Assault Tank"], orbital=False)
    return entry(u, name, typ="unit", cost=225 - 4 * 40, cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links([LR, "Deathwing", "Stubborn", "Death-sworn Companions",
                                        "Deathwing Retinue (Terminators)", "Mastery of the Blade"], key=u),
                 entries=[oath, terms, tp],
                 groups=[wing_group(u, "Deathwing"), pattern_choice(u, fixed_pattern), *swaps, tr])


ORDERS = ["Augurs of Weakness", "Icons of Resolve", "Guardians of Sanctity", "Slayers of Kings", "Hunters of Beasts",
          "Reapers of Hosts", "Breakers of Witches"]


def cenobium(key="Inner Circle Knights Cenobium", root=True):
    name = "Inner Circle Knights Cenobium"
    u = uid("unit", key)
    kid, pid = uid("model", u, "Knight Cenobite"), uid("model", u, "Order Preceptor")
    kit = ["Cataphractii Terminator Armour", "Terranic Greatsword", "Plasma-caster"]
    prec = entry(pid, "Order Preceptor", typ="model", cost=0,
                 constraints=[constraint(uid(pid, "min"), "min", 1), constraint(uid(pid, "max"), "max", 1)],
                 profiles=[unit_profile(u, "Order Preceptor", "Infantry (Character)", 6, 4, 4, 4, 1, 4, 2, 10, "2+")],
                 links=[gear(pid, k) for k in kit],
                 groups=[slot(pid, "Replace Terranic Greatsword", "Terranic Greatsword", [("Thunder Hammer", 0)]),
                         take(pid, "Preceptor Wargear", [("Grenade Harness", 10), ("Digital Weapons", 10)])])
    knights = entry(kid, "Knight Cenobite", typ="model", cost=45,
                    constraints=[constraint(uid(kid, "min"), "min", 4), constraint(uid(kid, "max"), "max", 9)],
                    profiles=[unit_profile(u, "Knight Cenobite", "Infantry", 5, 4, 4, 4, 1, 4, 2, 9, "2+")],
                    links=[gear(kid, k) for k in kit])
    swaps = model_swaps(u, "Knights Cenobite: replace Terranic Greatsword (any number)", u, [kid],
                        [("Thunder Hammer", 0)])
    gid = uid("grp", u, "transport")
    big5 = [cond("model", u, "greaterThan", 5)]
    tr_links = []
    for n in ["Land Raider Phobos", "Land Raider Proteus"]:
        lid = uid("link", gid, n)
        tr_links.append(link(lid, T[n], n + " (unit of five models)",
                             mods=[modifier("set", "hidden", "true", conds=big5),
                                   modifier("set", uid(lid, "max"), 0, conds=big5)],
                             constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    tr_links.append(link(uid("link", gid, "spartan"), T["Legion Spartan Assault Tank"], "Legion Spartan Assault Tank"))
    tr = group(gid, "Dedicated Transport", links=tr_links, constraints=[constraint(uid(gid, "max"), "max", 1,
                                                                                    auto=True)])
    tp = option(u, "Teleportation Transponders (entire squad)", 15, item="Teleportation Transponders")
    orders = required_choice(u, "Order Exemplars", [(o, [o]) for o in ORDERS])
    return entry(u, name, typ="unit", cost=275 - 4 * 45, cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links([LR, "Stubborn", "Adamantium Will", "Inner Circle", "Order Exemplars",
                                        "Uncompromising Discipline", "Mastery of the Blade"], key=u),
                 entries=[prec, knights, tp], groups=[orders, swaps, tr])


INTEREMPTORS = uid("unit", "Dreadwing Interemptor Squad")


def interemptors(key="Dreadwing Interemptor Squad", root=True):
    name = "Dreadwing Interemptor Squad"
    u = uid("unit", key)
    iid, pid = uid("model", u, "Interemptor"), uid("model", u, "Interemptor Praefectus")
    kit = ["Power Armour", "Plasma Burner", "Chainsword", "Frag Grenades", "Rad Grenades"]
    pref = entry(pid, "Interemptor Praefectus", typ="model", cost=0,
                 constraints=[constraint(uid(pid, "min"), "min", 1), constraint(uid(pid, "max"), "max", 1)],
                 profiles=[unit_profile(u, "Interemptor Praefectus", "Infantry (Character)", 4, 4, 4, 4, 1, 4, 2, 10,
                                        "3+")],
                 links=[gear(pid, k) for k in kit],
                 groups=[take(pid, "Praefectus Wargear", [("Phosphex Bomb", 10, 3)])])
    ints = entry(iid, "Interemptor", typ="model", cost=25,
                 constraints=[constraint(uid(iid, "min"), "min", 4), constraint(uid(iid, "max"), "max", 14)],
                 profiles=[unit_profile(u, "Interemptor", "Infantry", 4, 4, 4, 4, 1, 4, 1, 9, "3+")],
                 links=[gear(iid, k) for k in kit])
    heavy, _ = pool(u, "Heavy Weapons (1 per 5 models, replace Plasma Burner)", u, [
        ("Missile Launcher with Suspensor Web, Rad Missiles and Stasis Missiles", 15),
        ("Plasma Incinerator with Suspensor Web", 15)], 0, every=5)
    mods = []
    if root:
        mods = [modifier("set-primary", "category", TROOPS, conds=[rite("The Eskaton Imperative")]),
                modifier("remove", "category", ELITES, conds=[rite("The Eskaton Imperative")]),
                modifier("add", "category", gs.CAT_LINE, conds=[rite("The Eskaton Imperative")])]
    return entry(u, name, typ="unit", cost=160 - 4 * 25, mods=mods, cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links([LR, "Dreadwing", "Stubborn", "Bitter Duty", "Plasma Flame",
                                        "Mastery of the Blade"], key=u),
                 entries=[pref, ints, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
                 groups=[wing_group(u, "Dreadwing"), heavy,
                         L.one_each(u, "Squad Equipment", [("Legion Vexilla", 10), ("Nuncio Vox", 10)]),
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos",
                                           "Land Raider Proteus"], max_models=10)])


def enigmatus():
    name = "Firewing Enigmatus Cabal"
    u = uid("unit", name)
    mid = uid("model", u, "Firewing Enigmatus")
    m = entry(mid, "Firewing Enigmatus", typ="model", cost=0,
              constraints=[constraint(uid(mid, "min"), "min", 3), constraint(uid(mid, "max"), "max", 3)],
              profiles=[unit_profile(u, "Firewing Enigmatus", "Jump Infantry (Character)", 5, 4, 4, 4, 2, 5, 3, 10,
                                     "3+")],
              links=[gear(mid, k) for k in ["Power Armour", "Calibanite Charge-blade", "Needle Pistol", "Shroud Bombs",
                                            "Enigmatus-pattern Jump Pack"]])
    gl, _ = pool(u, "Grenade Launcher (one model)", u, [("Grenade Launcher with Frag, Krak and Stasis Grenades", 20)], 1)
    return entry(u, name, typ="unit", cost=150, cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links([LR, "Firewing", "Scout", "Hatred (Characters)", "Supercharged Blades",
                                        "Mastery of the Blade"], key=u),
                 entries=[m], groups=[wing_group(u, "Firewing"), gl])


# ---------------------------------------------------------------- characters
def krak(u):
    return take(u, "Wargear", [("Krak Grenades", 2)])


def characters():
    out = []
    # Corswain
    cor = uid("unit", "Corswain, Seneschal of the First Legion")
    out.append(named_character(
        LR, "Corswain, Seneschal of the First Legion", 200, (7, 5, 4, 4, 3, 5, 4, 10, "2+/4+"),
        ["Armour of the Forest", "Iron Halo", "Bolt Pistol", "The Blade", "Frag Grenades"],
        ["Deathwing", "Stubborn", "Paladin of Glory", "Seneschal of the First Legion", "Mastery of the Blade"],
        retinue=retinue_links("corswain", [companions("corswain-companions", root=False, ws_upgrade=True)]),
        extra_groups=[wing_group(cor, "Deathwing"), krak(cor)], profile_name="Corswain"))
    # Marduk Sedras
    sed = uid("unit", "Marduk Sedras, Lord of the Twenty-Third Order")
    out.append(named_character(
        LR, "Marduk Sedras, Lord of the Twenty-Third Order", 225, (6, 5, 4, 4, 3, 4, 4, 10, "2+/4+"),
        ["Regalia of the Shattered Sceptre", "Cataphractii Terminator Armour", "Combi-Volkite Charger",
         "Death of Worlds", "Grenade Harness"],
        ["Dreadwing", "Stubborn", "Ancient of War", "Eskaton", "Siege Specialists", "Cenobium Retinue",
         "Mastery of the Blade"],
        retinue=retinue_links("sedras", [cenobium("sedras-cenobium", root=False)]),
        extra_groups=[wing_group(sed, "Dreadwing")],
        extra_entries=[option(sed, "Teleportation Transponders", 10)], profile_name="Marduk Sedras"))
    # Farith Redloss
    red = uid("unit", "Farith Redloss")
    e = named_character(
        LR, "Farith Redloss", 185, (6, 5, 4, 4, 3, 5, 3, 10, "2+/4+"),
        ["Artificer Armour", "Iron Halo", "Terranic Greatsword", "Rad Grenades", "Frag Grenades"],
        ["Dreadwing", "Stubborn", "Voted-Lieutenant of the Dreadwing", "Extermination Protocol", "Mastery of the Blade"],
        retinue=retinue_links("redloss", [interemptors("redloss-interemptors", root=False)]),
        extra_groups=[wing_group(red, "Dreadwing"), krak(red),
                      slot(red, "Replace Plasma Pistol", "Plasma Pistol", [("Calibanite Plasma Pistol", 0)])])
    pb = uid("link", red, "phosphex")
    add_to(e, "entryLinks", [link(pb, W("Phosphex Bomb"), "Phosphex Bomb (two)",
                                  constraints=[constraint(uid(pb, "min"), "min", 2),
                                               constraint(uid(pb, "max"), "max", 2)])])
    out.append(e)
    # Holguin
    hol = uid("unit", "Holguin")
    out.append(named_character(
        LR, "Holguin", 190, (6, 5, 4, 4, 3, 4, 3, 10, "2+/4+"),
        ["Cataphractii Terminator Armour", "Combi-Bolter", "Master-crafted Terranic Greatsword", "Grenade Harness"],
        ["Deathwing", "Stubborn", "Voted-Lieutenant of the Deathwing", "Unbroken Line", "Mastery of the Blade"],
        retinue=retinue_links("holguin", [term_companions("holguin-termcomp", root=False,
                                                          fixed_pattern="Cataphractii Terminator Armour")]),
        extra_groups=[wing_group(hol, "Deathwing")],
        extra_entries=[option(hol, "Teleportation Transponders", 10)]))
    return out


LION = uid("unit", "Lion El'Jonson, The First")


def lion():
    ret = primarch_retinue("lion", extra=[companions("lion-companions", root=False),
                                          term_companions("lion-termcomp", root=False)])
    return primarch(LR, "Lion El'Jonson, The First", 550, (9, 6, 6, 6, 6, 7, 6, 10, "1+/4++"),
                    ["Leonine Panoply", "Fusil Actinaeus", "Stasis Grenades", "Frag Grenades"],
                    ["Primarch Armour", "An Absolute Focus", "The Point of the Blade", "The Lion's Choler",
                     "Knight of Knights", "Primarch Retinue (Lion El'Jonson)", "Mastery of the Blade"],
                    retinue=ret, loyalist=True, profile_name="Lion El'Jonson",
                    extra_groups=[slot(LION, "The Lion Sword or the Wolf Blade", "The Lion Sword",
                                       [("The Wolf Blade", 0)])])


# ---------------------------------------------------------------- changes to existing entries
def storm_centurion(ctx, squad):
    """Masters of the Storm of War: a 20-model Tactical/Assault Squad may include one Legion Centurion."""
    sid = squad.get("id")
    c = clone(ctx.unit("Legion Centurion"), "da-storm-" + sid,
              new_name="Legion Centurion (Masters of the Storm of War)")
    c.set("type", "model")
    for g in c.iter("selectionEntryGroup"):
        if g.get("name") in ("Legion Consul (max one)", "Retinue (no Force Organisation slot)"):
            g.set("hidden", "true")
            for k in g.findall("constraints/constraint"):
                if k.get("type") == "max":
                    k.set("value", "0")
    for x in c.iter("selectionEntry"):
        if x.get("name", "").startswith("Upgrade Bike to Jetbike"):
            x.set("hidden", "true")
            for k in x.findall("constraints/constraint"):
                k.set("value", "0")
    cid = c.get("id")
    mx = uid(cid, "storm-max")
    off = [any_of(cond(rite_id("The Storm of War"), "force", "lessThan", 1), cond("model", sid, "lessThan", 20))]
    add_to(c, "constraints", [constraint(mx, "max", 1)])
    add_mods(c, [modifier("set", "hidden", "true", groups=[off[0]]),
                 modifier("set", mx, 0, groups=[any_of(cond(rite_id("The Storm of War"), "force", "lessThan", 1),
                                                       cond("model", sid, "lessThan", 20))])])
    add_to(c, "selectionEntryGroups", [wing_group(cid, "Stormwing")])
    add_to(c, "rules", [rule(uid(cid, "storm-rule"), "Masters of the Storm of War",
                             "Does not occupy an HQ selection, is part of the squad and may not voluntarily leave it, may "
                             "not select a Consul upgrade, may not be the army's Warlord and belongs to the Stormwing.")])
    add_entry(squad, c)


def ic_terranic(ctx):
    for key, n in [("praetor", "Legion Praetor"), ("centurion", "Legion Centurion")]:
        e = ctx.unit(n)
        for g in e.iter("selectionEntryGroup"):
            if g.get("id") in (uid("slot", key, "Bolt Pistol"), uid("slot", key, "Chainsword")):
                lid = uid("link", g.get("id"), "Terranic Greatsword")
                g.find("entryLinks").append(link(lid, W("Terranic Greatsword"), "Terranic Greatsword", cost=35,
                                                 constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
        add_mods(e, [modifier("add", "error", "A Terranic Greatsword is Two-Handed: a model may only carry one.",
                              conds=[cond(W("Terranic Greatsword"), e.get("id"), "greaterThan", 1)])])


def steel_fist_transports(unit):
    """Armoured Assault: Ironwing Infantry units may take a Land Raider (<=10 models) or Spartan (11-20 models)."""
    u = unit.get("id")
    gid = uid("grp", u, "steel-fist")
    off = lambda: any_of(cond(rite_id("The Steel Fist"), "force", "lessThan", 1), cond(wing_id(u, "Ironwing"), u,
                                                                                     "lessThan", 1))
    links = []
    for n, bad in [("Land Raider Phobos", [cond("model", u, "greaterThan", 10)]),
                   ("Land Raider Proteus", [cond("model", u, "greaterThan", 10)]),
                   ("Legion Spartan Assault Tank", [cond("model", u, "atMost", 10), cond("model", u, "greaterThan", 20)])]:
        lid = uid("link", gid, n)
        links.append(link(lid, T[n], n, mods=[modifier("set", "hidden", "true", groups=[any_of(*bad)]),
                                              modifier("set", uid(lid, "max"), 0, groups=[any_of(*copy.deepcopy(bad))])],
                          constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    add_group(unit, group(gid, "Dedicated Transport (The Steel Fist, Ironwing)", links=links,
                          mods=[modifier("set", "hidden", "true", groups=[off()]),
                                modifier("set", uid(gid, "max"), 0, groups=[off()])],
                          constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)]))
    add_mods(unit, [modifier("add", "error", "A unit may only have one Dedicated Transport.",
                             conds=[cond(gs.CAT_TRANSPORT, u, "greaterThan", 1)])])


def is_infantry_unit(e):
    types = [ut for t, ut in profile_types(e) if t == "Unit"]
    return bool(types) and all(ut.startswith("Infantry") for ut in types)


def extend(ctx):
    ctx.legion_rules([LR, "Mastery of the Blade", "The Hexagrammaton"] + WINGS)
    praetor, centurion = ctx.unit("Legion Praetor"), ctx.unit("Legion Centurion")

    # ---- Armoury: Terranic Greatsword, Teleportation Transponders
    ic_terranic(ctx)
    for key, e in [("praetor", praetor), ("centurion", centurion)]:
        tp = option(key + "-da", "Teleportation Transponders", 10, hide=[L.no_tda(e.get("id"))])
        add_entry(e, tp)
    add_entry(ctx.unit("Legion Terminator Squad"),
              option("da-termsquad", "Teleportation Transponders (entire squad)", 15, item="Teleportation Transponders"))
    for r in ctx.retinues("Legion Terminator Command Squad"):
        add_entry(r, option(r.get("id") + "da", "Teleportation Transponders (entire squad)", 15,
                            item="Teleportation Transponders"))

    # ---- The Storm of War: Centurions inside 20-model Tactical / Assault Squads
    tac, ass = ctx.unit("Legion Tactical Squad"), ctx.unit("Legion Assault Squad")
    for sq in (tac, ass):
        storm_centurion(ctx, sq)

    # ---- new units
    new_units = [companions(), term_companions(), cenobium(), interemptors(), enigmatus()]
    ctx.add_units(*new_units)

    # ---- Deathwing retinues for the Praetor / Centurion
    pr_comp = companions("praetor-da-companions", root=False, jump_char=praetor.get("id"))
    pr_term = term_companions("praetor-da-termcomp", root=False)
    ce_term = term_companions("centurion-da-termcomp", root=False)
    for char, ents in [(praetor, [pr_comp, pr_term]), (centurion, [ce_term])]:
        cid = char.get("id")
        g = find_group(char, "Retinue (no Force Organisation slot)")
        for r in ents:
            L2.RETINUE_SHARED.append(r)
            mods = []
            if r.get("name") == "Deathwing Terminator Companions":
                no_pat = all_of(*[lacks(W(p), cid) for p in PATTERNS])
                mods = [modifier("set", "hidden", "true", groups=[no_pat])]
                ru = r.get("id")
                for p in PATTERNS:
                    add_mods(char, [modifier("add", "error", "Deathwing Terminator Companions must wear the same pattern "
                                                             "of Terminator Armour as their Character.",
                                             conds=[cond(choice_id(ru, "Terminator Armour Pattern (entire squad)", p),
                                                         cid, "atLeast", 1),
                                                    cond(W(p), cid, "lessThan", 2)])])
            g.find("entryLinks").append(link(uid("link", g.get("id"), r.get("id")), r.get("id"), r.get("name"),
                                             mods=mods))

    # ---- characters and the Primarch
    chars = characters()
    ctx.add_units(*chars, lion())

    # ---- Rites of War
    for n, t in RITE_TEXT.items():
        errors = []
        if n == "The Seeker's Arrow":
            slow = []
            for e in unique_entries(ctx.units + ctx.shared):
                pts = profile_types(e)
                veh = [ut for tn, ut in pts if tn in ("Vehicle", "Walker")]
                if veh and any(tn == "Walker" or ("Fast" not in ut and "Skimmer" not in ut) for tn, ut in pts
                               if tn in ("Vehicle", "Walker")):
                    slow.append(cond(e.get("id"), "force", "atLeast", 1))
            errors.append(("the army may not include a Vehicle unless it is Fast and/or a Skimmer.",
                           [any_of(*slow)]))
        rid = ctx.add_rite(n, t, limit_fa=(n == "The Steel Fist"), limit_hs=(n == "The Seeker's Arrow"))
        if errors:
            rites = ctx.unit("Rite of War")
            for txt, grps in errors:
                add_mods(rites, [modifier("add", "error", f"{n}: {txt}", conds=[cond(rid, "self", "atLeast", 1)],
                                          groups=grps)])

    # Storm of War: compulsory Troops = Stormwing Tactical / Assault Squads of 20 models
    for sq in (tac, ass):
        need_wing(sq, "The Storm of War", ["Stormwing"])
        add_mods(sq, [modifier("remove", "category", gs.CAT_LINE,
                               conds=[rite("The Storm of War"), cond("model", sq.get("id"), "lessThan", 20)])])
    # Unbroken Vow: Deathwing Veterans / Terminators
    for n in ["Legion Veteran Squad", "Legion Terminator Squad"]:
        need_wing(ctx.unit(n), "The Unbroken Vow", ["Deathwing"])
    # Eskaton: Dreadwing Destroyers (Interemptors are always Dreadwing)
    need_wing(ctx.unit("Legion Destroyer Squad"), "The Eskaton Imperative", ["Dreadwing"])
    # Steel Fist: Predators as Troops (no 0-2 limit), Ironwing only
    pred = ctx.unit("Legion Predator Strike Squadron")
    tog = find_entry(pred, "Selected as Troops (Armoured Breakthrough)")
    tid = tog.get("id")
    old = tog.find("modifiers")
    tog.remove(old)
    neither = lambda: all_of(cond(rite_id("Armoured Breakthrough"), "force", "lessThan", 1),
                             cond(rite_id("The Steel Fist"), "force", "lessThan", 1))
    add_mods(tog, [modifier("set", "hidden", "true", groups=[neither()]),
                   modifier("set", uid(tid, "max"), 0, groups=[neither()]),
                   modifier("increment", uid(tid, "roster"), 99, conds=[rite("The Steel Fist")]),
                   modifier("set", "name", "Selected as Troops (The Steel Fist)", conds=[rite("The Steel Fist")])])
    need_wing(pred, "The Steel Fist", ["Ironwing"])
    # Seeker's Arrow: Ravenwing Bikes / Sky Hunters
    bikes = ctx.unit("Legion Bike Squadron")
    make_troops(bikes, FA, [rite("The Seeker's Arrow")])
    for b in (bikes, ctx.unit("Legion Sky Hunter Jetbike Squadron")):
        need_wing(b, "The Seeker's Arrow", ["Ravenwing"])
    # Serpent's Bane: Firewing Seekers / Assault Squads
    seekers = ctx.unit("Legion Seeker Squad")
    make_troops(seekers, FA, [rite("The Serpent's Bane")])
    for s in (seekers, ass):
        need_wing(s, "The Serpent's Bane", ["Firewing"])

    # ---- Armoury: Calibanite Warblade, Ancient Plasma Weaponry, Stasis / Molecular Acid shells
    everything = unique_entries(ctx.all_entries())
    add_variants(everything, "Power Weapon", [("Calibanite Warblade", 10)], chars_only=True,
                 fixed_exchange=[("Calibanite Warblade", 10)])
    add_variants(everything, "Plasma Pistol", [("Calibanite Plasma Pistol", 0)])
    add_variants(everything, "Plasma Gun", [("Calibanite Plasma Gun", 0), ("Plasma Repeater", 10),
                                            ("Plasma Burner", 5)])
    add_variants(everything, "Plasma Cannon", [("Calibanite Plasma Cannon", 0)])
    ml = ["Missile Launcher", "Missile Launcher with Suspensor Web", "Missile Launcher with Suspensor Web and Rad Missiles",
          "Twin-linked Missile Launcher"]
    gl = ["Combi-Grenade Launcher"]
    hb = ["Heavy Bolter", "Twin-linked Heavy Bolter", "Heavy Bolter with Suspensor Web",
          "Heavy Bolter with Suspensor and Hellfire Rounds"]
    for e in everything:
        if e.get("name") in ("Legion", "Allegiance", "Rite of War"):
            continue
        if has_link_to(e, {W(x) for x in ml if x in WEAPONS}):
            ammo_upgrade(e, "Stasis Shells (per Missile Launcher)", 5, "Stasis Shell - Missile", ml)
        if has_link_to(e, {W(x) for x in gl}):
            ammo_upgrade(e, "Stasis Shells (per Grenade Launcher)", 5, "Stasis Shell - Grenade", gl)
        pts = profile_types(e)
        vehicle = any(t == "Vehicle" for t, _ in pts) and not any(t == "Walker" for t, _ in pts)
        if not vehicle and has_link_to(e, {W(x) for x in hb}):
            ammo_upgrade(e, "Molecular Acid Shells (per Heavy Bolter)", 7, "Molecular Acid Heavy Bolter", hb)

    # ---- The Hexagrammaton: every Dark Angels unit chooses a Wing (Primarch and Inner Circle excepted)
    skip = {LION, uid("unit", "Inner Circle Knights Cenobium")}
    for e in unique_entries(legion_units(ctx) + ctx.retinues()):
        if e.get("id") in skip or e.get("name") == "Inner Circle Knights Cenobium":
            continue
        if any(g.get("name") == WING for g in e.findall("selectionEntryGroups/selectionEntryGroup")):
            continue
        add_group(e, wing_group(e.get("id")))

    # ---- The Steel Fist transports for Ironwing Infantry units (only units that can choose a Wing; the Knights
    # Cenobium have no Wing and so can never be Ironwing)
    for e in unique_entries(legion_units(ctx) + ctx.retinues()):
        wg = [g for g in e.findall("selectionEntryGroups/selectionEntryGroup") if g.get("name") == WING]
        fixed = wg[0].get("defaultSelectionEntryId") if wg else None
        if fixed is not None and fixed != wing_id(e.get("id"), "Ironwing"):
            continue      # predetermined Wing other than the Ironwing
        if (wg and find_group(e, "Dedicated Transport") is not None and is_infantry_unit(e)
                and e.get("id") != LION):
            steel_fist_transports(e)
    for e in unique_entries(ctx.all_entries()):
        dedupe_kit(e)
