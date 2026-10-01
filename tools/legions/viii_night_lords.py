"""VIII Legion - Night Lords (Forces of the Legions)."""
from legions.common import *
from bsx import el

LEGION = "VIII - Night Lords"
LR = "Legiones Astartes (Night Lords)"
NL = "Night Lords"

RULES = {
    LR: ("Models with this rule belong to the VIII Legion and use the Night Lords Legion special rules: Lords of the "
         "Night, Terror Made Manifest, Masters of the Terror Assault and Terror Assault."),
    "Lords of the Night": ("All models with the Legiones Astartes (Night Lords) special rule gain Night Vision. Night "
                           "Lords retain exclusive access to the Stealth Adept Veteran Skill (see the Night Lords "
                           "Armoury)."),
    "Terror Made Manifest": (
        "Whenever a non-vehicle Night Lords unit completely destroys an enemy unit in close combat (including by "
        "Sweeping Advance), it becomes Terrifying until the end of its next Assault phase. A Terrifying unit gains Fear; "
        "if it charges an enemy unit that it outnumbers, every model in it gains +1 Attack for the first round of that "
        "combat. This bonus is not cumulative."),
    "Masters of the Terror Assault": ("Night Lords units arriving by Deep Strike may re-roll the Scatter die. Night "
                                      "Lords units arriving by Outflank may re-roll the roll that determines which "
                                      "table edge they arrive from."),
    "Terror Assault": ("A Night Lords army may exchange two Heavy Support selections for one additional Fast Attack "
                       "selection; the Standard Force Organisation Chart then allows 4 Fast Attack / 1 Heavy Support. "
                       "(Select the option on the Legion entry.)"),
    # armoury
    "Nostraman Chainglaive": "The Nostraman Chainglaive does not count as a Power Weapon.",
    "Stealth Adept": (
        "A Night Lords Independent Character may purchase Stealth Adept for +5 points; any Night Lords Infantry or Jump "
        "Infantry unit for +1 point per model (every model must purchase it). Models with Stealth Adept gain Stealth. "
        "Bikes, Jetbikes, any Terminator Armour, Dreadnoughts and Vehicles may not purchase it. An Independent "
        "Character joining a unit with Stealth Adept must also have it, otherwise the unit does not benefit while he "
        "remains attached."),
    "Teleportation Transponders": (
        "The model or unit gains Deep Strike and may deploy using Deep Strike even if the mission would not normally "
        "permit it. An Independent Character intending to Deep Strike as part of another unit must purchase "
        "Teleportation Transponders separately."),
    # units
    "Preferred Enemy (Infantry)": "The unit has the Preferred Enemy special rule against Infantry units.",
    "Preferred Enemy (Independent Characters)": ("The model has the Preferred Enemy special rule against Independent "
                                                 "Characters."),
    "Nostraman Chainblade": "A Nostraman Chainblade is a Two-Handed Rending Weapon which grants +1 Strength.",
    "Escaton Power Claw": ("Counts as a Power Fist. In addition, the wielder may re-roll failed To Wound rolls made with "
                           "the Escaton Power Claw."),
    "Teleport Assault": ("An Atramentar Flay-Clade may deploy using Deep Strike even if the mission being played does "
                         "not normally permit Deep Strike. All other normal Deep Strike rules apply."),
    "Headtaker": ("The Raptor Sergeant may be upgraded to a Headtaker for +15 points: Weapon Skill 5, and he may select "
                  "up to 50 points of permitted weapons and wargear from the Space Marine Armoury and Night Lords "
                  "Armoury."),
    # characters
    "Night's Whisper": ("A Two-Handed, Master-crafted Power Weapon. Attacks made with Night's Whisper are resolved at "
                        "Strength 6."),
    "Visions of Doom": ("Sevatar knows only the Withering Gaze psychic power. When making the Psychic Test to invoke "
                        "Withering Gaze he uses Leadership 7 rather than his normal Leadership."),
    "Withering Gaze": (
        "Used during the Night Lords Shooting phase instead of Sevatar firing a weapon. Choose one visible enemy unit "
        "within 12\" and take a Psychic Test. If successful, until the beginning of the next Night Lords turn that unit "
        "must pass a Leadership test before it may declare a charge against Sevatar or a unit he has joined; if failed it "
        "may not declare that charge this Assault phase, but may charge another eligible target."),
    "Command Retinue (Sevatar)": ("Sevatar may select one Legion Command Squad, Legion Terminator Command Squad or "
                                  "Atramentar Flay-Clade as his retinue. It does not occupy a separate Force "
                                  "Organisation slot."),
    "The Bloody Aegis": ("Against close-combat attacks, Ophion's Invulnerable Save is improved to 3+. Against all other "
                         "attacks he uses his Refractor Field normally."),
    "The Coward": ("After Ophion loses his first Wound, he gains Feel No Pain (4+) for the remainder of the battle. If he "
                   "is subsequently reduced to one remaining Wound, replace it with Feel No Pain (3+)."),
    "Command Retinue (Ophion)": ("Ophion may select a Legion Command Squad or Contekar Terminator Elite as his retinue. "
                                 "It does not occupy a separate Force Organisation slot."),
    "War-Sage": ("Malcharion and any Night Lords unit he has joined may re-roll failed Morale and Pinning tests. The "
                 "second result must be accepted."),
    "Command Retinue (Malcharion)": ("Malcharion may select one Legion Command Squad or Legion Veteran Squad as his "
                                     "retinue. It does not occupy a separate Force Organisation slot."),
    "Terror Retinue": ("Shang may select one Terror Squad as his retinue. It does not occupy a separate Force "
                       "Organisation slot; Shang and the Terror Squad count as a single HQ selection."),
    "Red Jaqa": ("Red Jaqa is a Rending Weapon. Any natural To Wound roll of 6 made with Red Jaqa inflicts a Massive "
                 "Wound (D3) instead of a normal Wound."),
    "Devil's Luck": "Mawdrym may re-roll Feel No Pain rolls of 1. A dice may never be re-rolled more than once.",
    "Unfit for Command": ("Mawdrym may not fulfil the army's compulsory HQ requirement. He may never be the army's "
                          "Warlord."),
    "Feel No Pain (5+)": "The model has the Feel No Pain special rule with a 5+ roll.",
    # Curze
    "Mercy & Forgiveness": ("A matched pair of Master-crafted Power Weapons. Attacks are resolved at Curze's normal "
                            "Strength and have Shred and Rending. They count as two close combat weapons."),
    "Lethal Precision": ("On an unmodified To Wound roll of 6, a Wound inflicted by the Widowmakers allows neither Armour "
                         "nor Invulnerable Saves. Cover Saves may be taken normally."),
    "King of Terrors": ("Enemy units with at least one model within 12\" of Konrad Curze suffer -2 Leadership. Models "
                        "and units with Fearless are unaffected."),
    "Bloody Murder": "Listed in Konrad Curze's special rules; no rule text is given in the army book.",
    "Night Haunter": (
        "Konrad Curze has Stealth and Hit & Run. In the Movement phase he moves as though he were Jump Infantry, despite "
        "not having a Jump Pack. This does not change his Unit Type or grant him Deep Strike, Bulky, Swift or any other "
        "rule normally associated with Jump Infantry."),
    "Dark Precognition": (
        "The first successful To Hit roll made against Konrad Curze during each player turn must be re-rolled; the "
        "second result must be accepted. Curze is a Psyker (Mastery Level 1) and knows only the Precognition power "
        "(Divination); he takes the Psychic Test for it on Leadership 8. All other rules (Perils of the Warp, "
        "Disturbance in the Warp) apply normally."),
    "Primarch Retinue (Konrad Curze)": (
        "Konrad Curze may select one Legion Terminator Command Squad, Atramentar Flay-Clade, Night Raptor Squad or "
        "Terror Squad as his Primarch Retinue (no additional Force Organisation selection). Night Raptor Retinue: a "
        "Night Raptor Squad selected this way may use his Hit & Run special rule while he remains part of the unit."),
}
RULES["Nightmare Mantle"] = "The Nightmare Mantle counts as Primarch Armour (1+ Armour Save, 4+ Invulnerable Save)."

