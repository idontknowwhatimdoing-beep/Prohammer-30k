"""XVI Legion - Sons of Horus (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from bsx import el

LEGION = "XVI - Sons of Horus"
LR = "Legiones Astartes (Sons of Horus)"
SHORT = "Sons of Horus"

HORUS = uid("unit", "Horus Lupercal, the Warmaster")
HORUS_ASC = uid("unit", "Horus Ascended, the Warmaster")
ABADDON = uid("unit", "Ezekyle Abaddon, First Captain")

# ---------------------------------------------------------------- data
RULES = {
    LR: ("Models with this rule belong to the XVI Legion and use the Sons of Horus Legion special rules: Close Range "
         "Brutality, Tip of the Spear and Pride of the Warmaster."),
    "Close Range Brutality": (
        "At the beginning of the Assault phase, a Sons of Horus unit which is otherwise able to charge may fire at the "
        "enemy unit it intends to charge. Only models with Rapid Fire, Pistol or Assault weapons may fire; Template "
        "weapons may not be used. These attacks hit only on a 5+ regardless of BS and never cause Morale or Pinning "
        "tests. Firing does not prevent the charge, but the unit must charge the unit it fired upon. If casualties leave "
        "the target out of charge range or destroy it, the unit may not charge another unit; instead it moves D6\" "
        "directly towards the target's current (or final) position. This is not a charge and may not bring the unit "
        "within 1\" of another enemy model."),
    "Tip of the Spear": (
        "Even if the mission does not normally permit Deep Strike, the following may deploy using Deep Strike: one Sons "
        "of Horus Infantry unit selected from Elites, and one Sons of Horus Independent Character (alone or joined by a "
        "Command Squad). These units must begin the battle in Reserve."),
    "Pride of the Warmaster": (
        "At the end of the final scheduled game turn, the opposing player may demand one additional complete game turn: "
        "roll a D6, on a 4+ one additional complete game turn is played. Only once per battle; does not extend a mission "
        "that already ended because a specific objective or action was completed."),
    # armoury
    "Banestrike": "A natural To Wound roll of 6 made with Banestrike Ammunition is resolved at AP3.",
    "Banestrike Ammunition": (
        "Sons of Horus Seeker Squads, Justaerin Terminator Squads and Independent Characters equipped with a Bolter, "
        "Foeblaster Boltgun, Combi-Bolter, Storm Bolter or Combi-Weapon may purchase Banestrike Ammunition (+5 points per "
        "eligible model). Every eligible model in a squad must purchase it, or none. Models that replaced their bolt "
        "weapon neither pay for nor benefit from it. Bolter profile: 18\", S4, AP4, Rapid Fire, Banestrike. With a "
        "Foeblaster Boltgun, Storm Bolter, Combi-Bolter or the bolter component of a Combi-Weapon keep the weapon's "
        "shots and firing type but use 18\" range, AP4 and Banestrike. May not be combined with Special Issue Ammunition "
        "or another ammunition upgrade."),
    "Rending (5+)": ("Follows the normal Rending rules, except that the effect is triggered on a natural To Wound roll of "
                     "5 or 6. Against Vehicles, Rending is still triggered only by a natural Armour Penetration roll of "
                     "6. A Cthonian Culling Blade does not count as a Power Weapon."),
    "Teleportation Transponders": (
        "Any Sons of Horus unit composed entirely of models in any form of Terminator Armour may purchase Teleportation "
        "Transponders for +15 points per unit; a Sons of Horus Independent Character in Terminator Armour for +10. The "
        "model or unit gains Deep Strike and may deploy using Deep Strike even if the mission would not normally permit "
        "it. An Independent Character intending to Deep Strike as part of another unit must purchase them separately."),
    # rites
    "The Long March": (
        "EFFECTS - Relentless March: at the beginning of each Sons of Horus player turn, each Sons of Horus Infantry unit "
        "gains, until the beginning of the next Sons of Horus player turn, a rule depending on where the majority of its "
        "surviving models are: own deployment zone - Relentless; outside either deployment zone - Fleet; enemy deployment "
        "zone - Crusader (equally divided: controlling player chooses). The Warmaster's Portion: during the first Sons of "
        "Horus player turn all units in the Detachment may re-roll To Hit rolls of 1. Legion Terminator Squads may be "
        "selected as non-compulsory Troops choices (they may not fulfil compulsory Troops).\n"
        "LIMITATIONS - Traitor Sons of Horus Detachment only. No models with Slow and Purposeful unless they begin the "
        "battle embarked on a Transport or enter play by Deep Strike. No Fortification or Allied Detachment."),
    "The Black Reaving": (
        "EFFECTS - Reaver Onslaught: Reaver Attack Squads may be selected as Troops and may fulfil compulsory Troops; at "
        "least one compulsory Troops choice must be a Reaver Attack Squad. Cthonian Encirclement: after both armies are "
        "selected, nominate up to two Sons of Horus Infantry units; they gain Outflank (their Dedicated Transports too, "
        "entering with them; an Independent Character attached at the start may Outflank with them). For one of the two "
        "the player chooses the side table edge instead of rolling. Lodge Ceremony: once per battle, at the beginning of "
        "a Sons of Horus player turn, the Warlord may declare a Lodge Ceremony: until the end of that turn all non-Vehicle "
        "Sons of Horus units gain Fleet. Cut Them Apart: in the first round of a close combat, a Sons of Horus unit that "
        "charged an enemy unit already engaged with another friendly Sons of Horus unit may re-roll To Hit rolls of 1 "
        "(only in the player turn it charged).\n"
        "LIMITATIONS - The Detachment must include a Legion Centurion upgraded to a Master of Signals Consul. At least "
        "one compulsory Troops choice must be a Reaver Attack Squad. At least as many Fast Attack as Heavy Support "
        "choices. No Fortification or Allied Detachment."),
    # units
    "Chosen of the Warmaster": (
        "A Sons of Horus Praetor, Ezekyle Abaddon or Horus Lupercal may select one Justaerin Terminator Squad as a "
        "retinue; it then does not occupy a separate Elites choice. 0-1 per Detachment otherwise."),
    "Justaerin Primus": ("While Falkus Kibre remains alive, his Justaerin Terminator Squad has Fearless. The squad may "
                         "purchase the Furious Charge Veteran Skill for +4 points per model."),
    "Cthonian Retinue": (
        "One Chieftain Squad may be selected as the retinue of a Sons of Horus Praetor or an appropriate named Sons of "
        "Horus Independent Character. It does not occupy a separate Elites choice; the Character and Chieftain Squad "
        "count as a single HQ selection."),
    "Jump Assault": ("The entire squad may purchase Jump Packs for +15 points per model: the unit becomes Jump Infantry, "
                     "follows the normal Jump Infantry rules and may not select a Dedicated Transport."),
    "Daemonic Talons": "Daemonic Talons are Rending Weapons.",
    "Damned": ("A Luperci Pack may never count as a Scoring Unit. No Independent Character may join a Luperci Pack unless "
               "it has the Daemon special rule."),
    # characters
    "Cthonian Dreadplate": ("Counts as Cataphractii Terminator Armour. Add +1 to the Reserve roll made for Abaddon and any "
                            "unit with which he began the battle in Reserve."),
    "First Captain": "Listed in Abaddon's special rules; the army book gives no text for this rule (see questions).",
    "Master of the Justaerin": (
        "If Abaddon is the army's Warlord, the army may include one additional Justaerin Terminator Squad beyond the "
        "normal 0-1 limit. A Justaerin Terminator Squad containing Abaddon gains Fearless and may purchase the Furious "
        "Charge Veteran Skill for +4 points per model."),
    "Command Retinue (Abaddon)": ("Abaddon may select a Justaerin Terminator Squad or a Legion Terminator Command Squad "
                                  "as his retinue. It does not occupy a separate Force Organisation slot."),
    "Mourn-it-All": ("A Master-crafted Power Weapon. A natural To Wound roll of 6 made with Mourn-it-All inflicts a "
                     "Massive Wound (D3) instead of a normal Wound."),
    "Strategist": "Add +1 to Reserve rolls made by a Sons of Horus army containing Horus Aximand.",
    "Command Retinue (Aximand)": ("Aximand may select one Legion Command Squad or Chieftain Squad as his retinue. It does "
                                  "not occupy a separate Force Organisation slot."),
    "The Last Wolf": (
        "The first time Loken is reduced to 0 Wounds, place a marker at his final position and remove him (not if the "
        "attack inflicted a Massive Wound). At the beginning of the next Sons of Horus turn roll a D6: 3+ - return Loken "
        "with 1 Wound at the marker (or as close as legally possible); 1-2 - he remains a casualty. Once per battle."),
    "Command Retinue (Loken)": ("Loken may select one Legion Command Squad or one Legion Veteran Squad as his retinue. It "
                                "does not occupy a separate Force Organisation slot."),
    "Banner of the Warmaster": ("Counts as a Legion Standard. Maloghurst therefore counts as the squad's Standard "
                                "Bearer."),
    "Broken Body": ("Reduce Normal, Advance, Charge, Fall Back and Consolidation movement made by Maloghurst's unit by 1\" "
                    "(minimum 1\"). Maloghurst's unit may not Pursue a retreating enemy."),
    "Maloghurst the Twisted": (
        "One Legion Command Squad containing a Standard Bearer may replace that model with Maloghurst (total cost 65 "
        "points; do not also pay for the Standard Bearer or Legion Standard). Maloghurst remains permanently part of the "
        "Command Squad, is a Character but not an Independent Character, and occupies no Force Organisation selection."),
    "The Either": ("Tybalt Marr and one Infantry unit he has joined before deployment gain Outflank. Marr must enter play "
                   "with that unit."),
    "Hunter of the Broken Legions": ("Marr and any Sons of Horus unit he has joined may re-roll To Hit rolls of 1 during "
                                     "the first Assault phase after entering play from Reserve."),
    "Command Retinue (Marr)": ("Marr may select one Legion Veteran Squad or Reaver Attack Squad as his retinue. It does "
                               "not occupy a separate Force Organisation slot."),
    "Axe Serpentis": "A Master-crafted Power Weapon. Attacks made with it are resolved at +1 Strength.",
    "First Reaver": ("Ashurhaddon may select one Reaver Attack Squad as his personal retinue. It does not occupy a "
                     "separate Force Organisation slot."),
    "Master of the True Sons": ("While Ashurhaddon is joined to a Reaver Attack Squad or Chieftain Squad, that unit may "
                                "re-roll failed Morale and Pinning tests."),
    "Falkus Kibre": ("One Justaerin Terminator may be upgraded to Falkus Kibre for +28 points (total 85 points). He "
                     "remains part of the squad, is a Character but not an Independent Character and occupies no "
                     "separate selection. He may take any normal Justaerin weapon replacement, but no Heavy weapon."),
    "Tarik Torgaddon": (
        "A Legion Veteran Squad, or a Legion Tactical Squad containing 20 models, may replace its Sergeant with Tarik "
        "Torgaddon (total cost 105 points; do not also pay for the Sergeant). Torgaddon remains part of the squad for the "
        "entire battle, is a Character but not an Independent Character, and occupies no Force Organisation selection. "
        "No Independent Character may join Torgaddon's squad."),
    "Defensive Grenades": "Listed in Aximand's wargear; the army book gives no rules text (see questions).",
    # Horus
    "Serpent's Scales": "The Serpent's Scales count as Primarch Armour.",
    "Worldbreaker": ("A Master-crafted Thunder Hammer. When Horus attacks with Worldbreaker he resolves his attacks at "
                     "Initiative 3 instead of Initiative 1. All other Thunder Hammer rules apply normally."),
    "The Talon of Horus": (
        "In close combat follows all rules for a Master-crafted Lightning Claw. Incorporates a Twin-linked Storm Bolter: "
        "each time it fires choose one ammunition profile (Banestrike, Dragonfire, Hellfire, Kraken, Vengeance); only one "
        "type per firing, never combined. Firing it does not prevent Horus from using the Talon or Worldbreaker in the "
        "following Assault phase."),
    "Will of the Warmaster": (
        "Any friendly unit with Legiones Astartes (Sons of Horus) which can draw line of sight to Horus may re-roll "
        "failed Morale and Pinning tests. Such units with at least one model within 12\" of Horus instead have Fearless. "
        "This is Horus' unique Warlord ability; he does not select a normal Warlord Trait."),
    "Master of the Speartip": (
        "When using Tip of the Spear, up to two Sons of Horus Infantry units selected from Elites may deploy using Deep "
        "Strike instead of one. The Independent Character allowance is unchanged. All such units obey the normal "
        "requirements of Tip of the Spear and begin the battle in Reserve."),
    "The First Company": (
        "Up to two Legion Terminator Squads in an army containing Horus may be selected as Troops instead of Elites; one "
        "of these two may instead be a Justaerin Terminator Squad (which then does not count against the 0-1 limit). "
        "Squads selected as Troops this way may fulfil compulsory Troops selections."),
    "The Vengeful Spirit": (
        "Spearhead Assault: reduce the points cost of every Legion Drop Pod and Anvillus Pattern Dreadclaw Drop Pod "
        "purchased by the army by 10 points (no other change). Orbital Bombardment: once per battle, from the second turn "
        "onwards, instead of shooting Horus may call down a Vengeful Spirit Lance Strike (Unlimited range, S10, AP1, "
        "Ordnance 1, Blast) while on the battlefield and not in close combat or a Primarch Duel: place the marker "
        "anywhere, no line of sight needed, scatter D6\" unless a Hit is rolled."),
    "Primarch Retinue (Horus)": (
        "Horus may select a Legion Honour Guard Squad, Legion Terminator Command Squad or Justaerin Terminator Squad as "
        "his Primarch Retinue. A Justaerin Terminator Squad selected this way does not count against the 0-1 limit, "
        "gains Furious Charge at no cost and may purchase any upgrades normally available to it (including Falkus "
        "Kibre)."),
    "Great Crusade Panoply": ("Horus may exchange Worldbreaker and the Talon of Horus for a Master-crafted Power Sword and "
                              "a Master-crafted Seeker Bolter with Special Issue Ammunition, reducing his cost by 25 "
                              "points. Only one ammunition type may be used each time the Seeker Bolter is fired."),
    # Horus Ascended
    "Serpent's Scales (Ascended)": "Confer a 1+ Armour Save and a 3+ Invulnerable Save.",
    "Worldbreaker (Ascended)": ("A Master-crafted Thunder Hammer. Horus strikes with it at Initiative 4 rather than "
                                "Initiative 1. All other Thunder Hammer rules apply normally."),
    "The Talon of Horus (Ascended)": (
        "Counts as a Master-crafted Lightning Claw and grants +1 Strength. Its Twin-linked Storm Bolter may use any "
        "ammunition of the Talon of Horus (Banestrike, Dragonfire, Hellfire, Kraken, Vengeance). Horus may divide his "
        "Attacks between Worldbreaker and the Talon in any combination."),
    "Will of the Warmaster (Ascended)": ("Friendly Sons of Horus units with line of sight to Horus may re-roll failed "
                                         "Morale and Pinning tests; those with at least one model within 12\" of Horus "
                                         "are Fearless."),
    "Master of the Speartip (Ascended)": ("When Horus commands the army, one additional eligible Sons of Horus Elites "
                                          "unit may use the Legion's Tip of the Spear deployment rule."),
    "The First Company (Ascended)": (
        "Horus may take a Justaerin Terminator Squad as his retinue instead of a normal Command Squad or Terminator "
        "Command Squad. Legion Terminators and Justaerin also receive any additional availability granted by the Sons of "
        "Horus army list while Horus is present."),
    "The Vengeful Spirit (Ascended)": (
        "Drop Pods and Dreadclaws in Horus' army use the reduced costs of the Sons of Horus army list (-10 points). Once "
        "per battle Horus may call down a Lance Strike in his Shooting phase (Unlimited, S10, AP1, Ordnance 1, Blast), "
        "resolved using the normal rules for an Orbital Strike."),
    "Vessel of the Four": (
        "Horus counts as a Daemon for all rules, weapons and abilities which specifically affect Daemons. He bears the "
        "favour of all four Chaos Gods but receives no additional characteristic bonuses from Blessings of the Four "
        "(already in his profile)."),
    "Favoured of the Dark Gods": (
        "Whenever an enemy psychic power directly targets or affects Horus, roll a D6 after the Psychic Test is passed: "
        "on a 3+ it is nullified against him. A power which directly targets or affects a friendly unit within 6\" of "
        "Horus is nullified on a 4+."),
    "Blessings of the Four": (
        "If Horus Ascended is in the army, Traitor Legiones Astartes Infantry units and Independent Characters may "
        "purchase one Blessing of Chaos (every model in a unit the same Blessing; Primarchs may not): Khorne +5/model or "
        "+20 (IC) - +1 Attack; Slaanesh +4/model or +15 - +1 Initiative; Nurgle +7/model or +25 - +1 Toughness and Slow "
        "and Purposeful (not Bikes, Jetbikes or Jump Infantry); Tzeentch +8/model or +25 - a 5+ Invulnerable Save, or +1 "
        "to an existing Invulnerable Save (max 4+)."),
    "The Warmaster Must Lead": ("Horus Ascended may never voluntarily begin the battle in Reserve and must be deployed at "
                                "the start whenever the mission permits. If a mission requires him to begin in Reserve, "
                                "he automatically arrives on the first turn."),
    "Blessing of Khorne": "+1 Attack.",
    "Blessing of Slaanesh": "+1 Initiative.",
    "Blessing of Nurgle": "+1 Toughness and Slow and Purposeful. Not for Bikes, Jetbikes or Jump Infantry.",
    "Blessing of Tzeentch": ("Gain a 5+ Invulnerable Save, or improve an existing Invulnerable Save by 1, to a maximum of "
                             "4+."),
}

TALON_AMMO = {
    "Talon of Horus - Banestrike": ('18"', "4", "4", "Assault 2, Twin-linked, Banestrike"),
    "Talon of Horus - Dragonfire": ('24"', "4", "5", "Assault 2, Twin-linked, Ignores Cover"),
    "Talon of Horus - Hellfire": ('24"', "X", "5", "Assault 2, Twin-linked, Poisoned (2+)"),
    "Talon of Horus - Kraken": ('30"', "4", "4", "Assault 2, Twin-linked"),
    "Talon of Horus - Vengeance": ('18"', "4", "3", "Assault 2, Twin-linked, Gets Hot"),
}
MULTI = {
    "The Talon of Horus": {"Talon of Horus (close combat)": ("-", "User", "-", "Master-crafted Lightning Claw"),
                           **TALON_AMMO},
    "The Talon of Horus (Ascended)": {"Talon of Horus - Ascended (close combat)":
                                      ("-", "+1", "-", "Master-crafted Lightning Claw"), **TALON_AMMO},
    "Master-crafted Seeker Bolter": {
        "Seeker Bolter - Dragonfire Bolts": ('24"', "4", "5", "Rapid Fire, Ignores Cover, Master-crafted"),
        "Seeker Bolter - Hellfire Bolts": ('24"', "X", "5", "Rapid Fire, Poisoned (2+), Master-crafted"),
        "Seeker Bolter - Kraken Bolts": ('30"', "4", "4", "Rapid Fire, Master-crafted"),
        "Seeker Bolter - Vengeance Rounds": ('18"', "4", "3", "Rapid Fire, Gets Hot, Master-crafted")},
}
WEAPONS_ = {
    "Banestrike Bolter": ('18"', "4", "4", "Rapid Fire, Banestrike"),
    "Cthonian Culling Blade": ("-", "User", "-", "Rending (5+)"),
    "Daemonic Talons": ("-", "User", "-", "Rending"),
    "Master-crafted Power Fist": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Master-crafted"),
    "Master-crafted Power Sword": ("-", "User", "-", "Ignores Armour Saves, Master-crafted"),
    "Master-crafted Storm Bolter": ('24"', "4", "5", "Assault 2, Master-crafted"),
    "Mourn-it-All": ("-", "User", "-", "Power Weapon, Master-crafted, Massive Wound (D3) on a natural 6 To Wound"),
    "Meltagun Pistol": ('6"', "8", "1", "Pistol, Melta"),
    "Master-crafted Rending Weapon": ("-", "User", "-", "Rending, Master-crafted"),
    "Master-crafted Lightning Claw": ("-", "User", "-",
                                      "Power Weapon, re-roll failed To Wound rolls, Specialist Weapon, Master-crafted"),
    "Axe Serpentis": ("-", "+1", "-", "Power Weapon, Master-crafted"),
    "Worldbreaker": ("-", "x2", "-", "Master-crafted Thunder Hammer, Initiative 3"),
    "Worldbreaker (Ascended)": ("-", "x2", "-", "Master-crafted Thunder Hammer, Initiative 4"),
    "Vengeful Spirit Lance Strike": ("Unlimited", "10", "1", "Ordnance 1, Blast"),
}
WEAPON_RULES_ = {
    "Banestrike Bolter": ["Banestrike"], "Cthonian Culling Blade": ["Rending (5+)"],
    "Daemonic Talons": ["Daemonic Talons", "Rending"],
    "Master-crafted Power Fist": ["Unwieldy", "Master-Crafted"], "Master-crafted Power Sword": ["Master-Crafted"],
    "Master-crafted Storm Bolter": ["Master-Crafted"], "Mourn-it-All": ["Mourn-it-All", "Master-Crafted"],
    "Meltagun Pistol": ["Melta"], "Master-crafted Rending Weapon": ["Rending", "Master-Crafted"],
    "Master-crafted Lightning Claw": ["Master-Crafted"], "Axe Serpentis": ["Axe Serpentis", "Master-Crafted"],
    "Worldbreaker": ["Worldbreaker", "Concussive", "Master-Crafted"],
    "Worldbreaker (Ascended)": ["Worldbreaker (Ascended)", "Concussive", "Master-Crafted"],
    "The Talon of Horus": ["The Talon of Horus", "Banestrike", "Twin-Linked"],
    "The Talon of Horus (Ascended)": ["The Talon of Horus (Ascended)", "Banestrike", "Twin-Linked"],
    "Master-crafted Seeker Bolter": ["Master-Crafted", "Special Issue Ammunition"],
    "Chainaxe": ["Chainaxe"],
}
WARGEAR_ = {
    "Banestrike Ammunition": RULES["Banestrike Ammunition"],
    "Teleportation Transponders": RULES["Teleportation Transponders"],
    "Cthonian Dreadplate": RULES["Cthonian Dreadplate"],
    "Defensive Grenades": RULES["Defensive Grenades"],
    "Banner of the Warmaster": RULES["Banner of the Warmaster"],
    "Serpent's Scales": (RULES["Serpent's Scales"], ["Primarch Armour"]),
    "Serpent's Scales (Ascended)": RULES["Serpent's Scales (Ascended)"],
}

BOLT_WEAPONS = ["Bolter", "Foeblaster Boltgun", "Combi-Bolter", "Storm Bolter", "Combi-Flamer", "Combi-Grenade Launcher",
                "Combi-Meltagun", "Combi-Plasma Gun", "Combi-Volkite Charger", "Combi-Weapon"]
COMBIS = [("Combi-Flamer", 10), ("Combi-Volkite Charger", 10), ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15)]


def register():
    RULES["Primarch Armour"] = PRIMARCH_RULES["Primarch Armour"]
    register_data(rules=RULES, weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_, multi_profile=MULTI)


# ---------------------------------------------------------------- local helpers
def char_groups(e):
    """All selection groups belonging to entry e itself (not to nested entries)."""
    out = []
    todo = list(e.findall("selectionEntryGroups/selectionEntryGroup"))
    while todo:
        g = todo.pop()
        out.append(g)
        todo += g.findall("selectionEntryGroups/selectionEntryGroup")
    return out


def unit_type(e):
    for p in e.findall("profiles/profile"):
        for c in p.iter("characteristic"):
            if c.get("name") == "Unit Type":
                return c.text or ""
    return None


def character_entries(roots):
    seen = set()
    for r in roots:
        for e in r.iter("selectionEntry"):
            t = unit_type(e)
            if t and "Character" in t and id(e) not in seen:
                seen.add(id(e))
                yield e


def add_character_variant(roots, base, new, extra):
    """Characters able to select `base` in a weapon slot may select `new` for +extra."""
    n = 0
    for e in character_entries(roots):
        for g in char_groups(e):
            links = g.find("entryLinks")
            if links is None:
                continue
            targets = {lk.get("targetId") for lk in links}
            if W(base) not in targets or W(new) in targets:
                continue
            for lk in list(links):
                if lk.get("targetId") != W(base):
                    continue
                links.append(link(uid(lk.get("id"), "variant", new), W(new), new, cost=extra or None))
                n += 1
    return n


def unique_across(legion_entry, name, ids):
    """Several copies of the same character (e.g. in different retinues): at most one in the army."""
    groups = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            groups.append(all_of(cond(a, "roster", "atLeast", 1), cond(b, "roster", "atLeast", 1)))
    if groups:
        grp = el("conditionGroup", {"type": "or"}, [wrap("conditionGroups", groups)])
        add_mods(legion_entry, [modifier("add", "error", f"{name} may only be included once in the army.",
                                         groups=[grp])])


def find_child(e, name):
    for x in e.iter("selectionEntry"):
        if x.get("name") == name:
            return x
    raise KeyError(name)


def model_limits(e):
    return uid(e.get("id"), "min"), uid(e.get("id"), "max")


def strip_role_mods(e):
    """Retinue copies of normal units: drop the Force Organisation modifiers of the original."""
    ms = e.find("modifiers")
    if ms is None:
        return e
    for m in list(ms):
        if m.get("field") == "category" or (m.get("type") == "add" and m.get("field") == "error"):
            ms.remove(m)
    return e


def no_torgaddon(e):
    """Retinue copies of the Veteran Squad: Torgaddon's squad may not be joined by an Independent Character."""
    for x in e.iter("selectionEntry"):
        if x.get("name", "").startswith("Tarik Torgaddon"):
            x.set("hidden", "true")
            for c in x.findall("constraints/constraint"):
                if c.get("type") == "max" and c.get("scope") == "parent":
                    c.set("value", "0")
    return e


