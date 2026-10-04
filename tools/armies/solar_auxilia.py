"""Solar Auxilia army book (Age of Darkness army list) for Prohammer 30k.

Source: the author's Solar Auxilia army book. Line numbers in comments refer to Solar_Auxilia.txt.
"""
from armies.common import *  # noqa: F401,F403
from armies.common import (k, unit, model, upgrade, unique, config, allegiance, error_if, catalogue, start,
                           register_data, LOW, FORT, COMMANDER, LINE, vehicle_profile)
from bsx import (PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group,
                 category_link, hide_if, info_link)
import gamesystem as gs
import legiones as L
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile, transport_profile
from legiones2 import (slot, take, pool, choice, add_mods, add_to, walker_profile, foc, model_swaps, model_takes,
                       numbered, TROOPS, ELITES, FA, HQ, HS)

ARMY = "Solar Auxilia"

# =====================================================================================================  RULES
RULES = {
    # ---------------------------------------------------------------- army construction (L70-L350)
    "Solar Auxilia Army": (
        "A Solar Auxilia army uses the Standard Force Organisation Chart (HQ 1-2, Troops 2-6, Elites 0-3, Fast Attack "
        "0-3, Heavy Support 0-3). The minimum selections (1 HQ, 2 Troops) are compulsory; a model or unit with the "
        "Support Officer special rule may not fulfil the compulsory HQ selection. Lords of War and Fortifications do "
        "not form part of the chart, may only be included where the mission permits or both players agree, and no "
        "army may contain more than one of each (their entries are presented in the Engines of War and other army "
        "lists). Aircraft are taken from the Aeronautica Imperialis army list (the Arvus Lighter is included here). "
        "Each Detachment fulfils its own compulsory selections; an Allied Detachment may not fulfil the compulsory "
        "selections of the Primary Detachment. Solar Auxilia special rules, High Command and Cohort Doctrines only "
        "affect Solar Auxilia units of the same Detachment unless stated otherwise."),
    "The Army's Warlord": (
        "One eligible Character must be nominated as the army's Warlord. Where the Primary Detachment is a Solar "
        "Auxilia Detachment the Warlord is determined by Disciplined Command, in this order of precedence: Lord Marshal, "
        "Legate Commander, Strategos, Auxilia Tank Commander. If several eligible models of the highest available rank "
        "are present, the controlling player chooses. An Auxilia Tank Commander selected as the Warlord receives no "
        "Warlord Trait unless another rule specifically states otherwise; otherwise the Warlord selects a Warlord Trait "
        "using the normal ProHammer Classic rules."),
    "Cohort Doctrines": (
        "A Solar Auxilia Detachment may select one Cohort Doctrine. A Detachment that does not select one represents a "
        "standard Cohort and uses the army list exactly as presented. A Doctrine's benefits, restrictions and changes "
        "apply only to the Detachment that selected it (not to Allied Detachments or other Solar Auxilia "
        "Detachments). Doctrines are modifications to the army list, not Formations."),
    # ---------------------------------------------------------------- army special rules (L4052-)
    "Disciplined Fire": (
        "When a model with this rule makes a Stand & Shoot! reaction with a Pistol, Assault or Rapid Fire weapon, it "
        "does not halve the number of shots fired because of Limited Fire. The normal -1 To Hit modifier and all "
        "other effects of Limited Fire still apply."),
    "Close Formation Fighting": (
        "So long as at least two friendly models with this rule are in base-to-base contact during an assault, those "
        "models receive +1 Weapon Skill."),
    "Hold the Line": (
        "A unit with this rule which is within 12\" of another unit from the same Tercio which is not Broken may "
        "re-roll individual rolls of a 6 when taking Pinning or Casualty Tests caused by enemy shooting or Psychic "
        "attacks."),
    "Disciplined Command": (
        "If a Solar Auxilia Detachment is the army's Primary Detachment, its Warlord must be chosen in the following "
        "order of precedence: Lord Marshal - Legate Commander - Strategos - Auxilia Tank Commander. Where several "
        "eligible models of the same rank are present, the controlling player chooses which becomes the Warlord. An "
        "Auxilia Tank Commander selected as Warlord receives no Warlord Trait unless another rule specifically states "
        "otherwise."),
    "High Command": (
        "So long as a model with this rule is on the battlefield (including while embarked upon a ground vehicle or "
        "occupying a friendly Fortification), is not Broken or Falling Back and is not engaged in close combat, "
        "friendly Solar Auxilia units from the same Detachment may use its Leadership when taking Morale (Break), "
        "Casualty and Pinning Tests. All normal modifiers apply. Where several models with High Command are present, "
        "use the highest available Leadership."),
    "Super-heavy Command Tank": (
        "Friendly Solar Auxilia units within 24\" of a vehicle with this rule may re-roll failed Break Tests."),
    "Support Officer": (
        "A model with this rule may be selected as an HQ choice but may not fulfil the army's compulsory HQ "
        "requirement (when selected as part of a Primary Detachment)."),
    "Support Section": (
        "A unit with this rule may only be included in an Auxilia Infantry Tercio which also contains at least one "
        "Auxilia Lasrifle Section."),
    "Attached Deployment": (
        "Before deployment, each Medicae Orderly must be assigned to one of the following friendly Solar Auxilia "
        "units: Auxilia Tactical Command Section, Solar Auxilia Life Ward Retinue, Auxilia Lasrifle Section, Auxilia "
        "Flamer Section or Veletaris Storm Section. It becomes part of that unit and may not voluntarily leave it. More "
        "than one Medicae Orderly may be assigned to the same unit. If the unit is destroyed, any surviving Medicae "
        "Orderly thereafter operates as an independent model."),
    "Retinue": (
        "A Retinue does not occupy a separate Force Organisation choice. The Retinue and the Character for whom it "
        "was selected form a single unit unless specifically stated otherwise."),
    "Explorator Adaption": (
        "A vehicle with this rule has a 6+ Invulnerable Save against attacks made with Blast or Template weapons, may "
        "re-roll failed Dangerous Terrain tests and counts as Void Hardened where that rule is relevant."),
    "Void Hardened": (
        "Void Hardened is a mission keyword and has no effect unless a mission, terrain or environmental rule "
        "specifically refers to it."),
    "Automated Artillery": (
        "Tarantula Sentry Guns operate without crew and may fire normally despite having no crew models. They may "
        "never move, Advance, charge, Pursue or Consolidate. Attacks made against Automated Artillery in close combat "
        "hit automatically, and it is never locked in close combat."),
    "Battlesmith": (
        "During the Shooting phase, instead of firing a weapon, a model with this rule in base contact with, or "
        "embarked upon, a damaged friendly vehicle may attempt to repair it. Roll a D6; on a 5+ repair one Engine "
        "Damaged, Weapon Destroyed or Immobilised result (a repaired weapon may fire from the following Shooting phase "
        "onwards). May not be used while Falling Back. A model equipped with a Cortex Controller may instead restore "
        "one previously lost Wound to a friendly Battle-automata within 2\"."),
    "Servo-automata Support": (
        "When an Enginseer Adept makes a Battlesmith roll, add +1 to the result for each Servo-automata in the unit "
        "equipped with a Servo-arm. An unmodified roll of 1 always fails."),
    "Cybernetica": (
        "If a unit of Servo-automata no longer contains an Enginseer Adept or other model capable of controlling "
        "them, it must take a Pinning Test at the beginning of each of its Movement phases. No test is required while "
        "the unit is engaged in close combat; it fights normally."),
    "Focus Fire": (
        "Once per battle, during its Shooting phase, an Achmiris Recon Section and any Character attached to it may "
        "fire their ranged weapons twice. After using Focus Fire, the unit may not fire any ranged weapons again "
        "until after the end of its controlling player's next turn, and it loses the Stealth special rule until the "
        "start of its controlling player's next turn."),
    "Very Bulky": "A Very Bulky model counts as three models for the purposes of Transport Capacity.",
    "Extremely Bulky": "An Extremely Bulky model counts as five models for the purposes of Transport Capacity.",
    "Feel No Pain (6+)": "This model has the Feel No Pain special rule; its Feel No Pain roll succeeds on a 6+.",
    "Preferred Enemy (Infantry)": "This unit has the Preferred Enemy special rule against Infantry units.",
    "Hatred (Traitors)": "This model has the Hatred special rule against Traitor units.",
    # ---------------------------------------------------------------- HQ
    "Lord Marshal": (
        "One Legate Commander in the army may be upgraded to a Lord Marshal (+35 points). A Lord Marshal uses the "
        "improved profile (WS4 BS4 S3 T3 W3 I4 A3 Ld10 Sv4+) and retains all of the normal Legate Commander options. "
        "Some options (Relic Blade, Grav-wave Generator, Displacer Matrix) are only available to a Lord Marshal."),
    "Household Retinue": (
        "If a Lord Marshal is the army's Warlord, Veletaris Storm Sections may be selected as Household Retinue squads "
        "in addition to their normal role. Household Retinue squads have Weapon Skill 4, lose the Hold the Line "
        "special rule, gain Preferred Enemy (Infantry) while the Lord Marshal is on the battlefield and is not Falling "
        "Back, are selected as Elites choices rather than as part of an Infantry Tercio, and may select a Dracosan "
        "Armoured Transport or Auxilia Arvus Lighter as a Dedicated Transport."),
    "Precision Bombardment": (
        "Once per game, instead of firing a weapon, the Strategos may call in a Precision Bombardment (Unlimited range, "
        "S9 AP2, Ordnance 1, Barrage, Pinning, Large Blast). It may not be used if the Strategos is engaged in close "
        "combat or is Falling Back."),
    "Armoured Warfare": (
        "An Auxilia Tank Commander must be assigned to one of the following vehicles included in the army: an Auxilia "
        "Leman Russ of any type, a Malcador, a Valdor Tank Hunter, a Baneblade, Stormblade, Stormlord, Stormhammer, "
        "Shadowsword or an Armoured Sentinel Squadron. The Tank Commander forms part of the vehicle and may never "
        "leave it; if the vehicle is destroyed, the Tank Commander is slain. A vehicle commanded by an Auxilia Tank "
        "Commander uses Ballistic Skill 4 and gains the Command Tank and Tank Ace special rules (the cost is included "
        "in the Tank Commander's points). The Tank Commander has no additional options; the commanded vehicle may "
        "select any upgrades normally available to it. Unit Type: Vehicle (Character), as per the vehicle selected. "
        "If an Armoured Sentinel Squadron is chosen, nominate one Sentinel as the Command Sentinel: the Tank Commander "
        "is embarked within it and is slain if it is destroyed; the Command Sentinel uses BS4 and gains the Tank Ace "
        "rules."),
    "Command Tank": (
        "So long as the Tank Commander's vehicle is on the battlefield and has not been destroyed, its controlling "
        "player may re-roll one Reserve roll during each turn."),
    "Tank Ace": (
        "A vehicle commanded by an Auxilia Tank Commander may make a Stand & Shoot! reaction despite being a vehicle "
        "(normal ProHammer rules for Stand & Shoot! and Limited Fire). In addition, choose one Tank Ace ability when "
        "the Tank Commander is selected; it applies to the vehicle for the entire battle."),
    "Life Ward Retinue": (
        "A Solar Auxilia Life Ward Retinue does not occupy a Force Organisation slot and is not considered a separate "
        "unit. Each Life Ward must be assigned to a Solar Auxilia Independent Character before deployment; more than "
        "one Life Ward may be assigned to the same Character, and a Life Ward must remain in the same unit as that "
        "Character for the entire battle. Where relevant for army selection, Life Wards are considered part of the HQ "
        "choice of the Character to which they are assigned. While attached to a unit belonging to a Tercio, a Life "
        "Ward is considered part of that Tercio for the purposes of Hold the Line. Only one Life Ward in the "
        "Detachment may select a Power Fist or an Inferno Pistol. A Retinue is selected for, and assigned as a whole to, "
        "one Character - the Legate Commander (Lord Marshal) or a Solar Auxilia special character (Ireton MaSade, Aevos "
        "Jovan); it may not be split between Characters, and the Strategos is not eligible. Cohort Attaches may also "
        "be selected for a Life Ward Retinue."),
    "Cohort Attaches": (
        "A Solar Auxilia Detachment containing a Legate Commander, Auxilia Tactical Command Section or Solar Auxilia "
        "Life Ward Retinue may include up to three Cohort Attaches. They do not occupy Force Organisation slots and "
        "each type may only be selected once per Detachment. Before deployment, each Attache must be assigned to a "
        "Legate Commander, Auxilia Tactical Command Section or Solar Auxilia Life Ward Retinue; it forms part of that "
        "unit for the duration of the battle and may not voluntarily leave it."),
    "Master Chirurgeon": (
        "The Cohort Chirurgeon and all models in the unit to which he is attached gain Feel No Pain (5+); a model which "
        "already has Feel No Pain of an equal or better value gains no additional effect. At the start of each "
        "friendly turn, the Chirurgeon may attempt to treat one wounded non-vehicle model in his unit: on a 5+ that "
        "model regains one previously lost Wound, up to its starting Wounds."),
    "Astropathic Discipline": (
        "Psyker - Mastery Level 1. An Astropath Primus selects one psychic power using the normal ProHammer rules, "
        "from Biomancy, Divination, Pyromancy, Telekinesis or Telepathy (never Daemonology). The Force Staff follows "
        "the normal ProHammer rules for Force Weapons."),
    "Fire Direction": (
        "Instead of firing a weapon in the Shooting phase, the Master of Ordnance may direct the fire of one friendly "
        "Solar Auxilia Artillery unit or Vehicle within 36\". Choose one Blast, Barrage or Ordnance weapon fired by "
        "that unit during the current Shooting phase: if fired using Direct Fire it may re-roll one failed To Hit "
        "roll; if fired using Indirect Fire the firing player may re-roll the Scatter die for its first shot. A die "
        "may never be re-rolled more than once."),
    "Fleet Coordination": (
        "Once per Battle Round, after a Reserve roll has been made but before its result is resolved, the Fleet "
        "Liaison Officer may add +1 to one Reserve roll made for a friendly Solar Auxilia unit, or apply -1 to one "
        "Reserve roll made for an enemy unit. This cannot prevent a unit from arriving when it would otherwise enter "
        "play automatically and cannot affect units whose arrival does not require a Reserve roll."),
    "Mechanicum Liaison": (
        "The Mechanicum Liaison Adept's Cortex Controller counts normally for all rules which require the presence of "
        "a Cortex Controller. A Solar Auxilia Detachment containing a Mechanicum Liaison Adept may include Thallax "
        "Cohorts and Castellax Battle-automata Maniples where permitted by the Solar Auxilia army list."),
    "Master Duellist": (
        "If the Household Champion is in base-to-base contact with an enemy Independent Character when his attacks are "
        "resolved, he may direct any or all of his attacks against that model, using his Weapon Skill against that "
        "Character's Weapon Skill, and may re-roll failed To Hit rolls against it. Unsaved wounds from these attacks "
        "must be allocated to the chosen Independent Character (an exception to the normal allocation rules)."),
    # ---------------------------------------------------------------- Elites
    "Artillery (Rapier)": (
        "Rapier Carriers use the normal Artillery rules of ProHammer Classic. Each Rapier requires at least one "
        "Auxiliary crewman within 2\" in order to move or fire. A Rapier may not fire in a turn in which it has moved "
        "unless a special rule specifically states otherwise."),
    "Dead-man's Switch": (
        "If the Ogryn Charonite Squad fails a Morale check while at least one friendly, unengaged Solar Auxilia HQ "
        "unit from the same Detachment remains on the battlefield, the controlling player may activate the Dead-man's "
        "Switch: the check is passed instead, then the squad suffers D3 wounds with no armour, cover or invulnerable "
        "saves allowed, allocated randomly to surviving models."),
    "Mind-slave": "Ogryn Charonites may never voluntarily Take Cover! and may never count as a Scoring unit.",
    "Brutal Fighters": (
        "Ogryn Charonites must always attempt to Pursue a defeated enemy whenever able to do so. When making a "
        "Consolidation move, the unit must move towards the nearest enemy unit by the shortest available route."),
    # ---------------------------------------------------------------- Troops
    "Auxilia Infantry Tercio": (
        "An Auxilia Infantry Tercio occupies a single Troops choice and contains one to three Sections in any "
        "combination of Auxilia Lasrifle Sections, Veletaris Storm Sections and Auxilia Flamer Sections. Each Section "
        "is purchased separately; the Tercio costs the combined points of its Sections. TERCIO DEPLOYMENT: all "
        "Sections of the same Tercio are deployed at the same time; if placed in Reserve, a single Reserve roll is "
        "made for the entire Tercio and all of its Sections arrive in the same turn. Once deployed each Section "
        "operates as a completely separate unit for all purposes (movement, shooting, assault, Morale, objectives "
        "and Victory Points). TROOP MASTER: one Sergeant of an Auxilia Lasrifle Section in each Tercio may be "
        "upgraded to a Troop Master. SUPPORT SECTION: a Section with this rule may only be included in a Tercio "
        "which also contains at least one Auxilia Lasrifle Section. DEDICATED TRANSPORTS: each Section may purchase "
        "one Dracosan Armoured Transport (so no Tercio contains more than three); each Dracosan is assigned to a "
        "particular Section before deployment."),
    "Troop Master": (
        "One Sergeant belonging to an Auxilia Lasrifle Section in each Infantry Tercio may be upgraded to a Troop "
        "Master (+15 points). The Troop Master uses the Troop Master profile (WS4 BS4 S3 T3 W2 I3 A2 Ld8 Sv4+) and "
        "retains all options otherwise available to the Sergeant."),
    "Zone Mortalis Deployment": (
        "In games of Zone Mortalis, an Auxilia Lasrifle Section is divided into two squads of ten models before "
        "deployment. These operate as separate units but are still part of the same Infantry Tercio."),
    # ---------------------------------------------------------------- Transports
    "Hades Breaching Drill": (
        "A Hades Breaching Drill may only be purchased as a Dedicated Transport for an Eidis Engineer Section. It has "
        "no Transport Capacity. If a Hades is selected, the Engineer Section enters play using Terrestrial Eruption."),
    "Tunnelling": (
        "During its Movement phase a Hades Breaching Drill may move underground instead of moving normally: up to 12\" "
        "in any direction, ignoring intervening models and terrain, ending outside Impassable Terrain and more than "
        "1\" from enemy models. It then gains a 4+ Invulnerable Save until the start of its next Movement phase and may "
        "not Advance or charge that turn."),
    "Tunnelling Assault": (
        "When declaring a charge, the Hades may attack underground: roll an additional D6 for its charge distance and "
        "discard the highest die. It ignores terrain during this charge and enemy units may not Stand & Shoot! "
        "against it. On a turn in which it charges using Tunnelling it inflicts D6+2 Hammer of Wrath attacks (using "
        "the Melta-cutter Drill profile) instead of the normal number. If it charges a building or fortification "
        "occupied by an enemy unit this way, roll a D6 for each enemy model within: on a 4+ it suffers an automatic "
        "S4 AP2 hit."),
    "Terrestrial Eruption": (
        "The Hades Breaching Drill and the Eidis Engineer Section for which it was purchased must begin the game in "
        "Reserve. When the Hades becomes available, deploy it by Deep Strike: before rolling Scatter place the 3\" "
        "Blast marker where it is intended to emerge; after Scatter every model touched by the marker suffers one "
        "automatic hit from the Melta-cutter Drill (vehicles on their Side Armour). Surviving models are moved the "
        "minimum distance to allow the Drill to be placed at least 1\" away. Terrain does not cause a Deep Strike "
        "Mishap unless no legal position can be found. The Engineer Section automatically arrives at the start of the "
        "controlling player's following turn within 6\" of the emergence point; it does not count as having Deep "
        "Struck and may shoot and charge normally. On the turn the Hades arrives it has a 4+ Invulnerable Save until "
        "the start of its next Movement phase."),
    # ---------------------------------------------------------------- Fast Attack
    "Firing Modes": (
        "Before deployment, choose one firing mode for the entire Battery. POINT DEFENCE: each Tarantula has a 90 "
        "degree fire arc and may engage enemy units within 24\". SENTRY: each Tarantula has a 360 degree fire arc but "
        "may only engage enemy units within 12\". Unless equipped with a Hyperios system, a Tarantula must fire at the "
        "nearest eligible enemy target: anti-infantry weapons prioritise Infantry, Lascannons and Multi-meltas "
        "prioritise Vehicles and Monstrous Creatures; if no preferred target is available, fire at the nearest "
        "eligible enemy unit."),
    "Induction Charger": (
        "Once per battle, declare that the Squadron is activating its Induction Chargers at the beginning of its "
        "Movement phase. For the remainder of that player turn every surviving vehicle in the Squadron counts as a "
        "Fast Vehicle. This does not permanently change the vehicle's type."),
    "Veletaris Crew": "Models with this upgrade have Ballistic Skill 4.",
    "Jet Pack": "Models equipped with Jet Packs use the normal ProHammer rules for Jet Pack Infantry.",
    # ---------------------------------------------------------------- Heavy Support
    "Co-ordinated Fire Protocols": (
        "So long as two or more tanks from the same Squadron fire at the same enemy unit during the same Shooting "
        "phase, those tanks gain +1 Ballistic Skill when resolving attacks against that target."),
    "Highly Flammable": "If the Malcador Infernus suffers an Explodes! result, add D3\" to the radius of the explosion.",
    "Dangerous Reactor Core": (
        "Whenever an enemy causes a Penetrating Hit against the Valdor, that player may re-roll a result of 1 on the "
        "Vehicle Damage table. If the Valdor suffers an Explodes! result, add D3\" to the radius of the explosion."),
    "Remote Control": (
        "The Cyclops are deployed as a single unit; immediately after deployment each Cyclops may separate and operate "
        "as an independent unit for the rest of the battle. A Cyclops must remain within 36\" of a friendly Solar "
        "Auxilia Character; if none is within 36\" it may not Move, Advance, Charge or voluntarily Detonate. A Cyclops "
        "cannot make normal close combat attacks, is hit automatically in close combat, may declare charges "
        "normally, may never Pursue or Consolidate, may never be joined by another model and is never a Scoring "
        "unit."),
    "Detonation": (
        "A Cyclops may voluntarily Detonate during its controlling player's Assault phase; if engaged in close combat "
        "it may instead Detonate during either player's Assault phase at Initiative 10. Centre the appropriate Blast "
        "marker over the Cyclops and resolve its payload against all models beneath it; the Cyclops is then destroyed. "
        "If a Cyclops is destroyed by any other means, roll a D6: on a 6 it immediately Detonates."),
    # ---------------------------------------------------------------- Dramatis Personae
    "Warlord (Ireton MaSade)": "Ireton MaSade must be the army's Warlord. This does not override Disciplined Command: "
                               "MaSade counts as a Legate Commander. An army may include either MaSade or a Lord Marshal, "
                               "not both. Loyalist only.",
    "Master of the Battlefield": (
        "After both armies have deployed, but before the first turn begins, MaSade may redeploy D3 friendly Solar "
        "Auxilia units from his Detachment anywhere they could normally have deployed, or place them into Reserve. A "
        "unit already in Reserve may instead be deployed normally, provided a legal deployment position exists."),
    "Protector of Agathon": (
        "The first time a non-Unique Solar Auxilia Infantry unit from MaSade's Detachment is completely destroyed, "
        "roll a D6. On a 5+, a replacement unit with the same starting composition and wargear is placed into "
        "Reserve (attached Characters, Cohort Attaches and Dedicated Transports are not returned) and enters play "
        "using the normal Reserve rules. Only one unit may be returned during the battle."),
    "Miraculous Skill": (
        "Once per player turn Jovan may either allow a failed Feel No Pain roll made by himself or a model in his unit "
        "to be re-rolled, or, at the start of a friendly turn, restore one previously lost Wound to himself or one "
        "friendly non-Vehicle model in his unit (never above its starting Wounds)."),
    "Surgeon-Primus": (
        "Jovan may be attached to an Auxilia Medicae Detachment before deployment; if so, Jovan and the Medicae "
        "Detachment form a single unit at the beginning of the battle. Jovan may otherwise join friendly units "
        "normally using the Independent Character rules."),
    "Vaskale Solar": (
        "Loyalist only. If an Auxilia Infantry Tercio contains a Troop Master, that Troop Master may be upgraded to "
        "Vaskale Solar for +30 points; only one Troop Master in the army may be. Vaskale replaces the Troop Master's "
        "profile (WS4 BS4 S3 T3 W2 I2 A2 Ld9 Sv4+), keeps the Troop Master's wargear and purchased options and has "
        "Disciplined Fire, Close Formation Fighting, Hold the Line, Tercio Commander, Veteran of the Dawn Gate, Hold "
        "Fast and Battered Body. Unit Type: Infantry (Character). Vaskale does not occupy a Force Organisation slot."),
    "Tercio Commander": (
        "So long as Vaskale Solar is on the battlefield and is not Broken, friendly Sections belonging to his Infantry "
        "Tercio with at least one model within 12\" of him may use his Leadership for Break, Casualty, Pinning or "
        "Regroup Tests."),
    "Veteran of the Dawn Gate": (
        "Vaskale Solar's Section has the Stubborn special rule. Friendly Sections of the same Infantry Tercio with at "
        "least one model within 12\" of Vaskale may re-roll failed Pinning Tests."),
    "Hold Fast": (
        "If Vaskale Solar's Section Remained Stationary during its Movement phase, it may re-roll failed Casualty Tests "
        "until the start of its next Movement phase."),
    "Battered Body": "A unit containing Vaskale Solar may not Advance (his reduced mobility is reflected by his I2).",
    # ---------------------------------------------------------------- weapon rules (L4893-)
    "Charger Burnout": (
        "After a unit fires its Auxilia Lasrifles using Blast-chargers, those Lasrifles may not be fired during its "
        "following player turn. After resolving the attack roll a D6 (one roll for the entire unit): on a 1 the "
        "Blast-chargers burn out and may not be used again for the rest of the battle."),
    "Cumbersome": (
        "A model attacking with a Cumbersome weapon may make only one attack with that weapon, regardless of its "
        "Attacks characteristic or other bonuses. That attack is made at Weapon Skill 1."),
    "Flesh Ripper": (
        "Any unmodified To Hit roll of 6 made with a weapon with Flesh Ripper is resolved at AP2 and inflicts Instant "
        "Death. All other hits use the weapon's normal profile."),
    "Heat Seeker": "Jink Saves may not be taken against attacks made with a Heat Seeker weapon.",
    "Lithe": "A model attacking with a weapon with Lithe receives +2 Initiative during a turn in which it charges.",
    "Massive Blast": "A weapon with Massive Blast uses the 7\" Blast marker; otherwise use the normal Blast rules.",
    "Shell Shock": "A Pinning Test caused by a weapon with Shell Shock suffers a -1 Leadership modifier.",
    "Shock Pulse": (
        "If a vehicle suffers a Penetrating Hit from a weapon with Shock Pulse, it may only fire using Snap Fire during "
        "its following player turn."),
    "Sunder": "A weapon with Sunder may re-roll failed Armour Penetration rolls.",
    "Torrent (18\")": (
        "Use the normal ProHammer Torrent rules, except that the Template may be placed entirely within 18\" of the "
        "firing weapon rather than the normal distance."),
    "Wrecker": (
        "A weapon with Wrecker may re-roll failed Armour Penetration rolls against Fortifications, buildings, "
        "barricades and other immobile structures. If a mission uses a Building Damage table, add +1 to any roll made "
        "on that table by the attack."),
    "Breaching Charge": (
        "A Breaching Charge may be used once per battle during an Assault phase instead of the bearer's normal "
        "attacks. The bearer makes one attack against an engaged enemy unit; if it hits, place a Blast marker in base "
        "contact with the bearer covering as many enemy models as possible without covering friendly models; models "
        "beneath it suffer a hit with the Breaching Charge profile. Against a vehicle, resolve one S8 AP2 attack "
        "against the Armour facing the bearer is in contact with."),
    "Collimator / Blast-charger firing modes": (
        "A model equipped with an Auxilia Lasrifle and Collimator may use the Collimator profile instead of the "
        "weapon's normal firing mode; a model with a Blast-charger may use the Blast-charger profile. All models in "
        "the same unit firing Auxilia Lasrifles must use the same firing mode."),
    # ---------------------------------------------------------------- Tank Ace abilities
    "Tank Ace: Tank Hunter": "The vehicle gains Tank Hunters.",
    "Tank Ace: Field Repairs": "The vehicle gains It Will Not Die.",
    "Tank Ace: Reconnaissance Ace": "The vehicle gains Scout. In addition, it may re-roll failed Dangerous Terrain tests.",
    "Tank Ace: Infantry Killer": "The vehicle may re-roll To Hit rolls of 1 when shooting at Infantry units.",
    "Tank Ace: Monster Hunter": "The vehicle gains Monster Hunter.",
    "Tank Ace: Dead-eye Gunner": (
        "Choose one non-Blast and non-Template weapon carried by the vehicle. That weapon gains Master-Crafted."),
    "Tarantula: Forward Deployment": "The unit gains Scout.",
    "Tarantula: Concealment": "The unit gains Stealth.",
    "Tarantula: Drop Capsules": "The unit gains Deep Strike.",
    # ---------------------------------------------------------------- Cohort Doctrines (L5032-)
    "Standard Cohort": (
        "No Cohort Doctrine: the Detachment represents a standard Solar Auxilia Cohort and uses the army list exactly "
        "as presented."),
    "Infantry Cohort": (
        "REQUIREMENTS - The Warlord must be a Lord Marshal, Legate Commander or Strategos. The Detachment must contain "
        "at least two Auxilia Infantry Tercios.\n"
        "RANK AND FILE - An Infantry Tercio containing three Sections, including at least one Auxilia Lasrifle Section "
        "with a Troop Master, gains Fury of the Auxilia. FURY OF THE AUXILIA: if a unit containing at least five models "
        "Remained Stationary during its Movement phase, it may fire twice with Auxilia Lasrifles, Laspistols, Rotor "
        "Cannons and Dual Rotor Cannons; afterwards it may not make a Stand & Shoot reaction until the beginning of "
        "its next turn and may not fire during its following Shooting phase. Not usable when firing Snap Shots.\n"
        "AMONGST THE MEN - Friendly Sections belonging to an Infantry Tercio within 12\" of the Warlord may use his "
        "Leadership for Break, Casualty and Pinning Tests; if they could already use it through High Command, they "
        "also gain Stubborn while within 12\".\n"
        "RESTRICTIONS - No Lykis Maelstrom Sections, no Hades Breaching Drills, no Tarantula Sentry Gun Batteries. No "
        "more than one Vehicle Squadron selected from Fast Attack and no more than one Vehicle Squadron selected from "
        "Heavy Support (single-vehicle units such as the Malcador or Valdor, and Tarantula Batteries, count as Vehicle "
        "Squadrons for this limit)."),
    "Armoured Cohort": (
        "REQUIREMENTS - An Auxilia Tank Commander must be the army's Warlord, regardless of the normal requirements of "
        "Disciplined Command.\n"
        "STEEL RANKS - Auxilia Leman Russ Strike Squadrons become Troops choices; at least two must be selected and "
        "they fulfil the compulsory Troops selections. Auxilia Leman Russ Assault Squadrons become Elites choices.\n"
        "ROLLING ARMY - All Infantry units able to purchase a Dedicated Transport must do so. The Detachment may not "
        "include Fortifications, Tarantula Sentry Gun Batteries or other Immobile units.\n"
        "ARMOURED COMMAND - Friendly Solar Auxilia Vehicle Squadrons within 12\" of the Warlord may use his Leadership "
        "for any Leadership or Morale tests. A Squadron containing three vehicles may upgrade one vehicle to a "
        "Squadron Prime for +25 points (Ballistic Skill 4).\n"
        "TOP WORKING ORDER - Solar Auxilia Vehicles which may normally purchase vehicle upgrades may also purchase a "
        "Nuncio-vox (+10 points; the vehicle itself is the bearer) and a Flare Shield (+35 points)."),
    "Reconnaissance Cohort": (
        "REQUIREMENTS - The Warlord must be a Lord Marshal, Legate Commander or Strategos. The Detachment must contain "
        "at least one Achmiris Recon Section.\n"
        "VEILED RANKS - Achmiris Recon Sections may be selected as Sections within an Auxilia Infantry Tercio; they "
        "then become Troops and gain Hold the Line. A Tercio may contain no more than two Achmiris Recon Sections.\n"
        "VEIL OF ASSURANCE - While the Warlord is occupying terrain, friendly Solar Auxilia Infantry units from the "
        "same Detachment which are also occupying terrain may use his Leadership for Break, Casualty and Pinning "
        "Tests.\n"
        "VEILED BODYGUARD - One Achmiris Recon Section may be selected as a Retinue for a Legate Commander at its "
        "normal cost and with its normal options; it occupies no Force Organisation slot and gains Preferred Enemy "
        "(Infantry).\n"
        "RESTRICTIONS - No Auxilia Rapier Batteries, no Tarantula Sentry Gun Batteries. Malcador Heavy Tanks, Malcador "
        "Infernus and Valdor Tank Hunters must begin the battle in Reserve."),
    "Veletaris Assault Cohort": (
        "REQUIREMENTS - The Warlord must be a Lord Marshal, Legate Commander or Strategos. The Detachment must contain "
        "at least two Veletaris Storm Sections.\n"
        "STORM TERCIOS - Veletaris Storm Sections may fulfil the compulsory Troops selections. An Auxilia Infantry "
        "Tercio may be composed entirely of Veletaris Storm Sections and does not require an Auxilia Lasrifle "
        "Section.\n"
        "CLOSE ASSAULT DRILLS - A Veletaris Storm Section which disembarks from a Dracosan may charge during the same "
        "turn provided the Dracosan moved no more than 6\"; it may shoot normally before charging.\n"
        "SHOCK TROOPS - Veletaris Storm Sections gain Furious Charge. A Veletaris Storm Section which wins a close "
        "combat may re-roll its Pursuit roll.\n"
        "ASSAULT FORMATION - Lykis Maelstrom Sections become Elites choices.\n"
        "RESTRICTIONS - No Auxilia Artillery Tank Batteries. No more than one Auxilia Rapier Battery."),
    "Void & Siege Cohort": (
        "REQUIREMENTS - The Detachment must contain at least one Eidis Engineer Section and at least one Auxilia "
        "Infantry Tercio.\n"
        "VOID-HARDENED FORMATION - Auxilia Lasrifle Sections may upgrade their Void Armour to Reinforced Void Armour "
        "for +2 points per model; the entire Section must be upgraded.\n"
        "PIONEER TERCIOS - Eidis Engineer Sections may be selected as Sections within an Auxilia Infantry Tercio; they "
        "then become Troops and count as Support Sections.\n"
        "BREACHING FORMATIONS - Eidis Engineer Sections may select a Hades Breaching Drill as a Dedicated Transport. "
        "One Eidis Engineer Section in the Detachment may take Breaching Charges for free.\n"
        "PREPARED POSITIONS - Auxilia Rapier Batteries gain Stubborn while occupying terrain or a Fortification. "
        "Friendly Solar Auxilia Infantry units within 6\" of a Rapier Battery may re-roll failed Pinning Tests.\n"
        "SIEGE TRAIN - Auxilia Artillery Tank Batteries may be selected as either Elites or Heavy Support choices.\n"
        "RESTRICTIONS - No more than one Lykis Maelstrom Section and no more than one Achmiris Recon Section. Units "
        "from this Detachment may not use Outflank."),
}

