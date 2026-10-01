"""XIX Legion - Raven Guard (Forces of the Legions)."""
from itertools import combinations

from legions.common import *  # noqa: F401,F403
from legions.common import (PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry,
                            link, group, category_link, gs, L, L2, W, has, lacks, TDA, has_tda, gear, per_model,
                            rules_links, unit_profile, slot, take, pool, transports, add_mods, add_to, foc, rite,
                            rite_id, RETINUE_SHARED, TROOPS, ELITES, FA, HQ, HS, model_swaps, model_takes, pa_armoury,
                            tda_armoury, register_data, unique, force_limit, allegiance_only, option, upgrade,
                            named_character, primarch, primarch_retinue, retinue_links, command_squad_for,
                            add_weapon_variant, add_armoury_items, TRAITOR, LOYALIST)

LEGION = "XIX - Raven Guard"
LR = "Legiones Astartes (Raven Guard)"

RULES = {
    LR: ("Models with this rule belong to the XIX Legion and use the Raven Guard Legion special rules: Surgical Strike, "
         "Rapid Reaction, Shadow Masters and Limited Vehicles."),
    "Surgical Strike": ("Whenever a Raven Guard unit deploys using Deep Strike, the Raven Guard player may re-roll the "
                        "Scatter die and any dice rolled for scatter distance. The entire result must be re-rolled and "
                        "the second result must be accepted."),
    "Rapid Reaction": ("At the beginning of each Raven Guard turn, if at least one friendly Legion Reconnaissance Squad or "
                       "Mor Deythan Squad has a surviving model on the battlefield and is not Falling Back, add +1 to all "
                       "Raven Guard Reserve rolls made during that turn. This bonus is not cumulative."),
    "Shadow Masters": ("Legion Reconnaissance Squads selected in a Raven Guard Detachment lose the Support Squad special "
                       "rule and may therefore fulfil compulsory Troops selections normally. Legion Reconnaissance Squads "
                       "and Independent Characters may buy Sniper Rifles for 2 points (instead of 5 points or any other "
                       "price otherwise applicable)."),
    "Limited Vehicles": ("A Raven Guard Detachment may never include more Heavy Support selections than Fast Attack "
                         "selections. Dedicated Transports are ignored when determining this restriction."),
    # armoury
    "Raven's Talons": ("Count as a pair of Rending Weapons: the bearer receives the normal +1 Attack for fighting with "
                       "two close-combat weapons. Any model in a Raven Guard Legion Veteran Squad equipped with a Bolt "
                       "Pistol and Chainsword may replace both with Raven's Talons for +7 points; a Raven Guard Character "
                       "already equipped with a Pair of Lightning Claws may upgrade them to Raven's Talons for +5 points. "
                       "Other units only where their entry permits."),
    "Shroud Bombs": ("Count as Defensive Grenades. An enemy unit attempting to charge a unit equipped with Shroud Bombs "
                     "must first pass a Leadership test; if failed, the charge may not be attempted and the unit may not "
                     "declare another charge that turn. Vehicles, models with the Daemon special rule and units "
                     "containing a model with Night Vision are unaffected."),
    "Teleportation Transponders": ("The model or unit gains the Deep Strike special rule and may deploy using Deep Strike "
                                   "even if the mission would not normally permit it. An Independent Character intending "
                                   "to Deep Strike as part of another unit must purchase Teleportation Transponders "
                                   "separately."),
    # units
    "Fatal Strike": ("Once per battle, at the beginning of the Raven Guard Shooting phase, nominate one enemy unit within "
                     "18\" and line of sight of the Mor Deythan Squad. Until the end of that Shooting phase, models in the "
                     "squad may re-roll To Hit rolls of 1 and To Wound rolls of 1 against it (against Vehicles, re-roll "
                     "Armour Penetration rolls of 1 instead of To Wound rolls)."),
    "Swooping Killers": ("During an Assault phase in which the Dark Furies charge, models in the squad may re-roll To Hit "
                         "rolls of 1 until the end of that Assault phase."),
    "Dark Fury Command Squad": ("A Dark Fury Assault Squad may be selected as the retinue of a Raven Guard Praetor "
                                "equipped with a Jump Pack. It then does not occupy a Fast Attack choice; the Praetor and "
                                "the squad count as a single HQ selection."),
    "Terran Veterans": ("Deliverers do not benefit from the Infiltrate ability if it is granted by another Raven Guard "
                        "rule or Rite of War. They may, however, always deploy using Teleportation Transponders if these "
                        "have been purchased normally."),
    "Rending (close combat only)": "The model's close-combat attacks have the Rending special rule.",
    "Unstable Creation": ("Raptors may never fulfil compulsory Troops selections and may not be joined by an Independent "
                          "Character other than Corax or Branne Nev."),
    # characters
    "Dangerous Weaponry": ("Kaedes Nex's special rule; no further text is given in Forces of the Legions (see the "
                           "questions file)."),
    "The Raven's Due": (
        "At the beginning of the battle, nominate one enemy Independent Character or unit-upgrade Character. Kaedes Nex "
        "may re-roll failed To Hit rolls against the nominated model in close combat. When Nex fires his Fulcrum Hand "
        "Cannons at a unit containing the nominated model, he may re-roll failed To Hit rolls. Unsaved Wounds caused by "
        "Nex's shooting may be allocated to the nominated model before other casualties, provided that model is within "
        "range and line of sight."),
    "Executioner's Instinct": ("If Kaedes Nex causes one or more unsaved Wounds upon his nominated target, that model's "
                               "unit must immediately take a Pinning test."),
    "Kaedes Nex": ("Kaedes Nex may replace the Sergeant of one Raven Guard Legion Destroyer Squad (the normal Sergeant is "
                   "removed). He remains part of the squad, is not an Independent Character and does not occupy a "
                   "separate Force Organisation choice. No Independent Character may join Kaedes Nex's squad."),
    "Master of Descent": ("If Alvarex Maun begins the battle in Reserve embarked aboard a Drop Pod, Dreadclaw or Flyer "
                          "Transport, Maun and that Transport arrive automatically during the first Raven Guard turn. No "
                          "Reserve roll is required."),
    "Command Squad (Alvarex Maun)": ("Alvarex Maun may be accompanied by a Legion Command Squad. Maun and the Command "
                                     "Squad count as a single HQ selection."),
    "Agapito Nev": ("Agapito Nev may replace the Dark Fury Strike Leader of one Dark Fury Assault Squad (the normal "
                    "Strike Leader is removed). He remains part of the squad and possesses all special rules belonging "
                    "to the Dark Fury Assault Squad."),
    "Commander of the Talons": ("An army containing Agapito Nev may include up to two Dark Fury Assault Squads rather "
                                "than the normal 0-1. Agapito's squad may also re-roll failed Morale tests caused by "
                                "shooting casualties."),
    "First Into the Fray": ("During an Assault phase in which Agapito and his squad charge, the squad may re-roll all "
                            "failed To Hit rolls during the first round of that close combat."),
    "Commander of the Survivors": (
        "If the army includes Branne Nev, one Raptor Squad may be selected without occupying an Elites choice. That unit "
        "still counts as an Elites unit for all other purposes and may not fulfil a compulsory selection. Branne Nev may "
        "join a Raptor Squad despite the restrictions of Unstable Creation."),
    "Hold Fast": "Branne Nev and any Raven Guard unit he has joined may re-roll failed Morale and Pinning tests.",
    "Nykona Sharrowkyn": ("Sharrowkyn may replace the Sergeant of one Raven Guard Legion Seeker Squad or Legion "
                          "Reconnaissance Squad (the normal Sergeant is removed). He remains part of the squad, is not an "
                          "Independent Character and does not occupy a separate Force Organisation choice."),
    "Ghost in the Dark": "While Sharrowkyn's unit is in cover, improve its Cover Save by 1, to a maximum of 3+.",
    "Perfect Ambusher": "When Sharrowkyn shoots at an enemy unit within 12\", he may re-roll failed To Hit rolls.",
    # Corax
    "The Shadowed Lord": "Corvus Corax has the Stealth and Hit & Run special rules.",
    "Sire of the Raven Guard": ("Friendly Raven Guard Infantry units with at least one model within 12\" of Corvus Corax "
                                "improve any Cover Save they receive by 1, to a maximum of 3+."),
    "Secret Deployment": (
        "Instead of deploying Corax normally, the Raven Guard player may secretly record one terrain feature outside the "
        "enemy deployment zone; Corax is held off the battlefield. At the beginning of any Raven Guard Movement phase from "
        "the second turn onwards, reveal it and place Corax wholly within or in contact with that terrain feature and "
        "more than 6\" from every enemy model; he may Move, Shoot and declare charges normally that turn. No Reserve roll "
        "is required. If he cannot be placed legally he may try again in a later Raven Guard turn. A Primarch Retinue is "
        "deployed normally and does not accompany him."),
    "Corax's Primarch Retinue": (
        "Corvus Corax may select a Legion Honour Guard Squad, Legion Terminator Command Squad, Dark Fury Assault Squad or "
        "Raptor Squad as his Primarch Retinue (no additional Force Organisation selection). Corax may join a Raptor "
        "Squad despite Unstable Creation."),
    "Patchwork Panoply": ("The Avenging Shadow: Corax has a 2+ Armour Save and a 4+ Invulnerable Save instead of the "
                          "normal protection of Primarch Armour. His armour still counts as Primarch Armour for all other "
                          "purposes."),
    "Ghost of Istvaan": ("The Avenging Shadow: Corax replaces the Stealth special rule granted by The Shadowed Lord with "
                         "Shrouded. He retains Hit & Run normally."),
    "Hater of Traitors": "The Avenging Shadow: Corax has Hatred (Traitor Legiones Astartes).",
    # Rites of War
    "Decapitation Strike": (
        "EFFECTS - For Whom the Bell Tolls: all Raven Guard units gain Preferred Enemy (Independent Characters); an enemy "
        "unit containing one or more Independent Characters counts as a Preferred Enemy until all of them have been slain "
        "or left the unit. Predatory Strike: once per battle, the Raven Guard player may re-roll a roll to determine "
        "deployment order, choice of deployment zone or which player takes the first turn (the entire result; the second "
        "must be accepted). Fury From Above: Raven Guard Legion Heavy Support Squads must select a Legion Drop Pod or "
        "Anvillus Dreadclaw Drop Pod as a Dedicated Transport at its normal cost (normal Transport Capacity and "
        "deployment restrictions apply).\nLIMITATIONS - No more than one Heavy Support choice. No more than one Centurion "
        "upgraded to a Consul. No Fortification. No Allied Detachment drawn from another Space Marine Legion."),
    "Liberation Force": (
        "EFFECTS - Freedom Fighters: once per battle, at the beginning of any Game Turn, every model in the Raven Guard "
        "Detachment and any allied Imperialis Militia Detachment gains Zealot until the end of that Game Turn. Slayers of "
        "Tyrants: if the mission awards Victory Points for slaying the enemy Warlord, the award is D3 times its normal "
        "value. Lead by Example: models of an allied Imperialis Militia Detachment gain Fearless while they have at least "
        "one model within 6\" of a friendly model with Legiones Astartes (Raven Guard). Liberators: an Allied Detachment "
        "drawn from the Imperialis Militia may be included without preventing the use of this Rite (all other Allied "
        "Detachment rules apply).\nLIMITATIONS - Loyalist Raven Guard Detachments only. No units with the Immobile or "
        "Slow and Purposeful special rules. No Fortification."),
}

