"""Aeronautica Imperialis - supplementary aircraft list (source: Areonautica_Imperialis.txt).

Every aircraft is a root unit in the Force Organisation slot its entry states. Which army may take it is shown
as an "Available to: ..." rule (New Recruit cannot check another catalogue's army)."""
from armies.common import *

ARMY = "Aeronautica Imperialis"

# ------------------------------------------------------------------ rules
LA = "Available to: Legiones Astartes"
LA_IA_MECH = "Available to: Legiones Astartes, Imperial Army, Mechanicum"
IA = "Available to: Imperial Army"
IA_MECH = "Available to: Imperial Army, Mechanicum"
_IA_NOTE = (" 'Imperial Army' includes the Exercitus Imperialis and the Solar Auxilia. The aircraft occupies the "
            "Force Organisation slot shown in its entry. (New Recruit cannot check which army takes it - check by "
            "hand.)")

RULES = {
    LA: "This aircraft may only be selected by a Legiones Astartes army." + _IA_NOTE,
    LA_IA_MECH: ("This aircraft may be selected by a Legiones Astartes, Imperial Army or Mechanicum army. An "
                 "Imperial Army or Mechanicum force selects the Primaris-Lightning Strike Fighter as a Fast Attack "
                 "choice using the profile and options of the Legiones Astartes entry." + _IA_NOTE),
    IA: "This aircraft may only be selected by an Imperial Army army." + _IA_NOTE,
    IA_MECH: "This aircraft may be selected by an Imperial Army or Mechanicum army." + _IA_NOTE,
    "Aeronautica Imperialis": (
        "The aircraft in this list are supplementary units for the armies of the Great Crusade and Horus Heresy. "
        "Each aircraft may be selected by the army or armies indicated in its entry and occupies the Force "
        "Organisation slot shown in its profile. Unless specifically stated otherwise, an aircraft follows all "
        "normal rules for Vehicles and Flyers presented in the ProHammer Core Rules.\n"
        "Flyers: any vehicle with the Flyer unit type uses the Flyer rules of the ProHammer Core Rules (deployment "
        "from Reserves, Zooming and Hovering, movement speeds, turning, leaving the battlefield, Hard to Hit, "
        "Evasion and damage suffered by Zooming Flyers). Where a rule in this book directly contradicts the "
        "normal Flyer rules, the rule in this book takes precedence."),
    "Air-to-Air Targeting": ("When a Zooming Flyer fires at another Flyer or Flying Monster, it may use its normal "
                             "Ballistic Skill when rolling To Hit."),
    "Agile": ("When a Flyer with this special rule enters Evasion, improve the Cover Save granted by Evasion by +1, "
              "to a maximum of 3+."),
    "Bomb": (
        "Weapons with the Bomb type may only be used by a Flyer while it is Zooming. During the Flyer's Movement "
        "phase, after it has completed its move, it may make one Bombing Run if it passed over an enemy unit during "
        "that move. Choose one enemy unit which the Flyer passed over and place the appropriate Blast marker with "
        "its centre over any model in that unit which the Flyer passed over. Roll for Scatter normally; the Flyer's "
        "Ballistic Skill does not reduce the distance scattered. Resolve the attack using the Bomb's weapon "
        "profile. A Flyer may only use one Bomb weapon during each Movement phase unless a special rule "
        "specifically states otherwise. Dropping a Bomb does not prevent the Flyer from firing its other weapons "
        "during the Shooting phase. Bomb weapons may not be used while the Flyer is Hovering."),
    "Bomb X": ("Some Bomb weapons have a number after their type, such as Bomb 2. When such a weapon is used during "
               "a Bombing Run, resolve a number of attacks equal to the number shown. All attacks must be placed "
               "over the same target unit and are resolved separately."),
    "Cluster Warhead": (
        "If a weapon with this special rule scores a Penetrating Hit against a target with an Armour Value, roll D3 "
        "times on the Vehicle Damage table and apply the highest result rolled. Only one Penetrating Hit is "
        "inflicted; the additional rolls merely determine the damage result."),
    "Heat Seeker": "Cover Saves granted by Evasion may not be taken against attacks made with a weapon with this "
                   "special rule.",
    "Sunder": "A weapon with this special rule may re-roll failed Armour Penetration rolls against Vehicles.",
    "Terminal Tracking": (
        "Successful Cover Saves, including those gained through Evasion (the Xiphon entry adds: or Jink), made "
        "against a weapon with this special rule must be re-rolled."),
    "One Use": "The weapon may only be fired once per battle (one-use ordnance; each missile/bomb is used once).",
    "Rad-phage": (
        "If a model suffers one or more unsaved Wounds from a weapon with Rad-phage and survives, reduce its "
        "Toughness by 1 for the remainder of the battle (minimum 1). Multiple applications are cumulative. "
        "(Text as in the Legiones Astartes list - not defined in this book.)"),
    "Lingering Death": (
        "After resolving the attack, leave the Blast marker in place. For the remainder of the battle, the area "
        "beneath it counts as Dangerous Terrain for non-vehicle models and Open-topped vehicles. (Text as in the "
        "Legiones Astartes list - not defined in this book.)"),
    "Special Ordnance - Rad Missiles": (
        "Any Twin-linked Missile Launcher carried by the Primaris-Lightning may additionally be equipped with Rad "
        "Missiles for +15 points per launcher."),
    "Independent Turret Fire": (
        "The Fire Raptor's two waist-mounted turrets operate independently of the gunship's other weapons. Each "
        "turret may fire at a different target from the Fire Raptor's other weapons and from the other turret. "
        "Weapons fired by these turrets do not count towards the number of weapons the Fire Raptor is normally "
        "permitted to fire because of its movement speed."),
    "Caestus Ram": (
        "The Caestus may declare a Ram against an enemy vehicle even though it does not normally have the Tank "
        "unit type. A Ram made by the Caestus inflicts a Strength 10 hit instead of using the normal Strength "
        "calculation for Ramming. When rolling Armour Penetration for the hit inflicted by the Caestus, roll two "
        "dice and use the higher result. In addition, add +1 to any roll made on the Vehicle Damage table as a "
        "result of a Ram inflicted by the Caestus. The Caestus has a 5+ Invulnerable Save against any Glancing or "
        "Penetrating Hit which strikes its Front Armour. This includes damage suffered as a result of Ramming or "
        "being Rammed."),
    "Misericord": (
        "The Caestus may only transport models wearing Power Armour, Artificer Armour or Terminator Armour. Models "
        "wearing any form of Terminator Armour count as one model each when determining the Caestus' Transport "
        "Capacity."),
    "Simulacra Repair": "Whenever the Thunderbolt suffers a Glancing Hit, roll a D6. On a 6, the damage is ignored.",
    "Combat Interdiction": (
        "If one or more enemy Flyers or Skimmers are already on the battlefield when Reserve rolls are made for the "
        "Thunderbolt, failed Reserve rolls for the Thunderbolt must be re-rolled."),
    "Defensive Heavy Stubber (Avenger)": ("The Defensive Heavy Stubber may fire at a different target from the "
                                          "Avenger's other weapons."),
}

