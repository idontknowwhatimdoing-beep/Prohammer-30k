# IV - Iron Warriors: questions for the author

Source: `/home/claude/src/legions/IV_Iron_Warriors.txt` (line numbers refer to that file).
Module: `tools/legions/iv_iron_warriors.py`.

## Legion rules

1. **An Army of Steel and Wrath - optional?** L17-18: "the player may exchange two Fast Attack selections for one additional Heavy Support selection. This exchange may only be made once."
   *Built:* an optional toggle on the Legion entry. When ticked, the Detachment has 0-1 Fast Attack and 0-4 Heavy Support. Without it, the normal 0-3 / 0-3 apply.
   *Question:* Is the exchange always a free choice (as built)? Or is it always in force for the Iron Warriors (L19-21 reads like the chart is simply 0-1 FA / 0-4 HS)?

2. **Rules shown only as text (not enforced):** Siege Masters (L5-11), Stubborn Resolve (L25-29), Preliminary Bombardment (L35-41). These are all in-game effects.

## Armoury

3. **Who may buy Shrapnel Bolts?** L102: "SHRAPNEL BOLTS — 5 POINTS PER UNIT". The text does not say which units may buy them.
   *Built:* a "Shrapnel Bolts (unit)" option for +5 on every non-vehicle unit that has at least one bolt weapon. That covers Praetor, Centurion, Tactical, Assault, Breacher, Recon, Veteran, Terminator, Techmarine Covenant, Rapier Battery, Bike, Sky Hunter, Attack Bike, Heavy Support, Tyrant, Iron Havoc and Dominator units, plus the Command, Terminator Command and Honour Guard retinues.
   - It is hidden on Seeker Squads, because they always carry Special Issue Ammunition.
   - It is hidden on a Centurion with the Vigilator Consul.
   - Named characters and Perturabo do not get it.
   - Dreadnoughts and vehicles do not get it.

   *Question:* Is this the right set of units? Should vehicles, Dreadnoughts or named characters be able to take it?

4. **Shrapnel Bolts vs Hellfire Rounds.** L103: "may not be combined with Special Issue Ammunition, Hellfire Rounds or another special ammunition type."
   *Built:* the option is blocked only when the unit has Special Issue Ammunition, or is a Vigilator Consul. No unit in the base Legion list can choose Hellfire Rounds, so nothing else is blocked.
   *Question:* None needed, unless other ammunition options are added later.

5. **Servo-Arm - does it count towards the Armoury cap?** L105: "may purchase a Servo-Arm for +30 points".
   *Built:* the Servo-Arm (+30) is added to every Space Marine Armoury: the Praetor and Centurion 100-point Armoury, and every 50-point Sergeant/Champion/Terminator Armoury. It counts towards that Armoury's points cap. It is hidden and forbidden while the unit has a Jump Pack.
   *Question:* Should the Servo-Arm count towards the 50/100-point cap (as built)? Or should it be bought on top of the cap?

6. **Bionics +5.** L112: "may purchase Bionics for +5 points instead of the normal +10 points".
   *Built:* every Armoury Bionics option costing +10 now costs +5.
   *Question:* None.

## Rites of War

7. **The Hammer of Olympia - free Shrapnel Bolts.** L126: "Compulsory Troops choices gain Shrapnel Bolts at no additional points cost."
   *Built:* with this Rite, Shrapnel Bolts cost 0 for every Legion Tactical Squad and Legion Breacher Siege Squad. That includes squads beyond the two compulsory ones, because New Recruit cannot tell which squads are the compulsory ones. The squads still have to tick the option.
   *Question:* Should only the two compulsory squads get them free (players would need to apply this themselves)? Or should all Tactical/Breacher squads get them free (as built)? Should they get them automatically instead of having to tick the option?

8. **Hammer of Olympia - compulsory Troops and Deep Strike.** L122-124 and L150-152.
   *Built:*
   - Legion Assault Squads no longer count towards the compulsory Troops under this Rite.
   - Tactical and Breacher Siege Squads still count. Recon Squads never counted.
   - An error is shown if the army contains a Legion Drop Pod, Dreadclaw Drop Pod or Dreadnought Drop Pod (L152: "Units which are required to enter play by Deep Strike may not be selected").

   *Question:* Are there any other units that count as "required to enter play by Deep Strike"? Should Teleport Homers or other Deep Strike wargear be forbidden as well?

