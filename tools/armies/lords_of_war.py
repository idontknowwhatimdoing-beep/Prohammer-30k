"""Lords of War supplement (super-heavy vehicles, flyers and engines used by several armies) for Prohammer 30k.

Source: the author's Lords of War book. Line numbers in comments refer to Lords_of_War.txt.

Structure: its own catalogue. Every unit is a Lords of War choice; the armies that may take it are given by an
"Available to: ..." rule on the unit (the book groups the entries under Legiones Astartes, Talons of the Emperor and
Exercitus et Mechanicus). New Recruit cannot check across catalogues which army takes a unit (see
tools/questions/Lords of War.md). The catalogue brings its own "Lords of War Detachment" force (one Lords of War
choice, no compulsory HQ/Troops) so the units can be added next to an army from another catalogue.
"""
from armies.common import *  # noqa: F401,F403
from armies.common import (k, unit, upgrade, catalogue, start, register_data, LOW, vehicle_profile, error_if)
from bsx import uid, el, wrap, cond, any_of, modifier, constraint, entry, link, group, category_link
import gamesystem as gs
from legiones import W, has, gear, rules_links, transport_profile
from legiones2 import slot, take

ARMY = "Lords of War"

# =====================================================================================================  RULES
SH_RULES = ["Lords of War", "Super-heavy Vehicle", "Structure Points", "Massive Firepower", "Lumbering War Engine",
            "Super-heavy Tank Shock", "Crushing Advance", "Immense Machine", "Catastrophic Destruction"]

AV_LEGION = "Available to: Legiones Astartes"
AV_TALONS = "Available to: Talons of the Emperor"
AV_EM = "Available to: Exercitus et Mechanicus"

