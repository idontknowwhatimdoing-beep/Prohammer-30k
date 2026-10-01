# Daemons of the Ruinstorm - questions for the author

Source: `/home/claude/src/Daemons_of_the_Ruinstorm.txt` (line numbers below).
Module: `tools/armies/daemons_of_the_ruinstorm.py`.

## Unclear / missing points

1. **Daemon Brute Retinue size (L716 vs L959, L983, L999)**: the Daemon Lord entry says "may be accompanied by between one and three Daemon Brutes. See the Daemon Brute entry for their points cost", but the Brute unit is 3 Brutes for 135 points, +45 per extra model up to 6, and the Retinue box says "A single unit of Ruinstorm Daemon Brutes may be taken as a Retinue".
   Built: the Retinue is a separate 1-3 model Brute unit at 45 points per model (135 / 3), with all normal Brute options (Emanations, weapons), linked from the Daemon Lord (no Elites slot).
   Question: is the Retinue 1-3 Brutes at 45 points each (as built), or a full Brute unit of 3-6 models (135 points + 45 per extra)?

2. **Number of Daemon Lords (L282-288, L723)**: "If the Primary Detachment contains a Ruinstorm Daemon Lord, that model must be selected as the army's Warlord." Two Lords in one Detachment cannot both be Warlord.
   Built: 0-1 Ruinstorm Daemon Lord per Detachment. Question: is that the intent, or 0-1 per army?

3. **Ka'Bandha and the Daemon Lord (L2309, L2338 "Lord of Murder")**: both Ka'Bandha and a Daemon Lord "must be the army's Warlord" if they are in the Primary Detachment.
   Built: an error when Ka'Bandha and a Ruinstorm Daemon Lord are in the same Detachment. Question: which takes precedence (the Lord of the Ruinstorm text says "unless another rule specifically requires a different model to be the Warlord", which suggests Ka'Bandha wins)? If so the error can be removed.

4. **"Miasma of Decay" is used twice (L2425 vs L2948)**: the Creeping Scourge Core Dominion Rule "Miasma of Decay" (-1 Initiative to enemies in base contact) and the Creeping Scourge Dominion Emanation "Miasma of Decay" (-1 Weapon Skill to enemies in base contact) have the same name and different effects.
   Built: two rules, "Miasma of Decay (Dominion Rule)" and "Miasma of Decay (Emanation)". Cor'bax (L2147) gets the Emanation. Question: please rename one of them. Also the Suffocating Dread Emanation "Oppressive Presence" (L2991) has exactly the same effect as the Miasma of Decay Emanation - intended?

5. **Daemonic Melee Weapon AP (L2798-2806)**: the table has only Strength and Type columns. Built with AP "-" and the type text as printed (e.g. "Melee, Power Weapon"). Question: confirm there is no AP value; how is "Armour Save -1" (Warp Maul) meant to work in ProHammer?