DOCTRINES = ["Standard Cohort", "Infantry Cohort", "Armoured Cohort", "Reconnaissance Cohort",
             "Veletaris Assault Cohort", "Void & Siege Cohort"]

# ==================================================================================================  WEAPONS
WEAPONS_ = {
    # pistols
    "Laspistol": ('12"', "3", "-", "Pistol"),
    "Blast Pistol": ('6"', "5", "-", "Pistol, Twin-linked, Gets Hot"),
    "Needle Pistol": ('12"', "1", "5", "Pistol, Poisoned (2+), Rending"),
    "Master-crafted Needle Pistol": ('12"', "1", "5", "Pistol, Poisoned (2+), Rending, Master-crafted"),
    "Volkite Serpenta": ('10"', "5", "5", "Pistol, Rending"),
    "Hand Flamer": ("Template", "3", "6", "Pistol"),
    "Plasma Pistol": ('12"', "7", "2", "Pistol, Gets Hot"),
    "Inferno Pistol": ('6"', "8", "1", "Pistol, Melta"),
    "Archaeotech Pistol": ('12"', "6", "3", "Pistol, Master-crafted"),
    # las & basic
    "Lasgun": ('24"', "3", "-", "Rapid Fire"),
    "Laslock": ('18"', "4", "-", "Assault 1"),
    "Auxilia Lasrifle": ('30"', "3", "-", "Rapid Fire"),
    "Shotgun": ('12"', "3", "-", "Assault 2"),
    "Sniper Rifle": ('36"', "3", "6", "Heavy 1, Sniper"),
    # volkite
    "Volkite Charger": ('15"', "5", "5", "Assault 2, Rending"),
    "Volkite Culverin": ('45"', "6", "5", "Heavy 4, Rending"),
    "Twin-linked Volkite Demi-culverin": ('45"', "7", "5", "Heavy 5, Rending, Twin-linked"),
    # flame
    "Flamer": ("Template", "4", "5", "Assault 1"),
    "Heavy Flamer": ("Template", "5", "4", "Assault 1"),
    "Twin-linked Heavy Flamer": ("Template", "5", "4", "Assault 1, Twin-linked"),
    "Inferno Gun": ("Template", "7", "3", 'Heavy 1, Torrent (18")'),
    # plasma
    "Plasma Gun": ('24"', "7", "2", "Rapid Fire, Gets Hot"),
    "Plasma Cannon": ('36"', "7", "2", "Heavy 1, Blast, Gets Hot"),
    "Phased Plasma-fusil": ('24"', "6", "3", "Salvo 2/3"),
    "Executioner Plasma Cannon": ('36"', "7", "2", "Heavy 3, Blast"),
    # melta
    "Meltagun": ('12"', "8", "1", "Assault 1, Melta"),
    "Multi-melta": ('24"', "8", "1", "Heavy 1, Melta"),
    # autocannons & rotary
    "Rotor Cannon": ('30"', "3", "6", "Salvo 3/4"),
    "Twin-linked Rotor Cannon": ('30"', "3", "6", "Salvo 3/4, Twin-linked"),
    "Dual Rotor Cannon": ('30"', "3", "6", "Salvo 6/8"),
    "Autocannon": ('48"', "7", "4", "Heavy 2"),
    "Twin-linked Autocannon": ('48"', "7", "4", "Heavy 2, Twin-linked"),
    "Exterminator Autocannon": ('48"', "7", "4", "Heavy 4, Twin-linked"),
    "Heavy Bolter": ('36"', "5", "4", "Heavy 3"),
    "Twin-linked Heavy Bolter": ('36"', "5", "4", "Heavy 3, Twin-linked"),
    # las & energy support
    "Multi-laser": ('36"', "6", "6", "Heavy 3"),
    "Twin-linked Multi-laser": ('36"', "6", "6", "Heavy 3, Twin-linked"),
    "Quad Multi-laser": ('36"', "6", "6", "Heavy 6, Twin-linked"),
    "Lascannon": ('48"', "9", "2", "Heavy 1"),
    "Twin-linked Lascannon": ('48"', "9", "2", "Heavy 1, Twin-linked"),
    "Laser Destroyer Array": ('36"', "9", "1", "Ordnance 1, Twin-linked"),
    "Neutron Beam Laser": ('36"', "10", "1", "Ordnance 2, Concussive, Shock Pulse"),
    # graviton
    "Graviton Gun": ('18"', "Special", "4", "Heavy 1, Blast, Concussive, Graviton"),
    "Graviton Cannon": ('36"', "Special", "4", "Heavy 1, Large Blast, Concussive, Graviton"),
    # missiles
    "Hunter-Killer Missile": ("Unlimited", "8", "3", "Heavy 1, One Use"),
    "Hellstrike Missile": ('72"', "8", "3", "Ordnance 1, One Use"),
    # artillery & tank
    "Battle Cannon": ('72"', "8", "3", "Ordnance 1, Large Blast"),
    "Vanquisher Battle Cannon": ('72"', "8", "2", "Heavy 1, Armourbane"),
    "Demolisher Cannon": ('24"', "10", "2", "Ordnance 1, Large Blast"),
    "Earthshaker Cannon": ('36-240"', "9", "3", "Ordnance 1, Barrage, Large Blast"),
    "Medusa Siege Gun": ('36"', "10", "2", "Ordnance 1, Barrage, Large Blast"),
    "Colossus Bombard": ('24-60"', "6", "3", "Ordnance 1, Barrage, Large Blast, Ignores Cover"),
    # close combat
    "Close Combat Weapon": ("-", "User", "-", "Melee"),
    "Rending Weapon": ("-", "User", "-", "Melee, Rending"),
    "Power Weapon": ("-", "User", "-", "Melee, Power Weapon"),
    "Master-crafted Power Weapon": ("-", "User", "-", "Melee, Power Weapon, Master-crafted"),
    "Power Axe": ("-", "User", "-", "Melee, Power Weapon"),
    "Power Fist": ("-", "x2", "-", "Melee, Power Weapon, Unwieldy, Specialist Weapon"),
    "Relic Blade": ("-", "6", "-", "Melee, Power Weapon, Two-handed"),
    "Force Staff": ("-", "User", "-", "Melee, Power Weapon, Force"),
    "Charonite Claws": ("-", "User+1", "3", "Melee, Flesh Ripper"),
    "Lascutter": ("-", "9", "2", "Melee, Unwieldy, Cumbersome"),
    "Achmiris Dagger": ("-", "User", "-", "Melee, Lithe"),
    "Melta-cutter Drill": ("-", "User", "1", "Melee, Armourbane, Shred"),
    "Phase Lancet": ("-", "User", "3", "Melee, Poisoned (4+), Instant Death"),
    # special & demolition
    "Breaching Charge": ("Special", "8", "2", "Melee, Blast, One Use, Wrecker"),
    "Precision Bombardment": ("Unlimited", "9", "2", "Ordnance 1, Barrage, Pinning, Large Blast"),
    "Cyclops Demolition Charge": ("-", "8", "3", "Ordnance 1, Large Blast"),
    "Cyclops Incineration Charge": ("-", "5", "4", "Ordnance 1, Massive Blast, Ignores Cover"),
    "Atomantic Imploder": ("-", "10", "1", "Ordnance 1, Blast, Blind, Instant Death"),
}