WEAPONS = {
    "Raven's Talons": ("-", "User", "-", "Rending; a pair (+1 Attack for two close-combat weapons)"),
    "Fulcrum Hand Cannon": ('18"', "4", "4", "Pistol, Rending, Concussive"),
    "Tolaedus": ("-", "User", "-", "Power Weapon, Master-crafted"),
    "Sudden Blade": ("-", "User", "-", "Rending, Master-crafted"),
    "Corvidine Talons": ("-", "+1", "-", "Power Weapon, Shred, Rending; a matched pair (two close-combat weapons)"),
    "Wrath & Justice": ('12"', "6", "4", "Assault 2, Rending, Master-crafted"),
}
MULTI = {"Two Fulcrum Hand Cannons": {"Fulcrum Hand Cannon": WEAPONS["Fulcrum Hand Cannon"]}}
WEAPON_RULES = {
    "Raven's Talons": ["Raven's Talons", "Rending"],
    "Fulcrum Hand Cannon": ["Rending", "Concussive"],
    "Two Fulcrum Hand Cannons": ["Rending", "Concussive"],
    "Tolaedus": ["Master-Crafted"],
    "Sudden Blade": ["Rending", "Master-Crafted"],
    "Corvidine Talons": ["Shred", "Rending"],
    "Wrath & Justice": ["Rending", "Master-Crafted"],
}
WARGEAR = {
    "Infravisor": ("The bearer gains the Night Vision special rule and +1 Ballistic Skill (maximum BS6). When taking an "
                   "Initiative test caused by the Blind special rule, the bearer and any unit he has joined count as "
                   "Initiative 1.", ["Night Vision"]),
    "Shroud Bombs": (RULES["Shroud Bombs"], []),
    "Teleportation Transponders": (RULES["Teleportation Transponders"], ["Deep Strike"]),
    "Nightfall Pattern Strato-Vox": (
        "Counts as a Nuncio Vox. In addition, once during each Raven Guard turn, one friendly Raven Guard unit deploying "
        "by Deep Strike with its first model within 12\" of Maun may re-roll the dice rolled for scatter distance (the "
        "second result must be accepted).", []),
    "Sable Armour": ("Counts as Primarch Armour (1+ Armour Save, 4+ Invulnerable Save).", []),
    "Korvidine Pinions": ("Corvus Corax is Jump Infantry and follows all normal ProHammer rules for Jump Infantry. This "
                          "ability may never be lost, disabled or destroyed as the result of damage to wargear.", []),
}