RULES = {
    # ---------------------------------------------------------------- general (L40-L170)
    "Lords of War": (
        "Lords of War are exceptionally powerful and costly battlefield assets and occupy the Lords of War Force "
        "Organisation slot unless otherwise stated. Unless specifically stated otherwise, all vehicles in this book use "
        "the normal Vehicle rules from the ProHammer Core Rules; Flyers use the normal ProHammer Flyer rules. Hull "
        "Points are not used. Structure Points are determined normally according to the ProHammer Core Rules."),
    "Super-heavy Vehicle": (
        "Unless otherwise stated, a Super-heavy Vehicle follows all normal rules for Vehicles in the ProHammer Core "
        "Rules, with the exceptions given by Structure Points, Massive Firepower, Lumbering War Engine, Super-heavy Tank "
        "Shock, Crushing Advance, Immense Machine and Catastrophic Destruction."),
    "Structure Points": (
        "A Super-heavy Vehicle uses the number of Structure Points listed in its unit entry instead of determining its "
        "Structure Points from its Armour Values; they otherwise function exactly as described in the ProHammer Core "
        "Rules. When a Super-heavy Vehicle suffers a Wrecked or Explodes! result while it still has one or more "
        "Structure Points remaining, one Structure Point is automatically expended and the result is reduced "
        "sufficiently for the vehicle to survive (a vehicle with 3 Structure Points can survive three otherwise "
        "destructive damage results). Once no Structure Points remain, a subsequent Wrecked or Explodes! result "
        "destroys the vehicle. A Super-heavy Vehicle may also Jury-Rig damage using its remaining Structure Points as "
        "normal."),
    "Massive Firepower": (
        "A Super-heavy Vehicle may fire Ordnance weapons without preventing it from firing its other weapons that turn. "
        "It automatically passes any Split Fire test. Each weapon may therefore be fired at a separate eligible target, "
        "subject to its normal range, Line of Sight and firing arc."),
    "Lumbering War Engine": (
        "Unless otherwise stated, a Super-heavy Vehicle may move up to 6\" in its Movement phase and may fire all of its "
        "weapons normally whether it remains stationary or moves up to 6\". It may pivot by up to 90 degrees at any point "
        "during its move. Super-heavy Vehicles may not move Flat Out unless specifically permitted by their unit entry. "
        "This rule does not apply to Super-heavy Flyers, which use the normal Flyer movement rules of the ProHammer "
        "Core Rules."),
    "Super-heavy Tank Shock": (
        "A Super-heavy Vehicle with the Tank unit type may Tank Shock and Ram using the normal ProHammer rules. Enemy "
        "units taking a Tank Shock Test caused by a Super-heavy Vehicle suffer a -1 modifier to their Leadership."),
    "Crushing Advance": (
        "Super-heavy Vehicles ignore low walls, hedges, rubble, barricades and other similarly minor obstacles when "
        "moving. Other Difficult Terrain is treated as Dangerous Terrain as normal. If a Super-heavy Vehicle fails a "
        "Dangerous Terrain test, it suffers an Engine Damaged result instead of becoming Immobilised."),
    "Immense Machine": (
        "Crew Shaken: the attacker chooses one weapon carried by the Super-heavy Vehicle; that weapon may only fire Snap "
        "Shots until the end of the vehicle's next turn, the remainder of the vehicle operates normally. Crew Stunned: "
        "the vehicle may not move during its next Movement phase; in addition the attacker chooses one weapon, which "
        "may only fire Snap Shots until the end of the vehicle's next turn (its other weapons may fire normally). "
        "Engine Damaged, Weapon Destroyed, Immobilised, Wrecked and Explodes! results are resolved normally, including "
        "the use of Structure Points."),
    "Catastrophic Destruction": (
        "Whenever a Super-heavy Vehicle is finally destroyed after it has no Structure Points remaining, roll a D6. "
        "1-3 Wrecked: the vehicle is destroyed and remains on the battlefield as a wreck. 4-5 Explosion: all models "
        "within D6\" of its hull suffer a Strength 5 AP- hit (vehicles: Strength 5 hit against their Side Armour). "
        "6 Catastrophic Explosion: roll one D3 for each Structure Point the vehicle possessed at the start of the battle "
        "and add the results together; the total is the radius of the explosion in inches. All models within this "
        "distance suffer a Strength 6 AP- hit (vehicles: Strength 6 hit against their Side Armour). Remove the vehicle "
        "and replace it with an appropriately sized crater where possible."),
    # ---------------------------------------------------------------- availability
    AV_LEGION: (
        "This Lord of War is presented in the Legiones Astartes section of the Lords of War book and may be taken by a "
        "Legiones Astartes army. (Not checked by the army builder: add it to a Lords of War Detachment next to the "
        "army.)"),
    AV_TALONS: (
        "This Lord of War is presented in the Talons of the Emperor section of the Lords of War book and may be taken by "
        "a Talons of the Emperor army. (Not checked by the army builder.)"),
    AV_EM: (
        "This Lord of War is presented in the Exercitus et Mechanicus section of the Lords of War book and may be taken "
        "by the Imperial Army and Mechanicum armies (Solar Auxilia, Exercitus Imperialis, Mechanicum). (Not checked by "
        "the army builder.)"),
    # ---------------------------------------------------------------- Lords of War special rules (L174-L218)
    "Super-heavy Command Tank": (
        "Friendly Infantry units within 24\" of a Super-heavy Command Tank may re-roll failed Morale Tests."),
    "Space Marine Legion Crew": "A vehicle upgraded with Space Marine Legion Crew has Ballistic Skill 4.",
    "Ordinatus Reactor Meltdown": (
        "When an Ordinatus is finally destroyed, add +2 to its Catastrophic Destruction roll. In addition, if it suffers "
        "a Catastrophic Explosion, roll one D6 (instead of one D3) for each Structure Point the Ordinatus possessed at "
        "the start of the battle when determining the explosion radius."),
    "Reinforced Ordinatus Chassis": (
        "Whenever an Ordinatus spends a Structure Point to Jury-Rig a damage result, roll a D6. On a 4+, the damage "
        "result is reduced as normal but the Structure Point is not lost; on a 1-3 the Structure Point is expended "
        "normally. In addition, the first Weapon Destroyed result suffered by the Ordinatus during the battle is ignored "
        "on a 4+."),
    "Bomb": (
        "Weapons with the Bomb type may only be used by a Flyer while it is Zooming. During the Flyer's Movement phase, "
        "after completing its move, it may make one Bombing Run if it passed over an enemy unit during that move: choose "
        "one enemy unit which the Flyer passed over and place the appropriate Blast marker with its centre over a model "
        "in that unit which the Flyer passed over. Roll for Scatter normally; the Flyer's Ballistic Skill does not "
        "reduce the distance scattered. Resolve the attack using the Bomb's weapon profile. A Flyer may only use one "
        "Bomb weapon during each Movement phase unless specifically stated otherwise. Dropping a Bomb does not prevent "
        "the Flyer from firing its other weapons during the Shooting phase. Bomb weapons may not be used while "
        "Hovering."),
    "Bomb X": (
        "When a Bomb weapon with a number after its type (e.g. Bomb 3) is used during a Bombing Run, resolve a number of "
        "attacks equal to the number shown. All attacks must be placed over the same target unit and are resolved "
        "separately."),
    # ---------------------------------------------------------------- weapon special rules (L476-L572)
    "Massive Blast": "A weapon with this special rule uses the 7\" Blast marker.",
    "Apocalyptic Blast": "A weapon with this special rule uses the 10\" Blast marker.",
    "Apocalyptic Barrage (X)": (
        "Resolve a number of Large Blast markers equal to the value shown in parentheses. If the value is a dice roll, "
        "roll once to determine the number of markers. Resolve these markers using the normal Multiple Barrage rules."),
    "Titan Killer": (
        "When a Titan Killer weapon scores a Penetrating Hit against a Super-heavy Vehicle, resolve the Penetrating Hit "
        "normally and then roll a D3: the target loses that many Structure Points, to a minimum of 0. Reducing a vehicle "
        "to 0 Structure Points in this manner does not by itself destroy it; subsequent damage is resolved normally. "
        "Against a non-Vehicle model, an unsaved Wound caused by a Titan Killer weapon inflicts D3 Wounds instead of 1."),
    "Machine Destroyer": (
        "When a weapon with this special rule scores a Penetrating Hit against a Vehicle, a result of 1 on the Vehicle "
        "Damage table may be re-rolled."),
    "Divert Power": (
        "A weapon profile with this special rule may only be used if the firing vehicle did not move during its "
        "Movement phase."),
    "Stone Burner": (
        "When a weapon with this special rule scores a Penetrating Hit against a Building or Fortification, that "
        "Penetrating Hit becomes D3 Penetrating Hits."),
    "Exoshock": (
        "When a weapon with this special rule scores a Penetrating Hit against a Vehicle, roll a D6. On a 4+, the target "
        "suffers one additional automatic Penetrating Hit. This additional hit cannot itself trigger Exoshock."),
    "Heavy Beam": (
        "When firing a Heavy Beam weapon, draw a 1\" wide line from the weapon's barrel out to its maximum range. The "
        "first model touched by the beam must belong to an enemy unit. Every model whose base lies wholly or partially "
        "beneath the beam suffers one automatic hit from the weapon (a unit may suffer several hits). Vehicles are struck "
        "against the Armour facing from which the beam entered their hull."),
    "Deflagrate": (
        "After resolving the weapon's attacks, count the number of unsaved Wounds caused. Immediately resolve that many "
        "additional automatic hits against the same unit using the same weapon profile. Hits generated by Deflagrate "
        "cannot themselves generate further hits."),
    "Heliothermic Detonation": (
        "If a non-Vehicle model suffers one or more unsaved Wounds from this weapon and survives, it must immediately "
        "pass a Toughness Test or suffer Instant Death. If the weapon scores a Penetrating Hit against a Vehicle, add +1 "
        "to the subsequent Vehicle Damage table roll."),
    "Sunder": "A weapon with this special rule may re-roll failed Armour Penetration rolls against Vehicles.",
    "Indirect Only": (
        "A weapon with this special rule does not require Line of Sight. It is always resolved using the Barrage rules "
        "and may not be fired directly at a target."),
    "Shock Pulse": (
        "If a Vehicle suffers a Penetrating Hit from a weapon with this special rule, it may only fire Snap Shots during "
        "its following Shooting phase."),
    "Feedback": (
        "Whenever a weapon with this special rule fails an Armour Penetration roll against a Vehicle, or fails a To "
        "Wound roll against a non-Vehicle model, roll a D6. On a 1 the firing model suffers dangerous energy feedback: a "
        "Vehicle suffers one Glancing Hit; a non-Vehicle model suffers one Wound with no Armour Save allowed "
        "(Invulnerable Saves may be taken normally)."),
    "Ulator Sonic Wave": (
        "When firing the Ulator Class Sonic Destructor, place the 7\" Massive Blast marker with its edge touching the "
        "front hull of the Ordinatus. Move the marker in a straight line away from the vehicle in any direction within "
        "its 45 degree forward firing arc until it reaches 72\" or leaves the table. Every model whose base is wholly or "
        "partially passed over by the marker suffers one automatic hit. The wave may pass through friendly units, "
        "terrain and units the Ordinatus cannot normally see, but the first unit in its path must be an enemy unit. "
        "Strength of each hit by target: Infantry, Jump Infantry, Jet Pack Infantry - S5; Bikes, Jetbikes, Beasts and "
        "Cavalry - S5; Monstrous Creatures and non-Tank Vehicles - S8; Tank Vehicles - S10; Super-heavy Vehicles - S10, "
        "Titan Killer; Gargantuan Creatures - S10, Titan Killer; Buildings and Fortifications - S10, Titan Killer. "
        "Flyers and Flying Monsters are also struck if the marker passes over their base."),
    # ---------------------------------------------------------------- unit rules
    "Reactor Blast": "When the Cerberus is finally destroyed, add +1 to the roll made for Catastrophic Destruction.",
    "Crushing Weight": (
        "Enemy units taking a Tank Shock Test caused by the Typhon suffer an additional -1 Leadership modifier. When the "
        "Typhon makes a Ram attack, add +1 to its Armour Penetration roll."),
    "Enhanced Defensive Fire": (
        "If at least one friendly unit is embarked within the vehicle, the vehicle may make a Stand & Shoot reaction "
        "when charged, despite Vehicles normally being unable to make Stand & Shoot reactions. Only the vehicle's "
        "sponson weapons may be fired as part of this reaction. These attacks are resolved using the normal Limited "
        "Fire rules, except that Lascannons fire at BS2. Heavy Flamers instead inflict D3+1 automatic hits against an "
        "eligible charging unit within their firing arc."),
    "Reinforced Shell": (
        "When rolling for Catastrophic Destruction, subtract 2 from the result. If the modified result is 0 or less, the "
        "Mastodon is destroyed but does not explode: its hull remains in place and is treated as a Ruin. Models embarked "
        "within suffer a Strength 4 hit. Vehicles transported within are struck against their lowest Armour Value."),
    "Loading Vehicles": (
        "While Hovering, an empty Thunderhawk Transporter may move over a stationary friendly vehicle which has not "
        "moved that turn. If it does so, that vehicle is embarked. The Transporter may move normally from its following "
        "turn onwards."),
    "Unloading Vehicles": (
        "If the Thunderhawk Transporter remains stationary while Hovering, any transported vehicles may disembark and "
        "move normally that turn."),
    "Shield Projection": (
        "If the Stormbird is Hovering and remains stationary, it may project its Void Shields at the beginning of its "
        "turn. Until the beginning of its next turn, friendly units wholly or partially within 12\" of the Stormbird's "
        "hull or wings are protected by its active Void Shields. Hits against those units must first be resolved "
        "against the projected Void Shields."),
    "Reinforced Structure": "The Stormbird has a 5+ Invulnerable Save against attacks which penetrate its Void Shields.",
    "Grav-backwash": (
        "While this vehicle is operating as a Hovering Flyer and is not Immobilised, enemy models attacking it in close "
        "combat suffer a -2 modifier to their To Hit rolls."),
    "Exposed Arachnus Capacitors": (
        "When the Ares is finally destroyed by an attack which struck its Rear Armour, add +1 to its Catastrophic "
        "Destruction roll."),
    "All Power to Weapons!": (
        "If the Stormlord remains stationary, its Vulcan Mega-Bolter may fire twice in the following Shooting phase. The "
        "two attacks may be directed at different targets."),
}

