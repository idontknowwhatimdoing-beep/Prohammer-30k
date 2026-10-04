"""Mechanicum (Taghmata, Orders of High Techno-Arcana, Dark Mechanicum) - Prohammer 30k army book.

Structure
- One common army list. A "Mechanicum Army" configuration entry (one per Detachment) holds the army rules, gives
  the Mechanicum Force Organisation chart its third HQ slot and lets the player pick an Order of High
  Techno-Arcana or (Traitor only) a Dark Techno-Arcana. Units, options and restrictions of an Order / Dark
  Techno-Arcana appear or are checked when it is chosen.
- A shared "Warlord" upgrade (one per army) on every HQ Independent Character drives the Warlord-dependent rules
  (Djinn-skein, Myrmidax / Ordo Reductor / Genetor Warlord options, "must be the Warlord" rules).
- Dark Mechanicum options (Daemonic Infusion, Warp-Wings, Abominable Reconstruction, Volatile Charges, Dark
  Invocation) are attached to the units listed in the book's cost tables.
"""
from armies.common import *
from bsx import el
from legiones2 import _negate
from legiones_wargear import WEAPON_PROFILES as _WP

ARMY = "Mechanicum"
import armies.common as _C
_C.ARMY_KEY = ARMY       # ids below are computed at import time

# Legiones Astartes profiles of standard weapons (snapshot before start() empties the tables)
LA = dict(_WP)