def all_entries(ctx):
    seen, out = set(), []
    for e in ctx.all_entries():
        if id(e) not in seen:
            seen.add(id(e))
            out.append(e)
    return out


def entry_models(e):
    return [x for x in e.findall("selectionEntries/selectionEntry") if x.get("type") == "model"]


# ---------------------------------------------------------------- units
def justaerin(key="Justaerin Terminator Squad", root=True, variant=None):
    """variant: None (normal), 'abaddon' (Abaddon's retinue), 'horus' (Horus' Primarch Retinue)."""
    name = "Justaerin Terminator Squad"
    u = uid("unit", key)
    jm = uid("model", u, "Justaerin Terminator")
    fk = uid("model", u, "Falkus Kibre")
    prof = unit_profile(u, "Justaerin Terminator", "Infantry", 5, 4, 4, 4, 2, 3, 2, 9, "2+/4+")
    jmin, jmax = uid(jm, "min"), uid(jm, "max")
    heavy_opts = [("Heavy Flamer", 10), ("Reaper Autocannon", 20), ("Multi-Melta", 25)]
    pid, pair = model_pair_claws(u, "Pair of Lightning Claws (replaces both weapons)", u, [jm], 0)
    jmodel = entry(jm, "Justaerin Terminator", typ="model", cost=57,
                   mods=specials_decrement(jm, jmin, jmax, [fk], u),
                   constraints=[constraint(jmin, "min", 5), constraint(jmax, "max", 10)],
                   profiles=[prof], links=[gear(jm, k) for k in ["Cataphractii Terminator Armour", "Foeblaster Boltgun",
                                                                 "Power Weapon"]])
    fpair = entry(uid(fk, "pair"), "Pair of Lightning Claws (replaces both)", links=[gear(uid(fk, "pair"),
                                                                                          "Pair of Lightning Claws")])
    falkus = entry(fk, "Falkus Kibre", typ="model", cost=85,
                   constraints=[constraint(uid(fk, "max"), "max", 1), unique(fk)],
                   profiles=[unit_profile(u, "Falkus Kibre", "Infantry (Character)", 5, 5, 4, 4, 2, 4, 3, 9, "2+/4+")],
                   infolinks=rules_links(["Falkus Kibre", "Justaerin Primus"], key=fk),
                   links=[gear(fk, "Cataphractii Terminator Armour")],
                   groups=[slot(fk, "Power weapon or Power fist", "Power Weapon",
                                [("Power Fist", 0), ("Chainfist", 5), (fpair, None)]),
                           slot(fk, "Replace Foeblaster Boltgun", "Foeblaster Boltgun", COMBIS,
                                zero_if=[has(uid(fk, "pair"), "parent")])])
    heavy, hmx = pool(u, "Heavy Weapons (up to two Justaerin per five models, replace Foeblaster Boltgun)", u,
                      heavy_opts, 0, every=5)
    add_mods(heavy, [modifier("increment", hmx, 1, repeats=[repeat("model", u, 5)])])
    swaps = [model_swaps(u, "Justaerin: Power weapon or Power fist (any number)", u, [jm],
                         [("Power Fist", 0), ("Chainfist", 5)], minus=[pid]),
             model_swaps(u, "Justaerin: replace Foeblaster Boltgun (any number)", u, [jm], COMBIS,
                         minus=[W(n) for n, _ in heavy_opts] + [pid], entries=[pair])]
    # Banestrike: +2 per eligible model (models that kept a bolt weapon)
    bid = uid(u, "banestrike")
    bmods = [modifier("increment", PTS, 2, repeats=[repeat("model", u, 1)])]
    bmods += [modifier("decrement", PTS, 2, repeats=[repeat(W(n), u, 1)]) for n, _ in heavy_opts]
    bmods += [modifier("decrement", PTS, 2, repeats=[repeat(p, u, 1)]) for p in (pid, uid(fk, "pair"))]
    bane = entry(bid, "Banestrike Ammunition (all eligible models)", cost=0, mods=bmods,
                 constraints=[constraint(uid(bid, "max"), "max", 1)], links=[gear(bid, "Banestrike Ammunition")])
    tp = option(u, "Teleportation Transponders (squad)", 15, item="Teleportation Transponders")
    ents = [jmodel, falkus, bane, tp]
    rls = [LR, "Chosen of the Warmaster"]
    if variant == "horus":
        rls.append("Furious Charge")
    else:
        fc = entry(uid(u, "fc"), "Furious Charge Veteran Skill (entire squad)", cost=0,
                   mods=[modifier("increment", PTS, 4, repeats=[repeat("model", u, 1)])],
                   constraints=[constraint(uid(u, "fc", "max"), "max", 1)], infolinks=rules_links(["Furious Charge"],
                                                                                                  key=uid(u, "fc")))
        if variant != "abaddon":
            add_mods(fc, [modifier("set", "hidden", "true", conds=[cond(fk, u, "lessThan", 1)]),
                          modifier("set", uid(u, "fc", "max"), 0, conds=[cond(fk, u, "lessThan", 1)])])
        ents.append(fc)
    if variant == "abaddon":
        rls += ["Master of the Justaerin", "Fearless"]
    cats = [foc(ELITES, "Elites", u)] if root else []
    cons = [force_limit(u)] if root else []
    tr = transports(u, u, ["Land Raider Phobos", "Land Raider Proteus", "Anvillus Pattern Dreadclaw Drop Pod",
                           "Legion Spartan Assault Tank"], orbital=False)
    return entry(u, name, typ="unit", cost=0, cats=cats, constraints=cons,
                 infolinks=rules_links(rls, key=u), entries=ents, groups=[*swaps, heavy, tr])


