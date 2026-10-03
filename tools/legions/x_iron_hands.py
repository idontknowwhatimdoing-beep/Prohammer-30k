"""X Legion - Iron Hands (Forces of the Legions)."""
import copy
from itertools import combinations

from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, upgrade, retinue_links, command_squad_for, named_character, primarch,
                            primarch_retinue, forbid_items, add_group, add_entry, legion_units, LOW, TRAITOR, LOYALIST)
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile
from legiones2 import (slot, take, pool, transports, add_mods, add_to, foc, rite_id, rite, walker_profile, TROOPS,
                       ELITES, FA, HQ, HS, model_swaps, model_pair_claws, pa_armoury, T)
from legiones_wargear import ARMY_RULES, WEAPONS

LEGION = "X - Iron Hands"
LR = "Legiones Astartes (Iron Hands)"

RULES = {
    LR: ("Models with this rule belong to the X Legion and use the Iron Hands Legion special rules: Wisdom of the "
         "Omnissiah, Inexorable Advance and More Machine than Man."),
    "Wisdom of the Omnissiah": (
        "A non-vehicle Iron Hands unit with at least one model within 6\" of a friendly model equipped with a Servo-Arm "
        "gains Counter-Attack and Feel No Pain (6+). These benefits last only while the unit remains within 6\" of an "
        "eligible model. Multiple Servo-Arms provide no additional benefit."),
    "Inexorable Advance": (
        "Iron Hands units may re-roll failed Morale and Pinning tests. However, Iron Hands units may never make a "
        "Sweeping Advance after winning a combat and may only Consolidate instead."),
    "More Machine than Man": (
        "Iron Hands Characters and Veteran Sergeants may purchase Bionics for 5 points. Any Iron Hands unit consisting "
        "wholly of Infantry, Jump Infantry, Bikes and/or Jetbikes may purchase Bionics for +3 points per model. Iron Hands "
        "models with Bionics successfully recover on a roll of 5+ rather than 6+."),
    # Armoury
    "Servo-Arm (Iron Hands Armoury)": (
        "Any Iron Hands model with access to the Space Marine Armoury may purchase a Servo-Arm for +30 points, even if the "
        "model is not normally permitted to select Techmarine equipment. A model equipped with a Jump Pack may not "
        "purchase a Servo-Arm."),
    "Dangerous Weaponry": (
        "Whenever an Iron Hands model may purchase a Flamer, it may instead purchase a Graviton Gun for +15 points. The "
        "Graviton Gun follows the normal Graviton rules."),
    "Rending (5+)": (
        "Follows the normal ProHammer rules for Rending, except that the effect is triggered on a natural To Wound roll of "
        "5 or 6 rather than only on a 6. Against Vehicles, Rending is still triggered only by a natural Armour Penetration "
        "roll of 6."),
    "Albian Power Gladius": (
        "Any Iron Hands Character with access to the Space Marine Armoury may purchase an Albian Power Gladius for +10 "
        "points. It is a weapon and does not count towards the Armoury points limit."),
    # Iron Father
    "Iron Father": (
        "Any Iron Hands Forge Lord Consul may be further upgraded to an Iron Father for +25 points. Wargear: Iron Halo, "
        "Bionics. Special rules: Rites of Battle. The Iron Father retains all rules, wargear and options of a normal Forge "
        "Lord Consul."),
    "Rites of Battle": ("The Iron Father and any Iron Hands unit he has joined may re-roll failed Morale tests. The second "
                        "result must be accepted."),
    # Rites of War
    "The Head of the Gorgon": (
        "EFFECTS - Ground of Choice: all Iron Hands Infantry units gain Stubborn while at least half of the unit's "
        "surviving models are within the Iron Hands deployment zone. Relics of War: all Iron Hands Vehicles in the "
        "Detachment receive Blessed Autosimulacra at no additional points cost. Scions of Iron: any Iron Hands Infantry "
        "unit of ten models or fewer which may normally select a Rhino as a Dedicated Transport may instead select a Land "
        "Raider Phobos or Land Raider Proteus as a Dedicated Transport at its normal points cost (all normal Transport "
        "Capacity restrictions apply). Armoured Encirclement: Iron Hands Vehicles with the Tank unit type gain Outflank if "
        "placed in Reserve; a Dedicated Transport carrying a unit may Outflank together with its passengers (they are "
        "treated as a single Reserve entry).\n"
        "LIMITATIONS - The Detachment may include no more than one Fast Attack choice. The Detachment may include no more "
        "than one Consul, excluding Forge Lords. The Detachment may not include an Allied Detachment drawn from another "
        "Space Marine Legion."),
    "Company of Bitter Iron": (
        "LOYALIST ONLY.\nEFFECTS - Company of Immortals: Medusan Immortal Squads may be selected as Troops choices and may "
        "fulfil compulsory Troops selections; at least one compulsory Troops choice in the Detachment must be a Medusan "
        "Immortal Squad. Immortal Hatred: all units in the Detachment with the Legiones Astartes (Iron Hands) rule gain "
        "Hatred against Traitor forces (any army or unit specifically designated as Traitor by the mission, campaign or "
        "army list). Bitter Duty: a Medusan Immortal Squad gains Fearless while the majority of its surviving models are "
        "within the enemy deployment zone. No Death Without Purpose: whenever a Medusan Immortal Squad is completely "
        "destroyed while the majority of its models were within the enemy deployment zone immediately before its "
        "destruction, every friendly Iron Hands unit within 6\" may immediately re-roll any failed Morale or Pinning test "
        "it is required to make as a result of that destruction.\n"
        "LIMITATIONS - Only a Loyalist Iron Hands Detachment. The army may not include an Allied Detachment. The army may "
        "not include Ferrus Manus."),
    "Selected as Troops (Company of Bitter Iron)": (
        "With the Company of Bitter Iron Rite of War, Medusan Immortal Squads may be selected as Troops without the 0-1 "
        "limit and may fulfil compulsory Troops selections."),
    # Units
    "Gorgon Field": (
        "If one or more models in the unit successfully pass an Invulnerable Save against shooting from an enemy unit, "
        "resolve all of that enemy unit's attacks before applying this rule. The attacking unit must then take an "
        "Initiative test; if failed, it is affected by the normal ProHammer Blind rule until the end of its next turn. A "
        "unit may only be required to take one Gorgon Field test per phase."),
    "Morlocks of the Avernii": (
        "Ferrus Manus or Gabriel Santar may select one Morlock Terminator Squad as a retinue. If selected in this manner, "
        "the Morlocks do not occupy a separate Elites choice."),
    "Paired Close-Combat Arms (Venerable Forge Lord)": (
        "If the Venerable Forge Lord retains both Dreadnought Close Combat Weapons, it gains +1 Attack. This bonus is not "
        "included in its printed profile (the builder raises the profile's Attacks to 3 while both are kept)."),
    "Old & Wise": (
        "If the mission requires a dice roll to determine which player takes the first turn, an Iron Hands army containing "
        "a Venerable Forge Lord may re-roll that roll once. The second result must be accepted."),
    "Hard to Kill": (
        "Whenever the Venerable Forge Lord suffers a Glancing or Penetrating Hit and a result is rolled on the Vehicle "
        "Damage table, the Iron Hands player may force the opponent to re-roll that Vehicle Damage result. The second "
        "result must be accepted."),
    "Auto-Repair Simulacra": (
        "Whenever a Vehicle Damage result would destroy the Venerable Forge Lord, roll a D6 after resolving Hard to Kill. "
        "On a 6, the Venerable Forge Lord is not destroyed; replace the result with Crew Shaken."),
    # Characters
    "Fury of the Survivors": (
        "Meduson and any Iron Hands unit he has joined have Counter-Attack. In addition, when attacking a Traitor unit, "
        "Meduson and his unit may re-roll To Hit rolls of 1 in both the Shooting and Assault phases."),
    "Command Retinue (Meduson)": ("Meduson may select one Legion Command Squad as his retinue. The squad does not "
                                  "occupy a separate Force Organisation slot."),
    "Command Retinue (Autek Mor)": ("Autek Mor may select one Legion Terminator Command Squad as his retinue. The squad "
                                    "does not occupy a separate Force Organisation slot."),
    "Battlesmith (Autek Mor)": (
        "Autek Mor uses the normal Battlesmith rule from the Legiones Astartes Army List. His Servo-Arm provides the "
        "normal +1 bonus to his repair roll, so he normally repairs a damaged Vehicle on a 4+."),
    "Castrmen Orth": (
        "Castrmen Orth may be purchased as an upgrade for one Iron Hands Vehicle (Tank) in the army for +50 points. Orth "
        "and his Vehicle together occupy the Vehicle's normal Force Organisation selection and one HQ selection. Orth may "
        "not command a Walker, a Vehicle without a Ballistic Skill characteristic, or a Vehicle already commanded by "
        "another named character."),
    "Spearhead Centurion": ("The Vehicle commanded by Castrmen Orth has Ballistic Skill 5. This replaces its normal "
                            "Ballistic Skill."),
    "Tank Hunters (Castrmen Orth)": (
        "Orth's Vehicle has the normal ProHammer Tank Hunters special rule. If the Vehicle is destroyed, Castrmen Orth is "
        "also considered slain for all Victory Point and mission purposes. Orth is not represented by a separate model "
        "and may not leave his Vehicle during the battle."),
    "Master of the Morlocks": (
        "Santar may select one Morlock Terminator Squad as his retinue. The Morlocks do not occupy a separate Elites "
        "choice. Santar and the Morlocks count as a single HQ selection."),
    # Ferrus Manus
    "Living Metal Hands": (
        "Ferrus Manus may choose to fight with his Living Metal Hands instead of Forgebreaker. Attacks made with his Living "
        "Metal Hands count as Power Weapon attacks and are resolved at Strength 8."),
    "The Gorgon": "Ferrus Manus has Feel No Pain (5+).",
    "Master of the Forge": (
        "Ferrus Manus has Battlesmith and succeeds on a roll of 3+. He may use this ability to repair friendly Vehicles, "
        "Dreadnoughts and Battle-Automata as appropriate."),
    "Forged for War": (
        "After both armies have been selected but before deployment, nominate one friendly Iron Hands Vehicle or "
        "Dreadnought which is not a Lord of War. That model gains +1 Structure Point for the duration of the battle. If "
        "the selected model does not normally use Structure Points, determine its normal Structure Point value using the "
        "standard ProHammer rules before applying this bonus."),
    "Primarch Retinue (Ferrus Manus)": (
        "Ferrus Manus may select a Legion Honour Guard Squad, a Legion Terminator Command Squad or a Morlock Terminator "
        "Squad as his Primarch Retinue. It does not occupy an additional Force Organisation selection and otherwise "
        "follows the normal Primarch Retinue rules."),
}

