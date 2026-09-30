"""Shared weapon & wargear data for the Legiones Astartes army list.

Profiles and rule texts are taken from the Legiones Astartes Army List
(Armoury and Additional Rules section).
"""

# name: (range, strength, ap, type)
WEAPON_PROFILES = {
    "Bolt Pistol": ('12"', "4", "5", "Pistol"),
    "Bolter": ('24"', "4", "5", "Rapid Fire"),
    "Combi-Bolter": ('24"', "4", "5", "Rapid Fire, Twin-linked"),
    "Foeblaster Boltgun": ('18"', "5", "4", "Rapid Fire, Twin-linked"),
    "Heavy Bolter": ('36"', "5", "4", "Heavy 3"),
    "Heavy Bolter - Hellfire Round": ('36"', "5", "4", "Heavy 1, Blast, Hellfire"),
    "Astartes Shotgun": ('12"', "3", "-", "Assault 2"),
    "Storm Bolter": ('24"', "4", "5", "Assault 2"),
    "Twin-linked Bolter": ('24"', "4", "5", "Rapid Fire, Twin-linked"),
    "Flamer": ("Template", "4", "5", "Assault 1"),
    "Hand Flamer": ("Template", "3", "6", "Pistol"),
    "Heavy Flamer": ("Template", "5", "4", "Assault 1"),
    "Plasma Cannon": ('36"', "7", "2", "Heavy 1, Blast, Gets Hot"),
    "Plasma Gun": ('24"', "7", "2", "Rapid Fire, Gets Hot"),
    "Plasma Pistol": ('12"', "7", "2", "Pistol, Gets Hot"),
    "Meltagun": ('12"', "8", "1", "Assault 1, Melta"),
    "Multi-Melta": ('24"', "8", "1", "Heavy 1, Melta"),
    "Volkite Caliver": ('30"', "6", "5", "Heavy 2, Rending"),
    "Volkite Charger": ('15"', "5", "5", "Assault 2, Rending"),
    "Volkite Serpenta": ('10"', "5", "5", "Pistol, Rending"),
    "Graviton Gun": ('18"', "Special", "4", "Heavy 1, Blast, Concussive, Graviton"),
    "Autocannon": ('48"', "7", "4", "Heavy 2"),
    "Rotor Cannon": ('30"', "3", "6", "Salvo 3/4"),
    "Lascannon": ('48"', "9", "2", "Heavy 1"),
    "Grenade Launcher - Frag": ('24"', "3", "6", "Assault 1, Blast"),
    "Grenade Launcher - Krak": ('24"', "6", "4", "Assault 1"),
    "Hunter-Killer Missile": ("Unlimited", "8", "3", "Heavy 1, One Use"),
    "Missile Launcher - Frag": ('48"', "4", "6", "Heavy 1, Blast"),
    "Missile Launcher - Krak": ('48"', "8", "3", "Heavy 1"),
    "Deathwind Missile Launcher": ('12"', "5", "-", "Heavy 1, Large Blast"),
    "Sniper Rifle": ('36"', "3", "6", "Heavy 1, Sniper"),
    "Grenade Harness": ('8"', "3", "-", "Assault 2, Blast, One Use"),
    "Chainaxe": ("-", "User", "-", "Chainaxe"),
    "Chainfist": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Armourbane"),
    "Chainsword": ("-", "User", "-", "Close Combat Weapon"),
    "Close Combat Weapon": ("-", "User", "-", "Close Combat Weapon"),
    "Combat Blade": ("-", "User", "-", "Close Combat Weapon"),
    "Force Weapon": ("-", "User", "-", "Power Weapon, Force"),
    "Lightning Claw": ("-", "User", "-", "Power Weapon, re-roll failed To Wound rolls, Specialist Weapon"),
    "Pair of Lightning Claws": ("-", "User", "-",
                                "Power Weapon, re-roll failed To Wound rolls, Specialist Weapon, +1 Attack"),
    "Power Fist": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon"),
    "Power Weapon": ("-", "User", "-", "Ignores Armour Saves"),
    "Relic Blade": ("-", "6", "-", "Power Weapon, Two-Handed"),
    "Rending Weapon": ("-", "User", "-", "Rending"),
    "Thunder Hammer": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Concussive"),
    "Crozius Arcanum": ("-", "User", "-", "Power Weapon"),
    "Aether-shock Maul": ("-", "User", "-", "Power Weapon; always wounds Psykers and Daemons on a 2+"),
    "Lascutter": ("-", "9", "2", "Melee, Unwieldy, Cumbersome"),
    "Breaching Charge": ("Special", "8", "2", "Melee, Blast, One Use, Wrecker"),
    "Krak Grenade": ("-", "6", "-", "Against vehicles only: 6 + D6 Armour Penetration"),
    "Melta Bomb": ("-", "8", "-", "Against vehicles only: 8 + 2D6 Armour Penetration"),
    "Lance Strike": ("Orbital", "10", "1", "Ordnance 1, Blast"),
    "Melta Torpedo": ("Orbital", "8", "3", "Ordnance 1, Blast, Armourbane"),
    "Barrage Bomb": ("Orbital", "6", "4", "Ordnance 1, Blast"),
}

# Weapon selection entries: entry name -> list of profile names
WEAPONS = {n: [n] for n in WEAPON_PROFILES}
WEAPONS.update({
    "Missile Launcher": ["Missile Launcher - Frag", "Missile Launcher - Krak"],
    "Heavy Bolter": ["Heavy Bolter", "Heavy Bolter - Hellfire Round"],
    "Combi-Flamer": ["Bolter", "Flamer"],
    "Combi-Grenade Launcher": ["Bolter", "Grenade Launcher - Frag", "Grenade Launcher - Krak"],
    "Combi-Meltagun": ["Bolter", "Meltagun"],
    "Combi-Plasma Gun": ["Bolter", "Plasma Gun"],
    "Combi-Volkite Charger": ["Bolter", "Volkite Charger"],
    "Combi-Weapon": ["Bolter"],
    "Havoc Launcher": ["Havoc Launcher"],
    "Krak Grenades": ["Krak Grenade"],
    "Melta Bombs": ["Melta Bomb"],
    "Frag Grenades": [],
})
for n in ["Missile Launcher - Frag", "Missile Launcher - Krak", "Grenade Launcher - Frag",
          "Grenade Launcher - Krak", "Heavy Bolter - Hellfire Round", "Krak Grenade", "Melta Bomb",
          "Lance Strike", "Melta Torpedo", "Barrage Bomb"]:
    WEAPONS.pop(n)

# Rules attached to weapons (army-book weapon rules; core rules are linked by name)
WEAPON_RULES = {
    "Chainaxe": ["Chainaxe"],
    "Force Weapon": ["Force"],
    "Rending Weapon": ["Rending"],
    "Volkite Caliver": ["Rending"], "Volkite Charger": ["Rending"], "Volkite Serpenta": ["Rending"],
    "Graviton Gun": ["Graviton", "Concussive"],
    "Combi-Flamer": ["Combi-Weapon"], "Combi-Grenade Launcher": ["Combi-Weapon"],
    "Combi-Meltagun": ["Combi-Weapon", "Melta"], "Combi-Plasma Gun": ["Combi-Weapon", "Gets Hot"],
    "Combi-Volkite Charger": ["Combi-Weapon", "Rending"], "Combi-Weapon": ["Combi-Weapon"],
    "Meltagun": ["Melta"], "Multi-Melta": ["Melta"],
    "Plasma Gun": ["Gets Hot"], "Plasma Pistol": ["Gets Hot"], "Plasma Cannon": ["Gets Hot"],
    "Sniper Rifle": ["Sniper"], "Thunder Hammer": ["Unwieldy", "Concussive"],
    "Power Fist": ["Unwieldy"], "Chainfist": ["Unwieldy", "Armourbane"],
    "Lascutter": ["Unwieldy", "Cumbersome"], "Breaching Charge": ["Breaching Charge", "Wrecker"],
    "Relic Blade": ["Two-Handed"], "Heavy Bolter": ["Hellfire"],
    "Twin-linked Bolter": ["Twin-Linked"], "Combi-Bolter": ["Twin-Linked"],
    "Foeblaster Boltgun": ["Twin-Linked"], "Hunter-Killer Missile": ["Hunter-Killer Missile"],
}

