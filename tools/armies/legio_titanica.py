"""Legio Titanica (Collegia Titanica Titans) - Prohammer 30k army book.

Titans are Super-heavy Walkers. The game system has no Titan profile, so every Titan uses the Walker profile
(WS, BS, S, Front, Side, Rear, I, A); Structure Points and Void Shields are written into the profile's unit type
and the Void Shields are carried as wargear (one 'Void Shield' item per shield). Every Titan is a Lords of War
choice (see the 'Fielding Titans' rule and the questions file).
"""
from armies.common import *

ARMY = "Legio Titanica"

# ---------------------------------------------------------------- rules
RULES = {
    # --- general Titan rules
    "Fielding Titans": (
        "The Legio Titanica list does not state how Titans are fielded. In this data set every Titan is a Lords of "
        "War choice and may be taken as the Lord of War of any army that allows one (for example a Questoris Knight "
        "Household may select an eligible engine from the Collegia Titanica list as its Lord of War; such a Titan "
        "uses all rules, weapons and wargear of the Collegia Titanica list). Lords of War may only be included "
        "where the mission permits it or both players agree."),
    "Super-heavy Walker": (
        "All Titans are Super-heavy Walkers. Unless stated otherwise they use all normal rules for Super-heavy "
        "Vehicles as well as the normal rules for Walkers. Super-heavy Walkers may move up to 12\" in the Movement "
        "phase. They may fire all of their weapons regardless of how far they moved and may engage different "
        "targets with different weapons as described under Massive Firepower."),
    "Structure Points": (
        "Titans use the normal Super-heavy Vehicle rules and the number of Structure Points listed in their unit "
        "entry (shown as 'Structure Points' in the unit type of the profile)."),
    "Titan Weapon Mounts": (
        "Titan weapons are mounted on separate arms, carapace hard-points and weapon housings and may therefore "
        "engage different targets. Each weapon must have Line of Sight to its chosen target and the target must lie "
        "within the weapon's firing arc. Arm-mounted Titan weapons generally use the firing arc of the arm on which "
        "they are mounted, while carapace-mounted weapons use the firing arcs stated in the Titan's unit entry."),
    "Towering Monstrosity": (
        "Certain Titan weapon mounts have a minimum range, stated in the Titan's unit entry. A weapon may not target "
        "a unit closer than its stated minimum range. Titan close combat weapons may only be used against Vehicles, "
        "Super-heavy Vehicles, Monstrous Creatures and Gargantuan Creatures, unless otherwise stated."),
    "Void Shields": (
        "A Titan has the number of Void Shields listed in its unit entry (shown in the unit type of the profile and "
        "as Void Shield wargear). These use the normal Void Shield rules (see Void Shield in the Collegia Titanica "
        "Armoury). Hits are resolved against active Void Shields before they can strike the Titan itself."),
    "Reactor Meltdown": (
        "If a Titan suffers an Apocalyptic Explosion result when rolling for Catastrophic Destruction, its reactor "
        "goes critical. Instead of resolving the normal Apocalyptic Explosion, roll 6D6\" for the explosion radius. "
        "Every model within this distance suffers a Titan Killer hit at Strength 10 and AP1. Vehicles are struck "
        "against their Side Armour. Remove the Titan and replace it with an appropriately sized crater where "
        "possible."),
    "Immense Machine": (
        "Titans are unaffected by rules which would move, push, knock down or otherwise forcibly reposition a normal "
        "Vehicle unless the attacking rule specifically states that it affects Super-heavy Vehicles. Titans may "
        "never be Pinned and automatically pass Morale and Leadership tests unless a rule specifically states that "
        "it affects Super-heavy Vehicles or Titans."),
    # --- weapon special rules
    "Apocalypse Missile Launcher": (
        "Place the first Large Blast marker anywhere within range and Line of Sight; it does not Scatter. Place four "
        "additional Large Blast markers using the normal Multiple Barrage rules and resolve each marker using the "
        "Apocalypse Missile Launcher's profile."),
    "Inferno Gun": (
        "Place the Hellstorm template so that its narrow end is within 18\" of the weapon and its wide end is no "
        "closer than 18\" to the firing Titan. Resolve hits normally. The Inferno Gun is not affected by a Titan's "
        "normal carapace-mounted minimum range restriction."),
    "Plasma Blastgun": (
        "A Plasma Blastgun may fire using either its Rapid or Full profile each time it shoots. The firing player "
        "chooses which profile is used before selecting its target."),
    "Vortex": (
        "After determining the final position of the Blast marker: non-Vehicle models touched by the marker are "
        "removed from play regardless of remaining Wounds (Invulnerable Saves may be taken normally); Vehicles "
        "touched suffer an automatic Penetrating Hit with the Titan Killer special rule; Super-heavy Vehicles "
        "touched automatically lose D3 Structure Points; Gargantuan Creatures suffer D3 Wounds with no Armour Save "
        "allowed. A Vortex weapon affects friendly and enemy models alike."),
    "Ardex-defensor": (
        "A Titan equipped with one or more Ardex-defensor weapons may make a Stand & Shoot reaction when charged, "
        "even though Vehicles normally cannot do so. Only weapons with the Ardex-defensor special rule may be fired "
        "as part of this reaction. A Titan may not use Ardex-defensor against a charging Super-heavy Vehicle, Titan "
        "or Gargantuan Creature."),
    "Reactor Overload": (
        "Whenever a weapon with this special rule is fired, roll a D6 after resolving its attacks. On a 1, the "
        "firing Titan suffers one Glancing Hit. Void Shields may not be used against this hit."),
    "Titan Close Combat Weapons": (
        "Titan Close Combat Weapons and Arioch Power Claws may only be used against Vehicles, Super-heavy Vehicles, "
        "Monstrous Creatures and Gargantuan Creatures. When one of these weapons scores a Penetrating Hit against a "
        "Super-heavy Vehicle, resolve Titan Killer normally."),
    # --- Collegia Titanica special rules
    "Massive Blast": "A weapon with this special rule uses the 7\" Blast marker.",
    "Apocalyptic Blast": "A weapon with this special rule uses the 10\" Blast marker.",
    "Apocalyptic Barrage (X)": (
        "Resolve a number of Large Blast markers equal to the value shown in parentheses. If the value is a dice "
        "roll, roll once to determine the number of markers. Resolve these markers using the normal Multiple "
        "Barrage rules."),
    "Titan Killer": (
        "When a Titan Killer weapon scores a Penetrating Hit against a Super-heavy Vehicle, resolve the Penetrating "
        "Hit normally and then roll a D3: the target loses that many Structure Points, to a minimum of 0. Reducing a "
        "vehicle to 0 Structure Points in this manner does not by itself destroy it; subsequent damage is resolved "
        "normally. Against a non-Vehicle model, an unsaved Wound caused by a Titan Killer weapon inflicts D3 Wounds "
        "instead of 1."),
    "Machine Destroyer": (
        "When a weapon with this special rule scores a Penetrating Hit against a Vehicle, a result of 1 on the "
        "Vehicle Damage table may be re-rolled."),
    # --- unit rules
    "Agile": (
        "During its Shooting phase, the Warhound may choose one of the following: fire all of its weapons normally; "
        "fire one Primary Weapon and immediately move an additional D6\"; or fire no weapons and immediately move an "
        "additional 2D6\". Any additional movement made using this rule follows the normal movement restrictions "
        "for the Warhound."),
    "Towering Monstrosity (Reaver)": (
        "The Reaver's carapace-mounted weapon has a minimum range of 18\". A Reaver Titan's Titan Close Combat "
        "Weapon may only be used against Vehicles, Super-heavy Vehicles, Monstrous Creatures and Gargantuan "
        "Creatures."),
    "Towering Monstrosity (Warlord)": (
        "Infantry and Monstrous Creatures attacking a Warlord Titan in close combat only hit it on a roll of 6. "
        "Super-heavy Walkers and Gargantuan Creatures hit a Warlord Titan in close combat on a 5+. A Warlord Titan "
        "may never be locked in close combat and may move away from enemy models normally during its Movement "
        "phase. The Warlord Titan is immune to Haywire attacks and Dangerous Terrain. Carapace-mounted weapons may "
        "not target enemy units within 24\" of the Warlord's hull; this restriction does not apply when targeting "
        "Flyers, Flying Monstrous Creatures, Super-heavy Vehicles or Gargantuan Creatures."),
    "Reinforced Structure": (
        "Once all of its Void Shields have been penetrated, the Warlord Titan has a 5+ Invulnerable Save against any "
        "Glancing or Penetrating Hit suffered."),
    "World Burner": (
        "When firing a weapon which uses a Blast marker, the Warlord may nominate any point on the battlefield "
        "within range and Line of Sight as its target rather than targeting an enemy unit. Buildings, "
        "fortifications and areas of terrain may therefore be deliberately targeted."),
}