# ------------------------------------------------------------------ weapons
TL_ML = "Twin-linked Missile Launcher"
WEAPONS = {
    # Aeronautica weapons table (L246-264)
    "Avenger Bolt Cannon": ('36"', "6", "3", "Heavy 7"),
    "Twin-linked Avenger Bolt Cannon": ('36"', "6", "3", "Heavy 7, Twin-linked"),
    "Defensive Heavy Stubber": ('36"', "4", "6", "Heavy 3, Skyfire"),
    "Electromagnetic Storm Charge": ("-", "3", "4", "Bomb 1, Large Blast, Haywire, Concussive, One Use"),
    "Hellstrike Missile": ('72"', "8", "2", "Heavy 1, Sunder, One Use"),
    "Kinetic Piercer Missile": ('48"', "6", "2", "Heavy 1, Armourbane, Heat Seeker, One Use"),
    "Kraken Penetrator Heavy Missile": ('36"', "8", "1", "Heavy 1, Armourbane, One Use"),
    "Twin-linked Magna-Melta": ('18"', "8", "1", "Heavy 1, Large Blast, Melta, Twin-linked"),
    "Phosphex Bomb Cluster": ("-", "5", "2", "Bomb 2, Barrage, Blast, Poisoned (3+), Crawling Fire, Lingering "
                                             "Death, Deadly Cargo, One Use"),
    "Quad Heavy Bolter": ('36"', "5", "4", "Heavy 6, Twin-linked"),
    "Rad Missile": ('48"', "4", "3", "Heavy 1, Blast, Fleshbane, Rad-phage"),
    "Reaper Autocannon Battery": ('36"', "7", "4", "Heavy 4, Twin-linked"),
    "Sunfury Heavy Missile": ('36"', "6", "3", "Heavy 1, Large Blast, Blind, One Use"),
    "Tactical Bomb": ("-", "6", "4", "Bomb 1, Barrage, Blast, One Use"),
    "Tempest Rocket": ('60"', "6", "4", "Heavy 1, Sunder, One Use"),
    "Vengeance Launcher": ('48"', "5", "4", "Heavy 2, Large Blast"),
    "Xiphon Rotary Missile Launcher": ('60"', "8", "2", "Heavy 2, Cluster Warhead, Terminal Tracking"),
    # standard weapons (ProHammer / army list profiles, not printed in this book)
    "Twin-linked Lascannon": ('48"', "9", "2", "Heavy 1, Twin-linked"),
    "Lascannon": ('48"', "9", "2", "Heavy 1"),
    "Twin-linked Autocannon": ('48"', "7", "4", "Heavy 2, Twin-linked"),
    "Autocannon": ('48"', "7", "4", "Heavy 2"),
    "Twin-linked Multi-laser": ('36"', "6", "6", "Heavy 3, Twin-linked"),
    "Multi-laser": ('36"', "6", "6", "Heavy 3"),
    "Twin-linked Heavy Bolter": ('36"', "5", "4", "Heavy 3, Twin-linked"),
    "Twin-linked Multi-Melta": ('24"', "8", "1", "Heavy 1, Melta, Twin-linked"),
    "Havoc Launcher": ('48"', "5", "5", "Heavy 1, Blast, Twin-linked"),
}
MULTI = {
    "Missile Launcher": {"Missile Launcher - Frag": ('48"', "4", "6", "Heavy 1, Blast"),
                         "Missile Launcher - Krak": ('48"', "8", "3", "Heavy 1")},
    TL_ML: {"Twin-linked Missile Launcher - Frag": ('48"', "4", "6", "Heavy 1, Blast, Twin-linked"),
            "Twin-linked Missile Launcher - Krak": ('48"', "8", "3", "Heavy 1, Twin-linked")},
}
WEAPON_RULES = {
    "Twin-linked Avenger Bolt Cannon": ["Twin-Linked"],
    "Defensive Heavy Stubber": ["Skyfire"],
    "Electromagnetic Storm Charge": ["Bomb", "Haywire", "Concussive", "One Use"],
    "Hellstrike Missile": ["Sunder", "One Use"],
    "Kinetic Piercer Missile": ["Armourbane", "Heat Seeker", "One Use"],
    "Kraken Penetrator Heavy Missile": ["Armourbane", "One Use"],
    "Twin-linked Magna-Melta": ["Melta", "Twin-Linked"],
    "Phosphex Bomb Cluster": ["Bomb", "Bomb X", "Poisoned", "Lingering Death", "One Use"],
    "Quad Heavy Bolter": ["Twin-Linked"],
    "Rad Missile": ["Fleshbane", "Rad-phage"],
    "Reaper Autocannon Battery": ["Twin-Linked"],
    "Sunfury Heavy Missile": ["Blind", "One Use"],
    "Tactical Bomb": ["Bomb", "One Use"],
    "Tempest Rocket": ["Sunder", "One Use"],
    "Xiphon Rotary Missile Launcher": ["Cluster Warhead", "Terminal Tracking"],
    "Twin-linked Lascannon": ["Twin-Linked"],
    "Twin-linked Autocannon": ["Twin-Linked"],
    "Twin-linked Multi-laser": ["Twin-Linked"],
    "Twin-linked Heavy Bolter": ["Twin-Linked"],
    "Twin-linked Multi-Melta": ["Melta", "Twin-Linked"],
    "Havoc Launcher": ["Twin-Linked"],
    TL_ML: ["Twin-Linked"],
}

