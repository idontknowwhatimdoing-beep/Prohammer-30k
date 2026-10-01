# Talons of the Emperor: questions for the author

Source: `/home/claude/src/Talons_of_the_Emperor.txt` (line numbers refer to that file).
Module: `tools/armies/talons_of_the_emperor.py`.

## Army construction

1. **Allegiance vs. the Infernus Abomination.** L302-306: "The Talons of the Emperor are Loyalist forces ... may not normally be selected as part of a Traitor force." L5576/L5595: the Infernus Abomination is "Traitor ... may only be included in an army with the Traitor Allegiance."
   *Built:* the Allegiance entry defaults to Loyalist. Traitor can still be picked, but it shows a warning. The Infernus Abomination is in the list as an Elites choice and shows an error unless the army is Traitor.
   *Question:* Should the Infernus Abomination be in this army book at all? It looks like it belongs in a Traitor list. Should Traitor be offered at all?

2. **The Emperor's Talons / Companions of the Ten Thousand / allies.** L310-337, L355-371.
   *Built:* rule text only, on the "Allegiance & Army Rules" entry. New Recruit cannot check Allied Detachments from other catalogues.
   *Question:* None. This is just to note that it is not enforced.

3. **Company-Cadres.** L212, L216-224: "Where a Sisters of Silence HQ possesses the Company-Cadre special rule ..."
   *Built:* rule text only. None of the HQ entries in the book (Knight-Abyssal, Knight-Centura, Vigil Command Cadre, Jenetia Krole) has the Company-Cadre rule, so there is nothing to enforce.
   *Question:* Is a Company-Cadre rule missing from one of the HQs? If so, which units must accompany it?

4. **Lords of War / Fortifications.** L242-262 describe both, but the book contains no Lord of War or Fortification entries.
   *Built:* nothing beyond the text and the standard chart's 0-1 slots.
   *Question:* Are any units planned for these slots?

5. **Officio Assassinorum.** L5016-5109 give a generic "0-1 Imperial Assassin" (50 points + Temple). L5141-5524 give seven separate Assassin entries with the same totals. L5128 adds the "Execution Force" alternative army list.
   *Built:*
   - In a normal Talons Detachment: only "0-1 Imperial Assassin" (Elites) with a required Temple choice. The Temple adds its cost, wargear and rules. It is limited to 0-1 per army (One Assassin).
   - A second force type, "Officio Assassinorum Execution Force", for the alternative list. It contains the seven named Assassin entries, exactly one of each (7/7), plus a required "Officio Assassinorum Execution Force" entry carrying the Execution Force rules. The Allegiance entry is also required there.
   *Question:* Is that split right, or should the seven named entries also be selectable in a normal Detachment? Assassins "do not benefit from army-wide special rules" (L5109). That is text only.

6. **Vigil Command Cadre and the HQ slot.** L3216: "A Vigil Command Cadre does not use up an HQ choice if the army includes a Knight-Centura, Knight-Abyssal or Jenetia Krole."
   *Built:* while the Detachment has one of those three, each Vigil Command Cadre raises the HQ maximum by 1, so it does not use up a slot. It still counts as an HQ choice towards the compulsory HQ.
   *Question:* Is the number of free Command Cadres unlimited, or one per Knight/Krole? Can a Command Cadre on its own fill the compulsory HQ choice and be Warlord? It has no Independent Character.

## Legio Custodes

7. **Dreadnoughts and the Legio Custodes rule.** L1425-1428, L1471-1474, L2294-2297: the Contemptor-Achillus, Contemptor-Galatus and Telemon do not list the Legio Custodes special rule. The Contemptors list Fleet / Move Through Cover / Counter-Attack.
   *Built:* exactly as listed, so no Legio Custodes rule on the Dreadnoughts. The Unit Type "Walker" (L1412) is shown as "Vehicle (Walker)".
   *Question:* Is that intended?

8. **Dreadnought Close Combat Weapon profile.** L1417: "Two Dreadnought Close Combat Weapons with inbuilt Lastrum Storm Bolters". The book gives no profile.
   *Built:* "Dreadnought Close Combat Weapon" shown as (- / x2 / - / Power Weapon), two of them.
   *Question:* What is the ProHammer profile? Should the second weapon give +1 Attack?

9. **Massive Wound.** This term is used throughout (L588, L717, L793, L1145, ...) but is not defined in the book or in the core rule list available to the builder.
   *Built:* only mentioned in the weapon texts.
   *Question:* Where is Massive Wound defined (ProHammer core)? Should it get its own rule entry?