# Army-book rules (name -> text). Core ProHammer rules live in the game system.
ARMY_RULES = {
    "Legiones Astartes": (
        "All models with this special rule also have the And They Shall Know No Fear special rule as presented in "
        "ProHammer Classic. They are not Fearless, though, and lose that bonus.\n"
        "In addition, each model possesses a named version of the Legiones Astartes special rule corresponding to its "
        "Legion, such as Legiones Astartes (Sons of Horus). A model may only ever possess one named version. Models "
        "with a named Legiones Astartes special rule gain any additional rules associated with that Legion (see "
        "Forces of the Legions).\nUnless specifically stated otherwise, vehicles do not have this special rule."),
    "Master of the Legion": (
        "RITES OF WAR: If the army contains a model with this rule, its Detachment may make use of a single Rite of "
        "War for which it qualifies.\nLIMITATION: A Legiones Astartes army may include no more than one model with the "
        "Master of the Legion special rule for every full 1,000 points in the army.\nRETINUE: A model with this rule may "
        "select a Legion Command Squad as a retinue where permitted (or a Terminator Command Squad if in Terminator "
        "Armour). They occupy a single HQ selection."),
    "Legion Support Officer": (
        "A model with this special rule may not be selected to fulfil the compulsory HQ selection of a Detachment. It "
        "may still be selected as an additional HQ choice. A Legion-specific rule or Rite of War may override this."),
    "Support Squad": (
        "A unit with this special rule may be selected as a Troops choice, but may not be used to fulfil either of the "
        "army's two compulsory Troops selections. A Legion-specific rule or Rite of War may remove this restriction."),
    "Legion Consuls": (
        "A Legion Centurion may be upgraded to one Legion Consul. A Consul retains the Centurion's profile, wargear, "
        "special rules and Armoury access unless stated otherwise. Wargear granted by a Consul upgrade is included in "
        "its cost. Any restrictions listed in a Consul entry override the Centurion's normal options."),
    "Honour Guard": (
        "For each Legion Praetor included in the army, one Legion Honour Guard Squad may be selected. It does not "
        "occupy a separate Force Organisation slot."),
    "Command Retinue": (
        "A Legion Centurion may select one Legion Command Squad (or a Terminator Command Squad if in Terminator "
        "Armour). The Command Squad does not occupy a separate Force Organisation slot."),
    "Fury of the Legion": (
        "A Legion Tactical Squad may declare a Fury of the Legion attack during its Shooting phase provided that: the "
        "unit did not move during the preceding Movement phase; the unit did not arrive from Reserves, Deep Strike or "
        "disembark from a Transport during that player turn; at least five models in the unit remain armed with "
        "Bolters or Bolt pistols.\nModels armed with Bolters or Bolt pistols may fire those weapons twice (a Bolter "
        "fires 2 shots at up to 24\" or 4 shots at up to 12\"; a Bolt pistol fires 2 shots). All attacks must be at "
        "the same target.\nAfterwards the squad may not enter Overwatch, may not make Return Fire or Stand & Shoot "
        "reactions, and may not fire during its next friendly Shooting phase."),
    "Hardened Armour": (
        "Failed Armour Saves caused by Blast or Template weapons may be re-rolled. When the unit makes an Advance "
        "move, reduce the additional distance rolled by 1\". Reduce any Charge or Pursuit distance rolled by 1\". In "
        "missions using Void Hardened armour, models with Hardened Armour count as Void Hardened. These movement "
        "penalties also apply to a model in Artificer Armour that is part of a Breacher Squad."),
    "Cumbersome": (
        "A model attacking with a Cumbersome weapon may make only one attack with that weapon during the Assault "
        "phase, regardless of its Attacks characteristic or any bonuses. That attack is made at Weapon Skill 1."),
    "Breaching Charge": (
        "May be used once per battle during an Assault phase instead of the bearer's normal close-combat attacks. The "
        "bearer makes a single attack against an engaged enemy unit. If it hits, place a Blast marker in base contact "
        "with the bearer covering as many enemy models as possible without covering friendly models; enemy models "
        "beneath it are hit using the Breaching Charge profile."),
    "Wrecker": (
        "When making Armour Penetration rolls against Fortifications, buildings, barricades or other immobile "
        "structures, an attack with Wrecker may re-roll a failed Armour Penetration roll. Where a mission uses a "
        "Building Damage table, add +1 to any roll made on that table by a Wrecker attack."),
    "Repair": (
        "If a Rhino is Immobilised, instead of firing any of its weapons during the Shooting phase roll a D6. On a 6, "
        "remove one Immobilised result. The vehicle may move normally from its following Movement phase."),
    "Auxiliary Drive": (
        "At the start of the controlling player's Movement phase, if the vehicle is Immobilised, roll a D6. On a 4+, "
        "remove one Immobilised result. The vehicle may move normally during that Movement phase."),
    "Drop Pod Assault": (
        "A Drop Pod and the unit transported within it must always begin the battle in Reserve. At the beginning of "
        "the first turn choose half of all friendly vehicles with this rule (rounding up); they arrive automatically "
        "that turn by Deep Strike, the rest use the normal Reserve rules. A unit which disembarks from a Drop Pod "
        "during the turn it arrives may not declare a charge that turn. When a Legion Drop Pod lands, all passengers "
        "must immediately disembark; no unit may embark upon it afterwards."),
    "Inertial Guidance System": (
        "If the vehicle would scatter onto impassable terrain or another model, reduce the scatter distance by the "
        "minimum amount required to avoid the obstacle. If no legal position is possible, resolve the Deep Strike "
        "normally."),
    "Immobile": (
        "After arriving, the Drop Pod may not move for the remainder of the battle. It counts as having suffered an "
        "Immobilised result but does not suffer any additional damage for doing so."),
    "Locator Beacon": "Friendly units arriving by Deep Strike within 6\" of a Locator Beacon do not scatter.",
    "Dreadclaw Assault": (
        "A Dreadclaw and any unit embarked within it must begin the battle in Reserve. At the beginning of the first "
        "turn roll a D6; on a 4+ the Dreadclaw becomes available. From the second turn roll for remaining Dreadclaws "
        "normally. It enters play by Deep Strike. Passengers do not immediately disembark when it lands. A unit may not "
        "charge in the turn the Dreadclaw arrived by Deep Strike."),
    "Assault Pod": (
        "Units disembarking from a Dreadclaw may charge during the same turn in which they disembark. This does not "
        "allow a charge in the turn the Dreadclaw arrived by Deep Strike."),
    "Hover Jets": (
        "After landing, the Dreadclaw remains operational. It moves as a Fast Skimmer and may transport its original "
        "passengers normally. Once its original passengers have completely disembarked, it may not embark another unit."),
    "Recon Armour": "Recon Armour confers a 4+ Armour Save.",
    "Cameleoline": "A model equipped with Cameleoline gains the Stealth special rule.",
    # Consul rules
    "Honour of the Legion": "The Chaplain and any unit he has joined have the Fearless special rule.",
    "Liturgies of Battle": (
        "In a player turn in which the Chaplain and a unit he has joined successfully charge, the Chaplain and all "
        "models in that unit may re-roll failed To Hit rolls in close combat for that Assault phase."),
    "Dual Pistols": ("A Moritat may fire both of his pistols during the Shooting phase. If he does so, he may not fire "
                     "any other weapon that phase."),
    "Lone Killer": (
        "A Moritat may not fulfil a compulsory HQ choice and may never be the army's Warlord. He may not join any unit "
        "other than a Legion Destroyer Squad. He may not benefit from beneficial psychic powers used by another model, "
        "nor use the Leadership characteristic or Leadership re-rolls provided by another friendly model."),
    "Chain Fire": (
        "When firing his pistols, the Moritat may declare a Chain Fire attack. Each successful To Hit roll immediately "
        "allows that pistol to make another shot against the same target; continue until that pistol misses (max 12 "
        "hits in total from both pistols). A Gets Hot! weapon overheats on a To Hit roll of 1; if either pistol "
        "overheats, the attack ends. Afterwards the Moritat may not charge that turn and may not shoot during his "
        "following Shooting phase."),
    "Delegated Authority": (
        "A Delegatus may possess Master of the Legion in an army of fewer than 1,000 points, overriding the normal "
        "restriction. Unless the army contains its Primarch, a Delegatus with Master of the Legion must be the army's "
        "Warlord. A detachment containing a Delegatus may not also contain a Legion Praetor. One weapon carried by the "
        "Delegatus may be made Master-crafted at no additional cost."),
    "Epistolary": "An Epistolary has Psychic Mastery Level 2.",
    "Psychic Powers (Librarian)": ("The Librarian selects psychic powers from the Psychic Power list except any form of "
                                   "Daemonology."),
    "Forbidden Lore": (
        "An Esoterist selects his psychic powers from the Sanctic Daemonology or Malefic Daemonology disciplines "
        "presented in ProHammer, regardless of his Legion or Allegiance."),
    "Battlesmith": (
        "During the Shooting phase, instead of firing a weapon, a Forge Lord in base contact with or embarked upon a "
        "friendly damaged vehicle may attempt to repair it. Roll a D6; on a 5+ (4+ with his Servo-Arm), remove one of: "
        "Engine Damaged, Weapon Destroyed, Immobilised."),
    "Lord of the Armoury": ("A Forge Lord may select equipment restricted to Techmarines from the Space Marine Armoury in "
                            "addition to the equipment normally available to a Centurion."),
    "Banner of the Aquila": (
        "Loyalist: The Herald and friendly Loyalist models with the Legiones Astartes special rule within 12\" receive "
        "+1 Weapon Skill, to a maximum of WS5."),
    "Banner of the Eye": (
        "Traitor: The Herald and friendly Traitor models with the Legiones Astartes special rule within 12\" add +1\" to "
        "Advance and Charge moves. On a turn in which such a unit successfully charges, it may re-roll To Hit rolls of "
        "1 in close combat."),
    "Fallen Honour": "If the Herald is slain, the opposing player gains +1 Victory Point in missions using Victory Points.",
    "Cognis Signum": ("The no-scatter deployment range provided by the Master of Signals' Nuncio Vox is increased from "
                      "6\" to 12\"."),
    "Targeting Matrix": "The Master of Signals also provides the normal benefits of a Signum to the unit he has joined.",
    "Orbital Bombardment": (
        "Plotting: After deployment zones are determined but before either army deploys, nominate one terrain feature "
        "as the target. Reserves: The bombardment begins the battle in Reserve (the controlling player may choose not to "
        "make its Reserve roll); once available it strikes in every subsequent friendly Shooting phase. Placement: "
        "place the Blast marker anywhere within the nominated terrain feature. Inaccuracy: resolve scatter normally; "
        "if an arrow is rolled, double the distance; if a Hit is rolled, the marker still scatters the distance rolled "
        "in the direction of the small arrow. The attack counts as an Ordnance Barrage and causes Pinning."),
    "Sacred Trust": (
        "In a mission using Victory Points, whenever a friendly Legiones Astartes Infantry or Jump Infantry unit with a "
        "model within 6\" of the Primus Medicae is completely destroyed by the enemy, roll a D6. On a 5+, gain 50 Victory "
        "Points. A unit whose Victory Points are recovered through the Reductor may not also generate Victory Points "
        "through Sacred Trust. The Primus Medicae counts as an Apothecary for selecting restricted Armoury equipment."),
    "Hexagrammic Wards": ("An enemy Psyker attempting to use a psychic power which directly targets the Primus "
                          "Nullificator or a unit he has joined suffers -1 Leadership for that Psychic test."),
    "Credo Annihilato": "The Primus Nullificator and any unit he has joined have Preferred Enemy (Daemons).",
    "Psychic Powers (Nullificator)": "A Primus Nullificator may select powers only from Sanctic Daemonology.",
    "Sabotage": (
        "After both armies have deployed but before the first game turn, nominate one enemy unit, vehicle or "
        "fortification (not an Independent Character unless part of another unit). The target suffers D6 Strength 5 "
        "AP6 hits (against the lowest Armour Value for vehicles or fortifications). Casualties do not cause Morale or "
        "Pinning tests."),
    "Special Issue Ammunition (Vigilator)": (
        "The Vigilator may use the Special Issue Ammunition profiles with his Bolter, overriding the normal restriction "
        "to Legion Seeker Squads."),
    "Cortex Designator": (
        "When the Praevian scores one or more successful To Hit rolls with a shooting weapon against an enemy unit, the "
        "Battle-Automata unit he is attached to gains Preferred Enemy against that unit until the end of the player turn."),
    "Master of Cybernetica": (
        "A Legion Praevian must be accompanied by a Castellax or Vorax Battle-Automata Maniple, purchased from the "
        "Mechanicum Army List without occupying an additional Force Organisation choice. The Praevian and the Maniple "
        "count as a single HQ selection. The Praevian must begin the battle joined to this unit and may not leave it "
        "while any Battle-Automata remain alive. The Maniple may not purchase the Paragon of Metal upgrade."),
    "Legion Inductees": (
        "Before deployment, choose one for the Praevian's Battle-Automata Maniple: the Legiones Astartes rule of the "
        "Praevian's Legion; Furious Charge; Tank Hunters; or Scout (the Praevian also gains Scout while attached)."),
    # weapon rules
    "Chainaxe": ("An Armour Save better than 4+ is reduced to 4+ against wounds caused by a Chainaxe. Armour Saves of 4+ "
                 "or worse and Invulnerable Saves are unaffected."),
    "Force": (
        "After a Psyker inflicts one or more unsaved wounds with a Force Weapon, it may take a Psychic Test. If passed, "
        "each unsaved wound becomes a Massive Wound and inflicts D3 Wounds. No additional effect against vehicles."),
    "Hellfire": ("Hellfire attacks wound non-vehicle models on a 2+ unless otherwise specified. Against vehicles, use the "
                 "weapon's normal Strength."),
    "Combi-Weapon": ("A Combi-weapon consists of a Bolter and a secondary weapon. The Bolter may be fired normally "
                     "throughout the battle. The secondary weapon may be fired once per battle. Both may not be fired in "
                     "the same Shooting phase."),
}

