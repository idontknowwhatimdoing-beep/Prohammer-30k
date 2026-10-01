"""Exercitus Imperialis (Imperialis Militia / Imperial Army) - Age of Darkness army list for Prohammer 30k.

Structure (see tools/questions/Exercitus Imperialis.md):
- Configuration: Allegiance and "Muster of Worlds: Provenances of War" (up to two Provenances, their points cost is
  paid on the configuration entry instead of on the Force Commander; incompatible pairs, Allegiance limits and the
  Force Commander requirement are errors).
- Provenance-dependent unit options are hidden until the Provenance is chosen in the same Detachment.
- Attached Advisors (Navigator, Memorator, Discipline Masters, Psyker Attaches ...) and the Field Officers are shared
  entries linked from the units they may join, so their 0-1 / 0-n limits count across the whole Detachment.
- Units that "do not occupy a Force Organisation slot" and are not attached (Remembrancer Circle) use the HQ slot plus
  the game system's "Force Org: +1 HQ" category, so they never use up an HQ choice.
"""
from armies.common import *
from armies.common import _negate

ARMY = "Exercitus Imperialis"

# ====================================================================== RULES
PROV_TEXT = {
    "Warrior Elite": (50, "Every model with the Provenance special rule receives +1 Leadership, to a maximum of 9. "
                          "Inducted Levy Squads gain the Support Squad special rule."),
    "Gene-Crafted": (100, "Every model with the Provenance special rule receives +1 Strength and +1 Initiative, to a "
                          "maximum of Strength 4 and Initiative 4 (Ogryn Brutes may instead increase their Strength to a "
                          "maximum of 6). Affected models may never benefit from Feel No Pain, regardless of its source."),
    "Cyber-Augmetics": (35, "Every model with the Provenance special rule receives a 6+ Invulnerable Save; a model which "
                            "already has an Invulnerable Save improves it by 1, to a maximum of 3+. Affected units "
                            "subtract 1 from Sweeping Advance rolls. May not be selected alongside Gene-Crafted."),
    "Alchem-Jackers": (35, "Models with the Provenance special rule ignore all negative Leadership modifiers when "
                           "taking Morale tests in the Assault phase. If an affected unit fails a Morale test caused by "
                           "Shooting phase casualties it becomes Pinned instead of Falling Back. FRENZON: any unit with "
                           "the Provenance special rule may take Frenzon Dispensers (+25 points per unit, Ogryn Brute "
                           "Squads +50 points)."),
    "Survivors of the Dark Age": (75, "Every model with the Provenance special rule improves its Armour Save by 1, to a "
                                      "maximum of 3+. All compulsory Troops choices must be Imperialis Militia "
                                      "Grenadier Squads. Inducted Levy Squads gain Support Squad. ADVANCED WEAPONS: "
                                      "Platoon Command Cadres, Grenadier Squads, Veteran Squads and Gene-Trooper "
                                      "Squads may upgrade their advanced weapons (+20 points per squad; if one squad "
                                      "of a type buys it, every squad of that type must): +1 Strength to laspistols, "
                                      "hellpistols, lasguns, lascarbines, laslocks and hellguns. ADVANCED TRANSPORTS: "
                                      "a Grenadier, Veteran or Gene-Trooper Squad or Platoon Command Cadre of no more "
                                      "than ten models may select an Imperial Rhino or an Imperialis Militia Land "
                                      "Raider as a Dedicated Transport. May not be selected alongside Cult Horde or "
                                      "Clanholds of the Deep Worlds."),
    "Feral Warriors": (35, "Every model with the Provenance special rule receives +1 Weapon Skill, to a maximum of 4 "
                           "(Ogryn Brutes instead receive +1 Attack). The army may not include more Vehicle units than "
                           "Infantry units. BLADE AND FURY: any unit with the Provenance special rule other than an Ogryn "
                           "Brute Squad may receive +1 Attack (+25 points per squad; Independent Characters +10 points "
                           "per model)."),
    "Abhuman Helots": (35, "Every model with the Provenance special rule receives +1 Toughness and -1 Initiative (minimum "
                           "1). Beastman Auxilia Herds and Ogryn Brute Squads are always eligible. DISCIPLINE COLLARS: any "
                           "unit with the Provenance special rule may take Discipline Collars (+20 points per unit)."),
    "Cult Horde": (35, "Every model with the Provenance special rule gains Fearless and may re-roll failed To Hit rolls "
                       "in the first round of any close combat. Affected units must charge whenever able (controlling "
                       "player chooses the target) and may charge after firing weapons that would normally prevent it, "
                       "but then get no bonus Attack for charging. All shooting by affected models is resolved at "
                       "Ballistic Skill 1 and they may not fire Template or Blast weapons. The army may not include "
                       "Imperialis Militia Grenadier Squads or Clone Auxilia Cohorts. The Force Commander becomes a Cult "
                       "Demagogue. May not be selected alongside Survivors of the Dark Age. Traitor only."),
    "Tainted Flesh": (50, "Every model with the Provenance special rule receives +1 Toughness (maximum 5) and -1 "
                          "Leadership (minimum 5). The army may select Mutant Spawn as Heavy Support choices. Beastman "
                          "Auxilia Herds may increase their Strength by 1 (+2 points per model). The Force Commander may "
                          "purchase a Tainted Weapon. May not be selected alongside Gene-Crafted or Survivors of the Dark "
                          "Age."),
    "Frontier Marksmen": (50, "All non-Ogryn Infantry models with the Provenance special rule and Ballistic Skill 3 may "
                              "re-roll To Hit rolls of 1 with ranged weapons (not with plasma weapons or sniper rifles). "
                              "Imperialis Militia Reconnaissance Squads lose Support Squad and may fulfil compulsory "
                              "Troops choices. One model in each Infantry Squad or Platoon Command Cadre may replace its "
                              "lasgun, lascarbine or autogun with a sniper rifle (+5 points). CAMELEOLINE: Platoon "
                              "Command Cadres, Infantry, Grenadier, Fire Support, Reconnaissance, Veteran and Combat "
                              "Engineer Squads may purchase Cameleoline (+10 points per squad). May not be selected "
                              "alongside Cult Horde."),
    "Mechanised Regiments": (25, "May only be selected alone. Platoon Command Cadres, Infantry, Grenadier, Fire Support, "
                                 "Reconnaissance, Veteran, Gene-Trooper and Combat Engineer Squads and Clone Auxilia "
                                 "Cohorts must purchase a Chimera (a five-model Veteran, Gene-Trooper or Combat Engineer "
                                 "Squad may select a Centaur instead) and must begin the battle embarked. Militia "
                                 "Infantry Squads consist of 1 Sergeant and 9 Militia Auxiliaries (40 points). Grenadier "
                                 "Squads may contain no more than ten models; Fire Support Squads no more than five Heavy "
                                 "Weapon Teams. An Ogryn Brute Squad of no more than six Ogryn Brutes may take a Chimera. "
                                 "Inducted Levy Squads may not be selected. Independent Characters, Discipline Masters, "
                                 "Rogue Psykers and Medicae Orderlies must be attached to units with sufficient Transport "
                                 "Capacity to begin on the table."),
    "Clanholds of the Deep Worlds": (60, "Every model with the Provenance special rule receives +1 Toughness (maximum 4) "
                                         "and -1 Initiative (minimum 1). Affected units may re-roll failed Morale tests "
                                         "caused by Shooting phase casualties. No Cavalry Squadrons. SONS OF THE DEEP "
                                         "HOLDS: Combat Engineer Squads may be selected as Troops (and fulfil compulsory "
                                         "Troops); all Combat Engineer Squads gain Move Through Cover. MINERS AND "
                                         "DELVERS: Platoon Command Cadres, Infantry, Veteran, Gene-Trooper and Combat "
                                         "Engineer Squads may purchase Mining Equipment (+10 points per squad). HEAVY "
                                         "INDUSTRIAL WEAPONS: Fire Support and Combat Engineer Squads may select Mining "
                                         "Lasers and industrial heavy weapons. HEAVY PANOPLIES: Veteran and Gene-Trooper "
                                         "Squads may exchange their armour for Power Armour (+5 points per model); one "
                                         "Veteran or Gene-Trooper Squad may instead take Terminator Armour (+15 points per "
                                         "model; max five models, no Sweeping Advances, no Chimera or Centaur, may select "
                                         "an Imperialis Militia Land Raider, may use Terminator weapons). The Force "
                                         "Commander may purchase Terminator Armour. May not be selected alongside "
                                         "Survivors of the Dark Age."),
    "Paragons of Humanity": (100, "Paragon Units: Veteran Squads, Gene-Trooper Squads and Force Commanders. Their models "
                                  "receive +1 Weapon Skill (maximum 5); Veterans and Gene-Troopers receive +1 Attack; the "
                                  "Force Commander receives +1 Attack. PARAGON PANOPLY: Veteran and Gene-Trooper Squads "
                                  "may exchange their armour for Power Armour (+5 points per model); any model in such a "
                                  "squad may exchange its close combat weapon for a Power Weapon (+5 points per model). "
                                  "EXEMPLAR GUARD: one Veteran or Gene-Trooper Squad may become an Exemplar Guard (+10 "
                                  "points per model; +1 Toughness to a maximum of 4, Stubborn, 5+ Invulnerable Save; no "
                                  "more than five models; may select an Imperialis Militia Land Raider). Inducted Levy "
                                  "Squads gain Support Squad. The army must include at least one Veteran or Gene-Trooper "
                                  "Squad. May not be selected alongside Cult Horde or Abhuman Helots. COMPANIONS OF THE "
                                  "TEN THOUSAND (+25 points): the army may include a Legio Custodes Allied Contingent; a "
                                  "Legio Custodes army may include this Exercitus Imperialis Allied Contingent and ignores "
                                  "it for Custodes rules restricting Allied Contingents."),
    "Horse Lords": (40, "Imperialis Militia Cavalry Squadrons may be selected as Troops choices and fulfil compulsory "
                        "Troops. MOUNTED COMMAND: a Force Commander may be mounted (+10 points), a Platoon Command Cadre "
                        "(+5 points per model): Unit Type Cavalry and Fleet of Hoof; a mounted Platoon Command Cadre may "
                        "not select a Chimera or Centaur. RIDERS OF THE HOST: Cavalry Squadrons may include up to fifteen "
                        "models; Hunting Lances cost +2 points per model; one Cavalry Squadron may be upgraded to "
                        "Veteran Riders (+3 points per model: +1 WS to a maximum of 4, +1 Ld to a maximum of 8). XENO "
                        "CAVALRY: Xeno Mounts cost +3 points per model. May not be selected with Mechanised Regiments."),
    "Drop Assault Regiments": (50, "DROP TROOPS: Platoon Command Cadres, Infantry, Grenadier, Fire Support, "
                                   "Reconnaissance, Veteran, Gene-Trooper and Combat Engineer Squads may purchase "
                                   "Grav-chutes (+2 points per model, every model); such units may not select a Dedicated "
                                   "Transport, may always be placed in Reserve and may Deep Strike. JUMP ASSAULT "
                                   "FORMATIONS: Jump Assault Squads may be selected as Troops and fulfil compulsory Troops. "
                                   "AIRBORNE COMMAND: Force Commander Jump Pack +15 points; every model in a Platoon "
                                   "Command Cadre +5 points per model; Discipline Master +10 points; Medicae Orderly +5 "
                                   "points (Unit Type Jump Infantry). DROP SENTINELS: Sentinels may gain Deep Strike (+5 "
                                   "points per Sentinel). LIGHTNING ASSAULT: units with Grav-chutes, Jump Packs or Deep "
                                   "Strike may Deep Strike even in missions that do not normally permit it (normal Reserve "
                                   "rules apply). A unit with Grav-chutes may not begin the battle embarked. May not be "
                                   "selected alongside Mechanised Regiments."),
    "Undying Horde": (75, "Inducted Levy Squads become Zombie Levy Squads (Fearless, Feel No Pain (5+), Slow and "
                          "Purposeful, Poisoned (5+) close combat attacks; no shooting attacks and no ranged weapon "
                          "upgrades). THE DEAD RISE AGAIN: the first time a Zombie Levy Squad is destroyed roll a D6 at "
                          "the end of the phase - on a 4+ it is placed into Reserves at its starting strength; if "
                          "destroyed again after returning it may return again on a 5+; at most twice per battle; "
                          "returned units arrive by Outflank with all upgrades and still count as destroyed for Victory "
                          "Points. NECROMANCER DEMAGOGUE: the Force Commander becomes a Psyker (Mastery Level 1) with one "
                          "Biomancy power and Raise the Dead. BLIGHTED OGRYNS: Ogryn Brute Squads may be upgraded (+3 "
                          "points per model). No Vehicle unit may be selected more than once and the army may include no "
                          "more than three Vehicle units. Traitor only. May not be selected alongside Cult Horde."),
    "Hive Platoons": (35, "HIVE FIGHTERS: Inducted Levy Squads may replace their ranged weapons with two laspistols or two "
                          "autopistols (+1 point per model); Grenadier Squads with two hellpistols or two bolt pistols (+2 "
                          "points per model); every model must make the same exchange and the unit gains Fleet. "
                          "GUNFIGHTERS: a model with two Pistols may fire both at the same target; two Pistols count as "
                          "two close combat weapons. STREET-BORN: a unit upgraded through Hive Fighters may not purchase "
                          "Advanced Weapons, Power Armour, Terminator Armour or Exemplar Guard."),
    "Engineer Corps": (35, "COMBAT ENGINEER FORMATIONS: up to two Combat Engineer Squads may be selected as Troops; one of "
                           "them may fulfil a compulsory Troops choice. FIELD FORTIFICATIONS: any Combat Engineer Squad "
                           "may purchase up to three Razorwire Sections (+2 points each) and then gains Infiltrate; the "
                           "sections are placed within 6\" of the unit when it deploys by Infiltrate, at least one model "
                           "must deploy within 6\" of one of them, and they use the normal Razorwire rules."),
    "Imperial Navy Battalion": (35, "NAVAL OFFICER: the army must include a Force Commander, who must be upgraded to a "
                                    "Naval Officer (+10 points): he gains Void-Hardened Armour and may purchase a Boarding "
                                    "Shield (+5 points). VOID-HARDENED ARMOUR: Platoon Command Cadres, Infantry, Grenadier, "
                                    "Fire Support, Reconnaissance, Veteran, Gene-Trooper and Combat Engineer Squads may "
                                    "purchase it (+2 points per model, every model). BOARDING SECTIONS: Veteran and Combat "
                                    "Engineer Squads may purchase Boarding Shields (+5 points per model, every model)."),
    "Ogryn Workdivision": (35, "HEAVY LABOUR COMPANIES: up to three Ogryn Brute Squads may be selected as Troops and "
                               "fulfil compulsory Troops. INDUSTRIAL CARAPACE: any Ogryn Brute Squad may exchange its armour "
                               "for Carapace Armour for +3 points per model. BONE 'EADS: one Ogryn Brute in each squad may "
                               "be upgraded to a Bone 'ead for free."),
}
PROVS = list(PROV_TEXT)

