"""Talons of the Emperor (Legio Custodes / Sisters of Silence / Officio Assassinorum) for Prohammer 30k.

Source: the author's army book 'Talons_of_the_Emperor.txt'. Questions: tools/questions/Talons of the Emperor.md
"""
from armies.common import *  # noqa: F401,F403
from armies.common import (k, unit, model, upgrade, unique, error_if, catalogue, start, register_data, W, gear,
                           per_model, rules_links, unit_profile, transport_profile, vehicle_profile, walker_profile,
                           slot, take, pool, choice, model_swaps, model_takes, numbered, add_to, add_mods,
                           HQ, TROOPS, ELITES, FA, HS)
from bsx import (PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group,
                 category_link)
import gamesystem as gs
import legiones as L

ARMY = "Talons of the Emperor"

# ====================================================================== rules
CUSTODES = ["Legio Custodes", "Bulky", "Fearless", "Crusader", "Counter-Attack"]
SISTERS = ["Anathema Psykana", "Adamantium Will", "Hatred", "Stubborn"]

RULES = {
    # ---------------------------------------------------------------- army
    "Talons of the Emperor": (
        "A Talons of the Emperor army is chosen with the normal ProHammer Classic army construction rules and the "
        "Standard Force Organisation Chart (HQ 1-2, Troops 2-6, Elites 0-3, Fast Attack 0-3, Heavy Support 0-3); the "
        "minimum selections (1 HQ, 2 Troops) are compulsory and may be filled by Legio Custodes or Sisters of Silence "
        "units. THE TWO TALONS: Legio Custodes and Sisters of Silence chosen together in one Talons Detachment are not "
        "Allied Detachments of each other. Rules referring to Legio Custodes only affect models with the Legio Custodes "
        "special rule, rules referring to Sisters of Silence only affect Sisters of Silence units, rules referring to "
        "Talons of the Emperor units affect both. Sisters of Silence never gain Legio Custodes special rules or command "
        "abilities by being in the same Detachment. ALLEGIANCE: a Talons of the Emperor Detachment is always Loyalist "
        "unless a scenario or campaign rule expressly states otherwise and may not normally be part of a Traitor force. "
        "WARLORD: one eligible HQ Character must be the Warlord; in a force with a Legio Custodes HQ Character that model "
        "normally serves as Warlord, a Sisters of Silence Character may be Warlord where her entry permits. The Warlord "
        "selects (not randomly generates) a Warlord Trait. LORDS OF WAR / FORTIFICATIONS: only where the mission permits "
        "or both players agree, no more than one of each. MULTIPLE DETACHMENTS: each Detachment fulfils its own "
        "compulsory selections; Detachment rules do not affect other Detachments. Allied Detachments may not fulfil the "
        "compulsory selections of the Primary Detachment."),
    "The Emperor's Talons": (
        "If the Primary Detachment of an army contains one or more Legio Custodes units, that army may not normally "
        "include an Allied Detachment. Sisters of Silence from this army list are part of the Talons Detachment and are "
        "not allies for this restriction. A Sisters of Silence force with no Legio Custodes units may use Allied "
        "Detachments normally. A mission, campaign rule or special rule may specifically override this restriction."),
    "Companions of the Ten Thousand": (
        "An Exercitus Imperialis Allied Contingent with the Companions of the Ten Thousand upgrade is an exception to The "
        "Emperor's Talons and may be included alongside the Legio Custodes exactly as described in the Paragons of "
        "Humanity Provenance. For The Emperor's Talons and any other rule limiting Allied Detachments it is ignored. It "
        "does not cause the Exercitus Imperialis units to gain any Legio Custodes or Talons of the Emperor special rules."),
    "Dedicated Transports (Talons)": (
        "Dedicated Transports purchased as part of a unit's entry do not occupy a separate Force Organisation slot and "
        "operate as separate units once deployed. Transport Capacity restrictions must always be observed. The Coronus "
        "Grav-Carrier is restricted to the Legio Custodes units named in its entry, the Anathema Psykana Rhino and "
        "Kharon Pattern Acquisitor to the Sisters of Silence units whose entries list them."),
    "Massive Wound": (
        "MASSIVE WOUNDS deals D3 wounds to the target model. Against target units with multi-wound models, massive "
        "wounds may need to be rolled and resolved one at a time to ensure that wounds are allocated to wounded models "
        "sequentially. Excess damage from a massive wound beyond what is needed to kill a model does not spill over "
        "onto other models."),
    # ------------------------------------------------------------ Custodes
    "Legio Custodes": (
        "All models with the Legio Custodes special rule have Bulky, Fearless, Crusader and Counter-Attack. Custodes "
        "models may charge up to 8\" instead of the normal 6\". Units composed entirely of Custodes models have a unit "
        "coherency of 3\" instead of 2\"."),
    "Very Bulky": "The model counts as three models for the purposes of Transport Capacity (ProHammer Classic).",
    "Disintegration": (
        "On an unmodified roll of 6 To Wound, a wound caused by a weapon with this rule becomes a Massive Wound. Against "
        "vehicles, an Armour Penetration roll of a natural 6 gains +1 on the Vehicle Damage Table."),
    "Fan-burst": (
        "Each unmodified roll of 6 To Hit generates another shooting attack with the weapon. These additional shots may "
        "generate further attacks, to a maximum of six To Hit rolls from each weapon."),
    "Volley Fire": ("If the firing model did not move during its Movement phase, it may fire its Spiculus Bolt Launcher "
                    "twice during the Shooting phase."),
    "Rapid Tracking": "Skimmers and Flyers may not claim Cover Saves gained from their movement against this weapon.",
    "Heliothermic Detonation": (
        "If a (non-vehicle) model suffers one or more unsaved wounds from this weapon and survives, it must immediately "
        "pass a Toughness test or suffer a Massive Wound. If this weapon scores a Penetrating Hit against a vehicle, add "
        "+1 to the resulting roll on the Vehicle Damage Table."),
    "Exoshock": ("If this weapon scores a Penetrating Hit against a vehicle, roll a D6. On a 4+, the target suffers a "
                 "second automatic Penetrating Hit. Cover Saves may not be taken against this additional hit."),
    "Molecular Severance": (
        "Apollonian Spear: an unmodified roll of 4+ To Wound inflicts a Massive Wound. Against vehicles, after scoring a "
        "hit, a D6 roll of 4+ causes a Penetrating Hit regardless of the target's Armour Value. Successful Invulnerable "
        "Saves made against wounds caused by the Apollonian Spear must be re-rolled."),
    "Legio Custodes Tribune": (
        "A Legio Custodes Tribune retains the Shield-Captain's profile, wargear and options and gains the Eternal Warrior "
        "special rule. If the Tribune is the army's Warlord, his Warlord Trait may be chosen rather than randomly "
        "determined. If a Tribune is present in the Primary Detachment, he must be the army's Warlord unless Constantin "
        "Valdor is also present. Only one Shield-Captain in an army of 2,000 points or more may be upgraded."),
    "The Shadow of the Throne": (
        "If Constantin Valdor is the army's Warlord, the controlling player may re-roll any attempt to Seize the "
        "Initiative. In addition, Valdor gains a Teleportation Transponder at no additional cost and one friendly unit "
        "with the Legio Custodes special rule may also receive Teleportation Transponders at no additional cost."),
    "Grav-backwash": (
        "If the Pallas Grav-Attack moved during its previous Movement phase, enemy models suffer -1 to their To Hit rolls "
        "when attacking it in close combat, to a maximum required roll of 6+."),
    "Auramite Pinions": "A model equipped with Auramite Pinions has a 4+ Invulnerable Save in close combat.",
    "Unyielding Sentinel": ("Whenever the Telemon suffers a Penetrating Hit, roll two dice when determining the result on "
                            "the Vehicle Damage Table and discard the highest result."),
    "Indomitable Charge": "When the Telemon charges, it inflicts D6 Hammer of Wrath hits instead of one.",
    # -------------------------------------------------------------- Sisters
    "Anathema Psykana": (
        "Models with this special rule have Adamantium Will, Hatred (Psykers) and Stubborn. Enemy Psykers within 8\" of "
        "one or more models with this special rule suffer -2 Leadership when taking Psychic Tests. This penalty is not "
        "cumulative."),
    "Ex Oblivio": (
        "Models with this special rule also have Anathema Psykana and are Fearless. Whenever an enemy Psyker within 8\" "
        "successfully passes a Psychic Test, the Psyker and one model with Ex Oblivio within range each roll a D6 and add "
        "their Leadership. If the model with Ex Oblivio equals or exceeds the Psyker's total, the Psyker immediately "
        "suffers Perils of the Warp. Only one Ex Oblivio test may be made against each Psychic Power."),
    "Mistress of the Silent Sisterhood": ("Friendly Sisters of Silence units within 12\" of the Knight-Abyssal may use her "
                                          "Leadership of 10 for any Leadership tests they are required to take."),
    "Mistress of the Black Ships": (
        "Friendly Sisters of Silence units within 12\" of Jenetia Krole may use her Leadership of 10 for any Leadership "
        "tests they are required to take. Once per battle, at the beginning of any friendly turn, Krole may declare a "
        "Silent Hunt: until the beginning of the next friendly turn, all friendly Sisters of Silence units within 12\" "
        "gain Hatred against all enemy models. In addition her Anathema Psykana and Ex Oblivio powers extend to 12\"."),
    "Command Cadre": ("A Vigil Command Cadre may be taken as a retinue for a Knight-Centura, Knight-Abyssal or Jenetia "
                      "Krole and does not use up an HQ choice in this way."),
    "Gunfighters": ("A model with this special rule may fire both of its Pistol weapons during the Shooting phase. Both "
                    "weapons must be fired at the same enemy unit."),
    "Firebrand Jump Packs": ("If the entire squad is equipped with Jump Packs, its Unit Type becomes Jump Infantry. A "
                             "Firebrand Destroyer Cadre equipped with Jump Packs may not select a Dedicated Transport."),
    "Condemned Quarry": (
        "At the start of the Sisters of Silence player's turn, the Excruciatus Cadre may nominate one enemy unit within "
        "18\". Until the start of the next Sisters of Silence turn, that unit may not use the Leadership characteristic "
        "of another model and friendly Sisters of Silence units may re-roll To Hit rolls of 1 against it. Only one enemy "
        "unit may be affected by Condemned Quarry at a time."),
    "Marked Quarry": ("After both armies have deployed but before the first turn begins, nominate one enemy unit. The "
                      "Seeker Cadre may re-roll ranged To Hit rolls of 1 against the nominated unit for the duration of "
                      "the battle."),
    "Snare": ("If a (non-vehicle) unit suffers one or more hits from a Snare weapon, it must pass a Strength test or "
              "become Entangled until the end of its next turn. An Entangled unit may not Run or charge and fights at "
              "-1 Initiative."),
    "Psyker Bane": "Against Psykers, the Stake Crossbow wounds on a 2+ and ignores Armour Saves.",
    "Hellfire": "Hellfire Bolts always wound non-vehicle models on a 2+. They cannot damage vehicles.",
    "Witchbane": (
        "Against Psykers, Psyk-out Bolts (and Psyk-out Heavy Bolts) wound on a 2+. If a Psyker suffers one or more "
        "unsaved wounds from them, it must immediately take a Leadership test; if failed, the Psyker suffers Perils of the "
        "Warp. In addition, a unit containing one or more Psykers that suffers an unsaved wound from them must "
        "immediately take a Pinning test at -2 Leadership."),
    "Psyk-out": ("Psyk-out Grenades may be thrown instead of firing another weapon (range 6\"). Roll To Hit as normal; "
                 "they only affect Psykers. If a Psyker is hit, it must take a Leadership test on 2D6. For every point by "
                 "which the test is failed, the Psyker/unit suffers one wound; saving throws may be taken normally. If a "
                 "Psyker is hit by a Psyk-out Missile, resolve the effect using this rule."),
    "Combi-Weapon": (
        "The Boltgun component uses the normal Boltgun profile. The secondary weapon uses the Flamer, Meltagun, Plasma "
        "Gun or Snare Gun profile and may be fired once per battle, following the normal rules for Combi-Weapons. Special "
        "Issue Ammunition may also be used by the Bolter component of a Combi-Weapon."),
    "Paired Pistol Weapons": ("Paired weapons use the normal profile for that weapon. Models with the Gunfighters special "
                              "rule may fire both weapons during the Shooting phase."),
    "Modified Rending": (
        "Where a weapon is listed as Rending (X+), it follows the normal rules for Rending, except that the Rending effect "
        "is triggered on the listed unmodified To Wound roll instead of only on a 6 (e.g. Rending (5+) triggers on 5 or "
        "6). Against vehicles, the additional Armour Penetration effect is likewise triggered on an unmodified Armour "
        "Penetration roll equal to or greater than the listed value."),
    "Battle Auspex": ("The Kharon Pattern Acquisitor has the Night Vision special rule. In addition, enemy Cover Saves "
                      "against shooting attacks made by the Kharon are worsened by 1."),
    "Capture-Grid": ("When the Kharon Pattern Acquisitor performs a Tank Shock against an Infantry unit, the target unit "
                     "suffers D6 Strength 5 hits before resolving any other effects of the Tank Shock."),
    # ------------------------------------------------------------ Assassins
    "Assassin Operative": (
        "An Imperial Assassin follows all of the normal rules for Independent Characters, except: an Assassin may never "
        "join another unit; no Independent Character may join an Assassin; an Assassin always fights as a unit of a "
        "single model; an Assassin may not capture or contest objectives."),
    "Dodge": ("The 4+ Save shown on an Assassin's profile is an Invulnerable Save, representing extraordinary reflexes "
              "rather than physical armour."),
    "Temple": (
        "When an Imperial Assassin is selected, choose one Assassin Temple (Vindicare +60, Callidus +70, Eversor +45, "
        "Culexus +55, Adamus +75, Venenum +75, Vanus +55 points). The Assassin gains all wargear and special rules "
        "listed for that Temple. An Assassin may belong to only one Temple."),
    "One Assassin": ("An army may include no more than one model with the Officio Assassinorum rules, regardless of the "
                     "number of Detachments or Force Organisation Charts being used."),
    "Assassinorum Agent": (
        "An Imperial Assassin may be included as an Elites choice in an Imperial army. Assassins are independent agents "
        "and do not benefit from army-wide special rules, Legion rules, Doctrines or similar abilities unless a rule "
        "specifically states that it affects Officio Assassinorum models."),
    "Marksman": (
        "When the Vindicare fires a ranged weapon, the controlling player may choose which visible model in the target "
        "unit suffers any wounds caused by the attack, including a Sergeant, special or heavy weapon bearer, attached "
        "character or Independent Character."),
    "Psychic Abomination": (
        "At the start of each enemy Player Turn, each enemy Psyker within 6\" of the Culexus Assassin must take a Morale "
        "test. If failed, the Psyker immediately Falls Back; if part of a unit, the entire unit Falls Back."),
    "Soulless": ("Any unit, friend or foe, with one or more models within 12\" of the Culexus Assassin counts as "
                 "Leadership 7. If its Leadership would normally be lower than 7, use the lower value instead."),
    "Psyker Assassin": (
        "The Culexus may specifically target an enemy Psyker with ranged attacks even if that Psyker is part of another "
        "unit or would normally be protected from being individually targeted. When charging a unit containing a "
        "Psyker, the Culexus may move past other models in the unit where necessary to make contact with the Psyker, "
        "provided the move can otherwise be completed legally."),
    "Life Drain": (
        "At the start of each round of close combat in which the Culexus is fighting a Psyker, before any attacks, both "
        "players roll 2D6 and add the Leadership of their respective models (Soulless applies to the Psyker). If the "
        "Culexus scores higher, the Psyker immediately suffers one Wound with no saving throws of any kind allowed; this "
        "Wound counts towards the combat result."),
    "Jump Back": (
        "At the start of any Assault phase, the Callidus may attempt to disengage from close combat. Roll a D6: on a 1 the "
        "attempt fails; on 2+ move the Callidus that many inches directly away from the enemy models she was fighting "
        "(not into contact with another enemy). If the enemy unit is left unengaged, it may make a normal Consolidation "
        "move at the end of the Assault phase."),
    "A Word in Your Ear...": (
        "After both armies have deployed, but before the first turn begins, the controlling player may select one enemy "
        "unit and move it up to 6\". The unit must remain entirely within its normal Deployment Zone. If the selected unit "
        "is a vehicle, its controlling player chooses its final facing."),
    "Fast Shot": ("The Eversor may fire the Executioner Pistol twice during each Shooting phase. Both shots must use the "
                  "same profile."),
    "Bio-Meltdown": (
        "When the Eversor is slain, centre a Blast marker over the model before removing it. Every model touched suffers "
        "one automatic Strength 5 hit (saves allowed). Then remove the Eversor from play."),
    "Death's Artisan": (
        "If the Adamus is fighting in a close combat containing an enemy Character, she may nominate one enemy Character "
        "at the beginning of the Assault phase; move the two models into base contact if possible. Until the end of that "
        "Assault phase, the Adamus and the nominated Character must direct all their close combat attacks against each "
        "other, and no other model may allocate attacks against either of them. The Adamus never requires worse than 4+ "
        "To Hit the nominated Character. If slain before making her attacks, she still attacks at her Initiative step and "
        "is removed afterwards."),
    "Unnatural Conditioning": (
        "The Venenum is immune to the Poisoned special rule: Poisoned weapons roll To Wound against her using their "
        "normal Strength instead of their fixed Poisoned value. Any other rules representing toxins, venoms or poisons "
        "have no effect on her."),
    "Autonomic Servo-Limbs": (
        "At the end of a round of close combat, after Morale tests, the Vanus may choose to disengage: move her 3D6\" in "
        "any direction away from the combat; she automatically regroups. Enemy units fighting her may not pursue but may "
        "make a normal Consolidation move."),
    "Infocyte": (
        "The Vanus may use each of the following abilities once per battle. AUSPECTRE: when an enemy Flyer enters play "
        "from Reserves, before it is moved onto the battlefield, choose the point along the appropriate table edge from "
        "which it must enter (the enemy still chooses its facing and moves it normally). SIGNUM SHUNT: when an enemy unit "
        "enters play from Reserves within 12\" and Line of Sight of the Vanus, that unit must immediately take a Pinning "
        "test. JINX: after both armies have deployed, before the first turn, nominate one enemy unit; it suffers -1 "
        "Leadership for the remainder of the battle."),
    "Execution Force": (
        "OFFICIO ASSASSINORUM EXECUTION FORCE (alternative army list). THE SEVEN CLADES: it must include exactly one each "
        "of the Vindicare, Callidus, Eversor, Culexus, Adamus, Venenum and Vanus Infocyte Assassin and no other units; it "
        "may not include Allied Detachments, Fortifications, Lords of War, Dedicated Transports or any other models. The "
        "normal Force Organisation Chart is not used and the One Assassin rule is ignored. Each Assassin remains a "
        "separate unit. MISSION OPERATIVES: the Assassins may capture and contest objectives normally. PREPARED "
        "POSITIONS: models may always use the Infiltrate special rule, even in missions which do not normally permit "
        "Infiltrators (this does not override special deployment rules such as Polymorphine). PERFECT COORDINATION: once "
        "during each friendly Player Turn, re-roll one individual dice rolled for a model in the Execution Force (To Hit, "
        "To Wound, Armour Penetration, Saving Throw, Leadership test, Difficult Terrain test or Advance roll); a dice may "
        "not be re-rolled twice. PRIORITY TARGETS: after deployment, before the first turn, nominate the enemy Warlord and "
        "up to two other enemy units; all Assassins may re-roll To Hit rolls of 1 against them; if all are destroyed by "
        "the end of the battle the Execution Force gains +1 Victory Point. WARLORD: nominate one Assassin as Warlord; it "
        "does not generate or select a Warlord Trait but counts as the Warlord for Victory Points."),
}

