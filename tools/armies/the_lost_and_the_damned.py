"""The Lost and the Damned - Shattered Legions, Blackshields and Agents of the Sigillite.

Source: the author's army book "The Lost and the Damned" (/home/claude/src/The_Lost_and_the_Damned.txt).

The book holds three parts:

* Shattered Legions - a theme for the Legiones Astartes Army List that mixes two or three Legions. It needs the
  units and rules of several Legions at once, so it can not be built in this catalogue; its rules are included as
  rule text (see the questions file).
* Blackshields - a theme for the Legiones Astartes Army List. The standard Force Organisation Chart of this
  catalogue is a Blackshields force: the generic Legiones Astartes Army List (no Praetor, no Legion-specific
  units) plus the Reaver Lord, Blackshield Marauder Squad, Chymeriae Squad, the Oaths of Moment and the
  Blackshield Armoury and Weapons.
* Agents of the Sigillite - a special Loyalist Allied Detachment with its own Force Organisation
  ("Agents of the Sigillite Allied Detachment", defined in this catalogue).
"""
import copy

from armies.common import *  # noqa: F401,F403
from bsx import el, wrap

ARMY = "The Lost and the Damned"

STD_FORCE = uid("force", "standard")

# ----------------------------------------------------------------------------------------------------- rules
RULES = {
    # ------------------------------------------------------------------ Shattered Legions (text only)
    "Shattered Legions": (
        "A Shattered Legions force is not a separate army list: it modifies a force chosen from the Legiones Astartes "
        "Army List. Before selecting the army, declare the Shattered Legions Theme and whether the force is Loyalist or "
        "Traitor. Choose two or three Legions; one is nominated as the Warlord's Legion and the Warlord must belong to "
        "it. Every unit must be assigned to one of the chosen Legions (record it on the roster); a unit may only belong "
        "to one Legion and models of different Legions may not be mixed in one unit. Vehicles and other units without "
        "Legion-specific rules must still be assigned to a Legion.\n"
        "LEGION UNITS AND EQUIPMENT: units are selected normally from the Legiones Astartes Army List, keep the special "
        "rules of their assigned Legion and may purchase the Legion-specific wargear of that Legion. Legion-specific "
        "rules only affect models of that Legion unless stated otherwise. An Independent Character may join a unit of "
        "another Legion of the force, but neither gains the other's Legion-specific rules, wargear or abilities. "
        "Assigning a vehicle to a Legion does not automatically grant it Legion-specific special rules.\n"
        "DEDICATED TRANSPORTS: a Dedicated Transport belongs to the same Legion as the unit it was purchased for.\n"
        "LEGION-SPECIFIC UNITS: each Legion-specific unit entry is limited to 0-1 per army, and requires at least one "
        "Praetor, Centurion or named HQ Character of the same Legion. Legion-specific wargear needs no such Character."),
    "The Whole is Greater than the Sum": (
        "Until the army's Warlord is slain, all units of the Shattered Legions force operate normally as part of the "
        "same friendly army. If the Warlord is slain, for the remainder of the battle only units of the Warlord's Legion "
        "count as Scoring units; all other units otherwise continue to fight normally."),
    "Shattered Legions Restrictions": (
        "A Shattered Legions force: must contain units from at least two and no more than three Legions; must nominate "
        "one of them as the Warlord's Legion; may include generic and Legion-specific units as described; may not "
        "include more than one of each Legion-specific unit entry; may not include a Primarch; may not include "
        "Blackshields; may only include Characters and units appropriate to its declared Allegiance; may not mix models "
        "of different Legions in one unit; may not use an Allied Detachment to include an additional Legiones Astartes "
        "Legion beyond those selected for the Shattered Legions force."),
    # ------------------------------------------------------------------ Blackshields
    "Legiones Astartes (Blackshields)": (
        "All units of a Blackshields force are Legiones Astartes (Blackshields). Blackshields do not benefit from the "
        "special rules of any of the eighteen Space Marine Legions, regardless of the Legion their warriors came from. "
        "A Blackshields force may not include Legion-specific units, Legion-specific named Characters or Primarchs "
        "unless this supplement specifically says otherwise."),
    "Blackshields Theme": (
        "Declare the Blackshields Theme before selecting the army. The army is selected normally from the Legiones "
        "Astartes Army List with the normal Force Organisation Chart; only units which are not restricted to a "
        "particular Legion may be selected.\n"
        "BLACKSHIELD COMMANDERS: a Blackshields force may not include Praetors. It may select a Reaver Lord as its "
        "senior commander. Centurions, Librarians and other generic Legiones Astartes Characters may still be selected "
        "unless prohibited by the chosen Oath of Moment.\n"
        "ALLEGIANCE: declare the force Loyalist or Traitor for army selection, scenarios and Allied Detachments.\n"
        "WARGEAR: models have access to the normal Space Marine Armoury and the Blackshield-specific wargear of this "
        "supplement, but not to Legion-specific wargear of any of the eighteen Legions unless an Oath of Moment or "
        "another rule of this supplement permits it.\n"
        "OATHS OF MOMENT: the force must select exactly one Oath of Moment, which applies to the entire force.\n"
        "RITES OF WAR: a Blackshields force may not use a Rite of War (author's ruling)."),
    "Blackshield Armoury": (
        "Blackshield Characters with access to the Space Marine Armoury may also select equipment from the Blackshield "
        "Armoury, in addition to the normal Space Marine Armoury. Items listed as Xenos Wargear may only be selected in a "
        "force whose Oath of Moment grants access to Xenos Wargear. Unless stated otherwise, no model may select the "
        "same item more than once."),
    "Blackshield Weapons": (
        "Any Blackshield Character, Veteran Sergeant or other model with access to the Space Marine Armoury may select "
        "Blackshield Weapons, following each weapon's replacement restrictions; this does not allow a model to exceed "
        "the normal number of weapons it may carry. Ordinary models may only take a Blackshield Weapon where their unit "
        "entry or the weapon permits it.\n"
        "Categories: a Sidearm replaces a bolt pistol; a Basic Weapon replaces a bolter; a Special Weapon replaces one "
        "Special Weapon the model would normally be allowed to select (flamer, meltagun, plasma gun ...); a Heavy Weapon "
        "replaces one Heavy Weapon the model would normally be allowed to select; a Melee Weapon replaces the weapon "
        "given in its entry. A model without the weapon required by the replacement rule may not select the weapon "
        "unless another rule permits it.\n"
        "Xenos Weapons may only be selected by a force whose Oath of Moment grants access to them (Outlanders: weapons "
        "marked Xenos in the Blackshield Weapons section; The Alien Brotherhood: all Blackshield and Xenos Weapons, "
        "including the conventional Shuriken, Splinter and other xenos weapons). Access to Xenos Weapons does not grant "
        "access to the armoury or army list of another faction."),
    "Xenos": ("Xenos equipment. It may only be selected by a Blackshields force whose Oath of Moment grants access to "
              "Xenos Wargear / Xenos Weapons (Outlanders: items marked Xenos in the Blackshield Armoury and Blackshield "
              "Weapons; The Alien Brotherhood: all Xenos items, including the conventional Xenos Weapons)."),
    # Oaths of Moment
    "Inured to Pain": (
        "All non-vehicle models with the Legiones Astartes (Blackshields) special rule gain Feel No Pain (6+). Blackshield "
        "units with this Oath automatically pass any Casualty Test or Pinning Test caused by enemy shooting attacks. They "
        "still gain Suppression tokens normally and suffer all other effects of Suppression."),
    "The Lure of Battle": (
        "Units with this Oath may never voluntarily fail a Morale or Break test. Before an unengaged unit voluntarily "
        "makes a move that would make it finish farther from the closest visible enemy unit than it began, it must pass a "
        "Leadership test. If failed, the unit must instead move D6\" towards the closest visible enemy unit, stopping 1\" "
        "away from enemy models. Broken or Pinned units, and units embarked on Transports or occupying Buildings or "
        "Fortifications, are not subject to this compulsory movement."),
    "Brothers Before Masters": (
        "Any Blackshield unit with at least one model within 6\" of another friendly Blackshield unit containing at least "
        "five models gains +1 Leadership (maximum 10) and may re-roll To Hit rolls of 1 in the Shooting and Assault "
        "phases. A Blackshield unit may not use the Leadership of an attached Independent Character for Morale, Pinning "
        "or Break tests - use the highest Leadership among the unit's own models. If a Blackshield unit fails a Break "
        "test after losing a close combat, remove D3 additional models from it as casualties before its Retreat move."),
    "Brother-Slayers": ("Blackshield Characters gain Preferred Enemy against enemy Independent Characters, only while in "
                        "base-to-base contact with an enemy Independent Character."),
    "No Gods, No Masters": ("A force using this Oath may not include Chaplains, Agents of the Sigillite or Agents of the "
                            "Warmaster. It may not include an Allied Detachment containing a Primarch."),
    "Void Reavers": (
        "Before deployment, up to half of the Blackshield Infantry units in the army which do not have a Dedicated "
        "Transport may be given the Deep Strike special rule and placed in Reserve. If one of these units suffers a Deep "
        "Strike Mishap, resolve the Mishap normally and then remove D3 models from the unit as casualties."),
    "Unsanctioned Weaponry": ("Models in an Outlanders force may purchase weapons and equipment marked Xenos in the "
                              "Blackshield Armoury. Blackshield Characters may also purchase Rad Grenades (Rad Grenades "
                              "are only available to an Outlanders force)."),
    "The Shadow of Oblivion": (
        "At the beginning of the battle, record the number of units with the Legiones Astartes (Blackshields) special "
        "rule. Once at least half of them have been destroyed or are Broken, this rule takes effect for the remainder of "
        "the battle: at the start of each subsequent Blackshield turn, every remaining Blackshield unit must pass a "
        "Leadership test or be removed from play (counts as destroyed)."),
    "Chymeriae Attributes": (
        "Before deployment, choose one of three Attributes (Gene-Bulked, Lone Wolves, Berserkers). It applies to all "
        "non-vehicle models with the Legiones Astartes (Blackshields) special rule for the entire battle. A Chymeriae "
        "Squad benefits from the Attribute selected for the army; its bonuses and penalties are applied in addition to "
        "the unit's characteristics."),
    "Gene-Bulked": ("Models gain +1 Strength and +1 Toughness and suffer -1 Initiative. Reduce all Advance and Charge "
                    "distances of these models by 1\". Units with this Attribute may not make Pursuit moves."),
    "Lone Wolves": "Models gain +1 Weapon Skill and +1 Ballistic Skill and suffer -2 Leadership.",
    "Berserkers": ("Models gain Fear and Fleet and gain +2 Attacks rather than +1 Attack when charging. Models suffer -1 "
                   "Ballistic Skill. A unit with this Attribute must always Pursue a retreating enemy if able."),
    "Shunned and Distrusted": "A Blackshields force using the Chymeriae Oath may not include an Allied Detachment.",
    "Unlikely Allies": (
        "A force using this Oath may include an Allied Detachment chosen from an Eldar army list; for the Allied "
        "Detachment rules these Eldar units are trusted allies of the Blackshields. No other Allied Detachment may be "
        "included."),
    "Forbidden Arsenals": ("Models in this force may purchase items from the Xenos Wargear section of the Blackshield "
                           "Armoury. Characters and Veteran Sergeants may take Xenos Wargear even if they would not "
                           "normally have access to it."),
    "Eldritch Tutelage": (
        "A single Blackshield Librarian in the army may replace one of his normal psychic powers with one Eldar psychic "
        "power: Doom, Guide, Mind War or Eldritch Storm. He gains no other Eldar special rules, equipment or psychic "
        "abilities and uses the power according to its normal rules unless stated otherwise."),
    "Outcasts Among Outcasts": ("A force using this Oath may not include Chaplains, Agents of the Sigillite or Agents of "
                                "the Warmaster. It may not include Allied Detachments drawn from Imperial forces."),
    "Desperate Warriors": (
        "All non-vehicle models with the Legiones Astartes (Blackshields) special rule gain Furious Charge. In addition, "
        "all non-vehicle models selected from the Legiones Astartes Army List cost 2 points less per model, to a minimum "
        "of 1 point per model."),
    "Scarce Ammunition": (
        "At the beginning of the battle, every Blackshield unit receives two Ammunition counters. Each time the unit "
        "fires one or more ammunition-fed ranged weapons, remove one counter after resolving all of its shooting attacks. "
        "With no counters left it may no longer fire ammunition-fed weapons. Ammunition-fed unless stated otherwise: bolt "
        "weapons, autocannons, assault cannons, shotguns, missile launchers, grenade launchers and other weapons which "
        "clearly rely on physical ammunition. Las weapons and weapons described as energy weapons do not use counters. "
        "Vehicles are not affected."),
    "Scavengers": "Models in this force may purchase las weapons from the Blackshield Armoury where listed.",
    "The Last Magazine": ("A Blackshield unit which has expended all of its Ammunition counters gains +1 Leadership while "
                          "charging or while engaged in close combat."),
    # Reaver Lord
    "Lord of the Blackshields": (
        "A Blackshields force may include no more than one Reaver Lord. If it includes a Reaver Lord, he must be selected "
        "as the army's Warlord. The Reaver Lord is the force's Master of the Legion; a Detachment may include a Reaver "
        "Lord or a Delegatus Consul, not both (author's ruling)."),
    "Reaver Retinue": (
        "For each Reaver Lord, one Legion Veteran Squad may be selected as his Reaver Retinue. It does not occupy a "
        "separate Force Organisation slot and the Reaver Lord must begin the battle attached to it. The squad may select "
        "equipment normally available to a Legion Veteran Squad and may also select Blackshield Weapons where permitted. "
        "Alternatively, the Reaver Lord may be accompanied by a Legion Command Squad or Legion Terminator Command Squad "
        "normally."),
    "Spoils of War": (
        "A Reaver Lord may have one weapon he carries Master-crafted for +10 points. The normal restriction preventing a "
        "model from selecting Blackshield-specific equipment does not apply to him: he may always select Blackshield "
        "Wargear and Blackshield Weapons. This does not grant access to Xenos Wargear or Xenos Weapons unless permitted "
        "by the army's Oath of Moment."),
    # Chymeriae Squad
    "Genetic Instability": (
        "At the beginning of each Blackshield turn, roll a D6 for each Chymeriae Squad; the result lasts until the "
        "beginning of the controlling player's next turn unless stated otherwise.\n"
        "1 Genetic Collapse: the unit suffers D3 wounds (Armour Saves allowed) and -1 Initiative for the remainder of "
        "the turn.\n2 Physiological Degradation: -1 Weapon Skill and -1 Ballistic Skill for the remainder of the turn.\n"
        "3 Momentary Stability: no effect.\n4 Hyper-Adrenal Response: +1 Initiative and Fleet for the remainder of the "
        "turn.\n5 Predatory Frenzy: Furious Charge and +1 Attack for the remainder of the turn; if able to declare a "
        "charge, it must charge the nearest eligible enemy unit.\n6 Genetic Ascendancy: +1 Strength, +1 Toughness and +1 "
        "Attack for the remainder of the turn; at the end of the turn roll a D6, on a 1 the unit suffers D3 wounds "
        "(Armour Saves allowed).\n"
        "UNSTABLE PHYSIOLOGY: these modifiers are temporary and never accumulate between turns. Other modifiers to the "
        "same characteristic apply normally, to the usual minimum and maximum limits."),
    # Blackshield weapon rules
    "Pariah Bolter": ("A unit which fires one or more Pariah Bolters may still charge in the following Assault phase, "
                      "but its models do not receive the normal +1 Attack bonus for charging that turn."),
    "Overpressure": (
        "Before firing a Pariah Flamer, choose to fire it normally or on Overpressure: Strength 4 and Gets Hot for that "
        "attack, and the narrow end of the Template may be placed up to 6\" away from the firing model (the rest of the "
        "Template pointing directly away from the firer). Overpressure may not be used for Stand and Shoot or other "
        "Reaction fire."),
    "Deathlock": (
        "At the end of a Shooting phase in which an enemy unit suffered one or more wounds from Deathlocks, that unit "
        "must take a Leadership test before any other Morale or Pinning tests, at -1 for each wound inflicted by "
        "Deathlocks that phase. Fearless and Stubborn units must still test but suffer no modifier. If failed, the unit "
        "suffers D6 additional wounds (Armour and Invulnerable Saves allowed)."),
    "Lethal Exposure": (
        "Whenever a unit fires one or more Xenos Deathlocks, roll 2D6 after resolving all of its attacks. If the result "
        "is lower than the total number of Deathlock shots fired by the unit, the firing unit suffers one wound with no "
        "Armour Save allowed (controlling player chooses the model). Not rolled for Stand and Shoot or other Reactions."),
    "Splinter Weapon": ("Splinter weapons do not use a Strength value against models with a Toughness characteristic "
                        "and instead wound on a 4+. Against vehicles they count as Strength 1."),
    "Shuriken Cannon": ("A model normally permitted to select a Heavy Bolter or other Heavy Weapon may select a Shuriken "
                        "Cannon instead; it is fired as an Assault weapon."),
    "Halo Blade": ("Character only; Xenos. A two-handed power weapon which adds +3 to the bearer's Strength. The bearer "
                   "may not claim an additional Attack for two close combat weapons. May replace a Power Weapon, Power "
                   "Fist, Thunder Hammer or other close combat weapon where the model has access to the Space Marine "
                   "Armoury."),
    "Witchblade": ("Librarian only; Xenos. Always wounds models with a Toughness characteristic on a 2+ (normal Armour "
                   "Saves allowed); counts as Strength 9 against vehicles. May replace a Force Weapon or Power Weapon. It "
                   "is not a Force Weapon and cannot use the Force Weapon special rule."),
    "Agoniser": ("Character or Veteran Sergeant only; Xenos. Counts as a Power Weapon and always wounds models with a "
                 "Toughness characteristic on a 4+. No special effect against vehicles. May replace a Power Weapon."),
    "Punisher": ("Character only; Xenos. Counts as a two-handed Power Weapon and grants +1 Strength. The bearer may not "
                 "claim an additional Attack for two close combat weapons. May replace a Power Weapon."),
    "Harlequin's Kiss": ("Character or Veteran Sergeant only; Xenos. Counts as a Rending Weapon; successful Rending hits "
                         "wound automatically. May replace a Close Combat Weapon or Rending Weapon."),
    "Scorpion Chainsword": ("Xenos. Counts as a Close Combat Weapon and grants +1 Strength. May replace a Chainsword or "
                            "Close Combat Weapon."),
    "Powerblades": ("Character or Veteran Sergeant only; Xenos. Count as a Power Weapon. They may be used alongside "
                    "another single-handed weapon and count as a second close combat weapon for the additional Attack, "
                    "but not combined with a Power Fist, Thunder Hammer or another two-handed weapon for this bonus."),
    # ------------------------------------------------------------------ Agents of the Sigillite
    "Agents of the Sigillite Detachment": (
        "Agents of the Sigillite are never selected as a Primary Detachment; they may only be included as this special "
        "Allied Detachment: 1 HQ (a Preceptor of the Sigillite or a Knight-Errant), 1 Troops (Sigillite Strike Force "
        "Squad) and 0-1 Elites (a Sigillite Operative Cell OR one Officio Assassinorum Assassin).\n"
        "RESTRICTIONS: exactly one HQ and one Troops choice; up to one Elites choice; no Fast Attack, Heavy Support or "
        "Lords of War. It may only be included alongside a Loyalist Primary Detachment and counts as the army's Allied "
        "Detachment. Models of this Detachment may not normally be chosen as the army's Warlord. An army may never "
        "contain more than one Agents of the Sigillite Detachment."),
    "Orders of the Sigillite": (
        "After both armies are revealed but before deployment, secretly select one Order and write it down. At the end "
        "of the battle reveal it: if fulfilled gain the listed Victory Points, otherwise lose the listed Victory Points. "
        "Only models of the Agents of the Sigillite Detachment count towards an Order unless stated otherwise.\n"
        "I - Venatores Monstrorum: destroy at least three enemy Monstrous Creatures (+5 / -5 VP). Only if the enemy has "
        "at least three Monstrous Creatures at the start.\n"
        "II - Venatores Maleficarum: +1 VP for every enemy Psyker slain by the Detachment; if any enemy Psyker remains "
        "alive at the end, gain nothing and instead lose VP equal to the number of enemy Psykers present at the start. "
        "Only if the enemy has at least one Psyker.\n"
        "III - Quaesito Sanguinis: record unsaved Wounds inflicted by the Detachment (not on Vehicles); +1 VP per full 10; "
        "fewer than 10: -1 VP.\n"
        "IV - Arcana Malcadoris: at the end of each of your turns, +1 VP (max 1 per turn) if a unit of the Detachment "
        "holds an Objective in No Man's Land or the enemy Deployment Zone; if no VP were gained from this Order, -3 VP.\n"
        "V - Vetus Inimicitia: secretly nominate one enemy Independent Character; +2 VP if slain by the Detachment, -2 VP "
        "if it survives."),
    "Agent of the Sigillite": (
        "This character acts with the direct authority of Malcador. He may join units of the Agents of the Sigillite "
        "Detachment or of the army's Loyalist Primary Detachment as a normal Independent Character. Legion-specific "
        "rules are not conferred upon him by joining a Legion unit, and he does not confer Legion-specific rules upon "
        "that unit."),
    "Agents of the Sigillite": (
        "This unit belongs to the Agents of the Sigillite Detachment and counts towards the Orders of the Sigillite."),
    "Hand-Picked Warriors": ("The Agents selected for these formations are drawn from the most capable survivors and "
                             "specialists available to the Sigillite. Sigillite Strike Operatives have Weapon Skill 5 as "
                             "shown in their profile."),
    "Special Issue Ammunition (Sigillite)": (
        "Whenever a model with Special Issue Ammunition fires a Bolter (a Sigillite Boltgun) or the bolter component of a "
        "Combi-weapon, it uses one of the Special Issue Ammunition profiles instead of the normal Bolter profile: Metal "
        "Storm (18\", S3, AP-, Assault 2), Inferno Bolts (24\", S4, AP5, Rapid Fire, Inferno) or Kraken Bolts (30\", S4, "
        "AP4, Rapid Fire). All models of a unit firing Special Issue Ammunition in the same Shooting phase must use the "
        "same ammunition type. Special Issue Ammunition may not be used with an M.40 Stalker Bolter."),
    "Inferno": "Failed To Wound rolls made with Inferno Bolts may be re-rolled. No effect on Armour Penetration rolls.",
    "Psi-shock": ("If a unit containing one or more Psykers is hit by a Psyk-out Grenade, randomly determine one Psyker in "
                  "that unit; it suffers Perils of the Warp in addition to any other damage."),
    "Psi-shock (Ammunition)": (
        "If a Psyker suffers one or more unsaved Wounds from Psyk-out Ammunition during a Shooting phase, it must take a "
        "Leadership test after all attacks from the firing unit have been resolved; if failed it suffers Perils of the "
        "Warp. A Psyker may only be forced to take one such test from each firing unit per Shooting phase. Psyk-out "
        "Ammunition may be used by Bolters (Sigillite Boltguns) and the bolter component of Combi-weapons; when firing it, "
        "use the Psyk-out Ammunition profile (24\", S4, AP5, Rapid Fire, Psi-shock). Psyk-out ammunition contains "
        "psycho-reactive compounds intended to disrupt the concentration and neural activity of enemy psykers."),
    "Mass Psi-shock": ("Every Psyker model hit by the Blast suffers Perils of the Warp in addition to any other damage. "
                       "Non-Psykers suffer only the normal effects of the weapon."),
    "Stasis Anomaly": ("If a unit is hit by a Stasis Grenade, all of its models count as Initiative 1 until the end of the "
                       "current player turn. Multiple Stasis Anomalies have no additional effect."),
    "Mission Equipment": ("Unless otherwise stated, each item of Mission Equipment is limited to 0-1 per Agents of the "
                          "Sigillite Detachment."),
    "Operative Discipline": (
        "When the unit is selected, the Cell Specialist must choose one Operative Discipline. It determines the "
        "Specialist's abilities and grants additional options or special rules to the Cell, and may not be changed "
        "during the battle."),
    "Sanctic Adept": (
        "The Cell Specialist is a Psyker with Psychic Mastery 1 and must select his Psychic Power from Sanctic "
        "Daemonology (never Malefic Daemonology or any other discipline). He is equipped with a Force Weapon (replacing "
        "his Close Combat Weapon) and may "
        "purchase a Psychic Hood for +20 points. The remaining members of the Cell may purchase Psyk-out Ammunition (+5 "
        "points per model) and Psyk-out Grenades (+5 points per model). The Cell may not include a Null Operative."),
    "Null Operative": (
        "The Cell Specialist possesses the Pariah gene or powerful nullification technology; he is not a Psyker. Enemy "
        "Psykers within 12\" of him suffer -1 Leadership when taking Psychic Tests. Any Psychic Power which directly "
        "targets the Specialist or his unit must first pass a Nullification roll of 4+; on a 1-3 the power is nullified "
        "and has no effect on the unit. The remaining members of the Cell may purchase Null-amp Collars (+5 points per "
        "model) and Psyk-out Grenades (+5 points per model). The Cell may never be joined by a Psyker."),
    "Sigillite Exhorter": (
        "The Cell Specialist is equipped with a Power Weapon (replacing his Close Combat Weapon). While he remains alive, "
        "the entire Cell may re-roll failed "
        "Morale and Pinning tests, and during the first round of any close combat in which the Cell charged, all models "
        "in the Cell may re-roll failed To Hit rolls. The remaining members may replace their Close Combat Weapons with "
        "Power Weapons for +10 points per model."),
    "Vigilator (Sigillite)": (
        "The Cell Specialist gains Infiltrate and Stealth and is equipped with a Stalker Bolter (replacing his Close Combat "
        "Weapon). The entire Cell gains "
        "Infiltrate. The remaining members may replace their Bolters with Stalker Bolters (+10 points per model) and may "
        "purchase Cameleoline (+5 points per model)."),
    "Champion (Sigillite)": (
        "The Cell Specialist gains Weapon Skill 6 and is equipped with a Master-crafted Power Weapon (replacing his Close "
        "Combat Weapon). While he remains "
        "alive, any model in the Cell may replace its Close Combat Weapon with a Rending Weapon (+5 points) or a Power "
        "Weapon (+10 points). When in base-to-base contact with an enemy Independent Character, he may re-roll failed "
        "To Hit rolls against that Character."),
    "Assassin Operative (Agents of the Sigillite)": (
        "Instead of a Sigillite Operative Cell, the Detachment's optional Elites choice may be a single Officio "
        "Assassinorum Assassin, selected from the appropriate entry of the Talons of the Emperor army list using all of "
        "its points costs, wargear and special rules. Only one Assassin may be included. For the Orders of the Sigillite "
        "it counts as a member of the Detachment, but it gains no other Agents of the Sigillite rules and no access to "
        "the Agents of the Sigillite Armoury. All normal Officio Assassinorum restrictions (including Assassin Operative "
        "and One Assassin) apply. An Assassin may not be the army's Warlord."),
    "Knight-Errant": (
        "A Knight-Errant counts as an Agent of the Sigillite for all rules purposes, including Orders of the Sigillite. "
        "He may be selected instead of a Preceptor of the Sigillite as the compulsory HQ choice of an Agents of the "
        "Sigillite Allied Detachment. Only one named Knight-Errant may be included in the same army. Unless stated "
        "otherwise he may join units of the Agents of the Sigillite Detachment or the Loyalist Primary Detachment; he "
        "does not gain the Legion special rules of a unit he joins and does not confer the special rules of his former "
        "Legion upon that unit."),
    "Aquila Imperator": (
        "Grants a 4+ Invulnerable Save (already included in Garro's profile). Whenever Garro or a unit he has joined "
        "would be affected by an enemy Psychic Power, roll a D6; on a 5+ that power is nullified and has no effect upon "
        "Garro or his unit. Only one Aquila Imperator nullification roll may be attempted against each Psychic Power."),
    "The Straight Arrow": ("Garro and any unit he has joined are Fearless. Friendly Loyalist units within 6\" of Garro "
                           "may re-roll failed Morale and Pinning tests."),
    "Unbroken Will": ("Garro has the Eternal Warrior special rule and may re-roll failed Leadership tests caused by enemy "
                      "special rules or Psychic Powers."),
    "The Legion of One": ("Loken is Fearless. When fighting in close combat against an enemy Independent Character, he "
                          "may re-roll To Hit rolls of 1."),
    "Fury Unbound": ("Each time Loken suffers an unsaved Wound but is not slain, increase his Strength and Attacks by +1 "
                     "for the remainder of the battle (cumulative). His Strength may not be increased above 7 by this "
                     "rule."),
    "The Half-Heard": "Qruze and any unit he has joined have the Stubborn special rule. Qruze may re-roll failed Morale "
                      "and Pinning tests.",
    "Protect the Innocent, Uphold the Lore": (
        "Once during each enemy Shooting phase, when a friendly Loyalist unit with a model within 12\" of Qruze is "
        "selected as the target of a ranged attack, Qruze may declare that he will protect it: resolve the enemy unit's "
        "shooting against Qruze and any unit he has joined instead (Range and Line of Sight are still measured to the "
        "original target). Not while Falling Back, Pinned, embarked or engaged in close combat. May also be used against "
        "a ranged Psychic Power which targets a friendly unit."),
    "Warrior Born": (
        "During each Assault phase, Varren gains additional Attacks equal to the number of enemy models he personally "
        "killed during the previous Assault phase. These additional Attacks are not cumulative; if he killed no enemy "
        "models in the previous Assault phase he receives no bonus."),
    "The Emperor's Warhound": ("Varren has the Furious Charge special rule. If Varren and a unit he has joined destroy an "
                               "enemy unit in close combat, they must Consolidate towards the nearest enemy unit if "
                               "able."),
    "The Errant Librarian": (
        "Rubio is a Psychic Mastery Level 3 Psyker who generates his Psychic Powers from the Sanctic Daemonology "
        "discipline. He may choose his powers rather than determining them randomly, and may never generate powers from "
        "Malefic Daemonology. Psychic Hood: whenever an enemy Psyker successfully passes a Psychic Test, Rubio may "
        "attempt to nullify the power using his Psychic Hood according to the normal rules."),
}