# ====================================================================== RULES
RULES = {
    # ------------------------------------------------------------ army construction
    "Mechanicum Army List": (
        "Mechanicum Detachments use the Mechanicum Standard Force Organisation Chart: HQ 1-3, Troops 2-6, Elites 0-3, "
        "Fast Attack 0-3, Heavy Support 0-3 (compulsory: 1 HQ and 2 Troops). Units with a rule preventing them from "
        "fulfilling a compulsory selection may not do so. Lords of War and Fortifications are not part of the chart; "
        "they may only be included where the mission permits it or both players agree, and no army may contain more "
        "than one Lord of War. Titans are selected with the appropriate Titan / Lords of War rules. Dedicated "
        "Transports do not use a Force Organisation slot. A Mechanicum Detachment may be a Primary or an Allied "
        "Detachment; each Detachment must fulfil its own compulsory selections and rules of one Detachment do not "
        "affect another. Unless stated otherwise units of different Cults and Orders may be selected together. "
        "Allegiance: every Mechanicum Detachment is Loyalist or Traitor; units are available to either unless their "
        "entry says otherwise. A Traitor army is not automatically Dark Mechanicum. Covenant of Mars: Mechanicum "
        "command abilities and special rules only affect Mechanicum units, allied rules do not affect Mechanicum "
        "units (and vice versa), Legion rules and Provenances of War do not affect Mechanicum units, and an Allied "
        "Detachment may not fulfil the compulsory selections of the Primary Detachment. Warlord: one eligible HQ "
        "Character is nominated as Warlord (normally the senior Magos or Archmagos) and selects a Warlord Trait under "
        "the ProHammer Classic rules (no random Warlord Traits)."),
    "The Rule of the Archmagos": (
        "A Mechanicum army (and a Detachment) may include no more than one Archmagos. If an Archmagos is included in "
        "the Primary Detachment and is eligible to be the army's Warlord, he must be the Warlord. If no Archmagos is "
        "present, a Magos Dominus may act as the army's Warlord."),
    "Orders of High Techno-Arcana": (
        "A Mechanicum Detachment may select one Order of High Techno-Arcana only if it includes at least one Magos "
        "Dominus or Archmagos (an army led by an Archmagos may select one Order for which it qualifies). Only one Order "
        "may normally be selected for a Detachment. The Order may alter the army's composition, wargear and special "
        "rules; its Restrictions must be obeyed. An Adjutant Specialisation does not affect which Order may be "
        "selected. Kelbor-Hal, Zagreus Kane, Calleb Decima, Lukas Chrom and Anacharis Scoria fulfil the Archmagos / "
        "Magos Dominus requirement."),
    "Cybernetic Command": (
        "A unit which requires a Cortex Controller or other command source must obey all restrictions imposed by its "
        "special rules. The presence of a Mechanicum Character does not satisfy such a requirement unless that model "
        "has the appropriate equipment or special rule. Cortex Controllers only affect units their rules permit."),
    "Iron and Machine": (
        "Models with this rule have the Stubborn special rule. In addition, attacks with the Poisoned or Fleshbane "
        "special rules may never wound a model with Iron and Machine on better than a 5+, regardless of any other "
        "rule. (Battle-Automata use the Cybernetica Cortex rule instead.)"),
    "Cybernetica Cortex": (
        "A model with this rule has the Fearless special rule, is unaffected by Poisoned and Fleshbane attacks except "
        "on a To Wound roll of 6+, and is subject to Programmed Behaviour unless controlled by a Cortex Controller."),
    "Programmed Behaviour": (
        "At the start of each phase, check whether the unit has at least one model within range (12\") of a friendly "
        "Cortex Controller. If not, for that phase: Movement - if an enemy unit is within 12\" it must move towards the "
        "nearest visible enemy if able; Shooting - if an enemy unit is within 12\" it must target the nearest eligible "
        "enemy unit; it may not Split Fire, enter Overwatch or voluntarily withdraw from combat; Assault - if an enemy "
        "unit is within charge range it must declare a charge against the nearest eligible enemy unit if able. "
        "Otherwise Battle-Automata act normally. Controlled units may move, select targets, Split Fire, enter "
        "Overwatch, perform reactions and charge normally."),
    "Paragon of Metal": (
        "A Battle-Automata upgraded to a Paragon of Metal ignores Programmed Behaviour at all times and does not "
        "require a Cortex Controller, gains It Will Not Die and Rampage, and may never Score or Contest objectives. A "
        "unit may contain no more than one Paragon of Metal. It still has the Cybernetica Cortex special rule for "
        "all other purposes. A model with Paragon of Metal may not also receive Daemonic Infusion."),
    "Atomantic Shielding": (
        "A model with Atomantic Shielding has a 5+ Invulnerable Save against shooting attacks and a 6+ Invulnerable "
        "Save against close-combat attacks."),
    "Reactor Blast": (
        "When a model with this rule loses its final Wound, roll a D6 before removing it. On a 6 its reactor ruptures: "
        "place a Large Blast marker centred over the model; every model touched, friend or foe, suffers a hit: Reactor "
        "Blast - Range Self, S = the model's unmodified Toughness (max 8), AP4, Large Blast. Then remove the model. In "
        "an Engines of Ruin army, Catastrophic Reactor Blast is used instead."),
    "Battlesmith": (
        "Instead of firing any weapons in its Shooting phase, the model may attempt a repair on one eligible friendly "
        "model in base contact (Vehicles, models with Cybernetica Cortex or Iron and Machine). Roll a D6: on a 5+ the "
        "repair succeeds - a Vehicle removes one Engine Damaged, Weapon Destroyed or Immobilised result; any other "
        "model regains one lost Wound (up to its starting Wounds). One repair attempt per Battlesmith per turn; a model "
        "may benefit from only one successful repair per turn; destroyed models are never returned to play. Equipment "
        "modifying repair rolls applies to Vehicle repairs and to restoring Wounds. Models with the Daemon special rule "
        "may not be repaired unless another rule allows it."),
    "Cybertheurgist": (
        "Once in each friendly Shooting phase, instead of firing a weapon or making any other shooting attack, the "
        "model may perform one Cybertheurgic Rite: choose one friendly unit with the Cybernetica Cortex special rule "
        "within 18\" and line of sight and take a Leadership test on the Cybertheurgist's Leadership. If passed, the "
        "Rite takes effect; if failed it has no effect; if failed on a double 6 a Cybertheurgy Mishap is suffered. "
        "Cybertheurgy is not a Psychic Power. Rites (until the start of the controlling player's next turn): Rite of "
        "Celerity - Fleet and +1 Initiative; Rite of Fury - +1 Attack; Rite of Mending - one model regains one lost "
        "Wound (immediately); Rite of Volition - the target ignores Programmed Behaviour and acts normally without a "
        "Cortex Controller. Cybertheurgy Mishap: the targeted unit suffers one Wound with no Armour Save allowed "
        "(Invulnerable Saves may be taken), allocated by its controlling player."),
    "Retinue (Protector Squad)": (
        "One Protector Squad may be selected for each Archmagos or Magos Dominus in the army. If selected in this way "
        "it does not use an additional Elites choice. The Archmagos or Magos Dominus may begin the battle joined to the "
        "Protector Squad but remains an Independent Character."),
    "Very Bulky": "Counts as three models for Transport Capacity (see Bulky).",
    "Rage": "The unit has the Rage special rule (ProHammer Classic): it gains +2 Attacks instead of +1 when it charges.",
    "Feel No Pain (6+)": "This model has the Feel No Pain special rule with a 6+ roll.",
    "Feel No Pain (5+)": "This model has the Feel No Pain special rule with a 5+ roll.",
    "Preferred Enemy (Characters)": "The unit has Preferred Enemy against Characters.",
    "Hatred (Everything)": "The unit has the Hatred special rule against all enemy units.",
    "Hatred (Traitors)": "The model has the Hatred special rule against units of the Traitor Allegiance.",
    "Wrecker": "Against Fortifications and immobile structures, failed Armour Penetration rolls may be re-rolled.",
    "Lumbering Advance": "Models with this rule may not make Advance or Pursuit moves.",
    "Fusillade Attack": (
        "A model with this rule may fire two ranged weapons during the Shooting phase, provided both are fired at the "
        "same target."),
    "Djinn-sight": "A model with Djinn-sight has Night Vision and may re-roll failed rolls made to detect Hidden units.",
    "Crew: Servitors": "The vehicle is crewed by Servitors (no additional rules given).",
    "Expendable": "Models with this rule may never Score or Contest objectives.",
    # ------------------------------------------------------------ HQ
    "Combat Attachés": (
        "Although purchased together as a single HQ choice, each Tech-Priest is a separate unit once deployed and may "
        "join friendly units as though it were an Independent Character. When a Tech-Priest joins a friendly unit, "
        "choose WS or BS: the unit receives +1 to that characteristic while the Tech-Priest remains with it. A unit may "
        "only benefit from one Combat Attaché at a time."),
    "Doctrina Imperatives": (
        "At the beginning of each friendly turn the Skitarii Marshal may nominate himself or one friendly Skitarii unit "
        "within 12\" and activate one Doctrina Imperative until the beginning of the controlling player's next turn: "
        "Protector Doctrina - +1 BS, -1 WS; Conqueror Doctrina - +1 WS, -1 BS. A unit may only be affected by one "
        "Doctrina Imperative at a time. (Skitarii Order: see that Order for the army-wide version.)"),
    "Titan Guard": (
        "Friendly Secutarii units within 6\" of the Axiarch (12\" with the Secutarii Order) may use his Leadership for "
        "all Leadership tests and gain Stubborn."),
    "Binaric Stratagems": (
        "At the beginning of each friendly turn, nominate one friendly Secutarii unit within 12\" of the Axiarch. Until "
        "the beginning of the controlling player's next turn it gains one of: Tank Hunters, Move Through Cover or "
        "Counter-Attack. A unit may only benefit from one Binaric Stratagem at a time. (Replaced by Binaric Command "
        "Network with the Secutarii Order.)"),
    "Rad Poisoning": (
        "When resolving a shooting attack with Rad Poisoning, each unmodified To Wound roll of 6 inflicts two Wounds "
        "instead of one, each allocated and saved separately. No effect against Vehicles."),
    # Adjutant specialisations
    "Adjutant Specialisations": (
        "An Adjutant may be upgraded to one specialisation only. A specialisation does not affect which Order of High "
        "Techno-Arcana the army may select."),
    "Malagra Adjutant": (
        "+1 WS; gains Preferred Enemy (Characters), Monster Hunter, Precision Strikes, Scout and Mark of Execution. May "
        "additionally purchase a Lucifex (+10), Photon Gauntlet (+10) and Rad Furnace (+25)."),
    "Precision Strikes": (
        "A model with this rule in base contact with an enemy Independent Character may direct any or all of its "
        "close-combat attacks against that Character; wounds from those attacks are allocated to the Character before "
        "normal wound allocation (exception to the normal rules)."),
    "Mark of Execution": (
        "After both armies have deployed but before the first turn, nominate one enemy Independent Character, "
        "Monstrous Creature or Walker. The model(s) with this rule may re-roll To Hit rolls of 1 against it. If the "
        "nominated model is destroyed by them (Malagra Adjutant) / is destroyed (Malagra Order), the Mechanicum player "
        "gains +1 Victory Point in missions which use Victory Points."),
    "Logis Adjutant": "+1 Ld; gains a Nuncio Vox, a Cognis Signum, Strategic Calculus and Calculated Deployment.",
    "Strategic Calculus": (
        "While this model is on the battlefield (Logis Adjutant) / always (Archimandrite Order), add +1 to friendly "
        "Reserve rolls. A natural 1 always fails."),
    "Calculated Deployment": (
        "After deployment but before the first turn, nominate one friendly Mechanicum Infantry unit; it may be removed "
        "and placed into Reserve, gaining Outflank. Vehicles, Monstrous Creatures and units with Cybernetica Cortex may "
        "not benefit."),
    "Secutor Adjutant": (
        "+1 BS; gains Fusillade Pistols and Chain Fire. May carry two Pistols, each selected independently from: Bolt "
        "Pistol +1, Volkite Serpenta +5, Archaeotech Pistol +10, Photon Gauntlet +10, Plasma Pistol +15, Lucifex +10."),
    "Fusillade Pistols": (
        "A Secutor Adjutant with two Pistols may fire both in the same Shooting phase; both must normally target the "
        "same enemy unit."),
    "Chain Fire (Secutor Adjutant)": (
        "Once per Shooting phase, when firing two Pistols, declare Chain Fire before rolling To Hit. Each successful "
        "To Hit roll generates one additional shot with the same weapon; continue while shots hit. A natural 1 To Hit "
        "ends the sequence for that weapon; at most six additional shots per weapon. An Adjutant which uses Chain Fire "
        "may not Charge in the same turn."),
    "Ordinator Adjutant": (
        "Gains a Cognis Signum and Master of Destruction. May purchase an Ordinator Bombardment (+35): once per battle, "
        "instead of firing his normal weapons, he may call it down while on the battlefield and not Pinned, Falling "
        "Back or in close combat (no Line of Sight required)."),
    "Master of Destruction": (
        "Once in each friendly Shooting phase, nominate one friendly Mechanicum Artillery unit, or one friendly unit "
        "firing an Ordnance or Barrage weapon, within 12\". It may re-roll the Scatter die for one Blast weapon fired "
        "that phase; the second result must be accepted."),
    "Explorator Adjutant": (
        "Gains Scout, Infiltrate, Move Through Cover, Djinn-sight and Telescopic Stalker Limbs. May replace his "
        "Laspistol with an Explorator Arquebus (+10)."),
    "Telescopic Stalker Limbs": (
        "At the beginning of each friendly Movement phase choose a configuration lasting until the next friendly "
        "Movement phase. Retracted: improve any Cover Save available to the model by +1 (max 3+); does not grant one. "
        "Extended: Cover Saves against the model's shooting attacks are worsened by 1, and Retracted does not apply."),
    # ------------------------------------------------------------ Elites
    "Destructor Doctrine": "Myrmidon Destructors may re-roll shooting To Hit rolls of 1.",
    "Crawling Fire": (
        "After placing the Blast marker the firing player may move it up to 2\" in any direction, provided it then "
        "covers more models than before."),
    "Lingering Death": (
        "After resolving the attack, leave the Blast marker in place; the area it covers counts as Dangerous Terrain "
        "for all models with a Toughness value for the rest of the battle."),
    "Guardian-Servitor Protocols": (
        "While at least one model of the unit is within 24\" of a friendly model with Battlesmith or Cybertheurgist, the "
        "Scyllax are Fearless. Otherwise the unit must take a Leadership test at the beginning of its Movement phase; "
        "if failed it must remain stationary that turn but may shoot normally (if already in close combat it fights "
        "normally)."),
    "Maelstrom": (
        "For each natural To Wound roll of 6, immediately make one additional attack. Additional attacks may not "
        "generate further attacks."),
    "Dismemberment": (
        "A Scyllax may give up all its normal close-combat attacks to make one attack which counts as a Strength 7 "
        "Unwieldy Power Weapon."),
    "Weapons Platform": (
        "A Weapons Platform and its crew follow the normal ProHammer rules for Artillery. If all Artillery Servitors "
        "belonging to a platform are removed, that platform may no longer fire."),
    "Servitor Protocols": (
        "If no friendly Tech-Priest, Magos, Archmagos or other model with Battlesmith is within 12\" at the beginning "
        "of the unit's turn, it operates on basic combat programming: it may move and shoot normally but may not "
        "Advance, may not voluntarily Fall Back, must shoot the nearest eligible enemy unit if it shoots and must charge "
        "the nearest eligible enemy unit if it charges. While a suitable controlling model is within 12\" these "
        "restrictions are ignored."),
    "Integrated Weapon Systems": (
        "A Praetorian Battle-Servitor with two ranged weapons may fire both in the Shooting phase; both must normally "
        "be fired at the same target."),
    "Targeting Protocols": (
        "A Cataphract Robot may fire two ranged weapons in each Shooting phase; both must be fired at the same target."),
    "Battle-Pilgryms": "When a Battle-Pilgrym unit makes an Advance move, add +2\" to the distance moved.",
    "Siphoned Vigour": (
        "If an Electro-Priest unit completely destroys an enemy unit in close combat, its invulnerable save improves "
        "from 4+ to 3+ for the rest of the battle."),
    # ------------------------------------------------------------ Troops
    "Rite of Pure Thought": "The unit is Fearless, but may not make Pursuit moves or fire Overwatch.",
    "Blind Barrage": (
        "Once per battle, instead of shooting, a Peltast Phalanx containing at least five models with Galvanic Casters "
        "may nominate one friendly non-vehicle unit within 18\" and Line of Sight; it gains a 5+ Cover Save until the "
        "beginning of the controlling player's next turn."),
    "Thallax Augments": (
        "The entire unit may select one Augment: Destructor (+15) - the unit gains Tank Hunters; Empyrite (+10) - "
        "Deep Strike; Ferrox (+25) - Rage, and all its close combat attacks gain Rending (a Ferrox unit may not replace "
        "any of its Lightning Guns); Icarian (+25) - if the unit remains stationary in its Movement phase its weapons "
        "may engage Flyers using the normal anti-aircraft rules until the beginning of its next turn."),
    "Support Unit": (
        "A Castellax Battle-Automata Maniple is a Troops choice but may not fulfil the compulsory Troops requirement "
        "unless another rule allows it."),
    # ------------------------------------------------------------ transports / vehicles
    "Repair": (
        "If a Mechanicum Rhino is Immobilised, instead of firing any of its weapons in the Shooting phase roll a D6; on "
        "a 6 remove one Immobilised result. The Rhino may move normally from its following Movement phase."),
    "Galvanic Traction Drive": "The vehicle may re-roll failed Dangerous Terrain tests.",
    "Volkite Sentinels": (
        "Each Volkite Sentinel is a pintle-mounted Volkite Charger (normal Volkite Charger profile). It may be fired in "
        "addition to the vehicle's other weapons and may target a different enemy unit."),
    "Shock Ram": (
        "When the vehicle Rams, or is Rammed against its Front Armour, it counts its Front Armour as 15 for resolving "
        "the Ram, and the opposing vehicle also suffers one roll on the Haywire table (one Haywire hit). When it Tank "
        "Shocks, the affected enemy unit suffers D6 Strength 6 AP5 hits before the Tank Shock is resolved. The Shock Ram "
        "is not a weapon and cannot be removed by Weapon Destroyed."),
    "Subterranean Assault": (
        "A Termite may begin the battle in Reserve and enter play by Deep Strike. If an army contains more than one "
        "Termite using Subterranean Assault, half of them (rounding up) arrive automatically in the controlling "
        "player's first turn; the rest use the normal Reserve rules."),
    "Death From Below": (
        "When a Termite arrives by Deep Strike, resolve scatter normally. If its final position is on top of enemy "
        "infantry, move them the minimum distance to clear the hull; that unit suffers D6 Strength 6 AP4 hits. If it "
        "emerges underneath a vehicle, that vehicle suffers one Strength 10 hit against its Side Armour before the "
        "Termite is placed. The area beneath its arrival point is Difficult Terrain for the rest of the battle."),
    "Melta Cutters": (
        "A Termite ignores Difficult Terrain and automatically passes Dangerous Terrain tests caused by terrain. When "
        "Ramming a Fortification add +2 Strength."),
    "Crawling Advance": "A Termite may never move faster than Combat Speed and may never move Flat Out.",
    "Prisoned": (
        "An Ursarax may make only one attack with the Volkite Incinerator Point-Blank Blast profile per Assault phase, "
        "regardless of its Attacks, and only against Infantry, Jump Infantry or Jet Pack Infantry models."),
    "Automated Artillery": (
        "Tarantula Sentry Guns automatically pass Morale and Pinning tests and may never Advance, Charge or make "
        "Pursuit moves."),
    "Firing Modes": (
        "Before deployment choose one firing mode for the Battery (fixed unless Anima Override is used). Point Defence "
        "Mode: each gun has a fixed 90 degree forward arc and normal weapon range. Sentry Mode: 360 degree arc but only "
        "targets within 18\". Automated Targeting: Heavy Bolter, Heavy Flamer, Rotor Cannon, Mauler Bolt Cannon and "
        "Volkite guns must target the nearest eligible non-vehicle unit; Lascannon, Multi-Melta and Photon Thruster "
        "guns must target the nearest eligible Vehicle or Monstrous Creature; if no preferred target is available, the "
        "nearest eligible enemy unit."),
    "Anima Override": (
        "If a friendly model with Battlesmith is within 6\" of the Battery at the beginning of the Shooting phase, the "
        "Battery may ignore Firing Modes and Automated Targeting that phase and select targets normally."),
    "Concealment (Tarantula)": "The Battery gains Stealth.",
    "Forward Deployment (Tarantula)": "The Battery gains Scout.",
    "Drop Capsule (Tarantula)": "The Battery gains Deep Strike; after entering play the Tarantulas remain Immobile.",
    "Setheno-Djinn": "Successful Cover Saves made against wounds caused by this weapon must be re-rolled.",
    "Flare Shield (Vultarax)": (
        "The Vultarax's Flare Shield applies against all ranged attacks made against it: reduce the Strength of Blast "
        "and Template attacks by 2 and of all other ranged attacks by 1. No effect in close combat."),
    "Void Shield Projector": (
        "The Guardian projects one active Void Shield (plus one per additional Void Shield purchased). The Guardian and "
        "friendly units with at least half their models within 6\" of it are protected against shooting attacks "
        "originating from outside the shield: resolve incoming hits against Armour Value 12 first; a Glancing or "
        "Penetrating Hit collapses one active Void Shield and is discarded. Once all are collapsed, attacks are "
        "resolved normally. At the beginning of each friendly turn roll a D6 per collapsed shield: on a 5+ it is "
        "restored."),
    "Two Power Swords": "The Crusader's pair of Power Swords count as Power Weapons and grant +1 Attack.",
    "Target Acquisition": (
        "At the beginning of the friendly Shooting phase nominate one enemy unit visible to a Seeker Robot within 24\". "
        "Until the end of that phase one friendly Mechanicum unit within 12\" of the Seeker may re-roll one failed To "
        "Hit roll when firing at it. A unit may only benefit from one Target Acquisition each Shooting phase."),
    "Programmed Demolition": (
        "Unless a Bombot is within 12\" of a friendly Cortex Controller at the beginning of its Movement phase, it must "
        "move towards the nearest enemy unit by the shortest route (it may Advance while doing so)."),
    "Detonation": (
        "In the controlling player's Shooting phase a Bombot may detonate instead of attacking (even if it Advanced): "
        "remove it and centre a Large Blast marker over its former position; every other model touched suffers a hit "
        "from the Internal Demolition Charge (Self, S8, AP2, Ordnance, Large Blast)."),
    "Volatile Payload": (
        "If a Bombot suffers an unsaved wound caused by a grenade or Melta Bomb, it immediately detonates before being "
        "removed as a casualty."),
    "Plasma Wave": "Successful Cover Saves made against this weapon must be re-rolled.",
    "Hazardous Munitions": (
        "If the Karacnos is destroyed by an Explodes result, increase the explosion radius by D6+2\" and resolve the "
        "hits at Strength 5 AP4."),
    "Indirect Fire (Minotaur)": (
        "The Dual Earthshaker Cannon may only fire using the Barrage rules and may not engage targets within 24\"."),
    "Special Configuration": (
        "Models attacking a Minotaur in close combat always resolve their attacks against Side Armour 12. Rams and "
        "other attacks against a specific facing use the appropriate Armour value normally."),
    # ------------------------------------------------------------ weapon rules
    "Taser": (
        "For every unmodified To Hit roll of 6 made with a Taser weapon in close combat, the attack inflicts three hits "
        "instead of one (extra hits cannot generate further hits)."),
    "Rad-phage": (
        "If a non-vehicle model suffers one or more unsaved Wounds from a weapon with Rad-phage and survives, reduce "
        "its Toughness by 1 for the rest of the battle (minimum 1). Cumulative."),
    "Luminagen": (
        "A unit suffering one or more unsaved Wounds, Glancing or Penetrating Hits from a Luminagen weapon is "
        "illuminated until the end of the player turn: its Cover Save is worsened by 1 and friendly units charging it "
        "add 1\" to their Charge distance. Not cumulative."),
    "Paired": (
        "A model with two weapons with the Paired rule receives +1 Attack in close combat (already included in the "
        "profile where stated). A Paired weapon counts as a single weapon for all other purposes; if one is lost the "
        "bonus is lost."),
    "Chainaxe": "An Armour Save better than 4+ is reduced to 4+ against wounds caused by a Chainaxe. Invulnerable Saves are unaffected.",
    "Firing Calibration": (
        "The weapon may not be fired if its bearer moved in the same turn, even if it has Relentless or is a vehicle."),
    "Mechanicum Axe": (
        "A Mechanicum Axe counts as a Power Weapon and gives its bearer +1 to Battlesmith and other repair rolls."),
    "Electro Stave": (
        "Attacks with an Electro Stave are resolved at Strength 6 against non-vehicle models and Strength 8 against "
        "vehicles; Two-Handed and Rending."),
    "Combi-Weapon": (
        "A Combi-Weapon consists of a Bolter and a secondary weapon. The Bolter may be fired normally; the secondary "
        "weapon may be fired once per battle; both may not be fired in the same Shooting phase."),
    # ------------------------------------------------------------ Orders of High Techno-Arcana
    "Legio Cybernetica": (
        "RESTRICTIONS: the Warlord must be an Archmagos or Magos Dominus equipped with a Cortex Controller; the "
        "compulsory Troops choices must be Castellax Battle-Automata Maniples, each containing at least two Castellax; "
        "if the army contains Fast Attack (Heavy Support) choices, at least one Fast Attack (Heavy Support) choice with "
        "Cybernetica Cortex must be selected before any without it. LEGION OF STEEL: all friendly models with "
        "Cybernetica Cortex gain +1 Initiative. ENHANCED CYBER-CONTROL: Cortex Controller range is 24\" instead of "
        "12\"; Cybertheurgic Rites targeting Cybernetica Cortex models have 24\" range instead of 18\". PATRIS "
        "CYBERNETICA: the Warlord gains Feel No Pain (5+) and may join friendly units composed entirely of Cybernetica "
        "Cortex models despite normally being unable to join Monstrous Creature units. CYBERNETIC COHORT: Castellax "
        "selected as compulsory Troops may fulfil the compulsory Troops requirement."),
    "Myrmidax": (
        "RESTRICTIONS: the Warlord must be an Archmagos or Magos Dominus; the army must include at least one Myrmidon "
        "Secutor Host or Myrmidon Destructor Host. MYRMIDON COVENANTS: Myrmidon Secutor Hosts may be selected as Troops "
        "but then may not fulfil the compulsory Troops requirement. THE WAY OF DESTRUCTION: all Myrmidon Secutors, "
        "Destructors, Reductors and the Warlord gain Hatred (Everything). MYRMIDAX WARLORD: the Warlord gains Fusillade "
        "Attack and Lumbering Advance, may select one additional ranged weapon at the normal cost from Rotor Cannon, "
        "Volkite Charger, Meltagun, Graviton Gun, Irad Cleanser, Phased Plasma-Fusil or Photon Thruster, and may take a "
        "Rad Furnace where normally permitted. PERFECTED ARMAMENT: one ranged weapon of the Warlord may be Master-crafted "
        "for free; one ranged weapon of each Myrmidon Lord may be Master-crafted for +10 points."),
    "Ordo Reductor": (
        "RESTRICTIONS: the Warlord must be an Archmagos or Magos Dominus; the army must contain at least one Myrmidon "
        "Reductor Host, Ordo Reductor Artillery Tank Battery or Ordo Reductor Minotaur Battery. ENGINES OF DESTRUCTION: "
        "Myrmidon Reductor Hosts, Ordo Reductor Artillery Tank Batteries, Minotaur Batteries and Mechanicum Weapons "
        "Platforms gain Tank Hunters (ranged attacks only); friendly Walkers and Monstrous Creatures within 12\" of the "
        "Warlord gain Wrecker. BODYGUARD: one Myrmidon Reductor Host may be the Warlord's Bodyguard and does not occupy "
        "an Elites choice (the Warlord and Bodyguard remain separate units). MASTER OF DESTRUCTION: the Warlord has "
        "Master of Destruction. REDUCTOR WAR MUNITIONS: the Warlord is equipped with one Breacher Charge and one "
        "Phosphex Bomb."),
    "Lachrimallus": (
        "RESTRICTIONS: at least one compulsory Troops choice must be an Adsecularis Tech-Thrall Covenant. LEGIONS OF "
        "THE EXPENDABLE: Tech-Thrall Covenants have Feel No Pain (5+) instead of (6+). RUTHLESS ASSAULT: Tech-Thrall "
        "Covenants gain Furious Charge; at the beginning of their Movement phase a Covenant within 12\" of a friendly "
        "Battlesmith may be ordered to make a Ruthless Assault and gains Fleet until the end of the turn (it may Advance "
        "and still Charge)."),
    "Macrotek": (
        "TECH-PRIEST AUXILIA: Tech-Priest Auxilia may be selected as Troops choices and may then fulfil a compulsory "
        "Troops requirement. MASTER ARTIFICERS: models with Battlesmith may re-roll failed repair rolls (one re-roll "
        "per attempt). FORTIFICATION ENGINEERS: after deployment select D3 terrain pieces at least partially within "
        "the Mechanicum deployment zone; their Cover Saves are improved by 1 (max 2+). FIELD REPAIRS: Battlesmiths may "
        "repair eligible friendly models within 3\" instead of in base contact."),
    "Malagra": (
        "RESTRICTIONS: the Warlord must be an Archmagos or Magos Dominus. THE GREAT HUNT: the Warlord and all friendly "
        "Mechanicum Independent Characters gain Preferred Enemy (Characters) and Monster Hunter. PRECISION STRIKES and "
        "MARK OF EXECUTION: see those rules (models with The Great Hunt re-roll To Hit rolls of 1 against the nominated "
        "model; +1 Victory Point if it is destroyed)."),
    "Explorator": (
        "EXPLORATOR EXPEDITION: all friendly Mechanicum Infantry units gain Move Through Cover. VOID-HARDENED ARMOUR: "
        "any Infantry unit wearing armour may upgrade it (+1 point per non-Bulky, +3 per Bulky, +5 per Very Bulky model): "
        "the Armour Save is unchanged, failed Armour Saves against Blast or Template weapons may be re-rolled, Advance "
        "distance is reduced by 1\" and Charge and Pursuit distances by 1\". EXPLORATION PARTY: up to one Troops choice "
        "may gain Scout for +15 points (not Vehicles or Cybernetica Cortex models)."),
    "Skitarii": (
        "RESTRICTIONS: the army must include a Skitarii Marshal; at least one compulsory Troops choice must be a "
        "Skitarii Cohort. SKITARII UNITS: Skitarii Marshals, Skitarii Cohorts and Skitarii Battle-Pilgrym Corpus. "
        "SKITARII BATTLE-PILGRYMS: Battle-Pilgrym Corpus units may be selected as Troops but then may not fulfil the "
        "compulsory Troops requirement. DOCTRINA IMPERATIVES: at the beginning of each friendly turn choose one "
        "Doctrina Imperative (Protector: +1 BS, -1 WS; Conqueror: +1 WS, -1 BS); all friendly Skitarii units with at "
        "least one model within 12\" of a Skitarii Marshal receive it until the next friendly turn; only one may be "
        "active at a time. BATTLEFIELD AUGMENTS: Skitarii Cohorts and Battle-Pilgrym Corpus units gain Move Through "
        "Cover. RAD SATURATION: enemy non-vehicle models in close combat with a Skitarii Cohort or Battle-Pilgrym "
        "Corpus suffer -1 Toughness (does not stack with other Rad Saturation, Rad Grenades or Rad Furnaces)."),
    "Secutarii": (
        "RESTRICTIONS: the army must include a Secutarii Axiarch and at least one Titan; at least one compulsory Troops "
        "choice must be a Secutarii Hoplite or Peltast Phalanx. ENHANCED TITAN GUARD: Titan Guard range is 12\". "
        "BINARIC COMMAND NETWORK (replaces Binaric Stratagems): at the beginning of each friendly turn each Axiarch may "
        "select Tank Hunters, Move Through Cover or Counter-Attack; until the next friendly turn every friendly "
        "Secutarii unit with at least one model within 12\" of him gains it (one Binaric Stratagem per unit; the "
        "controlling player chooses if in range of several). SECUTARII HAZARD PROTOCOLS: Secutarii units may re-roll "
        "failed Dangerous Terrain tests and failed Pinning tests caused by Blast, Large Blast or Barrage weapons."),
    "Ordinator": (
        "RESTRICTIONS: the Warlord must be an Archmagos or Magos Dominus. ORDINATOR: all close-combat and ranged attacks "
        "made personally by the Warlord gain Armourbane and Wrecker. BOMBARDMENT: once per battle, instead of firing "
        "its normal weapons, the Warlord may call down an Ordinator Bombardment (Unlimited, S8, AP3, Ordnance 1, Large "
        "Blast, Barrage, Lance, Twin-linked) while on the battlefield and not Pinned, Falling Back or in close combat. "
        "SIEGE CALCULATIONS: one friendly Mechanicum Heavy Support unit within 12\" of the Warlord may re-roll one failed "
        "Armour Penetration roll per friendly Shooting phase."),
    "Archimandrite": (
        "RESTRICTIONS: the Warlord must be an Archmagos. STRATEGIC CALCULUS: add +1 to all friendly Reserve rolls (a "
        "natural 1 always fails). OMNISSIAN ENGINES: all friendly Mechanicum Vehicles gain It Will Not Die; vehicles "
        "with Blessed Autosimulacra as standard wargear lose it (no further benefit) and vehicles may not purchase "
        "Blessed Autosimulacra. MASTER OF THE TAGHMATA: at the beginning of each friendly turn the Archmagos may "
        "nominate one friendly Mechanicum unit within 12\"; until the next friendly turn it may re-roll one failed "
        "Leadership, Morale or Pinning test, and a Cybernetica Cortex unit also ignores Programmed Behaviour. A unit may "
        "only be affected once at a time."),
    "Genetor - Magos Biologis": (
        "RESTRICTIONS: the Warlord must be an Archmagos or Magos Dominus; the army must include at least one unit "
        "eligible to purchase a Controlled Augmentation. MASTER OF THE FLESH: the Warlord gains Feel No Pain (5+) and "
        "Biologis. CONTROLLED AUGMENTATION: Tech-Thrall Covenants, Skitarii Cohorts, Battle-Pilgrym Corpus, Karkinos, "
        "Praetorian Battle-Servitors, Thallax and Ursarax may purchase one (every model the same): Reinforced Physiology "
        "(Feel No Pain 5+) +2/model, Enhanced Musculature (+1 S) +2/model, Accelerated Reflexes (+1 I) +2/model, "
        "Adrenal Induction (Furious Charge and Fleet) +2/model, Dermal Plating (improve Armour Save by 1, max 3+) "
        "+3/model; +5 per model for models with more than one starting Wound. PERFECTED SPECIMENS: one unit with a "
        "Controlled Augmentation may be upgraded for +20 points and may then purchase two different augmentations. "
        "ORGANIC RESILIENCE: Tech-Thralls, Skitarii, Battle-Pilgryms, Secutarii Hoplites and Peltasts, Karkinos, "
        "Praetorians, Thallax and Ursarax within 6\" of the Warlord may re-roll failed saves against Poisoned or "
        "Fleshbane attacks. RAD-ALCHEMY: the Warlord may purchase a Rad Furnace for +20; Tech-Priest Auxilia may "
        "purchase Rad Grenades for +10 per model, a Skitarii Primus for +10 and Praetorian Battle-Servitors for +5 per "
        "model. GENETOR AUXILIA: Praetorian Battle-Servitors may be selected as Troops but may not then fulfil the "
        "compulsory Troops requirement."),
    "Biologis": (
        "In the Shooting phase, instead of firing, the model may choose one friendly non-Vehicle model within 3\" which "
        "has lost Wounds and roll a D6: on a 4+ it regains one Wound (up to its starting Wounds). One successful "
        "Biologis per model per turn. Not on Vehicles, models composed entirely of machinery, Cybernetica Cortex models "
        "or Daemons."),
    # ------------------------------------------------------------ Dark Mechanicum
    "Dark Mechanicum": (
        "A Mechanicum army led by an Archmagos or Magos Dominus may instead be designated a Dark Mechanicum army. It "
        "uses the normal Mechanicum army list, Armoury and special rules, is always of Traitor Allegiance and must "
        "select one Dark Techno-Arcana instead of an Order of High Techno-Arcana (never both; normally only one). It "
        "gains access to the units designated Dark Mechanicum only, unless its Dark Techno-Arcana prohibits them."),
    "Daemon Engine Horde": (
        "DAEMONIC INFUSION: models listed in the cost table may purchase Daemonic Infusion (every model of a multi-model "
        "unit). WINGS OF THE ABOMINATION: models with Daemonic Infusion may purchase Warp-Wings. MALEFIC CYBERTHEURGY: "
        "Cybertheurgists may use Cybertheurgic Rites on friendly Daemon Engines within 18\" as if they had Cybernetica "
        "Cortex; a test failed on any double suffers a Cybertheurgy Mishap. DAEMON ENGINES: a non-Character Dark "
        "Mechanicum model with Daemon and Unstable (or whose entry says so) counts as a Daemon Engine. DARK INVOCATION: "
        "a Magos Dominus may become a Psyker (Mastery Level 1) for +30; an Archmagos for +30 (ML1) and a further +30 "
        "(ML2). Powers from the Malefic Daemonology discipline; Psychic Tests at Leadership 7."),
    "Daemonic Infusion": (
        "The model gains the Daemon and Unstable special rules. An existing Invulnerable Save is improved by +1 (max "
        "4+). A non-Character model with Daemonic Infusion counts as a Daemon Engine for Dark Mechanicum rules but keeps "
        "its Unit Type, wargear and special rules. A Paragon of Metal may not receive Daemonic Infusion. In a "
        "multi-model unit every model must purchase it."),
    "Unstable": (
        "At the beginning of the controlling player's Movement phase each unit containing Unstable models must take an "
        "Instability Test (Leadership test against Ld 7) unless at least one model is within 12\" of a friendly model "
        "with a Cortex Controller or Cybertheurgist (which counts as in range of itself). Whenever an Unstable unit fails "
        "a Leadership test it suffers one Wound per point by which the test was failed (no Armour Saves, Invulnerable "
        "Saves allowed, not negated by Feel No Pain). Cybernetica Cortex models with Unstable have a maximum Leadership "
        "of 7."),
    "Warp-Wings": (
        "Only for models with Daemonic Infusion (every model of a multi-model unit; not for models on an Abeyant). An "
        "Infantry model becomes Jump Infantry; a Monstrous Creature becomes a Flying Monster."),
    "Dark Invocation": (
        "The model is a Psyker of the purchased Mastery Level and selects its powers from the Malefic Daemonology "
        "discipline (ProHammer Core Rules). All its Psychic Tests are taken at Leadership 7; all other psychic rules "
        "apply normally."),
    "Scrapcode Covenant": (
        "MALIGNANT MACHINE-SPIRITS: at the beginning of the controlling player's Movement phase each friendly Vehicle or "
        "Cybernetica Cortex unit not within control range of a friendly Cortex Controller rolls once (per unit or "
        "squadron) on the Scrapcode Behaviour table: 1 System Lock (may not move, may shoot); 2-4 Nominal Function; 5 "
        "Manic Drive (must move as far as possible towards the nearest visible enemy, then shoots and charges normally); "
        "6 Weapons Frenzy (may not voluntarily move or charge; each model fires one ranged weapon twice at the nearest "
        "visible unit, friend or foe). SCRAPCODE INJECTION: a model with a Cortex Controller in base contact with an "
        "enemy Vehicle, Walker or Cybernetica Cortex model may, instead of firing in the Shooting phase (even while "
        "engaged), take a Leadership test; if passed roll a D6: 1-2 Static Corruption (non-vehicle Pinned, or a "
        "Suppression Token if immune; Vehicle Crew Shaken); 3-4 Motor Lock (may not voluntarily move next Movement "
        "phase); 5 Weapon Corruption (one ranged weapon may not fire next Shooting phase); 6 Machine Madness (rolls on "
        "the Scrapcode Behaviour table next turn, Dark Mechanicum player chooses). Failed on a double 6: the model "
        "suffers a Cybertheurgy Mishap."),
    "Engines of Ruin": (
        "RUINOUS IMPERATIVE: units with Iron and Machine or Cybernetica Cortex models, Vehicles and Tech-Thrall "
        "Covenants must shoot if they have an eligible target and must declare a Charge if able and an enemy is in "
        "range (Artillery, Immobile units and non-Walker Vehicles are never forced into charges they could not make). "
        "OVERLOAD PROTOCOLS: before such a unit fires, each model may overload one ranged weapon (+1 S, max 10); after "
        "its attacks roll a D6, on a 1 a non-vehicle model suffers a Wound (Armour Saves allowed) and a Vehicle an Engine "
        "Damaged result (not for S Special weapons, psychic powers, Ruinous Bombardment or weapons without S). "
        "DEATHWISH PROTOCOL: Tech-Thralls (one per five models, +5 each), Karkinos, Praetorians and Scyllax (any model, "
        "+10 each) may purchase Volatile Charges. CATASTROPHIC REACTORS: Reactor Blast becomes Catastrophic Reactor "
        "Blast (on 4+, S = Toughness max 10, AP3, Ordnance, Large Blast; Massive Blast on a natural 6). RUINOUS "
        "BOMBARDMENT: once per battle one Archmagos or Magos Dominus may call down a Ruinous Bombardment instead of "
        "firing (Unlimited, S9, AP3, Ordnance 1, Barrage, Large Blast, Pinning, One Use; no Line of Sight; on the "
        "battlefield, not Pinned, Falling Back or in combat)."),
    "Volatile Charge": (
        "Once per battle, after all Charge moves but before close-combat attacks, a unit with Volatile Charges that is "
        "engaged may detonate them: centre a Blast marker over each bearer (Volatile Charge - Self, S6, AP3, Blast, One "
        "Use); every model touched, friend or foe, is hit. The bearer is then removed as a casualty (no save of any "
        "kind) and makes no other attacks that phase."),
    "Flesh-Mechanica": (
        "HARVEST OF FLESH: the army must include at least one additional Adsecularis Tech-Thrall Covenant beyond its "
        "normal compulsory Troops requirements (it uses a Troops choice). FLESHCRAFT: after deployment roll on the "
        "Fleshcraft Mutation table for every Tech-Thrall Covenant: 1 Lobotomised (Fearless, -1 I); 2 Muscle-grafted "
        "(+1 S); 3 Bloated (+1 T, -1 I); 4 Accelerated Reflexes (+1 I); 5 Ravener Strain (+1 A, Furious Charge); 6 "
        "Monstrous Growth (+1 S, +1 T, Bulky); no characteristic above 10. RECLAMATION VATS: the first time a Tech-Thrall "
        "Covenant is destroyed, roll a D6 at the beginning of each subsequent friendly turn; on a 5+ it returns from the "
        "controlling player's table edge with half its starting models (rounding up), keeping its wargear, upgrades "
        "and mutation, counting as arriving from Reserves, unable to charge that turn (once per battle; Victory Points "
        "only once). ABOMINABLE RECONSTRUCTION: units in the cost table may purchase one Reconstruction (every model "
        "the same): Predatory (Armour Save worsened by one, +1 I, +1 A), Massive (+1 T, -1 I), Bestial (remove one "
        "ranged weapon; gains Fleet and Furious Charge). NO ENGINES GREATER THAN FLESH: no Thanatar-Cavas, -Calix or "
        "-Cynis, and no more than one Heavy Support choice containing Cybernetica Cortex models."),
    "Possessed Battle-Automata": "Dark Mechanicum unit - Daemon Engine Horde only.",
    "Fleshcrafted Brutes": (
        "After deployment but before the first turn this unit rolls once on the Fleshcraft Mutation table; the result "
        "may be re-rolled once (the second result must be accepted)."),
    "Scrapcode Emanation": (
        "At the beginning of the enemy Movement phase nominate one enemy Vehicle, Walker or Cybernetica Cortex unit within "
        "6\"; on a 4+ it must immediately roll once on the Scrapcode Behaviour table (the Dark Mechanicum player makes "
        "any choices)."),
    "Machine Revenants": (
        "Scrapcode Revenants do not require a Cortex Controller, are never subject to Programmed Behaviour and may never "
        "Score or Contest objectives."),
    "Scrapcode Injector": (
        "Instead of firing in the Shooting phase, a Scrapcode Hunter may attempt a Scrapcode Injection against an "
        "eligible enemy model within 6\", exactly as the Scrapcode Covenant rule but without base contact."),
    "Daemon Engine": "This model counts as a Daemon Engine for all Dark Mechanicum rules, including Malefic Cybertheurgy.",
    "Catastrophic Explosion": (
        "When the Brass Scorpion is destroyed roll a D6 before removing it: on a 4+ every model touched by a Large Blast "
        "marker centred over it suffers a S8 AP3 Ordnance hit (Massive Blast on a natural 6)."),
    "Overcharged Reactor": (
        "When firing its Infernal Bombard the controlling player may overcharge it: +1 Strength and AP improved by one "
        "for that attack; afterwards roll a D6, on a 1-2 the Infernal Siege Engine suffers an Engine Damaged result."),
    "Catastrophic Detonation": (
        "When the Infernal Siege Engine is destroyed roll a D6: on a 5+ (4+ in an Engines of Ruin army) every model "
        "touched by a Large Blast marker centred over it suffers a S8 AP3 hit."),
    # ------------------------------------------------------------ named characters
    "Master of Mondus Gamma": (
        "Lukas Chrom may re-roll failed Battlesmith repair rolls. When he successfully uses Battlesmith on a friendly "
        "Vehicle or Cybernetica Cortex model, it regains one additional lost Wound or repairs one additional eligible "
        "Vehicle Damage result."),
    "Lord of the Automata": (
        "Lukas Chrom's Cortex Controller has an 18\" range and he may perform Cybertheurgic Rites on friendly Cybernetica "
        "Cortex units within 24\"."),
    "Architect of Kaban": (
        "The Kaban Machine may only be selected in an army which includes Lukas Chrom; it does not occupy a Heavy "
        "Support choice."),
    "Abominable Intelligence": (
        "The Kaban Machine is not subject to Programmed Behaviour and never requires a Cortex Controller. It is not "
        "treated as having Cybernetica Cortex for rules which require or affect it and may not be targeted by "
        "Cybertheurgic Rites unless a rule states otherwise."),
    "Hunter-Killer Logic": (
        "After both armies have deployed, nominate one enemy Independent Character, Monstrous Creature, Walker or "
        "Vehicle; the Kaban Machine may re-roll To Hit rolls of 1 against it (no new target if it is destroyed)."),
    "Independent Targeting": (
        "The Kaban Machine may fire up to two ranged weapons in each Shooting phase, at different enemy units if desired."),
    "The Tyrant of Xana": (
        "If Anacharis Scoria is included in a Mechanicum Primary Detachment and is eligible to be the Warlord, he must "
        "be the Warlord."),
    "Entropic Destroyer": (
        "Each unsaved Wound caused by the Vodian Sceptre inflicts D3 Wounds. Against Vehicles, each Glancing or "
        "Penetrating Hit rolls twice on the Damage table, using the higher result. These Wounds may not be ignored by "
        "Feel No Pain nor restored by It Will Not Die, Battlesmith or similar rules."),
    "Patris Cybernetica (Scoria)": (
        "Anacharis Scoria may join friendly units composed entirely of Cybernetica Cortex models, even Monstrous "
        "Creatures; while joined they are a single unit for all normal purposes."),
    "Rite of the Beast": (
        "When Scoria would perform the Rite of Celerity he may instead attempt the Rite of the Beast (Cybertheurgy test "
        "at -2 Leadership). If successful the target gains Fleet, +1 Initiative and re-rolls failed close-combat To Hit "
        "rolls until the beginning of the controlling player's next turn; when the effect ends roll a D6 per surviving "
        "model, on a 1 it suffers a Wound with no Armour Save (Invulnerable Saves allowed). Double 6: Mishap as normal."),
    "Forbidden Protocols": (
        "Whenever a friendly Cybernetica Cortex unit of Scoria's Detachment is outside the control range of a friendly "
        "Cortex Controller, its Programmed Behaviour is replaced by: Movement - must move towards the nearest visible "
        "enemy unit if able; Shooting - must fire at the nearest eligible enemy unit if able; Assault - must charge the "
        "nearest eligible enemy unit in charge range if able. Paragons of Metal are unaffected."),
    "The Homonculex": (
        "An army containing Anacharis Scoria may include one Arlatax known as the Homonculex, at the normal Arlatax cost "
        "and using a Fast Attack choice. It gains Paragon of Metal and Rage at no cost. If Scoria is slain the "
        "Homonculex is immediately removed as a casualty."),
    "Xanathite Abeyant": (
        "Scoria gains +1 Wound, +1 Attack, It Will Not Die, Move Through Cover, Very Bulky, Xanathite Plating (failed "
        "Armour Saves against Blast or Template weapons may be re-rolled) and a Photon Thruster, which may be fired in "
        "addition to any other ranged weapons he may fire."),
    "Fabricator-General of Mars": (
        "Kelbor-Hal must be the army's Warlord and counts as an Archmagos for all rules and army construction purposes, "
        "fulfilling any requirement that the army be led by an Archmagos or Magos Dominus. An army led by Kelbor-Hal may "
        "be designated Dark Mechanicum and select one Dark Techno-Arcana normally."),
    "Open the Forbidden Vaults": (
        "After selecting the army's Dark Techno-Arcana, choose one Forbidden Edict corresponding to a different Dark "
        "Techno-Arcana: Daemonic Edict - one eligible unit may purchase Daemonic Infusion at the normal cost; Scrapcode "
        "Edict - one friendly Mechanicum Independent Character with a Cortex Controller gains Scrapcode Injection; Ruinous "
        "Edict - one eligible friendly unit may use Overload Protocols; Fleshcraft Edict - one eligible unit may purchase "
        "one Abominable Reconstruction at the normal cost."),
    "Dark Cybertheurgy": (
        "Kelbor-Hal may use Cybertheurgic Rites on friendly Daemon Engines within range as if they had Cybernetica "
        "Cortex; a test against a Daemon Engine failed on any double suffers a Cybertheurgy Mishap."),
    "Electro-Arc of Mars": (
        "Once in each friendly Shooting phase, instead of firing, Kelbor-Hal may choose one enemy unit within 24\" and "
        "Line of Sight and take a Leadership test; if passed resolve the Electro-Arc of Mars (24\", S7, AP3, Assault D6, "
        "Haywire, Arc Discharge: if it causes at least one unsaved Wound, Glancing or Penetrating Hit, on a 4+ it leaps "
        "once to the nearest enemy unit within 6\" of the target). Failed on a double 6: Kelbor-Hal suffers one Wound "
        "with no Armour Save (Invulnerable Saves allowed)."),
    "Fabricator-Locum of Mars": (
        "Zagreus Kane must be the army's Warlord and counts as an Archmagos for all rules and army construction purposes, "
        "fulfilling any requirement that the army be led by an Archmagos or Magos Dominus. A Mechanicum army led by Kane "
        "must be Loyalist."),
    "Synod of the Loyal Mechanicum": (
        "An army led by Zagreus Kane may select two different Orders of High Techno-Arcana and must fulfil the "
        "Restrictions of both (combinations whose Restrictions cannot both be fulfilled may not be chosen). Bonuses of "
        "the two Orders that modify the same characteristic, ability or effect do not stack unless stated otherwise."),
    "The Great Noospheric Conclave": (
        "While Kane is on the battlefield, friendly Mechanicum Independent Characters with Battlesmith gain "
        "Cybertheurgist, and a friendly Cybertheurgist within 18\" of Kane may re-roll a failed Cybertheurgy test "
        "(double 6 on the re-roll: Mishap). NOOSPHERIC CYBER-CONTROL: Cortex Controllers carried by friendly Mechanicum "
        "Independent Characters in Kane's Detachment have +6\" range (max 24\"); Rite range is not increased."),
    "Master of Mondus Occulam": (
        "Kane and friendly Battlesmiths within 12\" of him may re-roll failed repair rolls. Once in each friendly "
        "Shooting phase, when Kane or a friendly Battlesmith within 12\" successfully repairs a model, Kane may enhance "
        "the repair: a non-Vehicle regains one additional Wound, a Vehicle repairs one additional eligible Damage result "
        "(once per model per turn)."),
    "Lord of Ruin": (
        "Calleb Decima counts as an Archmagos for all rules and army construction purposes; if included in a Primary "
        "Detachment and eligible he must be the Warlord. An army led by him must select the Ordo Reductor Order, and he "
        "fulfils its Warlord requirement. Enhanced Master of Destruction: he may nominate up to two friendly Mechanicum "
        "Artillery units or units firing Ordnance or Barrage weapons within 18\"; each may re-roll the Scatter die for "
        "one Blast weapon that phase (second result stands)."),
    "Walker in Ruin": (
        "Calleb Decima and friendly Mechanicum units with at least one model within 6\" of him gain Move Through Cover "
        "and may re-roll failed Pinning tests."),
    "Curse of the Omnissiah": (
        "Once per battle, instead of firing his other ranged weapons, Decima may fire the Curse of the Omnissiah (18\", "
        "S3, AP3, Heavy 2D6, Haywire, Gets Hot, One Use); it counts as a weapon fired by him and Relentless allows it "
        "after moving."),
    "Calculated Devastation": (
        "Once in each friendly Shooting phase, after the final Scatter of a friendly Mechanicum Blast or Barrage weapon "
        "within 18\" of Decima is determined (also after a Master of Destruction re-roll), he may reduce the distance "
        "scattered by D6\" (minimum 0)."),
    "Guardian Retinue": (
        "An army containing Calleb Decima may include one Tech-Priest Auxilia or one Scyllax Guardian-Automata Covenant "
        "as his Guardian Retinue; it is purchased and upgraded normally but does not occupy an additional Force "
        "Organisation choice. Decima must begin the battle joined to it and may not voluntarily leave it."),
}

