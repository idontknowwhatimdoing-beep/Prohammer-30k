# Questoris Households - questions for the author

Source: `/home/claude/src/Questoris_Households.txt` (line numbers below).
Module: `tools/armies/questoris_households.py`.

## How the list is built

Every Household Rank is a root unit in its Force Organisation slot (Seneschal, Lord Scion, Scion Martial, Scion Aspirant, Scion Dolorous, Scion Uhlan, Preceptor, Aucteller, Scion Arbalester, Scion Implacable). The rank's points modifier is the unit's cost (Scion Aspirant: -35), and inside it the player must choose exactly one Knight armour (default: Knight Paladin). The armour carries its profile with the rank's characteristic modifiers already applied (WS/BS +1 for Seneschal and Lord Scion, -1 for Scion Aspirant, Front Armour -1 for Scion Uhlan), its wargear, options and rules.

## Settled with the author (built)

- Force Organisation: the normal (game-system) Force Organisation Chart is used; the book's Questoris Knight Crusade chart is no longer built.
- Structure Points: still shown in the Unit Type of the Walker profile until the game system gets a Super-heavy Walker / Super-heavy / Titan profile type with Structure Points (shared change requested; only for these unit types).
- Knight melee weapons ignore armour saves like all power weapons: Type reads "Melee, Power Weapon (ignores armour saves), ...", AP "-".
- Twin Icarus Autocannon is Twin-linked; Volkite Culverin has Rending (no Deflagrate).
- Knight-Atrapos limit counts the total points of the list; 0-1 ranks are per Detachment; Errant Bio-corrosive +5 and the Crusader Heavy Stubber handling stay as built.

## Open questions

No open questions.

## Rules shown as text only (not enforced)

- All Knight special rules: Super-heavy Walker, Structure Points, Massive Firepower, Striding War Machine, Crushing Advance, Immense Machine, Super-heavy Walker in Close Combat, Catastrophic Destruction, Flank Speed, Overtaxed Reactor, Volatile Reactor, Macro-extinction Targeting Protocols.
- All Household Rank rules: Master Knight, Ideal Mission Commander, Veteran Knight (WS/BS part is on the profile), Household Banner, Martial Knight, Aspirant (WS/BS part on the profile), Dolorous Charge, Worthy Foe, Impetuous Advance (Front -1 on the profile; Scouts and Hit & Run linked), Uhlan's Scorn, Oracle of Battle, Advanced Auspex Network, Defensive Coordination, Sworn Enemy, From Death I Strike, Weapon Calibration (Tank Hunters linked), Wall Breaker, Infantry Crusher, Close Defence, Relentless Advance.
- Ion Shield, Ionic Flare Shield, Ion Gauntlet Shield, Blessed Autosimulacra, Occular Augmetics (Night Vision linked), Bio-corrosive Rounds.
- Weapon rules: Massive Blast, Titan Killer, Machine Destroyer, Deflagrate, Sunder, Wrecker, Colossal, Hurl, Swift Strike, Tempest Attack, Graviton Pulse, Rad-phage, Collapsing Singularity, Hellstorm.
- The Army's Warlord: the Seneschal must be the Warlord if present (author's answer) - New Recruit has no Warlord selection here, so text only (the rule is linked on the army and on the Seneschal).
- Army rules: The Household, Knights and ProHammer Vehicle Rules, Alternative Force Organisation, Lords of War, Fortifications, The Army's Warlord, Allied Forces (allied allegiance compatibility and "Allied Detachments may not fulfil compulsory selections" are not checked).