# --------------------------------------------------------------------------------------------------- weapons
WEAPONS_ = {
    # Blackshield weapons
    "Pariah Bolter": ('16"', "4", "5", "Assault 2"),
    "Xenos Deathlock": ('18"', "5", "5", "Assault 2, Deathlock, Lethal Exposure"),
    # Xenos weapons
    "Shuriken Pistol": ('12"', "4", "5", "Pistol"),
    "Shuriken Catapult": ('12"', "4", "5", "Assault 2"),
    "Shuriken Cannon": ('24"', "6", "5", "Assault 3"),
    "Fusion Gun": ('12"', "8", "1", "Assault 1, Melta"),
    "Lasblaster": ('24"', "3", "5", "Assault 2"),
    "Splinter Pistol": ('12"', "—", "5", "Pistol, Poisoned (4+)"),
    "Splinter Rifle": ('24"', "—", "5", "Rapid Fire, Poisoned (4+)"),
    "Blaster": ('18"', "8", "2", "Assault 1, Lance"),
    "Shredder": ('12"', "6", "—", "Assault 1, Blast"),
    # Blackshield melee weapons (no profile printed; built from the text)
    "Halo Blade": ("-", "+3", "-", "Power Weapon, Two-Handed"),
    "Witchblade": ("-", "User", "-", "Wounds on 2+ (S9 against vehicles); not a Force Weapon"),
    "Agoniser": ("-", "User", "-", "Power Weapon; always wounds on 4+"),
    "Punisher": ("-", "+1", "-", "Power Weapon, Two-Handed"),
    "Harlequin's Kiss": ("-", "User", "-", "Rending; Rending hits wound automatically"),
    "Scorpion Chainsword": ("-", "+1", "-", "Close Combat Weapon"),
    "Powerblades": ("-", "User", "-", "Power Weapon; counts as a second close combat weapon"),
    # Marauder weapons (no profile in the book - see questions)
    "Lascarbine": ('18"', "3", "-", "Assault 2"),
    "Autogun": ('24"', "3", "-", "Rapid Fire"),
    "Laslock": ('24"', "3", "-", "Rapid Fire"),
    "Heavy Chainsword": ("-", "+1", "-", "Two-Handed"),
    # Agents of the Sigillite
    "M.40 Stalker Bolter": ('24"', "4", "5", "Heavy 2, Pinning"),
    "Psyk-out Ammunition": ('24"', "4", "5", "Rapid Fire, Psi-shock"),
    "Psyk-out Grenades": ('8"', "2", "-", "Assault 1, Blast, Psi-shock"),
    "Psyk-out Bomb": ('8"', "2", "-", "Assault 1, Large Blast, One Use, Mass Psi-shock"),
    "Stasis Grenade": ('8"', "2", "-", "Assault 1, Blast, One Use, Stasis Anomaly"),
    "Sabotage Charges": ('6"', "8", "2", "Ordnance 1, Blast, One Use"),
    "Libertas": ("-", "+2", "-", "Power Weapon, Two-Handed, Master-crafted"),
}
SIA = {"Sigillite Boltgun - Metal Storm": ('18"', "3", "-", "Assault 2"),
       "Sigillite Boltgun - Inferno": ('24"', "4", "5", "Rapid Fire, Inferno"),
       "Sigillite Boltgun - Kraken": ('30"', "4", "4", "Rapid Fire")}
