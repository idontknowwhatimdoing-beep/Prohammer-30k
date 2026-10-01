"""Legiones Astartes - slice 2: retinues, Damocles, Elites, Fast Attack, Heavy Support, Rites of War.

Built on the helpers in legiones.py. Every restriction from the army book that the builder can
check is written as a constraint/modifier so New Recruit enforces it.
"""
from bsx import (PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, hide_if, constraint, rule,
                 profile, info_link, category_link, entry, link, group)
import gamesystem as gs
import legiones as L
from legiones import W, has, lacks, TDA, has_tda, no_tda, gear, per_model, rules_links, unit_profile
from legiones_wargear import ARMOURY, TDA_SGT, RITES

TROOPS, ELITES, FA, HS, HQ = (gs.cat(n) for n in ["Troops", "Elites", "Fast Attack", "Heavy Support", "HQ"])


def foc(cat_id, name, key, primary=True):
    return category_link(cat_id, name, primary=primary, key=key)


# ------------------------------------------------------------------ rites
RITE_ENTRY = uid("cfg", "Rite of War")


def rite_id(name):
    return uid("rite", name)


def rite(name):
    return cond(rite_id(name), "force", "atLeast", 1)


def any_rite(*names):
    return any_of(*[rite(n) for n in names])


# which rite lets which unit be Troops (and makes it count for the compulsory Troops)
TROOP_RITES = {
    "Legion Veteran Squad": ["Pride of the Legion", "Primarch's Chosen"],
    "Legion Terminator Squad": ["Pride of the Legion", "Primarch's Chosen"],
    "Legion Destroyer Squad": ["Legion Destroyer Company"],
    "Legion Dreadnought": ["Fury of the Ancients"],
    "Legion Contemptor Dreadnought": ["Fury of the Ancients"],
    "Legion Sky Hunter Jetbike Squadron": ["Sky Hunter Phalanx"],
}
# which rites force the compulsory Troops to be something else: unit -> rites under which it stops counting
NOT_LINE_UNDER = {
    "Legion Tactical Squad": ["Primarch's Chosen", "Pride of the Legion", "Legion Assault Company", "Legion Breacher Company",
                              "Legion Recon Company", "Legion Destroyer Company", "Fury of the Ancients",
                              "Sky Hunter Phalanx"],
    "Legion Assault Squad": ["Primarch's Chosen", "Pride of the Legion", "Legion Breacher Company", "Legion Recon Company",
                             "Legion Destroyer Company", "Fury of the Ancients", "Sky Hunter Phalanx",
                             "Legion Tactical Company"],
    "Legion Breacher Siege Squad": ["Primarch's Chosen", "Pride of the Legion", "Legion Assault Company", "Legion Recon Company",
                                    "Legion Destroyer Company", "Fury of the Ancients", "Sky Hunter Phalanx",
                                    "Legion Tactical Company"],
}


NORMAL_ROLE = {"Legion Veteran Squad": ELITES, "Legion Terminator Squad": ELITES, "Legion Destroyer Squad": ELITES,
               "Legion Dreadnought": ELITES, "Legion Contemptor Dreadnought": ELITES,
               "Legion Sky Hunter Jetbike Squadron": FA}


def troop_role_mods(name):
    mods = []
    if name in TROOP_RITES:
        rs = TROOP_RITES[name]
        mods += [modifier("set-primary", "category", TROOPS, groups=[any_rite(*rs)]),
                 modifier("remove", "category", NORMAL_ROLE[name], groups=[any_rite(*rs)]),
                 modifier("add", "category", gs.CAT_LINE, groups=[any_rite(*rs)])]
    if name in NOT_LINE_UNDER:
        mods.append(modifier("remove", "category", gs.CAT_LINE, groups=[any_rite(*NOT_LINE_UNDER[name])]))
    if name == "Legion Reconnaissance Squad":
        mods.append(modifier("add", "category", gs.CAT_LINE, conds=[rite("Legion Recon Company")]))
    return mods


def add_mods(e, mods):
    """Insert modifiers into an existing entry element."""
    m = e.find("modifiers")
    if m is None:
        m = el("modifiers")
        e.insert(0, m)
    for x in mods:
        m.append(x)


def add_to(e, tag, children):
    c = e.find(tag)
    if c is None:
        c = el(tag)
        # keep costs as the last child
        costs = e.find("costs")
        if costs is not None:
            e.insert(list(e).index(costs), c)
        else:
            e.append(c)
    for x in children:
        c.append(x)


# ----------------------------------------------------------- generic parts
def walker_profile(key, name, ws, bs, s, f, si, r, i, a, ut="Vehicle (Walker)"):
    chars = [(gs.char_id("Walker", c), c, v) for c, v in zip(gs.WALKER_CHARS, [ut, ws, bs, s, f, si, r, i, a])]
    return profile(uid("prof-walker", key, name), name, gs.WALKER, "Walker", chars)


def slot(key, title, default, options, zero_if=None, show_if=None, default_is_entry=None):
    """Exactly-one replacement choice. options: [(name, pts)] linking shared items, or
    [(entry_element, None)] for inline entries. zero_if/show_if: conditions that empty the slot."""
    gid = uid("slot", key, title)
    links, entries = [], []
    if default_is_entry is not None:
        entries.append(default_is_entry)
        dl = default_is_entry.get("id")
    else:
        dl = uid("link", gid, default)
        links.append(link(dl, W(default), default))
    # no per-option limits: the group's own min/max of 1 already allows exactly one choice, and per-option
    # limits would wrongly count the same weapon chosen in a different slot of the same model
    for name, pts in options:
        if not isinstance(name, str):
            entries.append(name)
            continue
        lid = uid("link", gid, name)
        links.append(link(lid, W(name), name, cost=pts or None))
    mn, mx = uid(gid, "min"), uid(gid, "max")
    mods = []
    if zero_if:
        grp = any_of(*zero_if)
        mods += [modifier("set", mn, 0, groups=[grp]), modifier("set", mx, 0, groups=[any_of(*zero_if)]),
                 modifier("set", "hidden", "true", groups=[any_of(*zero_if)])]
    if show_if:
        # empty unless one of show_if is true
        none = all_of(*[_negate(c) for c in show_if])
        mods += [modifier("set", mn, 0, groups=[none]), modifier("set", mx, 0, groups=[all_of(*[_negate(c) for c in show_if])]),
                 modifier("set", "hidden", "true", groups=[all_of(*[_negate(c) for c in show_if])])]
    return group(gid, title, default=dl, links=links, entries=entries, mods=mods,
                 constraints=[constraint(mn, "min", 1, auto=True), constraint(mx, "max", 1, auto=True)])


def _negate(c):
    """Negate a simple 'atLeast 1' / 'equalTo 0' selection condition."""
    n = el("condition", dict(c.attrib))
    t = c.get("type")
    n.set("type", {"atLeast": "lessThan", "lessThan": "atLeast", "equalTo": "notEqualTo",
                   "notEqualTo": "equalTo", "greaterThan": "atMost", "atMost": "greaterThan"}[t])
    return n


def take(key, title, items, max_total=None, hide=None):
    """Optional extras: items [(name, pts)] or [(name, pts, max)]."""
    gid = uid("grp", key, title)
    links = []
    for it in items:
        name, pts = it[0], it[1]
        mx = it[2] if len(it) > 2 else 1
        lid = uid("link", gid, name)
        links.append(link(lid, W(name), name, cost=pts or None,
                          constraints=[constraint(uid(lid, "max"), "max", mx, auto=True)]))
    cons = [constraint(uid(gid, "max"), "max", max_total, auto=True)] if max_total else []
    mods = []
    if hide:
        mods = [modifier("set", "hidden", "true", groups=[any_of(*hide)])]
        if max_total:
            mods.append(modifier("set", uid(gid, "max"), 0, groups=[any_of(*hide)]))
    return group(gid, title, links=links, constraints=cons, mods=mods)


def pool(key, title, unit_id, options, base_max, every=None, per_child=None, extra_mods=None, at_least=None):
    """Squad-level pool of swaps, e.g. 'for every five models, one may ...'."""
    gid = uid("grp", key, title)
    mx = uid(gid, "max")
    mods = list(extra_mods or [])
    if every:
        mods.append(modifier("increment", mx, 1, repeats=[repeat(per_child or "model", unit_id, every)]))
    if at_least:
        for n, c in at_least:
            mods.append(modifier("increment", mx, 1, conds=[cond("model", unit_id, "atLeast", n)]))
    links = [link(uid("link", gid, n), W(n), n, cost=p or None) for n, p in options]
    return group(gid, title, mods=mods, links=links, constraints=[constraint(mx, "max", base_max, auto=True)]), mx


def _model_count_mods(max_id, unit_id, model_ids, minus=()):
    mods = [modifier("increment", max_id, 1, repeats=[repeat(m, unit_id, 1)]) for m in model_ids]
    mods += [modifier("decrement", max_id, 1, repeats=[repeat(m, unit_id, 1)]) for m in minus]
    return mods


def model_swaps(key, title, unit_id, model_ids, options, minus=(), entries=()):
    """'Any model may replace its X with ...' as one squad-level block.
    Every option can be taken several times; together they are limited to one per model in model_ids,
    minus the models whose X is already used up by the selections in `minus` (entry ids)."""
    gid = uid("grp", key, title)
    mx = uid(gid, "max")
    links = []
    for opt in options:
        n, p = opt[0], opt[1]
        lid = uid("link", gid, n)
        links.append(link(lid, W(n), n, cost=p or None, mods=list(opt[2]) if len(opt) > 2 else None))
    return group(gid, title, mods=_model_count_mods(mx, unit_id, model_ids, minus), links=links,
                 entries=list(entries), constraints=[constraint(mx, "max", 0)])


def model_takes(key, title, unit_id, model_ids, items):
    """'Any model may take ...': each item at most once per model."""
    gid = uid("grp", key, title)
    links = []
    for n, p in items:
        lid = uid("link", gid, n)
        mx = uid(lid, "max")
        links.append(link(lid, W(n), n, cost=p, mods=_model_count_mods(mx, unit_id, model_ids),
                          constraints=[constraint(mx, "max", 0)]))
    return group(gid, title, links=links)


def model_pair_claws(key, title, unit_id, model_ids, cost):
    """'Any model may replace both ... with a Pair of Lightning Claws' - an inline entry so it can be counted."""
    eid = uid(key, "pair-claws")
    mx = uid(eid, "max")
    return eid, entry(eid, title, cost=cost, mods=_model_count_mods(mx, unit_id, model_ids),
                      constraints=[constraint(mx, "max", 0)], links=[gear(eid, "Pair of Lightning Claws")])


def numbered(model, count, required=1):
    """Split a model entry that allows up to `count` models into `count` separate entries (max 1 each), so
    every model gets its own options. The first copy keeps the original ids."""
    import copy
    base = model.get("id")
    for c in model.findall("constraints/constraint"):
        if c.get("type") == "max" and c.get("scope") == "parent":
            c.set("value", "1")
        if c.get("type") == "min" and c.get("scope") == "parent":
            c.set("value", "1" if required >= 1 else "0")
    out = [model]
    for i in range(2, count + 1):
        m = copy.deepcopy(model)
        ids = {e.get("id") for e in m.iter() if e.get("id")}
        remap = {old: uid(old, "copy", i) for old in ids}
        for e in m.iter():
            for attr in ("id", "childId", "scope", "field", "defaultSelectionEntryId"):
                v = e.get(attr)
                if v in remap:
                    e.set(attr, remap[v])
        for c in m.findall("constraints/constraint"):
            if c.get("type") == "min" and c.get("scope") == "parent":
                c.set("value", "1" if i <= required else "0")
        out.append(m)
    return out