# the Legion Consuls a Centurion can take (for 'no more than one Consul' limits)
CONSUL_IDS = [L.consul_id(c) for c in L.CONSULS]


def register():
    register_data(rules=RULES, weapons=WEAPONS, weapon_rules=WEAPON_RULES, wargear=WARGEAR, multi_profile=MULTI)
    # Shadow Masters: Recon Squads count as compulsory Troops like Tactical Squads (and stop counting under the same
    # Rites that replace the compulsory Troops)
    L2.NOT_LINE_UNDER["Legion Reconnaissance Squad"] = [r for r in L2.NOT_LINE_UNDER["Legion Tactical Squad"]
                                                        if r != "Legion Recon Company"]


# ------------------------------------------------------------------ local helpers
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


ARMOURY_GROUPS = ("Space Marine Armoury (max 50 pts)", "Space Marine Armoury (max 100 pts)")


def has_armoury(m):
    return any(g.tag == "selectionEntryGroup" and g.get("name") in ARMOURY_GROUPS for g in walk_own(m))


def child_model(unit, name):
    for e in unit.find("selectionEntries"):
        if e.get("name") == name:
            return e
    raise KeyError(name)


def replace_model(unit, model_name, new_entry):
    """new_entry replaces the (single) model_name: its min/max drop to 0 while new_entry is chosen."""
    m = child_model(unit, model_name)
    c = [has(new_entry.get("id"), unit.get("id"))]
    add_mods(m, [modifier("set", k.get("id"), 0, conds=c) for k in m.find("constraints")
                 if k.get("type") in ("min", "max") and k.get("scope") == "parent"])
    add_to(unit, "selectionEntries", [new_entry])


def swap_fixed(parent, old, new, cost, title=None):
    """'May replace its <old> with <new>' for a fixed wargear link: an option entry that removes the old link."""
    lk = next(x for x in parent.find("entryLinks") if x.get("targetId") == W(old))
    eid = uid("rg-swap", parent.get("id"), old, new)
    e = entry(eid, title or f"{new} (replaces {old})", cost=cost,
              constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)], links=[gear(eid, new)])
    c = [has(eid, parent.get("id"))]
    add_mods(lk, [modifier("set", k.get("id"), 0, conds=c) for k in lk.find("constraints")
                  if k.get("type") in ("min", "max")])
    add_to(parent, "selectionEntries", [e])
    return eid


def all_entries(ctx):
    """ctx.all_entries() without duplicates (retinues are both shared entries and in RETINUE_SHARED)."""
    seen, out = set(), []
    for e in ctx.all_entries():
        if id(e) not in seen:
            seen.add(id(e))
            out.append(e)
    return out