MULTI = {
    "Collimator": {"Auxilia Lasrifle - Collimator": ('36"', "3", "-", "Heavy 2")},
    "Blast-charger": {"Auxilia Lasrifle - Blast-charger": ('18"', "6", "6", "Heavy 1, Charger Burnout")},
    "Chemical Ammunition": {"Chem Inferno Gun": ("Template", "3", "2", "Heavy 1, Poisoned (2+), Pinning, Armourbane, "
                                                                       'Torrent (18")')},
    "Missile Launcher": {"Missile Launcher - Frag": ('48"', "4", "6", "Heavy 1, Blast"),
                         "Missile Launcher - Krak": ('48"', "8", "3", "Heavy 1")},
    "Hyperios Air-defence Missile Launcher": {
        "Hyperios Air-defence Missile": ('48"', "8", "3", "Heavy 1, Skyfire, Interceptor, Heat Seeker")},
    "Solar Auxilia Grenade Launcher": {
        "Grenade Launcher - Kinetic Grenade": ('24"', "4", "5", "Assault 1, Blast"),
        "Grenade Launcher - Tempest Shell": ('24"', "-", "6", "Assault 1, Haywire"),
        "Grenade Launcher - Krak Grenade": ('24"', "6", "4", "Assault 1")},
    "Quad Mortar": {"Quad Mortar - Frag Shell": ('12-60"', "5", "5", "Heavy 4, Barrage, Blast, Shell Shock"),
                    "Quad Mortar - Shatter Shell": ('36"', "8", "4", "Heavy 4, Sunder")},
    "AT Rounds": {"AT Round": ('36"', "4", "-", "Heavy 1, Rending, Gets Hot")},
    "Volkite Rounds": {"Volkite Round": ('30"', "5", "5", "Heavy 1, Rending")},
}

WEAPON_RULES = {
    "Blast Pistol": ["Twin-Linked", "Gets Hot"],
    "Needle Pistol": ["Poison", "Rending"],
    "Master-crafted Needle Pistol": ["Poison", "Rending", "Master-Crafted"],
    "Volkite Serpenta": ["Rending"], "Volkite Charger": ["Rending"], "Volkite Culverin": ["Rending"],
    "Twin-linked Volkite Demi-culverin": ["Rending", "Twin-Linked"],
    "Plasma Pistol": ["Gets Hot"], "Plasma Gun": ["Gets Hot"], "Plasma Cannon": ["Gets Hot"],
    "Inferno Pistol": ["Melta"], "Meltagun": ["Melta"], "Multi-melta": ["Melta"],
    "Archaeotech Pistol": ["Master-Crafted"], "Master-crafted Power Weapon": ["Master-Crafted"],
    "Sniper Rifle": ["Sniper"],
    "Blast-charger": ["Charger Burnout", "Collimator / Blast-charger firing modes"],
    "Collimator": ["Collimator / Blast-charger firing modes"],
    "Inferno Gun": ['Torrent (18")'],
    "Chemical Ammunition": ['Torrent (18")', "Poison", "Pinning", "Armourbane"],
    "Twin-linked Heavy Flamer": ["Twin-Linked"], "Twin-linked Rotor Cannon": ["Twin-Linked"],
    "Twin-linked Autocannon": ["Twin-Linked"], "Exterminator Autocannon": ["Twin-Linked"],
    "Twin-linked Heavy Bolter": ["Twin-Linked"], "Twin-linked Multi-laser": ["Twin-Linked"],
    "Quad Multi-laser": ["Twin-Linked"], "Twin-linked Lascannon": ["Twin-Linked"],
    "Laser Destroyer Array": ["Twin-Linked"],
    "Neutron Beam Laser": ["Concussive", "Shock Pulse"],
    "Graviton Gun": ["Concussive", "Graviton"], "Graviton Cannon": ["Concussive", "Graviton"],
    "Hyperios Air-defence Missile Launcher": ["Skyfire", "Interceptor", "Heat Seeker"],
    "Solar Auxilia Grenade Launcher": ["Haywire"],
    "Quad Mortar": ["Shell Shock", "Sunder"],
    "AT Rounds": ["Rending", "Gets Hot", "Sniper"], "Volkite Rounds": ["Rending", "Sniper"],
    "Vanquisher Battle Cannon": ["Armourbane"],
    "Colossus Bombard": ["Ignores Cover"],
    "Rending Weapon": ["Rending"],
    "Power Fist": ["Unwieldy"], "Relic Blade": ["Two-Handed"],
    "Charonite Claws": ["Flesh Ripper"],
    "Lascutter": ["Unwieldy", "Cumbersome"],
    "Achmiris Dagger": ["Lithe"],
    "Melta-cutter Drill": ["Armourbane", "Shred"],
    "Phase Lancet": ["Poison"],
    "Breaching Charge": ["Breaching Charge", "Wrecker"],
    "Precision Bombardment": ["Precision Bombardment", "Pinning"],
    "Cyclops Incineration Charge": ["Massive Blast", "Ignores Cover"],
    "Atomantic Imploder": ["Blind"],
}