# ==================================================================== weapons
SPEAR_MELEE = ("-", "+1", "-", "Two-handed, Power Weapon; 6s To Hit give one extra attack")
GS_BOLT = ('12"', "5", "4", "Assault 2")

WEAPONS = {
    # Custodes infantry
    "Lastrum Storm Bolter": ('24"', "5", "4", "Assault 2"),
    "Lastrum Bolt Cannon": ('36"', "6", "3", "Heavy 3"),
    "Twin-linked Lastrum Bolt Cannon": ('36"', "6", "3", "Heavy 3, Twin-Linked"),
    "Adrastus Bolt Caliver": ('30"', "5", "3", "Heavy 2"),
    "Infernus Firepike": ("Template", "6", "4", "Heavy 1, Torrent"),
    "Adrathic Destructor": ('12"', "5", "2", "Assault 2, Disintegration"),
    "Twin-linked Adrathic Destructor": ('12"', "5", "2", "Assault 2, Disintegration, Twin-Linked"),
    "Adrathic Devastator": ('18"', "6", "2", "Heavy 2, Disintegration"),
    "Twin-linked Adrathic Devastator": ('18"', "6", "2", "Heavy 2, Disintegration, Twin-Linked"),
    "Corvae Las-Pulser": ('36"', "9", "2", "Heavy 2"),
    "Twin-linked Corvae Las-Pulser": ('36"', "9", "2", "Heavy 2, Twin-Linked"),
    "Archaeotech Kinetic Destroyer": ('12"', "7", "3", "Pistol, Master-Crafted, Fan-burst"),
    "Solarite Power Gauntlet": ("-", "x2", "-", "Power Fist (Power Weapon, Unwieldy), Master-Crafted"),
    "Solarite Power Talon": ("-", "User", "-", "Power Weapon, Shred"),
    "Pair of Solarite Power Talons": ("-", "User", "-", "Power Weapon, Shred, +1 Attack for two weapons"),
    "Tarsus Buckler": ("-", "+1", "-", "Power Weapon, Energy Nullifier"),
    "Solarite Power Lance": ("-", "User", "-", "Power Weapon; on the charge up to two attacks at I10, S8, Armourbane"),
    "Spiculus Bolt Launcher": ('48"', "5", "4", "Heavy 5, Rending, Volley Fire"),
    "Iliastus Accelerator Culverin": ('36"', "7", "2", "Heavy 5, Rending, Heliothermic Detonation"),
    "Twin-linked Iliastus Accelerator Cannon": ('60"', "7", "2", "Heavy 3, Twin-Linked, Rending, Rapid Tracking, "
                                                                 "Heliothermic Detonation"),
    "Dreadnought Close Combat Weapon": ("-", "x2 (max 10)", "-", "Power Weapon; a second Dreadnought Close Combat "
                                                                 "Weapon gives +1 Attack"),
    # Sisters of Silence
    "Bolt Pistol": ('12"', "4", "5", "Pistol"),
    "Boltgun": ('24"', "4", "5", "Rapid Fire"),
    "Storm Bolter": ('24"', "4", "5", "Assault 2"),
    "Hand Flamer": ("Template", "3", "6", "Pistol"),
    "Flamer": ("Template", "4", "5", "Assault 1"),
    "Heavy Flamer": ("Template", "5", "4", "Assault 1"),
    "Plasma Pistol": ('12"', "7", "2", "Pistol, Gets Hot"),
    "Needle Pistol": ('12"', "1", "5", "Pistol, Poisoned (2+), Rending"),
    "Assault Needler": ('18"', "1", "5", "Assault 2, Poisoned (2+), Rending"),
    "Needle Cannon": ('24"', "1", "5", "Heavy 4, Poisoned (2+), Rending, Pinning"),
    "Stake Crossbow": ('24"', "3", "5", "Assault 2, Psyker Bane"),
    "Toxiferran Flamer": ("Template", "1", "3", "Assault 1, Poisoned (2+)"),
    "Snare Gun": ('18"', "-", "-", "Assault 1, Snare"),
    "Snare Cannon": ('18"', "-", "-", "Heavy 3, Snare"),
    "Hellion Pattern Heavy Cannon Array": ('24"', "7", "4", "Heavy 4, Twin-Linked, Pinning"),
    "Twin-linked Multi-Melta": ('24"', "8", "1", "Heavy 1, Melta, Twin-Linked"),
    "Hunter-Killer Missile": ("Unlimited", "8", "3", "Heavy 1, One Shot"),
    "Close Combat Weapon": ("-", "User", "-", "Close Combat Weapon"),
    "Claws and Fangs": ("-", "User", "-", "Close Combat Weapon, Rending"),
    "Power Weapon": ("-", "User", "-", "Power Weapon"),
    "Power Fist": ("-", "x2", "-", "Power Weapon, Unwieldy"),
    "Execution Blade": ("-", "+1", "-", "Two-handed, Rending (5+)"),
    "Charnabal Sabre": ("-", "User", "-", "Close Combat Weapon, Rending"),
    "Proteus Neuro-Lash": ("-", "+1", "-", "Two-handed, Electro-arc, Sweeping Strikes"),
    "Power Stake": ("-", "User", "-", "Power Weapon; wounds Psykers on 2+"),
    "Relic Blade": ("-", "6", "-", "Two-handed, Power Weapon"),
    "Master-Crafted Relic Blade": ("-", "6", "-", "Two-handed, Power Weapon, Master-Crafted"),
    "Null Rod": ("-", "User", "-", "Power Weapon"),
    # Assassins
    "Exitus Rifle": ('36"', "X", "2", "Heavy 1; hits on 2+, wounds non-vehicles on 4+"),
    "Exitus Pistol": ('12"', "5", "2", "Pistol"),
    "Animus Speculum": ('12"', "5", "1", "Assault 2 (+1 per Psyker within 12\")"),
    "C'tan Phase Sword": ("-", "User", "-", "Power Weapon; no Armour or Invulnerable Saves"),
    "Neural Shredder": ("Template", "8", "1", "Assault 1; wounds against Leadership"),
    "Neuro-Gauntlet": ("-", "-", "-", "Wounds non-vehicles on 4+, ignores Armour Saves"),
    "Nemesii Blade": ("-", "User", "-", "Power Weapon, Shred; 5+ To Hit wounds automatically"),
    "Toxin Ejector": ("Template", "5", "4", "Assault 1, Poisoned (3+)"),
    "Poison Globes": ('8"', "1", "3", "Assault 1, Blast, Poisoned (3+), Pinning, One Shot"),
    "Hookfang": ("-", "User", "-", "Poisoned (3+), Rending, Venum"),
    "Sympatic Dataspikes": ("-", "User", "-", "Rending, Concussive, +2 Attacks"),
}