9. **Hammer of Olympia - Armoured Resolve.** L139-145 lists "Land Raiders".
   *Built:* text only.
   *Question:* Does this include Achilles-Alpha Land Raiders and Land Raiders in a Land Raider Battle Squadron (as written, "Land Raiders")?

10. **The Ironfire - Artillery Column.** L201-207.
    *Built:* the 0-1 Legion Artillery Tank Squadron gets a "Selected as Troops (Artillery Column)" option, shown only under this Rite. When ticked, the squadron is a Troops choice. It does not use a Heavy Support slot and does not count towards the compulsory Troops.
    *Question:* None.

11. **The Ironfire - Barrage weapon requirement.** L230: "The army must contain at least one unit equipped with a Barrage weapon."
    *Built:* an error is shown unless the Detachment contains at least one of: Whirlwind Launcher, Earthshaker Cannon, Medusa Siege Gun, Scorpius Multi-launcher, Quad Launcher (Rapier), Phosphex Discharger or Perturabo's Siege Bombardments.
    *Question:* Should Perturabo's Siege Bombardments (an "Ordnance Barrage attack", L1640) satisfy this requirement? It is not carried by a unit in the usual sense.

12. **Rite rules shown only as text (not enforced):**
    - the Warlord must have Master of the Legion (L149, L229)
    - Hail of Fire, Fury of Olympia, Rolling Bombardment, Walking the Fire, Ride the Ironfire
    - the Attacker requirement (L231)
    - the Fortification ban (L232) is enforced with an error

## Units

13. **Tyrant Siege Terminators - transport capacity.** L395: "may select a Land Raider, Dreadclaw Drop Pod or Spartan Assault Tank where Transport Capacity permits".
    *Built:* the transport choice offers Land Raider Phobos, Land Raider Proteus, Dreadclaw and Spartan. Transport Capacity is not checked. The Dominator Cohort (L777) is built the same way.
    *Question:* Which Land Raider variants are meant by "Land Raider"? Should the builder block transports too small for the squad (for example, a 10-model Terminator squad in a Land Raider)?

14. **Tyrant Siege Terminators - Grenade Harness.** L389-390: only the Tyrant Siege Master may take a Grenade Harness.
    *Built:* as written.
    *Question:* None.

15. **Tyrant Siege Terminators - missing Terminator rules.** L371-373 lists only Legiones Astartes (Iron Warriors) and Coordinated Bombardment.
    *Built:* as written. There is no Implacable Advance, and no Terminator Armour pattern choice (the unit always has Cataphractii).
    *Question:* Is that intended? The same applies to the Dominator Cohort.

16. **Iron Havoc Squad - no Dedicated Transport.** L466-560: no transport option is listed.
    *Built:* no transport.
    *Question:* Should Iron Havocs be able to take a Rhino like the Legion Heavy Support Squad?

17. **Iron Havoc Squad - Tank Hunters option.** L543: "Tank Hunters ... +3 points per model".
    *Built:* a squad-wide upgrade that grants the Tank Hunters rule.
    *Question:* None.

18. **Dominator Cohort - heavy weapons.** L765-769: "For every five models in the squad, one Dominator may replace its Combi-bolter".
    *Built:* a squad-level pool allowing 1 heavy weapon per 5 models. A Dominator who takes a heavy weapon cannot also take a Combi-bolter swap. The Warden cannot take a heavy weapon, but New Recruit does not check which model has it.
    *Question:* None.

19. **Iron Circle Domitar-Ferrum - Mechanicum rules missing.** L925-926 lists "Cybernetica Cortex" and "Reactor Blast", but these rules are not in this book or in the Legion list.
    *Built:* placeholder rule texts that refer to the Mechanicum army list.
    *Question:* Please provide the ProHammer texts for Cybernetica Cortex and Reactor Blast. Does the maniple need a controller (Cortex Controller / Praevian) to act normally?