# ==================================================================== WEAPONS
_LA_SIMPLE = ["Bolt Pistol", "Bolter", "Storm Bolter", "Flamer", "Hand Flamer", "Heavy Flamer", "Plasma Pistol",
              "Plasma Gun", "Plasma Blaster", "Plasma Cannon", "Meltagun", "Multi-Melta", "Volkite Serpenta",
              "Volkite Charger", "Volkite Caliver", "Volkite Culverin", "Graviton Gun", "Graviton Cannon",
              "Autocannon", "Rotor Cannon", "Lascannon", "Twin-linked Heavy Bolter", "Twin-linked Lascannon",
              "Twin-linked Autocannon", "Twin-linked Heavy Flamer", "Twin-linked Volkite Culverin", "Assault Cannon",
              "Demolisher Cannon", "Quad Lascannon", "Chainfist", "Power Fist", "Lightning Claw", "Relic Blade",
              "Close Combat Weapon", "Chainaxe", "Hunter-Killer Missile"]

WEAPONS = {n: LA[n] for n in _LA_SIMPLE}
WEAPONS.update({
    "Heavy Bolter": ('36"', "5", "4", "Heavy 3"),
    "Power Weapon": ("-", "User", "-", "Power Weapon"),
    "Laspistol": ('12"', "3", "-", "Pistol"),
    "Lasgun": ('24"', "3", "-", "Rapid Fire"),
    "Multilaser": ('36"', "6", "6", "Heavy 3"),
    "Shotgun": ('12"', "3", "-", "Assault 2"),
    "Maxima Bolter": ('12"', "4", "5", "Assault 3"),
    "Phased Plasma-Fusil": ('24"', "6", "3", "Salvo 2/3"),
    "Inferno Pistol": ('6"', "8", "2", "Pistol, Melta"),
    "Graviton Imploder": ('18"', "Special", "2", "Salvo 2/4, Concussive, Graviton"),
    "Archaeotech Pistol": ('12"', "6", "3", "Pistol, Master-crafted"),
    "Lucifex": ('6"', "2", "2", "Pistol, Fleshbane, Rad-phage"),
    "Photon Gauntlet": ('12"', "5", "2", "Assault 2, Blind, Gets Hot"),
    "Photon Thruster": ('48"', "6", "2", "Heavy 2, Lance, Blind, Gets Hot"),
    "Irad Cleanser": ("Template", "2", "5", "Assault 1, Fleshbane, Rad-phage"),
    "Lightning Gun": ('18"', "6", "4", "Assault 2"),
    "Radium Carabiner": ('18"', "4", "4", "Assault 1"),
    "Radium Pistol": ('12"', "4", "4", "Pistol"),
    "Darkfire Cannon": ('60"', "7", "2", "Heavy 2, Lance, Blind, Gets Hot"),
    "Irradiation Engine": ("Template", "4", "3", "Heavy 1, Torrent, Fleshbane, Rad-phage"),
    "Galvanic Rifle": ('30"', "4", "4", "Rapid Fire"),
    "Arc Rifle": ('24"', "6", "5", "Rapid Fire, Haywire"),
    "Arc Pistol": ('12"', "6", "5", "Pistol, Haywire"),
    "Phosphor Blast Pistol": ('12"', "5", "4", "Pistol, Luminagen"),
    "Flak Missiles": ('48"', "7", "4", "Heavy 1, Skyfire"),
    "Shattersphere Grenades": ('8"', "4", "5", "Assault 1, Blast, Pinning, Rad Poisoning"),
    "Mechanicum Axe": ("-", "User", "-", "Power Weapon, Mechanicum Axe"),
    "Corposant Stave": ("-", "User +1", "-", "Two-Handed, Concussive, Haywire, Rending"),
    "Electro Stave": ("-", "Special", "-", "Two-Handed, Rending, Electro Stave"),
    "Taser Goad": ("-", "User +2", "-", "Melee, Taser"),
    "Arc Maul": ("-", "User +2", "-", "Melee, Concussive, Haywire"),
    "Explorator Arquebus": ('36"', "Special", "4", "Heavy 1, Sniper, Rending"),
    "Ordinator Bombardment": ("Unlimited", "8", "3", "Ordnance 1, Large Blast, Barrage"),
    "Ordinator Bombardment (Ordinator Order)": ("Unlimited", "8", "3",
                                                "Ordnance 1, Large Blast, Barrage, Lance, Twin-linked"),
    "Breacher Charge": ("-", "10", "1", "Melee, Armourbane, Wrecker, One Use"),
    "Phosphex Bomb": ('6"', "5", "2", "Assault 1, Blast, Poisoned (3+), Lingering Death, One Use"),
    "Rad Missiles": ('48"', "4", "3", "Heavy 1, Blast, Fleshbane, Rad-phage"),
    "Phosphex Missiles": ('24"', "Special", "3", "Heavy 1, Blast, Poisoned (3+), Crawling Fire, Lingering Death"),
    "Scyllax Bolter": ('30"', "4", "4", "Rapid Fire"),
    "Mechadendrite Combat Array": ("-", "User", "-", "Melee, Maelstrom, Dismemberment"),
    "Graviton Hammers": ("-", "10", "-", "Melee, Concussive, Wrecker"),
    "Siege Wrecker": ("-", "10", "-", "Melee, Unwieldy, Armourbane"),
    "Voltlock Arquebus": ('18"', "5", "5", "Assault 2, Rending"),
    "Voltlock Handgun": ('12"', "5", "5", "Pistol, Rending"),
    "Las-lock": ('18"', "4", "6", "Assault 1"),
    "Heavy Chainblade": ("-", "User +2", "4", "Melee, Two-Handed"),
    "Mauler Bolt Cannon": ('24"', "6", "4", "Heavy 3"),
    "Twin-linked Mauler Bolt Cannon": ('24"', "6", "4", "Heavy 3, Twin-linked"),
    "Shock Chargers": ("-", "User +1", "-", "Melee, Concussive"),
    "Battle-Automata Power Blades": ("-", "User", "-", "Melee, Rending, Paired"),
    "Plasma Caster": ('36"', "7", "2", "Heavy 2, Blast, Gets Hot"),
    "Volkite Sentinel": ('15"', "5", "5", "Assault 2, Rending"),
    "Twin-linked Volkite Charger": ('15"', "5", "5", "Assault 2, Rending, Twin-linked"),
    "Two Heavy Flamers": ("Template", "5", "4", "Assault 1"),
    "Two Lightning Claws": ("-", "User", "-", "Power Weapon, re-roll failed To Wound rolls, Specialist Weapon"),
    "Two Power Fists": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon"),
    "Twin-linked Multilaser": ('36"', "6", "6", "Heavy 3, Twin-linked"),
    "Two Twin-linked Rotor Cannons": ('30"', "3", "6", "Salvo 3/4, Twin-linked"),
    "Twin-linked Photon Thruster": ('48"', "6", "2", "Heavy 2, Lance, Blind, Gets Hot, Twin-linked"),
    "Bio-corrosive Ammunition": ('15"', "3", "6", "Salvo 3/4, Poisoned (4+)"),
    "Arlatax Power Claw": ("-", "User +2", "-", "Melee, Shred"),
    "Arc Scourge": ("-", "User", "-", "Melee, Rampage, Armourbane, Concussive"),
    "Vultarax Arc Blaster": ('24"', "6", "5", "Heavy 3, Shred, Haywire"),
    "Setheno Pattern Havoc Launcher": ('48"', "5", "5", "Heavy 2, Blast, Twin-linked, Setheno-Djinn"),
    "Two Power Swords": ("-", "User", "-", "Power Weapon"),
    "Internal Demolition Charge": ("Self", "8", "2", "Ordnance, Large Blast"),
    "Sollex Pattern Heavy Lascannon": ('60"', "10", "2", "Heavy 1"),
    "Cynis Pattern Plasma Ejector": ('18"', "8", "2", "Heavy 1, Blast, Gets Hot, Plasma Wave"),
    "Lightning Cannon": ('48"', "7", "3", "Heavy 1, Large Blast, Rending, Shred"),
    "Pulsar-Fusil": ('36"', "9", "2", "Ordnance 4"),
    "Karacnos Mortar Battery": ('60"', "5", "4", "Heavy 3, Barrage, Blast, Fleshbane, Rad-phage, Ignores Cover, Pinning"),
    "Lightning-Blaster Sentinel": ('18"', "7", "5", "Heavy 3, Shred, Rending"),
    "Battle Cannon": ('72"', "8", "3", "Ordnance 1, Large Blast"),
    "Conqueror Cannon": ('48"', "7", "4", "Heavy 1, Blast"),
    "Vanquisher Battle Cannon": ('72"', "8", "2", "Heavy 1, Armourbane"),
    "Twin-linked Phased Plasma-Fusil": ('24"', "6", "3", "Salvo 2/3, Twin-linked"),
    "Twin-linked Irad Cleanser": ("Template", "2", "5", "Assault 1, Fleshbane, Rad-phage, Twin-linked"),
    "Two Twin-linked Mauler Bolt Cannons": ('24"', "6", "4", "Heavy 3, Twin-linked"),
    "Two Twin-linked Lascannons": ('48"', "9", "2", "Heavy 1, Twin-linked"),
    "Two Lascannons": ('48"', "9", "2", "Heavy 1"),
    "Two Irradiation Engines": ("Template", "4", "3", "Heavy 1, Torrent, Fleshbane, Rad-phage"),
    "Dual Melta Cannon": ('24"', "8", "1", "Heavy 1, Blast, Melta, Twin-linked"),
    "Earthshaker Cannon": ('36-120"', "9", "3", "Ordnance 1, Barrage, Large Blast"),
    "Medusa Cannon": ('36"', "10", "2", "Ordnance 1, Barrage, Large Blast"),
    "Mars-Colossus Bombard": ('12-72"', "7", "3", "Ordnance 2, Barrage, Large Blast, Concussive, Pinning"),
    "Dual Earthshaker Cannon": ('24-240"', "9", "3", "Ordnance 1, Barrage, Massive Blast, Twin-linked"),
    "Pintle-mounted Storm Bolter": ('24"', "4", "5", "Assault 2"),
    "Pintle-mounted Heavy Bolter": ('36"', "5", "4", "Heavy 3"),
    "Pintle-mounted Heavy Flamer": ("Template", "5", "4", "Assault 1"),
    "Pintle-mounted Phased Plasma-Fusil": ('24"', "6", "3", "Salvo 2/3"),
    "Hull-mounted Heavy Bolter": ('36"', "5", "4", "Heavy 3"),
    "Hull-mounted Heavy Flamer": ("Template", "5", "4", "Assault 1"),
    "Hull-mounted Lascannon": ('48"', "9", "2", "Heavy 1"),
    "Two Heavy Bolters (sponsons)": ('36"', "5", "4", "Heavy 3"),
    "Two Heavy Flamers (sponsons)": ("Template", "5", "4", "Assault 1"),
    "Two Multi-Meltas (sponsons)": ('24"', "8", "1", "Heavy 1, Melta"),
    "Two Plasma Cannons (sponsons)": ('36"', "7", "2", "Heavy 1, Blast, Gets Hot"),
    "Twin-linked Typhoon Missile Launcher": None,  # multi profile below
    "Heavy Stubber": ('36"', "4", "6", "Heavy 3"),
    "Two Rotor Cannons": ('30"', "3", "6", "Salvo 3/4"),
    "Two Setheno Pattern Havoc Launchers": ('48"', "5", "5", "Heavy 2, Blast, Twin-linked, Setheno-Djinn"),
    "Two Cynis Pattern Plasma Ejectors": ('18"', "8", "2", "Heavy 1, Blast, Gets Hot, Plasma Wave"),
    "Two Lightning-Blaster Sentinels": ('18"', "7", "5", "Heavy 3, Shred, Rending"),
    # Dark Mechanicum
    "Possessed Power Claw": ("-", "User +2", "Power Weapon", "Melee, Shred, Specialist Weapon"),
    "Warp-spitter": ('18"', "5", "4", "Assault 2, Rending"),
    "Abominant Claws": ("-", "User +1", "-", "Melee, Rending"),
    "Industrial Stubber": ('18"', "4", "6", "Assault 2"),
    "Scrapcode Projector": ('18"', "4", "5", "Assault 1, Haywire"),
    "Electro-blade": ("-", "User +1", "-", "Melee, Haywire"),
    "Crude Firearm": ('18"', "3", "6", "Assault 1"),
    "Stalker Claws": ("-", "User +1", "-", "Melee, Rending"),
    "Daemonspitter": ('18"', "5", "4", "Assault 2"),
    "Slaughterer Claws": ("-", "User +2", "-", "Melee, Shred, Paired"),
    "Hunter Arc Carbine": ('24"', "6", "5", "Assault 2, Haywire"),
    "Manipulator Claws": ("-", "User +1", "-", "Melee, Rending"),
    "Greater Engine Claws": ("-", "10", "-", "Melee, Armourbane, Wrecker"),
    "Scorpion Cannon": ('36"', "8", "3", "Heavy 4, Rending"),
    "Two Hellmaw Flamers": ("Template", "6", "4", "Assault 1"),
    "Two Scorpion Claws": ("-", "10", "-", "Melee, Armourbane"),
    "Infernal Bombard": ('24-72"', "9", "3", "Ordnance 1, Barrage, Large Blast, Pinning"),
    "Colossal Claws": ("-", "10", "-", "Melee, Wrecker"),
    "Bio-mechanical Cannon": ('24"', "6", "4", "Assault 3, Poisoned (4+)"),
    "Irradiated Bile Projector": ("Template", "5", "4", "Assault 1, Fleshbane"),
    "Bone-scythe Mutation": ("-", "User +1", "-", "Melee, Rending"),
    "Volatile Charge": ("Self", "6", "3", "Blast, One Use"),
    # named characters
    "Two Kaban Power Claws": ("-", "10", "-", "Power Weapon, Armourbane"),
    "Vodian Sceptre": ("-", "User +2", "-", "Power Weapon, Two-Handed, Armourbane, Entropic Destroyer"),
    "Two Archaeotech Pistols": ('12"', "6", "3", "Pistol, Master-crafted"),
    "Master-crafted Bolt Pistol": ('12"', "4", "5", "Pistol, Master-crafted"),
    "Master-crafted Power Weapon": ("-", "User", "-", "Power Weapon, Master-crafted"),
    "Electro-Arc of Mars": ('24"', "7", "3", "Assault D6, Haywire, Arc Discharge"),
    "Curse of the Omnissiah": ('18"', "3", "3", "Heavy 2D6, Haywire, Gets Hot, One Use"),
})
del WEAPONS["Twin-linked Typhoon Missile Launcher"]

MULTI = {
    "Missile Launcher": {"Missile Launcher - Frag": LA["Missile Launcher - Frag"],
                         "Missile Launcher - Krak": LA["Missile Launcher - Krak"]},
    "Missile Launcher with Frag, Krak and Ignis-Frag Missiles": {
        "Missile Launcher - Frag": LA["Missile Launcher - Frag"],
        "Missile Launcher - Krak": LA["Missile Launcher - Krak"],
        "Missile Launcher - Ignis-Frag": ('48"', "5", "6", "Heavy 1, Blast, Ignores Cover")},
    "Twin-linked Typhoon Missile Launcher": {
        "Twin-linked Typhoon Missile Launcher - Frag": ('48"', "4", "6", "Heavy 2, Blast, Twin-linked"),
        "Twin-linked Typhoon Missile Launcher - Krak": ('48"', "8", "3", "Heavy 2, Twin-linked")},
    "Conversion Beamer": {k_: LA[k_] for k_ in ['Conversion Beamer (0-18")', 'Conversion Beamer (18-42")',
                                                 'Conversion Beamer (42-72")']},
    "Arc Lance": {"Arc Lance - Ranged": ('12"', "6", "5", "Assault 1, Haywire"),
                  "Arc Lance - Melee": ("-", "User +1", "5", "Melee, Haywire")},
    "Galvanic Caster with Flechette and Ignis Ammunition": {
        "Galvanic Caster - Flechette": ('24"', "3", "6", "Rapid Fire, Shred"),
        "Galvanic Caster - Ignis": ('18"', "2", "5", "Assault 2, Blind, Ignores Cover")},
    "Hammershot Ammunition": {"Galvanic Caster - Hammershot": ('30"', "4", "3", "Assault 1")},
    "Volkite Incinerator": {"Volkite Incinerator - Beam": ('10"', "5", "5", "Assault 2, Rending"),
                            "Volkite Incinerator - Point-Blank Blast": ("-", "6", "Power Weapon",
                                                                       "Melee, Instant Death, Prisoned")},
    "Hellex Plasma Mortar": {"Hellex Plasma Mortar - Stationary": ('12-48"', "8", "2",
                                                                   "Ordnance 1, Barrage, Large Blast, Plasma Wave"),
                             "Hellex Plasma Mortar - Moved": ('12-24"', "8", "2",
                                                              "Ordnance 1, Barrage, Large Blast, Plasma Wave")},
    "Graviton Ram": {"Graviton Ram - Ranged": ("Template", "Special", "4", "Heavy 1, Concussive, Graviton"),
                     "Graviton Ram - Melee": ("-", "10", "-", "Melee, Armourbane, Concussive, Wrecker")},
    "Whirlwind Launcher with Vengeance and Castellan Missiles": {
        "Whirlwind - Vengeance Warhead": LA["Whirlwind - Vengeance Warhead"],
        "Whirlwind - Castellan Warhead": LA["Whirlwind - Castellan Warhead"]},
    "Machinator Array": {"Machinator Array": ("-", "User +1", "-", "Power Weapon, Unwieldy, Shred, Armourbane"),
                         "Flamer": LA["Flamer"], "Inferno Pistol": ('6"', "8", "2", "Pistol, Melta")},
    "Servo-Rig": {"Servo-Rig": ('3"', "8", "2", "Heavy 1")},
    "Kaban Integrated Heavy Weapon Systems": {
        "Kaban Autocannon": ('48"', "7", "4", "Heavy 2"),
        "Kaban Plasma Blaster": ('18"', "7", "2", "Assault 2, Gets Hot"),
        "Kaban Heavy Flamer": ("Template", "5", "4", "Assault 1")},
    "Krak Grenades": {"Krak Grenade": LA["Krak Grenade"]},
    "Melta Bombs": {"Melta Bomb": LA["Melta Bomb"]},
    "Ordo Reductor War Munitions": {"Breacher Charge": ("-", "10", "1", "Melee, Armourbane, Wrecker, One Use"),
                                    "Phosphex Bomb": ('6"', "5", "2",
                                                      "Assault 1, Blast, Poisoned (3+), Lingering Death, One Use")},
    "Multi-Melta and Searchlight": {"Multi-Melta": LA["Multi-Melta"]},
}