# ---------------------------------------------------------------- weapons (exactly as printed)
WEAPONS = {
    "Apocalypse Missile Launcher": ('24"-360"', "7", "3", "Apocalyptic Barrage (5), Barrage"),
    "Double-barrelled Turbo-laser Destructor": ('96"', "10", "2", "Ordnance 2, Large Blast, Titan Killer"),
    "Gatling Blaster": ('72"', "8", "3", "Heavy 6, Large Blast"),
    "Inferno Gun": ("Hellstorm", "7", "3", "Heavy 1, Ignores Cover"),
    "Laser Blaster": ('96"', "10", "2", "Ordnance 3, Large Blast, Titan Killer"),
    "Melta Cannon": ('72"', "10", "1", "Ordnance 1, Apocalyptic Blast, Melta"),
    "Volcano Cannon": ('180"', "10", "2", "Ordnance 1, Massive Blast, Titan Killer"),
    "Vulcan Mega-bolter": ('60"', "6", "3", "Heavy 15"),
    "Twin-linked Vulcan Mega-bolter": ('60"', "6", "3", "Heavy 15, Twin-linked"),
    "Vortex Support Missile": ('48"-480"', "-", "-", "Ordnance 1, Apocalyptic Blast, Barrage, One Use, Vortex"),
    "Mori Quake Cannon": ('24"-360"', "10", "3", "Ordnance 1, Apocalyptic Blast, Barrage, Titan Killer, Concussive"),
    "Belicosa Pattern Volcano Cannon": ('180"', "10", "1",
                                        "Ordnance 1, Apocalyptic Blast, Titan Killer, Machine Destroyer"),
    "Macro-gatling Blaster": ('72"', "10", "3", "Ordnance 3, Massive Blast, Titan Killer"),
    "Sunfury Plasma Annihilator": ('72"', "9", "2",
                                   "Ordnance 2, Massive Blast, Titan Killer, Ignores Cover, Reactor Overload"),
    "Defensor Bolt Cannon": ('24"', "6", "4", "Heavy 6, Ardex-defensor"),
    "Defensor Lascannon": ('48"', "9", "2", "Heavy 1, Twin-linked, Sunder, Ardex-defensor"),
    "Titan Close Combat Weapon": ("-", "10", "1", "Melee, Titan Killer, Armourbane"),
    "Arioch Power Claw": ("-", "10", "1", "Melee, Titan Killer, Armourbane, Instant Death"),
    # options of the Warlord with no profile in the book (see questions)
    "Saturnyne Lascutter": ("?", "?", "?", "No profile given in the army list"),
    "Incinerator Missile Bank": ("?", "?", "?", "No profile given in the army list"),
}
MULTI = {
    "Plasma Blastgun": {
        "Plasma Blastgun - Rapid": ('72"', "8", "2", "Ordnance 2, Massive Blast"),
        "Plasma Blastgun - Full": ('96"', "10", "2", "Ordnance 1, Apocalyptic Blast"),
    },
}
WEAPON_RULES = {
    "Apocalypse Missile Launcher": ["Apocalypse Missile Launcher", "Apocalyptic Barrage (X)"],
    "Double-barrelled Turbo-laser Destructor": ["Titan Killer"],
    "Inferno Gun": ["Inferno Gun", "Ignores Cover"],
    "Laser Blaster": ["Titan Killer"],
    "Melta Cannon": ["Apocalyptic Blast", "Melta"],
    "Volcano Cannon": ["Massive Blast", "Titan Killer"],
    "Twin-linked Vulcan Mega-bolter": ["Twin-Linked"],
    "Vortex Support Missile": ["Apocalyptic Blast", "Vortex"],
    "Mori Quake Cannon": ["Apocalyptic Blast", "Titan Killer", "Concussive"],
    "Belicosa Pattern Volcano Cannon": ["Apocalyptic Blast", "Titan Killer", "Machine Destroyer"],
    "Macro-gatling Blaster": ["Massive Blast", "Titan Killer"],
    "Sunfury Plasma Annihilator": ["Massive Blast", "Titan Killer", "Ignores Cover", "Reactor Overload"],
    "Defensor Bolt Cannon": ["Ardex-defensor"],
    "Defensor Lascannon": ["Twin-Linked", "Ardex-defensor"],
    "Titan Close Combat Weapon": ["Titan Close Combat Weapons", "Titan Killer", "Armourbane"],
    "Arioch Power Claw": ["Titan Close Combat Weapons", "Titan Killer", "Armourbane"],
    "Plasma Blastgun": ["Plasma Blastgun", "Massive Blast", "Apocalyptic Blast"],
}
WARGEAR = {
    "Armoured Ceramite": ("Weapons with the Melta special rule do not roll an additional D6 for Armour Penetration "
                          "against a vehicle equipped with Armoured Ceramite."),
    "Void Shield": (
        "A Void Shield has Armour Value 12. While one or more Void Shields remain active, resolve shooting hits "
        "against the protected Titan one at a time. Each hit is resolved against an active Void Shield before it "
        "can strike the Titan itself. A Glancing or Penetrating Hit immediately collapses one Void Shield. "
        "Subsequent hits are resolved against any remaining active Void Shields. At the end of each controlling "
        "player's turn, roll a D6 for each collapsed Void Shield. On a 5+, that shield is restored."),
}