def reavers(key="Reaver Attack Squad", root=True):
    name = "Reaver Attack Squad"
    u = uid("unit", key)
    rid, cid = uid("model", u, "Reaver"), uid("model", u, "Reaver Chieftain")
    kit = ["Power Armour", "Bolt Pistol", "Chainaxe", "Frag Grenades"]
    chief = entry(cid, "Reaver Chieftain", typ="model",
                  constraints=[constraint(uid(cid, "min"), "min", 1), constraint(uid(cid, "max"), "max", 1)],
                  profiles=[unit_profile(u, "Reaver Chieftain", "Infantry (Character)", 4, 4, 4, 4, 1, 4, 2, 9, "3+")],
                  links=[gear(cid, k) for k in ["Power Armour", "Frag Grenades"]],
                  groups=[pa_armoury(cid, u, 10, slots=["Bolt Pistol", "Chainaxe"])])
    rv = entry(rid, "Reaver", typ="model", cost=22,
               constraints=[constraint(uid(rid, "min"), "min", 4), constraint(uid(rid, "max"), "max", 9)],
               profiles=[unit_profile(u, "Reaver", "Infantry", 4, 4, 4, 4, 1, 4, 1, 9, "3+")],
               links=[gear(rid, k) for k in kit])
    pistols, _ = pool(u, "Up to two Reavers: replace Bolt Pistol", u,
                      [("Flamer", 5), ("Meltagun", 10), ("Plasma Gun", 15), ("Plasma Pistol", 15)], 2)
    heavy, _ = pool(u, "One Reaver per five models: Power Fist (replaces Chainaxe) or Pair of Lightning Claws "
                       "(replaces Bolt Pistol and Chainaxe)", u, [("Power Fist", 15), ("Pair of Lightning Claws", 15)],
                    0, every=5)
    honours = model_takes(u, "Reavers: Terminator Honours (any number)", u, [rid], [("Terminator Honours", 15)])
    jp_id = uid("squadwide", u, "Jump Packs (entire squad)")
    jp = per_model(u, "Jump Packs (entire squad)", 15, u, ["Jump Pack"])
    add_to(jp, "infoLinks", rules_links(["Jump Assault"], key=jp_id))
    cats, mods, cons = [], [], []
    if root:
        cats = [foc(FA, "Fast Attack", u)]
        br = [rite("The Black Reaving")]
        mods = [modifier("set-primary", "category", TROOPS, conds=br), modifier("remove", "category", FA, conds=br),
                modifier("add", "category", gs.CAT_LINE, conds=br)]
    return entry(u, name, typ="unit", cost=110 - 4 * 22, cats=cats, mods=mods, constraints=cons,
                 infolinks=rules_links([LR, "Furious Charge", "Jump Assault"], key=u),
                 entries=[chief, rv, jp, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[pistols, heavy, honours,
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos",
                                           "Land Raider Proteus"],
                                    block_if=[has(jp_id, u)])])