# ------------------------------------------------------------------ wargear (Aeronautica Armoury, L138-204)
WARGEAR = {
    "Armoured Ceramite": "Weapons with the Melta special rule do not roll an additional D6 for Armour Penetration "
                         "against a vehicle equipped with Armoured Ceramite.",
    "Armoured Cockpit": "Whenever a vehicle with an Armoured Cockpit suffers a Crew Shaken or Crew Stunned result, "
                        "roll a D6. On a 4+, that result is ignored.",
    "Battle Servitor Control": ("A vehicle equipped with Battle Servitor Control gains Tank Hunters.",
                                ["Tank Hunters"]),
    "Chaff Launcher": "Once per battle, when the vehicle suffers a Glancing or Penetrating Hit caused by a Missile "
                      "weapon, the controlling player may activate the Chaff Launcher. Roll a D6. On a 4+, the hit "
                      "is ignored.",
    "Ground-tracking Auguries": ("A vehicle equipped with Ground-tracking Auguries gains Strafing Run.",
                                 ["Strafing Run"]),
    "Ramjet Diffraction Grid": "Reduce the Strength of shooting attacks which strike the vehicle's Side or Rear "
                               "Armour by 1, to a minimum of Strength 1. A vehicle equipped with a Ramjet Diffraction "
                               "Grid may not claim a Cover Save granted by Night Fighting.",
    "Flare Shield": "The Strength of shooting attacks which strike the vehicle's Front Armour is reduced by 1. If "
                    "the attacking weapon has the Blast or Template type, its Strength is instead reduced by 2. A "
                    "Flare Shield has no effect against close combat attacks or attacks with the Destroyer special "
                    "rule.",
    "Illum Flares": "A Flyer equipped with Illum Flares may drop one flare during each friendly Movement phase in the "
                    "same manner as a Bomb. After resolving Scatter, place a marker where the flare lands and leave "
                    "it in place until the end of the turn. Any friendly unit firing at an enemy unit with at least "
                    "one model within 12\" of the marker gains Night Vision for that Shooting phase.",
    "Infra-red Targeting": ("A vehicle equipped with Infra-red Targeting gains Night Vision.", ["Night Vision"]),
    "Searchlight": ("", ["Searchlight"]),
    "Extra Armour": ("", ["Extra Armor"]),
    "Auxiliary Drive": "At the start of the controlling player's Movement phase, if the vehicle is Immobilised, roll "
                       "a D6. On a 4+, remove one Immobilised result. The vehicle may move normally during that "
                       "Movement phase. (Not defined in this book - Legiones Astartes text.)",
    "Frag Assault Launchers": "A unit which charges during the same turn that it disembarks from a Caestus equipped "
                              "with Frag Assault Launchers counts as being equipped with Frag Grenades for that "
                              "Assault phase.",
}