TITAN_RULES = ["Super-heavy Walker", "Structure Points", "Titan Weapon Mounts", "Towering Monstrosity",
               "Void Shields", "Reactor Meltdown", "Immense Machine"]
UT = "Vehicle (Walker, Super-heavy, Titan)"


# ---------------------------------------------------------------- helpers
def gear_n(key, name, n):
    """Fixed wargear carried n times (e.g. 'Two Apocalypse Missile Launchers')."""
    lid = uid("link", key, name, n)
    return link(lid, W(name), name, constraints=[constraint(uid(lid, "min"), "min", n),
                                                   constraint(uid(lid, "max"), "max", n, auto=True)])


def pair_entry(key, title, name, item, pts):
    """Inline option entry holding two of `item` (one cost for the pair)."""
    eid = uid(key, title, name)
    return entry(eid, name, cost=pts or 0, links=[gear_n(eid, item, 2)],
                 constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)])


def titan(name, cost, stats, sp, vs, kit, rules_, opts):
    """A Titan: Lords of War unit with one model (Walker profile, SP/VS in the unit type)."""
    u = k("unit", name)
    mid = uid("model", u, name)
    ws, bs, s, f, si, r, i, a = stats
    prof = walker_profile(mid, name, ws, bs, s, f, si, r, i, a,
                          ut=f"{UT}; Structure Points {sp}; Void Shields {vs}")
    m = entry(mid, name, typ="model", cost=0, profiles=[prof],
              links=[gear_n(mid, "Void Shield", vs)] + [gear(mid, x) if n == 1 else gear_n(mid, x, n)
                                                         for x, n in kit],
              infolinks=rules_links(TITAN_RULES + rules_, key=mid), groups=opts(mid),
              constraints=[constraint(uid(mid, "min"), "min", 1), constraint(uid(mid, "max"), "max", 1, auto=True)])
    return unit(name, cost, LOW, "Lords of War", models=[m], rules_=["Fielding Titans"], compulsory=False, key=u)