10. **Plasma Grenades.** L1130 (Valdor), L2089 (Venatari).
    *Built:* listed as wargear with "As described in the ProHammer rules."
    *Question:* Is that right?

11. **Iron Halo limit.** L469 has no army limit. The Legiones Astartes data limits Iron Halos to one per army.
    *Built:* that limit is removed for this catalogue. The Shield-Captain, Valdor and Talon Masters (+15) can all have one. A Talon Master may have both a Refractor Field and an Iron Halo (L960, L994).
    *Question:* Is that right?

12. **Praesidium Shield with Two-handed weapons.** L446-449: a model with a Praesidium Shield "may not use a Two-handed weapon". The Talon Master and Shield-Captain may buy a shield while keeping a Guardian Spear (Two-handed).
    *Built:* allowed. The restriction is rule text only. The Shield-Captain and Hetaeron Guard can take only one of Praesidium / Advanced Praesidium Shield (L459).
    *Question:* Should a Guardian Spear (or other Two-handed weapon) plus Praesidium Shield combination be forbidden in the builder?

13. **Legio Custodes Tribune.** L1088-1095.
    *Built:* a +50 upgrade on the Shield-Captain. It is hidden below 2,000 roster points and limited to one per army, and it adds Eternal Warrior. "Must be the Warlord unless Valdor is present" is text only.

14. **The Shadow of the Throne.** L1145: "If Constantin Valdor is the army's Warlord, ... re-roll Seize the Initiative. In addition, Valdor gains a Teleportation Transponder at no additional cost and one friendly unit with the Legio Custodes special rule may also receive Teleportation Transponders at no additional cost."
    *Built:* Valdor has an optional free Teleportation Transponder. Every Custodes squad that can buy Transponders also gets a free "Teleportation Transponders (The Shadow of the Throne)" option. It is shown only when Valdor is in the army and limited to one unit per army.
    *Question:* Does "In addition" depend on Valdor being the Warlord? Can the free unit be one that cannot normally buy Transponders (Agamatus, Venatari)?

15. **Custodian Guard spear swaps and the Vexilla.** L1597-1607: "For every three models, one Custodian Guard may replace his Guardian Spear with Adrasite/Pyrithite"; "One Custodian Guard may replace his Guardian Spear with Magisterium Vexilla and Sentinel Warblade (+10)".
    *Built:* a pool of 1 per 3 models, plus a separate one-off Vexilla option. The builder does not stop the same model from taking both.
    *Question:* Should the Vexilla bearer count towards the 1-per-3 limit?

16. **Coronus Grav-Carrier capacity.** L1828, L1845-1847: capacity 12, but only squads of six models or fewer (Aquilon four or fewer) may select it.
    *Built:* the Coronus option is hidden and blocked above 6 models (Aquilon above 4). It is offered only to Custodian, Sentinel, Hetaeron, Sagittarum and Aquilon squads.

17. **"Machine Spirit" wargear.** L1815, L2400 list "Machine Spirit" as wargear. The book does not define it.
    *Built:* a wargear item that grants Power of the Machine Spirit.
    *Question:* Is that intended?

18. **Two different Grav-backwash rules.** L1854 (Coronus/Caladius: "Unless the vehicle has been Immobilised ...") and L2016 (Pallas: "If the Pallas Grav-Attack moved ... maximum 6+").
    *Built:* two separate rules, "Grav-backwash" and "Grav-backwash (Pallas)".
    *Question:* Is the difference intended?

19. **Profiles with modified Toughness.** The Agamatus (L1935) "4(5)" and Subjugators (L4611) "3(4)" are shown as printed.

## Sisters of Silence

20. **Pursuer Cadre structure.** L4496-4567.
    *Built:*
    - Pursuer Prime, 2-5 Pursuers (+25 per additional Pursuer) and 3-6 Cyber-Jackals (free).
    - An error appears unless the Cadre has one Cyber-Jackal for every Pursuer plus one.
    - Frag/Krak Grenades cost +1/+2 per Pursuer, including the Prime but not the Cyber-Jackals.
    - Anathema Psykana applies to the Pursuers only.
    - The Anathema Psykana Rhino (10) is blocked above 10 models. The Kharon (12) is always possible.
    *Question:* Is the Pursuer Prime a "Pursuer" for the grenade cost? Do the Cyber-Jackals count against transport capacity?

21. **Rage version.** L4521 lists the Cyber-Jackals with "Rage". The core rule list has a 3rd-5th and a 6th-7th Edition Rage.
    *Built:* links the 6th-7th Edition version (+2 Attacks on the charge).
    *Question:* Which version is meant?