# ==================================================================================================  WEAPONS
WEAPONS = {
    # ---------------------------------------------------------------- Lords of War weapons (L366-L399)
    "Neutron Laser Battery": ('72"', "10", "1", "Ordnance D3, Blast, Twin-linked, Concussive, Shock Pulse, Feedback"),
    "Volcano Cannon": ('120"', "10", "2", "Ordnance 1, Large Blast, Titan Killer"),
    "Twin-linked Volcano Cannon": ('120"', "10", "2", "Ordnance 1, Large Blast, Titan Killer, Twin-linked"),
    "Quad Lascannon": ('48"', "9", "2", "Heavy 2, Twin-linked"),
    "Laser Destroyer": ('36"', "9", "1", "Ordnance 1, Twin-linked"),
    "Volkite Carronade": ('48"', "8", "2", "Ordnance 1, Heavy Beam, Deflagrate, Haywire, Ignores Cover"),
    "Siege Melta Array": ('12"', "9", "1", "Heavy 4, Blast, Melta, Stone Burner"),
    "Skyreaper Battery": ('48"', "7", "4", "Heavy 5, Twin-linked, Skyfire, Interceptor"),
    "Thunderhawk Cannon": ('72"', "8", "3", "Ordnance 1, Massive Blast"),
    "Turbo-laser Destructor": ('96"', "10", "2", "Ordnance 1, Large Blast, Titan Killer"),
    "Thunderhawk Cluster Bomb": ("-", "6", "4", "Bomb 6, Barrage, Large Blast, One Use"),
    "Dreadstrike Missile": ('120"', "10", "2", "Ordnance 1, Blast, One Use"),
    "Macro-bomb Cluster": ("-", "8", "3", "Bomb 1, Apocalyptic Barrage (3D6), Sunder, One Use"),
    "Orbital Strike": ("Unlimited", "10", "1", "Ordnance 1, Massive Blast, Barrage, Titan Killer, Indirect Only"),
    "Baneblade Cannon": ('72"', "9", "2", "Ordnance 1, Apocalyptic Blast"),
    "Vulcan Mega-Bolter": ('60"', "6", "3", "Heavy 15"),
    "Stormsword Siege Cannon": ('36"', "10", "1", "Ordnance 1, Apocalyptic Blast, Ignores Cover"),
    "Stormhammer Cannon": ('60"', "9", "2", "Ordnance 1, Massive Blast, Shred, Pinning"),
    "Dual Battlecannon": ('72"', "8", "3", "Ordnance 2, Large Blast, Twin-linked"),
    "Bomb": ("-", "6", "4", "Bomb 1, Blast, One Use"),
    "Hellstrike Missile": ('72"', "8", "2", "Heavy 1, Sunder, One Use"),
    # ---------------------------------------------------------------- Talons of the Emperor weapons (L408-L419)
    "Twin-linked Lastrum Bolt Cannon": ('36"', "6", "3", "Heavy 3, Twin-linked, Heliothermic Detonation"),
    "Spiculus Heavy Bolt Launcher": ('48"', "7", "4", "Heavy 3, Rending"),
    "Infernus Firebomb Cluster": ("-", "5", "4", "Bomb 3, Large Blast, Ignores Cover, One Use"),
    # ---------------------------------------------------------------- Mechanicum weapons (L421-L427)
    "Belicosa Pattern Volcano Cannon": ('180"', "10", "1", "Ordnance 1, Apocalyptic Blast, Titan Killer, "
                                                            "Machine Destroyer"),
    "Ulator Class Sonic Destructor": ('72"', "X", "2", "Ordnance 1, Ulator Sonic Wave, Pinning, Armourbane, "
                                                         "Instant Death, Ignores Cover"),
    # ---------------------------------------------------------------- not in this book (see questions)
    "Twin-linked Bolter": ('24"', "4", "5", "Rapid Fire, Twin-linked"),
    "Combi-weapon": ('24"', "4", "5", "Rapid Fire"),
    "Heavy Bolter": ('36"', "5", "4", "Heavy 3"),
    "Twin-linked Heavy Bolter": ('36"', "5", "4", "Heavy 3, Twin-linked"),
    "Quad Heavy Bolter": ('36"', "5", "4", "Heavy 6, Twin-linked"),
    "Heavy Flamer": ("Template", "5", "4", "Assault 1"),
    "Twin-linked Heavy Flamer": ("Template", "5", "4", "Assault 1, Twin-linked"),
    "Multi-Melta": ('24"', "8", "1", "Heavy 1, Melta"),
    "Havoc Launcher": ('48"', "5", "5", "Heavy 1, Blast, Twin-linked"),
    "Hunter-Killer Missile": ("Unlimited", "8", "3", "Heavy 1, One Use"),
    "Lascannon": ('48"', "9", "2", "Heavy 1"),
    "Twin-linked Lascannon": ('48"', "9", "2", "Heavy 1, Twin-linked"),
    "Autocannon": ('48"', "7", "4", "Heavy 2"),
    "Twin-linked Autocannon": ('48"', "7", "4", "Heavy 2, Twin-linked"),
    "Multi-laser": ('36"', "6", "6", "Heavy 3"),
    "Co-axial Multi-laser": ('36"', "6", "6", "Heavy 3"),
    "Demolisher Cannon": ('24"', "10", "2", "Ordnance 1, Large Blast"),
    "Demolisher Siege Cannon": ('24"', "10", "2", "Ordnance 1, Large Blast"),
    "Volkite Culverin": ('45"', "6", "5", "Heavy 4, Rending"),
}