RULES = {
    "Provenance": "A model with this special rule is affected by any Provenances of War selected for its army (its "
                  "Detachment), unless the Provenance itself states otherwise. Vehicles, Advisors and other units without "
                  "the Provenance special rule are unaffected unless specifically stated.",
    "Muster of Worlds": "An army (Detachment) containing a Force Commander may select up to two different Provenances of "
                        "War. The points cost of each selected Provenance is added to the cost of the Force Commander "
                        "(in this list it is paid on the Provenances of War configuration entry). An army may never "
                        "select more than two Provenances, regardless of the number of Force Commanders.",
    "Support Squad": "A unit with this special rule may not be used to fulfil a compulsory choice on the Force "
                     "Organisation chart.",
    "Commanding Officer": "Any friendly Exercitus Imperialis unit with a model within 12\" of a model with this special "
                          "rule may use that model's Leadership when taking Morale or Pinning tests. Not while the model "
                          "is Falling Back, Pinned or engaged in close combat. If more than one Commanding Officer is in "
                          "range, the controlling player chooses which Leadership value is used.",
    "Planetary Overlord": "A Planetary Overlord gains +1 Leadership, to a maximum of 9. The range of his Commanding "
                          "Officer special rule is increased to 18\".",
    "Cult Demagogue": "If the army has selected the Cult Horde Provenance, the Force Commander becomes a Cult Demagogue: "
                      "he gains Preferred Enemy (Loyalists) and may exchange his close combat weapon for a Tainted Weapon "
                      "for +5 points.",
    "Necromancer Demagogue": "With the Undying Horde Provenance the Force Commander gains Psyker (Mastery Level 1), may "
                             "generate one psychic power from the Biomancy discipline and knows Raise the Dead: instead of "
                             "using another psychic power that turn, select one destroyed Zombie Levy Squad still eligible "
                             "to return through The Dead Rise Again; if the Psychic Test is passed it immediately returns "
                             "(expending one of its returns), placed wholly within 6\" of the Force Commander and more than "
                             "1\" from any enemy. It may not charge that turn; if it cannot be placed it goes into Reserves "
                             "and enters by Outflank.",
    "Naval Officer": "Imperial Navy Battalion: a Naval Officer gains Void-Hardened Armour and may purchase a Boarding "
                     "Shield for +5 points.",
    "Attached Advisor": "A model with this special rule does not occupy a Force Organisation slot and may not be used to "
                        "fulfil a compulsory HQ choice. Before deployment it must be assigned to an eligible friendly unit "
                        "as described in its unit entry; it then becomes part of that unit and may not leave it. Unless "
                        "specifically stated otherwise, only one model with the Attached Advisor special rule may be "
                        "assigned to each unit.",
    "Instil Order": "While a Discipline Master is attached to a unit, the Leadership of every model in that unit is "
                    "increased by 1, to a maximum of 8. Whenever the unit fails a Leadership, Morale or Pinning test the "
                    "controlling player may re-roll it; if he does, the unit immediately suffers D3 Wounds with no Armour "
                    "Saves (not allocated to the Discipline Master, Independent Characters or Medicae Orderlies). The "
                    "second result must be accepted.",
    "Discipline Master Cadre": "0-1 Discipline Master Cadre of 1-5 Discipline Masters. The Cadre does not occupy a Force "
                               "Organisation slot and may not fulfil a compulsory HQ choice. Each Discipline Master must "
                               "be assigned to a different friendly Infantry unit before deployment and may not leave it.",
    "Warp Sight": "Whenever an enemy unit enters play by Deep Strike within 4D6\" of the Navigator, the Navigator and his "
                  "unit may immediately make a normal shooting attack against it (after it is placed, before it may "
                  "act), counting as stationary. Once per enemy turn. The Navigator must be assigned to the Force "
                  "Commander's unit or a Platoon Command Cadre and does not benefit from Provenances of War.",
    "Master of the Fleet": "A Master of the Fleet must be assigned to the Force Commander's unit or a Platoon Command "
                           "Cadre. He may purchase an Orbital Bombardment; only one Master of the Fleet in the army may "
                           "do so.",
    "Witness to Valour": "Once per battle, at the beginning of any friendly turn: until the beginning of the controlling "
                         "player's next turn, the Memorator's unit and all friendly Exercitus Imperialis units with a "
                         "model within 6\" may re-roll failed Morale and Pinning tests (the second result stands). A "
                         "Memorator must be assigned to the Force Commander's unit or a Platoon Command Cadre and does not "
                         "benefit from Provenances of War.",
    "You're Going in the Soup": "Once per game, immediately after a friendly Militia unit within 12\" of the Company Cook "
                                "wins a close combat, roll a D6 (effect lasts until the end of the next turn): 1 That "
                                "Wasn't Chicken... - the unit must immediately take a Morale Check; 2-3 Needs Salt - no "
                                "effect; 4-5 A Proper Meal - +1 Leadership; 6 Seconds! - the unit becomes Fearless. The "
                                "Company Cook must be assigned to the Force Commander's unit or a Platoon Command Cadre.",
    "At Your Service, Sir!": "The Personal Aide must be assigned to the Force Commander's unit. Once per game, when the "
                             "Force Commander suffers an unsaved Wound while the Aide is alive, the Wound may instead be "
                             "allocated to the Aide: remove the Aide as a casualty, the Force Commander suffers no Wound.",
    "Psyker Attache": "0-4 Psyker Attaches per army; they do not occupy a Force Organisation slot. Each must be assigned "
                      "to a single friendly Troops choice (never a Command Squad, HQ choice or non-Troops unit), becomes "
                      "part of it and may not voluntarily leave it. Psyker Attaches do not prevent their unit from "
                      "claiming or holding objectives.",
    "Cult Leader": "Psyker (Mastery Level 1), may only select powers from the Telepathy discipline. FANATICAL FOLLOWERS: "
                   "a unit containing a Cult Leader gains Zealot. OUTSIDE THE CHAIN OF COMMAND: the unit may not use the "
                   "Leadership of another friendly model and may not benefit from friendly rules, abilities or wargear "
                   "that improve its Leadership or Morale (it may claim objectives as normal) - unless the army uses a "
                   "Cult Provenance or other Cult army rule, in which case it benefits normally.",
    "Prophet": "Psyker (Mastery Level 1), may only select powers from the Divination discipline. LOWLY SEER: a Prophet "
               "has no additional psychic disciplines and may never exchange Divination for another discipline.",
    "Rogue Psyker": "Traitor only: may only be included in an army that has selected the Cult Horde Provenance. Occupies "
                    "an HQ choice but may not fulfil a compulsory HQ choice and does not benefit from Provenances of War. "
                    "A Rogue Psyker may use one psychic power per turn and must purchase at least one Rogue Psyker "
                    "psychic power (+20 points each).",
    "Alpha Psyker": "An Alpha Psyker (Rogue Alpha profile) may use up to two psychic powers per turn, although the same "
                    "power may not be used more than once in the same turn.",
    "Amuse Me, Jester!": "The Company Jester must be assigned to a single friendly Troops choice (not a Command Squad, HQ "
                         "or non-Troops unit). Once per game, immediately after his unit fails a Morale Check (before it "
                         "Falls Back), roll a D6: 2-6 That's the Spirit! - the check is treated as passed; 1 There Goes "
                         "Kevin... - remove the Jester as a casualty, the failed check stands.",
    "Chronicler of Deeds": "The Scribe Historicus must be assigned to the Force Commander's unit. While he is alive, the "
                           "Force Commander and his unit gain Counter-Attack.",
    "Prepared Fire": "The Locus Scribii must be assigned to a single friendly Troops choice. In its Shooting phase the "
                     "unit may choose not to fire any weapons and place a Prepared Fire marker. Until the beginning of "
                     "its next turn, the first time it fires as part of Overwatch, First Fire or another enemy-turn "
                     "reaction, it may fire twice (resolve the first attack completely first), then the marker is "
                     "removed. Unused markers are removed at the start of its next turn; never more than one marker. "
                     "ADMINISTRATUM DATA-SLATE: the Locus Scribii himself does not fire twice.",
    "Surveyed Ground": "Each Cartographica Adept must be assigned to a single friendly Troops choice (no unit may contain "
                       "more than one). After terrain is placed but before deployment, nominate one terrain feature per "
                       "Adept. While the Adept and his unit are within it, the unit has Move Through Cover and its Cover "
                       "Save from that feature improves by +1 (maximum 3+). Lost if the Adept is slain.",
    "Tank Commander": "A vehicle upgraded with a Militia Tank Commander increases its Ballistic Skill to 4. The Tank "
                      "Commander cannot leave the vehicle and is slain if it is destroyed. He does not occupy a Force "
                      "Organisation slot and may not fulfil a compulsory HQ choice. 0-1 per army; eligible: a Leman Russ "
                      "of a Militia Auxiliary Battle Tank Squadron or an Auxilia Malcador Heavy Tank.",
    "Command Tank": "The vehicle gains Improved Comms at no additional cost. The Tank Commander and his vehicle do not "
                    "benefit from Provenances of War unless a Provenance specifically states that it affects vehicles.",
    "Attached Deployment": "Before deployment each Medicae Orderly must be assigned to a Platoon Command Cadre, "
                           "Imperialis Militia Infantry Squad, Grenadier Squad or Fire Support Squad and may not leave it. "
                           "More than one Medicae Orderly may be assigned to the same unit.",
    "It's Dark in There!": "During the battle an Ogryn Brute Squad may only embark upon a Transport if a friendly Force "
                           "Commander, Platoon Commander or Discipline Master is within 12\". It may begin the battle "
                           "embarked. A squad including an Ogryn Bone 'ead ignores this restriction.",
    "Blessing of the Machine God": "If an Enginseer Adept is in base contact with a damaged friendly vehicle at the "
                                   "beginning of his turn he may repair it instead of moving: choose one Immobilised or "
                                   "Weapon Destroyed result and roll a D6, +1 for each accompanying Technical Servitor; on "
                                   "6+ it is repaired (a repaired weapon may fire that turn, a repaired vehicle may move).",
    "Enginseer Auxilia": "Up to two Enginseer Auxilia may be selected as a single Elites choice; they deploy "
                         "simultaneously but operate as separate units. An Enginseer Adept is an Independent Character "
                         "unless accompanied by Servitors, in which case he and his Servitors form a single unit (he "
                         "becomes an Independent Character again if all Servitors are slain).",
    "Hardened Veterans": "A unit with this special rule may re-roll failed Morale tests.",
    "Sappers": "Combat Engineers add +1 to Armour Penetration rolls against bunkers and fortifications. When crossing a "
               "minefield, a Combat Engineer only triggers a mine on a roll of 6.",
    "Disposable": "The opposing player receives no Victory Points specifically for destroying a unit with this special "
                  "rule. It otherwise counts normally for objectives or mission conditions based on units destroyed.",
    "Conditioned Cohort": "The unit may re-roll failed Morale and Pinning tests. A Clone Auxilia Cohort may not use the "
                          "Leadership of another model through the Commanding Officer special rule.",
    "Fleet of Hoof": "Instead of shooting, a unit with this special rule may move an additional D6\" in the Shooting "
                     "phase. This movement is unaffected by Difficult Terrain.",
    "Gunfighters": "A model armed with two pistols may fire both in the Shooting phase (at the same target). If both have "
                   "the same profile, resolve the attack as though the weapon were Assault 2; two different pistols each "
                   "fire one shot separately. Both pistols count as single-handed close combat weapons as normal.",
    "Amphibious": "Rivers, streams, lakes and similar water features count as clear terrain for this vehicle.",
    "Fire Points (Top Hatch)": "If one or more passengers fire from the top hatch, the vehicle counts as Open-topped "
                               "until the beginning of its next turn.",
    "Easy to Repair": "If the vehicle is Immobilised, its crew may attempt to repair it instead of firing in the Shooting "
                      "phase: on a 6 the Immobilised result is repaired.",
    "Artillery Tractor": "The vehicle may tow a friendly Artillery model: if it begins its Movement phase in contact with "
                         "a friendly Artillery model that has not moved, place the Artillery model in contact with it "
                         "after it moves. The Artillery model and crew may not move or fire in a turn it was towed.",
    "Remote Control": "The Cyclops may only move or detonate while its Operator is within 48\"; otherwise (or if the "
                      "Operator is slain) it takes no actions until the Operator is again in range. The Operator may "
                      "control it while embarked in a Transport.",
    "Demolition Vehicle": "In the Shooting phase the Cyclops may be detonated instead of making a normal shooting attack: "
                          "centre the Ordnance Blast marker over it and resolve its Demolition Charge attack; the Cyclops "
                          "is then destroyed.",
    "Fragile": "Any Glancing or Penetrating Hit automatically destroys a vehicle with this special rule.",
    "Weapons Platform": "A Rapier Carrier and its crew are treated as an Artillery unit. Only the Militia Auxiliary crew "
                        "benefit from Provenances of War, not the Rapier Carriers.",
    "Immobile Artillery": "An Artillery model with this special rule may not move under its own power; it may only change "
                          "position through a rule that allows it to be transported or towed.",
    "Indirect Fire": "An Earthshaker cannon equipped for Indirect Fire may target units outside line of sight; it then "
                     "becomes a Guess-range Barrage weapon with a range of 36\"-240\".",
    "High-speed Drive": "The vehicle may move up to 12\" in its Movement phase. If it moves more than 6\" it may not fire "
                        "in the following Shooting phase; if it moves no more than 6\" it fires normally using the "
                        "Super-heavy Vehicle rules.",
    "Siege Armour": "A Malcador with Siege Armour has Front Armour 14, loses High-speed Drive and may never move more than "
                    "6\" in its Movement phase.",
    "Heavily Armoured Prow": "The vehicle has a 5+ Invulnerable Save against attacks striking its Front Armour, improved "
                             "to 4+ against Blast and Template weapons.",
    "Reduced Blast": "If the vehicle is destroyed and a roll is made on the Super-heavy Vehicle Catastrophic Damage table, "
                     "subtract 2 from the result (minimum 1).",
    "Gorgon Transport": "Up to two units may embark upon or disembark from the Gorgon in the same turn. An Imperialis "
                        "Militia Infantry Platoon or Inducted Levy Squad may select a Gorgon as a Dedicated Transport; for "
                        "a Platoon, up to two units of that Platoon may begin the battle embarked in it.",
    "Random Attacks": "At the beginning of each Assault phase roll a D6 for each Mutant Spawn: the result is its Attacks "
                      "characteristic for that Assault phase.",
    "Mutated Beyond Reason": "After deployment, before the first turn, roll a D3 for the unit: 1 Armoured Hide - 5+ Armour "
                             "Save; 2 Grasping Claws and Flailing Pseudopods - each Mutant Spawn may re-roll results of 1 "
                             "for Random Attacks; 3 Toxic Plasm - close combat attacks gain Rending.",
    "Blind Aggression": "The unit must charge an enemy whenever able (controlling player chooses if several are eligible) "
                        "and must always make a Sweeping Advance when permitted.",
    "Special Selection (Mutant Spawn)": "Mutant Spawn may only be selected by an army with the Tainted Flesh Provenance.",
    "Vehicle Squadron": "The vehicles form a squadron and follow the Vehicle Squadron rules of ProHammer Classic.",
    "Super-heavy Tank": "Follows the Super-heavy Vehicle (Tank) rules of ProHammer Classic.",
    "Infantry Platoon": "An Imperialis Militia Infantry Platoon (1 Platoon Command Cadre and 2-5 Imperialis Militia "
                        "Infantry Squads) occupies a single Troops choice. Each unit deploys and operates independently. "
                        "A Platoon Command Cadre selected as part of a Platoon does not occupy an HQ choice.",
    "Zombie Levy": "Undying Horde: the squad is a Zombie Levy Squad - Fearless, Feel No Pain (5+), Slow and Purposeful, "
                   "Poisoned (5+) on all close combat attacks; it may not make shooting attacks or purchase ranged weapon "
                   "upgrades; The Dead Rise Again (see the Undying Horde Provenance).",
    "Blighted Ogryns": "Whenever a Blighted Ogryn is slain, roll a D6 before removing it: on a 5+ centre a Small Blast "
                       "marker over it; every model touched (friend or foe) suffers a Strength 3, AP -, Poisoned (4+) hit.",
    "Exemplar Guard": "Models in an Exemplar Guard receive +1 Toughness (maximum 4), Stubborn and a 5+ Invulnerable Save. "
                      "An Exemplar Guard may contain no more than five models and may select an Imperialis Militia Land "
                      "Raider as a Dedicated Transport. Only one per army.",
    "Veteran Riders": "Veteran Riders receive +1 Weapon Skill (maximum 4) and +1 Leadership (maximum 8). One Cavalry "
                      "Squadron per army.",
    "Razorwire Sections": "Engineer Corps: a Combat Engineer Squad with at least one Razorwire Section gains Infiltrate. "
                          "When it deploys by Infiltrate, place its sections within 6\" of at least one of its models "
                          "(obeying normal terrain and deployment restrictions); at least one model must then be within 6\" "
                          "of one of its sections. Razorwire uses the normal Razorwire terrain rules.",
    "Terminator Panoply": "Clanholds of the Deep Worlds: a squad in Terminator Armour may contain no more than five "
                          "models, may not make Sweeping Advances, may not select a Chimera or Centaur, may select an "
                          "Imperialis Militia Land Raider and may use Terminator weapons. Only one squad per army.",
    "Lord Commander": "If this character is included in an Exercitus Imperialis Primary Detachment and is eligible to be "
                      "the army's Warlord, he or she must be selected as its Warlord. Counts as a Force Commander for all "
                      "rules and army construction purposes, including Muster of Worlds.",
    "Veteran of the Expeditionary Fleets": "Friendly Exercitus Imperialis Infantry units within 18\" of Hektor Varvarus "
                                           "may re-roll failed Morale and Pinning tests (the second result stands).",
    "A Hundred Compliances": "After both armies have deployed, before the first turn, choose one friendly Exercitus "
                             "Imperialis unit: redeploy it anywhere in your Deployment Zone, or place it into Reserve. "
                             "While Namatjira is on the battlefield you may re-roll one failed Reserve roll each friendly "
                             "turn.",
    "The Line Must Hold": "After deployment nominate one objective or terrain feature in your Deployment Zone. Friendly "
                          "Exercitus Imperialis Infantry units within 6\" of it gain Stubborn and may always attempt to "
                          "regroup regardless of casualties.",
    "Ruthless Discipline": "At the beginning of each friendly turn nominate one friendly Exercitus Imperialis Infantry "
                           "unit within 12\" of Fayle: until your next turn it gains Fearless and may not voluntarily "
                           "Fall Back.",
    "Hidden Allegiance": "Before deployment nominate one friendly Exercitus Imperialis Infantry unit of no more than ten "
                         "models (not Vehicles, Artillery or units with Bulky models): it gains Infiltrate.",
    "Armoured Spearhead": "At the beginning of each friendly Shooting phase nominate one friendly Exercitus Imperialis "
                          "Vehicle or Vehicle Squadron within 12\" of Kourion's vehicle: it may re-roll one failed To Hit "
                          "roll that phase.",
    "Tyana Kourion": "One vehicle eligible for the Militia Tank Commander upgrade (or a Stormhammer Super-heavy Assault "
                     "Tank) may instead contain Tyana Kourion (+65 points, replacing the Tank Commander upgrade): Ballistic "
                     "Skill 4, Tank Commander, Command Tank and Armoured Spearhead. Kourion may be selected as the army's "
                     "Warlord. Unique.",
    "Veteran Crew": "Aika 73 (Leman Russ Battle Tank, +30 points, Unique): Ballistic Skill 4 and Extra Armour. Once per "
                    "battle, at the beginning of your Movement phase, automatically remove one Engine Damaged or "
                    "Immobilised result.",
    "Flag-Captain of the Conqueror": "Once during each friendly turn one failed Reserve roll for a friendly Flyer or "
                                     "Aeronautica Imperialis unit may be re-rolled. Once per battle Lotara Sarrin may "
                                     "call down one Barrage Bomb Orbital Bombardment without paying its points cost.",
    "Field Officer": "Before deployment this character must be attached to one of the units listed in his entry; he "
                     "becomes part of it for the battle and may not voluntarily leave it. Does not occupy a Force "
                     "Organisation choice.",
    "Jokers' Hetman": "A unit containing Hurtado Bronzi gains Counter-Attack and may use Bronzi's Leadership for Morale "
                      "and Pinning tests. (Bronzi: Imperial Army Veteran Squad or Gene-Trooper Squad.)",
    "Dancers' Hetman": "A unit containing Peto Soneka gains Scout and Move Through Cover; if it already has Scout it also "
                       "gains Outflank. (Soneka: Veteran Squad, Gene-Trooper Squad or Reconnaissance Squad.)",
    "Remembrancer Circle": "Before deployment the Circle may be attached to one friendly Exercitus Imperialis Infantry "
                           "unit; all three Remembrancers become part of it and may not voluntarily leave. The unit "
                           "benefits from Witness to Valour while at least one Remembrancer lives, up to three times per "
                           "battle. CIVILIAN OBSERVERS: the Remembrancers may never score or contest objectives; if not "
                           "attached they operate as a normal three-model unit. Does not occupy a Force Organisation "
                           "choice.",
    "Szu": "While Ilya Ravallion is on the battlefield, once during each friendly turn you may add +1 to one Reserve roll "
           "(declared before rolling; a natural 1 always fails).",
    "Cumbersome": "A model attacking with a Cumbersome weapon makes only one attack with it in the Assault phase, "
                  "regardless of its Attacks or bonuses, at Weapon Skill 1.",
    "Shell Shock": "Pinning tests caused by a weapon with Shell Shock are taken with a -1 Leadership modifier.",
    "Servo-arm": "A model with a Servo-arm makes one additional close combat attack each Assault phase, resolved "
                 "separately with the Servo-arm profile.",
    "Hunting Lance": "Usable once per battle, in the first round of a close combat in which the bearer charged: +2 "
                     "Strength, +2 Initiative and its attacks ignore Armour Saves; no +1 Attack for two close combat "
                     "weapons. It is then discarded.",
    "Orbital Bombardment": "PLOTTING: after deployment zones are determined, before deployment, nominate a terrain feature "
                           "as the target. RESERVES: the bombardment begins in Reserve (you may choose not to roll); once "
                           "available it strikes in every subsequent friendly Shooting phase. PLACEMENT: place the Blast "
                           "marker anywhere within the nominated terrain feature. INACCURACY: scatter normally; an arrow "
                           "doubles the distance; a Hit still scatters the distance rolled in the direction of the small "
                           "arrow on the Hit symbol. Orbital Bombardments count as Ordnance Barrages and cause Pinning.",
    "Siege Shells (Griffon)": "A Griffon with Siege Shells may fire them instead of its normal Heavy Mortar ammunition: "
                              "small Blast marker but Ordnance; 2D6+5 armour penetration against bunkers and "
                              "fortifications; models sheltering inside a building struck are affected on a 4+ instead "
                              "of 6.",
    "Siege Shells (Medusa)": "A Medusa siege gun with Siege Shells may fire them instead of its normal ammunition: 2D6+10 "
                             "armour penetration against bunkers and fortifications; models sheltering inside a building "
                             "struck are affected on a 4+ instead of 6.",
}
for _n, (_c, _t) in PROV_TEXT.items():
    RULES[f"Provenance: {_n}"] = f"+{_c} points. {_t}"

