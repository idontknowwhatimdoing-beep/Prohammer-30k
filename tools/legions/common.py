"""Shared building blocks for the Legion modules (Forces of the Legions).

Every Legion has its own catalogue: the full Legiones Astartes army list plus that Legion's module in this
folder. A module defines

    LEGION = "XV - Thousand Sons"          # exactly as in legiones_wargear.LEGIONS

    def register():                        # optional - runs BEFORE the army list is built
        register_data(rules={...}, weapons={...}, weapon_rules={...}, wargear={...})
        # may also change legiones2.TROOP_RITES / NOT_LINE_UNDER / RITES etc.

    def extend(ctx):                       # runs AFTER the standard army list is built
        ctx.legion_rules([...])            # Legion special rules (shown on the Legion configuration entry)
        ctx.add_units(...)                 # new root units (anything the player can add to the army)
        ctx.add_shared(...)                # new non-root shared entries (retinues, transports, ...)
        ctx.unit("Legion Praetor")         # existing entries to modify
        ctx.add_rite("Name", "text", ...)  # Legion Rites of War

Because every Legion catalogue only contains its own Legion, nothing needs to be hidden behind
"is this Legion" conditions any more.
"""
import copy

from bsx import (PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group,
                 info_link, category_link, hide_if)
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, TDA, has_tda, no_tda, gear, per_model, rules_links, unit_profile, rule_ref
from legiones import psychic_powers, power_entry, powers_group, power_rule, PSY, negate
from legiones2 import (slot, take, pool, choice, transports, add_mods, add_to, dedupe_kit, walker_profile, foc,
                       rite_id, rite, any_rite, RETINUE_SHARED, TROOPS, ELITES, FA, HQ, HS, _negate, model_swaps,
                       model_takes, model_pair_claws, numbered, specials_decrement, standard_choice, armour_pattern,
                       tda_armoury, pa_armoury, vehicle_upgrades, STD_UPGRADES, PINTLE, squadron, single_vehicle)
from legiones_wargear import ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR, RITES

LOW = gs.cat("Lords of War")
LOYALIST, TRAITOR = L.LOYALIST, L.TRAITOR


# ------------------------------------------------------------------ data
def register_data(rules=None, weapons=None, weapon_rules=None, wargear=None, multi_profile=None):
    """Add army-book data before anything is built.

    rules:         {rule name: text}
    weapons:       {weapon name: (range, S, AP, type)}  - one profile, entry of the same name
    multi_profile: {entry name: {profile name: (range, S, AP, type)}} - e.g. a weapon with two firing modes
    weapon_rules:  {weapon name: [rule names]}  (army rules or core USRs)
    wargear:       {item name: text} or {item name: (text, [core rule names])}
    """
    ARMY_RULES.update(rules or {})
    for n, prof in (weapons or {}).items():
        WEAPON_PROFILES[n] = prof
        WEAPONS[n] = [n]
    for n, profs in (multi_profile or {}).items():
        WEAPON_PROFILES.update(profs)
        WEAPONS[n] = list(profs)
    WEAPON_RULES.update(weapon_rules or {})
    for n, t in (wargear or {}).items():
        WARGEAR[n] = t if isinstance(t, tuple) else (t, [])


# ------------------------------------------------------------------ small helpers
def unique(eid, n=1):
    """At most n per army (e.g. named characters)."""
    return constraint(uid(eid, "unique"), "max", n, scope="roster", deep=True)


def force_limit(eid, n=1):
    """'0-n per Detachment'."""
    return constraint(uid(eid, "force-max"), "max", n, scope="force", deep=True)


def min_points_error(name, points):
    return modifier("add", "error", f"{name} may only be included in an army of {points:,} points or more.",
                    conds=[cond("any", "roster", "lessThan", points, field=PTS, deep=False)])


def allegiance_only(e, loyalist):
    """Loyalist-only / Traitor-only entry: error if the army has the other Allegiance."""
    other = TRAITOR if loyalist else LOYALIST
    add_mods(e, [modifier("add", "error", f"{e.get('name')} is {'Loyalist' if loyalist else 'Traitor'} only.",
                          conds=[cond(other, "roster", "atLeast", 1)])])
    return e