MULTI = {
    "Dreadhammer Siege Cannon": {
        "Dreadhammer Siege Cannon - Standard": ('24"', "10", "1", "Ordnance 1, Massive Blast, Ignores Cover"),
        "Dreadhammer Siege Cannon - Diverted": ('48"', "10", "1", "Ordnance 1, Massive Blast, Ignores Cover, "
                                                                  "Divert Power")},
    "Plasma Blastgun": {
        "Plasma Blastgun - Rapid": ('72"', "8", "2", "Ordnance 2, Massive Blast"),
        "Plasma Blastgun - Overload": ('96"', "10", "2", "Ordnance 1, Apocalyptic Blast")},
    "Twin-linked Fellblade Accelerator Cannon": {
        "Fellblade Accelerator Cannon - HE": ('100"', "8", "3", "Ordnance 1, Massive Blast, Twin-linked"),
        "Fellblade Accelerator Cannon - AE": ('100"', "9", "2", "Heavy 1, Blast, Armourbane, Twin-linked")},
    "Arachnus Heavy Blaze Cannon": {
        "Arachnus Heavy Blaze Cannon - Concentrated": ('72"', "10", "1", "Heavy 1, Exoshock"),
        "Arachnus Heavy Blaze Cannon - Burst": ('48"', "8", "3", "Heavy 4")},
    "Arachnus Magna-Blaze Cannon": {
        "Arachnus Magna-Blaze Cannon - Concentrated": ('72"', "10", "1", "Ordnance 2, Exoshock, Master-crafted, "
                                                                         "Armourbane, Instant Death"),
        "Arachnus Magna-Blaze Cannon - Burst": ('48"', "8", "2", "Heavy 2, Large Blast")},
}

WEAPON_RULES = {
    "Neutron Laser Battery": ["Twin-Linked", "Concussive", "Shock Pulse", "Feedback"],
    "Dreadhammer Siege Cannon": ["Massive Blast", "Ignores Cover", "Divert Power"],
    "Volcano Cannon": ["Titan Killer"],
    "Twin-linked Volcano Cannon": ["Titan Killer", "Twin-Linked"],
    "Plasma Blastgun": ["Massive Blast", "Apocalyptic Blast"],
    "Twin-linked Fellblade Accelerator Cannon": ["Massive Blast", "Armourbane", "Twin-Linked"],
    "Quad Lascannon": ["Twin-Linked"], "Laser Destroyer": ["Twin-Linked"],
    "Volkite Carronade": ["Heavy Beam", "Deflagrate", "Haywire", "Ignores Cover"],
    "Siege Melta Array": ["Melta", "Stone Burner"],
    "Skyreaper Battery": ["Twin-Linked", "Skyfire", "Interceptor"],
    "Thunderhawk Cannon": ["Massive Blast"],
    "Turbo-laser Destructor": ["Titan Killer"],
    "Thunderhawk Cluster Bomb": ["Bomb", "Bomb X"],
    "Macro-bomb Cluster": ["Bomb", "Apocalyptic Barrage (X)", "Sunder"],
    "Orbital Strike": ["Massive Blast", "Titan Killer", "Indirect Only"],
    "Baneblade Cannon": ["Apocalyptic Blast"],
    "Stormsword Siege Cannon": ["Apocalyptic Blast", "Ignores Cover"],
    "Stormhammer Cannon": ["Massive Blast", "Shred", "Pinning"],
    "Dual Battlecannon": ["Twin-Linked"],
    "Bomb": ["Bomb"],
    "Hellstrike Missile": ["Sunder"],
    "Arachnus Heavy Blaze Cannon": ["Exoshock"],
    "Twin-linked Lastrum Bolt Cannon": ["Twin-Linked", "Heliothermic Detonation"],
    "Spiculus Heavy Bolt Launcher": ["Rending"],
    "Arachnus Magna-Blaze Cannon": ["Exoshock", "Master-Crafted", "Armourbane"],
    "Infernus Firebomb Cluster": ["Bomb", "Bomb X", "Ignores Cover"],
    "Belicosa Pattern Volcano Cannon": ["Apocalyptic Blast", "Titan Killer", "Machine Destroyer"],
    "Ulator Class Sonic Destructor": ["Ulator Sonic Wave", "Pinning", "Armourbane", "Ignores Cover"],
    "Twin-linked Bolter": ["Twin-Linked"], "Twin-linked Heavy Bolter": ["Twin-Linked"],
    "Quad Heavy Bolter": ["Twin-Linked"], "Twin-linked Heavy Flamer": ["Twin-Linked"],
    "Multi-Melta": ["Melta"], "Havoc Launcher": ["Twin-Linked"], "Twin-linked Lascannon": ["Twin-Linked"],
    "Twin-linked Autocannon": ["Twin-Linked"], "Volkite Culverin": ["Rending"],
}

