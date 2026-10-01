# Writing an army module (non-Legion army books)

Every army book is its own New Recruit catalogue, `<ARMY>.cat`, built from one module in this folder:
`tools/armies/<snake_name>.py`. The Legiones Astartes catalogues are built separately (tools/legions/).

Build and check one army:

    python3 tools/build.py <module_name>        # e.g. python3 tools/build.py solar_auxilia

It must end with `All references resolve.` (unknown ids / duplicate ids are listed otherwise).

## Module layout

```python
from armies.common import *

ARMY = "Solar Auxilia"            # catalogue name

RULES = {"Rule name": "full rule text", ...}                 # army special rules
WEAPONS = {"Volkite Charger": ('15"', "5", "5", "Assault 2, Deflagrate")}
MULTI = {"Missile Launcher": {"Missile Launcher - Frag": (...), "Missile Launcher - Krak": (...)}}
WEAPON_RULES = {"Volkite Charger": ["Deflagrate"]}            # rules linked from a weapon
WARGEAR = {"Flak Armour": "5+ armour save", "Void Armour": ("4+ armour save", ["Some Core USR"])}


def build():
    start(ARMY)                                               # ALWAYS first
    register_data(rules=RULES, weapons=WEAPONS, multi_profile=MULTI, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    units = [allegiance(), ...]                               # every root unit
    shared = [...]                                            # transports, retinues etc. linked from units
    return catalogue(ARMY, units, shared)
```

`start()` empties the data tables, so your catalogue only contains your own army's weapons, wargear and rules.
Every weapon/wargear item used anywhere (kit, options) must be in WEAPONS/MULTI/WARGEAR; every rule name in
RULES or the core USRs (`tools/data/core_usr.json`, case-insensitive). A missing name raises a KeyError.

## Helpers (armies/common.py; plus everything in legiones.py / legiones2.py / bsx.py)

- `k(*parts)` stable id unique to your army - use it (or `uid(unit_id, ...)`) for every id you create.
- `unit(name, cost, TROOPS, "Troops", models=[...], kit=[...], rules_=[...], groups=[...], key=k("unit", name),
  compulsory=True)` - a root unit in a Force Organisation slot. Slots: `HQ, TROOPS, ELITES, FA, HS, LOW, FORT`
  with names "HQ", "Troops", "Elites", "Fast Attack", "Heavy Support", "Lords of War", "Fortification".
  `compulsory=True` makes an HQ count towards the compulsory HQ and a Troops unit towards the two compulsory
  Troops (set False for units the book says cannot fill compulsory slots).
- `model(unit_id, name, min, max, cost_per_model, profile, kit=[...], groups=[...])` - a model inside a unit.
  Unit `cost` = the listed price minus the cost of the minimum models (models carry their per-model cost).
- Profiles: `unit_profile(key, name, unit_type, WS, BS, S, T, W, I, A, Ld, Sv)`,
  `vehicle_profile(key, name, type, BS, Front, Side, Rear)`, `walker_profile(key, name, WS, BS, S, F, S, R, I, A)`,
  `transport_profile(key, name, capacity, access points, fire points)`.
- Options (all link to the shared weapon/wargear entries by name):
  - `slot(key, "Replace X", "X", [(item, pts), ...])` exactly-one replacement on ONE model (default X).
  - `take(key, title, [(item, pts) or (item, pts, max)], max_total=)` optional extras.
  - `pool(key, title, unit_id, [(item, pts)], base_max, every=5)` "for every five models, one may ...".
  - `model_swaps(key, title, unit_id, [model_ids], [(item, pts)], minus=[ids])` **"any model may replace X"**: a
    unit-level block where each option can be taken several times, capped at one per model. Always use this on
    model entries that can have more than one model (never put per-model slots on a model entry with count > 1).
  - `model_takes(key, title, unit_id, [model_ids], [(item, pts)])` "any model may take ...".
  - `choice(key, title, [(name, pts, per_model, [items], [rules])], unit_id=, required=, default=)` exclusive
    unit-wide choice (per_model=True multiplies the cost by the models in unit_id).
  - `per_model(key, name, pts, unit_id, [items])` "the entire unit may take X for +N points per model".
  - `upgrade(key, name, cost, rules_=[...], text="...")` a simple optional upgrade.
  - `numbered(model_entry, max_count, required=1)` squadrons of 1-3 vehicles / units of characters that are each
    equipped separately: every model becomes its own entry (returns a list).
- Army configuration: `allegiance(loyalist_ok=, traitor_ok=)` (include it as a root unit if allegiance matters),
  `config(key, name, [(option, [rules])], required=True)` for army-wide choices (Household, Legio, Cohort
  doctrine ...) - returns (entry, {option: id}) so you can write conditions on the chosen option.
- Limits: `unique(entry_id, n=1, scope="roster"|"force")` constraint (0-n per army / Detachment);
  `error_if(text, [conditions])` modifier that adds an error (put it in an entry's `mods`).
- Conditions: `has(id, scope)`, `lacks(id, scope)`, `cond(child_id, scope, "atLeast"|"lessThan"|..., value)`,
  `any_of(...)`, `all_of(...)`. Scopes: "self", "parent", "force" (the Detachment), "roster" (the army), or a
  unit/model id. Child ids: an entry id, `W(item)`, a category id, or "model"/"unit"/"any".
- `clone(entry, salt, new_name=)` deep copy with new ids (use an entry in two places).
- Low level (bsx): `entry, group, link, constraint, modifier, repeat, rule, category_link, info_link`.

Look at `tools/legiones.py`, `tools/legiones2.py` and a finished Legion module (`tools/legions/iii_emperors_children.py`)
for complete examples of squads with sergeants, characters, retinues, vehicles, squadrons and walkers.

## What to build (everything in the book)

1. Army special rules and army-wide restrictions (allegiance, Force Organisation changes, required units, 0-1 and
   per-points limits, army-wide choices such as a Household/Legio/Cohort/Covenant with their effects).
2. Armoury / wargear lists with profiles and rules, who may take what and at what cost (incl. points caps).
3. Every unit: models, profiles, base wargear, every option with its cost, unit size limits, "for every X models"
   limits, transports, special rules, Force Organisation slot, 0-1 / unique limits, prerequisites.
4. Named characters and unique units.
5. Any special detachment/organisation rules the builder can enforce; everything else as rule text.

Write rule texts as faithful, complete summaries of the book (they are the author's own rules - keep numbers,
conditions and exceptions; flavour text may be shortened). Weapon profiles exactly as printed.

## Do not edit shared files

Do **not** change `bsx.py`, `gamesystem.py`, `legiones.py`, `legiones2.py`, `armies/common.py`, `legions/*`,
`build.py` or `data/*` - several workers build at the same time. Put helpers in your own module. If something
truly needs a shared change (e.g. a new profile type, a Force Organisation chart the game system lacks), build the
best workaround in your module and describe the needed change in your questions file.

## Questions

Anything unclear, contradictory, missing (a cost, a profile, an option list) or impossible to enforce in New Recruit:
make the most sensible choice, build it, and write it down in `tools/questions/<ARMY>.md` as a numbered list: what
the book says (quote it, with the line number in the source .txt), what you built, and the concrete question for the
author. Also list the rules that are only shown as text and not enforced.