def option(key, name, cost, hide=None, per_model_unit=None, item=None, max_=1, rules_=()):
    """Optional purchase of a shared wargear item (item defaults to name). per_model_unit: cost per model."""
    eid = uid("opt", key, name)
    mods = []
    if hide:
        mods += [modifier("set", "hidden", "true", groups=[any_of(*hide)]),
                 modifier("set", uid(eid, "max"), 0, groups=[any_of(*hide)])]
    cost_val = cost
    if per_model_unit:
        cost_val = 0
        mods.append(modifier("increment", PTS, cost, repeats=[repeat("model", per_model_unit, 1)]))
    links = [gear(eid, item or name)] if (item or name) in WEAPONS or (item or name) in WARGEAR else []
    return entry(eid, name, cost=cost_val, mods=mods,
                 constraints=[constraint(uid(eid, "max"), "max", max_, auto=True)],
                 links=links, infolinks=rules_links(list(rules_), key=eid))


def upgrade(key, name, cost, rules_=(), text=None, hide=None, max_=1, links=()):
    """An inline upgrade entry that just grants special rules (and optionally wargear links)."""
    eid = uid("upg", key, name)
    mods = []
    if hide:
        mods += [modifier("set", "hidden", "true", groups=[any_of(*hide)]),
                 modifier("set", uid(eid, "max"), 0, groups=[any_of(*hide)])]
    return entry(eid, name, cost=cost, mods=mods, constraints=[constraint(uid(eid, "max"), "max", max_, auto=True)],
                 infolinks=rules_links(list(rules_), key=eid),
                 rules=[rule(uid(eid, "r"), name, text)] if text else [],
                 links=[gear(eid, k) for k in links])


def clone(e, salt, strip_cats=True, new_name=None):
    """Deep copy of an entry with every internal id renamed (e.g. a normal unit used as a retinue)."""
    c = copy.deepcopy(e)
    ids = {x.get("id") for x in c.iter() if x.get("id")}
    for x in c.iter():
        for a in ("id", "targetId", "childId", "scope", "field", "defaultSelectionEntryId", "value"):
            v = x.get(a)
            if v in ids:
                x.set(a, uid(salt, v))
    if strip_cats:
        cl = c.find("categoryLinks")
        if cl is not None:
            c.remove(cl)
    if new_name:
        c.set("name", new_name)
    return c