20. **Iron Circle - Force Organisation and size.** L906-916 and L931-932.
    *Built:* Elites, 1-6 Domitar-Ferrum at 205 points each. No options.
    *Question:* None.

## Characters

21. **Nârik Dreygur - Force Organisation and Master of the Legion.** L1012-1080: there is no Force Organisation line, and he does not have Master of the Legion.
    *Built:* HQ, may fill the compulsory HQ, not a Master of the Legion.
    *Question:* Is HQ correct? Should he count as a compulsory HQ choice?

22. **Forrix - not a Master of the Legion?** L1301-1306: his special rules do not include Master of the Legion, although he is First Captain. Kroeger (L1385-1391) and Dreygur are the same.
    *Built:* not a Master of the Legion. All three can still fill the compulsory HQ.
    *Question:* Is that intended for Forrix? Are no named characters Loyalist-only or Traitor-only? None are restricted in the builder.

23. **Erasmus Golg - Terminator Attack.** L1111-1114: "If Erasmus Golg is the army's Warlord, Legion Terminator Squads may be selected as Troops choices."
    *Built:* while Golg is in the Detachment, each Legion Terminator Squad shows a "Selected as Troops (Terminator Attack)" toggle. When ticked, the squad is a non-compulsory Troops choice. The Warlord condition cannot be checked by New Recruit.
    *Question:* None.

24. **Kyr Vhalen - Iron Halo.** L1220.
    *Built:* "Iron Halo (Named Character)", which does not count against the army's one-Iron-Halo limit. This matches the other Legions.
    *Question:* Should his Iron Halo count towards the normal limit of one Iron Halo per army?

25. **Kyr Vhalen - Servo-Arm and Battlesmith.** L1199-1200 and L1223.
    *Built:* a fixed Servo-Arm, plus his own Battlesmith rule (4+ with the Servo-Arm).
    *Question:* None.

26. **Kroeger's Command Squad.** L1368-1371.
    *Built:* the standard Legion Command Squad retinue (its Jump Pack and Bike options are hidden, because Kroeger cannot take them).
    *Question:* None.

27. **Named characters - Krak grenades only.** L1080, L1240, L1394 offer Krak grenades (+2) to Dreygur, Vhalen and Kroeger.
    *Built:* as written. Golg and Forrix have no options except their retinues.
    *Question:* None.

## Perturabo

28. **Siege Specialists is not defined.** L1644: "Perturabo has the Tank Hunters and Siege Specialists special rules."
    *Built:* a placeholder rule "Siege Specialists".
    *Question:* What does Siege Specialists do? Please give the text.

29. **Perturabo - allegiance.** L1487-1661: no allegiance restriction is given.
    *Built:* Perturabo can be taken by either allegiance.
    *Question:* Should Perturabo be Traitor-only?

30. **Perturabo - Primarch Armour invulnerable save.** L1502-1511 gives Sv "1+". The Logos counts as Primarch Armour (L1616), which gives a 4+ Invulnerable Save.
    *Built:* profile Sv 1+, with the Primarch Armour rule linked.
    *Question:* None. It works the same way for the other Primarchs.

31. **Perturabo's retinue - "Those Once Honoured".** L784-785 and L1655-1661.
    *Built:* Perturabo's Primarch Retinue can be a Legion Honour Guard Squad, a Legion Terminator Command Squad, a Dominator Cohort or an Iron Circle Domitar-Ferrum Maniple. None of them use a Force Organisation slot. The Dominator retinue has the same options as the Elites unit.
    *Question:* None.

32. **Siege Bombardments.** L1629-1640.
    *Built:* one wargear entry with three profiles (Lance Strike, Melta Torpedo, Barrage Bomb). The two plotted targets, the Reserve and the scatter rules are text only.
    *Question:* None.

33. **Rules shown only as text:** The Logos re-roll, Lord of Iron (Tank Hunters for the joined unit), Calculated Destruction, Battlefield Calculation, and every named character and unit special rule in play.
