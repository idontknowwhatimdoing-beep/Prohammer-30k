"""VII Legion - Imperial Fists (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, option, upgrade, retinue_links, command_squad_for, named_character,
                            primarch, primarch_retinue, add_armoury_items, add_group, add_entry, register_data)
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile, TDA
from legiones2 import (slot, take, pool, transports, add_mods, add_to, foc, rite_id, rite, any_rite, TROOPS, ELITES,
                       FA, HQ, model_swaps, pa_armoury, squadron, RETINUE_SHARED)
from legiones_wargear import ARMY_RULES, WEAPONS, TDA_SGT

LEGION = "VII - Imperial Fists"
LR = "Legiones Astartes (Imperial Fists)"

STONE = "The Stone Gauntlet"
HAMMERFALL = "Hammerfall Strike Force"
TEMPLAR_RITE = "Templar Assault"

RULES = {
    LR: ("Models with this rule belong to the VII Legion and use the Imperial Fists Legion special rules: Disciplined "
         "Fire, Fortification Masters and Blind to the Risk."),
    "Disciplined Fire": (
        "When an Imperial Fists unit makes a First Fire or Overwatch shooting attack, models in the unit may re-roll To "
        "Hit rolls of 1 when firing Bolters, Bolt Pistols, Combi-Bolters, Storm Bolters, Heavy Bolters or the bolter "
        "component of a Combi-weapon."),
    "Fortification Masters": (
        "Imperial Fists models receive +1 to Armour Penetration rolls against Fortifications, Buildings, Bunkers and "
        "other immobile structures with an Armour Value. A non-vehicle Imperial Fists unit occupying a friendly "
        "Fortification or Bunker gains the Stubborn special rule (no benefit while occupying an enemy Fortification). If "
        "the Imperial Fists are the defenders in a mission which permits the placement of Fortifications or Obstacles, "
        "they may place D3 additional 6\" sections of razor wire or tank traps, wholly within the Imperial Fists "
        "deployment zone."),
    "Blind to the Risk": (
        "In a mission with variable game length, when the battle would normally end, the opposing player may demand that "
        "one additional complete game turn be played. After this additional game turn has been completed, the battle "
        "ends automatically. No effect if the mission has already ended because a specific objective or action has been "
        "completed."),
    # Armoury
    "Solarite Power Gauntlet": (
        "Any Imperial Fists Character with access to the Space Marine Armoury may purchase a Solarite Power Gauntlet for "
        "+30 points; a model already equipped with a Power Fist may exchange it for a Solarite Power Gauntlet, also "
        "for +30 points. Unlike a normal Power Fist, the Solarite Power Gauntlet always strikes at Strength 10 regardless of the "
        "bearer's Strength characteristic."),
    "Vigil Pattern Storm Shield": (
        "An Imperial Fists Independent Character may purchase a Vigil Pattern Storm Shield for +25 points. The bearer may "
        "carry no more than one weapon in addition to the shield. Grants a 3+ Invulnerable Save. The shield occupies one "
        "hand and the bearer may never receive the bonus Attack for fighting with two close-combat weapons. Other "
        "Imperial Fists units may only gain access to it through their own army list entries; it does not make Storm "
        "Shields generally available to the Legiones Astartes. It counts towards the Armoury points limit and may not be "
        "combined with a Refractor Field, Combat Shield or Boarding Shield."),
    "Teleportation Transponders": (
        "Any Imperial Fists unit composed entirely of models wearing any form of Terminator Armour may purchase "
        "Teleportation Transponders for +15 points per unit. An Imperial Fists Independent Character wearing any form of "
        "Terminator Armour may purchase them for +10 points (Hammerfall Strike Force: any Imperial Fists Infantry unit "
        "+15 per unit, any Imperial Fists Independent Character +10). A model or unit equipped with Teleportation "
        "Transponders may deploy using Deep Strike even if the mission would not normally permit Deep Strike. An "
        "Independent Character intending to Deep Strike as part of another unit must purchase Teleportation "
        "Transponders separately. Units which already have Deep Strike built in (e.g. Jump Infantry) may not purchase "
        "them. Under Hammerfall Strike Force named characters and Rogal Dorn may purchase them as well (+10)."),
    # Rites of War
    STONE: (
        "EFFECTS - Warders of the Phalanx: Phalanx Warder Squads may be selected as Troops choices and may fulfil "
        "compulsory Troops selections; Legion Breacher Siege Squads may also fulfil compulsory Troops selections "
        "normally. Shield Wall: an Imperial Fists Infantry unit in which every model is equipped with either a Boarding "
        "Shield or a Vigil Pattern Storm Shield may form a Shield Wall. It is active provided the unit did not Advance "
        "during its preceding Movement phase, is not Falling Back and did not charge during the current player turn. "
        "While active, models in the unit may re-roll failed Invulnerable Saves granted by Boarding Shields or Vigil "
        "Pattern Storm Shields (a re-rolled save may never be re-rolled again). Unyielding Line: while its Shield Wall is "
        "active, the unit gains Stubborn and may re-roll failed Pinning tests. The Hammer Behind the Shield: models "
        "equipped with Boarding Shields gain the Hammer of Wrath special rule (normal ProHammer definition) - a model "
        "does not receive an additional attack; instead, one of its normally allowed attacks may be resolved at "
        "Initiative 10 during a turn in which it charges.\n"
        "LIMITATIONS - The army's compulsory Troops choices must be Legion Breacher Siege Squads or Phalanx Warder "
        "Squads. The Detachment must include at least one Independent Character equipped with either a Boarding Shield "
        "or a Vigil Pattern Storm Shield. No unit in the Detachment may voluntarily deploy using Deep Strike (Teleportation "
        "Transponders, Drop Pods and Dreadclaw Drop Pods may not be taken). The army "
        "may include no more than one Fast Attack choice."),
    HAMMERFALL: (
        "EFFECTS - Landing Force: Phalanx Warder Squads may be selected as Troops choices and may fulfil compulsory "
        "Troops selections. Teleport Array: any Imperial Fists Infantry unit may purchase Teleportation Transponders for "
        "+15 points per unit and any Imperial Fists Independent Character for +10 points; this overrides the normal "
        "restriction to models wearing Terminator Armour. A unit with Teleportation Transponders may deploy using Deep "
        "Strike even if the mission would not normally permit it (named characters and Rogal Dorn included); an Independent Character intending to Deep Strike as "
        "part of another unit must purchase them separately. Blinding Luminescence: an Imperial Fists unit arriving by "
        "Deep Strike using Teleportation Transponders gains Shrouded from the moment it is placed until the beginning of "
        "its next player turn. After it has been placed, every enemy unit with at least one model within 12\" of the "
        "arriving unit and with line of sight to at least one model in it must immediately take an Initiative test; if "
        "failed, that unit suffers the effects of the Blind special rule (Weapon Skill 1, Ballistic Skill 1) until the "
        "end of its next player turn. Each enemy unit only makes one such test per arriving Imperial Fists unit.\n"
        "LIMITATIONS - The army's Warlord must be equipped with Teleportation Transponders. Every Vehicle in the "
        "Detachment must begin the battle in Reserve; Tarantula Sentry Gun Batteries may not be taken. The Detachment "
        "may not include a Fortification."),
    TEMPLAR_RITE: (
        "EFFECTS - Templar Host: Templar Brethren Squads may be selected as Troops choices and may fulfil compulsory "
        "Troops selections. Crusading Assault: during an Assault phase in which a Templar Brethren Squad charged after "
        "disembarking from a vehicle with the Assault Vehicle special rule during the same player turn, the squad gains "
        "Furious Charge and its normal charge distance is increased from 6\" to 7\" for that Assault phase. Swords of "
        "the Legion: during the first round of a close combat in which a Templar Brethren Squad charged, models in that "
        "squad may re-roll To Hit rolls of 1 with Rending Weapons, Power Weapons, Relic Blades and other weapons "
        "specifically stated to count as swords. Assault Transports: a Templar Brethren Squad may select a Land Raider "
        "Phobos or Land Raider Proteus as a Dedicated Transport at its normal points cost; a squad of a size which "
        "cannot be carried by either vehicle may instead select a Legion Spartan Assault Tank at its normal points cost "
        "(the Templar Brethren Squad may take any Land Raider variant, including the Spartan, in any case). "
        "All normal Transport Capacity restrictions apply.\n"
        "LIMITATIONS - The army's compulsory Troops choices must be Templar Brethren Squads; while Templar Assault is "
        "selected, Templar Brethren Squads ignore their normal 0-1 limitation. The army may include no more than one "
        "Fast Attack choice. The army may not include a Fortification. The army's Warlord must be equipped with a Power "
        "Weapon, Rending Weapon, Relic Blade or another sword-like close-combat weapon which ignores Armour Saves."),
    "Selected as Troops (Imperial Fists Rites)": (
        "The Stone Gauntlet / Hammerfall Strike Force (Phalanx Warder Squads) and Templar Assault (Templar Brethren "
        "Squads): this unit is a Troops choice and may fulfil compulsory Troops selections."),
    # Units
    "Righteous Zeal": (
        "Whenever the squad would normally take a Morale test for suffering 25% or more casualties from enemy shooting, "
        "it may instead move D6\" directly towards the nearest visible enemy unit. This movement may not bring any model "
        "within 1\" of an enemy model and does not count as charging or Falling Back. If no enemy unit is visible, take "
        "the Morale test normally."),
    "Huscarl Retinue": (
        "One Huscarl Terminator Retinue may be selected for Rogal Dorn, Sigismund or an Imperial Fists Praetor wearing "
        "Terminator Armour (also for Evander Garrius as his Command Retinue). The squad does not occupy a separate Force "
        "Organisation slot."),
    "Firing Mode": (
        "After deployment but before the first turn begins, choose one firing mode for each Tarantula. Point Defence: "
        "fixed 90 degree firing arc, may engage targets within 24\". Sentry: 360 degree firing arc, may engage targets "
        "within 12\". The selected mode cannot be changed during the battle."),
    "Automated Targeting": (
        "A Tarantula fires automatically during the Imperial Fists Shooting phase if an eligible target is available. A "
        "Heavy Bolter Tarantula fires at the nearest visible non-Vehicle enemy unit. A Lascannon Tarantula fires at the "
        "nearest visible enemy Vehicle or Monstrous Creature. If no preferred target is available, it fires at the "
        "nearest other eligible enemy target."),
    "Disposable Platform": "Any Glancing or Penetrating Hit destroys the Tarantula.",
    # Characters
    "The Black Sword": (
        "The Black Sword is a Two-Handed, Master-crafted Power Weapon which grants Sigismund +2 Strength. Sigismund never "
        "requires worse than a 3+ To Hit in close combat. Any natural To Wound roll of 6 made with the Black Sword "
        "inflicts a Massive Wound (D3) instead of a normal Wound."),
    "Massive Wound": (
        "A Massive Wound deals D3 wounds to the target model. Against target units with multi-wound models, Massive "
        "Wounds may need to be rolled and resolved one at a time to ensure that wounds are allocated to wounded models "
        "sequentially. Excess damage from a Massive Wound beyond what is needed to kill a model does not spill over onto "
        "other models."),
    "Kingslayer": (
        "After deployment but before the first turn begins, nominate one enemy Independent Character. If Sigismund "
        "personally slays the nominated character, the Imperial Fists player receives an additional 150 Victory Points "
        "and Sigismund becomes Fearless for the remainder of the battle. If the nominated character survives the battle, "
        "the opposing player instead receives an additional 150 Victory Points. Only applies in missions using Victory "
        "Points."),
    "Command Retinue (Sigismund)": (
        "Sigismund may select either a Templar Brethren Squad or a Huscarl Terminator Retinue as his retinue. The "
        "selected unit does not occupy a separate Force Organisation slot."),
    "The Headsman and the Hunter": (
        "The Headsman and the Hunter are a matched pair of Power Weapons. The +1 Attack for fighting with two close-combat "
        "weapons is already included in Rann's profile. When fighting a Vehicle, Rann may choose to use both weapons as "
        "a single heavy blow: he makes one fewer Attack, but those attacks gain Armourbane."),
    "Executioner's Tax": (
        "Whenever an enemy unit successfully charges Rann or a unit he has joined, that enemy unit suffers D3 automatic "
        "Strength 5 AP4 hits after completing its charge move but before close-combat attacks are resolved."),
    "Lord Seneschal": ("While Rann has joined a Legion Breacher Squad or Phalanx Warder Squad, that unit receives +1 Weapon "
                       "Skill during an Assault phase in which it charged."),
    "Teleport Transponder (Polux)": (
        "Before deployment, Polux may be assigned to one Legion Terminator Squad, Legion Terminator Command Squad or "
        "Huscarl Terminator Retinue. Polux and the nominated unit gain Deep Strike and must enter play together if they "
        "use this rule."),
    "The Crimson Fist": (
        "At the beginning of an Assault phase in which Polux is engaged, he may make a single attack with his "
        "Master-crafted Power Fist instead of making his normal attacks. This attack is resolved at Initiative 4 and "
        "Strength 8 and ignores Armour Saves. Polux makes exactly one attack that Assault phase regardless of any other "
        "bonuses."),
    "Hold the Line": (
        "If Diaz and the unit he has joined did not move during the Movement phase, they gain Counter-Attack until the "
        "beginning of the next Imperial Fists turn. In addition, they may re-roll failed Morale tests during this time."),
    "Command Retinue (Diaz)": (
        "Diaz may select one Phalanx Warder Squad or Legion Command Squad as his retinue. The selected unit does not "
        "occupy a separate Force Organisation slot."),
    "Subjugator": ("Subjugator is a Master-crafted Power Fist. Attacks made with Subjugator are resolved at Strength 10 "
                   "instead of doubling Garrius' Strength."),
    "Tyrant of Cthonia": (
        "Garrius and any Imperial Fists unit he has joined may re-roll failed Pinning tests. In addition, if Garrius' unit "
        "wins a close combat, it may re-roll the dice when determining its Consolidation distance. The second result "
        "must be accepted."),
    "Command Retinue (Garrius)": (
        "Garrius may select a Huscarl Terminator Retinue or Legion Terminator Command Squad as his retinue. The selected "
        "unit does not occupy a separate Force Organisation slot."),
    # Rogal Dorn
    "Storm's Teeth": ("A colossal chainsword. Storm's Teeth is a Two-Handed Power Weapon. Attacks made with it are "
                      "resolved at +2 Strength and have the Shred and Rampage special rules."),
    "The Unyielding": "Rogal Dorn may re-roll Armour Saves of 1. The second result must be accepted.",
    "Lord Castellan": (
        "Friendly Imperial Fists units with at least one model within 12\" of Rogal Dorn gain the Stubborn special rule. "
        "A unit which already has Stubborn may instead re-roll failed Pinning tests while within 12\" of Dorn."),
    "Master of Defence": (
        "Rogal Dorn and any unit he has joined count as being equipped with Frag Grenades when assaulted through "
        "Difficult Terrain. In addition, Dorn and any unit he has joined may make an Overwatch attack when charged even "
        "if another rule or circumstance would normally prevent that unit from doing so."),
    "This Ground Shall Not Fall": (
        "After terrain has been placed but before either army deploys, nominate up to two Fortifications, ruins or other "
        "suitable defensive terrain features wholly or partially within the Imperial Fists deployment zone. The Cover "
        "Save provided by each nominated terrain feature is improved by 1, to a maximum of 3+. Friendly Imperial Fists "
        "units occupying either nominated terrain feature may not be Pinned. These benefits last for the duration of "
        "the battle."),
    "Primarch Retinue (Rogal Dorn)": (
        "Rogal Dorn may select one Legion Honour Guard Squad, Legion Terminator Command Squad, Huscarl Terminator Retinue "
        "or Templar Brethren Squad as his Primarch Retinue. It does not occupy an additional Force Organisation "
        "selection and otherwise follows the normal Primarch Retinue rules. A Huscarl Terminator Retinue selected for "
        "Rogal Dorn ignores any normal requirement for the accompanying Character to wear Terminator Armour."),
}

WEAPONS_ = {
    "Solarite Power Gauntlet": ("-", "10", "-", "Power Weapon, Unwieldy, Specialist Weapon"),
    "The Black Sword": ("-", "User +2", "-", "Power Weapon, Two-Handed, Master-crafted"),
    "The Headsman": ("-", "User", "-", "Power Weapon"),
    "The Hunter": ("-", "User", "-", "Power Weapon"),
    "Master-crafted Power Fist": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Master-crafted"),
    "Subjugator": ("-", "10", "-", "Power Weapon, Unwieldy, Specialist Weapon, Master-crafted"),
    "Storm's Teeth": ("-", "User +2", "-", "Power Weapon, Two-Handed, Shred, Rampage"),
    "Voice of Terra": ('24"', "5", "4", "Salvo 3/5, Rending"),
}
WEAPON_RULES_ = {
    "Solarite Power Gauntlet": ["Solarite Power Gauntlet", "Unwieldy"],
    "The Black Sword": ["The Black Sword", "Two-Handed", "Master-Crafted", "Massive Wound"],
    "The Headsman": ["The Headsman and the Hunter"],
    "The Hunter": ["The Headsman and the Hunter"],
    "Master-crafted Power Fist": ["Master-Crafted", "Unwieldy"],
    "Subjugator": ["Subjugator", "Master-Crafted", "Unwieldy"],
    "Storm's Teeth": ["Storm's Teeth", "Two-Handed", "Shred", "Rampage"],
    "Voice of Terra": ["Rending"],
}
WARGEAR_ = {
    "Vigil Pattern Storm Shield": RULES["Vigil Pattern Storm Shield"],
    "Teleportation Transponders": RULES["Teleportation Transponders"],
    "Iron Halo (Named Character)": (
        "Grants a 4+ Invulnerable Save. Part of this named character's own wargear; not counted towards the army's normal "
        "limit of one Iron Halo."),
    "Auric Armour": ("Rogal Dorn's armour. Auric Armour counts as Primarch Armour.", ["Primarch Armour"]),
}


def register():
    ARMY_RULES.update(RULES)
    register_data(weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_)
    # Rites of War changing the compulsory Troops
    for n in ["Legion Tactical Squad", "Legion Assault Squad"]:
        L2.NOT_LINE_UNDER[n] += [STONE, TEMPLAR_RITE]
    L2.NOT_LINE_UNDER["Legion Breacher Siege Squad"].append(TEMPLAR_RITE)


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


def find_group(e, name):
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == name:
            return g
    return None


def model(u, name, cost, mn, mx, utype, stats, kit, groups=(), rules_=()):
    mid = uid("model", u, name)
    return mid, entry(mid, name, typ="model", cost=cost,
                      constraints=[constraint(uid(mid, "min"), "min", mn), constraint(uid(mid, "max"), "max", mx)],
                      profiles=[unit_profile(u, name, utype, *stats)], links=[gear(mid, k) for k in kit],
                      groups=list(groups), infolinks=rules_links(list(rules_), key=mid))


def troops_mods(rites, normal=ELITES):
    on = any_rite(*rites)
    return [modifier("set-primary", "category", TROOPS, groups=[on]),
            modifier("remove", "category", normal, groups=[any_rite(*rites)]),
            modifier("add", "category", gs.CAT_LINE, groups=[any_rite(*rites)])]


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
                if id(g) in done:
                    continue
                done.add(id(g))
                links = g.find("entryLinks")
                if links is None:
                    continue
                if any(lk.get("targetId") == W(new) for lk in links):
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


# ------------------------------------------------------------------ units
TEMPLARS = uid("unit", "Templar Brethren Squad")
WARDERS = uid("unit", "Phalanx Warder Squad")
TARANTULA = uid("unit", "Tarantula Sentry Gun Battery")


def templars(key="Templar Brethren Squad", root=True):
    u = uid("unit", key)
    kit = ["Power Armour", "Combat Shield", "Bolt Pistol"]
    bid, brethren = model(u, "Templar Brethren", 27, 4, 9, "Infantry", (5, 4, 4, 4, 1, 4, 1, 9, "3+/6+"),
                          kit + ["Rending Weapon"])
    cid = uid("model", u, "Templar Champion")
    _, champ = model(u, "Templar Champion", 0, 1, 1, "Infantry (Character)", (5, 4, 4, 4, 1, 4, 2, 9, "3+/6+"), kit,
                     groups=[pa_armoury(cid, u, 10, slots=["Bolt Pistol", "Rending Weapon"], skip=("Combat Shield",))])
    pw = model_swaps(u, "Up to five Templar Brethren: replace Rending Weapon", u, [bid], [("Power Weapon", 10)])
    max5 = uid(pw.get("id"), "max5")
    # the Champion may be one of the five: Power Weapon for +10 (not counted towards his Armoury cap)
    champ_pw = cond(W("Power Weapon"), cid, "atLeast", 1)
    add_to(pw, "constraints", [constraint(max5, "max", 5)])
    add_mods(pw, [modifier("decrement", max5, 1, conds=[champ_pw])])
    for g in champ.iter("selectionEntryGroup"):
        if g.get("name") == "Replace Rending Weapon":
            for lk in g.iter("entryLink"):
                if lk.get("targetId") == W("Power Weapon"):
                    lk.find("costs")[0].set("value", "10")
        if g.get("name") == "Space Marine Armoury (max 50 pts)":
            cap_id = next(c.get("id") for c in g.find("constraints") if c.get("field") == PTS)
            add_mods(g, [modifier("increment", cap_id, 10, conds=[champ_pw])])
    tr = transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod", "Anvillus Pattern Dreadclaw Drop Pod",
                           "Land Raider Phobos", "Land Raider Proteus", "Legion Spartan Assault Tank"])
    mods, cons, cats = [], [], []
    if root:
        cats = [foc(ELITES, "Elites", u)]
        fl = force_limit(u, 1)
        cons = [fl]
        mods = troops_mods([TEMPLAR_RITE]) + [modifier("set", fl.get("id"), 99, conds=[rite(TEMPLAR_RITE)])]
    rl = [LR, "Stubborn", "Righteous Zeal"] + (["Selected as Troops (Imperial Fists Rites)"] if root else ["Retinue"])
    name = "0-1 Templar Brethren Squad" if root else "Templar Brethren Squad"
    e = entry(u, name, typ="unit", cost=135 - 4 * 27, cats=cats, mods=mods, constraints=cons,
              infolinks=rules_links(rl, key=u),
              entries=[champ, brethren, per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                       per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
              groups=[pw, L.one_each(u, "Squad Equipment (one model each)", [("Legion Vexilla", 10), ("Nuncio Vox", 10)]),
                      tr])
    if root:
        add_mods(e, [modifier("set", "name", "Templar Brethren Squad", conds=[rite(TEMPLAR_RITE)])])
    return e


def warders(key="Phalanx Warder Squad", root=True):
    u = uid("unit", key)
    kit = ["Power Armour", "Boarding Shield"]
    _, wards = model(u, "Phalanx Warder", 28, 4, 9, "Infantry", (4, 4, 4, 4, 1, 4, 1, 9, "3+/5+"),
                     kit + ["Bolt Pistol", "Power Weapon"])
    sid = uid("model", u, "Warder Sergeant")
    _, sgt = model(u, "Warder Sergeant", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 2, 9, "3+/5+"), kit,
                   groups=[pa_armoury(sid, u, 10, slots=["Bolt Pistol", "Power Weapon"],
                                      skip=("Combat Shield", "Refractor Field"))])
    specials, _ = pool(u, "Special Weapons (1 per 5 models, replace Bolt Pistol)", u,
                       [("Flamer", 5), ("Meltagun", 10), ("Plasma Gun", 15)], 0, every=5)
    cats, mods = [], []
    if root:
        cats = [foc(ELITES, "Elites", u)]
        mods = troops_mods([STONE, HAMMERFALL])
    rl = [LR, "Stubborn", "Counter-Attack"] + (["Selected as Troops (Imperial Fists Rites)"] if root else ["Retinue"])
    return entry(u, "Phalanx Warder Squad", typ="unit", cost=150 - 4 * 28, cats=cats, mods=mods,
                 infolinks=rules_links(rl, key=u),
                 entries=[sgt, wards, per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[specials,
                         L.one_each(u, "Squad Equipment (one model each)", [("Legion Vexilla", 10), ("Nuncio Vox", 10)]),
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Anvillus Pattern Dreadclaw Drop Pod",
                                           "Land Raider Phobos", "Land Raider Proteus",
                                           "Legion Spartan Assault Tank"])])


def captain_armoury(mid):
    """Huscarl Captain: up to 50 points of Terminator weapons and wargear (Terminator Sergeant column)."""
    ranged = [(n, p) for n, p in TDA_SGT.items() if n in ("Combi-Flamer", "Combi-Grenade Launcher", "Combi-Meltagun",
                                                          "Combi-Plasma Gun", "Combi-Volkite Charger",
                                                          "Foeblaster Boltgun", "Storm Bolter")]
    cc = [(n, p) for n, p in TDA_SGT.items() if n in ("Chainfist", "Lightning Claw", "Power Fist", "Thunder Hammer")]
    wargear = [(n, p) for n, p in TDA_SGT.items() if n in ("Bionics", "Master-crafted Weapon", "Purity Seals")]
    cap = uid("grp", mid, "captain-armoury")
    return group(cap, "Space Marine Armoury (max 50 pts)",
                 groups=L2.tda_weapon_slots(mid, ranged, cc, TDA_SGT["Pair of Lightning Claws"]) +
                 [take(mid, "Additional Wargear", wargear)],
                 constraints=[constraint(uid(cap, "maxpts"), "max", 50, scope="self", field=PTS, deep=True)])


def huscarls(key):
    """Huscarl Terminator Retinue (only ever a retinue)."""
    u = uid("unit", key)
    hid, hus = model(u, "Huscarl", 50, 4, 9, "Infantry", (5, 4, 4, 4, 1, 4, 2, 10, "2+/4+"),
                     ["Cataphractii Terminator Armour", "Combi-Bolter", "Power Weapon"])
    cid = uid("model", u, "Huscarl Captain")
    _, cap = model(u, "Huscarl Captain", 0, 1, 1, "Infantry (Character)", (5, 4, 4, 4, 2, 4, 3, 10, "2+/4+"),
                   ["Cataphractii Terminator Armour"], groups=[captain_armoury(cid)])
    return entry(u, "Huscarl Terminator Retinue", typ="unit", cost=250 - 4 * 50,
                 infolinks=rules_links([LR, "Stubborn", "Retinue", "Huscarl Retinue"], key=u),
                 entries=[cap, hus,
                          option(u, "Teleportation Transponders (entire unit)", 15, item="Teleportation Transponders",
                                 hide=[cond(rite_id(STONE), "force", "atLeast", 1)])],
                 groups=[model_swaps(u, "Huscarls: replace Combi-bolter (any number)", u, [hid],
                                     [("Foeblaster Boltgun", 5), ("Combi-Flamer", 10), ("Combi-Volkite Charger", 10),
                                      ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15)]),
                         model_swaps(u, "Huscarls: replace Power Weapon (any number)", u, [hid],
                                     [("Power Fist", 10), ("Lightning Claw", 10), ("Chainfist", 15),
                                      ("Thunder Hammer", 15)]),
                         take(u, "One model may take", [("Grenade Harness", 10)])])


def tarantulas():
    e = squadron("Tarantula Sentry Gun Battery", 20, "Tarantula Sentry Gun",
                 lambda k, n: L.vehicle_profile(k, n, "Vehicle (Immobile)", 2, 10, 10, 10), FA, "Fast Attack",
                 ["Immobile", "Automated Targeting", "Firing Mode", "Disposable Platform"], [],
                 lambda mid: [slot(mid, "Replace Twin-linked Heavy Bolter", "Twin-linked Heavy Bolter",
                                   [("Twin-linked Lascannon", 15)])])
    e.set("name", "0-2 Tarantula Sentry Gun Battery")
    fl = force_limit(TARANTULA, 2)
    add_to(e, "constraints", [fl])
    add_mods(e, [modifier("set", "hidden", "true", conds=[rite(HAMMERFALL)]),
                 modifier("set", fl.get("id"), 0, conds=[rite(HAMMERFALL)])])
    return e


# ------------------------------------------------------------------ characters
SIGISMUND = uid("unit", "Sigismund, First Captain")
RANN = uid("unit", "Fafnir Rann")
POLUX = uid("unit", "Alexis Polux")
DIAZ = uid("unit", "Camba Diaz")
GARRIUS = uid("unit", "Evander Garrius")
DORN = uid("unit", "Rogal Dorn, the Praetorian of Terra")
NAMED = [SIGISMUND, RANN, POLUX, DIAZ, GARRIUS]


def characters():
    out = [
        named_character(LR, "Sigismund, First Captain", 220, (7, 5, 4, 4, 3, 5, 4, 9, "2+/4+"),
                        ["Artificer Armour", "Iron Halo (Named Character)", "Terminator Honours", "Purity Seals",
                         "Bolt Pistol", "The Black Sword"],
                        ["Honour or Death", "Kingslayer", "Command Retinue (Sigismund)"],
                        retinue=retinue_links("sigismund", [templars("sigismund-templars", root=False),
                                                            huscarls("sigismund-huscarls")]),
                        profile_name="Sigismund"),
        named_character(LR, "Fafnir Rann", 175, (6, 5, 4, 4, 3, 5, 4, 10, "2+/5+"),
                        ["Artificer Armour", "Refractor Field", "The Headsman", "The Hunter", "Frag Grenades"],
                        ["Executioner's Tax", "Lord Seneschal"],
                        extra_groups=[take(RANN, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]),
        named_character(LR, "Alexis Polux", 170, (5, 5, 4, 4, 3, 4, 4, 9, "3+/3+"),
                        ["Power Armour", "Vigil Pattern Storm Shield", "Terminator Honours", "Combi-Meltagun",
                         "Master-crafted Power Fist", "Frag Grenades"],
                        ["Stubborn", "Teleport Transponder (Polux)", "The Crimson Fist"],
                        extra_groups=[take(POLUX, "Wargear", [("Krak Grenades", 2)])]),
        named_character(LR, "Camba Diaz", 160, (6, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
                        ["Artificer Armour", "Refractor Field", "Power Weapon", "Bolt Pistol", "Frag Grenades"],
                        ["Stubborn", "Hold the Line", "Command Retinue (Diaz)"],
                        retinue=retinue_links("diaz", [warders("diaz-warders", root=False),
                                                       command_squad_for("diaz", DIAZ)]),
                        extra_groups=[take(DIAZ, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]),
        named_character(LR, "Evander Garrius", 200, (6, 5, 4, 4, 3, 4, 4, 10, "2+/4+"),
                        ["Cataphractii Terminator Armour", "Subjugator", "Volkite Charger", "Bionics"],
                        ["Fearless", "Tyrant of Cthonia", "Command Retinue (Garrius)"],
                        retinue=retinue_links("garrius", [huscarls("garrius-huscarls"),
                                                          L2.terminator_command_squad("garrius")])),
    ]
    return out


def dorn():
    ret = primarch_retinue("dorn", extra=[huscarls("dorn-huscarls"), templars("dorn-templars", root=False)])
    return primarch(LR, "Rogal Dorn, the Praetorian of Terra", 490, (7, 6, 6, 6, 6, 6, 5, 10, "1+"),
                    ["Auric Armour", "Storm's Teeth", "Voice of Terra", "Frag Grenades"],
                    ["Primarch Armour", "The Unyielding", "Lord Castellan", "Master of Defence",
                     "This Ground Shall Not Fall", "Primarch Retinue (Rogal Dorn)"],
                    retinue=ret, profile_name="Rogal Dorn", loyalist=True)


# ------------------------------------------------------------------ Legion-wide options
IC_TT = uid("vii", "ic-teleportation-transponders")


def add_teleportation(ctx):
    """Teleportation Transponders: Terminator units (+15) and ICs in Terminator Armour (+10); with Hammerfall Strike
    Force any Infantry unit (+15) and any Independent Character (+10)."""
    no_hf = cond(rite_id(HAMMERFALL), "force", "lessThan", 1)
    stone = cond(rite_id(STONE), "force", "atLeast", 1)
    ic = entry(IC_TT, "Teleportation Transponders", cost=10, links=[gear(IC_TT, "Teleportation Transponders")])
    ctx.add_shared(ic)

    def ic_link(e, hide_conds):
        lid = uid("link", e.get("id"), "vii-tt")
        hide = any_of(stone, all_of(*hide_conds)) if hide_conds is not None else any_of(stone)
        mods = [modifier("set", "hidden", "true", groups=[hide]),
                modifier("set", uid(lid, "max"), 0, groups=[hide])]
        add_to(e, "entryLinks", [link(lid, IC_TT, "Teleportation Transponders", mods=mods,
                                      constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])])

    for n in ("Legion Praetor", "Legion Centurion"):
        e = ctx.unit(n)
        ic_link(e, [lacks(W(t), e.get("id")) for t in TDA] + [no_hf])
    for u in NAMED + [DORN]:
        e = next(x for x in ctx.units if x.get("id") == u)
        ic_link(e, None if u == GARRIUS else [no_hf])

    tda_units = {"Legion Terminator Squad", "Legion Terminator Command Squad"}
    seen = set()
    for e in ctx.all_entries():
        if e.get("type") != "unit" or id(e) in seen or e.get("name") == "Huscarl Terminator Retinue":
            continue
        seen.add(id(e))
        models = [m for m in e.iter("selectionEntry") if m.get("type") == "model"]
        if not models:
            continue
        types = [_unit_type(m) for m in models]
        if any(t is None or not t.startswith("Infantry") for t in types):
            continue
        key = e.get("id") + "vii-tt"
        hide = [stone] if e.get("name") in tda_units else [stone, no_hf]
        add_entry(e, option(key, "Teleportation Transponders (entire unit)", 15, item="Teleportation Transponders",
                            hide=hide))


def add_huscarls_to_praetor(ctx):
    p = ctx.unit("Legion Praetor")
    pid = p.get("id")
    hus = huscarls("praetor-huscarls")
    g = find_group(p, "Retinue (no Force Organisation slot)")
    RETINUE_SHARED.append(hus)
    g.find("entryLinks").append(link(uid("link", g.get("id"), hus.get("id")), hus.get("id"), hus.get("name"),
                                     mods=[modifier("set", "hidden", "true", groups=[L.no_tda(pid)])]))
    add_mods(p, [modifier("add", "error", "A Huscarl Terminator Retinue may only be selected for a Praetor wearing "
                                          "Terminator Armour.",
                          conds=[cond(hus.get("id"), pid, "atLeast", 1)] + [lacks(W(t), pid) for t in TDA])])


DEEP_STRIKE_TRANSPORTS = ["Legion Drop Pod", "Anvillus Pattern Dreadclaw Drop Pod", "Legion Dreadnought Drop Pod"]


def stone_no_drop_pods(ctx):
    """The Stone Gauntlet: no voluntary Deep Strike - Drop Pod / Dreadclaw Dedicated Transports are hidden."""
    targets = {L2.T[n] for n in DEEP_STRIKE_TRANSPORTS}
    seen = set()
    for e in ctx.all_entries():
        for lk in e.iter("entryLink"):
            if lk.get("targetId") not in targets or id(lk) in seen:
                continue
            seen.add(id(lk))
            on = [cond(rite_id(STONE), "force", "atLeast", 1)]
            mods = [modifier("set", "hidden", "true", conds=on)]
            for c in lk.iter("constraint"):
                if c.get("type") == "max":
                    mods.append(modifier("set", c.get("id"), 0, conds=[cond(rite_id(STONE), "force", "atLeast", 1)]))
            add_mods(lk, mods)


def vigil_shield_limits(ctx):
    """Vigil Pattern Storm Shield may not be combined with other shields / a Refractor Field."""
    for n in ("Legion Praetor", "Legion Centurion"):
        e = ctx.unit(n)
        pid = e.get("id")
        add_mods(e, [modifier("add", "error", "A Vigil Pattern Storm Shield may not be combined with a Refractor Field, "
                                              "Combat Shield or Boarding Shield.",
                              conds=[cond(W("Vigil Pattern Storm Shield"), pid, "atLeast", 1, deep=False)],
                              groups=[any_of(*[cond(W(x), pid, "atLeast", 1, deep=False)
                                               for x in ("Refractor Field", "Combat Shield", "Boarding Shield")])])])


# ------------------------------------------------------------------ extend
def extend(ctx):
    ctx.legion_rules([LR, "Disciplined Fire", "Fortification Masters", "Blind to the Risk"])

    ctx.add_units(templars(), warders(), tarantulas(), *characters(), dorn())
    add_huscarls_to_praetor(ctx)
    ctx.finish()  # new retinues become shared entries before the Legion-wide changes below

    # Armoury
    add_armoury_items(ctx, [("Vigil Pattern Storm Shield", 25)], who=("praetor", "centurion"))
    character_variant(ctx.all_entries(), "Power Fist", "Solarite Power Gauntlet", 5, 30)
    add_teleportation(ctx)
    vigil_shield_limits(ctx)
    stone_no_drop_pods(ctx)

    # Rites of War
    fort = cond(gs.cat("Fortification"), "force", "atLeast", 1)
    ctx.add_rite(STONE, RULES[STONE], limit_fa=True, errors=[
        ("no unit may take Teleportation Transponders, Drop Pods or Dreadclaw Drop Pods.",
         [any_of(*[cond(L2.T[n], "force", "atLeast", 1) for n in DEEP_STRIKE_TRANSPORTS] +
                 [cond(W("Teleportation Transponders"), "force", "atLeast", 1)])]),
    ])
    ctx.add_rite(HAMMERFALL, RULES[HAMMERFALL], errors=[
        ("the army's Warlord must be equipped with Teleportation Transponders (no Independent Character in the "
         "Detachment has them).", [cond(IC_TT, "force", "lessThan", 1)]),
        ("the Detachment may not include a Fortification.", [fort]),
    ])
    ctx.add_rite(TEMPLAR_RITE, RULES[TEMPLAR_RITE], limit_fa=True, errors=[
        ("the army may not include a Fortification.", [fort]),
    ])
