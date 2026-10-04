"""Questoris Knight Households (Imperial / Traitor Knights) - Prohammer 30k army book.

Structure: the Force Organisation slot of a Knight is set by its Household Rank, so every Household Rank is a
root unit in its slot (with the rank's points modifier as the unit cost) and contains a required choice of
Knight armour. The armour carries its profile (with the rank's characteristic modifiers already applied),
wargear and options.
"""
from armies.common import *

ARMY = "Questoris Households"

# ---------------------------------------------------------------- rules
RULES = {
    # --- army construction
    "Questoris Knight Household": (
        "A Questoris Knight Household is chosen with the normal ProHammer Force Organisation Chart (author's "
        "ruling: the normal Force Organisation applies; the book's Questoris Knight Crusade chart of HQ 1-2, Troops "
        "1-5, Elites 0-3, Fast Attack 0-2, Heavy Support 0-2 is not used). "
        "Every Knight must be given a Household Rank, which decides its Force Organisation slot and may modify its "
        "points, characteristics, shield save and special rules (applied after choosing the Knight armour and its "
        "normal equipment). Unless stated otherwise any Knight armour may be piloted by any Household Rank, and the "
        "rank does not change the weapons or equipment available to the armour. Any extra requirement of a rank, "
        "armour, unit entry or special rule must also be obeyed."),
    "The Household": (
        "All Knights of the same Questoris Knight Household Detachment are members of the same Household. Rules that "
        "affect friendly Household Knights only affect Knights of the same Detachment unless stated otherwise. "
        "Household Ranks and special rules of one Detachment do not affect Knights of another Detachment; each "
        "Detachment must fulfil its own compulsory selections."),
    "Knights and ProHammer Vehicle Rules": (
        "Knights are Vehicles and use the normal Vehicle and Walker rules of ProHammer Classic except where modified. "
        "Hull Points are not used - Knights use the Structure Points listed in their entry. All Knights are "
        "Super-heavy Walkers unless stated otherwise. Knights use normal Line of Sight and weapon firing arcs and do "
        "not use the minimum range or targeting restrictions of Titans; they may fire at nearby enemy units normally "
        "unless a weapon has its own minimum range or another rule states otherwise. Rules written for later "
        "editions of Warhammer 40,000 do not apply unless reproduced in this army list."),
    "Lords of War (Questoris Households)": (
        "Lords of War may only be included "
        "where the mission permits it or both players agree; no army may contain more than one Lord of War. A "
        "Questoris Knight Household may select an eligible engine from the Collegia Titanica army list as its Lord "
        "of War. Such a Titan gains no Household Rank and uses all rules, weapons and wargear of the Collegia "
        "Titanica army list."),
    "Fortifications (Questoris Households)": (
        "Fortifications may only be included "
        "where the mission permits it or both players agree, and no army may contain more than one Fortification."),
    "The Army's Warlord (Questoris Households)": (
        "One eligible HQ Knight is nominated as the army's Warlord. If the army contains a Knight Seneschal it must "
        "be the Warlord; otherwise another eligible HQ Knight may be chosen. The Warlord selects a Warlord "
        "Trait according to the ProHammer Classic rules (random Warlord Traits from older publications are not used)."),
    "Allied Forces (Questoris Households)": (
        "A Questoris Knight Household may use Allied Detachments according to the normal ProHammer rules. An Allied "
        "Detachment may not fulfil the compulsory selections of the Primary Detachment. Household Rank rules only "
        "affect Knights of the Questoris Knight Household Detachment; Allied rules do not automatically affect "
        "Knights and Household rules do not affect allied units; allied units never gain Ion Shields, Household "
        "Ranks or other Knight-specific rules. The Allegiance of an Allied Detachment must be compatible with the "
        "Household's Allegiance unless a scenario or campaign rule states otherwise."),
    "Alternative Force Organisation (Questoris Households)": (
        "Certain Household Ranks, Knight armours or special rules may change the battlefield role of a Knight, "
        "restrict which Knight armours a rank may select, allow normally restricted Knights to fulfil compulsory "
        "selections, modify the number of Knights in a Force Organisation category, allow additional Lords of War "
        "or otherwise modify the Force Organisation Chart. These are modifications to the army list, not Formations."),
    # --- Super-heavy Walker
    "Super-heavy Walker": (
        "Knights combine the normal rules for Walkers with the durability and independent weapon systems of "
        "Super-heavy Vehicles. Unless stated otherwise a Knight: may move and fire as described by these rules; may "
        "fire Ordnance weapons without preventing its other weapons from firing; may fire different weapons at "
        "different eligible targets; uses the normal firing arc of each weapon; fights in close combat using the "
        "rules for Walkers and Super-heavy Walkers; uses Structure Points rather than Hull Points. See Structure "
        "Points, Massive Firepower, Striding War Machine, Crushing Advance, Immense Machine, Super-heavy Walker in "
        "Close Combat and Catastrophic Destruction."),
    "Structure Points": (
        "Knights use the number of Structure Points listed in their unit entry. When a Knight suffers a Wrecked or "
        "Explodes! result while it still has one or more Structure Points remaining, one Structure Point is "
        "automatically expended and the result is reduced sufficiently for the Knight to survive. Once no Structure "
        "Points remain, a subsequent Wrecked or Explodes! result destroys the Knight. A Knight may Jury-Rig damage "
        "using its remaining Structure Points as normal."),
    "Massive Firepower": (
        "A Knight may fire Ordnance weapons without preventing it from firing its other weapons that turn. A Knight "
        "automatically passes any Split Fire test; each weapon may be fired at a separate eligible target, subject "
        "to its normal range, Line of Sight and firing arc. Knights do not suffer the minimum range or targeting "
        "restrictions used by Titans."),
    "Striding War Machine": (
        "A Knight may move up to 12\" in its Movement phase and may fire all of its weapons normally whether it "
        "remained stationary or moved up to 12\". A Knight may pivot freely as part of its movement. Unless "
        "specifically permitted by another rule, a Knight may not move Flat Out."),
    "Crushing Advance": (
        "Knights ignore low walls, hedges, rubble, barricades and similarly minor obstacles when moving. Other "
        "Difficult Terrain is treated as Dangerous Terrain as normal. If a Knight fails a Dangerous Terrain test it "
        "suffers an Engine Damaged result instead of becoming Immobilised."),
    "Immense Machine": (
        "Crew Shaken: the attacker chooses one weapon carried by the Knight; that weapon may only fire using Snap "
        "Fire until the end of the Knight's next turn, the rest of the Knight operates normally. Crew Stunned: the "
        "Knight may not move during its next Movement phase and the attacker chooses one weapon which may only fire "
        "using Snap Fire until the end of the Knight's next turn; its other weapons operate normally. Engine "
        "Damaged, Weapon Destroyed, Immobilised, Wrecked and Explodes! results are resolved normally, including the "
        "use of Structure Points."),
    "Super-heavy Walker in Close Combat": (
        "Knights fight in close combat using the normal ProHammer rules for Walkers, except: a Knight may make "
        "Pursuit and Consolidation moves normally; a Knight never takes Morale or Break Tests for losing a melee "
        "engagement; Grenades and Melta Bombs used against a Knight follow the normal rules for attacking Walkers; "
        "a Knight may use any melee weapon it is equipped with according to that weapon's profile; unless stated "
        "otherwise a Knight is never prevented from attacking ordinary Infantry, Vehicles or other battlefield "
        "targets in close combat."),
    "Catastrophic Destruction": (
        "When a Knight is finally destroyed after it has no Structure Points remaining, roll a D6. 1-3 Wrecked: the "
        "Knight is destroyed and remains as a wreck. 4-5 Explosion: all models within D6\" suffer a Strength 5 AP- "
        "hit (Vehicles: Strength 5 hit against their Side Armour). 6+ Catastrophic Explosion: roll one D3 for each "
        "Structure Point the Knight had at the start of the battle and add them together; the total is the "
        "explosion radius in inches. All models within it suffer a Strength 6 AP- hit (Vehicles: Strength 6 hit "
        "against their Side Armour). Remove the Knight and replace it with an appropriately sized crater where "
        "possible."),
    "Household Rank": (
        "Every Knight in a Questoris Knight Household must possess a Household Rank. The Knight's Household Rank "
        "determines its Force Organisation role and may modify its characteristics, points cost, shield or special "
        "rules (see the Household Rank entry the Knight is selected from)."),
    "Flank Speed": (
        "During its Shooting phase a Knight with this rule may use Flank Speed instead of firing any weapons: "
        "immediately move it up to 3D6\". This move is made in the Shooting phase, may not bring the Knight within "
        "1\" of an enemy model, is not reduced by Difficult Terrain (Dangerous Terrain applies normally) and does "
        "not count as a Flat Out move. A Knight that uses Flank Speed may not charge in the same turn. A Knight that "
        "is engaged in close combat, Immobilised or otherwise unable to move may not use Flank Speed."),
    "Overtaxed Reactor": (
        "When a Knight with this rule is finally destroyed, add +1 to its Catastrophic Destruction roll. This "
        "modifier is cumulative with any other rule which modifies that roll."),
    "Macro-extinction Targeting Protocols": (
        "All ranged weapons fired by a Knight with this rule count as Twin-linked when targeting Super-heavy "
        "Vehicles, Super-heavy Walkers, Titans or Gargantuan Creatures. No additional effect on a weapon which is "
        "already Twin-linked."),
    "Volatile Reactor": (
        "When a Knight with this rule is finally destroyed, add +2 to its Catastrophic Destruction roll. This "
        "replaces the normal Overtaxed Reactor modifier if the Knight would somehow possess both rules."),
    "Knight-Atrapos Restriction": (
        "A Questoris Knight Household may include no more than one Knight-Atrapos for every full 2,000 points in "
        "the army."),
    "Acastus Household Rank Restrictions": (
        "An Acastus Knight Porphyrion or Acastus Knight Asterius may not be selected for the Scion Martial, Scion "
        "Aspirant or Scion Uhlan Household Ranks."),
    # --- Household Rank rules
    "Master Knight": (
        "Increase the Knight's Weapon Skill and Ballistic Skill by +1. In addition, improve any Invulnerable Save "
        "granted by the Knight's Ion Shield, Ionic Flare Shield or Ion Gauntlet Shield by 1 (e.g. a 4+ Ion Shield "
        "becomes a 3+ Ion Shield)."),
    "Ideal Mission Commander": (
        "If the Seneschal is the army's Warlord, the controlling player begins the battle with +1 Strategy Point. "
        "This Strategy Point is subject to all normal ProHammer restrictions for Strategy Points."),
    "Veteran Knight": "Increase the Knight's Weapon Skill and Ballistic Skill by +1.",
    "Household Banner": (
        "Knights selected as Troops choices are always considered Scoring Units in missions where objectives or "
        "areas are controlled by Scoring Units, unless the mission specifically states otherwise. If an objective "
        "would otherwise be contested between a Knight with Household Banner and one or more enemy units which are "
        "not Troops choices, the Knight controls the objective. If one or more enemy Troops choices are also "
        "contesting the objective, determine control normally."),
    "Martial Knight": (
        "A Scion Martial applies no characteristic or equipment modifiers to its Knight armour. It gains Household "
        "Banner."),
    "Aspirant": (
        "Reduce the Knight's Weapon Skill and Ballistic Skill by -1. In addition, worsen any Invulnerable Save "
        "granted by the Knight's Ion Shield, Ionic Flare Shield or Ion Gauntlet Shield by 1 (e.g. a 4+ Ion Shield "
        "becomes a 5+ Ion Shield). The Knight also gains Household Banner."),
    "Young Blood": (
        "The number of Scions Aspirant in a Questoris Knight Household may never exceed the total number of Knights "
        "possessing all other Household Ranks combined (e.g. a Household of six Knights may include no more than "
        "three Scions Aspirant)."),
    "Dolorous Charge": (
        "A Scion Dolorous may re-roll a failed Charge. In addition, when making a Pursuit move, the controlling "
        "player may re-roll the D6 used to determine the Knight's Pursuit distance; the second result must be "
        "accepted."),
    "Worthy Foe": (
        "If, during the Knight's Assault phase, the Scion Dolorous has an eligible charge target which is a Knight, "
        "Walker, Monstrous Creature, Primarch, Super-heavy Vehicle, Super-heavy Walker, Gargantuan Creature or "
        "Titan, it must attempt to charge one such enemy. If more than one eligible target exists, the controlling "
        "player chooses which one the Knight attempts to charge."),
    "Impetuous Advance": (
        "The Knight gains the Scout and Hit & Run Universal Special Rules. Reduce the Knight's Front Armour Value "
        "by -1."),
    "Uhlan's Scorn": (
        "When firing at a target more than 24\" away, all of the Knight's weapons may only fire using Snap Fire. "
        "Weapons which cannot normally fire using Snap Fire may not be fired at targets more than 24\" away."),
    "Oracle of Battle": (
        "While at least one friendly Preceptor is on the battlefield, add +1 to Reserve rolls made for units "
        "belonging to the same Questoris Knight Household Detachment. This modifier does not stack if more than one "
        "Preceptor is present."),
    "Advanced Auspex Network": (
        "The Preceptor and all friendly Household Knights within 6\" gain the Interceptor special rule."),
    "Defensive Coordination": (
        "The Preceptor and all friendly Household Knights within 6\" may make a Stand & Shoot! reaction when charged, "
        "despite Vehicles normally being unable to. The reaction follows all normal ProHammer rules for Stand & "
        "Shoot! and Limited Fire. Template weapons fired as part of this reaction inflict D3 automatic hits against "
        "the charging unit instead of using the Template; Hellstorm weapons inflict D6 automatic hits instead. All "
        "normal penalties for having made a Stand & Shoot! reaction apply."),
    "Sworn Enemy": (
        "After deployment is complete but before the first turn begins, nominate one enemy unit as the Aucteller's "
        "Sworn Enemy: the enemy Warlord, a Lord of War other than a Flyer, a Knight, a Super-heavy Vehicle, a "
        "Super-heavy Walker, a Titan or a Gargantuan Creature. If the Aucteller personally destroys its Sworn Enemy "
        "(it must cause the final damage), the controlling player gains an additional D3 Victory Points; if the "
        "Sworn Enemy is destroyed by another unit no additional Victory Points are awarded. If the Sworn Enemy "
        "remains on the battlefield at the end of the game, the opposing player gains +1 Victory Point."),
    "From Death I Strike": (
        "If the Aucteller is destroyed while engaged in close combat with its Sworn Enemy, it may make one final "
        "close combat attack before resolving Catastrophic Destruction or removing the Knight. This attack must "
        "target the Sworn Enemy, uses the Aucteller's normal Weapon Skill, may use any melee weapon the Knight is "
        "equipped with and is resolved immediately before any other effects caused by the Knight's destruction."),
    "Weapon Calibration": (
        "The Knight gains the Tank Hunters Universal Special Rule. If the Knight remained stationary during its "
        "preceding Movement phase, the controlling player may choose for all of its ranged weapons to gain the "
        "Skyfire special rule until the end of that Shooting phase, following all normal ProHammer rules for "
        "Skyfire."),
    "Wall Breaker": (
        "When this Knight scores a Glancing or Penetrating Hit against a Building or Fortification, add +1 to any "
        "subsequent roll made on the Vehicle Damage table for that hit. This is cumulative with normal modifiers "
        "such as AP1 or Ordnance."),
    "Infantry Crusher": (
        "At the end of each Assault phase in which the Knight remains engaged with one or more enemy non-Vehicle "
        "units, choose one such enemy unit: it suffers D3 automatic Strength 6 AP4 hits. These hits count towards "
        "determining the result of the melee engagement."),
    "Close Defence": (
        "The Knight has a 5+ Invulnerable Save against attacks made against it in close combat using Grenades, "
        "Melta Bombs or similar hand-placed anti-vehicle explosives. This save may be taken regardless of the "
        "facing being protected by the Knight's Ion Shield."),
    "Relentless Advance": "A Scion Implacable may not make Pursuit moves. It may Consolidate normally.",
    # --- weapon special rules
    "Massive Blast": "A weapon with this special rule uses the 7\" Blast marker.",
    "Titan Killer": (
        "When a Titan Killer weapon scores a Penetrating Hit against a Super-heavy Vehicle, resolve the Penetrating "
        "Hit normally and then roll a D3: the target loses that many Structure Points, to a minimum of 0. Reducing a "
        "vehicle to 0 Structure Points in this manner does not by itself destroy it; subsequent damage is resolved "
        "normally. Against a non-Vehicle model, an unsaved Wound caused by a Titan Killer weapon inflicts D3 Wounds "
        "instead of 1."),
    "Machine Destroyer": (
        "When a weapon with this special rule scores a Penetrating Hit against a Vehicle, a result of 1 on the "
        "Vehicle Damage table may be re-rolled. The second result must be accepted."),
    "Deflagrate": (
        "After resolving the weapon's attacks, count the number of unsaved Wounds caused. Immediately resolve that "
        "many additional automatic hits against the same unit using the same weapon profile. Hits generated by "
        "Deflagrate cannot themselves generate further hits."),
    "Sunder": "A weapon with this special rule may re-roll failed Armour Penetration rolls against Vehicles.",
    "Wrecker": (
        "A weapon with Wrecker may re-roll failed Armour Penetration rolls against Buildings, Fortifications and "
        "immobile structures. If it scores a Penetrating Hit against such a target, add +1 to the subsequent Vehicle "
        "Damage table roll."),
    "Colossal": (
        "A model fighting with a Colossal weapon makes all attacks with that weapon at Initiative 1, even if the "
        "model is a Walker or would normally ignore the effects of Unwieldy weapons."),
    "Hurl": (
        "If a Knight equipped with a Thunderstrike Gauntlet destroys an enemy Monstrous Creature or non-Super-heavy "
        "Vehicle in close combat, it may hurl the destroyed model (not a model that suffered an Explodes! result). "
        "Immediately after the attack that destroyed it, choose an eligible enemy unit within 12\" and resolve: "
        "Hurled Model - Range 12\", Strength Special, AP -, Heavy 1, Large Blast. Strength equals the Toughness of a "
        "hurled Monstrous Creature, or half the Front Armour Value of a hurled Vehicle (rounding up). Then remove the "
        "hurled model from play. Passengers of a hurled Vehicle must make an Emergency Disembarkation before it is "
        "thrown. Super-heavy Vehicles, Super-heavy Walkers, Gargantuan Creatures and Titans may never be hurled."),
    "Swift Strike": (
        "A Knight attacking with a weapon with this special rule gains +1 Initiative with that weapon during a turn "
        "in which it charged."),
    "Tempest Attack": (
        "Instead of making its normal close combat attacks, a Knight equipped with a Tempest Warblade may make a "
        "Tempest Attack, resolved at Initiative 2: every enemy model in base contact with the Knight suffers one "
        "automatic hit using the Tempest Warblade. The Knight makes no other close combat attacks during that "
        "Initiative step."),
    "Graviton Pulse": (
        "Instead of rolling To Wound normally, each non-Vehicle model under the Blast marker must roll equal to or "
        "under its Strength on a D6 or suffer one Wound (a roll of 6 always fails). Against Vehicles, resolve the "
        "weapon using its Haywire special rule. After resolving the attack, leave the Blast marker in place: until "
        "the beginning of the firing player's next turn the area it covers counts as both Difficult and Dangerous "
        "Terrain."),
    "Rad-phage": (
        "If a non-Vehicle model suffers one or more unsaved Wounds from a weapon with this special rule and "
        "survives, reduce its Toughness by 1 for the remainder of the battle. Multiple applications may not reduce "
        "a model below Toughness 1."),
    "Collapsing Singularity": (
        "Before firing a Graviton Singularity Cannon, roll a D6. On a 1 the firing Knight suffers one automatic "
        "Glancing Hit before the attack is resolved (no Cover, Ion Shield, Ionic Flare Shield or Ion Gauntlet "
        "Shield save may be taken against it); the weapon is then fired normally. On a 6 the weapon gains the "
        "Titan Killer special rule for this attack. On any other result resolve the attack normally."),
    "Hellstorm": "A weapon with a Range of Hellstorm uses the Hellstorm template.",
}