WEAPONS = {
    # pistols & basic
    "Autopistol": ('12"', "3", "-", "Pistol"),
    "Laspistol": ('12"', "3", "-", "Pistol"),
    "Blast Pistol": ('6"', "5", "-", "Pistol, Twin-linked, Gets Hot"),
    "Bolt Pistol": ('12"', "4", "5", "Pistol"),
    "Hellpistol": ('12"', "3", "5", "Pistol"),
    "Hand Flamer": ("Template", "3", "6", "Pistol"),
    "Needle Pistol": ('12"', "2", "5", "Pistol, Poisoned, Rending"),
    "Plasma Pistol": ('12"', "7", "2", "Pistol, Gets Hot"),
    "Autogun": ('24"', "3", "-", "Rapid Fire"),
    "Lasgun": ('24"', "3", "-", "Rapid Fire"),
    "Lascarbine": ('24"', "3", "-", "Rapid Fire"),
    "Laslock": ('18"', "4", "-", "Assault 1"),
    "Shotgun": ('12"', "3", "-", "Assault 2"),
    "Boltgun": ('24"', "4", "5", "Rapid Fire"),
    "Twin-linked Bolter": ('24"', "4", "5", "Rapid Fire, Twin-linked"),
    "Combi-bolter": ('24"', "4", "5", "Rapid Fire, Twin-linked"),
    "Storm Bolter": ('24"', "4", "5", "Assault 2"),
    "Hellgun": ('24"', "3", "5", "Rapid Fire"),
    "Ripper Gun": ('12"', "4", "6", "Assault 2"),
    "Sniper Rifle": ('36"', "3", "6", "Heavy 1, Sniper"),
    # special
    "Flamer": ("Template", "4", "5", "Assault 1"),
    "Meltagun": ('12"', "8", "1", "Assault 1, Melta"),
    "Plasma Gun": ('24"', "7", "2", "Rapid Fire, Gets Hot"),
    "Heavy Stubber": ('36"', "4", "6", "Heavy 3"),
    "Twin-linked Heavy Stubber": ('36"', "4", "6", "Heavy 3, Twin-linked"),
    "Rotor Cannon": ('30"', "3", "6", "Salvo 3/4"),
    "Volkite Charger": ('15"', "5", "5", "Assault 2, Rending"),
    "Phased Plasma-fusil": ('24"', "6", "3", "Salvo 2/3"),
    "Graviton Gun": ('18"', "Special", "4", "Heavy 1, Blast, Concussive, Graviton"),
    # heavy
    "Heavy Flamer": ("Template", "5", "4", "Assault 1"),
    "Heavy Bolter": ('36"', "5", "4", "Heavy 3"),
    "Twin-linked Heavy Bolter": ('36"', "5", "4", "Heavy 3, Twin-linked"),
    "Multi-Laser": ('36"', "6", "6", "Heavy 3"),
    "Twin-linked Multi-Laser": ('36"', "6", "6", "Heavy 3, Twin-linked"),
    "Autocannon": ('48"', "7", "4", "Heavy 2"),
    "Twin-linked Autocannon": ('48"', "7", "4", "Heavy 2, Twin-linked"),
    "Lascannon": ('48"', "9", "2", "Heavy 1"),
    "Twin-linked Lascannon": ('48"', "9", "2", "Heavy 1, Twin-linked"),
    "Multi-Melta": ('24"', "8", "1", "Heavy 1, Melta"),
    "Plasma Cannon": ('36"', "7", "2", "Heavy 1, Blast, Gets Hot"),
    "Mortar": ('12-48"', "4", "6", "Heavy 1, Blast, Barrage, Pinning"),
    "Hunter-Killer Missile": ("Unlimited", "8", "3", "Heavy 1, One Use"),
    "Quad Heavy Bolter": ('36"', "5", "4", "Heavy 6, Twin-linked"),
    "Quad Multi-Laser": ('36"', "6", "6", "Heavy 6, Twin-linked"),
    "Thudd Gun": ('12-60"', "5", "5", "Heavy 4, Blast, Barrage, Shell Shock"),
    "Laser Destroyer": ('48"', "10", "1", "Heavy 1, Twin-linked"),
    "Gorgon Mortar Battery": ('12-48"', "5", "5", "Heavy 4, Blast, Barrage, Pinning, One Use"),
    "Mining Laser": ('24"', "9", "2", "Heavy 1"),
    # vehicle & ordnance
    "Exterminator Autocannon": ('48"', "7", "4", "Heavy 4, Twin-linked"),
    "Battle Cannon": ('72"', "8", "3", "Ordnance 1, Large Blast"),
    "Demolisher Cannon": ('24"', "10", "2", "Ordnance 1, Large Blast"),
    "Vanquisher Battle Cannon": ('72"', "8", "2", "Heavy 1, Armourbane"),
    "Earthshaker Cannon": ('120"', "9", "3", "Ordnance 1, Large Blast"),
    "Heavy Mortar": ('12-48"', "6", "4", "Ordnance 1, Blast, Barrage"),
    "Medusa Siege Gun": ('36"', "10", "2", "Ordnance 1, Large Blast"),
    "Demolition Charge": ('6"', "8", "2", "Assault 1, Large Blast, One Use"),
    # close combat
    "Close Combat Weapon": ("-", "User", "-", "Melee"),
    "Cooking Utensil": ("-", "User", "-", "Melee (counts as a close combat weapon)"),
    "Augmented Weapon": ("-", "4", "-", "Melee"),
    "Charnabal Sabre": ("-", "User", "-", "Melee, Rending"),
    "Ogryn Close Combat Weapon": ("-", "+1", "-", "Melee"),
    "Power Weapon": ("-", "User", "-", "Melee, Ignores Armour Saves"),
    "Power Fist": ("-", "x2", "-", "Melee, Power Weapon, Unwieldy, Specialist Weapon"),
    "Chainfist": ("-", "x2", "-", "Melee, Power Weapon, Unwieldy, Specialist Weapon, Armourbane"),
    "Lightning Claw": ("-", "User", "-", "Melee, Power Weapon, Re-roll failed To Wound rolls, Specialist Weapon"),
    "Pair of Lightning Claws": ("-", "User", "-", "Melee, Power Weapon, Re-roll failed To Wound rolls, Specialist "
                                                 "Weapon, +1 Attack"),
    "Thunder Hammer": ("-", "x2", "-", "Melee, Power Weapon, Unwieldy, Specialist Weapon, Concussive"),
    "Dreadnought Close Combat Weapon": ("-", "x2", "-", "Melee, Power Weapon, normal Initiative"),
    "Servo-arm": ("-", "8", "2", "Melee, Unwieldy, Servo-arm"),
    "Hunting Lance": ("-", "+2", "-", "Melee, Two-handed, One Use, Hunting Lance"),
    "Tainted Weapon": ("-", "User", "-", "Melee, Specialist Weapon, Instant Death"),
    "Lascutter": ("-", "9", "2", "Melee, Unwieldy, Cumbersome"),
    "Powered Mining Pick": ("-", "+1", "-", "Melee, Rending, Two-handed"),
    "Mutations": ("-", "User", "-", "Melee (claws, fangs, tentacles and other mutations)"),
    # orbital bombardments
    "Lance Strike": ("Orbital", "10", "1", "Ordnance 1, Blast"),
    "Melta Torpedo": ("Orbital", "8", "3", "Ordnance 1, Blast, Armourbane"),
    "Barrage Bomb": ("Orbital", "6", "4", "Ordnance 1, Blast"),
}
MULTI = {
    "Laspistol or Autopistol": {"Laspistol": WEAPONS["Laspistol"], "Autopistol": WEAPONS["Autopistol"]},
    "Lasgun or Autogun": {"Lasgun": WEAPONS["Lasgun"], "Autogun": WEAPONS["Autogun"]},
    "Lascarbine or Autogun": {"Lascarbine": WEAPONS["Lascarbine"], "Autogun": WEAPONS["Autogun"]},
    "Lasgun or Laspistol": {"Lasgun": WEAPONS["Lasgun"], "Laspistol": WEAPONS["Laspistol"]},
    "Two Laspistols or Autopistols": {"Laspistol": WEAPONS["Laspistol"], "Autopistol": WEAPONS["Autopistol"]},
    "Two Bolt Pistols": {"Bolt Pistol": WEAPONS["Bolt Pistol"]},
    "Two Hellpistols": {"Hellpistol": WEAPONS["Hellpistol"]},
    "Grenade Launcher": {"Grenade Launcher - Frag": ('24"', "3", "6", "Assault 1, Blast"),
                         "Grenade Launcher - Krak": ('24"', "6", "4", "Assault 1")},
    "Missile Launcher": {"Missile Launcher - Frag": ('48"', "4", "6", "Heavy 1, Blast"),
                         "Missile Launcher - Krak": ('48"', "8", "3", "Heavy 1")},
    "Rogue Psyker Power": {},
}
del MULTI["Rogue Psyker Power"]
WEAPON_RULES = {
    "Blast Pistol": ["Twin-Linked", "Gets Hot"], "Needle Pistol": ["Poison", "Rending"], "Plasma Pistol": ["Gets Hot"],
    "Plasma Gun": ["Gets Hot"], "Plasma Cannon": ["Gets Hot"], "Meltagun": ["Melta"], "Multi-Melta": ["Melta"],
    "Sniper Rifle": ["Sniper"], "Mortar": ["Pinning"], "Graviton Gun": ["Concussive", "Graviton"],
    "Volkite Charger": ["Rending"], "Vanquisher Battle Cannon": ["Armourbane"], "Chainfist": ["Unwieldy", "Armourbane"],
    "Power Fist": ["Unwieldy"], "Thunder Hammer": ["Unwieldy", "Concussive"], "Servo-arm": ["Unwieldy", "Servo-arm"],
    "Hunting Lance": ["Two-Handed", "Hunting Lance"], "Lascutter": ["Unwieldy", "Cumbersome"],
    "Powered Mining Pick": ["Rending", "Two-Handed"], "Charnabal Sabre": ["Rending"], "Thudd Gun": ["Shell Shock"],
    "Gorgon Mortar Battery": ["Pinning"], "Melta Torpedo": ["Armourbane", "Orbital Bombardment"],
    "Lance Strike": ["Orbital Bombardment"], "Barrage Bomb": ["Orbital Bombardment"],
}
WARGEAR = {
    "Sub-flak Armour": "6+ Armour Save.",
    "Flak Armour": "5+ Armour Save.",
    "Carapace Armour": "4+ Armour Save.",
    "Power Armour": "3+ Armour Save.",
    "Terminator Armour": ("2+ Armour Save and 5+ Invulnerable Save; Relentless; Bulky. May not make Sweeping Advances; "
                          "may not embark on a Chimera, Imperial Rhino or Centaur Light Carrier. Includes no weapons.",
                          ["Relentless", "Bulky"]),
    "Refractor Field": "5+ Invulnerable Save.",
    "Iron Halo": "4+ Invulnerable Save. An army may include no more than one Iron Halo (replaces the Refractor Field).",
    "Cameleoline": ("The model gains Stealth; if every model in the unit has Cameleoline the whole unit benefits.",
                    ["Stealth"]),
    "Vox-caster": "Once per player turn, when a friendly Exercitus Imperialis unit containing a Vox-caster takes a "
                  "Leadership, Morale or Pinning test, it may use the Leadership of a friendly Commanding Officer "
                  "regardless of distance, if that Commanding Officer's unit contains a Vox-caster or Nuncio-vox. A "
                  "Commanding Officer may only provide his Leadership through the Vox Network once per player turn; the "
                  "normal Commanding Officer restrictions apply.",
    "Nuncio-vox": "A friendly unit arriving by Deep Strike within 6\" does not scatter. When a friendly Barrage weapon "
                  "fires, line of sight may be drawn from the bearer (range still from the weapon). The bearer must have "
                  "been on the battlefield at the start of the turn and not be embarked. Also counts as a Vox-caster.",
    "Vexilla": "The unit counts as having inflicted one additional Wound when determining close combat results and may "
               "always attempt to Regroup at its normal Leadership regardless of casualties.",
    "Platoon Standard": "All the benefits of a Vexilla. In addition, friendly Exercitus Imperialis units with a model "
                        "within 24\" (including the bearer's unit) do not take Morale tests for suffering 25% casualties "
                        "from shooting.",
    "Targeter": "The model may measure range before deciding whether to fire. A unit using a Targeter may not fire "
                "Guess-range weapons that Shooting phase.",
    "Infravisor": ("The model gains Night Vision, but it and its unit count as Initiative 1 for Blind tests.",
                   ["Night Vision"]),
    "Improved Comms": "The army may re-roll one Reserve roll each turn; with Preliminary Bombardment it may also re-roll "
                      "one die used to determine whether an enemy unit or obstacle is struck. Multiple sets do not grant "
                      "additional re-rolls.",
    "Medi-pack": ("The bearer and the unit he has joined gain Feel No Pain (5+). Several Medi-packs in one unit do not "
                  "improve this further.", ["Feel No Pain"]),
    "Cyber-familiar": "6+ Invulnerable Save (or improves an existing Invulnerable Save by 1, to a maximum of 3+). The "
                      "bearer may re-roll failed Characteristic tests other than Leadership and failed Dangerous Terrain "
                      "tests.",
    "Digital Lasers": "+1 Attack in close combat.",
    "Frag Grenades": "Use the normal Core Rules.",
    "Krak Grenades": "Use the normal Core Rules.",
    "Melta Bombs": "Use the normal Core Rules.",
    "Frenzon Dispensers": "+1 Attack in any Assault phase in which the unit charges (in addition to the charge bonus). The "
                          "unit must charge an enemy whenever able (controlling player chooses the target) and must "
                          "always make a Sweeping Advance when permitted.",
    "Discipline Collars": ("The unit gains Stubborn. If it fails a Morale test with an unmodified double 6 it is removed "
                           "from play as though destroyed (attached Discipline Masters, Medicae Orderlies and Independent "
                           "Characters instead Fall Back normally).", ["Stubborn"]),
    "Mining Equipment": "The unit treats rubble, ruins, rocky ground, mine workings and similar subterranean or "
                        "industrial terrain as clear terrain for movement (it still receives cover). Models with Mining "
                        "Equipment may select Mining and Industrial weapons where permitted.",
    "Cavalry Mount": "The model changes its Unit Type to Cavalry and gains Fleet of Hoof (the whole unit is Cavalry if "
                     "every model is mounted). Does not alter the rider's characteristics.",
    "Xeno Mount": "Replaces the Cavalry Mount; the rider loses Fleet of Hoof, improves its Armour Save by 1 and the mount "
                  "makes one additional close combat attack each Assault phase at the rider's WS and Initiative, "
                  "Strength 4, normal Armour Saves, unaffected by the rider's weapons.",
    "Jump Pack": "The model changes its Unit Type to Jump Infantry.",
    "Grav-chute": "The unit may always be placed in Reserve and may enter by Deep Strike; unless a Hit is rolled on the "
                  "Scatter dice it counts as landing in Dangerous Terrain (in Difficult Terrain models fail on a 1 or 2; "
                  "arriving without scatter counts as a Hit).",
    "Dozer Blade": "Re-roll a failed Difficult Terrain test if the vehicle moves no more than 6\" that Movement phase.",
    "Extra Armour": "The vehicle treats Crew Stunned results as Crew Shaken.",
    "Searchlight": "In Night Fighting the vehicle may illuminate one enemy unit it spots; other friendly units may fire at "
                   "it without a spotting roll that phase. The vehicle is itself illuminated until the next enemy "
                   "Shooting phase.",
    "Smoke Launchers": "Once per battle, after moving, the vehicle may release smoke instead of firing: until the start "
                       "of its next turn Penetrating Hits count as Glancing Hits.",
    "Armoured Crew Compartment": "The vehicle no longer counts as Open-topped.",
    "Siege Armour": "Front Armour 14; the Malcador loses High-speed Drive and may never move more than 6\".",
    "Indirect Fire": "The Earthshaker cannon may fire indirectly as a Guess-range Barrage weapon (36\"-240\").",
    "Griffon Siege Shells": "Small Blast Ordnance shells; 2D6+5 armour penetration against bunkers and fortifications; "
                            "models inside a building struck are affected on a 4+.",
    "Medusa Siege Shells": "2D6+10 armour penetration against bunkers and fortifications; models inside a building struck "
                           "are affected on a 4+.",
    "Void-Hardened Armour": "The model may re-roll failed Armour Saves caused by Blast or Template weapons. A unit with "
                            "Void-Hardened Armour may not Run or make Sweeping Advances.",
    "Boarding Shield": "Rules referred to the Exercitus Imperialis Armoury but not printed there (see the questions "
                       "file): treated as +1 Armour Save in close combat until clarified.",
    "Razorwire Section": "One section of Razorwire terrain (see Razorwire Sections).",
    "Administratum Data-Slate": "The Locus Scribii himself does not fire twice when Prepared Fire is used.",
    "Surveyor's Auspex": "See Surveyed Ground.",
    "Questionable Props": "See Amuse Me, Jester!",
    "Combat Blades": "The Sentinel increases its Attacks characteristic by 1.",
}

# ============================================================== armoury lists
# The book names armoury sections but prints no list/costs - see questions file (Q3). Costs below are proposals.
ARMOURY = {
    "senior": dict(
        ranged=[("Bolt Pistol", 2), ("Hellpistol", 2), ("Needle Pistol", 5), ("Hand Flamer", 5), ("Blast Pistol", 8),
                ("Plasma Pistol", 10), ("Boltgun", 2), ("Hellgun", 2), ("Shotgun", 0), ("Combi-bolter", 3),
                ("Storm Bolter", 5), ("Volkite Charger", 10), ("Phased Plasma-fusil", 10)],
        ccw=[("Augmented Weapon", 3), ("Charnabal Sabre", 5), ("Power Weapon", 10), ("Lightning Claw", 15),
             ("Power Fist", 15), ("Thunder Hammer", 20)],
        gear=[("Carapace Armour", 5), ("Iron Halo", 15), ("Melta Bombs", 5), ("Demolition Charge", 5),
              ("Cyber-familiar", 10), ("Digital Lasers", 10), ("Vox-caster", 5), ("Nuncio-vox", 10), ("Infravisor", 3),
              ("Cameleoline", 5), ("Targeter", 2)]),
    "junior": dict(
        ranged=[("Bolt Pistol", 2), ("Hellpistol", 2), ("Needle Pistol", 5), ("Hand Flamer", 5), ("Blast Pistol", 8),
                ("Plasma Pistol", 10), ("Boltgun", 2), ("Shotgun", 0), ("Combi-bolter", 3)],
        ccw=[("Augmented Weapon", 3), ("Charnabal Sabre", 5), ("Power Weapon", 10), ("Lightning Claw", 15),
             ("Power Fist", 15)],
        gear=[("Refractor Field", 10), ("Melta Bombs", 5), ("Demolition Charge", 5), ("Cyber-familiar", 10),
              ("Digital Lasers", 10), ("Infravisor", 3), ("Targeter", 2)]),
    "sergeant": dict(
        ranged=[("Bolt Pistol", 2), ("Hellpistol", 2), ("Hand Flamer", 5), ("Plasma Pistol", 10), ("Boltgun", 2),
                ("Shotgun", 0)],
        ccw=[("Charnabal Sabre", 3), ("Power Weapon", 10), ("Power Fist", 15)],
        gear=[("Melta Bombs", 5), ("Demolition Charge", 5), ("Refractor Field", 10), ("Infravisor", 3)]),
    "advisor": dict(
        ranged=[("Bolt Pistol", 2), ("Hellpistol", 2), ("Needle Pistol", 5), ("Plasma Pistol", 10)],
        ccw=[("Charnabal Sabre", 3), ("Power Weapon", 10)],
        gear=[("Carapace Armour", 5), ("Refractor Field", 10), ("Melta Bombs", 5), ("Cyber-familiar", 10)]),
    "bonehead": dict(
        ranged=[], ccw=[],
        gear=[("Krak Grenades", 3), ("Melta Bombs", 5), ("Vox-caster", 5), ("Refractor Field", 10)]),
    "enginseer": dict(
        ranged=[("Bolt Pistol", 2), ("Needle Pistol", 5), ("Plasma Pistol", 10)],
        ccw=[("Lascutter", 5), ("Power Fist", 5), ("Thunder Hammer", 10)],
        gear=[("Melta Bombs", 5), ("Refractor Field", 10), ("Cyber-familiar", 10), ("Digital Lasers", 10),
              ("Infravisor", 3), ("Nuncio-vox", 10)]),
}
VEHICLE_UPGRADES = [("Hunter-Killer Missile", 10), ("Dozer Blade", 5), ("Extra Armour", 10), ("Searchlight", 1),
                    ("Smoke Launchers", 5), ("Improved Comms", 15)]
SENTINEL_UPGRADES = [("Hunter-Killer Missile", 10), ("Extra Armour", 10), ("Smoke Launchers", 5),
                     ("Armoured Crew Compartment", 10)]
SPEEDER_UPGRADES = [("Hunter-Killer Missile", 10), ("Extra Armour", 10), ("Smoke Launchers", 5)]
SUPERHEAVY_UPGRADES = [("Hunter-Killer Missile", 10), ("Searchlight", 1), ("Smoke Launchers", 5), ("Improved Comms", 15)]
TERMINATOR_WEAPONS = [("Storm Bolter", 3), ("Power Weapon", 5), ("Lightning Claw", 10), ("Power Fist", 10),
                      ("Chainfist", 15), ("Thunder Hammer", 15), ("Heavy Flamer", 10)]

SPECIAL_5 = [("Flamer", 6), ("Grenade Launcher", 8), ("Heavy Stubber", 10), ("Meltagun", 10), ("Plasma Gun", 10)]
SPECIAL_4 = [("Flamer", 6), ("Grenade Launcher", 8), ("Meltagun", 10), ("Plasma Gun", 10)]
HWT = [("Mortar", 10), ("Heavy Bolter", 10), ("Autocannon", 15), ("Missile Launcher", 15), ("Lascannon", 25)]

# ============================================================== conditions
P = {}            # provenance name -> option id (set in build)


def pc(name, scope="force"):
    return cond(P[name], scope, "atLeast", 1)


def _mk(c):
    return pc(c) if isinstance(c, str) else c()


def gate_mods(max_id, show=(), hide=()):
    """Hide (and limit to 0) unless any `show` condition holds / when any `hide` condition holds.
    Conditions are provenance names or zero-argument callables returning a condition."""
    mods = []
    if show:
        for tgt, val in (("hidden", "true"), (max_id, 0)):
            if tgt is None:
                continue
            mods.append(modifier("set", tgt, val, groups=[all_of(*[_negate(_mk(c)) for c in show])]))
    if hide:
        for tgt, val in (("hidden", "true"), (max_id, 0)):
            if tgt is None:
                continue
            mods.append(modifier("set", tgt, val, groups=[any_of(*[_mk(c) for c in hide])]))
    return mods


def opt(key, name, cost, items=(), rules_=(), per_unit=None, show=(), hide=(), max_=1, text=None, mods=(),
        constraints=()):
    """An optional purchase. per_unit: unit id -> cost is per model in that unit."""
    eid = k("opt", key, name)
    mx = uid(eid, "max")
    m = list(mods) + gate_mods(mx, show, hide)
    c = cost
    if per_unit:
        c = 0
        m.append(modifier("increment", PTS, cost, repeats=[repeat("model", per_unit, 1)]))
    return entry(eid, name, cost=c, mods=m, constraints=[constraint(mx, "max", max_, auto=True)] + list(constraints),
                 links=[gear(eid, i) for i in items], infolinks=rules_links(list(rules_), key=eid),
                 rules=[rule(uid(eid, "r"), name, text)] if text else [])


def grp(key, title, entries=(), links=(), max_=None, min_=None, mods=(), show=(), hide=(), default=None):
    gid = k("grp", key, title)
    cons = []
    if max_ is not None:
        cons.append(constraint(uid(gid, "max"), "max", max_, auto=True))
    if min_ is not None:
        cons.append(constraint(uid(gid, "min"), "min", min_, auto=True))
    m = list(mods) + gate_mods(uid(gid, "max") if max_ is not None else None, show, hide)
    return group(gid, title, entries=list(entries), links=list(links), constraints=cons, mods=m, default=default)