# Wargear (non-weapon) entries: name -> (rule text, [core rule names])
WARGEAR = {
    "Power Armour": ("A model wearing Power Armour has a 3+ Armour Save.", []),
    "Hardened Power Armour": ("Power Armour (3+ Armour Save) with the Hardened Armour special rule.", []),
    "Recon Armour": ("Recon Armour confers a 4+ Armour Save.", []),
    "Cameleoline": ("A model equipped with Cameleoline gains the Stealth special rule.", ["Stealth"]),
    "Scout Armour": ("The Vigilator gains Infiltrate and Move Through Cover.", ["Infiltrate", "Move Through Cover"]),
    "Artificer Armour": ("A model wearing Artificer Armour has a 2+ Armour Save. It does not count as Terminator Armour.",
                         []),
    "Terminator Armour": (
        "2+ Armour Save, 5+ Invulnerable Save, Relentless, Bulky. May not make Pursuit moves. May not embark upon "
        "Rhinos or Drop Pods.", ["Relentless", "Bulky"]),
    "Tartaros Terminator Armour": (
        "2+ Armour Save, 5+ Invulnerable Save, Relentless, Bulky. May make Pursuit moves normally (lost while joined by "
        "a model in another pattern of Terminator Armour). May not embark upon Rhinos or Drop Pods.",
        ["Relentless", "Bulky"]),
    "Cataphractii Terminator Armour": (
        "2+ Armour Save, 4+ Invulnerable Save, Relentless, Bulky. May not Advance, make Pursuit moves or fire Overwatch; "
        "a unit containing such a model may not Advance or Pursue. May not embark upon Rhinos or Drop Pods.",
        ["Relentless", "Bulky"]),
    "Combat Shield": ("Grants a 6+ Invulnerable Save. Does not occupy a hand and does not prevent the bonus Attack for two "
                      "weapons.", []),
    "Boarding Shield": ("Grants a 5+ Invulnerable Save. Occupies one hand; the bearer does not receive the bonus Attack for "
                        "fighting with two weapons.", []),
    "Refractor Field": (
        "Grants a 5+ Invulnerable Save. A Sergeant may only purchase a Refractor Field if his squad is purchased at its "
        "maximum starting strength. A model with a 5+ or better Invulnerable Save may not purchase one.", []),
    "Iron Halo": ("Grants a 4+ Invulnerable Save. An army may normally contain no more than one Iron Halo.", []),
    "Rosarius": ("Grants a 4+ Invulnerable Save. Does not count towards the army limit on Iron Halos.", []),
    "Frag Grenades": ("Use the normal ProHammer Frag Grenade and Assault Grenade rules. Against vehicles, Strength 4 + D6 "
                      "Armour Penetration.", []),
    "Krak Grenades": ("May exchange normal close-combat attacks for one Krak Grenade attack against a vehicle: Strength 6 "
                      "+ D6 Armour Penetration.", []),
    "Melta Bombs": ("May exchange normal close-combat attacks for one Melta Bomb attack against a vehicle: Strength 8 + "
                    "2D6 Armour Penetration.", []),
    "Grenade Harness": ("May only be fired once per battle. If fired in the Shooting phase, the bearer and his unit count "
                        "as having Frag Grenades during the following Assault phase.", []),
    "Auspex": (
        "After enemy Infiltrators have deployed, roll 4D6 for each unit containing an Auspex. If an enemy Infiltrating "
        "unit is within that distance and line of sight, the bearer's unit may immediately fire at it once before the "
        "battle begins. A unit may only make one Auspex attack.", []),
    "Nuncio Vox": (
        "A friendly unit arriving by Deep Strike whose centre model is placed within 6\" of the bearer does not scatter. "
        "Only usable if the bearer was on the battlefield at the start of the turn, is not Pinned or Falling Back and is "
        "not embarked.", []),
    "Teleport Homer": ("Friendly units arriving by teleportation whose first model is placed within 6\" of an active "
                       "Teleport Homer do not scatter. The Homer must have been on the battlefield at the start of the "
                       "turn.", []),
    "Signum": ("Once per friendly Shooting phase, the unit may re-roll one failed To Hit roll made with a shooting weapon. "
               "A unit may benefit from only one Signum per Shooting phase.", []),
    "Suspensor Web": ("A Heavy weapon fitted with a Suspensor Web may instead be fired as an Assault weapon with its "
                      "maximum range halved.", []),
    "Bionics": ("When the model loses its final Wound, leave it on its side. At the start of its controlling player's next "
                "turn roll a D6: on a 6 it returns with 1 Wound, otherwise remove it.", []),
    "Digital Weapons": "A model with Digital Weapons may re-roll one failed To Wound roll during each Assault phase.",
    "Master-crafted Weapon": ("A Master-crafted weapon may re-roll one failed To Hit roll per player turn. Applies to one "
                              "specific weapon (not grenades or other expendable equipment).", []),
    "Purity Seals": ("When the unit Falls Back, roll one additional D6 for its Fall Back distance and discard one die. Not "
                     "cumulative.", []),
    "Terminator Honours": "The model adds +1 to its Attacks characteristic.",
    "Psychic Hood": (
        "After an enemy Psyker passes a Psychic test, but before the power takes effect, the bearer may attempt to "
        "nullify it: both roll D6 and add their Leadership; if the bearer scores higher, the power is nullified.", []),
    "Narthecium": (
        "A unit containing an Apothecary with a Narthecium may ignore the first failed saving throw it suffers each "
        "player turn (not against Instant Death, attacks allowing no save, if the Apothecary is slain, or while he is in "
        "base contact with an enemy).", []),
    "Reductor": ("With Victory Points in use, the Apothecary recovers 1 Victory Point for each slain friendly Legiones "
                 "Astartes model from his unit, if he survives the battle.", []),
    "Servo-Arm": (
        "Makes one additional close-combat attack each Assault phase, resolved separately, always hitting on a 4+ and "
        "counting as a Power Fist (no charge or two-weapon bonuses). +1 to Battlefield Repair rolls. A model with a Jump "
        "Pack may not carry a Servo-Arm.", []),
    "Jump Pack": ("The model becomes Jump Infantry. May not be combined with a Bike, Jetbike or Terminator Armour.", []),
    "Space Marine Bike": ("The model becomes Bike unit type and is armed with twin-linked bolters. May not be combined "
                          "with a Jump Pack, Jetbike or Terminator Armour.", []),
    "Legion Vexilla": ("A unit containing a Legion Vexilla adds +1 to its combat-resolution score. Not cumulative; lost if "
                       "the bearer is slain.", []),
    "Cortex Controller": ("Controls Battle-Automata with the Cybernetica Cortex special rule (see Mechanicum Army List).",
                          []),
    "Cortex Designator": (ARMY_RULES["Cortex Designator"], []),
    "Cognis Signum": (ARMY_RULES["Cognis Signum"], []),
    "Targeting Matrix": (ARMY_RULES["Targeting Matrix"], []),
    "Smoke Launchers": ("", ["Smoke Launchers"]),
    "Searchlight": ("", ["Searchlight"]),
    "Dozer Blade": ("", ["Dozer Blade"]),
    "Extra Armour": ("", ["Extra Armor"]),
    "Auxiliary Drive": (ARMY_RULES["Auxiliary Drive"], []),
    "Locator Beacon": (ARMY_RULES["Locator Beacon"], []),
}
for k, v in list(WARGEAR.items()):
    if isinstance(v, str):
        WARGEAR[k] = (v, [])