MELEE = "-"
WEAPONS = {
    # Knight ranged weapons
    "Questoris Battlecannon": ('72"', "6", "3", "Ordnance 3, Large Blast"),
    "Rapid-fire Battlecannon": ('72"', "8", "3", "Ordnance 2, Large Blast"),
    "Thermal Cannon": ('36"', "9", "1", "Heavy 1, Large Blast, Melta"),
    "Questoris-avenger Gatling Cannon": ('36"', "6", "3", "Heavy 12, Rending"),
    "Ironstorm Missile Pod": ('72"', "5", "4", "Ordnance 1, Large Blast"),
    "Twin Icarus Autocannon": ('48"', "7", "4", "Heavy 2, Twin-linked, Skyfire, Interceptor"),
    "Stormspear Rocket Pod": ('48"', "8", "3", "Heavy 3"),
    "Heavy Stubber": ('36"', "4", "6", "Heavy 3"),
    "Heavy Flamer": ("Template", "5", "4", "Assault 1"),
    "Meltagun": ('12"', "8", "1", "Assault 1, Melta"),
    "Lightning Cannon": ('48"', "7", "3", "Heavy 1, Large Blast, Rending, Shred"),
    "Phased-plasma Fusil": ('24"', "6", "3", "Salvo 2/3"),
    "Volkite Chieorovile": ('45"', "8", "3", "Heavy 5, Deflagrate"),
    "Graviton Gun": ('18"', "Special", "4", "Heavy 1, Blast, Concussive, Haywire, Graviton Pulse"),
    "Twin-linked Castigator Pattern Bolt Cannon": ('36"', "7", "3", "Heavy 8, Twin-linked"),
    "Acheron Pattern Flame Cannon": ("Hellstorm", "7", "3", "Ordnance 1"),
    "Graviton Singularity Cannon": ('36"', "8", "2",
                                    "Heavy 1, Large Blast, Armourbane, Concussive, Collapsing Singularity"),
    # Acastus weapons
    "Twin-linked Magna Lascannon": ('72"', "10", "2", "Ordnance 2, Large Blast, Twin-linked"),
    "Ironstorm Missile Battery": ('72"', "6", "4", "Ordnance 1, Massive Blast"),
    "Helios Missile Defence System": ('60"', "8", "2", "Heavy 2, Skyfire, Interceptor"),
    "Autocannon": ('48"', "7", "4", "Heavy 2"),
    "Lascannon": ('48"', "9", "2", "Heavy 1"),
    "Irad-cleanser": ("Template", "2", "5", "Assault 1, Fleshbane, Rad-phage"),
    "Karacnos Mortar Battery": ('60"', "5", "4",
                                "Heavy 3, Blast, Barrage, Fleshbane, Rad-phage, Ignores Cover, Pinning"),
    "Volkite Culverin": ('45"', "6", "5", "Heavy 4, Rending"),
    # Knight melee weapons (the book gives Strength and special rules only; author: they ignore armour saves in
    # melee like all power weapons)
    "Reaper Chainsword": (MELEE, "10", "-", "Melee, Power Weapon (ignores armour saves), Titan Killer"),
    "Thunderstrike Gauntlet": (MELEE, "10", "-", "Melee, Power Weapon (ignores armour saves), Titan Killer, Colossal, Hurl"),
    "Tempest Warblade": (MELEE, "10", "-", "Melee, Power Weapon (ignores armour saves), Sunder, Tempest Attack"),
}