MULTI = {
    "Guardian Spear": {"Guardian Spear": SPEAR_MELEE, "Guardian Spear Boltgun": GS_BOLT},
    "Pyrithite Spear": {"Pyrithite Spear": SPEAR_MELEE, "Pyrithite Weapon": ('12"', "8", "1", "Assault 1, Melta")},
    "Adrasite Spear": {"Adrasite Spear": SPEAR_MELEE,
                       "Adrasite Weapon": ('12"', "5", "2", "Assault 1, Disintegration")},
    "Paragon Spear": {"Paragon Spear": ("-", "+2", "-", "Two-handed, Power Weapon; 6s To Hit give one extra attack; "
                                                       "6s To Wound inflict a Massive Wound"),
                      "Guardian Spear Boltgun": GS_BOLT},
    "Sentinel Warblade": {"Sentinel Warblade": ("-", "User", "-", "Power Weapon"),
                          "Sentinel Warblade Boltgun": ('12"', "5", "4", "Assault 2")},
    "Meridian Power Blades": {
        "Meridian Power Blades - Measured Strike": ("-", "10", "-", "One Attack only, ignores Armour Saves, Massive "
                                                                     "Wound"),
        "Meridian Power Blades - Lethal Precision": ("-", "+1", "-", "Power Weapon; 6s To Wound inflict a Massive Wound"),
        "Meridian Power Blades - Storm of Blades": ("-", "User", "-", "Power Weapon, +2 Attacks")},
    "The Apollonian Spear": {
        "The Apollonian Spear": ("-", "+1 (+2 on the charge)", "-", "Two-handed, Power Weapon; 6s To Hit give one extra "
                                                                     "attack; Molecular Severance"),
        "Hyper-velocity Bolter": ('18"', "5", "2", "Assault 2, Concussive")},
    "Venatari Lance": {"Venatari Lance": ("-", "User (+1 on the charge)", "-", "Two-handed, Power Weapon; 6s To Hit "
                                                                               "give one extra attack"),
                       "Archaeotech Repeater": ('12"', "7", "3", "Assault 2, Master-Crafted")},
    "Achillus Dreadspear with inbuilt Corvae Las-Pulser": {
        "Achillus Dreadspear": ("-", "10", "-", "Dreadnought CCW, Master-Crafted, Lance; Massive Wounds on the charge"),
        "Corvae Las-Pulser": ('36"', "9", "2", "Heavy 2")},
    "Galatus Warblade with inbuilt Twin-linked Infernus Incinerator": {
        "Galatus Warblade": ("-", "x2", "-", "Dreadnought CCW, Shred, Rampage"),
        "Infernus Incinerator": ("Template", "6", "4", "Heavy 1, Twin-Linked")},
    "Telemon Caestus with inbuilt Proteus Plasma Projector": {
        "Telemon Caestus": ("-", "x2", "-", "Dreadnought CCW, Shred; 6s To Wound inflict a Massive Wound"),
        "Proteus Plasma Projector": ("Template", "5", "2", "Assault 1, Gets Hot")},
    "Arachnus Storm Cannon": {"Arachnus Storm Cannon - Burst": ('48"', "7", "3", "Heavy 7"),
                              "Arachnus Storm Cannon - Concentrated": ('72"', "9", "1", "Heavy 2, Exoshock")},
    "Twin-linked Arachnus Blaze Cannon": {
        "Arachnus Blaze Cannon - Concentrated": ('48"', "8", "1", "Heavy 1, Exoshock, Twin-Linked"),
        "Arachnus Blaze Cannon - Burst": ('36"', "6", "5", "Heavy 3, Twin-Linked")},
    "Twin-linked Arachnus Heavy Blaze Cannon": {
        "Arachnus Heavy Blaze Cannon - Concentrated": ('72"', "10", "1", "Heavy 1, Exoshock, Twin-Linked"),
        "Arachnus Heavy Blaze Cannon - Burst": ('48"', "8", "3", "Heavy 4, Twin-Linked")},
    "Krak Grenades": {"Krak Grenade": ("-", "6", "-", "Against vehicles only: 6 + D6 Armour Penetration")},
    "Melta Bombs": {"Melta Bomb": ("-", "8", "-", "Against vehicles only: 8 + 2D6 Armour Penetration")},
    "Psyk-out Grenades": {"Psyk-out Grenade": ('6"', "-", "-", "Assault 1, Psyk-out; only affects Psykers")},
    # Sisters
    "Heavy Bolter": {"Heavy Bolter": ('36"', "5", "4", "Heavy 3"),
                     "Psyk-out Heavy Bolts": ('36"', "5", "4", "Heavy 3, Witchbane")},
    "Compression Flamer": {"Compression Flamer": ("Template", "5", "4", "Assault 1"),
                           "Compression Flamer - Projected": ('12"', "5", "4", "Assault 1")},
    "Vratine Missile Launcher": {
        "Vratine Missile - Frag": ('48"', "4", "6", "Heavy 1, Blast"),
        "Vratine Missile - Krak": ('48"', "8", "3", "Heavy 1"),
        "Vratine Missile - Psyk-out": ('48"', "4", "5", "Heavy 1, Blast, Psyk-out")},
    "Twin-linked Vratine Missile Launcher": {
        "Twin-linked Vratine Missile - Frag": ('48"', "4", "6", "Heavy 1, Blast, Twin-Linked"),
        "Twin-linked Vratine Missile - Krak": ('48"', "8", "3", "Heavy 1, Twin-Linked"),
        "Twin-linked Vratine Missile - Psyk-out": ('48"', "4", "5", "Heavy 1, Blast, Psyk-out, Twin-Linked")},
    "Special Issue Ammunition": {
        "Dragonfire Bolts": ('24"', "4", "5", "Rapid Fire, Ignores Cover"),
        "Hellfire Bolts": ('24"', "X", "5", "Rapid Fire, Hellfire"),
        "Kraken Bolts": ('30"', "4", "4", "Rapid Fire"),
        "Vengeance Rounds": ('18"', "4", "3", "Rapid Fire, Gets Hot"),
        "Psyk-out Bolts": ('24"', "4", "5", "Rapid Fire, Witchbane")},
    "Combi-Flamer": {"Boltgun": ('24"', "4", "5", "Rapid Fire"), "Flamer": ("Template", "4", "5", "Assault 1")},
    "Combi-Meltagun": {"Boltgun": ('24"', "4", "5", "Rapid Fire"), "Meltagun": ('12"', "8", "1", "Assault 1, Melta")},
    "Combi-Plasma Gun": {"Boltgun": ('24"', "4", "5", "Rapid Fire"),
                         "Plasma Gun": ('24"', "7", "2", "Rapid Fire, Gets Hot")},
    "Combi-Snare Gun": {"Boltgun": ('24"', "4", "5", "Rapid Fire"), "Snare Gun": ('18"', "-", "-", "Assault 1, Snare")},
    "Paired Bolt Pistols": {"Bolt Pistol": ('12"', "4", "5", "Pistol")},
    "Paired Hand Flamers": {"Hand Flamer": ("Template", "3", "6", "Pistol")},
    "Paired Needle Pistols": {"Needle Pistol": ('12"', "1", "5", "Pistol, Poisoned (2+), Rending")},
    "Paired Plasma Pistols": {"Plasma Pistol": ('12"', "7", "2", "Pistol, Gets Hot")},
    "Pintle-mounted Storm Bolter": {"Storm Bolter": ('24"', "4", "5", "Assault 2")},
    # Assassins
    "Executioner Pistol": {"Executioner Pistol - Bolt Pistol": ('12"', "4", "5", "Pistol"),
                           "Executioner Pistol - Needle Pistol": ('12"', "X", "6", "Pistol; wounds non-vehicles on 4+")},
    "Needlespine Blaster": {"Needlespine Blaster - Bolt Pistol": ('12"', "4", "5", "Pistol"),
                            "Needlespine Launcher": ('12"', "6", "4", "Assault 3, Rending (5+), Phage, One Shot")},
    "Paired Laspistols": {"Laspistol": ('12"', "3", "-", "Pistol")},
}

WEAPON_RULES = {
    "Twin-linked Lastrum Bolt Cannon": ["Twin-Linked"], "Infernus Firepike": ["Torrent"],
    "Adrathic Destructor": ["Disintegration"], "Twin-linked Adrathic Destructor": ["Disintegration", "Twin-Linked"],
    "Adrathic Devastator": ["Disintegration"], "Twin-linked Adrathic Devastator": ["Disintegration", "Twin-Linked"],
    "Twin-linked Corvae Las-Pulser": ["Twin-Linked"], "Adrasite Spear": ["Disintegration", "Two-Handed"],
    "Pyrithite Spear": ["Melta", "Two-Handed"], "Guardian Spear": ["Two-Handed"], "Paragon Spear": ["Two-Handed"],
    "Archaeotech Kinetic Destroyer": ["Master-Crafted", "Fan-burst"], "Venatari Lance": ["Two-Handed", "Master-Crafted"],
    "Solarite Power Gauntlet": ["Unwieldy", "Master-Crafted"], "Solarite Power Talon": ["Shred"],
    "Pair of Solarite Power Talons": ["Shred"], "Solarite Power Lance": ["Armourbane"],
    "The Apollonian Spear": ["Two-Handed", "Concussive", "Molecular Severance"],
    "Spiculus Bolt Launcher": ["Rending", "Volley Fire"],
    "Iliastus Accelerator Culverin": ["Rending", "Heliothermic Detonation"],
    "Twin-linked Iliastus Accelerator Cannon": ["Twin-Linked", "Rending", "Rapid Tracking", "Heliothermic Detonation"],
    "Arachnus Storm Cannon": ["Exoshock"], "Twin-linked Arachnus Blaze Cannon": ["Exoshock", "Twin-Linked"],
    "Twin-linked Arachnus Heavy Blaze Cannon": ["Exoshock", "Twin-Linked"],
    "Achillus Dreadspear with inbuilt Corvae Las-Pulser": ["Master-Crafted", "Lance"],
    "Galatus Warblade with inbuilt Twin-linked Infernus Incinerator": ["Shred", "Rampage", "Twin-Linked"],
    "Telemon Caestus with inbuilt Proteus Plasma Projector": ["Shred", "Gets Hot"],
    "Plasma Pistol": ["Gets Hot"], "Paired Plasma Pistols": ["Gets Hot", "Paired Pistol Weapons"],
    "Paired Bolt Pistols": ["Paired Pistol Weapons"], "Paired Hand Flamers": ["Paired Pistol Weapons"],
    "Paired Needle Pistols": ["Paired Pistol Weapons", "Poisoned", "Rending"],
    "Needle Pistol": ["Poisoned", "Rending"], "Assault Needler": ["Poisoned", "Rending"],
    "Needle Cannon": ["Poisoned", "Rending", "Pinning"], "Stake Crossbow": ["Psyker Bane"],
    "Toxiferran Flamer": ["Poisoned"], "Snare Gun": ["Snare"], "Snare Cannon": ["Snare"],
    "Heavy Bolter": ["Witchbane"], "Vratine Missile Launcher": ["Psyk-out"],
    "Twin-linked Vratine Missile Launcher": ["Psyk-out", "Twin-Linked"],
    "Special Issue Ammunition": ["Hellfire", "Witchbane", "Ignores Cover", "Gets Hot"],
    "Combi-Flamer": ["Combi-Weapon"], "Combi-Meltagun": ["Combi-Weapon", "Melta"],
    "Combi-Plasma Gun": ["Combi-Weapon", "Gets Hot"], "Combi-Snare Gun": ["Combi-Weapon", "Snare"],
    "Hellion Pattern Heavy Cannon Array": ["Twin-Linked", "Pinning"], "Twin-linked Multi-Melta": ["Melta", "Twin-Linked"],
    "Hunter-Killer Missile": ["Hunter-Killer Missile"], "Psyk-out Grenades": ["Psyk-out"],
    "Execution Blade": ["Two-Handed", "Rending", "Modified Rending"], "Charnabal Sabre": ["Rending"],
    "Proteus Neuro-Lash": ["Two-Handed"], "Relic Blade": ["Two-Handed"],
    "Master-Crafted Relic Blade": ["Two-Handed", "Master-Crafted"], "Power Fist": ["Unwieldy"],
    "Claws and Fangs": ["Rending"], "Needlespine Blaster": ["Rending", "Modified Rending"],
    "Nemesii Blade": ["Shred"], "Toxin Ejector": ["Poisoned"], "Poison Globes": ["Poisoned", "Pinning"],
    "Hookfang": ["Poisoned", "Rending"], "Sympatic Dataspikes": ["Rending", "Concussive"],
}
for _w in ["Adrathic Destructor", "Twin-linked Adrathic Destructor", "Adrathic Devastator", "Twin-linked Adrathic Devastator",
           "Adrasite Spear", "Paragon Spear", "Meridian Power Blades", "The Apollonian Spear",
           "Achillus Dreadspear with inbuilt Corvae Las-Pulser", "Telemon Caestus with inbuilt Proteus Plasma Projector",
           "Iliastus Accelerator Culverin", "Twin-linked Iliastus Accelerator Cannon"]:
    WEAPON_RULES.setdefault(_w, [])
    WEAPON_RULES[_w] = WEAPON_RULES[_w] + ["Massive Wound"]