WEAPONS_ = {
    "Albian Power Gladius": ("-", "User", "-", "Rending (5+)"),
    "Master-crafted Bolter": ('24"', "4", "5", "Rapid Fire, Master-crafted"),
    "Iron Aegis Power Claws": ("-", "User", "-", "Power Weapon, Rending, Master-crafted (paired; bonus Attack included)"),
    "Forgebreaker": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Concussive, Master-crafted, "
                                     "Armourbane"),
    "Living Metal Hands": ("-", "8", "-", "Power Weapon"),
}
WEAPON_RULES_ = {
    "Albian Power Gladius": ["Rending (5+)", "Albian Power Gladius"],
    "Master-crafted Bolter": ["Master-Crafted"],
    "Iron Aegis Power Claws": ["Rending", "Master-Crafted"],
    "Forgebreaker": ["Master-Crafted", "Concussive", "Unwieldy", "Armourbane"],
    "Living Metal Hands": ["Living Metal Hands"],
}
WARGEAR_ = {
    "Mechadendrites": (
        "Any Iron Hands Independent Character or Sergeant may purchase Mechadendrites for +15 points. Once during each "
        "phase, the bearer may re-roll one failed Armour Save. This cannot be used to re-roll an Invulnerable Save or "
        "Cover Save. The second result must be accepted."),
    "Splinter Bolts": (
        "Any Iron Hands Infantry unit equipped with Bolters may purchase Splinter Bolts for +5 points per unit. When firing "
        "Splinter Bolts, wounds caused by the unit's Bolters ignore Feel No Pain. Bolters include Bolters, Combi-Bolters, "
        "Twin-linked Bolters and the Bolter component of Combi-Weapons. Splinter Bolts may not be combined with Special "
        "Issue Ammunition or another ammunition upgrade. A Legion Tactical Squad may not use Fury of the Legion during a "
        "Shooting phase in which it fires Splinter Bolts."),
    "Blessed Autosimulacra": (
        "Any Iron Hands Vehicle may purchase Blessed Autosimulacra for +10 points. At the beginning of the Iron Hands "
        "Movement phase, select one Weapon Destroyed or Immobilised result currently affecting the Vehicle and roll a D6; "
        "on a 6 that result is repaired. A repaired weapon may fire normally and a repaired Immobilised Vehicle may move "
        "normally. Only one repair attempt per Vehicle per turn. Destroyed Vehicles cannot repair themselves."),
    "Iron Halo (Iron Hands)": (
        "Grants a 4+ Invulnerable Save. Part of this model's own wargear; not counted towards the army's normal limit of "
        "one Iron Halo."),
    "Gorgon-pattern Terminator Armour": (
        "Follows all normal rules for Terminator Armour: 2+ Armour Save and 5+ Invulnerable Save, and grants Relentless, "
        "Bulky and Deep Strike. Models wearing Gorgon-pattern Terminator Armour may not Pursue.",
        ["Relentless", "Bulky", "Deep Strike"]),
    "The Iron Aegis": (
        "A unique suit of Terminator Armour: grants Santar a 2+ Armour Save and 4+ Invulnerable Save and follows all other "
        "normal rules for Terminator Armour. It incorporates Bionics and a matched pair of master-crafted power claws "
        "(Power Weapons with Rending; the +1 Attack for two close-combat weapons is already included in Santar's profile; "
        "the claws count as a single Master-crafted weapon for re-rolling one failed To Hit roll).", ["Bionics"]),
    "Medusan Carapace": (
        "Counts as Primarch Armour. Incorporates a Twin-linked Meltagun, a Twin-linked Plasma Gun, a Heavy Flamer, a "
        "Cortex Controller and a Nuncio Vox. Ferrus Manus may fire up to two of the weapons incorporated into the Medusan "
        "Carapace during each Shooting phase. The Cortex Controller and Nuncio Vox use their normal rules.",
        ["Primarch Armour"]),
}