def choice(key, title, options, unit_id=None, required=False, default=None, hide=None):
    """Squad-wide exclusive choice built from inline entries.
    options: [(name, pts, per_model, links_to, rules)] - per_model multiplies pts by models in unit_id."""
    gid = uid("grp", key, title)
    ents = []
    default_id = None
    for name, pts, pm, links_to, rls in options:
        eid = uid("choice", key, title, name)
        mods = []
        cost = pts
        if pm:
            cost = 0
            mods.append(modifier("increment", PTS, pts, repeats=[repeat("model", unit_id, 1)]))
        ents.append(entry(eid, name, cost=cost, mods=mods,
                          constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                          links=[gear(eid, x) for x in links_to], infolinks=rules_links(rls, key=eid)))
        if name == default:
            default_id = eid
    cons = [constraint(uid(gid, "max"), "max", 1, auto=True)]
    if required:
        cons.append(constraint(uid(gid, "min"), "min", 1, auto=True))
    mods = []
    if hide:
        mods = [modifier("set", "hidden", "true", groups=[any_of(*hide)]),
                modifier("set", uid(gid, "max"), 0, groups=[any_of(*hide)])]
    return group(gid, title, entries=ents, constraints=cons, default=default_id, mods=mods)


def armour_pattern(key):
    return choice(key, "Terminator Armour Pattern (entire squad)",
                  [(n, 0, False, [n], []) for n in TDA], required=True, default="Terminator Armour")