TERROR_ASSAULT_RITE = (
    "EFFECTS - Cover of Darkness: the first Battle Round is fought using the Night Fighting rules; at the beginning of "
    "the second Battle Round roll a D6, on a 3+ Night Fighting remains in effect; if it did, at the beginning of the "
    "third Battle Round it remains on a 6; it always ends at the beginning of the fourth Battle Round. Night Lords units "
    "benefit from Night Vision. Terror Formations: Night Raptor Squads and Terror Squads may be selected as Troops and "
    "may fulfil compulsory Troops; at least one compulsory Troops selection must be a Night Raptor Squad or Terror "
    "Squad. Terror Attack: after the opposing player has made all Reserve rolls, the Night Lords player may force one "
    "successful Reserve roll to be re-rolled (second result stands; no die re-rolled more than once). Rapid Strike "
    "Force: Fast Attack 0-4, Heavy Support 0-1.\n"
    "LIMITATIONS - The Detachment must include at least one Night Raptor Squad or Terror Squad. No more than one Heavy "
    "Support choice. No Fortification.")
HORROR_CULT_RITE = (
    "EFFECTS - Raptor Cult: Night Raptor Squads may be selected as Troops and may fulfil compulsory Troops; at least one "
    "compulsory Troops selection must be a Night Raptor Squad. Beyond Judgement: any Night Lords Infantry or Jump "
    "Infantry squad may purchase Trophies of Judgement for +25 points per unit; every model counts as equipped (measure "
    "the 8\" from any model) and the unit gains Fear; penalties from multiple Trophies remain non-cumulative. Vox-Scream "
    "Broadcast: once per battle, at the beginning of any Night Lords player turn, all enemy units suffer -1 Leadership "
    "until the beginning of the next Night Lords player turn (may combine with Trophies of Judgement). The Scent of "
    "Blood: a non-Vehicle Night Lords unit must declare a charge in its Assault phase if it is eligible to charge, an "
    "enemy unit is within its current charge distance and that unit is a legal charge target (the player chooses among "
    "several; never an illegal charge).\n"
    "LIMITATIONS - Traitor Night Lords Detachment only. No Fortification. Night Lords units may not voluntarily "
    "withdraw from close combat.")