# Space Marine Armoury (Praetor / Centurion / Power Armour Sergeant columns)
# name, points, praetor, centurion, pa_sgt, kind, note
ARMOURY = [
    # single-handed
    ("Bolt Pistol", 1, 1, 1, 0, "weapon", ""),
    ("Chainaxe", 4, 1, 1, 0, "weapon", ""),
    ("Chainfist", 30, 1, 1, 0, "weapon", "tda"),
    ("Close Combat Weapon", 1, 1, 1, 0, "weapon", ""),
    ("Force Weapon", 40, 1, 1, 0, "weapon", "psyker"),
    ("Hand Flamer", 5, 1, 1, 1, "weapon", ""),
    ("Lightning Claw", 25, 1, 1, 1, "weapon", ""),
    ("Pair of Lightning Claws", 30, 1, 1, 1, "weapon", "pair"),
    ("Plasma Pistol", 15, 1, 1, 1, "weapon", ""),
    ("Power Fist", 25, 1, 1, 1, "weapon", ""),
    ("Power Weapon", 15, 1, 1, 1, "weapon", ""),
    ("Relic Blade", 30, 1, 1, 0, "weapon", "twohanded"),
    ("Rending Weapon", 5, 1, 1, 1, "weapon", ""),
    ("Thunder Hammer", 30, 1, 1, 1, "weapon", ""),
    ("Volkite Serpenta", 5, 1, 1, 1, "weapon", ""),
    # two-handed / ranged
    ("Bolter", 2, 1, 1, 0, "weapon", ""),
    ("Combi-Bolter", 5, 1, 1, 1, "weapon", ""),
    ("Combi-Flamer", 10, 1, 1, 1, "weapon", ""),
    ("Combi-Grenade Launcher", 10, 1, 1, 1, "weapon", ""),
    ("Combi-Meltagun", 15, 1, 1, 1, "weapon", ""),
    ("Combi-Plasma Gun", 15, 1, 1, 1, "weapon", ""),
    ("Combi-Volkite Charger", 10, 1, 1, 1, "weapon", ""),
    ("Foeblaster Boltgun", 5, 1, 1, 0, "weapon", "tda"),
    ("Storm Bolter", 5, 1, 1, 1, "weapon", ""),
    ("Volkite Charger", 10, 1, 1, 0, "weapon", ""),
    # armour & protection (armour itself is handled as a separate option on each unit)
    ("Artificer Armour", 20, 0, 0, 1, "wargear", ""),
    ("Combat Shield", 5, 0, 1, 1, "wargear", "inv6"),
    ("Boarding Shield", 10, 0, 1, 0, "wargear", "inv5"),
    ("Refractor Field", 15, 0, 1, 1, "wargear", "refractor"),
    ("Iron Halo", 25, 0, 1, 0, "wargear", "ironhalo"),
    # grenades
    ("Frag Grenades", 1, 0, 0, 0, "wargear", ""),
    ("Krak Grenades", 2, 1, 1, 1, "wargear", ""),
    ("Melta Bombs", 5, 1, 1, 1, "wargear", ""),
    # personal
    ("Auspex", 2, 1, 1, 1, "wargear", ""),
    ("Bionics", 10, 1, 1, 1, "wargear", ""),
    ("Digital Weapons", 10, 1, 1, 0, "wargear", ""),
    ("Master-crafted Weapon", 15, 1, 1, 1, "wargear", ""),
    ("Nuncio Vox", 10, 1, 1, 0, "wargear", ""),
    ("Psychic Hood", 25, 1, 1, 0, "wargear", "psyker"),
    ("Purity Seals", 5, 1, 1, 1, "wargear", ""),
    ("Signum", 15, 1, 1, 0, "wargear", ""),
    ("Teleport Homer", 5, 1, 1, 1, "wargear", ""),
    ("Terminator Honours", 15, 1, 1, 0, "wargear", ""),
    ("Reductor", 5, 0, 1, 0, "wargear", "apothecary"),
]

LEGIONS = [
    "I - Dark Angels", "III - Emperor's Children", "IV - Iron Warriors", "V - White Scars",
    "VI - Space Wolves", "VII - Imperial Fists", "VIII - Night Lords", "IX - Blood Angels",
    "X - Iron Hands", "XII - World Eaters", "XIII - Ultramarines", "XIV - Death Guard",
    "XV - Thousand Sons", "XVI - Sons of Horus", "XVII - Word Bearers", "XVIII - Salamanders",
    "XIX - Raven Guard", "XX - Alpha Legion",
]