WARGEAR = {
    "Power Armour": "3+ Armour Save.",
    "War Plate": "4+ Armour Save.",
    "Hardened Armour": ("3+ Armour Save. Failed Armour Saves against Blast or Template weapons may be re-rolled; when "
                        "the model Advances reduce the extra distance rolled by 1\"; reduce Charge and Pursuit distances "
                        "by 1\"."),
    "Artificer Armour": "2+ Armour Save.",
    "Flak Armour": "5+ Armour Save.",
    "Carapace Armour": ("4+ Armour Save. When purchased as an upgrade to Flak Armour it replaces that armour. A "
                        "Tech-Thrall Covenant buys it for 20 points for the entire unit, whatever its size."),
    "Refractor Field": "5+ Invulnerable Save.",
    "Conversion Field": "4+ Invulnerable Save.",
    "Mechanicum Protectiva": "4+ Invulnerable Save. This save may be improved by a Cyber-familiar.",
    "Augmetic Ward": "6+ Invulnerable Save.",
    "Force Shield": ("4+ Invulnerable Save. When the Electro-Priests' unit completely destroys an enemy unit in close "
                     "combat, Siphoned Vigour improves this Invulnerable Save to 3+ for the rest of the battle."),
    "Mag-inverter Shield": ("5+ Invulnerable Save. A model carrying it may not claim the +1 Attack for fighting with two "
                            "close combat weapons."),
    "Kyropatris Field Generator": ("If a unit contains at least five models with Kyropatris Field Generators, its models "
                                   "may re-roll Armour Saves of 1. With at least ten, reduce the Strength of shooting "
                                   "attacks against the unit by 1 (minimum 1)."),
    "Purity Seals": ("When a unit containing one or more models with Purity Seals rolls its Fall Back distance, roll one "
                     "additional D6 and discard one die of the controlling player's choice before adding the remaining "
                     "dice together (e.g. 3D6, keep two). Multiple sets in the same unit provide only one additional "
                     "die. This does not alter Morale, Pinning, Regroup or Pursuit rolls."),
    "Lorica Thallax": ("4+ Armour Save and Feel No Pain (6+). A model with Lorica Thallax may not make Pursuit moves. "
                       "Restricted to Thallax and units whose entry permits it."),
    "Atomantic Shielding": "5+ Invulnerable Save against shooting attacks, 6+ against close-combat attacks.",
    "Abeyant": "The model gains +1 Wound, It Will Not Die, Move Through Cover and Very Bulky.",
    "Bionics": ("When the model loses its final Wound, leave it on its side; at the beginning of its controlling "
                "player's next turn roll a D6: on a 6 it returns with 1 Wound, otherwise it is removed. Not usable if "
                "the entire unit was destroyed at the same time (an Independent Character that was the last survivor "
                "may still try)."),
    "Cyber-familiar": ("Improves the model's Invulnerable Save by +1 (max 3+), or gives a 6+ Invulnerable Save if it has "
                       "none. The model may re-roll failed Characteristic Tests except Leadership and Dangerous Terrain "
                       "tests. Not a separate model."),
    "Mechadendrites": "May re-roll one failed Armour Save per phase.",
    "Machinator Array": ("+1 Toughness, Night Vision and +2 to Battlesmith repair rolls. Incorporates a Flamer and an "
                         "Inferno Pistol: the bearer may fire both instead of another ranged weapon, or one of them and "
                         "one other ranged weapon. Also makes two additional close-combat attacks each Assault phase "
                         "with the Machinator Array profile."),
    "Rad Furnace": ("Enemy non-vehicle models engaged in the same close combat suffer -1 Toughness. The bearer is "
                    "unaffected by Rad Furnaces and Rad Grenades, and Poisoned or Rad-phage attacks only wound it on an "
                    "unmodified 6."),
    "Servo-Arm": ("+1 to Battlesmith repair rolls. Makes one additional close-combat attack each Assault phase which "
                  "always hits on a 4+, counts as a Power Fist and gains no charge or two-weapon bonus."),
    "Cortex Controller": ("At the start of each phase, a friendly unit with Cybernetica Cortex with at least one model "
                          "within 12\" of a friendly Cortex Controller ignores Programmed Behaviour for that phase."),
    "Signum": ("Once in each friendly Shooting phase the bearer's unit may re-roll one failed To Hit roll with a shooting "
               "weapon (any model of the unit). A unit benefits from only one Signum per Shooting phase."),
    "Nuncio Vox": ("A friendly unit arriving by Deep Strike does not scatter if its first model is placed within 6\" of "
                   "the bearer. Only if the bearer was on the battlefield at the start of the turn and is not Pinned, "
                   "Falling Back or embarked."),
    "Cognis Signum": ("The bearer counts as having a Nuncio Vox with a 12\" no-scatter range and has Night Vision. "
                      "Where specifically stated it also provides the benefits of a Signum."),
    "Djinn-skein": ("Counts as a Signum and a Nuncio Vox with a 12\" no-scatter range. If the bearer controls "
                    "Cyber-occularis, the Nuncio Vox may be measured from the bearer or any of them."),
    "Auspex": ("After enemy Infiltrators deploy, roll 4D6 for each unit with an Auspex: if an enemy Infiltrating unit is "
               "within that distance and Line of Sight of the bearer, the bearer's unit may fire at it once before the "
               "battle (one Auspex attack per unit). Replaces the Augury Scanner."),
    "Omnispex": "The bearer may detect Hidden units within 18\", even if they could not normally be detected.",
    "Infravisor": "Night Vision. When resolving a test caused by the Blind special rule the bearer counts as Initiative 1.",
    "Enhanced Targeting Array": "May re-roll one failed To Hit roll with a shooting weapon in each Shooting phase.",
    "Djinn-sight": "Night Vision; may re-roll failed rolls to detect Hidden units.",
    "Cyber-occularis": ("A small autonomous sensor construct: WS2 BS3 S2 T3 W1 I4 A1 Ld9 Sv3+, Jet Pack Infantry, Fearless, "
                        "Stealth. It may not Score or Contest objectives, join or be joined by another unit, and does "
                        "not block Line of Sight. It acts as a remote relay for its owner's Djinn-skein."),
    "Frag Grenades": "Normal ProHammer Frag (Assault) Grenades. Against vehicles: Strength 4 + D6 Armour Penetration.",
    "Rad Grenades": ("Neither Assault nor Defensive Grenades. In a player turn in which the unit charges or is charged, "
                     "enemy non-vehicle models engaged with it suffer -1 Toughness until the end of the Assault phase "
                     "(for all purposes, including Instant Death). Not cumulative between units."),
    "Jump Pack": "The model becomes Jump Infantry.",
    "Jet Pack": "The model becomes Jet Pack Infantry.",
    "Master-crafted Weapon": ("One weapon carried by the model is Master-crafted: it may re-roll one failed To Hit roll "
                              "per player turn (not grenades, Melta Bombs or other expendable equipment)."),
    "Induction Chargers": "Las-locks carried by models with Induction Chargers become Assault 2 instead of Assault 1.",
    "Enhanced Combat Array": "A model with an Enhanced Combat Array gains +1 Attack.",
    "Dozer Blade": "The vehicle may re-roll failed Dangerous Terrain tests caused by moving through terrain.",
    "Extra Armour": "The vehicle treats Crew Stunned results as Crew Shaken.",
    "Searchlight": ("During Night Fighting the vehicle may illuminate a unit it shoots at (it may be targeted normally "
                    "for the rest of the phase); a vehicle using it may itself be targeted normally until its next turn."),
    "Smoke Launchers": ("Once per battle, after moving, Penetrating Hits from shooting against the vehicle count as "
                        "Glancing Hits until the beginning of its next turn."),
    "Blessed Autosimulacra": ("At the beginning of the controlling player's turn roll a D6 for a damaged vehicle: on a 6 "
                              "remove one Engine Damaged, Weapon Destroyed or Immobilised result (one per turn). "
                              "Vultarax: when it has lost one or more Wounds, roll a D6 at the beginning of the "
                              "controlling player's turn; on a 6 it regains one lost Wound (up to its starting Wounds); "
                              "it does not roll on the vehicle-damage repair list."),
    "Armoured Ceramite": "Melta weapons roll only one D6 for Armour Penetration against this vehicle, regardless of range.",
    "Flare Shield": ("Against shooting attacks which strike the vehicle's Front Armour, reduce the Strength of Blast and "
                     "Template weapons by 2 and of all other ranged attacks by 1. No effect in close combat."),
    "Rear-facing Flare Shield": ("A Flare Shield protecting the vehicle's Rear Armour (as Flare Shield, against attacks "
                                 "striking the Rear Armour)."),
    "Explorator Augury Web": ("The vehicle gains Scout. While it is on the battlefield, at the start of the controlling "
                              "player's turn before Reserve rolls choose: Disruption Mode (opponent -1 to Reserve rolls) "
                              "or Relay Mode (controlling player may re-roll failed Reserve rolls). Multiple webs give no "
                              "extra benefit; one mode per army at a time."),
    "Anbaric Claw": ("Once per player turn, when the vehicle is attacked in close combat or Rams / is Rammed, every unit "
                     "with a model within 1\" of its hull suffers D6 Strength 5 Rending hits (friend and foe; not "
                     "embarked models), resolved at Initiative 10 in an Assault. In a Ram the other vehicle also "
                     "suffers D6 S5 AP4 Rending hits."),
    "Auxiliary Drive": ("At the beginning of the controlling player's Movement phase, if the vehicle is Immobilised, roll "
                        "a D6: on a 4+ remove one Immobilised result."),
    "Servo-Rig": ("One model embarked within the Macrocarid may use Battlesmith on a friendly vehicle within 3\" of it "
                  "without disembarking (no bonuses from extra repair equipment). The Servo-Rig may also attack with its "
                  "own profile."),
    "Siege Plating": "Increase the vehicle's Front Armour from 12 to 13.",
    "Power of the Machine Spirit (upgrade)": ("The vehicle gains the Power of the Machine Spirit special rule.",
                                              ["Power of the Machine Spirit"]),
    "Void Shield": "One additional active Void Shield for the Void Shield Projector.",
    "Shock Ram": "See the Shock Ram special rule.",
    "Galvanic Traction Drive": "The vehicle may re-roll failed Dangerous Terrain tests.",
    "Daemonic Infusion": ("Gains Daemon and Unstable; see the Daemonic Infusion rule.", ["Daemon"]),
    "Warp-Wings": "Infantry become Jump Infantry; Monstrous Creatures become Flying Monsters.",
    "Predatory Reconstruction": ("The model's Armour Save is worsened by one (a worsened 6+ becomes no save); +1 "
                                 "Initiative, +1 Attack."),
    "Massive Reconstruction": "+1 Toughness (max 10), -1 Initiative (min 1).",
    "Bestial Reconstruction": ("The model permanently removes one ranged weapon it carries (controlling player's choice) "
                               "and gains Fleet and Furious Charge. Not for models without a removable ranged weapon."),
    "Telescopic Stalker Limbs": "See the Telescopic Stalker Limbs special rule.",
    "Xanathite Plating": "Failed Armour Saves caused by Blast or Template weapons may be re-rolled.",
    "Multi-Melta and Searchlight": "A Multi-Melta together with a Searchlight (see Searchlight).",
}

# Order of High Techno-Arcana / Dark Techno-Arcana names
ORDERS = ["Legio Cybernetica", "Myrmidax", "Ordo Reductor", "Lachrimallus", "Macrotek", "Malagra", "Explorator",
          "Skitarii", "Secutarii", "Ordinator", "Archimandrite", "Genetor - Magos Biologis"]
DARK = ["Daemon Engine Horde", "Scrapcode Covenant", "Engines of Ruin", "Flesh-Mechanica"]


# ==================================================================== IDS
def U(name):
    return k("unit", name)


CFG = k("cfg", "Mechanicum Army")
ORD = {n: uid(CFG, "order", n) for n in ORDERS + DARK}
WARLORD = k("warlord")
EDICTS = ["Daemonic Edict", "Scrapcode Edict", "Ruinous Edict", "Fleshcraft Edict"]
EDICT_ARCANA = dict(zip(EDICTS, DARK[:1] + ["Scrapcode Covenant", "Engines of Ruin", "Flesh-Mechanica"]))
EDICT = {n: k("edict", n) for n in EDICTS}
TRANSPORT_IDS = {n: k("transport", n) for n in ["Mechanicum Rhino Armoured Carrier", "Triaros Armoured Conveyor"]}

AM, MD = U("Archmagos"), U("Magos Dominus")
KH, ZK, CDI = U("Kelbor-Hal"), U("Zagreus Kane"), U("Calleb Decima Invictus")
CHROM, SCORIA = U("Lukas Chrom"), U("Anacharis Scoria")
LOYALIST, TRAITOR = L.LOYALIST, L.TRAITOR
WL_ORDERS = ["Legio Cybernetica", "Myrmidax", "Ordo Reductor", "Malagra", "Ordinator", "Archimandrite",
             "Genetor - Magos Biologis"]
TROOP_UNITS = []        # unit elements that count as compulsory Troops (for Legio Cybernetica)


# ================================================================ conditions
def o(n):
    return cond(ORD[n], "force", "atLeast", 1)


def not_o(n):
    return cond(ORD[n], "force", "lessThan", 1)


def in_f(eid):
    return cond(eid, "force", "atLeast", 1)


def none_f(eid):
    return cond(eid, "force", "lessThan", 1)


def in_r(eid):
    return cond(eid, "roster", "atLeast", 1)


def none_r(eid):
    return cond(eid, "roster", "lessThan", 1)


def is_wl(u):
    return cond(WARLORD, u, "atLeast", 1)


def _hide_mods(grp_fn, max_id=None):
    mods = [modifier("set", "hidden", "true", groups=[grp_fn()])]
    if max_id:
        mods.append(modifier("set", max_id, 0, groups=[grp_fn()]))
    return mods


def show_any(e, *conds, max_id=None):
    """Hidden (and max 0) unless at least one condition holds."""
    add_mods(e, _hide_mods(lambda: all_of(*[_negate(c) for c in conds]), max_id))
    return e


def show_all(e, *conds, max_id=None):
    """Hidden (and max 0) unless all conditions hold."""
    add_mods(e, _hide_mods(lambda: any_of(*[_negate(c) for c in conds]), max_id))
    return e


def hide_any(e, *conds, max_id=None):
    add_mods(e, _hide_mods(lambda: any_of(*conds), max_id))
    return e


def err(text, *conds):
    """Error when ALL conditions hold."""
    return modifier("add", "error", text, groups=[all_of(*conds)])


def err_any(text, *conds):
    return modifier("add", "error", text, groups=[any_of(*conds)])


# ================================================================== helpers
def gear_n(key, name, n):
    lid = uid("link", key, name, n)
    return link(lid, W(name), name, constraints=[constraint(uid(lid, "min"), "min", n),
                                                 constraint(uid(lid, "max"), "max", n)])


def opt(key, name, cost=0, gear_=(), rules_=(), text=None, show=(), need=(), hide=(), max_=1, pm_unit=None,
        cats=(), groups=(), entries=(), mods=(), extra=0):
    """Optional upgrade entry. show: visible if any holds; need: visible only if all hold; hide: hidden if any."""
    eid = uid(key, "opt", name)
    mx = uid(eid, "max")
    ms = list(mods)
    c = cost
    if pm_unit:
        c = extra
        ms.append(modifier("increment", PTS, cost, repeats=[repeat("model", pm_unit, 1)]))
    e = entry(eid, name, cost=c, mods=ms, constraints=[constraint(mx, "max", max_, auto=True)],
              rules=[rule(uid(eid, "rule"), name, text)] if text else [],
              infolinks=rules_links(list(rules_), key=eid), links=[gear(eid, x) for x in gear_],
              cats=[category_link(ci, cn, key=eid) for ci, cn in cats], groups=list(groups), entries=list(entries))
    if show:
        show_any(e, *show, max_id=mx)
    if need:
        show_all(e, *need, max_id=mx)
    if hide:
        hide_any(e, *hide, max_id=mx)
    return e


def oid(key, name):
    return uid(key, "opt", name)


def link_mods(grp, name, mods):
    """Add modifiers to the entryLink called `name` inside a group."""
    for lk in grp.iter("entryLink"):
        if lk.get("name") == name:
            add_mods(lk, mods)
            return lk
    raise KeyError(name)


def slot_e(key, title, default, options):
    """Replace ONE of several identical items: the default is an inline entry (so the model's kit keeps the rest)."""
    d = entry(uid(key, title, "default"), default, links=[gear(uid(key, title, "default"), default)])
    return slot(key, title, None, options, default_is_entry=d)


def pick_group(key, title, unit_id, options, per=1, required=True):
    """'Every model must select N of the following' as a unit-level group (min = max = N per model)."""
    gid = uid("grp", key, title)
    mn, mx = uid(gid, "min"), uid(gid, "max")
    mods = [modifier("increment", mx, per, repeats=[repeat("model", unit_id, 1)])]
    cons = [constraint(mx, "max", 0)]
    if required:
        mods.append(modifier("increment", mn, per, repeats=[repeat("model", unit_id, 1)]))
        cons.append(constraint(mn, "min", 0))
    links = [link(uid("link", gid, n), W(n), n, cost=p or None) for n, p in options]
    return group(gid, title, mods=mods, links=links, constraints=cons)


def must_take(key, title, items, default):
    gid = uid("grp", key, title)
    links = [link(uid("link", gid, n), W(n), n, cost=p or None) for n, p in items]
    return group(gid, title, default=uid("link", gid, default), links=links,
                 constraints=[constraint(uid(gid, "min"), "min", 1, auto=True),
                              constraint(uid(gid, "max"), "max", 1, auto=True)])


def transport(u, names, max_models=None):
    gid = uid("grp", u, "transport")
    mx = uid(gid, "max")
    mods = []
    if max_models:
        mods = [modifier("set", mx, 0, conds=[cond("model", u, "greaterThan", max_models)]),
                modifier("set", "hidden", "true", conds=[cond("model", u, "greaterThan", max_models)])]
    return group(gid, "Dedicated Transport", mods=mods,
                 links=[link(uid("link", gid, n), TRANSPORT_IDS[n], n) for n in names],
                 constraints=[constraint(mx, "max", 1, auto=True)])


def warlord_link(u, hide_orders=WL_ORDERS, fixed=False, extra_hide=()):
    lid = uid("link", u, "Warlord")
    cons = [constraint(uid(lid, "max"), "max", 1, auto=True)]
    if fixed:
        cons.append(constraint(uid(lid, "min"), "min", 1))
    hc = [o(n) for n in hide_orders] + list(extra_hide)
    mods = []
    if hc:
        mods = [modifier("set", "hidden", "true", groups=[any_of(*hc)]),
                modifier("set", uid(lid, "max"), 0, groups=[any_of(*[o(n) for n in hide_orders] +
                                                                    [copy_cond(c) for c in extra_hide])])]
    return link(lid, WARLORD, "Warlord", mods=mods, constraints=cons)


def copy_cond(c):
    return el("condition", dict(c.attrib))


def paragon(u, cost=35):
    """'A Maniple consisting of a single X may take Paragon of Metal'."""
    e = opt(u, "Paragon of Metal", cost, rules_=["Paragon of Metal", "It Will Not Die", "Rampage"],
            hide=[cond("model", u, "greaterThan", 1)])
    return e


def single_only_error(u):
    return err("Paragon of Metal: only a Maniple consisting of a single model may take it.",
               cond(oid(u, "Paragon of Metal"), u, "atLeast", 1), cond("model", u, "greaterThan", 1))


def master_crafted(key, cost=15, **kw):
    return opt(key, "Master-crafted Weapon", cost, gear_=["Master-crafted Weapon"], **kw)


def troops_toggle(u, order_name, compulsory, old_cat, old_name, rule_name):
    """'X may be selected as Troops' (Order rule) as an upgrade on the unit + the unit modifiers it needs."""
    t = opt(u, "Selected as Troops (" + order_name.split(" -")[0] + ")", 0, rules_=[rule_name], show=[o(order_name)])
    tid = oid(u, "Selected as Troops (" + order_name.split(" -")[0] + ")")
    c = lambda: [cond(tid, u, "atLeast", 1)]
    mods = [modifier("set-primary", "category", TROOPS, conds=c()),
            modifier("remove", "category", old_cat, conds=c())]
    if compulsory:
        mods.append(modifier("add", "category", LINE, conds=c()))
        if old_cat == HQ:
            mods.append(modifier("remove", "category", COMMANDER, conds=c()))
    return t, mods


def foc_free(slot_name):
    return [(gs.FOC_PLUS[slot_name], f"Force Org: +1 {slot_name}")]


# ------------------------------------------------------------ order / dark tables
INFUSION = {"Archmagos": 15, "Magos Dominus": 20, "Adjutant": 15, "Tech-Priest Auxilia": 15,
            "Scyllax Guardian-Automata Covenant": 10, "Karkinos Servitor Maniple": 10,
            "Praetorian Battle-Servitor Maniple": 15, "Thallax Cohort": 15,
            "Castellax Class Battle-Automata Maniple": 20, "Domitar Battle-Automata Maniple": 25,
            "Cataphract Class Robot Maniple": 20, "Ursarax Cohort": 15, "Vorax Class Battle-Automata Maniple": 15,
            "Arlatax Class Battle-Automata Maniple": 25, "Vultarax Stratos-Automata Maniple": 25,
            "Crusader Class Robot Maniple": 15, "Seeker Robot Maniple": 10,
            "Thanatar-Cavas Siege-Automata Maniple": 30, "Thanatar-Calix Siege-Automata": 30,
            "Thanatar-Cynis Siege-Automata Maniple": 30, "Conqueror Class Robot Maniple": 20}
WINGS = {"Archmagos": (20, "Jump Infantry"), "Magos Dominus": (20, "Jump Infantry"), "Adjutant": (15, "Jump Infantry"),
         "Tech-Priest Auxilia": (15, "Jump Infantry"), "Castellax Class Battle-Automata Maniple": (30, "Flying Monster"),
         "Domitar Battle-Automata Maniple": (35, "Flying Monster"),
         "Cataphract Class Robot Maniple": (25, "Flying Monster"),
         "Vorax Class Battle-Automata Maniple": (25, "Flying Monster"),
         "Crusader Class Robot Maniple": (25, "Flying Monster"), "Seeker Robot Maniple": (15, "Jump Infantry")}
RECON = {"Archmagos": (10, 15, 10), "Magos Dominus": (10, 15, 10), "Adjutant": (5, 10, 5),
         "Tech-Priest Auxilia": (5, 10, 5), "Protector Squad": (5, 8, 5), "Myrmidon Secutor Host": (8, 12, 8),
         "Myrmidon Destructor Host": (8, 12, 8), "Myrmidon Reductor Host": (8, 12, 8),
         "Karkinos Servitor Maniple": (5, 8, 5), "Praetorian Battle-Servitor Maniple": (8, 12, 8),
         "Skitarii Cohort": (2, 3, 2), "Skitarii Battle-Pilgrym Corpus": (2, 3, 2), "Thallax Cohort": (8, 12, 8),
         "Ursarax Cohort": (8, 12, 8)}
# Genetor Controlled Augmentation: unit -> has multi-wound models
AUGMENT = {"Adsecularis Tech-Thrall Covenant": False, "Skitarii Cohort": False,
           "Skitarii Battle-Pilgrym Corpus": True, "Karkinos Servitor Maniple": True,
           "Praetorian Battle-Servitor Maniple": True, "Thallax Cohort": True, "Ursarax Cohort": True}
AUGMENTS = [("Reinforced Physiology", 2, ["Feel No Pain (5+)"], "Feel No Pain (5+)."),
            ("Enhanced Musculature", 2, [], "+1 Strength."),
            ("Accelerated Reflexes", 2, [], "+1 Initiative."),
            ("Adrenal Induction", 2, ["Furious Charge", "Fleet"], "Furious Charge and Fleet."),
            ("Dermal Plating", 3, [], "Improve the model's Armour Save by 1, to a maximum of 3+.")]
# Explorator Void-Hardened Armour: unit -> points per model
VOID = {"Archmagos": 1, "Magos Dominus": 1, "Adjutant": 1, "Tech-Priest Auxilia": 1, "Skitarii Marshal": 1,
        "Secutarii Axiarch": 1, "Protector Squad": 1, "Myrmidon Secutor Host": 3, "Myrmidon Destructor Host": 3,
        "Myrmidon Reductor Host": 3, "Scyllax Guardian-Automata Covenant": 1, "Karkinos Servitor Maniple": 1,
        "Praetorian Battle-Servitor Maniple": 3, "Skitarii Battle-Pilgrym Corpus": 1,
        "Adsecularis Tech-Thrall Covenant": 1, "Skitarii Cohort": 1, "Secutarii Hoplite Phalanx": 1,
        "Secutarii Peltast Phalanx": 1, "Thallax Cohort": 3, "Ursarax Cohort": 3}


def order_extras(u, name, pm, abeyant=None, paragon_id=None):
    """Order / Dark Techno-Arcana options of a unit (from the cost tables). Returns (entries, groups, mods)."""
    ents, grps, mods = [], [], []
    pmu = u if pm else None
    if name in INFUSION:
        inf = opt(u, "Daemonic Infusion", INFUSION[name], gear_=["Daemonic Infusion"], rules_=["Unstable"],
                  pm_unit=pmu, show=[o("Daemon Engine Horde"), in_r(EDICT["Daemonic Edict"])])
        ents.append(inf)
        iid = oid(u, "Daemonic Infusion")
        if paragon_id:
            mods.append(err("A Paragon of Metal may not also receive Daemonic Infusion.",
                            cond(iid, u, "atLeast", 1), cond(paragon_id, u, "atLeast", 1)))
        if name in WINGS:
            cost, ut = WINGS[name]
            ents.append(opt(u, "Warp-Wings", cost, gear_=["Warp-Wings"], pm_unit=pmu,
                            text=f"The model{'s' if pm else ''} become{'' if pm else 's'} {ut}.",
                            show=[cond(iid, u, "atLeast", 1)],
                            hide=[cond(abeyant, u, "atLeast", 1)] if abeyant else ()))
    if name in RECON:
        gid = uid("grp", u, "recon")
        rents = []
        for (rn, c) in zip(["Predatory Reconstruction", "Massive Reconstruction", "Bestial Reconstruction"],
                           RECON[name]):
            rents.append(opt(u, rn, c, gear_=[rn], pm_unit=pmu))
        g = group(gid, "Abominable Reconstruction (one)", entries=rents,
                  constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])
        show_any(g, o("Flesh-Mechanica"), in_r(EDICT["Fleshcraft Edict"]))
        grps.append(g)
    if name in AUGMENT:
        gid = uid("grp", u, "augment")
        extra = 5 if AUGMENT[name] else 0
        aents = [opt(u, an, c + extra, rules_=rl, text=t, pm_unit=u) for an, c, rl, t in AUGMENTS]
        ps = opt(u, "Perfected Specimens", 20, gear_=["Perfected Specimens"], show=[o("Genetor - Magos Biologis")])
        psid = oid(u, "Perfected Specimens")
        g = group(gid, "Controlled Augmentation (Genetor)", entries=aents,
                  mods=[modifier("increment", uid(gid, "max"), 1, conds=[cond(psid, u, "atLeast", 1)])],
                  constraints=[constraint(uid(gid, "max"), "max", 1)])
        show_any(g, o("Genetor - Magos Biologis"))
        grps.append(g)
        ents.append(ps)
        mods.append(err("Perfected Specimens requires a Controlled Augmentation.", cond(psid, u, "atLeast", 1),
                        *[cond(oid(u, an), u, "lessThan", 1) for an, *_ in AUGMENTS]))
    if name in VOID:
        c = VOID[name]
        ve = opt(u, "Void-Hardened Armour (Explorator)", c, gear_=["Void-Hardened Armour"], pm_unit=pmu,
                 show=[o("Explorator")])
        if abeyant:  # an Abeyant makes the model Very Bulky (+5 instead of +1)
            add_mods(ve, [modifier("increment", PTS, 4, conds=[cond(abeyant, u, "atLeast", 1)])])
        ents.append(ve)
    return ents, grps, mods