FLYER_RULES = ["Aeronautica Imperialis", "Air-to-Air Targeting"]


# ------------------------------------------------------------------ helpers
def gearn(key, name, n):
    """Fixed link to an item carried n times."""
    lid = uid("link", key, name)
    return link(lid, W(name), name, constraints=[constraint(uid(lid, "min"), "min", n),
                                                 constraint(uid(lid, "max"), "max", n, auto=True)])


def inline(key, name, cost, items, entries=()):
    """Inline entry carrying one or more linked items, e.g. 'Two Sunfury Heavy Missiles'."""
    eid = uid(key, "inline", name)
    links = [gearn(eid, it, items.count(it)) for it in dict.fromkeys(items)]
    return entry(eid, name, cost=cost, links=links, entries=list(entries),
                 constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)])


def one_of(key, title, links_=(), entries=()):
    """Optional 'one of the following' group: links_ [(item, pts)], entries = inline entries."""
    gid = uid("grp", key, title)
    return group(gid, title, constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)],
                 links=[link(uid("link", gid, n), W(n), n, cost=p or None) for n, p in links_],
                 entries=list(entries))


def _add_kit(e, links_):
    """Add fixed (counted) item links to a unit, keeping the schema order (entryLinks before costs)."""
    el_ = e.find("entryLinks")
    if el_ is None:
        el_ = wrap("entryLinks", list(links_))
        cs = e.find("costs")
        e.insert(list(e).index(cs) if cs is not None else len(e), el_)
    else:
        for lk in links_:
            el_.append(lk)