def register():
    ARMY_RULES.update(RULES)
    T.setdefault("Land Raider Achilles", uid("transport", "Land Raider Achilles"))
    register_data(weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_)
    # Bionics in a WARGEAR core-rule list must be a rule name -> give it one
    ARMY_RULES.setdefault("Bionics", "When the model loses its final Wound, leave it on its side. At the start of its "
                                     "controlling player's next turn roll a D6: on a 6 (5+ for Iron Hands, More Machine "
                                     "than Man) it returns with 1 Wound, otherwise remove it.")


# ------------------------------------------------------------------ local helpers
def unique_entries(entries):
    seen, out = set(), []
    for e in entries:
        if id(e) not in seen:
            seen.add(id(e))
            out.append(e)
    return out


def everything(ctx):
    return unique_entries(ctx.all_entries())


def walk_own(e):
    """Descendants of e, not entering nested model/unit entries."""
    for c in e:
        if c.tag == "selectionEntry" and c.get("type") in ("model", "unit"):
            continue
        yield c
        yield from walk_own(c)


def model_entries(root):
    yield root
    for x in root.iter("selectionEntry"):
        if x is not root and x.get("type") in ("model", "unit"):
            yield x


def own_profiles(e):
    ps = e.find("profiles")
    return list(ps) if ps is not None else []


def unit_type_of(p):
    for c in p.iter("characteristic"):
        if c.get("name") == "Unit Type":
            return c.text or ""
    return ""


def is_character(e):
    return any(p.get("typeName") == "Unit" and "Character" in unit_type_of(p) for p in own_profiles(e))


def find_group(e, name):
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == name:
            return g
    return None


def find_entry(e, name):
    for x in e.iter("selectionEntry"):
        if x.get("name") == name:
            return x
    return None


def link_cost(lk):
    cs = lk.find("costs")
    if cs is not None and len(cs):
        return float(cs[0].get("value"))
    return 0