def exploration_party(u):
    return opt(u, "Exploration Party (Explorator)", 15, gear_=["Exploration Party"], show=[o("Explorator")])


def volatile_any(u, model_ids):
    g = model_takes(u, "Volatile Charges (Engines of Ruin, any model)", u, model_ids, [("Volatile Charge", 10)])
    return show_any(g, o("Engines of Ruin"))


WARGEAR.update({
    "Void-Hardened Armour": ("Armour Save unchanged; failed Armour Saves against Blast or Template weapons may be "
                             "re-rolled; Advance distance -1\"; Charge and Pursuit distances -1\"."),
    "Exploration Party": ("The unit gains Scout (Explorator Order; up to one Troops choice; not Vehicles or "
                          "Cybernetica Cortex models).", ["Scouts"]),
    "Perfected Specimens": "The unit may purchase two different Controlled Augmentations instead of one.",
})


# ======================================================================= HQ
CHAR_NAMED = [KH, ZK, CDI]          # count as an Archmagos


def magos(name, cost, stats, kit, pistol_swaps, melee_swaps, one_of, add_weapons, wargear, occ, rules_, extra=()):
    u = U(name)
    prof = unit_profile(u, name, "Infantry (Character)", *stats)
    abeyant = opt(u, "Abeyant", 25, gear_=["Abeyant"], rules_=["It Will Not Die", "Move Through Cover", "Very Bulky"])
    ab_id = oid(u, "Abeyant")
    mc = master_crafted(u)
    add_mods(mc, [modifier("set", PTS, 0, groups=[all_of(o("Myrmidax"), is_wl(u))])])
    wg = take(u, "Wargear", wargear + [("Cyber-occularis", 15, occ)])
    link_mods(wg, "Rad Furnace", [modifier("set", PTS, 20, groups=[all_of(o("Genetor - Magos Biologis"), is_wl(u))])])
    myr = take(u, "Myrmidax Warlord: additional ranged weapon", [
        ("Rotor Cannon", 5), ("Volkite Charger", 10), ("Meltagun", 10), ("Graviton Gun", 15), ("Irad Cleanser", 20),
        ("Phased Plasma-Fusil", 20), ("Photon Thruster", 25)], max_total=1)
    show_all(myr, o("Myrmidax"), is_wl(u))
    groups = [slot(u, "Replace " + kit[1], kit[1], pistol_swaps),
              slot(u, "Replace Power Weapon", "Power Weapon", melee_swaps),
              take(u, "May take one of", one_of, max_total=1),
              take(u, "One additional weapon", add_weapons, max_total=1), wg, myr]
    ents = [abeyant, mc,
            opt(u, "Reductor War Munitions (Ordo Reductor Warlord)", 0, gear_=["Ordo Reductor War Munitions"],
                need=[o("Ordo Reductor"), is_wl(u)]),
            *extra]
    # Dark Invocation (Daemon Engine Horde)
    psy = opt(u, "Dark Invocation: Psyker (Mastery Level 1)", 30, rules_=["Dark Invocation", "Psyker"],
              show=[o("Daemon Engine Horde")])
    ents.append(psy)
    ml1 = oid(u, "Dark Invocation: Psyker (Mastery Level 1)")
    more = []
    if name == "Archmagos":
        ents.append(opt(u, "Dark Invocation: Mastery Level 2", 30, rules_=["Dark Invocation"],
                        show=[cond(ml1, u, "atLeast", 1)]))
        more = [(1, cond(oid(u, "Dark Invocation: Mastery Level 2"), u, "atLeast", 1))]
    # Possession: Mastery Level 2 or greater only
    groups.append(L.psychic_powers(uid(u, "dark-invocation"), u, 1, ["Daemonology (Malefic)"], more=more,
                                   hide=[cond(ml1, u, "lessThan", 1)], exclude=["Possession"],
                                   extra=[("Possession", [copy_cond(more[0][1])])] if more else ()))
    e2, g2, m2 = order_extras(u, name, False, abeyant=ab_id)
    mods = m2 + [
        err("Legio Cybernetica: the Warlord must be equipped with a Cortex Controller.", o("Legio Cybernetica"),
            is_wl(u), cond(W("Cortex Controller"), u, "lessThan", 1)),
        err("Archimandrite: the Warlord must be an Archmagos.", o("Archimandrite"), is_wl(u))
        if name == "Magos Dominus" else None]
    return u, prof, groups, ents + e2, g2, [m for m in mods if m is not None], rules_


def archmagos():
    u, prof, groups, ents, g2, mods, rules_ = magos(
        "Archmagos", 130, (4, 5, 4, 5, 3, 4, 2, 10, "2+/4+"),
        ["Artificer Armour", "Volkite Serpenta", "Power Weapon", "Mechanicum Protectiva"],
        [("Archaeotech Pistol", 5), ("Photon Gauntlet", 5), ("Plasma Pistol", 5), ("Lucifex", 5), ("Maxima Bolter", 5)],
        [("Power Fist", 10), ("Corposant Stave", 5), ("Chainfist", 10), ("Relic Blade", 15)],
        [("Servo-Arm", 10), ("Machinator Array", 25), ("Jet Pack", 20), ("Conversion Beamer", 15),
         ("Graviton Imploder", 25)],
        [("Rotor Cannon", 5), ("Meltagun", 10), ("Graviton Gun", 15), ("Phased Plasma-Fusil", 20),
         ("Irad Cleanser", 20), ("Photon Thruster", 25)],
        [("Auspex", 5), ("Cyber-familiar", 15), ("Infravisor", 5), ("Cortex Controller", 15), ("Rad Furnace", 30),
         ("Rad Grenades", 10), ("Melta Bombs", 5)], 4,
        ["Independent Character", "Iron and Machine", "Battlesmith", "Cybertheurgist", "The Rule of the Archmagos",
         "Orders of High Techno-Arcana"])
    ents.append(opt(u, "Djinn-skein (Warlord only)", 25, gear_=["Djinn-skein"], need=[is_wl(u)]))
    mods += [err("The Rule of the Archmagos: an Archmagos must be the army's Warlord.", cond(WARLORD, u, "lessThan", 1)),
             err_any("The Rule of the Archmagos: no more than one Archmagos (Kelbor-Hal, Zagreus Kane and Calleb Decima "
                     "count as Archmagos).", *[in_r(x) for x in CHAR_NAMED])]
    return unit("Archmagos", 130, HQ, "HQ", profiles=[prof],
                kit=["Artificer Armour", "Volkite Serpenta", "Power Weapon", "Mechanicum Protectiva"],
                rules_=rules_, groups=groups + g2, entries=ents, mods=mods,
                constraints=[unique(u, 1, "roster")], links_extra=[warlord_link(u, hide_orders=[],
                                                                               extra_hide=[in_r(KH), in_r(ZK)])])


def magos_dominus():
    u, prof, groups, ents, g2, mods, rules_ = magos(
        "Magos Dominus", 75, (4, 4, 4, 4, 2, 3, 2, 9, "3+/5+"),
        ["Power Armour", "Laspistol", "Power Weapon", "Cortex Controller", "Refractor Field"],
        [("Bolt Pistol", 1), ("Volkite Serpenta", 5), ("Archaeotech Pistol", 10), ("Photon Gauntlet", 10),
         ("Plasma Pistol", 15), ("Lucifex", 10)],
        [("Corposant Stave", 5), ("Power Fist", 10), ("Chainfist", 15), ("Relic Blade", 15)],
        [("Servo-Arm", 10), ("Machinator Array", 25), ("Jet Pack", 20), ("Conversion Beamer", 20),
         ("Graviton Imploder", 30)],
        [("Rotor Cannon", 5), ("Meltagun", 10), ("Graviton Gun", 15), ("Phased Plasma-Fusil", 20),
         ("Irad Cleanser", 20), ("Photon Thruster", 25)],
        [("Auspex", 5), ("Cyber-familiar", 15), ("Infravisor", 5), ("Rad Furnace", 30), ("Rad Grenades", 10),
         ("Melta Bombs", 5)], 2,
        ["Independent Character", "Iron and Machine", "Battlesmith", "Cybertheurgist", "Orders of High Techno-Arcana"])
    return unit("Magos Dominus", 75, HQ, "HQ", profiles=[prof],
                kit=["Power Armour", "Laspistol", "Power Weapon", "Cortex Controller", "Refractor Field"],
                rules_=rules_, groups=groups + g2, entries=ents, mods=mods,
                links_extra=[warlord_link(u, hide_orders=["Archimandrite"],
                                          extra_hide=[in_r(KH), in_r(ZK), in_r(AM)])])


def adjutant():
    n = "Adjutant"
    u = U(n)
    prof = unit_profile(u, n, "Infantry (Character)", 3, 4, 3, 3, 1, 3, 1, 8, "4+")
    sp = {s: uid(u, "spec", s) for s in ["Malagra", "Logis", "Secutor", "Ordinator", "Explorator"]}
    prof.insert(0, wrap("modifiers", [
        modifier("set", gs.char_id("Unit", "WS"), 4, conds=[cond(sp["Malagra"], u, "atLeast", 1)]),
        modifier("set", gs.char_id("Unit", "BS"), 5, conds=[cond(sp["Secutor"], u, "atLeast", 1)]),
        modifier("set", gs.char_id("Unit", "Ld"), 9, conds=[cond(sp["Logis"], u, "atLeast", 1)])]))

    def spec(s, cost, rules_, gear_=(), groups_=()):
        return entry(sp[s], f"{s} Adjutant", cost=cost, constraints=[constraint(uid(sp[s], "max"), "max", 1, auto=True)],
                     infolinks=rules_links(rules_, key=sp[s]), links=[gear(sp[s], x) for x in gear_],
                     groups=list(groups_))
    specs = [
        spec("Malagra", 20, ["Malagra Adjutant", "Preferred Enemy (Characters)", "Monster Hunter", "Precision Strikes",
                             "Scout", "Mark of Execution"],
             groups_=[take(sp["Malagra"], "Malagra wargear", [("Lucifex", 10), ("Photon Gauntlet", 10),
                                                               ("Rad Furnace", 25)])]),
        spec("Logis", 20, ["Logis Adjutant", "Strategic Calculus", "Calculated Deployment"],
             gear_=["Nuncio Vox", "Cognis Signum"]),
        spec("Secutor", 25, ["Secutor Adjutant", "Fusillade Pistols", "Chain Fire (Secutor Adjutant)"],
             groups_=[take(sp["Secutor"], "Second Pistol", [("Bolt Pistol", 1), ("Volkite Serpenta", 5),
                                                             ("Archaeotech Pistol", 10), ("Photon Gauntlet", 10),
                                                             ("Plasma Pistol", 15), ("Lucifex", 10)], max_total=1)]),
        spec("Ordinator", 20, ["Ordinator Adjutant", "Master of Destruction"], gear_=["Cognis Signum"],
             groups_=[take(sp["Ordinator"], "Ordinator Bombardment", [("Ordinator Bombardment", 35)])]),
        spec("Explorator", 20, ["Explorator Adjutant", "Scout", "Infiltrate", "Move Through Cover", "Djinn-sight",
                                "Telescopic Stalker Limbs"], gear_=["Telescopic Stalker Limbs"]),
    ]
    sg = uid("grp", u, "spec")
    spec_grp = group(sg, "Adjutant Specialisation (one)", entries=specs,
                     constraints=[constraint(uid(sg, "max"), "max", 1, auto=True)])
    pistol = slot(u, "Replace Laspistol", "Laspistol",
                  [("Bolt Pistol", 1), ("Volkite Serpenta", 5), ("Archaeotech Pistol", 10), ("Photon Gauntlet", 10),
                   ("Plasma Pistol", 15), ("Lucifex", 10), ("Explorator Arquebus", 10)])
    link_mods(pistol, "Lucifex", [modifier("set", "hidden", "true", conds=[cond(sp["Secutor"], u, "lessThan", 1)])])
    link_mods(pistol, "Explorator Arquebus",
              [modifier("set", "hidden", "true", conds=[cond(sp["Explorator"], u, "lessThan", 1)])])
    groups = [pistol, slot(u, "Replace Mechanicum Axe", "Mechanicum Axe",
                           [("Power Weapon", 0), ("Corposant Stave", 5), ("Power Fist", 10)]),
              take(u, "Wargear", [("Power Armour", 10), ("Refractor Field", 15), ("Servo-Arm", 10), ("Auspex", 5),
                                  ("Infravisor", 5), ("Signum", 15), ("Nuncio Vox", 10), ("Cortex Controller", 15),
                                  ("Cyber-familiar", 15), ("Melta Bombs", 5), ("Rad Grenades", 10), ("Jet Pack", 20)]),
              spec_grp]
    e2, g2, m2 = order_extras(u, n, False)
    return unit(n, 35, HQ, "HQ", profiles=[prof], kit=["War Plate", "Laspistol", "Mechanicum Axe"],
                rules_=["Independent Character", "Iron and Machine", "Battlesmith", "Adjutant Specialisations"],
                groups=groups + g2, entries=[master_crafted(u)] + e2, mods=m2,
                links_extra=[warlord_link(u, extra_hide=[in_r(KH), in_r(ZK), in_r(AM)])])


def tech_priest_auxilia():
    n = "Tech-Priest Auxilia"
    u = U(n)
    m = model(u, "Tech-Priest", 1, 5, 40,
              unit_profile(u, "Tech-Priest", "Infantry (Character)", 3, 3, 4, 4, 2, 3, 2, 9, "4+"),
              kit=["War Plate", "Laspistol", "Mechanicum Axe"],
              groups=[slot(uid(u, "tp"), "Replace Laspistol", "Laspistol",
                           [("Volkite Serpenta", 5), ("Plasma Pistol", 15), ("Archaeotech Pistol", 10)]),
                      take(uid(u, "tp"), "Wargear", [("Power Armour", 10), ("Refractor Field", 15), ("Servo-Arm", 10),
                                                     ("Signum", 15), ("Nuncio Vox", 10), ("Auspex", 5), ("Omnispex", 5),
                                                     ("Cortex Controller", 15), ("Jet Pack", 20)]),
                      take(uid(u, "tp"), "One additional weapon", [("Bolter", 2), ("Volkite Charger", 5),
                                                                   ("Meltagun", 10), ("Plasma Gun", 15),
                                                                   ("Graviton Gun", 15)], max_total=1),
                      show_any(take(uid(u, "tp"), "Rad-Alchemy (Genetor)", [("Rad Grenades", 10)]),
                               o("Genetor - Magos Biologis"))],
              entries=[master_crafted(uid(u, "tp"))])
    t, tmods = troops_toggle(u, "Macrotek", True, HQ, "HQ", "Macrotek")
    ret = opt(u, "Guardian Retinue (Calleb Decima)", 0, rules_=["Guardian Retinue"], cats=foc_free("HQ"),
              show=[in_r(CDI)])
    e2, g2, m2 = order_extras(u, n, True)
    return unit(n, 0, HQ, "HQ", models=numbered(m, 5, 1), rules_=["Iron and Machine", "Battlesmith", "Combat Attachés"],
                entries=[t, ret] + e2, groups=g2, mods=tmods + m2)


def skitarii_marshal():
    n = "Skitarii Marshal"
    u = U(n)
    e2, g2, m2 = order_extras(u, n, False)
    return unit(n, 75, HQ, "HQ",
                profiles=[unit_profile(u, n, "Infantry (Character)", 4, 4, 4, 4, 2, 4, 2, 9, "3+/5+")],
                kit=["Power Armour", "Refractor Field", "Radium Carabiner", "Power Weapon", "Frag Grenades",
                     "Krak Grenades"],
                rules_=["Independent Character", "Iron and Machine", "Stubborn", "Feel No Pain (6+)",
                        "Doctrina Imperatives", "Rad Poisoning"],
                groups=[slot(u, "Replace Radium Carabiner", "Radium Carabiner",
                             [("Galvanic Rifle", 5), ("Volkite Charger", 5), ("Arc Rifle", 10), ("Graviton Gun", 15)]),
                        slot(u, "Replace Power Weapon", "Power Weapon",
                             [("Taser Goad", 5), ("Corposant Stave", 5), ("Arc Maul", 10), ("Power Fist", 15)]),
                        take(u, "Wargear", [("Auspex", 5), ("Omnispex", 5), ("Infravisor", 5),
                                            ("Shattersphere Grenades", 5), ("Conversion Field", 15),
                                            ("Cyber-familiar", 15)])] + g2,
                entries=[master_crafted(u)] + e2, mods=m2,
                links_extra=[warlord_link(u, extra_hide=[in_r(KH), in_r(ZK), in_r(AM)])])


def secutarii_axiarch():
    n = "Secutarii Axiarch"
    u = U(n)
    e2, g2, m2 = order_extras(u, n, False)
    return unit(n, 80, HQ, "HQ",
                profiles=[unit_profile(u, n, "Infantry (Character)", 4, 4, 4, 4, 2, 4, 2, 9, "3+/5+")],
                kit=["Power Armour", "Refractor Field", "Volkite Serpenta", "Arc Lance", "Shattersphere Grenades"],
                rules_=["Independent Character", "Iron and Machine", "Stubborn", "Feel No Pain (6+)", "Titan Guard",
                        "Binaric Stratagems", "Rad Poisoning"],
                groups=[slot(u, "Replace Volkite Serpenta", "Volkite Serpenta",
                             [("Radium Pistol", 0), ("Phosphor Blast Pistol", 5), ("Arc Pistol", 5),
                              ("Archaeotech Pistol", 10), ("Photon Gauntlet", 10)]),
                        slot(u, "Replace Arc Lance", "Arc Lance",
                             [("Taser Goad", 0), ("Power Weapon", 0), ("Corposant Stave", 5), ("Arc Maul", 5),
                              ("Power Fist", 15)]),
                        take(u, "Wargear", [("Auspex", 5), ("Omnispex", 5), ("Infravisor", 5),
                                            ("Conversion Field", 15), ("Cyber-familiar", 15)])] + g2,
                entries=[master_crafted(u)] + e2, mods=m2,
                links_extra=[warlord_link(u, extra_hide=[in_r(KH), in_r(ZK), in_r(AM)])])


# =================================================================== ELITES
def protector_squad():
    n = "Protector Squad"
    u = U(n)
    m = model(u, "Protector", 5, 10, 18, unit_profile(u, "Protector", "Infantry", 4, 4, 4, 4, 2, 4, 2, 8, "3+"),
              kit=["Power Armour", "Laspistol", "Close Combat Weapon", "Bionics"])
    mid = m.get("id")
    ret = opt(u, "Retinue (Archmagos / Magos Dominus)", 0, rules_=["Retinue (Protector Squad)"], cats=foc_free("Elites"))
    rmax = uid(oid(u, "Retinue (Archmagos / Magos Dominus)"), "force-max")
    add_to(ret, "constraints", [constraint(rmax, "max", 0, scope="force", deep=True)])
    add_mods(ret, [modifier("increment", rmax, 1, repeats=[repeat(x, "force", 1)]) for x in [AM, MD] + CHAR_NAMED])
    e2, g2, m2 = order_extras(u, n, True)
    return unit(n, 0, ELITES, "Elites", models=[m], rules_=["Iron and Machine"],
                entries=[ret, per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                         per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])] + e2,
                groups=[model_swaps(u, "Protectors: replace Laspistol (any model)", u, [mid],
                                    [("Bolter", 2), ("Shotgun", 2), ("Flamer", 6), ("Meltagun", 10), ("Plasma Gun", 15),
                                     ("Volkite Charger", 5)]),
                        model_takes(u, "Protectors: may take (any model)", u, [mid],
                                    [("Power Weapon", 10), ("Refractor Field", 12)]),
                        take(u, "Up to two Protectors may take (Servo-Arm and/or Mechanicum Axe)",
                             [("Servo-Arm", 10, 2), ("Mechanicum Axe", 10, 2)]),
                        transport(u, ["Mechanicum Rhino Armoured Carrier", "Triaros Armoured Conveyor"], 10)] + g2,
                mods=m2)


MYRMIDON_KIT = ["Frag Grenades", "Krak Grenades", "Refractor Field", "Infravisor"]


def myrmidon(n, base, per, model_name, weapon_kit, rules_, groups_fn, order_only=False):
    u = U(n)
    lord_mc = opt(uid(u, "lord"), "Perfected Armament: Master-crafted ranged weapon (Myrmidax)", 10,
                  gear_=["Master-crafted Weapon"], show=[o("Myrmidax")])
    lord = model(u, "Myrmidon Lord", 1, 1, 0,
                 unit_profile(u, "Myrmidon Lord", "Infantry (Character)", 4, 5, 4, 5, 2, 2, 3, 10, "3+/5+"),
                 kit=weapon_kit + MYRMIDON_KIT, entries=[lord_mc])
    men = model(u, model_name, 2, 9, per,
                unit_profile(u, model_name, "Infantry", 4, 5, 4, 5, 2, 2, 2, 9, "3+/5+"), kit=weapon_kit + MYRMIDON_KIT)
    e2, g2, m2 = order_extras(u, n, True)
    ents, mods = list(e2), list(m2)
    if n == "Myrmidon Secutor Host":
        t, tm = troops_toggle(u, "Myrmidax", False, ELITES, "Elites", "Myrmidax")
        ents.append(t)
        mods += tm
    if order_only:
        bg = opt(u, "Warlord's Bodyguard (Ordo Reductor)", 0, cats=foc_free("Elites"), show=[o("Ordo Reductor")])
        add_to(bg, "constraints", [unique(oid(u, "Warlord's Bodyguard (Ordo Reductor)"), 1, "force")])
        ents.append(bg)
        mods.append(err("Myrmidon Reductor Host: Ordo Reductor only.", not_o("Ordo Reductor")))
    e = unit(n, base - 2 * per, ELITES, "Elites", models=[lord, men],
             rules_=["Bulky", "Relentless", "Stubborn", "Lumbering Advance"] + rules_, entries=ents,
             groups=groups_fn(u, [lord.get("id"), men.get("id")]) + [transport(u, ["Triaros Armoured Conveyor"])] + g2,
             mods=mods)
    if order_only:
        show_any(e, o("Ordo Reductor"))
    return e


def myrmidon_secutors():
    return myrmidon("Myrmidon Secutor Host", 120, 35, "Myrmidon Secutor", ["Power Weapon"], ["Fusillade Attack"],
                    lambda u, ids: [pick_group(u, "Weapons (every model selects two; the same weapon may be taken twice "
                                                  "but is not Twin-linked)", u,
                                               [("Maxima Bolter", 10), ("Volkite Charger", 10), ("Graviton Gun", 15),
                                                ("Irad Cleanser", 20), ("Phased Plasma-Fusil", 20)], per=2)])


def myrmidon_destructors():
    return myrmidon("Myrmidon Destructor Host", 135, 40, "Myrmidon Destructor", ["Power Fist"], ["Destructor Doctrine"],
                    lambda u, ids: [pick_group(u, "Heavy Weapon (every model selects one)", u,
                                               [("Volkite Culverin", 25), ("Photon Thruster", 35),
                                                ("Irradiation Engine", 40), ("Conversion Beamer", 35),
                                                ("Graviton Imploder", 35)], per=1)])


def myrmidon_reductors():
    def g(u, ids):
        return [model_swaps(u, "Replace Multi-Melta (any model)", u, ids,
                            [("Missile Launcher", 0)]),
                model_takes(u, "Models with a Missile Launcher may take", u, [W("Missile Launcher")],
                            [("Rad Missiles", 5), ("Phosphex Missiles", 10)])]
    return myrmidon("Myrmidon Reductor Host", 135, 40, "Myrmidon Reductor", ["Multi-Melta", "Power Fist"], ["Wrecker"],
                    g, order_only=True)