# ============================================================================
# Slice 2: remaining HQ, Elites, Fast Attack, Heavy Support, Rites of War
# ============================================================================
WEAPON_PROFILES.update({
    "Volkite Culverin": ('45"', "6", "5", "Heavy 4, Rending"),
    "Assault Cannon": ('24"', "6", "4", "Heavy 3, Rending, Jam"),
    "Kheres Assault Cannon": ('24"', "6", "4", "Heavy 6, Rending"),
    "Reaper Autocannon": ('36"', "7", "4", "Heavy 2, Twin-linked"),
    "Twin-linked Accelerator Autocannon": ('48"', "7", "4", "Heavy 6, Twin-linked, Accelerator Rounds, Rapid Tracking"),
    "Flamestorm Cannon": ("Template", "6", "3", "Heavy 1"),
    "Plasma Blaster": ('18"', "7", "2", "Assault 2, Gets Hot"),
    "Conversion Beamer (0-18\")": ('0-18"', "6", "-", "Heavy 1, Blast"),
    "Conversion Beamer (18-42\")": ('18-42"', "8", "4", "Heavy 1, Blast"),
    "Conversion Beamer (42-72\")": ('42-72"', "10", "1", "Heavy 1, Blast"),
    "Heavy Conversion Beamer (0-18\")": ('0-18"', "6", "-", "Heavy 1, Large Blast, Firing Calibration"),
    "Heavy Conversion Beamer (18-42\")": ('18-42"', "8", "4", "Heavy 1, Large Blast, Firing Calibration"),
    "Heavy Conversion Beamer (42-72\")": ('42-72"', "10", "1", "Heavy 1, Large Blast, Firing Calibration"),
    "Dreadnought Close Combat Weapon": ("-", "x2", "-", "Power Weapon, normal Initiative"),
    "Cyclone Missile Launcher - Frag": ('48"', "4", "6", "Heavy 2, Blast"),
    "Cyclone Missile Launcher - Krak": ('48"', "8", "3", "Heavy 2"),
    "Quad Heavy Bolter": ('36"', "5", "4", "Heavy 6, Twin-linked"),
    "Laser Destroyer": ('48"', "10", "1", "Heavy 1, Twin-linked"),
    "Graviton Cannon": ('36"', "Special", "4", "Heavy 1, Large Blast, Concussive, Graviton"),
    "Quad Launcher - Frag": ('12"-60"', "5", "5", "Heavy 4, Barrage, Blast, Shell Shock"),
    "Quad Launcher - Shatter": ('36"', "8", "4", "Heavy 4, Sunder"),
    "Quad Launcher - Incendiary": ('12"-60"', "4", "5", "Heavy 4, Barrage, Blast, Ignores Cover"),
    "Quad Launcher - Splinter": ('12"-36"', "2", "4", "Heavy 4, Barrage, Blast, Rending"),
    "Quad Launcher - Phosphex": ('12"-36"', "4", "3", "Heavy 4, Barrage, Blast, Poisoned (3+), Lingering Death"),
    "Rad Missile": ('48"', "4", "3", "Heavy 1, Blast, Fleshbane, Rad-phage"),
    "Phosphex Bomb": ('6"', "5", "2", "Assault 1, Blast, One Use, Poison (3+), Lingering Death"),
    "M.40 Stalker Bolter": ('24"', "4", "5", "Heavy 2, Pinning"),
    "Dragonfire Bolts": ('24"', "4", "5", "Rapid Fire, Ignores Cover"),
    "Hellfire Bolts": ('24"', "X", "5", "Rapid Fire, Poison (2+)"),
    "Kraken Bolts": ('30"', "4", "4", "Rapid Fire"),
    "Vengeance Rounds": ('18"', "4", "3", "Rapid Fire, Gets Hot"),
    "Heavy Bolter - Suspensor Fire": ('18"', "5", "4", "Assault 3"),
    "Predator Cannon": ('48"', "7", "4", "Heavy 4"),
    "Executioner Plasma Destroyer": ('36"', "7", "2", "Heavy 3, Blast"),
    "Magna-Melta": ('18"', "8", "1", "Heavy 1, Large Blast, Melta"),
    "Demolisher Cannon": ('24"', "10", "2", "Ordnance 1, Large Blast"),
    "Laser Destroyer Array": ('36"', "9", "1", "Ordnance 1, Twin-linked, Power Capacitor"),
    "Whirlwind - Vengeance Warhead": ('12-48"', "5", "4", "Ordnance 1, Barrage, Large Blast"),
    "Whirlwind - Castellan Warhead": ('12-48"', "4", "5", "Ordnance 1, Barrage, Large Blast, Ignores Cover"),
    "Whirlwind - Hyperios Warhead": ('48"', "8", "3", "Heavy 1, Skyfire, Interceptor"),
    "Earthshaker Cannon": ('36-240"', "9", "3", "Ordnance 1, Barrage, Large Blast"),
    "Medusa Siege Gun": ('36"', "10", "2", "Ordnance 1, Barrage, Large Blast"),
    "Scorpius Multi-launcher": ('48"', "8", "3", "Heavy 1, Barrage, Blast, Rocket Barrage"),
    "Quad Lascannon": ('48"', "9", "2", "Heavy 2, Twin-linked"),
    "Anvilus Autocannon Battery": ('48"', "8", "4", "Heavy 4"),
    "Hellfire Plasma Cannonade - Sustained": ('36"', "7", "2", "Heavy 4"),
    "Hellfire Plasma Cannonade - Maximal": ('36"', "7", "2", "Heavy 1, Large Blast, Plasma Overload"),
    "Arachnus Heavy Lascannon Battery": ('48"', "10", "2", "Heavy 2"),
    "Aiolos Missile Launcher": ('60"', "6", "3", "Heavy 3, Pinning"),
    "Neutron Beam Laser": ('36"', "10", "1", "Ordnance 2, Concussive"),
    "Leviathan Siege Claw": ("-", "x2", "-", "Dreadnought Close Combat Weapon"),
    "Leviathan Siege Drill": ("-", "x2", "-", "Dreadnought Close Combat Weapon, Armourbane"),
    "Leviathan Storm Cannon": ('24"', "7", "3", "Heavy 6"),
    "Cyclonic Melta Lance": ('18"', "9", "1", "Heavy 3, Melta"),
    "Grav-flux Bombard": ('18"', "Special", "2", "Heavy 1, Large Blast, Concussive, Ignores Cover, Graviton Collapse"),
    "Phosphex Discharger": ('6-18"', "5", "2", "Heavy 3, Barrage, Blast, Poison (3+), One Use"),
    "Focused Bombardment": ("Unlimited", "8", "3", "Ordnance 1, Large Blast, Barrage, Lance, Twin-linked"),
    # not in the army book - taken from Horus Heresy 1st edition / Warhammer 40,000 5th edition
    "Havoc Launcher": ('48"', "5", "5", "Heavy 1, Blast, Twin-linked"),
    "Typhoon Missile Launcher - Frag": ('48"', "4", "6", "Heavy 2, Blast"),
    "Typhoon Missile Launcher - Krak": ('48"', "8", "3", "Heavy 2"),
})

# twin-linked versions: same profile + Twin-linked
for base in ["Heavy Bolter", "Autocannon", "Lascannon", "Volkite Culverin", "Heavy Flamer", "Multi-Melta",
             "Flamer", "Meltagun", "Plasma Gun", "Volkite Caliver"]:
    r, s, ap, t = WEAPON_PROFILES[base]
    WEAPON_PROFILES["Twin-linked " + base] = (r, s, ap, t + ", Twin-linked")
for part in ["Frag", "Krak"]:
    r, s, ap, t = WEAPON_PROFILES["Missile Launcher - " + part]
    WEAPON_PROFILES["Twin-linked Missile Launcher - " + part] = (r, s, ap, t + ", Twin-linked")
    r, s, ap, t = WEAPON_PROFILES["Cyclone Missile Launcher - " + part]
    WEAPON_PROFILES["Twin-linked Cyclone Missile Launcher - " + part] = (r, s, ap, t + ", Twin-linked")

