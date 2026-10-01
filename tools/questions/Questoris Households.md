# Questoris Households - questions for the author

Source: `/home/claude/src/Questoris_Households.txt` (line numbers below).
Module: `tools/armies/questoris_households.py`.

## How the list is built

Every Household Rank is a root unit in its Force Organisation slot (Seneschal, Lord Scion, Scion Martial, Scion Aspirant, Scion Dolorous, Scion Uhlan, Preceptor, Aucteller, Scion Arbalester, Scion Implacable). The rank's points modifier is the unit's cost (Scion Aspirant: -35), and inside it the player must choose exactly one Knight armour (default: Knight Paladin). The armour carries its profile with the rank's characteristic modifiers already applied (WS/BS +1 for Seneschal and Lord Scion, -1 for Scion Aspirant, Front Armour -1 for Scion Uhlan), its wargear, options and rules.

## Unclear / missing points

1. **Force Organisation Chart (L99-137)**: HQ 1-2, Troops 1-5, Elites 0-3, Fast Attack 0-2, Heavy Support 0-2. The game system's standard chart needs 2 Troops and allows 6/3/3.
   Built: a separate force type "Questoris Knight Crusade Force Organisation Chart" in this catalogue with these limits (plus Lords of War 0-1 and Fortification 0-1, compulsory 1 HQ and 1 Troops). The game system's "Standard Force Organisation Chart" can still be chosen for this catalogue. Question: is that fine, or should the standard chart be hidden for this army (needs a game-system change)?

2. **No profile type for Super-heavy Walkers / Structure Points (L1009-1031 etc.)**: the game system has no Structure Points column.
   Built: Walker profile; the Unit Type reads "Vehicle (Walker, Super-heavy, Knight); Structure Points N". Question: should a Super-heavy Walker profile type (with SP) be added to the game system?

3. **Melee weapon profiles (L758-769)**: the table only gives Strength and special rules, no AP.
   Built: Range "-", S 10, AP "-", Type "Melee, Power Weapon, <rules>". Question: what AP do Knight melee weapons have (AP2 as a power/destroyer weapon, or the ProHammer Power Weapon AP)?

4. **Lords of War from the Collegia Titanica list (L277-281)**: New Recruit cannot put another catalogue's units into this Detachment.
   Built: rule text only; no Lords of War or Fortification entries. A Titan has to be added as a separate Collegia Titanica Detachment. Question: acceptable?

5. **Bio-corrosive Rounds costs differ**: Paladin "Either Heavy Stubber ... +10 points each" (L1071-1075), Errant "for its Heavy Stubbers ... +5 points" (L1146) for both stubbers.
   Built as printed: Paladin up to 2 x +10, Errant one upgrade for +5 covering both. Question: is the Errant price intended?

6. **Knight Crusader Heavy Stubbers (L1410-1436)**: the Crusader may swap its Gatling Cannon for a Battlecannon *and Heavy Stubber*, and swap "its Heavy Stubber" for a Meltagun.
   Built: the Meltagun only replaces the original Heavy Stubber; Bio-corrosive Rounds (+10 each) are limited to the Heavy Stubbers actually carried (1, +1 with a Battlecannon swap, -1 with the Meltagun). Warden and Gallant lose the Bio-corrosive option once they take the Meltagun. Question: correct?

7. **Ion Shield save modifiers of Seneschal / Scion Aspirant (L395, L401)**: the 3+/5+ shield save is not shown on the profile (shields are wargear rules); it is only in the rank's rule text. Question: fine?

8. **Scion Uhlan Front Armour -1 (L410)**: applied to the profile (Questoris 13 -> 12). Acastus armours cannot be Uhlans, so no conflict.

9. **Twin Icarus Autocannon (L720)**: printed "Heavy 2, Skyfire, Interceptor" without Twin-linked despite the name. Built as printed. Question: should it be Twin-linked?