def set_link_cost(lk, value):
    cs = lk.find("costs")
    if cs is None:
        lk.append(wrap("costs", [el("cost", {"name": "pts", "typeId": PTS, "value": value})]))
    else:
        cs[0].set("value", str(value))


def ic_wargear(ctx, items):
    """Legion Armoury items for the Praetor/Centurion 'Additional Wargear' (counts towards the 100-pt cap).
    items: [(name, pts, forbid(unit_id) -> list of conditions / ('group', conditionGroup))]."""
    for n in ("Legion Praetor", "Legion Centurion"):
        u = ctx.unit(n)
        for g in u.iter("selectionEntryGroup"):
            if g.get("name") != "Additional Wargear":
                continue
            links = g.find("entryLinks")
            for name, pts, forbid in items:
                lid = uid("link", g.get("id"), "rg", name)
                links.append(link(lid, W(name), name, cost=pts, mods=L.forbid_mods(lid, forbid(u.get("id"))),
                                  constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))


def one_per_army(entries, name):
    """Several copies of the same named model (root unit + retinue copies): only one per army."""
    ids = [e.get("id") for e in entries]
    for e in entries:
        others = [cond(i, "roster", "atLeast", 1) for i in ids if i != e.get("id")]
        if others:
            add_mods(e, [modifier("add", "error", f"{name} may only be included once in an army.",
                                  groups=[any_of(*others)], conds=[cond(e.get("id"), "roster", "atLeast", 1)])])


def consul_limit_group(exclude=()):
    """True when the Detachment contains more than one Centurion upgraded to a Consul."""
    ids = [L.consul_id(c) for c in L.CONSULS if c not in exclude]
    singles = [cond(i, "force", "atLeast", 2) for i in ids]
    pairs = [all_of(cond(a, "force", "atLeast", 1), cond(b, "force", "atLeast", 1)) for a, b in combinations(ids, 2)]
    return el("conditionGroup", {"type": "or"}, [wrap("conditions", singles), wrap("conditionGroups", pairs)])


def cats_strip_limits(e):
    """Remove per-Detachment limits from a retinue copy."""
    cs = e.find("constraints")
    if cs is not None:
        for c in list(cs):
            if c.get("scope") == "force":
                cs.remove(c)


COMBIS = [("Combi-Flamer", 10), ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15), ("Combi-Volkite Charger", 10)]


# ------------------------------------------------------------------ units
def mor_deythan():
    name = "Mor Deythan Squad"
    u = uid("unit", name)
    mid, sid = uid("model", u, "Mor Deythan"), uid("model", u, "Mor Deythan Sergeant")
    kit = ["Power Armour", "Sniper Rifle", "Bolt Pistol", "Close Combat Weapon", "Frag Grenades"]
    sgt = entry(sid, "Mor Deythan Sergeant", typ="model",
                constraints=[constraint(uid(sid, "min"), "min", 1), constraint(uid(sid, "max"), "max", 1)],
                profiles=[unit_profile(u, "Mor Deythan Sergeant", "Infantry (Character)", 4, 5, 4, 4, 1, 4, 2, 9, "3+")],
                links=[gear(sid, k) for k in kit],
                groups=[slot(sid, "Replace Sniper Rifle", "Sniper Rifle", COMBIS),
                        pa_armoury(sid, u, 10, slots=["Bolt Pistol", "Close Combat Weapon"])])
    mds = entry(mid, "Mor Deythan", typ="model", cost=24,
                constraints=[constraint(uid(mid, "min"), "min", 4), constraint(uid(mid, "max"), "max", 9)],
                profiles=[unit_profile(u, "Mor Deythan", "Infantry", 4, 5, 4, 4, 1, 4, 1, 8, "3+")],
                links=[gear(mid, k) for k in kit])
    heavy_opts = [("Heavy Bolter", 15), ("Missile Launcher", 20)]
    heavy, _ = pool(u, "Heavy Weapons (1 per 5 models, replace Sniper Rifle)", u, heavy_opts, 0, every=5)
    swaps = model_swaps(u, "Mor Deythan: replace Sniper Rifle (any number)", u, [mid], COMBIS,
                        minus=[W(n) for n, _ in heavy_opts])
    return entry(u, name, typ="unit", cost=120 - 4 * 24, cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links([LR, "Infiltrate", "Move Through Cover", "Fatal Strike"], key=u),
                 entries=[sgt, mds, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          option(u, "Shroud Bombs (entire squad)", 20, item="Shroud Bombs")],
                 groups=[swaps, heavy])


AGAPITO_KEYS = []


