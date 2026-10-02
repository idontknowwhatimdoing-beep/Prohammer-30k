"""XV Legion - Thousand Sons (Forces of the Legions)."""
import copy

from bsx import (PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group,
                 info_link, category_link)
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, TDA, has_tda, no_tda, gear, per_model, rules_links, unit_profile
from legiones2 import (slot, take, pool, choice, transports, add_mods, add_to, dedupe_kit, walker_profile, foc,
                       rite_id, rite, any_rite, RETINUE_SHARED, TROOPS, ELITES, FA, HQ, _negate, model_swaps,
                       pa_armoury)
from legiones_wargear import ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR
from legions.common import PRIMARCH_RULES

LEGION = "XV - Thousand Sons"

TS = uid("legion", "XV - Thousand Sons")
LOW = gs.cat("Lords of War")


def ts():
    return cond(TS, "force", "atLeast", 1)


def not_ts():
    return cond(TS, "force", "lessThan", 1)


def ts_only(e, max_id=None):
    """Hide an entry/link (and forbid it) unless the army is Thousand Sons."""
    mods = [modifier("set", "hidden", "true", conds=[not_ts()])]
    if max_id:
        mods.append(modifier("set", max_id, 0, conds=[not_ts()]))
    add_mods(e, mods)
    return e


# ---------------------------------------------------------------- data
CULTS = {
    "Pavoni": ("Pavoni - Quickblood", "Cult Arcana: the unit gains Fleet. Cult Mastery (Psyker unit or Psychic "
               "Brotherhood): also gains Crusader.", "Biomancy"),
    "Raptora": ("Raptora - Kine Shields", "Cult Arcana: models gain a 6+ Invulnerable Save against shooting attacks (does "
                "not improve an existing one). Cult Mastery: instead a 5+ Invulnerable Save against shooting, or +1 to an "
                "existing Invulnerable Save against shooting (max 4+); +1 to Cover Saves against shooting (max 3+). No "
                "effect in close combat.", "Telekinesis"),
    "Corvidae": ("Corvidae - Precognitive Strike", "Cult Arcana: re-roll To Hit rolls of 1 for First Fire shooting "
                 "attacks. Cult Mastery: also re-roll To Hit rolls of 1 for Overwatch, Return Fire and Stand & Shoot "
                 "attacks.", "Divination"),
    "Athanaeans": ("Athanaeans - Discipline of the Mind", "Cult Arcana: Stubborn and re-roll failed Pinning tests. Cult "
                   "Mastery: also Adamantium Will.", "Telepathy"),
    "Pyrae": ("Pyrae - Ashen Blow", "Cult Arcana: Hammer of Wrath. Cult Mastery: close-combat attacks and Flame weapons "
              "gain Soul Blaze.", "Pyromancy"),
}
DISCIPLINES = ["Biomancy", "Divination", "Pyromancy", "Telekinesis", "Telepathy"]

