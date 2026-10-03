"""IX Legion - Blood Angels (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, allegiance_only, option, upgrade, clone, retinue_links,
                            command_squad_for, named_character, primarch, add_consul, add_group, add_entry,
                            add_armoury_items, LOW, TRAITOR, LOYALIST)
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile
from legiones2 import (slot, take, pool, transports, add_mods, add_to, foc, rite_id, rite, TROOPS, ELITES, FA, HQ,
                       model_swaps, pa_armoury, specials_decrement)
from legiones_wargear import ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR

LEGION = "IX - Blood Angels"
LR = "Legiones Astartes (Blood Angels)"

RULES = {
    LR: ("Models with this rule belong to the IX Legion and use the Blood Angels Legion special rules: Angels of "
         "Death, Descent of Angels and Vengeance of a Fallen Angel."),
    "Angels of Death": (
        "During an Assault phase in which a Blood Angels model charges, it gains +1 Weapon Skill until the end of that "
        "Assault phase. This bonus may be combined with other Weapon Skill modifiers. In addition, friendly Imperial "
        "Army or Imperial Militia units with at least one model within 6\" of a Blood Angels unit receive +1 Leadership, "
        "to a maximum of 10. This Leadership bonus is not cumulative."),
    "Descent of Angels": (
        "When a Blood Angels Jump Infantry unit deploys using Deep Strike, the controlling player may re-roll the Scatter "
        "die and any dice rolled for scatter distance. The entire result must be re-rolled and the second result must "
        "be accepted."),
    "Vengeance of a Fallen Angel": (
        "A Blood Angels Character for this rule is an Independent Character, named Character, Sergeant or equivalent "
        "squad leader. Whenever a friendly Blood Angels Character is slain, every friendly non-vehicle Blood Angels unit "
        "with at least one model able to draw line of sight to the Character's final position is affected until the end "
        "of the following Blood Angels player turn: +1 Attack; -1 Leadership; must charge the nearest enemy unit it is "
        "legally able to charge. Units already engaged in close combat still receive the Attack bonus. Not cumulative; "
        "if another Blood Angels Character is slain while the rule is active, its duration is extended until the end of "
        "the following Blood Angels player turn."),
    # Armoury
    "Death Mask": (
        "Any Blood Angels Independent Character may purchase a Death Mask for +10 points. If an enemy unit loses a close "
        "combat in which at least one of its models was in base contact with the bearer, that unit suffers an "
        "additional -1 Leadership when taking the resulting Morale test. The effects of multiple Death Masks are not "
        "cumulative. Counts towards the Space Marine Armoury points limit. Named characters may not take it."),
    "Inferno Pistol": (
        "Any Blood Angels model with access to the Space Marine Armoury may replace its Bolt Pistol with an Inferno "
        "Pistol for +15 points (models in Terminator Armour may not take it). A Legion Moritat may replace both of his "
        "Bolt Pistols with two Inferno Pistols for +20 points in total."),
    "Perdition": (
        "A natural To Wound roll of 6 made with a Blade of Perdition causes a Massive Wound instead of a normal wound. A "
        "Blade of Perdition counts as a sword-like weapon. Any Blood Angels Character with access to the Space Marine "
        "Armoury may purchase a Blade of Perdition for +25 points; a model already equipped with a Power Weapon "
        "(including one that is part of its fixed wargear, e.g. a Legion Champion) may exchange it for a Blade of "
        "Perdition for +10 points."),
    "Over-charged Engines": (
        "Any Blood Angels Rhino (including every Rhino-chassis vehicle: Damocles Command Rhino, Predator, Vindicator, "
        "Whirlwind and Whirlwind Scorpius) may purchase Over-charged Engines for +15 points. Before moving the Rhino during the "
        "Movement phase, the controlling player may declare that it will use its Over-charged Engines and roll a D6: on "
        "a 1 the engines stall and the Rhino may not move that turn; on a 2-3 it moves normally; on a 4-6 it may move as "
        "though it were a Fast Vehicle that turn, to a maximum of 18\". Passengers follow the normal ProHammer rules for "
        "embarking, disembarking and Transport movement."),
    "Furioso-pattern Jump Pack": (
        "One Blood Angels Legion Contemptor Dreadnought in the army may purchase a Furioso-pattern Jump Pack for +55 "
        "points. The Contemptor must be equipped with two Dreadnought Close Combat Weapons. During its Movement phase it "
        "may move up to 12\" and may pass over models and terrain in the same manner as Jump Infantry. It remains a "
        "Walker for all other purposes, may charge normally after making this movement and may not deploy using Deep "
        "Strike (so it may not take a Dedicated Transport Drop Pod). If it ends this movement in Difficult or Dangerous Terrain, roll a D6; on a 1 it suffers a Glancing "
        "Hit."),
    # Consul
    "Sanguinary High Priest": (
        "A Blood Angels Legion Centurion may be upgraded to a Sanguinary High Priest for +45 points. Wargear: Narthecium, "
        "Reductor. Special Rules: Legion Support Officer, Sanguinius' Chosen. A Sanguinary High Priest retains the "
        "normal weapon and wargear options available to a Legion Centurion (he may therefore take a Jump Pack for the "
        "normal points cost)."),
    "Apothecarion": "A Sanguinary High Priest counts as an Apothecary for all rules and wargear restrictions.",
    "Sanguinius' Chosen": ("The Sanguinary High Priest and any Blood Angels unit he has joined have the Furious Charge "
                           "special rule."),
    # Rites of War
    "The Day of Revelation": (
        "EFFECTS - Host of Angels: Legion Veteran Squads equipped with Jump Packs may be selected as Troops choices and may "
        "fulfil compulsory Troops selections. Legion Assault Squads remain Troops choices normally; "
        "Legion Tactical Squads and Legion Breacher Siege Squads no longer count towards compulsory Troops (only Jump "
        "Pack units do). The Day is Revealed: "
        "Blood Angels units composed entirely of Jump Infantry may deploy using Deep Strike even if the mission would not "
        "normally permit it; all Jump Infantry units placed in Reserve using this Rite must enter play using Deep Strike. "
        "On Wings of Fire: at the beginning of the second Blood Angels player turn, all Blood Angels Jump Infantry units "
        "currently held in Reserve become available automatically (no Reserve rolls) and must enter play during that "
        "turn using Deep Strike. Angelic Shock Assault: a Blood Angels Jump Infantry unit which charges during the same "
        "turn that it arrived using Deep Strike receives the normal +1 Attack bonus for charging and the normal benefits "
        "of any Assault Grenades it carries (this overrides the normal ProHammer restrictions on charging after Deep "
        "Strike; all other Deep Strike rules apply normally).\n"
        "LIMITATIONS - The army's Warlord must be equipped with a Jump Pack. At least half of the non-Vehicle units in "
        "the Detachment, rounding up, must be composed entirely of models equipped with Jump Packs. Every Jump Infantry "
        "unit must begin the battle in Reserve and enter play using Deep Strike. The Detachment may include no more than "
        "one Heavy Support choice. The Detachment may not include a Fortification."),
    "The Day of Sorrows": (
        "EFFECTS - The Bitter End: when a non-Vehicle Blood Angels unit is reduced to half or fewer of the number of "
        "models with which it began the battle, it gains Stubborn and Feel No Pain (6+) for the remainder of the battle; "
        "if the unit already has Feel No Pain, improve it by one step instead (maximum 4+). Sorrow Becomes Fury: a Blood "
        "Angels unit affected by The Bitter End gains +1 to its combat-resolution score whenever it wins a close combat "
        "(not cumulative). No Death Unremembered: whenever a Blood Angels unit affected by The Bitter End is completely "
        "destroyed, every friendly non-Vehicle Blood Angels unit with at least one model within 6\" may re-roll its next "
        "failed Morale or Pinning test before the end of the following Blood Angels player turn. Hold Until the Last: "
        "Legion Tactical Squads and Legion Breacher Siege Squads may re-roll failed Pinning tests while they have at "
        "least one model within 6\" of an Objective.\n"
        "LIMITATIONS - The army's compulsory Troops choices must be selected from Legion Tactical Squads, Legion Assault "
        "Squads or Legion Breacher Siege Squads. Units affected by The Bitter End may not voluntarily withdraw from close "
        "combat; if such a unit wins a close combat and the enemy retreats, it must Pursue whenever normally permitted. "
        "The Detachment may not include a Fortification."),
    "Selected as Troops (Host of Angels)": (
        "Under The Day of Revelation, a Legion Veteran Squad equipped with Jump Packs is a Troops choice and may fulfil "
        "compulsory Troops selections."),
    # Units
    "Falling-star Spear": ("A Falling-star Spear is a Two-Handed Power Weapon. Attacks made with it are resolved at +1 "
                           "Strength."),
    "Equinox Blades": "Equinox Blades count as a pair of Power Weapons.",
    "Dawnbreaker Champion": ("The Dawnbreaker Champion may select up to 50 points of permitted weapons and wargear from "
                             "the Space Marine Armoury."),
    "Coriolis Shield": ("A model equipped with a Coriolis Shield has a 3+ Invulnerable Save against close-combat attacks. "
                        "Against all other attacks, use the model's normal saves."),
    "The Blood is Forever": (
        "At the beginning of each Assault phase, if the number of enemy models engaged in the same combat is greater than "
        "the number of models in this unit, the Crimson Paladins gain Feel No Pain (5+) until the end of that Assault "
        "phase. If the enemy outnumbers the unit by at least two models to one, they instead gain Feel No Pain (4+)."),
    "Dual Pistols (Blood Angels)": ("A model with this rule may fire both of its Pistol weapons during the Shooting "
                                    "phase. Both pistols must fire at the same target."),
    "Destroyer Cadre (Angel's Tears)": ("An Angel's Tears Squad may normally only be joined by a Moritat. Dominion Zephon "
                                        "is an exception to this rule."),
    "Blade of Judgement": (
        "A Blade of Judgement is a Two-Handed Power Weapon. Attacks made with it are resolved at +2 Strength. In "
        "addition, a natural To Wound roll of 6 inflicts a Massive Wound (D3) instead of a normal Wound."),
    "Preferred Enemy (Characters)": "The unit has the Preferred Enemy special rule against Characters.",
    "Ofanim Jump Packs": "If equipped with Jump Packs, the unit becomes Jump Infantry.",
    "Grav Engines": (
        "Grav Chariots follow all normal ProHammer rules for Jetbikes. A Grav Chariot may fire both its Twin-linked "
        "Bolters and its mounted Heavy Bolter, Multi-Melta or Assault Cannon during the same Shooting phase. The mounted "
        "weapon may be fired after the Grav Chariot moves."),
    "Sanguine-pattern Jump Pack": ("Follows all normal ProHammer rules for Jump Packs. In addition, it grants its wearer "
                                   "a 5+ Invulnerable Save."),
    "Angelus Boltgun": "An Angelus Boltgun is a 12\" Storm Bolter.",
    "Perdition Weapon": ("A Perdition Weapon counts as a Power Weapon. A natural To Wound roll of 6 made with a Perdition "
                         "Weapon inflicts a Massive Wound (D3) instead of a normal Wound."),
    "Servants of the Great Angel": (
        "A Sanguinary Guard Squad may only be selected as the retinue of a Blood Angels Praetor, Raldoron or Sanguinius. "
        "It does not occupy a separate Force Organisation slot; the character and Sanguinary Guard count as a single HQ "
        "selection. The character must begin the battle joined to the Sanguinary Guard, but may leave the unit normally "
        "during the battle."),
    "Master of the Seraphim": (
        "A Sanguinary Guard Squad containing Azkaellon may deploy using Deep Strike even if the mission does not normally "
        "permit Deep Strike. If the squad has been selected as a character's retinue, that character must also be "
        "capable of deploying by Deep Strike or the unit must deploy normally."),
    "Azkaellon": (
        "One Sanguinary Guard may be upgraded to Azkaellon for +35 points. Azkaellon replaces one Sanguinary Guard and "
        "remains part of the unit for the entire battle. Azkaellon is a Character but is not an Independent Character. "
        "If the Sanguinary Guard purchase Krak grenades or Melta bombs, Azkaellon receives the same upgrade at the normal "
        "squad cost."),
    "Glaive Encarmine": ("The Glaive Encarmine is a Two-Handed, Master-crafted Power Weapon. Attacks made with it are "
                         "resolved at Strength 6."),
    # Characters
    "Encarmine Warblade": "The Encarmine Warblade is a Power Weapon. Attacks made with it are resolved at +1 Strength.",
    "First Captain of the Blood Angels": (
        "Raldoron and any Blood Angels unit he has joined may re-roll failed Morale tests. In addition, friendly Blood "
        "Angels units with a model within 6\" of Raldoron may use his Leadership when taking Morale or Pinning tests."),
    "The Blooded": (
        "At the beginning of each Assault phase, nominate one enemy Independent Character or squad leader in base "
        "contact with Raldoron. Until the end of that Assault phase, Raldoron may re-roll failed To Hit rolls made "
        "against that model."),
    "Command Retinue (Raldoron)": (
        "Raldoron may select a Legion Command Squad, Legion Terminator Command Squad or Sanguinary Guard Squad as his "
        "retinue."),
    "Spiritum Sanguis": (
        "Spiritum Sanguis is a Two-Handed, Master-crafted Power Weapon. Attacks made with it are resolved at +1 Strength. "
        "If Zephon begins an Assault phase in base contact with two or more enemy models, he receives +1 Attack for that "
        "Assault phase."),
    "Lament and Grief": "Lament and Grief are both Volkite Serpentas.",
    "Exarch of the High Host": (
        "Zephon may join an Angel's Tears Squad or Legion Destroyer Squad despite the normal restrictions of Destroyer "
        "Cadre. He may select one Angel's Tears Squad as his retinue. The squad does not occupy a separate Force "
        "Organisation slot."),
    "Saiphan Shard-Axe": ("The Saiphan Shard-Axe is a Master-crafted Power Weapon. Attacks made with it are resolved at "
                          "+1 Strength."),
    "Command Retinue (Blood Angels)": "The character may select one Legion Command Squad as his retinue.",
    "Feel No Pain (4+)": "The model has the Feel No Pain special rule with a 4+ roll.",
    "One Use": "This Weapon can only be fired once per game.",
    # Sanguinius
    "Regalia Resplendent": "The Regalia Resplendent counts as Primarch Armour.",
    "Blade Encarmine": ("The Blade Encarmine is a Master-crafted Power Weapon. Attacks made with it are resolved at +1 "
                        "Strength and have the Shred and Rampage special rules."),
    "Spear of Telesto": ("The Spear of Telesto is a Master-crafted, Two-Handed Power Weapon. Attacks made with it are "
                         "resolved at +3 Strength and have the Lance special rule."),
    "Great Wings": (
        "Sanguinius is treated as Jump Infantry and follows all normal ProHammer rules for Jump Infantry. His ability to "
        "move as Jump Infantry may never be lost, disabled or destroyed as the result of damage to wargear."),
    "Angelic Charge": ("During an Assault phase in which Sanguinius charged, increase his Strength and Attacks "
                       "characteristics by +1 for that Assault phase."),
    "Sire of the Blood Angels": ("Friendly Blood Angels units with at least one model within 12\" of Sanguinius may "
                                 "re-roll failed Morale and Pinning tests. The second result must be accepted."),
    "The Angel Descends": (
        "When Sanguinius enters play using Deep Strike, he does not scatter. If Sanguinius declares a charge during the "
        "same turn in which he arrived using Deep Strike, he receives the normal +1 Attack bonus for charging and the "
        "normal benefits of any Assault Grenades he carries. This overrides the normal ProHammer restrictions on "
        "charging after Deep Strike."),
    "Primarch Retinue (Sanguinius)": (
        "Sanguinius may select a Legion Honour Guard Squad or a Sanguinary Guard Squad as his Primarch Retinue. It does "
        "not occupy an additional Force Organisation selection and otherwise follows the normal Primarch Retinue rules. "
        "A Legion Honour Guard Squad selected this way may equip every model in the squad with a Jump Pack for +10 "
        "points per model; every model in the squad must take this upgrade."),
}

WEAPONS_ = {
    "Inferno Pistol": ('6"', "8", "1", "Pistol, Melta"),
    "Blade of Perdition": ("-", "User", "-", "Power Weapon, Two-Handed, Perdition"),
    "Falling-star Spear": ("-", "User +1", "-", "Power Weapon, Two-Handed"),
    "Pair of Equinox Blades": ("-", "User", "-", "Power Weapon, pair (counts as a pair of Power Weapons)"),
    "Angel's Tears Grenade Launcher": ('24"', "4", "4", "Assault 3, Fleshbane, Rad-phage"),
    "Blade of Judgement": ("-", "User +2", "-", "Power Weapon, Two-Handed, Massive Wound (D3) on a 6 to wound"),
    "Angelus Boltgun": ('12"', "4", "5", "Assault 2"),
    "Perdition Weapon": ("-", "User", "-", "Power Weapon, Massive Wound (D3) on a 6 to wound"),
    "Glaive Encarmine": ("-", "6", "-", "Power Weapon, Two-Handed, Master-crafted"),
    "Encarmine Warblade": ("-", "User +1", "-", "Power Weapon"),
    "Spiritum Sanguis": ("-", "User +1", "-", "Power Weapon, Two-Handed, Master-crafted"),
    "Saiphan Shard-Axe": ("-", "User +1", "-", "Power Weapon, Master-crafted"),
    "Blade Encarmine": ("-", "User +1", "-", "Power Weapon, Master-crafted, Shred, Rampage"),
    "Spear of Telesto": ("-", "User +3", "-", "Power Weapon, Master-crafted, Two-Handed, Lance"),
    "Infernus": ('18"', "8", "1", "Assault 2, Melta, One Use"),
}
MULTI = {
    "Grenade Discharger": {"Grenade Discharger - Frag": ('12"', "3", "6", "Assault 1, Blast"),
                           "Grenade Discharger - Krak": ('12"', "6", "4", "Assault 1")},
}
WEAPON_RULES_ = {
    "Inferno Pistol": ["Melta"],
    "Blade of Perdition": ["Two-Handed", "Perdition"],
    "Falling-star Spear": ["Two-Handed", "Falling-star Spear"],
    "Pair of Equinox Blades": ["Equinox Blades"],
    "Angel's Tears Grenade Launcher": ["Fleshbane", "Rad-phage"],
    "Blade of Judgement": ["Two-Handed", "Blade of Judgement"],
    "Angelus Boltgun": ["Angelus Boltgun"],
    "Perdition Weapon": ["Perdition Weapon"],
    "Glaive Encarmine": ["Two-Handed", "Master-Crafted", "Glaive Encarmine"],
    "Encarmine Warblade": ["Encarmine Warblade"],
    "Spiritum Sanguis": ["Two-Handed", "Master-Crafted", "Spiritum Sanguis"],
    "Saiphan Shard-Axe": ["Master-Crafted", "Saiphan Shard-Axe"],
    "Blade Encarmine": ["Master-Crafted", "Shred", "Rampage", "Blade Encarmine"],
    "Spear of Telesto": ["Master-Crafted", "Two-Handed", "Lance", "Spear of Telesto"],
    "Infernus": ["Melta", "One Use"],
}
WARGEAR_ = {
    "Death Mask": RULES["Death Mask"],
    "Over-charged Engines": RULES["Over-charged Engines"],
    "Furioso-pattern Jump Pack": RULES["Furioso-pattern Jump Pack"],
    "Coriolis Shield": RULES["Coriolis Shield"],
    "Sanguine-pattern Jump Pack": RULES["Sanguine-pattern Jump Pack"],
    "Regalia Resplendent": ("Counts as Primarch Armour.", ["Primarch Armour"]),
    "Great Wings": RULES["Great Wings"],
    "Iron Halo (Named Character)": (
        "Grants a 4+ Invulnerable Save. Part of this named character's own wargear; not counted towards the army's normal "
        "limit of one Iron Halo."),
}


def register():
    ARMY_RULES.update(RULES)
    register_data(weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_, multi_profile=MULTI)
    # weapons that reuse an existing profile
    for n, base in [("Two Volkite Serpentas", "Volkite Serpenta"), ("Lament", "Volkite Serpenta"),
                    ("Grief", "Volkite Serpenta"), ("Assault Cannon with Suspensor Web", "Assault Cannon")]:
        WEAPONS[n] = list(WEAPONS[base])
        WEAPON_RULES[n] = list(WEAPON_RULES.get(base, []))
    WEAPON_RULES["Lament"].append("Lament and Grief")
    WEAPON_RULES["Grief"].append("Lament and Grief")
    WEAPON_RULES["Assault Cannon with Suspensor Web"].append("Suspensor Web")
    # The Day of Revelation: only Jump Pack units count for the compulsory Troops
    for n in ("Legion Tactical Squad", "Legion Breacher Siege Squad"):
        L2.NOT_LINE_UNDER[n].append("The Day of Revelation")


# ------------------------------------------------------------------ local helpers
def _unit_type(e):
    ps = e.find("profiles")
    if ps is None:
        return None
    for p in ps:
        if p.get("typeName") == "Unit":
            for c in p.iter("characteristic"):
                if c.get("name") == "Unit Type":
                    return c.text or ""
    return None


def is_character(e):
    t = _unit_type(e)
    return bool(t) and "Character" in t


def character_variant(roots, base, new, cost_exchange, cost_other, skip_names=()):
    """'Any Character able to select <base> may instead select <new>': adds <new> next to every <base> option inside
    a Character model's own weapon groups (cost_exchange where <base> is free, cost_other otherwise)."""
    base_id = W(base)
    done = set()
    n = 0
    for r in roots:
        for e in r.iter("selectionEntry"):
            if not is_character(e) or e.get("name") in skip_names:
                continue
            for g in e.iter("selectionEntryGroup"):
                if id(g) in done or "Servo-automata" in (g.get("name") or ""):
                    continue
                done.add(id(g))
                links = g.find("entryLinks")
                if links is None:
                    continue
                for lk in list(links):
                    if lk.get("targetId") != base_id:
                        continue
                    cs = lk.find("costs")
                    cost = float(cs[0].get("value")) if cs is not None and len(cs) else 0
                    nid = uid(lk.get("id"), "variant", new)
                    cons = []
                    if any(c.get("type") == "max" for c in lk.iter("constraint")):
                        cons = [constraint(uid(nid, "max"), "max", 1, auto=True)]
                    new_l = link(nid, W(new), new, cost=(cost_exchange if cost == 0 else cost_other) or None,
                                 constraints=cons)
                    if g.get("defaultSelectionEntryId") is not None:
                        new_l.set("sortIndex", str(int(lk.get("sortIndex") or 1) + 100))
                    links.append(new_l)
                    n += 1
    return n