# ------------------------------------------------------------------ units
def primaris_lightning():
    u = k("unit", "Primaris-Lightning Strike Fighter")

    def mount(i):
        key = uid(u, "mount", i)
        rad = upgrade(uid(key, "tlml"), "Rad Missiles", 15, links=["Rad Missile"])
        return one_of(key, f"Dual Hardpoint Mount {i} (one)",
                      [("Twin-linked Autocannon", 20), ("Twin-linked Multi-laser", 20)],
                      [inline(key, "Twin-linked Missile Launcher with Frag and Krak missiles", 25, [TL_ML],
                              entries=[rad]),
                       inline(key, "Two Sunfury Heavy Missiles", 25, ["Sunfury Heavy Missile"] * 2),
                       inline(key, "Two Kraken Penetrator Heavy Missiles", 35,
                              ["Kraken Penetrator Heavy Missile"] * 2),
                       inline(key, "Phosphex Bomb Cluster", 15, ["Phosphex Bomb Cluster"]),
                       inline(key, "Two Electromagnetic Storm Charges", 10, ["Electromagnetic Storm Charge"] * 2)])

    e = unit("Primaris-Lightning Strike Fighter", 135, FA, "Fast Attack", key=u, compulsory=False,
             profiles=[vehicle_profile(u, "Primaris-Lightning", "Vehicle (Flyer)", 4, 11, 11, 10)],
             rules_=[LA_IA_MECH] + FLYER_RULES + ["Agile", "Deep Strike", "Supersonic",
                                                 "Special Ordnance - Rad Missiles"],
             groups=[mount(1), mount(2), mount(3),
                     take(u, "Upgrades", [("Battle Servitor Control", 15), ("Ground-tracking Auguries", 10),
                                          ("Ramjet Diffraction Grid", 20)])])
    _add_kit(e, [gearn(u, "Twin-linked Lascannon", 1), gearn(u, "Chaff Launcher", 1),
                 gearn(u, "Armoured Cockpit", 1)])
    return e


def xiphon():
    u = k("unit", "Xiphon Pattern Interceptor")
    e = unit("Xiphon Pattern Interceptor", 205, FA, "Fast Attack", key=u, compulsory=False,
             profiles=[vehicle_profile(u, "Xiphon Interceptor", "Vehicle (Flyer)", 4, 11, 11, 11)],
             rules_=[LA] + FLYER_RULES + ["Agile", "Deep Strike", "Supersonic"],
             groups=[take(u, "Upgrades", [("Ground-tracking Auguries", 10), ("Chaff Launcher", 5),
                                          ("Armoured Cockpit", 5)])])
    _add_kit(e, [gearn(u, "Twin-linked Lascannon", 2), gearn(u, "Xiphon Rotary Missile Launcher", 1),
                 gearn(u, "Armoured Ceramite", 1)])
    return e


def storm_eagle():
    u = k("unit", "Legion Storm Eagle Assault Gunship")
    rockets = inline(uid(u, "rk"), "Four Tempest Rockets", 0, ["Tempest Rocket"] * 4)
    e = unit("Legion Storm Eagle Assault Gunship", 210, FA, "Fast Attack", key=u, compulsory=False,
             profiles=[vehicle_profile(u, "Storm Eagle", "Vehicle (Flyer, Hover, Transport)", 4, 12, 12, 12),
                       transport_profile(u, "Storm Eagle", "20 models",
                                         "One on each side, one front ramp, one rear ramp", "-")],
             rules_=[LA] + FLYER_RULES + ["Deep Strike", "Assault Vehicle", "Power of the Machine Spirit"],
             groups=[slot(u, "Replace Twin-linked Heavy Bolter", "Twin-linked Heavy Bolter",
                          [("Missile Launcher", 5), ("Twin-linked Multi-Melta", 15)]),
                     slot(u, "Replace Four Tempest Rockets", None, [
                         (inline(uid(u, "rk"), "Four Hellstrike Missiles", 20, ["Hellstrike Missile"] * 4), None),
                         (inline(uid(u, "rk"), "Two Twin-linked Lascannons", 40, ["Twin-linked Lascannon"] * 2),
                          None)], default_is_entry=rockets),
                     take(u, "Upgrades", [("Armoured Ceramite", 20), ("Searchlight", 1), ("Extra Armour", 5)])])
    _add_kit(e, [gearn(u, "Vengeance Launcher", 1)])
    return e