TS_RULES = {
    "Legiones Astartes (Thousand Sons)": (
        "Models with this rule belong to the XV Legion and use the Thousand Sons Legion special rules: Sorcerers of "
        "Prospero, The Prosperine Cults, Psychic Brotherhoods, Price of Knowledge and Signs and Portents."),
    "Sorcerers of Prospero": (
        "All Thousand Sons Independent Characters are Psykers: Psyker (Mastery Level 1) unless they already have a higher "
        "Mastery Level; a Thousand Sons Praetor is Psyker (Mastery Level 2). A Psyker permitted to select a Psychic "
        "Discipline selects its powers from ONE of Biomancy, Divination, Pyromancy, Telekinesis or Telepathy. A Librarian "
        "Consul follows these rules; activating a Force Weapon counts as the use of a psychic power. A Psyker may not use "
        "the same power more than once in the same player turn."),
    "The Prosperine Cults": (
        "Any Thousand Sons unit or Independent Character permitted by its entry to select a Prosperine Cult must be "
        "assigned to one Cult (Pavoni, Raptora, Corvidae, Athanaeans, Pyrae) when the army is selected and receives its "
        "Cult Arcana. A model or unit belongs to one Cult only. An Independent Character keeps its own Cult when joining "
        "another unit; Cult Arcana and Cult Mastery are not shared. A Cult does not make a model a Psyker."),
    "Cult Mastery": ("A unit with the Psyker or Brotherhood of Psykers special rule additionally receives the Cult Mastery "
                     "benefit of its Cult. Cult Mastery needs no Psychic Test and is not a psychic power."),
    "Psychic Brotherhoods": (
        "Legion Veteran Squads and Legion Terminator Squads may purchase Brotherhood of Psykers (Mastery Level 1) for +25 "
        "points. The unit selects one psychic power from the Discipline of its Cult (Pavoni - Biomancy, Raptora - "
        "Telekinesis, Corvidae - Divination, Athanaeans - Telepathy, Pyrae - Pyromancy) and gains its Cult Mastery. An "
        "Independent Character joining a Brotherhood remains a separate Psyker."),
    "Price of Knowledge": (
        "A Thousand Sons Detachment has one additional HQ and one additional Elites selection and one fewer Fast Attack "
        "selection (HQ 1-3, Elites 0-4, Fast Attack 0-2 on the Standard Force Organisation Chart). Mark the units in the "
        "additional slots on the roster: with Victory Points, each such unit completely destroyed gives the opponent an "
        "additional 50 Victory Points."),
    "Signs and Portents": (
        "Whenever a Thousand Sons Psyker or Brotherhood suffers one or more Wounds from Perils of the Warp, every friendly "
        "non-vehicle Thousand Sons unit must take a Pinning test. If every Thousand Sons Independent Character in the "
        "Detachment has been slain, surviving Thousand Sons units suffer -1 Leadership and may no longer Pursue."),
    "Prosperine Force Weapon": (
        "Follows the normal rules for Force Weapons. In a Psychic Brotherhood, nominate one model that inflicted unsaved "
        "wounds with a Force Weapon; the Brotherhood makes one Psychic Test to activate that model's weapon (only its "
        "wounds become Massive Wounds). A Brotherhood may make only one Force Weapon activation each Assault phase."),
    "Arcane Litanies": ("Once per battle, when the bearer suffers a Wound from Perils of the Warp, it may ignore that "
                        "Wound. The Psychic Test and power are otherwise resolved normally."),
    "Asphyx Shells": ("Bolt Pistols, Bolters, Combi-Bolters and the Bolter component of Combi-Weapons gain the Shred "
                      "special rule. May not be combined with Special Issue Ammunition or another ammunition upgrade."),
    "Teleportation Transponders": ("The model or unit gains Deep Strike and may deploy using Deep Strike even if the "
                                   "mission would not normally permit it. An Independent Character Deep Striking with "
                                   "another unit must purchase its own."),
    "Prosperine Aether-Disc": (
        "The bearer becomes Jump Infantry and gains Turbo-Boosters and Hammer of Wrath. Aetheric Evasion: if it moved at "
        "least 6\" in its preceding Movement phase, enemy models suffer -1 To Hit against it in close combat (max 6+), not "
        "while Falling Back. May not be combined with a Jump Pack, Bike, Jetbike or Terminator Armour."),
    "Aether-fire Cannon": ("Free upgrade for a Plasma Cannon. If a unit has more than one Plasma Cannon, all or none of "
                           "them must be upgraded."),
    "Scarab Occult": (
        "The Cabal is a Psychic Brotherhood assigned to one Prosperine Cult and receives its Cult Arcana and Cult Mastery. "
        "It selects one power from Biomancy, Divination, Pyromancy, Telekinesis or Telepathy and tests on Leadership 9. "
        "While the Sekhmet Inceptor lives, it is Mastery Level 2, knows one additional power and tests on Leadership 10."),
    "Mindsong of Blades": ("Blessing invoked at the beginning of an Assault phase. Until the end of that phase, models in "
                           "the Psyker's unit gain +1 Initiative and may re-roll close-combat To Hit rolls of 1."),
    "Paired Prosperine Force Blades": ("Count as a pair of Prosperine Force Weapons; the bonus Attack for two close-combat "
                                       "weapons is already included in the profile."),
    "Aetheric Command Matrix": (
        "At the beginning of each Thousand Sons Movement phase, if no model in the Maniple is within 12\" of a friendly "
        "Thousand Sons Psyker, it takes a Leadership test. If failed, it may not Advance or charge and must shoot the "
        "nearest visible eligible enemy unit."),
    "Psychic Conduit": (
        "Once per Thousand Sons Shooting phase, a friendly Thousand Sons Psyker within 12\" may channel one psychic "
        "shooting power through one Castellax-Achea (range and line of sight from it). That Castellax-Achea may not fire "
        "its Aether-fire Cannon that phase, and suffers one Wound (Invulnerable Save allowed) if the Psyker suffers Perils."),
    "Aetheric Shielding": "The Castellax-Achea has a 5+ Invulnerable Save (included in its profile).",
    "Thousand Sons Construct": ("Counts as a Thousand Sons unit for rules affecting friendly Thousand Sons units, but "
                                "does not have Legiones Astartes and is not assigned to a Prosperine Cult."),
    "Psychic Dreadnought": (
        "The Osiron selects one psychic power from Biomancy, Divination, Pyromancy, Telekinesis or Telepathy (a second one "
        "at Mastery Level 2) and tests on Leadership 9. If it suffers Perils of the Warp it suffers one automatic Glancing "
        "Hit that Atomantic Shielding may not prevent. It is not assigned to a Prosperine Cult."),
    "Aetheric Battle-Engine": (
        "The Osiron may invoke psychic powers in a turn in which it fires its weapons; one psychic shooting power may be "
        "resolved in addition to its normal shooting. All its shooting that phase must target the same enemy unit."),
    "Osiron Force Blade": ("Counts as both a Dreadnought Close Combat Weapon and a Force Weapon. Force Weapon activation "
                           "does not count as invoking a psychic power."),
    "Order of Ruin": ("The Cabal is assigned to one Prosperine Cult and receives its Cult Arcana; while the Numerologist "
                      "lives it also receives its Cult Mastery. The Numerologist knows only Psy-Synchronicity."),
    "Psy-Synchronicity": (
        "Blessing invoked in the Thousand Sons Movement phase: up to two friendly Thousand Sons units with a model within "
        "6\" of the Numerologist may re-roll shooting To Hit rolls of 1 until the end of the following Shooting phase. The "
        "Numerologist may not fire a weapon in a turn in which he invokes it."),
    "Corvidae (Ahriman)": "Ahriman always belongs to the Corvidae and receives both its Cult Arcana and Cult Mastery.",
    "Chief Librarian": ("Ahriman knows every psychic power in the Divination discipline, but still follows the normal "
                        "limits on how many powers he may invoke each player turn."),
    "Black Staff of Ahriman": (
        "A Master-crafted Prosperine Force Weapon. Once per player turn Ahriman may re-roll one failed Psychic Test; if the "
        "re-roll also fails he suffers Perils of the Warp. Activating it as a Force Weapon is not invoking a power."),
    "Ahriman's Cabal": (
        "Ahriman may select one Legion Command Squad as his retinue (no Force Organisation slot). It may purchase Ahriman's "
        "Cabal for +50 points: it becomes a Brotherhood of Psykers (Mastery Level 2), is Corvidae with both Cult Arcana "
        "and Cult Mastery, and selects two Divination powers. Models permitted a Power Weapon may upgrade it to a "
        "Prosperine Force Weapon for +5 points."),
    "Raptora (Phosis)": "Phosis always belongs to the Raptora and receives both its Cult Arcana and Cult Mastery.",
    "Magister of the Raptora": "Phosis selects both his psychic powers from the Telekinesis discipline.",
    "Eldritch Force Field": (
        "Phosis has a 4+ Invulnerable Save, 3+ against shooting. While joined to a friendly Thousand Sons Infantry unit, "
        "its models get a 5+ Invulnerable Save (or +1 to an existing one), never better than 3+ against shooting or 4+ in "
        "close combat; this may combine with Raptora benefits within those limits."),
    "Athanaeans (Amon)": "Amon always belongs to the Athanaeans and receives both its Cult Arcana and Cult Mastery.",
    "Psychic Powers (Amon)": "Amon selects both his psychic powers from the Telepathy discipline.",
    "Armour of Shades": ("2+ Armour Save. Amon receives a 5+ Cover Save even in open ground; any Cover Save he would "
                         "normally receive is improved by two steps (max 3+)."),
    "The Hidden One": (
        "While Amon is joined to a friendly Thousand Sons Infantry unit, it gains the protection of the Armour of Shades "
        "(5+ Cover Save in the open, existing Cover Saves +2 steps, max 3+); Amon and that unit gain Infiltrate. Not "
        "conferred to Terminator Armour, Bikes, Jetbikes or Jump Infantry."),
    "Master of the Hidden Orders": ("Instead of a Legion Command Squad, Amon may select an Ammitara Occult Intercession "
                                    "Cabal or a Legion Seeker Squad as his retinue (single HQ selection, no extra slot)."),
    "Pavoni (Hathor Maat)": "Hathor Maat always belongs to the Pavoni and receives both its Cult Arcana and Cult Mastery.",
    "Magister Templi of the Pavoni": "Hathor Maat selects both his psychic powers from the Biomancy discipline.",
    "Aetheric Refractor Field": "Hathor Maat has a 4+ Invulnerable Save (included in his profile).",
    "Pavoni Vitalist": (
        "Hathor Maat has Feel No Pain (5+). A friendly Thousand Sons Infantry unit he has joined also gains Feel No Pain "
        "(5+), or improves an existing Feel No Pain by one step (max 4+), until he leaves or is slain."),
    "Athanaeans (Sanakht)": "Sanakht always belongs to the Athanaeans and receives both its Cult Arcana and Cult Mastery.",
    "Blademaster of Prospero": ("Sanakht may re-roll one failed To Hit roll and one failed To Wound roll during each "
                                "Assault phase. No dice may be re-rolled more than once."),
    "Khenetai Retinue": ("Sanakht may select one Khenetai Occult Blade Cabal as his retinue (single HQ selection, no extra "
                         "slot)."),
    "Psyker (Mastery Level 1)": "This model is a Psyker with Psychic Mastery Level 1.",
    "Psyker (Mastery Level 2)": "This model is a Psyker with Psychic Mastery Level 2.",
    "Psyker (Mastery Level 3)": "This model is a Psyker with Psychic Mastery Level 3.",
    "Psychic Powers (Sanakht)": ("Sanakht knows only Mindsong of Blades; he does not select a psychic power from the "
                                 "normal Psychic Disciplines. Activating his Force Weapons does not count as invoking a "
                                 "psychic power."),
    "Psychic Brotherhood (Khenetai)": (
        "Assign the Cabal to one Prosperine Cult; it receives both the Cult Arcana and Cult Mastery of that Cult. It does "
        "not select a power from the normal Psychic Disciplines and knows only Mindsong of Blades. The Blademaster may "
        "select up to 50 points of permitted weapons and wargear from the Space Marine Armoury but may not replace his "
        "Paired Prosperine Force Blades."),
    "Psychic Brotherhood (Ammitara)": (
        "Assign the Cabal to one Prosperine Cult; it receives both the Cult Arcana and Cult Mastery of that Cult. It "
        "selects one psychic power from Divination or Telepathy and follows the normal rules for a Brotherhood of "
        "Psykers (Mastery Level 1). The Ammitara Fate may select up to 50 points of permitted weapons and wargear from "
        "the Space Marine Armoury."),
    "Narthecium (Hathor Maat)": "Hathor Maat additionally uses the normal Narthecium rules from the Legiones Astartes "
                                "Army List.",
    "Command Retinue (Thousand Sons)": ("This character may select one Legion Command Squad as his retinue. It does not "
                                        "occupy a separate Force Organisation slot."),
    # Primarchs (universal)
    "Primarch": (
        "Independent Character, Eternal Warrior, Fear, Fearless, Adamantium Will, Fleet, It Will Not Die and Master of the "
        "Legion; automatically passes Fear tests caused by another Primarch; has the named Legiones Astartes rule of his "
        "Legion. FIELDING A PRIMARCH: selected as a Lord of War; no more than one Primarch per army; normally only in "
        "armies of 2,000 points or more; only for a Detachment of his own Legion, never an Allied Detachment; must be the "
        "army's Warlord; counts towards the Master of the Legion limit; may not purchase wargear, Consul upgrades or other "
        "character upgrades unless his entry permits it."),
    "Supreme Commander": ("A Primarch must be the army's Warlord even though he is a Lord of War. He does not roll for or "
                          "select a normal Warlord Trait; any command ability is in his own entry."),
    "Sire of the Legion": (
        "A Primarch may only join units with the same named Legiones Astartes rule (or his own bodyguard/retinue). He counts "
        "as a member of his Legion for rules referring to friendly models of that Legion, but does not automatically gain "
        "the Legion Special Rules unless his profile says so."),
    "Primarch Retinue": ("A Primarch may select one Legion Honour Guard Squad (or a Legion-specific bodyguard where his "
                         "entry permits) as a retinue without occupying an additional selection. They need not deploy or "
                         "stay together."),
    "Primarchs and Transports": "A Primarch counts as two models for Transport Capacity.",
    "The Price of Failure": ("If an enemy Primarch is destroyed, the opposing player gains +1 Victory Point in addition to "
                             "any Victory Points for destroying that model or the enemy Warlord."),
    "The Clash of Demigods": (
        "At the start of any Assault phase, if two opposing Primarchs are within 12\" of one another (and neither is "
        "embarked), the active player's Primarch issues a Primarch Challenge. If accepted, both leave their units and fight "
        "a Primarch Duel at a suitable location until one is slain (the Challenger counts as charging in the first round; "
        "no other models may interfere; see Forces of the Legions for the full rules). If refused, the Challenger's player "
        "gains +2 Victory Points and the refusing Primarch may not attack the Challenger that Assault phase."),
    "Primarch Armour": ("Confers a 1+ Armour Save and a 4+ Invulnerable Save. A natural roll of 1 always fails; even AP1 "
                        "attacks merely impact the armour as normal."),
    "Daemon Primarchs": (
        "A Daemon Primarch is a separate version of that Primarch; an army may never include both forms. Unless stated "
        "otherwise it uses only its own rules, but counts as a Primarch for rules referring to Primarch models."),
    # Magnus
    "Horned Raiment": ("Counts as Primarch Armour. Shooting attacks against Magnus or a unit he has joined suffer -1 To "
                       "Hit (-2 for Blast weapons). No effect in close combat."),
    "Blade of Ahn-Nunurta": "A Master-crafted, Two-Handed Force Weapon.",
    "Arcane Litanies (Magnus)": "Once per battle, when Magnus suffers a Wound from Perils of the Warp, he may ignore it.",
    "Psyker - Mastery Level 4 (Magnus)": (
        "Magnus selects five psychic powers from Biomancy, Divination, Pyromancy, Telekinesis and Telepathy, from at least "
        "two different disciplines. Infernal Phoenix and Strands of Fate are always known and count towards the five. He "
        "counts as belonging to all five Prosperine Cults for army selection, but gains no Cult Arcana or Mastery. "
        "Psychic Supremacy: no more than two Blessings on himself at once, and no more than two ongoing powers affecting "
        "himself and/or the opposing Primarch."),
    "Lord of the Ether": ("Magnus may invoke up to four psychic powers each player turn, including multiple Witchfire "
                          "powers in one Shooting phase, but never the same power twice in a turn. Activating the Blade "
                          "of Ahn-Nunurta does not count against this limit."),
    "The Crimson King": ("Magnus may re-roll one failed Psychic Test each player turn. He may Deny the Witch against any "
                         "power whose Psyker or target is within 24\" of him."),
    "The Warp Bends to Magnus": ("Magnus ignores Leadership penalties from Disturbance in the Warp, and his own powers do "
                                 "not count towards Disturbance in the Warp for other friendly Psykers; powers of other "
                                 "friendly Psykers still count normally. He may also attempt to Deny the Witch at 18\" "
                                 "around him (see The Crimson King for the 24\" Deny the Witch)."),
    "Infernal Phoenix": "Witchfire - Beam. Range 24\", S8, AP1, Melta. Resolve using the normal rules for Beam powers.",
    "Strands of Fate": (
        "Malediction. One enemy non-Vehicle unit within 18\" and line of sight must pass a Leadership test each time it "
        "attempts to move, shoot or declare a charge until the beginning of Magnus' next turn; if failed, that action is "
        "lost for that phase."),
    "Sorcerous Duellist": ("During a Primarch Duel, at the beginning of each Assault phase Magnus may invoke a Blessing on "
                           "himself or a Malediction on the opposing Primarch (counts towards his four powers)."),
    "The Crimson King's Guard": (
        "Magnus may select a Legion Honour Guard Squad, Legion Terminator Command Squad or Sekhmet Terminator Cabal as his "
        "Primarch Retinue. An Honour Guard or Terminator Command Squad selected this way may become a Brotherhood of "
        "Psykers (Mastery Level 1) for +25 points: it is assigned a Prosperine Cult (Cult Arcana and Mastery) and selects "
        "one power from the Thousand Sons disciplines."),
    # Magnus, Shard of the Crimson King
    "Ethereal": (
        "Magnus has seven Wounds but no Toughness and no Armour or Invulnerable Save. Non-psychic shooting hits only on an "
        "unmodified 6 and wounds only on an unmodified 6; non-psychic Blast weapons cannot strike him. In close combat he is "
        "wounded on 6+ by normal weapons, 5+ by Power Weapons/Fists/Hammers, 2+ by Force Weapons (which may be activated "
        "normally). Psychic attacks ignore these limits and treat him as Toughness 7. Immune to Instant Death; Massive "
        "Wounds only from activated Force Weapons or psychic effects. No saves."),
    "Incorporeal Will": ("Magnus may never charge or Pursue; he fights normally if charged and may Consolidate. He may "
                         "never join a unit and no model may join him."),
    "The Crimson King Unbound": (
        "Mastery Level 5: choose six powers from Biomancy, Divination, Pyromancy, Telekinesis and Telepathy; he always knows "
        "Infernal Phoenix and Strands of Fate in addition. He may attempt up to five powers each player turn (each only "
        "once), and up to two Witchfire powers in one Shooting phase."),
    "Beyond the Prosperine Cults": ("Not assigned to a Prosperine Cult; counts as Thousand Sons for army selection and "
                                    "rules referring to friendly Thousand Sons models."),
    "Nothing to Bless": "Magnus may never be the target of a Blessing; his Blessings must target another friendly unit.",
    "Master of the Great Ocean": (
        "Magnus ignores Leadership penalties from Disturbance in the Warp and his powers do not count towards it for other "
        "Psykers. He may Deny the Witch against any power whose Psyker or target is within 24\" of him."),
    "Beyond the Perils of the Warp": ("Instead of suffering Perils of the Warp, Magnus gains one Instability Counter (-1 "
                                      "each to his next Warp Breath roll, then all are removed)."),
    "The Warp Breathes": (
        "At the beginning of each Thousand Sons turn roll a D6 (modified by Instability Counters): 1 or less - The Crimson "
        "King Fades (placed in Reserve, returns by Deep Strike; counts as destroyed if still in Reserve at the end); 2-5 - "
        "Reality Holds; 6+ - The Warp Ascendant (every Psyker on the battlefield, friendly or enemy, may re-roll failed "
        "Psychic Tests, but any double causes Perils even if the test succeeds or is re-rolled) until the next Thousand "
        "Sons turn. The Crimson King Fades does not trigger The Crimson King Shattered."),
    "The Crimson King Shattered": (
        "If Magnus is destroyed, every friendly non-Vehicle Thousand Sons unit suffers D3 Strength 4 AP- hits, then every "
        "friendly Thousand Sons Psyker or Brotherhood suffers Perils of the Warp (Independent Characters twice). This counts "
        "as one Signs and Portents event."),
    "Aetheric Blade": "A Master-crafted Force Weapon; Magnus resolves attacks with it at Strength 7.",
    # Rites of War
    "The Axis of Dissolution": (
        "EFFECTS - The Alembic of Adamant: Thousand Sons units automatically pass Morale and Pinning tests while within 6\" "
        "of an Objective (without Objectives, nominate one terrain feature outside the enemy deployment zone). The Caustic "
        "of Grace: Thousand Sons Infantry may enter Overwatch even if they moved (but did not Advance). The Transition of "
        "Vitriol: re-roll failed To Hit and To Wound (Armour Penetration against vehicles) against units Falling Back.\n"
        "LIMITATIONS - Every Troops choice must be taken at its maximum unit size. No more Tank or Flyer vehicles than "
        "Infantry units. No Fortification."),
    "The Guard of the Crimson King": (
        "EFFECTS - Astral Warfare: the first two powers successfully invoked by Thousand Sons Psykers each player turn are "
        "ignored for Disturbance in the Warp. Wreathed in Lightning: all Thousand Sons units entirely in Terminator Armour "
        "gain Teleportation Transponders for free; Independent Characters may buy them for +10 in any armour; units arriving "
        "this way gain Fear and re-roll Invulnerable Saves of 1 until the next Thousand Sons turn. Initiates of the Scarab: "
        "Sekhmet Terminator Cabals may be Troops and must fulfil the compulsory Troops. The Bidding of the Crimson King: "
        "Magnus may fulfil a compulsory HQ and does not occupy a Lord of War selection.\nLIMITATIONS - The Warlord must be "
        "Magnus, Ahzek Ahriman or a Thousand Sons Praetor (a Praetor Warlord may be upgraded to Mastery Level 3 for +25). "
        "No more Vehicle units than Thousand Sons units. No Allied Detachment or Fortification."),
    "The Fellowships of Prospero": (
        "EFFECTS - Circles of Initiates: a Legion Tactical Squad of 20 models may purchase Brotherhood of Psykers (Mastery "
        "Level 1) for +25 (one power from the Thousand Sons disciplines, plus its Cult Mastery). Fellowship Veterans: "
        "Veteran and Terminator Squads buy Brotherhood of Psykers for +15 instead of +25. Magister Templi: each Thousand "
        "Sons turn the Warlord may let one Brotherhood within 12\" use his Leadership for Psychic Tests. Order of the Cults: "
        "every Brotherhood must share a Cult with at least one Thousand Sons Independent Character.\nLIMITATIONS - The "
        "Warlord must be a Thousand Sons Psyker. At least two Psychic Brotherhoods. No more than one Fast Attack choice. No "
        "Allied Detachment."),
}
for n, (full, text, _d) in CULTS.items():
    TS_RULES[full] = text
