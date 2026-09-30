# Writing a Legion module

Every Legion gets its own catalogue, `Legiones Astartes - <Legion>.cat`: the full Legiones Astartes army list
(built by `tools/legiones.py` + `tools/legiones2.py`) plus that Legion's module from this folder, which adds the
Forces of the Legions content (Legion rules, armoury, Consuls, Rites of War, unique units, named characters,
Primarch). Only that one Legion is in the catalogue, so nothing has to be hidden behind "is this Legion" checks.

Source text: `/home/claude/src/legions/<Legion>.txt` (one file per Legion, cut from Forces of the Legions).
Universal Primarch rules: `/home/claude/src/legions/_primarch_rules.txt` (already in `common.PRIMARCH_RULES`).
Base army list (for reference, e.g. what a Legion unit replaces): `/home/claude/src/legiones_new4.txt`.
Core rules: `/home/claude/src/core.txt`.

Build and check one Legion:

    python3 tools/build.py "I - Dark Angels"

It must end with `All references resolve.` (unknown ids / duplicate ids are listed otherwise).

## Module layout (`tools/legions/<number>_<name>.py`)

```python
from legions.common import *          # all helpers below

LEGION = "I - Dark Angels"            # exactly as in legiones_wargear.LEGIONS
LR = "Legiones Astartes (Dark Angels)"

RULES = {LR: "...", "Mastery of the Blade": "...", ...}      # every rule text this Legion uses
WEAPONS = {"Calibanite Warblade": ("-", "User +1", "-", "Power Weapon")}
WEAPON_RULES = {"Calibanite Warblade": ["Calibanite Warblade"]}
WARGEAR = {"Some Relic": "rule text"}


def register():                       # BEFORE the army list is built: data only
    register_data(rules=RULES, weapons=WEAPONS, weapon_rules=WEAPON_RULES, wargear=WARGEAR)


def extend(ctx):                      # AFTER the army list is built
    ctx.legion_rules([LR, "Mastery of the Blade", ...], force_org=[...])
    ...
```

Everything you reference by name (`W(name)`, `gear(key, name)`, `rules_links([...])`, options in `slot/take/pool`)
must exist: weapons/wargear in `WEAPONS`/`WARGEAR` of the base data or registered by you; rules in `ARMY_RULES`
(base or yours) or the core USRs (`tools/data/core_usr.json`, looked up case-insensitively). A missing name raises
a KeyError at build time - add it to your RULES/WARGEAR.

## Do not edit shared files

Do **not** change `bsx.py`, `gamesystem.py`, `legiones.py`, `legiones2.py`, `legions/common.py`, `build.py` or
`data/*` - several people build Legions at the same time. If you need a helper, write it in your own module.
If something truly needs a shared change, describe it in your questions file instead.
Your module may change shared data structures at build time (each catalogue is built in its own process),
e.g. in `register()`: `L2.TROOP_RITES["Legion Veteran Squad"].append("My Rite")`,
`L2.NOT_LINE_UNDER[...]`, `RITES`, `ARMY_RULES[...] = ...`.

## Helpers (see `common.py`, `legiones.py`, `legiones2.py`, `bsx.py`)

IDs: `uid(*parts)` makes a stable id from any strings. Use keys that include your Legion/unit name so they never
collide (e.g. `uid("unit", "Deathwing Companion Detachment")`). Never reuse a key for two different elements.

Entries (bsx): `entry(id, name, typ="upgrade"|"unit"|"model", cost=, mods=[], constraints=[], cats=[], profiles=[],
infolinks=[], rules=[], links=[], entries=[], groups=[])`, `group(id, name, default=, mods=, constraints=,
entries=, links=, groups=)`, `link(id, target_id, name, cost=, mods=, constraints=)`,
`constraint(id, "min"|"max", value, scope="parent"|"force"|"roster"|"self", field="selections"|PTS, deep=False,
auto=False)`, `modifier("set"|"increment"|"decrement"|"add"|"remove"|"set-primary", field, value, conds=[],
groups=[], repeats=[])`, `cond(child_id, scope, "atLeast"|"lessThan"|"equalTo"|..., value)`, `any_of(*conds)`,
`all_of(*conds)`, `repeat(child_id, scope, every)`, `rule(id, name, text)`, `category_link(cat_id, name, key=)`.
`has(id, scope)` / `lacks(id, scope)` are shortcuts for conditions.

Units (legiones / legiones2):
- `unit_profile(key, name, unit_type, WS, BS, S, T, W, I, A, Ld, Sv)`, `L.vehicle_profile(key, name, type, BS, F, S, R)`,
  `walker_profile(key, name, WS, BS, S, F, S, R, I, A)`, `L.transport_profile(key, name, capacity, access, fire)`.
- `gear(key, item)` fixed wargear link; `rules_links([names], key=)` special rule links.
- `foc(category, "Elites", unit_id)` primary Force Organisation category; categories: `HQ, TROOPS, ELITES, FA, HS, LOW`.
- `slot(key, "Replace X", "X", [(item, pts), ...])` exactly-one replacement on ONE model (default = X).
- `take(key, title, [(item, pts) or (item, pts, max)], max_total=)` optional extras.
- `pool(key, title, unit_id, [(item, pts)], base_max, every=5)` "for every five models, one may ...".
- `model_swaps(key, title, unit_id, [model_ids], [(item, pts)], minus=[ids])` **"any model may replace X"** - a
  squad-level block, each option several times, capped at one per model. Use this (never per-model slots) on a
  model entry that can have more than one model. `model_takes(...)` for "any model may take ...".
  `model_pair_claws(...)` for "replace both with a pair of Lightning Claws".