def set_link_cost(lk, value):
    cs = lk.find("costs")
    if cs is None:
        from bsx import costs
        lk.append(costs(value))
    else:
        cs[0].set("value", str(value))


def prof_mods(p, mods):
    m = p.find("modifiers")
    if m is None:
        p.insert(0, wrap("modifiers", list(mods)))
    else:
        for x in mods:
            m.append(x)


def hide_unless(eid, conds_hide):
    return [modifier("set", "hidden", "true", groups=[any_of(*conds_hide)]),
            modifier("set", uid(eid, "max"), 0, groups=[any_of(*copy.deepcopy(conds_hide))])]


ARMOURY_GROUPS = ("Space Marine Armoury (max 50 pts)", "Space Marine Armoury (max 100 pts)")


def armoury_targets(ctx):
    """[(root, model entry, group to add Armoury items to)] for every model with access to the Space Marine Armoury.
    Praetor/Centurion: the 'Additional Wargear' group of their 100-pt Armoury; others: the 50-pt Armoury group."""
    out, seen = [], set()
    for r in everything(ctx):
        for m in model_entries(r):
            for g in walk_own(m):
                if g.tag != "selectionEntryGroup" or g.get("name") not in ARMOURY_GROUPS or id(g) in seen:
                    continue
                seen.add(id(g))
                tgt = g
                if g.get("name") == "Space Marine Armoury (max 100 pts)":
                    tgt = find_group(g, "Additional Wargear")
                out.append((r, m, tgt))
    return out


def add_link(g, key, name, pts, hide=None):
    lid = uid("link", g.get("id"), "ih", key, name)
    mods = hide_unless(lid, hide) if hide else None
    add_to(g, "entryLinks", [link(lid, W(name), name, cost=pts or None, mods=mods,
                                  constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])])
    return lid


def copy_link_variant(lk, new_name, cost):
    """A link to new_name with the same constraints/hide modifiers as the base link lk."""
    nid = uid(lk.get("id"), "variant", new_name)
    cons, remap = [], {}
    for c in lk.findall("constraints/constraint"):
        c2 = copy.deepcopy(c)
        remap[c.get("id")] = uid(c.get("id"), new_name)
        c2.set("id", remap[c.get("id")])
        cons.append(c2)
    mods = []
    for m in lk.findall("modifiers/modifier"):
        m2 = copy.deepcopy(m)
        if m2.get("field") in remap:
            m2.set("field", remap[m2.get("field")])
        if m2.get("field") in remap.values() or m2.get("field") == "hidden":
            mods.append(m2)
    return link(nid, W(new_name), new_name, cost=int(cost) or None, mods=mods, constraints=cons)


def add_variant_everywhere(entries, base, new, cost):
    """Dangerous Weaponry: wherever `base` can be selected, also offer `new` for `cost` points (unless `new` is
    already offered in that group). Squad-level limits counting `base` also count `new`."""
    base_id = W(base)
    done = set()
    n = 0
    for r in entries:
        parents = {c: p for p in r.iter() for c in p}
        for g in list(r.iter("selectionEntryGroup")):
            links = g.find("entryLinks")
            if links is None:
                continue
            existing = {x.get("targetId") for x in links}
            if W(new) in existing:
                continue
            for lk in list(links):
                if lk.get("targetId") != base_id or id(lk) in done:
                    continue
                done.add(id(lk))
                nl = copy_link_variant(lk, new, cost)
                if g.get("defaultSelectionEntryId") is not None:
                    nl.set("sortIndex", str(int(lk.get("sortIndex") or 1) + 100))
                links.append(nl)
                n += 1
        for m in list(r.iter("modifier")):
            reps = m.findall("repeats/repeat")
            if any(rp.get("childId") == base_id for rp in reps):
                parent = parents.get(m)
                if parent is None:
                    continue
                m2 = copy.deepcopy(m)
                for rp in m2.iter("repeat"):
                    if rp.get("childId") == base_id:
                        rp.set("childId", W(new))
                parent.append(m2)
    return n


def consul_limit_group(exclude=()):
    """True when the Detachment contains more than one Centurion upgraded to a Consul (excluding `exclude`)."""
    ids = [L.consul_id(c) for c in L.CONSULS if c not in exclude]
    singles = [cond(i, "force", "atLeast", 2) for i in ids]
    pairs = [all_of(cond(a, "force", "atLeast", 1), cond(b, "force", "atLeast", 1)) for a, b in combinations(ids, 2)]
    return el("conditionGroup", {"type": "or"}, [wrap("conditions", singles), wrap("conditionGroups", pairs)])


def model(u, name, cost, mn, mx, utype, stats, kit, groups=(), rules_=()):
    mid = uid("model", u, name)
    return mid, entry(mid, name, typ="model", cost=cost,
                      constraints=[constraint(uid(mid, "min"), "min", mn), constraint(uid(mid, "max"), "max", mx)],
                      profiles=[unit_profile(u, name, utype, *stats)], links=[gear(mid, k) for k in kit],
                      groups=list(groups), infolinks=rules_links(list(rules_), key=mid))


# ------------------------------------------------------------------ units
IMMORTALS = uid("unit", "Medusan Immortal Squad")
LAND_RAIDERS = ["Land Raider Phobos", "Land Raider Proteus", "Land Raider Achilles"]
GORGONS = uid("unit", "Gorgon Terminator Squad")
MORLOCKS = uid("unit", "Morlock Terminator Squad")
VFL = uid("unit", "Venerable Forge Lord")