MULTI = {
    "Cerastus Shock Lance": {
        "Cerastus Shock Lance": (MELEE, "10", "-", "Melee, Power Weapon (ignores armour saves), Titan Killer, Swift Strike"),
        "Cerastus Shock Lance - Shock Blast": ('18"', "7", "2", "Heavy 6, Concussive")},
    "Atrapos Lascutter": {
        "Atrapos Lascutter": (MELEE, "10", "-", "Melee, Power Weapon (ignores armour saves), Titan Killer, Wrecker"),
        "Atrapos Lascutter - Beam": ('8"', "10", "2", "Heavy 1, Titan Killer")},
    "Hekaton Siege Claw with Twin-linked Rad-cleanser": {
        "Hekaton Siege Claw": (MELEE, "10", "-", "Melee, Power Weapon (ignores armour saves), Titan Killer, Wrecker"),
        "Twin-linked Rad-cleanser": ("Template", "2", "5", "Assault 1, Twin-linked, Fleshbane, Rad-phage")},
    "Reaper Chainfist with Twin-linked Heavy Bolter": {
        "Reaper Chainfist": (MELEE, "10", "-", "Melee, Power Weapon (ignores armour saves), Titan Killer, Machine Destroyer"),
        "Twin-linked Heavy Bolter": ('36"', "5", "4", "Heavy 3, Twin-linked")},
    "Twin-linked Conversion Beam Cannon": {
        "Conversion Beam Cannon - Short": ('Up to 18"', "10", "3", "Ordnance 1, Blast, Twin-linked"),
        "Conversion Beam Cannon - Medium": ('18"-42"', "10", "2", "Ordnance 1, Large Blast, Twin-linked, Wrecker"),
        "Conversion Beam Cannon - Long": ('42"-72"', "10", "1",
                                          "Ordnance 1, Massive Blast, Twin-linked, Wrecker, Sunder")},
    "Bio-corrosive Rounds": {
        "Heavy Stubber (Bio-corrosive Rounds)": ('30"', "2", "6", "Heavy 3, Poisoned (4+)")},
}