WARGEAR = {
    # ---------------------------------------------------------------- Lords of War armoury (L248-L364)
    "Armoured Ceramite": ("Weapons with the Melta special rule do not roll an additional D6 for Armour Penetration "
                          "against a vehicle equipped with Armoured Ceramite."),
    "Flare Shield": (
        "Reduce the Strength of shooting attacks which strike the vehicle's Front Armour by 1. If the attacking weapon "
        "has the Blast or Template type, reduce its Strength by 2 instead. A Flare Shield has no effect against close "
        "combat attacks, Haywire attacks or weapons with the Titan Killer special rule."),
    "Void Shield": (
        "A Void Shield has Armour Value 12. While one or more Void Shields remain active, resolve shooting hits against "
        "the protected vehicle one at a time. Each hit is resolved against an active Void Shield before it can strike "
        "the vehicle itself. A Glancing or Penetrating Hit immediately collapses one Void Shield; subsequent hits are "
        "resolved against any remaining active Void Shields. At the end of each controlling player's turn, roll a D6 for "
        "each collapsed Void Shield; on a 5+ that shield is restored."),
    "Chaff Launcher": (
        "Once per battle, when the vehicle suffers a Glancing or Penetrating Hit caused by a Missile weapon, the "
        "controlling player may activate the Chaff Launcher. Roll a D6; on a 4+ the hit is ignored."),
    "Armoured Cockpit": ("Whenever a vehicle with an Armoured Cockpit suffers a Crew Shaken or Crew Stunned result, "
                         "roll a D6. On a 4+, that result is ignored."),
    "Illum Flares": (
        "A Flyer equipped with Illum Flares may drop one flare during each friendly Movement phase in the same manner as "
        "a Bomb. After resolving Scatter, place a marker where the flare lands; it remains until the end of the turn. "
        "Friendly units firing at an enemy unit with at least one model within 12\" of the marker gain Night Vision for "
        "that Shooting phase."),
    "Ramjet Diffraction Grid": (
        "Reduce the Strength of shooting attacks which strike the vehicle's Side or Rear Armour by 1, to a minimum of "
        "Strength 1. A vehicle equipped with a Ramjet Diffraction Grid may not claim Cover Saves granted by Night "
        "Fighting."),
    "Eclipse Shield": (
        "Reduce the Strength of shooting attacks which strike the vehicle's Front Armour by 1 (by 2 if the attacking "
        "weapon has the Blast or Template type). In addition, if a shooting attack against the vehicle's Front Armour "
        "inflicts a Glancing or Penetrating Hit, the vehicle gains Shrouded against all subsequent shooting attacks "
        "which strike its Front Armour during the remainder of that phase. No effect against close combat attacks, "
        "Haywire attacks or weapons with the Titan Killer special rule.", ["Shrouded"]),
    "Macro Arae-shrike": (
        "Deep Strike Interference: if an enemy unit attempts to Deep Strike within 12\" of the vehicle, roll a D6 before "
        "resolving its landing; on a 4+ that unit suffers a Deep Strike Mishap (even units which would normally avoid "
        "scattering or ignore Deep Strike Mishaps). Targeting Interference: when a Barrage weapon targets the vehicle, "
        "roll one additional D6 when determining Scatter distance and use the highest two dice (a Hit result on the "
        "Scatter die remains a Hit). Interception Interference: whenever an enemy unit attempts to make an Interceptor "
        "attack against the vehicle, roll a D6; on a 1-3 the Interceptor attack may not be made, on a 4+ it proceeds "
        "normally."),
    "Blessed Autosimulacra": (
        "At the end of the controlling player's turn, if the vehicle has lost one or more Structure Points, roll a D6. "
        "On a 6, restore one lost Structure Point, up to the vehicle's starting total."),
    "Anbaric Claw": (
        "An Anbaric Claw may be activated once per player turn when the vehicle is being attacked in close combat, or "
        "when it is Ramming or being Rammed. When activated, every unit, friend or foe, with at least one model within "
        "1\" of the vehicle's hull suffers D6 Strength 5 AP4 hits with the Rending special rule (models embarked inside "
        "Vehicles are unaffected). If activated during close combat, resolve these hits at Initiative 10; if activated "
        "during a Ram, resolve them simultaneously with the hits caused by the Ram.", ["Rending"]),
    "Ordinatus Dispersion Shield": (
        "Protects the vehicle against shooting attacks which strike its Front or Side Armour, and against Barrage "
        "attacks regardless of the Armour facing struck. First turn the Ordinatus is on the battlefield: reduce the "
        "Strength of affected shooting attacks by 3; Titan Killer attacks inflict only 1 Structure Point of additional "
        "damage instead of D3. Second turn: reduce the Strength of affected attacks by 2; reduce Structure Point damage "
        "inflicted by Titan Killer by 1, to a minimum of 1. Third and subsequent turns: reduce the Strength of affected "
        "attacks by 1; Titan Killer functions normally. Strength may never be reduced below 1."),
    "Auxiliary Drive": (
        "At the start of the vehicle's Movement phase, if it is Immobilised, roll a D6. On a 4+, remove the Immobilised "
        "result and the vehicle may move normally that turn."),
    # ---------------------------------------------------------------- unit wargear
    "Dual Void Shield Generator": (
        "The vehicle is protected by two independent Void Shields, each with Armour Value 12. While one or more Void "
        "Shields remain active, resolve shooting hits against the vehicle one at a time; each hit is resolved against "
        "an active Void Shield at Armour Value 12. A Glancing or Penetrating Hit immediately collapses one shield; "
        "subsequent hits are resolved against any remaining active shields before they can strike the vehicle itself. "
        "At the end of each controlling player's turn, roll a D6 for each collapsed Void Shield; on a 5+ that shield is "
        "restored."),
    "Command Vox Relay": (
        "While the vehicle is on the battlefield, the controlling player may add +1 to or subtract 1 from their Reserve "
        "rolls. In addition, when an enemy unit suffers a Deep Strike Mishap, the controlling player may reposition the "
        "enemy unit up to 18\" from its intended target location instead of the normal 12\". All other Deep Strike "
        "Mishap rules apply normally."),
    "Targeters": "Two sponson Lascannons fitted with Targeters gain +1 BS for those weapons.",
    "Power of the Machine Spirit": ("The vehicle has the Power of the Machine Spirit special rule.",
                                    ["Power of the Machine Spirit"]),
    # not described in this book (standard ProHammer vehicle equipment)
    "Searchlight": ("Searchlight (see the ProHammer Core Rules).", ["Searchlight"]),
    "Smoke Launchers": ("Smoke Launchers (see the ProHammer Core Rules).", ["Smoke Launchers"]),
    "Extra Armour": ("Extra Armour (see the ProHammer Core Rules).", ["Extra Armour"]),
    "Combi-weapon": ("A Combi-weapon consists of a Bolter and a secondary weapon. The Bolter may be fired normally "
                     "throughout the battle; the secondary weapon may be fired once per battle. Both may not be fired in "
                     "the same Shooting phase. (The secondary weapon is not specified in the Lords of War book.)"),
}

# shared option lists
PINTLE_A = [("Twin-linked Bolter", 5), ("Combi-weapon", 5), ("Heavy Bolter", 10), ("Heavy Flamer", 10),
            ("Multi-Melta", 15), ("Havoc Launcher", 15)]                           # Cerberus, Typhon, Stormblade
PINTLE_FALCHION = [("Twin-linked Bolter", 5), ("Combi-weapon", 10), ("Heavy Flamer", 15), ("Havoc Launcher", 15),
                   ("Heavy Bolter", 15), ("Multi-Melta", 20)]
PINTLE_FELLBLADE = [("Twin-linked Bolter", 5), ("Combi-weapon", 10), ("Heavy Flamer", 15), ("Heavy Bolter", 15),
                    ("Multi-Melta", 20)]
PINTLE_BANEBLADE = [("Twin-linked Bolter", 5), ("Combi-weapon", 10), ("Heavy Flamer", 15), ("Heavy Bolter", 15),
                    ("Multi-laser", 15), ("Multi-Melta", 20)]
FLYER_UPGRADES = [("Chaff Launcher", 10), ("Armoured Cockpit", 15), ("Flare Shield", 50),
                  ("Ramjet Diffraction Grid", 50)]


# ==================================================================================================  HELPERS
def counted_links(eid, items):
    """Links to shared items, each with an exact count (items may repeat)."""
    out = []
    for it in dict.fromkeys(items):
        n = items.count(it)
        lid = uid("link", eid, it)
        out.append(link(lid, W(it), it, constraints=[constraint(uid(lid, "min"), "min", n),
                                                     constraint(uid(lid, "max"), "max", n)]))
    return out


def inline(key, name, cost, items, max_=1):
    """Inline option entry carrying one or more linked items (e.g. a sponson pair)."""
    eid = uid(key, "inline", name)
    return entry(eid, name, cost=cost, links=counted_links(eid, items),
                 constraints=[constraint(uid(eid, "max"), "max", max_, auto=True)])


def pick(key, title, entries, max_total=1):
    """Optional group of inline entries (0..max_total)."""
    gid = uid("grp", key, title)
    return group(gid, title, entries=entries, constraints=[constraint(uid(gid, "max"), "max", max_total, auto=True)])


def swap(key, title, default_name, default_items, options):
    """Exactly-one replacement of a set of weapons. options: [(name, pts, items)]."""
    d = inline(key, default_name, 0, default_items)
    return slot(key, title, None, [(inline(key, n, p, its), None) for n, p, its in options], default_is_entry=d)