def standard_choice(key, extra=()):
    """Legion Vexilla / Sacred Standard / Legion Standard (+ Crusade Relic where allowed)."""
    gid = uid("grp", key, "standard")
    items = [("Legion Vexilla", 10), ("Sacred Standard", 20), ("Legion Standard", 60), *extra]
    links = []
    for name, pts in items:
        lid = uid("link", gid, name)
        mods, cons = [], [constraint(uid(lid, "max"), "max", 1, auto=True)]
        if name == "Legion Standard":
            small = [cond("any", "roster", "lessThan", 2000, field=PTS, deep=False)]
            mods = [modifier("set", uid(lid, "max"), 0, conds=small), modifier("set", "hidden", "true", conds=small)]
        links.append(link(lid, W(name), name, cost=pts, mods=mods, constraints=cons))
    return group(gid, "Standard", links=links, constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


def tda_armoury(key, skip=()):
    """Up to 50 points from the Terminator-Sergeant column of the Space Marine Armoury."""
    gid = uid("grp", key, "tda-armoury")
    links = [link(uid("link", gid, n), W(n), n, cost=p, constraints=[constraint(uid("link", gid, n, "max"), "max", 1,
                                                                                 auto=True)])
             for n, p in TDA_SGT.items() if n not in skip]
    return group(gid, "Space Marine Armoury (max 50 pts)", links=links,
                 constraints=[constraint(uid(gid, "maxpts"), "max", 50, scope="self", field=PTS, deep=True)])


def pa_armoury(key, unit_id, max_size, slots=(), skip=()):
    if slots:
        return L.sgt_armoury_capped(key, unit_id, max_size, list(slots), skip=skip)
    return L.sgt_extra_capped(key, unit_id, max_size, skip=skip)


# ------------------------------------------------------------- transports
T = L.TRANSPORTS
T.update({n: uid("transport", n) for n in [
    "Legion Dreadnought Drop Pod", "Land Raider Phobos", "Land Raider Proteus", "Legion Spartan Assault Tank",
    "Damocles Command Rhino"]})

PINTLE = [("Twin-linked Bolter", 5), ("Combi-Weapon", 5), ("Heavy Bolter", 10), ("Heavy Flamer", 10),
          ("Multi-Melta", 15), ("Havoc Launcher", 15)]
ORBITAL = ["Legion Drop Pod", "Anvillus Pattern Dreadclaw Drop Pod"]


def transports(key, unit_id, options, max_models=None, block_if=(), orbital=True, spearhead=True):
    """Dedicated Transport choice. Rite options appear when that Rite of War is chosen."""
    gid = uid("grp", key, "transport")
    mx = uid(gid, "max")
    blockers = list(block_if)
    if max_models:
        blockers.append(cond("model", unit_id, "greaterThan", max_models))
    links = [link(uid("link", gid, n), T[n], n) for n in options]
    extra = []
    if orbital:
        extra += [(n, "Orbital Assault") for n in ORBITAL if n not in options]
    if spearhead and "Land Raider Phobos" not in options:
        extra.append(("Land Raider Phobos", "Armoured Spearhead"))
    for n, r in extra:
        lid = uid("link", gid, "rite", n)
        links.append(link(lid, T[n], f"{n} ({r})", mods=[
            modifier("set", "hidden", "true", conds=[cond(rite_id(r), "force", "lessThan", 1)])],
            constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    mods = []
    if blockers:
        mods = [modifier("set", mx, 0, groups=[any_of(*blockers)]),
                modifier("set", "hidden", "true", groups=[any_of(*blockers)])]
    return group(gid, "Dedicated Transport", links=links, mods=mods,
                 constraints=[constraint(mx, "max", 1, auto=True)])


def vehicle_upgrades(key, items, pintle=True):
    out = [take(key, "Vehicle Upgrades", items)]
    if pintle:
        out.append(take(key, "Pintle-mounted Weapon", PINTLE, max_total=1))
    return out


STD_UPGRADES = [("Hunter-Killer Missile", 5), ("Dozer Blade", 5), ("Extra Armour", 5), ("Auxiliary Drive", 10),
                ("Armoured Ceramite", 20)]


def land_raider(variant, typ="unit", key=None):
    """Land Raider Phobos / Proteus / Achilles as a transport (unit) or as a squadron model."""
    key = key or variant
    eid = T.get(variant) if typ == "unit" else uid("model", key, variant)
    data = {
        "Land Raider Phobos": (250, ["Twin-linked Lascannon", "Twin-linked Lascannon", "Twin-linked Heavy Bolter",
                                     "Searchlight", "Smoke Launchers"],
                               ["Power of the Machine Spirit", "Assault Vehicle"], "10 models"),
        "Land Raider Proteus": (200, ["Twin-linked Lascannon", "Twin-linked Lascannon", "Searchlight",
                                      "Smoke Launchers"], ["Power of the Machine Spirit"], "10 models"),
        "Land Raider Achilles": (275, ["Quad Launcher with Frag and Shatter Shells", "Twin-linked Multi-Melta",
                                       "Twin-linked Multi-Melta", "Extra Armour", "Armoured Ceramite", "Searchlight",
                                       "Smoke Launchers"],
                                 ["Power of the Machine Spirit", "Ferromantic Invulnerability"], "6 models"),
    }[variant]
    cost, kit, rls, cap = data
    kit_links = []
    counts = {}
    for k in kit:
        counts[k] = counts.get(k, 0) + 1
    for k, n in counts.items():
        lid = uid("link", eid, k)
        kit_links.append(link(lid, W(k), k, constraints=[constraint(uid(lid, "min"), "min", n),
                                                         constraint(uid(lid, "max"), "max", n)]))
    ups = [u for u in STD_UPGRADES if not (variant == "Land Raider Achilles" and u[0] in ("Extra Armour",
                                                                                          "Armoured Ceramite"))]
    groups = vehicle_upgrades(eid, ups)
    if variant == "Land Raider Proteus":
        groups.append(take(eid, "Hull-mounted Weapon", [("Twin-linked Heavy Bolter", 20),
                                                         ("Twin-linked Heavy Flamer", 20),
                                                         ("Twin-linked Lascannon", 30)], max_total=1))
        groups.append(take(eid, "Proteus Upgrades", [("Explorator Augury Web", 50)]))
    cons = []
    cats = []
    if typ == "unit":
        cats = [foc(gs.CAT_TRANSPORT, "Dedicated Transport", eid)]
    return entry(eid, variant, typ=typ, cost=cost, cats=cats, constraints=cons,
                 profiles=[L.vehicle_profile(key, variant, "Vehicle (Tank, Transport)", 4, 14, 14, 14),
                           L.transport_profile(key, variant, cap, "Side and front access points", "-")],
                 infolinks=rules_links(rls, key=eid), links=kit_links, groups=groups)


def dread_drop_pod():
    n = "Legion Dreadnought Drop Pod"
    t = T[n]
    return entry(t, n, typ="unit", cost=65, cats=[foc(gs.CAT_TRANSPORT, "Dedicated Transport", t)],
                 profiles=[L.vehicle_profile(t, n, "Vehicle (Open-topped, Transport)", 4, 12, 12, 12),
                           L.transport_profile(t, n, "One Legion Dreadnought or Contemptor (entire capacity)", "-",
                                               "Open-topped")],
                 infolinks=rules_links(["Deep Strike", "Drop Pod Assault", "Immobile", "Inertial Guidance System",
                                        "Burning Retros", "Assault Vehicle"], key=t))


def spartan(typ="unit"):
    n = "Legion Spartan Assault Tank"
    eid = T[n] if typ == "unit" else uid("unit", n)
    cats = [foc(gs.CAT_TRANSPORT, "Dedicated Transport", eid)] if typ == "unit" else \
        [foc(HS, "Heavy Support", eid)]
    return entry(eid, n, typ="unit", cost=305, cats=cats,
                 profiles=[L.vehicle_profile(eid, n, "Vehicle (Tank, Transport)", 4, 14, 14, 14),
                           L.transport_profile(eid, n, "25 models", "Side and front access points", "-")],
                 infolinks=rules_links(["Power of the Machine Spirit", "Assault Vehicle"], key=eid),
                 links=[gear(eid, "Extra Armour"), gear(eid, "Searchlight"), gear(eid, "Smoke Launchers")],
                 groups=[slot(eid, "Main Weapons", None, [(entry(uid(eid, "ld"), "Two Laser Destroyers", links=[
                     link(uid(eid, "ld", "l"), W("Laser Destroyer"), "Laser Destroyer",
                          constraints=[constraint(uid(eid, "ld", "n"), "min", 2),
                                       constraint(uid(eid, "ld", "x"), "max", 2)])]), None)],
                              default_is_entry=entry(uid(eid, "quadlas"), "Two Quad Lascannons",
                                                     links=[link(uid(eid, "ql"), W("Quad Lascannon"), "Quad Lascannon",
                                                                 constraints=[constraint(uid(eid, "ql", "n"), "min", 2),
                                                                              constraint(uid(eid, "ql", "x"), "max",
                                                                                         2)])])),
                         slot(eid, "Hull Weapon", "Twin-linked Heavy Bolter", [("Twin-linked Heavy Flamer", 0)]),
                         *vehicle_upgrades(eid, [("Hunter-Killer Missile", 5), ("Dozer Blade", 5),
                                                 ("Auxiliary Drive", 10), ("Frag Assault Launchers", 10),
                                                 ("Armoured Ceramite", 20), ("Flare Shield", 45)])])


def damocles(typ="unit"):
    n = "Damocles Command Rhino"
    eid = T[n] if typ == "transport" else uid("unit", n)
    if typ == "transport":
        cats = [foc(gs.CAT_TRANSPORT, "Dedicated Transport", eid)]
        cons, mods = [], []
    else:
        cats = [foc(HQ, "HQ", eid)]
        small = [cond("any", "roster", "lessThan", 1000, field=PTS, deep=False)]
        cons = [constraint(uid(eid, "force-max"), "max", 1, scope="force", deep=True)]
        mods = [modifier("set", uid(eid, "force-max"), 0, conds=small)]
    return entry(eid, n, typ="unit", cost=100, cats=cats, constraints=cons, mods=mods,
                 profiles=[L.vehicle_profile(eid, n, "Vehicle (Tank)", 4, 11, 11, 11),
                           L.transport_profile(eid, n, "6 models", "One on each side and one at the rear", "None")],
                 infolinks=rules_links(["Geo-Locator Beacon", "Command Vox Relay", "Focused Bombardment (Damocles)",
                                        "Command Vehicle"], key=eid),
                 links=[gear(eid, "Twin-linked Bolter"), gear(eid, "Searchlight"), gear(eid, "Smoke Launchers"),
                        gear(eid, "Focused Bombardment")],
                 groups=[take(eid, "Vehicle Upgrades", [("Extra Armour", 5), ("Havoc Launcher", 15)])])


# ---------------------------------------------------------------- retinues
CS_WEAPONS = [("Bolter", 0), ("Storm Bolter", 3), ("Combi-Flamer", 10), ("Combi-Meltagun", 10),
              ("Combi-Plasma Gun", 10), ("Combi-Volkite Charger", 10), ("Flamer", 5), ("Meltagun", 10),
              ("Plasma Gun", 15), ("Volkite Charger", 10), ("Volkite Caliver", 15), ("Rotor Cannon", 4),
              ("Hand Flamer", 5), ("Plasma Pistol", 15), ("Rending Weapon", 5), ("Power Weapon", 15),
              ("Lightning Claw", 25), ("Power Fist", 25), ("Thunder Hammer", 30)]


def specials_decrement(base_id, base_min_id, base_max_id, special_ids, unit_id):
    """Each upgraded model (Champion, Apothecary...) replaces one of the base models."""
    mods = []
    for s in special_ids:
        c = [cond(s, unit_id, "atLeast", 1)]
        mods += [modifier("decrement", base_min_id, 1, conds=c), modifier("decrement", base_max_id, 1, conds=c)]
    return mods


def command_squad(char_key, char_id):
    key = f"{char_key}-cs"
    u = uid("unit", key)
    vid = uid("model", u, "Legion Veteran")
    prof = lambda n, ws=4: unit_profile(u, n, "Infantry" + (" (Character)" if n != "Legion Veteran" else ""),
                                        ws, 4, 4, 4, 1, 4, 2, 9, "3+")
    kit = ["Power Armour", "Frag Grenades"]
    vet_groups = [model_swaps(key, "Legion Veterans: replace Bolt Pistol (any number)", u, [vid], CS_WEAPONS),
                  model_swaps(key, "Legion Veterans: replace Chainsword (any number)", u, [vid], CS_WEAPONS),
                  model_takes(key, "Legion Veterans: wargear (any number)", u, [vid],
                              [("Combat Shield", 5), ("Melta Bombs", 5), ("Krak Grenades", 2)])]
    champ = uid("model", u, "Legion Champion")
    apo = uid("model", u, "Legion Apothecary")
    sb = uid("model", u, "Legion Standard Bearer")
    specials = [
        entry(champ, "Legion Champion", typ="model", cost=33,
              constraints=[constraint(uid(champ, "max"), "max", 1)], profiles=[prof("Legion Champion", 5)],
              links=[gear(champ, k) for k in kit + ["Bolt Pistol", "Power Weapon", "Combat Shield"]],
              groups=[pa_armoury(champ, u, 5, slots=["Bolt Pistol"], skip=("Combat Shield",))]),
        entry(apo, "Legion Apothecary", typ="model", cost=43,
              constraints=[constraint(uid(apo, "max"), "max", 1)], profiles=[prof("Legion Apothecary")],
              links=[gear(apo, k) for k in kit + ["Narthecium"]],
              groups=[take(apo, "Apothecary Wargear", [("Reductor", 5)]),
                      pa_armoury(apo, u, 5, slots=["Bolt Pistol", "Chainsword"])]),
        entry(sb, "Legion Standard Bearer", typ="model", cost=18,
              constraints=[constraint(uid(sb, "max"), "max", 1)], profiles=[prof("Legion Standard Bearer")],
              links=[gear(sb, k) for k in kit],
              groups=[standard_choice(sb, extra=[("Crusade Relic", 40)]),
                      pa_armoury(sb, u, 5, slots=["Bolt Pistol", "Chainsword"])]),
    ]
    vmin, vmax = uid(vid, "min"), uid(vid, "max")
    vet = entry(vid, "Legion Veteran", typ="model", cost=18,
                mods=specials_decrement(vid, vmin, vmax, [champ, apo, sb], u),
                constraints=[constraint(vmin, "min", 5, auto=True), constraint(vmax, "max", 5, auto=True)],
                profiles=[prof("Legion Veteran")], links=[gear(vid, k) for k in kit])
    mobility = choice(key, "Mobility (entire squad)", [
        ("Jump Packs", 15, True, ["Jump Pack"], []), ("Space Marine Bikes", 20, True, ["Space Marine Bike"], [])],
        unit_id=u)
    # only the same mobility as their character
    for e in mobility.find("selectionEntries"):
        need = "Jump Pack" if "Jump" in e.get("name") else "Space Marine Bike"
        add_mods(e, [modifier("set", "hidden", "true", conds=[lacks(W(need), char_id)]),
                     modifier("set", uid(e.get("id"), "max"), 0, conds=[lacks(W(need), char_id)])])
    tr = transports(key, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                             "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos"],
                    block_if=[has(uid("choice", key, "Mobility (entire squad)", "Jump Packs"), u),
                              has(uid("choice", key, "Mobility (entire squad)", "Space Marine Bikes"), u)])
    return entry(u, "Legion Command Squad", typ="unit", infolinks=rules_links(["Legiones Astartes", "Retinue"], key=u),
                 entries=[vet, *specials], groups=[*vet_groups, mobility, tr])


HG_PW = [("Lightning Claw", 10), ("Power Fist", 10), ("Relic Blade", 15), ("Thunder Hammer", 15)]
HG_BP = [("Bolter", 2), ("Combi-Bolter", 5), ("Foeblaster Boltgun", 5), ("Volkite Charger", 10)]


def honour_guard(char_key):
    key = f"{char_key}-hg"
    u = uid("unit", key)
    kit = ["Artificer Armour", "Refractor Field", "Frag Grenades"]
    hg = uid("model", u, "Legion Honour Guard")
    sb = uid("model", u, "Legion Honour Guard Standard Bearer")
    hp = lambda n, ws=5, w=1, a=2: unit_profile(u, n, "Infantry" + (" (Character)" if "Champion" in n else ""),
                                                 ws, 5, 4, 4, w, 4, a, 10, "2+")

    def weap(mid):
        return [slot(mid, "Replace Power Weapon", "Power Weapon", HG_PW),
                slot(mid, "Replace Bolt Pistol", "Bolt Pistol", HG_BP)]
    champ = uid("model", u, "Legion Champion")
    hmin, hmax = uid(hg, "min"), uid(hg, "max")
    models = [
        entry(champ, "Legion Champion", typ="model", cost=55,
              constraints=[constraint(uid(champ, "min"), "min", 1), constraint(uid(champ, "max"), "max", 1)],
              profiles=[hp("Legion Champion", 6, 2, 3)], links=[gear(champ, k) for k in kit],
              infolinks=rules_links(["Honour or Death"], key=champ),
              groups=weap(champ) + [pa_armoury(champ, u, 10, skip=("Artificer Armour", "Refractor Field",
                                                                     "Combat Shield"))]),
        entry(hg, "Legion Honour Guard", typ="model", cost=40,
              mods=specials_decrement(hg, hmin, hmax, [sb], u),
              constraints=[constraint(hmin, "min", 2), constraint(hmax, "max", 9)],
              profiles=[hp("Legion Honour Guard")], links=[gear(hg, k) for k in kit]),
        entry(sb, "Legion Honour Guard Standard Bearer (Legion Standard)", typ="model", cost=100,
              constraints=[constraint(uid(sb, "max"), "max", 1)],
              mods=[modifier("set", uid(sb, "max"), 0,
                             conds=[cond("any", "roster", "lessThan", 2000, field=PTS, deep=False)])],
              profiles=[hp("Legion Honour Guard Standard Bearer")], links=[gear(sb, k) for k in kit + ["Legion Standard"]],
              groups=weap(sb)),
        per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
    ]
    tr = transports(key, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod", "Land Raider Phobos"])
    swaps = [model_swaps(key, "Legion Honour Guard: replace Power Weapon (any number)", u, [hg], HG_PW),
             model_swaps(key, "Legion Honour Guard: replace Bolt Pistol (any number)", u, [hg], HG_BP)]
    return entry(u, "Legion Honour Guard Squad", typ="unit",
                 infolinks=rules_links(["Legiones Astartes", "Honour or Death", "Retinue"], key=u),
                 entries=models, groups=[*swaps, tr])


TDA_RANGED = [("Combi-Flamer", 10), ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15), ("Combi-Volkite Charger", 10),
              ("Foeblaster Boltgun", 5), ("Volkite Charger", 10)]
TDA_CC = [("Power Fist", 10), ("Lightning Claw", 10), ("Chainfist", 15), ("Thunder Hammer", 15)]
TDA_HEAVY = [("Heavy Flamer", 10), ("Reaper Autocannon", 15), ("Plasma Blaster", 15), ("Assault Cannon", 20),
             ("Cyclone Missile Launcher", 30)]


def tda_weapon_slots(mid, ranged, cc, pair_cost):
    pair = entry(uid(mid, "pair"), "Pair of Lightning Claws (replaces both)", cost=pair_cost,
                 links=[gear(uid(mid, "pair"), "Pair of Lightning Claws")])
    return [slot(mid, "Replace Combi-bolter", "Combi-Bolter", ranged + [(pair, None)]),
            slot(mid, "Replace Power Weapon", "Power Weapon", cc, zero_if=[has(uid(mid, "pair"), "parent")])]


def tda_model_swaps(key, unit_id, model_ids, label, ranged, cc, pair_cost, heavy):
    """Squad-level weapon blocks for the ordinary models of a Terminator unit ('any model may ...')."""
    pid, pair = model_pair_claws(key, "Pair of Lightning Claws (replaces Combi-bolter and Power Weapon)", unit_id,
                                 model_ids, pair_cost)
    replaces_combi = [W(n) for n, _ in heavy if n != "Cyclone Missile Launcher"]
    return [model_swaps(key, f"{label}: replace Combi-bolter (any number)", unit_id, model_ids, ranged,
                        minus=replaces_combi, entries=[pair]),
            model_swaps(key, f"{label}: replace Power Weapon (any number)", unit_id, model_ids, cc, minus=[pid])]


def terminator_command_squad(char_key):
    key = f"{char_key}-tcs"
    u = uid("unit", key)
    vid = uid("model", u, "Terminator Veteran")
    prof = lambda n, ws=4: unit_profile(u, n, "Infantry" + (" (Character)" if n != "Terminator Veteran" else ""),
                                        ws, 4, 4, 4, 1, 4, 2, 9, "2+")
    champ, apo, sb = (uid("model", u, n) for n in ["Terminator Champion", "Terminator Apothecary",
                                                   "Terminator Standard Bearer"])
    vmin, vmax = uid(vid, "min"), uid(vid, "max")
    specials = [
        entry(champ, "Terminator Champion", typ="model", cost=58, constraints=[constraint(uid(champ, "max"), "max", 1)],
              profiles=[prof("Terminator Champion", 5)],
              rules=[rule(uid(champ, "mc"), "Master-crafted Power Weapon",
                          "The Terminator Champion's power weapon is Master-crafted at no additional points cost.")],
              groups=tda_weapon_slots(champ, TDA_RANGED, TDA_CC, 15) + [tda_armoury(champ)]),
        entry(apo, "Terminator Apothecary", typ="model", cost=68, constraints=[constraint(uid(apo, "max"), "max", 1)],
              profiles=[prof("Terminator Apothecary")], links=[gear(apo, "Narthecium")],
              groups=tda_weapon_slots(apo, TDA_RANGED, TDA_CC, 15) +
              [take(apo, "Apothecary Wargear", [("Reductor", 5)]), tda_armoury(apo)]),
        entry(sb, "Terminator Standard Bearer", typ="model", cost=43, constraints=[constraint(uid(sb, "max"), "max", 1)],
              profiles=[prof("Terminator Standard Bearer")],
              groups=tda_weapon_slots(sb, TDA_RANGED, TDA_CC, 15) +
              [standard_choice(sb, extra=[("Crusade Relic", 40)]), tda_armoury(sb)]),
    ]
    vet = entry(vid, "Terminator Veteran", typ="model", cost=43,
                mods=specials_decrement(vid, vmin, vmax, [champ, apo, sb], u),
                constraints=[constraint(vmin, "min", 5, auto=True), constraint(vmax, "max", 5, auto=True)],
                profiles=[prof("Terminator Veteran")])
    heavy, _ = pool(key, "Heavy Weapon (one model)", u, TDA_HEAVY, 1)
    swaps = tda_model_swaps(key, u, [vid], "Terminator Veterans", TDA_RANGED, TDA_CC, 15, TDA_HEAVY)
    harness, _ = pool(key, "Grenade Harness (one model)", u, [("Grenade Harness", 10)], 1)
    tr = transports(key, u, ["Land Raider Phobos", "Land Raider Proteus", "Anvillus Pattern Dreadclaw Drop Pod"],
                    orbital=False)
    return entry(u, "Legion Terminator Command Squad", typ="unit",
                 infolinks=rules_links(["Legiones Astartes", "Retinue"], key=u),
                 entries=[vet, *specials], groups=[armour_pattern(key), *swaps, heavy, harness, tr])


RETINUE_SHARED = []


def retinue_group(char_key, char_id, praetor):
    gid = uid("grp", char_key, "retinue")
    tcs = terminator_command_squad(char_key)
    ents = []
    if praetor:
        ents.append(honour_guard(char_key))
    ents += [command_squad(char_key, char_id), tcs]
    # retinues are shared entries linked from the character (like normal units), so New Recruit sets up
    # their default wargear the same way it does for any other unit
    RETINUE_SHARED.extend(ents)
    links = []
    for e in ents:
        lid = uid("link", gid, e.get("id"))
        mods = []
        if e is tcs:
            mods = [modifier("set", "hidden", "true", groups=[no_tda(char_id)])]
        links.append(link(lid, e.get("id"), e.get("name"), mods=mods))
    return group(gid, "Retinue (no Force Organisation slot)", links=links,
                 constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)],
                 mods=[modifier("set", "hidden", "true", conds=[cond(L.consul_id("Moritat"), char_id, "atLeast", 1)])])


