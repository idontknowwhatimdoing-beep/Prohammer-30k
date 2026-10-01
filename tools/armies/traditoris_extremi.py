"""Traditoris Extremi (work-in-progress supplement for fully corrupted Traitor Legions).

Source: /home/claude/src/Traditoris_Extremi.txt
Questions: tools/questions/Traditoris Extremi.md

The supplement is meant to be used together with the Legiones Astartes army list (it changes some Force
Organisation spaces and adds unit upgrades). A New Recruit catalogue cannot modify another catalogue, so this is a
small Traitor-only catalogue that holds the additional units; the supplement-wide changes are rule text.
"""
from armies.common import *  # noqa: F401,F403
from armies.common import k, unit, model, allegiance, catalogue, start, register_data
from legiones import unit_profile
from legiones2 import choice, HQ

ARMY = "Traditoris Extremi"

RULES = {
    "Traditoris Extremi": (
        "This supplement represents the fully corrupted and mutated Traitor Legions of the latter days of the Horus "
        "Heresy and the Scouring, which have dedicated their worship to Chaos. It is used together with the regular "
        "Legiones Astartes army list and the Legion army books (Forces of the Legions): certain Force Organisation "
        "spaces are changed and certain unit upgrades may be applied (not yet defined in this work-in-progress "
        "supplement). Traitor Allegiance only. In New Recruit, add this catalogue as an additional Detachment next to "
        "the Legion Detachment; the units here must belong to the same Traitor Legion army."),
    "Legiones Astartes": (
        "All models with this special rule also have the And They Shall Know No Fear special rule as presented in "
        "ProHammer Classic. They are not Fearless, though, and lose that bonus.\n"
        "In addition, each model possesses a named version of the Legiones Astartes special rule corresponding to its "
        "Legion, such as Legiones Astartes (Sons of Horus). A model may only ever possess one named version. Models "
        "with a named Legiones Astartes special rule gain any additional rules associated with that Legion (see "
        "Forces of the Legions).\nUnless specifically stated otherwise, vehicles do not have this special rule."),
}

WEAPONS = {
    "Daemonic Weapon": ("-", "User", "-", "Counts as a Power Weapon (Ignores Armour Saves)"),
}

WARGEAR = {
    "Power Armour": "A model wearing Power Armour has a 3+ Armour Save.",
    "Daemonic Aura": ("Listed as wargear of the Daemon Prince; the supplement does not yet give its rules "
                      "(work in progress). The Daemon Prince's profile shows a 5+ Invulnerable Save."),
}

TRAITOR_LEGIONS = ["III - Emperor's Children", "IV - Iron Warriors", "VIII - Night Lords", "XII - World Eaters",
                   "XIV - Death Guard", "XV - Thousand Sons", "XVI - Sons of Horus", "XVII - Word Bearers",
                   "XX - Alpha Legion"]


def daemon_prince():
    u = k("unit", "Daemon Prince")
    prof = unit_profile(u, "Daemon Prince", "Monstrous Creature (Character)", 7, 5, 6, 5, 4, 5, 4, 10, "3+/5++")
    m = model(u, "Daemon Prince", 1, 1, 0, prof, kit=["Power Armour", "Daemonic Weapon", "Daemonic Aura"])
    legion = choice(u, "Legion (named Legiones Astartes rule)", [(n, 0, False, [], []) for n in TRAITOR_LEGIONS],
                    required=True)
    return unit("Daemon Prince", 125, HQ, "HQ", models=[m], groups=[legion],
                rules_=["Legiones Astartes", "Independent Character", "Daemon"], key=u)


def build():
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS, wargear=WARGEAR)
    alleg = allegiance(loyalist_ok=False)
    from legiones import rules_links
    from legiones2 import add_to
    add_to(alleg, "infoLinks", rules_links(["Traditoris Extremi"], key=k("army-rules")))
    units = [alleg, daemon_prince()]
    return catalogue(ARMY, units)