WARHOUND_ARMS = ["Double-barrelled Turbo-laser Destructor", "Plasma Blastgun", "Inferno Gun", "Vulcan Mega-bolter"]
REAVER_CARAPACE = ["Double-barrelled Turbo-laser Destructor", "Plasma Blastgun", "Inferno Gun",
                   "Vulcan Mega-bolter", "Apocalypse Missile Launcher", "Vortex Support Missile"]
REAVER_ARMS = ["Gatling Blaster", "Melta Cannon", "Volcano Cannon", "Laser Blaster", "Titan Close Combat Weapon"]
WARLORD_ARMS = [("Sunfury Plasma Annihilator", 0), ("Mori Quake Cannon", 0), ("Saturnyne Lascutter", 0),
                ("Arioch Power Claw", 0), ("Macro-gatling Blaster", 0)]
WARLORD_CARAPACE = [("Two Double-barrelled Turbo-laser Destructors", "Double-barrelled Turbo-laser Destructor", 0),
                    ("Two Twin-linked Vulcan Mega-bolters", "Twin-linked Vulcan Mega-bolter", 0),
                    ("Two Plasma Blastguns", "Plasma Blastgun", 0),
                    ("Two Laser Blasters", "Laser Blaster", 100),
                    ("Two Melta Cannons", "Melta Cannon", 100),
                    ("Two Gatling Blasters", "Gatling Blaster", 100),
                    ("Two Incinerator Missile Banks", "Incinerator Missile Bank", 75),
                    ("Two Vortex Missile Banks", "Vortex Support Missile", 150)]