# ------------------------------------------------------------------ Elites
def veteran_squad():
    name = "Legion Veteran Squad"
    u = uid("unit", name)
    vid = uid("model", u, "Legion Veteran")
    sid = uid("model", u, "Legion Veteran Sergeant")
    kit = ["Power Armour", "Bolter", "Bolt Pistol", "Chainsword", "Frag Grenades"]

    def model_opts(mid):
        sniper = entry(uid(mid, "sniper"), "Sniper Rifle (Legion Recon Company)", cost=5,
                       mods=[modifier("set", "hidden", "true", conds=[cond(rite_id("Legion Recon Company"), "force",
                                                                               "lessThan", 1)])],
                       links=[gear(uid(mid, "sniper"), "Sniper Rifle")])
        return [slot(mid, "Replace Chainsword", "Chainsword", [("Chainaxe", 4), ("Rending Weapon", 5),
                                                               ("Power Weapon", 10)]),
                slot(mid, "Replace Bolter", "Bolter", [("Foeblaster Boltgun", 2), ("Combi-Flamer", 5),
                                                       ("Combi-Grenade Launcher", 5), ("Combi-Volkite Charger", 5),
                                                       ("Combi-Meltagun", 10), ("Combi-Plasma Gun", 10),
                                                       (sniper, None)]),
                take(mid, "Wargear", [("Combat Shield", 5), ("Melta Bombs", 5)])]
    sgt = entry(sid, "Legion Veteran Sergeant", typ="model", cost=0,
                constraints=[constraint(uid(sid, "min"), "min", 1), constraint(uid(sid, "max"), "max", 1)],
                profiles=[unit_profile(u, "Legion Veteran Sergeant", "Infantry (Character)", 5, 4, 4, 4, 1, 4, 2, 9,
                                       "3+")],
                links=[gear(sid, k) for k in kit],
                groups=model_opts(sid) + [pa_armoury(sid, u, 10, skip=("Combat Shield", "Melta Bombs"))])
    vets = entry(vid, "Legion Veteran", typ="model", cost=20,
                 constraints=[constraint(uid(vid, "min"), "min", 4), constraint(uid(vid, "max"), "max", 9)],
                 profiles=[unit_profile(u, "Legion Veteran", "Infantry", 5, 4, 4, 4, 1, 4, 2, 9, "3+")],
                 links=[gear(vid, k) for k in kit])
    heavy = ["Heavy Flamer with Suspensor Web", "Heavy Bolter with Suspensor Web", "Missile Launcher with Suspensor Web"]
    spec_opts = [("Rotor Cannon", 4), ("Flamer", 5), ("Meltagun", 10), ("Plasma Gun", 15), ("Volkite Charger", 10),
                 ("Volkite Caliver", 15), ("Heavy Flamer with Suspensor Web", 10),
                 ("Heavy Bolter with Suspensor Web", 15), ("Missile Launcher with Suspensor Web", 20)]
    spec, _ = pool(u, "Specialist Weapons (1 per 5 models)", u, spec_opts, 0, every=5)
    no_recon = [cond(rite_id("Legion Recon Company"), "force", "lessThan", 1)]
    vet_swaps = [
        model_swaps(u, "Legion Veterans: replace Chainsword (any number)", u, [vid],
                    [("Chainaxe", 4), ("Rending Weapon", 5), ("Power Weapon", 10)]),
        model_swaps(u, "Legion Veterans: replace Bolter (any number)", u, [vid],
                    [("Foeblaster Boltgun", 2), ("Combi-Flamer", 5), ("Combi-Grenade Launcher", 5),
                     ("Combi-Volkite Charger", 5), ("Combi-Meltagun", 10), ("Combi-Plasma Gun", 10),
                     ("Sniper Rifle", 5, [modifier("set", "hidden", "true", conds=no_recon)])],
                    minus=[W(n) for n, _ in spec_opts]),
        model_takes(u, "Legion Veterans: wargear (any number)", u, [vid], [("Combat Shield", 5), ("Melta Bombs", 5)]),
    ]
    has_heavy = [has(W(h), u) for h in heavy]
    jp_id = uid("squadwide", u, "Jump Packs (entire squad)")
    jp = per_model(u, "Jump Packs (entire squad)", 15, u, ["Jump Pack"])
    add_mods(jp, [modifier("set", "hidden", "true", groups=[any_of(*has_heavy)]),
                  modifier("set", uid(jp_id, "max"), 0, groups=[any_of(*has_heavy)]),
                  modifier("decrement", PTS, 5, conds=[rite("Legion Assault Company")],
                           repeats=[repeat("model", u, 1)])])
    tactics = choice(u, "Veteran Tactics", [
        ("Resolve", 0, False, [], ["Resolve", "Stubborn"]),
        ("Assault Veterans", 0, False, [], ["Assault Veterans", "Furious Charge"]),
        ("Counter-Assault", 0, False, [], ["Counter-Assault", "Counter-Attack"]),
        ("Machine Killers", 0, False, [], ["Machine Killers", "Tank Hunters"]),
        ("Recon Veterans", 0, False, [], ["Recon Veterans", "Infiltrate"]),
        ("Marksmen", 0, False, [], ["Marksmen"])], required=True)
    return entry(u, name, typ="unit", cost=125 - 4 * 20, mods=troop_role_mods(name),
                 cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links(["Legiones Astartes", "Veteran Tactics"], key=u),
                 entries=[sgt, vets, jp, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
                 groups=[tactics, *vet_swaps, spec, L.one_each(u, "Squad Equipment", [("Legion Vexilla", 10), ("Nuncio Vox", 10)]),
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos"],
                                    block_if=[has(jp_id, u)])])


def terminator_squad():
    name = "Legion Terminator Squad"
    u = uid("unit", name)
    tid = uid("model", u, "Legion Terminator")
    sid = uid("model", u, "Legion Terminator Sergeant")
    ranged = [("Storm Bolter", 0), ("Foeblaster Boltgun", 5), ("Combi-Grenade Launcher", 10), ("Combi-Flamer", 10),
              ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15), ("Combi-Volkite Charger", 10), ("Volkite Charger", 10)]
    cc = [("Power Fist", 5), ("Lightning Claw", 5), ("Chainfist", 10), ("Thunder Hammer", 10)]
    sgt = entry(sid, "Legion Terminator Sergeant", typ="model", cost=0,
                constraints=[constraint(uid(sid, "min"), "min", 1), constraint(uid(sid, "max"), "max", 1)],
                profiles=[unit_profile(u, "Legion Terminator Sergeant", "Infantry (Character)", 4, 4, 4, 4, 1, 4, 2, 9,
                                       "2+")],
                groups=tda_weapon_slots(sid, ranged, cc, 15) +
                [take(sid, "Sergeant Wargear", [("Grenade Harness", 10)]), tda_armoury(sid)])
    terms = entry(tid, "Legion Terminator", typ="model", cost=30,
                  constraints=[constraint(uid(tid, "min"), "min", 4), constraint(uid(tid, "max"), "max", 9)],
                  profiles=[unit_profile(u, "Legion Terminator", "Infantry", 4, 4, 4, 4, 1, 4, 2, 9, "2+")])
    heavy, _ = pool(u, "Heavy Weapons (1 per 5 models)", u, TDA_HEAVY, 0, every=5)
    swaps = tda_model_swaps(u, u, [tid], "Legion Terminators", ranged, cc, 15, TDA_HEAVY)
    return entry(u, name, typ="unit", cost=175 - 4 * 30, mods=troop_role_mods(name),
                 cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links(["Legiones Astartes", "Implacable Advance"], key=u),
                 entries=[sgt, terms],
                 groups=[armour_pattern(u), *swaps, heavy,
                         transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                                    orbital=False)])


def destroyer_squad():
    name = "Legion Destroyer Squad"
    u = uid("unit", name)
    did = uid("model", u, "Legion Destroyer")
    sid = uid("model", u, "Legion Destroyer Sergeant")
    kit = ["Power Armour", "Two Bolt Pistols", "Chainsword", "Frag Grenades", "Rad Grenades"]
    sgt = entry(sid, "Legion Destroyer Sergeant", typ="model", cost=0,
                constraints=[constraint(uid(sid, "min"), "min", 1), constraint(uid(sid, "max"), "max", 1)],
                profiles=[unit_profile(u, "Legion Destroyer Sergeant", "Infantry (Character)", 4, 4, 4, 4, 1, 4, 2, 9,
                                       "3+")],
                links=[gear(sid, k) for k in kit],
                groups=[slot(sid, "Replace Chainsword", "Chainsword", [("Rending Weapon", 5), ("Power Weapon", 10),
                                                                       ("Power Fist", 15), ("Lightning Claw", 15),
                                                                       ("Thunder Hammer", 20)]),
                        take(sid, "Sergeant Wargear", [("Phosphex Bomb", 10, 3)]),
                        pa_armoury(sid, u, 10)])
    dests = entry(did, "Legion Destroyer", typ="model", cost=20,
                  constraints=[constraint(uid(did, "min"), "min", 4), constraint(uid(did, "max"), "max", 9)],
                  profiles=[unit_profile(u, "Legion Destroyer", "Infantry", 4, 4, 4, 4, 1, 4, 1, 9, "3+")],
                  links=[gear(did, k) for k in kit])
    gid_key = u
    weapons, mx = pool(gid_key, "Destroyer Weapons (1 per 5 models; 2 per 5 in a Destroyer Company)", u, [
        ("Volkite Serpenta", 5), ("Hand Flamer", 10), ("Plasma Pistol", 15),
        ("Missile Launcher with Suspensor Web and Rad Missiles", 25)], 0, every=5)
    add_mods(weapons, [modifier("increment", mx, 1, conds=[rite("Legion Destroyer Company")],
                                repeats=[repeat("model", u, 5)])])
    jp_id = uid("squadwide", u, "Jump Packs (entire squad)")
    return entry(u, name, typ="unit", cost=150 - 4 * 20, mods=troop_role_mods(name),
                 cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links(["Legiones Astartes", "Counter-Attack", "Dual Pistols (Destroyers)",
                                        "Destroyer Cadre"], key=u),
                 entries=[sgt, dests, per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]),
                          per_model(u, "Jump Packs (entire squad)", 15, u, ["Jump Pack"]),
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
                 groups=[weapons, transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                                    "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos"],
                                             block_if=[has(jp_id, u)])])


TECHMARINE_COVENANT = uid("unit", "Techmarine Covenant")