def has_armoury(e):
    return any((g.get("name") or "").startswith("Space Marine Armoury") for g in e.iter("selectionEntryGroup"))


def model(u, name, cost, mn, mx, utype, stats, kit, groups=(), mods=(), rules_=(), auto=False):
    mid = uid("model", u, name)
    return entry(mid, name, typ="model", cost=cost, mods=list(mods),
                 constraints=[constraint(uid(mid, "min"), "min", mn, auto=auto),
                              constraint(uid(mid, "max"), "max", mx, auto=auto)],
                 profiles=[unit_profile(u, name, utype, *stats)], links=[gear(mid, k) for k in kit],
                 groups=list(groups), infolinks=rules_links(list(rules_), key=mid))


def krak_melta(u):
    return [per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
            per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])]


def unit_type_mod(e, value, conds):
    """Change the Unit Type shown on every Unit profile inside e while conds hold."""
    for p in e.iter("profile"):
        if p.get("typeName") != "Unit":
            continue
        cur = None
        for c in p.iter("characteristic"):
            if c.get("name") == "Unit Type":
                cur = c.text or ""
        new = value + (" (Character)" if "Character" in (cur or "") else "")
        p.insert(0, wrap("modifiers", [modifier("set", gs.char_id("Unit", "Unit Type"), new, conds=list(conds))]))