WEAPON_RULES = {
    "Thermal Cannon": ["Melta"],
    "Questoris-avenger Gatling Cannon": ["Rending"],
    "Twin Icarus Autocannon": ["Twin-Linked", "Skyfire", "Interceptor"],
    "Meltagun": ["Melta"],
    "Lightning Cannon": ["Rending", "Shred"],
    "Volkite Chieorovile": ["Deflagrate"],
    "Graviton Gun": ["Concussive", "Haywire", "Graviton Pulse"],
    "Twin-linked Castigator Pattern Bolt Cannon": ["Twin-Linked"],
    "Acheron Pattern Flame Cannon": ["Hellstorm"],
    "Graviton Singularity Cannon": ["Armourbane", "Concussive", "Collapsing Singularity", "Titan Killer"],
    "Twin-linked Magna Lascannon": ["Twin-Linked"],
    "Ironstorm Missile Battery": ["Massive Blast"],
    "Helios Missile Defence System": ["Skyfire", "Interceptor"],
    "Irad-cleanser": ["Fleshbane", "Rad-phage"],
    "Volkite Culverin": ["Rending"],
    "Karacnos Mortar Battery": ["Fleshbane", "Rad-phage", "Ignores Cover", "Pinning"],
    "Reaper Chainsword": ["Titan Killer"],
    "Thunderstrike Gauntlet": ["Titan Killer", "Colossal", "Hurl"],
    "Tempest Warblade": ["Sunder", "Tempest Attack"],
    "Cerastus Shock Lance": ["Titan Killer", "Swift Strike", "Concussive"],
    "Atrapos Lascutter": ["Titan Killer", "Wrecker"],
    "Hekaton Siege Claw with Twin-linked Rad-cleanser": ["Titan Killer", "Wrecker", "Twin-Linked", "Fleshbane",
                                                         "Rad-phage"],
    "Reaper Chainfist with Twin-linked Heavy Bolter": ["Titan Killer", "Machine Destroyer", "Twin-Linked"],
    "Twin-linked Conversion Beam Cannon": ["Twin-Linked", "Wrecker", "Sunder", "Massive Blast"],
    "Bio-corrosive Rounds": ["Poison"],
}

