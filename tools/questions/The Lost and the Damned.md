# The Lost and the Damned - questions for the author

Source: `/home/claude/src/The_Lost_and_the_Damned.txt` (line numbers below).
Module: `tools/armies/the_lost_and_the_damned.py`.

The catalogue holds: the Blackshields force (standard Force Organisation Chart: generic Legiones Astartes Army List
without Praetors, plus Reaver Lord, Blackshield Marauder Squad, Chymeriae Squad, Oath of Moment and Chymeriae Attribute
configuration, Blackshield Armoury / Weapons / Xenos Weapons injected into every armoury and weapon list) and the
"Agents of the Sigillite Allied Detachment" force (Preceptor, five Knights-Errant, Strike Force Squad, Operative Cell,
Assassin). Allegiance is Loyalist or Traitor, because the book allows both for Blackshields (L214) and Agents of the
Sigillite are Loyalist only (L1569).

## Answered, waiting for a shared change (not buildable in this module alone)

- **Shattered Legions (L68-158)** - author: make it a separate catalogue. Needs a new army module / catalogue that can
  use the units of two or three Legion catalogues (gamesystem-level change). Until then the rules stay as text here.
- **Agents of the Sigillite for Loyalist Legions** - author: add an extra Force Organisation slot every Loyalist
  Legion can select when it picks Loyalist, which then offers these units like an Allied Detachment. Needs the
  "Agents of the Sigillite Allied Detachment" force entry (and access to its units) in the gamesystem / Legion
  catalogues. Here it stays this catalogue's own force entry.

## Unclear / missing points

1. **Eldritch Tutelage powers (L395-405).** "A single Blackshield Librarian in the army may replace one of his normal
   psychic powers with one selected Eldar psychic power: Doom, Guide, Mind War, Eldritch Storm ... uses the power
   according to its normal rules". The rules of these four powers are not in the book or the data set. Built: the four
   powers are pickable in the Librarian's Psychic Powers (The Alien Brotherhood only, they take the place of a normal
   power, one Eldar power per army); their text only says to use the Eldar army list rules. Question: please give the
   rules (type, range, effect) of Doom, Guide, Mind War and Eldritch Storm.
2. **Force Organisation slots of the Blackshield units (L1210, L1416).** The Blackshield Marauder Squad and the
   Chymeriae Squad entries give no Force Organisation slot. Built: Marauder Squad = Troops (counts towards the
   compulsory Troops), Chymeriae Squad = Elites. Question: which slots should they use?
3. **Agents of the Sigillite weapon costs (L1850-1872, L2036, L2220).** The Specialist Ranged Weapons table has no
   points costs, and the only melee weapon listed is the Aether-shock Maul (15). The Preceptor "may replace his Bolt
   pistol, Bolter and/or Power Weapon with weapons available to him from the Agents of the Sigillite Armoury, paying the
   points costs listed there". Built: Bolt pistol -> Hand Flamer / Volkite Serpenta +5, Plasma Pistol +15; Bolter ->
   Combi-weapons / Storm Bolter / Flamer / Volkite Charger +5, M.40 Stalker Bolter / Meltagun / Plasma Gun / Heavy Bolter
   +10, Autocannon / Missile Launcher / Multi-Melta +15 (costs of the Strike Force Squad options); Power Weapon ->
   Chainsword free, Power Fist / Lightning Claw / Aether-shock Maul +15, Relic Blade +20. Question: confirm these costs
   and whether melee weapons other than the Aether-shock Maul are allowed.

## Shown as text only (not enforced)

- Shattered Legions rules and restrictions; The Whole is Greater than the Sum.
- Allied Detachment restrictions of the Oaths (No Gods, No Masters: no Allied Detachment with a Primarch; Shunned and
  Distrusted; Unlikely Allies / Eldar allies; Outcasts Among Outcasts: no Imperial allies). Chaplains are hidden under
  Orphans of War and The Alien Brotherhood; Agents of the Sigillite show an error under those Oaths.
- Eldar psychic power effects (Eldritch Tutelage), Void Reavers, The Shadow of Oblivion, Scarce Ammunition / The Last Magazine,
  Brothers Before Masters, Brother-Slayers, Inured to Pain, The Lure of Battle.
- Chymeriae Attribute effects and Genetic Instability (the Attribute is chosen as configuration, effects are text).
- Lord of the Blackshields "must be the Warlord"; Agents of the Sigillite may not be the Warlord; Assassin may not be
  the Warlord.
- Orders of the Sigillite; Agent of the Sigillite / Knight-Errant joining rules.
- "Only Blackshield Characters, Veteran Sergeants and models with Armoury access" for individual Blackshield weapons
  beyond the slots built; "no model may select the same item twice" is enforced only inside each armoury group.
- Desperate Warriors: the "minimum 1 point per model" is not checked (no model costs less than 3 points).
- All weapon special rules (Overpressure, Deathlock, Lethal Exposure, Psi-shock, Stasis Anomaly ...).