def retinue_links(key, entries, title="Retinue (no Force Organisation slot)"):
    """A 0-1 retinue choice for a character. The retinue entries become shared entries automatically."""
    gid = uid("grp", key, "retinue")
    RETINUE_SHARED.extend(e for e in entries if e not in RETINUE_SHARED)
    return group(gid, title, links=[link(uid("link", gid, e.get("id")), e.get("id"), e.get("name")) for e in entries],
                 constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


def command_squad_for(char_key, char_id, extra_entries=()):
    cs = L2.command_squad(char_key, char_id)
    if extra_entries:
        add_to(cs, "selectionEntries", list(extra_entries))
    return cs


def replace_group_options(e, group_name, new_options):
    """Add options [(name, pts)] (shared items) to every selectionEntryGroup called group_name inside e."""
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == group_name:
            links = g.find("entryLinks")
            if links is None:
                links = el("entryLinks")
                g.append(links)
            for n, p in new_options:
                links.append(link(uid("link", g.get("id"), n), W(n), n, cost=p or None))


def add_weapon_variant(roots, base_name, new_name, extra_cost, hide=None, done=None):
    """Wherever `base_name` can be chosen from a weapon group (link to the shared item), also offer `new_name` for the
    same cost + extra_cost (e.g. 'Calibanite Warblade - Power Weapon +10'). Returns the number of groups changed."""
    base = W(base_name)
    done = done if done is not None else set()
    n = 0
    for r in roots:
        for g in list(r.iter("selectionEntryGroup")):
            key = (id(g), new_name)
            if key in done:
                continue
            done.add(key)
            links = g.find("entryLinks")
            if links is None:
                continue
            for lk in list(links):
                if lk.get("targetId") != base:
                    continue
                cost = 0
                cs = lk.find("costs")
                if cs is not None and len(cs):
                    cost = float(cs[0].get("value"))
                nid = uid(lk.get("id"), "variant", new_name)
                mods = [modifier("set", "hidden", "true", groups=[any_of(*hide)])] if hide else None
                new = link(nid, W(new_name), new_name, cost=int(cost + extra_cost) or None, mods=mods)
                if g.get("defaultSelectionEntryId") is not None:
                    new.set("sortIndex", str(int(lk.get("sortIndex") or 1) + 100))
                links.append(new)
                n += 1
    return n


# ------------------------------------------------------------------ characters
def named_character(legion_rule, name, cost, stats, kit, rules_, retinue=None, master=True, min_points=None,
                    extra_groups=(), extra_entries=(), unit_type="Infantry (Character)", loyalist=None,
                    compulsory=True, primary=None, profile_name=None, key=None):
    """A unique named HQ character. stats = (WS, BS, S, T, W, I, A, Ld, Sv)."""
    u = uid("unit", key or name)
    cats = [foc(primary or HQ, "HQ" if primary in (None, HQ) else "Elites", u)]
    if compulsory:
        cats.append(category_link(gs.CAT_COMMANDER, "Compulsory HQ Eligible", key=u))
    if master:
        cats.append(category_link(gs.CAT_MASTER, "Master of the Legion", key=u))
    mods = []
    if min_points:
        mods.append(min_points_error(name, min_points))
    groups = list(extra_groups)
    if retinue is not None:
        groups.append(retinue)
    e = entry(u, name, typ="unit", cost=cost, cats=cats, mods=mods, constraints=[unique(u)],
              profiles=[unit_profile(u, profile_name or name, unit_type, *stats)],
              infolinks=rules_links([legion_rule, "Independent Character"] +
                                    (["Master of the Legion"] if master else []) + list(rules_), key=u),
              links=[gear(u, k) for k in kit], groups=groups, entries=list(extra_entries))
    if loyalist is not None:
        allegiance_only(e, loyalist)
    return e


PRIMARCH_RULES = {
    "Primarch": (
        "Independent Character, Eternal Warrior, Fear, Fearless, Adamantium Will, Fleet, It Will Not Die and Master of the "
        "Legion; automatically passes Fear tests caused by another Primarch; has the named Legiones Astartes rule of his "
        "Legion. FIELDING A PRIMARCH: selected as a Lord of War; no more than one Primarch per army; normally only in "
        "armies of 2,000 points or more; only for a Detachment of his own Legion, never an Allied Detachment; must be the "
        "army's Warlord; counts towards the Master of the Legion limit; may not purchase wargear, Consul upgrades or other "
        "character upgrades unless his entry permits it."),
    "Supreme Commander": ("A Primarch must be the army's Warlord even though he is a Lord of War. He does not roll for or "
                          "select a normal Warlord Trait; any command ability is in his own entry."),
    "Sire of the Legion": (
        "A Primarch may only join units with the same named Legiones Astartes rule (or his own bodyguard/retinue). He counts "
        "as a member of his Legion for rules referring to friendly models of that Legion, but does not automatically gain "
        "the Legion Special Rules unless his profile says so."),
    "Primarch Retinue": ("A Primarch may select one Legion Honour Guard Squad (or a Legion-specific bodyguard where his "
                         "entry permits) as a retinue without occupying an additional selection. They need not deploy or "
                         "stay together."),
    "Primarchs and Transports": "A Primarch counts as two models for Transport Capacity.",
    "The Price of Failure": ("If an enemy Primarch is destroyed, the opposing player gains +1 Victory Point in addition to "
                             "any Victory Points for destroying that model or the enemy Warlord."),
    "The Clash of Demigods": (
        "At the start of any Assault phase, if two opposing Primarchs are within 12\" of one another (and neither is "
        "embarked), the active player's Primarch issues a Primarch Challenge. If accepted, both leave their units and fight "
        "a Primarch Duel at a suitable location until one is slain (the Challenger counts as charging in the first round; "
        "no other models may interfere; see Forces of the Legions for the full rules). If refused, the Challenger's player "
        "gains +2 Victory Points and the refusing Primarch may not attack the Challenger that Assault phase."),
    "Primarch Armour": ("Confers a 1+ Armour Save and a 4+ Invulnerable Save. A natural roll of 1 always fails; even AP1 "
                        "attacks merely impact the armour as normal."),
    "Daemon Primarchs": (
        "A Daemon Primarch is a separate version of that Primarch; an army may never include both forms. Unless stated "
        "otherwise it uses only its own rules, but counts as a Primarch for rules referring to Primarch models."),
}
PRIMARCH_CORE = ["Primarch", "Supreme Commander", "Sire of the Legion", "Primarch Retinue", "Primarchs and Transports",
                 "The Price of Failure", "The Clash of Demigods"]


def primarch_mods(other=None, chosen_ok=True, other_text="An army may never include both forms of this Primarch."):
    mods = []
    small = [cond("any", "roster", "lessThan", 2000, field=PTS, deep=False)]
    if chosen_ok:
        mods.append(modifier("add", "error", "A Primarch may normally only be included in an army of 2,000 points or "
                                             "more (1,500 with the Primarch's Chosen Rite of War).",
                             conds=small + [cond(rite_id("Primarch's Chosen"), "force", "lessThan", 1)]))
    else:
        mods.append(modifier("add", "error", "A Primarch may only be included in an army of 2,000 points or more.",
                             conds=small))
    mods.append(modifier("add", "error", "An army may never include more than one Primarch.",
                         conds=[cond(gs.CAT_PRIMARCH, "roster", "greaterThan", 1)]))
    if other:
        mods.append(modifier("add", "error", other_text, conds=[cond(other, "roster", "atLeast", 1)]))
    # Primarch's Chosen: the Primarch fulfils the compulsory HQ
    mods.append(modifier("add", "category", gs.CAT_COMMANDER,
                         conds=[cond(rite_id("Primarch's Chosen"), "force", "atLeast", 1)]))
    return mods


def primarch(legion_rule, name, cost, stats, kit, rules_, retinue=None, other=None, unit_type="Infantry (Character)",
             loyalist=None, extra_groups=(), extra_entries=(), extra_mods=(), key=None, profile_name=None,
             chosen_ok=True, core=True):
    """A Primarch (Lord of War, Master of the Legion, unique). stats = (WS, BS, S, T, W, I, A, Ld, Sv).
    retinue: a group from primarch_retinue()/retinue_links(); kit: fixed wargear names."""
    u = uid("unit", key or name)
    groups = list(extra_groups)
    if retinue is not None:
        groups.append(retinue)
    rl = (PRIMARCH_CORE if core else []) + [legion_rule] + list(rules_)
    e = entry(u, name, typ="unit", cost=cost, mods=primarch_mods(other, chosen_ok) + list(extra_mods),
              cats=[foc(LOW, "Lords of War", u), category_link(gs.CAT_MASTER, "Master of the Legion", key=u),
                    category_link(gs.CAT_PRIMARCH, "Primarch", key=u)],
              constraints=[unique(u)],
              profiles=[unit_profile(u, profile_name or name.split(",")[0], unit_type, *stats)],
              infolinks=rules_links(rl, key=u), links=[gear(u, k) for k in kit], groups=groups,
              entries=list(extra_entries))
    if loyalist is not None:
        allegiance_only(e, loyalist)
    return e


def primarch_retinue(key, extra=(), honour_guard=True, terminators=True):
    """The standard Primarch retinue choice (Honour Guard / Terminator Command Squad) plus Legion bodyguards."""
    ents = []
    if honour_guard:
        ents.append(L2.honour_guard(key))
    if terminators:
        ents.append(L2.terminator_command_squad(key))
    ents += list(extra)
    return retinue_links(key, ents, title="Primarch Retinue")


def register_primarch_rules():
    for k, v in PRIMARCH_RULES.items():
        ARMY_RULES.setdefault(k, v)


register_primarch_rules()


# ------------------------------------------------------------------ context
class Context:
    """Handed to a Legion module's extend(ctx)."""

    def __init__(self, legion, units, shared):
        self.legion = legion
        self.legion_id = uid("legion", legion)
        self.units = units          # root entries (the player can add these)
        self.shared = shared        # other shared entries (transports, retinues, ...)
        self._retinue_start = len(RETINUE_SHARED)

    # lookups
    def unit(self, name):
        """An existing root or shared entry by name (e.g. 'Legion Praetor', 'Legion Tactical Squad')."""
        for e in self.units + self.shared + RETINUE_SHARED:
            if e.get("name") == name:
                return e
        raise KeyError(name)

    def all_entries(self):
        return self.units + self.shared + list(RETINUE_SHARED)

    def retinues(self, name=None):
        return [e for e in RETINUE_SHARED if name is None or e.get("name") == name]

    # additions
    def add_units(self, *entries):
        for e in entries:
            dedupe_kit(e)
            self.units.append(e)

    def add_shared(self, *entries):
        for e in entries:
            dedupe_kit(e)
            self.shared.append(e)

    def legion_rules(self, names, force_org=None):
        """Show the Legion's special rules on the Legion configuration entry.
        force_org: iterable of gamesystem categories applied to the Detachment (e.g. gs.CAT_HQ_PLUS1)."""
        legion = self.unit("Legion")
        for e in legion.iter("selectionEntry"):
            if e.get("id") == self.legion_id:
                add_to(e, "infoLinks", rules_links(list(names), key=self.legion_id + "rules"))
        if force_org:
            add_mods(legion, [modifier("add", "category", c) for c in force_org])

    def add_rite(self, name, text, mods=(), limit_fa=False, limit_hs=False, errors=()):
        """A Legion-specific Rite of War. errors: [(text, conds)] shown while the rite is chosen and conds are true."""
        rites = self.unit("Rite of War")
        rg = rites.find("selectionEntryGroups")[0]
        rid = rite_id(name)
        m = list(mods)
        for txt, conds in errors:
            m.append(modifier("add", "error", f"{name}: {txt}",
                              conds=[cond(rid, "force", "atLeast", 1)] + list(conds)))
        add_to(rg, "selectionEntries", [entry(rid, f"{name} ({self.legion.split(' - ', 1)[1]})",
                                              rules=[rule(uid("rite-rule", name), name, text)], mods=m)])
        if limit_fa:
            add_mods(rites, [modifier("add", "category", gs.CAT_LIMIT_FA, conds=[cond(rid, "self", "atLeast", 1)])])
        if limit_hs:
            add_mods(rites, [modifier("add", "category", gs.CAT_LIMIT_HS, conds=[cond(rid, "self", "atLeast", 1)])])
        return rid

    def finish(self):
        for r in RETINUE_SHARED[self._retinue_start:]:
            dedupe_kit(r)
            if r not in self.shared:
                self.shared.append(r)


# ------------------------------------------------------------------ common Legion patterns
def required_choice(key, title, options, required=True, fixed=None, hide=None):
    """Exactly-one choice made on a unit when the army is built (Wings, Cults, Chapters, Tactics...).
    options: [(name, [rule names])]. Missing choice shows an error instead of New Recruit auto-picking one.
    fixed: name of the only allowed option (others hidden) for units with a predetermined choice."""
    gid = uid("grp", key, title)
    ents = []
    for n, rls in options:
        eid = uid("choice", key, title, n)
        mods = []
        if fixed and n != fixed:
            mods = [modifier("set", "hidden", "true"), modifier("set", uid(eid, "max"), 0)]
        ents.append(entry(eid, n, infolinks=rules_links(list(rls), key=eid), mods=mods,
                          constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)]))
    cons = [constraint(uid(gid, "max"), "max", 1, auto=True)]
    mods = []
    if required:
        none = all_of(*[cond(e.get("id"), "parent", "lessThan", 1) for e in ents])
        mods.append(modifier("add", "error", f"Choose a {title}.", groups=[none]))
    if hide:
        mods += [modifier("set", "hidden", "true", groups=[any_of(*hide)])]
    default = uid("choice", key, title, fixed) if fixed else None
    return group(gid, title, entries=ents, constraints=cons, mods=mods, default=default)