def find_group(e, name=None, gid=None):
    for g in e.iter("selectionEntryGroup"):
        if (name and g.get("name") == name) or (gid and g.get("id") == gid):
            return g
    return None


# ------------------------------------------------------------------ units
def dawnbreakers():
    name = "Dawnbreaker Cohort"
    u = uid("unit", name)
    kit = ["Artificer Armour", "Jump Pack", "Grenade Discharger", "Frag Grenades"]
    did = uid("model", u, "Dawnbreaker")
    cid = uid("model", u, "Dawnbreaker Champion")
    champ = model(u, "Dawnbreaker Champion", 0, 1, 1, "Jump Infantry (Character)", (5, 4, 4, 4, 1, 4, 3, 10, "2+"),
                  kit, rules_=["Dawnbreaker Champion"],
                  groups=[slot(cid, "Replace Falling-star Spear", "Falling-star Spear", [("Pair of Equinox Blades", 0)]),
                          pa_armoury(cid, u, 10)])
    dbs = model(u, "Dawnbreaker", 35, 4, 9, "Jump Infantry", (5, 4, 4, 4, 1, 4, 2, 9, "2+"),
                kit + ["Falling-star Spear"])
    swaps = model_swaps(u, "Dawnbreakers: replace Falling-star Spear (any number)", u, [did],
                        [("Pair of Equinox Blades", 0)])
    return entry(u, name, typ="unit", cost=210 - 4 * 35, cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links([LR, "Hammer of Wrath"], key=u),
                 entries=[champ, dbs, *krak_melta(u)], groups=[swaps])


