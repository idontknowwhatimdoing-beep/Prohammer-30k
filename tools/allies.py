"""Allied Detachments and the Allies Matrix (Games in the Age of Darkness), applied to every catalogue.

ProHammer Classic: with both players' agreement an army may use several Detachments; one is the Primary Detachment,
each Detachment takes its units from one army list and fulfils its own compulsory selections. A second Detachment
from the same army list needs all Troops slots of the first filled.

In New Recruit every Detachment is a force in the roster:
* "Primary Detachment" (game system force entry, the former Standard Force Organisation Chart - same id),
* "Allied Detachment" (game system force entry, same chart),
* special allied charts defined by army books (Ruinstorm Allied Detachment, Covenant Detachment, Agents of the
  Sigillite) count as Allied Detachments.

Every catalogue's Allegiance entry (always present in a force) carries a marker category "Army: <army>" and, through
modifiers, "Detachment: Primary" / "Detachment: Allied". Roster-wide errors then enforce the matrix (Sworn Enemies),
a single Primary Detachment, mixed allegiances, Primarchs only in the Primary Detachment and Rites of War that forbid
Allied Detachments.
"""
import re

import gamesystem as gs
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, rule, category_link
from legiones2 import add_mods, add_to, RITE_ENTRY
import allies_matrix as AM

ALLEGIANCE_ENTRY = uid("cfg", "Allegiance")
LOYALIST = uid("cfg", "Loyalist")
TRAITOR = uid("cfg", "Traitor")

PRIMARY_FORCE = uid("force", "standard")
ALLIED_FORCE = uid("force", "allied")
CAT_PRIMARY = gs.cat("Detachment: Primary")
CAT_ALLIED = gs.cat("Detachment: Allied")
CAT_CUSTODES = gs.cat("Legio Custodes unit")
CAT_COMPANIONS = gs.cat("Companions of the Ten Thousand")
CAT_ALLIED_UNIT = gs.cat("Allied Detachment unit")
CAT_NO_CAP = gs.cat("No allied points limit")  # allied charts of army books without the 25% limit
NO_CAP_FORCES = {"Ruinstorm Allied Detachment"}

LEGIONS = {  # matrix abbreviation -> Legion
    "DA": "Dark Angels", "EC": "Emperor's Children", "WS": "White Scars", "SW": "Space Wolves",
    "IF": "Imperial Fists", "NL": "Night Lords", "BA": "Blood Angels", "IH": "Iron Hands", "WE": "World Eaters",
    "UM": "Ultramarines", "DG": "Death Guard", "TS": "Thousand Sons", "SOH": "Sons of Horus", "WB": "Word Bearers",
    "S": "Salamanders", "RG": "Raven Guard", "AL": "Alpha Legion", "IW": "Iron Warriors"}
ARMIES = {"ME": "Mechanicum", "EX": "Exercitus Imperialis", "Q": "Questoris Households", "SA": "Solar Auxilia",
          "D": "Daemons of the Ruinstorm", "BS": "The Lost and the Damned", "T": "Talons of the Emperor"}
# catalogue name -> matrix abbreviation (None: not in the matrix)
CATALOGUES = {"Legiones Astartes - " + n: a for a, n in LEGIONS.items()}
CATALOGUES.update({n: a for a, n in ARMIES.items()})
SHORT = {**LEGIONS, **ARMIES, "BS": "Blackshields (The Lost and the Damned)"}
# The side each army stands on in the matrix ("At the Height of the Heresy"). Author: a Legion fielded with the other
# allegiance swaps sides - enmities that only come from the Heresy's two sides no longer apply (Loyalist Sons of Horus
# may ally with Ultramarines). In a valid army every detachment has the same allegiance, so a Sworn Enemies pair whose
# canonical sides differ is either fine (one of them swapped sides) or already an allegiance error: only pairs on the
# same canonical side (or with an army without a side) are checked as Sworn Enemies.
TRAITOR_SIDE = {"EC", "IW", "NL", "WE", "DG", "TS", "SOH", "WB", "AL", "D"}
LOYAL_SIDE = {"DA", "WS", "SW", "IF", "BA", "IH", "UM", "S", "RG", "T"}