MULTI = {
    "Pariah Flamer": {"Pariah Flamer": ("Template", "3", "5", "Assault 1, Overpressure"),
                      "Pariah Flamer - Overpressure": ("Template (narrow end up to 6\" away)", "4", "5",
                                                       "Assault 1, Gets Hot")},
    "Grenade Launcher": {"Grenade Launcher - Frag": ('24"', "3", "6", "Assault 1, Blast"),
                         "Grenade Launcher - Krak": ('24"', "6", "4", "Assault 1")},
    "Second Bolt Pistol": {"Bolt Pistol": ('12"', "4", "5", "Pistol")},
    "Sigillite Boltgun": dict(SIA),
    "Special Issue Ammunition": dict(SIA),
}
XENOS_MARKED = ["Xenos Deathlock", "Halo Blade", "Witchblade", "Agoniser", "Punisher", "Harlequin's Kiss",
                "Scorpion Chainsword", "Powerblades"]
XENOS_CONV = ["Shuriken Pistol", "Shuriken Catapult", "Shuriken Cannon", "Fusion Gun", "Lasblaster", "Splinter Pistol",
              "Splinter Rifle", "Blaster", "Shredder"]
WEAPON_RULES_ = {
    "Pariah Bolter": ["Pariah Bolter"], "Pariah Flamer": ["Overpressure", "Gets Hot"],
    "Xenos Deathlock": ["Deathlock", "Lethal Exposure", "Xenos"],
    "Splinter Pistol": ["Splinter Weapon", "Poison", "Xenos"], "Splinter Rifle": ["Splinter Weapon", "Poison", "Xenos"],
    "Fusion Gun": ["Melta", "Xenos"], "Blaster": ["Lance", "Xenos"], "Shuriken Cannon": ["Shuriken Cannon", "Xenos"],
    "Shuriken Pistol": ["Xenos"], "Shuriken Catapult": ["Xenos"], "Lasblaster": ["Xenos"], "Shredder": ["Xenos"],
    "Halo Blade": ["Halo Blade", "Two-Handed", "Xenos"], "Witchblade": ["Witchblade", "Xenos"],
    "Agoniser": ["Agoniser", "Xenos"], "Punisher": ["Punisher", "Two-Handed", "Xenos"],
    "Harlequin's Kiss": ["Harlequin's Kiss", "Rending", "Xenos"], "Scorpion Chainsword": ["Scorpion Chainsword", "Xenos"],
    "Powerblades": ["Powerblades", "Xenos"], "Heavy Chainsword": ["Two-Handed"],
    "Sigillite Boltgun": ["Special Issue Ammunition (Sigillite)", "Inferno"],
    "Special Issue Ammunition": ["Special Issue Ammunition (Sigillite)", "Inferno"],
    "M.40 Stalker Bolter": ["Pinning"], "Psyk-out Ammunition": ["Psi-shock (Ammunition)"],
    "Psyk-out Grenades": ["Psi-shock"], "Psyk-out Bomb": ["Mass Psi-shock", "Mission Equipment"],
    "Stasis Grenade": ["Stasis Anomaly", "Mission Equipment"], "Sabotage Charges": ["Mission Equipment"],
    "Libertas": ["Two-Handed", "Master-Crafted"],
}
WARGEAR_ = {
    # Blackshield Armoury
    "Rad Grenades (Blackshield)": (
        "While the bearer is engaged in close combat, enemy models engaged in the same combat count their Toughness as 1 "
        "lower when resolving To Wound rolls made by the bearer and his unit (not below Toughness 1). The effects of "
        "multiple Rad Grenades do not stack."),
    "Cyber-familiar": ("Improves the bearer's Invulnerable Save by one point; if the bearer has no Invulnerable Save it "
                       "grants a 6+ Invulnerable Save. An Invulnerable Save may never be improved beyond 3+ in this way."),
    "Ghosthelm": ("Librarian only; Xenos Wargear. Whenever the bearer suffers a wound from Perils of the Warp, roll a D6; "
                  "on a 3+ the wound is ignored. No protection against ordinary weapons or psychic attacks."),
    "Spirit Stones": ("Librarian only; Xenos Wargear. The Librarian may attempt to use one additional Psychic Power each "
                      "turn beyond his normal number. The same power may not be used more than once in the same turn as "
                      "a result of this rule."),
    "Shadow Field": ("0-1 per army; Xenos Wargear. Grants a 2+ Invulnerable Save. The first time the bearer fails an "
                     "Invulnerable Save made with the Shadow Field, the field collapses and may not be used again for "
                     "the battle; the bearer may use any other saves normally afterwards."),
    "Xenos Combat Drugs": ("Xenos Wargear. Once per battle, at the beginning of any Assault phase, the bearer may "
                           "activate them and choose +1 Strength, +1 Initiative or +1 Attack until the end of that "
                           "Assault phase. At the end of the phase roll a D6; on a 1 the bearer suffers one wound with no "
                           "Armour Save allowed."),
    "Deathlock Teleporter": (
        "0-1 per army; Xenos Wargear. DEATHLOCK: whenever the bearer would lose his last Wound, roll a D6 before removing "
        "him: on a 1-2 he is slain normally; on a 3+ he survives with 1 Wound and is teleported - roll a Scatter dice and "
        "4D6 and move him that distance in the direction shown (on a Hit the controlling player chooses the direction); "
        "afterwards he is Pinned. If the final position is in impassable terrain, inside another model or off the "
        "battlefield, he is slain instead. UNSTABLE TECHNOLOGY: at the beginning of each of the controlling player's "
        "turns roll a D6; on a 1 the teleporter activates unexpectedly - resolve a teleport as above without losing "
        "Wounds; the bearer is Pinned afterwards."),
    "Mind Projector": (
        "Xenos Wargear. PSYCHIC REPULSION: when the bearer or a unit he has joined is declared as the target of a charge, "
        "the bearer may use the Mind Projector instead of a Stand and Shoot reaction. The bearer and one Character or "
        "unit leader of the charging unit each roll a D6 and add their Leadership. If the bearer scores higher, the "
        "charge fails and the charging unit stays in place and may make no further charge attempt that phase; otherwise "
        "the charge proceeds normally. No effect on vehicles, Fearless units or models without Leadership. Once per "
        "Assault phase."),
    # Agents of the Sigillite Armoury
    "Null-amp Collar": ("Whenever the bearer or a unit he has joined would be directly affected by an enemy Psychic "
                        "Power, roll a D6; on a 5+ the power has no effect upon the bearer or his unit (other units are "
                        "affected normally). May not be combined with a Psychic Hood to make more than one attempt to "
                        "nullify the same power."),
    "Cameleoline (Sigillite)": ("The model gains the Stealth special rule. If it already has Stealth, it instead "
                                "improves any Cover Save it receives by +1.", ["Stealth"]),
    "Augury Scanner": ("Enemy models may not deploy using Infiltrate within 18\" of the bearer. If an enemy unit arrives "
                       "by Deep Strike within 18\" of the bearer, the bearer's unit may immediately make a Reaction Fire "
                       "attack against it; Rapid Fire and Heavy weapons may be fired normally. Only one such attack "
                       "against each arriving enemy unit regardless of how many Augury Scanners the unit contains."),
    "Sigillite Rosette": ("Preceptor of the Sigillite only. Friendly Loyalist units with at least one model within 6\" "
                          "of the bearer may use his Leadership for Morale, Pinning and Break tests. Once per battle, at "
                          "the beginning of the controlling player's Movement phase, the bearer may cause one friendly "
                          "Loyalist unit within 6\" to automatically Regroup. Does not affect Fearless units or models "
                          "prohibited from using another model's Leadership."),
    "Target Designator": ("Mission Equipment. Instead of firing a weapon in the Shooting phase, the bearer may nominate "
                          "one enemy unit within line of sight. For the rest of that phase all other units of the Agents "
                          "of the Sigillite Detachment may re-roll To Hit rolls of 1 against it. The bearer gains no "
                          "benefit himself."),
    "Shroud Bombs": ("Mission Equipment. A unit containing a model with Shroud Bombs counts as equipped with Defensive "
                     "Grenades. An enemy unit wishing to charge the bearer or a unit he has joined must first pass a "
                     "Leadership test or the charge may not be attempted. Vehicles, Daemons and units with Night Vision "
                     "are unaffected by this test."),
    "False Transponder Codes": (
        "Mission Equipment. The bearer and any unit he has joined gain Outflank (if the unit already has Outflank it may "
        "re-roll the dice for its table edge). During the turn the unit enters play from Reserve, an enemy unit "
        "attempting Reaction Fire or an Interceptor attack against it must first pass a Leadership test or may not fire "
        "at it with that Reaction or Interceptor attack.", ["Outflank"]),
    "Aquila Imperator": RULES["Aquila Imperator"],
}