def crimson_paladins():
    name = "Crimson Paladin Squad"
    u = uid("unit", name)
    pid = uid("model", u, "Crimson Paladin")
    eid = uid("model", u, "Crimson Exemplar")
    kit = ["Cataphractii Terminator Armour", "Coriolis Shield"]
    cc = [("Power Fist", 10), ("Thunder Hammer", 15)]
    ex = model(u, "Crimson Exemplar", 0, 1, 1, "Infantry (Character)", (5, 4, 4, 4, 2, 4, 3, 10, "2+/4+"), kit,
               groups=[slot(eid, "Replace Power Weapon", "Power Weapon", cc),
                       take(eid, "Crimson Exemplar Wargear", [("Grenade Harness", 10)])])
    pal = model(u, "Crimson Paladin", 45, 2, 4, "Infantry", (4, 4, 4, 4, 1, 4, 2, 10, "2+/4+"), kit + ["Power Weapon"])
    swaps = model_swaps(u, "Crimson Paladins: replace Power Weapon (any number)", u, [pid], cc)
    heavy, _ = pool(u, "One Crimson Paladin: replace Coriolis Shield", u,
                    [("Heavy Flamer", 10), ("Assault Cannon", 15), ("Plasma Blaster", 15)], 1)
    return entry(u, name, typ="unit", cost=160 - 2 * 45, cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links([LR, "Stubborn", "The Blood is Forever"], key=u),
                 entries=[ex, pal], groups=[swaps, heavy,
                                            transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                                              "Anvillus Pattern Dreadclaw Drop Pod",
                                                              "Legion Spartan Assault Tank"], orbital=False)])


