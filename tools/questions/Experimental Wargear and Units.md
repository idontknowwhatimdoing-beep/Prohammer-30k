# Experimental Wargear and Units: questions for the author

Source: `/home/claude/src/Experimental_Wargear_and_Units.txt` (line numbers refer to that file).
Module: `tools/armies/experimental.py`.

## Catalogue / army construction

1. **How the experimental units are added to an army.** L53-55: "This Will be the place where all bad decisions will be put ... Use them as you wish." The document gives no Detachment or army rules.
   *Built:* its own catalogue. Every unit has the rule "Experimental (Unofficial)". There is also an optional configuration entry, "Experimental Wargear and Units", that holds the rules for the whole document. The catalogue adds a second force type, "Experimental Supplement (no compulsory selections)", with HQ 0-2, Elites 0-3, Fast Attack 0-3, Heavy Support 0-3 and Dedicated Transports. You add it next to a Legiones Astartes Detachment. You can also use the Standard chart, but then the compulsory HQ and Troops can't be filled from this catalogue.
   *Not enforced:* the slots these units use should count against the Legion Detachment's Force Organisation chart. New Recruit cannot do that across Detachments.
   *Question:* Are these units meant to be part of the Legiones Astartes list (as Legion units)? If yes, the clean fix is a shared change: each Legion catalogue imports this catalogue (catalogueLink), or the units move into `legiones2.py`. Should that be done?

2. **New Recruit cannot add options to other catalogues.** Saturnine Exo-armour for Praetors and Centurions (L64), "vehicle upgrades from the Space Marine Armoury" (L333, L422), Legion-specific wargear (L243) and the Focused Fire Configuration for the Legion Heavy Support Squad (L755) all change units or options in the Legiones Astartes catalogues.
   *Built:* rule text only, except where noted below.
   *Question:* None. This is just to note the limitation.

## Saturnine Exo-armour and Saturnine units

3. **Saturnine Exo-armour cost and who may take it.** L64: "SATURNINE EXO-ARMOUR 65 ca". No unit entry says who may buy it. L212 needs "a Praetor or Centurion equipped with Saturnine Exo-armour".
   *Built:* it is part of every Saturnine model's kit, with its full rule text. The text adds: "a Legion Praetor or Centurion may take it for about +65 points". It cannot be added to the Legion characters.
   *Question:* Is the exact cost 65 points? Which characters may take it (Praetor, Centurion, Consuls)? Does it replace Terminator Armour, or is it bought on top of Terminator Armour? Can a character in it use the normal Terminator Armour Armoury options?

4. **"Terminator profile above".** L75: "These modifiers are already included in the Saturnine Terminator profile above." The exo-armour section comes before the unit profiles.
   *Built:* the profiles as printed (S5 T5 W2 I3 A3, Veteran A4). These match a Legion Terminator plus the modifiers.
   *Question:* None. The wording only needs "below".

5. **Save notation.** L70-73 give "2+/4++". The profiles at L105-106 and L178 give "2+/4+".
   *Built:* "2+/4+" in the profiles. The exo-armour text says 2+ armour save with a 4+ invulnerable save.
   *Question:* Is the invulnerable save 4++? It is better than the 5++ of normal Terminator Armour (Cataphractii level).

6. **"Power weapon or power fist".** L128, L198.
   *Built:* each model gets a free choice, Power Weapon by default and Power Fist at +0. A Power Fist can be replaced by a Chainfist (+5). In the Command Squad it can also be replaced by a Thunder Hammer (+10). For the ordinary models this is one squad-level block, capped at one per model.
   *Question:* Is the fist really free, or should it cost something?

7. **Heavy weapons in the Saturnine Terminator Squad.** L153: "For every three models in the squad, one Saturnine Terminator may replace its Foeblaster boltgun ...".
   *Built:* one heavy weapon for every three models, counting all models including the Veteran (3-5 models: 1, 6 models: 2). Only the Saturnine Terminators can take them, not the Veteran. A heavy weapon uses up that model's Foeblaster, so it also reduces the number of Combi-Foeblaster swaps.
   *Question:* Is that right?

8. **Saturnine Veteran Armoury.** L162: "up to 50 points of permitted weapons and wargear from the Space Marine Armoury".
   *Built:* the Terminator-Sergeant column of the Armoury (same list as the Legion Terminator Sergeant), except Force Weapon, capped at 50 points.
   *Question:* Is that the intended list?

9. **Saturnine Terminator Command Squad as a retinue.** L181: "Force Organisation: Retinue". L212: "may only be selected as a retinue for a Praetor or Centurion equipped with Saturnine Exo-armour. The character and Command Squad count as a single HQ choice."
   *Built:* a root unit in the HQ slot. It does not count towards the compulsory HQ. It carries the "Saturnine Retinue" rule. The character requirement and the shared HQ slot are not enforced, because the character is in another catalogue.
   *Question:* Should it become a retinue option on the Legion Praetor and Centurion (a shared change to `legiones2.retinue_group`, together with a Saturnine Exo-armour option)?

10. **Command Squad upgrades.** L233-241: Apothecary +25 (Narthecium & Reductor), Standard Bearer +15 (Legion Standard), Champion +15 (+1 Attack).
    *Built:* three separate models (95 / 85 / 85 points), each 0-1. Each one replaces a Bodyguard (2-5 models in total). Each has its own weapon choices. The Legion Standard shows an error in armies under 2,000 points, following the normal Legion Standard rule.
    *Question:* Should the Legion Standard really cost only +15 (the normal Armoury price is 60), and should the 2,000-point limit apply? Does the Champion get any other rule (Honour or Death, a Master-crafted weapon)?