WARGEAR = {
    # Custodes
    "Custodian Armour": ("Confers a 2+ Armour Save and the Move Through Cover special rule.", ["Move Through Cover"]),
    "Aquilon Terminator Armour": (
        "Confers a 2+ Armour Save and a 4+ Invulnerable Save. Models wearing it have the Relentless, Hammer of Wrath and "
        "Very Bulky special rules. Counts as Terminator Armour for the purposes of rules, transport capacity and wargear "
        "restrictions.", ["Relentless", "Hammer of Wrath", "Very Bulky"]),
    "Praesidium Shield": (
        "Improves the bearer's Invulnerable Save by +1, to a maximum of 3+. A model with a Praesidium Shield may not use a "
        "Two-handed weapon and may not claim the +1 Attack for fighting with two close combat weapons. A model may never "
        "benefit from both a Praesidium Shield and an Advanced Praesidium Shield."),
    "Advanced Praesidium Shield": (
        "Improves the bearer's Invulnerable Save by +1, to a maximum of 3+. Unlike a normal Praesidium Shield, it does "
        "not prevent the bearer from using Two-handed weapons or claiming the bonus Attack for fighting with two close "
        "combat weapons. A model may never benefit from both a Praesidium Shield and an Advanced Praesidium Shield."),
    "Refractor Field": "Confers a 5+ Invulnerable Save.",
    "Iron Halo": "Confers a 4+ Invulnerable Save.",
    "Teleportation Transponder": (
        "A unit in which every model is equipped with a Teleportation Transponder gains the Deep Strike special rule. An "
        "Independent Character joining the unit must also possess one for the unit to use this ability.", ["Deep Strike"]),
    "Arae-Shrikes": ("Enemy units may not deploy using Deep Strike within 8\" of a model equipped with Arae-Shrikes. "
                     "Multiple Arae-Shrikes do not increase this distance."),
    "Magisterium Vexilla": (
        "A unit containing a Magisterium Vexilla may re-roll failed Leadership tests and causes Fear. When determining the "
        "winner of a close combat, add +1 to the friendly side's combat resolution if at least one friendly model "
        "involved in that combat is within 12\" of a Magisterium Vexilla (does not stack).", ["Fear"]),
    "Guardian Spear": (
        "A Two-handed Power Weapon which grants the bearer +1 Strength. For every unmodified roll of 6 To Hit in close "
        "combat, the bearer immediately makes one additional attack with it (these cannot generate further attacks). "
        "Incorporates a Guardian Spear Boltgun."),
    "Pyrithite Spear": "Follows all of the rules for a Guardian Spear but replaces its built-in boltgun with a Pyrithite "
                       "Weapon.",
    "Adrasite Spear": "Follows all of the rules for a Guardian Spear but replaces its built-in boltgun with an Adrasite "
                      "Weapon.",
    "Paragon Spear": (
        "A Two-handed Power Weapon which grants the bearer +2 Strength. For every unmodified roll of 6 To Hit, the bearer "
        "immediately makes one additional attack (these cannot generate further attacks). An unmodified roll of 6 To "
        "Wound inflicts a Massive Wound. Incorporates a Guardian Spear Boltgun."),
    "Sentinel Warblade": ("A Power Weapon incorporating a Sentinel Warblade Boltgun. This weapon may also be fired when "
                          "making Snap Shots at BS2."),
    "Solarite Power Gauntlet": "Counts as a Master-Crafted Power Fist.",
    "Solarite Power Talon": ("A Power Weapon with the Shred special rule. A model with a pair of Solarite Power Talons "
                             "receives the normal +1 Attack for fighting with two close combat weapons."),
    "Pair of Solarite Power Talons": ("Two Solarite Power Talons (Power Weapons with Shred). The bearer receives the "
                                      "normal +1 Attack for fighting with two close combat weapons."),
    "Meridian Power Blades": (
        "At the beginning of each Assault phase, select one fighting style. MEASURED STRIKE: the model makes only one "
        "Attack, resolved at Strength 10, ignoring Armour Saves and inflicting a Massive Wound if successful. LETHAL "
        "PRECISION: attacks are resolved at +1 Strength and count as Power Weapon attacks; an unmodified 6 To Wound "
        "inflicts a Massive Wound. STORM OF BLADES: attacks count as Power Weapon attacks and the bearer receives +2 "
        "Attacks for that Assault phase."),
    "The Apollonian Spear": (
        "A Two-handed Power Weapon. Attacks are resolved at +1 Strength, increased to +2 Strength on a turn in which "
        "Valdor charges. Every unmodified 6 To Hit generates one additional attack (these cannot generate further "
        "attacks). Molecular Severance. Incorporates a Hyper-velocity Bolter."),
    "Achillus Dreadspear with inbuilt Corvae Las-Pulser": (
        "The Achillus Dreadspear is a Master-Crafted Dreadnought Close Combat Weapon. Attacks are resolved at Strength 10 "
        "and have the Lance special rule. On a turn in which the Dreadnought charges, successful wounds caused by the "
        "Dreadspear inflict Massive Wounds. The Dreadspear incorporates a Corvae Las-Pulser."),
    "Galatus Warblade with inbuilt Twin-linked Infernus Incinerator": (
        "The Galatus Warblade counts as a Dreadnought Close Combat Weapon with the Shred and Rampage special rules. It "
        "incorporates a Twin-linked Infernus Incinerator."),
    "Telemon Caestus with inbuilt Proteus Plasma Projector": (
        "The Telemon Caestus counts as a Dreadnought Close Combat Weapon with the Shred special rule. On an unmodified "
        "roll of 6 To Wound, the attack inflicts a Massive Wound. Incorporates a Proteus Plasma Projector."),
    "Dreadnought Praesidium Shield": (
        "When the Contemptor-Galatus suffers an attack originating from its Front Armour arc, or an attack in close "
        "combat, it may re-roll failed Invulnerable Saves. Enemy models suffer -1 To Hit when making close combat attacks "
        "against the Contemptor-Galatus (not Gargantuan models or attacks which hit automatically)."),
    "Multi-layer Refractor Field": ("The Telemon has a 4+ Invulnerable Save against Glancing and Penetrating Hits, "
                                    "improved to 3+ against attacks made with Blast or Template weapons."),
    "Gyrfalcon Jetbike": ("Follows all the normal rules for Jetbikes and increases the rider's Toughness by +1, as shown "
                          "in the model's profile."),
    "Solarite Power Lance": (
        "Counts as a Power Weapon. On a turn in which the bearer charges, he may resolve up to two of his normal close "
        "combat attacks at Initiative 10; these are resolved at Strength 8 and have Armourbane. Remaining attacks are "
        "resolved normally. In subsequent rounds it simply counts as a Power Weapon."),
    "Custodian Jump Harness": "Confers a 3+ Armour Save and causes the bearer to count as Jump Infantry.",
    "Tarsus Buckler": (
        "Counts as a +1 Strength Power Weapon. Energy Nullifier: Power Weapons and Lightning Claws do not negate the "
        "bearer's normal Armour Save (no effect against Power Fists, Thunder Hammers or similarly powerful weapons)."),
    "Venatari Lance": (
        "A Two-handed Power Weapon. On a turn in which the bearer charges, its attacks are resolved at +1 Strength. Every "
        "unmodified 6 To Hit generates one additional attack (these cannot generate further attacks). Incorporates an "
        "Archaeotech Repeater."),
    "Flare Shield": ("Ranged attacks which strike the vehicle's Front Armour suffer -1 Strength; Blast and Template "
                     "weapons instead suffer -2 Strength. No effect against close combat attacks."),
    "Machine Spirit": ("Power of the Machine Spirit: A vehicle moving less than flat out speed and not using smoke "
                       "launchers can fire one additional main weapon at full Ballistic Skill.",
                       ["Power of the Machine Spirit"]),
    "Armoured Ceramite": ("Melta Bombs and weapons with the Melta special rule do not roll an additional D6 for Armour "
                          "Penetration against a vehicle with Armoured Ceramite."),
    "Extra Armour": ("", ["Extra Armour"]),
    "Searchlight": ("", ["Searchlight"]),
    "Smoke Launchers": ("", ["Smoke Launchers"]),
    "Dozer Blade": ("", ["Dozer Blade"]),
    "Plasma Grenades": (
        "ASSAULT/FRAG/PLASMA GRENADES: Any model equipped with assault, frag, or plasma grenades (or other equipment "
        "that provides a similar effect) that charged into the melee combat this turn ignores the initiative penalty for "
        "charging through cover (the models attack at its normal initiative value)."),
    "Frag Grenades": "As described in the ProHammer rules.",
    "Krak Grenades": "As described in the ProHammer rules.",
    "Melta Bombs": "As described in the ProHammer rules.",
    # Sisters
    "Vratine Armour": "Confers a 3+ Armour Save.",
    "Artificer Armour": "Confers a 2+ Armour Save.",
    "Voidsheen Cloak": "Confers a 5+ Invulnerable Save.",
    "Enhanced Voidsheen Cloak": "Confers a 4+ Invulnerable Save, improved to 3+ against wounds caused by Blast or "
                                "Template weapons.",
    "Psyk-out Grenades": ("Thrown instead of firing another weapon, range 6\". Roll To Hit as normal; only affects "
                          "Psykers. A Psyker hit must take a Leadership test on 2D6; for every point by which it is "
                          "failed, the Psyker/unit suffers one wound (saves allowed)."),
    "Augury Scanner": ("The bearer and her unit may detect enemy infiltrators and other concealed threats as described "
                       "in the ProHammer rules."),
    "Master-Crafted Weapon": ("One weapon carried by the model is upgraded to Master-Crafted.", ["Master-Crafted"]),
    "Null Rod": ("Counts as a Power Weapon. The bearer and any unit she has joined cannot be affected by Psychic Powers. "
                 "Models in the unit may not use Psychic Powers themselves."),
    "Execution Blade": "Strength +1, Two-handed, Rending (5+).",
    "Charnabal Sabre": "Counts as a close combat weapon with the Rending special rule.",
    "Proteus Neuro-Lash": (
        "Strength +1, Two-handed. Electro-arc: for every successful hit, roll a D6; on a 3+ the target suffers one "
        "additional Poisoned (4+) hit. Sweeping Strikes: instead of her normal Attacks characteristic, the bearer may make "
        "a number of attacks equal to the number of enemy models within 3\" engaged in the same combat."),
    "Power Stake": "Counts as a Power Weapon. Against Psykers, attacks made with a Power Stake always wound on a 2+.",
    "Relic Blade": "Two-handed Power Weapon. The bearer strikes at S6.",
    "Master-Crafted Relic Blade": "Two-handed, Master-Crafted Power Weapon. The bearer strikes at S6.",
    "Jump Packs": "The model counts as Jump Infantry (if the entire squad is equipped).",
    "Erinyes Pattern Jetbike": ("Follows all the normal rules for Jetbikes and increases the rider's Toughness by +1, as "
                                "shown in the model's profile."),
    "Special Issue Ammunition": (
        "Each time the unit fires its Boltguns, select one ammunition type; every eligible model in the unit must use the "
        "same type during that Shooting phase. May also be used by the Bolter component of a Combi-Weapon."),
    "Heavy Bolter": "Expurgators equipped with Heavy Bolters may fire Psyk-out Heavy Bolts instead of normal ammunition.",
    "Compression Flamer": "A model with Compression Tanks may use either the Template or Projected profile each time it "
                          "fires.",
    "Spectra-Distort Field": ("The Kharon Pattern Acquisitor has the Stealth special rule. Shooting attacks made against "
                              "it from more than 12\" away suffer -1 Ballistic Skill, to a minimum of BS1.", ["Stealth"]),
    # Assassins
    "Exitus Rifle": (
        "Hits on a 2+ and wounds non-vehicle models on a 4+, regardless of Toughness; cannot normally damage vehicles. "
        "The Vindicare carries one of each special round, each fired once per battle instead of a normal shot (declare "
        "before rolling To Hit). SHIELD-BREAKER ROUND: Invulnerable Saves granted by wargear may not be taken (natural "
        "Invulnerable Saves are unaffected). TURBO-PENETRATOR ROUND: a model wounded suffers 2 Wounds instead of 1; "
        "against a vehicle roll 3D6 for Armour Penetration. HELLFIRE ROUND: wounds non-vehicle models on a 2+."),
    "Spy Mask": ("Cover Saves taken against shooting attacks made by the Vindicare are worsened by 1. When determining "
                 "how far the Vindicare can see using Night Fighting rules, roll 2D6 x 5\"."),
    "Stealth Suit": ("Any enemy unit wishing to shoot at the Vindicare must check whether it can see him using the Night "
                     "Fighting rules, even if Night Fighting is not otherwise in effect. If Night Fighting is in effect, "
                     "halve the distance rolled."),
    "Animus Speculum": "For every Psyker model within 12\" of the Culexus, increase the weapon's Assault value by +1.",
    "C'tan Phase Sword": "Counts as a Power Weapon. Neither Armour Saves nor Invulnerable Saves may be taken against "
                         "wounds it causes.",
    "Neural Shredder": (
        "When rolling To Wound, use the target's Leadership instead of its Toughness. Against vehicles, do not roll for "
        "Armour Penetration; if the vehicle is hit, roll a D3 directly on the Glancing Hit table (no modifiers)."),
    "Polymorphine": ("The Callidus always begins the battle in Reserve. When she becomes available, place her anywhere "
                     "on the battlefield more than 1\" from an enemy model; she may move, shoot and charge normally that "
                     "turn."),
    "Poison Blades": (
        "If the Callidus remains in base contact with an enemy model at the end of the Assault phase, after all combats "
        "and consolidation, she may make one additional attack: roll To Hit normally; a hit wounds on a 4+ regardless of "
        "Toughness and ignores Armour Saves (Invulnerable Saves allowed)."),
    "Executioner Pistol": ("Fire either profile. The Needle Pistol profile always wounds non-vehicle models on a 4+; "
                           "against vehicles roll a single D6 for Armour Penetration."),
    "Neuro-Gauntlet": ("A close combat weapon. Each hit wounds a non-vehicle model on a 4+ regardless of Toughness and "
                       "ignores Armour Saves (Invulnerable Saves allowed). Against vehicles, each hit causes a Glancing "
                       "Hit on an unmodified D6 roll of 6."),
    "Combat Drugs": ("The Eversor may charge up to 12\"; when charging through Difficult Terrain, double the distance it "
                     "would normally be allowed to charge. Whenever it charges it gains +D6 Attacks instead of +1."),
    "Needlespine Blaster": ("Fire either profile. PHAGE: a model suffering one or more unsaved wounds from the "
                            "Needlespine Launcher reduces its Toughness by 1 for the rest of the battle (minimum 1, does "
                            "not stack)."),
    "Nemesii Blade": "Counts as a Power Weapon with Shred. An unmodified 5+ To Hit automatically wounds the target.",
    "Nemesii Grenades": ("Any enemy unit charging the Adamus counts as charging through Difficult Terrain, and models "
                         "charging her do not receive the +1 Attack bonus for charging."),
    "Hookfang": (
        "A close combat weapon with Poisoned (3+) and Rending. THE VENUM: a model suffering one or more unsaved wounds "
        "from it must take a Toughness test at the end of each subsequent Battle Round; if failed it suffers one Wound "
        "with no Armour or Invulnerable Saves. A model may only be affected once; the effect lasts the battle."),
    "Paired Laspistols": "The Vanus may fire both Laspistols during the Shooting phase at the same enemy unit.",
    "Sympatic Dataspikes": "Close combat weapons with Rending and Concussive. The Vanus receives +2 Attacks when fighting "
                           "with them.",
    "Etherium": (
        "Any enemy unit wishing to shoot at or charge the Culexus Assassin must first pass a Leadership test. A Psyker "
        "attempting to target the Culexus with a Psychic Power must also pass this test. If the test is failed, that "
        "unit or Psyker may not target the Culexus during that phase, but may choose another eligible target."),
}

