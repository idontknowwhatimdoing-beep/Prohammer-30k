# Prohammer 30k

New Recruit game data for the Prohammer-based Horus Heresy ruleset (ProHammer Classic Core Rules v2.4).

## Load it in New Recruit

Systems list → **Add more games** → **Add from Github** → paste `https://github.com/idontknowwhatimdoing-beep/Prohammer-30k` → green **+**.
After an update is pushed, refresh New Recruit (or fully close and reopen on mobile) to pull it.

## What's in it

| File | Contents |
|---|---|
| `Prohammer 30k.gst` | Game system: points, profile types, Standard Force Organisation Chart, ProHammer Classic universal special rules |
| `Legiones Astartes.cat` | Legiones Astartes Army List (work in progress, see below) |

### Legiones Astartes status

- [x] Army configuration: Legion, Allegiance
- [x] HQ: Legion Praetor, Legion Centurion with all 12 Consul upgrades
- [x] Troops: Tactical, Assault, Breacher Siege, Reconnaissance
- [x] Dedicated Transports: Rhino, Drop Pod, Dreadclaw
- [x] Space Marine Armoury (Praetor / Centurion / Power Armour Sergeant)
- [ ] HQ: Damocles Command Rhino, Honour Guard, Command Squads
- [ ] Elites, Fast Attack, Heavy Support
- [ ] Rites of War, Legion-specific rules (Forces of the Legions)

### Rules enforced by the builder

- Force org: 1-2 HQ, 2-6 Troops, 0-3 Elites / Fast Attack / Heavy Support, 0-1 Lord of War / Fortification
- At least one compulsory HQ that is not a Legion Support Officer or Moritat; at least two Troops that are not Support Squads
- One Master of the Legion per full 1,000 points; only one Iron Halo per army
- Terminator Armour removes Jump Pack / Bike options; Chainfist and Foeblaster need Terminator Armour
- Pair of Lightning Claws takes both weapon hands
- Consul restrictions (Moritat, Herald, Vigilator, Praevian, Master of Signals, Forge Lord, Primus Nullificator)
- Psyker-only and Apothecary-only wargear, invulnerable saves that would not stack
- Special / heavy weapon counts scale with squad size; Dedicated Transports only for squads of 10 or fewer
- Armoury points caps (100 pts for Praetor / Centurion, 50 pts for Sergeants)

## Editing the data

The `.gst` / `.cat` files are generated from `tools/`. Change the data there and rebuild:

```
python3 tools/build.py
```

The build keeps every internal id stable, so saved army lists keep working after updates.