WEAPONS = {
    "Nostraman Chainglaive": ("-", "User +1", "-", "Rending, Two-Handed"),
    "Nostraman Chainblade": ("-", "User +1", "-", "Rending, Two-Handed"),
    "Escaton Power Claw": ("-", "x2", "-", "Power Fist, re-roll failed To Wound rolls"),
    "Night's Whisper": ("-", "6", "-", "Power Weapon, Two-Handed, Master-crafted"),
    "Power Axe": ("-", "User", "-", "Power Weapon"),
    "Red Jaqa": ("-", "User", "-", "Rending, Massive Wound (D3) on a To Wound roll of 6"),
    "Mercy & Forgiveness": ("-", "User", "-", "Power Weapon, Master-crafted, Shred, Rending, two close combat weapons"),
    "Widowmakers": ('12"', "4", "5", "Assault 3, Lethal Precision"),
}
WEAPON_RULES = {
    "Nostraman Chainglaive": ["Nostraman Chainglaive", "Rending", "Two-Handed"],
    "Nostraman Chainblade": ["Nostraman Chainblade", "Rending", "Two-Handed"],
    "Escaton Power Claw": ["Escaton Power Claw", "Unwieldy"],
    "Night's Whisper": ["Night's Whisper", "Two-Handed", "Master-Crafted"],
    "Red Jaqa": ["Red Jaqa", "Rending"],
    "Mercy & Forgiveness": ["Mercy & Forgiveness", "Shred", "Rending", "Master-Crafted"],
    "Widowmakers": ["Lethal Precision"],
}
WARGEAR = {
    "Trophies of Judgement": (
        "Enemy units with one or more models within 8\" of one or more models with Trophies of Judgement suffer -1 "
        "Leadership. Multiple Trophies are not cumulative; friendly models are never affected. Where an entire squad is "
        "equipped with Trophies, measure from any model in the squad; the squad counts as a single source."),
    "Stealth Adept": (RULES["Stealth Adept"], ["Stealth"]),
    "Kraken Light Bolts": (
        "Usable with Bolters, Combi-Bolters, Twin-linked Bolters and the Bolter component of Combi-Weapons; when firing "
        "Kraken Light Bolts those weapons are AP4. May not be combined with Special Issue Ammunition or any other "
        "ammunition upgrade. A Legion Tactical Squad may not use Fury of the Legion in a Shooting phase in which it "
        "fires Kraken Light Bolts."),
    "Teleportation Transponders": RULES["Teleportation Transponders"],
    "The Bloody Aegis": RULES["The Bloody Aegis"],
    "Nightmare Mantle": RULES["Nightmare Mantle"],
    "Iron Halo (Sevatar)": ("Grants a 4+ Invulnerable Save. Part of Sevatar's fixed wargear (not counted against the "
                            "one-Iron-Halo-per-army limit of the Space Marine Armoury)."),
}

TERROR = uid("unit", "Terror Squad")
RAPTORS = uid("unit", "Night Raptor Squad")
CONTEKAR = uid("unit", "Contekar Terminator Elite")
ATRAMENTAR = uid("unit", "Atramentar Flay-Clade")
CURZE = uid("unit", "Konrad Curze, the Night Haunter")

PA_INFANTRY = ["Legion Tactical Squad", "Legion Assault Squad", "Legion Breacher Siege Squad",
               "Legion Reconnaissance Squad", "Legion Veteran Squad", "Legion Destroyer Squad", "Legion Seeker Squad",
               "Legion Heavy Support Squad", "Legion Command Squad", "Legion Honour Guard Squad"]
TDA_UNITS = ["Legion Terminator Squad", "Legion Terminator Command Squad", "Contekar Terminator Elite"]