def chieftains(key="Chieftain Squad", root=True):
    name = "Chieftain Squad"
    u = uid("unit", key)
    cid, pid = uid("model", u, "Chieftain"), uid("model", u, "Chieftain Prime")
    kit = ["Power Armour", "Boarding Shield", "Bolter", "Cthonian Culling Blade", "Frag Grenades"]
    blade = [("Power Weapon", 5), ("Power Fist", 10), ("Lightning Claw", 10), ("Thunder Hammer", 15)]
    bolter = [("Foeblaster Boltgun", 5)] + COMBIS
    prime = entry(pid, "Chieftain Prime", typ="model",
                  constraints=[constraint(uid(pid, "min"), "min", 1), constraint(uid(pid, "max"), "max", 1)],
                  profiles=[unit_profile(u, "Chieftain Prime", "Infantry (Character)", 5, 4, 4, 4, 2, 4, 3, 10,
                                         "3+/5+")],
                  links=[gear(pid, k) for k in kit],
                  groups=[slot(pid, "Replace Cthonian Culling Blade", "Cthonian Culling Blade", blade),
                          slot(pid, "Replace Bolter", "Bolter", bolter),
                          pa_armoury(pid, u, 10, skip=("Boarding Shield", "Combat Shield"))])
    ch = entry(cid, "Chieftain", typ="model", cost=40,
               constraints=[constraint(uid(cid, "min"), "min", 4), constraint(uid(cid, "max"), "max", 9)],
               profiles=[unit_profile(u, "Chieftain", "Infantry", 5, 4, 4, 4, 2, 4, 2, 9, "3+/5+")],
               links=[gear(cid, k) for k in kit])
    swaps = [model_swaps(u, "Chieftains: replace Cthonian Culling Blade (any number)", u, [cid], blade),
             model_swaps(u, "Chieftains: replace Bolter (any number)", u, [cid], bolter)]
    cats = [foc(ELITES, "Elites", u)] if root else []
    cons = [force_limit(u)] if root else []
    return entry(u, name, typ="unit", cost=200 - 4 * 40, cats=cats, constraints=cons,
                 infolinks=rules_links([LR, "Stubborn", "Cthonian Retinue"], key=u),
                 entries=[prime, ch, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[*swaps, transports(u, u, ["Legion Rhino Armoured Carrier", "Anvillus Pattern Dreadclaw Drop Pod",
                                                   "Land Raider Phobos", "Land Raider Proteus"])])


def luperci():
    name = "Luperci Pack"
    u = uid("unit", name)
    lid, cid = uid("model", u, "Luperci"), uid("model", u, "Luperci Chieftain")
    kit = ["Power Armour", "Bolt Pistol", "Daemonic Talons", "Frag Grenades"]
    chief = entry(cid, "Luperci Chieftain", typ="model",
                  constraints=[constraint(uid(cid, "min"), "min", 1), constraint(uid(cid, "max"), "max", 1)],
                  profiles=[unit_profile(u, "Luperci Chieftain", "Infantry (Character)", 4, 4, 5, 4, 2, 4, 3, 9,
                                         "3+/5+")],
                  links=[gear(cid, k) for k in kit])
    lp = entry(lid, "Luperci", typ="model", cost=25,
               constraints=[constraint(uid(lid, "min"), "min", 4), constraint(uid(lid, "max"), "max", 9)],
               profiles=[unit_profile(u, "Luperci", "Infantry", 4, 4, 5, 4, 2, 4, 2, 9, "3+/5+")],
               links=[gear(lid, k) for k in kit])
    sp, _ = pool(u, "One Luperci per five models: replace Bolt Pistol", u,
                 [("Flamer", 5), ("Meltagun", 10), ("Plasma Gun", 15)], 0, every=5)
    e = entry(u, name, typ="unit", cost=150 - 4 * 25, cats=[foc(ELITES, "Elites", u)], constraints=[force_limit(u)],
              infolinks=rules_links([LR, "Daemon", "Fearless", "Bulky", "Furious Charge", "Damned"], key=u),
              entries=[chief, lp], groups=[sp])
    return allegiance_only(e, loyalist=False)


# ---------------------------------------------------------------- characters
def krak(key, melta=False, extra=()):
    items = [("Krak Grenades", 2)] + ([("Melta Bombs", 5)] if melta else []) + list(extra)
    return take(key, "Wargear", items)


def characters(ctx):
    out = []
    # Abaddon
    abd_ret = retinue_links("abaddon", [justaerin("abaddon-justaerin", root=False, variant="abaddon"),
                                        L2.terminator_command_squad("abaddon")])
    out.append(named_character(LR, "Ezekyle Abaddon, First Captain", 210, (6, 5, 5, 4, 3, 5, 3, 10, "2+/4+"),
                               ["Cthonian Dreadplate", "Master-crafted Power Fist", "Master-crafted Power Sword",
                                "Master-crafted Storm Bolter", "Banestrike Ammunition"],
                               ["First Captain", "Master of the Justaerin", "Command Retinue (Abaddon)",
                                "Cthonian Dreadplate"],
                               retinue=abd_ret, min_points=1500, profile_name="Ezekyle Abaddon"))
    # Aximand
    ax = uid("unit", "Horus Aximand, \"Little Horus\"")
    out.append(named_character(LR, "Horus Aximand, \"Little Horus\"", 175, (6, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
                               ["Artificer Armour", "Combat Shield", "Mourn-it-All", "Meltagun Pistol", "Bolter",
                                "Frag Grenades", "Defensive Grenades"],
                               ["Strategist", "Command Retinue (Aximand)"],
                               retinue=retinue_links("aximand", [command_squad_for("aximand", ax),
                                                                 chieftains("aximand-chieftains", root=False)]),
                               loyalist=False, profile_name="Horus Aximand",
                               extra_groups=[krak(ax, extra=[("Banestrike Ammunition", 5)])]))
    # Loken
    lk = uid("unit", "Garviel Loken")
    vets = no_torgaddon(strip_role_mods(clone(ctx.unit("Legion Veteran Squad"), "loken-vets")))
    out.append(named_character(LR, "Garviel Loken", 115, (5, 5, 4, 4, 2, 5, 3, 9, "2+/5+"),
                               ["Artificer Armour", "Refractor Field", "Master-crafted Rending Weapon", "Bolt Pistol",
                                "Frag Grenades"],
                               ["The Last Wolf", "Command Retinue (Loken)"], master=False, loyalist=True,
                               retinue=retinue_links("loken", [command_squad_for("loken", lk), vets]),
                               extra_groups=[krak(lk)]))
    # Tybalt Marr
    mr = uid("unit", "Tybalt Marr, \"The Either\"")
    mvets = no_torgaddon(strip_role_mods(clone(ctx.unit("Legion Veteran Squad"), "marr-vets")))
    out.append(named_character(LR, "Tybalt Marr, \"The Either\"", 155, (6, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
                               ["Artificer Armour", "Refractor Field", "Master-crafted Lightning Claw", "Bolt Pistol",
                                "Frag Grenades"],
                               ["The Either", "Hunter of the Broken Legions", "Command Retinue (Marr)"],
                               retinue=retinue_links("marr", [mvets, reavers("marr-reavers", root=False)]),
                               loyalist=False, profile_name="Tybalt Marr", extra_groups=[krak(mr, melta=True)]))
    # Ashurhaddon
    ash = uid("unit", "Vheren Ashurhaddon")
    out.append(named_character(LR, "Vheren Ashurhaddon", 185, (6, 5, 4, 4, 3, 5, 4, 10, "2+/4+"),
                               ["Artificer Armour", "Iron Halo", "Axe Serpentis", "Bolt Pistol", "Frag Grenades"],
                               ["Furious Charge", "First Reaver", "Master of the True Sons"],
                               retinue=retinue_links("ashurhaddon", [reavers("ashurhaddon-reavers", root=False)]),
                               loyalist=False, extra_groups=[krak(ash, melta=True)]))
    return out


def weapons_choice(key):
    wb = entry(uid(key, "wb-talon"), "Worldbreaker and the Talon of Horus",
               links=[gear(uid(key, "wb-talon"), "Worldbreaker"), gear(uid(key, "wb-talon"), "The Talon of Horus")])
    gc = entry(uid(key, "panoply"), "Great Crusade Panoply", cost=-25,
               infolinks=rules_links(["Great Crusade Panoply"], key=uid(key, "panoply")),
               links=[gear(uid(key, "panoply"), "Master-crafted Power Sword"),
                      gear(uid(key, "panoply"), "Master-crafted Seeker Bolter")])
    return slot(key, "Weapons", None, [(gc, None)], default_is_entry=wb)


def horus():
    ret = primarch_retinue("horus", extra=[justaerin("horus-justaerin", root=False, variant="horus")])
    return primarch(LR, "Horus Lupercal, the Warmaster", 525, (8, 6, 6, 6, 6, 6, 6, 10, "1+/4+"),
                    ["Serpent's Scales", "Frag Grenades", "Krak Grenades"],
                    ["Will of the Warmaster", "Master of the Speartip", "The First Company", "The Vengeful Spirit",
                     "Primarch Retinue (Horus)", "Primarch Armour"],
                    retinue=ret, other=HORUS_ASC, profile_name="Horus Lupercal",
                    extra_groups=[weapons_choice(HORUS)], extra_entries=[lance_strike(HORUS)])


def lance_strike(key):
    e = entry(uid(key, "lance"), "Vengeful Spirit Lance Strike (once per battle)",
              constraints=[constraint(uid(key, "lance", "min"), "min", 1), constraint(uid(key, "lance", "max"), "max", 1)],
              links=[gear(uid(key, "lance"), "Vengeful Spirit Lance Strike")])
    return e


def horus_ascended():
    ret = primarch_retinue("horus-asc", extra=[justaerin("horus-asc-justaerin", root=False, variant="horus")])
    return primarch(LR, "Horus Ascended, the Warmaster", 725, (9, 7, 7, 7, 7, 7, 7, 10, "1+/3+"),
                    ["Serpent's Scales (Ascended)", "Worldbreaker (Ascended)", "The Talon of Horus (Ascended)",
                     "Frag Grenades", "Krak Grenades"],
                    ["Will of the Warmaster (Ascended)", "Master of the Speartip (Ascended)",
                     "The First Company (Ascended)", "The Vengeful Spirit (Ascended)", "Vessel of the Four",
                     "Favoured of the Dark Gods", "Blessings of the Four", "The Warmaster Must Lead", "Daemon"],
                    retinue=ret, other=HORUS, loyalist=False, profile_name="Horus Ascended",
                    extra_entries=[lance_strike(HORUS_ASC)])


# ---------------------------------------------------------------- additions to existing units
def ic_options(ctx):
    """Praetor / Centurion: Teleportation Transponders (TDA), Banestrike (bolt weapon)."""
    for n in ("Legion Praetor", "Legion Centurion"):
        e = ctx.unit(n)
        u = e.get("id")
        tp = option(u + "soh", "Teleportation Transponders", 10)
        add_mods(tp, [modifier("set", "hidden", "true", groups=[no_tda(u)]),
                      modifier("set", uid(tp.get("id"), "max"), 0, groups=[no_tda(u)])])
        add_to(e, "selectionEntryGroups", [group(uid("grp", u, "soh"), "Sons of Horus Wargear", entries=[tp])])
    add_armoury_items(ctx, [("Banestrike Ammunition", 5)], who=("praetor", "centurion"))
    for n in ("Legion Praetor", "Legion Centurion"):
        e = ctx.unit(n)
        u = e.get("id")
        no_bolt = all_of(*[lacks(W(b), u) for b in BOLT_WEAPONS])
        for lk in e.iter("entryLink"):
            if lk.get("targetId") == W("Banestrike Ammunition"):
                add_mods(lk, [modifier("set", "hidden", "true", groups=[no_bolt]),
                              modifier("set", uid(lk.get("id"), "max"), 0,
                                       groups=[all_of(*[lacks(W(b), u) for b in BOLT_WEAPONS])])])


def seeker_banestrike(ctx):
    s = ctx.unit("Legion Seeker Squad")
    u = s.get("id")
    bid = uid(u, "banestrike")
    specials = ["Flamer", "Meltagun", "Plasma Gun", "M.40 Targeter and Stalker Bolter",
                "Heavy Bolter with Suspensor and Hellfire Rounds", "Volkite Charger", "Volkite Caliver"]
    mods = [modifier("increment", PTS, 5, repeats=[repeat("model", u, 1)])]
    mods += [modifier("decrement", PTS, 5, repeats=[repeat(W(n), u, 1)]) for n in specials]
    add_to(s, "selectionEntries", [entry(bid, "Banestrike Ammunition (all eligible models, replaces Special Issue "
                                              "Ammunition)", cost=0, mods=mods,
                                         constraints=[constraint(uid(bid, "max"), "max", 1)],
                                         links=[gear(bid, "Banestrike Ammunition")])])


def transponders(ctx):
    for e in all_entries(ctx):
        if e.get("name") in ("Legion Terminator Squad", "Legion Terminator Command Squad"):
            u = e.get("id")
            add_to(e, "selectionEntries", [option(u + "soh", "Teleportation Transponders (squad)", 15,
                                                  item="Teleportation Transponders")])


def terminator_changes(ctx):
    """The Long March / The First Company Troops options."""
    tds = ctx.unit("Legion Terminator Squad")
    u = tds.get("id")
    lm = [rite("The Long March")]
    add_mods(tds, [modifier("set-primary", "category", TROOPS, conds=lm),
                   modifier("remove", "category", ELITES, conds=lm)])
    tog = uid(u, "first-company")
    no_horus = all_of(cond(HORUS, "roster", "lessThan", 1), cond(HORUS_ASC, "roster", "lessThan", 1))
    add_to(tds, "selectionEntries", [entry(
        tog, "Selected as Troops (The First Company)",
        constraints=[constraint(uid(tog, "max"), "max", 1, auto=True),
                     constraint(uid(tog, "force"), "max", 2, scope="force", deep=True)],
        mods=[modifier("set", "hidden", "true", groups=[no_horus]),
              modifier("set", uid(tog, "max"), 0, groups=[all_of(cond(HORUS, "roster", "lessThan", 1),
                                                                  cond(HORUS_ASC, "roster", "lessThan", 1))])],
        infolinks=rules_links(["The First Company"], key=tog))])
    on = [cond(tog, "self", "atLeast", 1)]
    add_mods(tds, [modifier("set-primary", "category", TROOPS, conds=on),
                   modifier("remove", "category", ELITES, conds=on),
                   modifier("add", "category", gs.CAT_LINE, conds=on)])
    return tog


def justaerin_root_mods(j, term_toggle):
    u = j.get("id")
    tog = uid(u, "first-company")
    add_to(j, "selectionEntries", [entry(
        tog, "Selected as Troops (The First Company)",
        constraints=[constraint(uid(tog, "max"), "max", 1, auto=True),
                     constraint(uid(tog, "force"), "max", 1, scope="force", deep=True)],
        mods=[modifier("set", "hidden", "true", groups=[all_of(cond(HORUS, "roster", "lessThan", 1),
                                                               cond(HORUS_ASC, "roster", "lessThan", 1))]),
              modifier("set", uid(tog, "max"), 0, groups=[all_of(cond(HORUS, "roster", "lessThan", 1),
                                                                  cond(HORUS_ASC, "roster", "lessThan", 1))])],
        infolinks=rules_links(["The First Company"], key=tog))])
    on = [cond(tog, "self", "atLeast", 1)]
    add_mods(j, [modifier("set-primary", "category", TROOPS, conds=on),
                 modifier("remove", "category", ELITES, conds=on),
                 modifier("add", "category", gs.CAT_LINE, conds=on),
                 modifier("increment", uid(u, "force-max"), 1, conds=[cond(tog, "force", "atLeast", 1)]),
                 modifier("increment", uid(u, "force-max"), 1, conds=[cond(ABADDON, "force", "atLeast", 1)]),
                 modifier("add", "error", "The First Company: no more than two squads (one of which may be a Justaerin "
                                          "Terminator Squad) may be selected as Troops.",
                          conds=[cond(tog, "force", "atLeast", 1), cond(term_toggle, "force", "atLeast", 2)])])


def maloghurst(ctx):
    ids = []
    for cs in ctx.retinues("Legion Command Squad"):
        u = cs.get("id")
        mid = uid(u, "maloghurst")
        vet = find_child(cs, "Legion Veteran")
        sb = find_child(cs, "Legion Standard Bearer")
        vmin, vmax = model_limits(vet)
        add_mods(vet, [modifier("decrement", vmin, 1, conds=[cond(mid, u, "atLeast", 1)]),
                       modifier("decrement", vmax, 1, conds=[cond(mid, u, "atLeast", 1)])])
        add_mods(sb, [modifier("set", uid(sb.get("id"), "max"), 0, conds=[cond(mid, u, "atLeast", 1)])])
        m = entry(mid, "Maloghurst the Twisted (replaces the Standard Bearer)", typ="model", cost=65,
                  constraints=[constraint(uid(mid, "max"), "max", 1), unique(mid)],
                  profiles=[unit_profile(mid, "Maloghurst", "Infantry (Character)", 4, 4, 4, 4, 2, 4, 2, 9, "3+/5+")],
                  infolinks=rules_links([LR, "Maloghurst the Twisted", "Broken Body", "Banner of the Warmaster"],
                                        key=mid),
                  links=[gear(mid, k) for k in ["Power Armour", "Refractor Field", "Bolter", "Close Combat Weapon",
                                                "Frag Grenades", "Banner of the Warmaster"]],
                  groups=[krak(mid)])
        add_to(cs, "selectionEntries", [m])
        ids.append(mid)
    unique_across(ctx.unit("Legion"), "Maloghurst the Twisted", ids)


def torgaddon(ctx, e, sgt_name, cost, need20=False):
    u = e.get("id")
    tid = uid(u, "torgaddon")
    sgt = find_child(e, sgt_name)
    smin, smax = model_limits(sgt)
    add_mods(sgt, [modifier("set", smin, 0, conds=[cond(tid, u, "atLeast", 1)]),
                   modifier("set", smax, 0, conds=[cond(tid, u, "atLeast", 1)])])
    mods = []
    if need20:
        small = [cond("model", u, "lessThan", 20)]
        mods = [modifier("set", "hidden", "true", conds=small), modifier("set", uid(tid, "max"), 0, conds=small)]
    t = entry(tid, "Tarik Torgaddon (replaces the Sergeant)", typ="model", cost=cost, mods=mods,
              constraints=[constraint(uid(tid, "max"), "max", 1), unique(tid)],
              profiles=[unit_profile(tid, "Tarik Torgaddon", "Infantry (Character)", 5, 4, 4, 4, 2, 5, 3, 9, "2+/5+")],
              infolinks=rules_links([LR, "Stubborn", "Tarik Torgaddon"], key=tid),
              links=[gear(tid, k) for k in ["Artificer Armour", "Refractor Field", "Bolter", "Power Weapon",
                                            "Frag Grenades"]],
              groups=[krak(tid)])
    add_to(e, "selectionEntries", [t])
    return tid


def add_praetor_retinues(ctx, extra):
    p = ctx.unit("Legion Praetor")
    for g in p.iter("selectionEntryGroup"):
        if g.get("name") == "Retinue (no Force Organisation slot)":
            RETINUE_SHARED.extend(x for x in extra if x not in RETINUE_SHARED)
            add_to(g, "entryLinks", [link(uid("link", g.get("id"), x.get("id")), x.get("id"), x.get("name"))
                                     for x in extra])
            return
    raise KeyError("Praetor retinue group")


BLESSINGS = [("Khorne", 5, 20), ("Slaanesh", 4, 15), ("Nurgle", 7, 25), ("Tzeentch", 8, 25)]


def blessings(ctx):
    """Blessings of the Four: Traitor Infantry units and Independent Characters while Horus Ascended is present."""
    off = [cond(HORUS_ASC, "roster", "lessThan", 1)]
    for e in all_entries(ctx):
        if e.get("type") != "unit" or e.get("name") in ("Legion", "Allegiance", "Rite of War", "Techmarine Covenant",
                                                        "Legion Rapier Weapons Battery"):
            continue
        if any(c.get("targetId") == gs.CAT_PRIMARCH for c in e.iter("categoryLink")):
            continue
        models = entry_models(e)
        types = [unit_type(m) for m in models] if models else [unit_type(e)]
        types = [t for t in types if t]
        if not types or any(x in t for t in types for x in ("Vehicle", "Artillery", "Monstrous", "Walker")):
            continue
        u = e.get("id")
        squad = bool(models)
        mobile = any(x in t for t in types for x in ("Bike", "Jetbike", "Jump"))
        gid = uid("grp", u, "blessing")
        ents = []
        for god, per, ic in BLESSINGS:
            if god == "Nurgle" and mobile:
                continue
            eid = uid("blessing", u, god)
            mods = []
            cost = ic
            if squad:
                cost = 0
                mods.append(modifier("increment", PTS, per, repeats=[repeat("model", u, 1)]))
            if god == "Nurgle":
                block = [has(W("Jump Pack"), u), has(W("Space Marine Bike"), u)]
                mods += [modifier("set", "hidden", "true", groups=[any_of(*block)]),
                         modifier("set", uid(eid, "max"), 0, groups=[any_of(*[has(W("Jump Pack"), u),
                                                                            has(W("Space Marine Bike"), u)])])]
            ents.append(entry(eid, f"Blessing of {god}" + (" (entire unit)" if squad else ""), cost=cost, mods=mods,
                              constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                              infolinks=rules_links([f"Blessing of {god}", "Blessings of the Four"], key=eid)))
        g = group(gid, "Blessing of Chaos (Horus Ascended)", entries=ents,
                  constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)],
                  mods=[modifier("set", "hidden", "true", conds=off),
                        modifier("set", uid(gid, "max"), 0, conds=[cond(HORUS_ASC, "roster", "lessThan", 1)]),
                        modifier("set", uid(gid, "max"), 0, conds=[cond(LOYALIST, "roster", "atLeast", 1)])])
        add_to(e, "selectionEntryGroups", [g])


def add_chainaxe(roots):
    add_character_variant(roots, "Chainsword", "Chainaxe", 4)
    add_character_variant(roots, "Close Combat Weapon", "Chainaxe", 4)


# ---------------------------------------------------------------- extend
def extend(ctx):
    ctx.legion_rules([LR, "Close Range Brutality", "Tip of the Spear", "Pride of the Warmaster"])

    # changes to existing entries (before any clone is made)
    ic_options(ctx)
    seeker_banestrike(ctx)
    torgaddon(ctx, ctx.unit("Legion Veteran Squad"), "Legion Veteran Sergeant", 105 - (125 - 4 * 20))
    torgaddon(ctx, ctx.unit("Legion Tactical Squad"), "Legion Tactical Sergeant", 105 - (150 - 9 * 15), need20=True)
    term_toggle = terminator_changes(ctx)

    # new units
    j = justaerin()
    justaerin_root_mods(j, term_toggle)
    reaver = reavers()
    units = [j, reaver, chieftains(), luperci(), *characters(ctx), horus(), horus_ascended()]
    ctx.add_units(*units)
    add_praetor_retinues(ctx, [justaerin("praetor-justaerin", root=False), chieftains("praetor-chieftains", root=False)])
    maloghurst(ctx)
    transponders(ctx)

    # unique copies across retinues
    legion = ctx.unit("Legion")
    for name in ("Falkus Kibre", "Tarik Torgaddon (replaces the Sergeant)"):
        ids = [e.get("id") for r in all_entries(ctx) for e in r.iter("selectionEntry") if e.get("name") == name]
        unique_across(legion, name.split(" (")[0], sorted(set(ids)))

    # The Vengeful Spirit: -10 points for Drop Pods and Dreadclaws
    for n in ("Legion Drop Pod", "Anvillus Pattern Dreadclaw Drop Pod"):
        add_mods(ctx.unit(n), [modifier("decrement", PTS, 10, groups=[any_of(cond(HORUS, "roster", "atLeast", 1),
                                                                             cond(HORUS_ASC, "roster", "atLeast", 1))])])

    # Rites of War
    ctx.add_rite("The Long March", RULES["The Long March"],
                 errors=[("only a Traitor Sons of Horus Detachment may select this Rite of War.",
                          [cond(LOYALIST, "roster", "atLeast", 1)])])
    ctx.add_rite("The Black Reaving", RULES["The Black Reaving"],
                 errors=[("the Detachment must include a Legion Centurion upgraded to a Master of Signals Consul.",
                          [cond(L.consul_id("Master of Signals"), "force", "lessThan", 1)]),
                         ("at least one compulsory Troops choice must be a Reaver Attack Squad.",
                          [cond(reaver.get("id"), "force", "lessThan", 1)])])

    # Chainaxe for characters, Blessings of the Four
    add_armoury_items(ctx, [("Cthonian Culling Blade", 10)])
    add_chainaxe(all_entries(ctx))
    blessings(ctx)