- `numbered(model_entry, max_count, required=1)` for squadrons of 1-3 vehicles or characters that are each
  equipped separately (every model becomes its own entry). `squadron(...)` already does it.
- `choice(key, title, [(name, pts, per_model, [items], [rules])], unit_id=, required=, default=)` squad-wide option.
- `per_model(key, name, pts, unit_id, [items])` "the entire squad may take X for +N points per model".
- `transports(key, unit_id, ["Legion Rhino Armoured Carrier", ...])` Dedicated Transport choice (includes the
  Orbital Assault / Armoured Spearhead rite options automatically).
- `specials_decrement(...)`, `standard_choice(key)`, `armour_pattern(key)`, `tda_armoury(key)`,
  `pa_armoury(key, unit_id, max_size)` sergeant armoury (50 pts), `vehicle_upgrades(key, items)`, `STD_UPGRADES`.
- Look at `legiones2.py` for full examples of every kind of unit (squads with sergeants, Terminators, Dreadnoughts,
  squadrons, vehicles, retinues). Unit cost convention: unit `cost` = listed price minus the cost of the minimum
  number of per-model models (e.g. `cost=175 - 4 * 30` with 4 Terminators at 30 each + a 0-cost Sergeant).

Legion helpers (common.py):
- `register_data(...)`, `ctx.legion_rules(names, force_org=[gs.FOC_PLUS["HQ"], gs.FOC_MINUS["Fast Attack"], ...])`.
- `ctx.unit("Legion Praetor")` existing entry (also retinues like "Legion Command Squad"); `ctx.all_entries()`;
  `ctx.add_units(*roots)`; `ctx.add_shared(*non_roots)`; `ctx.add_rite(name, text, limit_fa=, limit_hs=,
  errors=[(text, [conds])])` returns the rite id (use `rite(name)` / `rite_id(name)` in conditions).
  Rites that change what counts as Troops: edit `L2.TROOP_RITES` / `L2.NOT_LINE_UNDER` in `register()` (see how
  the base rites work in legiones2) or add `set-primary` modifiers yourself.
- `required_choice(key, title, [(name, [rules])], fixed=None)` e.g. Dark Angels Wings, Thousand Sons Cults.
  `choice_id(key, title, name)` gives an option's id. `legion_units(ctx)` all root units to add such a choice to.
- `add_consul(ctx, name, cost, rules, kit=, options=, groups_=, forbids=[items], support_officer=)`.
- `add_armoury_items(ctx, [(item, pts)], who=("praetor", "centurion", "sergeants"))` Legion Armoury items that
  count towards the normal Armoury points caps.
- `add_weapon_variant(ctx.all_entries(), "Power Weapon", "Calibanite Warblade", 10)` "any character able to
  select a Power Weapon may instead select X for +10".
- `forbid_items(unit, [items], [conds])`, `option(key, name, cost, ...)`, `upgrade(key, name, cost, rules_, text=)`.
- `named_character(LR, name, cost, (WS,BS,S,T,W,I,A,Ld,Sv), kit, rules, retinue=, master=, min_points=, loyalist=)`.
- `primarch(LR, name, cost, stats, kit, rules, retinue=primarch_retinue(key, extra=[...]), other=id_of_other_form,
  loyalist=True/False/None)` - adds the universal Primarch rules, Lord of War slot, 2,000 pts check, one per army.
- `retinue_links(key, [entries])`, `command_squad_for(char_key, char_id)`, `clone(entry, salt, new_name=)`.
- `unique(id)` one per army, `force_limit(id, n)` 0-n per Detachment, `min_points_error(name, pts)`,
  `allegiance_only(entry, loyalist=True)`.

`tools/legions/xv_thousand_sons.py` is a complete (large) example. It was written before the per-Legion split,
so it still wraps things in `ts()` / `not_ts()` checks - you don't need those.

## What to build (everything in the Legion's text)

1. Legion special rules (the named `Legiones Astartes (<Legion>)` rule + each Legion rule) -> `ctx.legion_rules`.
   Force Organisation changes -> `force_org=`. Army-wide restrictions -> errors (see `ctx.add_rite(errors=)` or
   `modifier("add", "error", text, conds=...)` on the Legion entry `ctx.unit("Legion")`).
2. Legion Armoury: weapons with profiles, wargear with rules, who may take them and costs.
3. Legion Consuls, Legion-specific upgrades on existing units (e.g. "Legion Veteran Squads may ...").
4. Rites of War (all of them, with effects that the builder can enforce: Troops changes, 0-1 limits, required
   units, forbidden units, cost changes).
5. Unique units (full options: models, weapons, "any model" blocks, sergeant armoury, transports, limits).
6. Named characters (unique, Master of the Legion or not, retinues, allegiance, min points).
7. The Primarch (and Daemon Primarch / other forms where present).

Write rule texts as faithful, complete summaries of the book (they are the user's own rules - keep numbers,
conditions and exceptions; you may shorten flavour text). Weapon profiles go in WEAPONS exactly as printed.

## Questions

Anything unclear, contradictory, missing (a points cost, a profile, an option list) or impossible to enforce in
New Recruit: make the most sensible choice, build it, and write it down in
`tools/questions/<Legion>.md` as a numbered list: what the book says (quote the line, with its line number in the
source .txt), what you did, and the question for the author. Keep each question short and concrete.
Also list rules that are only shown as text and not enforced by the builder.