for d in DISCIPLINES:
    TS_RULES[f"Discipline: {d}"] = f"Psychic powers are selected from the {d} discipline (ProHammer Classic)."

TS_WEAPONS = {
    "Prosperine Force Weapon": ("-", "User", "-", "Power Weapon, Force"),
    "Aether-fire Cannon": ('36"', "7", "2", "Heavy 1, Blast, Gets Hot, Soul Blaze"),
    "Paired Prosperine Force Blades": ("-", "User", "-", "Power Weapon, Force, +1 Attack (included)"),
    "Osiron Force Blade": ("-", "x2", "-", "Dreadnought Close Combat Weapon, Force"),
    "Black Staff of Ahriman": ("-", "User", "-", "Power Weapon, Force, Master-crafted"),
    "Blade of Ahn-Nunurta": ("-", "User", "-", "Power Weapon, Force, Master-crafted, Two-Handed"),
    "Infernal Phoenix": ('24"', "8", "1", "Witchfire, Beam, Melta"),
    "Aetheric Blade": ("-", "7", "-", "Power Weapon, Force, Master-crafted"),
}
TS_WEAPON_RULES = {
    "Prosperine Force Weapon": ["Prosperine Force Weapon", "Force"], "Aether-fire Cannon": ["Aether-fire Cannon",
                                                                                           "Gets Hot", "Soul Blaze"],
    "Paired Prosperine Force Blades": ["Paired Prosperine Force Blades", "Prosperine Force Weapon"],
    "Osiron Force Blade": ["Osiron Force Blade", "Force"], "Black Staff of Ahriman": ["Black Staff of Ahriman"],
    "Blade of Ahn-Nunurta": ["Blade of Ahn-Nunurta", "Force"], "Aetheric Blade": ["Aetheric Blade", "Force"],
}
TS_WARGEAR = {
    "Arcane Litanies": TS_RULES["Arcane Litanies"],
    "Asphyx Shells": TS_RULES["Asphyx Shells"],
    "Teleportation Transponders": TS_RULES["Teleportation Transponders"],
    "Prosperine Aether-Disc": TS_RULES["Prosperine Aether-Disc"],
    "Eldritch Force Field": TS_RULES["Eldritch Force Field"],
    "Armour of Shades": TS_RULES["Armour of Shades"],
    "Aetheric Refractor Field": TS_RULES["Aetheric Refractor Field"],
    "Horned Raiment": TS_RULES["Horned Raiment"],
}