def sponsons(u, swap_flamer=False):
    """'Up to two pairs of side sponsons, each containing one Lascannon and one Twin-linked Heavy Bolter' (+50 per
    pair). swap_flamer: 'any sponson Twin-linked Heavy Bolter may be replaced with a Twin-linked Heavy Flamer'."""
    hb, hf = "Twin-linked Heavy Bolter", "Twin-linked Heavy Flamer"
    opts = [inline(u, "Sponson Pair (Lascannon + Twin-linked Heavy Bolter each)", 50, ["Lascannon"] * 2 + [hb] * 2, 2)]
    if swap_flamer:
        opts += [inline(u, "Sponson Pair (one Twin-linked Heavy Bolter swapped for a Twin-linked Heavy Flamer)", 50,
                        ["Lascannon"] * 2 + [hb, hf], 2),
                 inline(u, "Sponson Pair (Lascannon + Twin-linked Heavy Flamer each)", 50, ["Lascannon"] * 2 + [hf] * 2,
                        2)]
    return pick(u, "Side Sponsons (up to two pairs)", opts, 2)


def set_char(prof, ptype, char, value, conds):
    prof.insert(0, wrap("modifiers", [modifier("set", gs.char_id(ptype, char), value, conds=conds)]))


def up_id(u, name):
    return uid(u, "upgrade", name)


def command_tank(u, cost):
    return upgrade(u, "Super-heavy Command Tank", cost, rules_=["Super-heavy Command Tank"])


def legion_crew(u):
    return upgrade(u, "Space Marine Legion Crew", 15, rules_=["Space Marine Legion Crew"])


def lord(name, cost, prof_name, ut, bs, f, s, r, sp, kit, rules_=(), groups=(), entries=(), available=AV_EM,
         transport=None, bs_up=None):
    """One Lords of War unit (a single super-heavy vehicle / flyer).
    sp: Structure Points (None = not listed). bs_up: upgrade name that sets BS to 4. transport: (cap, access, fire)."""
    u = k("unit", name)
    sp_txt = f"{sp} Structure Points" if sp else "Structure Points not listed"
    prof = vehicle_profile(u, prof_name, f"Vehicle ({ut}), {sp_txt}", bs, f, s, r)
    if bs_up:
        set_char(prof, "Vehicle", "BS", 4, [has(up_id(u, bs_up), u)])
    profiles = [prof]
    if transport:
        profiles.append(transport_profile(u, prof_name, *transport))
    e = unit(name, cost, LOW, "Lords of War", key=u, profiles=profiles, rules_=[available] + SH_RULES + list(rules_),
             groups=list(groups), entries=list(entries))
    # weapons/wargear with counts
    from legiones2 import add_to
    add_to(e, "entryLinks", counted_links(u, kit))
    return e


# ==================================================================================================  LEGIONES ASTARTES
def cerberus():
    name = "Legion Cerberus Heavy Tank Destroyer"
    u = k("unit", name)
    return lord(name, 395, "Legion Cerberus", "Tank, Super-heavy", 4, 14, 14, 13, 3,
                ["Neutron Laser Battery", "Searchlight", "Smoke Launchers", "Flare Shield"],
                rules_=["Reactor Blast"], available=AV_LEGION,
                groups=[pick(u, "Sponsons (one pair)", [inline(u, "Heavy Bolter Sponsons", 20, ["Heavy Bolter"] * 2),
                                                        inline(u, "Lascannon Sponsons", 40, ["Lascannon"] * 2)]),
                        take(u, "Vehicle Upgrades", [("Hunter-Killer Missile", 5), ("Armoured Ceramite", 20)]),
                        take(u, "Pintle-mounted Weapon", PINTLE_A, max_total=1)])


def typhon():
    name = "Legion Typhon Heavy Siege Tank"
    u = k("unit", name)
    return lord(name, 395, "Legion Typhon", "Tank, Super-heavy", 4, 14, 14, 14, 3,
                ["Dreadhammer Siege Cannon", "Searchlight", "Smoke Launchers"],
                rules_=["Crushing Weight"], available=AV_LEGION,
                groups=[pick(u, "Sponsons (one pair)", [inline(u, "Heavy Bolter Sponsons", 20, ["Heavy Bolter"] * 2),
                                                        inline(u, "Lascannon Sponsons", 40, ["Lascannon"] * 2)]),
                        take(u, "Vehicle Upgrades", [("Hunter-Killer Missile", 5), ("Armoured Ceramite", 20)]),
                        take(u, "Pintle-mounted Weapon", PINTLE_A, max_total=1)])


def falchion():
    name = "Legion Falchion Super-heavy Tank Destroyer"
    u = k("unit", name)
    nwc = upgrade(u, "Neutron Wave Capacitor", 35,
                  text="The Falchion's Volcano Cannon gains Shock Pulse and Feedback.")
    from legiones2 import add_to
    add_to(nwc, "infoLinks", rules_links(["Shock Pulse", "Feedback"], key=nwc.get("id")))
    return lord(name, 525, "Falchion", "Tank, Super-heavy", 3, 14, 13, 12, 3,
                ["Twin-linked Volcano Cannon", "Quad Lascannon", "Quad Lascannon", "Searchlight", "Smoke Launchers"],
                available=AV_LEGION, bs_up="Space Marine Legion Crew",
                groups=[take(u, "Vehicle Upgrades", [("Hunter-Killer Missile", 5), ("Auxiliary Drive", 10),
                                                     ("Armoured Ceramite", 25)]),
                        take(u, "Pintle-mounted Weapon", PINTLE_FALCHION, max_total=1)],
                entries=[legion_crew(u), nwc])


def legion_stormblade():
    name = "Legion Stormblade Super-heavy Tank"
    u = k("unit", name)
    return lord(name, 455, "Legion Stormblade", "Tank, Super-heavy", 3, 14, 13, 12, 3,
                ["Plasma Blastgun", "Heavy Bolter", "Searchlight", "Smoke Launchers"],
                available=AV_LEGION, bs_up="Space Marine Legion Crew",
                groups=[sponsons(u, swap_flamer=True),
                        take(u, "Vehicle Upgrades", [("Hunter-Killer Missile", 5), ("Armoured Ceramite", 25)]),
                        take(u, "Pintle-mounted Weapon", PINTLE_A, max_total=1)],
                entries=[command_tank(u, 25), legion_crew(u)])


def fellblade_glaive(u, rest):
    """Shared Fellblade/Glaive swaps: Quad Lascannon sponsons -> Laser Destroyer sponsons; TL HB -> TL HF."""
    return [swap(u, "Sponson Weapons", "Two Quad Lascannon Sponsons", ["Quad Lascannon"] * 2,
                 [("Two Laser Destroyer Sponsons", 0, ["Laser Destroyer"] * 2)]),
            slot(u, "Replace Twin-linked Heavy Bolter", "Twin-linked Heavy Bolter", [("Twin-linked Heavy Flamer", 0)]),
            take(u, "Vehicle Upgrades", [("Hunter-Killer Missile", 5), ("Armoured Ceramite", 25)])] + rest


def fellblade():
    name = "Legion Fellblade Super-heavy Tank"
    u = k("unit", name)
    return lord(name, 525, "Fellblade", "Tank, Super-heavy", 3, 14, 13, 12, 3,
                ["Twin-linked Fellblade Accelerator Cannon", "Demolisher Siege Cannon", "Searchlight",
                 "Smoke Launchers"],
                available=AV_LEGION, bs_up="Space Marine Legion Crew",
                groups=fellblade_glaive(u, [take(u, "Pintle-mounted Weapon", PINTLE_FELLBLADE, max_total=1)]),
                entries=[command_tank(u, 25), legion_crew(u)])