def dark_fury(key="Dark Fury Assault Squad", root=True):
    name = "Dark Fury Assault Squad"
    u = uid("unit", key)
    fid, lid = uid("model", u, "Dark Fury"), uid("model", u, "Dark Fury Strike Leader")
    kit = ["Power Armour", "Jump Pack", "Bolt Pistol", "Raven's Talons", "Frag Grenades"]
    leader = entry(lid, "Dark Fury Strike Leader", typ="model",
                   constraints=[constraint(uid(lid, "min"), "min", 1), constraint(uid(lid, "max"), "max", 1)],
                   profiles=[unit_profile(u, "Dark Fury Strike Leader", "Jump Infantry (Character)",
                                          5, 4, 4, 4, 1, 5, 3, 9, "3+")],
                   links=[gear(lid, k) for k in kit], groups=[pa_armoury(lid, u, 10, slots=["Bolt Pistol"])])
    furies = entry(fid, "Dark Fury", typ="model", cost=34,
                   constraints=[constraint(uid(fid, "min"), "min", 4), constraint(uid(fid, "max"), "max", 9)],
                   profiles=[unit_profile(u, "Dark Fury", "Jump Infantry", 4, 4, 4, 4, 1, 4, 2, 9, "3+")],
                   links=[gear(fid, k) for k in kit])
    aid = uid("model", u, "Agapito Nev")
    AGAPITO_KEYS.append(aid)
    agapito = entry(aid, "Agapito Nev (replaces the Strike Leader)", typ="model", cost=140,
                    constraints=[constraint(uid(aid, "max"), "max", 1, auto=True), unique(aid)],
                    profiles=[unit_profile(u, "Agapito Nev", "Jump Infantry (Character)", 6, 5, 4, 4, 2, 5, 4, 10,
                                           "3+/5+")],
                    infolinks=rules_links(["Agapito Nev", "Commander of the Talons", "First Into the Fray"], key=aid),
                    links=[gear(aid, k) for k in ["Power Armour", "Refractor Field", "Jump Pack", "Bolter",
                                                  "Power Weapon", "Close Combat Weapon", "Frag Grenades"]])
    cats, cons, mods = [], [], []
    if root:
        cats = [foc(FA, "Fast Attack", u)]
        cons = [force_limit(u, 1)]
        # Commander of the Talons: up to two Dark Fury Assault Squads with Agapito Nev in the army
        mods = [modifier("increment", uid(u, "force-max"), 1,
                         groups=[any_of(*[cond(i, "roster", "atLeast", 1) for i in AGAPITO_ALL])])]
    e = entry(u, name, typ="unit", cost=170 - 4 * 34, cats=cats, constraints=cons, mods=mods,
              infolinks=rules_links([LR, "Swooping Killers", "Dark Fury Command Squad"], key=u),
              entries=[leader, furies, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                       per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])])
    replace_model(e, "Dark Fury Strike Leader", agapito)
    return e, agapito


# every copy of Agapito Nev (root squad, Praetor retinue, Corax retinue)
AGAPITO_ALL = [uid("model", uid("unit", k), "Agapito Nev") for k in ["Dark Fury Assault Squad", "praetor-darkfury",
                                                                      "corax-darkfury"]]


def deliverers():
    name = "Deliverer Terminator Squad"
    u = uid("unit", name)
    did, cid = uid("model", u, "Deliverer"), uid("model", u, "Deliverer Chieftain")
    kit = ["Cataphractii Terminator Armour", "Combi-Bolter", "Power Weapon"]
    cc = [("Power Fist", 10), ("Chainfist", 15), ("Raven's Talons", 10)]
    heavy_opts = [("Heavy Flamer", 10), ("Reaper Autocannon", 15), ("Multi-Melta", 20)]
    chief = entry(cid, "Deliverer Chieftain", typ="model",
                  constraints=[constraint(uid(cid, "min"), "min", 1), constraint(uid(cid, "max"), "max", 1)],
                  profiles=[unit_profile(u, "Deliverer Chieftain", "Infantry (Character)", 5, 4, 4, 4, 1, 4, 3, 9,
                                         "2+/4+")],
                  links=[gear(cid, k) for k in kit],
                  groups=[slot(cid, "Replace Power Weapon", "Power Weapon", cc),
                          slot(cid, "Replace Combi-bolter", "Combi-Bolter", COMBIS),
                          tda_armoury(cid)])
    dels = entry(did, "Deliverer", typ="model", cost=43,
                 constraints=[constraint(uid(did, "min"), "min", 4), constraint(uid(did, "max"), "max", 9)],
                 profiles=[unit_profile(u, "Deliverer", "Infantry", 5, 4, 4, 4, 1, 3, 2, 9, "2+/4+")],
                 links=[gear(did, k) for k in kit])
    heavy, _ = pool(u, "Heavy Weapons (1 per 5 models, replace Combi-bolter)", u, heavy_opts, 0, every=5)
    swaps = [model_swaps(u, "Deliverers: replace Power Weapon (any number)", u, [did], cc),
             model_swaps(u, "Deliverers: replace Combi-bolter (any number)", u, [did], COMBIS,
                         minus=[W(n) for n, _ in heavy_opts])]
    return entry(u, name, typ="unit", cost=215 - 4 * 43, cats=[foc(ELITES, "Elites", u)], constraints=[force_limit(u)],
                 infolinks=rules_links([LR, "Stubborn", "Terran Veterans"], key=u),
                 entries=[chief, dels, option(u, "Teleportation Transponders (entire squad)", 15,
                                              item="Teleportation Transponders")],
                 groups=[*swaps, heavy,
                         transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                                    orbital=False)])


BRANNE = uid("unit", "Branne Nev")