def fire_raptor():
    u = k("unit", "Legion Fire Raptor Gunship")
    turrets = inline(uid(u, "tu"), "Two Quad Heavy Bolter Turrets", 0, ["Quad Heavy Bolter"] * 2)
    rockets = inline(uid(u, "rk"), "Four Tempest Rockets", 0, ["Tempest Rocket"] * 4)
    e = unit("Legion Fire Raptor Gunship", 200, HS, "Heavy Support", key=u, compulsory=False,
             profiles=[vehicle_profile(u, "Fire Raptor", "Vehicle (Flyer, Hover)", 4, 12, 12, 12)],
             rules_=[LA] + FLYER_RULES + ["Deep Strike", "Strafing Run", "Power of the Machine Spirit",
                                         "Independent Turret Fire"],
             groups=[slot(u, "Turrets", None, [
                         (inline(uid(u, "tu"), "Two Reaper Autocannon Batteries", 10,
                                 ["Reaper Autocannon Battery"] * 2), None)], default_is_entry=turrets),
                     slot(u, "Replace Four Tempest Rockets", None, [
                         (inline(uid(u, "rk"), "Four Hellstrike Missiles", 20, ["Hellstrike Missile"] * 4), None)],
                          default_is_entry=rockets),
                     take(u, "Upgrades", [("Searchlight", 1), ("Armoured Ceramite", 20)])])
    _add_kit(e, [gearn(u, "Twin-linked Avenger Bolt Cannon", 1), gearn(u, "Extra Armour", 1)])
    return e


def caestus():
    u = k("unit", "Legion Caestus Assault Ram")
    havoc = inline(uid(u, "hv"), "Two Havoc Launchers", 0, ["Havoc Launcher"] * 2)
    e = unit("Legion Caestus Assault Ram", 305, HS, "Heavy Support", key=u, compulsory=False,
             profiles=[vehicle_profile(u, "Legion Caestus", "Vehicle (Flyer, Hover, Transport)", 4, 13, 13, 11),
                       transport_profile(u, "Legion Caestus", "10 models", "Two front access points", "-")],
             rules_=[LA] + FLYER_RULES + ["Deep Strike", "Assault Vehicle", "Power of the Machine Spirit",
                                         "Caestus Ram", "Misericord"],
             groups=[take(u, "Upgrades", [("Frag Assault Launchers", 10), ("Auxiliary Drive", 10)]),
                     slot(u, "Replace Two Havoc Launchers", None, [
                         (inline(uid(u, "hv"), "Two Missile Launchers with Frag and Krak Missiles", 10,
                                 ["Missile Launcher"] * 2), None)], default_is_entry=havoc)])
    _add_kit(e, [gearn(u, "Twin-linked Magna-Melta", 1), gearn(u, "Armoured Ceramite", 1),
                 gearn(u, "Extra Armour", 1)])
    return e


def thunderbolt():
    u = k("unit", "Auxilia Thunderbolt Heavy Fighter")
    kp = inline(uid(u, "ms"), "Four Kinetic Piercer Missiles", 0, ["Kinetic Piercer Missile"] * 4)
    e = unit("Auxilia Thunderbolt Heavy Fighter", 200, FA, "Fast Attack", key=u, compulsory=False,
             profiles=[vehicle_profile(u, "Thunderbolt Heavy Fighter", "Vehicle (Flyer)", 4, 11, 11, 10)],
             rules_=[IA] + FLYER_RULES + ["Simulacra Repair", "Supersonic", "Deep Strike", "Combat Interdiction"],
             groups=[take(u, "Upgrades", [("Ground-tracking Auguries", 10), ("Flare Shield", 20)]),
                     slot(u, "Replace Four Kinetic Piercer Missiles", None, [
                         (inline(uid(u, "ms"), "Four Hellstrike Missiles", 0, ["Hellstrike Missile"] * 4), None),
                         (inline(uid(u, "ms"), "Four Sunfury Heavy Missiles", 20, ["Sunfury Heavy Missile"] * 4),
                          None)], default_is_entry=kp)])
    _add_kit(e, [gearn(u, "Twin-linked Autocannon", 2), gearn(u, "Twin-linked Lascannon", 1),
                 gearn(u, "Armoured Cockpit", 1), gearn(u, "Chaff Launcher", 1)])
    return e