WARGEAR_ = {
    # armour
    "Void Armour": "Void Armour provides a 4+ Armour Save and counts as Void Hardened where relevant.",
    "Reinforced Void Armour": (
        "Reinforced Void Armour provides a 4+ Armour Save and counts as Void Hardened. The wearer may re-roll failed "
        "Armour Saves against attacks made with Blast or Template weapons."),
    "Void Recon Armour": ("Void Recon Armour provides a 5+ Armour Save, grants Stealth, and counts as Void Hardened.",
                          ["Stealth"]),
    "Void-Hardened Power Armour": "Void-Hardened Power Armour provides a 3+ Armour Save and counts as Void Hardened.",
    "Power Armour": "Power Armour provides a 3+ Armour Save.",
    "Artificer Armour": "Artificer Armour provides a 2+ Armour Save.",
    "Ambulator Frame": ("The Ambulator Frame provides MaSade with a 2+ Armour Save and grants him the It Will Not Die "
                        "special rule.", ["It Will Not Die"]),
    # protective
    "Boarding Shield": (
        "A Boarding Shield grants a 5+ Invulnerable Save. The shield occupies one hand; a model using one may not "
        "claim the bonus Attack for fighting with two close combat weapons."),
    "Refractor Field": "A Refractor Field grants a 5+ Invulnerable Save.",
    "Iron Halo": "An Iron Halo grants a 4+ Invulnerable Save.",
    "Displacer Matrix": (
        "A Displacer Matrix grants a 3+ Invulnerable Save. If a natural 1 is rolled when making this save, resolve the "
        "attack normally; if the bearer survives, remove it from the battlefield and place it in Reserve. It returns "
        "by Deep Strike at the beginning of its controlling player's next turn."),
    # command
    "Troop Vexilla": (
        "A unit containing a Troop Vexilla counts as having inflicted one additional Wound when determining which "
        "side won a close combat. The unit may also re-roll failed Regroup Tests."),
    "Cohort Vexilla": (
        "A Cohort Vexilla confers all the benefits of a Troop Vexilla. In addition, friendly Solar Auxilia units with "
        "at least one model within 24\" may re-roll failed Casualty Tests."),
    "Nuncio-vox": (
        "A friendly unit arriving by Deep Strike may use a Nuncio-vox as a teleport or landing beacon: if the first "
        "model is placed within 6\" of the bearer, the arriving unit does not scatter. It may not be used while its "
        "bearer is Broken, Pinned or embarked upon a Transport. (Taken by a vehicle under Top Working Order, the "
        "vehicle itself is the bearer.)"),
    "Cognis-signum": (
        "A Cognis-signum incorporates an Augury Scanner and grants its bearer Night Vision. In the Shooting phase the "
        "bearer may forgo firing; if it does so, its unit may re-roll one failed To Hit roll that phase.",
        ["Night Vision"]),
    "Augury Scanner": (
        "After all enemy Infiltrators have deployed, roll 4D6 for each unit containing an Augury Scanner. If an enemy "
        "Infiltrating unit is within the distance rolled and line of sight of the bearer, the unit may immediately "
        "fire once at that enemy unit before the battle begins (only one such attack per unit)."),
    "Infravisor": ("The bearer and its unit gain Night Vision. Models using an Infravisor count as Initiative 1 when "
                   "resolving the effects of Blind.", ["Night Vision"]),
    "Surveyor and Fire-direction Auguries": "Used by the Master of Ordnance for the Fire Direction special rule.",
    # medical
    "Medi-pack": ("The bearer and all models in the unit to which it is attached gain Feel No Pain (5+). Multiple "
                  "Medi-packs in the same unit do not improve this save.", ["Feel No Pain"]),
    "Narthecium": (
        "A unit containing a model equipped with a Narthecium may ignore the first failed saving throw it suffers "
        "during each player turn. It may not be used against Instant Death or against an attack which permits no "
        "saving throw of any kind."),
    "Auto-gurney": (
        "Jovan has Feel No Pain (4+). So long as Jovan has joined a friendly Infantry unit, all models in that unit "
        "also gain Feel No Pain (4+). Jovan counts as Very Bulky.", ["Feel No Pain"]),
    # personal
    "Psi-jammer": ("The bearer and its unit gain Adamantium Will.", ["Adamantium Will"]),
    "Grav-wave Generator": (
        "An enemy unit charging the bearer or its unit subtracts D3\" from its Charge distance. A unit which "
        "successfully charges the bearer gains no Hammer of Wrath attacks that turn."),
    "Cyber-familiar": (
        "A Cyber-familiar improves the bearer's Invulnerable Save by +1, to a maximum of 3+; a model without an "
        "Invulnerable Save instead gains a 6+ Invulnerable Save. The bearer may also re-roll failed characteristic "
        "tests other than Leadership tests and failed Dangerous Terrain tests."),
    "Digital Weapons": "The bearer may re-roll one failed To Wound roll in each Assault phase.",
    "Master-crafted Weapon": ("One weapon carried by the model is Master-crafted: it may re-roll one failed To Hit roll "
                              "per player turn.", ["Master-Crafted"]),
    "Shroud Bombs": "A unit equipped with Shroud Bombs counts as carrying Defensive Grenades.",
    "Camo Swags": "A model equipped with Camo Swags improves any Cover Save it receives by +1.",
    "Grim Endurance": "A model with this upgrade has +1 Wound.",
    "Jet Pack": ("Models equipped with Jet Packs use the normal ProHammer rules for Jet Pack Infantry.", []),
    "Heavy Stabilisers": (
        "Models equipped with Heavy Stabilisers reduce their normal Move distance by 2\". They also suffer a -2\" "
        "modifier to any Advance or Charge move they make, to a minimum of 0\"."),
    # mechanicum
    "Cortex Controller": (
        "Friendly Battle-Automata within 6\" of a model equipped with a Cortex Controller automatically pass any "
        "Command Uplink roll they are required to make."),
    "Servo-arm": (
        "A Servo-arm grants its bearer one additional close combat attack, resolved separately: it hits on a 4+, "
        "counts as a Power Fist attack and receives no bonus for charging or for fighting with another weapon. A "
        "Servo-arm also grants +1 to Battlesmith repair rolls."),
    # grenades
    "Frag Grenades": "Frag Grenades count as Assault Grenades. Against vehicles they attack at Strength 4 + D6 Armour "
                     "Penetration.",
    "Krak Grenades": "A model may exchange its normal attacks for one Krak Grenade attack against a vehicle (Strength "
                     "6 + D6 Armour Penetration).",
    "Melta Bombs": "A model may exchange its normal attacks for one Melta Bomb attack against a vehicle (Strength 8 + "
                   "2D6 Armour Penetration).",
    # vehicle equipment
    "Armoured Ceramite": "Melta weapons attacking a vehicle with Armoured Ceramite do not roll their additional Armour "
                         "Penetration die.",
    "Armoured Cockpit": "4+ to ignore Crew Shaken / Crew Stunned results (see Aeronautica Imperialis).",
    "Auxiliary Drive": "At the beginning of the vehicle's Movement phase, roll a D6 if it is Immobilised. On a 4+, the "
                       "Immobilised result is removed and the vehicle may move normally that turn.",
    "Flare Shield": "A Flare Shield only affects shooting attacks striking the vehicle's Front Armour: reduce the "
                    "Strength of Blast and Template weapons by 2 and of all other shooting attacks by 1. No effect in "
                    "close combat.",
    "Chaff Launcher": "Flare/Chaff Launcher: 4+ Invulnerable Save against missile weapons (see Aeronautica "
                      "Imperialis).",
    "Illum Flares": "Illuminates enemies at night (see Aeronautica Imperialis).",
    "Dozer Blade": "A vehicle equipped with a Dozer Blade may re-roll failed terrain tests.",
    "Extra Armour": "A vehicle with Extra Armour treats Crew Stunned results as Crew Shaken.",
    "Searchlight": "During Night Fighting, a vehicle may illuminate one enemy unit it has successfully targeted; that "
                   "unit may be fired upon normally for the rest of the turn. The vehicle may itself be targeted "
                   "normally.",
    "Smoke Launchers": "Once per battle, after moving, a vehicle may use its Smoke Launchers. Until the beginning of "
                       "its next turn, any Penetrating Hits suffered by the vehicle are treated as Glancing Hits.",
    "Induction Charger": ("Once per battle, at the beginning of its Movement phase, the Squadron may activate its "
                          "Induction Chargers: for the rest of that player turn every surviving vehicle in the Squadron "
                          "counts as a Fast Vehicle.", []),
    "Siege Armour": "A Malcador equipped with Siege Armour increases its Front Armour value to 14. It loses the Fast "
                    "vehicle type.",
    "Seismic Shock Shells": ("A Colossus Bombard firing Seismic Shock Shells gains Concussive and Sunder.",
                             ["Concussive"]),
}

# shared option lists
SGT_SWAPS = [("Blast Pistol", 2), ("Rending Weapon", 5), ("Needle Pistol", 5), ("Hand Flamer", 10),
             ("Plasma Pistol", 10), ("Power Weapon", 10), ("Power Fist", 15)]
LEGATE_SWAPS = [("Blast Pistol", 2), ("Rending Weapon", 5), ("Needle Pistol", 5), ("Volkite Serpenta", 5),
                ("Hand Flamer", 10), ("Plasma Pistol", 10), ("Power Weapon", 10), ("Power Fist", 15),
                ("Inferno Pistol", 15), ("Relic Blade", 25)]
CORE_RULES = ["Disciplined Fire", "Close Formation Fighting"]

# filled in by build()
DOC = {}
T = {}
IDS = {}


# ==================================================================================================  HELPERS
def doc(name):
    return cond(DOC[name], "force", "atLeast", 1)


def nodoc(name):
    return cond(DOC[name], "force", "lessThan", 1)


def gate(e, doctrine, max_id=None):
    """Hide e (and set its max to 0) unless the Cohort Doctrine is chosen."""
    mods = [modifier("set", "hidden", "true", conds=[nodoc(doctrine)])]
    if max_id:
        mods.append(modifier("set", max_id, 0, conds=[nodoc(doctrine)]))
    add_mods(e, mods)
    return e


def or_groups(*groups):
    return el("conditionGroup", {"type": "or"}, [wrap("conditionGroups", list(groups))])


def total_at_least_2(a, b):
    """Condition group: (selections of a) + (selections of b) >= 2 in the force."""
    return any_of(cond(a, "force", "atLeast", 2), cond(b, "force", "atLeast", 2))


def sum_ge2(ids):
    """Group true when the combined number of selections of the ids in the force is two or more."""
    gs_ = [any_of(*[cond(i, "force", "atLeast", 2) for i in ids])]
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            gs_.append(all_of(cond(ids[i], "force", "atLeast", 1), cond(ids[j], "force", "atLeast", 1)))
    return or_groups(*gs_)


def doc_error(doctrine, text, conds=(), groups=()):
    return modifier("add", "error", f"{doctrine}: {text}", conds=[doc(doctrine), *conds], groups=list(groups))


def forbid_error(name, unit_id, doctrines):
    """Error on a unit that a Cohort Doctrine forbids."""
    return [modifier("add", "error", f"{d}: the Detachment may not include {name}.", conds=[doc(d)])
            for d in doctrines]


def inline(key, name, cost, items, counts=None):
    """Inline entry carrying one or more linked items (e.g. 'Two Lascannons')."""
    eid = uid(key, "inline", name)
    links = []
    for it in dict.fromkeys(items):
        n = (counts or {}).get(it, items.count(it))
        lid = uid("link", eid, it)
        links.append(link(lid, W(it), it, constraints=[constraint(uid(lid, "min"), "min", n),
                                                       constraint(uid(lid, "max"), "max", n)]))
    return entry(eid, name, cost=cost, links=links)