def armoury(key, section, ranged_default=None, ccw_default="Close Combat Weapon", gear_skip=(), extra_gear=(),
            title=None):
    """Weapon replacement slots and additional wargear from one Armoury section (costs: see questions file)."""
    a = ARMOURY[section]
    out = []
    if ranged_default and a["ranged"]:
        out.append(slot(key, f"Replace {ranged_default}", ranged_default,
                        [x for x in a["ranged"] if x[0] != ranged_default]))
    if ccw_default and a["ccw"]:
        out.append(slot(key, f"Replace {ccw_default}", ccw_default, [x for x in a["ccw"] if x[0] != ccw_default]))
    gear_ = [x for x in a["gear"] if x[0] not in gear_skip] + list(extra_gear)
    if gear_:
        out.append(take(key, "Additional Wargear", gear_))
    sect = {"senior": "Senior Officer", "junior": "Junior Officer", "sergeant": "Militia Sergeant",
            "advisor": "Advisor", "bonehead": "Ogryn Bone 'ead", "enginseer": "Enginseer"}[section]
    gid = k("armoury", key)
    return group(gid, title or f"Exercitus Imperialis Armoury ({sect})", groups=out)


def error_if_conds(text, conds):
    return modifier("add", "error", text, groups=[any_of(*conds)])


def and_group(conds, groups=()):
    return el("conditionGroup", {"type": "and"}, [wrap("conditions", list(conds)), wrap("conditionGroups", list(groups))])


def models_over(u, n):
    return lambda: cond("model", u, "greaterThan", n)


def models_not(u, n):
    return lambda: cond("model", u, "notEqualTo", n)


# ============================================================== shared entries
TRANSPORT = {}       # name -> shared entry id
ADVISOR = {}         # name -> shared entry id
SHARED = []


def dedicated_transport(name, cost, prof, kit, rules_, groups, tprof):
    t = k("transport", name)
    TRANSPORT[name] = t
    SHARED.append(entry(t, name, typ="unit", cost=cost,
                        cats=[category_link(gs.CAT_TRANSPORT, "Dedicated Transport", primary=True, key=t)],
                        profiles=[prof(t), tprof(t)], infolinks=rules_links(rules_, key=t),
                        links=[gear(t, x) for x in kit], groups=groups(t)))


def transports(key, u, options, mech_required=False, grav=None):
    """options: [(transport name, show-conditions or (), hide-conditions or ())]."""
    gid = k("grp", key, "transport")
    mx = uid(gid, "max")
    mn = uid(gid, "min")
    links = []
    for n, show, hide in options:
        lid = uid("link", gid, n)
        lmx = uid(lid, "max")
        links.append(link(lid, TRANSPORT[n], n, mods=gate_mods(lmx, show, hide),
                          constraints=[constraint(lmx, "max", 1, auto=True)]))
    mods = []
    cons = [constraint(mx, "max", 1, auto=True), constraint(mn, "min", 0)]
    if mech_required:
        mods.append(modifier("set", mn, 1, conds=[pc("Mechanised Regiments")]))
    if grav:
        mods += [modifier("set", mx, 0, conds=[cond(grav, u, "atLeast", 1)]),
                 modifier("set", mn, 0, conds=[cond(grav, u, "atLeast", 1)]),
                 modifier("set", "hidden", "true", conds=[cond(grav, u, "atLeast", 1)])]
    return group(gid, "Dedicated Transport", links=links, constraints=cons, mods=mods)


def build_transports():
    dedicated_transport(
        "Chimera", 85, lambda t: vehicle_profile(t, "Chimera", "Vehicle (Tank)", 3, 12, 10, 10),
        ["Multi-Laser", "Heavy Bolter", "Searchlight", "Smoke Launchers"], ["Amphibious", "Fire Points (Top Hatch)"],
        lambda t: [slot(t, "Replace turret-mounted Multi-laser", "Multi-Laser", [("Heavy Bolter", 0),
                                                                                 ("Heavy Flamer", 0)]),
                   slot(t, "Replace hull-mounted Heavy Bolter", "Heavy Bolter", [("Heavy Flamer", 0)]),
                   take(t, "Vehicle Upgrades", [x for x in VEHICLE_UPGRADES if x[0] not in ("Searchlight",
                                                                                           "Smoke Launchers")])],
        lambda t: transport_profile(t, "Chimera", "12 models (each Ogryn Brute counts as two; no Terminator Armour)",
                                    "Rear hull", "Up to six passengers may fire the hull-mounted lasguns; one "
                                                 "passenger may fire from the top hatch"))
    dedicated_transport(
        "Imperial Rhino", 40, lambda t: vehicle_profile(t, "Imperial Rhino", "Vehicle (Tank)", 3, 11, 11, 10),
        ["Storm Bolter", "Searchlight", "Smoke Launchers"], ["Easy to Repair", "Fire Points (Top Hatch)"],
        lambda t: [take(t, "Vehicle Upgrades", [x for x in VEHICLE_UPGRADES if x[0] not in ("Searchlight",
                                                                                           "Smoke Launchers")])],
        lambda t: transport_profile(t, "Imperial Rhino", "10 models (no Ogryn Brutes, no Terminator Armour)",
                                    "One on each side, one at the rear", "Up to two passengers from the top hatch"))
    dedicated_transport(
        "Centaur Light Carrier", 40,
        lambda t: vehicle_profile(t, "Centaur Light Carrier", "Vehicle (Fast, Open-topped)", 3, 11, 10, 10),
        ["Heavy Stubber", "Searchlight", "Smoke Launchers"], ["Artillery Tractor"],
        lambda t: [take(t, "Vehicle Upgrades", [x for x in VEHICLE_UPGRADES if x[0] not in ("Searchlight",
                                                                                           "Smoke Launchers")])],
        lambda t: transport_profile(t, "Centaur Light Carrier", "5 models (no Terminator Armour)", "Open-topped",
                                    "Open-topped"))
    dedicated_transport(
        "Imperialis Militia Land Raider", 235,
        lambda t: vehicle_profile(t, "Land Raider", "Vehicle (Tank)", 3, 14, 14, 14), *land_raider_parts())
    dedicated_transport(
        "Auxilia Gorgon Heavy Transporter", 275, *gorgon_parts())


def land_raider_parts():
    return (["Twin-linked Lascannon", "Twin-linked Lascannon", "Twin-linked Heavy Bolter", "Searchlight",
             "Smoke Launchers"], ["Power of the Machine Spirit", "Assault Vehicle"],
            lambda t: [take(t, "Vehicle Upgrades", [x for x in VEHICLE_UPGRADES if x[0] not in ("Searchlight",
                                                                                               "Smoke Launchers")])],
            lambda t: transport_profile(t, "Land Raider", "10 models (no Ogryn Brutes)", "One at the front, one on each "
                                                                                         "side", "-"))


def gorgon_parts():
    def groups(t):
        mortar = uid(t, "sponsons")
        return [slot(t, "Replace both Twin-linked Autocannons", "Twin-linked Autocannon",
                     [("Twin-linked Multi-Laser", 0), ("Twin-linked Lascannon", 10)]),
                group(mortar, "Replace Gorgon Mortar Battery with sponsons", entries=[
                    entry(uid(mortar, "e"), "Sponsons instead of Gorgon Mortar Battery", constraints=[
                        constraint(uid(mortar, "e", "max"), "max", 1, auto=True)], groups=[
                        slot(uid(mortar, "fwd"), "Forward sponson pair", "Heavy Bolter",
                             [("Heavy Flamer", 0), ("Autocannon", 10), ("Multi-Laser", 10), ("Lascannon", 20)]),
                        slot(uid(mortar, "rear"), "Rearward sponson pair", "Heavy Bolter",
                             [("Heavy Flamer", 0), ("Autocannon", 10), ("Multi-Laser", 10), ("Lascannon", 20)])])]),
                take(t, "Vehicle Upgrades", [x for x in SUPERHEAVY_UPGRADES if x[0] not in ("Searchlight",
                                                                                            "Smoke Launchers")])]
    return (lambda t: vehicle_profile(t, "Auxilia Gorgon", "Super-heavy Vehicle (3 Structure Points)", 3, 14, 14, 10),
            ["Twin-linked Autocannon", "Twin-linked Autocannon", "Gorgon Mortar Battery", "Searchlight",
             "Smoke Launchers"], ["Super-heavy Tank", "Heavily Armoured Prow", "Reduced Blast", "Gorgon Transport"],
            groups,
            lambda t: transport_profile(t, "Auxilia Gorgon", "40 models", "Front assault ramp (up to two units may "
                                                                          "embark/disembark per turn)", "None"))


def adv_profile(key, name, ws, bs, s, t, w, i, a, ld, sv, ut="Infantry (Character)"):
    return unit_profile(key, name, ut, ws, bs, s, t, w, i, a, ld, sv)


def advisor(name, cost, prof, kit, rules_, limit=1, scope="force", groups=(), entries=(), mods=(), loyalist=None,
            display=None):
    """A shared Attached Advisor entry (linked from every unit it may join)."""
    eid = k("advisor", name)
    ADVISOR[name] = eid
    m = list(mods)
    if loyalist is not None:
        other = L.TRAITOR if loyalist else L.LOYALIST
        m.append(modifier("add", "error", f"{name} is {'Loyalist' if loyalist else 'Traitor'} only.",
                          conds=[cond(other, "roster", "atLeast", 1)]))
    SHARED.append(entry(eid, display or name, cost=cost, mods=m,
                        constraints=[constraint(uid(eid, "lim"), "max", limit, scope=scope, deep=True)],
                        profiles=[prof(eid)], links=[gear(eid, x) for x in kit],
                        infolinks=rules_links(list(rules_), key=eid), groups=list(groups), entries=list(entries)))


def build_advisors():
    def orbital(key, free=False):
        gid = k("grp", key, "orbital")
        ents = []
        for n, c in [("Lance Strike", 40), ("Melta Torpedo", 45), ("Barrage Bomb", 30)]:
            eid = k("orbital", key, n)
            ents.append(entry(eid, f"Orbital Bombardment: {n}", cost=c, links=[gear(eid, n)],
                              constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)]))
        return group(gid, "Orbital Bombardment (only one Master of the Fleet in the army)", entries=ents,
                     constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])

    std = ["Laspistol or Autopistol", "Close Combat Weapon"]
    advisor("Navigator", 20, lambda e: adv_profile(e, "Navigator", 2, 3, 3, 3, 1, 3, 1, 9, "6+"), std,
            ["Attached Advisor", "Warp Sight"])
    advisor("Master of the Fleet", 30, lambda e: adv_profile(e, "Master of the Fleet", 3, 4, 3, 3, 1, 3, 1, 8, "5+"),
            ["Flak Armour"] + std, ["Attached Advisor", "Master of the Fleet"],
            groups=[armoury(k("adv", "motf"), "advisor", "Laspistol or Autopistol"), orbital("motf")])
    advisor("Memorator", 15, lambda e: adv_profile(e, "Memorator", 2, 2, 3, 3, 1, 3, 1, 7, "6+"), std,
            ["Attached Advisor", "Witness to Valour"])
    advisor("Company Cook", 20, lambda e: adv_profile(e, "Company Cook", 3, 3, 3, 3, 1, 3, 1, 8, "5+"),
            ["Flak Armour", "Laspistol or Autopistol", "Cooking Utensil"], ["Attached Advisor",
                                                                            "You're Going in the Soup"])
    advisor("Personal Aide", 10, lambda e: adv_profile(e, "Personal Aide", 3, 3, 3, 3, 1, 3, 1, 7, "5+"),
            std + ["Flak Armour"], ["Attached Advisor", "At Your Service, Sir!"])
    advisor("Scribe Historicus", 10, lambda e: adv_profile(e, "Scribe Historicus", 2, 2, 3, 3, 1, 3, 1, 7, "5+"),
            std + ["Flak Armour"], ["Attached Advisor", "Chronicler of Deeds"])
    advisor("Company Jester", 10, lambda e: adv_profile(e, "Company Jester", 2, 2, 3, 3, 1, 3, 1, 7, "5+"),
            std + ["Flak Armour", "Questionable Props"], ["Attached Advisor", "Amuse Me, Jester!"])
    advisor("Locus Scribii", 20, lambda e: adv_profile(e, "Locus Scribii", 2, 2, 3, 3, 1, 3, 1, 7, "5+"),
            std + ["Flak Armour", "Administratum Data-Slate"], ["Attached Advisor", "Prepared Fire"])
    advisor("Cartographica Adept", 15, lambda e: adv_profile(e, "Cartographica Adept", 2, 3, 3, 3, 1, 3, 1, 7, "5+"),
            std + ["Flak Armour", "Surveyor's Auspex"], ["Attached Advisor", "Surveyed Ground"], limit=2)
    advisor("Psyker Attache: Cult Leader", 20,
            lambda e: adv_profile(e, "Cult Leader (ML1)", 3, 3, 3, 3, 1, 3, 1, 8, "5+"), std + ["Flak Armour"],
            ["Attached Advisor", "Psyker Attache", "Psyker", "Cult Leader"], limit=4)
    advisor("Psyker Attache: Prophet", 15,
            lambda e: adv_profile(e, "Prophet (ML1)", 2, 2, 3, 3, 1, 3, 1, 7, "5+"), std + ["Flak Armour"],
            ["Attached Advisor", "Psyker Attache", "Psyker", "Prophet"], limit=4)
    # 0-4 in total: error when Cult Leaders + Prophets > 4
    for n in ("Psyker Attache: Cult Leader", "Psyker Attache: Prophet"):
        e = [x for x in SHARED if x.get("id") == ADVISOR[n]][0]
        mods = [modifier("add", "error", "No more than four Psyker Attaches (Cult Leaders and Prophets) may be included.",
                         conds=[cond(ADVISOR["Psyker Attache: Cult Leader"], "force", "equalTo", a),
                                cond(ADVISOR["Psyker Attache: Prophet"], "force", "greaterThan", 4 - a)])
                for a in range(0, 5)]
        add_mods(e, mods)
    dm_key = k("adv", "dm")
    advisor("Discipline Master", 20, lambda e: adv_profile(e, "Discipline Master", 4, 3, 3, 3, 2, 3, 2, 8, "5+"),
            ["Flak Armour", "Laspistol or Autopistol", "Close Combat Weapon", "Frag Grenades"],
            ["Provenance", "Attached Advisor", "Discipline Master Cadre", "Instil Order"], limit=5,
            groups=[armoury(dm_key, "advisor", "Laspistol or Autopistol")],
            entries=[opt(dm_key, "Jump Pack (Airborne Command)", 10, ["Jump Pack"], show=["Drop Assault Regiments"])],
            display="Discipline Master (Discipline Master Cadre, 0-5)")
    advisor("Lotara Sarrin", 55, lambda e: adv_profile(e, "Lotara Sarrin", 3, 4, 3, 3, 2, 3, 2, 9, "5+"),
            ["Flak Armour", "Laspistol", "Close Combat Weapon", "Nuncio-vox"],
            ["Attached Advisor", "Master of the Fleet", "Flag-Captain of the Conqueror"], scope="roster", loyalist=False)
    advisor("Ilya Ravallion", 35, lambda e: adv_profile(e, "Ilya Ravallion", 2, 2, 3, 3, 1, 3, 1, 8, "6+"),
            ["Sub-flak Armour", "Laspistol", "Nuncio-vox"], ["Attached Advisor", "Szu"], scope="roster", loyalist=True)
    advisor("Hurtado Bronzi", 30, lambda e: adv_profile(e, "Hurtado Bronzi", 4, 4, 3, 3, 2, 4, 2, 8, "4+"),
            ["Carapace Armour", "Laspistol", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"],
            ["Field Officer", "Jokers' Hetman"], scope="roster")
    advisor("Peto Soneka", 30, lambda e: adv_profile(e, "Peto Soneka", 4, 4, 3, 3, 2, 4, 2, 8, "4+"),
            ["Carapace Armour", "Laspistol", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"],
            ["Field Officer", "Dancers' Hetman"], scope="roster")
    # Lotara counts as a Master of the Fleet (0-1)
    add_mods([x for x in SHARED if x.get("id") == ADVISOR["Master of the Fleet"]][0], [
        modifier("add", "error", "Lotara Sarrin is a Master of the Fleet: only one Master of the Fleet may be included.",
                 conds=[cond(ADVISOR["Lotara Sarrin"], "force", "atLeast", 1)])])


def advisor_links(key, names, title="Attached Advisor (one per unit)", show=(), extra=()):
    """Group of links to shared advisors. Max one Attached Advisor per unit."""
    gid = k("grp", key, "advisors", title)
    links = [link(uid("link", gid, n), ADVISOR[n], n) for n in names]
    mods = gate_mods(uid(gid, "max"), show) if show else []
    return group(gid, title, links=links, constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)], mods=mods)


FC_ADVISORS = ["Navigator", "Master of the Fleet", "Memorator", "Company Cook", "Personal Aide", "Scribe Historicus",
               "Lotara Sarrin", "Ilya Ravallion"]
PCC_ADVISORS = ["Navigator", "Master of the Fleet", "Memorator", "Company Cook", "Lotara Sarrin", "Ilya Ravallion",
                "Discipline Master"]
TROOP_ADVISORS = ["Psyker Attache: Cult Leader", "Psyker Attache: Prophet", "Company Jester", "Locus Scribii",
                  "Cartographica Adept", "Discipline Master"]


def infantry_advisors(key, troops=True, troop_show=()):
    """Advisor links for an Infantry unit: Troops advisors (when selected as Troops) and Discipline Masters."""
    if troops and not troop_show:
        return [advisor_links(key, TROOP_ADVISORS)]
    if troops:
        # Troops-only advisors appear when the unit is selected as Troops; Discipline Master always
        return [advisor_links(key, ["Discipline Master"], title="Attached Advisor (one per unit)"),
                advisor_links(key, TROOP_ADVISORS[:-1], title="Attached Advisor (Troops only, one per unit)",
                              show=troop_show)]
    return [advisor_links(key, ["Discipline Master"])]


# ============================================================== provenance options on units
def provenance_options(key, u, kinds=(), ogryn=False, ic=False, skip=()):
    """Unit options granted by Provenances of War. kinds: which unit lists the unit belongs to."""
    ents = []
    if "Frenzon" not in skip:
        ents.append(opt(key, "Frenzon Dispensers (Alchem-Jackers)", 50 if ogryn else 25, ["Frenzon Dispensers"],
                        show=["Alchem-Jackers"]))
    if not ogryn and "Blade" not in skip:
        if ic:
            ents.append(opt(key, "Blade and Fury: +1 Attack (Feral Warriors)", 10, show=["Feral Warriors"],
                            text="+1 Attack."))
        else:
            ents.append(opt(key, "Blade and Fury: +1 Attack (Feral Warriors)", 25, show=["Feral Warriors"],
                            text="Every model in the unit receives +1 Attack."))
    if "Collars" not in skip:
        ents.append(opt(key, "Discipline Collars (Abhuman Helots)", 20, ["Discipline Collars"],
                        show=["Abhuman Helots"]))
    if "cameleoline" in kinds:
        ents.append(opt(key, "Cameleoline (Frontier Marksmen)", 10, ["Cameleoline"], show=["Frontier Marksmen"]))
    if "mining" in kinds:
        ents.append(opt(key, "Mining Equipment (Clanholds of the Deep Worlds)", 10, ["Mining Equipment"],
                        show=["Clanholds of the Deep Worlds"]))
    if "void" in kinds:
        ents.append(opt(key, "Void-Hardened Armour (Imperial Navy Battalion)", 2, ["Void-Hardened Armour"],
                        per_unit=u, show=["Imperial Navy Battalion"]))
    if "advanced" in kinds:
        ents.append(opt(key, "Advanced Weapons (Survivors of the Dark Age)", 20, show=["Survivors of the Dark Age"],
                        text="+1 Strength to all laspistols, hellpistols, lasguns, lascarbines, laslocks and hellguns "
                             "carried by the squad. If one squad of a type buys it, every eligible squad of that type in "
                             "the army must."))
    return ents


def grav_option(key, u):
    e = opt(key, "Grav-chutes (Drop Assault Regiments)", 2, ["Grav-chute"], per_unit=u,
            show=["Drop Assault Regiments"],
            text="Every model has a Grav-chute: the unit may not select a Dedicated Transport, may always be placed in "
                 "Reserve and may Deep Strike; it may not begin the battle embarked.")
    return e, e.get("id")


def troops_toggle(key, u, provs, normal_cat, limit=None, limit_unless=None, line=True):
    """'May be selected as Troops' under the given Provenances. Returns (toggle entry, unit modifiers)."""
    t = k("troops", key)
    lim = uid(t, "force")
    cons = [constraint(uid(t, "max"), "max", 1, auto=True)]
    mods = gate_mods(uid(t, "max"), show=provs)
    if limit:
        cons.append(constraint(lim, "max", limit, scope="force", deep=True))
        if limit_unless:
            mods.append(modifier("set", lim, 99, conds=[pc(limit_unless)]))
    tog = entry(t, "Selected as Troops (" + " / ".join(provs) + ")", constraints=cons, mods=mods)
    on = lambda: cond(t, "self", "atLeast", 1)
    umods = [modifier("set-primary", "category", TROOPS, conds=[on()]),
             modifier("remove", "category", normal_cat, conds=[on()])]
    if line:
        umods.append(modifier("add", "category", gs.CAT_LINE, conds=[on()]))
    return tog, umods, (lambda: cond(t, u, "atLeast", 1))