def scyllax():
    n = "Scyllax Guardian-Automata Covenant"
    u = U(n)
    m = model(u, "Scyllax Guardian-Automata", 4, 16, 35,
              unit_profile(u, "Scyllax Guardian-Automata", "Infantry", 3, 4, 4, 5, 2, 3, 2, 7, "4+"),
              kit=["Scyllax Bolter", "Mechadendrite Combat Array", "War Plate", "Rad Furnace"])
    mid = m.get("id")
    specials = [("Meltagun", 15), ("Graviton Gun", 15), ("Irad Cleanser", 20), ("Plasma Gun", 20)]
    sp, _ = pool(u, "Special weapons (one per four models, replace Scyllax Bolter)", u, specials, 0, every=4)
    e2, g2, m2 = order_extras(u, n, True)
    ret = opt(u, "Guardian Retinue (Calleb Decima)", 0, rules_=["Guardian Retinue"], cats=foc_free("Elites"),
              show=[in_r(CDI)])
    return unit(n, 155 - 4 * 35, ELITES, "Elites", models=[m],
                rules_=["Guardian-Servitor Protocols", "Move Through Cover", "Night Vision", "Relentless", "Maelstrom",
                        "Dismemberment"],
                entries=[opt(u, "Frag Grenades (entire squad)", 10, gear_=["Frag Grenades"]), ret] + e2,
                groups=[model_swaps(u, "Replace Scyllax Bolter (any model)", u, [mid],
                                    [("Enhanced Combat Array", 5), ("Rotor Cannon", 5), ("Flamer", 10),
                                     ("Volkite Charger", 10)], minus=[W(x) for x, _ in specials]),
                        sp, volatile_any(u, [mid]), transport(u, ["Triaros Armoured Conveyor"])] + g2, mods=m2)


def automata_unit(n, slot_cat, slot_name, mname, cost, mx, prof, kit, rules_, groups_fn=None, whole=(),
                  paragon_ok=True, number=True, compulsory=True, extra_entries=(), extra_mods=()):
    """Maniple of 1-mx Battle-Automata / robots. groups_fn(model_key) gives per-model options (then numbered)."""
    u = U(n)
    m = model(u, mname, 1, mx, cost, prof(u), kit=kit, groups=groups_fn(uid(u, "m")) if groups_fn else [])
    models = numbered(m, mx, 1) if (number and groups_fn) else [m]
    ents = [per_model(u, f"{it} (entire maniple)", c, u, [it]) for it, c in whole]
    mods = list(extra_mods)
    pid = None
    if paragon_ok:
        ents.append(paragon(u))
        mods.append(single_only_error(u))
        pid = oid(u, "Paragon of Metal")
    e2, g2, m2 = order_extras(u, n, True, paragon_id=pid)
    return unit(n, 0, slot_cat, slot_name, models=models, rules_=rules_, entries=ents + list(extra_entries) + e2,
                groups=g2, mods=mods + m2, compulsory=compulsory)


def mc(stats, ut="Monstrous Creature"):
    return lambda u_, name: unit_profile(u_, name, ut, *stats)


def domitar():
    n = "Domitar Battle-Automata Maniple"
    return automata_unit(n, ELITES, "Elites", "Domitar", 175, 5,
                         lambda u: unit_profile(u, "Domitar", "Monstrous Creature", 4, 3, 7, 7, 4, 3, 3, 7, "3+/5+"),
                         ["Graviton Hammers", "Missile Launcher with Frag, Krak and Ignis-Frag Missiles",
                          "Atomantic Shielding"],
                         ["Cybernetica Cortex", "Programmed Behaviour", "Reactor Blast", "Crusader", "Atomantic Shielding"],
                         whole=[("Searchlight", 1), ("Frag Grenades", 5), ("Flak Missiles", 5)])


def weapons_platform():
    n = "Mechanicum Weapons Platform"
    u = U(n)
    plat = uid("model", u, "Weapons Platform")
    crew = uid("model", u, "Artillery Servitor")
    cmin, cmax = uid(crew, "min"), uid(crew, "max")
    p = entry(plat, "Weapons Platform", typ="model", cost=27,
              constraints=[constraint(uid(plat, "min"), "min", 1), constraint(uid(plat, "max"), "max", 3)],
              profiles=[unit_profile(plat, "Weapons Platform", "Artillery", "-", "-", "-", 7, 2, "-", "-", "-", "3+")])
    c = entry(crew, "Artillery Servitor", typ="model", cost=0,
              mods=[modifier("increment", cmin, 3, repeats=[repeat(plat, u, 1)]),
                    modifier("increment", cmax, 3, repeats=[repeat(plat, u, 1)])],
              constraints=[constraint(cmin, "min", 0, auto=True), constraint(cmax, "max", 0, auto=True)],
              profiles=[unit_profile(u, "Artillery Servitor", "Artillery (crew)", 3, 3, 3, 3, 1, 3, 1, 8, "5+")],
              links=[gear(crew, x) for x in ["Laspistol", "Close Combat Weapon"]])
    gid = uid("grp", u, "weapon")
    ents = []
    for w, pts in [("Twin-linked Heavy Bolter", 20), ("Twin-linked Lascannon", 40), ("Photon Thruster", 40),
                   ("Plasma Caster", 40), ("Graviton Cannon", 50)]:
        eid = uid("choice", u, "weapon", w)
        ents.append(entry(eid, w, mods=[modifier("increment", PTS, pts, repeats=[repeat(plat, u, 1)])],
                          constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)], links=[gear(eid, w)]))
    wg = group(gid, "Platform weapon (every platform the same)", entries=ents, default=ents[0].get("id"),
               constraints=[constraint(uid(gid, "min"), "min", 1, auto=True),
                            constraint(uid(gid, "max"), "max", 1, auto=True)])
    return unit(n, 0, ELITES, "Elites", models=[p, c], rules_=["Weapons Platform"], groups=[wg])


def karkinos():
    n = "Karkinos Servitor Maniple"
    u = U(n)
    m = model(u, "Karkinos Servitor", 3, 9, 30,
              unit_profile(u, "Karkinos Servitor", "Infantry", 3, 3, 4, 4, 2, 2, 2, 7, "4+"),
              kit=["War Plate", "Maxima Bolter", "Close Combat Weapon", "Bionics"])
    sp, _ = pool(u, "Replace Maxima Bolter (one per three models)", u,
                 [("Rotor Cannon", 5), ("Flamer", 5), ("Heavy Bolter", 10), ("Meltagun", 10)], 0, every=3)
    e2, g2, m2 = order_extras(u, n, True)
    return unit(n, 0, ELITES, "Elites", models=[m], rules_=["Iron and Machine", "Relentless", "Servitor Protocols"],
                groups=[sp, volatile_any(u, [m.get("id")])] + g2, entries=e2, mods=m2)


def praetorians():
    n = "Praetorian Battle-Servitor Maniple"
    u = U(n)
    mk = uid(u, "p")
    m = model(u, "Praetorian Battle-Servitor", 2, 4, 50,
              unit_profile(u, "Praetorian Battle-Servitor", "Infantry", 4, 3, 5, 6, 3, 3, 3, 8, "3+"),
              kit=["Power Armour", "Heavy Bolter", "Power Fist", "Bionics"],
              groups=[slot(mk, "Replace Heavy Bolter", "Heavy Bolter",
                           [("Multilaser", 0), ("Autocannon", 5), ("Meltagun", 0), ("Plasma Gun", 5),
                            ("Missile Launcher", 5), ("Graviton Gun", 10), ("Lascannon", 15)]),
                      slot(mk, "Replace Power Fist (melee weapon or second ranged weapon)", "Power Fist",
                           [("Chainfist", 5), ("Siege Wrecker", 5), ("Heavy Bolter", 10), ("Multilaser", 10),
                            ("Meltagun", 10), ("Autocannon", 15), ("Plasma Gun", 15), ("Missile Launcher", 15),
                            ("Graviton Gun", 20), ("Lascannon", 25)])])
    models = numbered(m, 4, 2)
    ids = [x.get("id") for x in models]
    t, tm = troops_toggle(u, "Genetor - Magos Biologis", False, ELITES, "Elites", "Genetor - Magos Biologis")
    rad = per_model(u, "Rad Grenades (Genetor Rad-Alchemy)", 5, u, ["Rad Grenades"])
    show_any(rad, o("Genetor - Magos Biologis"))
    e2, g2, m2 = order_extras(u, n, True)
    return unit(n, 115 - 100, ELITES, "Elites", models=models,
                rules_=["Iron and Machine", "Relentless", "Bulky", "Servitor Protocols", "Integrated Weapon Systems"],
                entries=[t, rad] + e2, groups=[volatile_any(u, ids)] + g2, mods=tm + m2)


def cataphract():
    n = "Cataphract Class Robot Maniple"
    return automata_unit(
        n, ELITES, "Elites", "Cataphract Robot", 95, 4,
        lambda u: unit_profile(u, "Cataphract Robot", "Monstrous Creature", 3, 3, 6, 6, 3, 2, 2, 7, "3+/5+"),
        ["Lascannon", "Bolter", "Flamer", "Atomantic Shielding"],
        ["Cybernetica Cortex", "Programmed Behaviour", "Relentless", "Targeting Protocols", "Atomantic Shielding"],
        groups_fn=lambda mk: [slot(mk, "Replace Lascannon", "Lascannon", [("Autocannon", -10), ("Heavy Bolter", -15)]),
                              slot(mk, "Replace Flamer", "Flamer", [("Power Fist", 10), ("Chainfist", 15)]),
                              slot(mk, "Replace Bolter", "Bolter", [("Heavy Bolter", 10)])])


def battle_pilgryms():
    n = "Skitarii Battle-Pilgrym Corpus"
    u = U(n)
    pil = model(u, "Battle-Pilgrym", 8, 16, 18,
                unit_profile(u, "Battle-Pilgrym", "Infantry", 3, 3, 3, 4, 2, 3, 2, 8, "4+/6+"),
                kit=["War Plate", "Voltlock Arquebus", "Close Combat Weapon", "Augmetic Ward"])
    ordi = model(u, "Ordinator", 0, 1, 33, unit_profile(u, "Ordinator", "Infantry", 4, 3, 3, 4, 2, 3, 3, 9, "4+/6+"),
                 kit=["War Plate", "Volkite Charger", "Power Weapon", "Close Combat Weapon", "Augmetic Ward"])
    pid = pil.get("id")
    add_mods(pil, specials_decrement(pid, uid(pid, "min"), uid(pid, "max"), [ordi.get("id")], u))
    sp, _ = pool(u, "Replace Close Combat Weapon (one per four Battle-Pilgryms)", u,
                 [("Power Weapon", 5), ("Corposant Stave", 5)], 0, every=4, per_child=pid)
    t, tm = troops_toggle(u, "Skitarii", False, ELITES, "Elites", "Skitarii")
    e2, g2, m2 = order_extras(u, n, True)
    return unit(n, 0, ELITES, "Elites", models=[pil, ordi], rules_=["Iron and Machine", "Battle-Pilgryms"],
                entries=[per_model(u, "Voltlock Handguns instead of Arquebuses (entire unit)", 0, u, ["Voltlock Handgun"]),
                         per_model(u, "Frag Grenades (entire unit)", 1, u, ["Frag Grenades"]),
                         per_model(u, "Krak Grenades (entire unit)", 2, u, ["Krak Grenades"]), t] + e2,
                groups=[sp] + g2, mods=tm + m2)


def electro_priests():
    n = "Electro-Priest Covenant"
    u = U(n)
    m = model(u, "Electro-Priest", 5, 10, 42, unit_profile(u, "Electro-Priest", "Infantry", 4, 2, 4, 4, 1, 4, 2, 9, "4++"),
              kit=["Electro Stave", "Force Shield"])
    return unit(n, 0, ELITES, "Elites", models=[m], rules_=["Fearless", "Siphoned Vigour"])


# =================================================================== TROOPS
def thralls():
    n = "Adsecularis Tech-Thrall Covenant"
    u = U(n)
    m = model(u, "Tech-Thrall", 10, 20, 3, unit_profile(u, "Tech-Thrall", "Infantry", 2, 2, 4, 3, 1, 2, 1, 7, "5+"),
              kit=["Flak Armour", "Las-lock", "Close Combat Weapon"])
    vol, _ = pool(u, "Volatile Charges (Engines of Ruin, one per five models)", u, [("Volatile Charge", 5)], 0, every=5)
    show_any(vol, o("Engines of Ruin"))
    e2, g2, m2 = order_extras(u, n, True)
    return unit(n, 5, TROOPS, "Troops", models=[m], rules_=["Feel No Pain (6+)"],
                entries=[opt(u, "Heavy Chainblades instead of Las-locks (entire Covenant)", 20,
                             gear_=["Heavy Chainblade"]),
                         opt(u, "Frag Grenades (entire Covenant)", 5, gear_=["Frag Grenades"]),
                         opt(u, "Carapace Armour (entire Covenant)", 20, gear_=["Carapace Armour"]),
                         opt(u, "Rite of Pure Thought (entire Covenant)", 15, rules_=["Rite of Pure Thought"]),
                         opt(u, "Induction Chargers (entire Covenant)", 15, gear_=["Induction Chargers"]),
                         exploration_party(u)] + e2,
                groups=[vol] + g2, mods=m2)


def skitarii_cohort():
    n = "Skitarii Cohort"
    u = U(n)
    sk = model(u, "Skitarii", 5, 10, 12, unit_profile(u, "Skitarii", "Infantry", 3, 3, 3, 4, 1, 3, 1, 8, "4+"),
               kit=["War Plate", "Radium Carabiner", "Purity Seals"])
    pk = uid(u, "primus")
    pr = model(u, "Skitarii Primus", 0, 1, 26,
               unit_profile(u, "Skitarii Primus", "Infantry (Character)", 4, 3, 3, 4, 1, 3, 2, 8, "4+"),
               kit=["War Plate", "Radium Carabiner", "Purity Seals"],
               groups=[slot(pk, "Replace Radium Carabiner", "Radium Carabiner",
                            [("Radium Pistol", 0), ("Bolt Pistol", 1), ("Galvanic Rifle", 5), ("Volkite Charger", 5),
                             ("Volkite Serpenta", 5), ("Phosphor Blast Pistol", 5), ("Arc Rifle", 10),
                             ("Arc Pistol", 10), ("Graviton Gun", 15)]),
                       take(pk, "Melee weapon (one)", [("Power Weapon", 10), ("Taser Goad", 10),
                                                       ("Corposant Stave", 10), ("Arc Maul", 15), ("Power Fist", 15)],
                            max_total=1),
                       take(pk, "Wargear", [("Power Armour", 10), ("Refractor Field", 10), ("Auspex", 5),
                                            ("Omnispex", 5), ("Infravisor", 5), ("Melta Bombs", 5),
                                            ("Shattersphere Grenades", 5)]),
                       show_any(take(pk, "Rad-Alchemy (Genetor)", [("Rad Grenades", 10)]),
                                o("Genetor - Magos Biologis"))],
               entries=[master_crafted(pk)])
    sid = sk.get("id")
    add_mods(sk, specials_decrement(sid, uid(sid, "min"), uid(sid, "max"), [pr.get("id")], u))
    pg, _ = pool(u, "Plasma Guns (up to two Skitarii, replace Radium Carabiner)", u, [("Plasma Gun", 15)], 2)
    e2, g2, m2 = order_extras(u, n, True)
    return unit(n, 0, TROOPS, "Troops", models=[sk, pr], rules_=["Iron and Machine"],
                entries=[per_model(u, "Frag Grenades (entire unit)", 1, u, ["Frag Grenades"]),
                         per_model(u, "Krak Grenades (entire unit)", 2, u, ["Krak Grenades"]),
                         exploration_party(u)] + e2,
                groups=[pg, transport(u, ["Mechanicum Rhino Armoured Carrier", "Triaros Armoured Conveyor"], 10)] + g2,
                mods=m2)


def secutarii(n, base, per, mname, aname, sv, kit, rules_, alpha_groups, unit_extra=(), unit_groups=()):
    u = U(n)
    men = model(u, mname, 9, 19, per, unit_profile(u, mname, "Infantry", 3, 4, 3, 3, 1, 3, 1, 7, sv), kit=kit)
    alpha = model(u, aname, 1, 1, 0, unit_profile(u, aname, "Infantry (Character)", 3, 4, 3, 3, 2, 3, 2, 8, sv),
                  kit=kit, groups=alpha_groups(uid(u, "alpha")))
    e2, g2, m2 = order_extras(u, n, True)
    return unit(n, base - 9 * per, TROOPS, "Troops", models=[men, alpha], rules_=rules_,
                entries=list(unit_extra) + [exploration_party(u)] + e2,
                groups=[g(u, men.get("id")) for g in unit_groups] + [transport(u, ["Triaros Armoured Conveyor"])] + g2,
                mods=m2)


ALPHA_PISTOLS = [("Radium Pistol", 5), ("Volkite Serpenta", 5), ("Arc Pistol", 10)]


def hoplites():
    return secutarii("Secutarii Hoplite Phalanx", 130, 12, "Secutarii Hoplite", "Hoplite Alpha", "4+/5+",
                     ["War Plate", "Arc Lance", "Mag-inverter Shield", "Kyropatris Field Generator"],
                     ["Feel No Pain (6+)"],
                     lambda ak: [take(ak, "Pistol (one)", ALPHA_PISTOLS, max_total=1),
                                 slot(ak, "Replace Arc Lance", "Arc Lance", [("Arc Maul", 0), ("Power Weapon", 0)]),
                                 take(ak, "Wargear", [("Auspex", 5), ("Rad Grenades", 10)])])


def peltasts():
    n = "Secutarii Peltast Phalanx"
    u = U(n)
    gc = "Galvanic Caster with Flechette and Ignis Ammunition"
    return secutarii(n, 120, 10, "Secutarii Peltast", "Peltast Alpha", "4+",
                     ["War Plate", gc, "Kyropatris Field Generator"], ["Feel No Pain (6+)", "Blind Barrage"],
                     lambda ak: [take(ak, "Pistol (one)", ALPHA_PISTOLS, max_total=1),
                                 slot(ak, "Replace Galvanic Caster", gc, [("Arc Maul", 0), ("Power Weapon", 0)]),
                                 take(ak, "Wargear", [("Auspex", 5), ("Rad Grenades", 10), ("Refractor Field", 10)])],
                     unit_extra=[per_model(u, "Hammershot Ammunition (entire unit)", 5, u, ["Hammershot Ammunition"])],
                     unit_groups=[lambda u_, mid: model_swaps(u_, "Secutarii Peltasts: replace Galvanic Caster (any)",
                                                              u_, [mid], [("Radium Carabiner", 0), ("Arc Rifle", 10)])])


def thallax():
    n = "Thallax Cohort"
    u = U(n)
    m = model(u, "Thallax", 3, 9, 40, unit_profile(u, "Thallax", "Jet Pack Infantry", 3, 4, 5, 5, 3, 2, 2, 8, "4+"),
              kit=["Lorica Thallax", "Lightning Gun", "Close Combat Weapon", "Frag Grenades", "Jet Pack"])
    aug = choice(u, "Augment (entire unit, one)", [
        ("Destructor", 15, False, [], ["Tank Hunters"]), ("Empyrite", 10, False, [], ["Deep Strike"]),
        ("Ferrox", 25, False, [], ["Rage", "Rending"]), ("Icarian", 25, False, [], [])], unit_id=u)
    ferrox = uid("choice", u, "Augment (entire unit, one)", "Ferrox")
    sp, _ = pool(u, "Replace Lightning Gun (one per three models)", u,
                 [("Multilaser", 5), ("Phased Plasma-Fusil", 10), ("Irad Cleanser", 10), ("Multi-Melta", 15),
                  ("Photon Thruster", 25)], 0, every=3)
    hide_any(sp, cond(ferrox, u, "atLeast", 1))
    e2, g2, m2 = order_extras(u, n, True)
    return unit(n, 15, TROOPS, "Troops", models=[m],
                rules_=["Bulky", "Iron and Machine", "Relentless", "Stubborn", "Djinn-sight", "Thallax Augments"],
                entries=[per_model(u, "Melta Bombs (entire unit)", 5, u, ["Melta Bombs"]), exploration_party(u)] + e2,
                groups=[aug, sp, transport(u, ["Triaros Armoured Conveyor"], 6)] + g2,
                mods=m2)


def castellax():
    n = "Castellax Class Battle-Automata Maniple"
    u = U(n)
    e = automata_unit(
        n, TROOPS, "Troops", "Castellax", 105, 5,
        lambda u_: unit_profile(u_, "Castellax", "Monstrous Creature", 3, 4, 6, 7, 4, 3, 2, 7, "3+/5+"),
        ["Mauler Bolt Cannon", "Bolter", "Shock Chargers", "Atomantic Shielding"],
        ["Cybernetica Cortex", "Programmed Behaviour", "Reactor Blast", "Rage", "Support Unit", "Atomantic Shielding"],
        groups_fn=lambda mk: [slot(mk, "Replace Mauler Bolt Cannon", "Mauler Bolt Cannon",
                                   [("Multi-Melta", 0), ("Darkfire Cannon", 20)]),
                              slot(mk, "Bolter 1", "Bolter", [("Flamer", 5)]),
                              slot(mk, "Bolter 2", "Bolter", [("Flamer", 5)]),
                              slot(mk, "Replace Shock Chargers", "Shock Chargers",
                                   [("Battle-Automata Power Blades", 10), ("Siege Wrecker", 20)])],
        whole=[("Searchlight", 1), ("Frag Grenades", 5), ("Infravisor", 5), ("Enhanced Targeting Array", 15)],
        compulsory=False,
        extra_mods=[modifier("add", "category", LINE, conds=[o("Legio Cybernetica"), cond("model", u, "atLeast", 2)])])
    return e


# ============================================================ TRANSPORTS
def veh(u, name, prof_vals, ut):
    return vehicle_profile(u, name, ut, *prof_vals)


def rhino():
    n = "Mechanicum Rhino Armoured Carrier"
    t = TRANSPORT_IDS[n]
    return entry(t, n, typ="unit", cost=40, cats=[foc(gs.CAT_TRANSPORT, "Dedicated Transport", t)],
                 profiles=[vehicle_profile(t, "Mechanicum Rhino", "Vehicle (Tank, Transport)", 3, 11, 11, 10),
                           transport_profile(t, n, "10 models (no Bulky, Very Bulky or Extremely Bulky models)",
                                             "One on each side, one at the rear",
                                             "Up to two models through the top hatch")],
                 infolinks=rules_links(["Repair"], key=t),
                 links=[gear(t, x) for x in ["Storm Bolter", "Smoke Launchers", "Searchlight"]],
                 groups=[take(t, "Options", [("Dozer Blade", 5), ("Extra Armour", 5), ("Hunter-Killer Missile", 5),
                                             ("Blessed Autosimulacra", 5), ("Pintle-mounted Storm Bolter", 10)])])


def triaros():
    n = "Triaros Armoured Conveyor"
    t = TRANSPORT_IDS[n]
    return entry(t, n, typ="unit", cost=135, cats=[foc(gs.CAT_TRANSPORT, "Dedicated Transport", t)],
                 profiles=[vehicle_profile(t, n, "Vehicle (Tank, Transport)", 3, 14, 12, 12),
                           transport_profile(t, n, "20 models (Thallax may embark despite being Jet Pack Infantry)",
                                             "One on each side of the hull", "None")],
                 infolinks=rules_links(["Galvanic Traction Drive", "Volkite Sentinels", "Shock Ram"], key=t),
                 links=[gear(t, "Twin-linked Mauler Bolt Cannon"), gear_n(t, "Volkite Sentinel", 2),
                        gear(t, "Flare Shield"), gear(t, "Shock Ram"), gear(t, "Searchlight")],
                 groups=[take(t, "Options", [("Extra Armour", 5), ("Hunter-Killer Missile", 5, 2),
                                             ("Smoke Launchers", 5), ("Blessed Autosimulacra", 5)])])


# ============================================================ FAST ATTACK
def vunit(n, cost, slot_cat, slot_name, prof, kit, rules_, groups, entries=(), mods=(), kit_links=()):
    u = U(n)
    e = unit(n, cost, slot_cat, slot_name, profiles=[prof(u)], kit=kit, rules_=rules_, groups=groups(u),
             entries=list(entries), mods=list(mods))
    if kit_links:
        add_to(e, "entryLinks", [f(u) for f in kit_links])
    return e


def termite():
    n = "Terrax Pattern Termite Assault Drill"
    u = U(n)
    return unit(n, 85, FA, "Fast Attack",
                profiles=[vehicle_profile(u, "Termite Assault Drill", "Vehicle (Tank, Transport)", 4, 12, 12, 10),
                          transport_profile(u, n, "12 models (no Very Bulky or Extremely Bulky models)",
                                            "One access hatch on each side of the hull", "-")],
                rules_=["Deep Strike", "Subterranean Assault", "Death From Below", "Crawling Advance", "Melta Cutters"],
                groups=[slot(u, "Heavy Flamer 1", "Heavy Flamer", [("Twin-linked Volkite Charger", 0)]),
                        slot(u, "Heavy Flamer 2", "Heavy Flamer", [("Twin-linked Volkite Charger", 0)]),
                        take(u, "Options", [("Blessed Autosimulacra", 5), ("Extra Armour", 5),
                                            ("Armoured Ceramite", 20)])])


def ursarax():
    n = "Ursarax Cohort"
    u = U(n)
    m = model(u, "Ursarax", 3, 9, 50, unit_profile(u, "Ursarax", "Jump Infantry", 4, 3, 5, 5, 3, 2, 2, 8, "4+"),
              kit=["Lorica Thallax", "Two Lightning Claws", "Volkite Incinerator", "Frag Grenades"])
    e2, g2, m2 = order_extras(u, n, True)
    return unit(n, 25, FA, "Fast Attack", models=[m], rules_=["Bulky", "Stubborn", "Feel No Pain (5+)", "Prisoned"],
                groups=[model_swaps(u, "Replace Two Lightning Claws (any model)", u, [m.get("id")],
                                    [("Two Power Fists", 10)])] + g2, entries=e2, mods=m2)