def type_choice(key, title, unit_id, model_ids, options, extra_mods=()):
    """Exclusive choice for every model of one type: options [(name, pts per model, [items])]."""
    gid = uid("grp", key, title)
    ents = []
    for name, pts, items in options:
        eid = uid("choice", key, title, name)
        mods = [modifier("increment", PTS, pts, repeats=[repeat(m, unit_id, 1)]) for m in model_ids] if pts else []
        ents.append(entry(eid, name, mods=mods, constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                          links=[gear(eid, x) for x in items]))
    return group(gid, title, entries=ents, mods=list(extra_mods),
                 constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


def flat_choice(key, title, options, required=False, default=None):
    """Exclusive choice: options [(name, pts, [items], [rules])]."""
    gid = uid("grp", key, title)
    ents, dflt = [], None
    for name, pts, items, rls in options:
        eid = uid("choice", key, title, name)
        ents.append(entry(eid, name, cost=pts, constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                          links=[gear(eid, x) for x in items], infolinks=rules_links(list(rls), key=eid)))
        if name == default:
            dflt = eid
    cons = [constraint(uid(gid, "max"), "max", 1, auto=True)]
    if required:
        cons.append(constraint(uid(gid, "min"), "min", 1, auto=True))
    return group(gid, title, entries=ents, constraints=cons, default=dflt)


def transport_group(key, names):
    gid = uid("grp", key, "transport")
    return group(gid, "Dedicated Transport", links=[link(uid("link", gid, n), T[n], n) for n in names],
                 constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


def rolling_army(names):
    """Armoured Cohort - Rolling Army: an Infantry unit able to purchase a Dedicated Transport must do so."""
    return modifier("add", "error", "Armoured Cohort (Rolling Army): this unit must purchase a Dedicated Transport.",
                    conds=[doc("Armoured Cohort")], groups=[all_of(*[lacks(T[n], "self") for n in names])])


def top_working_order(key, flare=True):
    items = [("Nuncio-vox", 10)] + ([("Flare Shield", 35)] if flare else [])
    g = take(key, "Top Working Order (Armoured Cohort)", items)
    return gate(g, "Armoured Cohort")


def rename(eid, name):
    return modifier("set", "name", name, conds=[cond(eid, "self", "atLeast", 1)])


def set_stats(prof, ptype, changes, conds):
    """Profile modifiers: changes {characteristic: value} applied when conds hold."""
    mods = [modifier("set", gs.char_id(ptype, c), v, conds=list(conds)) for c, v in changes.items()]
    m = prof.find("modifiers")
    if m is None:
        m = el("modifiers")
        prof.insert(0, m)
    for x in mods:
        m.append(x)
    return prof


def sgt_slots(mid, opts=SGT_SWAPS, pistol="Laspistol", ccw="Close Combat Weapon"):
    return [slot(mid, f"Replace {pistol}", pistol, opts), slot(mid, f"Replace {ccw}", ccw, opts)]


def no_doc_error(text, doctrines_cond):
    return modifier("add", "error", text, groups=[doctrines_cond])


def move_role(new_cat, old_cat, doctrine, line=None):
    """Cohort Doctrine changes the unit's battlefield role."""
    mods = [modifier("set-primary", "category", new_cat, conds=[doc(doctrine)]),
            modifier("remove", "category", old_cat, conds=[doc(doctrine)])]
    if line == "add":
        mods.append(modifier("add", "category", LINE, conds=[doc(doctrine)]))
    return mods


# ==================================================================================================  HQ
def legate_commander():
    u = IDS["legate"]
    lm = IDS["lord_marshal"]
    prof = unit_profile(u, "Legate Commander", "Infantry (Character)", 4, 4, 3, 3, 3, 3, 2, 9, "4+")
    set_stats(prof, "Unit", {"I": 4, "A": 3, "Ld": 10}, [cond(lm, u, "atLeast", 1)])
    add_mods(prof, [modifier("set", "name", "Lord Marshal", conds=[cond(lm, u, "atLeast", 1)])])
    lm_entry = entry(lm, "Upgrade to Lord Marshal", cost=35,
                     constraints=[constraint(uid(lm, "max"), "max", 1, auto=True), unique(lm, 1, "roster")],
                     infolinks=rules_links(["Lord Marshal", "Household Retinue"], key=lm),
                     mods=[hide_if(has(IDS["masade"], "roster"))])
    lm_only = [("Relic Blade", W("Relic Blade")), ("Grav-wave Generator", W("Grav-wave Generator")),
               ("Displacer Matrix", W("Displacer Matrix"))]
    # deep=False: only the Legate's own wargear, not an attached Household Champion's Relic Blade (Cohort Attaches)
    errs = [modifier("add", "error", f"{n} is Lord Marshal only.",
                     groups=[all_of(has(i, u, deep=False), lacks(lm, u))]) for n, i in lm_only]
    veiled = gate(group(uid("grp", u, "veiled"), "Veiled Bodyguard (Reconnaissance Cohort)",
                        links=[link(uid("link", u, "veiled"), IDS["ach_ret"], "Achmiris Recon Section (Veiled Bodyguard)")],
                        constraints=[constraint(uid("grp", u, "veiled", "max"), "max", 1, auto=True)]),
                  "Reconnaissance Cohort", uid("grp", u, "veiled", "max"))
    groups = [
        *sgt_slots(u, LEGATE_SWAPS),
        take(u, "Wargear", [("Melta Bombs", 5), ("Digital Weapons", 5), ("Infravisor", 5), ("Psi-jammer", 5),
                            ("Grav-wave Generator", 10), ("Cyber-familiar", 10), ("Master-crafted Weapon", 10)]),
        slot(u, "Replace Refractor Field", "Refractor Field", [("Iron Halo", 10), ("Displacer Matrix", 15)]),
        slot(u, "Replace Void Armour", "Void Armour", [("Artificer Armour", 20)]),
        retinue_links(u, "legate"),
        attache_links(u),
        veiled,
    ]
    return unit("Legate Commander", 45, HQ, "HQ", profiles=[prof], key=u,
                kit=["Frag Grenades", "Krak Grenades"],
                rules_=["Independent Character", *CORE_RULES, "Disciplined Command", "High Command",
                        "Household Retinue"],
                entries=[lm_entry], groups=groups,
                mods=[modifier("set", "name", "Lord Marshal", conds=[cond(lm, "self", "atLeast", 1)]), *errs])


def retinue_links(u, key):
    gid = uid("grp", u, "lifeward")
    return group(gid, "Life Ward Retinue (no Force Organisation slot)",
                 links=[link(uid("link", gid, "lw"), IDS["lifeward"], "Solar Auxilia Life Ward Retinue")],
                 constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


def attache_links(u):
    gid = uid("grp", u, "attaches")
    return group(gid, "Cohort Attaches (no Force Organisation slot)",
                 links=[link(uid("link", gid, "att"), IDS["attaches"], "Cohort Attaches")],
                 constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


def tactical_command_section():
    u = IDS["tcs"]
    prof = lambda n, ws, w, a, ld, ut="Infantry (Character)": unit_profile(u, n, ut, ws, 4, 3, 3, w, 3, a, ld, "4+")
    kit = ["Void Armour", "Laspistol", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"]
    strat = model(u, "Strategos", 1, 1, 0, prof("Strategos", 3, 2, 2, 8),
                  kit=["Void Armour", "Frag Grenades", "Krak Grenades", "Cognis-signum", "Precision Bombardment"],
                  groups=sgt_slots(uid("model", u, "Strategos")), rules_=["Precision Bombardment"])
    proc = model(u, "Proclaimator", 1, 1, 0, prof("Proclaimator", 3, 1, 1, 7), kit=kit + ["Nuncio-vox"])
    vex = model(u, "Vexilarius", 1, 1, 0, prof("Vexilarius", 3, 1, 1, 7), kit=kit + ["Cohort Vexilla"])
    vid = uid("model", u, "Veteran Auxiliary")
    vets = model(u, "Veteran Auxiliary", 2, 7, 5, prof("Veteran Auxiliary", 3, 1, 1, 7, "Infantry"),
                 kit=["Void Armour", "Laspistol", "Close Combat Weapon", "Frag Grenades", "Krak Grenades",
                      "Auxilia Lasrifle", "Collimator", "Blast-charger"])
    swaps, _ = pool(u, "Veteran Auxiliaries: replace Auxilia Lasrifle, Collimator and Blast-charger (up to two)", u,
                    [("Volkite Charger", 5), ("Solar Auxilia Grenade Launcher", 5), ("Flamer", 5),
                     ("Rotor Cannon", 10), ("Meltagun", 10), ("Plasma Gun", 15)], 2)
    names = ["Dracosan Armoured Transport", "Auxilia Arvus Lighter"]
    return unit("Auxilia Tactical Command Section", 75 - 2 * 5, HQ, "HQ", key=u,
                models=[strat, proc, vex, vets], rules_=[*CORE_RULES, "Disciplined Command"],
                groups=[swaps, attache_links(u), transport_group(u, names)], mods=[rolling_army(names)])


def tank_commander():
    u = IDS["tank_cmd"]
    aces = [("Tank Hunter", ["Tank Ace: Tank Hunter", "Tank Hunters"]),
            ("Field Repairs", ["Tank Ace: Field Repairs", "It Will Not Die"]),
            ("Reconnaissance Ace", ["Tank Ace: Reconnaissance Ace", "Scout"]),
            ("Infantry Killer", ["Tank Ace: Infantry Killer"]),
            ("Monster Hunter", ["Tank Ace: Monster Hunter", "Monster Hunter"]),
            ("Dead-eye Gunner", ["Tank Ace: Dead-eye Gunner", "Master-Crafted"])]
    ace = flat_choice(u, "Tank Ace ability", [(n, 0, [], r) for n, r in aces], required=True)
    vehicles = ["Auxilia Leman Russ (any type)", "Auxilia Malcador Heavy Tank", "Auxilia Malcador Infernus",
                "Auxilia Valdor Tank Hunter", "Baneblade / Stormblade / Stormlord / Stormhammer / Shadowsword "
                "(Engines of War)", "Armoured Sentinel Squadron (Command Sentinel)"]
    veh = flat_choice(u, "Commanded Vehicle", [(n, 0, [], []) for n in vehicles], required=True)
    eligible = [IDS["lr_strike"], IDS["lr_assault"], IDS["malcador"], IDS["infernus"], IDS["valdor"],
                IDS["sentinels"]]
    warn = modifier("add", "warning", "An Auxilia Tank Commander must be assigned to an eligible vehicle included in "
                                      "the army (Leman Russ, Malcador, Valdor, super-heavy tank or Armoured Sentinel "
                                      "Squadron).",
                    groups=[all_of(*[cond(i, "force", "lessThan", 1) for i in eligible])])
    return unit("Auxilia Tank Commander", 55, HQ, "HQ", key=u, compulsory=False,
                rules_=["Support Officer", "Disciplined Command", "Armoured Warfare", "Command Tank", "Tank Ace"],
                groups=[veh, ace], mods=[warn])


def life_ward_retinue():
    u = IDS["lifeward"]
    mid = uid("model", u, "Life Ward")
    lw = model(u, "Life Ward", 1, 6, 15, unit_profile(u, "Life Ward", "Infantry (Character)", 4, 4, 3, 3, 1, 4, 2, 8,
                                                      "4+"),
               kit=["Void Armour", "Laspistol", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"])
    opts = [("Blast Pistol", 2), ("Volkite Serpenta", 2), ("Rending Weapon", 5), ("Needle Pistol", 5),
            ("Hand Flamer", 5), ("Power Weapon", 10), ("Plasma Pistol", 10)]
    # *Power Fist / Inferno Pistol: only one Life Ward in the Detachment (L870) - own entries, counted force-wide
    star_ids = IDS.setdefault("lw_star", [])

    def stars(title):
        out = []
        for n in ["Power Fist", "Inferno Pistol"]:
            eid = uid(u, "star", title, n)
            star_ids.append(eid)
            out.append(entry(eid, f"{n}*", cost=15, links=[gear(eid, n)]))
        return out
    t1, t2 = "Life Wards: replace Laspistol (any number)", "Life Wards: replace Close Combat Weapon (any number)"
    groups = [model_swaps(u, t1, u, [mid], opts, entries=stars(t1)),
              model_swaps(u, t2, u, [mid], opts, entries=stars(t2)),
              model_swaps(u, "Life Wards: one of the following each (any number)", u, [mid],
                          [("Shotgun", 2), ("Laslock", 2), ("Sniper Rifle", 5), ("Volkite Charger", 5), ("Flamer", 5),
                           ("Rotor Cannon", 5), ("Nuncio-vox", 10), ("Augury Scanner", 15)]),
              model_takes(u, "Life Wards: wargear (any number)", u, [mid],
                          [("Melta Bombs", 5), ("Infravisor", 5), ("Refractor Field", 10), ("Grim Endurance", 10)]),
              attache_links(u)]
    err = modifier("add", "error", "Only one Life Ward in the Detachment may select a Power Fist or Inferno Pistol.",
                   groups=[sum_ge2(list(star_ids))])
    return entry(u, "Solar Auxilia Life Ward Retinue", typ="unit", mods=[err],
                 infolinks=rules_links([*CORE_RULES, "Hold the Line", "Retinue", "Life Ward Retinue"], key=u),
                 entries=[lw], groups=groups)


def cohort_attaches():
    u = IDS["attaches"]
    base_kit = ["Void Armour", "Laspistol", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"]

    def att(name, cost, stats, kit, rls, groups=(), sv="4+"):
        mid = uid("model", u, name)
        return entry(mid, name, typ="model", cost=cost,
                     constraints=[constraint(uid(mid, "max"), "max", 1, auto=True)],
                     profiles=[unit_profile(u, name, "Infantry (Character)", *stats, sv)],
                     links=[gear(mid, x) for x in kit], infolinks=rules_links(rls, key=mid), groups=list(groups))
    champ_id = uid("model", u, "Household Champion")
    ast_id = uid("model", u, "Astropath Primus")
    # Psyker - Mastery Level 1: one power from Biomancy, Divination, Pyromancy, Telekinesis or Telepathy (L984)
    psy = L.psychic_powers(ast_id, ast_id, 1, L.PSY.LIBRARIAN)
    models = [
        att("Cohort Chirurgeon", 35, (3, 4, 3, 3, 2, 3, 1, 8), base_kit + ["Narthecium"],
            [*CORE_RULES, "Master Chirurgeon"]),
        att("Astropath Primus", 45, (3, 3, 3, 3, 2, 3, 1, 9),
            ["Void Armour", "Laspistol", "Force Staff", "Frag Grenades", "Krak Grenades"],
            ["Psyker", "Astropathic Discipline"], groups=[psy]),
        att("Master of Ordnance", 30, (3, 4, 3, 3, 2, 3, 1, 8),
            base_kit + ["Nuncio-vox", "Surveyor and Fire-direction Auguries"], [*CORE_RULES, "Fire Direction"]),
        att("Fleet Liaison Officer", 25, (3, 4, 3, 3, 2, 3, 1, 8), base_kit + ["Nuncio-vox"],
            [*CORE_RULES, "Fleet Coordination"]),
        att("Mechanicum Liaison Adept", 45, (3, 3, 3, 3, 2, 3, 1, 8),
            ["Power Armour", "Laspistol", "Power Axe", "Servo-arm", "Cortex Controller"],
            ["Battlesmith", "Mechanicum Liaison"], sv="3+"),
        att("Household Champion", 40, (5, 4, 3, 3, 2, 4, 3, 9),
            ["Void Armour", "Laspistol", "Frag Grenades", "Krak Grenades", "Refractor Field"],
            [*CORE_RULES, "Master Duellist"],
            groups=[slot(champ_id, "Replace Power Weapon", "Power Weapon",
                         [("Rending Weapon", 0), ("Power Fist", 5), ("Relic Blade", 15)])], sv="4+/5+"),
    ]
    gid = uid("grp", u, "attaches")
    g = group(gid, "Cohort Attaches (up to three, each type once)", entries=models,
              constraints=[constraint(uid(gid, "min"), "min", 1), constraint(uid(gid, "max"), "max", 3)])
    return entry(u, "Cohort Attaches", typ="unit", constraints=[unique(u, 1, "force")],
                 infolinks=rules_links(["Cohort Attaches"], key=u), groups=[g])


def ireton_masade():
    u = IDS["masade"]
    e = unit("Ireton MaSade", 165, HQ, "HQ", key=u,
             profiles=[unit_profile(u, "Ireton MaSade", "Infantry (Independent Character)", 3, 5, 3, 3, 3, 3, 2, 10,
                                    "2+")],
             kit=["Ambulator Frame", "Archaeotech Pistol", "Master-crafted Power Weapon", "Frag Grenades",
                  "Krak Grenades", "Iron Halo", "Psi-jammer"],
             rules_=["Independent Character", *CORE_RULES, "Disciplined Command", "High Command", "Hatred (Traitors)",
                     "Master of the Battlefield", "Protector of Agathon", "Warlord (Ireton MaSade)"],
             groups=[retinue_links(u, "masade")],
             constraints=[unique(u, 1, "roster")],
             mods=[hide_if(has(L.TRAITOR, "roster")),
                   modifier("add", "error", "Ireton MaSade is Loyalist only.", conds=[has(L.TRAITOR, "roster")]),
                   modifier("add", "error", "Ireton MaSade must be the army's Warlord: an army with MaSade may not "
                                            "include a Lord Marshal (either one or the other).",
                            conds=[has(IDS["lord_marshal"], "roster")])])
    return e


# ==================================================================================================  ELITES
def medicae_detachment():
    u = IDS["medicae"]
    mid = uid("model", u, "Medicae Orderly")
    m = model(u, "Medicae Orderly", 3, 6, 15,
              unit_profile(u, "Medicae Orderly", "Infantry (Character)", 3, 3, 3, 3, 1, 3, 1, 8, "4+"),
              kit=["Void Armour", "Laspistol", "Close Combat Weapon", "Medi-pack"])
    return unit("Auxilia Medicae Detachment", 60 - 3 * 15, ELITES, "Elites", key=u, models=[m],
                rules_=[*CORE_RULES, "Attached Deployment"],
                groups=[model_takes(u, "Medicae Orderlies: wargear (any number)", u, [mid], [("Needle Pistol", 10)])])


def rapier_battery():
    u = IDS["rapier"]
    car = uid("model", u, "Rapier Carrier")
    crew = uid("model", u, "Auxiliary Crew")
    carrier = model(u, "Rapier Carrier", 1, 3, 35,
                    unit_profile(u, "Rapier Carrier", "Artillery", "-", "-", "-", 7, 2, "-", "-", "-", "3+"),
                    groups=[slot(car, "Replace Quad Multi-laser", "Quad Multi-laser",
                                 [("Laser Destroyer Array", 15), ("Quad Mortar", 35), ("Graviton Cannon", 35)])])
    carriers = numbered(carrier, 3, 1)
    cids = [c.get("id") for c in carriers]
    cmin, cmax = uid(crew, "min"), uid(crew, "max")
    crews = entry(crew, "Auxiliary Crew", typ="model",
                  mods=[modifier(t, f, 2, repeats=[repeat(c, u, 1)]) for c in cids for t, f in
                        (("increment", cmin), ("increment", cmax))],
                  constraints=[constraint(cmin, "min", 0, auto=True), constraint(cmax, "max", 0, auto=True)],
                  profiles=[unit_profile(u, "Auxiliary", "Infantry", 3, 3, 3, 3, 1, 3, 1, 7, "4+")],
                  links=[gear(crew, x) for x in ["Void Armour", "Lasgun", "Close Combat Weapon"]],
                  infolinks=rules_links(CORE_RULES, key=crew))
    return unit("Auxilia Rapier Battery", 0, ELITES, "Elites", key=u, models=[*carriers, crews],
                rules_=["Artillery (Rapier)"],
                mods=[*forbid_error("Auxilia Rapier Batteries", u, ["Reconnaissance Cohort"]),
                      doc_error("Veletaris Assault Cohort", "no more than one Auxilia Rapier Battery may be selected.",
                                conds=[cond(u, "force", "atLeast", 2)])])


def ogryn_charonites():
    u = IDS["ogryns"]
    m = model(u, "Ogryn Charonite", 3, 9, 55,
              unit_profile(u, "Ogryn Charonite", "Infantry", 4, 3, 5, 5, 3, 2, 3, 6, "4+"),
              kit=["Void Armour", "Charonite Claws"])
    return unit("Auxilia Ogryn Charonite Squad", 185 - 3 * 55, ELITES, "Elites", key=u, models=[m],
                rules_=["Hammer of Wrath", "Stubborn", "Very Bulky", "Feel No Pain (6+)", "Dead-man's Switch",
                        "Brutal Fighters", "Mind-slave"])


def enginseer_auxilia():
    u = IDS["enginseer"]
    aid = uid("model", u, "Enginseer Adept")
    sid = uid("model", u, "Servo-automata")
    adept = model(u, "Enginseer Adept", 1, 3, 20,
                  unit_profile(u, "Enginseer Adept", "Infantry (Character)", 3, 3, 3, 3, 1, 3, 1, 8, "3+"),
                  kit=["Power Armour", "Laspistol", "Power Weapon", "Servo-arm"],
                  rules_=["Battlesmith", "Servo-automata Support"])
    servo = model(u, "Servo-automata", 0, 8, 5,
                  unit_profile(u, "Servo-automata", "Infantry", 3, 3, 4, 5, 1, 1, 1, 6, "5+"),
                  kit=["Close Combat Weapon"], rules_=["Cybernetica"])
    return unit("Enginseer Auxilia", 45 - 20, ELITES, "Elites", key=u, models=[adept, servo],
                groups=[model_takes(u, "Enginseer Adepts: wargear (any number)", u, [aid],
                                    [("Augury Scanner", 5), ("Infravisor", 5), ("Melta Bombs", 5), ("Nuncio-vox", 10),
                                     ("Volkite Charger", 10), ("Refractor Field", 10), ("Cyber-familiar", 10),
                                     ("Cortex Controller", 15), ("Graviton Gun", 15)]),
                        model_swaps(u, "Servo-automata: one of the following each (any number)", u, [sid],
                                    [("Servo-arm", 5), ("Flamer", 5), ("Phased Plasma-fusil", 10),
                                     ("Rotor Cannon", 10), ("Solar Auxilia Grenade Launcher", 10),
                                     ("Heavy Bolter", 15), ("Multi-melta", 15)])])


def eidis_section(u, tercio):
    """Eidis Engineer Section: Elites (standalone) or a Pioneer Section inside a Tercio (Void & Siege Cohort)."""
    pid = uid("model", u, "Prime")
    eng = uid("model", u, "Engineer")
    eii = uid("model", u, "Eidii")
    up = uid("model", u, "Eidii (upgraded Engineer)")
    rva_kit = ["Reinforced Void Armour", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"]
    prime_opts = [("Blast Pistol", 2), ("Rending Weapon", 5), ("Needle Pistol", 5), ("Boarding Shield", 5),
                  ("Hand Flamer", 10), ("Plasma Pistol", 10), ("Power Weapon", 10), ("Power Fist", 15)]
    weapons = [("Lascutter", 5), ("Plasma Gun", 15), ("Meltagun", 15)]
    bc_id = uid(u, "breaching-free")
    # Void & Siege - Breaching Formations (L5064): one Section in the Detachment; only the Prime gets it (author)
    free_bc = gate(entry(bc_id, "Breaching Charge for free (Void & Siege Cohort, one Section in the Detachment)",
                         constraints=[constraint(uid(bc_id, "max"), "max", 1, auto=True)],
                         links=[gear(bc_id, "Breaching Charge")]),
                   "Void & Siege Cohort", uid(bc_id, "max"))
    add_mods(free_bc, [modifier("add", "error", "The Prime may carry only one Breaching Charge (paid or free).",
                                conds=[cond(W("Breaching Charge"), pid, "atLeast", 2)])])
    IDS.setdefault("eidis_bc", []).append(bc_id)
    prime = model(u, "Prime", 1, 1, 0, unit_profile(u, "Prime", "Infantry (Character)", 4, 4, 3, 3, 1, 3, 2, 9, "4+"),
                  kit=["Reinforced Void Armour", "Frag Grenades", "Krak Grenades"],
                  groups=[*sgt_slots(pid, prime_opts),
                          slot(pid, "Replace Volkite Charger (optional, need not match the Section)",
                               "Volkite Charger", weapons),
                          take(pid, "Prime Wargear", [("Breaching Charge", 10)], max_total=1,
                               hide=[cond(bc_id, pid, "atLeast", 1)])],
                  entries=[free_bc])
    emin, emax = uid(eng, "min"), uid(eng, "max")
    engineers = entry(eng, "Engineer", typ="model",
                      mods=[modifier("decrement", emin, 1, repeats=[repeat(up, u, 1)]),
                            modifier("decrement", emax, 1, repeats=[repeat(up, u, 1)])],
                      constraints=[constraint(emin, "min", 4, auto=True), constraint(emax, "max", 4, auto=True)],
                      profiles=[unit_profile(u, "Engineer", "Infantry", 3, 3, 3, 3, 1, 3, 1, 7, "4+")],
                      links=[gear(eng, x) for x in rva_kit + ["Auxilia Lasrifle"]])
    eidii_prof = unit_profile(u, "Eidii", "Infantry", 3, 4, 3, 3, 1, 3, 1, 8, "4+")
    eidii = model(u, "Eidii", 0, 5, 5, eidii_prof, kit=rva_kit + ["Volkite Charger", "Laspistol"])
    upgraded = model(u, "Eidii (upgraded Engineer)", 0, 4, 10,
                     unit_profile(u, "Eidii (upgraded Engineer)", "Infantry", 3, 4, 3, 3, 1, 3, 1, 8, "4+"),
                     kit=rva_kit + ["Volkite Charger", "Laspistol"])
    groups = [
        type_choice(u, "Engineers: replace Auxilia Lasrifles (all Engineers)", u, [eng],
                    [(n, p, [n]) for n, p in weapons]),
        type_choice(u, "Eidii: replace Volkite Chargers (all Eidii)", u, [eii, up], [(n, p, [n]) for n, p in weapons]),
        model_swaps(u, "Engineers and Eidii: replace Close Combat Weapon (any number)", u, [eng, eii, up],
                    [("Boarding Shield", 5)]),
        take(u, "Section Equipment (one model)", [("Nuncio-vox", 10)]),
        transport_group(u, ["Hades Breaching Drill"]),
    ]
    rules_ = [*CORE_RULES, "Move Through Cover"] + (["Support Section"] if tercio else [])
    ents = [prime, engineers, eidii, upgraded, per_model(u, "Melta Bombs (entire Section)", 5, u, ["Melta Bombs"])]
    mods = [rolling_army(["Hades Breaching Drill"])]
    if tercio:
        return entry(u, "Eidis Engineer Section (Pioneer Section)", typ="unit", mods=mods,
                     infolinks=rules_links(rules_, key=u), entries=ents, groups=groups)
    return unit("Eidis Engineer Section", 25, ELITES, "Elites", key=u, entries=ents, groups=groups, rules_=rules_,
                mods=mods)


def aevos_jovan():
    u = IDS["jovan"]
    return unit("Surgeon-Primus Aevos Jovan", 65, ELITES, "Elites", key=u,
                profiles=[unit_profile(u, "Aevos Jovan", "Infantry (Character)", 2, 2, 3, 3, 2, 3, 1, 9, "4+")],
                kit=["Void Armour", "Master-crafted Needle Pistol", "Phase Lancet", "Auto-gurney"],
                rules_=["Independent Character", "Very Bulky", "Miraculous Skill", "Surgeon-Primus"],
                groups=[retinue_links(u, "jovan")], constraints=[unique(u, 1, "roster")])


# ==================================================================================================  TROOPS
def lasrifle_section():
    u = IDS["las"]
    sid = uid("model", u, "Sergeant")
    tm = IDS["troop_master"]
    vs = IDS["vaskale"]
    sprof = unit_profile(u, "Sergeant", "Infantry (Character)", 3, 3, 3, 3, 1, 3, 2, 8, "4+")
    set_stats(sprof, "Unit", {"WS": 4, "BS": 4, "W": 2}, [cond(tm, sid, "atLeast", 1)])
    set_stats(sprof, "Unit", {"WS": 4, "BS": 4, "W": 2, "I": 2, "Ld": 9}, [cond(vs, sid, "atLeast", 1)])
    add_mods(sprof, [modifier("set", "name", "Troop Master", conds=[cond(tm, sid, "atLeast", 1)]),
                     modifier("set", "name", "Vaskale Solar", conds=[cond(vs, sid, "atLeast", 1)])])
    vaskale = entry(vs, "Upgrade to Vaskale Solar (Loyalist)", cost=30,
                    constraints=[constraint(uid(vs, "max"), "max", 1, auto=True), unique(vs, 1, "roster")],
                    infolinks=rules_links(["Vaskale Solar", "Tercio Commander", "Veteran of the Dawn Gate", "Hold Fast",
                                           "Battered Body"], key=vs),
                    mods=[hide_if(has(L.TRAITOR, "roster")),
                          modifier("add", "error", "Vaskale Solar is Loyalist only.", conds=[has(L.TRAITOR, "roster")])])
    troop_master = entry(tm, "Upgrade to Troop Master", cost=15,
                         constraints=[constraint(uid(tm, "max"), "max", 1, auto=True)],
                         infolinks=rules_links(["Troop Master"], key=tm), entries=[vaskale])
    las_default = inline(sid, "Auxilia Lasrifle and Collimator", 0, ["Auxilia Lasrifle", "Collimator"])
    opts = [("Laspistol", 0)] + SGT_SWAPS
    sgt = model(u, "Sergeant", 1, 1, 0, sprof,
                kit=["Void Armour", "Frag Grenades", "Krak Grenades"],
                entries=[troop_master],
                groups=[slot(sid, "Replace Auxilia Lasrifle and Collimator", None, opts, default_is_entry=las_default),
                        slot(sid, "Replace Close Combat Weapon", "Close Combat Weapon", opts),
                        take(sid, "Sergeant Wargear", [("Melta Bombs", 5)])],
                mods=[modifier("set", "name", "Troop Master", conds=[cond(tm, "self", "atLeast", 1)]),
                      modifier("set", "name", "Vaskale Solar", conds=[cond(vs, "self", "atLeast", 1)])])
    kit = ["Void Armour", "Auxilia Lasrifle", "Collimator", "Close Combat Weapon", "Frag Grenades", "Krak Grenades"]
    prof = lambda n: unit_profile(u, n, "Infantry", 3, 3, 3, 3, 1, 3, 1, 7, "4+")
    vex = model(u, "Vexilla Bearer", 1, 1, 0, prof("Vexilla Bearer"), kit=kit + ["Troop Vexilla"])
    vox = model(u, "Vox Operator", 1, 1, 0, prof("Vox Operator"), kit=kit + ["Nuncio-vox"])
    aux = model(u, "Auxiliary", 17, 17, 0, prof("Auxiliary"), kit=kit)
    bc = upgrade(u, "Blast-chargers (entire Section)", 25, links=["Blast-charger"])
    rva_id = uid(u, "rva")
    rva = gate(entry(rva_id, "Reinforced Void Armour (entire Section, Void & Siege Cohort)", cost=40,
                     constraints=[constraint(uid(rva_id, "max"), "max", 1, auto=True)],
                     links=[gear(rva_id, "Reinforced Void Armour")]), "Void & Siege Cohort", uid(rva_id, "max"))
    names = ["Dracosan Armoured Transport"]
    return entry(u, "Auxilia Lasrifle Section", typ="unit", cost=100, mods=[rolling_army(names)],
                 infolinks=rules_links([*CORE_RULES, "Hold the Line", "Zone Mortalis Deployment"], key=u),
                 entries=[sgt, vex, vox, aux, bc, rva], groups=[transport_group(u, names)])


def veletaris_section(u, household):
    prime_ws = 4
    vel_ws = 4 if household else 3
    pid = uid("model", u, "Prime")
    prime = model(u, "Prime", 1, 1, 0,
                  unit_profile(u, "Prime", "Infantry (Character)", prime_ws, 4, 3, 3, 1, 3, 2, 9, "4+"),
                  kit=["Reinforced Void Armour", "Volkite Charger", "Frag Grenades", "Krak Grenades"],
                  groups=[*sgt_slots(pid), take(pid, "Prime Wargear", [("Melta Bombs", 5)])])
    vel = model(u, "Veletarii", 9, 9, 0, unit_profile(u, "Veletarii", "Infantry", vel_ws, 4, 3, 3, 1, 3, 1, 8, "4+"),
                kit=["Reinforced Void Armour", "Volkite Charger", "Laspistol", "Close Combat Weapon", "Frag Grenades",
                     "Krak Grenades"])
    weapons = flat_choice(u, "Veletarii: replace Volkite Chargers (all Veletarii; the Prime may match)", [
        ("Rotor Cannons (Veletarii)", 0, ["Rotor Cannon"], []),
        ("Rotor Cannons (Veletarii and Prime)", 0, ["Rotor Cannon"], []),
        ("Power Weapons (Veletarii)", 45, ["Power Weapon"], []),
        ("Power Weapons (Veletarii and Prime)", 50, ["Power Weapon"], [])])
    names = ["Dracosan Armoured Transport"] + (["Auxilia Arvus Lighter"] if household else [])
    rls = [*CORE_RULES, "Move Through Cover"]
    rls += ["Household Retinue", "Preferred Enemy (Infantry)"] if household else ["Hold the Line"]
    ents = [prime, vel, upgrade(u, "Shroud Bombs (entire Section)", 25, links=["Shroud Bombs"])]
    groups = [weapons, take(u, "Section Equipment (one Veletarii)", [("Nuncio-vox", 10)]),
              transport_group(u, names)]
    mods = [rolling_army(names)]
    if household:
        mods.append(modifier("add", "error", "Household Retinue: requires a Lord Marshal as the army's Warlord.",
                             conds=[cond(IDS["lord_marshal"], "force", "lessThan", 1)]))
        return unit("Veletaris Storm Section (Household Retinue)", 115, ELITES, "Elites", key=u, entries=ents,
                    groups=groups, rules_=rls, mods=mods)
    return entry(u, "Veletaris Storm Section", typ="unit", cost=115, mods=mods, infolinks=rules_links(rls, key=u),
                 entries=ents, groups=groups)


def flamer_section():
    u = IDS["flamer"]
    sid = uid("model", u, "Sergeant")
    sgt = model(u, "Sergeant", 1, 1, 0, unit_profile(u, "Sergeant", "Infantry (Character)", 3, 3, 3, 3, 1, 3, 2, 8, "4+"),
                kit=["Reinforced Void Armour", "Flamer", "Frag Grenades", "Krak Grenades"],
                groups=[*sgt_slots(sid), take(sid, "Sergeant Wargear", [("Melta Bombs", 5)])])
    aux = model(u, "Auxiliary", 9, 9, 0, unit_profile(u, "Auxiliary", "Infantry", 3, 3, 3, 3, 1, 3, 1, 7, "4+"),
                kit=["Reinforced Void Armour", "Flamer", "Frag Grenades", "Krak Grenades"])
    names = ["Dracosan Armoured Transport"]
    return entry(u, "Auxilia Flamer Section", typ="unit", cost=125, mods=[rolling_army(names)],
                 infolinks=rules_links([*CORE_RULES, "Hold the Line", "Support Section"], key=u),
                 entries=[sgt, aux], groups=[transport_group(u, names)])


def achmiris_section(u, variant):
    """variant: 'fa' (Fast Attack), 'tercio' (Veiled Ranks), 'retinue' (Veiled Bodyguard)."""
    sid = uid("model", u, "Veil Sergeant")
    sgt = model(u, "Veil Sergeant", 1, 1, 0,
                unit_profile(u, "Veil Sergeant", "Infantry (Character)", 4, 4, 3, 3, 1, 3, 2, 8, "5+"),
                kit=["Void Recon Armour", "Sniper Rifle", "Laspistol", "Close Combat Weapon", "Nuncio-vox"])
    ach = model(u, "Achmirii", 4, 9, 15, unit_profile(u, "Achmirii", "Infantry", 3, 4, 3, 3, 1, 3, 1, 7, "5+"),
                kit=["Void Recon Armour", "Sniper Rifle", "Laspistol", "Close Combat Weapon"])
    swap_title = "Exchange Sniper Rifles (entire Section)"
    swap = flat_choice(u, swap_title, [
        ("Auxilia Lasrifles with Collimators and Blast-chargers", 0,
         ["Auxilia Lasrifle", "Collimator", "Blast-charger"], []),
        ("Achmiris Daggers", 0, ["Achmiris Dagger"], [])])
    swapped = [has(uid("choice", u, swap_title, n), u) for n in
               ["Auxilia Lasrifles with Collimators and Blast-chargers", "Achmiris Daggers"]]
    # L2820-2824: whole-Section upgrade, every model buys it, only one of the two (author)
    ammo = choice(u, "Special Ammunition (entire Section, one; only with Sniper Rifles)",
                  [(n, 5, True, [n], []) for n in ["AT Rounds", "Volkite Rounds"]], unit_id=u, hide=swapped)
    ammo_ids = [uid("choice", u, "Special Ammunition (entire Section, one; only with Sniper Rifles)", n)
                for n in ["AT Rounds", "Volkite Rounds"]]
    ammo_err = modifier("add", "error", "Special Ammunition may only be purchased if the Section retains its "
                                        "Sniper Rifles.",
                        groups=[any_of(*swapped), any_of(*[has(a, u) for a in ammo_ids])])
    rls = [*CORE_RULES, "Move Through Cover", "Infiltrate", "Focus Fire"]
    if variant == "tercio":
        rls.append("Hold the Line")
    if variant == "retinue":
        rls += ["Retinue", "Preferred Enemy (Infantry)"]
    ents = [sgt, ach, upgrade(u, "Camo Swags (entire Section)", 25, links=["Camo Swags"])]
    mods = [ammo_err]
    if variant == "fa":
        return unit("Achmiris Recon Section", 90 - 4 * 15, FA, "Fast Attack", key=u, entries=ents, groups=[swap, ammo],
                    rules_=rls, mods=mods)
    cons = [unique(u, 1, "force")] if variant == "retinue" else []
    name = {"tercio": "Achmiris Recon Section (Veiled Ranks)",
            "retinue": "Achmiris Recon Section (Veiled Bodyguard)"}[variant]
    return entry(u, name, typ="unit", cost=90 - 4 * 15, mods=mods, constraints=cons,
                 infolinks=rules_links(rls, key=u), entries=ents, groups=[swap, ammo])


def infantry_tercio():
    u = IDS["tercio"]
    gid = uid("grp", u, "sections")
    links = [link(uid("link", gid, "las"), IDS["las"], "Auxilia Lasrifle Section"),
             link(uid("link", gid, "vel"), IDS["vel"], "Veletaris Storm Section"),
             link(uid("link", gid, "flm"), IDS["flamer"], "Auxilia Flamer Section")]
    for key, target, name, doctrine, mx in [
            ("ach", IDS["ach_t"], "Achmiris Recon Section (Veiled Ranks)", "Reconnaissance Cohort", 2),
            ("eid", IDS["eid_t"], "Eidis Engineer Section (Pioneer Section)", "Void & Siege Cohort", 3)]:
        lid = uid("link", gid, key)
        lk = link(lid, target, name, constraints=[constraint(uid(lid, "max"), "max", mx, auto=True)])
        links.append(gate(lk, doctrine, uid(lid, "max")))
    sections = group(gid, "Sections (one to three)", links=links,
                     constraints=[constraint(uid(gid, "min"), "min", 1), constraint(uid(gid, "max"), "max", 3)])
    support = modifier("add", "error", "Support Section: an Auxilia Flamer Section (or Pioneer Eidis Engineer Section) "
                                       "requires an Auxilia Lasrifle Section in the same Tercio.",
                       conds=[lacks(IDS["las"], "self")],
                       groups=[any_of(has(IDS["flamer"], "self"), has(IDS["eid_t"], "self"))])
    tm = modifier("add", "error", "Only one Sergeant in each Infantry Tercio may be upgraded to a Troop Master.",
                  conds=[cond(IDS["troop_master"], "self", "atLeast", 2)])
    return unit("Auxilia Infantry Tercio", 0, TROOPS, "Troops", key=u, groups=[sections],
                rules_=["Auxilia Infantry Tercio"],
                mods=[support, tm, modifier("remove", "category", LINE, conds=[doc("Armoured Cohort")])])


# ==================================================================================================  TRANSPORTS
def dracosan():
    t = T["Dracosan Armoured Transport"]
    tp = transport_profile(t, "Dracosan", "20 models (no Bulky, Very Bulky or Extremely Bulky models)",
                           "One access hatch on each side of the hull", "None")
    tp.insert(0, wrap("modifiers", [modifier("set", gs.char_id("Transport", "Capacity"),
                                             "10 models (Demolisher Cannon; no Bulky, Very Bulky or Extremely Bulky "
                                             "models)", conds=[has(W("Demolisher Cannon"), t)])]))
    return entry(t, "Dracosan Armoured Transport", typ="unit", cost=135,
                 cats=[foc(gs.CAT_TRANSPORT, "Dedicated Transport", t)],
                 profiles=[vehicle_profile(t, "Dracosan", "Vehicle (Tank, Transport)", 3, 13, 12, 11), tp],
                 infolinks=rules_links(["Explorator Adaption"], key=t),
                 links=[gear(t, x) for x in ["Searchlight", "Smoke Launchers", "Extra Armour"]],
                 groups=[slot(t, "Replace Twin-linked Lascannon", "Twin-linked Lascannon", [("Demolisher Cannon", 30)]),
                         take(t, "Vehicle Upgrades", [("Dozer Blade", 5), ("Auxiliary Drive", 10),
                                                      ("Hunter-Killer Missile", 10, 2), ("Armoured Ceramite", 20),
                                                      ("Flare Shield", 25)]),
                         take(t, "Pintle-mounted Weapon", [("Multi-laser", 10), ("Heavy Flamer", 10)], max_total=1),
                         top_working_order(t, flare=False)])


def arvus():
    t = T["Auxilia Arvus Lighter"]
    gid = uid("grp", t, "weapon")
    weapon = group(gid, "Weapon (one)", constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)],
                   links=[link(uid("link", gid, n), W(n), n, cost=p) for n, p in [
                       ("Multi-laser", 10), ("Autocannon", 10), ("Lascannon", 20), ("Twin-linked Multi-laser", 15),
                       ("Twin-linked Autocannon", 15), ("Twin-linked Lascannon", 25)]],
                   entries=[inline(t, "Two Hellstrike Missiles", 20, ["Hellstrike Missile", "Hellstrike Missile"])])
    return entry(t, "Auxilia Arvus Lighter", typ="unit", cost=75,
                 cats=[foc(gs.CAT_TRANSPORT, "Dedicated Transport", t)],
                 profiles=[vehicle_profile(t, "Arvus Lighter", "Vehicle (Flyer, Hover, Transport)", 3, 11, 11, 10),
                           transport_profile(t, "Arvus Lighter", "12 models", "One rear access hatch", "None")],
                 infolinks=rules_links(["Deep Strike"], key=t),
                 groups=[take(t, "Upgrades", [("Chaff Launcher", 10), ("Armoured Cockpit", 15), ("Illum Flares", 5),
                                              ("Searchlight", 1), ("Extra Armour", 10), ("Flare Shield", 20)]),
                         weapon, top_working_order(t, flare=False)])


def hades():
    t = T["Hades Breaching Drill"]
    return entry(t, "Hades Breaching Drill", typ="unit", cost=100,
                 cats=[foc(gs.CAT_TRANSPORT, "Dedicated Transport", t)],
                 profiles=[unit_profile(t, "Hades Breaching Drill", "Monstrous Creature", 2, "-", 8, 7, 3, 1, 1, 8,
                                        "3+")],
                 infolinks=rules_links(["Hades Breaching Drill", "Deep Strike", "Extremely Bulky",
                                        "Terrestrial Eruption", "Tunnelling", "Tunnelling Assault", "Void Hardened"],
                                       key=t),
                 links=[gear(t, "Melta-cutter Drill")],
                 mods=[modifier("add", "error", "Infantry Cohort: the Detachment may not include Hades Breaching Drills.",
                                conds=[doc("Infantry Cohort")])])


# ==================================================================================================  FAST ATTACK
def tarantulas():
    u = IDS["tarantula"]
    hyp_title = "Hyperios Air-defence Missile Launchers (entire Battery, instead)"
    hyp_id = uid("choice", u, hyp_title, "Hyperios Air-defence Missile Launchers")
    tid = uid("model", u, "Tarantula Sentry Gun")
    m = model(u, "Tarantula Sentry Gun", 1, 3, 30,
              unit_profile(u, "Tarantula Sentry Gun", "Artillery (Immobile)", "-", 3, "-", 6, 2, "-", "-", "-", "3+"),
              groups=[slot(tid, "Replace Twin-linked Heavy Bolter", "Twin-linked Heavy Bolter", [
                  ("Twin-linked Multi-laser", 0), ("Twin-linked Heavy Flamer", 0),
                  (inline(tid, "Two Twin-linked Rotor Cannons", 0, ["Twin-linked Rotor Cannon"] * 2), None),
                  (inline(tid, "Multi-melta and Searchlight", 5, ["Multi-melta", "Searchlight"]), None),
                  ("Twin-linked Lascannon", 10)], zero_if=[has(hyp_id, u)])])
    hyp = choice(u, hyp_title, [("Hyperios Air-defence Missile Launchers", 20, True,
                                 ["Hyperios Air-defence Missile Launcher"], [])], unit_id=u)
    deploy = choice(u, "Battery Deployment (entire Battery, one)", [
        ("Forward Deployment", 5, True, [], ["Tarantula: Forward Deployment", "Scout"]),
        ("Concealment", 10, True, [], ["Tarantula: Concealment", "Stealth"]),
        ("Drop Capsules", 20, True, [], ["Tarantula: Drop Capsules", "Deep Strike"])], unit_id=u)
    mode = flat_choice(u, "Firing Mode (entire Battery)", [("Point Defence", 0, [], []), ("Sentry", 0, [], [])],
                       required=True, default="Point Defence")
    return unit("Tarantula Sentry Gun Battery", 0, FA, "Fast Attack", key=u, models=numbered(m, 3, 1),
                rules_=["Automated Artillery", "Firing Modes"], groups=[hyp, deploy, mode],
                mods=forbid_error("Tarantula Sentry Gun Batteries", u,
                                  ["Infantry Cohort", "Armoured Cohort", "Reconnaissance Cohort"]))


def count_error(u, text, lo, hi):
    return modifier("add", "error", text, groups=[any_of(cond("model", u, "lessThan", lo),
                                                         cond("model", u, "greaterThan", hi))])


def squadron_prime(u):
    eid = uid(u, "squadron-prime")
    e = entry(eid, "Squadron Prime (Armoured Cohort, one vehicle: BS4)", cost=25,
              constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
              mods=[modifier("set", "hidden", "true", groups=[any_of(nodoc("Armoured Cohort"),
                                                                     cond("model", u, "lessThan", 3))]),
                    modifier("set", uid(eid, "max"), 0, groups=[any_of(nodoc("Armoured Cohort"),
                                                                       cond("model", u, "lessThan", 3))])],
              rules=[rule(uid(eid, "r"), "Squadron Prime", "Armoured Cohort - Armoured Command: a Squadron containing "
                     "three vehicles may upgrade one vehicle to a Squadron Prime. A Squadron Prime has Ballistic "
                     "Skill 4.")])
    return e


def leman_russ_squadron(u, name, variants, rear, rules_, kit, cat_id, cat_name):
    models = []
    for vname, cost, main in variants:
        mid = uid("model", u, vname)
        groups = [slot(mid, "Replace Hull-mounted Heavy Bolter", "Heavy Bolter",
                       [("Multi-laser", 0), ("Heavy Flamer", 0), ("Lascannon", 10)]),
                  take(mid, "Vehicle Upgrades", [("Dozer Blade", 5), ("Hunter-Killer Missile", 10),
                                                 ("Extra Armour", 10), ("Armoured Ceramite", 20)]),
                  take(mid, "Pintle-mounted Weapon", [("Multi-laser", 10), ("Heavy Flamer", 10)], max_total=1),
                  top_working_order(mid)]
        m = model(u, vname, 0, 3, cost, vehicle_profile(u, vname, "Vehicle (Tank)", 3, 14, 13, rear),
                  kit=[main, *kit], groups=groups)
        models += numbered(m, 3, 0)
    return models


def lr_strike():
    u = IDS["lr_strike"]
    variants = [("Leman Russ Battle Tank", 175, "Battle Cannon"),
                ("Leman Russ Exterminator", 170, "Exterminator Autocannon"),
                ("Leman Russ Annihilator", 170, "Twin-linked Lascannon"),
                ("Leman Russ Vanquisher", 175, "Vanquisher Battle Cannon")]
    models = leman_russ_squadron(u, "Auxilia Leman Russ Strike Squadron", variants, 10, [],
                                 ["Searchlight", "Smoke Launchers", "Auxiliary Drive", "Induction Charger"], FA,
                                 "Fast Attack")
    return unit("Auxilia Leman Russ Strike Squadron", 0, FA, "Fast Attack", key=u, compulsory=False,
                models=models, entries=[squadron_prime(u)],
                rules_=["Explorator Adaption", "Outflank", "Induction Charger"],
                mods=[count_error(u, "A Leman Russ Strike Squadron contains one to three Auxilia Leman Russ.", 1, 3),
                      *move_role(TROOPS, FA, "Armoured Cohort", line="add")])


def sentinels():
    u = IDS["sentinels"]
    vc = uid("squadwide", u, "Veletaris Crew (entire Squadron)")
    mid = uid("model", u, "Armoured Sentinel")
    prof = walker_profile(u, "Armoured Sentinel", 3, 3, 5, 12, 11, 10, 3, 1)
    set_stats(prof, "Walker", {"BS": 4}, [cond(vc, u, "atLeast", 1)])
    m = model(u, "Armoured Sentinel", 2, 5, 40, prof, kit=["Searchlight", "Smoke Launchers"],
              groups=[slot(mid, "Replace Multi-laser", "Multi-laser", [
                  ("Heavy Flamer", 0), ("Autocannon", 5), ("Missile Launcher", 5), ("Multi-melta", 10),
                  ("Volkite Culverin", 15), ("Plasma Cannon", 15), ("Lascannon", 20)]),
                  take(mid, "Upgrades", [("Hunter-Killer Missile", 5), ("Lascutter", 5)]),
                  top_working_order(mid)])
    crew = per_model(u, "Veletaris Crew (entire Squadron)", 10, u, [])
    add_to(crew, "infoLinks", rules_links(["Veletaris Crew"], key=vc))
    return unit("Armoured Sentinel Squadron", 0, FA, "Fast Attack", key=u, models=numbered(m, 5, 2),
                entries=[crew, squadron_prime(u)], rules_=["Scout"])


def lykis_section():
    u = IDS["lykis"]
    pid = uid("model", u, "Prime")
    prime = model(u, "Prime", 1, 1, 0,
                  unit_profile(u, "Prime", "Jet Pack Infantry (Character)", 4, 4, 3, 3, 1, 3, 2, 9, "4+"),
                  kit=["Reinforced Void Armour", "Jet Pack", "Volkite Charger", "Frag Grenades", "Krak Grenades"],
                  groups=[*sgt_slots(pid), take(pid, "Prime Wargear", [("Melta Bombs", 5)])])
    lyk = model(u, "Lykii", 9, 9, 0, unit_profile(u, "Lykii", "Jet Pack Infantry", 3, 4, 3, 3, 1, 3, 1, 8, "4+"),
                kit=["Reinforced Void Armour", "Jet Pack", "Volkite Charger", "Laspistol", "Close Combat Weapon",
                     "Frag Grenades", "Krak Grenades"])
    weapons = flat_choice(u, "Lykii: replace Volkite Chargers (all Lykii; the Prime may match)", [
        ("Rending Weapons (Lykii)", 36, ["Rending Weapon"], []),
        ("Rending Weapons (Lykii and Prime)", 40, ["Rending Weapon"], []),
        ("Power Weapons (Lykii)", 45, ["Power Weapon"], []),
        ("Power Weapons (Lykii and Prime)", 50, ["Power Weapon"], [])])
    return unit("Lykis Maelstrom Section", 165, FA, "Fast Attack", key=u, models=[prime, lyk],
                rules_=[*CORE_RULES, "Jet Pack"],
                groups=[weapons, take(u, "Section Equipment (one Lykii)", [("Nuncio-vox", 10)])],
                mods=[*move_role(ELITES, FA, "Veletaris Assault Cohort"),
                      *forbid_error("Lykis Maelstrom Sections", u, ["Infantry Cohort"]),
                      doc_error("Void & Siege Cohort", "no more than one Lykis Maelstrom Section may be selected.",
                                conds=[cond(u, "force", "atLeast", 2)])])


# ==================================================================================================  HEAVY SUPPORT
def epostremis():
    u = IDS["epostremis"]
    pid = uid("model", u, "Prime")
    kit = ["Void-Hardened Power Armour", "Dual Rotor Cannon", "Close Combat Weapon", "Heavy Stabilisers"]
    prime = model(u, "Prime", 1, 1, 0, unit_profile(u, "Prime", "Infantry (Character)", 4, 4, 4, 3, 1, 2, 2, 9, "3+"),
                  kit=kit, groups=[take(pid, "Prime Wargear", [("Nuncio-vox", 10)])])
    ep = model(u, "Epostremii", 4, 9, 20, unit_profile(u, "Epostremii", "Infantry", 3, 4, 4, 3, 1, 2, 1, 8, "3+"),
               kit=kit)
    weapons = choice(u, "Replace Dual Rotor Cannons (all models, Prime identical)", [
        (n, p, True, [n], []) for n, p in [("Multi-laser", 0), ("Heavy Flamer", 0),
                                           ("Solar Auxilia Grenade Launcher", 10), ("Multi-melta", 10),
                                           ("Volkite Culverin", 10), ("Lascannon", 20)]], unit_id=u)
    return unit("Epostremis Thunder Section", 135 - 4 * 20, HS, "Heavy Support", key=u, models=[prime, ep],
                rules_=[*CORE_RULES, "Bulky"], groups=[weapons])


def lr_assault():
    u = IDS["lr_assault"]
    variants = [("Leman Russ Demolisher", 195, "Demolisher Cannon"),
                ("Leman Russ Incinerator", 185, "Twin-linked Volkite Demi-culverin"),
                ("Leman Russ Executioner", 200, "Executioner Plasma Cannon")]
    models = leman_russ_squadron(u, "Auxilia Leman Russ Assault Squadron", variants, 11, [],
                                 ["Searchlight", "Smoke Launchers", "Auxiliary Drive"], HS, "Heavy Support")
    return unit("Auxilia Leman Russ Assault Squadron", 0, HS, "Heavy Support", key=u, models=models,
                entries=[squadron_prime(u)], rules_=["Explorator Adaption", "Co-ordinated Fire Protocols"],
                mods=[count_error(u, "A Leman Russ Assault Squadron contains one to three Auxilia Leman Russ.", 1, 3),
                      *move_role(ELITES, HS, "Armoured Cohort")])


def artillery_battery():
    u = IDS["artillery"]
    data = [("Auxilia Basilisk", 160, "Earthshaker Cannon"), ("Auxilia Medusa", 175, "Medusa Siege Gun"),
            ("Auxilia Bombard", 180, "Colossus Bombard")]
    ids = [uid("model", u, n) for n, *_ in data]
    models = []
    for (n, cost, main), mid in zip(data, ids):
        others = [cond(c, u, "atLeast", 1) for o in ids if o != mid for c in [o] + [uid(o, "copy", i) for i in (2, 3)]]
        groups = [take(mid, "Pintle-mounted Weapon", [("Heavy Bolter", 10), ("Heavy Flamer", 10), ("Multi-laser", 10)],
                       max_total=1),
                  take(mid, "Vehicle Upgrades", [("Dozer Blade", 5), ("Auxiliary Drive", 10), ("Extra Armour", 10),
                                                 ("Hunter-Killer Missile", 10), ("Armoured Ceramite", 20)]),
                  top_working_order(mid)]
        if n == "Auxilia Bombard":
            groups.insert(0, take(mid, "Ammunition", [("Seismic Shock Shells", 25)]))
        m = model(u, n, 0, 3, cost, vehicle_profile(u, n, "Vehicle (Tank)", 3, 13, 12, 10),
                  kit=[main, "Searchlight", "Smoke Launchers"], groups=groups,
                  mods=[modifier("set", "hidden", "true", groups=[any_of(*others)]),
                        modifier("set", uid(mid, "max"), 0, groups=[any_of(*others)])])
        models += numbered(m, 3, 0)
    tog = uid(u, "siege-train")
    toggle = gate(entry(tog, "Selected as Elites (Void & Siege Cohort - Siege Train)",
                        constraints=[constraint(uid(tog, "max"), "max", 1, auto=True)]),
                  "Void & Siege Cohort", uid(tog, "max"))
    return unit("Auxilia Artillery Tank Battery", 0, HS, "Heavy Support", key=u, models=models,
                entries=[toggle, squadron_prime(u)], rules_=["Explorator Adaption"],
                mods=[count_error(u, "An Artillery Tank Battery contains one to three tanks, all of the same type.",
                                  1, 3),
                      modifier("set-primary", "category", ELITES, conds=[cond(tog, "self", "atLeast", 1)]),
                      modifier("remove", "category", HS, conds=[cond(tog, "self", "atLeast", 1)]),
                      *forbid_error("Auxilia Artillery Tank Batteries", u, ["Veletaris Assault Cohort"])])


def sponsons(key, default, opts):
    """'Exchange both sponson-mounted X for ...' as one slot of inline pair entries."""
    d = inline(key, f"Two sponson-mounted {default}s", 0, [default, default])
    return slot(key, f"Replace both sponson-mounted {default}s", None,
                [(inline(key, f"Two {n}s", p, [n, n]), None) for n, p in opts], default_is_entry=d)


def malcador():
    u = IDS["malcador"]
    prof = vehicle_profile(u, "Malcador Heavy Tank", "Vehicle (Tank, Fast)", 3, 13, 13, 12)
    set_stats(prof, "Vehicle", {"Front": 14, "Unit Type": "Vehicle (Tank)"}, [has(W("Siege Armour"), u)])
    return unit("Auxilia Malcador Heavy Tank", 235, HS, "Heavy Support", key=u, profiles=[prof],
                kit=["Searchlight", "Smoke Launchers"], rules_=["Explorator Adaption"],
                groups=[slot(u, "Replace Traverse-mounted Battle Cannon", "Battle Cannon",
                             [("Twin-linked Lascannon", 0)]),
                        slot(u, "Replace Hull-mounted Autocannon", "Autocannon",
                             [("Multi-laser", 0), ("Heavy Flamer", 0), ("Lascannon", 10), ("Demolisher Cannon", 30)]),
                        sponsons(u, "Autocannon", [("Multi-laser", 0), ("Heavy Flamer", 0), ("Lascannon", 20)]),
                        take(u, "Vehicle Upgrades", [("Dozer Blade", 5), ("Auxiliary Drive", 10), ("Siege Armour", 10),
                                                     ("Hunter-Killer Missile", 10, 2), ("Armoured Ceramite", 20),
                                                     ("Flare Shield", 25)]),
                        take(u, "Pintle-mounted Weapon", [("Multi-laser", 10), ("Heavy Flamer", 10)], max_total=1),
                        top_working_order(u, flare=False)])


def infernus():
    u = IDS["infernus"]
    return unit("Auxilia Malcador Infernus", 265, HS, "Heavy Support", key=u,
                profiles=[vehicle_profile(u, "Malcador Infernus", "Vehicle (Tank)", 3, 13, 12, 11)],
                kit=["Inferno Gun", "Searchlight", "Smoke Launchers"],
                rules_=["Explorator Adaption", "Highly Flammable"],
                groups=[sponsons(u, "Autocannon", [("Multi-laser", 0), ("Heavy Flamer", 0), ("Lascannon", 20)]),
                        take(u, "Vehicle Upgrades", [("Auxiliary Drive", 10), ("Armoured Ceramite", 20)]),
                        take(u, "Pintle-mounted Weapon", [("Multi-laser", 10), ("Heavy Flamer", 10)], max_total=1),
                        take(u, "Inferno Gun Ammunition", [("Chemical Ammunition", 25)]),
                        top_working_order(u)])


def valdor():
    u = IDS["valdor"]
    return unit("Auxilia Valdor Tank Hunter", 300, HS, "Heavy Support", key=u,
                profiles=[vehicle_profile(u, "Valdor Tank Hunter", "Vehicle (Tank)", 3, 13, 12, 11)],
                kit=["Neutron Beam Laser", "Searchlight", "Smoke Launchers"],
                rules_=["Explorator Adaption", "Dangerous Reactor Core"],
                groups=[slot(u, "Replace sponson-mounted Autocannon", "Autocannon",
                             [("Multi-laser", 0), ("Heavy Flamer", 0), ("Lascannon", 10)]),
                        take(u, "Vehicle Upgrades", [("Auxiliary Drive", 10), ("Armoured Ceramite", 20)]),
                        take(u, "Pintle-mounted Weapon", [("Multi-laser", 10), ("Heavy Flamer", 10)], max_total=1),
                        top_working_order(u)])


def cyclops():
    u = IDS["cyclops"]
    m = model(u, "Cyclops", 1, 5, 70, unit_profile(u, "Cyclops", "Infantry (Special)", "-", "-", "-", 6, 2, "-", "-",
                                                    "-", "4+"),
              kit=["Cyclops Demolition Charge"])
    title = "Replace Demolition Charges (all Cyclops)"
    payload = choice(u, title, [("Incineration Charges", 10, True, ["Cyclops Incineration Charge"], []),
                                ("Atomantic Imploders (Lord Marshal)", 50, True, ["Atomantic Imploder"], [])],
                     unit_id=u)
    ai = uid("choice", u, title, "Atomantic Imploders (Lord Marshal)")
    for e in payload.iter("selectionEntry"):
        if e.get("id") == ai:
            no_lm = [cond(IDS["lord_marshal"], "roster", "lessThan", 1)]
            add_mods(e, [modifier("set", "hidden", "true", conds=no_lm),
                         modifier("set", uid(ai, "max"), 0, conds=no_lm)])
    return unit("0-1 Cyclops Remote Demolitions Unit", 0, HS, "Heavy Support", key=u, models=[m],
                rules_=["Extremely Bulky", "Fearless", "Remote Control", "Detonation"], groups=[payload],
                constraints=[unique(u, 1, "force")])


# ==================================================================================================  CONFIG
def doctrine_config():
    cfg, ids = config("doctrine", "Cohort Doctrine", [(n, [n]) for n in DOCTRINES], required=True,
                      default="Standard Cohort")
    i = IDS
    errs = {
        "Infantry Cohort": [
            doc_error("Infantry Cohort", "the Detachment must contain at least two Auxilia Infantry Tercios.",
                      conds=[cond(i["tercio"], "force", "lessThan", 2)]),
            doc_error("Infantry Cohort", "no more than one Vehicle Squadron selected from Fast Attack.",
                      groups=[sum_ge2([i["lr_strike"], i["sentinels"], i["tarantula"]])]),
            doc_error("Infantry Cohort", "no more than one Vehicle Squadron selected from Heavy Support.",
                      groups=[sum_ge2([i["lr_assault"], i["artillery"], i["malcador"], i["infernus"],
                                              i["valdor"]])]),
        ],
        "Armoured Cohort": [
            doc_error("Armoured Cohort", "at least two Auxilia Leman Russ Strike Squadrons must be selected.",
                      conds=[cond(i["lr_strike"], "force", "lessThan", 2)]),
            doc_error("Armoured Cohort", "an Auxilia Tank Commander must be the army's Warlord.",
                      conds=[cond(i["tank_cmd"], "force", "lessThan", 1)]),
            doc_error("Armoured Cohort", "the Detachment may not include Fortifications.",
                      conds=[cond(FORT, "force", "atLeast", 1)]),
        ],
        "Reconnaissance Cohort": [
            doc_error("Reconnaissance Cohort", "the Detachment must contain at least one Achmiris Recon Section.",
                      groups=[all_of(*[cond(x, "force", "lessThan", 1) for x in
                                       [i["ach_fa"], i["ach_t"], i["ach_ret"]]])]),
        ],
        "Veletaris Assault Cohort": [
            doc_error("Veletaris Assault Cohort", "the Detachment must contain at least two Veletaris Storm Sections.",
                      groups=[or_groups(all_of(cond(i["vel"], "force", "equalTo", 0),
                                               cond(i["vel_hh"], "force", "lessThan", 2)),
                                        all_of(cond(i["vel"], "force", "equalTo", 1),
                                               cond(i["vel_hh"], "force", "equalTo", 0)))]),
        ],
        "Void & Siege Cohort": [
            doc_error("Void & Siege Cohort", "the Detachment must contain at least one Eidis Engineer Section.",
                      groups=[all_of(cond(i["eid_el"], "force", "lessThan", 1),
                                     cond(i["eid_t"], "force", "lessThan", 1))]),
            doc_error("Void & Siege Cohort", "the Detachment must contain at least one Auxilia Infantry Tercio.",
                      conds=[cond(i["tercio"], "force", "lessThan", 1)]),
            doc_error("Void & Siege Cohort", "no more than one Achmiris Recon Section may be selected.",
                      groups=[sum_ge2([i["ach_fa"], i["ach_t"]])]),
            doc_error("Void & Siege Cohort", "only one Eidis Engineer Section may take Breaching Charges for free.",
                      groups=[sum_ge2(i["eidis_bc"])]),
        ],
    }
    for e in cfg.iter("selectionEntry"):
        for n, mods in errs.items():
            if e.get("id") == ids[n]:
                add_mods(e, mods)
    return cfg


# ==================================================================================================  BUILD
def build():
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS_, multi_profile=MULTI, weapon_rules=WEAPON_RULES, wargear=WARGEAR_)
    L._PSY_REGISTERED.clear()  # start() emptied the rule tables: let psychic_powers() register the powers again
    dk = k("cfg", "doctrine")
    DOC.update({n: uid(dk, n) for n in DOCTRINES})
    T.update({n: k("transport", n) for n in ["Dracosan Armoured Transport", "Auxilia Arvus Lighter",
                                              "Hades Breaching Drill"]})
    IDS.clear()
    IDS.update({
        "legate": k("unit", "Legate Commander"), "lord_marshal": k("upgrade", "Lord Marshal"),
        "tcs": k("unit", "Auxilia Tactical Command Section"), "tank_cmd": k("unit", "Auxilia Tank Commander"),
        "lifeward": k("retinue", "Life Ward Retinue"), "attaches": k("attaches", "Cohort Attaches"),
        "masade": k("unit", "Ireton MaSade"), "jovan": k("unit", "Aevos Jovan"),
        "medicae": k("unit", "Auxilia Medicae Detachment"), "rapier": k("unit", "Auxilia Rapier Battery"),
        "ogryns": k("unit", "Auxilia Ogryn Charonite Squad"), "enginseer": k("unit", "Enginseer Auxilia"),
        "eid_el": k("unit", "Eidis Engineer Section"), "eid_t": k("section", "Eidis Engineer Section"),
        "tercio": k("unit", "Auxilia Infantry Tercio"), "las": k("section", "Auxilia Lasrifle Section"),
        "vel": k("section", "Veletaris Storm Section"), "flamer": k("section", "Auxilia Flamer Section"),
        "vel_hh": k("unit", "Veletaris Storm Section (Household Retinue)"),
        "troop_master": k("upgrade", "Troop Master"), "vaskale": k("upgrade", "Vaskale Solar"),
        "ach_fa": k("unit", "Achmiris Recon Section"), "ach_t": k("section", "Achmiris Recon Section"),
        "ach_ret": k("retinue", "Achmiris Recon Section"),
        "tarantula": k("unit", "Tarantula Sentry Gun Battery"), "lr_strike": k("unit", "Leman Russ Strike Squadron"),
        "sentinels": k("unit", "Armoured Sentinel Squadron"), "lykis": k("unit", "Lykis Maelstrom Section"),
        "epostremis": k("unit", "Epostremis Thunder Section"), "lr_assault": k("unit", "Leman Russ Assault Squadron"),
        "artillery": k("unit", "Auxilia Artillery Tank Battery"), "malcador": k("unit", "Auxilia Malcador Heavy Tank"),
        "infernus": k("unit", "Auxilia Malcador Infernus"), "valdor": k("unit", "Auxilia Valdor Tank Hunter"),
        "cyclops": k("unit", "Cyclops Remote Demolitions Unit"),
    })
    # Eidis sections first: they register their free Breaching Charge ids used by the Doctrine errors
    eidis_el = eidis_section(IDS["eid_el"], tercio=False)
    eidis_t = eidis_section(IDS["eid_t"], tercio=True)
    army_rules = entry(k("cfg", "army rules"), "Solar Auxilia Army Rules",
                       cats=[category_link(gs.CAT_CONFIG, "Configuration", primary=True, key=k("cfg", "army rules"))],
                       constraints=[constraint(k("cfg", "army rules", "max"), "max", 1, scope="force", deep=True)],
                       infolinks=rules_links(["Solar Auxilia Army", "The Army's Warlord", "Cohort Doctrines",
                                              *CORE_RULES, "Hold the Line", "Disciplined Command", "High Command",
                                              "Support Officer", "Support Section", "Retinue", "Explorator Adaption"],
                                             key="armyrules"))
    units = [
        allegiance(), doctrine_config(), army_rules,
        # HQ
        legate_commander(), tactical_command_section(), tank_commander(), ireton_masade(),
        # Elites
        medicae_detachment(), rapier_battery(), ogryn_charonites(), enginseer_auxilia(), eidis_el,
        veletaris_section(IDS["vel_hh"], household=True), aevos_jovan(),
        # Troops
        infantry_tercio(),
        # Fast Attack
        tarantulas(), lr_strike(), sentinels(), achmiris_section(IDS["ach_fa"], "fa"), lykis_section(),
        # Heavy Support
        epostremis(), lr_assault(), artillery_battery(), malcador(), infernus(), valdor(), cyclops(),
    ]
    # Reconnaissance Cohort restrictions on the Achmiris FA entry
    ach_fa = units[-9]
    add_mods(ach_fa, [doc_error("Void & Siege Cohort", "no more than one Achmiris Recon Section may be selected.",
                                conds=[cond(IDS["ach_fa"], "force", "atLeast", 2)])])
    shared = [
        lasrifle_section(), veletaris_section(IDS["vel"], household=False), flamer_section(),
        achmiris_section(IDS["ach_t"], "tercio"), achmiris_section(IDS["ach_ret"], "retinue"), eidis_t,
        life_ward_retinue(), cohort_attaches(),
        dracosan(), arvus(), hades(),
    ]
    root = catalogue(ARMY, units, shared)
    mechanicum_liaison_units(root)
    return root


def mechanicum_liaison_units(root):
    """Mechanicum Liaison (author): a Detachment with a Mechanicum Liaison Adept may include Thallax Cohorts and Castellax
    Battle-automata Maniples, in their Mechanicum slots (Troops). The units are linked from the Mechanicum catalogue
    (catalogueLink), so they stay exactly as in the Mechanicum list."""
    mech = "Mechanicum"
    liaison = uid("model", IDS["attaches"], "Mechanicum Liaison Adept")
    root.insert(0, wrap("catalogueLinks", [el("catalogueLink", {
        "id": k("catlink", mech), "name": mech, "targetId": uid(mech, "catalogue"), "type": "catalogue",
        "importRootEntries": "false"})]))
    links = []
    for n in ("Thallax Cohort", "Castellax Class Battle-Automata Maniple"):
        lid = k("link", "liaison", n)
        links.append(link(lid, uid(mech, "unit", n), f"{n} (Mechanicum Liaison)",
                          mods=[modifier("set", "hidden", "true", conds=[cond(liaison, "force", "lessThan", 1)]),
                                modifier("add", "error", f"{n}: only a Solar Auxilia Detachment containing a Mechanicum "
                                                         "Liaison Adept may include it.",
                                         conds=[cond(liaison, "force", "lessThan", 1)])]))
    root.find("entryLinks").extend(links)