# ------------------------------------------------------------------------------------------- ids & conditions
SIG_FORCE = None          # set in build()
CAT_SIG_HQ = None
CAT_KE = None
OATH = {}
CHYM_ATTR_CFG = None


def in_force(fid):
    return cond(fid, "force", "instanceOf", 0, deep=False)


def find_group(e, name):
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == name:
            return g
    raise KeyError(name)


def link_names(g):
    gl = g.find("entryLinks")
    return {lk.get("name"): lk for lk in (gl if gl is not None else [])}


def link_cost(lk):
    c = lk.find("costs/cost")
    return float(c.get("value")) if c is not None else 0


def fmt(v):
    return int(v) if float(v).is_integer() else v


def add_links(g, items, mods_for=None):
    """Append links to shared items [(name, pts)] to group g (skipping names already present)."""
    have = link_names(g)
    new = []
    for n, p in items:
        if n in have:
            continue
        lid = uid("link", g.get("id"), "bs", n)
        new.append(link(lid, W(n), n, cost=p or None, mods=(mods_for(n) if mods_for else None)))
    if new:
        add_to(g, "entryLinks", new)


def has_vehicle_profile(e):
    return any(p.get("typeId") in (gs.VEHICLE, gs.WALKER) for p in e.iter("profile"))


# ----------------------------------------------------------------------------------- Blackshield equipment
SIDEARMS = [("Shuriken Pistol", 0), ("Splinter Pistol", 0)]
BASICS = [("Pariah Bolter", 2), ("Xenos Deathlock", 8), ("Shuriken Catapult", 1), ("Lasblaster", 2),
          ("Splinter Rifle", 1)]
MELEE_CHAR = [("Halo Blade", 30), ("Punisher", 20)]
MELEE_SGT = [("Agoniser", 20), ("Harlequin's Kiss", 10), ("Powerblades", 15), ("Scorpion Chainsword", 5)]
BS_WEAPONS = SIDEARMS + BASICS + MELEE_CHAR + MELEE_SGT
MELEE_SLOTS = ("Replace Chainsword", "Replace Close Combat Weapon", "Replace Power Weapon")