def register():
    """Add the Thousand Sons rules, weapons and wargear to the shared data before anything is built."""
    for n in ["Legion Tactical Squad", "Legion Assault Squad", "Legion Breacher Siege Squad"]:
        L2.NOT_LINE_UNDER[n].append("The Guard of the Crimson King")
    ARMY_RULES.update(TS_RULES)
    WEAPON_PROFILES.update(TS_WEAPONS)
    for n in TS_WEAPONS:
        WEAPONS[n] = [n]
    WEAPON_RULES.update(TS_WEAPON_RULES)
    for n, t in TS_WARGEAR.items():
        WARGEAR[n] = (t, [])


# ------------------------------------------------------------ building blocks
def cult_choice(key, required=True, fixed=None, only_ts=False):
    gid = uid("grp", key, "cult")
    ents = []
    for n, (full, _t, disc) in CULTS.items():
        eid = uid("cult", key, n)
        ents.append(entry(eid, n, infolinks=rules_links([full, "Cult Mastery"], key=eid),
                          constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)]))
    cons = [constraint(uid(gid, "max"), "max", 1, auto=True)]
    mods = []
    if required:
        none = all_of(*[cond(e.get("id"), "parent", "lessThan", 1) for e in ents])
        mods.append(modifier("add", "error", "Choose a Prosperine Cult.", groups=[none],
                             conds=[ts()] if only_ts else None))
    return group(gid, "Prosperine Cult", entries=ents, constraints=cons, mods=mods)


def discipline_choice(key, options=DISCIPLINES, required=True, title="Psychic Discipline"):
    gid = uid("grp", key, "discipline")
    ents = [entry(uid("disc", key, d), d, infolinks=rules_links([f"Discipline: {d}"], key=uid("disc", key, d)),
                  constraints=[constraint(uid("disc", key, d, "max"), "max", 1, auto=True)]) for d in options]
    cons = [constraint(uid(gid, "max"), "max", 1, auto=True)]
    mods = []
    if required:
        none = all_of(*[cond(e.get("id"), "parent", "lessThan", 1) for e in ents])
        mods.append(modifier("add", "error", f"Choose a {title}.", groups=[none]))
    return group(gid, title, entries=ents, constraints=cons, mods=mods)


def brotherhood(key, cost=25, fellowships_cost=None, visible_if=None, any_discipline=False):
    """'May purchase the Brotherhood of Psykers special rule' - chooses its Cult (and so its Discipline).
    any_discipline: the unit picks its power from any Thousand Sons discipline instead of its Cult's one."""
    eid = uid("brotherhood", key)
    mods = []
    if fellowships_cost is not None:
        mods.append(modifier("set", PTS, fellowships_cost, conds=[rite("The Fellowships of Prospero")]))
    e = entry(eid, "Psychic Brotherhood (Brotherhood of Psykers, Mastery Level 1)", cost=cost, mods=mods,
              constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
              infolinks=rules_links(["Brotherhood of Psychers", "Psychic Brotherhoods", "Cult Mastery"], key=eid),
              groups=[cult_choice(eid)] + ([discipline_choice(eid)] if any_discipline else []))
    ts_only(e, uid(eid, "max"))
    if visible_if:
        add_mods(e, [modifier("set", "hidden", "true", groups=[visible_if[0]]),
                     modifier("set", uid(eid, "max"), 0, groups=[visible_if[1]])])
    return e


def ts_option(key, name, cost, hide=None, per_model_unit=None, item=None):
    """Optional Thousand Sons wargear purchase (hidden unless Thousand Sons)."""
    eid = uid("ts-opt", key, name)
    mods = [modifier("set", "hidden", "true", conds=[not_ts()]),
            modifier("set", uid(eid, "max"), 0, conds=[not_ts()])]
    if hide:
        mods += [modifier("set", "hidden", "true", groups=[any_of(*hide)]),
                 modifier("set", uid(eid, "max"), 0, groups=[any_of(*hide)])]
    cost_val = cost
    if per_model_unit:
        cost_val = 0
        mods.append(modifier("increment", PTS, cost, repeats=[repeat("model", per_model_unit, 1)]))
    return entry(eid, name, cost=cost_val, mods=mods, constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                 links=[gear(eid, item or name)])


def unique(eid):
    return constraint(uid(eid, "unique"), "max", 1, scope="roster", deep=True)


def clone(e, salt, strip_cats=True, new_name=None):
    """Deep copy of an entry with every internal id renamed (for retinue copies of normal units)."""
    c = copy.deepcopy(e)
    ids = {x.get("id") for x in c.iter() if x.get("id")}
    for x in c.iter():
        for a in ("id", "targetId", "childId", "scope", "field", "defaultSelectionEntryId", "value"):
            v = x.get(a)
            if v in ids:
                x.set(a, uid(salt, v))
    if strip_cats:
        cl = c.find("categoryLinks")
        if cl is not None:
            c.remove(cl)
    if new_name:
        c.set("name", new_name)
    return c