def techmarine_covenant():
    u = TECHMARINE_COVENANT
    tm = uid("model", u, "Legion Techmarine")
    sv = uid("model", tm, "Servo-automata")
    servo = entry(sv, "Servo-automata", typ="model", cost=12,
                  constraints=[constraint(uid(sv, "max"), "max", 4)],
                  profiles=[unit_profile(u, "Servo-automata", "Infantry", 3, 3, 4, 5, 1, 1, 1, 6, "5+")],
                  links=[gear(sv, "Bolter"), gear(sv, "Chainsword")],
                  infolinks=rules_links(["Cybernetica"], key=sv))
    sb, _ = pool(tm, "Servo-automata: replace Bolter", tm, [("Flamer", 5), ("Rotor Cannon", 5), ("Heavy Bolter", 10),
                                                            ("Multi-Melta", 10), ("Missile Launcher", 15)],
                 0, every=1, per_child=sv)
    sc, _ = pool(tm, "Servo-automata: replace Chainsword", tm, [("Power Fist", 15)], 0, every=1, per_child=sv)
    rad, _ = pool(tm, "Servo-automata: Rad Missiles for Missile Launchers", tm, [("Rad Missiles", 10)], 0,
                  every=1, per_child=W("Missile Launcher"))
    add_mods(rad, [modifier("set", "hidden", "true", conds=[lacks(W("Rad Grenades"), tm)])])
    tech = entry(tm, "Legion Techmarine", typ="model", cost=50,
                 constraints=[constraint(uid(tm, "min"), "min", 1), constraint(uid(tm, "max"), "max", 3)],
                 profiles=[unit_profile(u, "Legion Techmarine", "Infantry (Character)", 4, 4, 4, 4, 1, 4, 1, 9, "3+")],
                 infolinks=rules_links(["Legiones Astartes", "Independent Character", "Battlesmith (Techmarine)",
                                        "Bolster Defences", "Field Team"], key=tm),
                 links=[gear(tm, k) for k in ["Power Armour", "Frag Grenades"]],
                 entries=[servo],
                 groups=[
                     take(tm, "Wargear", [("Auspex", 2), ("Melta Bombs", 5), ("Nuncio Vox", 10), ("Rad Grenades", 10),
                                          ("Signum", 15), ("Krak Grenades", 2)]),
                     slot(tm, "Replace Bolt Pistol", "Bolt Pistol", [("Volkite Serpenta", 5), ("Plasma Pistol", 15)]),
                     slot(tm, "Replace Power Weapon", "Power Weapon", [("Thunder Hammer", 15)]),
                     take(tm, "Additional Weapon (one)", [
                         ("Bolter", 2), ("Combi-Flamer", 10), ("Combi-Volkite Charger", 10), ("Combi-Meltagun", 15),
                         ("Combi-Plasma Gun", 15), ("Volkite Charger", 10), ("Graviton Gun", 15),
                         ("Volkite Caliver", 15), ("Rotor Cannon", 4)], max_total=1),
                     slot(tm, "Replace Servo-Arm", "Servo-Arm", [("Conversion Beamer", 35)]),
                     take(tm, "Mobility", [("Space Marine Bike", 35)]),
                     sb, sc, rad,
                     transports(tm, tm, ["Legion Rhino Armoured Carrier"], block_if=[has(W("Space Marine Bike"), tm)],
                                orbital=False, spearhead=False)])
    return entry(u, "Techmarine Covenant", typ="unit", cats=[foc(ELITES, "Elites", u)], entries=numbered(tech, 3, 1))


DREAD_ARM1 = [("Multi-Melta", 0), ("Twin-linked Autocannon", 5), ("Twin-linked Missile Launcher", 10),
              ("Plasma Cannon", 10), ("Volkite Culverin", 10), ("Assault Cannon", 10), ("Flamestorm Cannon", 15),
              ("Twin-linked Lascannon", 25)]
DREAD_ARM2 = [("Twin-linked Heavy Bolter", 0), ("Multi-Melta", 0), ("Twin-linked Autocannon", 10),
              ("Twin-linked Missile Launcher", 15), ("Plasma Cannon", 10), ("Volkite Culverin", 10),
              ("Assault Cannon", 15), ("Twin-linked Lascannon", 25)]
CONT_ARM1 = [("Multi-Melta", 0), ("Twin-linked Autocannon", 5), ("Plasma Cannon", 10),
             ("Twin-linked Volkite Culverin", 15), ("Kheres Assault Cannon", 15), ("Twin-linked Lascannon", 25),
             ("Heavy Conversion Beamer", 35)]
CONT_ARM2 = [("Twin-linked Heavy Bolter", 0), ("Multi-Melta", 0), ("Twin-linked Autocannon", 10),
             ("Plasma Cannon", 10), ("Twin-linked Volkite Culverin", 15), ("Kheres Assault Cannon", 15),
             ("Twin-linked Lascannon", 25)]
BUILT_IN = [("Heavy Flamer", 10), ("Meltagun", 15), ("Graviton Gun", 15), ("Plasma Blaster", 20)]