def register():
    register_data(rules=RULES, weapons=WEAPONS, weapon_rules=WEAPON_RULES, wargear=WARGEAR)


# ---------------------------------------------------------------- local helpers
def cgroup(typ, conds=(), groups=()):
    return el("conditionGroup", {"type": typ}, [wrap("conditions", list(conds)), wrap("conditionGroups", list(groups))])


def _max_id(e):
    cs = e.find("constraints")
    for c in (cs if cs is not None else []):
        if c.get("type") == "max" and c.get("scope") == "parent":
            return c.get("id")
    return None


def forbid_when(e, grp):
    """Hide an entry/link and set its max to 0 while conditionGroup grp is true."""
    mods = [modifier("set", "hidden", "true", groups=[grp])]
    mx = _max_id(e)
    if mx:
        mods.append(modifier("set", mx, 0, groups=[copy_group(grp)]))
    add_mods(e, mods)


def copy_group(g):
    import copy as _c
    return _c.deepcopy(g)


def gate_group(g, grp):
    """Forbid every non-default option inside group g (and its subgroups) while grp is true."""
    for sg in g.iter("selectionEntryGroup"):
        d = sg.get("defaultSelectionEntryId")
        for tag in ("entryLinks", "selectionEntries"):
            c = sg.find(tag)
            for x in (c if c is not None else []):
                if x.get("id") != d:
                    forbid_when(x, copy_group(grp))


def armoury_groups(ctx, who):
    """[(group, root)] of the Armoury groups Legion items are added to."""
    out, seen = [], set()
    for r in all_unique(ctx):
        n = r.get("name")
        if n in ("Legion Praetor", "Legion Centurion"):
            if n.split()[-1].lower() in who:
                for g in r.iter("selectionEntryGroup"):
                    if g.get("name") == "Space Marine Armoury (max 100 pts)":
                        for sub in g.iter("selectionEntryGroup"):
                            if sub.get("name") == "Additional Wargear" and id(sub) not in seen:
                                seen.add(id(sub))
                                out.append((sub, r))
            continue
        if "sergeants" in who:
            for g in r.iter("selectionEntryGroup"):
                if g.get("name") == "Space Marine Armoury (max 50 pts)" and id(g) not in seen:
                    seen.add(id(g))
                    out.append((g, r))
    return out


def add_legion_armoury(ctx, items, who=("praetor", "centurion", "sergeants"), skip_units=()):
    for g, r in armoury_groups(ctx, who):
        if r.get("name") in skip_units:
            continue
        add_to(g, "entryLinks", [link(uid("link", g.get("id"), "legion", n), W(n), n, cost=p or None,
                                      constraints=[constraint(uid("link", g.get("id"), "legion", n, "max"), "max", 1,
                                                              auto=True)])
                                 for n, p in items])


def strip_rite_mods(e):
    """Remove category modifiers (Troops/compulsory changes) from a retinue clone."""
    m = e.find("modifiers")
    if m is not None:
        for x in list(m):
            if x.get("field") == "category":
                m.remove(x)
    return e


def troop_mods(rites, normal):
    grp = any_rite(*rites)
    return [modifier("set-primary", "category", TROOPS, groups=[grp]),
            modifier("remove", "category", normal, groups=[copy_group(grp)]),
            modifier("add", "category", gs.CAT_LINE, groups=[copy_group(grp)])]


def all_unique(ctx):
    out, seen = [], set()
    for e in ctx.all_entries():
        if id(e) not in seen:
            seen.add(id(e))
            out.append(e)
    return out


def entries_named(ctx, names):
    return [e for e in all_unique(ctx) if e.get("name") in names]


def krak_melta(key, krak=True, melta=True):
    items = ([("Krak Grenades", 2)] if krak else []) + ([("Melta Bombs", 5)] if melta else [])
    return take(key, "Options", items)


# ---------------------------------------------------------------- units
TDA_RANGED = [("Storm Bolter", 0), ("Foeblaster Boltgun", 5), ("Combi-Flamer", 10), ("Combi-Volkite Charger", 10),
              ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15)]
TDA_CC = [("Power Fist", 5), ("Lightning Claw", 5), ("Chainfist", 10), ("Thunder Hammer", 10)]