def survivors_not_line():
    """Survivors of the Dark Age: only Grenadier Squads fulfil compulsory Troops."""
    return modifier("remove", "category", gs.CAT_LINE, conds=[pc("Survivors of the Dark Age")])


# ============================================================== HQ
FC_IDS = []


def fc_options(key, u, named=False):
    """Force Commander options granted by Provenances (shared with the named Lords Commander)."""
    ents = [
        opt(key, "Naval Officer (Imperial Navy Battalion)", 10, ["Void-Hardened Armour"], rules_=["Naval Officer"],
            show=["Imperial Navy Battalion"]),
        opt(key, "Boarding Shield (Naval Officer)", 5, ["Boarding Shield"],
            show=[lambda: cond(k("opt", key, "Naval Officer (Imperial Navy Battalion)"), u, "atLeast", 1)]),
        opt(key, "Mounted (Horse Lords)", 10, ["Cavalry Mount"], rules_=["Fleet of Hoof"], show=["Horse Lords"],
            hide=[lambda: cond(k("opt", key, "Jump Pack (Drop Assault Regiments)"), u, "atLeast", 1)]),
        opt(key, "Jump Pack (Drop Assault Regiments)", 15, ["Jump Pack"], show=["Drop Assault Regiments"]),
        opt(key, "Terminator Armour (Clanholds of the Deep Worlds)", 25, ["Terminator Armour"],
            show=["Clanholds of the Deep Worlds"]),
        opt(key, "Tainted Weapon (Cult Demagogue / Tainted Flesh)", 5, ["Tainted Weapon"],
            show=["Cult Horde", "Tainted Flesh"],
            text="Replaces the close combat weapon (Cult Demagogue: exchange for +5 points; Tainted Flesh: purchased "
                 "from the Armoury)."),
    ]
    ents += provenance_options(key, u, ic=True)
    return ents


def force_commander():
    u = k("unit", "Force Commander")
    FC_IDS.append(u)
    key = k("fc")
    return unit("0-1 Force Commander", 50, HQ, "HQ", key=u,
                profiles=[unit_profile(u, "Force Commander", "Infantry (Character)", 4, 4, 3, 3, 3, 3, 2, 8, "5+")],
                kit=["Flak Armour", "Refractor Field", "Laspistol or Autopistol", "Close Combat Weapon",
                     "Frag Grenades", "Krak Grenades"],
                rules_=["Independent Character", "Provenance", "Muster of Worlds", "Commanding Officer",
                        "Cult Demagogue", "Necromancer Demagogue"],
                constraints=[unique(u, 1, "force")],
                entries=[upgrade(key, "Planetary Overlord", 20, rules_=["Planetary Overlord"])] + fc_options(key, u),
                groups=[armoury(key, "senior", "Laspistol or Autopistol"), advisor_links(key, FC_ADVISORS)])


def named_lord(name, cost, ld, kit, rules_, loyalist):
    u = k("unit", name)
    FC_IDS.append(u)
    e = unit(name, cost, HQ, "HQ", key=u,
             profiles=[unit_profile(u, name, "Infantry (Character)", 4, 4, 3, 3, 3, 3, 2, ld, "4+/5+")],
             kit=kit, rules_=["Independent Character", "Provenance", "Commanding Officer", "Planetary Overlord",
                              "Lord Commander", "Muster of Worlds"] + rules_,
             constraints=[unique(u)], entries=fc_options(k("lord", name), u),
             groups=[advisor_links(k("lord", name), FC_ADVISORS)])
    other = L.TRAITOR if loyalist else L.LOYALIST
    add_mods(e, [modifier("add", "error", f"{name} is {'Loyalist' if loyalist else 'Traitor'} only.",
                          conds=[cond(other, "roster", "atLeast", 1)])])
    return e


def fc_count_errors(units_by_id):
    """Named Lords Commander count as Force Commanders: only one per Detachment."""
    for i in FC_IDS:
        others = [cond(o, "force", "atLeast", 1) for o in FC_IDS if o != i]
        add_mods(units_by_id[i], [modifier("add", "error", "Only one Force Commander (including a named Lord Commander, "
                                                           "who counts as a Force Commander) per Detachment.",
                                           groups=[any_of(*others)])])