def immortals():
    u = IMMORTALS
    kit = ["Power Armour", "Boarding Shield"]
    stats = (4, 4, 4, 4, 1, 4, 1, 9, "3+/5+")
    imm_id, imm = model(u, "Medusan Immortal", 27, 4, 19, "Infantry", stats, kit + ["Bolter"])
    sid = uid("model", u, "Immortal Sergeant")
    _, sgt = model(u, "Immortal Sergeant", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 2, 9, "3+/5+"), kit,
                   groups=[pa_armoury(sid, u, 20, slots=["Bolter"], skip=("Combat Shield", "Refractor Field"))])
    spec, _ = pool(u, "Special Weapons (1 per 5 models, replace Bolter)", u,
                   [("Flamer", 5), ("Meltagun", 10), ("Plasma Gun", 15), ("Graviton Gun", 15)], 0, every=5)
    on = [rite("Company of Bitter Iron")]
    fmax = uid(uid(u, "force-max"))
    e = entry(u, "Medusan Immortal Squad", typ="unit", cost=150 - 4 * 27, cats=[foc(TROOPS, "Troops", u)],
              constraints=[force_limit(u, 1)],
              mods=[modifier("increment", uid(u, "force-max"), 99, conds=on),
                    modifier("add", "category", gs.CAT_LINE, conds=on)],
              infolinks=rules_links([LR, "Stubborn", "Selected as Troops (Company of Bitter Iron)"], key=u),
              entries=[sgt, imm, per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                       per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
              groups=[spec, L.one_each(u, "Squad Equipment (different models)", [("Legion Vexilla", 10),
                                                                                   ("Nuncio Vox", 10)]),
                      transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                        "Anvillus Pattern Dreadclaw Drop Pod"] + LAND_RAIDERS, max_models=10)])
    del fmax
    return e


GORGON_RANGED = [("Foeblaster Boltgun", 0), ("Combi-Flamer", 10), ("Combi-Volkite Charger", 10),
                 ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15)]