6. **Ruinstorm Possessed weapon profiles (L1301-1344)**: Lasgun, Laspistol, Heavy Stubber, Grenade Launcher, Flamer, Plasma Gun, Meltagun, Bolter, Bolt Pistol, Power Weapon, Power Fist, Lightning Claw and Thunder Hammer are not printed in the book. Built with the standard ProHammer / Legiones Astartes profiles (Lasgun 24" S3 AP- Rapid Fire, Laspistol 12" S3 AP- Pistol, Heavy Stubber 36" S4 AP6 Heavy 3, Grenade Launcher Frag 24" S3 AP6 Assault 1 Blast / Krak 24" S6 AP4 Assault 1). Question: please confirm.

7. **Possessed Auxiliaries armour (L1288, L1301-1303)**: Save 5+ but no armour listed as wargear (Legionaries list Power Armour). Built: Sv 5+ in the profile, no armour item. Question: should they have Flak Armour?

8. **Possessed Legionary upgrade (L1332)**: "The entire unit may be upgraded to Possessed Legionaries for +5 points per model."
   Built: an "Upgrade to Possessed Legionaries" toggle; once taken the unit uses Possessed Legionary models (10 points each = 5 + 5) instead of Auxiliaries, 10-20 models. The Lasgun/Laspistol choice and the Auxiliary special-weapon pool are then hidden and the Legionary options appear. Question: may a Legionary unit also use the Auxiliary weapon list (Heavy Stubber, Grenade Launcher)? (Built: no.)

9. **Possessed special weapons with Laspistols (L1322-1323)**: "may exchange its Lasguns for Laspistols" and "one model may replace its Lasgun with ...". Built: the special weapon pool is still available after the Laspistol swap. Question: is that allowed?

10. **Possessed Legionary Bolt Pistol swap vs special weapon pool (L1334-1338)**: built so that the number of Bolt Pistol swaps plus special weapons cannot exceed the number of Legionaries. Question: OK?

11. **Greater Manifestation eligibility of the Daemon Lord (L593-600, L2419-2468)**: every Greater Manifestation lists "Greater Daemons (and Daemon Behemoths) only"; the Daemon Lord is not mentioned (only the Arch-Daemon via Apex Manifestation).
   Built: Ruinstorm Greater Daemons (all six), Daemon Behemoths (Crimson Fury, Creeping Scourge, Lurid Onslaught, Suffocating Dread) and the Arch-Daemon (all six) receive their Dominion's Greater Manifestation automatically; the Daemon Lord does not. Question: should the Daemon Lord count as a "Greater Daemon" for this?

12. **Sorcerous Conduit on multi-model units (L2959)**: "Daemon Characters and Monstrous Creatures only. The model becomes a Psyker ... may select one power". Greater Ruinstorm Daemon Beasts (Monstrous Creatures, 1-3 per unit, Favoured by Maddening Swarms) may take it.
   Built: available to Daemon Lords, Greater Daemons, Daemon Chosen, Arch-Daemons and Greater Daemon Beasts (Daemon Behemoths are not Favoured by Maddening Swarms). A unit with Sorcerous Conduit must select exactly one Ruinstorm Psychic Power for the whole unit. Question: does every model of a Greater Daemon Beast unit become a separate Psyker, and may they choose different powers?

13. **Ruinstorm Daemon Shrike (L1482, L1499-1507)**: "may select up to two General Emanations" - built with General Emanations only (Monstrous cost class, L2523). No Dominion lists Shrikes as Favoured. Horned Crown is not offered (not a Character). Question: confirm. The Shrike is a "Flying Monster" - is that a Monstrous Creature for Warp Blade (L2822) purposes? Built: Monstrous class, so no Warp Blade.

14. **Greater Daemon Beasts Favoured status (L1622)**: "count as a Favoured Archetype where a Dominion specifically lists Daemon Beasts". Built: Favoured for Crimson Fury, Maddening Swarms, Lurid Onslaught and Suffocating Dread.

15. **Daemon Chosen is "Infantry (Character)" with Independent Character** - built as Greater cost class (L2522), Favoured for every Dominion (Daemon Characters are always Favoured, L512). Horned Crown available.

16. **Daemonic Forms do not change the profile (L2691)**: the Unit Type in the profile is not changed by Winged / Mounted / Beast Form; the Form is shown as a selected item with its rule. Question: none - just noting that the profile stays e.g. "Infantry (Character)".

17. **Lords of War limit (L231)**: "no army may contain more than one Lord of War selection". Built: an error if the roster contains more than one Lord of War (across all Detachments), plus the normal 0-1 per Detachment. "Only where permitted by the mission or by agreement" is text only.

18. **Ruinstorm Allied Detachment (L315-360)**: built as a separate Detachment type in the catalogue ("Ruinstorm Allied Detachment": HQ 1, Troops 1-2, Elites/Fast Attack/Heavy Support 0-1, compulsory 1 HQ + 1 Troops, no Lords of War, no Fortifications, no Ruinstorm Daemon Lord). Its Aetheric Dominion and Allegiance configuration work as in the standard Detachment. Question: should the Allied Detachment be restricted to Traitor armies only by the builder (it is a text rule now: the host army's Allegiance lives in another catalogue and cannot be checked)?

19. **Named characters' parameterised rules**: "Preferred Enemy (Characters)", "Feel No Pain (5+)", "Psyker (Mastery Level 2/3)", "Rage (6th-7th Edition)" are linked as short army rules / the core rule. Ka'Bandha's "Rage (6th–7th Edition)" (L2307) is mapped to the core rule "Rage (6th-7th Edition Codexes)".

20. **Cor'bax Biomancy powers (L2157)**: "may select two powers from the Biomancy Psychic Discipline presented in ProHammer Classic" - the discipline is not in this book or the game data. Built as text only (no power selection in the builder). Same for the Telepathy powers known by Kyriss and Madail (text).

21. **Named characters' free Emanations**: Samus (Dread Visage), Kyriss (Quicksilver Grace + Transfixing Presence), Cor'bax (Miasma of Decay Emanation + Crushing Limbs), Madail (Horned Crown), Ka'Bandha (Molten Blood + Horned Crown) - built as linked rules. Named characters cannot buy further Emanations, Daemonic Weapons or Forms (their entries list no options). Question: confirm.

22. **Madail's Dominion rules (L2227-2235)**: "possesses the Core Dominion Rules of the Aetheric Dominion selected" - shown through the Dominion configuration entry (not linked on Madail himself, since it varies).

23. **Arch-Daemon Winged cost (L1797, L2714)**: +60 points in both places - built +60.

24. **Swarms "may select one Daemonic Emanations" (L1228)**: built as 1 Emanation (General, or Dominion if Favoured), per model at the Lesser cost.

25. **Emanation costs in the summary table vs. descriptions**: General Emanations L2541-2553 are used. "Unnatural Vigour", "Preternatural Speed" etc. "may only be selected once" - every Emanation is 0-1 per unit anyway.

26. **Daemon Brutes inside the Retinue and Vanguard of Hell (L999)**: a Retinue forms one unit with the Daemon Lord (MV 3), so the unit uses MV 3 (L3259). Built: Vanguard of Hell is still listed on the Retinue. Question: does Vanguard of Hell ever apply to a Retinue?

27. **Ruinstorm Possessed Troops**: Support Unit - they cannot fill compulsory Troops (built: no "Compulsory Troops Eligible"). Same for Daemon Swarms.

## Rules shown as text only (not enforced)

- Daemonic Instability, Manifestation Value, The Veil Thins, Aetheric Reserves, Warp Portals (allowance of 1 per full 750 points of the Detachment, placement, Manifestation Capacity, Sealing, If the Rifts are Closed).
- Aetheric Dominion effects (all Core Dominion Rules), Favoured Archetype benefits other than access to Dominion Emanations (which IS enforced), Greater Manifestation effects (the Manifestation itself is added automatically).
- The Army's Warlord / Lord of the Ruinstorm (Daemon Lord must be Warlord), Warlord Traits.
- Allied Forces restrictions (Independent Characters joining across Detachments, allied models and Portals, Allegiance compatibility of allies).
- Malefic Daemonology summoned Daemons.
- Lords of War / Fortifications only by mission or agreement.
- Shepherd of Malign Intent (nominated enemy type), Vanguard of Hell, Daemon Brute Retinue behaviour in play, Slaves to Darkness (no Objectives, no IC may join), Unstoppable, Apex Manifestation.
- Daemonic Forms' change of Unit Type (Jump Infantry / Flying Monster / Cavalry / Beast).
- Named character rules: Born of Murder, Noisome Tide of Flesh, Lord of Murder, Miasma of Rage, Scythe of Hatred, Eternal Rivalry, psychic powers known.
- Ruinstorm Psychic Powers effects (selection is enforced for Sorcerous Conduit).