def terror_squad(key="Terror Squad", root=True):
    u = uid("unit", key)
    mid, hid = uid("model", u, "Terror Marine"), uid("model", u, "Headsman")
    kit = ["Power Armour", "Bolter", "Bolt Pistol", "Chainsword", "Frag Grenades", "Trophies of Judgement"]
    cc = [("Rending Weapon", 5), ("Power Weapon", 10)]
    head = entry(hid, "Headsman", typ="model",
                 constraints=[constraint(uid(hid, "min"), "min", 1), constraint(uid(hid, "max"), "max", 1)],
                 profiles=[unit_profile(u, "Headsman", "Infantry (Character)", 5, 4, 4, 4, 1, 4, 3, 9, "3+")],
                 links=[gear(hid, k) for k in kit if k != "Bolt Pistol"],
                 groups=[slot(hid, "Replace Chainsword", "Chainsword", cc),
                         slot(hid, "Replace Bolter", "Bolter", [("Volkite Charger", 10)]),
                         pa_armoury(hid, u, 10, slots=["Bolt Pistol"])])
    marines = entry(mid, "Terror Marine", typ="model", cost=25,
                    constraints=[constraint(uid(mid, "min"), "min", 4), constraint(uid(mid, "max"), "max", 9)],
                    profiles=[unit_profile(u, "Terror Marine", "Infantry", 5, 4, 4, 4, 1, 4, 2, 9, "3+")],
                    links=[gear(mid, k) for k in kit])
    special_opts = [("Flamer", 5), ("Rotor Cannon", 10), ("Heavy Flamer", 10)]
    specials, _ = pool(u, "Special Weapons (1 per 5 models, replace Bolter)", u, special_opts, 0, every=5)
    swaps = [model_swaps(u, "Terror Marines: replace Chainsword (any number)", u, [mid], cc),
             model_swaps(u, "Terror Marines: replace Bolter (any number)", u, [mid], [("Volkite Charger", 10)],
                         minus=[W(n) for n, _ in special_opts])]
    cats = [foc(ELITES, "Elites", u)] if root else []
    mods = troop_mods(["Terror Assault"], ELITES) if root else []
    return entry(u, "Terror Squad", typ="unit", cost=150 - 4 * 25, cats=cats, mods=mods,
                 infolinks=rules_links([LR, "Infiltrate", "Preferred Enemy (Infantry)", "Preferred Enemy"], key=u),
                 entries=[head, marines,
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]),
                          per_model(u, "Stealth Adept (entire squad)", 1, u, ["Stealth Adept"])],
                 groups=[*swaps, specials,
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos",
                                           "Land Raider Proteus"])])


GATES = []   # (group, conditionGroup) gated after the Night Lords Armoury has been added