def side(abbr):
    return "T" if abbr in TRAITOR_SIDE else "L" if abbr in LOYAL_SIDE else None


def short_name(catalogue):
    return catalogue.replace("Legiones Astartes - ", "")


def army_cat(catalogue):
    return gs.cat("Army: " + short_name(catalogue))


def army_categories():
    """[(name, id)] for the game system."""
    out = [("Detachment: Primary", CAT_PRIMARY), ("Detachment: Allied", CAT_ALLIED),
           ("Legio Custodes unit", CAT_CUSTODES), ("Companions of the Ten Thousand", CAT_COMPANIONS),
           ("Allied Detachment unit", CAT_ALLIED_UNIT), ("No allied points limit", CAT_NO_CAP)]
    out += [("Allied Detachment units: " + short_name(c), allied_units_cat(c)) for c in CATALOGUES]
    out += [("Army: " + short_name(c), army_cat(c)) for c in CATALOGUES]
    return out


def relations():
    """{(abbr, abbr): 'A'|'C'|'S'} symmetric. A pair is Sworn Enemies if either cell says so; otherwise Conditional
    if either cell says so; a blank cell takes the other direction's value."""
    _, m = AM.matrix()
    m = {(a.upper(), b.upper()): v for (a, b), v in m.items()}
    out = {}
    for (a, b), v in m.items():
        w = m.get((b, a), "")
        # the Talons row (added last) disagrees with the Talons column in a few cells: the other army's row wins
        if a == "T" and b != "T":
            v = w or v
        elif b == "T" and a != "T":
            w = v or w
        both = {v, w} - {""}
        out[(a, b)] = "S" if "S" in both else "C" if "C" in both else "A" if "A" in both else ""
    return out


def sworn_pairs():
    rel = relations()
    return sorted({tuple(sorted(p)) for p, v in rel.items() if v == "S"})


# ------------------------------------------------------------------ game system
EXTRA_RULES = [
    ("Multiple Detachments", "If both players agree before the game, players may use multiple detachments: one "
     "detachment must be designated as the first and primary detachment; each detachment may only take units from a "
     "single codex book unless a special rule stipulates otherwise; a second detachment may use a different codex book, "
     "thus allowing for that player's army to represent forces that are allied together for the battle. A second "
     "detachment of the same codex may be taken without prior permission, however all TROOP slots in the first "
     "detachment must first be filled. Each Detachment fulfils its own compulsory selections; an Allied Detachment may "
     "not fulfil the compulsory selections of the Primary Detachment.\n"
     "In New Recruit: add one force 'Primary Detachment' and one further force per Allied Detachment ('Allied "
     "Detachment', or a special allied chart of an army list) to the same roster."),
    ("Allies Matrix", "Allies Matrix - At the Height of the Heresy (Games in the Age of Darkness). A - Allies and "
     "Brothers, C - Conditional Alliance, S - Sworn Enemies. " + AM.GENERAL),
] + [(n, t) for n, t in AM.LEGEND.values()]


def allied_force_entry(foc_links):
    """The game system's Allied Detachment: the Standard Force Organisation Chart with its own ids."""
    return el("forceEntry", {"id": ALLIED_FORCE, "name": "Allied Detachment", "hidden": "false"},
              [wrap("categoryLinks", foc_links)])


# ------------------------------------------------------------------ catalogues
def in_force(fid):
    return cond(fid, "force", "instanceOf", 0, deep=False)


def allied_units_cat(catalogue):
    return gs.cat("Allied Detachment units: " + short_name(catalogue))