def raptors(key="Raptor Squad", root=True):
    name = "Raptor Squad"
    u = uid("unit", key)
    rid, aid = uid("model", u, "Raptor"), uid("model", u, "Raptor Alpha")
    kit = ["Power Armour", "Bolt Pistol", "Close Combat Weapon", "Frag Grenades"]
    alpha = entry(aid, "Raptor Alpha", typ="model",
                  constraints=[constraint(uid(aid, "min"), "min", 1), constraint(uid(aid, "max"), "max", 1)],
                  profiles=[unit_profile(u, "Raptor Alpha", "Infantry (Character)", 4, 4, 5, 4, 1, 5, 3, 9, "3+")],
                  links=[gear(aid, k) for k in kit],
                  groups=[pa_armoury(aid, u, 10, slots=["Bolt Pistol", "Close Combat Weapon"])])
    raps = entry(rid, "Raptor", typ="model", cost=32,
                 constraints=[constraint(uid(rid, "min"), "min", 4), constraint(uid(rid, "max"), "max", 9)],
                 profiles=[unit_profile(u, "Raptor", "Infantry", 4, 4, 5, 4, 1, 5, 2, 8, "3+")],
                 links=[gear(rid, k) for k in kit])
    pistols, _ = pool(u, "Pistols (1 per 5 models, replace Bolt Pistol)", u,
                      [("Hand Flamer", 5), ("Plasma Pistol", 15)], 0, every=5)
    ents = [alpha, raps, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
            per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])]
    cats, cons, mods = [], [], []
    if root:
        cats = [foc(ELITES, "Elites", u)]
        cons = [force_limit(u)]
        tog = uid(u, "survivors")
        no_branne = [cond(BRANNE, "roster", "lessThan", 1)]
        ents.append(entry(tog, "Commander of the Survivors (does not occupy an Elites choice)",
                          constraints=[constraint(uid(tog, "max"), "max", 1, auto=True),
                                       constraint(uid(tog, "roster"), "max", 1, scope="roster", deep=True)],
                          mods=[modifier("set", "hidden", "true", conds=no_branne),
                                modifier("set", uid(tog, "max"), 0, conds=no_branne)],
                          infolinks=rules_links(["Commander of the Survivors"], key=tog)))
        mods = [modifier("add", "category", gs.FOC_PLUS["Elites"], conds=[cond(tog, "self", "atLeast", 1)])]
    e = entry(u, name, typ="unit", cost=160 - 4 * 32, cats=cats, constraints=cons, mods=mods,
              infolinks=rules_links([LR, "Fleet", "Furious Charge", "Move Through Cover", "Rending (close combat only)",
                                     "Unstable Creation"], key=u),
              entries=ents, groups=[pistols])
    return allegiance_only(e, True)