def angels_tears(key="Angel's Tears Squad", root=True):
    name = "Angel's Tears Squad"
    u = uid("unit", key)
    kit = ["Power Armour", "Jump Pack", "Two Volkite Serpentas", "Frag Grenades", "Rad Grenades"]
    aid = uid("model", u, "Arch-Erelim")
    arch = model(u, "Arch-Erelim", 0, 1, 1, "Jump Infantry (Character)", (4, 4, 4, 4, 1, 4, 2, 9, "3+"), kit,
                 groups=[slot(aid, "Replace Chainsword", "Chainsword",
                              [("Rending Weapon", 5), ("Power Weapon", 10), ("Power Fist", 15)]),
                         pa_armoury(aid, u, 10)])
    ere = model(u, "Erelim", 30, 4, 9, "Jump Infantry", (4, 4, 4, 4, 1, 4, 1, 9, "3+"), kit + ["Chainsword"])
    weapons, _ = pool(u, "Heavy Weapons (1 per 5 models, an Erelim replaces one Volkite Serpenta)", u,
                      [("Rotor Cannon", 5), ("Heavy Flamer", 10), ("Angel's Tears Grenade Launcher", 15),
                       ("Assault Cannon with Suspensor Web", 25)], 0, every=5)
    return entry(u, name, typ="unit", cost=210 - 4 * 30, cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links([LR, "Counter-Attack", "Dual Pistols (Blood Angels)",
                                        "Destroyer Cadre (Angel's Tears)"] + ([] if root else ["Retinue"]), key=u),
                 entries=[arch, ere, *krak_melta(u)], groups=[weapons])