def pct_cond(catalogue, pct=25):
    """The points of this army list's Allied Detachment units are more than pct % of the army's points. (New Recruit
    takes a percentage of the scope's total: units of an Allied Detachment carry a category per army list, counted
    across the roster - so the limit applies per Allied Detachment.)"""
    c = cond(allied_units_cat(catalogue), "roster", "greaterThan", pct, field=PTS, deep=True)
    c.set("percentValue", "true")
    return c


def roster_has(cid, n=1):
    return cond(cid, "roster", "atLeast", n)


def find_entry(root, eid):
    for e in root.iter("selectionEntry"):
        if e.get("id") == eid:
            return e
    return None


def rule_texts(e):
    out = []
    for r in e.iter("rule"):
        d = r.find("description")
        if d is not None and d.text:
            out.append(d.text)
    return " ".join(out)


NO_ALLIES = re.compile(r"(?:no|not include an?|not include a Fortification or an?|not include an? Fortification or)"
                       r"\s+(?:Fortification or\s+)?Allied Detachment(?:s)?(?! (?:drawn from|belonging to|from) another)"
                       r"(?: or Fortification)?\s*[.;]", re.I)
NEEDS_MILITIA = re.compile(r"must include an Allied Detachment (?:drawn )?from the\s+Imperialis Militia", re.I)
NO_LEGION_ALLIES = re.compile(r"Allied Detachment (?:drawn from|belonging to|from) another Space Marine Legion", re.I)