def dreadnought(name, cost, stats, arm1, arm2, rules_, upgrades, extra_groups=()):
    u = uid("unit", name)
    ws, bs, s, f, si, r, i, a = stats
    ccw1 = uid(u, "arm1-ccw")
    ccw2 = uid(u, "arm2-ccw")
    fist2 = uid(u, "arm2-chainfist")
    # the built-in weapon lives inside the close-combat arm, so it exists exactly when that arm does
    arm1_ccw = entry(ccw1, "Dreadnought Close Combat Weapon", links=[gear(ccw1, "Dreadnought Close Combat Weapon")],
                     groups=[slot(ccw1, "Built-in weapon", "Twin-linked Bolter", BUILT_IN)])
    arm2_ccw = entry(ccw2, "Dreadnought Close Combat Weapon", links=[gear(ccw2, "Dreadnought Close Combat Weapon")],
                     groups=[slot(ccw2, "Built-in weapon", "Twin-linked Bolter", BUILT_IN)])
    arm2_fist = entry(fist2, "Chainfist", cost=10, links=[gear(fist2, "Chainfist")],
                      groups=[slot(fist2, "Built-in weapon", "Twin-linked Bolter", BUILT_IN)])
    prof = walker_profile(u, name, ws, bs, s, f, si, r, i, a)
    both = all_of(cond(ccw1, u, "atLeast", 1), cond(ccw2, u, "atLeast", 1))
    pilot = [cond(W("Veteran Pilot"), u, "atLeast", 1)]
    sarc = [cond(W("Armoured Sarcophagus"), u, "atLeast", 1)]
    prof.insert(0, wrap("modifiers", [
        modifier("set", gs.char_id("Walker", "A"), int(a) + 1, groups=[both]),
        modifier("set", gs.char_id("Walker", "WS"), int(ws) + 1, conds=pilot),
        modifier("set", gs.char_id("Walker", "BS"), int(bs) + 1, conds=pilot),
        modifier("set", gs.char_id("Walker", "Front"), 13, conds=sarc)]))
    groups = [
        slot(u, "Weapon Arm 1 (replace Twin-linked Heavy Bolter)", "Twin-linked Heavy Bolter",
             arm1 + [(arm1_ccw, None)]),
        slot(u, "Weapon Arm 2 (replace Dreadnought Close Combat Weapon)", None, arm2 + [(arm2_fist, None)],
             default_is_entry=arm2_ccw),
        take(u, "Vehicle Upgrades", upgrades),
        *extra_groups,
    ]
    dp = uid("grp", u, "transport")
    fury_orbital = [("Legion Drop Pod", "Orbital Assault"), ("Anvillus Pattern Dreadclaw Drop Pod", "Orbital Assault")]
    tr_links = [link(uid("link", dp, "Legion Dreadnought Drop Pod"), T["Legion Dreadnought Drop Pod"],
                     "Legion Dreadnought Drop Pod")]
    for n, r in fury_orbital:
        lid = uid("link", dp, "rite", n)
        tr_links.append(link(lid, T[n], f"{n} ({r})",
                             mods=[modifier("set", "hidden", "true", conds=[cond(rite_id(r), "force", "lessThan", 1)])],
                             constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    groups.append(group(dp, "Dedicated Transport", links=tr_links, constraints=[constraint(uid(dp, "max"), "max", 1,
                                                                                            auto=True)]))
    return entry(u, name, typ="unit", cost=cost, mods=troop_role_mods(name), cats=[foc(ELITES, "Elites", u)],
                 profiles=[prof], infolinks=rules_links(rules_ + ["Paired Close-Combat Arms"], key=u),
                 links=[gear(u, "Smoke Launchers"), gear(u, "Searchlight")], groups=groups)


def rapier_battery():
    name = "Legion Rapier Weapons Battery"
    u = uid("unit", name)
    car = uid("model", u, "Rapier Carrier")
    crew = uid("model", u, "Legion Space Marine Crew")
    cmin, cmax = uid(crew, "min"), uid(crew, "max")
    carrier = entry(car, "Rapier Carrier", typ="model", cost=50,
                    constraints=[constraint(uid(car, "min"), "min", 1), constraint(uid(car, "max"), "max", 3)],
                    profiles=[unit_profile(u, "Rapier Carrier", "Artillery", "-", "-", "-", 7, 2, "-", "-", "-",
                                           "3+")])
    crews = entry(crew, "Legion Space Marine Crew", typ="model", cost=0,
                  mods=[modifier("increment", cmin, 2, repeats=[repeat(car, u, 1)]),
                        modifier("increment", cmax, 2, repeats=[repeat(car, u, 1)])],
                  constraints=[constraint(cmin, "min", 0, auto=True), constraint(cmax, "max", 0, auto=True)],
                  profiles=[unit_profile(u, "Legion Space Marine", "Infantry", 4, 4, 4, 4, 1, 4, 1, 8, "3+")],
                  links=[gear(crew, k) for k in ["Power Armour", "Bolt Pistol", "Frag Grenades"]],
                  infolinks=rules_links(["Legiones Astartes"], key=crew))

    def per_carrier(key, title, options, required=False, default=None, hide=None):
        gid = uid("grp", key, title)
        ents = []
        dflt = None
        for n, pts, profs in options:
            eid = uid("choice", key, title, n)
            ents.append(entry(eid, n, cost=0,
                              mods=[modifier("increment", PTS, pts, repeats=[repeat(car, u, 1)])] if pts else [],
                              constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                              links=[gear(eid, p) for p in profs]))
            if n == default:
                dflt = eid
        cons = [constraint(uid(gid, "max"), "max", 1, auto=True)]
        if required:
            cons.append(constraint(uid(gid, "min"), "min", 1, auto=True))
        mods = [modifier("set", "hidden", "true", groups=[any_of(*hide)])] if hide else []
        return group(gid, title, entries=ents, constraints=cons, default=dflt, mods=mods)
    weapon = per_carrier(u, "Battery Weapon (all carriers)", [
        ("Quad Heavy Bolters", 0, ["Quad Heavy Bolter"]), ("Laser Destroyers", 20, ["Laser Destroyer"]),
        ("Quad Launchers", 20, ["Quad Launcher"]), ("Graviton Cannons", 35, ["Graviton Cannon"])],
        required=True, default="Quad Heavy Bolters")
    ql = uid("choice", u, "Battery Weapon (all carriers)", "Quad Launchers")
    siege = uid("siegebreaker")
    ammo_gid = uid("grp", u, "ammo")
    ammo_ents = []
    for n, pts in [("Incendiary Shells", 5), ("Shatter Shells", 10), ("Splinter Shells", 10),
                   ("Phosphex Canister Shot", 20)]:
        eid = uid("choice", u, "ammo", n)
        mods = [modifier("increment", PTS, pts, repeats=[repeat(car, u, 1)])]
        if n == "Phosphex Canister Shot":
            mods.append(modifier("set", "hidden", "true", conds=[cond(siege, "force", "lessThan", 1)]))
        ammo_ents.append(entry(eid, n, cost=0, mods=mods, constraints=[constraint(uid(eid, "max"), "max", 1,
                                                                                   auto=True)],
                               links=[gear(eid, n)]))
    ammo = group(ammo_gid, "Quad Launcher Ammunition (all carriers)", entries=ammo_ents,
                 mods=[modifier("set", "hidden", "true", conds=[cond(ql, u, "lessThan", 1)])])
    return entry(u, name, typ="unit", cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links(["Rapier Battery", "Shell Shock", "Sunder"], key=u),
                 entries=[carrier, crews], groups=[weapon, ammo])


# ------------------------------------------------------------- Fast Attack
SGT_PISTOL = L.PISTOL_SWAPS
SGT_CCW = [("Rending Weapon", 5), ("Power Weapon", 10), ("Lightning Claw", 15), ("Power Fist", 15),
           ("Thunder Hammer", 20)]


def pair_sergeant_slots(sk):
    pair = entry(uid(sk, "pair"), "Pair of Lightning Claws (replaces both)", cost=20,
                 links=[gear(uid(sk, "pair"), "Pair of Lightning Claws")])
    return [slot(sk, "Replace Bolt Pistol", "Bolt Pistol", SGT_PISTOL + [(pair, None)]),
            slot(sk, "Replace Chainsword", "Chainsword", SGT_CCW, zero_if=[has(uid(sk, "pair"), "parent")])]


def seeker_squad():
    name = "Legion Seeker Squad"
    u = uid("unit", name)
    sid, mid = uid("model", u, "Legion Seeker Sergeant"), uid("model", u, "Legion Seeker")
    kit = ["Power Armour", "Bolter", "Bolt Pistol", "Frag Grenades", "Special Issue Ammunition"]
    combis = [("Combi-Flamer", 5), ("Combi-Grenade Launcher", 5), ("Combi-Volkite Charger", 5), ("Combi-Meltagun", 10),
              ("Combi-Plasma Gun", 10)]
    sgt = entry(sid, "Legion Seeker Sergeant", typ="model",
                constraints=[constraint(uid(sid, "min"), "min", 1), constraint(uid(sid, "max"), "max", 1)],
                profiles=[unit_profile(u, "Legion Seeker Sergeant", "Infantry (Character)", 4, 5, 4, 4, 1, 4, 2, 9,
                                       "3+")],
                links=[gear(sid, k) for k in kit],
                groups=[slot(sid, "Replace Bolt Pistol", "Bolt Pistol", SGT_PISTOL),
                        take(sid, "Sergeant Wargear", [("Power Weapon", 10), ("Lightning Claw", 15), ("Power Fist", 15),
                                                       ("Melta Bombs", 5)]),
                        pa_armoury(sid, u, 10, skip=("Melta Bombs",))])
    seekers = entry(mid, "Legion Seeker", typ="model", cost=20,
                    constraints=[constraint(uid(mid, "min"), "min", 4), constraint(uid(mid, "max"), "max", 9)],
                    profiles=[unit_profile(u, "Legion Seeker", "Infantry", 4, 5, 4, 4, 1, 4, 1, 8, "3+")],
                    links=[gear(mid, k) for k in kit])
    spec_opts = [("Flamer", 5), ("Meltagun", 10), ("Plasma Gun", 12), ("M.40 Targeter and Stalker Bolter", 10),
                 ("Heavy Bolter with Suspensor and Hellfire Rounds", 15), ("Volkite Charger", 5), ("Volkite Caliver", 10)]
    specials, _ = pool(u, "Special Weapons (up to two Seekers)", u, spec_opts, 2)
    combi_swaps = model_swaps(u, "Legion Seekers: replace Bolter (any number)", u, [mid], combis,
                              minus=[W(n) for n, _ in spec_opts])
    return entry(u, name, typ="unit", cost=155 - 4 * 20, cats=[foc(FA, "Fast Attack", u)],
                 infolinks=rules_links(["Legiones Astartes", "Infiltrate", "Move Through Cover", "Marked for Death",
                                        "Special Issue Ammunition"], key=u),
                 entries=[sgt, seekers, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[combi_swaps, specials, L.one_each(u, "Squad Equipment", [("Nuncio Vox", 10)]),
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod"])])


def bike_squadron():
    name = "Legion Bike Squadron"
    u = uid("unit", name)
    sid, mid = uid("model", u, "Legion Biker Sergeant"), uid("model", u, "Legion Biker")
    kit = ["Power Armour", "Space Marine Bike with Twin-linked Bolters", "Bolt Pistol", "Chainsword", "Frag Grenades"]
    sgt = entry(sid, "Legion Biker Sergeant", typ="model",
                constraints=[constraint(uid(sid, "min"), "min", 1), constraint(uid(sid, "max"), "max", 1)],
                profiles=[unit_profile(u, "Legion Biker Sergeant", "Bike (Character)", 4, 4, 4, 5, 1, 4, 2, 9, "3+")],
                links=[gear(sid, k) for k in kit],
                groups=pair_sergeant_slots(sid) + [take(sid, "Sergeant Wargear", [("Melta Bombs", 5)]),
                                                   pa_armoury(sid, u, 10, skip=("Melta Bombs",))])
    bikers = entry(mid, "Legion Biker", typ="model", cost=30,
                   constraints=[constraint(uid(mid, "min"), "min", 2), constraint(uid(mid, "max"), "max", 9)],
                   profiles=[unit_profile(u, "Legion Biker", "Bike", 4, 4, 4, 5, 1, 4, 1, 8, "3+")],
                   links=[gear(mid, k) for k in kit])
    specials, _ = pool(u, "Special Weapons (up to two Bikers, replace Bolt Pistol)", u,
                       [("Flamer", 5), ("Meltagun", 10), ("Plasma Gun", 15)], 2)
    bike_weapons = choice(u, "Bike Weapons (entire squad)", [
        ("Twin-linked Flamers", 10, True, ["Twin-linked Flamer"], []),
        ("Twin-linked Meltaguns", 20, True, ["Twin-linked Meltagun"], []),
        ("Twin-linked Plasma Guns", 20, True, ["Twin-linked Plasma Gun"], [])], unit_id=u)
    eq = take(u, "Squad Equipment (one only)", [("Legion Vexilla", 10), ("Nuncio Vox", 10)], max_total=1)
    return entry(u, name, typ="unit", cost=90 - 2 * 30, cats=[foc(FA, "Fast Attack", u)],
                 infolinks=rules_links(["Legiones Astartes"], key=u),
                 entries=[sgt, bikers, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[specials, bike_weapons, eq])


def sky_hunters():
    name = "Legion Sky Hunter Jetbike Squadron"
    u = uid("unit", name)
    sid, mid = uid("model", u, "Sky Hunter Sergeant"), uid("model", u, "Legion Sky Hunter")
    kit = ["Power Armour", "Scimitar Jetbike with Heavy Bolter", "Bolt Pistol", "Chainsword", "Frag Grenades"]
    sgt = entry(sid, "Sky Hunter Sergeant", typ="model",
                constraints=[constraint(uid(sid, "min"), "min", 1), constraint(uid(sid, "max"), "max", 1)],
                profiles=[unit_profile(u, "Sky Hunter Sergeant", "Jetbike (Character)", 4, 4, 4, 5, 1, 4, 2, 9, "2+")],
                links=[gear(sid, k) for k in kit],
                groups=pair_sergeant_slots(sid) + [take(sid, "Sergeant Wargear", [("Melta Bombs", 5)]),
                                                   pa_armoury(sid, u, 10, skip=("Melta Bombs",))])
    hunters = entry(mid, "Legion Sky Hunter", typ="model", cost=35,
                    constraints=[constraint(uid(mid, "min"), "min", 2), constraint(uid(mid, "max"), "max", 9)],
                    profiles=[unit_profile(u, "Legion Sky Hunter", "Jetbike", 4, 4, 4, 5, 1, 4, 1, 8, "2+")],
                    links=[gear(mid, k) for k in kit])
    jw, _ = pool(u, "Jetbike Weapons (1 per 3 models, replace Heavy Bolter)", u,
                 [("Multi-Melta", 10), ("Volkite Culverin", 10), ("Plasma Cannon", 15)], 0, every=3)
    return entry(u, name, typ="unit", cost=150 - 2 * 35, mods=troop_role_mods(name), cats=[foc(FA, "Fast Attack", u)],
                 infolinks=rules_links(["Legiones Astartes", "Deep Strike"], key=u),
                 entries=[sgt, hunters, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[jw])


def squadron(name, per, model_name, prof_fn, cat_id, cat_name, rules_, kit, groups_fn, unit_groups=(),
             unit_entries=(), mn=1, mx=3, extra_mods=()):
    """Units of 1-3 identical models/vehicles, each configured separately."""
    u = uid("unit", name)
    mid = uid("model", u, model_name)
    m = entry(mid, model_name, typ="model", cost=per,
              constraints=[constraint(uid(mid, "min"), "min", mn), constraint(uid(mid, "max"), "max", mx)],
              profiles=[prof_fn(u, model_name)], links=[gear(mid, k) for k in kit], groups=groups_fn(mid))
    return entry(u, name, typ="unit", cats=[foc(cat_id, cat_name, u)], mods=list(extra_mods),
                 infolinks=rules_links(rules_, key=u), entries=[*numbered(m, mx, mn), *unit_entries],
                 groups=list(unit_groups))


def attack_bikes():
    u = uid("unit", "Legion Attack Bike Squadron")
    return squadron("Legion Attack Bike Squadron", 40, "Legion Attack Bike",
                    lambda k, n: unit_profile(k, n, "Bike", 4, 4, 4, 5, 2, 4, 1, 8, "3+"), FA, "Fast Attack",
                    ["Legiones Astartes"],
                    ["Power Armour", "Attack Bike with Twin-linked Bolters", "Bolt Pistol", "Chainsword",
                     "Frag Grenades"],
                    lambda mid: [slot(mid, "Replace Heavy Bolter", "Heavy Bolter",
                                      [("Heavy Flamer", 0), ("Autocannon", 5), ("Multi-Melta", 10)])],
                    unit_entries=[per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                                  per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])])


def land_speeders():
    return squadron("Legion Land Speeder Squadron", 50, "Legion Land Speeder",
                    lambda k, n: L.vehicle_profile(k, n, "Vehicle (Fast, Skimmer)", 4, 10, 10, 10), FA, "Fast Attack",
                    ["Deep Strike", "Armoured Crew"], [],
                    lambda mid: [slot(mid, "Replace Heavy Bolter", "Heavy Bolter",
                                      [("Heavy Flamer", 0), ("Multi-Melta", 10), ("Volkite Culverin", 10)]),
                                 take(mid, "Additional Weapon (one)", [
                                     ("Heavy Flamer", 10), ("Heavy Bolter", 10), ("Havoc Launcher", 15),
                                     ("Graviton Gun", 15), ("Assault Cannon", 20), ("Plasma Cannon", 25),
                                     ("Typhoon Missile Launcher", 25)], max_total=1),
                                 take(mid, "Upgrades", [("Hunter-Killer Missile", 5, 2)])])


def javelins():
    return squadron("Legion Javelin Attack Speeder Squadron", 75, "Javelin Attack Speeder",
                    lambda k, n: L.vehicle_profile(k, n, "Vehicle (Fast, Skimmer)", 4, 11, 11, 10), FA, "Fast Attack",
                    ["Deep Strike", "Outflank", "Strafing Run", "Armoured Crew"], [],
                    lambda mid: [slot(mid, "Replace Twin-linked Cyclone Missile Launcher",
                                      "Twin-linked Cyclone Missile Launcher", [("Twin-linked Lascannon", 10)]),
                                 slot(mid, "Replace Heavy Bolter", "Heavy Bolter",
                                      [("Heavy Flamer", 0), ("Multi-Melta", 10)]),
                                 take(mid, "Upgrades", [("Searchlight", 1), ("Hunter-Killer Missile", 5, 2)])])


# ------------------------------------------------------------ Heavy Support
SIEGE_BREAKER = uid("siegebreaker")


def heavy_support_squad():
    name = "Legion Heavy Support Squad"
    u = uid("unit", name)
    sid, mid = uid("model", u, "Legion Sergeant"), uid("model", u, "Legion Space Marine")
    kit = ["Power Armour", "Bolter", "Bolt Pistol", "Frag Grenades"]
    spec_gid = uid("grp", sid, "specialist")
    specialist = group(spec_gid, "Heavy Support Specialist", constraints=[
        constraint(uid(spec_gid, "max"), "max", 1, auto=True)], entries=[
        entry(uid("armistos"), "Armistos", cost=20, infolinks=rules_links(["Fire Control"], key="armistos")),
        entry(SIEGE_BREAKER, "Siege Breaker", cost=35, infolinks=rules_links(["Art of Destruction"], key="sb"))])
    sgt = entry(sid, "Legion Sergeant", typ="model",
                constraints=[constraint(uid(sid, "min"), "min", 1), constraint(uid(sid, "max"), "max", 1)],
                profiles=[unit_profile(u, "Legion Sergeant", "Infantry (Character)", 4, 4, 4, 4, 1, 4, 2, 9, "3+")],
                links=[gear(sid, k) for k in kit],
                groups=[slot(sid, "Replace Bolter", "Bolter", [("Chainsword", 0), ("Combat Blade", 0),
                                                               ("Combi-Flamer", 10), ("Combi-Volkite Charger", 10),
                                                               ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15)]),
                        slot(sid, "Replace Bolt Pistol", "Bolt Pistol", SGT_PISTOL),
                        take(sid, "Sergeant Wargear", [("Signum", 15), ("Melta Bombs", 5)]),
                        specialist,
                        pa_armoury(sid, u, 10, skip=("Signum", "Melta Bombs"))])
    marines = entry(mid, "Legion Space Marine", typ="model", cost=15,
                    constraints=[constraint(uid(mid, "min"), "min", 4), constraint(uid(mid, "max"), "max", 9)],
                    profiles=[unit_profile(u, "Legion Space Marine", "Infantry", 4, 4, 4, 4, 1, 4, 1, 8, "3+")],
                    links=[gear(mid, k) for k in kit])
    heavy, _ = pool(u, "Heavy Weapons (up to four models)", u, [
        ("Heavy Bolter", 15), ("Autocannon", 20), ("Missile Launcher", 20), ("Volkite Culverin", 20),
        ("Multi-Melta", 25), ("Plasma Cannon", 30), ("Lascannon", 35)], 4)
    hardened = entry(uid(u, "hardened"), "Hardened Armour (entire squad)", cost=25,
                     constraints=[constraint(uid(u, "hardened", "max"), "max", 1)],
                     infolinks=rules_links(["Hardened Armour"], key=u))
    return entry(u, name, typ="unit", cost=75 - 4 * 15, cats=[foc(HS, "Heavy Support", u)],
                 infolinks=rules_links(["Legiones Astartes"], key=u),
                 entries=[sgt, marines, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          hardened],
                 groups=[heavy, take(u, "Squad Equipment (one only)", [("Legion Vexilla", 10), ("Nuncio Vox", 10)],
                                     max_total=1),
                         transports(u, u, ["Legion Rhino Armoured Carrier"])])


def predators():
    name = "Legion Predator Strike Squadron"
    u = uid("unit", name)
    toggle = uid(u, "troops")
    tog = entry(toggle, "Selected as Troops (Armoured Breakthrough)", constraints=[
        constraint(uid(toggle, "max"), "max", 1, auto=True),
        constraint(uid(toggle, "roster"), "max", 2, scope="force", deep=True)],
        mods=[modifier("set", "hidden", "true", conds=[cond(rite_id("Armoured Breakthrough"), "force", "lessThan", 1)]),
              modifier("set", uid(toggle, "max"), 0, conds=[cond(rite_id("Armoured Breakthrough"), "force", "lessThan",
                                                                     1)])])
    mods = [modifier("set-primary", "category", TROOPS, conds=[cond(toggle, "self", "atLeast", 1)]),
            modifier("add", "category", gs.CAT_LINE, conds=[cond(toggle, "self", "atLeast", 1)])]
    return squadron(name, 100, "Legion Predator",
                    lambda k, n: L.vehicle_profile(k, n, "Vehicle (Tank)", 4, 13, 11, 10), HS, "Heavy Support",
                    [], ["Searchlight", "Smoke Launchers"],
                    lambda mid: [slot(mid, "Replace Predator Cannon", "Predator Cannon", [
                        ("Twin-linked Lascannon", 20), ("Flamestorm Cannon", 15), ("Heavy Conversion Beamer", 35),
                        ("Magna-Melta", 45), ("Executioner Plasma Destroyer", 55)]),
                        take(mid, "Sponsons (one pair)", [("Heavy Bolter Sponsons", 10), ("Heavy Flamer Sponsons", 10),
                                                          ("Lascannon Sponsons", 25)], max_total=1),
                        *vehicle_upgrades(mid, STD_UPGRADES + [("Power of the Machine Spirit", 25)])],
                    unit_entries=[tog], extra_mods=mods)


def vindicators():
    return squadron("Legion Vindicator Siege Tank Squadron", 120, "Legion Vindicator",
                    lambda k, n: L.vehicle_profile(k, n, "Vehicle (Tank)", 4, 13, 11, 10), HS, "Heavy Support",
                    [], ["Combi-Bolter", "Searchlight", "Smoke Launchers"],
                    lambda mid: [slot(mid, "Replace Demolisher Cannon", "Demolisher Cannon",
                                      [("Laser Destroyer Array", 10)]),
                                 *vehicle_upgrades(mid, STD_UPGRADES + [("Power of the Machine Spirit", 25)])])


def count_error(u, text, lo=1, hi=3):
    return [modifier("add", "error", text, groups=[any_of(cond("model", u, "lessThan", lo),
                                                          cond("model", u, "greaterThan", hi))])]


def land_raider_squadron():
    name = "Legion Land Raider Battle Squadron"
    u = uid("unit", name)
    models = []
    for v in ["Land Raider Phobos", "Land Raider Proteus", "Land Raider Achilles"]:
        m = land_raider(v, typ="model", key=u + v)
        add_to(m, "constraints", [constraint(uid(m.get("id"), "max"), "max", 1 if "Achilles" in v else 3)])
        models += [m] if "Achilles" in v else numbered(m, 3, 0)
    return entry(u, name, typ="unit", cats=[foc(HS, "Heavy Support", u)],
                 mods=count_error(u, "A Land Raider Battle Squadron contains 1-3 Land Raiders."), entries=models)


def artillery_squadron():
    name = "Legion Artillery Tank Squadron"
    u = uid("unit", name)
    data = [("Legion Whirlwind", 75, (11, 11, 10), ["Whirlwind Launcher", "Twin-linked Bolter"]),
            ("Legion Basilisk", 140, (12, 10, 10), ["Earthshaker Cannon", "Heavy Bolter"]),
            ("Legion Medusa", 155, (12, 10, 10), ["Medusa Siege Gun", "Heavy Bolter"])]
    ids = [uid("model", u, n) for n, *_ in data]
    models = []
    for (n, cost, (f, s, r), kit), mid in zip(data, ids):
        others = [cond(c, u, "atLeast", 1) for o in ids if o != mid
                  for c in [o] + [uid(o, "copy", i) for i in (2, 3)]]
        groups = [take(mid, "Vehicle Upgrades", STD_UPGRADES[:4]),
                  take(mid, "Pintle-mounted Weapon", PINTLE, max_total=1)]
        if n == "Legion Whirlwind":
            groups.insert(0, take(mid, "Warheads", [("Hyperios Warheads", 0)]))
        models.append(entry(mid, n, typ="model", cost=cost,
                            constraints=[constraint(uid(mid, "max"), "max", 3)],
                            mods=[modifier("set", "hidden", "true", groups=[any_of(*others)]),
                                  modifier("set", uid(mid, "max"), 0, groups=[any_of(*others)])],
                            profiles=[L.vehicle_profile(u, n, "Vehicle (Tank)", 4, f, s, r)],
                            links=[gear(mid, k) for k in kit + ["Searchlight", "Smoke Launchers"]], groups=groups))
        models[-1:] = numbered(models[-1], 3, 0)
    return entry(u, "0-1 " + name, typ="unit", cats=[foc(HS, "Heavy Support", u)],
                 constraints=[constraint(uid(u, "force-max"), "max", 1, scope="force", deep=True)],
                 mods=count_error(u, "An Artillery Tank Squadron contains 1-3 vehicles, all of the same type."),
                 entries=models)


def single_vehicle(name, cost, prof, kit, rules_, groups_fn, cat_id=HS, cat_name="Heavy Support", mods=()):
    u = uid("unit", name)
    return entry(u, name, typ="unit", cost=cost, cats=[foc(cat_id, cat_name, u)], mods=list(mods),
                 profiles=[prof(u)], infolinks=rules_links(rules_, key=u),
                 links=[gear(u, k) for k in kit], groups=groups_fn(u))


def heavy_vehicles():
    out = []
    out.append(single_vehicle(
        "Legion Whirlwind Scorpius", 115,
        lambda u: L.vehicle_profile(u, "Whirlwind Scorpius", "Vehicle (Tank)", 4, 13, 12, 10),
        ["Scorpius Multi-launcher", "Twin-linked Bolter", "Searchlight", "Smoke Launchers"], ["Rocket Barrage"],
        lambda u: vehicle_upgrades(u, STD_UPGRADES[:3])))
    out.append(spartan(typ="hs"))
    out.append(single_vehicle(
        "Legion Sicaran Battle Tank", 185,
        lambda u: L.vehicle_profile(u, "Legion Sicaran", "Vehicle (Fast, Tank)", 4, 13, 12, 12),
        ["Twin-linked Accelerator Autocannon", "Extra Armour", "Searchlight", "Smoke Launchers"],
        ["Rapid Tracking"],
        lambda u: [slot(u, "Replace Heavy Bolter", "Heavy Bolter", [("Heavy Flamer", 0)]),
                   take(u, "Sponsons (one pair)", [("Heavy Bolter Sponsons", 10), ("Lascannon Sponsons", 25)],
                        max_total=1),
                   *vehicle_upgrades(u, [("Hunter-Killer Missile", 5), ("Dozer Blade", 5), ("Auxiliary Drive", 10),
                                         ("Armoured Ceramite", 20)])]))
    deredeo_u = uid("unit", "Deredeo Pattern Dreadnought")
    out.append(single_vehicle(
        "Deredeo Pattern Dreadnought", 185,
        lambda u: walker_profile(u, "Deredeo Dreadnought", 4, 5, 6, 13, 12, 11, 4, 1),
        ["Extra Armour", "Searchlight", "Smoke Launchers"],
        ["Atomantic Shielding", "Helical Targeting Array"],
        lambda u: [slot(u, "Main Weapon", "Anvilus Autocannon Battery", [("Hellfire Plasma Cannonade", 35),
                                                                         ("Arachnus Heavy Lascannon Battery", 50)]),
                   slot(u, "Secondary Weapon", "Twin-linked Heavy Bolter", [("Twin-linked Heavy Flamer", 0)]),
                   take(u, "Upgrades", [("Armoured Ceramite", 20)]),
                   take(u, "Carapace System (one)", [("Aiolos Missile Launcher", 35), ("Atomantic Pavaise", 50)],
                        max_total=1)]))
    out.append(single_vehicle(
        "Sicaran Venator Tank Destroyer", 190,
        lambda u: L.vehicle_profile(u, "Sicaran Venator", "Vehicle (Fast, Tank)", 4, 13, 12, 12),
        ["Neutron Beam Laser", "Heavy Bolter", "Extra Armour", "Searchlight", "Smoke Launchers"], [],
        lambda u: [take(u, "Sponsons (one pair)", [("Heavy Bolter Sponsons", 20), ("Lascannon Sponsons", 40)],
                        max_total=1),
                   *vehicle_upgrades(u, [("Hunter-Killer Missile", 5), ("Dozer Blade", 5), ("Auxiliary Drive", 10),
                                         ("Armoured Ceramite", 20)])]))
    out.append(single_vehicle(
        "Achilles-Alpha Pattern Land Raider", 300,
        lambda u: L.vehicle_profile(u, "Achilles-Alpha", "Vehicle (Tank, Transport)", 4, 14, 14, 14),
        ["Quad Launcher with Frag and Shatter Shells", "Twin-linked Volkite Culverin", "Extra Armour", "Searchlight",
         "Smoke Launchers"],
        ["Power of the Machine Spirit", "Enhanced Ferromantic Rites", "Galvanic Traction Drive"],
        lambda u: [take(u, "Quad Launcher Shells", [("Incendiary Shells", 5), ("Splinter Shells", 10),
                                                    ("Phosphex Canister Shot", 20)],
                        hide=None)]))
    # Achilles-Alpha has TWO twin-linked volkite culverins, and phosphex needs a Siege Breaker
    aa = out[-1]
    for lk in aa.iter("entryLink"):
        if lk.get("name") == "Twin-linked Volkite Culverin":
            for c in lk.iter("constraint"):
                c.set("value", "2")
        if lk.get("name") == "Phosphex Canister Shot":
            add_mods(lk, [modifier("set", "hidden", "true", conds=[cond(SIEGE_BREAKER, "force", "lessThan", 1)])])
    lev = "Leviathan Siege Dreadnought"
    lu = uid("unit", lev)

    def lev_groups(u):
        claw = lambda arm: entry(uid(u, arm, "claw"), "Leviathan Siege Claw with Meltagun",
                                 links=[gear(uid(u, arm, "claw"), "Leviathan Siege Claw with Meltagun")])
        opts = [("Leviathan Siege Drill with Meltagun", 5), ("Leviathan Storm Cannon", 10),
                ("Cyclonic Melta Lance", 20), ("Grav-flux Bombard", 20)]
        return [slot(u, "Arm 1", None, opts, default_is_entry=claw("1")),
                slot(u, "Arm 2", None, opts, default_is_entry=claw("2")),
                slot(u, "Heavy Flamer 1", "Heavy Flamer", [("Twin-linked Volkite Caliver", 5)]),
                slot(u, "Heavy Flamer 2", "Heavy Flamer", [("Twin-linked Volkite Caliver", 5)]),
                take(u, "Upgrades", [("Phosphex Discharger", 15), ("Armoured Ceramite", 20)]),
                group(uid("grp", u, "transport"), "Dedicated Transport",
                      links=[link(uid("link", uid("grp", u, "transport"), "dp"), T["Legion Dreadnought Drop Pod"],
                                  "Legion Dreadnought Drop Pod")],
                      constraints=[constraint(uid("grp", u, "transport", "max"), "max", 1, auto=True)])]
    lprof = walker_profile(lu, lev, 5, 5, 8, 13, 13, 12, 4, 4)
    ranged = ["Leviathan Storm Cannon", "Cyclonic Melta Lance", "Grav-flux Bombard"]
    lprof.insert(0, wrap("modifiers", [modifier("decrement", gs.char_id("Walker", "A"), 1,
                                                repeats=[repeat(W(r), lu, 1)]) for r in ranged]))
    out.append(entry(lu, lev, typ="unit", cost=270, cats=[foc(HS, "Heavy Support", lu)], profiles=[lprof],
                     infolinks=rules_links(["Reinforced Atomantic Shielding", "Crushing Charge", "Move Through Cover"],
                                           key=lu),
                     links=[gear(lu, k) for k in ["Extra Armour", "Frag Grenades", "Searchlight", "Smoke Launchers"]],
                     groups=lev_groups(lu)))
    return out


# ------------------------------------------------------------ Rites of War
def rites_entry():
    master = [cond(gs.CAT_MASTER, "force", "atLeast", 1), cond(L.consul_id("Delegatus"), "force", "atLeast", 1)]
    no_master = all_of(*[_negate(c) for c in master])
    fa_limit = ["Armoured Breakthrough", "Legion Breacher Company", "Fury of the Ancients"]
    hs_limit = ["Legion Assault Company", "Legion Destroyer Company", "Sky Hunter Phalanx"]
    ents = []
    tactical = uid("unit", "Legion Tactical Squad")
    for name, text in RITES.items():
        rid = rite_id(name)
        mods = []
        if name == "Legion Tactical Company":
            mods.append(modifier("add", "error", "Legion Tactical Company: the army must include at least three Legion "
                                                 "Tactical Squads.", conds=[cond(tactical, "force", "lessThan", 3)]))
        if name == "Legion Recon Company":
            mods.append(modifier("add", "error", "Legion Recon Company: no model may wear Terminator Armour or "
                                                 "Cataphractii Terminator Armour.",
                                 groups=[any_of(cond(W("Terminator Armour"), "force", "atLeast", 1),
                                                cond(W("Cataphractii Terminator Armour"), "force", "atLeast", 1))]))
        if name == "Sky Hunter Phalanx":
            mods.append(modifier("add", "error", "Sky Hunter Phalanx: the army may not include Castraferrum (Legion) or "
                                                 "Contemptor Dreadnoughts.",
                                 groups=[any_of(cond(uid("unit", "Legion Dreadnought"), "force", "atLeast", 1),
                                                cond(uid("unit", "Legion Contemptor Dreadnought"), "force",
                                                     "atLeast", 1))]))
        if name == "Legion Destroyer Company":
            mods.append(modifier("add", "error", "Legion Destroyer Company: the army must include at least one Moritat.",
                                 conds=[cond(L.consul_id("Moritat"), "force", "lessThan", 1)]))
        if name == "Primarch's Chosen":
            mods.append(modifier("add", "error", "Primarch's Chosen: the army must include the Primarch of its Legion.",
                                 conds=[cond(gs.CAT_PRIMARCH, "force", "lessThan", 1)]))
            mods.append(modifier("add", "error", "Primarch's Chosen: the army must contain at least 1,500 points.",
                                 conds=[cond("any", "roster", "lessThan", 1500, field=PTS, deep=False)]))
        if name == "Fury of the Ancients":
            mods.append(modifier("add", "error", "Fury of the Ancients: the army must include at least one Techmarine.",
                                 conds=[cond(TECHMARINE_COVENANT, "force", "lessThan", 1)]))
        for m in mods:  # an error only applies while this Rite is the one chosen
            cs = m.find("conditions")
            if cs is None:
                cs = el("conditions")
                m.insert(0, cs)
            cs.append(cond(rid, "force", "atLeast", 1))
        ents.append(entry(rid, name, rules=[rule(uid("rite-rule", name), name, text)], mods=mods))
    gid = uid("grp", "rites")
    root_mods = [modifier("add", "error", "A Rite of War requires a model with Master of the Legion (Legion Praetor or "
                                          "Delegatus Consul) in the Detachment.", groups=[no_master])]
    for n in fa_limit:
        root_mods.append(modifier("add", "category", gs.CAT_LIMIT_FA, conds=[cond(rite_id(n), "self", "atLeast", 1)]))
    for n in hs_limit:
        root_mods.append(modifier("add", "category", gs.CAT_LIMIT_HS, conds=[cond(rite_id(n), "self", "atLeast", 1)]))
    return entry(RITE_ENTRY, "Rite of War", cats=[category_link(gs.CAT_CONFIG, "Configuration", primary=True,
                                                               key="rite")],
                 constraints=[constraint(uid(RITE_ENTRY, "max"), "max", 1, scope="force", deep=True)], mods=root_mods,
                 groups=[group(gid, "Rite of War", entries=ents, constraints=[
                     constraint(uid(gid, "min"), "min", 1, auto=True), constraint(uid(gid, "max"), "max", 1,
                                                                                  auto=True)])])


def dedupe_kit(root):
    """A model's standard wargear that also appears as the default of a 'Replace X' choice is only kept
    in the choice (otherwise it would be counted twice)."""
    for e in root.iter("selectionEntry"):
        groups = e.find("selectionEntryGroups")
        links = e.find("entryLinks")
        if groups is None or links is None:
            continue
        defaults = set()
        for g in groups:
            d = g.get("defaultSelectionEntryId")
            gl = g.find("entryLinks")
            if d and gl is not None:
                defaults |= {lk.get("targetId") for lk in gl if lk.get("id") == d}
        for lk in list(links):
            if lk.get("targetId") in defaults:
                links.remove(lk)


# ---------------------------------------------------------------- assemble
def extend(units_by_name, shared):
    """Attach retinues / new options to slice-1 entries and return (root units, shared entries)."""
    praetor = units_by_name["Legion Praetor"]
    centurion = units_by_name["Legion Centurion"]
    add_to(praetor, "selectionEntryGroups", [retinue_group("praetor", L.PRAETOR, True)])
    add_to(centurion, "selectionEntryGroups", [retinue_group("centurion", L.CENTURION, False)])
    # Sky Hunter Phalanx: Jetbike upgrade for Independent Characters on bikes
    for key, e in [("praetor", praetor), ("centurion", centurion)]:
        jid = uid(key, "jetbike")
        add_to(e, "selectionEntries", [entry(
            jid, "Upgrade Bike to Jetbike (Sky Hunter Phalanx)", cost=5,
            constraints=[constraint(uid(jid, "max"), "max", 1, auto=True)],
            mods=[modifier("set", "hidden", "true", groups=[any_of(cond(rite_id("Sky Hunter Phalanx"), "force",
                                                                        "lessThan", 1),
                                                                   lacks(W("Space Marine Bike"), e.get("id")))]),
                  modifier("set", uid(jid, "max"), 0, groups=[any_of(cond(rite_id("Sky Hunter Phalanx"), "force",
                                                                          "lessThan", 1),
                                                                     lacks(W("Space Marine Bike"), e.get("id")))])],
            rules=[rule(uid(jid, "r"), "Jetbike", "The model follows the normal ProHammer rules for Jetbikes. A model "
                                                  "may not combine a Jetbike with a Bike, Jump Pack or Terminator "
                                                  "Armour.")])])
    # Master of Signals may take a Damocles Command Rhino as a Dedicated Transport
    for e in centurion.iter("selectionEntry"):
        if e.get("id") == L.consul_id("Master of Signals"):
            gid = uid("grp", "mos", "transport")
            add_to(e, "selectionEntryGroups", [group(gid, "Dedicated Transport", links=[
                link(uid("link", gid, "damocles"), T["Damocles Command Rhino"], "Damocles Command Rhino")],
                constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])])
    # Rites of War on slice-1 Troops
    for n in ["Legion Tactical Squad", "Legion Assault Squad", "Legion Breacher Siege Squad",
              "Legion Reconnaissance Squad"]:
        add_mods(units_by_name[n], troop_role_mods(n))
    # new transport options (Land Raiders for Breachers, rite transports for everyone)
    tac, bre, rec = (units_by_name[n] for n in ["Legion Tactical Squad", "Legion Breacher Siege Squad",
                                                 "Legion Reconnaissance Squad"])
    for e, opts, mx in [(tac, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                               "Anvillus Pattern Dreadclaw Drop Pod"], 10),
                        (bre, ["Land Raider Phobos", "Land Raider Proteus"], 10),
                        (rec, ["Legion Rhino Armoured Carrier"], None)]:
        grps = e.find("selectionEntryGroups")
        for g in list(grps):
            if g.get("name") == "Dedicated Transport":
                grps.remove(g)
        grps.append(transports(e.get("id"), e.get("id"), opts, max_models=mx))
    # Assault Company: compulsory Assault Squads may not remove Jump Packs (they cannot in this builder anyway)
    roots = [
        rites_entry(),
        damocles("hq"),
        veteran_squad(), terminator_squad(), destroyer_squad(), techmarine_covenant(),
        dreadnought("Legion Dreadnought", 105, (4, 4, 6, 12, 12, 10, 4, 2), DREAD_ARM1, DREAD_ARM2, [],
                    [("Extra Armour", 5), ("Frag Assault Launchers", 15), ("Armoured Sarcophagus", 20),
                     ("Veteran Pilot", 20), ("Hunter-Killer Missile", 5, 2), ("Havoc Launcher", 15)]),
        dreadnought("Legion Contemptor Dreadnought", 155, (5, 5, 7, 13, 12, 10, 4, 2), CONT_ARM1, CONT_ARM2,
                    ["Atomantic Shielding", "Fleet"], [("Extra Armour", 5), ("Havoc Launcher", 15)]),
        rapier_battery(),
        seeker_squad(), bike_squadron(), sky_hunters(), attack_bikes(), land_speeders(), javelins(),
        heavy_support_squad(), predators(), vindicators(), land_raider_squadron(), artillery_squadron(),
        *heavy_vehicles(),
    ]
    for r in roots:
        dedupe_kit(r)
    for e in (praetor, centurion):
        dedupe_kit(e)
    for e in RETINUE_SHARED:
        dedupe_kit(e)
    new_shared = RETINUE_SHARED + [land_raider("Land Raider Phobos"), land_raider("Land Raider Proteus"), dread_drop_pod(),
                  spartan("unit"), damocles("transport")]
    return roots, new_shared