def choice_id(key, title, name):
    """Id of an option created by required_choice (for conditions)."""
    return uid("choice", key, title, name)


def legion_units(ctx, include_vehicles=True):
    """Root units of the army (not configuration entries, Rites of War or Primarchs)."""
    skip = {"Legion", "Allegiance", "Rite of War"}
    out = []
    for e in ctx.units:
        if e.get("name") in skip:
            continue
        if not include_vehicles:
            profs = [p.get("typeName") for p in e.iter("profile")]
            if profs and all(t in ("Vehicle", "Walker", "Weapon", "Transport") for t in profs):
                continue
        out.append(e)
    return out


def add_consul(ctx, name, cost, rules_, kit=(), options=(), groups_=(), forbids=(), support_officer=False,
               psyker=False, replaces=()):
    """A Legion-specific Consul type for the Legion Centurion.
    forbids: Armoury item names the Consul may not take. replaces: kit names the Consul replaces (removed while the
    Consul is chosen, e.g. ['Chainsword'] adds nothing - use for documentation only)."""
    cen = ctx.unit("Legion Centurion")
    cid = L.consul_id(name)
    cgrp = None
    for g in cen.iter("selectionEntryGroup"):
        if g.get("name") == "Legion Consul (max one)":
            cgrp = g
    ce = entry(cid, f"{name} Consul", cost=cost, constraints=[constraint(uid(cid, "max"), "max", 1)],
               infolinks=rules_links(list(rules_), key=cid), links=[gear(cid, k) for k in kit],
               entries=list(options), groups=list(groups_))
    add_to(cgrp, "selectionEntries", [ce])
    mods = [modifier("set", "name", f"Legion {name} Consul", conds=[has(cid, cen.get("id"))])]
    if support_officer:
        mods.append(modifier("remove", "category", gs.CAT_COMMANDER, conds=[has(cid, cen.get("id"))]))
    add_mods(cen, mods)
    # forbidden Armoury items / armour / mobility while this Consul is chosen
    if forbids:
        forbid_items(cen, forbids, [has(cid, cen.get("id"))])
    return cid