def terminator_unit(key, name, model_name, leader_name, per, base_cost, stats, leader_stats, cc, heavy, pair_cost,
                    rules_, root, cat=ELITES, limit=False):
    u = uid("unit", key)
    kit = ["Gorgon-pattern Terminator Armour", "Bionics", "Storm Bolter", "Power Weapon"]
    tid, terms = model(u, model_name, per, 4, 9, "Infantry", stats, kit)
    lid = uid("model", u, leader_name)
    _, leader = model(u, leader_name, 0, 1, 1, "Infantry (Character)", leader_stats,
                      ["Gorgon-pattern Terminator Armour", "Bionics", "Storm Bolter", "Thunder Hammer",
                       "Iron Halo (Iron Hands)"],
                      groups=[take(lid, f"{leader_name} Wargear", [("Grenade Harness", 10), ("Mechadendrites", 15)])])
    heavy_grp, _ = pool(u, f"Up to two {model_name}s: replace Storm Bolter", u, heavy, 2)
    groups = [heavy_grp]
    minus_ranged = [W(n) for n, _ in heavy]
    if pair_cost is not None:
        pid, pair = model_pair_claws(u, "Pair of Lightning Claws (replaces Storm Bolter and Power Weapon)", u, [tid],
                                     pair_cost)
        groups.insert(0, model_swaps(u, f"{model_name}s: replace Storm Bolter (any number)", u, [tid], GORGON_RANGED,
                                     minus=minus_ranged, entries=[pair]))
        groups.insert(1, model_swaps(u, f"{model_name}s: replace Power Weapon (any number)", u, [tid], cc,
                                     minus=[pid]))
    else:
        groups.insert(0, model_swaps(u, f"{model_name}s: replace Storm Bolter (any number)", u, [tid], GORGON_RANGED,
                                     minus=minus_ranged))
        groups.insert(1, model_swaps(u, f"{model_name}s: replace Power Weapon (any number)", u, [tid], cc))
    groups.append(transports(u, u, LAND_RAIDERS + ["Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                             orbital=False))
    cons = [force_limit(u, 1)] if (limit and root) else []
    return entry(u, name, typ="unit", cost=base_cost - 4 * per, cats=[foc(cat, "Elites", u)] if root else [],
                 constraints=cons,
                 infolinks=rules_links([LR, "Fearless", "Gorgon Field"] + list(rules_) + ([] if root else ["Retinue"]),
                                       key=u),
                 entries=[leader, terms], groups=groups)


def gorgons():
    return terminator_unit("Gorgon Terminator Squad", "Gorgon Terminator Squad", "Gorgon Terminator", "Gorgon Sergeant",
                           45, 250, (4, 4, 4, 4, 1, 3, 2, 9, "2+/5+"), (5, 4, 4, 4, 1, 3, 3, 9, "2+/4+"),
                           [("Power Fist", 5), ("Lightning Claw", 5), ("Chainfist", 10)],
                           [("Heavy Flamer", 10), ("Plasma Blaster", 15), ("Graviton Gun", 15)], 10, [], True)


def morlocks(key="Morlock Terminator Squad", root=True):
    return terminator_unit(key, "Morlock Terminator Squad", "Morlock", "Morlock Captain", 50, 275,
                           (5, 4, 4, 4, 1, 3, 2, 9, "2+/5+"), (5, 4, 4, 4, 1, 3, 3, 10, "2+/4+"),
                           [("Power Fist", 5), ("Lightning Claw", 5), ("Chainfist", 10), ("Thunder Hammer", 10)],
                           [("Heavy Flamer", 10), ("Plasma Blaster", 15), ("Plasma Cannon", 20)], None,
                           ["Morlocks of the Avernii"], root, limit=True)


VFL_ARM = [("Twin-linked Heavy Bolter", 0), ("Multi-Melta", 0), ("Twin-linked Autocannon", 10),
           ("Twin-linked Missile Launcher", 15), ("Plasma Cannon", 10), ("Volkite Culverin", 10), ("Assault Cannon", 15),
           ("Twin-linked Lascannon", 25)]
VFL_BUILT_IN = [("Heavy Flamer", 10), ("Meltagun", 15), ("Graviton Gun", 15)]


def venerable_forge_lord():
    u = VFL
    arms, ccws = [], []
    for i in (1, 2):
        cid = uid(u, f"arm{i}-ccw")
        ccws.append(cid)
        ccw = entry(cid, "Dreadnought Close Combat Weapon", links=[gear(cid, "Dreadnought Close Combat Weapon")],
                    groups=[slot(cid, "Built-in weapon", "Twin-linked Bolter", VFL_BUILT_IN)])
        arms.append(slot(u, f"Weapon Arm {i} (replace Dreadnought Close Combat Weapon)", None, VFL_ARM,
                         default_is_entry=ccw))
    prof = walker_profile(u, "Venerable Forge Lord", 5, 5, 6, 12, 12, 10, 4, 2)
    prof.insert(0, wrap("modifiers", [modifier("set", gs.char_id("Walker", "A"), 3,
                                               groups=[all_of(cond(ccws[0], u, "atLeast", 1),
                                                              cond(ccws[1], u, "atLeast", 1))])]))
    return entry(u, "Venerable Forge Lord", typ="unit", cost=155, cats=[foc(ELITES, "Elites", u)],
                 constraints=[force_limit(u, 1)], profiles=[prof],
                 infolinks=rules_links([LR, "Paired Close-Combat Arms (Venerable Forge Lord)", "Old & Wise", "Hard to Kill", "Auto-Repair Simulacra"],
                                       key=u),
                 links=[gear(u, "Smoke Launchers"), gear(u, "Searchlight")],
                 groups=arms + [take(u, "Vehicle Upgrades", [("Extra Armour", 5)])])


# ------------------------------------------------------------------ characters
MEDUSON = uid("unit", "Shadrak Meduson")
AUTEK = uid("unit", "Autek Mor")
SANTAR = uid("unit", "Gabriel Santar")
FERRUS = uid("unit", "Ferrus Manus, the Gorgon")
ORTH = uid("ih", "Castrmen Orth")


def characters():
    out = []
    out.append(named_character(
        LR, "Shadrak Meduson", 165, (5, 5, 4, 5, 2, 4, 3, 10, "3+/4+"),
        ["Power Armour", "Iron Halo (Iron Hands)", "Master-crafted Bolter", "Power Weapon", "Bionics", "Mechadendrites",
         "Frag Grenades"],
        ["Fury of the Survivors", "Command Retinue (Meduson)"], loyalist=True,
        retinue=retinue_links("meduson", [command_squad_for("meduson", MEDUSON)]),
        extra_groups=[take(MEDUSON, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]))
    out.append(named_character(
        LR, "Autek Mor", 205, (6, 5, 4, 5, 3, 5, 4, 10, "2+/4+"),
        ["Cataphractii Terminator Armour", "Relic Blade", "Volkite Charger", "Servo-Arm", "Bionics"],
        ["Battlesmith", "Battlesmith (Autek Mor)", "Furious Charge", "Command Retinue (Autek Mor)"],
        retinue=retinue_links("autekmor", [L2.terminator_command_squad("autekmor")])))
    out.append(named_character(
        LR, "Gabriel Santar", 220, (6, 5, 4, 5, 3, 4, 4, 10, "2+/4+"),
        ["The Iron Aegis", "Iron Aegis Power Claws", "Nuncio Vox", "Mechadendrites", "Servo-Arm"],
        ["Master of the Morlocks"], min_points=1500, loyalist=True,
        retinue=retinue_links("santar", [morlocks("santar-morlocks", root=False)])))
    return out


def orth_entry():
    return entry(ORTH, "Castrmen Orth (+50, commands this Vehicle)", cost=50,
                 constraints=[constraint(uid(ORTH, "roster"), "max", 1, scope="roster", deep=True)],
                 infolinks=rules_links(["Castrmen Orth", "Spearhead Centurion", "Tank Hunters",
                                        "Tank Hunters (Castrmen Orth)"], key=ORTH))


def ferrus():
    return primarch(LR, "Ferrus Manus, the Gorgon", 505, (7, 7, 7, 7, 6, 5, 4, 10, "1+"),
                    ["Medusan Carapace", "Forgebreaker", "Living Metal Hands", "Frag Grenades", "Twin-linked Meltagun",
                     "Twin-linked Plasma Gun", "Heavy Flamer", "Cortex Controller", "Nuncio Vox"],
                    ["Primarch Armour", "The Gorgon", "Feel No Pain", "Master of the Forge", "Battlesmith",
                     "Forged for War", "Primarch Retinue (Ferrus Manus)"],
                    retinue=primarch_retinue("ferrus", extra=[morlocks("ferrus-morlocks", root=False)]),
                    profile_name="Ferrus Manus", loyalist=True)


# ------------------------------------------------------------------ Legion-wide changes
SKIP_CHAR = {MEDUSON, AUTEK, SANTAR, FERRUS}


def more_machine_than_man(ctx):
    """Bionics: 5 points for Characters (and Veteran Sergeants), +3 per model for whole units."""
    n_char = n_unit = 0
    whole = {r.get("id") for r in everything(ctx) if unit_bionics_ok(r)}
    for r in everything(ctx):
        if r.get("id") in SKIP_CHAR or r.get("name") in ("Legion", "Allegiance", "Rite of War"):
            continue
        for m in model_entries(r):
            if not is_character(m):
                continue
            if m is not r and r.get("id") in whole:
                # the unit-wide +3 option covers the sergeant: no separate Bionics in his Armoury
                parents = {c: p for p in m.iter() for c in p}
                for x in list(walk_own(m)):
                    if x.tag == "entryLink" and x.get("targetId") == W("Bionics"):
                        parents[x].remove(x)
                continue
            own = m.find("entryLinks")
            if own is not None and any(x.get("targetId") == W("Bionics") for x in own):
                continue  # fixed Bionics
            found = False
            for x in walk_own(m):
                if x.tag == "entryLink" and x.get("targetId") == W("Bionics"):
                    set_link_cost(x, 5)
                    found = True
            if not found:
                add_group(m, take(uid(m.get("id"), "ih"), "More Machine than Man", [("Bionics", 5)]))
            n_char += 1
        # whole units
        if r.get("id") not in whole:
            continue
        u = r.get("id")
        add_entry(r, per_model(u + "ih", "Bionics (entire unit, More Machine than Man)", 3, u, ["Bionics"]))
        n_unit += 1
    return n_char, n_unit


def unit_bionics_ok(r):
    """Multi-model unit made wholly of Infantry, Jump Infantry, Bikes and/or Jetbikes (unit-wide Bionics, +3/model)."""
    if r.get("type") != "unit" or r.get("id") in SKIP_CHAR:
        return False
    if any(p.get("typeName") == "Unit" for p in own_profiles(r)):
        return False  # single-model characters (Praetor, Centurion, named characters)
    types = [(p.get("typeName"), unit_type_of(p)) for p in r.iter("profile")]
    unit_types = [ut for tn, ut in types if tn == "Unit"]
    if not unit_types or any(tn in ("Vehicle", "Walker") for tn, _ in types):
        return False
    ok = ("Infantry", "Jump Infantry", "Bike", "Jetbike")
    if not all(ut.replace(" (Character)", "") in ok for ut in unit_types):
        return False
    if r.get("id") in (GORGONS, MORLOCKS) or r.get("name") == "Morlock Terminator Squad":
        return False  # every model already has Bionics
    return True


BOLTERS = ["Bolter", "Combi-Bolter", "Twin-linked Bolter", "Combi-Flamer", "Combi-Grenade Launcher", "Combi-Meltagun",
           "Combi-Plasma Gun", "Combi-Volkite Charger", "Combi-Weapon", "Master-crafted Bolter"]


def splinter_bolts(ctx):
    ids = {W(b) for b in BOLTERS if b in WEAPONS}
    n = 0
    for r in everything(ctx):
        if r.get("type") != "unit" or r.get("id") == FERRUS:
            continue
        types = [(p.get("typeName"), unit_type_of(p)) for p in r.iter("profile")]
        uts = [ut for tn, ut in types if tn == "Unit"]
        if not uts or any(tn in ("Vehicle", "Walker") for tn, _ in types):
            continue
        if not all(ut.startswith("Infantry") for ut in uts):
            continue
        if not any(lk.get("targetId") in ids for lk in r.iter("entryLink")):
            continue
        u = r.get("id")
        eid = uid("ih-splinter", u)
        sia = [has(W("Special Issue Ammunition"), u)]
        add_entry(r, entry(eid, "Splinter Bolts (entire unit)", cost=5, mods=hide_unless(eid, sia),
                           constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                           links=[gear(eid, "Splinter Bolts")]))
        add_mods(r, [modifier("add", "error", "Splinter Bolts may not be combined with Special Issue Ammunition.",
                              conds=[has(eid, u), has(W("Special Issue Ammunition"), u)])])
        n += 1
    return n


def armoury(ctx):
    targets = armoury_targets(ctx)
    forge = L.consul_id("Forge Lord")
    done = set()
    for r, m, g in targets:
        ru = r.get("id")
        hide = [has(W("Jump Pack"), ru)]
        if r.get("name") == "Legion Centurion":
            hide.append(has(forge, ru))
        add_link(g, "servo", "Servo-Arm", 30, hide=hide)
        if id(m) not in done:  # a weapon: outside the Armoury points cap
            done.add(id(m))
            add_group(m, take(uid(m.get("id"), "ih-gladius"), "Iron Hands Weaponry", [("Albian Power Gladius", 10)]))
        name = m.get("name") or ""
        if r.get("name") in ("Legion Praetor", "Legion Centurion") or "Sergeant" in name:
            add_link(g, "mecha", "Mechadendrites", 15)
    # a Servo-Arm and a Jump Pack never together
    for r in unique_entries([t[0] for t in targets]):
        ru = r.get("id")
        add_mods(r, [modifier("add", "error", "A model equipped with a Jump Pack may not have a Servo-Arm.",
                              groups=[all_of(has(W("Servo-Arm"), ru), has(W("Jump Pack"), ru))])])
    # Dangerous Weaponry: Graviton Gun wherever a Flamer may be purchased
    add_variant_everywhere(everything(ctx), "Flamer", "Graviton Gun", 15)
    return len(targets)


def vehicles(ctx):
    """Blessed Autosimulacra on every Vehicle (free with The Head of the Gorgon); Castrmen Orth on every Tank."""
    gorgon = [rite("The Head of the Gorgon")]
    n = 0
    for r in everything(ctx):
        if r.get("id") == FERRUS:
            continue
        orth_here = False
        for e in model_entries(r):
            vp = [p for p in own_profiles(e) if p.get("typeName") in ("Vehicle", "Walker")]
            if not vp:
                continue
            eid = uid("ih-autosim", e.get("id"))
            add_entry(e, entry(eid, "Blessed Autosimulacra", cost=10,
                               mods=[modifier("set", PTS, 0, conds=copy.deepcopy(gorgon)),
                                     modifier("set", "name", "Blessed Autosimulacra (free: The Head of the Gorgon)",
                                              conds=copy.deepcopy(gorgon))],
                               constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                               links=[gear(eid, "Blessed Autosimulacra")]))
            n += 1
            tank = [p for p in vp if p.get("typeName") == "Vehicle" and "Tank" in unit_type_of(p)]
            if tank:
                lid = uid("link", e.get("id"), "ih-orth")
                add_to(e, "entryLinks", [link(lid, ORTH, "Castrmen Orth (+50, commands this Vehicle)",
                                              constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])])
                for p in tank:
                    prof_mods(p, [modifier("set", gs.char_id("Vehicle", "BS"), 5, conds=[has(ORTH, e.get("id"))])])
                orth_here = True
        if orth_here and r.get("type") == "unit":
            add_mods(r, [modifier("add", "category", HQ, conds=[has(ORTH, r.get("id"))]),
                         modifier("add", "category", gs.CAT_COMMANDER, conds=[has(ORTH, r.get("id"))])])
    return n


def iron_father(ctx):
    cen = ctx.unit("Legion Centurion")
    fid = uid("ih", "Iron Father")
    forbid_items(cen, ["Iron Halo", "Bionics"], [has(fid, cen.get("id"))])
    forge = None
    for e in cen.iter("selectionEntry"):
        if e.get("id") == L.consul_id("Forge Lord"):
            forge = e
    add_entry(forge, entry(fid, "Iron Father", cost=25, constraints=[constraint(uid(fid, "max"), "max", 1, auto=True)],
                           infolinks=rules_links(["Iron Father", "Rites of Battle"], key=fid),
                           links=[gear(fid, "Iron Halo (Iron Hands)"), gear(fid, "Bionics")]))
    add_mods(cen, [modifier("set", "name", "Legion Iron Father", conds=[has(fid, cen.get("id"))])])


def scions_of_iron(ctx):
    """The Head of the Gorgon: Infantry units of up to ten models that may take a Rhino may take a Land Raider."""
    rhino = T["Legion Rhino Armoured Carrier"]
    n = 0
    for r in everything(ctx):
        g = find_group(r, "Dedicated Transport")
        if g is None or r.get("type") != "unit":
            continue
        links = g.find("entryLinks")
        if links is None or not any(x.get("targetId") == rhino for x in links):
            continue
        types = [unit_type_of(p) for p in r.iter("profile") if p.get("typeName") == "Unit"]
        if not types or not all(t.startswith("Infantry") for t in types):
            continue
        u = r.get("id")
        normal = {x.get("targetId") for x in links if x.find("modifiers") is None}
        for name in ("Land Raider Phobos", "Land Raider Proteus"):
            if T[name] in normal:
                continue
            lid = uid("link", g.get("id"), "ih-scions", name)
            off = lambda: any_of(cond(rite_id("The Head of the Gorgon"), "force", "lessThan", 1),
                                 cond("model", u, "greaterThan", 10))
            links.append(link(lid, T[name], f"{name} (Scions of Iron)",
                              mods=[modifier("set", "hidden", "true", groups=[off()]),
                                    modifier("set", uid(lid, "max"), 0, groups=[off()])],
                              constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
        n += 1
    return n


def rites(ctx):
    rites_e = ctx.unit("Rite of War")
    hg = ctx.add_rite("The Head of the Gorgon", RULES["The Head of the Gorgon"], limit_fa=True)
    add_mods(rites_e, [modifier("add", "error", "The Head of the Gorgon: the Detachment may include no more than one "
                                                "Consul, excluding Forge Lords.",
                                conds=[cond(hg, "self", "atLeast", 1)], groups=[consul_limit_group(["Forge Lord"])])])
    ctx.add_rite("Company of Bitter Iron", RULES["Company of Bitter Iron"], errors=[
        ("only a Loyalist Iron Hands Detachment may use this Rite.", [cond(TRAITOR, "roster", "atLeast", 1)]),
        ("the army may not include Ferrus Manus.", [cond(FERRUS, "roster", "atLeast", 1)]),
        ("at least one compulsory Troops choice must be a Medusan Immortal Squad.",
         [cond(IMMORTALS, "force", "lessThan", 1)]),
    ])


# ------------------------------------------------------------------ extend
def extend(ctx):
    ctx.legion_rules([LR, "Wisdom of the Omnissiah", "Inexorable Advance", "More Machine than Man",
                      "Servo-Arm (Iron Hands Armoury)", "Dangerous Weaponry"])
    iron_father(ctx)
    ctx.add_shared(orth_entry(), L2.land_raider("Land Raider Achilles"))
    ctx.add_units(immortals(), gorgons(), morlocks(), venerable_forge_lord(), *characters(), ferrus())
    ctx.finish()  # new retinues become shared entries before the Legion-wide changes below

    armoury(ctx)
    more_machine_than_man(ctx)
    splinter_bolts(ctx)
    vehicles(ctx)
    scions_of_iron(ctx)
    rites(ctx)
    for e in everything(ctx):
        L2.dedupe_kit(e)