_NEW_WEAPONS = {
    "Volkite Culverin": None, "Assault Cannon": None, "Kheres Assault Cannon": None, "Reaper Autocannon": None,
    "Twin-linked Accelerator Autocannon": None, "Flamestorm Cannon": None, "Plasma Blaster": None,
    "Conversion Beamer": ["Conversion Beamer (0-18\")", "Conversion Beamer (18-42\")", "Conversion Beamer (42-72\")"],
    "Heavy Conversion Beamer": ["Heavy Conversion Beamer (0-18\")", "Heavy Conversion Beamer (18-42\")",
                                "Heavy Conversion Beamer (42-72\")"],
    "Dreadnought Close Combat Weapon": ["Dreadnought Close Combat Weapon", "Twin-linked Bolter"],
    "Chainfist with built-in Twin-linked Bolter": ["Chainfist", "Twin-linked Bolter"],
    "Cyclone Missile Launcher": ["Cyclone Missile Launcher - Frag", "Cyclone Missile Launcher - Krak"],
    "Twin-linked Cyclone Missile Launcher": ["Twin-linked Cyclone Missile Launcher - Frag",
                                             "Twin-linked Cyclone Missile Launcher - Krak"],
    "Twin-linked Missile Launcher": ["Twin-linked Missile Launcher - Frag", "Twin-linked Missile Launcher - Krak"],
    "Quad Heavy Bolter": None, "Laser Destroyer": None, "Graviton Cannon": None,
    "Quad Launcher": ["Quad Launcher - Frag"],
    "Quad Launcher with Frag and Shatter Shells": ["Quad Launcher - Frag", "Quad Launcher - Shatter"],
    "Missile Launcher with Suspensor Web and Rad Missiles": ["Rad Missile"],
    "Phosphex Bomb": None, "Rad Missiles": ["Rad Missile"],
    "M.40 Targeter and Stalker Bolter": ["M.40 Stalker Bolter"],
    "Special Issue Ammunition": ["Dragonfire Bolts", "Hellfire Bolts", "Kraken Bolts", "Vengeance Rounds"],
    "Heavy Bolter with Suspensor Web": ["Heavy Bolter - Suspensor Fire", "Heavy Bolter"],
    "Heavy Bolter with Suspensor and Hellfire Rounds": ["Heavy Bolter - Suspensor Fire",
                                                        "Heavy Bolter - Hellfire Round"],
    "Heavy Flamer with Suspensor Web": ["Heavy Flamer"],
    "Missile Launcher with Suspensor Web": ["Missile Launcher - Frag", "Missile Launcher - Krak"],
    "Predator Cannon": None, "Executioner Plasma Destroyer": None, "Magna-Melta": None,
    "Demolisher Cannon": None, "Laser Destroyer Array": None,
    "Whirlwind Launcher": ["Whirlwind - Vengeance Warhead", "Whirlwind - Castellan Warhead"],
    "Hyperios Warheads": ["Whirlwind - Hyperios Warhead"],
    "Earthshaker Cannon": None, "Medusa Siege Gun": None, "Scorpius Multi-launcher": None,
    "Quad Lascannon": None, "Anvilus Autocannon Battery": None,
    "Hellfire Plasma Cannonade": ["Hellfire Plasma Cannonade - Sustained", "Hellfire Plasma Cannonade - Maximal"],
    "Arachnus Heavy Lascannon Battery": None, "Aiolos Missile Launcher": None, "Neutron Beam Laser": None,
    "Leviathan Siege Claw with Meltagun": ["Leviathan Siege Claw", "Meltagun"],
    "Leviathan Siege Drill with Meltagun": ["Leviathan Siege Drill", "Meltagun"],
    "Leviathan Storm Cannon": None, "Cyclonic Melta Lance": None, "Grav-flux Bombard": None,
    "Phosphex Discharger": None, "Focused Bombardment": None,
    "Typhoon Missile Launcher": ["Typhoon Missile Launcher - Frag", "Typhoon Missile Launcher - Krak"],
    "Heavy Bolter Sponsons": ["Heavy Bolter"], "Heavy Flamer Sponsons": ["Heavy Flamer"],
    "Lascannon Sponsons": ["Lascannon"],
    "Incendiary Shells": ["Quad Launcher - Incendiary"], "Shatter Shells": ["Quad Launcher - Shatter"],
    "Splinter Shells": ["Quad Launcher - Splinter"], "Phosphex Canister Shot": ["Quad Launcher - Phosphex"],
    "Scimitar Jetbike with Heavy Bolter": ["Heavy Bolter"],
    "Space Marine Bike with Twin-linked Bolters": ["Twin-linked Bolter"],
    "Attack Bike with Twin-linked Bolters": ["Twin-linked Bolter"],
    "Two Bolt Pistols": ["Bolt Pistol"],
}
for base in ["Heavy Bolter", "Autocannon", "Lascannon", "Volkite Culverin", "Heavy Flamer", "Multi-Melta",
             "Flamer", "Meltagun", "Plasma Gun", "Volkite Caliver"]:
    _NEW_WEAPONS["Twin-linked " + base] = None
for n, profs in _NEW_WEAPONS.items():
    WEAPONS[n] = profs if profs is not None else [n]

WEAPON_RULES.update({
    "Assault Cannon": ["Rending", "Jam"], "Kheres Assault Cannon": ["Rending", "Jam"],
    "Twin-linked Accelerator Autocannon": ["Twin-Linked", "Accelerator Rounds", "Rapid Tracking"],
    "Heavy Conversion Beamer": ["Firing Calibration"], "Plasma Blaster": ["Gets Hot"],
    "Quad Launcher": ["Shell Shock"], "Quad Launcher with Frag and Shatter Shells": ["Shell Shock", "Sunder"],
    "Shatter Shells": ["Sunder"], "Phosphex Canister Shot": ["Lingering Death"],
    "Rad Missiles": ["Rad-phage", "Fleshbane"],
    "Missile Launcher with Suspensor Web and Rad Missiles": ["Rad-phage", "Fleshbane", "Suspensor Web"],
    "Phosphex Bomb": ["Lingering Death"], "Phosphex Discharger": ["Lingering Death"],
    "Special Issue Ammunition": ["Special Issue Ammunition"],
    "Heavy Bolter with Suspensor and Hellfire Rounds": ["Hellfire"],
    "Laser Destroyer Array": ["Power Capacitor"], "Scorpius Multi-launcher": ["Rocket Barrage"],
    "Hellfire Plasma Cannonade": ["Plasma Overload"], "Grav-flux Bombard": ["Graviton Collapse"],
    "Leviathan Siege Drill with Meltagun": ["Armourbane", "Melta"],
    "Leviathan Siege Claw with Meltagun": ["Melta"],
    "Cyclonic Melta Lance": ["Melta"], "Magna-Melta": ["Melta"],
    "Neutron Beam Laser": ["Concussive"], "Graviton Cannon": ["Graviton", "Concussive"],
    "Focused Bombardment": ["Lance"], "Conversion Beamer": [],
})