def tarantula():
    n = "Tarantula Sentry Gun Battery"
    u = U(n)
    mk = uid(u, "gun")
    m = model(u, "Tarantula Sentry Gun", 1, 3, 30,
              unit_profile(u, "Tarantula Sentry Gun", "Artillery (Immobile)", "-", 3, "-", 6, 2, "-", "-", "-", "3+"),
              kit=["Twin-linked Heavy Bolter"],
              groups=[slot(mk, "Replace Twin-linked Heavy Bolter", "Twin-linked Heavy Bolter",
                           [("Twin-linked Multilaser", 0), ("Twin-linked Heavy Flamer", 0),
                            ("Two Twin-linked Rotor Cannons", 0), ("Twin-linked Mauler Bolt Cannon", 10),
                            ("Twin-linked Lascannon", 10), ("Twin-linked Photon Thruster", 15),
                            ("Twin-linked Volkite Culverin", 20), ("Multi-Melta and Searchlight", 5)])])
    return unit(n, 0, FA, "Fast Attack", models=numbered(m, 3, 1),
                rules_=["Automated Artillery", "Firing Modes", "Anima Override"],
                groups=[choice(u, "Battery upgrade (one)", [
                    ("Concealment", 10, True, [], ["Concealment (Tarantula)", "Stealth"]),
                    ("Forward Deployment", 5, True, [], ["Forward Deployment (Tarantula)", "Scout"]),
                    ("Drop Capsule", 20, True, [], ["Drop Capsule (Tarantula)", "Deep Strike"])], unit_id=u)])


def vorax():
    return automata_unit(
        "Vorax Class Battle-Automata Maniple", FA, "Fast Attack", "Vorax", 65, 6,
        lambda u: unit_profile(u, "Vorax", "Monstrous Creature", 4, 4, 6, 6, 3, 4, "2(3)", 7, "4+"),
        ["Lightning Gun", "Two Rotor Cannons", "Battle-Automata Power Blades", "Infravisor"],
        ["Cybernetica Cortex", "Programmed Behaviour", "Fleet", "Scout", "Paired"],
        groups_fn=lambda mk: [slot(mk, "Replace Lightning Gun", "Lightning Gun", [("Irad Cleanser", 10)])],
        whole=[("Searchlight", 1), ("Frag Grenades", 5), ("Enhanced Targeting Array", 15),
               ("Bio-corrosive Ammunition", 10)], paragon_ok=False)


def arlatax():
    n = "Arlatax Class Battle-Automata Maniple"
    u = U(n)
    hom = opt(u, "The Homonculex (Anacharis Scoria)", 0, rules_=["The Homonculex", "Paragon of Metal", "Rage",
                                                                 "It Will Not Die", "Rampage"],
              show=[in_r(SCORIA)])
    add_to(hom, "constraints", [unique(oid(u, "The Homonculex (Anacharis Scoria)"), 1, "roster")])
    return automata_unit(
        n, FA, "Fast Attack", "Arlatax", 175, 3,
        lambda u_: unit_profile(u_, "Arlatax", "Flying Monster", 4, 3, 7, 6, 4, 4, 3, 8, "3+/5+"),
        ["Atomantic Shielding", "Arlatax Power Claw", "Plasma Blaster", "Frag Grenades"],
        ["Cybernetica Cortex", "Programmed Behaviour", "Reactor Blast", "Feel No Pain (6+)", "Atomantic Shielding"],
        groups_fn=lambda mk: [slot_e(mk, "Replace one Arlatax Power Claw", "Arlatax Power Claw", [("Arc Scourge", 10)])],
        extra_entries=[hom])


def vultarax():
    return automata_unit(
        "Vultarax Stratos-Automata Maniple", FA, "Fast Attack", "Vultarax", 175, 3,
        lambda u: unit_profile(u, "Vultarax", "Flying Monster", 3, 4, 4, 6, 4, 3, 2, 8, "3+"),
        ["Vultarax Arc Blaster", "Two Setheno Pattern Havoc Launchers", "Enhanced Targeting Array", "Flare Shield",
         "Searchlight"],
        ["Cybernetica Cortex", "Programmed Behaviour", "Reactor Blast", "Night Vision", "Flare Shield (Vultarax)",
         "Setheno-Djinn"],
        groups_fn=lambda mk: [take(mk, "Options", [("Battle-Automata Power Blades", 15)])],
        whole=[("Blessed Autosimulacra", 10)], paragon_ok=False)


def land_speeders():
    n = "Mechanicum Land Speeder Squadron"
    u = U(n)
    mk = uid(u, "ls")
    m = model(u, "Mechanicum Land Speeder", 1, 3, 65,
              vehicle_profile(u, "Mechanicum Land Speeder", "Vehicle (Fast, Skimmer)", 3, 10, 10, 10),
              kit=["Multilaser", "Heavy Flamer"],
              groups=[slot(mk, "Replace Multilaser", "Multilaser",
                           [("Heavy Bolter", -5), ("Twin-linked Typhoon Missile Launcher", 10), ("Multi-Melta", 15),
                            ("Graviton Gun", 15)]),
                      slot(mk, "Replace Heavy Flamer", "Heavy Flamer",
                           [("Assault Cannon", 10), ("Twin-linked Heavy Bolter", 35), ("Multi-Melta", 40),
                            ("Plasma Cannon", 45), ("Graviton Cannon", 45), ("Twin-linked Lascannon", 55)])])
    return unit(n, 0, FA, "Fast Attack", models=numbered(m, 3, 1), rules_=["Crew: Servitors"])


def triaros_guardian():
    n = "Triaros Guardian"
    u = U(n)
    return unit(n, 135, FA, "Fast Attack",
                profiles=[vehicle_profile(u, n, "Vehicle (Tank)", 4, 14, 12, 12)],
                kit=["Twin-linked Mauler Bolt Cannon", "Flare Shield", "Shock Ram", "Searchlight"],
                rules_=["Void Shield Projector", "Galvanic Traction Drive", "Shock Ram", "Volkite Sentinels"],
                groups=[take(u, "Options", [("Void Shield", 35, 2), ("Extra Armour", 5), ("Hunter-Killer Missile", 5, 2),
                                            ("Smoke Launchers", 5), ("Blessed Autosimulacra", 15)])],
                links_extra=[gear_n(u, "Volkite Sentinel", 2)])


def crusader():
    return automata_unit(
        "Crusader Class Robot Maniple", FA, "Fast Attack", "Crusader Robot", 90, 4,
        lambda u: unit_profile(u, "Crusader Robot", "Monstrous Creature", 4, 4, 5, 5, 3, 4, 2, 7, "4+/5+"),
        ["Lascannon", "Two Power Swords", "Atomantic Shielding"],
        ["Cybernetica Cortex", "Programmed Behaviour", "Fleet", "Scout", "Reactor Blast", "Two Power Swords",
         "Atomantic Shielding"],
        groups_fn=lambda mk: [slot(mk, "Replace Lascannon", "Lascannon", [("Heavy Bolter", -10), ("Meltagun", 0)])])


def seekers():
    return automata_unit(
        "Seeker Robot Maniple", FA, "Fast Attack", "Seeker Robot", 65, 5,
        lambda u: unit_profile(u, "Seeker Robot", "Infantry", 3, 4, 4, 5, 2, 4, 1, 8, "4+"),
        ["Volkite Charger", "Enhanced Targeting Array", "Infravisor", "Auspex"],
        ["Cybernetica Cortex", "Programmed Behaviour", "Scout", "Infiltrate", "Stealth", "Target Acquisition"],
        groups_fn=lambda mk: [slot(mk, "Replace Volkite Charger", "Volkite Charger",
                                   [("Rotor Cannon", 0), ("Lightning Gun", 10), ("Graviton Gun", 15)])],
        paragon_ok=False)


def bombots():
    n = "Bombot Maniple"
    u = U(n)
    m = model(u, "Bombot", 1, 5, 25, unit_profile(u, "Bombot", "Infantry", 2, "-", 4, 4, 1, 2, 1, 10, "4+"),
              kit=["Internal Demolition Charge"])
    return unit(n, 0, FA, "Fast Attack", models=[m],
                rules_=["Fearless", "Expendable", "Programmed Demolition", "Detonation", "Volatile Payload"])


# ========================================================== HEAVY SUPPORT
TH_RULES = ["Cybernetica Cortex", "Programmed Behaviour", "Reactor Blast", "Lumbering Advance", "Atomantic Shielding"]


def thanatars():
    fm = [err("Flesh-Mechanica: No Engines Greater than Flesh - Thanatar Siege-Automata may not be included.",
              o("Flesh-Mechanica"))]
    out = [automata_unit("Thanatar-Cavas Siege-Automata Maniple", HS, "Heavy Support", "Thanatar-Cavas", 250, 3,
                         lambda u: unit_profile(u, "Thanatar-Cavas", "Monstrous Creature", 3, 4, 8, 8, 4, 2, 2, 8, "2+/5+"),
                         ["Hellex Plasma Mortar", "Twin-linked Mauler Bolt Cannon", "Infravisor", "Atomantic Shielding"],
                         TH_RULES + ["Plasma Wave"],
                         whole=[("Searchlight", 1), ("Enhanced Targeting Array", 15)], extra_mods=fm),
           automata_unit("Thanatar-Cynis Siege-Automata Maniple", HS, "Heavy Support", "Thanatar-Cynis", 275, 3,
                         lambda u: unit_profile(u, "Thanatar-Cynis", "Monstrous Creature", 3, 4, 8, 8, 4, 2, 2, 8, "2+/5+"),
                         ["Mauler Bolt Cannon", "Two Cynis Pattern Plasma Ejectors", "Infravisor",
                          "Atomantic Shielding"], TH_RULES + ["Plasma Wave"],
                         whole=[("Searchlight", 1), ("Enhanced Targeting Array", 15)], extra_mods=fm)]
    n = "Thanatar-Calix Siege-Automata"
    u = U(n)
    e2, g2, m2 = order_extras(u, n, False, paragon_id=oid(u, "Paragon of Metal"))
    out.append(unit(n, 295, HS, "Heavy Support",
                    profiles=[unit_profile(u, "Thanatar-Calix", "Monstrous Creature", 3, 4, 8, 8, 4, 2, 2, 8, "2+/5+")],
                    kit=["Sollex Pattern Heavy Lascannon", "Twin-linked Mauler Bolt Cannon", "Graviton Ram",
                         "Infravisor", "Atomantic Shielding"], rules_=TH_RULES + ["Wrecker"],
                    groups=[take(u, "Options", [("Searchlight", 1), ("Enhanced Targeting Array", 15)])] + g2,
                    entries=[opt(u, "Paragon of Metal", 35, rules_=["Paragon of Metal", "It Will Not Die", "Rampage"])]
                    + e2, mods=m2 + [copy_mod(fm[0])]))
    for e in out:
        show_any(e, not_o("Flesh-Mechanica"))
    return out


def copy_mod(m):
    import copy as _c
    return _c.deepcopy(m)


def krios():
    n = "Krios Battle Tank Squadron"
    u = U(n)
    mk = uid(u, "krios")
    m = model(u, "Krios Battle Tank", 1, 3, 125,
              vehicle_profile(u, "Krios Battle Tank", "Vehicle (Tank, Fast)", 4, 13, 12, 10),
              kit=["Lightning Cannon", "Flare Shield", "Blessed Autosimulacra", "Searchlight"],
              groups=[slot(mk, "Krios Venator (replace Lightning Cannon)", "Lightning Cannon", [("Pulsar-Fusil", 25)]),
                      take(mk, "Options", [("Extra Armour", 5), ("Hunter-Killer Missile", 5, 2), ("Smoke Launchers", 5),
                                           ("Anbaric Claw", 15), ("Volkite Sentinel", 15, 2)])],
              mods=[modifier("set", "name", "Krios Venator", conds=[cond(W("Pulsar-Fusil"), "self", "atLeast", 1)])])
    return unit(n, 50, HS, "Heavy Support", models=numbered(m, 3, 1), rules_=["Galvanic Traction Drive"])


def karacnos():
    n = "Karacnos Assault Tank"
    u = U(n)
    return unit(n, 225, HS, "Heavy Support", profiles=[vehicle_profile(u, "Karacnos", "Vehicle (Tank)", 4, 14, 12, 12)],
                kit=["Karacnos Mortar Battery", "Two Lightning-Blaster Sentinels", "Flare Shield", "Shock Ram",
                     "Searchlight"],
                rules_=["Galvanic Traction Drive", "Hazardous Munitions", "Shock Ram", "Rad-phage"],
                groups=[take(u, "Options", [("Extra Armour", 5), ("Hunter-Killer Missile", 5, 2), ("Smoke Launchers", 5),
                                            ("Blessed Autosimulacra", 5)])])


def conqueror():
    return automata_unit(
        "Conqueror Class Robot Maniple", HS, "Heavy Support", "Conqueror Robot", 110, 4,
        lambda u: unit_profile(u, "Conqueror Robot", "Monstrous Creature", 4, 4, 6, 6, 3, 3, 2, 7, "3+/5+"),
        ["Autocannon", "Heavy Bolter", "Power Fist", "Atomantic Shielding"],
        ["Cybernetica Cortex", "Programmed Behaviour", "Reactor Blast", "Tank Hunters", "Atomantic Shielding"],
        groups_fn=lambda mk: [slot(mk, "Replace Autocannon", "Autocannon",
                                   [("Lascannon", 10), ("Meltagun", -10), ("Heavy Bolter", -5)]),
                              slot(mk, "Replace Heavy Bolter", "Heavy Bolter",
                                   [("Autocannon", 5), ("Lascannon", 15), ("Flamer", -10), ("Meltagun", 0)]),
                              slot(mk, "Replace Power Fist", "Power Fist",
                                   [("Autocannon", 10), ("Heavy Bolter", 5), ("Meltagun", 0)])])


def leman_russ():
    n = "Mechanicum Leman Russ Squadron"
    u = U(n)
    data = [("Leman Russ Battle Tank", 140, (14, 12, 10), "Battle Cannon"),
            ("Leman Russ Exterminator", 120, (14, 12, 10), "Twin-linked Autocannon"),
            ("Leman Russ Conqueror", 145, (14, 12, 11), "Conqueror Cannon"),
            ("Leman Russ Demolisher", 150, (14, 13, 11), "Demolisher Cannon"),
            ("Leman Russ Vanquisher", 175, (14, 12, 10), "Vanquisher Battle Cannon")]
    ids = [uid("model", u, d[0]) for d in data]
    models = []
    for (mn, cost, (f, s, r), gun), mid in zip(data, ids):
        others = [cond(c, u, "atLeast", 1) for x in ids if x != mid for c in [x] + [uid(x, "copy", i) for i in (2, 3)]]
        sponsons = [("Two Heavy Bolters (sponsons)", 10), ("Two Heavy Flamers (sponsons)", 10)]
        if "Demolisher" in mn:
            sponsons += [("Two Multi-Meltas (sponsons)", 30), ("Two Plasma Cannons (sponsons)", 20)]
        m = entry(mid, mn, typ="model", cost=cost, constraints=[constraint(uid(mid, "max"), "max", 3)],
                  mods=[modifier("set", "hidden", "true", groups=[any_of(*others)]),
                        modifier("set", uid(mid, "max"), 0,
                                 groups=[any_of(*[copy_cond(c) for c in others])])],
                  profiles=[vehicle_profile(u, mn, "Vehicle (Tank)", 3, f, s, r)],
                  links=[gear(mid, gun)],
                  groups=[must_take(mid, "Hull-mounted weapon", [("Hull-mounted Heavy Bolter", 5),
                                                                  ("Hull-mounted Lascannon", 15)],
                                    "Hull-mounted Heavy Bolter"),
                          take(mid, "Sponsons (one pair)", sponsons, max_total=1),
                          take(mid, "Options", [("Extra Armour", 5), ("Hunter-Killer Missile", 5), ("Searchlight", 1),
                                                ("Smoke Launchers", 5), ("Blessed Autosimulacra", 10)])])
        models += numbered(m, 3, 0)
    return unit(n, 0, HS, "Heavy Support", models=models, rules_=["Crew: Servitors"],
                mods=[err_any("A Leman Russ Squadron contains 1-3 Leman Russ, all of the same type.",
                              cond("model", u, "lessThan", 1), cond("model", u, "greaterThan", 3))])


def land_raider():
    n = "Mechanicum Land Raider"
    u = U(n)
    return unit(n, 245, HS, "Heavy Support",
                profiles=[vehicle_profile(u, n, "Vehicle (Tank, Transport)", 3, 14, 14, 14),
                          transport_profile(u, n, "10 models; alternatively up to 20 Tech-Thralls, or 9 Tech-Thralls "
                                                  "and one Independent Character", "One at the front, one on either side",
                                            "-")],
                kit=["Twin-linked Heavy Bolter", "Searchlight", "Smoke Launchers"],
                rules_=["Power of the Machine Spirit", "Assault Vehicle"],
                groups=[take(u, "Options", [("Dozer Blade", 5), ("Extra Armour", 5), ("Hunter-Killer Missile", 5),
                                            ("Blessed Autosimulacra", 10), ("Pintle-mounted Storm Bolter", 10),
                                            ("Armoured Ceramite", 20)])],
                links_extra=[gear_n(u, "Twin-linked Lascannon", 2)])


def macrocarid():
    n = "Macrocarid Explorator"
    u = U(n)
    return unit(n, 195, HS, "Heavy Support",
                profiles=[vehicle_profile(u, n, "Vehicle (Tank, Transport)", 4, 14, 14, 14),
                          transport_profile(u, n, "10 models", "One on either side", "-")],
                kit=["Mauler Bolt Cannon", "Two Lascannons", "Auspex", "Searchlight", "Smoke Launchers", "Extra Armour",
                     "Blessed Autosimulacra"],
                rules_=["Power of the Machine Spirit"],
                groups=[slot(u, "Replace Mauler Bolt Cannon", "Mauler Bolt Cannon",
                             [("Volkite Culverin", 0), ("Multi-Melta", 0), ("Twin-linked Phased Plasma-Fusil", 10),
                              ("Twin-linked Irad Cleanser", 10), ("Lascannon", 5), ("Conversion Beamer", 15),
                              ("Graviton Imploder", 15)]),
                        slot(u, "Replace Two Lascannons", "Two Lascannons",
                             [("Two Twin-linked Mauler Bolt Cannons", 0), ("Two Twin-linked Lascannons", 20),
                              ("Two Irradiation Engines", 40)]),
                        take(u, "Options", [("Hunter-Killer Missile", 5), ("Dozer Blade", 5), ("Auxiliary Drive", 10),
                                            ("Anbaric Claw", 10), ("Armoured Ceramite", 20), ("Flare Shield", 25),
                                            ("Explorator Augury Web", 50), ("Servo-Rig", 20)])])


def artillery_battery():
    n = "Ordo Reductor Artillery Tank Battery"
    u = U(n)
    mk = uid(u, "tank")
    m = model(u, "Artillery Tank", 1, 3, 85, vehicle_profile(u, "Artillery Tank", "Vehicle (Tank)", 4, 12, 10, 10),
              kit=["Searchlight", "Smoke Launchers"],
              groups=[take(mk, "Hull-mounted weapon (one)", [("Hull-mounted Heavy Bolter", 10),
                                                             ("Hull-mounted Heavy Flamer", 10)], max_total=1),
                      take(mk, "Options", [("Hunter-Killer Missile", 5), ("Dozer Blade", 5), ("Auxiliary Drive", 10),
                                           ("Extra Armour", 10), ("Blessed Autosimulacra", 10),
                                           ("Power of the Machine Spirit (upgrade)", 10), ("Siege Plating", 15)])])
    wpn = choice(u, "Battery weapon (all vehicles the same)", [
        ("Whirlwind Launcher", 0, True, ["Whirlwind Launcher with Vengeance and Castellan Missiles"], []),
        ("Demolisher Cannon", 10, True, ["Demolisher Cannon"], []), ("Quad Lascannon", 15, True, ["Quad Lascannon"], []),
        ("Dual Melta Cannon", 20, True, ["Dual Melta Cannon"], []),
        ("Earthshaker Cannon", 30, True, ["Earthshaker Cannon"], []),
        ("Medusa Cannon", 45, True, ["Medusa Cannon"], []),
        ("Mars-Colossus Bombard", 50, True, ["Mars-Colossus Bombard"], [])],
        unit_id=u, required=True, default="Whirlwind Launcher")
    e = unit(n, 0, HS, "Heavy Support", models=numbered(m, 3, 1), groups=[wpn],
             mods=[err("Ordo Reductor Artillery Tank Battery: Ordo Reductor only.", not_o("Ordo Reductor"))])
    return show_any(e, o("Ordo Reductor"))


def minotaur():
    n = "Ordo Reductor Minotaur Battery"
    u = U(n)
    mk = uid(u, "mino")
    m = model(u, "Ordo Reductor Minotaur", 1, 3, 205,
              vehicle_profile(u, "Ordo Reductor Minotaur", "Vehicle (Tank)", 4, 13, 12, 13),
              kit=["Dual Earthshaker Cannon", "Searchlight", "Smoke Launchers", "Blessed Autosimulacra",
                   "Rear-facing Flare Shield", "Extra Armour"],
              groups=[take(mk, "Options", [("Pintle-mounted Heavy Bolter", 10), ("Pintle-mounted Heavy Flamer", 10),
                                           ("Pintle-mounted Phased Plasma-Fusil", 10), ("Anbaric Claw", 10),
                                           ("Armoured Ceramite", 10), ("Auxiliary Drive", 10), ("Dozer Blade", 5)])])
    e = unit(n, 0, HS, "Heavy Support", models=numbered(m, 3, 1),
             rules_=["Indirect Fire (Minotaur)", "Special Configuration"],
             mods=[err("Ordo Reductor Minotaur Battery: Ordo Reductor only.", not_o("Ordo Reductor"))])
    return show_any(e, o("Ordo Reductor"))


# ========================================================= DARK MECHANICUM
def avail(e, allowed, label):
    show_any(e, *[o(x) for x in allowed])
    add_mods(e, [err(f"{e.get('name')}: {label} only.", *[not_o(x) for x in allowed])])
    return e


DARK_RULES = ["Daemon", "Fear", "Unstable"]


def possessed():
    n = "Possessed Battle-Automata"
    u = U(n)
    mk = uid(u, "pba")
    m = model(u, n, 1, 3, 120, unit_profile(u, n, "Monstrous Creature", 4, 3, 6, 6, 3, 4, 3, 7, "3+/5++"),
              kit=["Possessed Power Claw", "Warp-spitter"],
              groups=[slot(mk, "Replace Warp-spitter", "Warp-spitter",
                           [("Heavy Flamer", 0), ("Mauler Bolt Cannon", 10), ("Plasma Blaster", 15),
                            ("Multi-Melta", 15)])])
    add_to(m, "entryLinks", [])
    e = unit(n, 0, ELITES, "Elites", models=numbered(m, 3, 1),
             rules_=DARK_RULES + ["Fearless", "Fleet", "Move Through Cover", "Rage", "Reactor Blast", "Daemon Engine"])
    return avail(e, ["Daemon Engine Horde"], "Daemon Engine Horde")


def abominants():
    n = "Abominant Servitor Maniple"
    u = U(n)
    kit = ["Abominant Claws", "Industrial Stubber"]
    ser = model(u, "Abominant Servitor", 2, 5, 30,
                unit_profile(u, "Abominant Servitor", "Infantry", 4, 2, 5, 5, 3, 2, 3, 7, "4+"), kit=kit)
    ov = model(u, "Abominant Overseer", 1, 1, 0,
               unit_profile(u, "Abominant Overseer", "Infantry", 4, 3, 5, 5, 3, 2, 4, 8, "4+"), kit=kit)
    e = unit(n, 100 - 60, ELITES, "Elites", models=[ser, ov],
             rules_=["Iron and Machine", "Feel No Pain (5+)", "Stubborn", "Bulky", "Fear", "Fleshcrafted Brutes"],
             groups=[model_swaps(u, "Replace Industrial Stubber (any model)", u, [ser.get("id"), ov.get("id")],
                                 [("Flamer", 0), ("Meltagun", 10)])])
    return avail(e, ["Flesh-Mechanica"], "Flesh-Mechanica")


def revenants():
    n = "Scrapcode Revenant Maniple"
    u = U(n)
    m = model(u, "Scrapcode Revenant", 3, 6, 30,
              unit_profile(u, "Scrapcode Revenant", "Infantry", 3, 3, 4, 4, 2, 3, 2, 7, "4+"),
              kit=["Scrapcode Projector", "Electro-blade"])
    e = unit(n, 0, ELITES, "Elites", models=[m],
             rules_=["Iron and Machine", "Fearless", "Scrapcode Emanation", "Machine Revenants"])
    return avail(e, ["Scrapcode Covenant"], "Scrapcode Covenant")