# ================================================================ helpers
SLOT = {HQ: "HQ", TROOPS: "Troops", ELITES: "Elites", FA: "Fast Attack", HS: "Heavy Support"}
CORONUS = k("transport", "Coronus Grav-Carrier")
RHINO = k("transport", "Anathema Psykana Rhino")
KHARON = k("transport", "Kharon Pattern Acquisitor")
TRANSPORT_IDS = {"Legio Custodes Coronus Grav-Carrier": CORONUS, "Anathema Psykana Rhino": RHINO,
                 "Kharon Pattern Acquisitor": KHARON}
VALDOR = k("unit", "Constantin Valdor")
KROLE = k("unit", "Jenetia Krole")
KNIGHT_ABYSSAL = k("unit", "Sisters of Silence Knight-Abyssal")
KNIGHT_CENTURA = k("unit", "Sisters of Silence Oblivion Knight-Centura")
SHADOW_TT = k("shared", "shadow-tt")
VALDOR_WL = k("upgrade", "Constantin Valdor is the army's Warlord")
NOT_VALDOR_WL = [cond(VALDOR_WL, "roster", "lessThan", 1)]
TWO_HANDED = ["Guardian Spear", "Adrasite Spear", "Pyrithite Spear", "Paragon Spear"]


def gear_n(key, name, n):
    lid = uid("link", key, name, n)
    return link(lid, W(name), name, constraints=[constraint(uid(lid, "min"), "min", n),
                                                 constraint(uid(lid, "max"), "max", n, auto=True)])


def kit_entry(key, name, items, cost=0):
    """Inline entry bundling several items (used for 'replace X with Y and Z' choices)."""
    eid = uid(key, "kit", name)
    return entry(eid, name, cost=cost, constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                 links=[gear(eid, i) for i in items])


def transport_grp(u, options):
    """options: [(transport name, max models or None)]. At most one Dedicated Transport."""
    gid = uid("grp", u, "transport")
    links = []
    for n, mx in options:
        lid = uid("link", gid, n)
        mods = []
        if mx:
            big = [cond("model", u, "greaterThan", mx)]
            mods = [modifier("set", uid(lid, "max"), 0, conds=big), modifier("set", "hidden", "true", conds=big)]
        links.append(link(lid, TRANSPORT_IDS[n], n, mods=mods, constraints=[constraint(uid(lid, "max"), "max", 1,
                                                                                         auto=True)]))
    return group(gid, "Dedicated Transport", links=links, constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


def block_group(g, conds):
    """Hide a group and set its max to 0 while any condition is true."""
    mx = uid(g.get("id"), "max")
    add_mods(g, [modifier("set", "hidden", "true", groups=[any_of(*conds)]),
                 modifier("set", mx, 0, groups=[any_of(*conds)])])
    if g.find("constraints") is None or not any(c.get("id") == mx for c in g.iter("constraint")):
        add_to(g, "constraints", [constraint(mx, "max", 1, auto=True)])
    return g


def forbid_item(g, name, conds):
    """Set the max of the option `name` inside group g to 0 while any condition is true (error if taken)."""
    for lk in g.iter("entryLink"):
        if lk.get("name") == name:
            mx = uid(lk.get("id"), "max")
            if not any(c.get("id") == mx for c in lk.iter("constraint")):
                add_to(lk, "constraints", [constraint(mx, "max", 1, auto=True)])
            add_mods(lk, [modifier("set", mx, 0, groups=[any_of(*conds)])])
    return g


def no_two_handed_shield(g, mid):
    """A Praesidium Shield may not be used with a Two-handed weapon (author's answer Q12)."""
    return forbid_item(g, "Praesidium Shield", [has(W(n), mid) for n in TWO_HANDED])


def custodes_tt(u):
    """Teleportation Transponders for the whole unit (+5/model) or free via The Shadow of the Throne."""
    no_valdor = NOT_VALDOR_WL
    lid = uid("link", u, "shadow-tt")
    return [per_model(u, "Teleportation Transponders (entire squad)", 5, u, ["Teleportation Transponder"]),
            link(lid, SHADOW_TT, "Teleportation Transponders (The Shadow of the Throne, free)",
                 mods=[modifier("set", "hidden", "true", conds=no_valdor),
                       modifier("set", uid(lid, "max"), 0, conds=no_valdor)],
                 constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])]


def shadow_tt_entry():
    return entry(SHADOW_TT, "Teleportation Transponders (The Shadow of the Throne, free)",
                 constraints=[constraint(uid(SHADOW_TT, "roster"), "max", 1, scope="roster", deep=True)],
                 infolinks=rules_links(["The Shadow of the Throne"], key=SHADOW_TT),
                 links=[gear(SHADOW_TT, "Teleportation Transponder")])


def size_error(u, ids, lo, hi, text):
    """Error if the number of models of the given entries is outside lo..hi (for units of several model types)."""
    conds_lo, conds_hi = [], []
    # model count over the whole unit is enough: these units only contain the listed models
    return error_if(text, [cond("model", u, "lessThan", lo), cond("model", u, "greaterThan", hi)])


def per_models(key, name, per, unit_id, model_ids, contains):
    """'+N points per <listed model>' for the whole unit."""
    eid = uid("squadwide", key, name)
    return entry(eid, name, mods=[modifier("increment", PTS, per, repeats=[repeat(m, unit_id, 1)]) for m in model_ids],
                 constraints=[constraint(uid(eid, "max"), "max", 1)], links=[gear(eid, c) for c in contains])


def required_choice(key, title, unit_id, options, default):
    """Squad-wide exclusive weapon choice with a default. options: [(name, pts per model, [items])]."""
    return choice(key, title, [(n, p, True, items, []) for n, p, items in options], unit_id=unit_id, required=True,
                  default=default)


# ============================================================ configuration
def army_config():
    eid = uid("cfg", "Allegiance")
    gid = uid(eid, "grp")
    loyal = entry(L.LOYALIST, "Loyalist", constraints=[constraint(uid(L.LOYALIST, "max"), "max", 1, auto=True)])
    traitor = entry(L.TRAITOR, "Traitor", constraints=[constraint(uid(L.TRAITOR, "max"), "max", 1, auto=True)],
                    mods=[modifier("add", "warning", "A Talons of the Emperor Detachment is always Loyalist unless a "
                                                     "scenario or campaign rule expressly states otherwise.",
                                   conds=[cond(L.TRAITOR, "force", "atLeast", 1)])])
    g = group(gid, "Allegiance", entries=[loyal, traitor], default=L.LOYALIST,
              constraints=[constraint(uid(gid, "min"), "min", 1, auto=True),
                           constraint(uid(gid, "max"), "max", 1, auto=True)])
    return entry(eid, "Allegiance & Army Rules",
                 cats=[category_link(gs.CAT_CONFIG, "Configuration", primary=True, key=eid)],
                 constraints=[constraint(uid(eid, "min"), "min", 1, scope="force", deep=True),
                              constraint(uid(eid, "max"), "max", 1, scope="force", deep=True)],
                 mods=[modifier("set", uid(eid, "min"), 0, conds=[cond(CAT_OPERATIVE, "force", "atLeast", 1)])],
                 infolinks=rules_links(["Talons of the Emperor", "The Emperor's Talons", "Companions of the Ten Thousand",
                                        "Dedicated Transports (Talons)"], key=eid),
                 groups=[g])


# ================================================================ Custodes
SPEAR_SWAPS = [("Sentinel Warblade", 0), ("Solarite Power Talon", 15), ("Pair of Solarite Power Talons", 20),
               ("Solarite Power Gauntlet", 20), ("Adrasite Spear", 10), ("Pyrithite Spear", 15)]


def talon_master():
    name = "Legio Custodes Talon Master"
    u = k("unit", name)
    mid = uid("model", u, "Talon Master")
    aq = [has(W("Aquilon Terminator Armour"), mid)]
    tda_weapons = take(mid, "Aquilon Terminator Armour weapon", [("Lastrum Storm Bolter", 0), ("Infernus Firepike", 10),
                                                                 ("Twin-linked Adrathic Destructor", 15)], max_total=1)
    block_group(tda_weapons, [lacks(W("Aquilon Terminator Armour"), mid)])
    m = model(u, "Talon Master", 1, 1, 0,
              unit_profile(u, "Talon Master", "Infantry (Character)", 5, 5, 5, 4, 3, 5, 3, 10, "2+"),
              kit=["Refractor Field", "Krak Grenades"],
              groups=[slot(mid, "Replace Guardian Spear", "Guardian Spear", SPEAR_SWAPS + [("Paragon Spear", 25)]),
                      slot(mid, "Armour", "Custodian Armour", [("Aquilon Terminator Armour", 20)]),
                      tda_weapons,
                      no_two_handed_shield(
                          take(mid, "Wargear", [("Melta Bombs", 5), ("Arae-Shrikes", 10), ("Teleportation Transponder", 5),
                                                ("Iron Halo", 15), ("Praesidium Shield", 15)]), mid)])
    return unit(name, 150, HQ, "HQ", models=[m], rules_=CUSTODES + ["Independent Character"], key=u)


def shield_captain():
    name = "Legio Custodes Shield-Captain"
    u = k("unit", name)
    mid = uid("model", u, "Shield-Captain")
    small = cond("any", "roster", "lessThan", 2000, field=PTS, deep=False)
    trib = upgrade(mid, "Legio Custodes Tribune", 50, rules_=["Legio Custodes Tribune", "Eternal Warrior"],
                   hide=[small])
    add_to(trib, "constraints", [unique(trib.get("id"))])
    m = model(u, "Shield-Captain", 1, 1, 0,
              unit_profile(u, "Shield-Captain", "Infantry (Character)", 6, 5, 5, 4, 4, 6, 5, 10, "2+"),
              kit=["Custodian Armour", "Iron Halo", "Krak Grenades"],
              groups=[slot(mid, "Replace Guardian Spear", "Guardian Spear",
                           SPEAR_SWAPS + [("Meridian Power Blades", 35), ("Paragon Spear", 25)]),
                      take(mid, "Wargear", [("Melta Bombs", 5), ("Arae-Shrikes", 15),
                                            ("Teleportation Transponder", 10)]),
                      no_two_handed_shield(take(mid, "Shield (one)", [("Praesidium Shield", 15),
                                                                     ("Advanced Praesidium Shield", 25)], max_total=1),
                                           mid)],
              entries=[trib])
    return unit(name, 220, HQ, "HQ", models=[m], rules_=CUSTODES + ["Independent Character"], key=u)


def valdor():
    name = "Constantin Valdor"
    u = VALDOR
    mid = uid("model", u, name)
    m = model(u, name, 1, 1, 0, unit_profile(u, name, "Infantry (Character)", 7, 5, 5, 4, 5, 6, 5, 10, "2+"),
              kit=["Custodian Armour", "The Apollonian Spear", "Iron Halo", "Arae-Shrikes", "Krak Grenades",
                   "Plasma Grenades"],
              groups=[take(mid, "The Shadow of the Throne (Valdor is the Warlord)", [("Teleportation Transponder", 0)],
                           max_total=1, hide=NOT_VALDOR_WL)],
              entries=[entry(VALDOR_WL, "Constantin Valdor is the army's Warlord",
                             constraints=[constraint(uid(VALDOR_WL, "max"), "max", 1, auto=True)],
                             infolinks=rules_links(["The Shadow of the Throne"], key=VALDOR_WL))])
    return unit(name, 325, HQ, "HQ", models=[m], key=u, constraints=[unique(u)],
                rules_=CUSTODES + ["Independent Character", "Eternal Warrior", "The Shadow of the Throne",
                                   "Molecular Severance"])


def guard_squad(name, cost, per, slot_cat, model_name, stats, kit, groups_fn, entries_fn, rules_=(), coronus=6):
    u = k("unit", name)
    mid = uid("model", u, model_name)
    m = model(u, model_name, 3, 10, per,
              unit_profile(u, model_name, *stats), kit=kit)
    groups = groups_fn(u, mid)
    if coronus:
        groups.append(transport_grp(u, [("Legio Custodes Coronus Grav-Carrier", coronus)]))
    return unit(name, cost - 3 * per, slot_cat, SLOT[slot_cat], models=[m], entries=entries_fn(u, mid), groups=groups,
                rules_=CUSTODES + list(rules_), key=u)


def arae(u):
    return take(u, "One model may take", [("Arae-Shrikes", 15)])


def hetaeron_shields(u, mid):
    """Shields for models without a Vexilla; a Praesidium Shield only for models that gave up their (Two-handed)
    Guardian Spear for a one-handed weapon."""
    vex = uid(u, "kit", "Magisterium Vexilla and Sentinel Warblade")
    g = model_swaps(u, "Any model without a Magisterium Vexilla: shield", u, [mid],
                    [("Praesidium Shield", 15), ("Advanced Praesidium Shield", 25)], minus=[vex])
    one_handed = [W(n) for n in ("Sentinel Warblade", "Solarite Power Talon", "Pair of Solarite Power Talons",
                                 "Solarite Power Gauntlet", "Meridian Power Blades")]
    for lk in g.iter("entryLink"):
        if lk.get("name") == "Praesidium Shield":
            mx = uid(lk.get("id"), "one-handed")
            add_to(lk, "constraints", [constraint(mx, "max", 0)])
            add_mods(lk, [modifier("increment", mx, 1, repeats=[repeat(x, u, 1)]) for x in one_handed] +
                     [modifier("decrement", mx, 1, repeats=[repeat(vex, u, 1)])])
    return g