def ofanim():
    name = "Ofanim Court"
    u = uid("unit", name)
    kit = ["Artificer Armour", "Blade of Judgement", "Bolt Pistol", "Combat Shield", "Frag Grenades"]
    pref = model(u, "Ofanim Prefector", 0, 1, 1, "Infantry (Character)", (5, 4, 4, 4, 2, 4, 4, 10, "2+"), kit)
    ofs = model(u, "Ofanim", 50, 2, 4, "Infantry", (5, 4, 4, 4, 2, 4, 3, 9, "2+"), kit)
    jp = per_model(u, "Jump Packs (entire squad)", 15, u, ["Jump Pack"])
    add_to(jp, "infoLinks", rules_links(["Ofanim Jump Packs"], key=jp.get("id")))
    e = entry(u, name, typ="unit", cost=150 - 2 * 50, cats=[foc(ELITES, "Elites", u)],
              infolinks=rules_links([LR, "Preferred Enemy", "Preferred Enemy (Characters)"], key=u),
              entries=[pref, ofs, *krak_melta(u), jp])
    unit_type_mod(e, "Jump Infantry", [has(jp.get("id"), u)])
    return e


def grav_chariots():
    name = "Grav Chariot Squadron"
    u = uid("unit", name)
    mid = uid("model", u, "Grav Chariot")
    gc = model(u, "Grav Chariot", 65, 1, 3, "Jetbike", (4, 4, 4, 5, 1, 4, 2, 8, "2+"),
               ["Twin-linked Bolter", "Heavy Bolter", "Bolt Pistol"])
    swaps = model_swaps(u, "Grav Chariots: replace Heavy Bolter (any number)", u, [mid],
                        [("Multi-Melta", 15), ("Assault Cannon", 20)])
    return entry(u, name, typ="unit", cost=0, cats=[foc(FA, "Fast Attack", u)],
                 infolinks=rules_links([LR, "Grav Engines"], key=u), entries=[gc], groups=[swaps])


SG = uid("unit", "Sanguinary Guard")
AZK = uid("model", SG, "Azkaellon")


def sanguinary_guard():
    u = SG
    gid = uid("model", u, "Sanguinary Guard")
    gmin, gmax = uid(gid, "min"), uid(gid, "max")
    kit = ["Artificer Armour", "Sanguine-pattern Jump Pack", "Death Mask", "Angelus Boltgun", "Perdition Weapon",
           "Frag Grenades"]
    guard = entry(gid, "Sanguinary Guard", typ="model", cost=55,
                  mods=specials_decrement(gid, gmin, gmax, [AZK], u),
                  constraints=[constraint(gmin, "min", 3), constraint(gmax, "max", 6)],
                  profiles=[unit_profile(u, "Sanguinary Guard", "Jump Infantry", 5, 5, 4, 4, 2, 4, 3, 10, "2+/5+")],
                  links=[gear(gid, k) for k in kit])
    azk = entry(AZK, "Azkaellon", typ="model", cost=55 + 35,
                constraints=[constraint(uid(AZK, "max"), "max", 1), unique(AZK)],
                profiles=[unit_profile(u, "Azkaellon", "Jump Infantry (Character)", 6, 5, 4, 4, 2, 4, 3, 10,
                                       "2+/5+")],
                links=[gear(AZK, k) for k in ["Artificer Armour", "Sanguine-pattern Jump Pack", "Death Mask",
                                              "Glaive Encarmine", "Angelus Boltgun", "Frag Grenades"]],
                infolinks=rules_links(["Azkaellon", "Master of the Seraphim"], key=AZK))
    swaps = model_swaps(u, "Any model: replace Angelus Boltgun (any number)", u, [gid, AZK], [("Inferno Pistol", 10)])
    return entry(u, "Sanguinary Guard", typ="unit", cost=175 - 3 * 55,
                 infolinks=rules_links([LR, "Fearless", "Servants of the Great Angel", "Retinue"], key=u),
                 entries=[azk, guard, *krak_melta(u)], groups=[swaps])


# ------------------------------------------------------------------ characters
RALDORON = uid("unit", "Raldoron, the Blooded")
ZEPHON = uid("unit", "Dominion Zephon")
CROHNE = uid("unit", "Aster Crohne")
AMIT = uid("unit", "Nassir Amit, the Flesh Tearer")