ARMY_RULES.update({
    "Burning Retros": (
        "From the moment the Dreadnought Drop Pod arrives by Deep Strike until the start of its controlling player's next "
        "turn, it has the Shrouded special rule, as does a Dreadnought which disembarks from it during this period. Any "
        "unit targeted by a shooting attack whose line of sight passes through or over the Drop Pod also gains Shrouded."),
    "Jam": ("If all three To Hit rolls made by an Assault Cannon when it fires are natural 1s, the weapon is destroyed and "
            "may not be fired again. If mounted on a vehicle, this counts as a Weapon Destroyed result."),
    "Accelerator Rounds": ("A natural To Wound roll of 6 ignores Armour Saves. Against vehicles, if the Armour "
                           "Penetration die scores a natural 6, roll an additional D6 and add it to the total."),
    "Firing Calibration": ("A weapon with Firing Calibration may not be fired if its bearer moved during the same turn, "
                           "even if the bearer has Relentless or is a vehicle."),
    "Suspensor Web": ("A Heavy weapon fitted with a Suspensor Web may instead be fired as an Assault weapon with its "
                      "maximum range halved. Shots, Strength, AP and other special rules are unchanged."),
    "Honour or Death": (
        "If the Legion Champion is in base contact with one or more enemy Independent Characters, he must direct all of "
        "his close-combat attacks against one of them. When attacking an enemy Independent Character in close combat, he "
        "may re-roll failed To Hit and To Wound rolls."),
    "Retinue": (
        "This unit is selected for a character (Honour Guard: one per Legion Praetor; Command Squads: for an eligible HQ "
        "character; Terminator Command Squad: only for a character in any form of Terminator Armour). It does not occupy "
        "a separate Force Organisation slot; the character and the retinue count as a single HQ selection, but deploy "
        "and operate as separate units."),
    "Veteran Tactics": ("When constructing the army, select one Veteran Tactic for each Legion Veteran Squad. It applies "
                        "to every model in the squad for the battle."),
    "Resolve": "The squad gains the Stubborn special rule.",
    "Assault Veterans": "The squad gains the Furious Charge special rule.",
    "Counter-Assault": "The squad gains the Counter-Attack special rule.",
    "Machine Killers": "The squad gains the Tank Hunters special rule.",
    "Recon Veterans": "The squad gains the Infiltrate special rule.",
    "Marksmen": ("Bolters fired by models in the squad have the Twin-linked special rule (normal Bolters only, not "
                 "Combi-weapons, Foeblaster Boltguns or other bolt weapon variants)."),
    "Implacable Advance": ("In any mission which distinguishes between Scoring and non-Scoring units, a Legion Terminator "
                           "Squad counts as a Scoring Unit whenever Troops choices normally count as Scoring Units."),
    "Dual Pistols (Destroyers)": ("A model with this special rule may fire both of its Pistol weapons during the Shooting "
                                  "phase at the same target. If it does, it may not fire another weapon that phase."),
    "Destroyer Cadre": ("A Legion Destroyer Squad may only be joined by an Independent Character with the Legion Moritat "
                        "Consul upgrade. No other Independent Character may join the squad."),
    "Rad Grenades": (
        "Rad Grenades are neither Assault nor Defensive Grenades. During any player turn in which a unit equipped with Rad "
        "Grenades charges or is charged, enemy non-vehicle models engaged with that unit suffer -1 Toughness until the end "
        "of the Assault phase (for all purposes, including Instant Death). Multiple units' effects are not cumulative."),
    "Rad-phage": ("If a model suffers one or more unsaved Wounds from a weapon with Rad-phage and survives, reduce its "
                  "Toughness by 1 for the remainder of the battle (minimum 1). Multiple applications are cumulative."),
    "Lingering Death": ("After resolving the attack, leave the Blast marker in place. For the remainder of the battle, the "
                        "area beneath it counts as Dangerous Terrain for non-vehicle models and Open-topped vehicles."),
    "Battlesmith (Techmarine)": (
        "Instead of shooting, the Battlesmith may attempt a repair on one eligible friendly model in base contact "
        "(Vehicles, models with Cybernetica Cortex, models with Iron and Machine). Roll a D6; on a 5+ it succeeds. "
        "Vehicle: remove one Engine Damaged, Weapon Destroyed or Immobilised result. Other: regain one lost Wound. One "
        "attempt per turn; a model benefits from one successful repair per turn; never returns destroyed models; Daemons "
        "may not be repaired unless a rule allows it. Equipment modifying the roll applies to both uses."),
    "Bolster Defences": (
        "Before either army deploys, each Legion Techmarine may nominate one ruin or similar defensive terrain feature "
        "wholly or partially within his deployment zone. Its Cover Save is improved by 1 (maximum 3+). A feature may only "
        "be Bolstered once."),
    "Field Team": (
        "A Legion Techmarine accompanied by Servo-automata forms a single Field Team. He may not voluntarily leave them "
        "while any remain alive. The Field Team may join and leave friendly units as though the Techmarine were an "
        "Independent Character. If the Techmarine is slain, surviving Servo-automata form their own unit and become "
        "subject to Cybernetica."),
    "Cybernetica": ("At the beginning of each friendly Movement phase, a unit of Servo-automata not accompanied by a Legion "
                    "Techmarine must take a Pinning test, unless it is already engaged in close combat."),
    "Armoured Sarcophagus": "The Dreadnought's Front Armour increases from 12 to 13.",
    "Veteran Pilot": "The Dreadnought's Weapon Skill and Ballistic Skill increase by +1 (WS5, BS5).",
    "Frag Assault Launchers": (
        "A Walker with Frag Assault Launchers counts as having Frag Grenades when charging an enemy in or behind cover. If "
        "a Transport has them, any unit charging in the turn it disembarks counts as having Frag Grenades that Assault "
        "phase."),
    "Paired Close-Combat Arms": ("If the Dreadnought has two Dreadnought Close Combat Weapons it gains +1 Attack (already "
                                 "applied to the profile in this builder)."),
    "Atomantic Shielding": (
        "Each time the vehicle suffers a Glancing or Penetrating Hit from a shooting attack, roll a D6: on a 5+ the hit is "
        "ignored. In close combat, the hit is ignored on a 6. Roll before the Vehicle Damage table. If the vehicle "
        "suffers an Explodes! result, add +1\" to the radius of the explosion."),
    "Rapier Battery": (
        "Follows the ProHammer rules for Artillery. Each Rapier Carrier has two designated crew and needs at least one "
        "within 2\" to move or fire. One crew model operates the Rapier and may not fire another weapon that phase. "
        "Carriers may move with their crew but may not fire in a turn in which they moved, and cannot be transported "
        "unless a rule says otherwise. All carriers must have the same weapon and ammunition."),
    "Shell Shock": "Any Pinning test caused by a weapon with this rule suffers a -1 Leadership modifier.",
    "Sunder": "A weapon with this rule may re-roll failed Armour Penetration rolls against vehicles.",
    "Marked for Death": (
        "After both armies have deployed, nominate one enemy unit for each Legion Seeker Squad. When the squad shoots at "
        "that unit it re-rolls To Hit rolls of 1 and To Wound rolls of 1 (Armour Penetration rolls of 1 against vehicles). "
        "If the target is destroyed, no new target may be selected."),
    "Special Issue Ammunition": (
        "Each time the squad fires Bolters, Foeblaster Boltguns or the bolter component of Combi-weapons, select one "
        "ammunition type (Dragonfire Bolts, Hellfire Bolts, Kraken Bolts, Vengeance Rounds). All eligible models must use "
        "the same type."),
    "Armoured Crew": "The vehicle does not count as Open-topped.",
    "Power Capacitor": (
        "If the Vindicator remained stationary during its Movement phase, it may fire the Laser Destroyer Array as "
        "Ordnance 2, Twin-linked, or an Overcharged Volley as Ordnance 3, Twin-linked. After an Overcharged Volley, roll a "
        "D6: on a 1 the Vindicator suffers an automatic Glancing Hit."),
    "Ferromantic Invulnerability": ("Melta weapons do not roll an additional Armour Penetration die against the Achilles. "
                                    "Lance weapons do not reduce its Armour Value."),
    "Explorator Augury Web": (
        "The Proteus gains Scout. At the start of the controlling player's turn, before Reserve rolls, choose a mode until "
        "the start of the next turn: Disruption (opponent suffers -1 to Reserve rolls) or Relay (re-roll failed Reserve "
        "rolls). Multiple webs give no extra benefit; one mode per army. Transport Capacity is reduced to 8 models."),
    "Rocket Barrage": ("If the Whirlwind Scorpius remained stationary during its Movement phase, the Scorpius "
                       "Multi-launcher becomes Heavy 1+D3 for that Shooting phase."),
    "Flare Shield": ("Against shooting attacks which strike the Spartan's Front Armour, reduce the Strength of Blast and "
                     "Template weapons by 2 and all other ranged attacks by 1. No effect in close combat."),
    "Rapid Tracking": "Jink saves may not be taken against attacks made with the Accelerator Autocannon.",
    "Plasma Overload": ("After firing the Hellfire Plasma Cannonade in Maximal mode, roll a D6. On a 1 the Deredeo suffers "
                        "an automatic Glancing Hit that may not be prevented by cover saves or Atomantic Shielding."),
    "Helical Targeting Array": (
        "At the beginning of the controlling player's turn, the Deredeo may activate its Helical Targeting Array. If it "
        "does, it must remain stationary that turn and its ranged weapons gain Skyfire and Interceptor until the beginning "
        "of its next turn."),
    "Atomantic Pavaise": (
        "Improves the Deredeo's Atomantic Shielding save against shooting from 5+ to 4+. Friendly Infantry within 3\" gain "
        "a 6+ Invulnerable Save against shooting, or improve an existing Invulnerable Save by 1 (maximum 3+)."),
    "Enhanced Ferromantic Rites": (
        "Melta weapons do not roll an additional Armour Penetration die against the Achilles-Alpha; Lance weapons do not "
        "reduce its Armour Value. Apply -1 to all Vehicle Damage table rolls caused by Penetrating Hits against it."),
    "Galvanic Traction Drive": "The Achilles-Alpha may re-roll failed Dangerous Terrain tests.",
    "Graviton Collapse": (
        "Against non-vehicle models, for each model hit roll 2D6; if the result is greater than the model's Strength it "
        "suffers a wound. Against vehicles, do not use the Graviton rule; roll 3D6 for Armour Penetration instead."),
    "Reinforced Atomantic Shielding": (
        "Each time the Leviathan suffers a Glancing or Penetrating Hit, roll a D6: on a 4+ the hit is ignored. Roll before "
        "the Vehicle Damage table. On an Explodes! result, increase the explosion's Strength by D3 and its radius by D3\"."),
    "Crushing Charge": (
        "On a turn in which the Leviathan charges, it may resolve two of its attacks at Initiative 10 instead of one "
        "(Hammer of Wrath), and gains +1 Initiative for the remainder of that Assault phase."),
    "Geo-Locator Beacon": ("Friendly units arriving by Deep Strike do not scatter if their first model is placed within 24\" "
                           "of the Damocles and otherwise has a legal deployment position."),
    "Command Vox Relay": ("While the Damocles is on the battlefield, its controlling player may apply +1 or -1 to any of "
                          "their Reserve rolls."),
    "Focused Bombardment (Damocles)": ("Once per battle, provided the Damocles did not move that turn, it may fire the "
                                       "Focused Bombardment."),
    "Command Vehicle": ("0-1 Damocles Command Rhino may be selected as a non-compulsory HQ choice in an army of at least "
                        "1,000 points. Alternatively, a Master of Signals may select one as a Dedicated Transport."),
    "Fire Control": ("When a Heavy Support Squad led by an Armistos enters Overwatch, its models may declare Overwatch "
                     "targets out to the normal maximum range of their weapons rather than 24\"."),
    "Art of Destruction": ("Heavy weapons fired by the Siege Breaker's unit receive +1 to Armour Penetration rolls against "
                           "vehicles and fortifications (not pistols, grenades or close-combat attacks)."),
    "Hardened Armour (Heavy Support)": ("The squad has the Hardened Armour special rule described in the Legion Breacher "
                                        "Siege Squad entry."),
    "Sacred Standard": ("Friendly Legiones Astartes units add +1 to their combat-resolution score in any close combat "
                        "within 6\" of a Sacred Standard. Not cumulative with another Sacred Standard or Legion Standard."),
    "Crusade Relic": ("May be revealed once per battle in either player's turn provided the bearer does not move that turn. "
                      "Roll 2D6: until the end of that player turn, all friendly Legiones Astartes models within that "
                      "distance gain +1 Attack. An army may normally include no more than one Crusade Relic."),
    "Legion Standard": ("Combines the effects of a Sacred Standard and a Crusade Relic. Only an army of 2,000 points or "
                        "more may include one; it counts as the army's Crusade Relic. In battles of 3,000 points or more, "
                        "one additional Crusade Relic may also be included."),
    "Heavy Support Specialists": ("One Legion Heavy Support Squad Sergeant may be upgraded to an Armistos (+20) or a Siege "
                                  "Breaker (+35)."),
})