def forbid_items(unit, item_names, conds):
    """Hide and forbid the given shared items (anywhere inside unit) while any of conds is true."""
    targets = {W(n) for n in item_names}
    for lk in unit.iter("entryLink"):
        if lk.get("targetId") in targets:
            mx = None
            for c in lk.iter("constraint"):
                if c.get("type") == "max" and c.get("scope") == "parent":
                    mx = c.get("id")
            mods = [modifier("set", "hidden", "true", groups=[any_of(*conds)])]
            if mx:
                mods.append(modifier("set", mx, 0, groups=[any_of(*conds)]))
            add_mods(lk, mods)


def add_armoury_items(ctx, items, who=("praetor", "centurion", "sergeants"), hide=None):
    """Add Legion Armoury items [(name, pts)] to the Space Marine Armoury of characters.
    who: 'praetor' / 'centurion' -> the 'Additional Wargear' group inside their 100-pt Armoury;
         'sergeants' -> every 'Space Marine Armoury (max 50 pts)' group (Sergeants, Champions, ...).
    The items count towards the Armoury points cap."""
    targets = []
    if "praetor" in who or "centurion" in who:
        for n in ("Legion Praetor", "Legion Centurion"):
            if n.split()[-1].lower() in who:
                for g in ctx.unit(n).iter("selectionEntryGroup"):
                    if g.get("name") == "Space Marine Armoury (max 100 pts)":
                        for sub in g.iter("selectionEntryGroup"):
                            if sub.get("name") == "Additional Wargear":
                                targets.append(sub)
    if "sergeants" in who:
        for e in ctx.all_entries():
            for g in e.iter("selectionEntryGroup"):
                if g.get("name") == "Space Marine Armoury (max 50 pts)":
                    targets.append(g)
    seen = set()
    for g in targets:
        if id(g) in seen:
            continue
        seen.add(id(g))
        links = g.find("entryLinks")
        if links is None:
            links = el("entryLinks")
            g.append(links)
        for n, p in items:
            lid = uid("link", g.get("id"), "legion", n)
            mods = None
            if hide:
                mods = [modifier("set", "hidden", "true", groups=[any_of(*hide)])]
            links.append(link(lid, W(n), n, cost=p or None, mods=mods,
                              constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    return len(seen)


def add_group(e, g):
    add_to(e, "selectionEntryGroups", [g])


def add_entry(e, x):
    add_to(e, "selectionEntries", [x])