def retinue_links(key, entries, title="Retinue (no Force Organisation slot)"):
    gid = uid("grp", key, "retinue")
    RETINUE_SHARED.extend(e for e in entries if e not in RETINUE_SHARED)
    return group(gid, title, links=[link(uid("link", gid, e.get("id")), e.get("id"), e.get("name")) for e in entries],
                 constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


# ------------------------------------------------------------ units
def sekhmet(key="Sekhmet Terminator Cabal", root=True):
    name = "Sekhmet Terminator Cabal"
    u = uid("unit", key)
    tid = uid("model", u, "Sekhmet Terminator")
    iid = uid("model", u, "Sekhmet Inceptor")
    prof = lambda n, a, ld: unit_profile(u, n, "Infantry" + (" (Character)" if "Inceptor" in n else ""),
                                         5, 4, 4, 4, 2, 3, a, ld, "2+/4+")
    combis = [("Combi-Flamer", 10), ("Combi-Grenade Launcher", 10), ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15),
              ("Combi-Volkite Charger", 10)]

    cc = [("Power Fist", 0), ("Chainfist", 10)]
    heavies = [("Heavy Flamer", 10), ("Plasma Blaster", 15), ("Reaper Autocannon", 20)]

    def weap(mid):
        return [slot(mid, "Replace Prosperine Force Weapon", "Prosperine Force Weapon", cc),
                slot(mid, "Replace Foeblaster Boltgun", "Foeblaster Boltgun", combis)]
    tmin, tmax = uid(tid, "min"), uid(tid, "max")
    terms = entry(tid, "Sekhmet Terminator", typ="model", cost=60,
                  mods=[modifier("decrement", tmin, 1, conds=[cond(iid, u, "atLeast", 1)]),
                        modifier("decrement", tmax, 1, conds=[cond(iid, u, "atLeast", 1)])],
                  constraints=[constraint(tmin, "min", 5, auto=True), constraint(tmax, "max", 10, auto=True)],
                  profiles=[prof("Sekhmet Terminator", 2, 9)],
                  links=[gear(tid, k) for k in ["Cataphractii Terminator Armour", "Prosperine Force Weapon",
                                                "Foeblaster Boltgun"]])
    inc = entry(iid, "Sekhmet Inceptor", typ="model", cost=80, constraints=[constraint(uid(iid, "max"), "max", 1)],
                profiles=[prof("Sekhmet Inceptor", 3, 10)], links=[gear(iid, "Cataphractii Terminator Armour")],
                groups=weap(iid) + [take(iid, "Inceptor Wargear", [("Grenade Harness", 10)])])
    heavy, hmx = pool(u, "Heavy Weapons (up to two per five models, replace Foeblaster Boltgun)", u, heavies, 0,
                      every=5)
    # two per five: increment again with the same repeat
    add_mods(heavy, [modifier("increment", hmx, 1, repeats=[repeat("model", u, 5)])])
    tp = ts_option(u, "Teleportation Transponders (entire Cabal)", 15, item="Teleportation Transponders")
    add_mods(tp, [modifier("set", PTS, 0, conds=[rite("The Guard of the Crimson King")])])
    cats = [foc(ELITES, "Elites", u)] if root else []
    mods = [modifier("set", "hidden", "true", conds=[not_ts()])]
    if root:
        mods += [modifier("set-primary", "category", TROOPS, conds=[rite("The Guard of the Crimson King")]),
                 modifier("remove", "category", ELITES, conds=[rite("The Guard of the Crimson King")]),
                 modifier("add", "category", gs.CAT_LINE, conds=[rite("The Guard of the Crimson King")])]
    if root:
        mods.append(modifier("increment", uid(u, "force-max"), 5, conds=[rite("The Guard of the Crimson King")]))
    e = entry(u, name, typ="unit", cost=0, cats=cats, mods=mods,
              constraints=[constraint(uid(u, "force-max"), "max", 1, scope="force", deep=True)] if root else [],
              infolinks=rules_links(["Legiones Astartes (Thousand Sons)", "Fearless", "Brotherhood of Psychers",
                                     "Scarab Occult", "Prosperine Force Weapon"], key=u),
              entries=[terms, inc, tp],
              groups=[cult_choice(u), discipline_choice(u),
                      model_swaps(u, "Sekhmet Terminators: replace Prosperine Force Weapon (any number)", u, [tid], cc),
                      model_swaps(u, "Sekhmet Terminators: replace Foeblaster Boltgun (any number)", u, [tid], combis,
                                  minus=[W(n) for n, _ in heavies]),
                      heavy,
                      transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                        "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                                 orbital=False)])
    return e


def khenetai(key="Khenetai Occult Blade Cabal", root=True):
    name = "Khenetai Occult Blade Cabal"
    u = uid("unit", key)
    bid, mid = uid("model", u, "Khenetai Blade"), uid("model", u, "Khenetai Blademaster")
    kit = ["Power Armour", "Paired Prosperine Force Blades", "Frag Grenades"]
    bmin, bmax = uid(bid, "min"), uid(bid, "max")
    blades = entry(bid, "Khenetai Blade", typ="model", cost=38,
                   mods=[modifier("decrement", bmin, 1, conds=[cond(mid, u, "atLeast", 1)]),
                         modifier("decrement", bmax, 1, conds=[cond(mid, u, "atLeast", 1)])],
                   constraints=[constraint(bmin, "min", 5, auto=True), constraint(bmax, "max", 10, auto=True)],
                   profiles=[unit_profile(u, "Khenetai Blade", "Infantry", 5, 4, 4, 4, 1, 4, 3, 9, "3+")],
                   links=[gear(bid, k) for k in kit])
    master = entry(mid, "Khenetai Blademaster", typ="model", cost=53, constraints=[constraint(uid(mid, "max"), "max", 1)],
                   profiles=[unit_profile(u, "Khenetai Blademaster", "Infantry (Character)", 5, 4, 4, 4, 1, 5, 4, 10,
                                          "3+")],
                   links=[gear(mid, k) for k in kit], groups=[L.sgt_extra_capped(mid, u, 10, skip=())])
    pistols, _ = pool(u, "Pistols (1 per 5 models)", u, [("Hand Flamer", 5), ("Plasma Pistol", 15)], 0, every=5)
    cats = [foc(ELITES, "Elites", u)] if root else []
    return entry(u, name, typ="unit", cost=0 if root else 0, cats=cats,
                 mods=[modifier("set", "hidden", "true", conds=[not_ts()])],
                 constraints=[constraint(uid(u, "force-max"), "max", 1, scope="force", deep=True)] if root else [],
                 infolinks=rules_links(["Legiones Astartes (Thousand Sons)", "Brotherhood of Psychers",
                                        "Psychic Brotherhood (Khenetai)", "Mindsong of Blades",
                                        "Paired Prosperine Force Blades", "Cult Mastery"], key=u),
                 entries=[blades, master, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[cult_choice(u), pistols])


def ammitara(key="Ammitara Occult Intercession Cabal", root=True):
    name = "Ammitara Occult Intercession Cabal"
    u = uid("unit", key)
    iid, fid = uid("model", u, "Ammitara Intercessor"), uid("model", u, "Ammitara Fate")
    kit = ["Recon Armour", "Sniper Rifle", "Bolt Pistol", "Combat Blade", "Frag Grenades"]
    combis = [("Combi-Flamer", 10), ("Combi-Volkite Charger", 10), ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15)]
    inter = entry(iid, "Ammitara Intercessor", typ="model", cost=20,
                  constraints=[constraint(uid(iid, "min"), "min", 4), constraint(uid(iid, "max"), "max", 9)],
                  profiles=[unit_profile(u, "Ammitara Intercessor", "Infantry", 4, 5, 4, 4, 1, 4, 1, 8, "4+")],
                  links=[gear(iid, k) for k in kit])
    # the Fate's Bolt Pistol / Combat Blade can be exchanged through his Armoury
    fate = entry(fid, "Ammitara Fate", typ="model", constraints=[constraint(uid(fid, "min"), "min", 1),
                                                                  constraint(uid(fid, "max"), "max", 1)],
                 profiles=[unit_profile(u, "Ammitara Fate", "Infantry (Character)", 4, 5, 4, 4, 1, 4, 2, 9, "4+")],
                 links=[gear(fid, k) for k in ["Recon Armour", "Sniper Rifle", "Frag Grenades"]],
                 groups=[pa_armoury(fid, u, 10, slots=["Bolt Pistol", "Combat Blade"])])
    spec_opts = [("Meltagun", 10), ("Plasma Gun", 15)]
    specials, _ = pool(u, "Special Weapons (up to two models, replace Sniper Rifle)", u, spec_opts, 2)
    combi_swaps = model_swaps(u, "Any model: replace Sniper Rifle (any number)", u, [iid, fid], combis,
                              minus=[W(n) for n, _ in spec_opts])
    cats = [foc(FA, "Fast Attack", u)] if root else []
    return entry(u, name, typ="unit", cost=135 - 4 * 20, cats=cats,
                 mods=[modifier("set", "hidden", "true", conds=[not_ts()])],
                 constraints=[constraint(uid(u, "force-max"), "max", 1, scope="force", deep=True)] if root else [],
                 infolinks=rules_links(["Legiones Astartes (Thousand Sons)", "Brotherhood of Psychers",
                                        "Psychic Brotherhood (Ammitara)", "Cult Mastery", "Scout", "Infiltrate",
                                        "Move Through Cover", "Stealth"], key=u),
                 entries=[fate, inter, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[cult_choice(u), discipline_choice(u, ["Divination", "Telepathy"]), combi_swaps, specials,
                         L.one_each(u, "Squad Equipment", [("Nuncio Vox", 10)])])


def castellax_achea():
    name = "Castellax-Achea Maniple"
    u = uid("unit", name)
    mid = uid("model", u, "Castellax-Achea")
    m = entry(mid, "Castellax-Achea", typ="model", cost=130,
              constraints=[constraint(uid(mid, "min"), "min", 1), constraint(uid(mid, "max"), "max", 3)],
              profiles=[unit_profile(u, "Castellax-Achea", "Monstrous Creature", 3, 3, 5, 6, 3, 3, 2, 8, "3+/5+")],
              links=[gear(mid, "Dreadnought Close Combat Weapon"), gear(mid, "Twin-linked Bolter"),
                     gear(mid, "Aether-fire Cannon")])
    for lk in m.find("entryLinks"):
        if lk.get("name") == "Dreadnought Close Combat Weapon":
            for c in lk.iter("constraint"):
                c.set("value", "2")
    return entry(u, name, typ="unit", cats=[foc(ELITES, "Elites", u)],
                 mods=[modifier("set", "hidden", "true", conds=[not_ts()])],
                 constraints=[constraint(uid(u, "force-max"), "max", 1, scope="force", deep=True)],
                 infolinks=rules_links(["Fearless", "Aetheric Command Matrix", "Psychic Conduit", "Aetheric Shielding",
                                        "Thousand Sons Construct"], key=u),
                 entries=[m],
                 groups=[model_swaps(u, "Any Castellax-Achea: replace Twin-linked Bolter", u, [mid],
                                     [("Heavy Flamer", 5)])])


def osiron():
    name = "Contemptor-Osiron Dreadnought"
    u = uid("unit", name)
    prof = walker_profile(u, name, 5, 5, 6, 13, 12, 10, 4, 3)
    ml2 = uid(u, "ml2")
    ml2e = entry(ml2, "Psyker (Mastery Level 2)", cost=25, constraints=[constraint(uid(ml2, "max"), "max", 1)])
    return entry(u, name, typ="unit", cost=225, cats=[foc(ELITES, "Elites", u)],
                 mods=[modifier("set", "hidden", "true", conds=[not_ts()])],
                 constraints=[constraint(uid(u, "force-max"), "max", 1, scope="force", deep=True)],
                 profiles=[prof],
                 infolinks=rules_links(["Atomantic Shielding", "Fleet", "Psyker", "Psychic Dreadnought",
                                        "Aetheric Battle-Engine", "Osiron Force Blade"], key=u),
                 links=[gear(u, "Osiron Force Blade"), gear(u, "Smoke Launchers"), gear(u, "Searchlight")],
                 entries=[ml2e],
                 groups=[slot(u, "Force Blade built-in weapon (replace Twin-linked Bolter)", "Twin-linked Bolter",
                              [("Heavy Flamer", 10), ("Graviton Gun", 15), ("Meltagun", 15)]),
                         slot(u, "Replace Dreadnought Close Combat Weapon", "Dreadnought Close Combat Weapon",
                              [("Twin-linked Heavy Bolter", 0), ("Multi-Melta", 0), ("Twin-linked Autocannon", 10),
                               ("Plasma Cannon", 10), ("Twin-linked Volkite Culverin", 15),
                               ("Kheres Assault Cannon", 15), ("Twin-linked Lascannon", 25)]),
                         take(u, "Upgrades", [("Extra Armour", 5)]),
                         discipline_choice(u)])


def numerologist():
    name = "Numerologist Cabal"
    u = uid("unit", name)
    nid, lid = uid("model", u, "Numerologist"), uid("model", u, "Life Ward")
    num = entry(nid, "Numerologist", typ="model", constraints=[constraint(uid(nid, "min"), "min", 1),
                                                                 constraint(uid(nid, "max"), "max", 1)],
                profiles=[unit_profile(u, "Numerologist", "Infantry (Character)", 5, 5, 4, 4, 2, 4, 2, 9, "2+")],
                infolinks=rules_links(["Psyker", "Battlesmith (Techmarine)", "Psy-Synchronicity"], key=nid),
                links=[gear(nid, k) for k in ["Artificer Armour", "Servo-Arm", "Frag Grenades"]],
                groups=[slot(nid, "Replace Chainsword", "Chainsword", [("Power Weapon", 10),
                                                                       ("Prosperine Force Weapon", 20),
                                                                       ("Thunder Hammer", 20)]),
                        slot(nid, "Replace Bolt Pistol", "Bolt Pistol", [("Volkite Charger", 5), ("Flamer", 5),
                                                                         ("Plasma Gun", 15), ("Meltagun", 15),
                                                                         ("Graviton Gun", 15)])])
    wards = entry(lid, "Life Ward", typ="model", cost=15,
                  constraints=[constraint(uid(lid, "min"), "min", 4), constraint(uid(lid, "max"), "max", 9)],
                  profiles=[unit_profile(u, "Life Ward", "Infantry", 4, 4, 4, 4, 1, 4, 2, 8, "3+")],
                  links=[gear(lid, k) for k in ["Power Armour", "Bolt Pistol", "Chainsword", "Frag Grenades"]])
    heavy, _ = pool(u, "Life Ward weapons (1 per 5 models, replace Bolt Pistol)", u,
                    [("Rotor Cannon", 5), ("Volkite Caliver", 10)], 0, every=5)
    return entry(u, name, typ="unit", cost=130 - 4 * 15, cats=[foc(ELITES, "Elites", u)],
                 mods=[modifier("set", "hidden", "true", conds=[not_ts()])],
                 constraints=[constraint(uid(u, "force-max"), "max", 1, scope="force", deep=True)],
                 infolinks=rules_links(["Legiones Astartes (Thousand Sons)", "Order of Ruin"], key=u),
                 entries=[num, wards, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
                 groups=[cult_choice(u), heavy,
                         L.one_each(u, "Squad Equipment", [("Legion Vexilla", 10), ("Nuncio Vox", 10)])])


def named_character(name, cost, stats, kit, rules_, retinue=None, master=True, min_points=None, extra_groups=()):
    u = uid("unit", name)
    cats = [foc(HQ, "HQ", u), category_link(gs.CAT_COMMANDER, "Compulsory HQ Eligible", key=u)]
    if master:
        cats.append(category_link(gs.CAT_MASTER, "Master of the Legion", key=u))
    mods = [modifier("set", "hidden", "true", conds=[not_ts()])]
    if min_points:
        mods.append(modifier("add", "error", f"{name} may only be included in an army of {min_points:,} points or more.",
                             conds=[cond("any", "roster", "lessThan", min_points, field=PTS, deep=False)]))
    groups = [take(u, "Wargear", [("Krak Grenades", 2)])] + list(extra_groups)
    if retinue:
        groups.append(retinue)
    return entry(u, name, typ="unit", cost=cost, cats=cats, mods=mods, constraints=[unique(u)],
                 profiles=[unit_profile(u, name, "Infantry (Character)", *stats)],
                 infolinks=rules_links(["Legiones Astartes (Thousand Sons)", "Independent Character"] +
                                       (["Master of the Legion"] if master else []) + rules_, key=u),
                 links=[gear(u, k) for k in kit], groups=groups)


def command_squad_for(char_key, char_id, extra_entries=()):
    cs = L2.command_squad(char_key, char_id)
    if extra_entries:
        add_to(cs, "selectionEntries", list(extra_entries))
    return cs


def characters():
    out = []
    # Ahzek Ahriman
    a = uid("unit", "Ahzek Ahriman")
    cabal = uid("ahriman-cabal")
    cs = command_squad_for("ahriman", a, [entry(
        cabal, "Ahriman's Cabal (Brotherhood of Psykers, Mastery Level 2, Corvidae)", cost=50,
        constraints=[constraint(uid(cabal, "max"), "max", 1, auto=True)],
        infolinks=rules_links(["Ahriman's Cabal", "Brotherhood of Psychers", "Corvidae - Precognitive Strike",
                               "Cult Mastery"], key=cabal))])
    out.append(named_character("Ahzek Ahriman", 210, (5, 5, 4, 4, 3, 5, 3, 10, "2+/4+"),
                               ["Artificer Armour", "Iron Halo", "Black Staff of Ahriman", "Bolt Pistol",
                                "Frag Grenades"],
                               ["Psyker", "Psyker (Mastery Level 3)", "Corvidae (Ahriman)", "Corvidae - Precognitive Strike", "Cult Mastery",
                                "Chief Librarian", "Ahriman's Cabal"],
                               retinue=retinue_links("ahriman", [cs]), min_points=1500))
    mark_brotherhood(cs, cabal)
    # Phosis T'Kar
    p = uid("unit", "Phosis T'Kar")
    out.append(named_character("Phosis T'Kar", 205, (5, 5, 4, 4, 2, 5, 3, 10, "3+/4+"),
                               ["Power Armour", "Eldritch Force Field", "Prosperine Force Weapon", "Bolter",
                                "Frag Grenades"],
                               ["Psyker", "Psyker (Mastery Level 2)", "Raptora (Phosis)", "Raptora - Kine Shields", "Cult Mastery",
                                "Magister of the Raptora", "Command Retinue (Thousand Sons)"],
                               retinue=retinue_links("phosis", [command_squad_for("phosis", p)])))
    # Magistus Amon
    am = uid("unit", "Magistus Amon, the Hidden")
    amon_amm = ammitara("amon-ammitara", root=False)
    add_to(amon_amm, "categoryLinks", [category_link(gs.CAT_BROTHERHOOD, "Psychic Brotherhood",
                                                     key=amon_amm.get("id"))])
    amon_ret = [command_squad_for("amon", am), amon_amm,
                clone(L2.seeker_squad(), "amon-seekers")]
    out.append(named_character("Magistus Amon, the Hidden", 185, (5, 5, 4, 4, 2, 5, 3, 10, "2+"),
                               ["Armour of Shades", "Prosperine Force Weapon", "Bolt Pistol", "Frag Grenades"],
                               ["Psyker", "Psyker (Mastery Level 2)", "Athanaeans (Amon)", "Athanaeans - Discipline of the Mind", "Cult Mastery",
                                "Psychic Powers (Amon)", "The Hidden One", "Master of the Hidden Orders"],
                               retinue=retinue_links("amon", amon_ret), min_points=1500))
    # Hathor Maat
    h = uid("unit", "Hathor Maat")
    out.append(named_character("Hathor Maat", 190, (5, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
                               ["Artificer Armour", "Aetheric Refractor Field", "Prosperine Force Weapon",
                                "Bolt Pistol", "Narthecium", "Reductor", "Frag Grenades"],
                               ["Psyker", "Psyker (Mastery Level 2)", "Pavoni (Hathor Maat)", "Pavoni - Quickblood",
                                "Cult Mastery", "Magister Templi of the Pavoni", "Pavoni Vitalist",
                                "Narthecium (Hathor Maat)", "Command Retinue (Thousand Sons)"],
                               retinue=retinue_links("hathor", [command_squad_for("hathor", h)])))
    # Sanakht (no Master of the Legion)
    san_kh = khenetai("sanakht-khenetai", root=False)
    add_to(san_kh, "categoryLinks", [category_link(gs.CAT_BROTHERHOOD, "Psychic Brotherhood", key=san_kh.get("id"))])
    out.append(named_character("Sanakht", 195, (7, 5, 4, 4, 3, 6, 4, 10, "2+/5+"),
                               ["Artificer Armour", "Refractor Field", "Paired Prosperine Force Blades",
                                "Frag Grenades"],
                               ["Psyker", "Psyker (Mastery Level 1)", "Athanaeans (Sanakht)",
                                "Athanaeans - Discipline of the Mind", "Cult Mastery", "Psychic Powers (Sanakht)",
                                "Blademaster of Prospero", "Mindsong of Blades", "Khenetai Retinue"],
                               retinue=retinue_links("sanakht", [san_kh]),
                               master=False))
    return out


MAGNUS = uid("unit", "Magnus the Red, the Crimson King")
MAGNUS_SHARD = uid("unit", "Magnus, Shard of the Crimson King")


def primarch_mods(u, other=None, chosen_ok=True):
    mods = [modifier("set", "hidden", "true", conds=[not_ts()])]
    small = [cond("any", "roster", "lessThan", 2000, field=PTS, deep=False)]
    if chosen_ok:
        mods.append(modifier("add", "error", "A Primarch may normally only be included in an army of 2,000 points or "
                                             "more (1,500 with the Primarch's Chosen Rite of War).",
                             conds=small + [cond(rite_id("Primarch's Chosen"), "force", "lessThan", 1)]))
    if other:
        mods.append(modifier("add", "error", "An army may never include both the mortal and the Shard form of Magnus.",
                             conds=[cond(other, "roster", "atLeast", 1)]))
    return mods


def magnus_retinue():
    hg = L2.honour_guard("magnus")
    tcs = L2.terminator_command_squad("magnus")
    for e in (hg, tcs):
        bro = brotherhood(e.get("id") + "magnus", any_discipline=True)
        add_to(e, "selectionEntries", [bro])
        mark_brotherhood(e, bro.get("id"))
    sek = sekhmet("magnus-sekhmet", root=False)
    return retinue_links("magnus", [hg, tcs, sek], title="Primarch Retinue")


def magnus():
    u = MAGNUS
    mods = primarch_mods(u, other=MAGNUS_SHARD)
    guard = [cond(rite_id("The Guard of the Crimson King"), "force", "atLeast", 1)]
    mods += [modifier("set-primary", "category", HQ, conds=guard), modifier("remove", "category", LOW, conds=guard),
             modifier("add", "category", gs.CAT_COMMANDER, conds=guard),
             modifier("add", "category", gs.CAT_COMMANDER,
                      conds=[cond(rite_id("Primarch's Chosen"), "force", "atLeast", 1)])]
    return entry(u, "Magnus the Red, the Crimson King", typ="unit", cost=550, mods=mods,
                 cats=[foc(LOW, "Lords of War", u), category_link(gs.CAT_MASTER, "Master of the Legion", key=u),
                       category_link(gs.CAT_PRIMARCH, "Primarch", key=u)],
                 constraints=[unique(u)],
                 profiles=[unit_profile(u, "Magnus the Red", "Infantry (Character)", 7, 7, 7, 7, 7, 6, 4, 10, "1+/4+")],
                 infolinks=rules_links(["Primarch", "Supreme Commander", "Sire of the Legion", "Primarch Retinue",
                                        "Primarchs and Transports", "The Price of Failure", "The Clash of Demigods",
                                        "Legiones Astartes (Thousand Sons)", "Psyker - Mastery Level 4 (Magnus)",
                                        "Lord of the Ether", "The Crimson King", "The Warp Bends to Magnus",
                                        "Strands of Fate", "Sorcerous Duellist", "The Crimson King's Guard",
                                        "Primarch Armour", "Arcane Litanies (Magnus)"], key=u),
                 links=[gear(u, "Horned Raiment"), gear(u, "Blade of Ahn-Nunurta"), gear(u, "Infernal Phoenix")],
                 groups=[magnus_retinue()])


def magnus_shard():
    u = MAGNUS_SHARD
    return entry(u, "Magnus, Shard of the Crimson King", typ="unit", cost=675, mods=primarch_mods(u, other=MAGNUS),
                 cats=[foc(LOW, "Lords of War", u), category_link(gs.CAT_MASTER, "Master of the Legion", key=u),
                       category_link(gs.CAT_PRIMARCH, "Primarch", key=u)],
                 constraints=[unique(u)],
                 profiles=[unit_profile(u, "Magnus, Shard of the Crimson King", "Monstrous Creature (Character)",
                                        7, 7, 7, "*", "7*", 6, 5, 10, "-")],
                 infolinks=rules_links(["Daemon Primarchs", "Fear", "Fearless", "Master of the Legion", "Ethereal",
                                        "Incorporeal Will", "The Crimson King Unbound", "Strands of Fate",
                                        "Beyond the Prosperine Cults", "Nothing to Bless", "Master of the Great Ocean",
                                        "Beyond the Perils of the Warp", "The Warp Breathes",
                                        "The Crimson King Shattered"], key=u),
                 links=[gear(u, "Aetheric Blade"), gear(u, "Infernal Phoenix")])


# ------------------------------------------------------------ changes to existing entries
def ic_additions(key, e, praetor):
    """Thousand Sons options on a Praetor / Centurion."""
    uid_ = e.get("id")
    grp = uid("grp", key, "ts")
    tp = ts_option(key, "Teleportation Transponders", 10)
    add_mods(tp, [modifier("set", "hidden", "true", groups=[all_of(
        *[lacks(W(n), uid_) for n in TDA], cond(rite_id("The Guard of the Crimson King"), "force", "lessThan", 1))])])
    disc = ts_option(key, "Prosperine Aether-Disc", 30,
                     hide=has_tda(uid_) + [has(W("Jump Pack"), uid_), has(W("Space Marine Bike"), uid_)])
    opts = [ts_option(key, "Arcane Litanies", 10), ts_option(key, "Asphyx Shells", 10), tp, disc]
    if praetor:
        ml3 = entry(uid(key, "ml3"), "Mastery Level 3 (Warlord, The Guard of the Crimson King)", cost=25,
                    constraints=[constraint(uid(key, "ml3", "max"), "max", 1, auto=True)],
                    mods=[modifier("set", "hidden", "true", conds=[cond(rite_id("The Guard of the Crimson King"),
                                                                            "force", "lessThan", 1)])])
        opts.append(ml3)
    g = group(grp, "Thousand Sons Wargear", entries=opts)
    ts_only(g)
    # Sorcerers of Prospero: psyker and discipline
    exclude = [] if praetor else [cond(L.consul_id(c), uid_, "atLeast", 1) for c in ["Esoterist", "Primus Nullificator"]]
    dg = discipline_choice(key, required=False)
    dmin = uid(dg.get("id"), "min")
    add_to(dg, "constraints", [constraint(dmin, "min", 0)])
    need = [ts()] + [_negate(c) for c in exclude]
    add_mods(dg, [modifier("set", dmin, 1, groups=[all_of(*need)]),
                  modifier("set", "hidden", "true", groups=[any_of(not_ts(), *exclude)] if exclude else None,
                           conds=None if exclude else [not_ts()])])
    if exclude:
        # an Esoterist / Primus Nullificator drops a Discipline picked earlier
        add_mods(dg, [modifier("set", uid(dg.get("id"), "max"), 0, groups=[any_of(*exclude)])])
    cg = cult_choice(key, required=True, only_ts=True)
    ts_only(cg)
    add_to(e, "selectionEntryGroups", [g, dg, cg])
    ml = "Psyker (Mastery Level 2) - Sorcerers of Prospero" if praetor else "Psyker (Mastery Level 1) - Sorcerers of Prospero"
    add_to(e, "infoLinks", [info_link(L.rule_ref("Sorcerers of Prospero")[0], ml, key=key + "sop",
                                      mods=[modifier("set", "hidden", "true", conds=[not_ts()])])])


def add_ts_links_to_power_weapons(roots):
    """Prosperine Force Weapon (+10 over the Power Weapon) and Aether-fire Cannon (free for a Plasma Cannon) wherever
    those can be chosen, visible only for Thousand Sons."""
    pw, pc = W("Power Weapon"), W("Plasma Cannon")
    done = set()
    for r in roots:
        for g in list(r.iter("selectionEntryGroup")):
            if id(g) in done:
                continue
            done.add(id(g))
            links = g.find("entryLinks")
            if links is None:
                continue
            for lk in list(links):
                t = lk.get("targetId")
                if t not in (pw, pc):
                    continue
                cost = 0
                cs = lk.find("costs")
                if cs is not None:
                    cost = float(cs[0].get("value"))
                name, target, extra = (("Prosperine Force Weapon", W("Prosperine Force Weapon"), 10) if t == pw else
                                       ("Aether-fire Cannon", W("Aether-fire Cannon"), 0))
                nid = uid(lk.get("id"), "ts", name)
                new = link(nid, target, name, cost=int(cost + extra) or None,
                           mods=[modifier("set", "hidden", "true", conds=[not_ts()])])
                if g.get("defaultSelectionEntryId") is not None:
                    new.set("sortIndex", str(int(lk.get("sortIndex") or 1) + 100))
                links.append(new)


def mark_brotherhood(unit, bro_id):
    add_mods(unit, [modifier("add", "category", gs.CAT_BROTHERHOOD, conds=[cond(bro_id, "self", "atLeast", 1)])])


def extend(ctx):
    units_by_name = {e.get("name"): e for e in ctx.units + ctx.shared}
    roots, new_shared = _extend(units_by_name, ctx.units, ctx.shared)
    ctx.add_units(*roots)
    ctx.add_shared(*[e for e in new_shared if e not in ctx.shared])


def _extend(units_by_name, units, shared):
    roots = []
    first_retinue = len(RETINUE_SHARED)
    # Legion rules on the Legion choice, Price of Knowledge force org changes
    legion = units_by_name["Legion"]
    for e in legion.iter("selectionEntry"):
        if e.get("id") == TS:
            add_to(e, "infoLinks", rules_links(["Legiones Astartes (Thousand Sons)", "Sorcerers of Prospero",
                                                "The Prosperine Cults", "Cult Mastery", "Psychic Brotherhoods",
                                                "Price of Knowledge", "Signs and Portents"], key="ts-legion"))
    add_mods(legion, [modifier("add", "category", c, conds=[cond(TS, "self", "atLeast", 1)])
                      for c in (gs.CAT_HQ_PLUS1, gs.CAT_EL_PLUS1, gs.CAT_FA_MINUS1)])

    # Praetor / Centurion
    ic_additions("praetor-ts", units_by_name["Legion Praetor"], True)
    ic_additions("centurion-ts", units_by_name["Legion Centurion"], False)

    # Veteran / Terminator squads: Psychic Brotherhood, Asphyx Shells, Transponders
    for n in ["Legion Veteran Squad", "Legion Terminator Squad"]:
        e = units_by_name[n]
        adds = [brotherhood(e.get("id"), 25, fellowships_cost=15), ts_option(e.get("id"), "Asphyx Shells (squad)", 20,
                                                                              item="Asphyx Shells")]
        mark_brotherhood(e, uid("brotherhood", e.get("id")))
        if n == "Legion Terminator Squad":
            tp = ts_option(e.get("id"), "Teleportation Transponders (entire squad)", 15,
                           item="Teleportation Transponders")
            add_mods(tp, [modifier("set", PTS, 0, conds=[rite("The Guard of the Crimson King")])])
            adds.append(tp)
        add_to(e, "selectionEntries", adds)
    # Terminator Command Squads (retinues) may take Transponders too
    for e in RETINUE_SHARED:
        if e.get("name") == "Legion Terminator Command Squad":
            tp = ts_option(e.get("id"), "Teleportation Transponders (entire squad)", 15,
                           item="Teleportation Transponders")
            add_mods(tp, [modifier("set", PTS, 0, conds=[rite("The Guard of the Crimson King")])])
            add_to(e, "selectionEntries", [tp])
    # Tactical Squads of 20 in The Fellowships of Prospero
    tac = units_by_name["Legion Tactical Squad"]
    tid = tac.get("id")
    off = any_of(cond(rite_id("The Fellowships of Prospero"), "force", "lessThan", 1),
                 cond("model", tid, "lessThan", 20))
    off2 = any_of(cond(rite_id("The Fellowships of Prospero"), "force", "lessThan", 1),
                  cond("model", tid, "lessThan", 20))
    add_to(tac, "selectionEntries", [brotherhood(tid, 25, visible_if=(off, off2), any_discipline=True)])
    mark_brotherhood(tac, uid("brotherhood", tid))

    # new units
    roots += [sekhmet(), khenetai(), ammitara(), castellax_achea(), osiron(), numerologist(), *characters(),
              magnus(), magnus_shard()]
    for r in roots[:3]:  # Sekhmet, Khenetai, Ammitara are Psychic Brotherhoods
        add_to(r, "categoryLinks", [category_link(gs.CAT_BROTHERHOOD, "Psychic Brotherhood", key=r.get("id"))])
    for r in roots:
        dedupe_kit(r)

    # Rites of War
    rites = units_by_name["Rite of War"]
    rg = rites.find("selectionEntryGroups")[0]
    ts_rites = []
    for n in ["The Axis of Dissolution", "The Guard of the Crimson King", "The Fellowships of Prospero"]:
        rid = rite_id(n)
        mods = [modifier("set", "hidden", "true", conds=[not_ts()])]
        if n == "The Fellowships of Prospero":
            mods.append(modifier("add", "error", "The Fellowships of Prospero: the Detachment must include at least two "
                                                 "Psychic Brotherhoods.",
                                 conds=[cond(rid, "force", "atLeast", 1),
                                        cond(gs.CAT_BROTHERHOOD, "force", "lessThan", 2)]))
        if n in ("The Axis of Dissolution", "The Guard of the Crimson King"):
            mods.append(modifier("add", "error", f"{n}: the Detachment may not include a Fortification.",
                                 conds=[cond(rid, "force", "atLeast", 1),
                                        cond(gs.cat("Fortification"), "force", "atLeast", 1)]))
        ts_rites.append(entry(rid, f"{n} (Thousand Sons)", rules=[rule(uid("rite-rule", n), n, TS_RULES[n])],
                              mods=mods))
    add_to(rg, "selectionEntries", ts_rites)
    add_mods(rites, [modifier("add", "category", gs.CAT_LIMIT_FA,
                              conds=[cond(rite_id("The Fellowships of Prospero"), "self", "atLeast", 1)])])

    # Prosperine Force Weapons / Aether-fire Cannons everywhere they can be chosen
    new_shared = RETINUE_SHARED[first_retinue:]
    for r in new_shared:
        dedupe_kit(r)
    add_ts_links_to_power_weapons(units + roots + shared + RETINUE_SHARED)
    # Ahriman's Cabal: Prosperine Force Weapon for +5 (instead of +10) over a Power Weapon
    cabal = uid("ahriman-cabal")
    for r in RETINUE_SHARED:
        if not any(e.get("id") == cabal for e in r.iter("selectionEntry")):
            continue
        for lk in r.iter("entryLink"):
            if lk.get("targetId") == W("Prosperine Force Weapon"):
                add_mods(lk, [modifier("decrement", PTS, 5, conds=[cond(cabal, r.get("id"), "atLeast", 1)])])
    return roots, new_shared