def hetaeron():
    def groups(u, mid):
        vex = kit_entry(u, "Magisterium Vexilla and Sentinel Warblade", ["Magisterium Vexilla", "Sentinel Warblade"])
        return [model_swaps(u, "Any model: replace Guardian Spear", u, [mid],
                            [("Sentinel Warblade", 0), ("Solarite Power Talon", 15),
                             ("Pair of Solarite Power Talons", 20), ("Solarite Power Gauntlet", 20),
                             ("Meridian Power Blades", 45)], entries=[vex]),
                hetaeron_shields(u, mid),
                arae(u)]

    def entries(u, mid):
        return [per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]), *custodes_tt(u)]
    return guard_squad("Legio Custodes Hetaeron Guard Squad", 285, 95, ELITES, "Hetaeron Guard",
                       ("Infantry", 5, 5, 5, 4, 3, 5, 4, 10, "2+"),
                       ["Custodian Armour", "Guardian Spear", "Refractor Field", "Krak Grenades"], groups, entries)


def aquilon():
    def groups(u, mid):
        return [model_swaps(u, "Any model: replace Lastrum Storm Bolter", u, [mid],
                            [("Infernus Firepike", 10), ("Twin-linked Adrathic Destructor", 15)]),
                model_swaps(u, "Any model: replace Solarite Power Gauntlet", u, [mid], [("Solarite Power Talon", 0)]),
                arae(u)]

    def entries(u, mid):
        return custodes_tt(u)
    return guard_squad("Legio Custodes Aquilon Terminator Squad", 285, 95, ELITES, "Aquilon Terminator",
                       ("Infantry", 5, 5, 5, 4, 3, 5, 3, 9, "2+"),
                       ["Aquilon Terminator Armour", "Lastrum Storm Bolter", "Solarite Power Gauntlet"], groups,
                       entries, coronus=4)


def custodian_guard():
    def groups(u, mid):
        p, _ = pool(u, "For every three models, one may replace Guardian Spear (Vexilla bearer included)", u,
                    [("Adrasite Spear", 10), ("Pyrithite Spear", 15)], 0, every=3)
        vex = kit_entry(u, "Magisterium Vexilla and Sentinel Warblade", ["Magisterium Vexilla", "Sentinel Warblade"],
                        cost=10)
        # the Vexilla bearer counts towards the one-per-three limit (author's answer Q15)
        add_to(p, "selectionEntries", [vex])
        return [p, arae(u)]

    def entries(u, mid):
        return [per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]), *custodes_tt(u)]
    return guard_squad("Legio Custodes Custodian Guard Squad", 210, 70, TROOPS, "Custodian Guard",
                       ("Infantry", 5, 5, 5, 4, 2, 5, 3, 9, "2+"),
                       ["Custodian Armour", "Guardian Spear", "Refractor Field", "Krak Grenades"], groups, entries)


def sentinel_guard():
    def groups(u, mid):
        return [model_swaps(u, "Any model: replace Sentinel Warblade", u, [mid],
                            [("Solarite Power Talon", 10), ("Solarite Power Gauntlet", 15)]),
                take(u, "One Sentinel Guard may exchange his Praesidium Shield", [("Magisterium Vexilla", 0)]),
                arae(u)]

    def entries(u, mid):
        return [per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]), *custodes_tt(u)]
    return guard_squad("Legio Custodes Sentinel Guard Squad", 225, 75, TROOPS, "Sentinel Guard",
                       ("Infantry", 5, 5, 5, 4, 2, 5, 3, 9, "2+"),
                       ["Custodian Armour", "Sentinel Warblade", "Praesidium Shield", "Refractor Field",
                        "Krak Grenades"], groups, entries)


def sagittarum():
    def groups(u, mid):
        return [model_swaps(u, "Any model: replace Adrastus Bolt Caliver", u, [mid], [("Adrathic Destructor", 10)]),
                arae(u)]

    def entries(u, mid):
        return [per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]), *custodes_tt(u)]
    return guard_squad("Legio Custodes Sagittarum Guard Squad", 185, 65, HS, "Sagittarum Guard",
                       ("Infantry", 5, 5, 5, 4, 2, 5, 2, 9, "2+"),
                       ["Custodian Armour", "Adrastus Bolt Caliver", "Refractor Field", "Krak Grenades"], groups,
                       entries)


def agamatus():
    name = "Legio Custodes Agamatus Jetbike Squadron"
    u = k("unit", name)
    mid = uid("model", u, "Agamatus Custodian")
    m = model(u, "Agamatus Custodian", 3, 6, 95,
              unit_profile(u, "Agamatus Custodian", "Jetbike", 5, 5, 5, "4(5)", 2, 5, 3, 9, "2+"),
              kit=["Custodian Armour", "Gyrfalcon Jetbike", "Solarite Power Lance", "Lastrum Bolt Cannon",
                   "Refractor Field", "Krak Grenades"])
    return unit(name, 285 - 3 * 95, FA, "Fast Attack", models=[m], key=u, rules_=CUSTODES + ["Deep Strike"],
                entries=[per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                groups=[model_swaps(u, "Any model: replace Lastrum Bolt Cannon", u, [mid],
                                    [("Adrathic Devastator", 10), ("Twin-linked Corvae Las-Pulser", 15)])])


def venatari():
    name = "Legio Custodes Custodian Venatari Squad"
    u = k("unit", name)
    mid = uid("model", u, "Custodian Venatari")
    m = model(u, "Custodian Venatari", 3, 10, 65,
              unit_profile(u, "Custodian Venatari", "Jump Infantry", 5, 5, 5, 4, 2, 5, 2, 9, "3+"),
              kit=["Custodian Jump Harness", "Tarsus Buckler", "Archaeotech Kinetic Destroyer", "Refractor Field",
                   "Krak Grenades", "Plasma Grenades"])
    return unit(name, 210 - 3 * 65, FA, "Fast Attack", models=[m], key=u,
                rules_=CUSTODES + ["Fleet", "Move Through Cover", "Auramite Pinions"],
                entries=[per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                groups=[model_swaps(u, "Any model: replace Tarsus Buckler and Archaeotech Kinetic Destroyer", u, [mid],
                                    [("Venatari Lance", 10)])])


def achillus():
    name = "Legio Custodes Contemptor-Achillus Dreadnought"
    u = k("unit", name)
    mid = uid("model", u, "Contemptor-Achillus Dreadnought")
    dflt = entry(uid(mid, "ccw"), "Two Dreadnought Close Combat Weapons with inbuilt Lastrum Storm Bolters",
                 constraints=[constraint(uid(mid, "ccw", "max"), "max", 1, auto=True)],
                 links=[gear_n(uid(mid, "ccw"), "Dreadnought Close Combat Weapon", 2),
                        gear_n(uid(mid, "ccw"), "Lastrum Storm Bolter", 2)])
    m = model(u, "Contemptor-Achillus Dreadnought", 1, 1, 0,
              walker_profile(u, "Contemptor-Achillus Dreadnought", 6, 5, 8, 13, 13, 11, 5, 4),
              kit=["Refractor Field", "Extra Armour", "Smoke Launchers", "Searchlight"],
              groups=[slot(mid, "Weapons", None, [("Achillus Dreadspear with inbuilt Corvae Las-Pulser", 95)],
                           default_is_entry=dflt)])
    return unit(name, 280, ELITES, "Elites", models=[m], key=u, rules_=["Fleet", "Move Through Cover",
                                                                         "Counter-Attack"])


def galatus():
    name = "Legio Custodes Contemptor-Galatus Dreadnought"
    u = k("unit", name)
    m = model(u, "Contemptor-Galatus Dreadnought", 1, 1, 0,
              walker_profile(u, "Contemptor-Galatus Dreadnought", 6, 5, 8, 13, 13, 11, 5, 4),
              kit=["Galatus Warblade with inbuilt Twin-linked Infernus Incinerator", "Dreadnought Praesidium Shield",
                   "Refractor Field", "Extra Armour", "Smoke Launchers", "Searchlight"])
    return unit(name, 250, ELITES, "Elites", models=[m], key=u, rules_=["Fleet", "Move Through Cover",
                                                                         "Counter-Attack"])


def telemon():
    name = "Legio Custodes Telemon Heavy Dreadnought"
    u = k("unit", name)
    mid = uid("model", u, "Telemon Heavy Dreadnought")
    arms = []
    for i in (1, 2):
        key = uid(mid, "arm", i)
        dflt = entry(uid(key, "caestus"), "Telemon Caestus with inbuilt Proteus Plasma Projector",
                     constraints=[constraint(uid(key, "caestus", "max"), "max", 1, auto=True)],
                     links=[gear(uid(key, "caestus"), "Telemon Caestus with inbuilt Proteus Plasma Projector")])
        arms.append(slot(key, f"Arm {i}", None, [("Arachnus Storm Cannon", 40), ("Iliastus Accelerator Culverin", 25)],
                         default_is_entry=dflt))
    m = model(u, "Telemon Heavy Dreadnought", 1, 1, 0,
              walker_profile(u, "Telemon Heavy Dreadnought", 6, 5, 9, 13, 13, 12, 5, 4),
              kit=["Spiculus Bolt Launcher", "Multi-layer Refractor Field", "Armoured Ceramite", "Extra Armour",
                   "Smoke Launchers", "Searchlight"], groups=arms)
    return unit(name, 320, HS, "Heavy Support", models=[m], key=u,
                rules_=["Move Through Cover", "Unyielding Sentinel", "Indomitable Charge"])


def caladius():
    name = "Legio Custodes Caladius Grav-Tank"
    u = k("unit", name)
    mid = uid("model", u, "Caladius Grav-Tank")
    m = model(u, "Caladius Grav-Tank", 1, 1, 0,
              vehicle_profile(u, "Caladius Grav-Tank", "Vehicle (Skimmer, Fast)", 5, 13, 13, 11),
              kit=["Twin-linked Lastrum Bolt Cannon", "Flare Shield", "Machine Spirit", "Searchlight"],
              groups=[slot(mid, "Replace Twin-linked Iliastus Accelerator Cannon",
                           "Twin-linked Iliastus Accelerator Cannon", [("Twin-linked Arachnus Heavy Blaze Cannon", 25)]),
                      take(mid, "Vehicle Upgrades", [("Armoured Ceramite", 20), ("Extra Armour", 5)])])
    return unit(name, 220, HS, "Heavy Support", models=[m], key=u, rules_=["Deep Strike", "Outflank", "Grav-backwash"])


def pallas():
    name = "Legio Custodes Pallas Grav-Attack Squadron"
    u = k("unit", name)
    mid = uid("model", u, "Pallas Grav-Attack")
    m = model(u, "Pallas Grav-Attack", 1, 3, 85,
              vehicle_profile(u, "Pallas Grav-Attack", "Vehicle (Skimmer, Fast)", 5, 12, 11, 11),
              kit=["Flare Shield"],
              groups=[slot(mid, "Replace Twin-linked Arachnus Blaze Cannon", "Twin-linked Arachnus Blaze Cannon",
                           [("Twin-linked Adrathic Devastator", 20)]),
                      take(mid, "Vehicle Upgrades", [("Searchlight", 1), ("Extra Armour", 5)])])
    return unit(name, 0, FA, "Fast Attack", models=numbered(m, 3, 1), key=u,
                rules_=["Power of the Machine Spirit", "Deep Strike", "Outflank", "Grav-backwash"])


def coronus():
    n = "Legio Custodes Coronus Grav-Carrier"
    t = CORONUS
    return entry(t, n, typ="unit", cost=175,
                 cats=[category_link(gs.CAT_TRANSPORT, "Dedicated Transport", primary=True, key=t)],
                 profiles=[vehicle_profile(t, n, "Vehicle (Skimmer, Fast, Transport)", 5, 13, 12, 11),
                           transport_profile(t, n, "12 models (Custodian, Sentinel, Hetaeron or Sagittarum Guard Squad "
                                                   "of six models or fewer, or Aquilon Terminator Squad of four or "
                                                   "fewer)", "One access point at the rear", "-")],
                 infolinks=rules_links(["Deep Strike", "Outflank", "Grav-backwash"], key=t),
                 links=[gear(t, x) for x in ["Twin-linked Lastrum Bolt Cannon", "Twin-linked Arachnus Blaze Cannon",
                                             "Flare Shield", "Machine Spirit", "Searchlight"]],
                 groups=[take(t, "Vehicle Upgrades", [("Armoured Ceramite", 20), ("Extra Armour", 5)])])


# ================================================================= Sisters
PISTOLS = [("Hand Flamer", 5), ("Needle Pistol", 5)]
PRIME_PISTOLS = PISTOLS + [("Plasma Pistol", 10)]
SOS_TRANSPORT = [("Anathema Psykana Rhino", 10), ("Kharon Pattern Acquisitor", 12)]


def knight(name, model_name, cost, stats, rules_, key):
    u = key
    mid = uid("model", u, model_name)
    m = model(u, model_name, 1, 1, 0, unit_profile(u, model_name, "Infantry (Character)", *stats),
              kit=["Frag Grenades", "Psyk-out Grenades"],
              groups=[slot(mid, "Replace Execution Blade", "Execution Blade",
                           [("Power Weapon", 0), ("Power Stake", 5), ("Proteus Neuro-Lash", 10), ("Relic Blade", 15)]),
                      slot(mid, "Replace Bolt Pistol", "Bolt Pistol", PISTOLS + [("Plasma Pistol", 15)]),
                      slot(mid, "Armour", "Vratine Armour", [("Artificer Armour", 10)]),
                      take(mid, "Cloak (one)", [("Voidsheen Cloak", 10), ("Enhanced Voidsheen Cloak", 20)],
                           max_total=1),
                      take(mid, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5), ("Augury Scanner", 5),
                                            ("Null Rod", 15)]),
                      take(mid, "One weapon may be", [("Master-Crafted Weapon", 10)])])
    return unit(name, cost, HQ, "HQ", models=[m], key=u, rules_=SISTERS + rules_, groups=[vigil_retinue(u)])