def characters(ctx):
    out = []
    # Alvarex Maun
    m = uid("unit", "Alvarex Maun")
    out.append(named_character(LR, "Alvarex Maun", 140, (5, 5, 4, 4, 3, 4, 3, 9, "2+/5+"),
                               ["Artificer Armour", "Refractor Field", "Bolt Pistol", "Tolaedus",
                                "Nightfall Pattern Strato-Vox", "Frag Grenades"],
                               ["Master of Descent", "Command Squad (Alvarex Maun)"],
                               retinue=retinue_links("maun", [command_squad_for("maun", m)])))
    # Branne Nev (Command Squad per the general Master of the Legion rule - see questions)
    out.append(named_character(LR, "Branne Nev", 155, (6, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
                               ["Artificer Armour", "Refractor Field", "Bolter", "Bolt Pistol", "Power Weapon",
                                "Frag Grenades", "Krak Grenades"],
                               ["Commander of the Survivors", "Hold Fast"],
                               retinue=retinue_links("branne", [command_squad_for("branne", BRANNE)])))
    return out


def kaedes_nex(ctx):
    dest = ctx.unit("Legion Destroyer Squad")
    nid = uid("model", dest.get("id"), "Kaedes Nex")
    nex = entry(nid, "Kaedes Nex (replaces the Sergeant)", typ="model", cost=135,
                constraints=[constraint(uid(nid, "max"), "max", 1, auto=True), unique(nid)],
                profiles=[unit_profile(dest.get("id"), "Kaedes Nex", "Jump Infantry (Character)", 5, 5, 4, 4, 3, 4, 3, 9,
                                       "3+/5+")],
                infolinks=rules_links(["Kaedes Nex", "Dangerous Weaponry", "The Raven's Due", "Executioner's Instinct"],
                                      key=nid),
                links=[gear(nid, k) for k in ["Power Armour", "Refractor Field", "Two Fulcrum Hand Cannons",
                                              "Rending Weapon", "Jump Pack", "Frag Grenades", "Krak Grenades"]])
    replace_model(dest, "Legion Destroyer Sergeant", nex)


def sharrowkyn(ctx):
    copies = []
    for n, sgt in [("Legion Seeker Squad", "Legion Seeker Sergeant"),
                   ("Legion Reconnaissance Squad", "Legion Recon Sergeant")]:
        sq = ctx.unit(n)
        sid = uid("model", sq.get("id"), "Nykona Sharrowkyn")
        e = entry(sid, "Nykona Sharrowkyn (replaces the Sergeant)", typ="model", cost=125,
                  constraints=[constraint(uid(sid, "max"), "max", 1, auto=True), unique(sid)],
                  profiles=[unit_profile(sq.get("id"), "Nykona Sharrowkyn", "Infantry (Character)", 6, 5, 4, 4, 2, 5, 3,
                                         9, "2+/5+")],
                  infolinks=rules_links(["Nykona Sharrowkyn", "Infiltrate", "Move Through Cover", "Ghost in the Dark",
                                         "Perfect Ambusher"], key=sid),
                  links=[gear(sid, k) for k in ["Artificer Armour", "Refractor Field", "Bolt Pistol", "Sniper Rifle",
                                                "Sudden Blade", "Frag Grenades"]])
        replace_model(sq, sgt, e)
        copies.append(e)
    one_per_army(copies, "Nykona Sharrowkyn")


def corax():
    key = "Corvus Corax, the Raven-Lord"
    u = uid("unit", key)
    av = uid(u, "avenging-shadow")
    avenging = entry(av, "The Avenging Shadow (post-Istvaan variant)", cost=0,
                     constraints=[constraint(uid(av, "max"), "max", 1, auto=True)],
                     infolinks=rules_links(["Patchwork Panoply", "Ghost of Istvaan", "Shrouded", "Hater of Traitors",
                                            "Hatred"], key=av))
    ret = primarch_retinue("corax", extra=[dark_fury("corax-darkfury", root=False)[0],
                                           raptors("corax-raptors", root=False)])
    e = primarch(LR, key, 500, (8, 7, 6, 6, 6, 8, 6, 10, "1+/4+"),
                 ["Sable Armour", "Korvidine Pinions", "Corvidine Talons", "Wrath & Justice", "Frag Grenades"],
                 ["Primarch Armour", "The Shadowed Lord", "Stealth", "Hit & Run", "Surgical Strike",
                  "Sire of the Raven Guard", "Secret Deployment", "Corax's Primarch Retinue"],
                 retinue=ret, unit_type="Jump Infantry (Character)", loyalist=True, extra_entries=[avenging])
    # Avenging Shadow: 2+/4+ instead of Primarch Armour's 1+/4+
    for p in e.iter("profile"):
        p.insert(0, wrap("modifiers", [
            modifier("set", gs.char_id("Unit", "Sv"), "2+/4+", conds=[has(av, u)]),
            modifier("set", "name", "Corvus Corax, the Avenging Shadow", conds=[has(av, u)])]))
    return e


# ------------------------------------------------------------------ changes to existing units
def recon_changes(ctx):
    rec = ctx.unit("Legion Reconnaissance Squad")
    # Shadow Masters: no Support Squad, counts as compulsory Troops
    il = rec.find("infoLinks")
    for x in list(il):
        if x.get("name") == "Support Squad":
            il.remove(x)
    add_to(rec, "categoryLinks", [category_link(gs.CAT_LINE, "Compulsory Troops Eligible", key=rec.get("id") + "rg")])
    add_to(rec, "infoLinks", rules_links(["Shadow Masters"], key=rec.get("id") + "rg"))
    # Sniper Rifles for 2 points
    for lk in rec.iter("entryLink"):
        if lk.get("targetId") == W("Sniper Rifle") and lk.find("costs") is not None:
            set_link_cost(lk, 2)
    add_to(rec, "selectionEntries", [option(rec.get("id"), "Shroud Bombs (entire squad)", 20, item="Shroud Bombs")])


def veteran_changes(ctx):
    vet = ctx.unit("Legion Veteran Squad")
    u = vet.get("id")
    vid = uid("model", u, "Legion Veteran")
    sid = uid("model", u, "Legion Veteran Sergeant")
    add_to(vet, "selectionEntries", [option(u, "Shroud Bombs (entire squad)", 20, item="Shroud Bombs")])
    # Raven's Talons for the Veterans: shares the per-model limit of the Chainsword swaps
    for g in vet.iter("selectionEntryGroup"):
        if g.get("name") == "Legion Veterans: replace Chainsword (any number)":
            tid = uid(u, "rg-talons")
            mx = uid(tid, "max")
            add_to(g, "selectionEntries", [entry(
                tid, "Raven's Talons (replace Bolt Pistol and Chainsword)", cost=7,
                mods=L2._model_count_mods(mx, u, [vid]), constraints=[constraint(mx, "max", 0)],
                links=[gear(tid, "Raven's Talons")])])
    # ... and for the Sergeant (removes his Bolt Pistol)
    sgt = child_model(vet, "Legion Veteran Sergeant")
    tal = uid(sid, "rg-talons")
    for g in sgt.iter("selectionEntryGroup"):
        if g.get("name") == "Replace Chainsword":
            add_to(g, "selectionEntries", [entry(tal, "Raven's Talons (replace Bolt Pistol and Chainsword)", cost=7,
                                                 links=[gear(tal, "Raven's Talons")])])
    lk = next(x for x in sgt.find("entryLinks") if x.get("targetId") == W("Bolt Pistol"))
    add_mods(lk, [modifier("set", k.get("id"), 0, conds=[has(tal, sid)]) for k in lk.find("constraints")])


def praetor_dark_fury(ctx):
    pr = ctx.unit("Legion Praetor")
    df, _ag = dark_fury("praetor-darkfury", root=False)
    RETINUE_SHARED.append(df)
    for g in pr.iter("selectionEntryGroup"):
        if g.get("name") == "Retinue (no Force Organisation slot)":
            lid = uid("link", g.get("id"), df.get("id"))
            add_to(g, "entryLinks", [link(lid, df.get("id"), "Dark Fury Assault Squad (Praetor with Jump Pack)",
                                          mods=[modifier("set", "hidden", "true",
                                                         conds=[lacks(W("Jump Pack"), pr.get("id"))])])])
            break
    # error if chosen without a Jump Pack
    add_mods(pr, [modifier("add", "error", "A Dark Fury Assault Squad may only be the retinue of a Praetor with a Jump "
                                           "Pack.", conds=[cond(df.get("id"), pr.get("id"), "atLeast", 1),
                                                           lacks(W("Jump Pack"), pr.get("id"))])])


def armoury(ctx):
    roots = all_entries(ctx)
    no_tda = lambda u: L.has_tda(u)  # noqa: E731
    # Fulcrum Hand Cannon: any IC or Sergeant with the Space Marine Armoury may replace a Bolt Pistol
    seen = set()
    for r in roots:
        for m in model_entries(r):
            if id(m) in seen or not has_armoury(m):
                continue
            seen.add(id(m))
            pistol_groups = [g for g in walk_own(m) if g.tag == "selectionEntryGroup"
                             and g.get("name") == "Replace Bolt Pistol"]
            for g in pistol_groups:
                add_to(g, "entryLinks", [link(uid("link", g.get("id"), "rg", "Fulcrum Hand Cannon"),
                                              W("Fulcrum Hand Cannon"), "Fulcrum Hand Cannon", cost=10)])
            if not pistol_groups:
                el_ = m.find("entryLinks")
                if el_ is not None and any(x.get("targetId") == W("Bolt Pistol") for x in el_):
                    swap_fixed(m, "Bolt Pistol", "Fulcrum Hand Cannon", 10)
    # Moritat: his second Bolt Pistol too
    for e in ctx.unit("Legion Centurion").iter("selectionEntry"):
        if e.get("id") == L.consul_id("Moritat"):
            swap_fixed(e, "Bolt Pistol", "Fulcrum Hand Cannon", 10,
                       title="Fulcrum Hand Cannon (replaces the Moritat's second Bolt Pistol)")
    # Raven's Talons: Characters with a Pair of Lightning Claws may upgrade them for +5
    add_weapon_variant(roots, "Pair of Lightning Claws", "Raven's Talons", 5)
    # Infravisor: Independent Characters and Sergeants with the Armoury
    add_armoury_items(ctx, [("Infravisor", 10)])
    # Independent Characters: Shroud Bombs, Cameleoline, Teleportation Transponders, Sniper Rifle (Shadow Masters)
    ic_wargear(ctx, [
        ("Shroud Bombs", 10, lambda u: []),
        ("Cameleoline", 10, lambda u: no_tda(u)),
        ("Teleportation Transponders", 10, lambda u: [("group", L.no_tda(u))]),
        ("Sniper Rifle", 2, lambda u: []),
    ])
    # Teleportation Transponders for units entirely in Terminator Armour
    for n in ("Legion Terminator Squad",):
        e = ctx.unit(n)
        add_to(e, "selectionEntries", [option(e.get("id"), "Teleportation Transponders (entire squad)", 15,
                                              item="Teleportation Transponders")])
    for e in ctx.retinues("Legion Terminator Command Squad"):
        add_to(e, "selectionEntries", [option(e.get("id"), "Teleportation Transponders (entire squad)", 15,
                                              item="Teleportation Transponders")])


def rites(ctx):
    rites_e = ctx.unit("Rite of War")
    # Decapitation Strike
    dec = ctx.add_rite("Decapitation Strike", RULES["Decapitation Strike"], limit_hs=True)
    add_mods(rites_e, [modifier("add", "error", "Decapitation Strike: the Detachment may include no more than one "
                                                "Centurion upgraded to a Consul.",
                                conds=[cond(dec, "force", "atLeast", 1)], groups=[consul_limit_group()])])
    hss = ctx.unit("Legion Heavy Support Squad")
    u = hss.get("id")
    pods = [L.TRANSPORTS["Legion Drop Pod"], L.TRANSPORTS["Anvillus Pattern Dreadclaw Drop Pod"]]
    for g in hss.iter("selectionEntryGroup"):
        if g.get("name") == "Dedicated Transport":
            for n in ["Legion Drop Pod", "Anvillus Pattern Dreadclaw Drop Pod"]:
                lid = uid("link", g.get("id"), "rg-decap", n)
                add_to(g, "entryLinks", [link(lid, L.TRANSPORTS[n], f"{n} (Decapitation Strike)",
                                              mods=[modifier("set", "hidden", "true",
                                                             conds=[cond(dec, "force", "lessThan", 1)])])])
    add_mods(hss, [modifier("add", "error", "Decapitation Strike (Fury From Above): Legion Heavy Support Squads must "
                                            "select a Legion Drop Pod or Anvillus Dreadclaw Drop Pod as a Dedicated "
                                            "Transport.",
                            conds=[cond(dec, "force", "atLeast", 1)] + [cond(p, u, "lessThan", 1) for p in pods])])
    # Liberation Force
    lib = ctx.add_rite("Liberation Force", RULES["Liberation Force"],
                       errors=[("only a Loyalist Raven Guard Detachment may select this Rite of War.",
                                [cond(TRAITOR, "roster", "atLeast", 1)])])
    bad = {L.rule_ref("Immobile")[0], L.rule_ref("Slow and Purposeful")[0]}
    for e in all_entries(ctx):
        if e.get("type") != "unit":
            continue
        il = e.find("infoLinks")
        if il is not None and any(x.get("targetId") in bad for x in il):
            add_mods(e, [modifier("add", "error", "Liberation Force: the Detachment may not include units with the "
                                                  "Immobile or Slow and Purposeful special rules.",
                                  conds=[cond(lib, "force", "atLeast", 1)])])


def limited_vehicles(ctx):
    """Limited Vehicles: no more Heavy Support than Fast Attack selections (HS > FA for some n: HS >= n+1, FA <= n)."""
    hs, fa = gs.cat("Heavy Support"), gs.cat("Fast Attack")
    txt = "Limited Vehicles: a Raven Guard Detachment may not include more Heavy Support than Fast Attack selections."
    add_mods(ctx.unit("Legion"), [modifier("add", "error", txt, conds=[cond(hs, "force", "atLeast", n + 1),
                                                                      cond(fa, "force", "lessThan", n + 1)])
                                  for n in range(8)])


def extend(ctx):
    ctx.legion_rules([LR, "Surgical Strike", "Rapid Reaction", "Shadow Masters", "Limited Vehicles"])
    limited_vehicles(ctx)
    recon_changes(ctx)
    veteran_changes(ctx)
    kaedes_nex(ctx)
    sharrowkyn(ctx)
    praetor_dark_fury(ctx)
    df, agapito = dark_fury()
    ctx.add_units(mor_deythan(), df, deliverers(), raptors(), *characters(ctx), corax())
    # every copy of Agapito Nev: only one per army
    ags = [x for r in all_entries(ctx) for x in r.iter("selectionEntry") if x.get("id") in AGAPITO_ALL]
    one_per_army(ags, "Agapito Nev")
    rites(ctx)
    armoury(ctx)