def free_choice(m, title, items):
    """'Chosen from the following list' - exactly one, first item preselected, all free."""
    return slot(m, title, items[0], [(x, 0) for x in items[1:]])


def _warhound(m):
    return [free_choice(m, "Arm-mounted weapon (left)", WARHOUND_ARMS),
            free_choice(m, "Arm-mounted weapon (right)", WARHOUND_ARMS)]


def _reaver(m):
    return [free_choice(m, "Carapace-mounted weapon", REAVER_CARAPACE),
            free_choice(m, "Arm-mounted weapon (left)", REAVER_ARMS),
            free_choice(m, "Arm-mounted weapon (right)", REAVER_ARMS)]


def _warlord(m):
    title = "Carapace-mounted weapons"
    default = pair_entry(m, title, "Two Apocalypse Missile Launchers", "Apocalypse Missile Launcher", 0)
    pairs = [(pair_entry(m, title, n, item, pts), None) for n, item, pts in WARLORD_CARAPACE]
    return [slot(m, "Arm-mounted weapon (left): replace Belicosa Pattern Volcano Cannon",
                 "Belicosa Pattern Volcano Cannon", WARLORD_ARMS),
            slot(m, "Arm-mounted weapon (right): replace Belicosa Pattern Volcano Cannon",
                 "Belicosa Pattern Volcano Cannon", WARLORD_ARMS),
            slot(m, title, None, pairs, default_is_entry=default)]


# name, cost, (WS, BS, S, F, Si, R, I, A), SP, Void Shields, kit [(item, n)], rules, options
TITANS = [
    ("Warhound Scout Titan", 750, (2, 4, 10, 14, 13, 12, 1, 1), 3, 2, [], ["Agile"], _warhound),
    ("Reaver Battle Titan", 1450, (2, 4, 10, 14, 14, 13, 1, 2), 6, 4, [], ["Towering Monstrosity (Reaver)"],
     _reaver),
    ("Warlord Battle Titan", 2750, (2, 4, 10, 15, 15, 14, 1, 3), 9, 6,
     [("Defensor Bolt Cannon", 2), ("Defensor Lascannon", 2), ("Armoured Ceramite", 1)],
     ["Reinforced Structure", "Towering Monstrosity (Warlord)", "World Burner"], _warlord),
]

ARMY_RULE_NAMES = ["Fielding Titans", "Super-heavy Walker", "Structure Points", "Titan Weapon Mounts",
                   "Towering Monstrosity", "Void Shields", "Reactor Meltdown", "Immense Machine"]


def build():
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS, multi_profile=MULTI, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    alg = allegiance()
    cl = alg.find("categoryLinks")
    alg.insert(list(alg).index(cl), wrap("infoLinks", rules_links(ARMY_RULE_NAMES, key=k("army-rules"))))
    titans = [titan(*t) for t in TITANS]
    return catalogue(ARMY, [alg] + titans, [])