11. **No Veteran or Sergeant in the Command Squad.** L186: "2 Saturnine Bodyguards", and there is no Character in it.
    *Built:* as written.
    *Question:* None.

12. **Transport capacity.** L87, L167, L248: each model counts as two models in Terminator Armour.
    *Built:* rule text only.
    *Question:* None.

13. **Unit type and named Legiones Astartes rule.** L133, L203.
    *Built:* the Legiones Astartes rule with the Legion text. The named Legion version is not added, because this catalogue has no Legion choice.
    *Question:* None.

## Vehicles

14. **Sabre / Arquitor squadrons.** L312, L408.
    *Built:* 1-3 vehicles, each equipped separately.
    *Question:* None.

15. **"Vehicle upgrades from the Space Marine Armoury as normally permitted".** L333, L422.
    *Built:* the Legion upgrade list on each vehicle: Hunter-Killer Missile 5, Dozer Blade 5, Extra Armour 5, Auxiliary Drive 10, Armoured Ceramite 20, plus one pintle-mounted weapon (Twin-linked Bolter 5, Combi-weapon 5, Heavy Bolter 10, Heavy Flamer 10, Multi-Melta 15, Havoc Launcher 15).
    *Question:* Is the pintle weapon allowed on the Sabre and the Arquitor? Is Armoured Ceramite allowed?

16. **Sunder.** L340 and L433 use Sunder. L435 defines it as "Failed Armour Penetration rolls made by this weapon may be re-rolled." The Legiones Astartes list defines it as a re-roll against vehicles only.
    *Built:* the L435 wording for this catalogue.
    *Question:* Should the two definitions be the same?

17. **Graviton-Charge Cannon Strength.** L432: Strength "\*".
    *Built:* Strength "\*", with the Graviton rule linked.
    *Question:* Is "\*" the same as "Special" on the Legion graviton weapons?

18. **Anvillus snub autocannon on a Fast Tank.** The profile is Heavy 2, Twin-linked (L340).
    *Built:* as printed.
    *Question:* None.

19. **Legion Rhino Advancer: slot.** L630-698 give no Force Organisation entry.
    *Built:* a root unit in the "Dedicated Transport" category, so it uses no slot. It cannot be bought as a transport for units in other catalogues.
    *Question:* Is it a Dedicated Transport (for which units?) or a Fast Attack / Heavy Support choice?

20. **Rhino Advancer: Open Topped and Fire Points.** L670 says "Open Topped". L696 says "Up to two transported models may fire through the Rhino's top hatch". L652 says "Vehicle (Tank, Transport)".
    *Built:* both are kept. "Open Topped" refers to the ProHammer Classic Open-topped rules. There is no core USR entry for it.
    *Question:* Is it really Open-topped? If yes, all passengers may normally fire, so the fire point line is not needed. Also, there is no fire point line on most Rhinos.

21. **Rhino Advancer: Combi-weapon.** L718: "Combi-weapon +5 points".
    *Built:* the generic Legion "Combi-Weapon" entry.
    *Question:* Which combi-weapon is meant?

22. **Rhino Advancer: Armoured Ceramite.** L704-712 list only Dozer Blade, Extra Armour, Hunter-Killer Missile and Auxiliary Drive.
    *Built:* exactly those four. There is no Armoured Ceramite and no other Armoury upgrade.
    *Question:* None.

## Army-wide rules

23. **Focused Fire Configuration.** L751-755: "A heavy Support squad that is part of an army over the size of 2000 points may be fully equipped with heavy weapons instead of the Usual 4 Marines which can do so. Only one Unit may be upgraded like that."
    *Built:* an optional toggle on the configuration entry. It is 0-1 per army and shows an error at 2,000 points or less. The Legion Heavy Support Squad itself is in the Legion catalogue, so its heavy weapon limit stays at four (add the rest by hand).
    *Question:* Is there an extra cost? Does "fully equipped" include the Sergeant? Does "over 2000" mean more than 2,000 points, or 2,000 points or more? Should this become a shared change to the Legion Heavy Support Squad?

24. **General Additions (design notes).** L468-562: a list of ideas for Ultramarines, Dark Angels, the Corrupted Legions, Knights and the Mechanicum (Logos Command Squad, Excindio Battle-Automata, Daemon Prince, blessings, Plague Marines, Obliterators, Nemesis Warbringer and Psychic Titans and others). None of them has a profile, cost or rule.
    *Built:* nothing playable. The list is kept as the text-only rule "Planned Additions (design notes)" on the configuration entry.
    *Question:* Please write these up when they are ready, with profiles, costs and rules.

## Rules shown only as text (not enforced)

- Experimental (Unofficial) and Experimental Supplement: no checks across Detachments or catalogues.
- Saturnine Exo-armour: the character option and its ~65 point cost; counts as Terminator Armour; Deep Strike only where the mission permits it.
- Massive Exo-armour: no Sweeping Advance; Consolidate only after winning; each model counts as two Terminators for transport.
- Combi-Foeblaster: fires the secondary weapon once per battle.
- Saturnine Retinue: the character requirement and the shared HQ slot.
- Legion-specific Wargear (Saturnine).
- Repair, Auxiliary Drive, Open Topped, and the Rhino Advancer embark restrictions (no Terminators, Jump Packs, Bikes or Jetbikes).
- Focused Fire Configuration: the extra heavy weapons in the Legion catalogue.
- Planned Additions (design notes).