VIGIL_RETINUE = k("unit", "Sisters of Silence Vigil Command Cadre", "retinue")


def vigil_command(retinue=False):
    name = "Sisters of Silence Vigil Command Cadre"
    u = VIGIL_RETINUE if retinue else k("unit", name)
    vs, qs, sj = (uid("model", u, n) for n in ("Vigil Sister", "Questora", "Silent Judge"))
    kit = ["Vratine Armour", "Boltgun", "Bolt Pistol", "Frag Grenades", "Psyk-out Grenades"]
    models = [model(u, "Vigil Sister", 3, 6, 15, unit_profile(u, "Vigil Sister", "Infantry", 4, 4, 3, 3, 1, 4, 1, 8,
                                                                "3+"), kit=kit),
              model(u, "Questora", 0, 2, 25, unit_profile(u, "Questora", "Infantry (Character)", 4, 4, 3, 3, 1, 4, 2, 9,
                                                          "3+"), kit=kit),
              model(u, "Silent Judge", 0, 1, 35, unit_profile(u, "Silent Judge", "Infantry (Character)", 5, 4, 3, 3, 2, 5,
                                                              2, 9, "3+"), kit=kit, rules_=["Ex Oblivio"])]
    # Questora / Silent Judge are upgraded Vigil Sisters: each one lowers the Vigil Sisters needed for the minimum 3
    add_mods(models[0], [modifier("decrement", uid(vs, "min"), 1, repeats=[repeat(x, u, 1)]) for x in (qs, sj)])
    melee = [("Execution Blade", 5), ("Power Weapon", 10), ("Power Stake", 10), ("Proteus Neuro-Lash", 15)]
    groups = [model_swaps(u, "Any model: replace Boltgun", u, [vs, qs, sj],
                          [("Flamer", 5), ("Assault Needler", 5), ("Stake Crossbow", 5)],
                          minus=[W(n) for n, _ in melee]),
              model_swaps(u, "Any Questora or Silent Judge: replace Boltgun", u, [qs, sj], melee),
              model_swaps(u, "Any model: replace Bolt Pistol", u, [vs, qs, sj], PISTOLS),
              take(u, "One model may take", [("Augury Scanner", 5)]),
              model_takes(u, "Every model may take", u, [vs, qs, sj], [("Krak Grenades", 2)])]
    mods = [size_error(u, [vs, qs, sj], 3, 6, "A Vigil Command Cadre contains 3-6 models (up to two Questora and one "
                                              "Silent Judge).")]
    e = unit(name, 0, HQ, "HQ", models=models, key=u, rules_=SISTERS + ["Command Cadre"], groups=groups, mods=mods)
    if retinue:
        # taken as a retinue of a Knight-Centura, Knight-Abyssal or Jenetia Krole: no HQ choice used
        e.remove(e.find("categoryLinks"))
    return e


def vigil_retinue(key):
    gid = uid("grp", key, "retinue")
    return group(gid, "Retinue (no HQ choice used)",
                 links=[link(uid("link", gid, "vigil"), VIGIL_RETINUE, "Sisters of Silence Vigil Command Cadre")],
                 constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


def krole():
    name = "Jenetia Krole"
    u = KROLE
    m = model(u, name, 1, 1, 0, unit_profile(u, name, "Infantry (Character)", 7, 5, 3, 3, 4, 6, 4, 10, "2+"),
              kit=["Artificer Armour", "Enhanced Voidsheen Cloak", "Master-Crafted Relic Blade", "Bolt Pistol",
                   "Psyk-out Grenades", "Frag Grenades", "Krak Grenades", "Melta Bombs"])
    return unit(name, 160, HQ, "HQ", models=[m], key=u, constraints=[unique(u)], groups=[vigil_retinue(u)],
                rules_=SISTERS + ["Ex Oblivio", "Independent Character", "Eternal Warrior",
                                  "Mistress of the Black Ships"])


def cadre(name, cost, slot_cat, sister, prime, per, mn, mx, sister_stats, prime_stats, kit, rules_, groups_fn,
          entries_fn=lambda u, s, p: [], prime_kit=None, transport=True, prime_rules=()):
    """Sisters of Silence squad: <mn> Sisters + 1 Prime, up to <mx> Sisters."""
    u = k("unit", name)
    sid, pid = uid("model", u, sister), uid("model", u, prime)
    pm = model(u, prime, 1, 1, 0, unit_profile(u, prime, "Infantry (Character)", *prime_stats),
               kit=prime_kit if prime_kit is not None else kit, rules_=prime_rules)
    sm = model(u, sister, mn, mx, per, unit_profile(u, sister, sister_stats[0], *sister_stats[1:]), kit=kit)
    groups = groups_fn(u, sid, pid)
    if transport:
        groups.append(transport_grp(u, SOS_TRANSPORT))
    return unit(name, cost - mn * per, slot_cat, SLOT[slot_cat], models=[pm, sm], key=u, rules_=SISTERS + rules_,
                groups=groups, entries=entries_fn(u, sid, pid)), u, sid, pid


def frag_krak(u):
    return [per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
            per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])]


def firebrand():
    def groups(u, s, p):
        return [model_swaps(u, "Any model: replace Paired Hand Flamers", u, [s, p],
                            [("Paired Bolt Pistols", 0), ("Paired Needle Pistols", 5), ("Paired Plasma Pistols", 15)])]

    def entries(u, s, p):
        return frag_krak(u) + [per_model(u, "Jump Packs (entire squad)", 5, u, ["Jump Packs"])]
    e, u, s, p = cadre("Sisters of Silence Firebrand Destroyer Cadre", 100, ELITES, "Firebrand Sister",
                       "Firebrand Prime", 20, 4, 9, ("Infantry", 4, 4, 3, 3, 1, 4, 1, 8, "3+"),
                       (4, 4, 3, 3, 1, 4, 2, 9, "3+"), ["Vratine Armour", "Paired Hand Flamers", "Psyk-out Grenades"],
                       ["Gunfighters", "Firebrand Jump Packs"], groups, entries)
    jp = uid("squadwide", u, "Jump Packs (entire squad)")
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == "Dedicated Transport":
            block_group(g, [has(jp, u)])
    add_prime(e, p, [take(p, "Firebrand Prime may take (one)", [("Power Weapon", 10), ("Power Stake", 10)],
                          max_total=1)])
    return e


def raptor_guard():
    def groups(u, s, p):
        return [model_swaps(u, "Any model: replace Relic Blade", u, [s, p], [("Execution Blade", 0), ("Power Stake", 0)]),
                model_swaps(u, "Any model: replace Bolt Pistol", u, [s, p], PRIME_PISTOLS)]

    def entries(u, s, p):
        return [per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]),
                per_model(u, "Upgrade to Enhanced Voidsheen Cloaks (entire squad)", 10, u,
                          ["Enhanced Voidsheen Cloak"])]
    kit = ["Vratine Armour", "Relic Blade", "Bolt Pistol", "Voidsheen Cloak", "Psyk-out Grenades", "Frag Grenades"]
    e, u, s, p = cadre("Sisters of Silence Raptor Guard", 120, ELITES, "Raptor Guard", "Raptor Prime", 30, 4, 8,
                       ("Infantry", 5, 4, 3, 3, 2, 5, 2, 9, "3+"), (5, 4, 3, 3, 2, 5, 3, 10, "3+"), kit,
                       ["Ex Oblivio", "Preferred Enemy"], groups, entries)
    add_prime(e, p, [take(p, "One weapon carried by the Raptor Prime may be", [("Master-Crafted Weapon", 10)])])
    return e


def excruciatus():
    def groups(u, s, p):
        return [model_swaps(u, "Any Questora: replace Boltgun", u, [s],
                            [("Assault Needler", 5), ("Stake Crossbow", 5), ("Flamer", 5), ("Snare Gun", 10)]),
                model_swaps(u, "Any model: replace Bolt Pistol", u, [s, p], PISTOLS),
                take(u, "One model may take", [("Augury Scanner", 5)])]

    def entries(u, s, p):
        return frag_krak(u)
    pkit = ["Vratine Armour", "Bolt Pistol", "Psyk-out Grenades"]
    e, u, s, p = cadre("Sisters of Silence Excruciatus Cadre", 70, ELITES, "Questora", "Silent Judge", 20, 2, 5,
                       ("Infantry", 4, 4, 3, 3, 1, 4, 2, 9, "3+"), (5, 4, 3, 3, 2, 5, 2, 9, "3+"),
                       ["Vratine Armour", "Boltgun", "Bolt Pistol", "Psyk-out Grenades"],
                       ["Ex Oblivio", "Condemned Quarry"], groups, entries, prime_kit=pkit)
    judge = [x for x in e.iter("selectionEntry") if x.get("id") == p][0]
    add_to(judge, "selectionEntryGroups", [
        slot(p, "Replace Boltgun", "Boltgun", [("Execution Blade", 5), ("Power Weapon", 10), ("Power Stake", 10),
                                               ("Proteus Neuro-Lash", 15)]),
        take(p, "Silent Judge may take", [("Voidsheen Cloak", 10)])])
    return e


def prime_groups(p, first_slot=None, takes=None, pistol=True):
    out = []
    if first_slot:
        out.append(slot(p, *first_slot))
    if pistol:
        out.append(slot(p, "Replace Bolt Pistol", "Bolt Pistol", PRIME_PISTOLS))
    if takes:
        out.append(take(p, "Prime may take (one)", takes, max_total=1))
    return out


def add_prime(e, p, groups):
    prime = [x for x in e.iter("selectionEntry") if x.get("id") == p][0]
    add_to(prime, "selectionEntryGroups", groups)