WARGEAR = {
    "Ion Shield": (
        "When the Knight is deployed, and at the start of each opposing Shooting phase, declare which Armour Facing "
        "(Front, Left Side, Right Side or Rear) its Ion Shield protects, before any shooting attacks are resolved. "
        "Until the start of the opposing player's next Shooting phase the Knight has a 4+ Invulnerable Save against "
        "shooting attacks which strike the chosen facing. No protection against attacks in close combat. Household "
        "Rank modifiers to the Ion Shield save apply to this save. Ion Shields are not Void Shields: rules affecting "
        "Void Shields have no effect on them unless expressly stated."),
    "Ionic Flare Shield": (
        "When the Knight is deployed, and at the start of each opposing Shooting phase, declare which Armour Facing "
        "(Front, Left Side, Right Side or Rear) is protected. Until the start of the opposing player's next Shooting "
        "phase the Knight has a 4+ Invulnerable Save against shooting attacks which strike that facing. In addition, "
        "reduce the Strength of shooting attacks which strike the protected facing by 1, or by 2 if the attack uses "
        "a Blast, Massive Blast, Apocalyptic Blast, Template or Hellstorm marker (never below 1). The Strength "
        "reduction has no effect against Haywire attacks or Titan Killer weapons. No protection against attacks in "
        "close combat. Household Rank modifiers to the shield save apply normally."),
    "Ion Gauntlet Shield": (
        "At the start of each opposing Shooting phase choose the Front, Left Side or Right Side facing (never the "
        "Rear). Until the start of the opposing player's next Shooting phase the Knight has a 4+ Invulnerable Save "
        "against shooting attacks which strike the chosen facing. It also provides a 5+ Invulnerable Save against "
        "attacks made against the Knight in close combat, and Super-heavy Walkers and Gargantuan Creatures attacking "
        "the Knight-Lancer in close combat suffer -1 To Hit. Household Rank modifiers to the shield save apply to "
        "both the shooting and close combat Invulnerable Saves."),
    "Blessed Autosimulacra": (
        "At the end of the controlling player's turn, if the Knight has lost one or more Structure Points, roll a "
        "D6. On a 6, restore one lost Structure Point, up to the Knight's starting total."),
    "Occular Augmetics": (
        "The Knight gains Night Vision. In addition, when one of the Knight's shooting attacks made against a target "
        "within 12\" causes a roll on the Vehicle Damage table, the controlling player may re-roll a result of 1. "
        "The second result must be accepted.", ["Night Vision"]),
    "Bio-corrosive Rounds": (
        "Replaces the standard ammunition of a Heavy Stubber: the upgraded Heavy Stubber uses the profile 30\", S2, "
        "AP6, Heavy 3, Poisoned (4+) instead of its normal profile. No additional effect against Vehicles."),
}