22. **Hatred (Psykers), Feel No Pain (5+), Preferred Enemy (Characters), Poisoned (2+), Rending (5+).** The qualifier is shown in the rule or weapon text. The link goes to the generic core rule (Hatred, Feel No Pain, Preferred Enemy, Poison, Rending + "Modified Rending").

23. **Vigil Command Cadre composition.** L3118-3174: 3 Vigil Sisters, up to 3 more, up to two upgraded to Questora (+10) and one to Silent Judge (+20).
    *Built:* Vigil Sisters (15), Questora (25) and Silent Judge (35) are separate model entries. The minimum of three Vigil Sisters drops by one for each upgrade. An error appears outside 3-6 models. L3204 "Every model may take Krak Grenades (+2)" is per model.
    *Question:* Is the per-model Krak Grenade purchase right, or is it squad-wide?

24. **Firebrand Jump Packs.** L3447-3459.
    *Built:* "Jump Packs (entire squad)" at +5/model. Taking it removes the Dedicated Transport option. The change of Unit Type to Jump Infantry is text only; the profile still says Infantry.

25. **"The Prime may take" lists (Firebrand L3451, Seeker L4789, Expurgator L4969).**
    *Built:* only one of the listed weapons may be taken.
    *Question:* Can a Prime take more than one, e.g. both a Power Weapon and a Power Stake?

26. **Weapons replaced for the whole unit (Subjugator L4657, Expurgator L4952).**
    *Built:* a required unit-wide choice (default Snare Cannons / Heavy Flamers) priced per model, including the Prime.
    *Question:* Does the Prime also carry and swap the heavy weapon?

27. **Master-Crafted Weapon (Knights L3008/L3097, Raptor Prime L3592).**
    *Built:* a "Master-Crafted Weapon" upgrade (+10). The builder does not record which weapon is upgraded.

28. **Etherium, Storm Bolter, Plasma Gun, Meltagun, Multi-Melta** appear in the Sisters wargear/weapon lists (L2561, L2583-2591), but no Sister can buy Etherium. The guns only appear inside Combi-Weapons and on vehicles.
    *Question:* Is something missing from the unit option lists, e.g. who may buy an Etherium?

29. **Relic Blade text ends early.** L2801-2805: "Two-handed Power Weapon. The bearer strikes at S6" and nothing more.
    *Built:* (S6, Power Weapon, Two-handed).
    *Question:* Is anything missing?

30. **Kharon Pattern Acquisitor missiles.** L4304: "Two Twin-Linked Vratine Missile Launchers".
    *Built:* two "Twin-linked Vratine Missile Launcher" items with the three ammunition profiles marked Twin-Linked.

31. **Unit types.** The book lists every character as "Infantry". Independent Characters and Assassins are shown as "Infantry (Character)". Primes, Questora and Silent Judges stay "Infantry".
    *Question:* Are the Primes Characters (for challenges, Look Out Sir, etc.)?

## Shown as rule text only (not enforced by the builder)

32. Army-level text: Talons of the Emperor (mustering, Two Talons, Warlord, Multiple Detachments), The Emperor's Talons, Companions of the Ten Thousand, Company-Cadres, Dedicated Transport restrictions.
33. Custodes rules: the Legio Custodes rule (8" charge, 3" coherency), Very Bulky, Teleportation Transponder (every model + joined IC), Arae-Shrikes, Magisterium Vexilla, the Tribune Warlord requirement, The Shadow of the Throne re-roll, weapon rules (Disintegration, Fan-burst, Volley Fire, Rapid Tracking, Heliothermic Detonation, Exoshock, Molecular Severance), the Meridian Power Blades styles, Auramite Pinions, Unyielding Sentinel, Indomitable Charge, Grav-backwash, Flare Shield, Dreadnought Praesidium Shield, Multi-layer Refractor Field.
34. Sisters rules: Anathema Psykana, Ex Oblivio, Mistress of the Silent Sisterhood, Mistress of the Black Ships, Gunfighters, Condemned Quarry, Marked Quarry, Snare, Psyker Bane, Hellfire, Witchbane, Psyk-out, Special Issue Ammunition (same type for the whole unit), Battle Auspex, Spectra-Distort Field, Capture-Grid, Null Rod, Augury Scanner.
35. Assassin and Infernus rules: Assassin Operative, Dodge, Assassinorum Agent, all Temple rules and wargear, all Execution Force rules, Cult Operative, Osmeotic Regeneration, Transmutative Armaments.
36. Display note: with "any model may replace X" options, the original weapon stays listed in the model's wargear. The swap is recorded as a separate selection, as in the Legiones Astartes catalogues.
