# Prohammer 30k

New Recruit game data for the Prohammer-based Horus Heresy ruleset (ProHammer Classic Core Rules v2.4).

## Load it in New Recruit

Systems list → **Add more games** → **Add from Github** → paste `https://github.com/idontknowwhatimdoing-beep/Prohammer-30k` → green **+**.
After an update is pushed, refresh New Recruit (or fully close and reopen on mobile) to pull it.

## What's in it

| File | Contents |
|---|---|
| `Prohammer 30k.gst` | Game system: points, profile types, Standard Force Organisation Chart, ProHammer Classic universal special rules |
| `Legiones Astartes - <Legion>.cat` (18) | The full Legiones Astartes Army List plus that Legion's Forces of the Legions content: Legion rules, armoury, Consuls, Rites of War, unique units, named characters, Primarch |
| `Solar Auxilia.cat`, `Mechanicum.cat`, `Talons of the Emperor.cat`, `Questoris Households.cat`, `Daemons of the Ruinstorm.cat`, `The Lost and the Damned.cat`, `Exercitus Imperialis.cat` | The other main army books |
| `Lords of War.cat`, `Legio Titanica.cat`, `Aeronautica Imperialis.cat`, `Traditoris Extremi.cat` | Supplementary lists (Experimental Wargear and Units is kept in `tools/armies/_experimental.py`, not published yet) |

Pick the catalogue for your army when you create a list (e.g. "Legiones Astartes - Sons of Horus").
Open points that still need the author's decision are collected per army in `tools/questions/`.

### Rules enforced by the builder

- Force org: 1-2 HQ, 2-6 Troops, 0-3 Elites / Fast Attack / Heavy Support, 0-1 Lord of War / Fortification
- At least one compulsory HQ that is not a Legion Support Officer or Moritat; two compulsory Troops that are not Support Squads
- One Master of the Legion per full 1,000 points; one Iron Halo per army; 0-1 Damocles (1,000+ pts); Legion Standard only at 2,000+ pts
- Retinues (Honour Guard, Command Squad, Terminator Command Squad) inside their character, no extra slot; Terminator Command Squad only for a character in Terminator Armour
- Terminator Armour removes Jump Pack / Bike options; Chainfist and Foeblaster need Terminator Armour; Pair of Lightning Claws takes both hands
- Consul restrictions, psyker-only and Apothecary-only wargear, invulnerable saves that would not stack
- "Any model may..." options are squad-level blocks: each weapon can be taken several times, up to one per model
  (special/heavy weapons and Pairs of Lightning Claws use up the weapon they replace); squadrons and Techmarine
  Covenants list every model/vehicle separately so each one is equipped on its own
- Armoury items marked "Not with Terminator Armour" are blocked for models in Terminator Armour
- Weapon counts scale with squad size; Dedicated Transports only where allowed (squad size, no Jump Packs/Bikes)
- Dreadnoughts: paired close-combat arms +1 Attack, Veteran Pilot WS/BS, Armoured Sarcophagus front armour applied to the profile
- Rites of War: needs a Master of the Legion; changes which units are Troops and which count as compulsory Troops; 0-1 Fast Attack / Heavy Support limits; extra transport and wargear options; checks for Tactical Company, Recon Company, Sky Hunter Phalanx and Fury of the Ancients limitations
- Armoury points caps (100 pts for Praetor / Centurion, 50 pts for Sergeants and squad characters)

## Allied Detachments

Add a force **Primary Detachment** for your main army, then one more force per Allied Detachment to the same roster
(**Allied Detachment**, or an army list's own chart: Ruinstorm Allied Detachment, Daemons of the Ruinstorm Covenant
Detachment, Agents of the Sigillite). Each detachment picks its own army list and fills its own compulsory slots.
The builder checks the Allies Matrix of *Games in the Age of Darkness* (Sworn Enemies may not share an army), one
Primary Detachment, no Loyalist + Traitor mix, Primarchs only in the Primary, and Rites of War / army rules that forbid
allies. Each army's Allegiance entry shows its row of the matrix.

## Editing the data

The `.gst` / `.cat` files are generated from `tools/` (Legion modules in `tools/legions/`, other armies in
`tools/armies/`, each folder has a README for writing a module). Change the data there and rebuild:

```
python3 tools/build.py
```

The build keeps every internal id stable, so saved army lists keep working after updates.