def night_raptors(key="Night Raptor Squad", root=True):
    u = uid("unit", key)
    rid, sid = uid("model", u, "Night Raptor"), uid("model", u, "Raptor Sergeant")
    kit = ["Power Armour", "Jump Pack", "Bolt Pistol", "Chainsword", "Frag Grenades", "Trophies of Judgement"]
    ht = uid(sid, "headtaker")
    headtaker = entry(ht, "Upgrade to Headtaker", cost=15, constraints=[constraint(uid(ht, "max"), "max", 1, auto=True)],
                      infolinks=rules_links(["Headtaker"], key=ht))
    prof = unit_profile(u, "Raptor Sergeant", "Jump Infantry (Character)", 4, 4, 4, 4, 1, 4, 2, 9, "3+")
    prof.insert(0, wrap("modifiers", [modifier("set", gs.char_id("Unit", "WS"), 5, conds=[has(ht, sid)]),
                                      modifier("set", "name", "Headtaker", conds=[has(ht, sid)])]))
    arm = pa_armoury(sid, u, 15, slots=["Bolt Pistol"])
    GATES.append((arm, cgroup("and", [lacks(ht, sid)])))
    sgt = entry(sid, "Raptor Sergeant", typ="model",
                mods=[modifier("set", "name", "Headtaker", conds=[has(ht, sid)])],
                constraints=[constraint(uid(sid, "min"), "min", 1), constraint(uid(sid, "max"), "max", 1)],
                profiles=[prof], links=[gear(sid, k) for k in kit if k != "Bolt Pistol"],
                entries=[headtaker], groups=[arm])
    raptors = entry(rid, "Night Raptor", typ="model", cost=28,
                    constraints=[constraint(uid(rid, "min"), "min", 4), constraint(uid(rid, "max"), "max", 14)],
                    profiles=[unit_profile(u, "Night Raptor", "Jump Infantry", 4, 4, 4, 4, 1, 4, 1, 8, "3+")],
                    links=[gear(rid, k) for k in kit])
    cc, _ = pool(u, "Replace Chainsword (up to five models)", u, [("Rending Weapon", 5), ("Power Weapon", 10)], 5)
    pistols, _ = pool(u, "Night Raptors: replace Bolt Pistol (up to two)", u,
                      [("Volkite Serpenta", 5), ("Hand Flamer", 5), ("Plasma Pistol", 15)], 2)
    melta, _ = pool(u, "Melta Bombs (up to two models)", u, [("Melta Bombs", 5)], 2)
    cats = [foc(FA, "Fast Attack", u)] if root else []
    mods = troop_mods(["Terror Assault", "Horror Cult"], FA) if root else []
    return entry(u, "Night Raptor Squad", typ="unit", cost=140 - 4 * 28, cats=cats, mods=mods,
                 infolinks=rules_links([LR, "Hit & Run"], key=u),
                 entries=[sgt, raptors,
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Stealth Adept (entire squad)", 1, u, ["Stealth Adept"])],
                 groups=[cc, pistols, melta])


def contekar(key="Contekar Terminator Elite", root=True):
    u = uid("unit", key)
    mid, did = uid("model", u, "Contekar"), uid("model", u, "Contekar Dissident")
    kit = ["Tartaros Terminator Armour", "Heavy Flamer", "Nostraman Chainblade"]
    diss = entry(did, "Contekar Dissident", typ="model",
                 constraints=[constraint(uid(did, "min"), "min", 1), constraint(uid(did, "max"), "max", 1)],
                 profiles=[unit_profile(u, "Contekar Dissident", "Infantry (Character)", 5, 4, 4, 4, 1, 4, 3, 9,
                                        "2+/5+")],
                 links=[gear(did, k) for k in kit],
                 groups=[slot(did, "Replace Heavy Flamer", "Heavy Flamer", [("Volkite Culverin", 10)]),
                         take(did, "Dissident Wargear", [("Grenade Harness", 10), ("Trophies of Judgement", 10)])])
    cont = entry(mid, "Contekar", typ="model", cost=50,
                 constraints=[constraint(uid(mid, "min"), "min", 4), constraint(uid(mid, "max"), "max", 9)],
                 profiles=[unit_profile(u, "Contekar", "Infantry", 5, 4, 4, 4, 1, 4, 2, 9, "2+/5+")],
                 links=[gear(mid, k) for k in kit])
    claws, _ = pool(u, "Replace Nostraman Chainblade (up to two models)", u, [("Escaton Power Claw", 10)], 2)
    cats = [foc(ELITES, "Elites", u)] if root else []
    return entry(u, "Contekar Terminator Elite", typ="unit", cost=250 - 4 * 50, cats=cats,
                 infolinks=rules_links([LR, "Stubborn"], key=u),
                 entries=[diss, cont,
                          option(u, "Teleportation Transponders (entire unit)", 15,
                                 item="Teleportation Transponders")],
                 groups=[model_swaps(u, "Contekar: replace Heavy Flamer (any number)", u, [mid],
                                     [("Volkite Culverin", 10)]), claws,
                         transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                                    orbital=False)])


def atramentar(key="Atramentar Flay-Clade", root=True):
    u = uid("unit", key)
    mid = uid("model", u, "Atramentar")
    kit = ["Cataphractii Terminator Armour", "Trophies of Judgement", "Combi-Bolter", "Power Weapon"]
    m = entry(mid, "Atramentar", typ="model", cost=50,
              constraints=[constraint(uid(mid, "min"), "min", 5), constraint(uid(mid, "max"), "max", 10)],
              profiles=[unit_profile(u, "Atramentar", "Infantry", 5, 4, 4, 4, 1, 4, 2, 9, "2+/4+")],
              links=[gear(mid, k) for k in kit])
    heavy = [("Heavy Flamer", 10), ("Reaper Autocannon", 15), ("Plasma Blaster", 15)]
    hp, _ = pool(u, "Heavy Weapons (1 per 5 models, replace Combi-bolter)", u, heavy, 0, every=5)
    pid, pair = model_pair_claws(u, "Pair of Lightning Claws (replaces Combi-bolter and Power Weapon)", u, [mid], 15)
    swaps = [model_swaps(u, "Atramentar: replace Combi-bolter (any number)", u, [mid], TDA_RANGED,
                         minus=[W(n) for n, _ in heavy], entries=[pair]),
             model_swaps(u, "Atramentar: replace Power Weapon (any number)", u, [mid], TDA_CC, minus=[pid])]
    cats = [foc(ELITES, "Elites", u)] if root else []
    return entry(u, "Atramentar Flay-Clade", typ="unit", cost=0, cats=cats,
                 infolinks=rules_links([LR, "Fearless", "Teleport Assault"], key=u),
                 entries=[m], groups=[*swaps, hp,
                                      transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                                        "Anvillus Pattern Dreadclaw Drop Pod",
                                                        "Legion Spartan Assault Tank"], orbital=False)])