# ---------------------------------------------------------------- ranks
# name, slot cat, slot name, cost modifier, 0-1?, WS/BS modifier, Front modifier, rules, compulsory
RANKS = [
    ("Seneschal", HQ, "HQ", 50, True, 1, 0, ["Master Knight", "Ideal Mission Commander",
                                                   "The Army's Warlord (Questoris Households)"]),
    ("Lord Scion", HQ, "HQ", 25, True, 1, 0, ["Veteran Knight"]),
    ("Scion Martial", TROOPS, "Troops", 0, False, 0, 0, ["Martial Knight", "Household Banner"]),
    ("Scion Aspirant", TROOPS, "Troops", -35, False, -1, 0, ["Aspirant", "Household Banner", "Young Blood"]),
    ("Scion Dolorous", FA, "Fast Attack", 25, False, 0, 0, ["Dolorous Charge", "Worthy Foe"]),
    ("Scion Uhlan", FA, "Fast Attack", 0, False, 0, -1, ["Impetuous Advance", "Scouts", "Hit & Run",
                                                          "Uhlan's Scorn"]),
    ("Preceptor", ELITES, "Elites", 25, False, 0, 0, ["Oracle of Battle", "Advanced Auspex Network",
                                                       "Defensive Coordination"]),
    ("Aucteller", ELITES, "Elites", 35, True, 0, 0, ["Sworn Enemy", "From Death I Strike"]),
    ("Scion Arbalester", HS, "Heavy Support", 25, False, 0, 0, ["Weapon Calibration", "Tank Hunters"]),
    ("Scion Implacable", HS, "Heavy Support", 35, False, 0, 0, ["Wall Breaker", "Infantry Crusher",
                                                                 "Close Defence", "Relentless Advance"]),
]
NO_ACASTUS = {"Scion Martial", "Scion Aspirant", "Scion Uhlan"}

KNIGHT_RULES = ["Household Rank", "Super-heavy Walker", "Structure Points", "Massive Firepower",
                "Striding War Machine", "Crushing Advance", "Immense Machine", "Super-heavy Walker in Close Combat",
                "Catastrophic Destruction"]
UT = "Vehicle (Walker, Super-heavy, Knight)"
CARAPACE = [("Ironstorm Missile Pod", 30), ("Twin Icarus Autocannon", 35), ("Stormspear Rocket Pod", 40)]
OCCULAR = [("Occular Augmetics", 10)]


def gear_n(key, name, n):
    """Fixed wargear carried n times (e.g. 'Two Heavy Stubbers')."""
    lid = uid("link", key, name, n)
    return link(lid, W(name), name, constraints=[constraint(uid(lid, "min"), "min", n),
                                                   constraint(uid(lid, "max"), "max", n, auto=True)])


def opt_link(key, title, name, pts, mx=1, mods=()):
    lid = uid("link", key, title, name)
    return link(lid, W(name), name, cost=pts or None, mods=list(mods),
                constraints=[constraint(uid(lid, "max"), "max", mx, auto=True)]), uid(lid, "max")


def opt_group(key, title, links_):
    return group(uid("grp", key, title), title, links=links_)


# ---------------------------------------------------------------- armours
# name, cost, (WS, BS, S, F, Si, R, I, A), SP, kit [(item, n)], rules, options builder
def _paladin(m):
    bio, _ = opt_link(m, "Heavy Stubber upgrades", "Bio-corrosive Rounds", 10, mx=2)
    return [slot(m, "Replace Questoris Battlecannon", "Questoris Battlecannon", [("Rapid-fire Battlecannon", 0)]),
            take(m, "Carapace weapon", CARAPACE, max_total=1),
            opt_group(m, "Heavy Stubber upgrades (either Heavy Stubber, +10 each)", [bio]),
            take(m, "Options", OCCULAR)]


def _errant(m):
    return [take(m, "Carapace weapon", CARAPACE, max_total=1),
            take(m, "Options", [("Bio-corrosive Rounds", 5), ("Occular Augmetics", 10)])]