def characters(sg):
    out = []
    out.append(named_character(
        LR, "Raldoron, the Blooded", 195, (7, 5, 4, 4, 3, 4, 4, 10, "2+/4+"),
        ["Artificer Armour", "Iron Halo (Named Character)", "Encarmine Warblade", "Combi-Flamer", "Frag Grenades"],
        ["First Captain of the Blood Angels", "The Blooded", "Command Retinue (Raldoron)"],
        retinue=retinue_links("raldoron", [command_squad_for("raldoron", RALDORON),
                                           L2.terminator_command_squad("raldoron"), sg]),
        extra_groups=[take(RALDORON, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])],
        profile_name="Raldoron"))
    out.append(named_character(
        LR, "Dominion Zephon", 175, (6, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Jump Pack", "Lament", "Grief", "Spiritum Sanguis", "Frag Grenades"],
        ["Dual Pistols (Blood Angels)", "Exarch of the High Host"], master=False,
        unit_type="Jump Infantry (Character)",
        retinue=retinue_links("zephon", [angels_tears("zephon-angels-tears", root=False)]),
        extra_groups=[take(ZEPHON, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]))
    out.append(named_character(
        LR, "Aster Crohne", 180, (6, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Saiphan Shard-Axe", "Hand Flamer", "Frag Grenades"],
        ["Feel No Pain", "Feel No Pain (4+)", "Command Retinue (Blood Angels)"], master=False,
        retinue=retinue_links("crohne", [command_squad_for("crohne", CROHNE)]),
        extra_groups=[take(CROHNE, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]))
    out.append(named_character(
        LR, "Nassir Amit, the Flesh Tearer", 180, (6, 5, 4, 4, 3, 5, 3, 10, "2+/4+"),
        ["Artificer Armour", "Iron Halo (Named Character)", "Power Weapon", "Rending Weapon", "Frag Grenades"],
        ["Furious Charge", "Command Retinue (Blood Angels)"],
        retinue=retinue_links("amit", [command_squad_for("amit", AMIT)]),
        extra_groups=[take(AMIT, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])],
        profile_name="Nassir Amit", loyalist=True))
    return out


SANGUINIUS = uid("unit", "Sanguinius, the Great Angel")


def sanguinius(sg):
    u = SANGUINIUS
    hg = L2.honour_guard("sanguinius")
    hg_id = hg.get("id")
    jp = per_model("sanguinius-hg", "Jump Packs (entire squad, Sanguinius' retinue)", 10, hg_id, ["Jump Pack"])
    add_to(hg, "selectionEntries", [jp])
    # no Dedicated Transport for a Jump Pack squad
    tg = find_group(hg, gid=uid("grp", "sanguinius-hg", "transport"))
    if tg is not None:
        c = [has(jp.get("id"), hg_id)]
        add_mods(tg, [modifier("set", uid(tg.get("id"), "max"), 0, conds=c), modifier("set", "hidden", "true", conds=c)])
    unit_type_mod(hg, "Jump Infantry", [has(jp.get("id"), hg_id)])
    ret = retinue_links("sanguinius", [hg, sg], title="Primarch Retinue")
    weapon = slot(u, "Weapon", "Blade Encarmine", [("Spear of Telesto", 0)])
    return primarch(LR, "Sanguinius, the Great Angel", 510, (9, 6, 6, 6, 6, 7, 6, 10, "1+"),
                    ["Regalia Resplendent", "Infernus", "Great Wings", "Frag Grenades"],
                    ["Primarch Armour", "Angelic Charge", "Sire of the Blood Angels", "The Angel Descends",
                     "Great Wings", "Primarch Retinue (Sanguinius)"],
                    retinue=ret, extra_groups=[weapon], unit_type="Jump Infantry (Character)", loyalist=True,
                    profile_name="Sanguinius")


# ------------------------------------------------------------------ extend
def extend(ctx):
    ctx.legion_rules([LR, "Angels of Death", "Descent of Angels", "Vengeance of a Fallen Angel"])

    # Sanguinary High Priest Consul
    add_consul(ctx, "Sanguinary High Priest", 45,
               ["Legion Support Officer", "Sanguinary High Priest", "Apothecarion", "Sanguinius' Chosen",
                "Furious Charge"],
               kit=["Narthecium", "Reductor"], support_officer=True)

    # Moritat: replace both Bolt Pistols with two Inferno Pistols (+20)
    cen = ctx.unit("Legion Centurion")
    mor = L.consul_id("Moritat")
    for e in cen.iter("selectionEntry"):
        if e.get("id") == mor:
            oid = uid("ba", "moritat-inferno")
            ip = link(uid("link", oid, "Inferno Pistol"), W("Inferno Pistol"), "Inferno Pistol",
                      constraints=[constraint(uid(oid, "ip-min"), "min", 2), constraint(uid(oid, "ip-max"), "max", 2)])
            opt = entry(oid, "Two Inferno Pistols (replace both Bolt Pistols)", cost=20,
                        constraints=[constraint(uid(oid, "max"), "max", 1, auto=True)], links=[ip])
            add_to(e, "selectionEntries", [opt])
            c = [has(oid, L.CENTURION)]
            # the Moritat's second Bolt Pistol
            for lk in e.find("entryLinks"):
                if lk.get("targetId") == W("Bolt Pistol"):
                    add_mods(lk, [modifier("set", k.get("id"), 0, conds=c) for k in lk.find("constraints")
                                  if k.get("type") in ("min", "max")])
            # the Centurion's own Bolt Pistol (Armoury slot)
            sgid = uid("slot", "centurion", "Bolt Pistol")
            sg_ = find_group(cen, gid=sgid)
            add_mods(sg_, [modifier("set", uid(sgid, "min"), 0, conds=c), modifier("set", uid(sgid, "max"), 0, conds=c),
                           modifier("set", "hidden", "true", conds=c)])

    # Death Mask: Independent Characters (Praetor / Centurion), counts towards the Armoury cap
    add_armoury_items(ctx, [("Death Mask", 10)], who=("praetor", "centurion"))
    # Over-charged Engines: Blood Angels Rhinos and Rhino-chassis vehicles
    rhinos = {("unit", "Legion Rhino Armoured Carrier"), ("unit", "Damocles Command Rhino"),
              ("unit", "Legion Whirlwind Scorpius"), ("model", "Legion Predator"), ("model", "Legion Vindicator"),
              ("model", "Legion Whirlwind")}
    seen = set()
    for r in ctx.all_entries():
        for e in r.iter("selectionEntry"):
            if (e.get("type"), e.get("name")) in rhinos and e.get("id") not in seen:
                seen.add(e.get("id"))
                oid = uid("ba", "overcharged", e.get("id"))
                add_entry(e, entry(oid, "Over-charged Engines", cost=15, links=[gear(oid, "Over-charged Engines")],
                                   constraints=[constraint(uid(oid, "max"), "max", 1, auto=True)]))
    # Furioso-pattern Jump Pack: one Contemptor in the army, with two Dreadnought Close Combat Weapons
    cont = ctx.unit("Legion Contemptor Dreadnought")
    cu = cont.get("id")
    fid = uid("ba", "furioso")
    not_both = any_of(cond(uid(cu, "arm1-ccw"), cu, "lessThan", 1), cond(uid(cu, "arm2-ccw"), cu, "lessThan", 1))
    add_entry(cont, entry(fid, "Furioso-pattern Jump Pack", cost=55, links=[gear(fid, "Furioso-pattern Jump Pack")],
                          constraints=[constraint(uid(fid, "max"), "max", 1, auto=True),
                                       constraint(uid(fid, "roster"), "max", 1, scope="roster", deep=True)]))
    add_mods(cont, [modifier("add", "error", "A Furioso-pattern Jump Pack requires two Dreadnought Close Combat "
                                             "Weapons.", conds=[has(fid, cu)], groups=[not_both])])
    # ... and may not deploy by Deep Strike: no Dreadnought Drop Pod
    for g in cont.iter("selectionEntryGroup"):
        if g.get("name") == "Dedicated Transport":
            mx = [k for k in g.iter("constraint") if k.get("type") == "max"]
            c = [has(fid, cu)]
            add_mods(g, [modifier("set", k.get("id"), 0, conds=c) for k in mx[:1]] +
                     [modifier("set", "hidden", "true", conds=c)])

    # Blade of Perdition: Characters with the Armoury (+10 exchanging a basic Power Weapon, +25 otherwise)
    sg = sanguinary_guard()
    new_units = [dawnbreakers(), crimson_paladins(), angels_tears(), ofanim(), grav_chariots(), *characters(sg),
                 sanguinius(sg)]
    ctx.add_units(*new_units)
    skip = ("Raldoron, the Blooded", "Dominion Zephon", "Aster Crohne", "Nassir Amit, the Flesh Tearer",
            "Sanguinius, the Great Angel", "Azkaellon", "Crimson Exemplar")
    character_variant(ctx.all_entries(), "Power Weapon", "Blade of Perdition", 10, 25, skip_names=skip)
    armoury_characters, seen_e = [], set()
    for r in ctx.all_entries():
        for e in r.iter("selectionEntry"):
            if id(e) not in seen_e and is_character(e) and e.get("name") not in skip and has_armoury(e):
                seen_e.add(id(e))
                armoury_characters.append(e)
    # ... fixed-kit Power Weapons (e.g. Legion Champion) may be exchanged for +10
    for e in armoury_characters:
        links = e.find("entryLinks")
        for lk in list(links) if links is not None else []:
            if lk.get("targetId") != W("Power Weapon"):
                continue
            oid = uid("ba", "perdition-exchange", lk.get("id"))
            add_entry(e, entry(oid, "Blade of Perdition (replaces Power Weapon)", cost=10,
                               links=[gear(oid, "Blade of Perdition")],
                               constraints=[constraint(uid(oid, "max"), "max", 1, auto=True)]))
            c = [has(oid, e.get("id"))]
            add_mods(lk, [modifier("set", k.get("id"), 0, conds=c) for k in lk.iter("constraint")
                          if k.get("type") in ("min", "max")] + [modifier("set", "hidden", "true", conds=c)])
    # Inferno Pistol: replaces the Bolt Pistol of any model with Armoury access (+15)
    done = set()
    for e in armoury_characters:
        for g in e.iter("selectionEntryGroup"):
            links = g.find("entryLinks")
            if id(g) in done or links is None or g.get("defaultSelectionEntryId") is None:
                continue
            done.add(id(g))
            dflt = [lk for lk in links if lk.get("id") == g.get("defaultSelectionEntryId")]
            if not dflt or dflt[0].get("targetId") != W("Bolt Pistol"):
                continue
            nid = uid(g.get("id"), "ba-inferno")
            links.append(link(nid, W("Inferno Pistol"), "Inferno Pistol", cost=15,
                              constraints=[constraint(uid(nid, "max"), "max", 1, auto=True)]))

    # Sanguinary Guard as a retinue of a Blood Angels Praetor
    pr = ctx.unit("Legion Praetor")
    rg = find_group(pr, gid=uid("grp", "praetor", "retinue"))
    add_to(rg, "entryLinks", [link(uid("link", rg.get("id"), SG), SG, "Sanguinary Guard")])

    # Rites of War
    no_fort = [cond(gs.cat("Fortification"), "force", "atLeast", 1)]
    rev = ctx.add_rite("The Day of Revelation", RULES["The Day of Revelation"], limit_hs=True,
                       errors=[("the Detachment may not include a Fortification.", no_fort)])
    ctx.add_rite("The Day of Sorrows", RULES["The Day of Sorrows"],
                 errors=[("the Detachment may not include a Fortification.", no_fort)])
    # Host of Angels: Veteran Squads with Jump Packs are Troops
    vet = ctx.unit("Legion Veteran Squad")
    vu = vet.get("id")
    on = [cond(rev, "force", "atLeast", 1), has(uid("squadwide", vu, "Jump Packs (entire squad)"), vu)]
    add_mods(vet, [modifier("set-primary", "category", TROOPS, conds=on),
                   modifier("remove", "category", ELITES, conds=on),
                   modifier("add", "category", gs.CAT_LINE, conds=on)])
    add_to(vet, "infoLinks", rules_links(["Selected as Troops (Host of Angels)"], key=vu + "ba"))