# ---------------------------------------------------------------- characters
def characters():
    out = []
    sev = uid("unit", "Jago Sevatarion")
    out.append(named_character(
        LR, "Jago Sevatarion", 200, (7, 5, 4, 4, 3, 5, 4, 10, "2+/4+"),
        ["Artificer Armour", "Iron Halo (Sevatar)", "Night's Whisper", "Bolt Pistol", "Trophies of Judgement",
         "Frag Grenades"],
        ["Psyker", "Visions of Doom", "Withering Gaze", "Command Retinue (Sevatar)"],
        retinue=retinue_links("sevatar", [command_squad_for("sevatar", sev), L2.terminator_command_squad("sevatar"),
                                          atramentar("sevatar-atramentar", root=False)]),
        extra_groups=[krak_melta(sev, melta=False)], profile_name="Sevatar"))
    oph = uid("unit", "Kheron Ophion")
    out.append(named_character(
        LR, "Kheron Ophion", 180, (6, 5, 4, 4, 3, 5, 4, 10, "3+/5+"),
        ["Power Armour", "Refractor Field", "Power Axe", "Volkite Serpenta", "The Bloody Aegis", "Frag Grenades",
         "Melta Bombs"],
        ["Stubborn", "The Coward", "Command Retinue (Ophion)"],
        retinue=retinue_links("ophion", [command_squad_for("ophion", oph), contekar("ophion-contekar", root=False)]),
        extra_groups=[krak_melta(oph, melta=False)], loyalist=False))
    mal = uid("unit", "Malcharion, the War-Sage")
    vets = strip_rite_mods(clone(L2.veteran_squad(), "malcharion-vets"))
    out.append(named_character(
        LR, "Malcharion, the War-Sage", 155, (6, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Power Weapon", "Master-crafted Weapon", "Bolter", "Bolt Pistol",
         "Frag Grenades"],
        ["War-Sage", "Command Retinue (Malcharion)"],
        retinue=retinue_links("malcharion", [command_squad_for("malcharion", mal), vets]),
        extra_groups=[krak_melta(mal)], master=False, profile_name="Malcharion"))
    shang = uid("unit", "Shang")
    out.append(named_character(
        LR, "Shang", 165, (6, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Power Weapon", "Master-crafted Weapon", "Bolt Pistol",
         "Trophies of Judgement", "Frag Grenades"],
        ["Infiltrate", "Preferred Enemy (Independent Characters)", "Preferred Enemy", "Terror Retinue"],
        retinue=retinue_links("shang", [terror_squad("shang-terror", root=False)]),
        extra_groups=[krak_melta(shang)]))
    maw = uid("unit", "Flaymaster Mawdrym Llansahai")
    out.append(named_character(
        LR, "Flaymaster Mawdrym Llansahai", 125, (5, 5, 4, 4, 3, 4, 2, 9, "3+/5+"),
        ["Power Armour", "Refractor Field", "Narthecium", "Red Jaqa", "Bolt Pistol", "Frag Grenades"],
        ["Fearless", "Feel No Pain (5+)", "Feel No Pain", "Devil's Luck", "Unfit for Command"],
        extra_groups=[krak_melta(maw, melta=False)], master=False, compulsory=False, loyalist=False,
        profile_name="Mawdrym Llansahai"))
    return out


def curze():
    ret = retinue_links("curze", [L2.terminator_command_squad("curze"), atramentar("curze-atramentar", root=False),
                                  night_raptors("curze-raptors", root=False), terror_squad("curze-terror", root=False)],
                        title="Primarch Retinue")
    return primarch(LR, "Konrad Curze, the Night Haunter", 500, (8, 6, 6, 6, 6, 8, 6, 10, "1+/4+"),
                    ["Nightmare Mantle", "Mercy & Forgiveness", "Widowmakers", "Frag Grenades"],
                    ["Primarch Armour", "Psyker", "King of Terrors", "Bloody Murder", "Night Haunter", "Stealth",
                     "Hit & Run", "Dark Precognition", "Primarch Retinue (Konrad Curze)"],
                    retinue=ret)