def glaive():
    name = "Legion Glaive Super-heavy Special Weapons Tank"
    u = k("unit", name)
    return lord(name, 625, "Glaive", "Tank, Super-heavy", 4, 14, 13, 12, 3,
                ["Volkite Carronade", "Searchlight", "Smoke Launchers"],
                available=AV_LEGION, groups=fellblade_glaive(u, []))


def mastodon():
    name = "Legion Mastodon Heavy Assault Transport"
    u = k("unit", name)
    return lord(name, 700, "Mastodon", "Tank, Super-heavy", 4, 14, 14, 14, 4,
                ["Siege Melta Array", "Heavy Flamer", "Heavy Flamer", "Lascannon", "Lascannon", "Smoke Launchers",
                 "Searchlight", "Armoured Ceramite", "Void Shield", "Void Shield"],
                rules_=["Assault Vehicle", "Enhanced Defensive Fire", "Reinforced Shell"], available=AV_LEGION,
                transport=("40 models; up to two Dreadnoughts, each counting as 10 models",
                           "One front access point, one rear access point", "None"),
                groups=[slot(u, "Replace Skyreaper Battery", "Skyreaper Battery", [("Command Vox Relay", 25)]),
                        take(u, "Vehicle Upgrades", [("Hunter-Killer Missile", 5, 4)])],
                entries=[command_tank(u, 20)])


def thunderhawk_transporter():
    name = "Legion Thunderhawk Transporter"
    u = k("unit", name)
    vch = upgrade(u, "Void-crafted Hull", 35, text="Increase the Thunderhawk Transporter's Rear Armour from 10 to 12.")
    e = lord(name, 400, "Thunderhawk Transporter", "Super-heavy, Flyer, Hover, Transport", 4, 12, 12, 10, 3,
             ["Twin-linked Heavy Bolter"] * 4 + ["Armoured Ceramite"],
             rules_=["Loading Vehicles", "Unloading Vehicles"], available=AV_LEGION,
             transport=("15 models; in addition either two Rhino-sized vehicles or one Land Raider-sized vehicle "
                        "(transported vehicles may contain passengers)",
                        "One access hatch on each side of the cockpit section", "None"),
             groups=[take(u, "Upgrades", FLYER_UPGRADES[:2] + [("Illum Flares", 5)] + FLYER_UPGRADES[2:]),
                     take(u, "Hellstrike Missiles", [("Hellstrike Missile", 10, 6)])],
             entries=[vch])
    set_char(e.find("profiles")[0], "Vehicle", "Rear", 12, [has(vch.get("id"), u)])
    return e


def thunderhawk_gunship():
    name = "Legion Thunderhawk Gunship"
    u = k("unit", name)
    vch = upgrade(u, "Void-crafted Hull", 35, text="Increase the Thunderhawk's Rear Armour from 10 to 12.")
    e = lord(name, 685, "Thunderhawk Gunship", "Super-heavy, Flyer, Hover, Transport", 4, 12, 12, 10, 3,
             ["Twin-linked Heavy Bolter"] * 4 + ["Lascannon", "Lascannon", "Armoured Ceramite",
                                                 "Power of the Machine Spirit"],
             rules_=["Assault Vehicle"], available=AV_LEGION,
             transport=("30 models; may transport Dreadnoughts (each counting as 10 models, forward ramp only), Jump "
                        "Infantry and Bikes", "One access hatch on each side, one forward assault ramp", "None"),
             groups=[slot(u, "Replace Thunderhawk Cannon", "Thunderhawk Cannon", [("Turbo-laser Destructor", 90)]),
                     swap(u, "Missiles / Bombs", "Six Hellstrike Missiles", ["Hellstrike Missile"] * 6,
                          [("Six Thunderhawk Cluster Bombs", 60, ["Thunderhawk Cluster Bomb"] * 6)]),
                     take(u, "Upgrades", FLYER_UPGRADES)],
             entries=[vch])
    set_char(e.find("profiles")[0], "Vehicle", "Rear", 12, [has(vch.get("id"), u)])
    return e


def stormbird():
    name = "Sokar Pattern Stormbird"
    u = k("unit", name)
    turrets = [slot(u, f"Twin-linked Lascannon Turret {i}", "Twin-linked Lascannon", [("Quad Heavy Bolter", 0)])
               for i in range(1, 5)]
    return lord(name, 850, "Sokar Stormbird", "Super-heavy, Flyer, Hover, Transport", 4, 14, 13, 12, 4,
                ["Twin-linked Heavy Bolter"] * 3 + ["Armoured Ceramite", "Power of the Machine Spirit",
                                                    "Dual Void Shield Generator"],
                rules_=["Assault Vehicle", "Shield Projection", "Reinforced Structure"], available=AV_LEGION,
                transport=("50 models; may transport Dreadnoughts of any type (10 models each), Jump Infantry, Rapier "
                           "Batteries, Bikes, Jetbikes and one Rhino including its passengers (25 models; an exception "
                           "to the single-unit rule). Dreadnoughts and a Rhino use the rear ramp only",
                           "One side access point on each side, one rear assault ramp", "None"),
                groups=turrets + [
                    swap(u, "Missiles", "Six Dreadstrike Missiles", ["Dreadstrike Missile"] * 6,
                         [("Macro-bomb Cluster Payload", 50, ["Macro-bomb Cluster"])]),
                    take(u, "Orbital Strike", [("Orbital Strike", 150)])])


# ==================================================================================================  TALONS
def orion():
    name = "Orion Assault Dropship"
    return lord(name, 615, "Orion Assault Dropship", "Super-heavy, Flyer, Hover, Transport", 5, 13, 12, 11, None,
                ["Arachnus Heavy Blaze Cannon"] * 2 + ["Twin-linked Lastrum Bolt Cannon"] * 2 +
                ["Spiculus Heavy Bolt Launcher"] * 2 +
                ["Extra Armour", "Armoured Ceramite", "Armoured Cockpit", "Eclipse Shield", "Macro Arae-shrike"],
                rules_=["Assault Vehicle", "Deep Strike", "Grav-backwash"], available=AV_TALONS,
                transport=("24 models; may transport a single Custodes Contemptor-Achillus or Contemptor-Galatus "
                           "Dreadnought (counts as 10 models)", "One rear access ramp", "None"))


def ares():
    name = "Ares Gunship"
    return lord(name, 640, "Ares Gunship", "Super-heavy, Flyer, Hover, Transport", 5, 13, 12, 10, None,
                ["Arachnus Heavy Blaze Cannon"] * 2 + ["Arachnus Magna-Blaze Cannon"] +
                ["Infernus Firebomb Cluster"] * 2 +
                ["Extra Armour", "Armoured Ceramite", "Armoured Cockpit", "Eclipse Shield", "Macro Arae-shrike"],
                rules_=["Deep Strike", "Grav-backwash", "Exposed Arachnus Capacitors"], available=AV_TALONS)