def vigilator():
    kit = ["Vratine Armour", "Execution Blade", "Bolt Pistol", "Frag Grenades", "Psyk-out Grenades"]
    e, u, s, p = cadre("Sisters of Silence Vigilator Cadre", 75, TROOPS, "Vigilator", "Vigilator Prime", 15, 4, 9,
                       ("Infantry", 4, 4, 3, 3, 1, 4, 1, 8, "3+"), (4, 4, 3, 3, 1, 4, 2, 9, "3+"), kit, [],
                       lambda u, s, p: [],
                       lambda u, s, p: [per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                                        per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                       prime_kit=["Vratine Armour", "Frag Grenades", "Psyk-out Grenades"])
    add_prime(e, p, prime_groups(p, ("Replace Execution Blade", "Execution Blade",
                                     [("Power Stake", 5), ("Relic Blade", 10)])))
    return e


def prosecutor():
    kit = ["Vratine Armour", "Boltgun", "Bolt Pistol", "Psyk-out Grenades"]
    e, u, s, p = cadre("Sisters of Silence Prosecutor Cadre", 60, TROOPS, "Prosecutor", "Prosecutor Prime", 12, 4, 9,
                       ("Infantry", 4, 4, 3, 3, 1, 4, 1, 8, "3+"), (4, 4, 3, 3, 1, 4, 2, 9, "3+"), kit, [],
                       lambda u, s, p: [], lambda u, s, p: frag_krak(u),
                       prime_kit=["Vratine Armour", "Psyk-out Grenades"])
    add_prime(e, p, prime_groups(p, ("Replace Boltgun", "Boltgun",
                                     [("Assault Needler", 5), ("Stake Crossbow", 5), ("Execution Blade", 5),
                                      ("Power Weapon", 10), ("Power Stake", 10)])))
    return e


def witchseeker():
    kit = ["Vratine Armour", "Flamer", "Bolt Pistol", "Psyk-out Grenades"]

    def groups(u, s, p):
        g, _ = pool(u, "For every five models, one Witchseeker may replace her Flamer", u,
                    [("Toxiferran Flamer", 5), ("Compression Flamer", 10), ("Heavy Flamer", 10)], 0, every=5)
        return [g]
    e, u, s, p = cadre("Sisters of Silence Witchseeker Cadre", 70, TROOPS, "Witchseeker", "Witchseeker Prime", 14, 4,
                       9, ("Infantry", 4, 4, 3, 3, 1, 4, 1, 8, "3+"), (4, 4, 3, 3, 1, 4, 2, 9, "3+"), kit, [], groups,
                       lambda u, s, p: frag_krak(u), prime_kit=["Vratine Armour", "Psyk-out Grenades"])
    add_prime(e, p, prime_groups(p, ("Replace Flamer", "Flamer",
                                     [("Execution Blade", 5), ("Power Weapon", 10), ("Power Stake", 10)])))
    return e


def seeker():
    kit = ["Vratine Armour", "Boltgun", "Bolt Pistol", "Psyk-out Grenades", "Special Issue Ammunition"]

    def groups(u, s, p):
        return [model_swaps(u, "Any model: replace Boltgun", u, [s, p],
                            [("Assault Needler", 5), ("Stake Crossbow", 5), ("Combi-Flamer", 5), ("Combi-Snare Gun", 5),
                             ("Combi-Meltagun", 10), ("Combi-Plasma Gun", 10)]),
                take(u, "One model may take", [("Augury Scanner", 5)])]
    e, u, s, p = cadre("Sisters of Silence Seeker Cadre", 85, FA, "Seeker", "Seeker Prime", 17, 4, 9,
                       ("Infantry", 4, 4, 3, 3, 1, 4, 1, 8, "3+"), (4, 4, 3, 3, 1, 4, 2, 9, "3+"), kit,
                       ["Infiltrate", "Move Through Cover", "Marked Quarry"], groups, lambda u, s, p: frag_krak(u),
                       prime_kit=["Vratine Armour", "Boltgun", "Psyk-out Grenades", "Special Issue Ammunition"])
    add_prime(e, p, prime_groups(p, takes=[("Power Weapon", 10), ("Power Stake", 10), ("Charnabal Sabre", 5)]))
    return e


def expurgator():
    kit = ["Vratine Armour", "Bolt Pistol", "Psyk-out Grenades"]

    def entries(u, s, p):
        return frag_krak(u)

    def groups(u, s, p):
        return [required_choice(u, "Heavy weapons (entire squad)", u, [
            ("Heavy Flamers", 0, ["Heavy Flamer"]), ("Heavy Bolters", 0, ["Heavy Bolter"]),
            ("Compression Flamers", 5, ["Compression Flamer"]), ("Toxiferran Flamers", 5, ["Toxiferran Flamer"]),
            ("Snare Cannons", 5, ["Snare Cannon"]), ("Vratine Missile Launchers", 10, ["Vratine Missile Launcher"]),
            ("Adrathic Destructors", 15, ["Adrathic Destructor"])], "Heavy Flamers"),
            take(u, "One model may take", [("Augury Scanner", 5)])]
    e, u, s, p = cadre("Sisters of Silence Expurgator Cadre", 100, HS, "Expurgator", "Expurgator Prime", 20, 4, 9,
                       ("Infantry", 4, 4, 3, 3, 1, 4, 1, 8, "3+"), (4, 4, 3, 3, 1, 4, 2, 9, "3+"), kit, [], groups,
                       entries, prime_kit=["Vratine Armour", "Psyk-out Grenades"])
    add_prime(e, p, prime_groups(p, takes=[("Power Weapon", 10), ("Power Stake", 10)]))
    return e


def pursuer():
    name = "Sisters of Silence Pursuer Cadre"
    u = k("unit", name)
    pid, sid, jid = (uid("model", u, n) for n in ("Pursuer Prime", "Pursuer", "Cyber-Jackal"))
    kit = ["Vratine Armour", "Bolt Pistol", "Close Combat Weapon", "Psyk-out Grenades"]
    prime = model(u, "Pursuer Prime", 1, 1, 0, unit_profile(u, "Pursuer Prime", "Infantry (Character)", 4, 4, 3, 3, 1, 4, 2, 9,
                                                             "3+"),
                  kit=["Vratine Armour", "Psyk-out Grenades"], rules_=SISTERS,
                  groups=prime_groups(pid, ("Replace Close Combat Weapon", "Close Combat Weapon",
                                            [("Charnabal Sabre", 5), ("Power Weapon", 10), ("Power Stake", 10)])))
    purs = model(u, "Pursuer", 2, 5, 25, unit_profile(u, "Pursuer", "Infantry", 4, 4, 3, 3, 1, 4, 1, 8, "3+"), kit=kit,
                 rules_=SISTERS)
    jack = model(u, "Cyber-Jackal", 3, 6, 0, unit_profile(u, "Cyber-Jackal", "Infantry", 4, "-", 4, 4, 1, 4, 2, 5,
                                                           "5+"),
                 kit=["Claws and Fangs"], rules_=["Rage (6th-7th Edition Codexes)", "Feel No Pain", "Rending"])
    pairs = [all_of(cond(sid, u, "equalTo", n), cond(jid, u, "notEqualTo", n + 1)) for n in range(2, 6)]
    tr = transport_grp(u, SOS_TRANSPORT)
    return unit(name, 80 - 50, FA, "Fast Attack", models=[prime, purs, jack], key=u,
                rules_=["Anathema Psykana", "Fleet", "Move Through Cover"],
                mods=[modifier("add", "error", "A Pursuer Cadre has one Cyber-Jackal for every Pursuer plus one "
                                               "(added in Pursuer and Cyber-Jackal pairs).", groups=[any_of(*pairs)])],
                entries=[per_models(u, "Frag Grenades (entire cadre)", 1, u, [pid, sid], ["Frag Grenades"]),
                         per_models(u, "Krak Grenades (entire cadre)", 2, u, [pid, sid], ["Krak Grenades"])],
                groups=[model_swaps(u, "Any Pursuer: replace Bolt Pistol", u, [sid], PISTOLS), tr])


def subjugator():
    name = "Sisters of Silence Subjugator Jetbike Cadre"
    u = k("unit", name)
    pid, sid = uid("model", u, "Subjugator Prime"), uid("model", u, "Subjugator")
    kit = ["Vratine Armour", "Erinyes Pattern Jetbike", "Bolt Pistol", "Close Combat Weapon", "Psyk-out Grenades"]
    prime = model(u, "Subjugator Prime", 1, 1, 0,
                  unit_profile(u, "Subjugator Prime", "Jetbike (Character)", 4, 4, 3, "3(4)", 1, 4, 2, 9, "3+"),
                  kit=["Vratine Armour", "Erinyes Pattern Jetbike", "Psyk-out Grenades"],
                  groups=prime_groups(pid, ("Replace Close Combat Weapon", "Close Combat Weapon",
                                            [("Charnabal Sabre", 5), ("Power Weapon", 10), ("Power Stake", 10),
                                             ("Power Fist", 15)])))
    subs = model(u, "Subjugator", 2, 9, 45, unit_profile(u, "Subjugator", "Jetbike", 4, 4, 3, "3(4)", 1, 4, 1, 8,
                                                          "3+"), kit=kit)
    return unit(name, 135 - 90, FA, "Fast Attack", models=[prime, subs], key=u,
                rules_=SISTERS + ["Deep Strike", "Outflank"], entries=frag_krak(u),
                groups=[required_choice(u, "Erinyes Pattern Jetbike weapons (entire unit)", u, [
                    ("Snare Cannons", 0, ["Snare Cannon"]), ("Needle Cannons", 5, ["Needle Cannon"]),
                    ("Adrathic Destructors", 10, ["Adrathic Destructor"])], "Snare Cannons")])


def rhino():
    n = "Anathema Psykana Rhino"
    t = RHINO
    return entry(t, n, typ="unit", cost=50,
                 cats=[category_link(gs.CAT_TRANSPORT, "Dedicated Transport", primary=True, key=t)],
                 profiles=[vehicle_profile(t, n, "Vehicle (Tank, Transport)", 4, 11, 11, 10),
                           transport_profile(t, n, "10 models", "One on each side, one at the rear", "-")],
                 links=[gear(t, "Storm Bolter"), gear(t, "Smoke Launchers")],
                 groups=[take(t, "Vehicle Upgrades", [("Dozer Blade", 5), ("Extra Armour", 5),
                                                      ("Hunter-Killer Missile", 15), ("Searchlight", 1),
                                                      ("Pintle-mounted Storm Bolter", 10)])])


def kharon():
    n = "Kharon Pattern Acquisitor"
    t = KHARON
    return entry(t, n, typ="unit", cost=125,
                 cats=[category_link(gs.CAT_TRANSPORT, "Dedicated Transport", primary=True, key=t)],
                 profiles=[vehicle_profile(t, n, "Vehicle (Tank, Skimmer, Fast, Transport)", 4, 12, 11, 10),
                           transport_profile(t, n, "12 models", "One access point at the front", "-")],
                 infolinks=rules_links(["Assault Vehicle", "Deep Strike", "Battle Auspex", "Capture-Grid"], key=t),
                 links=[gear_n(t, "Twin-linked Vratine Missile Launcher", 2)] +
                       [gear(t, x) for x in ["Spectra-Distort Field", "Searchlight", "Smoke Launchers"]],
                 groups=[slot(t, "Replace Hellion Pattern Heavy Cannon Array", "Hellion Pattern Heavy Cannon Array",
                              [("Twin-linked Multi-Melta", 0)]),
                         take(t, "Vehicle Upgrades", [("Extra Armour", 5), ("Armoured Ceramite", 20)])])


# =============================================================== Assassins
ASSASSIN_RULES = ["Assassin Operative", "Fearless", "Infiltrate", "Dodge"]
TEMPLES = [  # name, extra cost, wargear, rules
    ("Vindicare", 60, ["Exitus Rifle", "Exitus Pistol", "Spy Mask", "Stealth Suit"], ["Marksman"]),
    ("Callidus", 70, ["C'tan Phase Sword", "Neural Shredder", "Polymorphine", "Poison Blades"],
     ["Jump Back", "A Word in Your Ear..."]),
    ("Eversor", 45, ["Executioner Pistol", "Power Weapon", "Neuro-Gauntlet", "Melta Bombs", "Combat Drugs"],
     ["Fast Shot", "Bio-Meltdown"]),
    ("Culexus", 55, ["Etherium", "Animus Speculum", "Psyk-out Grenades"],
     ["Psychic Abomination", "Soulless", "Psyker Assassin", "Life Drain"]),
    ("Adamus", 75, ["Needlespine Blaster", "Nemesii Blade", "Nemesii Grenades"], ["Death's Artisan"]),
    ("Venenum", 75, ["Toxin Ejector", "Poison Globes", "Hookfang"], ["Unnatural Conditioning"]),
    ("Vanus", 55, ["Paired Laspistols", "Sympatic Dataspikes"], ["Autonomic Servo-Limbs", "Infocyte"]),
]
CAT_OPERATIVE = k("cat", "Execution Force Operative")


def assassin_profile(key, name):
    return unit_profile(key, name, "Infantry (Character)", 5, 5, 4, 4, 2, 5, 3, 10, "4+")


def imperial_assassin():
    name = "0-1 Imperial Assassin"
    u = k("unit", name)
    mid = uid("model", u, "Imperial Assassin")
    gid = uid("grp", u, "temple")
    ents = []
    for t, extra, kit, rls in TEMPLES:
        eid = uid(gid, t)
        ents.append(entry(eid, f"{t} Temple", cost=extra, constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                          links=[gear(eid, x) for x in kit], infolinks=rules_links(rls, key=eid)))
    temple = group(gid, "Temple", entries=ents, constraints=[constraint(uid(gid, "min"), "min", 1, auto=True),
                                                             constraint(uid(gid, "max"), "max", 1, auto=True)])
    m = model(u, "Imperial Assassin", 1, 1, 0, assassin_profile(u, "Imperial Assassin"), groups=[temple])
    return unit(name, 50, ELITES, "Elites", models=[m], key=u, constraints=[unique(u)],
                rules_=ASSASSIN_RULES + ["Temple", "One Assassin", "Assassinorum Agent", "Modified Rending"])


def operatives():
    out = []
    names = {"Vanus": "Vanus Infocyte Assassin"}
    for t, extra, kit, rls in TEMPLES:
        n = names.get(t, f"{t} Assassin")
        name = f"Officio Assassinorum {n}"
        u = k("unit", name)
        m = model(u, n, 1, 1, 0, assassin_profile(u, n), kit=kit)
        e = entry(u, name, typ="unit", cost=50 + extra,
                  cats=[category_link(CAT_OPERATIVE, "Execution Force Operative", primary=True, key=u)],
                  constraints=[unique(u, 1, "force")],
                  infolinks=rules_links(ASSASSIN_RULES + rls + ["Modified Rending", "Execution Force"], key=u),
                  entries=[m])
        out.append(e)
    return out


def execution_force_entry():
    fid = k("force", "Execution Force")

    def cl(cat_id, name, mn=None, mx=None):
        c = category_link(cat_id, name, key=fid)
        cons = []
        if mn is not None:
            cons.append(constraint(uid(fid, name, "min"), "min", mn))
        if mx is not None:
            cons.append(constraint(uid(fid, name, "max"), "max", mx))
        if cons:
            c.append(wrap("constraints", cons))
        return c
    return el("forceEntry", {"id": fid, "name": "Officio Assassinorum Execution Force", "hidden": "false"},
              [wrap("categoryLinks", [cl(CAT_OPERATIVE, "Execution Force Operative", 7, 7)])])


# ================================================================== build
def build():
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS, multi_profile=MULTI, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    units = [
        army_config(),
        # HQ
        talon_master(), shield_captain(), valdor(),
        knight("Sisters of Silence Knight-Abyssal", "Knight-Abyssal", 100, (6, 5, 3, 3, 4, 6, 4, 10, "3+"),
               ["Ex Oblivio", "Independent Character", "Mistress of the Silent Sisterhood"], KNIGHT_ABYSSAL),
        knight("Sisters of Silence Oblivion Knight-Centura", "Oblivion Knight-Centura", 60,
               (5, 4, 3, 3, 3, 5, 3, 9, "3+"), ["Ex Oblivio", "Independent Character"], KNIGHT_CENTURA),
        vigil_command(), krole(),
        # Troops
        custodian_guard(), sentinel_guard(), vigilator(), prosecutor(), witchseeker(),
        # Elites
        hetaeron(), aquilon(), achillus(), galatus(), firebrand(), raptor_guard(), excruciatus(),
        imperial_assassin(),
        # Fast Attack
        agamatus(), pallas(), venatari(), pursuer(), subjugator(), seeker(),
        # Heavy Support
        sagittarum(), telemon(), caladius(), expurgator(),
        # Execution Force
        *operatives(),
    ]
    shared = [coronus(), rhino(), kharon(), shadow_tt_entry(), vigil_command(retinue=True)]
    root = catalogue(ARMY, units, shared, force_entries=[execution_force_entry()])
    # the catalogue's own categories (Execution Force)
    cats = wrap("categoryEntries", [el("categoryEntry", {"id": CAT_OPERATIVE, "name": "Execution Force Operative",
                                                         "hidden": "false"})])
    root.insert(1, cats)
    # Custodes carry several Iron Halos: drop the Legiones Astartes 'one Iron Halo per army' limit
    for e in root.iter("selectionEntry"):
        if e.get("name") == "Iron Halo":
            c = e.find("constraints")
            if c is not None:
                e.remove(c)
    return root
