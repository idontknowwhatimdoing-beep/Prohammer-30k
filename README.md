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

Complete army list: HQ (with retinues and all Consuls), Troops, Elites, Fast Attack, Heavy Support,
Dedicated Transports, Space Marine Armoury and all 11 Rites of War, plus the universal Primarch rules and the
Primarch's Chosen Rite.

Forces of the Legions (chosen with the Legion option in each list):
- [x] XV Thousand Sons: Legion rules, Prosperine Cults, Psychic Brotherhoods, Price of Knowledge force org, armoury,
  3 Rites of War, Sekhmet, Khenetai, Ammitara, Castellax-Achea, Contemptor-Osiron, Numerologist Cabal, Ahriman,
  Phosis T'Kar, Amon, Hathor Maat, Sanakht, Magnus the Red and Magnus, Shard of the Crimson King
- [ ] the other 17 Legions

### Rules enforced by the builder

- Force org: 1-2 HQ, 2-6 Troops, 0-3 Elites / Fast Attack / Heavy Support, 0-1 Lord of War / Fortification
- At least one compulsory HQ that is not a Legion Support Officer or Moritat; two compulsory Troops that are not Support Squads
- One Master of the Legion per full 1,000 points; one Iron Halo per army; 0-1 Damocles (1,000+ pts); Legion Standard only at 2,000+ pts
- Retinues (Honour Guard, Command Squad, Terminator Command Squad) inside their character, no extra slot; Terminator Command Squad only for a character in Terminator Armour
- Terminator Armour removes Jump Pack / Bike options; Chainfist and Foeblaster need Terminator Armour; Pair of Lightning Claws takes both hands
- Consul restrictions, psyker-only and Apothecary-only wargear, invulnerable saves that would not stack
- Weapon counts scale with squad size; Dedicated Transports only where allowed (squad size, no Jump Packs/Bikes)
- Dreadnoughts: paired close-combat arms +1 Attack, Veteran Pilot WS/BS, Armoured Sarcophagus front armour applied to the profile
- Rites of War: needs a Master of the Legion; changes which units are Troops and which count as compulsory Troops; 0-1 Fast Attack / Heavy Support limits; extra transport and wargear options; checks for Tactical Company, Recon Company, Sky Hunter Phalanx and Fury of the Ancients limitations
- Armoury points caps (100 pts for Praetor / Centurion, 50 pts for Sergeants and squad characters)

## Editing the data

The `.gst` / `.cat` files are generated from `tools/`. Change the data there and rebuild:

```
python3 tools/build.py
```

The build keeps every internal id stable, so saved army lists keep working after updates.