# ---------------------------------------------------------------- extend
def extend(ctx):
    legion = ctx.unit("Legion")
    ctx.legion_rules([LR, "Lords of the Night", "Night Vision", "Terror Made Manifest", "Masters of the Terror Assault",
                      "Terror Assault"])
    # Terror Assault (Legion rule): exchange two Heavy Support for one Fast Attack (the Rite does the same)
    ex = uid("nl", "terror-assault-exchange")
    rite_on = cond(rite_id("Terror Assault"), "force", "atLeast", 1)
    add_to(legion, "selectionEntries", [entry(
        ex, "Terror Assault: exchange two Heavy Support for one additional Fast Attack (4 FA / 1 HS)",
        constraints=[constraint(uid(ex, "max"), "max", 1, auto=True)],
        mods=[modifier("set", "hidden", "true", conds=[rite_on]), modifier("set", uid(ex, "max"), 0, conds=[rite_on])],
        infolinks=rules_links(["Terror Assault"], key=ex))])
    on = any_of(cond(ex, "self", "atLeast", 1), cond(rite_id("Terror Assault"), "force", "atLeast", 1))
    add_mods(legion, [modifier("add", "category", gs.FOC_PLUS["Fast Attack"], groups=[on]),
                      modifier("add", "category", gs.CAT_LIMIT_HS, groups=[copy_group(on)])])

    # units
    GATES.clear()
    units = [terror_squad(), night_raptors(), contekar(), atramentar(), *characters(), curze()]
    ctx.add_units(*units)

    # Rites of War
    none_nr_terror = [cond(RAPTORS, "force", "lessThan", 1), cond(TERROR, "force", "lessThan", 1)]
    ctx.add_rite("Terror Assault", TERROR_ASSAULT_RITE,
                 errors=[("the Detachment must include at least one Night Raptor Squad or Terror Squad (and one of "
                          "them must be a compulsory Troops selection).", none_nr_terror)])
    ctx.add_rite("Horror Cult", HORROR_CULT_RITE,
                 errors=[("only a Traitor Night Lords Detachment may use this Rite of War.",
                          [cond(LOYALIST, "roster", "atLeast", 1)]),
                         ("at least one compulsory Troops selection must be a Night Raptor Squad.",
                          [cond(RAPTORS, "force", "lessThan", 1)])])

    # ---- Armoury: Praetor / Centurion
    for n in ("Legion Praetor", "Legion Centurion"):
        e = ctx.unit(n)
        i = e.get("id")
        sa = option(i, "Stealth Adept", 5)
        forbid_when(sa, cgroup("or", has_tda(i) + [has(W("Space Marine Bike"), i)]))
        tt = option(i, "Teleportation Transponders", 10)
        forbid_when(tt, no_tda(i))
        add_to(e, "selectionEntryGroups", [group(uid("grp", i, "nl"), "Night Lords Wargear", entries=[sa, tt])])
    # Techmarines are Independent Characters too
    for e in entries_named(ctx, ["Legion Techmarine"]):
        i = e.get("id")
        sa = option(i, "Stealth Adept", 5)
        forbid_when(sa, cgroup("or", [has(W("Space Marine Bike"), i)]))
        add_to(e, "selectionEntries", [sa])
    # Chainglaive / Trophies for Independent Characters and Sergeants
    add_legion_armoury(ctx, [("Nostraman Chainglaive", 10)])
    # (squads already equipped with Trophies of Judgement do not offer them to their Sergeant again)
    add_legion_armoury(ctx, [("Trophies of Judgement", 10)], skip_units=("Terror Squad", "Night Raptor Squad"))
    for g, grp in GATES:
        gate_group(g, grp)

    # Stealth Adept (+1 per model) for Infantry / Jump Infantry squads
    for e in entries_named(ctx, PA_INFANTRY):
        i = e.get("id")
        sa = per_model(i + "nl", "Stealth Adept (entire squad)", 1, i, ["Stealth Adept"])
        if e.get("name") == "Legion Command Squad":
            forbid_when(sa, cgroup("or", [has(W("Space Marine Bike"), i)]))
        add_to(e, "selectionEntries", [sa])
    # Kraken Light Bolts
    for e in entries_named(ctx, ["Legion Tactical Squad", "Legion Veteran Squad"]):
        add_to(e, "selectionEntries", [option(e.get("id") + "nl", "Kraken Light Bolts (unit)", 10,
                                              item="Kraken Light Bolts")])
    # Teleportation Transponders for units entirely in Terminator Armour
    for e in entries_named(ctx, ["Legion Terminator Squad", "Legion Terminator Command Squad"]):
        add_to(e, "selectionEntries", [option(e.get("id") + "nl", "Teleportation Transponders (entire unit)", 15,
                                              item="Teleportation Transponders")])
    # Horror Cult - Beyond Judgement
    no_cult = cgroup("or", [cond(rite_id("Horror Cult"), "force", "lessThan", 1)])
    for e in entries_named(ctx, PA_INFANTRY + TDA_UNITS + ["Terror Squad", "Night Raptor Squad",
                                                           "Atramentar Flay-Clade"]):
        bj = uid("nl-bj", e.get("id"))
        o = entry(bj, "Trophies of Judgement (entire squad, Beyond Judgement)", cost=25,
                  constraints=[constraint(uid(bj, "max"), "max", 1, auto=True)],
                  links=[gear(bj, "Trophies of Judgement")], infolinks=rules_links(["Fear"], key=bj))
        forbid_when(o, copy_group(no_cult))
        add_to(e, "selectionEntries", [o])