def apply(root, special_allied=()):
    """Add Army / Detachment markers and the roster-wide alliance checks to one catalogue.
    special_allied: ids of force entries of this catalogue that count as Allied Detachments."""
    name = root.get("name")
    if name not in CATALOGUES:
        return
    me = CATALOGUES[name]
    alleg = find_entry(root, ALLEGIANCE_ENTRY)
    if alleg is None:
        raise SystemExit(f"{name}: no Allegiance entry to carry the army markers")
    mark = army_cat(name)
    # New Recruit: an "instanceOf" force condition on the game system's Allied Detachment is also true inside a
    # Primary Detachment (live test), so "allied" = any force whose Allegiance did not get the Primary marker.
    not_primary = cond(CAT_PRIMARY, "force", "lessThan", 1)
    add_to(alleg, "categoryLinks", [category_link(mark, "Army: " + short_name(name), key=uid("allies", name))])
    mods = [
        modifier("add", "category", CAT_PRIMARY, conds=[in_force(PRIMARY_FORCE)]),
        modifier("add", "category", CAT_ALLIED, conds=[not_primary]),
        # one Primary Detachment; an Allied Detachment needs one
        modifier("add", "error", "An army has exactly one Primary Detachment.",
                 conds=[in_force(PRIMARY_FORCE), roster_has(CAT_PRIMARY, 2)]),
        modifier("add", "error", "An Allied Detachment needs a Primary Detachment in the same army (add a 'Primary "
                                 "Detachment' force first).",
                 conds=[cond(CAT_PRIMARY, "roster", "lessThan", 1)]),
        # Loyalist and Traitor do not mix
        modifier("add", "error", "Loyalist and Traitor Detachments may not be part of the same army (an alliance never "
                                 "overrides allegiance requirements).",
                 conds=[roster_has(LOYALIST), roster_has(TRAITOR)]),
        # a second Detachment from the same army list: all Troops slots of the Primary Detachment filled first
        modifier("add", "error", "A second Detachment from the same army list may only be taken once all Troops slots of "
                                 "the Primary Detachment are filled.",
                 conds=[in_force(PRIMARY_FORCE), roster_has(mark, 2),
                        cond(gs.cat("Troops"), "force", "lessThan", 6)]),
        # Games in the Age of Darkness: the Allied Detachment may only ever make up 25% of the army's points
        modifier("add", "error", "An Allied Detachment may only make up 25% of the army's points.",
                 conds=[not_primary, cond(CAT_NO_CAP, "force", "lessThan", 1), pct_cond(name)]),
        # Primarchs: Primary Detachment only (Forces of the Legions, Fielding a Primarch)
        modifier("add", "error", "A Primarch may only be selected as part of the army's Primary Detachment, never an "
                                 "Allied Detachment.",
                 conds=[cond(gs.CAT_PRIMARCH, "force", "atLeast", 1), not_primary]),
    ]
    # Sworn Enemies
    rel = relations()
    if me:
        for (a, b), v in sorted(rel.items()):
            if a != me or v != "S" or b == me:
                continue
            if side(a) and side(b) and side(a) != side(b):
                continue  # opposite sides: an allegiance error, or allowed because one side swapped
            for cat_name, abbr in CATALOGUES.items():
                if abbr == b:
                    who = SHORT[b] if b != me else short_name(name)
                    mods.append(modifier(
                        "add", "error",
                        f"Sworn Enemies (Allies Matrix): {SHORT[me]} and {who} may not be part of the same army.",
                        conds=[roster_has(army_cat(cat_name), 2 if b == me else 1)]))
    mods += army_specific(root, name, alleg)
    # every unit of a non-Primary Detachment carries CAT_ALLIED_UNIT (for the 25% limit)
    root_ids = {l.get("targetId") for l in root.find("entryLinks")}
    for u in shared_units(root):
        if u.get("id") in root_ids:
            add_mods(u, [modifier("add", "category", CAT_ALLIED_UNIT, conds=[not_primary]),
                         modifier("add", "category", allied_units_cat(name), conds=[not_primary])])
    fe = root.find("forceEntries")
    for f in (fe if fe is not None else []):
        if f.get("name") in NO_CAP_FORCES:
            add_mods(alleg, [modifier("add", "category", CAT_NO_CAP, conds=[in_force(f.get("id"))])])
    add_mods(alleg, mods)
    add_to(alleg, "rules", [matrix_rule(name)])

    # Rites of War that forbid Allied Detachments
    rites = find_entry(root, RITE_ENTRY)
    if rites is not None:
        import legiones2
        legiones2.rite_master_error(rites)
        legions_other = [c for c, a in CATALOGUES.items() if c.startswith("Legiones Astartes") and c != name]
        for opt in rites.iter("selectionEntry"):
            if opt is rites:
                continue
            text = rule_texts(opt)
            rid = opt.get("id")
            if NO_LEGION_ALLIES.search(text):
                add_mods(opt, [modifier(
                    "add", "error", f"{opt.get('name')}: the army may not include an Allied Detachment drawn from "
                                    "another Space Marine Legion.",
                    conds=[cond(rid, "force", "atLeast", 1)],
                    groups=[any_of(*[roster_has(army_cat(c)) for c in legions_other])])])
            if NEEDS_MILITIA.search(text):
                add_mods(opt, [modifier(
                    "add", "error", f"{opt.get('name')}: the army must include an Allied Detachment drawn from the "
                                    "Imperialis Militia (Exercitus Imperialis).",
                    conds=[cond(rid, "force", "atLeast", 1),
                           cond(army_cat("Exercitus Imperialis"), "roster", "lessThan", 1)])])
            if NO_LEGION_ALLIES.search(text):
                pass
            elif NO_ALLIES.search(text):
                add_mods(opt, [modifier(
                    "add", "error", f"{opt.get('name')}: the army may not include an Allied Detachment.",
                    conds=[cond(rid, "force", "atLeast", 1), roster_has(CAT_ALLIED)])])


def shared_units(root):
    sse = root.find("{http://www.battlescribe.net/schema/catalogueSchema}sharedSelectionEntries")
    if sse is None:
        sse = root.find("sharedSelectionEntries")
    return [e for e in (sse if sse is not None else []) if e.get("type") == "unit"]


def has_rule_link(e, rule_name):
    il = e.find("infoLinks")
    return il is not None and any(x.get("name") == rule_name for x in il)