def bs_wargear_group(key, librarian_cond=None, digital=True, cap=None):
    """Blackshield Armoury (character equipment)."""
    items = [("Rad Grenades (Blackshield)", 10), ("Cyber-familiar", 15)]
    if digital:
        items.append(("Digital Weapons", 15))
    items += [("Shadow Field", 30), ("Xenos Combat Drugs", 15), ("Deathlock Teleporter", 25), ("Mind Projector", 20)]
    gid = uid("grp", key, "bs-armoury")
    links = []
    for n, p in items:
        lid = uid("link", gid, n)
        links.append(link(lid, W(n), n, cost=p, constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    if librarian_cond is not None:
        for n, p, t in [("Ghosthelm", 15, None), ("Spirit Stones", 25, None),
                        ("Witchblade", 15, "Witchblade (replaces Force Weapon)")]:
            lid = uid("link", gid, n)
            links.append(link(lid, W(n), t or n, cost=p,
                              mods=[modifier("set", "hidden", "true", conds=[librarian_cond]),
                                    modifier("set", uid(lid, "max"), 0, conds=[librarian_cond])],
                              constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    cons = []
    name = "Blackshield Armoury"
    if cap:
        cons.append(constraint(uid(gid, "maxpts"), "max", cap, scope="self", field=PTS, deep=True))
        name += f" (max {cap} pts)"
    return group(gid, name, links=links, constraints=cons)


def inject_armoury(root):
    """Blackshield Weapons into the weapon slots and a Blackshield Armoury group for every model with access to the
    Space Marine Armoury inside a Legiones Astartes entry."""
    for e in list(root.iter("selectionEntry")):
        groups = e.find("selectionEntryGroups")
        if groups is None or not any(g.get("name", "").startswith("Space Marine Armoury") for g in groups):
            continue
        ic = e.get("type") == "unit"
        for g in list(e.iter("selectionEntryGroup")):
            nm = g.get("name")
            if nm == "Replace Bolt Pistol":
                add_links(g, SIDEARMS + (BASICS if "Bolter" in link_names(g) else []))
            elif nm == "Replace Bolter":
                add_links(g, BASICS)
            elif nm in MELEE_SLOTS:
                add_links(g, (MELEE_CHAR if ic else []) + MELEE_SGT)
        lib = lacks(L.consul_id("Librarian"), e.get("id")) if ic else None
        add_to(e, "selectionEntryGroups", [bs_wargear_group(e.get("id"), librarian_cond=lib, digital=not ic)])


SPECIAL_SUBS = {  # weapon in a list -> Blackshield / Xenos alternatives (None = same cost as that weapon)
    "Flamer": [("Pariah Flamer", None), ("Shredder", 8)],
    "Meltagun": [("Fusion Gun", None), ("Blaster", 15), ("Shredder", 8)],
    "Plasma Gun": [("Blaster", 15), ("Shredder", 8)],
    "Heavy Bolter": [("Shuriken Cannon", 10)],
}


def copy_link(src, gid, name, cost):
    c = copy.deepcopy(src)
    ids = {x.get("id") for x in c.iter() if x.get("id")}
    remap = {i: uid(i, "bs", name) for i in ids}
    for x in c.iter():
        for a in ("id", "field", "scope", "childId"):
            v = x.get(a)
            if v in remap:
                x.set(a, remap[v])
    c.set("id", uid("link", gid, "bs", name))
    c.set("targetId", W(name))
    c.set("name", name)
    old = c.find("costs")
    if old is not None:
        c.remove(old)
    if cost:
        c.append(wrap("costs", [el("cost", {"name": "pts", "typeId": PTS, "value": fmt(cost)})]))
    return c


def inject_specials(root):
    """Special/Heavy Weapon lists of non-vehicle units also offer the Blackshield and Xenos alternatives."""
    if has_vehicle_profile(root):
        return
    for g in list(root.iter("selectionEntryGroup")):
        names = link_names(g)
        new = []
        added = set(names)
        for w, subs in SPECIAL_SUBS.items():
            if w not in names:
                continue
            for n, p in subs:
                if n in added:
                    continue
                added.add(n)
                new.append(copy_link(names[w], g.get("id"), n, link_cost(names[w]) if p is None else p))
        if new:
            add_to(g, "entryLinks", new)


def inject_xenos_bolters(root):
    """'Any Blackshield model equipped with a Bolter may replace it with a Shuriken Catapult / Lasblaster.'"""
    if has_vehicle_profile(root):
        return
    mids = []
    for e in root.iter("selectionEntry"):
        if e.get("type") != "model":
            continue
        groups = e.find("selectionEntryGroups")
        if groups is not None and any(g.get("name", "").startswith("Space Marine Armoury") for g in groups):
            continue
        gl = e.find("entryLinks")
        if gl is not None and any(lk.get("targetId") == W("Bolter") for lk in gl):
            mids.append(e.get("id"))
    if not mids:
        return
    g = model_swaps(k("xb", root.get("id")), "Xenos Weapons: replace Bolter (The Alien Brotherhood)", root.get("id"),
                    mids, [("Shuriken Catapult", 1), ("Lasblaster", 2)])
    add_mods(g, [modifier("set", "hidden", "true", conds=[lacks(OATH["The Alien Brotherhood"], "force")])])
    add_to(root, "selectionEntryGroups", [g])


def apply_ashes(root):
    """Ashes of the Armoury: non-vehicle models from the Legiones Astartes Army List cost 2 points less."""
    c = [has(OATH["Ashes of the Armoury"], "force")]
    zero_models = 0
    any_model = False
    for m in root.iter("selectionEntry"):
        if m.get("type") != "model":
            continue
        profs = m.find("profiles")
        if profs is None or not any(p.get("typeId") == gs.UNIT for p in profs):
            continue
        any_model = True
        if link_cost(m) > 0:
            add_mods(m, [modifier("decrement", PTS, 2, conds=list(c))])
        else:
            mn = [x for x in m.findall("constraints/constraint") if x.get("type") == "min" and x.get("scope") == "parent"]
            zero_models += int(float(mn[0].get("value"))) if mn else 0
    if not any_model:
        profs = root.find("profiles")
        if profs is not None and any(p.get("typeId") == gs.UNIT for p in profs):
            zero_models = 1
    if zero_models:
        add_mods(root, [modifier("decrement", PTS, 2 * zero_models, conds=list(c))])


def blackshield_unit(root):
    """Turn a Legiones Astartes entry into its Blackshields version."""
    if not has_vehicle_profile(root) or any(p.get("typeId") == gs.UNIT for p in root.iter("profile")):
        add_to(root, "infoLinks", rules_links(["Legiones Astartes (Blackshields)"], key=k("bsrule", root.get("id"))))
    inject_armoury(root)
    inject_specials(root)
    inject_xenos_bolters(root)
    apply_ashes(root)


ELDAR_POWERS = ["Doom", "Guide", "Mind War", "Eldritch Storm"]
CAT_ELDAR_POWER = None    # set in build()


def eldar_rule(n):
    return f"{n} (Eldar Psychic Power)"


for _n in ELDAR_POWERS:
    RULES[eldar_rule(_n)] = (
        f"{_n} - an Eldar psychic power, available through Eldritch Tutelage (The Alien Brotherhood): a single "
        "Blackshield Librarian in the army may select it in place of one of his normal psychic powers. He uses the power "
        "according to its normal rules from the Eldar army list (not printed in The Lost and the Damned) and gains no "
        "other Eldar special rules, equipment or psychic abilities.")


def add_eldritch_tutelage(roots):
    """Eldritch Tutelage: the Librarian's Psychic Powers group also offers the four Eldar powers (The Alien Brotherhood
    only, one Eldar power in the whole army). They take the place of a normal power (same power count)."""
    for r in roots:
        for e in r.iter("selectionEntry"):
            if e.get("id") != L.consul_id("Librarian"):
                continue
            g = L.powers_group(e)
            if g is None:
                continue
            off = lacks(OATH["The Alien Brotherhood"], "force")
            ents = []
            for n in ELDAR_POWERS:
                eid = uid("psy-power", g.get("id"), "eldar", n)
                ents.append(entry(eid, f"{n} (Eldar - Eldritch Tutelage)",
                                  cats=[category_link(CAT_ELDAR_POWER, "Eldar Psychic Power", key=eid)],
                                  mods=[modifier("set", "hidden", "true", conds=[off]),
                                        modifier("set", uid(eid, "max"), 0, conds=[off]),
                                        error_if("Eldritch Tutelage: only a single Blackshield Librarian in the army "
                                                 "may take one Eldar psychic power.",
                                                 [cond(CAT_ELDAR_POWER, "roster", "greaterThan", 1)])],
                                  constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                                  infolinks=rules_links([eldar_rule(n), "Eldritch Tutelage"], key=eid)))
            add_to(g, "selectionEntries", ents)


# ------------------------------------------------------------------------------------------- Blackshield units
def reaver_lord():
    u = k("unit", "Reaver Lord")
    arm = L.ic_armoury(k("reaver"), u, True)
    cap_id = uid(arm.get("id"), "maxpts")
    for c in arm.iter("constraint"):
        if c.get("id") == cap_id:
            c.set("value", "75")
    arm.set("name", "Space Marine Armoury (max 75 pts)")
    for g in arm.iter("selectionEntryGroup"):
        gl = g.find("entryLinks")
        if g.get("name") == "Additional Wargear":
            for lk in list(gl):
                if lk.get("name") in ("Iron Halo", "Master-crafted Weapon"):
                    gl.remove(lk)
        elif g.get("name") == "Replace Bolt Pistol":
            add_links(g, SIDEARMS + BASICS + MELEE_CHAR + MELEE_SGT)
        elif g.get("name") == "Replace Chainsword":
            add_links(g, MELEE_CHAR + MELEE_SGT + BASICS)
    bs = bs_wargear_group(k("reaver"), digital=False, cap=50)
    bs_cap = uid(bs.get("id"), "maxpts")
    # Blackshield Weapons count towards the 50-point Blackshield allowance, not the 75-point Armoury
    for n, p in BS_WEAPONS:
        if p:
            add_mods(arm, [modifier("increment", cap_id, p, repeats=[repeat(W(n), u, 1)])])
            add_mods(bs, [modifier("decrement", bs_cap, p, repeats=[repeat(W(n), u, 1)])])
    bs.set("name", "Blackshield Armoury and Weapons (max 50 pts; Blackshield Weapons are chosen in the weapon slots)")
    mc = upgrade(k("reaver"), "Master-crafted Weapon (Spoils of War; counts towards the 75 pts)", 10,
                 links=["Master-crafted Weapon"])
    # the Master-craft counts towards the 75-point Space Marine Armoury allowance (author's answer)
    add_mods(arm, [modifier("decrement", cap_id, 10, conds=[has(mc.get("id"), u)])])
    # retinue: Reaver Retinue (Legion Veteran Squad) or a Legion Command Squad / Terminator Command Squad
    before = len(L2.RETINUE_SHARED)
    rg = L2.retinue_group(k("reaver"), u, False)
    vet = clone(L2.veteran_squad(), "reaver-retinue", "Reaver Retinue (Legion Veteran Squad)")
    for tag in ("categoryLinks", "modifiers"):
        x = vet.find(tag)
        if x is not None:
            vet.remove(x)
    add_to(vet, "infoLinks", rules_links(["Reaver Retinue", "Retinue"], key=k("rr")))
    add_to(rg, "entryLinks", [link(uid("link", rg.get("id"), "reaver-vets"), vet.get("id"), vet.get("name"))])
    retinues = L2.RETINUE_SHARED[before:] + [vet]
    e = unit("Reaver Lord", 125, HQ, "HQ", key=u,
             profiles=[unit_profile(u, "Reaver Lord", "Infantry (Character)", 6, 5, 4, 4, 3, 5, 3, 10, "3+/4+")],
             kit=["Frag Grenades", "Iron Halo"],
             rules_=["Legiones Astartes", "Legiones Astartes (Blackshields)", "Independent Character",
                     "Lord of the Blackshields", "Reaver Retinue", "Spoils of War", "Master of the Legion",
                     "Blackshield Armoury", "Blackshield Weapons"],
             groups=[arm, *L.ic_armour_mobility(k("reaver"), u, False), bs, rg], entries=[mc],
             mods=[L.tda_pistol_error(u),
                   error_if("A Detachment may include a Reaver Lord or a Delegatus Consul, not both.",
                            [has(L.consul_id("Delegatus"), "force")])],
             constraints=[unique(u)],
             extra_cats=[(gs.CAT_MASTER, "Master of the Legion")])
    return e, retinues


MARAUDER_SPECIALS = [("Sniper Rifle", 5), ("Flamer", 6), ("Pariah Flamer", 6), ("Grenade Launcher", 8),
                     ("Heavy Flamer", 10), ("Meltagun", 10), ("Plasma Gun", 10), ("Heavy Bolter", 10),
                     ("Autocannon", 15), ("Missile Launcher", 15), ("Multi-Melta", 15), ("Plasma Pistol", 5),
                     ("Power Weapon", 10),
                     # Xenos Weapons (The Alien Brotherhood)
                     ("Fusion Gun", 10), ("Blaster", 15), ("Shredder", 8), ("Shuriken Cannon", 10)]


def marauder_squad():
    name = "Blackshield Marauder Squad"
    u = k("unit", name)
    ck = k("marauder-chief")
    chief = model(u, "Marauder Chief", 1, 1, 0,
                  unit_profile(u, "Marauder Chief", "Infantry (Character)", 5, 4, 4, 4, 1, 4, 3, 9, "3+"),
                  kit=["Power Armour", "Frag Grenades", "Krak Grenades"],
                  groups=[slot(ck, "Replace Chainsword", "Chainsword",
                               [("Rending Weapon", 5), ("Power Weapon", 10), ("Power Fist", 15),
                                ("Lightning Claw", 15), ("Thunder Hammer", 20)] + MELEE_CHAR + MELEE_SGT),
                          slot(ck, "Replace Bolt Pistol", "Bolt Pistol", SIDEARMS),
                          take(ck, "Combi-weapon", [("Combi-Flamer", 10), ("Combi-Grenade Launcher", 10),
                                                    ("Combi-Meltagun", 10), ("Combi-Plasma Gun", 10),
                                                    ("Combi-Volkite Charger", 10)], max_total=1),
                          take(ck, "Marauder Chief Wargear", [("Plasma Pistol", 10), ("Melta Bombs", 5)]),
                          bs_wargear_group(ck)])
    mar = model(u, "Marauder", 4, 19, 15,
                unit_profile(u, "Marauder", "Infantry", 4, 4, 4, 4, 1, 4, 2, 8, "3+"),
                kit=["Power Armour", "Bolt Pistol", "Chainsword", "Frag Grenades", "Krak Grenades"])
    mid = mar.get("id")
    spec, _ = pool(k("marauder"), "Special and Heavy Weapons (one Marauder per 5 models, instead of a Marauder "
                                  "Weapon)", u, MARAUDER_SPECIALS, 0, every=5)
    spec_ids = [W(n) for n, _ in MARAUDER_SPECIALS]
    weapons = model_swaps(k("marauder"), "Marauder Weapons (each Marauder may take one)", u, [mid],
                          [("Lascarbine", 0), ("Autogun", 0), ("Astartes Shotgun", 1), ("Laslock", 2),
                           ("Second Bolt Pistol", 2), ("Bolter", 2), ("Pariah Bolter", 2), ("Heavy Chainsword", 5)],
                          minus=spec_ids)
    xenos = model_swaps(k("marauder"), "Xenos Basic Weapon or Sidearm (The Alien Brotherhood; replaces Bolt Pistol)",
                        u, [mid], [("Shuriken Pistol", 0), ("Splinter Pistol", 0), ("Shuriken Catapult", 1),
                                   ("Splinter Rifle", 1), ("Lasblaster", 2)])
    add_mods(xenos, [modifier("set", "hidden", "true", conds=[lacks(OATH["The Alien Brotherhood"], "force")])])
    return unit(name, 100 - 4 * 15, TROOPS, "Troops", key=u, models=[chief, mar],
                rules_=["Legiones Astartes", "Legiones Astartes (Blackshields)", "Blackshield Weapons"],
                groups=[weapons, spec, xenos, take(k("marauder"), "Squad Equipment (one Marauder)",
                                                   [("Nuncio Vox", 10)]),
                        L2.transports(k("marauder"), u, ["Legion Rhino Armoured Carrier"], max_models=10,
                                      orbital=False, spearhead=False)])


def chymeriae_squad():
    name = "Chymeriae Squad"
    u = k("unit", name)
    ak = k("chym-alpha")
    arm = L2.pa_armoury(ak, u, 10, slots=["Bolt Pistol", "Chainsword"])
    for g in arm.iter("selectionEntryGroup"):
        names = link_names(g)
        if g.get("name") == "Replace Chainsword":
            add_links(g, [("Heavy Chainsword", 5)] + MELEE_SGT)
            for n, p in [("Rending Weapon", 5), ("Power Weapon", 10)]:
                if n in names:
                    lk = names[n]
                    lk.remove(lk.find("costs")) if lk.find("costs") is not None else None
                    lk.append(wrap("costs", [el("cost", {"name": "pts", "typeId": PTS, "value": p})]))
        elif g.get("name") == "Replace Bolt Pistol":
            if "Bolter" in names:
                lk = names["Bolter"]
                if lk.find("costs") is not None:
                    lk.remove(lk.find("costs"))
            add_links(g, SIDEARMS + BASICS)
    alpha = model(u, "Chymeriae Alpha", 1, 1, 0,
                  unit_profile(u, "Chymeriae Alpha", "Infantry", 5, 4, 4, 4, 1, 4, 3, 9, "3+"),
                  kit=["Power Armour", "Frag Grenades", "Krak Grenades"], groups=[arm, bs_wargear_group(ak)])
    ch = model(u, "Chymeriae", 4, 9, 20, unit_profile(u, "Chymeriae", "Infantry", 4, 4, 4, 4, 1, 4, 2, 8, "3+"),
               kit=["Power Armour", "Bolt Pistol", "Chainsword", "Frag Grenades", "Krak Grenades"])
    cid = ch.get("id")
    specs = [("Flamer", 6), ("Pariah Flamer", 6), ("Meltagun", 10), ("Plasma Gun", 10),
             ("Fusion Gun", 10), ("Blaster", 15), ("Shredder", 8)]
    spec, _ = pool(k("chym"), "Special Weapons (one Chymeriae per 5 models; replaces Bolt Pistol)", u, specs, 0,
                   every=5)
    swaps = [model_swaps(k("chym"), "Chymeriae: replace Chainsword (any number)", u, [cid],
                         [("Heavy Chainsword", 5), ("Rending Weapon", 5), ("Power Weapon", 10)]),
             model_swaps(k("chym"), "Chymeriae: replace Bolt Pistol with Bolter (any number)", u, [cid],
                         [("Bolter", 0)], minus=[W(n) for n, _ in specs])]
    no_oath = [lacks(OATH["Chymeriae"], "force")]
    return unit(name, 115 - 4 * 20, ELITES, "Elites", key=u, models=[alpha, ch],
                rules_=["Legiones Astartes", "Legiones Astartes (Blackshields)", "Chymeriae Attributes",
                        "Genetic Instability"],
                groups=[*swaps, spec, L2.transports(k("chym"), u, ["Legion Rhino Armoured Carrier"], max_models=10,
                                                    orbital=False, spearhead=False)],
                mods=[modifier("set", "hidden", "true", conds=list(no_oath)),
                      error_if("Only a Blackshields force using the Chymeriae Oath of Moment may include a Chymeriae "
                               "Squad.", no_oath)])


# ------------------------------------------------------------------------------------- Agents of the Sigillite
SIG_PISTOLS = [("Hand Flamer", 5), ("Volkite Serpenta", 5), ("Plasma Pistol", 15)]
SIG_COMBIS = [("Combi-Flamer", 5), ("Combi-Grenade Launcher", 5), ("Combi-Meltagun", 5), ("Combi-Plasma Gun", 5)]
SIG_RANGED = SIG_COMBIS + [("Storm Bolter", 5), ("M.40 Stalker Bolter", 10), ("Flamer", 5), ("Volkite Charger", 5),
                           ("Meltagun", 10), ("Plasma Gun", 10), ("Heavy Bolter", 10), ("Autocannon", 15),
                           ("Missile Launcher", 15), ("Multi-Melta", 15)]
SIG_MELEE = [("Chainsword", 0), ("Power Fist", 15), ("Lightning Claw", 15), ("Relic Blade", 20),
             ("Aether-shock Maul", 15)]
SIG_GEAR = [("Psyk-out Grenades", 5), ("Psyk-out Ammunition", 5), ("Null-amp Collar", 10), ("Digital Weapons", 15),
            ("Cyber-familiar", 15), ("Cameleoline (Sigillite)", 5), ("Augury Scanner", 15), ("Nuncio Vox", 10),
            ("Suspensor Web", 10), ("Teleport Homer", 5)]
MISSION = [("Target Designator", 15), ("Sabotage Charges", 10), ("Shroud Bombs", 10), ("Psyk-out Bomb", 15),
           ("Stasis Grenade", 15), ("False Transponder Codes", 15)]


def sig_mods(hq=False, ke=False):
    mods = [hide_if(in_force(STD_FORCE)),
            error_if("Agents of the Sigillite may only be included alongside a Loyalist Primary Detachment.",
                     [has(L.TRAITOR, "roster"), lacks(L.LOYALIST, "roster")]),
            error_if("A force using the Orphans of War or The Alien Brotherhood Oath of Moment may not include Agents of "
                     "the Sigillite.", [has(OATH["Orphans of War"], "roster"),
                                        has(OATH["The Alien Brotherhood"], "roster")])]
    if hq:
        mods.append(error_if("An army may never contain more than one Agents of the Sigillite Detachment (one HQ "
                             "choice).", [cond(CAT_SIG_HQ, "roster", "greaterThan", 1)]))
    if ke:
        mods.append(error_if("Only one named Knight-Errant may be included in the same army.",
                             [cond(CAT_KE, "roster", "greaterThan", 1)]))
    return mods


def sig_unit(name, cost, slot_cat, slot_name, hq=False, ke=False, **kw):
    cats = list(kw.pop("extra_cats", []))
    if hq:
        cats.append((CAT_SIG_HQ, "Agents of the Sigillite HQ"))
    if ke:
        cats.append((CAT_KE, "Knight-Errant"))
    mods = sig_mods(hq, ke) + list(kw.pop("mods", []))
    return unit(name, cost, slot_cat, slot_name, compulsory=False, extra_cats=cats, mods=mods, **kw)


def preceptor():
    name = "Preceptor of the Sigillite"
    u = k("unit", name)
    pk = k("preceptor")
    gear_links = []
    gid = uid("grp", pk, "wargear")
    for n, p in SIG_GEAR + MISSION:
        lid = uid("link", gid, n)
        gear_links.append(link(lid, W(n), n, cost=p, constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    extra = group(gid, "Agents of the Sigillite Armoury (max 75 pts)", links=gear_links,
                  constraints=[constraint(uid(gid, "maxpts"), "max", 75, scope="self", field=PTS, deep=True)])
    armour = slot(pk, "Armour", "Artificer Armour", [("Terminator Armour", 15)])
    return sig_unit(name, 125, HQ, "HQ", hq=True, key=u,
                    profiles=[unit_profile(u, name, "Infantry (Character)", 5, 5, 4, 4, 3, 5, 3, 10, "2+/4+")],
                    kit=["Iron Halo", "Frag Grenades", "Krak Grenades",
                         "Special Issue Ammunition", "Sigillite Rosette"],
                    rules_=["Independent Character", "Agent of the Sigillite", "Special Issue Ammunition (Sigillite)",
                            "Agents of the Sigillite Detachment", "Orders of the Sigillite", "Mission Equipment"],
                    groups=[armour, slot(pk, "Replace Bolt Pistol", "Bolt Pistol", SIG_PISTOLS),
                            slot(pk, "Replace Bolter", "Bolter", SIG_RANGED),
                            slot(pk, "Replace Power Weapon", "Power Weapon", SIG_MELEE), extra],
                    entries=[upgrade(pk, "Master-crafted Weapon", 10, links=["Master-crafted Weapon"])],
                    mods=[modifier("add", "error", "A Preceptor in Terminator Armour may not keep a Bolt Pistol - "
                                                   "replace it.",
                                   groups=[all_of(has(W("Terminator Armour"), u), has(W("Bolt Pistol"), u))])])


def strike_force():
    name = "Sigillite Strike Force Squad"
    u = k("unit", name)
    pk = k("strike-prime")
    prime = model(u, "Strike Prime", 1, 1, 0,
                  unit_profile(u, "Strike Prime", "Infantry (Character)", 5, 5, 4, 4, 2, 4, 3, 9, "3+"),
                  kit=["Power Armour", "Bolt Pistol", "Frag Grenades", "Krak Grenades", "Special Issue Ammunition"],
                  groups=[slot(pk, "Replace Close Combat Weapon", "Close Combat Weapon",
                               [("Chainsword", 0), ("Power Weapon", 10), ("Power Fist", 15), ("Lightning Claw", 15),
                                ("Relic Blade", 20)]),
                          take(pk, "Strike Prime Wargear", [("Melta Bombs", 5), ("Refractor Field", 15)])])
    op = model(u, "Sigillite Strike Operative", 4, 9, 25,
               unit_profile(u, "Sigillite Strike Operative", "Infantry", 5, 5, 4, 4, 1, 4, 2, 9, "3+"),
               kit=["Power Armour", "Bolt Pistol", "Close Combat Weapon", "Frag Grenades", "Krak Grenades",
                    "Special Issue Ammunition"])
    heavy = [("Flamer", 5), ("Volkite Charger", 5), ("Meltagun", 10), ("Plasma Gun", 10), ("Heavy Bolter", 10),
             ("Autocannon", 15), ("Missile Launcher", 15), ("Multi-Melta", 15)]
    spec, mx = pool(k("ssf"), "Special and Heavy Weapons (up to two models per five; replace Boltgun)", u, heavy, 0,
                    every=5)
    add_mods(spec, [modifier("increment", mx, 1, repeats=[repeat("model", u, 5)])])
    pid, oid = prime.get("id"), op.get("id")
    # Boltgun: every model carries one (the Bolter is bought back through these blocks)
    bolt = model_swaps(k("ssf"), "Replace Boltgun (any model)", u, [pid, oid],
                       SIG_COMBIS + [("Storm Bolter", 5), ("Chainsword", 0), ("Power Weapon", 10)],
                       minus=[W(n) for n, _ in heavy])
    ccw = model_swaps(k("ssf"), "Sigillite Strike Operatives: replace Close Combat Weapon (any number)", u, [oid],
                      [("Chainsword", 0), ("Power Weapon", 10), ("Power Fist", 15), ("Lightning Claw", 15)])
    return sig_unit(name, 150 - 4 * 25, TROOPS, "Troops", key=u, models=[prime, op],
                    kit=["Bolter"] if False else [],
                    rules_=["Agents of the Sigillite", "Hand-Picked Warriors", "Special Issue Ammunition (Sigillite)"],
                    groups=[bolt, spec, ccw], constraints=[unique(u)],
                    entries=[entry(k("ssf", "bolters"), "Boltguns (every model not replacing it)", cost=0,
                                   rules=[rule(k("ssf", "bolters", "r"), "Boltguns",
                                               "Every model carries a Bolter (Sigillite Boltgun) unless it replaced it "
                                               "using the options above.")],
                                   constraints=[constraint(k("ssf", "bolters", "min"), "min", 1, auto=True),
                                                constraint(k("ssf", "bolters", "max"), "max", 1, auto=True)],
                                   links=[gear(k("ssf", "bolters"), "Bolter")])])


DISCIPLINES = [("Sanctic Adept", 30, ["Force Weapon"], ["Sanctic Adept", "Psyker"]),
               ("Null Operative", 25, ["Close Combat Weapon"], ["Null Operative"]),
               ("Sigillite Exhorter (Confessor)", 20, ["Power Weapon"], ["Sigillite Exhorter"]),
               ("Vigilator", 20, ["M.40 Stalker Bolter"], ["Vigilator (Sigillite)", "Infiltrate", "Stealth"]),
               ("Champion (Blade Champion)", 25, ["Power Weapon", "Master-crafted Weapon"], ["Champion (Sigillite)"])]


def operative_cell():
    name = "Sigillite Operative Cell"
    u = k("unit", name)
    sk = k("cell-specialist")
    disc = choice(sk, "Operative Discipline", [(n, p, False, items, r) for n, p, items, r in DISCIPLINES],
                  required=True)
    did = {n: uid("choice", sk, "Operative Discipline", n) for n, *_ in DISCIPLINES}

    def only(*names):
        """mods: hidden and unavailable unless one of the named disciplines is chosen."""
        off = all_of(*[lacks(did[n], u) for n in names])
        return off

    def gated(key, nm, cost, items, names, text=None):
        eid = k("cell", key)
        return entry(eid, nm, cost=cost,
                     mods=[modifier("set", "hidden", "true", groups=[only(*names)]),
                           modifier("set", uid(eid, "max"), 0, groups=[only(*names)])],
                     constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                     links=[gear(eid, x) for x in items],
                     rules=[rule(uid(eid, "r"), nm, text)] if text else [])
    spec = model(u, "Cell Specialist", 1, 1, 0,
                 unit_profile(u, "Cell Specialist", "Infantry (Character)", 5, 5, 4, 4, 2, 5, 3, 9, "3+"),
                 kit=["Power Armour", "Bolter", "Bolt Pistol", "Frag Grenades", "Krak Grenades",
                      "Special Issue Ammunition"],
                 groups=[disc, L.psychic_powers(k("cell-adept"), u, 1, ["Daemonology (Sanctic)"],
                                                hide=[lacks(did["Sanctic Adept"], u)])],
                 entries=[gated("hood", "Psychic Hood (Sanctic Adept)", 20, ["Psychic Hood"], ["Sanctic Adept"])])
    op = model(u, "Sigillite Operative", 4, 4, 0,
               unit_profile(u, "Sigillite Operative", "Infantry", 5, 5, 4, 4, 1, 4, 2, 9, "3+"),
               kit=["Power Armour", "Bolt Pistol", "Frag Grenades", "Krak Grenades", "Special Issue Ammunition"])
    oid = op.get("id")
    heavy = [("Heavy Bolter", 10), ("Autocannon", 15), ("Missile Launcher", 15), ("Multi-Melta", 15)]
    hv, _ = pool(k("cell"), "Heavy Weapon (up to one Sigillite Operative; replaces Boltgun)", u, heavy, 1)
    vig_off = [lacks(did["Vigilator"], u)]
    champ_off = [lacks(did["Champion (Blade Champion)"], u)]
    bolt = model_swaps(k("cell"), "Sigillite Operatives: replace Boltgun (any number)", u, [oid],
                       SIG_COMBIS + [("Storm Bolter", 5), ("Chainsword", 0), ("Flamer", 5), ("Volkite Charger", 5),
                                     ("Meltagun", 10), ("Plasma Gun", 10),
                                     ("M.40 Stalker Bolter", 10, [modifier("set", "hidden", "true", conds=vig_off)])],
                       minus=[W(n) for n, _ in heavy])
    ccw = model_swaps(k("cell"), "Sigillite Operatives: replace Close Combat Weapon (any number)", u, [oid],
                      [("Chainsword", 0), ("Power Weapon", 10), ("Lightning Claw", 15), ("Power Fist", 15),
                       ("Rending Weapon", 5, [modifier("set", "hidden", "true", conds=champ_off)])])
    keep = entry(k("cell", "bolters"), "Boltguns (Sigillite Operatives not replacing it)", cost=0,
                 constraints=[constraint(k("cell", "bolters", "min"), "min", 1, auto=True),
                              constraint(k("cell", "bolters", "max"), "max", 1, auto=True)],
                 links=[gear(k("cell", "bolters"), "Bolter"), gear(k("cell", "ccw"), "Close Combat Weapon")],
                 rules=[rule(k("cell", "bolters", "r"), "Operative weapons",
                             "Every Sigillite Operative carries a Bolter (Sigillite Boltgun) and a Close Combat Weapon "
                             "unless it replaced them using the options above.")])
    upgrades = [
        gated("psykammo", "Psyk-out Ammunition (4 Sigillite Operatives, +5 each)", 20, ["Psyk-out Ammunition"],
              ["Sanctic Adept"]),
        gated("psykgren", "Psyk-out Grenades (4 Sigillite Operatives, +5 each)", 20, ["Psyk-out Grenades"],
              ["Sanctic Adept", "Null Operative"]),
        gated("nullamp", "Null-amp Collars (4 Sigillite Operatives, +5 each)", 20, ["Null-amp Collar"],
              ["Null Operative"]),
        gated("camo", "Cameleoline (4 Sigillite Operatives, +5 each)", 20, ["Cameleoline (Sigillite)"],
              ["Vigilator"]),
    ]
    vig_rule = gated("vig-infiltrate", "Vigilator: entire Cell gains Infiltrate", 0, [], ["Vigilator"],
                     text="The entire Cell gains Infiltrate.")
    add_mods(vig_rule, [modifier("set", uid(vig_rule.get("id"), "min"), 1, conds=[has(did["Vigilator"], u)])])
    add_to(vig_rule, "constraints", [constraint(uid(vig_rule.get("id"), "min"), "min", 0, auto=True)])
    return sig_unit(name, 150, ELITES, "Elites", key=u, models=[spec, op],
                    rules_=["Agents of the Sigillite", "Hand-Picked Warriors", "Operative Discipline",
                            "Special Issue Ammunition (Sigillite)"],
                    groups=[bolt, hv, ccw], entries=[keep, *upgrades, vig_rule], constraints=[unique(u)])


ASSASSINS = [("Vindicare Assassin", 110), ("Callidus Assassin", 120), ("Eversor Assassin", 95),
             ("Culexus Assassin", 105), ("Adamus Assassin", 125), ("Venenum Assassin", 125),
             ("Vanus Infocyte Assassin", 105)]


def assassin():
    name = "Officio Assassinorum Assassin"
    u = k("unit", name)
    temple = choice(k("assassin"), "Assassin Temple", [(n, p, False, [], []) for n, p in ASSASSINS], required=True)
    return sig_unit(name, 0, ELITES, "Elites", key=u, groups=[temple], constraints=[unique(u)],
                    rules_=["Assassin Operative (Agents of the Sigillite)"])


def knight(name, cost, stats, kit, rules_, powers=0):
    u = k("unit", name.split(" — ")[0])
    groups = [L.psychic_powers(k("psy", u), u, powers, ["Daemonology (Sanctic)"])] if powers else []
    return sig_unit(name, cost, HQ, "HQ", hq=True, ke=True, key=u, groups=groups,
                    profiles=[unit_profile(u, name.split(" — ")[0], "Infantry (Character)", *stats)],
                    kit=kit, constraints=[unique(u)],
                    rules_=["Independent Character", "Agent of the Sigillite", "Knight-Errant", *rules_,
                            "Agents of the Sigillite Detachment", "Orders of the Sigillite"])


def knights():
    std = ["Bolt Pistol", "Frag Grenades", "Krak Grenades"]
    sia = ["Sigillite Boltgun", "Special Issue Ammunition"]
    return [
        knight("Nathaniel Garro — The Straight Arrow", 165, (6, 5, 4, 4, 3, 5, 3, 10, "2+/4+"),
               ["Artificer Armour", "Aquila Imperator", "Libertas", *std],
               ["The Straight Arrow", "Unbroken Will", "Fearless", "Eternal Warrior"]),
        knight("Garviel Loken — The Legion of One", 175, (7, 5, 4, 4, 3, 5, 4, 10, "3+/4+"),
               ["Power Armour", "Iron Halo", "Power Weapon", "Master-crafted Weapon", *sia,
                *std], ["The Legion of One", "Fury Unbound", "Fearless", "Special Issue Ammunition (Sigillite)"]),
        knight("Iacton Qruze — The Half-Heard", 170, (6, 5, 4, 4, 4, 5, 3, 10, "3+/4+"),
               ["Power Armour", "Iron Halo", "Power Weapon", *sia, *std, "Teleport Homer"],
               ["The Half-Heard", "Protect the Innocent, Uphold the Lore", "Stubborn",
                "Special Issue Ammunition (Sigillite)"]),
        knight("Macer Varren — The Emperor's Warhound", 155, (6, 5, 4, 4, 3, 5, 3, 10, "3+/4+"),
               ["Power Armour", "Iron Halo", "Power Weapon", *sia, *std],
               ["Furious Charge", "Warrior Born", "The Emperor's Warhound", "Special Issue Ammunition (Sigillite)"]),
        knight("Tylos Rubio — The Errant Librarian", 180, (5, 5, 4, 4, 3, 5, 3, 10, "3+/5+"),
               ["Power Armour", "Refractor Field", "Force Weapon", *sia, "Psychic Hood", *std],
               ["Psyker", "Acute Senses", "The Errant Librarian", "Special Issue Ammunition (Sigillite)"], powers=3),
    ]


def sig_force():
    links = [category_link(gs.CAT_CONFIG, "Configuration", key="sigf")]
    for name, mn, mx in [("HQ", 1, 1), ("Troops", 1, 1), ("Elites", 0, 1), ("Fast Attack", 0, 0),
                         ("Heavy Support", 0, 0), ("Lords of War", 0, 0), ("Fortification", 0, 0)]:
        cl = category_link(gs.cat(name), name, key="sigf")
        cons = [constraint(k("sigfoc", name, "max"), "max", mx)]
        if mn:
            cons.insert(0, constraint(k("sigfoc", name, "min"), "min", mn))
        cl.append(wrap("constraints", cons))
        links.append(cl)
    links.append(category_link(gs.CAT_TRANSPORT, "Dedicated Transport", key="sigf"))
    return el("forceEntry", {"id": SIG_FORCE, "name": "Agents of the Sigillite Allied Detachment", "hidden": "false"},
              [wrap("categoryLinks", links)])


# ------------------------------------------------------------------------------------------------------ build
def build():
    global SIG_FORCE, CAT_SIG_HQ, CAT_KE, OATH, CHYM_ATTR_CFG, CAT_ELDAR_POWER
    # keep the Legiones Astartes data: a Blackshields force is chosen from the Legiones Astartes Army List
    snap = [copy.deepcopy(d) for d in (ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR)]
    start(ARMY)
    for d, s in zip((ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR), snap):
        d.update(s)
    register_data(rules=RULES, weapons=WEAPONS_, multi_profile=MULTI, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_)

    SIG_FORCE = k("force", "Agents of the Sigillite")
    CAT_SIG_HQ = k("cat", "Agents of the Sigillite HQ")
    CAT_KE = k("cat", "Knight-Errant")
    CAT_ELDAR_POWER = k("cat", "Eldar Psychic Power")
    hide_sig = hide_if(in_force(SIG_FORCE))

    # ---------------------------------------------------------------- configuration
    alleg = allegiance()
    oath, OATH = config("oath", "Oath of Moment", [
        ("Death Seekers", ["Inured to Pain", "The Lure of Battle", "Feel No Pain"]),
        ("Orphans of War", ["Brothers Before Masters", "Brother-Slayers", "No Gods, No Masters"]),
        ("Outlanders", ["Void Reavers", "Unsanctioned Weaponry", "The Shadow of Oblivion"]),
        ("Chymeriae", ["Chymeriae Attributes", "Shunned and Distrusted"]),
        ("The Alien Brotherhood", ["Unlikely Allies", "Forbidden Arsenals", "Eldritch Tutelage",
                                   "Outcasts Among Outcasts"]),
        ("Ashes of the Armoury", ["Desperate Warriors", "Scarce Ammunition", "Scavengers", "The Last Magazine"])])
    add_to(oath, "infoLinks", rules_links(["Blackshields Theme", "Legiones Astartes (Blackshields)",
                                           "Blackshield Armoury", "Blackshield Weapons", "Xenos", "Shattered Legions",
                                           "The Whole is Greater than the Sum", "Shattered Legions Restrictions"],
                                          key=k("theme")))
    attr, _ = config("chym-attr", "Chymeriae Attribute", [("Gene-Bulked", ["Gene-Bulked"]),
                                                          ("Lone Wolves", ["Lone Wolves"]),
                                                          ("Berserkers", ["Berserkers", "Fear", "Fleet"])])
    no_chym = lacks(OATH["Chymeriae"], "force")
    add_mods(attr, [modifier("set", "hidden", "true", groups=[any_of(no_chym, in_force(SIG_FORCE))]),
                    modifier("set", uid(attr.get("id"), "min"), 0,
                             groups=[any_of(lacks(OATH["Chymeriae"], "force"), in_force(SIG_FORCE))]),
                    error_if("A Chymeriae Attribute may only be chosen with the Chymeriae Oath of Moment.",
                             [lacks(OATH["Chymeriae"], "force")])])
    for cfg in (alleg, oath):
        add_mods(cfg, [hide_if(in_force(SIG_FORCE)),
                       modifier("set", uid(cfg.get("id"), "min"), 0, conds=[in_force(SIG_FORCE)])])

    # ---------------------------------------------------------------- Legiones Astartes Army List (Blackshields)
    praetor, cent = L.praetor(), L.centurion()
    base = [praetor, cent, L.tactical(), L.assault(), L.breacher(), L.recon()]
    trans = [L.rhino(), L.drop_pod(), L.dreadclaw()]
    more, more_shared = L2.extend({u.get("name"): u for u in base}, trans)
    praetor_only = {uid("unit", f"praetor-{x}") for x in ("hg", "cs", "tcs")}
    more_shared = [e for e in more_shared if e.get("id") not in praetor_only]
    legion_roots = base[1:] + more          # no Praetors in a Blackshields force
    # no Rite of War in a Blackshields force (author's answer): the entry stays (other entries refer to it) but is
    # hidden and may not be selected
    for e in legion_roots:
        if e.get("id") == L2.RITE_ENTRY:
            add_mods(e, [modifier("set", "hidden", "true"), modifier("set", uid(L2.RITE_ENTRY, "max"), 0),
                         modifier("add", "error", "A Blackshields force may not use a Rite of War.")])
    # Chaplains are forbidden by Orphans of War and The Alien Brotherhood
    for e in cent.iter("selectionEntry"):
        if e.get("id") == L.consul_id("Chaplain"):
            ban = [has(OATH["Orphans of War"], "force"), has(OATH["The Alien Brotherhood"], "force")]
            add_mods(e, [modifier("set", "hidden", "true", groups=[any_of(*ban)]),
                         modifier("set", uid(e.get("id"), "max"), 0, groups=[any_of(*ban)])])

    reaver, reaver_retinues = reaver_lord()
    for e in legion_roots + more_shared + reaver_retinues:
        if e.get("id") == L2.RITE_ENTRY:
            continue
        blackshield_unit(e)
    # Reaver Lord: no "Space Marine Armoury" injection (built explicitly), but Ashes of the Armoury applies
    apply_ashes(reaver)
    add_eldritch_tutelage(legion_roots + more_shared + reaver_retinues)
    bs_units = [reaver, marauder_squad(), chymeriae_squad()]
    # Ashes of the Armoury also applies to the Blackshield-specific units (author's answer)
    for e in bs_units[1:]:
        apply_ashes(e)
    for e in bs_units + legion_roots:
        add_mods(e, [hide_if(in_force(SIG_FORCE))])

    # ---------------------------------------------------------------- Agents of the Sigillite
    sig_units = [preceptor(), *knights(), strike_force(), operative_cell(), assassin()]

    units = [alleg, oath, attr] + bs_units + legion_roots + sig_units
    shared = trans + more_shared + reaver_retinues
    root = catalogue(ARMY, units, shared, force_entries=[sig_force()])
    root.insert(1, wrap("categoryEntries", [
        el("categoryEntry", {"id": CAT_SIG_HQ, "name": "Agents of the Sigillite HQ", "hidden": "false"}),
        el("categoryEntry", {"id": CAT_KE, "name": "Knight-Errant", "hidden": "false"}),
        el("categoryEntry", {"id": CAT_ELDAR_POWER, "name": "Eldar Psychic Power", "hidden": "false"})]))

    # No Praetors in a Blackshields force: conditions that look for a Praetor (e.g. the Delegatus Consul, hidden
    # when a Praetor commands) look for the Reaver Lord, the force's senior commander, instead.
    for c in root.iter("condition"):
        if c.get("childId") == L.PRAETOR:
            c.set("childId", reaver.get("id"))

    # ---------------------------------------------------------------- shared item limits
    sse = {e.get("id"): e for e in root.find("sharedSelectionEntries")}

    def item(n):
        return sse[W(n)]
    for n in XENOS_MARKED + ["Ghosthelm", "Spirit Stones", "Shadow Field", "Xenos Combat Drugs",
                             "Deathlock Teleporter", "Mind Projector"]:
        add_mods(item(n), [
            modifier("set", "hidden", "true", groups=[all_of(lacks(OATH["Outlanders"], "force"),
                                                             lacks(OATH["The Alien Brotherhood"], "force"))]),
            modifier("add", "error", f"{n} is Xenos: only an Outlanders or The Alien Brotherhood force may take it.",
                     groups=[all_of(lacks(OATH["Outlanders"], "force"),
                                    lacks(OATH["The Alien Brotherhood"], "force"))])])
    for n in XENOS_CONV:
        add_mods(item(n), [
            modifier("set", "hidden", "true", conds=[lacks(OATH["The Alien Brotherhood"], "force")]),
            modifier("add", "error", f"{n} is a Xenos Weapon: only a force using The Alien Brotherhood Oath may take it.",
                     conds=[lacks(OATH["The Alien Brotherhood"], "force")])])
    # Rad Grenades: Outlanders only (Unsanctioned Weaponry; author's answer)
    add_mods(item("Rad Grenades (Blackshield)"), [
        modifier("set", "hidden", "true", conds=[lacks(OATH["Outlanders"], "force")]),
        modifier("add", "error", "Rad Grenades may only be purchased by Blackshield Characters of an Outlanders force.",
                 conds=[lacks(OATH["Outlanders"], "force")])])
    for n in ("Shadow Field", "Deathlock Teleporter"):
        add_to(item(n), "constraints", [unique(W(n))])
    for n, _ in MISSION:
        add_to(item(n), "constraints", [unique(W(n), scope="force")])
    return root