def _stubber_bio(m, cost=10):
    """Bio-corrosive Rounds for the single Heavy Stubber - gone once the Heavy Stubber became a Meltagun."""
    melta = has(W("Meltagun"), m)
    lid = uid("link", m, "bio")
    return opt_group(m, "Heavy Stubber upgrade", [link(
        lid, W("Bio-corrosive Rounds"), "Bio-corrosive Rounds", cost=cost,
        mods=[modifier("set", uid(lid, "max"), 0, conds=[melta]), modifier("set", "hidden", "true", conds=[melta])],
        constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])])


def _warden(m):
    return [slot(m, "Replace Reaper Chainsword", "Reaper Chainsword", [("Thunderstrike Gauntlet", 10)]),
            slot(m, "Replace Heavy Stubber", "Heavy Stubber", [("Meltagun", 5)]),
            take(m, "Carapace weapon", CARAPACE, max_total=1),
            _stubber_bio(m),
            take(m, "Options", OCCULAR)]


def _gallant(m):
    return [slot(m, "Replace Heavy Stubber", "Heavy Stubber", [("Meltagun", 5)]),
            take(m, "Carapace weapon", CARAPACE, max_total=1),
            _stubber_bio(m),
            take(m, "Options", OCCULAR)]


def _crusader(m):
    bc_ids = []
    ents = []
    for bc in ("Questoris Battlecannon", "Rapid-fire Battlecannon"):
        eid = uid(m, "gatling-swap", bc)
        bc_ids.append(eid)
        ents.append(entry(eid, f"{bc} and Heavy Stubber", cost=5,
                          links=[gear(eid, bc), gear(eid, "Heavy Stubber")]))
    gat = slot(m, "Replace Questoris-avenger Gatling Cannon", "Questoris-avenger Gatling Cannon",
               [(e, None) for e in ents])
    lid = uid("link", m, "bio")
    mx = uid(lid, "max")
    bio = link(lid, W("Bio-corrosive Rounds"), "Bio-corrosive Rounds", cost=10,
               mods=[modifier("increment", mx, 1, conds=[has(i, m)]) for i in bc_ids]
               + [modifier("decrement", mx, 1, conds=[has(W("Meltagun"), m)])],
               constraints=[constraint(mx, "max", 1, auto=True)])
    return [slot(m, "Replace Heavy Stubber", "Heavy Stubber", [("Meltagun", 5)]),
            gat,
            take(m, "Carapace weapon", CARAPACE, max_total=1),
            opt_group(m, "Heavy Stubber upgrades (any Heavy Stubber, +10 each)", [bio]),
            take(m, "Options", OCCULAR)]


def _mech(m):
    return [slot(m, "Replace Reaper Chainsword", "Reaper Chainsword",
                 [("Hekaton Siege Claw with Twin-linked Rad-cleanser", 25)]),
            take(m, "Options", OCCULAR)]


def _occ(m):
    return [take(m, "Options", OCCULAR)]


def _porphyrion(m):
    return [slot(m, "Replace Autocannon (1)", "Autocannon", [("Irad-cleanser", 0), ("Lascannon", 10)]),
            slot(m, "Replace Autocannon (2)", "Autocannon", [("Irad-cleanser", 0), ("Lascannon", 10)]),
            slot(m, "Replace Ironstorm Missile Battery", "Ironstorm Missile Battery",
                 [("Helios Missile Defence System", 0)]),
            take(m, "Options", OCCULAR)]


Q = (4, 4, 10, 13, 12, 12, 4, 3)
ARMOURS = [
    ("Questoris Knight Paladin", 375, Q, 2,
     [("Two Heavy Stubbers", "Heavy Stubber", 2), ("Reaper Chainsword", None, 1), ("Ion Shield", None, 1)],
     [], _paladin),
    ("Questoris Knight Errant", 370, Q, 2,
     [("Thermal Cannon", None, 1), ("Two Heavy Stubbers", "Heavy Stubber", 2), ("Reaper Chainsword", None, 1),
      ("Ion Shield", None, 1)], [], _errant),
    ("Questoris Knight Warden", 385, Q, 2,
     [("Questoris-avenger Gatling Cannon", None, 1), ("Heavy Flamer", None, 1), ("Ion Shield", None, 1)],
     [], _warden),
    ("Questoris Knight Gallant", 335, Q, 2,
     [("Reaper Chainsword", None, 1), ("Thunderstrike Gauntlet", None, 1), ("Ion Shield", None, 1)],
     [], _gallant),
    ("Questoris Knight Crusader", 435, Q, 2,
     [("Thermal Cannon", None, 1), ("Heavy Flamer", None, 1), ("Ion Shield", None, 1)],
     [], _crusader),
    ("Questoris Knight Magaera", 395, (4, 4, 10, 13, 12, 12, 2, 3), 2,
     [("Lightning Cannon", None, 1), ("Phased-plasma Fusil", None, 1), ("Ionic Flare Shield", None, 1),
      ("Blessed Autosimulacra", None, 1)], ["Overtaxed Reactor"], _mech),
    ("Questoris Knight Styrix", 405, (4, 4, 10, 13, 12, 12, 2, 3), 2,
     [("Volkite Chieorovile", None, 1), ("Graviton Gun", None, 1), ("Ionic Flare Shield", None, 1),
      ("Blessed Autosimulacra", None, 1)], ["Overtaxed Reactor"], _mech),
    ("Cerastus Knight-Atrapos", 435, (4, 4, 10, 13, 12, 12, 4, 4), 2,
     [("Graviton Singularity Cannon", None, 1), ("Atrapos Lascutter", None, 1), ("Ionic Flare Shield", None, 1),
      ("Blessed Autosimulacra", None, 1)],
     ["Flank Speed", "Macro-extinction Targeting Protocols", "Volatile Reactor", "Knight-Atrapos Restriction"], _occ),
    ("Cerastus Knight-Lancer", 400, (4, 4, 10, 13, 12, 12, 4, 4), 2,
     [("Cerastus Shock Lance", None, 1), ("Ion Gauntlet Shield", None, 1)], ["Flank Speed"], _occ),
    ("Cerastus Knight-Castigator", 380, (4, 4, 10, 13, 12, 12, 4, 4), 2,
     [("Twin-linked Castigator Pattern Bolt Cannon", None, 1), ("Tempest Warblade", None, 1),
      ("Ion Shield", None, 1)], ["Flank Speed"], _occ),
    ("Cerastus Knight-Acheron", 415, (4, 4, 10, 13, 12, 12, 4, 4), 2,
     [("Acheron Pattern Flame Cannon", None, 1), ("Reaper Chainfist with Twin-linked Heavy Bolter", None, 1),
      ("Ion Shield", None, 1)], ["Flank Speed"], _occ),
    ("Acastus Knight Porphyrion", 560, (4, 5, 10, 14, 13, 12, 3, 3), 3,
     [("Two Twin-linked Magna Lascannons", "Twin-linked Magna Lascannon", 2), ("Ion Shield", None, 1)],
     ["Acastus Household Rank Restrictions"], _porphyrion),
    ("Acastus Knight Asterius", 540, (4, 5, 10, 14, 13, 12, 3, 3), 3,
     [("Two Twin-linked Conversion Beam Cannons", "Twin-linked Conversion Beam Cannon", 2),
      ("Karacnos Mortar Battery", None, 1), ("Two Volkite Culverins", "Volkite Culverin", 2),
      ("Ion Shield", None, 1), ("Blessed Autosimulacra", None, 1)],
     ["Acastus Household Rank Restrictions"], _occ),
]
ATRAPOS = "Cerastus Knight-Atrapos"