def army_specific(root, name, alleg):
    """Allied-detachment restrictions written in the army books themselves."""
    mods = []
    if name == "Talons of the Emperor":
        # The Emperor's Talons: Legio Custodes in the Primary Detachment - no Allied Detachment (an Exercitus
        # Imperialis Allied Contingent with Companions of the Ten Thousand is ignored)
        for u in shared_units(root):
            if has_rule_link(u, "Legio Custodes"):
                add_to(u, "categoryLinks", [category_link(CAT_CUSTODES, "Legio Custodes unit", key=uid("allies", "cust", u.get("id")))])
        mods.append(modifier(
            "add", "error", "The Emperor's Talons: an army whose Primary Detachment contains Legio Custodes units may not "
                            "include an Allied Detachment (except an Exercitus Imperialis Allied Contingent with "
                            "Companions of the Ten Thousand).",
            conds=[in_force(PRIMARY_FORCE), cond(CAT_CUSTODES, "force", "atLeast", 1)],
            groups=[any_of(cond(CAT_ALLIED, "roster", "atLeast", 2),
                           all_of(roster_has(CAT_ALLIED), cond(CAT_COMPANIONS, "roster", "lessThan", 1)))]))
    if name == "Exercitus Imperialis":
        comp = next((e for e in root.iter("selectionEntry")
                     if (e.get("name") or "").startswith("Companions of the Ten Thousand")), None)
        if comp is None:
            raise SystemExit("Exercitus Imperialis: Companions of the Ten Thousand not found")
        mods.append(modifier("add", "category", CAT_COMPANIONS, conds=[cond(comp.get("id"), "force", "atLeast", 1)]))
    if name == "The Lost and the Damned":
        oaths = {e.get("name"): e.get("id") for e in root.iter("selectionEntry")}
        for oath, text in [("Chymeriae", "Shunned and Distrusted: a Blackshields force using the Chymeriae Oath may not "
                                         "include an Allied Detachment."),
                           ("The Alien Brotherhood", "Unlikely Allies: a force using The Alien Brotherhood Oath may only "
                                                     "include an Allied Detachment chosen from an Eldar army list.")]:
            mods.append(modifier("add", "error", text, conds=[in_force(PRIMARY_FORCE), cond(oaths[oath], "force",
                                                                                              "atLeast", 1),
                                                               roster_has(CAT_ALLIED)]))
        # Agents of the Sigillite count as the army's Allied Detachment
        for u in shared_units(root):
            cl = u.find("categoryLinks")
            if cl is not None and any(x.get("name") == "Agents of the Sigillite HQ" for x in cl):
                add_to(u, "categoryLinks", [category_link(CAT_ALLIED, "Detachment: Allied", key=uid("allies", "sig", u.get("id")))])
    return mods


def matrix_rule(name):
    me = CATALOGUES[name]
    if me is None:
        text = (f"{short_name(name)} has no row in the Allies Matrix (Games in the Age of Darkness); no alliance "
                "restrictions are checked for it. " + AM.GENERAL)
    else:
        rel = relations()
        groups = {"A": [], "C": [], "S": []}
        for (a, b), v in rel.items():
            if a == me and v in groups:
                groups[v].append(SHORT[b])
        parts = []
        for k_ in ("A", "C", "S"):
            title = AM.LEGEND[k_][0]
            parts.append(f"{title}: " + (", ".join(sorted(groups[k_])) or "-"))
        text = ("Allies Matrix - At the Height of the Heresy. " + ". ".join(parts) + ". " + AM.GENERAL +
                " A Legion fielded with the other allegiance (e.g. Loyalist Sons of Horus) swaps sides: Sworn "
                "Enemies that only come from the two sides of the Heresy become allies, and all detachments of an army "
                "must share one allegiance.")
    return rule(uid("allies-rule", name), "Allies Matrix: " + short_name(name), text)