def wretched():
    n = "Wretched Servitor Covenant"
    u = U(n)
    ws = model(u, "Wretched Servitor", 9, 29, 4,
               unit_profile(u, "Wretched Servitor", "Infantry", 2, 2, 3, 3, 1, 2, 1, 6, "6+"),
               kit=["Crude Firearm", "Close Combat Weapon"])
    ov = model(u, "Overseer", 1, 1, 0, unit_profile(u, "Overseer", "Infantry", 3, 3, 3, 3, 1, 3, 2, 7, "5+"),
               kit=["Crude Firearm", "Close Combat Weapon"],
               groups=[slot(uid(u, "ov"), "Replace Crude Firearm", "Crude Firearm",
                            [("Laspistol", 0), ("Bolt Pistol", 1), ("Radium Pistol", 3), ("Arc Pistol", 5)])])
    sp, _ = pool(u, "Replace Crude Firearm (one per five Wretched Servitors)", u,
                 [("Flamer", 5), ("Heavy Stubber", 5)], 0, every=5, per_child=ws.get("id"))
    e = unit(n, 40 - 36, TROOPS, "Troops", models=[ws, ov], rules_=["Expendable", "Servitor Protocols"], groups=[sp])
    TROOP_UNITS.append(e)
    return avail(e, DARK, "Dark Mechanicum")


def stalkers():
    n = "Stalker Engine Maniple"
    u = U(n)
    m = model(u, "Stalker Engine", 1, 3, 95,
              unit_profile(u, "Stalker Engine", "Monstrous Creature", 4, 3, 6, 6, 3, 4, 3, 7, "3+/5++"),
              kit=["Stalker Claws", "Daemonspitter"],
              groups=[slot(uid(u, "s"), "Replace Daemonspitter", "Daemonspitter",
                           [("Heavy Flamer", 0), ("Volkite Charger", 5), ("Meltagun", 10), ("Plasma Blaster", 15)])])
    e = unit(n, 0, FA, "Fast Attack", models=numbered(m, 3, 1),
             rules_=DARK_RULES + ["Fleet", "Move Through Cover", "Scout", "Daemon Engine"])
    return avail(e, ["Daemon Engine Horde", "Scrapcode Covenant", "Engines of Ruin"],
                 "Dark Mechanicum (not Flesh-Mechanica)")


def slaughterers():
    n = "Slaughterer Engine Maniple"
    u = U(n)
    m = model(u, "Slaughterer Engine", 1, 3, 115,
              unit_profile(u, "Slaughterer Engine", "Monstrous Creature", 5, 2, 6, 6, 3, 4, 4, 7, "3+/5++"),
              kit=["Slaughterer Claws"],
              groups=[take(uid(u, "s"), "Mounted weapon (one)", [("Heavy Flamer", 5), ("Meltagun", 10),
                                                                 ("Plasma Blaster", 15)], max_total=1)])
    e = unit(n, 150 - 115, FA, "Fast Attack", models=numbered(m, 3, 1),
             rules_=DARK_RULES + ["Fleet", "Furious Charge", "Rage", "Move Through Cover", "Paired", "Daemon Engine"])
    return avail(e, ["Daemon Engine Horde", "Engines of Ruin"], "Daemon Engine Horde or Engines of Ruin")


def scrapcode_hunters():
    n = "Scrapcode Hunter"
    u = U(n)
    m = model(u, n, 1, 3, 70, unit_profile(u, n, "Infantry", 3, 4, 5, 5, 2, 4, 2, 8, "4+"),
              kit=["Hunter Arc Carbine", "Manipulator Claws"])
    e = unit(n, 0, FA, "Fast Attack", models=[m],
             rules_=["Iron and Machine", "Scout", "Infiltrate", "Move Through Cover", "Stealth", "Tank Hunters",
                     "Scrapcode Injector"])
    return avail(e, ["Scrapcode Covenant"], "Scrapcode Covenant")


def greater_daemon_engine():
    n = "Greater Daemon Engine"
    u = U(n)
    hp = [("Heavy Flamer", 0), ("Mauler Bolt Cannon", 10), ("Autocannon", 10), ("Multi-Melta", 15),
          ("Plasma Cannon", 20), ("Photon Thruster", 25)]
    e = unit(n, 225, HS, "Heavy Support",
             profiles=[unit_profile(u, n, "Monstrous Creature", 4, 3, 8, 7, 5, 3, 4, 8, "3+/5++")],
             kit=["Greater Engine Claws"],
             rules_=DARK_RULES + ["Fearless", "Move Through Cover", "Reactor Blast", "Wrecker", "Daemon Engine"],
             groups=[must_take(u, "Weapon hardpoint 1", hp, "Heavy Flamer"),
                     must_take(uid(u, "2"), "Weapon hardpoint 2", hp, "Heavy Flamer")],
             entries=[opt(u, "Warp-Wings", 40, gear_=["Warp-Wings"], text="The model becomes a Flying Monster.")])
    return avail(e, ["Daemon Engine Horde"], "Daemon Engine Horde")


def brass_scorpion():
    n = "Brass Scorpion"
    u = U(n)
    e = unit(n, 285, HS, "Heavy Support", profiles=[walker_profile(u, n, 4, 3, 8, 13, 13, 11, 3, 5)],
             kit=["Scorpion Cannon", "Two Hellmaw Flamers", "Two Scorpion Claws"],
             rules_=["Daemon", "Fear", "Fleet", "Move Through Cover", "Daemon Engine", "Catastrophic Explosion"])
    return avail(e, ["Daemon Engine Horde", "Scrapcode Covenant", "Engines of Ruin"],
                 "Dark Mechanicum (not Flesh-Mechanica)")


def infernal_siege_engine():
    n = "Infernal Siege Engine"
    u = U(n)
    e = unit(n, 150, HS, "Heavy Support", profiles=[vehicle_profile(u, n, "Vehicle (Tank)", 3, 13, 12, 10)],
             kit=["Infernal Bombard", "Heavy Bolter"],
             rules_=["Lumbering Advance", "Overcharged Reactor", "Catastrophic Detonation"],
             groups=[slot(u, "Replace Heavy Bolter", "Heavy Bolter", [("Heavy Flamer", 0)]),
                     take(u, "Mechanicum Vehicle Wargear", [
                         ("Dozer Blade", 5), ("Extra Armour", 5), ("Hunter-Killer Missile", 5),
                         ("Pintle-mounted Storm Bolter", 10), ("Searchlight", 1), ("Smoke Launchers", 5),
                         ("Blessed Autosimulacra", 5), ("Armoured Ceramite", 20)])])
    return avail(e, ["Engines of Ruin"], "Engines of Ruin")


def flesh_colossus():
    n = "Flesh-Colossus"
    u = U(n)
    e = unit(n, 190, HS, "Heavy Support",
             profiles=[unit_profile(u, n, "Monstrous Creature", 4, 2, 7, 7, 5, 2, 4, 8, "4+")],
             kit=["Colossal Claws", "Bio-mechanical Cannon"],
             rules_=["Fear", "Feel No Pain (5+)", "It Will Not Die", "Move Through Cover", "Stubborn", "Wrecker",
                     "Very Bulky"],
             groups=[slot(u, "Replace Bio-mechanical Cannon", "Bio-mechanical Cannon",
                          [("Irradiated Bile Projector", 10), ("Bone-scythe Mutation", 0)])])
    return avail(e, ["Flesh-Mechanica"], "Flesh-Mechanica")


# ======================================================== NAMED CHARACTERS
def named(n, cost, stats, kit, rules_, alleg, groups=(), entries=(), mods=(), wl_fixed=False, min_pts=None):
    u = U(n)
    ms = list(mods)
    other = TRAITOR if alleg == "Loyalist" else LOYALIST
    ms.append(hide_if(in_r(other)))
    ms.append(err(f"{n} is {alleg} only.", in_r(other)))
    if min_pts:
        ms.append(modifier("add", "error", f"{n} may only be selected in an army of {min_pts} points or more.",
                           conds=[cond("any", "roster", "lessThan", min_pts, field=PTS, deep=False)]))
    if not wl_fixed:
        ms.append(err(f"{n} must be the army's Warlord.", cond(WARLORD, u, "lessThan", 1)))
    return unit(n, cost, HQ, "HQ", profiles=[unit_profile(u, n, "Infantry (Character)", *stats)], kit=kit,
                rules_=["Independent Character", "Iron and Machine", "Battlesmith", "Cybertheurgist"] + rules_,
                groups=list(groups), entries=list(entries), mods=ms, constraints=[unique(u, 1, "roster")],
                links_extra=[warlord_link(u, hide_orders=[], fixed=wl_fixed,
                                          extra_hide=[] if wl_fixed else [in_r(KH), in_r(ZK)])])


ARCHMAGOS_LIKE = "counts as an Archmagos - no other Archmagos (or Kelbor-Hal / Zagreus Kane / Calleb Decima) allowed."


def lukas_chrom():
    u = CHROM
    e = named("Lukas Chrom", 150, (4, 5, 4, 5, 3, 4, 2, 10, "2+/4+"),
              ["Artificer Armour", "Mechanicum Protectiva", "Volkite Serpenta", "Mechanicum Axe", "Machinator Array",
               "Cortex Controller", "Cyber-familiar", "Infravisor"],
              ["Master of Mondus Gamma", "Lord of the Automata", "Architect of Kaban"], "Traitor")
    # Lukas Chrom has no "must be the Warlord" rule
    for m in list(e.find("modifiers")):
        if m.get("value", "").endswith("must be the army's Warlord."):
            e.find("modifiers").remove(m)
    return e


def kaban():
    n = "Kaban Machine"
    u = U(n)
    return unit(n, 265, HS, "Heavy Support",
                profiles=[unit_profile(u, n, "Monstrous Creature", 4, 4, 7, 7, 5, 4, 4, 10, "2+/5+")],
                kit=["Atomantic Shielding", "Two Kaban Power Claws", "Kaban Integrated Heavy Weapon Systems",
                     "Infravisor"],
                rules_=["Fear", "Fearless", "Relentless", "Move Through Cover", "Reactor Blast", "Abominable Intelligence",
                        "Hunter-Killer Logic", "Independent Targeting", "Architect of Kaban"],
                extra_cats=foc_free("Heavy Support"),
                constraints=[unique(u, 1, "roster")],
                mods=[hide_if(none_r(CHROM)),
                      err("The Kaban Machine may only be selected in an army which includes Lukas Chrom.",
                          none_r(CHROM))])


def scoria():
    return named("Anacharis Scoria", 275, (5, 5, 5, 5, 4, 5, 3, 10, "2+/3+"),
                 ["Artificer Armour", "Mechanicum Protectiva", "Two Archaeotech Pistols", "Vodian Sceptre",
                  "Machinator Array", "Cortex Controller", "Cyber-familiar"],
                 ["Relentless", "Adamantium Will", "Eternal Warrior", "Feel No Pain (5+)", "Patris Cybernetica (Scoria)",
                  "Rite of the Beast", "Forbidden Protocols", "The Homonculex", "The Tyrant of Xana",
                  "Entropic Destroyer"], "Traitor",
                 entries=[opt(SCORIA, "Xanathite Abeyant", 40, gear_=["Photon Thruster", "Xanathite Plating"],
                              rules_=["Xanathite Abeyant", "It Will Not Die", "Move Through Cover", "Very Bulky"])])


def kelbor_hal():
    u = KH
    ents = []
    gid = uid("grp", u, "edict")
    for en in EDICTS:
        ents.append(entry(EDICT[en], en, constraints=[constraint(uid(EDICT[en], "max"), "max", 1, auto=True)],
                          infolinks=rules_links(["Open the Forbidden Vaults"], key=EDICT[en])))
    g = group(gid, "Forbidden Edict (Dark Mechanicum)", entries=ents,
              constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])
    show_any(g, *[o(d) for d in DARK])
    mods = [err(f"Open the Forbidden Vaults: the Edict must belong to a different Dark Techno-Arcana ({en}).",
                in_r(EDICT[en]), o(EDICT_ARCANA[en])) for en in EDICTS]
    mods += [err("Open the Forbidden Vaults: choose one Forbidden Edict.", o(d), *[none_r(EDICT[en]) for en in EDICTS])
             for d in DARK]
    mods += [err_any("Kelbor-Hal " + ARCHMAGOS_LIKE, in_r(AM), in_r(ZK), in_r(CDI))]
    return named("Kelbor-Hal", 400, (4, 5, 4, 5, 5, 4, 3, 10, "2+/3+"),
                 ["Artificer Armour", "Mechanicum Protectiva", "Machinator Array", "Cortex Controller", "Djinn-skein",
                  "Cyber-familiar", "Infravisor", "Archaeotech Pistol", "Electro-Arc of Mars"],
                 ["Relentless", "Adamantium Will", "Eternal Warrior", "Feel No Pain (5+)", "Fabricator-General of Mars",
                  "Open the Forbidden Vaults", "Dark Cybertheurgy", "Electro-Arc of Mars", "Dark Mechanicum"],
                 "Traitor", groups=[g], mods=mods, wl_fixed=True, min_pts=2000)


def zagreus_kane():
    return named("Zagreus Kane", 410, (4, 5, 4, 5, 5, 3, 2, 10, "2+/3+"),
                 ["Artificer Armour", "Mechanicum Protectiva", "Machinator Array", "Cortex Controller", "Djinn-skein",
                  "Cyber-familiar", "Infravisor", "Corposant Stave", "Graviton Imploder"],
                 ["Relentless", "Adamantium Will", "Eternal Warrior", "Feel No Pain (5+)", "Very Bulky",
                  "Fabricator-Locum of Mars", "Synod of the Loyal Mechanicum", "The Great Noospheric Conclave",
                  "Master of Mondus Occulam"], "Loyalist",
                 mods=[err_any("Zagreus Kane " + ARCHMAGOS_LIKE, in_r(AM), in_r(KH), in_r(CDI))],
                 wl_fixed=True, min_pts=2000)


def calleb_decima():
    tpa = oid(U("Tech-Priest Auxilia"), "Guardian Retinue (Calleb Decima)")
    scy = oid(U("Scyllax Guardian-Automata Covenant"), "Guardian Retinue (Calleb Decima)")
    return named("Calleb Decima Invictus", 230, (4, 5, 5, 5, 3, 4, 2, 10, "2+/4+"),
                 ["Artificer Armour", "Mechanicum Protectiva", "Master-crafted Bolt Pistol", "Master-crafted Power Weapon",
                  "Machinator Array", "Cortex Controller", "Melta Bombs", "Curse of the Omnissiah"],
                 ["Eternal Warrior", "Relentless", "Hatred (Traitors)", "Lord of Ruin", "Walker in Ruin",
                  "Curse of the Omnissiah", "Calculated Devastation", "Guardian Retinue", "Master of Destruction"],
                 "Loyalist",
                 mods=[err("Lord of Ruin: an army led by Calleb Decima must select the Ordo Reductor Order.",
                           not_o("Ordo Reductor")),
                       err_any("Calleb Decima " + ARCHMAGOS_LIKE, in_r(AM), in_r(KH), in_r(ZK)),
                       err_any("Guardian Retinue: only one Tech-Priest Auxilia or Scyllax Covenant.",
                               cond(tpa, "roster", "greaterThan", 1), cond(scy, "roster", "greaterThan", 1)),
                       err("Guardian Retinue: only one Tech-Priest Auxilia or Scyllax Covenant.", in_r(tpa), in_r(scy))])


# ============================================================ CONFIGURATION
def army_config():
    gid = uid(CFG, "orders")
    ents = []
    for n in ORDERS + DARK:
        mods = []
        if n in DARK:
            mods = [hide_if(in_r(LOYALIST))]
        ents.append(entry(ORD[n], n, mods=mods, constraints=[constraint(uid(ORD[n], "max"), "max", 1, auto=True)],
                          infolinks=rules_links([n] + (["Dark Mechanicum"] if n in DARK else []), key=ORD[n])))
    g = group(gid, "Order of High Techno-Arcana / Dark Techno-Arcana (optional)", entries=ents,
              mods=[modifier("increment", uid(gid, "max"), 1, conds=[in_f(ZK)])],
              constraints=[constraint(uid(gid, "max"), "max", 1)])
    magi = [none_f(x) for x in [AM, MD, KH, ZK, CDI, CHROM, SCORIA]]
    errs = []
    for n in ORDERS + DARK:
        errs.append(err(f"{n}: requires an Archmagos or Magos Dominus in the Detachment.", o(n), *magi))
    for n in DARK:
        errs.append(err(f"{n}: a Dark Mechanicum Detachment is always Traitor.", o(n), in_r(LOYALIST)))
    myr = [none_f(U("Myrmidon Secutor Host")), none_f(U("Myrmidon Destructor Host"))]
    red = [none_f(U(x)) for x in ["Myrmidon Reductor Host", "Ordo Reductor Artillery Tank Battery",
                                  "Ordo Reductor Minotaur Battery"]]
    gen = [none_f(U(x)) for x in AUGMENT]
    errs += [
        err("Myrmidax: the army must include a Myrmidon Secutor Host or Myrmidon Destructor Host.", o("Myrmidax"), *myr),
        err("Ordo Reductor: the army must contain a Myrmidon Reductor Host, Artillery Tank Battery or Minotaur Battery.",
            o("Ordo Reductor"), *red),
        err("Lachrimallus: at least one compulsory Troops choice must be an Adsecularis Tech-Thrall Covenant.",
            o("Lachrimallus"), none_f(U("Adsecularis Tech-Thrall Covenant"))),
        err("Skitarii: the army must include a Skitarii Marshal.", o("Skitarii"), none_f(U("Skitarii Marshal"))),
        err("Skitarii: at least one compulsory Troops choice must be a Skitarii Cohort.", o("Skitarii"),
            none_f(U("Skitarii Cohort"))),
        err("Secutarii: the army must include a Secutarii Axiarch.", o("Secutarii"), none_f(U("Secutarii Axiarch"))),
        err("Secutarii: at least one compulsory Troops choice must be a Secutarii Hoplite or Peltast Phalanx.",
            o("Secutarii"), none_f(U("Secutarii Hoplite Phalanx")), none_f(U("Secutarii Peltast Phalanx"))),
        err("Genetor: the army must include a unit eligible for a Controlled Augmentation.",
            o("Genetor - Magos Biologis"), *gen),
        err("Legio Cybernetica: the compulsory Troops must be Castellax Maniples of at least two Castellax.",
            o("Legio Cybernetica"), cond(U("Castellax Class Battle-Automata Maniple"), "force", "lessThan", 2)),
        err("Flesh-Mechanica: Harvest of Flesh - the army must include an additional Adsecularis Tech-Thrall Covenant "
            "beyond its compulsory Troops.", o("Flesh-Mechanica"), none_f(U("Adsecularis Tech-Thrall Covenant"))),
        err("Flesh-Mechanica: Harvest of Flesh - the army must include an additional Adsecularis Tech-Thrall Covenant "
            "beyond its compulsory Troops.", o("Flesh-Mechanica"), cond(TROOPS, "force", "lessThan", 3)),
        err("Flesh-Mechanica: no more than one Heavy Support choice containing Cybernetica Cortex models.",
            o("Flesh-Mechanica"), cond(U("Conqueror Class Robot Maniple"), "force", "greaterThan", 1)),
        err("Explorator: Exploration Party may be taken by only one Troops choice.",
            cond(W("Exploration Party"), "force", "greaterThan", 1)),
        err("Genetor: only one unit may be upgraded to Perfected Specimens.",
            cond(W("Perfected Specimens"), "roster", "greaterThan", 1)),
        err("Daemonic Edict: only one unit may purchase Daemonic Infusion outside a Daemon Engine Horde.",
            not_o("Daemon Engine Horde"), cond(W("Daemonic Infusion"), "roster", "greaterThan", 1)),
    ]
    rc = [W(x) for x in ["Predatory Reconstruction", "Massive Reconstruction", "Bestial Reconstruction"]]
    many = el("conditionGroup", {"type": "or"}, [
        wrap("conditions", [cond(r, "roster", "greaterThan", 1) for r in rc]),
        wrap("conditionGroups", [all_of(cond(a, "roster", "atLeast", 1), cond(b, "roster", "atLeast", 1))
                                 for i, a in enumerate(rc) for b in rc[i + 1:]])])
    errs.append(modifier("add", "error", "Fleshcraft Edict: only one unit may purchase an Abominable Reconstruction "
                                         "outside a Flesh-Mechanica army.", conds=[not_o("Flesh-Mechanica")],
                         groups=[many]))
    rls = ["Mechanicum Army List", "The Rule of the Archmagos", "Orders of High Techno-Arcana", "Cybernetic Command",
           "Iron and Machine", "Cybernetica Cortex", "Programmed Behaviour", "Battlesmith", "Cybertheurgist",
           "Paragon of Metal", "Reactor Blast", "Atomantic Shielding", "Dark Mechanicum"]
    return entry(CFG, "Mechanicum Army", typ="upgrade",
                 cats=[category_link(gs.CAT_CONFIG, "Configuration", primary=True, key=CFG),
                       category_link(gs.FOC_PLUS["HQ"], "Force Org: +1 HQ", key=CFG)],
                 constraints=[constraint(uid(CFG, "min"), "min", 1, scope="force", deep=True),
                              constraint(uid(CFG, "max"), "max", 1, scope="force", deep=True)],
                 infolinks=rules_links(rls, key=CFG), groups=[g], mods=errs)


def warlord_entry():
    return entry(WARLORD, "Warlord", constraints=[unique(WARLORD, 1, "roster")],
                 rules=[rule(uid(WARLORD, "rule"), "Warlord",
                             "This model is the army's Warlord (one per army). It selects a Warlord Trait under the "
                             "ProHammer Classic rules. Order and Archmagos rules that refer to the Warlord apply to it.")])


# ================================================================== assemble
_common_unit = unit


def unit(*a, links_extra=(), **kw):  # noqa: F811 - adds extra entry links (e.g. the Warlord upgrade)
    e = _common_unit(*a, **kw)
    if links_extra:
        add_to(e, "entryLinks", list(links_extra))
    return e


def _post(units):
    # Legio Cybernetica: only Castellax Maniples count as compulsory Troops
    for e in units:
        cats = [c.get("targetId") for c in e.iter("categoryLink")]
        if LINE in cats and e.get("id") != U("Castellax Class Battle-Automata Maniple"):
            add_mods(e, [modifier("remove", "category", LINE, conds=[o("Legio Cybernetica")])])
    # Archimandrite: vehicles may not purchase Blessed Autosimulacra
    for e in units:
        for lk in e.iter("entryLink"):
            if lk.get("name") == "Blessed Autosimulacra" and lk.find("costs") is not None:
                add_mods(lk, [modifier("set", "hidden", "true", conds=[o("Archimandrite")]),
                              modifier("add", "error", "Archimandrite: vehicles may not purchase Blessed Autosimulacra.",
                                       conds=[o("Archimandrite"), cond(lk.get("targetId"), "parent", "atLeast", 1)])])
        for en in e.iter("selectionEntry"):
            if "Blessed Autosimulacra" in en.get("name", "") and en.get("id") != W("Blessed Autosimulacra"):
                add_mods(en, [modifier("set", "hidden", "true", conds=[o("Archimandrite")])])


def _weapon_rules():
    out = {}
    names = dict(WEAPONS)
    for n, profs in MULTI.items():
        for p in profs.values():
            names.setdefault(n + "#", None)
    for n in list(WEAPONS) + list(MULTI):
        profs = [WEAPONS[n]] if n in WEAPONS else list(MULTI[n].values())
        rl = []
        for p in profs:
            for tok in p[3].split(","):
                t = tok.strip().split(" (")[0].strip()
                if not t or t[0].isdigit():
                    continue
                if t in ("Assault", "Heavy", "Rapid Fire", "Pistol", "Melee", "Ordnance", "Salvo", "Blast",
                         "Large Blast", "Massive Blast", "Barrage", "Power Weapon", "Specialist Weapon", "One Use"):
                    continue
                try:
                    L.rule_ref(t)
                except KeyError:
                    continue
                if t not in rl:
                    rl.append(t)
        if rl:
            out[n] = rl
    return out


def build():
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS, multi_profile=MULTI, wargear=WARGEAR)
    register_data(weapon_rules=_weapon_rules())
    units = [allegiance(), army_config(),
             archmagos(), magos_dominus(), adjutant(), tech_priest_auxilia(), skitarii_marshal(), secutarii_axiarch(),
             lukas_chrom(), scoria(), kelbor_hal(), zagreus_kane(), calleb_decima(),
             protector_squad(), myrmidon_secutors(), myrmidon_destructors(), myrmidon_reductors(), scyllax(), domitar(),
             weapons_platform(), karkinos(), praetorians(), cataphract(), battle_pilgryms(), electro_priests(),
             thralls(), skitarii_cohort(), hoplites(), peltasts(), thallax(), castellax(),
             termite(), ursarax(), tarantula(), vorax(), arlatax(), vultarax(), land_speeders(), triaros_guardian(),
             crusader(), seekers(), bombots(),
             *thanatars(), krios(), karacnos(), conqueror(), leman_russ(), land_raider(), macrocarid(),
             artillery_battery(), minotaur(), kaban(),
             possessed(), abominants(), revenants(), wretched(), stalkers(), slaughterers(), scrapcode_hunters(),
             greater_daemon_engine(), brass_scorpion(), infernal_siege_engine(), flesh_colossus()]
    shared = [rhino(), triaros(), warlord_entry()]
    _post(units + shared)
    return catalogue(ARMY, units, shared)