def rank_unit_id(rank):
    return k("unit", rank)


def armour_model(rank, mod_wsbs, mod_front, unit_id, a):
    name, cost, stats, sp, kit, rules_, opts = a
    ws, bs, s, f, si, r, i, att = stats
    mid = uid("model", unit_id, name)
    prof = sh_walker_profile(mid, name, ws + mod_wsbs, bs + mod_wsbs, s, f + mod_front, si, r, i, att, sp, ut=UT)
    links_ = []
    for item, real, n in kit:
        links_.append(gear(mid, item) if real is None else gear_n(mid, real, n))
    e = entry(mid, name, typ="model", cost=cost, profiles=[prof],
              infolinks=rules_links(rules_ + KNIGHT_RULES[1:], key=mid), links=links_, groups=opts(mid),
              constraints=[constraint(uid(mid, "max"), "max", 1, auto=True)])
    return e


def rank_unit(rank_def, atrapos_ids):
    rank, cat_, cat_name, cost, only_one, wsbs, front, rules_ = rank_def
    u = rank_unit_id(rank)
    armours = [a for a in ARMOURS if not (rank in NO_ACASTUS and a[0].startswith("Acastus"))]
    models = [armour_model(rank, wsbs, front, u, a) for a in armours]
    gid = uid(u, "armour")
    default = models[0].get("id")
    grp = group(gid, "Knight Armour", default=default, entries=models,
                constraints=[constraint(uid(gid, "min"), "min", 1, auto=True),
                             constraint(uid(gid, "max"), "max", 1, auto=True)])
    cons, mods = [], []
    if only_one:
        cons.append(unique(u, 1, "force"))
    if rank == "Scion Aspirant":
        # Young Blood: Scions Aspirant <= Knights of all other Household Ranks in the Detachment
        cid = uid(u, "youngblood")
        cons.append(constraint(cid, "max", 0, scope="force", deep=True))
        mods += [modifier("increment", cid, 1, repeats=[repeat(rank_unit_id(r[0]), "force", 1)])
                 for r in RANKS if r[0] != rank]
    return entry(u, rank, typ="unit", cost=cost, mods=mods, constraints=cons,
                 cats=_cats(u, cat_, cat_name), infolinks=rules_links(rules_ + KNIGHT_RULES[:1], key=u),
                 groups=[grp])


def _cats(u, cat_, cat_name):
    cats = [foc(cat_, cat_name, u)]
    if cat_name == "HQ":
        cats.append(category_link(COMMANDER, "Compulsory HQ Eligible", key=u))
    if cat_name == "Troops":
        cats.append(category_link(LINE, "Compulsory Troops Eligible", key=u))
    return cats


def atrapos_limits(units):
    """No more than one Knight-Atrapos for every full 2,000 points in the army (counted over every rank)."""
    ids = []
    for u in units:
        for e in u.iter("selectionEntry"):
            if e.get("name") == ATRAPOS:
                ids.append(e)
    all_ids = [e.get("id") for e in ids]
    for e in ids:
        cid = uid(e.get("id"), "atrapos-limit")
        mods = [modifier("increment", cid, 1, repeats=[repeat("any", "roster", 2000, field=PTS, deep=False)])]
        mods += [modifier("decrement", cid, 1, repeats=[repeat(o, "roster", 1)]) for o in all_ids
                 if o != e.get("id")]
        add_mods(e, mods)
        add_to(e, "constraints", [constraint(cid, "max", 0, scope="roster", deep=True)])


ARMY_RULE_NAMES = ["Questoris Knight Household", "The Household", "Knights and ProHammer Vehicle Rules",
                   "Alternative Force Organisation (Questoris Households)", "Lords of War (Questoris Households)",
                   "Fortifications (Questoris Households)", "The Army's Warlord (Questoris Households)",
                   "Allied Forces (Questoris Households)"]


def build():
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS, multi_profile=MULTI, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    alg = allegiance()
    cl = alg.find("categoryLinks")
    alg.insert(list(alg).index(cl), wrap("infoLinks", rules_links(ARMY_RULE_NAMES, key=k("army-rules"))))
    knights = [rank_unit(r, None) for r in RANKS]
    atrapos_limits(knights)
    return catalogue(ARMY, [alg] + knights, [])