WARGEAR.update({
    "Rad Grenades": (ARMY_RULES["Rad Grenades"], []),
    "Armoured Ceramite": ("The vehicle does not suffer the additional Armour Penetration die normally granted by the Melta "
                          "special rule.", []),
    "Armoured Sarcophagus": (ARMY_RULES["Armoured Sarcophagus"], []),
    "Veteran Pilot": (ARMY_RULES["Veteran Pilot"], []),
    "Frag Assault Launchers": (ARMY_RULES["Frag Assault Launchers"], []),
    "Power of the Machine Spirit": ("", ["Power of the Machine Spirit"]),
    "Explorator Augury Web": (ARMY_RULES["Explorator Augury Web"], ["Scouts"]),
    "Flare Shield": (ARMY_RULES["Flare Shield"], []),
    "Atomantic Pavaise": (ARMY_RULES["Atomantic Pavaise"], []),
    "Sacred Standard": (ARMY_RULES["Sacred Standard"], []),
    "Crusade Relic": (ARMY_RULES["Crusade Relic"], []),
    "Legion Standard": (ARMY_RULES["Legion Standard"], []),
    "Hardened Armour": (ARMY_RULES["Hardened Armour"], []),
})

# Power Armour Sergeants that are in Terminator Armour ('TDA Sgt' column of the Armoury)
TDA_SGT = {"Chainfist": 30, "Force Weapon": 40, "Lightning Claw": 25, "Pair of Lightning Claws": 30,
           "Power Fist": 25, "Power Weapon": 15, "Thunder Hammer": 30, "Combi-Bolter": 5, "Combi-Flamer": 10,
           "Combi-Grenade Launcher": 10, "Combi-Meltagun": 15, "Combi-Plasma Gun": 15, "Combi-Volkite Charger": 10,
           "Foeblaster Boltgun": 5, "Storm Bolter": 5, "Auspex": 2, "Bionics": 10, "Master-crafted Weapon": 15,
           "Purity Seals": 5, "Suspensor Web": 10, "Teleport Homer": 5}

RITES = {
    "Pride of the Legion": (
        "EFFECTS - The Legion's Finest: Legion Veteran Squads and Legion Terminator Squads (and Legion-specific Terminator "
        "units) may be selected as Troops choices; the army's compulsory Troops choices must be selected from these units.\n"
        "LIMITATIONS - Price of Failure: if every such unit selected as Troops has been destroyed by the end of the battle, "
        "the enemy receives an additional 150 Victory Points (Victory Point missions only)."),
    "Orbital Assault": (
        "EFFECTS - Orbital Transports: any Legiones Astartes Infantry unit which can be carried by a Drop Pod or Dreadclaw "
        "may purchase one at its normal cost. Dreadnought Assault: a Castraferrum (Legion Dreadnought) or Contemptor may "
        "purchase a Drop Pod for +50 or a Dreadclaw for +65. Teleport Assault: units entirely in Terminator or Cataphractii "
        "Armour may Deep Strike even if the mission would not permit it. Orbital Deployment: any unit with Deep Strike may "
        "use it even if the mission would not permit it; the army may begin with no models deployed.\n"
        "LIMITATIONS - Every unit must have Deep Strike or begin embarked aboard a Drop Pod or Dreadclaw (Independent "
        "Characters may join an eligible unit)."),
    "Armoured Spearhead": (
        "EFFECTS - Armoured Transports: any Legiones Astartes Infantry unit which fits in a Land Raider may purchase one for "
        "+250 points. Crushing Advance: enemy units suffer -1 Leadership on Morale tests caused by Tank Shock from this "
        "army's vehicles.\nLIMITATIONS - Mechanised Force: every Infantry unit must begin embarked aboard a vehicle with the "
        "Tank and Transport types. Broken Spearhead: if every Tank has been destroyed by the end of the battle, the enemy "
        "receives an additional 150 Victory Points."),
    "Armoured Breakthrough": (
        "EFFECTS - Predator Squadrons: up to two Troops choices may be Legion Predator Strike Squadrons; they may satisfy "
        "compulsory Troops. Predators may still be taken as Heavy Support.\nLIMITATIONS - The army may include no more than "
        "one Fast Attack choice."),
    "Legion Assault Company": (
        "EFFECTS - Assault Formation: compulsory Troops must be Legion Assault Squads, which may not remove their Jump Packs. "
        "Veteran Assault Squads: a Legion Veteran Squad may take Jump Packs for +10 points per model (no Transport). Death "
        "from Above: units entirely equipped with Jump Packs may Deep Strike even if the mission would not permit it.\n"
        "LIMITATIONS - At least one Independent Character must have a Jump Pack. No more than one Heavy Support choice."),
    "Legion Breacher Company": (
        "EFFECTS - Breacher Formation: compulsory Troops must be Legion Breacher Siege Squads. Shield Wall: models with "
        "Boarding Shields may re-roll results of 1 on Invulnerable Saves granted by them.\nLIMITATIONS - At least one "
        "Independent Character must have a Boarding Shield. No more than one Fast Attack choice."),
    "Legion Recon Company": (
        "EFFECTS - Recon Formation: compulsory Troops must be Legion Reconnaissance Squads. Covert Deployment: units with "
        "Infiltrate may use it even if the mission would not permit it. Recon Veterans: any Legion Veteran may replace its "
        "bolter, or both bolt pistol and close-combat weapon, with a Sniper Rifle for +5. Forward Positions: a unit which "
        "Infiltrated or made a pre-game Scout move improves its Cover Save by +1 in the first game turn (max 3+).\n"
        "LIMITATIONS - No model may have Terminator Armour or Cataphractii Terminator Armour. All Heavy Support choices "
        "must begin in Reserve."),
    "Legion Destroyer Company": (
        "EFFECTS - Destroyer Formation: Legion Destroyer Squads may be Troops, and compulsory Troops must be Destroyer "
        "Squads. Forbidden Arsenal: any Legiones Astartes Character without access to Phosphex Bombs may take one for +10; "
        "for every five models in a Destroyer Squad, up to two Destroyers may take a Missile Launcher with Suspensor Web "
        "and Rad Missiles (+25).\nLIMITATIONS - The army must include at least one Moritat. No more than one Heavy "
        "Support choice."),
    "Fury of the Ancients": (
        "EFFECTS - Ancient Warhost: Castraferrum (Legion) Dreadnoughts and Contemptor Dreadnoughts may be Troops; the "
        "compulsory Troops must be selected from these units.\nLIMITATIONS - Keeper of the Ancients: the army must include "
        "at least one Techmarine. Irreplaceable Ancients: +50 Victory Points to the enemy per Dreadnought destroyed. No "
        "more than one Fast Attack choice."),
    "Sky Hunter Phalanx": (
        "EFFECTS - Sky Hunter Formation: Legion Sky Hunter Jetbike Squadrons may be Troops, and compulsory Troops must be "
        "Sky Hunter Squadrons. Jetbike Command: an Independent Character with a Space Marine Bike may upgrade it to a "
        "Jetbike for +5. Rapid Encirclement: once per battle each Sky Hunter Squadron may leave the battlefield into "
        "Ongoing Reserves and return using Outflank.\nLIMITATIONS - At least one Independent Character must be mounted on a "
        "Jetbike. No Castraferrum or Contemptor Dreadnoughts. No more than one Heavy Support choice."),
    "Legion Tactical Company": (
        "EFFECTS - Line Company: compulsory Troops must be Legion Tactical Squads. Fury of the Legion: once per battle each "
        "Legion Tactical Squad which remained stationary may fire one additional shot with every bolter and may not charge "
        "that turn.\nLIMITATIONS - Strength of the Legion: the army must include at least three Legion Tactical Squads."),
}

RITES["Primarch's Chosen"] = (
    "REQUIREMENTS - The army must include the Primarch of its Legion, who must be the Warlord; the army must contain at "
    "least 1,500 points.\nEFFECTS - Lord and Master: the Primarch fulfils the compulsory HQ requirement despite being a "
    "Lord of War, and may be included in an army of 1,500 points or more. The Chosen Sons: Legion Veteran Squads and "
    "Legion Terminator Squads may be Troops; the two compulsory Troops must be selected from them. The Primarch's Guard: "
    "the Primarch may select one Legion Honour Guard Squad or Legion-specific bodyguard as his retinue.\nLIMITATIONS - "
    "No other Lord of War; no Allied Detachment; no more than one other model with Master of the Legion; at least half "
    "of the army's non-vehicle units must have the Legiones Astartes special rule; if the Primarch is destroyed, all "
    "other units in the Detachment cease to count as Scoring units.")