def avenger():
    u = k("unit", "Avenger Strike Fighter")
    key = uid(u, "wing")
    e = unit("Avenger Strike Fighter", 150, FA, "Fast Attack", key=u, compulsory=False,
             profiles=[vehicle_profile(u, "Avenger Strike Fighter", "Vehicle (Flyer)", 3, 12, 10, 10)],
             rules_=[IA_MECH] + FLYER_RULES + ["Strafing Run", "Deep Strike", "Supersonic",
                                               "Defensive Heavy Stubber (Avenger)"],
             groups=[one_of(key, "Wing-mounted Hardpoints (one)", entries=[
                         inline(key, "Six Tactical Bombs", 40, ["Tactical Bomb"] * 6),
                         inline(key, "Two Kraken Penetrator Heavy Missiles", 25,
                                ["Kraken Penetrator Heavy Missile"] * 2),
                         inline(key, "Two Missile Launchers with Frag and Krak Missiles", 20,
                                ["Missile Launcher"] * 2),
                         inline(key, "Two Autocannons", 20, ["Autocannon"] * 2),
                         inline(key, "Two Multi-lasers", 20, ["Multi-laser"] * 2)]),
                     take(u, "Upgrades", [("Chaff Launcher", 10), ("Infra-red Targeting", 5),
                                          ("Battle Servitor Control", 15)])])
    _add_kit(e, [gearn(u, "Avenger Bolt Cannon", 1), gearn(u, "Lascannon", 2), gearn(u, "Armoured Cockpit", 1),
                 gearn(u, "Defensive Heavy Stubber", 1)])
    return e


def arvus():
    u = k("unit", "Arvus Lighter Orbital Shuttle")
    key = uid(u, "wpn")
    automata = upgrade(u, "Battle-automata Carriage (Mechanicum only)", 20, text=(
        "Mechanicum only: an Arvus Lighter selected by a Mechanicum army may be modified to carry Battle-automata. "
        "If this upgrade is taken, it may transport either 1 Castellax Battle-Automata, or up to 2 Vorax "
        "Battle-Automata. An Arvus modified in this manner may not transport any other models."))
    return unit("Arvus Lighter Orbital Shuttle", 75, FA, "Fast Attack", key=u, compulsory=False,
                profiles=[vehicle_profile(u, "Arvus Lighter", "Vehicle (Flyer, Hover, Transport)", 3, 11, 11, 10),
                          transport_profile(u, "Arvus Lighter", "12 models", "One rear access hatch", "None")],
                rules_=[IA_MECH] + FLYER_RULES + ["Deep Strike"],
                groups=[take(u, "Upgrades", [("Chaff Launcher", 10), ("Armoured Cockpit", 15), ("Illum Flares", 5),
                                             ("Searchlight", 1), ("Extra Armour", 10), ("Flare Shield", 20)]),
                        one_of(key, "Weapon (one)", [("Multi-laser", 10), ("Autocannon", 10), ("Lascannon", 20),
                                                     ("Twin-linked Multi-laser", 15), ("Twin-linked Autocannon", 15),
                                                     ("Twin-linked Lascannon", 25)],
                               [inline(key, "Two Hellstrike Missiles", 20, ["Hellstrike Missile"] * 2)])],
                entries=[automata])


def build():
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS, multi_profile=MULTI, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    units = [primaris_lightning(), xiphon(), storm_eagle(), fire_raptor(), caestus(), thunderbolt(), avenger(),
             arvus()]
    return catalogue(ARMY, units, [])