# ==================================================================================================  EXERCITUS ET MECHANICUS
def ordinatus(name, cost, gun):
    return lord(name, cost, name, "Tank, Super-heavy", 4, 14, 13, 13, 5,
                [gun] + ["Volkite Culverin"] * 3 + ["Blessed Autosimulacra", "Anbaric Claw", "Armoured Ceramite",
                                                    "Ordinatus Dispersion Shield"],
                rules_=["Ordinatus Reactor Meltdown", "Reinforced Ordinatus Chassis"])


def targeters(u):
    """'Two sponson Lascannons may be fitted with Targeters (+1 BS for those weapons) - Free' (needs sponsons)."""
    t = take(u, "Sponson Lascannon Targeters", [("Targeters", 0)])
    gid = uid("grp", u, "Side Sponsons (up to two pairs)")
    from legiones2 import add_mods
    add_mods(t, [error_if("Targeters need at least one pair of side sponsons.",
                          [cond(gid, u, "lessThan", 1)]),
                 modifier("set", "hidden", "true", conds=[cond(gid, u, "lessThan", 1)])])
    return t


def eh_upgrades(u):
    return take(u, "Vehicle Upgrades", [("Hunter-Killer Missile", 10), ("Armoured Ceramite", 25)])


def baneblade():
    name = "Baneblade Super-heavy Battle Tank"
    u = k("unit", name)
    return lord(name, 535, "Baneblade", "Tank, Super-heavy", 3, 14, 13, 12, 3,
                ["Baneblade Cannon", "Autocannon", "Demolisher Cannon", "Twin-linked Heavy Bolter", "Searchlight",
                 "Smoke Launchers"],
                groups=[eh_upgrades(u), sponsons(u), take(u, "Pintle-mounted Weapon", PINTLE_BANEBLADE, max_total=1)],
                entries=[command_tank(u, 25)])


def stormlord():
    name = "Stormlord Super-heavy Assault Tank"
    u = k("unit", name)
    return lord(name, 490, "Stormlord", "Tank, Super-heavy, Transport", 3, 14, 13, 12, 3,
                ["Vulcan Mega-Bolter", "Twin-linked Heavy Bolter", "Heavy Bolter", "Heavy Bolter", "Searchlight",
                 "Smoke Launchers"],
                rules_=["All Power to Weapons!"],
                transport=("40 models",
                           "Treated as Open-topped for embarking and disembarking (does not suffer the normal "
                           "additional damage modifier for being Open-topped)",
                           "Up to 20 transported models may fire from the troop bay"),
                groups=[eh_upgrades(u), sponsons(u, swap_flamer=True)], entries=[command_tank(u, 25)])


def shadowsword():
    name = "Shadowsword Super-heavy Tank Destroyer"
    u = k("unit", name)
    return lord(name, 455, "Shadowsword", "Tank, Super-heavy", 3, 14, 13, 12, 3,
                ["Volcano Cannon", "Twin-linked Heavy Bolter", "Searchlight", "Smoke Launchers"],
                groups=[eh_upgrades(u), sponsons(u), targeters(u)], entries=[command_tank(u, 25)])


def stormsword():
    name = "Stormsword Super-heavy Siege Tank"
    u = k("unit", name)
    return lord(name, 485, "Stormsword", "Tank, Super-heavy", 3, 14, 13, 12, 3,
                ["Stormsword Siege Cannon", "Searchlight", "Smoke Launchers"],
                groups=[eh_upgrades(u), sponsons(u)], entries=[command_tank(u, 25)])


def stormblade():
    name = "Stormblade Super-heavy Tank"
    u = k("unit", name)
    return lord(name, 465, "Stormblade", "Tank, Super-heavy", 3, 14, 13, 12, 3,
                ["Plasma Blastgun", "Searchlight", "Smoke Launchers"],
                groups=[eh_upgrades(u), sponsons(u), targeters(u)], entries=[command_tank(u, 25)])


def stormhammer():
    """Built from the second (complete) Stormhammer entry (L2752-L2823)."""
    name = "Stormhammer Super-heavy Assault Tank"
    u = k("unit", name)
    ml = [slot(u, f"Sponson-mounted Multi-laser {i}", "Multi-laser",
               [("Heavy Flamer", 0), ("Heavy Bolter", 0), ("Lascannon", 10)]) for i in range(1, 7)]
    tg = upgrade(u, "Targeters (BS4)", 20, text="The Stormhammer has Ballistic Skill 4.")
    e = lord(name, 555, "Stormhammer", "Tank, Super-heavy", 3, 14, 13, 12, 3,
             ["Stormhammer Cannon", "Co-axial Multi-laser", "Dual Battlecannon", "Lascannon", "Searchlight",
              "Smoke Launchers"],
             groups=ml + [take(u, "Vehicle Upgrades", [("Armoured Ceramite", 25), ("Hunter-Killer Missile", 10, 4)]),
                          take(u, "Pintle-mounted Weapon", [("Multi-laser", 10), ("Heavy Flamer", 10)], max_total=1)],
             entries=[tg, command_tank(u, 25)])
    set_char(e.find("profiles")[0], "Vehicle", "BS", 4, [has(tg.get("id"), u)])
    return e


def marauder_bomber():
    return lord("Marauder Bomber", 400, "Marauder Bomber", "Super-heavy, Flyer", 3, 10, 10, 10, 3,
                ["Twin-linked Lascannon", "Twin-linked Heavy Bolter", "Twin-linked Heavy Bolter"] + ["Bomb"] * 10,
                rules_=["Supersonic"])


def marauder_destroyer():
    return lord("Marauder Destroyer", 555, "Marauder Destroyer", "Super-heavy, Flyer", 3, 10, 10, 10, 3,
                ["Twin-linked Autocannon"] * 4 + ["Twin-linked Heavy Bolter"] + ["Bomb"] * 5 +
                ["Hellstrike Missile"] * 8,
                rules_=["Supersonic"])


# ==================================================================================================  FORCE
def low_force():
    """A Detachment holding exactly one Lords of War choice (no compulsory HQ / Troops)."""
    fid = k("force", "low")
    cl = category_link(LOW, "Lords of War", key=fid)
    cl.append(wrap("constraints", [constraint(uid(fid, "min"), "min", 1), constraint(uid(fid, "max"), "max", 1)]))
    links = [category_link(gs.CAT_CONFIG, "Configuration", key=fid), cl]
    return el("forceEntry", {"id": fid, "name": "Lords of War Detachment", "hidden": "false"},
              [wrap("categoryLinks", links)])


# ==================================================================================================  BUILD
def build():
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS, multi_profile=MULTI, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    units = [
        # Legiones Astartes
        cerberus(), typhon(), falchion(), legion_stormblade(), fellblade(), glaive(), mastodon(),
        thunderhawk_transporter(), thunderhawk_gunship(), stormbird(),
        # Talons of the Emperor
        orion(), ares(),
        # Exercitus et Mechanicus
        ordinatus("Ordinatus Sagittar", 700, "Belicosa Pattern Volcano Cannon"),
        ordinatus("Ordinatus Ulator", 1075, "Ulator Class Sonic Destructor"),
        baneblade(), stormlord(), shadowsword(), stormsword(), stormblade(), stormhammer(),
        marauder_bomber(), marauder_destroyer(),
    ]
    return catalogue(ARMY, units, force_entries=[low_force()])
