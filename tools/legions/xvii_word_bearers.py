"""XVII Legion - Word Bearers (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, allegiance_only, option, upgrade, retinue_links, command_squad_for,
                            named_character, primarch, primarch_retinue, required_choice, add_consul,
                            add_armoury_items, add_group, add_entry, LOW, TRAITOR, LOYALIST)
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile, has_tda, TDA
from legiones2 import (slot, take, pool, transports, add_mods, add_to, foc, rite_id, rite, walker_profile, TROOPS,
                       ELITES, FA, HQ, HS, model_swaps, specials_decrement, T)
from legiones_wargear import ARMY_RULES, WEAPONS, WEAPON_RULES

LEGION = "XVII - Word Bearers"
LR = "Legiones Astartes (Word Bearers)"

RULES = {
    LR: ("Models with this rule belong to the XVII Legion and use the Word Bearers Legion special rules: Fanatical "
         "Devotion, The Dark Shepherds, Ritual of Consecration and Daemonic Covenant."),
    "Fanatical Devotion": ("Non-Daemon units with the Legiones Astartes (Word Bearers) special rule may re-roll failed "
                           "Morale and Pinning tests."),
    "The Dark Shepherds": (
        "A Word Bearers Detachment must include at least one Legion Chaplain Consul or Legion-specific Dark Apostle as an "
        "HQ selection. A character specifically stated to count as a Dark Apostle also fulfils this requirement: any model "
        "with an Accursed Crozius (Praetor, Centurion, Diabolist or Chaplain) and every Word Bearers named character "
        "(Argel Tal, Erebus, Kor Phaeron, Zardu Layak, Hol Beloth, Lorgar)."),
    "Ritual of Consecration": (
        "TRAITOR ONLY (no effect in a Loyalist Word Bearers army). When a non-Daemon Word Bearers unit completely destroys "
        "an enemy unit during the Assault phase, it may forgo its Consolidation move. If it does so, nominate one friendly "
        "Daemonic Covenant unit currently in Reserve: that unit may re-roll its next Reserve roll. Only one Covenant unit "
        "may receive this benefit each turn."),
    "Daemonic Covenant": (
        "A Traitor Word Bearers army may include a Daemons of the Ruinstorm Covenant Detachment, selected from the Daemons "
        "of the Ruinstorm Army List. COVENANT DETACHMENT: HQ 0-1, Troops 1-3, Elites 0-1, Fast Attack 0-1, Heavy Support "
        "0-1; an HQ is not compulsory but at least one Troops choice must be selected. It may cost no more than 25% of "
        "the army's total points limit and has no minimum points requirement. Units use their normal profiles, options, "
        "Dominions and special rules from the Daemons of the Ruinstorm Army List. The Covenant Detachment counts as the "
        "army's Allied Detachment and needs no additional permission; the army may not include another Allied Detachment "
        "unless a rule specifically states otherwise. Covenant units may not fulfil compulsory selections in the primary "
        "Word Bearers Detachment and may not provide the Warlord. Word Bearers and Covenant units are Fellow Warriors; "
        "Independent Characters from one Detachment may not join units from the other.\n"
        "DAEMONIC SUMMONING: all Covenant units must begin the battle in Reserve; they may not deploy normally, Infiltrate "
        "or Outflank. When a Covenant unit becomes available from Reserve, nominate one friendly Summoning Point already on "
        "the battlefield (Personal Icons, Icons of Chaos Undivided, Accursed Crozii and any rule stated to act as a "
        "Summoning Point). Place the centre model within 6\" of the Summoning Point and more than 2\" from any enemy model; "
        "the unit then enters play using the normal Deep Strike rules (Mishaps resolved normally, all normal Deep Strike "
        "restrictions apply). If no eligible Summoning Point or legal position is available, the unit stays in Reserve and "
        "must roll again in a later turn. A Summoning Point may be used while its bearer is in close combat, is not "
        "consumed and may summon several units during the battle.\n"
        "DAEMONOLOGY: Daemonic Covenant is separate from Daemonology (Malefic). Units created by Conjuration psychic powers "
        "are not Covenant units and do not use these rules.\n"
        "(The Covenant Detachment is a separate Detachment from the Daemons of the Ruinstorm army list and cannot yet be "
        "added as a Covenant Detachment in this data set.)"),
    # Armoury
    "Accursed Crozius": (
        "Any Word Bearers Praetor or Centurion (including a Diabolist) may purchase an Accursed Crozius for +40 points. "
        "It replaces the model's close combat weapon and does not count towards the Space Marine Armoury points limit. "
        "A Chaplain may replace his Crozius and Rosarius with an Accursed Crozius for free. The bearer receives a 4+ Invulnerable Save and counts as possessing a Personal Icon for the purposes of summoning "
        "Daemons (Summoning Point). A model with an Accursed Crozius counts as a Dark Apostle for The Dark Shepherds. A "
        "model may never possess more than one Accursed Crozius."),
    "Tainted Strike": (
        "Any unsaved wound inflicted by a Tainted Weapon becomes a Massive Wound and inflicts D3 Wounds instead of 1. A "
        "Tainted Weapon is not a Power Weapon and does not ignore Armour Saves. (Any Word Bearers Character eligible to "
        "select a Power Weapon may instead select a Tainted Weapon for the same points cost.)"),
    "Burning Lore": (
        "Any Word Bearers Praetor, Centurion, Chaplain or Diabolist which is not already a Psyker may purchase Burning Lore "
        "for +30 points. The model becomes a Psyker with Mastery Level 1 and selects one psychic power from either the "
        "Biomancy or Telepathy discipline. It follows all normal ProHammer rules for Psykers."),
    "Hex-Bolts": (
        "Any Word Bearers Infantry unit equipped with Bolt weapons (including a Praetor or Centurion; not Covenant Zealot "
        "Mobs) may purchase Hex-Bolts for +5 points per unit. Bolt "
        "Pistols, Bolters, Combi-Bolters, Storm Bolters and the Bolter component of Combi-Weapons carried by models in the "
        "unit gain the Soul Blaze special rule. Hex-Bolts may not be combined with Special Issue Ammunition or another "
        "ammunition upgrade."),
    "Icon of Chaos Undivided": (
        "One model in a Legion Command Squad, Legion Veteran Squad or Legion Terminator Squad may carry an Icon of Chaos "
        "Undivided for +30 points. The Icon counts as a Summoning Point for the Daemonic Covenant. Friendly non-Daemon "
        "Word Bearers units with at least one model within 6\" of the bearer gain the Fearless special rule."),
    "Favour of the Pantheon": (
        "One non-named Word Bearers Independent Character in the army (Praetor, Centurion, Techmarine, ...) may purchase one "
        "Favour of the Pantheon. A model may "
        "never possess more than one Favour. Daemonic Aura (15): 5+ Invulnerable Save. Daemonic Mutation (15): +1 Attack. "
        "Daemonic Strength (10): +1 Strength. Daemonic Wings (20): the model becomes Jump Infantry; may not be combined "
        "with a Jump Pack, Bike, Jetbike or Terminator Armour. Daemonic Visage (5): an enemy unit which loses a close "
        "combat involving the bearer suffers an additional -1 Leadership on the resulting Morale test. The effects are "
        "already included in the model's characteristics or special rules and may not be purchased more than once."),
    "Diabolist": (
        "TRAITOR ONLY. A Word Bearers Centurion may be upgraded to a Diabolist Consul for +35 points. The Diabolist gains the Daemon and "
        "Preferred Enemy (Loyalists) special rules. He may not select a Bike, Jetbike, any form of Terminator Armour, Power "
        "Fist or Thunder Hammer. The presence of at least one Diabolist allows eligible units in the Detachment to purchase "
        "Dark Channelling. A Diabolist remains a Centurion for the purposes of purchasing an Accursed Crozius, and a "
        "Diabolist with an Accursed Crozius counts as a Dark Apostle for The Dark Shepherds."),
    "Preferred Enemy (Loyalists)": "This model has the Preferred Enemy special rule against models of the Loyalist faction.",
    "Dark Channelling": (
        "If the Detachment includes at least one Diabolist, a Legion Tactical Squad, Legion Veteran Squad, Legion Breacher "
        "Siege Squad, Legion Terminator Squad or Legion Assault Squad may purchase Dark Channelling for +25 points per "
        "squad. After both armies have deployed but before the first turn begins, roll a D6 for each such unit: 1-3 Zealot "
        "- the unit gains Zealot for the battle; 4-5 Unholy Strength - models gain +1 Strength for the battle; 6 Daemon - "
        "the unit gains the Daemon special rule for the battle, may no longer count as a Scoring Unit and, in a mission "
        "using Victory Points, counts as destroyed at the end of the battle even if it survives. Only the models of the "
        "upgraded squad are affected (not Independent Characters or other models joining it later). (Zardu Layak: add +1 "
        "to the roll, to a maximum of 6.)"),
    # Rites of War
    "The Dark Brethren": (
        "TRAITOR ONLY.\nEFFECTS - Arch-Traitors: all Word Bearers Independent Characters in the Detachment gain Preferred "
        "Enemy against models belonging to the Loyalist faction. Signs and Portents: after deployment but before the first "
        "turn, select one Word Bearers Troops unit and roll a D6: 1-3 all enemy units gain Preferred Enemy against it for "
        "the battle; 4-6 it gains Preferred Enemy against all enemy units for the battle. From Beyond: the Detachment may "
        "include an Allied Detachment from Daemons of the Ruinstorm, treated as Sworn Brothers with the Word Bearers; this "
        "does not prevent the normal Daemonic Covenant. If the army includes a Daemons of the Ruinstorm Covenant "
        "Detachment: it may use the normal Daemons of the Ruinstorm Allied Detachment Force Organisation Chart instead of "
        "the restricted Covenant chart; the 25% limit is removed and the normal Allied Detachment points restrictions "
        "apply; Word Bearers and the Daemons of the Ruinstorm are Sworn Brothers; before deployment each Daemon unit is "
        "designated Manifested (deploys and enters play normally) or Summoned (begins in Reserve and uses Daemonic "
        "Summoning); the army may still include only one Daemons of the Ruinstorm Allied Detachment. Hell Follows With "
        "Them: whenever an enemy Psyker suffers a Wound from Perils of the Warp, it becomes a Massive Wound and inflicts D3 "
        "Wounds instead of 1.\n"
        "LIMITATIONS - Only a Traitor Word Bearers Detachment. The Detachment must include at least one Diabolist. No more "
        "than one Heavy Support choice. The army may not include a Fortification or an Allied Detachment drawn from "
        "another Space Marine Legion. Any Allied Detachment other than Daemons of the Ruinstorm is treated as Desperate "
        "Allies."),
    "Last of the Serrated Sun": (
        "TRAITOR ONLY.\nEFFECTS - Company of Monsters: Gal Vorbak Dark Brethren may be selected as Troops choices and may "
        "fulfil compulsory Troops selections; every Gal Vorbak unit in the Detachment must purchase a Legion Drop Pod or "
        "Dreadclaw Drop Pod as a Dedicated Transport; if their unit size is more than 5 models they may purchase "
        "Teleportation Transponders for +25 points per unit. Drop Elite: any Word Bearers Infantry unit which may normally "
        "purchase a Rhino as a Dedicated Transport may instead purchase a Legion Drop Pod at its normal points cost. "
        "Burning Sun: whenever a Legion Drop Pod or Dreadclaw Drop Pod of this Detachment arrives by Deep Strike, every "
        "enemy unit with at least one model within 12\" of its final position must take a Pinning test (one test per "
        "arriving Drop Pod).\n"
        "LIMITATIONS - Only a Traitor Word Bearers Detachment. All Infantry units must begin the battle in Reserve and "
        "enter play using a Deep Striking Drop Pod, Teleportation Transponders or embarked aboard a Transport with the "
        "Flyer type. The army may not include Immobile units. The army may not include a Fortification or an Allied "
        "Detachment."),
    "Selected as Troops (Last of the Serrated Sun)": (
        "Under Last of the Serrated Sun this Gal Vorbak unit is a Troops choice, may fulfil compulsory Troops selections "
        "and must purchase a Legion Drop Pod or Dreadclaw Drop Pod as a Dedicated Transport."),
    # Units
    "Driven to Slaughter": (
        "While the Legion Overseer is alive, the Covenant Zealot Mob is Fearless and ignores all Leadership penalties. If "
        "the unit is able to declare a charge against an enemy unit during the Assault phase, it must do so (the "
        "controlling player chooses the target if several are possible). During an Assault phase in which the unit "
        "charges, all Covenant Zealots (not the Overseer) gain +1 Attack and +1 Initiative. If the Legion Overseer is "
        "slain, the unit immediately loses Fearless and Driven to Slaughter for the rest of the battle; if not locked in "
        "close combat it immediately becomes Pinned, otherwise it becomes Pinned as soon as that combat ends (if still on "
        "the battlefield). Once it recovers from being Pinned it functions normally and uses its own Leadership."),
    "Expendable": ("Casualties suffered by a Covenant Zealot Mob, or the destruction of the unit, never cause friendly "
                   "units to take Morale, Leadership or Pinning tests."),
    "Rending (Gal Vorbak)": "The Rending special rule applies only to the Gal Vorbak's close-combat attacks.",
    "Axe-rake": (
        "An Axe-rake is a close-combat weapon. Attacks made with it are resolved at +1 Strength. If an enemy unit Retreats "
        "from a close combat involving one or more models armed with Axe-rakes, reduce its Retreat distance by 1\" (to a "
        "minimum of 1\")."),
    "Bitter Duty": "Only an Independent Character specifically permitted to join Bitter Duty units may join an Ashen "
                   "Circle Squad.",
    "Selected as Troops (Reign of Fire)": (
        "Zardu Layak's Reign of Fire: if Zardu Layak is the army's Warlord, Ashen Circle Squads may be selected as Troops "
        "choices and may fulfil compulsory Troops selections. Tick this only if Zardu Layak is the Warlord."),
    "Daemonic Engine": ("Each time the Mhara Gal suffers a Glancing or Penetrating Hit, roll a D6 before rolling on the "
                        "Vehicle Damage table. On a 5+ the hit is ignored."),
    "Shroud of Dark Fire": ("When resolving a shooting attack against the Mhara Gal made with a Flame, Melta, Plasma or "
                            "Volkite weapon, reduce the Strength of the attack by 1 (to a minimum of 1)."),
    "Accursed": ("Successful Invulnerable Saves made against the Mhara Gal's close-combat attacks must be re-rolled. Enemy "
                 "units taking a Fear test caused by the Mhara Gal suffer a -2 Leadership modifier. The Mhara Gal never "
                 "counts as a Scoring Unit."),
    "Paired Close-Combat Arms (Mhara Gal)": "If equipped with two Dreadnought Close Combat Weapons, the Mhara Gal gains "
                                            "+1 Attack (already shown in its profile).",
    "Flesh Harvesters": ("When a Procurator Squad uses Ritual of Consecration, the Daemon unit nominated by that rule "
                         "receives +1 to its next Reserve roll in addition to the normal re-roll. This modifier is not "
                         "cumulative."),
    "Procurator Prime": "The Procurator Prime counts as an Apothecary for the purposes of his Narthecium and Reductor.",
    "Procurator Jump Packs": ("If every model purchases a Jump Pack, the unit becomes Jump Infantry and may not select a "
                              "Dedicated Transport."),
    "Daemonkin": ("After deployment but before the first turn begins, roll a D6 for each Possessed Marine Squad; the entire "
                  "squad gains the corresponding rule for the battle: 1 Scout; 2 Furious Charge; 3 Fleet; 4 Rending in "
                  "close combat; 5 Feel No Pain (5+); 6 Counter-Attack."),
    # Characters
    "Custodian Spear": ("A Two-Handed, Master-crafted Power Weapon with an inbuilt Foeblaster Boltgun. During the first "
                        "round of each close combat, attacks made with the Custodian Spear are resolved at +1 Strength and "
                        "+1 Initiative."),
    "Lord of the Gal Vorbak": ("Argel Tal may select one Gal Vorbak Dark Brethren Squad as his personal retinue. The squad "
                               "does not occupy a separate Elites selection; Argel Tal and the Gal Vorbak count as a single "
                               "HQ selection."),
    "Master-crafted Accursed Crozius": ("Erebus' Accursed Crozius follows the normal rules from the Word Bearers Armoury "
                                        "and is additionally Master-crafted."),
    "Anathame Dagger": (
        "During an Assault phase, Erebus may exchange one of his normal Attacks for one attack with the Anathame Dagger. "
        "Invulnerable Saves may not be taken against this attack. If it inflicts an unsaved Wound upon a non-Vehicle "
        "model, it inflicts a Massive Wound (D3) instead of one Wound. Against Vehicles it has no additional effect."),
    "High Chaplain": ("Erebus counts as both a Legion Chaplain Consul and a Diabolist for all Word Bearers rules, army "
                      "construction requirements and Rites of War. His presence therefore fulfils The Dark Shepherds and "
                      "allows eligible units to purchase Dark Channelling."),
    "Burning Lore (Named Character)": ("This character has Burning Lore at no additional points cost (Psyker, Mastery "
                                       "Level 1, one power from Biomancy or Telepathy) and follows the normal rules "
                                       "presented in the Word Bearers Armoury."),
    "Command Retinue (Word Bearers)": ("This character may select one Legion Command Squad (Kor Phaeron: one Legion "
                                       "Terminator Command Squad) as his retinue. The squad does not occupy a separate "
                                       "Force Organisation slot."),
    "Terminus Consolaris": ("Counts as Cataphractii Terminator Armour. Its life-support systems grant Kor Phaeron Feel No "
                            "Pain (6+). These rules are already reflected in his profile and special rules."),
    "Black Cardinal": ("Kor Phaeron counts as both a Dark Apostle and a Diabolist for all Word Bearers rules, army "
                       "construction requirements and Rites of War. His presence therefore fulfils The Dark Shepherds and "
                       "allows eligible units to purchase Dark Channelling."),
    "Jealous Command": "If Kor Phaeron is included in the army, he must be the army's Warlord unless Lorgar is also included.",
    "Psychic Powers (Zardu Layak)": ("Zardu Layak selects two powers from Malefic Daemonology and follows all normal "
                                     "ProHammer rules for a Mastery Level 2 Psyker."),
    "Crimson Apostle": ("Zardu Layak counts as both a Dark Apostle and a Diabolist for all Word Bearers rules, army "
                        "construction requirements and Rites of War."),
    "Dark Channeler": ("When rolling on the Dark Channelling table for a unit in an army containing Zardu Layak, add +1 to "
                       "the result, to a maximum of 6."),
    "Reign of Fire": ("If Zardu Layak is the army's Warlord, Ashen Circle Squads may be selected as Troops choices. They "
                      "may fulfil compulsory Troops selections."),
    "Anakatis Kul": ("Zardu Layak may be accompanied by the Anakatis Kul Blade-Slaves (2 models) for +100 points. Zardu "
                     "Layak and the Blade-Slaves count as a single HQ selection."),
    "Mindless Killers": (
        "The Anakatis Kul may only be selected as part of Zardu Layak's unit. While Zardu Layak is alive, they must remain "
        "part of his unit. If Zardu Layak is slain, the surviving Blade-Slaves must declare a charge against the nearest "
        "eligible enemy unit during each Assault phase if able. Whenever they win a close combat and an enemy unit "
        "Retreats, they must Pursue if legally able to do so."),
    "Tainted Weapon (Hol Beloth)": "Hol Beloth's Tainted Weapon follows the normal rules presented in the Word Bearers "
                                   "Armoury.",
    "Hexaglyphic Ward": ("The first unsaved Wound suffered by Hol Beloth during the battle is ignored. If that attack would "
                         "inflict a Massive Wound, the Ward is used before rolling the D3 Wounds. After preventing one "
                         "Wound, the Ward has no further effect."),
    "Exhortation of Battle": (
        "Once per battle, at the beginning of a Word Bearers Assault phase, Hol Beloth may declare an Exhortation of "
        "Battle. Until the end of that Assault phase, Word Bearers models with a Weapon Skill lower than 5 count as having "
        "Weapon Skill 5. Models which already have Weapon Skill 5 or higher are unaffected."),
    # Lorgar
    "Armour of the Word": ("Counts as Primarch Armour. Enemy Psykers suffer -1 Leadership when taking a Psychic Test to "
                           "invoke a psychic power which directly targets Lorgar or a unit he has joined."),
    "Illuminarum": ("A Master-crafted Power Weapon. Attacks made with Illuminarum are resolved at +2 Strength and have the "
                    "Concussive special rule. Lorgar may also use Illuminarum to make a Smash attack using the normal "
                    "ProHammer rules."),
    "Voice of the Urizen": ("Friendly Word Bearers units with at least one model within 12\" of Lorgar may re-roll failed "
                            "Morale and Pinning tests. The second result must be accepted."),
    "Fanatical Devotion (Lorgar)": ("A friendly Word Bearers unit joined by Lorgar has the Hatred (Infantry) special rule "
                                    "while he remains part of that unit."),
    "Dark Oratory": (
        "At the beginning of each Word Bearers turn, nominate one friendly Word Bearers unit with at least one model within "
        "12\" of Lorgar. Until the beginning of the next Word Bearers turn, that unit may re-roll close combat To Hit rolls "
        "of 1. Only one unit may benefit from Dark Oratory at a time."),
    "Lorgar Transfigured": (
        "TRAITOR ONLY (+75 points). Lorgar Transfigured gains Psyker (Mastery Level 3), Psychic Ascendancy, and Illuminarum "
        "becomes a Force Weapon. PSYKER - MASTERY LEVEL 3: selects three psychic powers before the battle, each from "
        "either Divination or Telekinesis (any combination); otherwise follows all normal ProHammer rules for a Mastery "
        "Level 3 Psyker."),
    "Psychic Ascendancy": ("Lorgar Transfigured may ignore the first -1 Leadership penalty he would suffer from "
                           "Disturbance in the Warp during each player turn. Further Disturbance in the Warp penalties "
                           "apply normally."),
    "Illuminarum (Transfigured)": (
        "When wielded by Lorgar Transfigured, Illuminarum additionally counts as a Force Weapon. It retains its "
        "Master-crafted, +2 Strength, Concussive and Smash rules. After Lorgar inflicts one or more unsaved Wounds with "
        "Illuminarum, he may attempt to activate it using the normal ProHammer rules for Force Weapons."),
    "Primarch Retinue (Lorgar)": (
        "Lorgar may select a Legion Honour Guard Squad, a Legion Terminator Command Squad or Gal Vorbak Dark Brethren as "
        "his Primarch Retinue. It does not occupy an additional Force Organisation selection and otherwise follows the "
        "normal Primarch Retinue rules. Gal Vorbak Dark Brethren may only be selected as Lorgar's Primarch Retinue in a "
        "Traitor army."),
}

WEAPONS_ = {
    "Accursed Crozius": ("-", "User", "-", "Power Weapon; 4+ Invulnerable Save; Summoning Point (Personal Icon)"),
    "Master-crafted Accursed Crozius": ("-", "User", "-", "Power Weapon, Master-crafted; 4+ Invulnerable Save; "
                                                         "Summoning Point (Personal Icon)"),
    "Tainted Weapon": ("-", "User", "-", "Specialist Weapon, Tainted Strike"),
    "Axe-rake": ("-", "User +1", "-", "Axe-rake"),
    "Autopistol": ('12"', "3", "-", "Pistol"),
    "Custodian Spear": ("-", "User (+1 first round)", "-", "Power Weapon, Two-Handed, Master-crafted; +1 Strength and "
                                                           "+1 Initiative in the first round of each close combat"),
    "Anathame Dagger": ("-", "User", "-", "One Attack in place of a normal Attack; no Invulnerable Saves; Massive Wound "
                                          "(D3) against non-Vehicle models"),
    "Master-crafted Force Weapon": ("-", "User", "-", "Power Weapon, Force, Master-crafted"),
    "Master-crafted Power Fist": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Master-crafted"),
    "Pair of Rending Weapons": ("-", "User", "-", "Rending, pair (+1 Attack)"),
    "Illuminarum": ("-", "User +2", "-", "Power Weapon, Master-crafted, Concussive, Smash"),
}
WEAPON_RULES_ = {
    "Accursed Crozius": ["Accursed Crozius"],
    "Master-crafted Accursed Crozius": ["Accursed Crozius", "Master-crafted Accursed Crozius", "Master-Crafted"],
    "Tainted Weapon": ["Tainted Strike"],
    "Axe-rake": ["Axe-rake"],
    "Custodian Spear": ["Custodian Spear", "Two-Handed", "Master-Crafted"],
    "Anathame Dagger": ["Anathame Dagger"],
    "Master-crafted Force Weapon": ["Force", "Master-Crafted"],
    "Master-crafted Power Fist": ["Unwieldy", "Master-Crafted"],
    "Pair of Rending Weapons": ["Rending"],
    "Illuminarum": ["Illuminarum", "Master-Crafted", "Concussive", "Smash"],
}
WARGEAR_ = {
    "Flak Armour": "Flak armour confers a 6+ Armour Save.",
    "Icon of Chaos Undivided": RULES["Icon of Chaos Undivided"],
    "Hex-Bolts": RULES["Hex-Bolts"],
    "Iron Halo (Named Character)": ("Grants a 4+ Invulnerable Save. Part of this named character's own wargear; not "
                                    "counted towards the army's normal limit of one Iron Halo."),
    "Terminus Consolaris": (RULES["Terminus Consolaris"], ["Feel No Pain"]),
    "Armour of the Word": (RULES["Armour of the Word"], ["Primarch Armour"]),
    "Jump Pack (Daemonic Wings)": ("Argel Tal's daemonic wings count as a Jump Pack: the model is Jump Infantry.", []),
}

DISCIPLINES = ["Biomancy", "Telepathy"]


def register():
    ARMY_RULES.update(RULES)
    register_data(weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_)
    # the Custodian Spear has an inbuilt Foeblaster Boltgun
    WEAPONS["Custodian Spear"] = ["Custodian Spear", "Foeblaster Boltgun"]


# ------------------------------------------------------------------ local helpers
def _unit_type(e):
    for p in e.findall("profiles/profile"):
        for c in p.iter("characteristic"):
            if c.get("name") == "Unit Type":
                return c.text or ""
    return None


def is_character(e):
    t = _unit_type(e)
    return bool(t) and "Character" in t


def find_group(e, name):
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == name:
            return g
    return None


def entries_named(ctx, names):
    seen, out = set(), []
    for e in ctx.all_entries():
        if e.get("name") in names and id(e) not in seen:
            seen.add(id(e))
            out.append(e)
    return out


def hide_mods(eid, groups_):
    """Hide an entry and set its max to 0 while the condition group is true (groups_: factory returning groups)."""
    return [modifier("set", "hidden", "true", groups=groups_()),
            modifier("set", uid(eid, "max"), 0, groups=groups_())]


def prof_mods(prof, mods):
    m = prof.find("modifiers")
    if m is None:
        prof.insert(0, wrap("modifiers", list(mods)))
    else:
        for x in mods:
            m.append(x)


def model(u, name, cost, mn, mx, utype, stats, kit, groups=(), mods=(), rules_=(), auto=False):
    mid = uid("model", u, name)
    return mid, entry(mid, name, typ="model", cost=cost, mods=list(mods),
                      constraints=[constraint(uid(mid, "min"), "min", mn, auto=auto),
                                   constraint(uid(mid, "max"), "max", mx, auto=auto)],
                      profiles=[unit_profile(u, name, utype, *stats)], links=[gear(mid, k) for k in kit],
                      groups=list(groups), infolinks=rules_links(list(rules_), key=mid))


def unit_type_mod(new_type, conds):
    return modifier("set", gs.char_id("Unit", "Unit Type"), new_type, conds=conds)


def troops_mods(conds_fn):
    return [modifier("set-primary", "category", TROOPS, conds=conds_fn()),
            modifier("add", "category", gs.CAT_LINE, conds=conds_fn())]


def character_variant(roots, base, new, skip_names=()):
    """'Any Character eligible to select <base> may instead select <new> for the same points cost'."""
    base_id = W(base)
    done = set()
    n = 0
    for r in roots:
        for e in r.iter("selectionEntry"):
            if not is_character(e) or e.get("name") in skip_names:
                continue
            for g in e.iter("selectionEntryGroup"):
                if id(g) in done:
                    continue
                done.add(id(g))
                links = g.find("entryLinks")
                if links is None or any(lk.get("targetId") == W(new) for lk in links):
                    continue
                for lk in list(links):
                    if lk.get("targetId") != base_id:
                        continue
                    cs = lk.find("costs")
                    cost = float(cs[0].get("value")) if cs is not None and len(cs) else 0
                    nid = uid(lk.get("id"), "variant", new)
                    cons = []
                    if any(c.get("type") == "max" for c in lk.iter("constraint")):
                        cons = [constraint(uid(nid, "max"), "max", 1, auto=True)]
                    new_l = link(nid, W(new), new, cost=int(cost) or None, constraints=cons)
                    if g.get("defaultSelectionEntryId") is not None:
                        new_l.set("sortIndex", str(int(lk.get("sortIndex") or 1) + 100))
                    links.append(new_l)
                    n += 1
    return n


def krak(key, melta=True):
    items = [("Krak Grenades", 2)] + ([("Melta Bombs", 5)] if melta else [])
    return take(key, "Wargear", items)


def burning_lore_powers(key, owner):
    """Burning Lore: one power picked directly from the allowed Disciplines (no separate Discipline choice)."""
    return psychic_powers(key, owner, 1, DISCIPLINES)


# ------------------------------------------------------------------ ids
ZEALOTS = uid("unit", "Covenant Zealot Mob")
GAL_VORBAK = uid("unit", "Gal Vorbak Dark Brethren")
ASHEN = uid("unit", "Ashen Circle")
MHARA = uid("unit", "Mhara Gal Tainted Dreadnought")
PROCURATORS = uid("unit", "Procurator Squad")
POSSESSED = uid("unit", "Possessed Marine Squad")
ARGEL = uid("unit", "Argel Tal")
EREBUS = uid("unit", "High Chaplain Erebus")
KOR = uid("unit", "Kor Phaeron, the Black Cardinal")
ZARDU = uid("unit", "Zardu Layak")
HOL = uid("unit", "Hol Beloth")
LORGAR = uid("unit", "Lorgar Aurelian, the Urizen")
DIABOLIST = L.consul_id("Diabolist")


def diabolist_conds():
    """Conditions that are all true when the Detachment has no Diabolist (or a character counting as one)."""
    return [cond(DIABOLIST, "force", "lessThan", 1), cond(EREBUS, "force", "lessThan", 1),
            cond(KOR, "force", "lessThan", 1), cond(ZARDU, "force", "lessThan", 1)]


# ------------------------------------------------------------------ units
def zealot_mob():
    u = ZEALOTS
    oid = uid("model", u, "Legion Overseer")
    _, overseer = model(u, "Legion Overseer", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 2, 4, 2, 9, "3+/5+"),
                        ["Power Armour", "Refractor Field", "Bolt Pistol", "Frag Grenades", "Krak Grenades"],
                        groups=[slot(oid, "Replace Close Combat Weapon", "Close Combat Weapon",
                                     [("Power Weapon", 10), ("Power Fist", 15)])])
    _, zealots = model(u, "Covenant Zealot", 5, 10, 40, "Infantry", (3, 3, 3, 3, 1, 3, 1, 7, "6+"),
                       ["Autopistol", "Close Combat Weapon", "Flak Armour"])
    e = entry(u, "Covenant Zealot Mob", typ="unit", cost=80 - 10 * 5,
              cats=[foc(TROOPS, "Troops", u), category_link(gs.CAT_LINE, "Compulsory Troops Eligible", key=u)],
              infolinks=rules_links(["Expendable", "Driven to Slaughter"], key=u),
              entries=[overseer, zealots])
    return allegiance_only(e, loyalist=False)


def gal_vorbak(key="Gal Vorbak Dark Brethren", root=True):
    u = uid("unit", key)
    kit = ["Power Armour", "Bolter", "Bolt Pistol", "Close Combat Weapon", "Frag Grenades"]
    mid = uid("model", u, "Dark Martyr")
    _, martyr = model(u, "Dark Martyr", 0, 1, 1, "Infantry (Character)", (5, 4, 5, 5, 3, 5, 3, 10, "3+/5+"), kit,
                      groups=[slot(mid, "Replace Close Combat Weapon", "Close Combat Weapon",
                                   [("Power Weapon", 10), ("Power Fist", 15), ("Lightning Claw", 15)]),
                              take(mid, "Dark Martyr Wargear", [("Artificer Armour", 10)])])
    _, brethren = model(u, "Dark Brethren", 30, 4, 9, "Infantry", (5, 4, 5, 5, 2, 5, 2, 9, "3+/5+"), kit)
    bolter, _ = pool(u, "Dark Brethren: replace Bolter (1 per 5 models)", u,
                     [("Flamer", 5), ("Meltagun", 10), ("Plasma Gun", 15)], 0, every=5)
    ccw, _ = pool(u, "Dark Brethren: replace Close Combat Weapon (1 per 5 models)", u,
                  [("Power Weapon", 10), ("Power Fist", 15)], 0, every=5)
    tr = transports(u, u, ["Land Raider Phobos", "Land Raider Proteus", "Anvillus Pattern Dreadclaw Drop Pod",
                           "Legion Spartan Assault Tank"], orbital=root, spearhead=False)
    gid = tr.get("id")
    big = [cond("model", u, "greaterThan", 5)]  # Bulky: count as two models
    links = tr.find("entryLinks")
    for lk in links:
        # author: Drop Pod, Dreadclaw and Land Raiders carry at most 5 Gal Vorbak; only a Spartan carries more
        if lk.get("targetId") in (T["Land Raider Phobos"], T["Land Raider Proteus"], T["Legion Drop Pod"],
                                  T["Anvillus Pattern Dreadclaw Drop Pod"]):
            add_mods(lk, [modifier("set", "hidden", "true", conds=big)])
    mods, rl = [], [LR, "Daemon", "Fearless", "Bulky", "Rending", "Rending (Gal Vorbak)"]
    if root:
        ss = lambda: [rite("Last of the Serrated Sun")]  # noqa: E731
        lid = uid("link", gid, "serrated", "Legion Drop Pod")
        links.append(link(lid, T["Legion Drop Pod"], "Legion Drop Pod (Last of the Serrated Sun)",
                          mods=[modifier("set", "hidden", "true",
                                         conds=[cond(rite_id("Last of the Serrated Sun"), "force", "lessThan", 1)]),
                                modifier("set", "hidden", "true", conds=big)],
                          constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
        tp = uid(u, "serrated", "Teleportation Transponders")
        transponders = entry(tp, "Teleportation Transponders (Last of the Serrated Sun, units of 6+)", cost=25,
                             rules=[rule(uid(tp, "r"), "Teleportation Transponders (Last of the Serrated Sun)",
                                         "If their unit size is more than 5 models, Gal Vorbak may purchase Teleportation "
                                         "Transponders for +25 points per unit instead of a Legion Drop Pod or Dreadclaw "
                                         "Drop Pod.")],
                             constraints=[constraint(uid(tp, "max"), "max", 1, auto=True)],
                             mods=[modifier("set", "hidden", "true", groups=[any_of(
                                 cond(rite_id("Last of the Serrated Sun"), "force", "lessThan", 1),
                                 cond("model", u, "lessThan", 6))])])
        mods = troops_mods(ss) + [modifier("remove", "category", ELITES, conds=ss()),
                                  modifier("add", "error", "Last of the Serrated Sun: every Gal Vorbak unit must purchase "
                                                           "a Legion Drop Pod or Dreadclaw Drop Pod as a Dedicated "
                                                           "Transport (units of more than 5 models: or Teleportation "
                                                           "Transponders).",
                                           conds=ss() + [cond(T["Legion Drop Pod"], u, "lessThan", 1),
                                                         cond(T["Anvillus Pattern Dreadclaw Drop Pod"], u, "lessThan",
                                                              1)],
                                           groups=[any_of(cond("model", u, "lessThan", 6),
                                                          cond(tp, u, "lessThan", 1))])]
        rl.append("Selected as Troops (Last of the Serrated Sun)")
    else:
        rl.append("Retinue")
    e = entry(u, "Gal Vorbak Dark Brethren", typ="unit", cost=200 - 4 * 30, mods=mods,
              cats=[foc(ELITES, "Elites", u)] if root else [],
              infolinks=rules_links(rl, key=u),
              entries=[martyr, brethren, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                       per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])] + (
                  [transponders] if root else []),
              groups=[bolter, ccw, tr])
    return allegiance_only(e, loyalist=False)


def ashen_circle():
    u = ASHEN
    kit = ["Hardened Power Armour", "Jump Pack", "Hand Flamer", "Frag Grenades"]
    iid = uid("model", u, "Iconoclast")
    swaps = [("Rending Weapon", 5), ("Power Weapon", 10)]
    _, icon = model(u, "Iconoclast", 0, 1, 1, "Jump Infantry (Character)", (5, 4, 4, 4, 1, 4, 3, 10, "3+"), kit,
                    groups=[slot(iid, "Replace Axe-rake", "Axe-rake", swaps),
                            slot(iid, "Replace Hand Flamer", "Hand Flamer", [("Plasma Pistol", 15)]),
                            take(iid, "Iconoclast Wargear", [("Artificer Armour", 10)])])
    inc_id, inc = model(u, "Incendiary", 25, 4, 9, "Jump Infantry", (5, 4, 4, 4, 1, 4, 2, 9, "3+"), kit + ["Axe-rake"])
    tog = uid(u, "reign-of-fire")
    no_zardu = lambda: [cond(ZARDU, "roster", "lessThan", 1)]  # noqa: E731
    troops = entry(tog, "Selected as Troops (Reign of Fire)",
                   constraints=[constraint(uid(tog, "max"), "max", 1, auto=True)],
                   mods=[modifier("set", "hidden", "true", conds=no_zardu()),
                         modifier("set", uid(tog, "max"), 0, conds=no_zardu())],
                   infolinks=rules_links(["Selected as Troops (Reign of Fire)"], key=tog))
    on = lambda: [cond(tog, "self", "atLeast", 1)]  # noqa: E731
    return entry(u, "Ashen Circle", typ="unit", cost=175 - 4 * 25,
                 mods=troops_mods(on) + [modifier("remove", "category", FA, conds=on())],
                 cats=[foc(FA, "Fast Attack", u)],
                 infolinks=rules_links([LR, "Hardened Armour", "Bitter Duty"], key=u),
                 entries=[icon, inc, troops,
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[model_swaps(u, "Incendiaries: replace Axe-rake (any number)", u, [inc_id], swaps)])


def mhara_gal():
    u = MHARA
    built_in = [("Heavy Flamer", 10), ("Meltagun", 15), ("Plasma Blaster", 20)]
    a1 = uid(u, "arm1-ccw")
    a2 = uid(u, "arm2-ccw")
    arm1 = entry(a1, "Dreadnought Close Combat Weapon", constraints=[constraint(uid(a1, "min"), "min", 1),
                                                                     constraint(uid(a1, "max"), "max", 1)],
                 links=[gear(a1, "Dreadnought Close Combat Weapon")],
                 groups=[slot(a1, "Built-in weapon", "Twin-linked Bolter", built_in)])
    arm2 = entry(a2, "Second Dreadnought Close Combat Weapon", links=[gear(a2, "Dreadnought Close Combat Weapon")],
                 groups=[slot(a2, "Built-in weapon", "Twin-linked Bolter", built_in)])
    prof = walker_profile(u, "Mhara Gal", 6, 3, 7, 13, 12, 11, 5, 3)
    prof_mods(prof, [modifier("set", gs.char_id("Walker", "A"), 4, conds=[cond(a2, u, "atLeast", 1)])])
    dp = uid("grp", u, "transport")
    tr = group(dp, "Dedicated Transport",
               links=[link(uid("link", dp, "ddp"), T["Legion Dreadnought Drop Pod"], "Legion Dreadnought Drop Pod")],
               constraints=[constraint(uid(dp, "max"), "max", 1, auto=True)])
    e = entry(u, "Mhara Gal Tainted Dreadnought", typ="unit", cost=305, cats=[foc(ELITES, "Elites", u)],
              constraints=[force_limit(u, 1)], profiles=[prof],
              infolinks=rules_links(["Daemon", "Fleet", "It Will Not Die", "Adamantium Will", "Daemonic Engine",
                                     "Shroud of Dark Fire", "Accursed", "Paired Close-Combat Arms (Mhara Gal)"], key=u),
              links=[gear(u, "Smoke Launchers"), gear(u, "Searchlight")],
              entries=[arm1],
              groups=[slot(u, "Replace Plasma Cannon", "Plasma Cannon",
                           [("Multi-Melta", 0), ("Twin-linked Autocannon", 5), ("Twin-linked Lascannon", 20),
                            (arm2, None)]), tr])
    return allegiance_only(e, loyalist=False)


def procurators():
    u = PROCURATORS
    jp_id = uid("squadwide", u, "Jump Packs (entire squad)")
    jp_on = lambda: [has(jp_id, u)]  # noqa: E731
    pid = uid("model", u, "Procurator Prime")
    _, prime = model(u, "Procurator Prime", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 2, 10, "2+"),
                     ["Artificer Armour", "Bolt Pistol", "Frag Grenades", "Narthecium", "Reductor"],
                     groups=[slot(pid, "Replace Chainsword", "Chainsword", [("Power Weapon", 10), ("Power Fist", 15)])],
                     rules_=["Procurator Prime"])
    prime.find("profiles")[0].insert(0, wrap("modifiers", [unit_type_mod("Jump Infantry (Character)", jp_on())]))
    _, procs = model(u, "Procurator", 20, 4, 9, "Infantry", (4, 4, 4, 4, 1, 4, 2, 9, "3+"),
                     ["Power Armour", "Bolt Pistol", "Chainsword", "Frag Grenades"])
    procs.find("profiles")[0].insert(0, wrap("modifiers", [unit_type_mod("Jump Infantry", jp_on())]))
    cs, _ = pool(u, "Procurators: replace Chainsword (1 per 5 models)", u,
                 [("Rending Weapon", 5), ("Power Weapon", 10), ("Power Fist", 15)], 0, every=5)
    bp, _ = pool(u, "Procurators: replace Bolt Pistol (1 per 5 models)", u,
                 [("Hand Flamer", 5), ("Plasma Pistol", 15)], 0, every=5)
    e = entry(u, "Procurator Squad", typ="unit", cost=130 - 4 * 20, cats=[foc(ELITES, "Elites", u)],
              infolinks=rules_links([LR, "Flesh Harvesters", "Procurator Jump Packs"], key=u),
              entries=[prime, procs, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                       per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]),
                       per_model(u, "Jump Packs (entire squad)", 15, u, ["Jump Pack"])],
              groups=[cs, bp, transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                                "Anvillus Pattern Dreadclaw Drop Pod"], block_if=jp_on())])
    return allegiance_only(e, loyalist=False)


def possessed():
    u = POSSESSED
    kit = ["Power Armour", "Bolt Pistol"]
    pm = uid("model", u, "Possessed Marine")
    ch = uid("model", u, "Possessed Champion")
    champ = entry(ch, "Possessed Champion (upgrade one Possessed Marine)", typ="model", cost=26 + 10,
                  constraints=[constraint(uid(ch, "max"), "max", 1)],
                  profiles=[unit_profile(u, "Possessed Champion", "Infantry (Character)", 4, 4, 5, 4, 1, 4, 3, 10,
                                         "3+/5+")],
                  links=[gear(ch, k) for k in kit],
                  groups=[slot(ch, "Replace Close Combat Weapon", "Close Combat Weapon",
                               [("Rending Weapon", 5), ("Power Weapon", 10), ("Power Fist", 15)])])
    mn, mx = uid(pm, "min"), uid(pm, "max")
    marines = entry(pm, "Possessed Marine", typ="model", cost=26, mods=specials_decrement(pm, mn, mx, [ch], u),
                    constraints=[constraint(mn, "min", 5, auto=True), constraint(mx, "max", 10, auto=True)],
                    profiles=[unit_profile(u, "Possessed Marine", "Infantry", 4, 4, 5, 4, 1, 4, 2, 10, "3+/5+")],
                    links=[gear(pm, k) for k in kit + ["Close Combat Weapon"]])
    e = entry(u, "Possessed Marine Squad", typ="unit", cost=0, cats=[foc(ELITES, "Elites", u)],
              constraints=[force_limit(u, 2)],
              infolinks=rules_links([LR, "Daemon", "Fearless", "Daemonkin"], key=u),
              entries=[marines, champ, per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                       per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
              groups=[transports(u, u, ["Legion Rhino Armoured Carrier", "Anvillus Pattern Dreadclaw Drop Pod"])])
    return allegiance_only(e, loyalist=False)


# ------------------------------------------------------------------ characters
def anakatis_kul():
    eid = uid("upg", ZARDU, "Anakatis Kul")
    return entry(eid, "Anakatis Kul Blade-Slaves (2 models)", cost=100,
                 constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                 profiles=[unit_profile(eid, "Anakatis Kul", "Infantry", 5, 4, 6, 5, 3, 5, 3, 8, "3+/5+")],
                 links=[gear(eid, k) for k in ["Power Armour", "Pair of Rending Weapons", "Plasma Pistol"]],
                 infolinks=rules_links(["Anakatis Kul", "Daemon", "Fearless", "Furious Charge", "It Will Not Die",
                                        "Bulky", "Mindless Killers"], key=eid))


def characters():
    out = []
    out.append(named_character(
        LR, "Argel Tal", 195, (5, 4, 5, 5, 3, 5, 4, 10, "3+/4+"),
        ["Power Armour", "Jump Pack (Daemonic Wings)", "Custodian Spear", "Bolt Pistol", "Frag Grenades"],
        ["Daemon", "Fearless", "Lord of the Gal Vorbak"],
        retinue=retinue_links("argel", [gal_vorbak("argel-gv", root=False)]),
        extra_groups=[krak(ARGEL)], unit_type="Jump Infantry (Character)", loyalist=False))
    out.append(named_character(
        LR, "High Chaplain Erebus", 195, (5, 5, 4, 4, 3, 5, 3, 10, "2+/4+"),
        ["Artificer Armour", "Master-crafted Accursed Crozius", "Bolt Pistol", "Anathame Dagger", "Frag Grenades"],
        ["Psyker", "High Chaplain", "Burning Lore", "Burning Lore (Named Character)", "Command Retinue (Word Bearers)"],
        retinue=retinue_links("erebus", [command_squad_for("erebus", EREBUS)]),
        extra_groups=[krak(EREBUS), burning_lore_powers(EREBUS, EREBUS)], loyalist=False, profile_name="Erebus"))
    out.append(named_character(
        LR, "Kor Phaeron, the Black Cardinal", 165, (4, 4, 4, 3, 4, 3, 2, 10, "2+/4+"),
        ["Terminus Consolaris", "Pair of Lightning Claws", "Hand Flamer"],
        ["Psyker", "Feel No Pain", "Burning Lore", "Burning Lore (Named Character)", "Black Cardinal",
         "Jealous Command", "Command Retinue (Word Bearers)"],
        retinue=retinue_links("kor", [L2.terminator_command_squad("kor")]),
        extra_groups=[burning_lore_powers(KOR, KOR)], loyalist=False, profile_name="Kor Phaeron"))
    out.append(named_character(
        LR, "Zardu Layak", 175, (5, 5, 4, 5, 2, 5, 2, 10, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Master-crafted Force Weapon", "Bolt Pistol", "Legion Standard",
         "Frag Grenades"],
        ["Daemon", "Zealot", "Psyker", "Psychic Powers (Zardu Layak)", "Crimson Apostle", "Dark Channeler",
         "Reign of Fire"],
        extra_groups=[krak(ZARDU, melta=False), psychic_powers(ZARDU, ZARDU, 2, ["Daemonology (Malefic)"])],
        extra_entries=[anakatis_kul()], loyalist=False))
    out.append(named_character(
        LR, "Hol Beloth", 175, (6, 5, 4, 4, 3, 5, 4, 10, "2+/4+"),
        ["Artificer Armour", "Iron Halo (Named Character)", "Master-crafted Power Fist", "Tainted Weapon",
         "Plasma Pistol", "Frag Grenades"],
        ["Tainted Weapon (Hol Beloth)", "Hexaglyphic Ward", "Exhortation of Battle", "Command Retinue (Word Bearers)"],
        retinue=retinue_links("hol", [command_squad_for("hol", HOL)]),
        extra_groups=[krak(HOL)], loyalist=False))
    return out


def lorgar():
    u = LORGAR
    gv = gal_vorbak("lorgar-gv", root=False)
    ret = primarch_retinue("lorgar", extra=[gv])
    loyal = lambda: [cond(LOYALIST, "roster", "atLeast", 1)]  # noqa: E731
    for lk in ret.iter("entryLink"):
        if lk.get("targetId") == gv.get("id"):
            add_mods(lk, [modifier("set", "hidden", "true", conds=loyal())])
    tid = uid("upg", u, "Lorgar Transfigured")
    trans = entry(tid, "Lorgar Transfigured (Traitor only)", cost=75,
                  constraints=[constraint(uid(tid, "max"), "max", 1, auto=True)],
                  mods=[modifier("set", "hidden", "true", conds=loyal())],
                  infolinks=rules_links(["Lorgar Transfigured", "Psyker", "Psychic Ascendancy",
                                         "Illuminarum (Transfigured)", "Force"], key=tid),
                  groups=[psychic_powers(tid, u, 3, ["Divination", "Telekinesis"])])
    e = primarch(LR, "Lorgar Aurelian, the Urizen", 460, (6, 6, 6, 6, 5, 6, 5, 10, "1+"),
                 ["Armour of the Word", "Illuminarum", "Frag Grenades"],
                 ["Primarch Armour", "Fanatical Devotion", "Voice of the Urizen", "Fanatical Devotion (Lorgar)",
                  "Dark Oratory", "Primarch Retinue (Lorgar)"],
                 retinue=ret, extra_entries=[trans], profile_name="Lorgar Aurelian",
                 extra_mods=[modifier("add", "error", "Lorgar Transfigured may only be selected in a Traitor Word "
                                                      "Bearers army.", conds=[has(tid, u)] + loyal()),
                             modifier("set", "name", "Lorgar Transfigured", conds=[has(tid, u)])])
    return e


# ------------------------------------------------------------------ Legion-wide options
def add_diabolist(ctx):
    cid = add_consul(ctx, "Diabolist", 35, ["Diabolist", "Daemon", "Preferred Enemy", "Preferred Enemy (Loyalists)"],
                     forbids=["Space Marine Bike", *TDA, "Power Fist", "Thunder Hammer"])
    cen = ctx.unit("Legion Centurion")
    loyal = lambda: [cond(LOYALIST, "roster", "atLeast", 1)]  # noqa: E731
    for ce in cen.iter("selectionEntry"):
        if ce.get("id") == cid:
            add_mods(ce, [modifier("set", "hidden", "true", conds=loyal())])
    add_mods(cen, [modifier("add", "error", "The Diabolist Consul is Traitor only.",
                            conds=[has(cid, cen.get("id"))] + loyal())])
    return cid


def add_crozius(ctx):
    """Accursed Crozius: Praetor/Centurion replace their close combat weapon (+40, outside the 100-pt Armoury cap);
    a Chaplain may swap his Crozius Arcanum and Rosarius for one for free."""
    ac = W("Accursed Crozius")
    for n in ("Legion Praetor", "Legion Centurion"):
        e = ctx.unit(n)
        u = e.get("id")
        cap = find_group(e, "Space Marine Armoury (max 100 pts)")
        cc = None
        for g in cap.iter("selectionEntryGroup"):
            if g.get("name") == "Replace Chainsword":
                cc = g
        lid = uid("link", cc.get("id"), "wb", "Accursed Crozius")
        cc.find("entryLinks").append(link(lid, ac, "Accursed Crozius", cost=40,
                                          constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
        cap_c = next(c for c in cap.iter("constraint") if c.get("field") == PTS)
        add_mods(cap, [modifier("increment", cap_c.get("id"), 40, conds=[has(ac, u)])])
    cen = ctx.unit("Legion Centurion")
    u = cen.get("id")
    chap = next(x for x in cen.iter("selectionEntry") if x.get("id") == L.consul_id("Chaplain"))
    oid = uid("wb", "chaplain", "Accursed Crozius")
    opt = entry(oid, "Accursed Crozius (replaces Crozius Arcanum and Rosarius)", cost=0,
                constraints=[constraint(uid(oid, "max"), "max", 1, auto=True)],
                links=[gear(oid, "Accursed Crozius")])
    add_to(chap, "selectionEntries", [opt])
    on = lambda: [has(oid, u)]  # noqa: E731
    for lk in chap.find("entryLinks"):
        if lk.get("targetId") in (W("Crozius Arcanum"), W("Rosarius")):
            mods = [modifier("set", "hidden", "true", conds=on())]
            for c in lk.iter("constraint"):
                mods.append(modifier("set", c.get("id"), 0, conds=on()))
            add_mods(lk, mods)


def add_ic_options(ctx):
    """Accursed Crozius (Armoury), Burning Lore, Favour of the Pantheon for the Praetor and Centurion."""
    add_crozius(ctx)
    # Favour of the Pantheon: one shared entry, at most one per army
    fid = uid("wb", "favour")
    fg = uid("grp", fid, "favour")
    favours = [("Daemonic Aura", 15, "5+ Invulnerable Save."), ("Daemonic Mutation", 15, "+1 Attack."),
               ("Daemonic Strength", 10, "+1 Strength."),
               ("Daemonic Wings", 20, "The model becomes Jump Infantry. May not be combined with a Jump Pack, Bike, "
                                      "Jetbike or Terminator Armour."),
               ("Daemonic Visage", 5, "An enemy unit which loses a close combat involving the bearer suffers an "
                                      "additional -1 Leadership when taking the resulting Morale test.")]
    fav_ents = [entry(uid(fid, n), n, cost=c, constraints=[constraint(uid(fid, n, "max"), "max", 1, auto=True)],
                      rules=[rule(uid(fid, n, "r"), n, t)]) for n, c, t in favours]
    favour = entry(fid, "Favour of the Pantheon (one Independent Character per army)",
                   constraints=[constraint(uid(fid, "roster"), "max", 1, scope="roster", deep=True)],
                   infolinks=rules_links(["Favour of the Pantheon"], key=fid),
                   groups=[group(fg, "Favour", entries=fav_ents,
                                 constraints=[constraint(uid(fg, "min"), "min", 1, auto=True),
                                              constraint(uid(fg, "max"), "max", 1, auto=True)])])
    ctx.add_shared(favour)
    wings, aura = uid(fid, "Daemonic Wings"), uid(fid, "Daemonic Aura")
    psy = [L.consul_id(c) for c in L.PSYKER_CONSULS]
    for n, base_s, base_a in [("Legion Praetor", 4, 3), ("Legion Centurion", 4, 3)]:
        e = ctx.unit(n)
        u = e.get("id")
        lid = uid("link", u, "wb-favour")
        fl = link(lid, fid, favour.get("name"), constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])
        bl = uid("upg", u, "Burning Lore")
        lore = entry(bl, "Burning Lore (Psyker, Mastery Level 1)", cost=30,
                     constraints=[constraint(uid(bl, "max"), "max", 1, auto=True)],
                     infolinks=rules_links(["Burning Lore", "Psyker"], key=bl),
                     groups=[burning_lore_powers(bl, u)])
        if n == "Legion Centurion":
            add_mods(lore, hide_mods(bl, lambda: [any_of(*[has(c, u) for c in psy])]))
        hb = option(u + "wb", "Hex-Bolts", 5, item="Hex-Bolts")
        if n == "Legion Centurion":  # the Vigilator has Special Issue Ammunition
            add_mods(hb, hide_mods(hb.get("id"), lambda: [any_of(has(L.consul_id("Vigilator"), u))]))
        add_group(e, group(uid("grp", u, "wb"), "Word Bearers Options", entries=[lore, hb], links=[fl]))
        # Daemonic Wings: not with a Jump Pack, Bike or Terminator Armour
        for x in ["Jump Pack", "Space Marine Bike", *TDA]:
            add_mods(e, [modifier("add", "error", f"Daemonic Wings may not be combined with {x}.",
                                  groups=[all_of(has(wings, u), has(W(x), u))])])
        prof = e.find("profiles")[0]
        prof_mods(prof, [
            modifier("set", gs.char_id("Unit", "S"), base_s + 1, conds=[has(uid(fid, "Daemonic Strength"), u)]),
            modifier("set", gs.char_id("Unit", "A"), base_a + 1, conds=[has(uid(fid, "Daemonic Mutation"), u)]),
            unit_type_mod("Jump Infantry (Character)", [has(wings, u)])])
    # other non-named Independent Characters (Techmarines): Favour as text (profile not changed)
    for e in entries_named(ctx, ["Legion Techmarine"]):
        if e.get("type") != "model":
            continue
        lid = uid("link", e.get("id"), "wb-favour")
        add_to(e, "entryLinks", [link(lid, fid, favour.get("name"),
                                      constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])])


def add_squad_options(ctx):
    """Hex-Bolts, Icon of Chaos Undivided, Dark Channelling."""
    hex_units = ["Legion Tactical Squad", "Legion Assault Squad", "Legion Breacher Siege Squad",
                 "Legion Reconnaissance Squad", "Legion Veteran Squad", "Legion Command Squad",
                 "Legion Honour Guard Squad", "Legion Terminator Squad", "Legion Terminator Command Squad",
                 "Legion Destroyer Squad", "Legion Heavy Support Squad", "Gal Vorbak Dark Brethren",
                 "Procurator Squad", "Possessed Marine Squad"]
    for e in entries_named(ctx, hex_units):
        u = e.get("id")
        o = option(u + "wb", "Hex-Bolts (unit)", 5, item="Hex-Bolts")
        oid = o.get("id")
        add_mods(o, hide_mods(oid, lambda: [any_of(has(W("Special Issue Ammunition"), u))]))
        add_to(e, "selectionEntries", [o])
    for e in entries_named(ctx, ["Legion Command Squad", "Legion Veteran Squad", "Legion Terminator Squad"]):
        add_to(e, "selectionEntries", [option(e.get("id") + "wb", "Icon of Chaos Undivided (one model)", 30,
                                              item="Icon of Chaos Undivided")])
    for e in entries_named(ctx, ["Legion Tactical Squad", "Legion Veteran Squad", "Legion Breacher Siege Squad",
                                 "Legion Terminator Squad", "Legion Assault Squad"]):
        dc = upgrade(e.get("id") + "wb", "Dark Channelling", 25, rules_=["Dark Channelling"])
        add_mods(dc, hide_mods(dc.get("id"), lambda: [all_of(*diabolist_conds())]))
        add_to(e, "selectionEntries", [dc])


def add_drop_elite(ctx):
    """Last of the Serrated Sun: units able to take a Rhino may take a Legion Drop Pod instead."""
    rhino, pod = T["Legion Rhino Armoured Carrier"], T["Legion Drop Pod"]
    seen = set()
    for r in ctx.all_entries():
        for g in r.iter("selectionEntryGroup"):
            if g.get("name") != "Dedicated Transport" or id(g) in seen:
                continue
            seen.add(id(g))
            links = g.find("entryLinks")
            if links is None:
                continue
            targets = [lk.get("targetId") for lk in links]
            plain_pod = any(lk.get("targetId") == pod and "(" not in (lk.get("name") or "") for lk in links)
            if rhino not in targets or plain_pod:
                continue
            lid = uid("link", g.get("id"), "drop-elite")
            links.append(link(lid, pod, "Legion Drop Pod (Drop Elite)",
                              mods=[modifier("set", "hidden", "true",
                                             conds=[cond(rite_id("Last of the Serrated Sun"), "force", "lessThan", 1)])],
                              constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))


# ------------------------------------------------------------------ extend
def extend(ctx):
    ctx.legion_rules([LR, "Fanatical Devotion", "The Dark Shepherds", "Ritual of Consecration", "Daemonic Covenant"])

    # changes to existing entries (before retinue copies are made)
    add_diabolist(ctx)
    add_ic_options(ctx)

    ctx.add_units(zealot_mob(), gal_vorbak(), ashen_circle(), mhara_gal(), procurators(), possessed(), *characters(),
                  lorgar())
    ctx.finish()

    add_squad_options(ctx)
    add_drop_elite(ctx)
    character_variant(ctx.all_entries(), "Power Weapon", "Tainted Weapon")

    # The Dark Shepherds: a Chaplain Consul or Dark Apostle in the Detachment
    legion = ctx.unit("Legion")
    no_shepherd = all_of(cond(L.consul_id("Chaplain"), "force", "lessThan", 1),
                         cond(W("Accursed Crozius"), "force", "lessThan", 1),
                         cond(EREBUS, "force", "lessThan", 1), cond(KOR, "force", "lessThan", 1),
                         cond(ZARDU, "force", "lessThan", 1), cond(ARGEL, "force", "lessThan", 1),
                         cond(HOL, "force", "lessThan", 1), cond(LORGAR, "force", "lessThan", 1))
    add_mods(legion, [modifier("add", "error", "The Dark Shepherds: a Word Bearers Detachment must include at least one "
                                               "Legion Chaplain Consul or Dark Apostle (a model with an Accursed "
                                               "Crozius or a Word Bearers named character) as an HQ selection.", groups=[no_shepherd])])

    # Rites of War
    traitor_only = ("only a Traitor Word Bearers Detachment may use this Rite of War.",
                    [cond(LOYALIST, "roster", "atLeast", 1)])
    fort = [cond(gs.cat("Fortification"), "roster", "atLeast", 1)]
    ctx.add_rite("The Dark Brethren", RULES["The Dark Brethren"], limit_hs=True, errors=[
        traitor_only,
        ("the Detachment must include at least one Diabolist (or Erebus, Kor Phaeron or Zardu Layak).",
         diabolist_conds()),
        ("the army may not include a Fortification.", fort),
    ])
    ctx.add_rite("Last of the Serrated Sun", RULES["Last of the Serrated Sun"], errors=[
        traitor_only,
        ("the army may not include a Fortification.", fort),
    ])