def platoon_command_cadre(key, in_platoon=False):
    u = key
    sk = uid(u, "cmd")
    commander = model(u, "Platoon Commander", 1, 1, 0,
                      unit_profile(u, "Platoon Commander", "Infantry (Character)", 4, 4, 3, 3, 2, 3, 2, 8, "5+"),
                      kit=["Flak Armour", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"],
                      groups=[armoury(sk, "junior", "Laspistol or Autopistol")])
    vox = model(u, "Vox Operator", 1, 1, 0, unit_profile(u, "Vox Operator", "Infantry", 3, 3, 3, 3, 1, 3, 1, 6, "5+"),
                kit=["Flak Armour", "Close Combat Weapon", "Frag Grenades", "Krak Grenades", "Laspistol or Autopistol",
                     "Nuncio-vox"])
    std = model(u, "Platoon Standard Bearer", 1, 1, 0,
                unit_profile(u, "Platoon Standard Bearer", "Infantry", 3, 3, 3, 3, 1, 3, 1, 6, "5+"),
                kit=["Flak Armour", "Close Combat Weapon", "Frag Grenades", "Krak Grenades", "Laspistol or Autopistol",
                     "Platoon Standard"])
    bg_id = uid("model", u, "Militia Bodyguard")
    bg = model(u, "Militia Bodyguard", 3, 7, 5,
               unit_profile(u, "Militia Bodyguard", "Infantry", 3, 3, 3, 3, 1, 3, 1, 6, "5+"),
               kit=["Flak Armour", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"])
    bg_weapons = choice(u, "Militia Bodyguards: weapons (all)", [
        ("Lascarbines or Autoguns", 0, False, ["Lascarbine or Autogun"], []),
        ("Close Combat Weapons", 0, False, ["Close Combat Weapon"], []),
        ("Shotguns", 0, False, ["Shotgun"], []),
        ("Laslocks", 10, False, ["Laslock"], []),
        ("Boltguns", 20, False, ["Boltgun"], []),
        ("Heavy Stubbers", 35, False, ["Heavy Stubber"], []),
        ("Grenade Launchers", 70, False, ["Grenade Launcher"], [])], required=True, default="Lascarbines or Autoguns")
    grav, grav_id = grav_option(uid(u, "p"), u)
    mounted = opt(uid(u, "p"), "Mounted (Horse Lords)", 5, ["Cavalry Mount"], rules_=["Fleet of Hoof"], per_unit=u,
                  show=["Horse Lords"], hide=[lambda: cond(k("opt", uid(u, "p"), "Jump Packs (Drop Assault Regiments)"),
                                                           u, "atLeast", 1)])
    jump = opt(uid(u, "p"), "Jump Packs (Drop Assault Regiments)", 5, ["Jump Pack"], per_unit=u,
               show=["Drop Assault Regiments"])
    sniper = opt(uid(u, "p"), "One Bodyguard: Sniper Rifle (Frontier Marksmen)", 5, ["Sniper Rifle"],
                 show=["Frontier Marksmen"])
    prov = provenance_options(uid(u, "p"), u, kinds=("cameleoline", "mining", "void", "advanced"))
    mounted_id = mounted.get("id")
    tr = transports(uid(u, "t"), u, [
        ("Chimera", (), [lambda: cond(mounted_id, u, "atLeast", 1)]),
        ("Imperial Rhino", ["Survivors of the Dark Age"], [models_over(u, 10)]),
        ("Imperialis Militia Land Raider", ["Survivors of the Dark Age"], [models_over(u, 10)])],
        mech_required=True, grav=grav_id)
    groups = [bg_weapons, advisor_links(uid(u, "a"), PCC_ADVISORS)]
    if not in_platoon:
        groups.append(tr)
    else:
        groups.append(tr)
    entries = [commander, vox, std, bg,
               opt(uid(u, "p"), "Carapace Armour (entire squad)", 10, ["Carapace Armour"]),
               mounted, jump, grav, sniper] + prov
    return dict(models=entries, groups=groups, rules_=["Provenance", "Commanding Officer"], cost=40 - 15)


def pcc_root():
    u = k("unit", "Platoon Command Cadre")
    d = platoon_command_cadre(u)
    return unit("Platoon Command Cadre", d["cost"], HQ, "HQ", key=u, models=d["models"], groups=d["groups"],
                rules_=d["rules_"])


def rogue_psyker():
    u = k("unit", "Rogue Psyker")
    key = k("rp")
    alpha = upgrade(key, "Alpha Psyker", 25, rules_=["Alpha Psyker"])
    powers = k("rp", "powers")
    pw = entry(powers, "Rogue Psyker psychic power", cost=20,
               constraints=[constraint(uid(powers, "min"), "min", 1), constraint(uid(powers, "max"), "max", 3)],
               rules=[rule(uid(powers, "r"), "Rogue Psyker psychic powers",
                           "Each purchased power is one Rogue Psyker psychic power (+20 points each, at least one). "
                           "The list of Rogue Psyker powers is not printed in the army book - see the questions file.")])
    e = unit("0-1 Rogue Psyker", 35, HQ, "HQ", key=u, compulsory=False,
             profiles=[unit_profile(u, "Rogue Psyker", "Infantry (Character)", 2, 2, 3, 3, 2, 3, 1, 8, "-"),
                       unit_profile(u, "Rogue Alpha (Alpha Psyker)", "Infantry (Character)", 3, 3, 3, 4, 3, 4, 2, 9,
                                    "-")],
             kit=["Laspistol", "Close Combat Weapon"],
             rules_=["Independent Character", "Psyker", "Rogue Psyker"], constraints=[unique(u, 1, "force")],
             entries=[alpha, pw], groups=[armoury(key, "advisor", "Laspistol")],
             mods=[modifier("add", "error", "A Rogue Psyker may only be included in an army with the Cult Horde "
                                            "Provenance (Traitor only).",
                            conds=[cond(P["Cult Horde"], "force", "lessThan", 1)])])
    return e


def remembrancer_circle():
    u = k("unit", "63rd Expedition Remembrancer Circle")
    ms = []
    for n in ["Mersadie Oliton", "Ignace Karkasy", "Euphrati Keeler"]:
        ms.append(model(u, n, 1, 1, 0, unit_profile(u, n, "Infantry", 2, 2, 3, 3, 1, 3, 1, 7, "6+"),
                        kit=["Sub-flak Armour", "Laspistol"]))
    e = unit("63rd Expedition Remembrancer Circle", 35, HQ, "HQ", key=u, compulsory=False, models=ms,
             rules_=["Witness to Valour", "Remembrancer Circle"], constraints=[unique(u)],
             extra_cats=[(gs.FOC_PLUS["HQ"], "Force Org: +1 HQ")])
    add_mods(e, [modifier("add", "error", "The Remembrancer Circle is Loyalist only.",
                          conds=[cond(L.TRAITOR, "roster", "atLeast", 1)])])
    return e


# ============================================================== Elites
def medicae():
    u = k("unit", "Imperialis Auxilia Medicae Detachment")
    mid = uid("model", u, "Medicae Orderly")
    m = model(u, "Medicae Orderly", 3, 6, 10,
              unit_profile(u, "Medicae Orderly", "Infantry", 3, 3, 3, 3, 1, 3, 1, 7, "5+"),
              kit=["Flak Armour", "Laspistol or Autopistol", "Close Combat Weapon", "Medi-pack"])
    jp = model_takes(uid(u, "jp"), "Jump Packs (Drop Assault Regiments, per Orderly)", u, [mid], [("Jump Pack", 5)])
    add_mods(jp, [modifier("set", "hidden", "true", conds=[cond(P["Drop Assault Regiments"], "force", "lessThan", 1)])])
    return unit("Imperialis Auxilia Medicae Detachment", 0, ELITES, "Elites", key=u, models=[m],
                rules_=["Provenance", "Attached Deployment"], groups=[jp],
                entries=provenance_options(uid(u, "p"), u))


def ogryns():
    u = k("unit", "Auxilia Ogryn Brute Squad")
    bid = uid("model", u, "Ogryn Brute")
    hid = uid("model", u, "Ogryn Bone 'ead")
    prof_b = unit_profile(u, "Ogryn Brute", "Infantry", 4, 3, 5, 4, 3, 3, 2, 8, "5+")
    kit = ["Flak Armour", "Ripper Gun", "Close Combat Weapon", "Frag Grenades"]
    head = model(u, "Ogryn Bone 'ead", 0, 1, 35,
                 unit_profile(u, "Ogryn Bone 'ead", "Infantry (Character)", 4, 3, 5, 4, 3, 3, 3, 9, "5+"), kit=kit,
                 groups=[slot(hid, "Replace Ripper Gun", "Ripper Gun", [("Ogryn Close Combat Weapon", 0)]),
                         armoury(hid, "bonehead")],
                 mods=[modifier("decrement", PTS, 10, conds=[pc("Ogryn Workdivision")])])
    brute = model(u, "Ogryn Brute", 3, 10, 25, prof_b, kit=kit,
                  mods=[modifier("decrement", uid(bid, "min"), 1, conds=[cond(hid, u, "atLeast", 1)]),
                        modifier("decrement", uid(bid, "max"), 1, conds=[cond(hid, u, "atLeast", 1)])])
    swaps = model_swaps(u, "Ogryn Brutes: replace Ripper Gun with Ogryn close-combat weapon", u, [bid],
                        [("Ogryn Close Combat Weapon", 0)])
    tog, tmods, troops_on = troops_toggle("ogryn", u, ["Ogryn Workdivision"], ELITES, limit=3)
    carapace = choice(u, "Armour (entire squad)", [
        ("Carapace Armour", 5, True, ["Carapace Armour"], []),
        ("Industrial Carapace (Ogryn Workdivision)", 3, True, ["Carapace Armour"], [])], unit_id=u)
    ic_id = uid("choice", u, "Armour (entire squad)", "Industrial Carapace (Ogryn Workdivision)")
    # hide the Workdivision price without the Provenance
    for e in carapace.iter("selectionEntry"):
        if e.get("id") == ic_id:
            add_mods(e, gate_mods(uid(ic_id, "max"), show=["Ogryn Workdivision"]))
    blighted = opt(uid(u, "p"), "Blighted Ogryns (Undying Horde)", 3, per_unit=u, rules_=["Blighted Ogryns"],
                   show=["Undying Horde"])
    prov = provenance_options(uid(u, "p"), u, ogryn=True)
    tr = transports(uid(u, "t"), u, [("Chimera", (), [models_over(u, 6)])])
    return unit("Auxilia Ogryn Brute Squad", 0, ELITES, "Elites", key=u, models=[head, brute],
                rules_=["Provenance", "It's Dark in There!"], mods=tmods + [survivors_not_line()],
                entries=[tog, blighted] + prov, groups=[swaps, carapace, tr] + infantry_advisors(
                    uid(u, "a"), troop_show=[troops_on]))


def enginseer():
    u = k("unit", "Enginseer Auxilia")
    eid = uid("model", u, "Enginseer Adept")

    def servitors(mid):
        ents = []
        gid = uid("grp", mid, "servitors")
        data = [("Technical Servitor", 10, unit_profile(mid, "Technical Servitor", "Infantry", 3, 3, 3, 3, 1, 3, 1, 8,
                                                         "5+"), ["Flak Armour", "Close Combat Weapon"]),
                ("Combat Servitor", 25, unit_profile(mid, "Combat Servitor", "Infantry", 4, 3, 3, 3, 1, 3, 1, 8, "4+"),
                 ["Carapace Armour", "Power Fist", "Close Combat Weapon"]),
                ("Gun Servitor with Heavy Bolter", 35, None, ["Carapace Armour", "Heavy Bolter"]),
                ("Gun Servitor with Multi-melta", 35, None, ["Carapace Armour", "Multi-Melta"]),
                ("Gun Servitor with Plasma Cannon", 45, None, ["Carapace Armour", "Plasma Cannon"])]
        for n, c, prof, kit in data:
            sid = uid(gid, n)
            prof = prof or unit_profile(sid, "Gun Servitor", "Infantry", 3, 4, 3, 3, 1, 3, 1, 8, "4+")
            cons = [constraint(uid(sid, "max"), "max", 1 if "Plasma" in n else 4)]
            ents.append(entry(sid, n, typ="model", cost=c, constraints=cons, profiles=[prof],
                              links=[gear(sid, x) for x in kit]))
        return group(gid, "Servitors (up to four)", entries=ents,
                     constraints=[constraint(uid(gid, "max"), "max", 4)])

    adept = entry(eid, "Enginseer Adept", typ="model", cost=45,
                  constraints=[constraint(uid(eid, "min"), "min", 1), constraint(uid(eid, "max"), "max", 2)],
                  profiles=[unit_profile(u, "Enginseer Adept", "Infantry (Character)", 3, 3, 3, 3, 1, 3, 1, 8, "3+")],
                  links=[gear(eid, x) for x in ["Power Armour", "Laspistol", "Power Weapon", "Servo-arm"]],
                  groups=[servitors(eid), armoury(uid(eid, "a"), "enginseer", "Laspistol", "Power Weapon")])
    tr = transports(uid(u, "t"), u, [("Chimera", (), ())])
    return unit("0-2 Enginseer Auxilia (one Elites choice)", 0, ELITES, "Elites", key=u,
                models=numbered(adept, 2, 1), rules_=["Independent Character", "Blessing of the Machine God",
                                                      "Enginseer Auxilia"],
                constraints=[unique(u, 1, "force")], groups=[tr])


def battle_armour():
    u = k("unit", "Imperial Battle Armour")
    dccw = entry(uid(u, "dccw2"), "Dreadnought close combat weapon with built-in twin-linked bolter",
                 links=[gear(uid(u, "dccw2"), "Dreadnought Close Combat Weapon"),
                        gear(uid(u, "dccw2"), "Twin-linked Bolter")])
    arm = slot(u, "Second arm (one required)", None, [
        ("Twin-linked Heavy Bolter", 25), ("Twin-linked Autocannon", 30), ("Multi-Melta", 30), ("Plasma Cannon", 35),
        ("Twin-linked Lascannon", 40)], default_is_entry=dccw)
    hf = take(u, "Replace built-in twin-linked bolter(s)", [("Heavy Flamer", 10, 2)])
    ml = take(u, "Replace one Dreadnought close combat weapon", [("Missile Launcher", 10)])
    two_dccw = uid(u, "dccw2")
    err = modifier("add", "error", "Only a second Dreadnought close combat weapon has a second built-in twin-linked "
                                   "bolter to replace.",
                   conds=[cond(W("Heavy Flamer"), u, "atLeast", 2), cond(two_dccw, u, "lessThan", 1)])
    return unit("Imperial Battle Armour", 70, ELITES, "Elites", key=u,
                profiles=[walker_profile(u, "Imperial Battle Armour", 3, 3, "6(10)", 12, 12, 10, 3, 2)],
                kit=["Dreadnought Close Combat Weapon", "Twin-linked Bolter", "Searchlight", "Smoke Launchers"],
                groups=[arm, hf, ml, take(u, "Vehicle Upgrades", [x for x in VEHICLE_UPGRADES
                                                                 if x[0] not in ("Searchlight", "Smoke Launchers")])],
                mods=[err], rules_=[])


def elite_squad(name, cost, sgt_name, sgt_prof, mname, mprof, mcost, base, extra, kit_sgt, kit, rules_, gene=False):
    """Imperial Army Veteran Squad / Gene-Trooper Squad (shared Provenance options)."""
    u = k("unit", name)
    sid, mid = uid("model", u, sgt_name), uid("model", u, mname)
    ranged = kit[1]
    sgt = model(u, sgt_name, 1, 1, 0, unit_profile(u, sgt_name, "Infantry (Character)", *sgt_prof),
                kit=[x for x in kit_sgt if x != ranged],
                groups=[armoury(sid, "sergeant", ranged)])
    men = model(u, mname, base, base + extra, mcost, unit_profile(u, mname, "Infantry", *mprof), kit=kit)
    tda = opt(uid(u, "p"), "Terminator Armour (Clanholds: Heavy Panoplies, one squad)", 15, ["Terminator Armour"],
              per_unit=u, rules_=["Terminator Panoply"], show=["Clanholds of the Deep Worlds"],
              constraints=[constraint(uid(k("tda-squad"), u), "max", 1, scope="force", deep=True)])
    tda_id = tda.get("id")
    exemplar = opt(uid(u, "p"), "Exemplar Guard (Paragons of Humanity, one squad)", 10, per_unit=u,
                   rules_=["Exemplar Guard", "Stubborn"], show=["Paragons of Humanity"],
                   constraints=[constraint(uid(k("exemplar"), u), "max", 1, scope="force", deep=True)])
    ex_id = exemplar.get("id")
    pa = opt(uid(u, "p"), "Power Armour (Heavy Panoplies / Paragon Panoply)", 5, ["Power Armour"], per_unit=u,
             show=["Clanholds of the Deep Worlds", "Paragons of Humanity"], hide=[lambda: cond(tda_id, u, "atLeast", 1)])
    grav, grav_id = grav_option(uid(u, "p"), u)
    tdm_swaps = model_swaps(uid(u, "tda"), "Terminator weapons (any model in Terminator Armour)", u, [sid, mid],
                            TERMINATOR_WEAPONS)
    add_mods(tdm_swaps, [modifier("set", "hidden", "true", conds=[cond(tda_id, u, "lessThan", 1)])])
    pw = model_swaps(uid(u, "pw"), "Paragon Panoply: replace close combat weapon with Power Weapon (any model)", u,
                     [sid, mid], [("Power Weapon", 5)])
    add_mods(pw, [modifier("set", "hidden", "true", conds=[cond(P["Paragons of Humanity"], "force", "lessThan", 1)])])
    big = lambda: cond("model", u, "greaterThan", 5)
    errs = [modifier("add", "error", f"A {name} in Terminator Armour or an Exemplar Guard may contain no more than five "
                                     "models.", groups=[and_group([big()], [any_of(cond(tda_id, u, "atLeast", 1),
                                                                                   cond(ex_id, u, "atLeast", 1))])])]
    lr_show = ["Survivors of the Dark Age", lambda: cond(tda_id, u, "atLeast", 1), lambda: cond(ex_id, u, "atLeast", 1)]
    tr = transports(uid(u, "t"), u, [
        ("Chimera", (), [models_over(u, 10), lambda: cond(tda_id, u, "atLeast", 1)]),
        ("Centaur Light Carrier", (), [models_not(u, 5), lambda: cond(tda_id, u, "atLeast", 1)]),
        ("Imperial Rhino", ["Survivors of the Dark Age"], [models_over(u, 10)]),
        ("Imperialis Militia Land Raider", lr_show, [models_over(u, 10)])], mech_required=True, grav=grav_id)
    return u, sid, mid, sgt, men, [tda, exemplar, pa, grav], [tdm_swaps, pw, tr], errs


def veterans():
    name = "Imperial Army Veteran Squad"
    kit = ["Flak Armour", "Lasgun or Autogun", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"]
    u, sid, mid, sgt, men, prov_e, prov_g, errs = elite_squad(
        name, 50, "Veteran Sergeant", (4, 4, 3, 3, 1, 3, 2, 9, "5+"), "Veteran", (4, 4, 3, 3, 1, 3, 1, 8, "5+"), 10,
        4, 5, kit, kit, [])
    swaps = model_swaps(u, "Any model: replace Lasgun or Autogun", u, [mid],
                        [("Laspistol or Autopistol", 0), ("Shotgun", 0), ("Boltgun", 2)])
    specials, _ = pool(u, "Special Weapons (up to three Veterans)", u, SPECIAL_5, 3)
    hwt = take(u, "Heavy Weapon Team (two Veterans)", HWT, max_total=1)
    boarding = opt(uid(u, "p"), "Boarding Shields (Imperial Navy Battalion)", 5, ["Boarding Shield"], per_unit=u,
                   show=["Imperial Navy Battalion"])
    prov = provenance_options(uid(u, "p"), u, kinds=("cameleoline", "mining", "void", "advanced"))
    return unit(name, 50 - 40, ELITES, "Elites", key=u, models=[sgt, men],
                rules_=["Provenance", "Hardened Veterans"], mods=errs,
                entries=[opt(uid(u, "o"), "Carapace Armour (entire squad)", 3, ["Carapace Armour"], per_unit=u,
                             hide=[lambda: cond(prov_e[0].get("id"), u, "atLeast", 1),
                                   lambda: cond(prov_e[2].get("id"), u, "atLeast", 1)])]
                + prov_e + [boarding] + prov,
                groups=[swaps, specials, hwt] + prov_g + [advisor_links(uid(u, "fo"), ["Hurtado Bronzi", "Peto Soneka"],
                                                                        title="Field Officer")]
                + infantry_advisors(uid(u, "a"), troops=False))


def gene_troopers():
    name = "Gene-Trooper Squad"
    kit = ["Carapace Armour", "Lascarbine", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"]
    u, sid, mid, sgt, men, prov_e, prov_g, errs = elite_squad(
        name, 75, "Gene-Trooper Prime", (4, 3, 4, 3, 1, 4, 2, 9, "4+"), "Gene-Trooper", (4, 3, 4, 3, 1, 4, 1, 8, "4+"),
        12, 4, 5, kit, kit, [], gene=True)
    weapons = choice(u, "Gene-Troopers: replace Lascarbines (entire squad)", [
        ("Laspistols and close combat weapons", 0, False, ["Laspistol"], []),
        ("Shotguns", 0, False, ["Shotgun"], []),
        ("Boltguns", 2, True, ["Boltgun"], [])], unit_id=u)
    specials, _ = pool(u, "Special Weapons (up to two Gene-Troopers)", u, SPECIAL_5, 2)
    eq = take(u, "Squad Equipment", [("Vexilla", 10), ("Vox-caster", 5)])
    prov = provenance_options(uid(u, "p"), u, kinds=("mining", "void", "advanced"))
    return unit(name, 75 - 48, ELITES, "Elites", key=u, models=[sgt, men], rules_=["Provenance"], mods=errs,
                entries=prov_e + prov,
                groups=[weapons, specials, eq] + prov_g + [advisor_links(uid(u, "fo"), ["Hurtado Bronzi",
                                                                                         "Peto Soneka"],
                                                                         title="Field Officer")]
                + infantry_advisors(uid(u, "a"), troops=False))


def combat_engineers():
    name = "Imperial Combat Engineer Squad"
    u = k("unit", name)
    sid, mid = uid("model", u, "Engineer Sergeant"), uid("model", u, "Combat Engineer")
    kit = ["Flak Armour", "Shotgun", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"]
    sgt = model(u, "Engineer Sergeant", 1, 1, 0,
                unit_profile(u, "Engineer Sergeant", "Infantry (Character)", 3, 3, 3, 3, 1, 3, 2, 8, "5+"),
                kit=[x for x in kit if x != "Shotgun"], groups=[armoury(sid, "sergeant", "Shotgun")])
    men = model(u, "Combat Engineer", 4, 9, 8, unit_profile(u, "Combat Engineer", "Infantry", 3, 3, 3, 3, 1, 3, 1, 7,
                                                            "5+"), kit=kit)
    specials, _ = pool(u, "Special Weapons (up to two Combat Engineers)", u,
                       [("Flamer", 6), ("Grenade Launcher", 8), ("Meltagun", 10)], 2)
    charges = take(u, "Demolition Charges (up to two Combat Engineers)", [("Demolition Charge", 5, 2)])
    industrial = take(u, "Heavy Industrial Weapons (Clanholds of the Deep Worlds)", [("Mining Laser", 15, 1),
                                                                                    ("Powered Mining Pick", 5, 2),
                                                                                    ("Lascutter", 10, 1)])
    add_mods(industrial, [modifier("set", "hidden", "true",
                                   conds=[cond(P["Clanholds of the Deep Worlds"], "force", "lessThan", 1)])])
    grav, grav_id = grav_option(uid(u, "p"), u)
    tog, tmods, troops_on = troops_toggle("ce", u, ["Clanholds of the Deep Worlds", "Engineer Corps"], ELITES,
                                          limit=2, limit_unless="Clanholds of the Deep Worlds")
    razor = opt(uid(u, "p"), "Razorwire Sections (Engineer Corps)", 2, ["Razorwire Section"],
                rules_=["Razorwire Sections", "Infiltrate"], show=["Engineer Corps"], max_=3)
    boarding = opt(uid(u, "p"), "Boarding Shields (Imperial Navy Battalion)", 5, ["Boarding Shield"], per_unit=u,
                   show=["Imperial Navy Battalion"])
    prov = provenance_options(uid(u, "p"), u, kinds=("cameleoline", "mining", "void"))
    tr = transports(uid(u, "t"), u, [("Chimera", (), ()), ("Centaur Light Carrier", (), [models_not(u, 5)])],
                    mech_required=True, grav=grav_id)
    return unit(name, 40 - 32, ELITES, "Elites", key=u, models=[sgt, men],
                rules_=["Provenance", "Sappers"], mods=tmods + [survivors_not_line()],
                entries=[tog, opt(uid(u, "o"), "Carapace Armour (entire squad)", 3, ["Carapace Armour"], per_unit=u),
                         opt(uid(u, "o"), "Melta Bombs (entire squad)", 4, ["Melta Bombs"], per_unit=u),
                         razor, grav, boarding] + prov,
                groups=[specials, charges, industrial, tr] + infantry_advisors(uid(u, "a"), troop_show=[troops_on]))


# ============================================================== Troops
def infantry_squad(u, platoon=False):
    """Imperialis Militia Infantry Squad (as a unit entry; root or inside a Platoon)."""
    sid, mid = uid("model", u, "Sergeant"), uid("model", u, "Militia Auxiliary")
    mech = lambda: pc("Mechanised Regiments")
    sgt = model(u, "Sergeant", 1, 1, 0, unit_profile(u, "Sergeant", "Infantry (Character)", 3, 3, 3, 3, 1, 3, 2, 7,
                                                     "5+"),
                kit=["Flak Armour", "Close Combat Weapon", "Frag Grenades"],
                groups=[armoury(sid, "sergeant", "Laspistol or Autopistol")])
    men = model(u, "Militia Auxiliary", 19, 19, 0,
                unit_profile(u, "Militia Auxiliary", "Infantry", 3, 3, 3, 3, 1, 3, 1, 6, "5+"),
                kit=["Flak Armour", "Close Combat Weapon", "Frag Grenades"],
                mods=[modifier("set", uid(mid, "min"), 9, conds=[mech()]),
                      modifier("set", uid(mid, "max"), 9, conds=[mech()])])
    weapons = choice(u, "Militia Auxiliaries: weapons (all)", [
        ("Lasguns or Autoguns", 0, False, ["Lasgun or Autogun"], []),
        ("Laspistols or Autopistols and close combat weapons", 0, False, ["Laspistol or Autopistol"], []),
        ("Shotguns", 0, False, ["Shotgun"], [])], required=True, default="Lasguns or Autoguns")
    special = take(u, "Special Weapon (one Militia Auxiliary)", SPECIAL_4, max_total=1)
    hwt = take(u, "Heavy Weapon Team (two Militia Auxiliaries)", HWT, max_total=1)
    eq = take(u, "Squad Equipment", [("Vexilla", 10), ("Vox-caster", 5)])
    grav, grav_id = grav_option(uid(u, "p"), u)
    sniper = opt(uid(u, "p"), "One Militia Auxiliary: Sniper Rifle (Frontier Marksmen)", 5, ["Sniper Rifle"],
                 show=["Frontier Marksmen"])
    prov = provenance_options(uid(u, "p"), u, kinds=("cameleoline", "mining", "void"))
    tr = transports(uid(u, "t"), u, [("Chimera", ["Mechanised Regiments"], ())], mech_required=True, grav=grav_id)
    mods = [modifier("decrement", PTS, 40, conds=[mech()])]
    return dict(models=[sgt, men], cost=80, mods=mods,
                entries=[opt(uid(u, "o"), "Krak Grenades (entire squad)", 2, ["Krak Grenades"], per_unit=u),
                         sniper, grav] + prov,
                groups=[weapons, special, hwt, eq, tr] + infantry_advisors(uid(u, "a")))


def infantry_squad_root():
    u = k("unit", "Imperialis Militia Infantry Squad")
    d = infantry_squad(u)
    return unit("Imperialis Militia Infantry Squad", d["cost"], TROOPS, "Troops", key=u, models=d["models"],
                entries=d["entries"], groups=d["groups"], mods=d["mods"] + [survivors_not_line()],
                rules_=["Provenance"])


def infantry_platoon():
    u = k("unit", "Imperialis Militia Infantry Platoon")
    pc_id = uid(u, "pcc")
    d = platoon_command_cadre(pc_id, in_platoon=True)
    pcc = entry(pc_id, "Platoon Command Cadre", typ="unit", cost=d["cost"],
                constraints=[constraint(uid(pc_id, "min"), "min", 1), constraint(uid(pc_id, "max"), "max", 1)],
                infolinks=rules_links(d["rules_"], key=pc_id), entries=d["models"], groups=d["groups"])
    sq_id = uid(u, "squad")
    s = infantry_squad(sq_id, platoon=True)
    sq = entry(sq_id, "Imperialis Militia Infantry Squad", typ="unit", cost=s["cost"], mods=s["mods"],
               constraints=[constraint(uid(sq_id, "min"), "min", 1), constraint(uid(sq_id, "max"), "max", 5)],
               infolinks=rules_links(["Provenance"], key=sq_id), entries=s["models"] + s["entries"],
               groups=s["groups"])
    squads = numbered(sq, 5, 2)
    tr = transports(uid(u, "t"), u, [("Auxilia Gorgon Heavy Transporter", (), ())])
    return unit("Imperialis Militia Infantry Platoon", 0, TROOPS, "Troops", key=u, entries=[pcc] + squads,
                groups=[tr], rules_=["Infantry Platoon"], mods=[survivors_not_line()])


def levy():
    name = "Inducted Levy Squad"
    u = k("unit", name)
    sid, mid = uid("model", u, "Custodian"), uid("model", u, "Levy Auxiliary")
    undying = lambda: pc("Undying Horde")
    sgt = model(u, "Custodian", 1, 1, 0, unit_profile(u, "Custodian", "Infantry (Character)", 3, 3, 3, 3, 1, 3, 2, 7,
                                                      "5+"),
                kit=["Flak Armour", "Close Combat Weapon"], groups=[armoury(sid, "sergeant", "Laspistol or Autopistol")])
    men = model(u, "Levy Auxiliary", 19, 49, 2, unit_profile(u, "Levy Auxiliary", "Infantry", 2, 2, 3, 3, 1, 3, 1, 6,
                                                             "6+"), kit=["Sub-flak Armour"])
    hive = k("hive", u)
    weapons = choice(u, "Levy Auxiliaries: weapons (all)", [
        ("Lasguns or Autoguns", 0, False, ["Lasgun or Autogun"], []),
        ("Laspistols or Autopistols and close combat weapons", 0, False, ["Laspistol or Autopistol",
                                                                          "Close Combat Weapon"], []),
        ("Two Laspistols or Autopistols (Hive Platoons)", 1, True, ["Two Laspistols or Autopistols"],
         ["Fleet", "Gunfighters"])], unit_id=u, required=True, default="Lasguns or Autoguns")
    hid = uid("choice", u, "Levy Auxiliaries: weapons (all)", "Two Laspistols or Autopistols (Hive Platoons)")
    for e in weapons.iter("selectionEntry"):
        if e.get("id") == hid:
            add_mods(e, gate_mods(uid(hid, "max"), show=["Hive Platoons"]))
    specials, _ = pool(u, "Special Weapons (one per ten models)", u, [("Flamer", 6), ("Grenade Launcher", 8)], 0,
                       every=10)
    add_mods(specials, [modifier("set", "hidden", "true", conds=[undying()])])
    mods = [modifier("remove", "category", gs.CAT_LINE, groups=[any_of(pc("Warrior Elite"),
                                                                       pc("Survivors of the Dark Age"),
                                                                       pc("Paragons of Humanity"))]),
            modifier("add", "error", "Inducted Levy Squads may not be selected with the Mechanised Regiments "
                                     "Provenance.", conds=[pc("Mechanised Regiments")]),
            modifier("set", "name", "Zombie Levy Squad", conds=[undying()])]
    collars = opt(uid(u, "o"), "Discipline Collars", 10, ["Discipline Collars"])
    prov = provenance_options(uid(u, "p"), u, skip=("Collars",))
    tr = transports(uid(u, "t"), u, [("Auxilia Gorgon Heavy Transporter", (), ())])
    return unit(name, 40 - 38, TROOPS, "Troops", key=u, models=[sgt, men],
                rules_=["Provenance", "Disposable", "Zombie Levy"], mods=mods,
                entries=[opt(uid(u, "o"), "Vexilla (one Levy Auxiliary)", 10, ["Vexilla"]),
                         opt(uid(u, "o"), "Frag Grenades (entire squad)", 10, ["Frag Grenades"]), collars] + prov,
                groups=[weapons, specials, tr] + infantry_advisors(uid(u, "a")))


def grenadiers():
    name = "Imperialis Militia Grenadier Squad"
    u = k("unit", name)
    sid, mid = uid("model", u, "Grenadier Sergeant"), uid("model", u, "Grenadier")
    kit = ["Carapace Armour", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"]
    sgt = model(u, "Grenadier Sergeant", 1, 1, 0,
                unit_profile(u, "Grenadier Sergeant", "Infantry (Character)", 3, 4, 3, 3, 1, 3, 2, 8, "4+"),
                kit=kit, groups=[armoury(sid, "sergeant", "Hellpistol")])
    men = model(u, "Grenadier", 9, 17, 10, unit_profile(u, "Grenadier", "Infantry", 3, 4, 3, 3, 1, 3, 1, 7, "4+"),
                kit=kit + ["Targeter"],
                mods=[modifier("set", uid(mid, "max"), 9, conds=[pc("Mechanised Regiments")])])
    hive = k("hive", u)
    weapons = choice(u, "Grenadiers: weapons (all)", [
        ("Hellguns", 0, False, ["Hellgun"], []),
        ("Hellpistols and close combat weapons", 0, False, ["Hellpistol"], []),
        ("Shotguns", 0, False, ["Shotgun"], []),
        ("Boltguns", 2, True, ["Boltgun"], []),
        ("Two Hellpistols (Hive Platoons)", 2, True, ["Two Hellpistols"], ["Fleet", "Gunfighters"]),
        ("Two Bolt Pistols (Hive Platoons)", 2, True, ["Two Bolt Pistols"], ["Fleet", "Gunfighters"])],
        unit_id=u, required=True, default="Hellguns")
    for e in weapons.iter("selectionEntry"):
        if "Hive Platoons" in e.get("name"):
            add_mods(e, gate_mods(uid(e.get("id"), "max"), show=["Hive Platoons"]))
    # marker so Street-born can hide Advanced Weapons
    hive_ids = [uid("choice", u, "Grenadiers: weapons (all)", n) for n in ("Two Hellpistols (Hive Platoons)",
                                                                          "Two Bolt Pistols (Hive Platoons)")]
    specials, _ = pool(u, "Special Weapons (up to two Grenadiers)", u, SPECIAL_5, 2)
    eq = take(u, "Squad Equipment", [("Vexilla", 10), ("Vox-caster", 5)])
    grav, grav_id = grav_option(uid(u, "p"), u)
    prov = provenance_options(uid(u, "p"), u, kinds=("cameleoline", "void", "advanced"))
    for e in prov:
        if e.get("name").startswith("Advanced Weapons"):
            add_mods(e, [modifier("set", "hidden", "true", groups=[any_of(*[cond(h, u, "atLeast", 1)
                                                                           for h in hive_ids])]),
                         modifier("set", uid(e.get("id"), "max"), 0,
                                  groups=[any_of(*[cond(h, u, "atLeast", 1) for h in hive_ids])])])
    tr = transports(uid(u, "t"), u, [
        ("Chimera", (), [models_over(u, 12)]),
        ("Imperial Rhino", ["Survivors of the Dark Age"], [models_over(u, 10)]),
        ("Imperialis Militia Land Raider", ["Survivors of the Dark Age"], [models_over(u, 10)])],
        mech_required=True, grav=grav_id)
    return unit(name, 100 - 90, TROOPS, "Troops", key=u, models=[sgt, men], rules_=["Provenance"],
                mods=[modifier("add", "error", "Grenadier Squads may not be included with the Cult Horde Provenance.",
                               conds=[pc("Cult Horde")])],
                entries=[grav] + prov, groups=[weapons, specials, eq, tr] + infantry_advisors(uid(u, "a")))


def fire_support():
    name = "Imperialis Militia Fire Support Squad"
    u = k("unit", name)
    tid = uid("model", u, "Heavy Weapon Team")
    team = model(u, "Heavy Weapon Team", 5, 10, 0,
                 unit_profile(u, "Militia Auxiliary (two per Heavy Weapon Team)", "Infantry", 3, 3, 3, 3, 1, 3, 1, 6,
                              "5+"),
                 kit=["Flak Armour", "Laspistol or Autopistol", "Close Combat Weapon", "Frag Grenades",
                      "Heavy Stubber"],
                 mods=[modifier("set", uid(tid, "max"), 5, conds=[pc("Mechanised Regiments")])])
    swaps = model_swaps(u, "Heavy Weapon Teams: replace Heavy Stubber (any team)", u, [tid], [
        ("Mortar", 5), ("Twin-linked Heavy Stubber", 5), ("Heavy Bolter", 10), ("Multi-Laser", 10),
        ("Heavy Flamer", 10), ("Missile Launcher", 10), ("Autocannon", 10), ("Lascannon", 15)])
    industrial = model_swaps(uid(u, "ind"), "Heavy Industrial Weapons (Clanholds of the Deep Worlds)", u, [tid],
                             [("Mining Laser", 15)])
    add_mods(industrial, [modifier("set", "hidden", "true",
                                   conds=[cond(P["Clanholds of the Deep Worlds"], "force", "lessThan", 1)])])
    extra_cost = [modifier("increment", PTS, 15, conds=[cond(tid, u, "atLeast", n)]) for n in range(6, 11)]
    grav, grav_id = grav_option(uid(u, "p"), u)
    prov = provenance_options(uid(u, "p"), u, kinds=("cameleoline", "void"))
    tr = transports(uid(u, "t"), u, [("Chimera", ["Mechanised Regiments"], ())], mech_required=True, grav=grav_id)
    return unit(name, 65, TROOPS, "Troops", key=u, models=[team], compulsory=False,
                rules_=["Provenance", "Support Squad"], mods=extra_cost,
                entries=[opt(uid(u, "o"), "Vox-caster (one Militia Auxiliary)", 5, ["Vox-caster"]), grav] + prov,
                groups=[swaps, industrial, tr] + infantry_advisors(uid(u, "a")))


def recon():
    name = "Imperialis Militia Reconnaissance Squad"
    u = k("unit", name)
    sid, mid = uid("model", u, "Recon Sergeant"), uid("model", u, "Recon Auxiliary")
    kit = ["Flak Armour", "Lasgun or Autogun", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"]
    sgt = model(u, "Recon Sergeant", 1, 1, 0,
                unit_profile(u, "Recon Sergeant", "Infantry (Character)", 3, 4, 3, 3, 1, 3, 1, 8, "5+"),
                kit=[x for x in kit if x != "Lasgun or Autogun"],
                groups=[armoury(sid, "sergeant", "Lasgun or Autogun"),
                        take(sid, "Recon Sergeant: one of", [("Melta Bombs", 5), ("Demolition Charge", 5)],
                             max_total=1)])
    men = model(u, "Recon Auxiliary", 4, 4, 0, unit_profile(u, "Recon Auxiliary", "Infantry", 3, 4, 3, 3, 1, 3, 1, 7,
                                                            "5+"), kit=kit)
    weapons = choice(u, "Replace Lasguns or Autoguns (entire squad)", [
        ("Shotguns", 0, False, ["Shotgun"], []), ("Sniper Rifles", 25, False, ["Sniper Rifle"], [])], unit_id=u)
    grav, grav_id = grav_option(uid(u, "p"), u)
    prov = provenance_options(uid(u, "p"), u, kinds=("void",))
    tr = transports(uid(u, "t"), u, [("Chimera", ["Mechanised Regiments"], ())], mech_required=True, grav=grav_id)
    fm = lambda: pc("Frontier Marksmen")
    return unit(name, 50, TROOPS, "Troops", key=u, models=[sgt, men], compulsory=False,
                rules_=["Provenance", "Support Squad", "Infiltrate", "Scouts", "Move Through Cover"],
                mods=[modifier("add", "category", gs.CAT_LINE, conds=[fm()]), survivors_not_line()],
                entries=[opt(uid(u, "o"), "Cameleoline (entire squad)", 10, ["Cameleoline"]),
                         opt(uid(u, "o"), "Infravisors (entire squad)", 10, ["Infravisor"]), grav] + prov,
                groups=[weapons, tr, advisor_links(uid(u, "fo"), ["Peto Soneka"], title="Field Officer")]
                + infantry_advisors(uid(u, "a")))


def beastmen():
    name = "Beastman Auxilia Herd"
    u = k("unit", name)
    sid, mid = uid("model", u, "Beastman Chieftain"), uid("model", u, "Beastman Auxiliary")
    kit = ["Sub-flak Armour", "Close Combat Weapon", "Frag Grenades"]
    sgt = model(u, "Beastman Chieftain", 1, 1, 0,
                unit_profile(u, "Beastman Chieftain", "Infantry (Character)", 4, 2, 3, 3, 1, 3, 2, 7, "6+"),
                kit=kit, groups=[armoury(sid, "sergeant", "Laspistol or Autopistol")])
    men = model(u, "Beastman Auxiliary", 9, 29, 6,
                unit_profile(u, "Beastman Auxiliary", "Infantry", 4, 2, 3, 3, 1, 3, 1, 6, "6+"), kit=kit)
    weapons = choice(u, "Beastman Auxiliaries: weapons (entire herd)", [
        ("Laspistols or Autopistols", 0, False, ["Laspistol or Autopistol"], []),
        ("Lasguns", 0, False, ["Lasgun"], []), ("Autoguns", 0, False, ["Autogun"], []),
        ("Shotguns", 0, False, ["Shotgun"], [])], unit_id=u, required=True, default="Laspistols or Autopistols")
    specials, _ = pool(u, "Special Weapons (one per ten models)", u,
                       [("Flamer", 6), ("Grenade Launcher", 8), ("Heavy Stubber", 10)], 0, every=10)
    prov = provenance_options(uid(u, "p"), u)
    return unit(name, 60 - 54, TROOPS, "Troops", key=u, models=[sgt, men],
                rules_=["Provenance", "Fleet", "Furious Charge", "Outflank"], mods=[survivors_not_line()],
                entries=[opt(uid(u, "o"), "Vexilla (one Beastman Auxiliary)", 10, ["Vexilla"]),
                         opt(uid(u, "o"), "Flak Armour (entire herd)", 1, ["Flak Armour"], per_unit=u),
                         opt(uid(u, "o"), "+1 Strength (Tainted Flesh)", 2, per_unit=u, show=["Tainted Flesh"],
                             text="Every model in the herd increases its Strength by 1.")] + prov,
                groups=[weapons, specials] + infantry_advisors(uid(u, "a")))


def clones():
    name = "Clone Auxilia Cohort"
    u = k("unit", name)
    sid, mid = uid("model", u, "Clone Prime"), uid("model", u, "Clone Auxiliary")
    kit = ["Flak Armour", "Lasgun", "Close Combat Weapon", "Frag Grenades"]
    sgt = model(u, "Clone Prime", 1, 1, 0,
                unit_profile(u, "Clone Prime", "Infantry (Character)", 3, 3, 3, 3, 1, 3, 2, 8, "5+"),
                kit=[x for x in kit if x != "Lasgun"], groups=[armoury(sid, "sergeant", "Lasgun")])
    men = model(u, "Clone Auxiliary", 9, 19, 7, unit_profile(u, "Clone Auxiliary", "Infantry", 3, 3, 3, 3, 1, 3, 1, 7,
                                                             "5+"), kit=kit)
    specials, _ = pool(u, "Special Weapons (one per ten models)", u, SPECIAL_4, 0, every=10)
    hwt = take(u, "Heavy Weapon Team (two Clone Auxiliaries)", HWT, max_total=1)
    eq = take(u, "Squad Equipment", [("Vexilla", 10), ("Vox-caster", 5)])
    prov = provenance_options(uid(u, "p"), u)
    tr = transports(uid(u, "t"), u, [("Chimera", ["Mechanised Regiments"], ())], mech_required=True)
    return unit(name, 70 - 63, TROOPS, "Troops", key=u, models=[sgt, men],
                rules_=["Provenance", "Conditioned Cohort"],
                mods=[survivors_not_line(),
                      modifier("add", "error", "Clone Auxilia Cohorts may not be included with the Cult Horde "
                                               "Provenance.", conds=[pc("Cult Horde")])],
                entries=[opt(uid(u, "o"), "Krak Grenades (entire cohort)", 2, ["Krak Grenades"], per_unit=u)] + prov,
                groups=[specials, hwt, eq, tr] + infantry_advisors(uid(u, "a")))


# ============================================================== Fast Attack
def sentinels():
    name = "Imperialis Militia Sentinel Squadron"
    u = k("unit", name)
    mid = uid("model", u, "Auxilia Sentinel")
    m = model(u, "Auxilia Sentinel", 1, 3, 40,
              walker_profile(u, "Auxilia Sentinel", 3, 3, "5", 10, 10, 10, 3, 1, ut="Vehicle (Walker, Open-topped)"),
              kit=["Heavy Flamer", "Searchlight"],
              groups=[slot(mid, "Replace Heavy Flamer", "Heavy Flamer", [("Multi-Laser", 5), ("Autocannon", 5),
                                                                         ("Missile Launcher", 5), ("Lascannon", 15),
                                                                         ("Multi-Melta", 15)]),
                      take(mid, "Combat Blades", [("Combat Blades", 5)]),
                      take(mid, "Vehicle Upgrades (Sentinel)", SENTINEL_UPGRADES)],
              entries=[opt(mid, "Drop Sentinel: Deep Strike (Drop Assault Regiments)", 5, rules_=["Deep Strike"],
                           show=["Drop Assault Regiments"])])
    return unit(name, 0, FA, "Fast Attack", key=u, models=numbered(m, 3, 1), rules_=["Scouts", "Vehicle Squadron"])


def land_speeders():
    name = "Imperial Land Speeder Squadron"
    u = k("unit", name)
    mid = uid("model", u, "Imperial Land Speeder")
    m = model(u, "Imperial Land Speeder", 1, 3, 50,
              vehicle_profile(u, "Imperial Land Speeder", "Vehicle (Fast, Skimmer, Open-topped)", 3, 11, 11, 10),
              kit=["Heavy Bolter", "Searchlight"],
              groups=[slot(mid, "Replace Heavy Bolter", "Heavy Bolter", [("Heavy Flamer", 0), ("Multi-Laser", 5),
                                                                         ("Autocannon", 10), ("Multi-Melta", 15)]),
                      take(mid, "Armoured Crew Compartment", [("Armoured Crew Compartment", 10)]),
                      take(mid, "Vehicle Upgrades (Land Speeder)", SPEEDER_UPGRADES)])
    return unit(name, 0, FA, "Fast Attack", key=u, models=numbered(m, 3, 1), rules_=["Vehicle Squadron"])


def cavalry():
    name = "Imperialis Militia Cavalry Squadron"
    u = k("unit", name)
    sid, mid = uid("model", u, "Sergeant"), uid("model", u, "Cavalry Auxiliary")
    kit = ["Flak Armour", "Laspistol or Autopistol", "Close Combat Weapon", "Cavalry Mount"]
    hl = lambda: pc("Horse Lords")
    vet = k("opt", uid(u, "o"), "Upgrade Sergeant to Veteran Sergeant")
    sgt = model(u, "Sergeant", 1, 1, 0,
                unit_profile(u, "Sergeant", "Cavalry (Character)", 3, 3, 3, 3, 1, 3, 1, 7, "5+"),
                kit=[x for x in kit if x != "Laspistol or Autopistol"],
                groups=[armoury(sid, "sergeant", "Laspistol or Autopistol")])
    add_to(sgt, "profiles", [unit_profile(u, "Veteran Sergeant", "Cavalry (Character)", 3, 3, 3, 3, 1, 3, 2, 8, "5+")])
    men = model(u, "Cavalry Auxiliary", 4, 9, 8, unit_profile(u, "Cavalry Auxiliary", "Cavalry", 3, 3, 3, 3, 1, 3, 1,
                                                              7, "5+"), kit=kit,
                mods=[modifier("set", uid(mid, "max"), 14, conds=[hl()])])
    lance = choice(u, "Hunting Lances (entire squadron)", [
        ("Hunting Lances replace pistols", 3, True, ["Hunting Lance"], []),
        ("Hunting Lances replace close combat weapons", 3, True, ["Hunting Lance"], [])], unit_id=u)
    for e in lance.iter("selectionEntry"):
        add_mods(e, [modifier("decrement", PTS, 1, repeats=[repeat("model", u, 1)], conds=[hl()])])
    lance_ids = [uid("choice", u, "Hunting Lances (entire squadron)", n) for n in
                 ("Hunting Lances replace pistols", "Hunting Lances replace close combat weapons")]
    no_lance = [cond(i, u, "atLeast", 1) for i in lance_ids]
    pistols = model_swaps(u, "Models without Hunting Lances: replace pistol", u, [mid],
                          [("Lasgun", 0), ("Autogun", 0), ("Shotgun", 0)])
    add_mods(pistols, [modifier("set", "hidden", "true", groups=[any_of(*no_lance)])])
    specials, _ = pool(u, "Special Weapons (up to two models without Hunting Lances)", u, SPECIAL_4, 2)
    add_mods(specials, [modifier("set", "hidden", "true", groups=[any_of(*[cond(i, u, "atLeast", 1)
                                                                            for i in lance_ids])])])
    mounts = choice(u, "Mounts (entire squadron)", [("Xeno Mounts", 4, True, ["Xeno Mount"], [])], unit_id=u)
    for e in mounts.iter("selectionEntry"):
        add_mods(e, [modifier("decrement", PTS, 1, repeats=[repeat("model", u, 1)], conds=[hl()])])
    tog, tmods, _ = troops_toggle("cav", u, ["Horse Lords"], FA)
    vet_riders = opt(uid(u, "p"), "Veteran Riders (Horse Lords, one squadron)", 3, per_unit=u,
                     rules_=["Veteran Riders"], show=["Horse Lords"],
                     constraints=[constraint(k("vet-riders"), "max", 1, scope="force", deep=True)])
    prov = provenance_options(uid(u, "p"), u)
    return unit(name, 40 - 32, FA, "Fast Attack", key=u, models=[sgt, men], rules_=["Provenance", "Fleet of Hoof"],
                mods=tmods + [survivors_not_line(),
                              modifier("add", "error", "Cavalry Squadrons may not be included with the Clanholds of "
                                                       "the Deep Worlds Provenance.",
                                       conds=[pc("Clanholds of the Deep Worlds")])],
                entries=[tog, upgrade(uid(u, "o"), "Upgrade Sergeant to Veteran Sergeant", 6,
                                      text="The Sergeant uses the Veteran Sergeant profile."),
                         opt(uid(u, "o"), "Vox-caster (one model without a special weapon)", 5, ["Vox-caster"]),
                         opt(uid(u, "o"), "Krak Grenades (entire squadron)", 2, ["Krak Grenades"], per_unit=u),
                         opt(uid(u, "o"), "Melta Bombs (entire squadron)", 4, ["Melta Bombs"], per_unit=u),
                         vet_riders] + prov,
                groups=[lance, pistols, specials, mounts])


def cyclops():
    name = "Cyclops Demolition Vehicle"
    u = k("unit", name)
    cy = model(u, "Cyclops", 1, 1, 0, vehicle_profile(u, "Cyclops", "Vehicle", "-", 10, 10, 10),
               kit=["Demolition Charge"])
    op = model(u, "Cyclops Operator", 1, 1, 0,
               unit_profile(u, "Cyclops Operator", "Infantry", 3, 3, 3, 3, 1, 3, 1, 6, "5+"),
               kit=["Flak Armour", "Laspistol", "Close Combat Weapon"])
    tr = transports(uid(u, "t"), u, [("Chimera", (), ())])
    return unit(name, 25, FA, "Fast Attack", key=u, models=[cy, op],
                rules_=["Remote Control", "Demolition Vehicle", "Fragile"], groups=[tr])


def salamander():
    name = "Salamander Scout Vehicle"
    u = k("unit", name)
    return unit(name, 100, FA, "Fast Attack", key=u,
                profiles=[vehicle_profile(u, name, "Vehicle (Fast, Open-topped)", 3, 12, 10, 10)],
                kit=["Autocannon", "Heavy Bolter", "Searchlight", "Smoke Launchers"],
                groups=[take(u, "Vehicle Upgrades", [x for x in VEHICLE_UPGRADES
                                                     if x[0] not in ("Searchlight", "Smoke Launchers")])])


def jump_assault():
    name = "Imperialis Militia Jump Assault Squad"
    u = k("unit", name)
    sid, mid = uid("model", u, "Assault Sergeant"), uid("model", u, "Jump Auxiliary")
    kit = ["Laspistol or Autopistol", "Laspistol or Autopistol", "Frag Grenades", "Flak Armour", "Jump Pack"]
    sgt = model(u, "Assault Sergeant", 1, 1, 0,
                unit_profile(u, "Assault Sergeant", "Jump Infantry (Character)", 3, 3, 3, 3, 1, 3, 2, 8, "5+"),
                kit=["Frag Grenades", "Flak Armour", "Jump Pack", "Laspistol or Autopistol"],
                groups=[armoury(sid, "sergeant", "Laspistol or Autopistol", ccw_default=None)])
    men = model(u, "Jump Auxiliary", 4, 9, 10, unit_profile(u, "Jump Auxiliary", "Jump Infantry", 3, 3, 3, 3, 1, 3, 1,
                                                            7, "5+"),
                kit=["Two Laspistols or Autopistols", "Frag Grenades", "Flak Armour", "Jump Pack"])
    bolt = choice(u, "Bolt Pistols (entire squad)", [
        ("Replace one pistol with a Bolt Pistol", 1, True, ["Bolt Pistol"], []),
        ("Replace both pistols with Bolt Pistols", 2, True, ["Two Bolt Pistols"], [])], unit_id=u)
    special, _ = pool(u, "Up to two models: replace one pistol", u, [("Hand Flamer", 5), ("Blast Pistol", 8),
                                                                     ("Plasma Pistol", 10)], 2)
    tog, tmods, _ = troops_toggle("jump", u, ["Drop Assault Regiments"], FA)
    prov = provenance_options(uid(u, "p"), u)
    return unit(name, 60 - 40, FA, "Fast Attack", key=u, models=[sgt, men],
                rules_=["Provenance", "Deep Strike", "Gunfighters"], mods=tmods + [survivors_not_line()],
                entries=[tog, opt(uid(u, "o"), "Carapace Armour (entire squad)", 3, ["Carapace Armour"], per_unit=u),
                         opt(uid(u, "o"), "Krak Grenades (entire squad)", 2, ["Krak Grenades"], per_unit=u),
                         opt(uid(u, "o"), "Melta Bombs (entire squad)", 4, ["Melta Bombs"], per_unit=u)] + prov,
                groups=[bolt, special])


# ============================================================== Heavy Support
def mutant_spawn():
    name = "Mutant Spawn"
    u = k("unit", name)
    m = model(u, "Mutant Spawn", 3, 10, 25, unit_profile(u, "Mutant Spawn", "Beasts", 3, 0, 5, 5, 3, 2, "D6", 10, "-"),
              kit=["Mutations"])
    return unit(name, 10, HS, "Heavy Support", key=u, models=[m],
                rules_=["Fearless", "Random Attacks", "Mutated Beyond Reason", "Blind Aggression",
                        "Special Selection (Mutant Spawn)"],
                mods=[modifier("add", "error", "Mutant Spawn may only be selected by an army with the Tainted Flesh "
                                               "Provenance.", conds=[cond(P["Tainted Flesh"], "force", "lessThan", 1)])])


TANK_CMD = None


def tank_commander_group(key, mid, battle_tank=False):
    """Militia Tank Commander / Tyana Kourion / Aika 73 upgrades on an eligible vehicle."""
    ents = [entry(k("tankcmd", key), "Militia Tank Commander", cost=40,
                  constraints=[constraint(uid(k("tankcmd", key), "max"), "max", 1, auto=True)],
                  infolinks=rules_links(["Tank Commander", "Command Tank"], key=k("tankcmd", key)),
                  links=[gear(k("tankcmd", key), "Improved Comms")]),
            entry(k("kourion", key), "Tyana Kourion", cost=65,
                  constraints=[constraint(uid(k("kourion", key), "max"), "max", 1, auto=True)],
                  infolinks=rules_links(["Tyana Kourion", "Tank Commander", "Command Tank", "Armoured Spearhead"],
                                        key=k("kourion", key)),
                  links=[gear(k("kourion", key), "Improved Comms")])]
    if battle_tank:
        ents.append(entry(k("aika", key), "Aika 73", cost=30,
                          constraints=[constraint(uid(k("aika", key), "max"), "max", 1, auto=True)],
                          infolinks=rules_links(["Veteran Crew"], key=k("aika", key)),
                          links=[gear(k("aika", key), "Extra Armour")]))
    gid = k("grp", key, "commander")
    return group(gid, "Tank Commander", entries=ents, constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


TC_IDS, KOURION_IDS, AIKA_IDS = [], [], []


def collect_tank_ids(root):
    for e in root.iter("selectionEntry"):
        n = e.get("name")
        if n == "Militia Tank Commander":
            TC_IDS.append(e.get("id"))
        elif n == "Tyana Kourion":
            KOURION_IDS.append(e.get("id"))
        elif n == "Aika 73":
            AIKA_IDS.append(e.get("id"))


def tank_limit_errors(roots):
    """0-1 Tank Commander and unique Kourion / Aika 73 across every eligible vehicle (incl. squadron copies)."""
    for ids, text in [(TC_IDS, "Only one Militia Tank Commander may be included in the army."),
                      (KOURION_IDS, "Tyana Kourion is unique."), (AIKA_IDS, "Aika 73 is unique.")]:
        for r in roots:
            for e in r.iter("selectionEntry"):
                if e.get("id") in ids:
                    # error when the total across all copies exceeds one
                    conds = [cond(i, "roster", "atLeast", 1) for i in ids if i != e.get("id")]
                    if conds:
                        add_mods(e, [modifier("add", "error", text, groups=[any_of(*conds)])])
                    add_to(e, "constraints", [constraint(uid(e.get("id"), "roster"), "max", 1, scope="roster",
                                                         deep=True)])


def leman_russ():
    name = "Militia Auxiliary Battle Tank Squadron"
    u = k("unit", name)
    data = [("Leman Russ Battle Tank", 145, (14, 12, 10), "Battle Cannon"),
            ("Leman Russ Annihilator", 140, (14, 12, 10), "Twin-linked Lascannon"),
            ("Leman Russ Exterminator", 125, (14, 12, 10), "Exterminator Autocannon"),
            ("Leman Russ Demolisher", 155, (14, 13, 11), "Demolisher Cannon"),
            ("Leman Russ Vanquisher", 180, (14, 12, 10), "Vanquisher Battle Cannon")]
    models = []
    for n, c, (f, s, r), gun in data:
        mid = uid("model", u, n)
        spons = [("Heavy Bolters", 10, False, ["Heavy Bolter", "Heavy Bolter"], []),
                 ("Heavy Flamers", 10, False, ["Heavy Flamer", "Heavy Flamer"], [])]
        if "Demolisher" in n:
            spons += [("Plasma Cannons", 20, False, ["Plasma Cannon", "Plasma Cannon"], []),
                      ("Multi-meltas", 30, False, ["Multi-Melta", "Multi-Melta"], [])]
        m = model(u, n, 0, 1 if "Vanquisher" in n else 3, c,
                  vehicle_profile(u, n, "Vehicle (Tank)", 3, f, s, r), kit=[gun, "Heavy Bolter"],
                  groups=[slot(mid, "Replace hull-mounted Heavy Bolter", "Heavy Bolter",
                               [("Heavy Flamer", 0), ("Multi-Laser", 0), ("Lascannon", 10)]),
                          choice(mid, "Side Sponsons (one pair)", spons),
                          take(mid, "Vehicle Upgrades", VEHICLE_UPGRADES),
                          tank_commander_group(mid, mid, battle_tank=n == "Leman Russ Battle Tank")])
        models += [m] if "Vanquisher" in n else numbered(m, 3, 0)
    return unit(name, 0, HS, "Heavy Support", key=u, models=models, rules_=["Vehicle Squadron"],
                mods=[modifier("add", "error", "A Battle Tank Squadron contains 1-3 Leman Russ tanks (no more than one "
                                               "Vanquisher).", groups=[any_of(cond("model", u, "lessThan", 1),
                                                                              cond("model", u, "greaterThan", 3))])])


def rapiers():
    name = "Imperialis Auxilia Rapier Battery"
    u = k("unit", name)
    car = uid("model", u, "Rapier Carrier")
    crew = uid("model", u, "Militia Auxiliary Crew")
    cmin, cmax = uid(crew, "min"), uid(crew, "max")
    carrier = model(u, "Rapier Carrier", 1, 3, 40,
                    unit_profile(u, "Rapier Carrier", "Artillery", "-", "-", "-", 7, 2, "-", "-", "-", "3+"))
    crews = entry(crew, "Militia Auxiliary Crew", typ="model", cost=0,
                  mods=[modifier("increment", cmin, 2, repeats=[repeat(car, u, 1)]),
                        modifier("increment", cmax, 2, repeats=[repeat(car, u, 1)])],
                  constraints=[constraint(cmin, "min", 0, auto=True), constraint(cmax, "max", 0, auto=True)],
                  profiles=[unit_profile(u, "Militia Auxiliary", "Infantry", 3, 3, 3, 3, 1, 3, 1, 6, "5+")],
                  links=[gear(crew, x) for x in ["Flak Armour", "Lasgun or Laspistol", "Close Combat Weapon"]])
    gid = uid("grp", u, "weapon")
    ents = []
    for n, pts, w in [("Quad Multi-lasers", 0, "Quad Multi-Laser"), ("Quad Heavy Bolters", 0, "Quad Heavy Bolter"),
                      ("Thudd Guns", 15, "Thudd Gun"), ("Laser Destroyers", 35, "Laser Destroyer")]:
        eid = uid(gid, n)
        ents.append(entry(eid, n, mods=[modifier("increment", PTS, pts, repeats=[repeat(car, u, 1)])] if pts else [],
                          constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)], links=[gear(eid, w)]))
    weapon = group(gid, "Battery Weapon (all Rapier Carriers)", entries=ents, default=ents[0].get("id"),
                   constraints=[constraint(uid(gid, "min"), "min", 1, auto=True),
                                constraint(uid(gid, "max"), "max", 1, auto=True)])
    extra = [modifier("increment", PTS, 10, conds=[cond(car, u, "atLeast", n)]) for n in (2, 3)]
    return unit(name, 0, HS, "Heavy Support", key=u, models=[carrier, crews], mods=extra,
                rules_=["Provenance", "Weapons Platform"], groups=[weapon],
                entries=provenance_options(uid(u, "p"), u, skip=("Blade",)))


def land_raider_hs():
    name = "Imperialis Militia Land Raider"
    u = k("unit", name)
    kit, rules_, groups, tprof = land_raider_parts()
    return unit(name, 235, HS, "Heavy Support", key=u,
                profiles=[vehicle_profile(u, "Land Raider", "Vehicle (Tank)", 3, 14, 14, 14), tprof(u)], kit=kit,
                rules_=rules_, groups=groups(u))


def artillery_battery():
    name = "Imperialis Auxilia Artillery Tank Battery"
    u = k("unit", name)
    data = [("Basilisk", 100, "Earthshaker Cannon"), ("Griffon", 75, "Heavy Mortar"),
            ("Medusa", 200, "Medusa Siege Gun")]
    ids = [uid("model", u, n) for n, *_ in data]
    models = []
    for (n, c, gun), mid in zip(data, ids):
        others = [cond(c2, u, "atLeast", 1) for o in ids if o != mid for c2 in [o] + [uid(o, "copy", i) for i in (2, 3)]]
        extra = []
        if n == "Basilisk":
            extra.append(take(mid, "Indirect Fire", [("Indirect Fire", 25)]))
        if n == "Griffon":
            extra.append(take(mid, "Siege Shells", [("Griffon Siege Shells", 5)]))
        m = model(u, n, 0, 3, c, vehicle_profile(u, n, "Vehicle (Tank, Open-topped)", 3, 12, 10, 10),
                  kit=[gun, "Heavy Bolter"], groups=extra + [take(mid, "Vehicle Upgrades", VEHICLE_UPGRADES)],
                  mods=[modifier("set", "hidden", "true", groups=[any_of(*others)]),
                        modifier("set", uid(mid, "max"), 0, groups=[any_of(*others)])])
        models += numbered(m, 3, 0)
    return unit(name, 0, HS, "Heavy Support", key=u, models=models,
                rules_=["Vehicle Squadron", "Indirect Fire", "Siege Shells (Griffon)"],
                mods=[modifier("add", "error", "An Artillery Tank Battery contains 1-3 vehicles, all of the same type.",
                               groups=[any_of(cond("model", u, "lessThan", 1), cond("model", u, "greaterThan", 3))])])


def ordnance_battery():
    name = "Auxilia Heavy Ordnance Battery"
    u = k("unit", name)
    car = uid("model", u, "Artillery Carriage")
    crew = uid("model", u, "Militia Auxiliary Crew")
    cmin, cmax = uid(crew, "min"), uid(crew, "max")
    carriage = model(u, "Artillery Carriage", 1, 3, 63,
                     unit_profile(u, "Artillery Carriage", "Artillery", "-", "-", "-", 7, 4, "-", "-", "-", "3+"))
    crews = entry(crew, "Militia Auxiliary Crew", typ="model", cost=3,
                  mods=[modifier("increment", cmin, 4, repeats=[repeat(car, u, 1)]),
                        modifier("increment", cmax, 8, repeats=[repeat(car, u, 1)])],
                  constraints=[constraint(cmin, "min", 0, auto=True), constraint(cmax, "max", 0, auto=True)],
                  profiles=[unit_profile(u, "Militia Auxiliary Crew", "Infantry", 3, 3, 3, 3, 1, 3, 1, 6, "5+")],
                  links=[gear(crew, x) for x in ["Flak Armour", "Lasgun or Autogun", "Close Combat Weapon"]])
    gid = uid("grp", u, "gun")
    es = uid(gid, "Earthshaker Cannons")
    md = uid(gid, "Medusa Siege Guns")
    ents = [entry(es, "Earthshaker Cannons", constraints=[constraint(uid(es, "max"), "max", 1, auto=True)],
                  links=[gear(es, "Earthshaker Cannon")]),
            entry(md, "Medusa Siege Guns", mods=[modifier("increment", PTS, 25, repeats=[repeat(car, u, 1)])],
                  constraints=[constraint(uid(md, "max"), "max", 1, auto=True)], links=[gear(md, "Medusa Siege Gun")],
                  entries=[entry(uid(md, "shells"), "Siege Shells (all carriages)",
                                 mods=[modifier("increment", PTS, 5, repeats=[repeat(car, u, 1)])],
                                 constraints=[constraint(uid(md, "shells", "max"), "max", 1, auto=True)],
                                 links=[gear(uid(md, "shells"), "Medusa Siege Shells")],
                                 infolinks=rules_links(["Siege Shells (Medusa)"], key=md))])]
    gun = group(gid, "Battery Weapon (all carriages)", entries=ents, default=es,
                constraints=[constraint(uid(gid, "min"), "min", 1, auto=True),
                             constraint(uid(gid, "max"), "max", 1, auto=True)])
    return unit(name, 0, HS, "Heavy Support", key=u, models=[carriage, crews],
                rules_=["Immobile Artillery"], groups=[gun])


def malcador():
    name = "0-1 Auxilia Malcador Heavy Tank"
    u = k("unit", name)
    return unit(name, 235, HS, "Heavy Support", key=u, constraints=[unique(u, 1, "force")],
                profiles=[vehicle_profile(u, "Malcador Heavy Tank", "Super-heavy Vehicle (Tank), 2 Structure Points",
                                          3, 13, 13, 12)],
                kit=["Battle Cannon", "Autocannon", "Autocannon", "Autocannon", "Searchlight", "Smoke Launchers"],
                rules_=["Super-heavy Tank", "High-speed Drive"],
                groups=[slot(u, "Replace traverse-mounted Battle Cannon", "Battle Cannon",
                             [("Twin-linked Lascannon", 0)]),
                        take(u, "Replace hull-mounted Autocannon (one)", [("Multi-Laser", 0), ("Heavy Flamer", 0),
                                                                          ("Lascannon", 10), ("Demolisher Cannon", 30)],
                             max_total=1),
                        choice(u, "Replace both sponson Autocannons", [
                            ("Two Multi-lasers", 0, False, ["Multi-Laser", "Multi-Laser"], []),
                            ("Two Heavy Flamers", 0, False, ["Heavy Flamer", "Heavy Flamer"], []),
                            ("Two Lascannons", 20, False, ["Lascannon", "Lascannon"], [])]),
                        take(u, "Siege Armour", [("Siege Armour", 10)]),
                        take(u, "Vehicle Upgrades", [x for x in VEHICLE_UPGRADES
                                                     if x[0] not in ("Searchlight", "Smoke Launchers")]),
                        tank_commander_group(u, u)])


def gorgon_hs():
    name = "Auxilia Gorgon Heavy Transporter"
    u = k("unit", name)
    prof, kit, rules_, groups, tprof = gorgon_parts()
    return unit(name, 275, HS, "Heavy Support", key=u, profiles=[prof(u), tprof(u)], kit=kit, rules_=rules_,
                groups=groups(u))


# ============================================================== configuration
def provenances_config():
    eid = k("cfg", "Provenances")
    gid = uid(eid, "grp")
    ents = []
    for n, (c, _t) in PROV_TEXT.items():
        oid = uid(eid, n)
        P[n] = oid
    for n, (c, _t) in PROV_TEXT.items():
        oid = P[n]
        mods = []
        if n in ("Cult Horde", "Undying Horde"):
            mods.append(modifier("add", "error", f"{n} may only be selected by a Traitor army.",
                                 conds=[cond(L.LOYALIST, "roster", "atLeast", 1)]))
        ents.append(entry(oid, n, cost=c, mods=mods, constraints=[constraint(uid(oid, "max"), "max", 1, auto=True)],
                          infolinks=rules_links([f"Provenance: {n}"], key=oid)))
    comp = uid(eid, "Companions of the Ten Thousand")
    companions = entry(comp, "Companions of the Ten Thousand (Paragons of Humanity)", cost=25,
                       constraints=[constraint(uid(comp, "max"), "max", 1, auto=True)],
                       mods=gate_mods(uid(comp, "max"), show=["Paragons of Humanity"]),
                       rules=[rule(uid(comp, "r"), "Companions of the Ten Thousand",
                                   "The army may include a Legio Custodes Allied Contingent. A Legio Custodes army may "
                                   "include an Exercitus Imperialis Allied Contingent using Paragons of Humanity and this "
                                   "option; it is ignored for any Legio Custodes rule which prohibits, restricts or "
                                   "limits Allied Contingents. It does not grant Legio Custodes army-wide rules, command "
                                   "abilities or wargear.")])
    g = group(gid, "Provenances of War (up to two)", entries=ents,
              constraints=[constraint(uid(gid, "max"), "max", 2, auto=True)])
    # errors
    errs = []
    pairs = [("Cyber-Augmetics", "Gene-Crafted"), ("Survivors of the Dark Age", "Cult Horde"),
             ("Survivors of the Dark Age", "Clanholds of the Deep Worlds"), ("Tainted Flesh", "Gene-Crafted"),
             ("Tainted Flesh", "Survivors of the Dark Age"), ("Frontier Marksmen", "Cult Horde"),
             ("Paragons of Humanity", "Cult Horde"), ("Paragons of Humanity", "Abhuman Helots"),
             ("Undying Horde", "Cult Horde")]
    for a, b in pairs:
        errs.append(modifier("add", "error", f"{a} may not be selected alongside {b}.",
                             conds=[cond(P[a], "self", "atLeast", 1), cond(P[b], "self", "atLeast", 1)]))
    others = [cond(P[n], "self", "atLeast", 1) for n in PROVS if n != "Mechanised Regiments"]
    errs.append(modifier("add", "error", "Mechanised Regiments may only be selected alone.",
                         groups=[and_group([cond(P["Mechanised Regiments"], "self", "atLeast", 1)], [any_of(*others)])]))
    fc_present = [cond(i, "force", "atLeast", 1) for i in FC_IDS]
    any_prov = any_of(*[cond(P[n], "self", "atLeast", 1) for n in PROVS])
    errs.append(modifier("add", "error", "Provenances of War may only be selected by a Detachment containing a Force "
                                         "Commander (or a named Lord Commander who counts as one).",
                         groups=[and_group([_negate(c) for c in fc_present], [any_prov])]))
    errs.append(modifier("add", "error", "Paragons of Humanity: the army must include at least one Imperial Army "
                                         "Veteran Squad or Gene-Trooper Squad.",
                         conds=[cond(P["Paragons of Humanity"], "self", "atLeast", 1),
                                cond(k("unit", "Imperial Army Veteran Squad"), "force", "lessThan", 1),
                                cond(k("unit", "Gene-Trooper Squad"), "force", "lessThan", 1)]))
    naval_ids = [k("opt", k("fc"), "Naval Officer (Imperial Navy Battalion)")] + \
                [k("opt", k("lord", n), "Naval Officer (Imperial Navy Battalion)") for n in LORDS]
    errs.append(modifier("add", "error", "Imperial Navy Battalion: the army must include a Force Commander upgraded to a "
                                         "Naval Officer.",
                         conds=[cond(P["Imperial Navy Battalion"], "self", "atLeast", 1)] +
                               [cond(i, "force", "lessThan", 1) for i in naval_ids]))
    rules_ = rules_links(["Muster of Worlds", "Provenance"], key=eid)
    return entry(eid, "Muster of Worlds: Provenances of War", cats=[category_link(gs.CAT_CONFIG, "Configuration",
                                                                                   primary=True, key=eid)],
                 constraints=[constraint(uid(eid, "min"), "min", 1, scope="force", deep=True),
                              constraint(uid(eid, "max"), "max", 1, scope="force", deep=True)],
                 mods=errs, infolinks=rules_, groups=[g], entries=[companions])


LORDS = ["Hektor Varvarus", "Teng Namatjira", "Saul Niborran", "Thaddeus Fayle", "Yennu Egwu"]
LORD_KIT = ["Carapace Armour", "Refractor Field", "Bolt Pistol", "Power Weapon", "Frag Grenades", "Krak Grenades"]


# ============================================================== build
def merge_duplicate_links(root):
    """Kit lists with the same item twice (e.g. two Autocannons) produce identical link ids: keep one link and raise
    its fixed count."""
    for parent in root.iter("entryLinks"):
        seen = {}
        for lk in list(parent):
            i = lk.get("id")
            if i in seen:
                seen[i] += 1
                parent.remove(lk)
            else:
                seen[i] = 1
        for lk in parent:
            n = seen.get(lk.get("id"), 1)
            if n > 1:
                for c in lk.iter("constraint"):
                    if c.get("type") in ("min", "max") and c.get("value") == "1":
                        c.set("value", str(n))
                lk.set("name", f"{n}x {lk.get('name')}")


def build():
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS, multi_profile=MULTI, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    TRANSPORT.clear(), ADVISOR.clear(), SHARED.clear(), FC_IDS.clear(), P.clear()
    TC_IDS.clear(), KOURION_IDS.clear(), AIKA_IDS.clear()
    for n in PROVS:   # provenance ids are needed before the units are built
        P[n] = uid(k("cfg", "Provenances"), n)
    build_transports()
    build_advisors()

    fc = force_commander()
    lords = [
        named_lord("Hektor Varvarus", 90, 9, LORD_KIT, ["Veteran of the Expeditionary Fleets"], True),
        named_lord("Teng Namatjira", 95, 9, LORD_KIT + ["Nuncio-vox"], ["A Hundred Compliances"], True),
        named_lord("Saul Niborran", 100, 10, LORD_KIT + ["Nuncio-vox"], ["The Line Must Hold"], True),
        named_lord("Thaddeus Fayle", 95, 9, LORD_KIT, ["Ruthless Discipline"], False),
        named_lord("Yennu Egwu", 90, 9, ["Carapace Armour", "Refractor Field", "Laspistol", "Power Weapon",
                                         "Frag Grenades", "Krak Grenades", "Nuncio-vox"], ["Hidden Allegiance"], False),
    ]
    fc_count_errors({e.get("id"): e for e in [fc] + lords})
    vet, gene = veterans(), gene_troopers()
    for name in ("Terminator Armour (Clanholds: Heavy Panoplies, one squad)",
                 "Exemplar Guard (Paragons of Humanity, one squad)"):
        ids = [k("opt", uid(k("unit", n), "p"), name) for n in ("Imperial Army Veteran Squad", "Gene-Trooper Squad")]
        for r in (vet, gene):
            for e in r.iter("selectionEntry"):
                if e.get("id") in ids:
                    other = [i for i in ids if i != e.get("id")][0]
                    add_mods(e, [modifier("add", "error", f"Only one Veteran or Gene-Trooper Squad in the army may "
                                                          f"take: {name.split(' (')[0]}.",
                                          conds=[cond(other, "force", "atLeast", 1)])])
    config = provenances_config()

    units = [allegiance(), config,
             fc, *lords, pcc_root(), rogue_psyker(), remembrancer_circle(),
             medicae(), ogryns(), enginseer(), battle_armour(), vet, gene, combat_engineers(),
             infantry_platoon(), infantry_squad_root(), levy(), grenadiers(), fire_support(), recon(), beastmen(),
             clones(),
             sentinels(), land_speeders(), cavalry(), cyclops(), salamander(), jump_assault(),
             mutant_spawn(), leman_russ(), rapiers(), land_raider_hs(), artillery_battery(), ordnance_battery(),
             malcador(), gorgon_hs()]
    for r in units:
        collect_tank_ids(r)
    tank_limit_errors(units)
    root = catalogue(ARMY, units, SHARED)
    merge_duplicate_links(root)
    return root