10. **Volkite Culverin (L752)**: "Heavy 4" with no Deflagrate, unlike the Volkite Chieorovile. Built as printed. Question: should it have Deflagrate?

11. **Cerastus Shock Lance (L730, L766)**: built as one weapon with a melee profile and the "Shock Blast" ranged profile. Same for the Atrapos Lascutter (melee + "Beam" L735/L769). The Hekaton Siege Claw with Twin-linked Rad-cleanser and Reaper Chainfist with Twin-linked Heavy Bolter are single wargear entries with two profiles.

12. **"Large Blast", "Ordnance", "Power Weapon", "Barrage", "Salvo", "Poisoned (4+)"** are ProHammer Classic weapon types without a linked rule entry in the game system (only shown in the Type column). "Poisoned (4+)" is linked to the core Poison rule.

13. **Graviton Gun (L728)**: the Knight version uses "Graviton Pulse" (army rule) and not the core Graviton rule; built that way.

14. **Knight-Atrapos limit (L1670-1674)**: "no more than one Knight-Atrapos for every full 2,000 points in the army". Built: enforced across all ranks, counting the roster's total points (like the Legiones Master of the Legion rule). Question: total points or the game's points limit?

15. **0-1 ranks (Seneschal, Lord Scion, Aucteller, L374-381)**: built as 0-1 per Detachment (Household = Detachment, L263). Question: per Detachment or per army?

16. **Young Blood (L401)**: enforced: Scions Aspirant in a Detachment may not exceed the number of Knights of all other ranks in that Detachment.

17. **Acastus rank restrictions (L1978-1986, L2086-2094)**: Porphyrion and Asterius are simply not offered under Scion Martial, Scion Aspirant and Scion Uhlan.

18. **Household Banner (L401)**: "Knights selected as Troops choices are always considered Scoring Units". Linked on Scion Martial and Scion Aspirant (the only Troops ranks). The rank table L376 says Scion Martial is "Free" - built with cost 0.

19. **Seneschal as Warlord (L329)**: "will normally serve as the Warlord" - not enforced (New Recruit has no Warlord selection here). Question: must the Seneschal be the Warlord if present?

20. **Allegiance (L271-273)**: built as the standard Allegiance configuration (Loyalist/Traitor required). No unit is allegiance-restricted.

## Rules shown as text only (not enforced)

- All Knight special rules: Super-heavy Walker, Structure Points, Massive Firepower, Striding War Machine, Crushing Advance, Immense Machine, Super-heavy Walker in Close Combat, Catastrophic Destruction, Flank Speed, Overtaxed Reactor, Volatile Reactor, Macro-extinction Targeting Protocols.
- All Household Rank rules: Master Knight, Ideal Mission Commander, Veteran Knight (WS/BS part is on the profile), Household Banner, Martial Knight, Aspirant (WS/BS part on the profile), Dolorous Charge, Worthy Foe, Impetuous Advance (Front -1 on the profile; Scouts and Hit & Run linked), Uhlan's Scorn, Oracle of Battle, Advanced Auspex Network, Defensive Coordination, Sworn Enemy, From Death I Strike, Weapon Calibration (Tank Hunters linked), Wall Breaker, Infantry Crusher, Close Defence, Relentless Advance.
- Ion Shield, Ionic Flare Shield, Ion Gauntlet Shield, Blessed Autosimulacra, Occular Augmetics (Night Vision linked), Bio-corrosive Rounds.
- Weapon rules: Massive Blast, Titan Killer, Machine Destroyer, Deflagrate, Sunder, Wrecker, Colossal, Hurl, Swift Strike, Tempest Attack, Graviton Pulse, Rad-phage, Collapsing Singularity, Hellstorm.
- Army rules: The Household, Knights and ProHammer Vehicle Rules, Alternative Force Organisation, Lords of War, Fortifications, The Army's Warlord, Allied Forces (allied allegiance compatibility and "Allied Detachments may not fulfil compulsory selections" are not checked).
