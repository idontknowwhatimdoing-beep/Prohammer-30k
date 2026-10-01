# XVIII - Salamanders: questions for the author

Source: `/home/claude/src/legions/XVIII_Salamanders.txt` (line numbers refer to that file).
Module: `tools/legions/xviii_salamanders.py`.

## Legion rules

1. **Sturdy is not in the profiles.** L18-19: "All Salamanders models with an Initiative characteristic, except Dreadnoughts, suffer -1 Initiative. This modifier applies after all other profile modifications."
   *Built:* all profiles show the printed Initiative (e.g. Firedrake I4, Vulkan I5). The -1 is only in the rule text.
   *Question:* Should the builder show the reduced value in every Salamanders profile (including Vulkan and the named characters), or keep the printed value plus the rule?

2. **Rules shown only as text (not enforced):** Promethean Cult (L5-13), Sturdy (L16-20), Never Give Up (L23-28), all in-game Rite of War effects, Covenant "may not deploy using Deep Strike" (L152, only units that *must* Deep Strike are flagged), Awakening "no more than one Jump Infantry, Jetbike, Skimmer and Flyer unit" (L235) and "no Allied Detachment" (L237), Master Artificer / Keeper of the Forge (free upgrades chosen before deployment, L1370-1375), Firedrake retinue Master upgrade for Numeon (see 9).

## Armoury

3. **Heavy Flamer instead of a Flamer: +10 total or +10 on top of the Flamer?** L85: "Where a Legion Tactical Squad or Legion Veteran Squad may purchase a Flamer, it may instead purchase a Heavy Flamer for +10 points."
   *Built:* a "Heavy Flamer (Fire-based Warfare)" option for +10 in the Tactical special weapons and Veteran specialist weapons groups (the Flamer itself costs +5 there).
   *Question:* Is +10 the full price, or +10 more than the Flamer (= +15)?

4. **Fire-based Warfare profiles are global.** L69-84: Flamer S5 AP5, Heavy Flamer S6 AP4.
   *Built:* every Flamer / Heavy Flamer profile in the Salamanders catalogue uses the Dragon's Breath values (also Combi-Flamer, vehicle Heavy Flamers, Suspensor Web Heavy Flamers). Hand Flamers are unchanged.
   *Question:* Correct that vehicle-mounted Heavy Flamers and the Flamer part of a Combi-Flamer get +1 S too? Hand Flamers stay S3?

5. **Artificer Armour for non-IC characters.** L64-65: "+15 points even if his unit entry would not normally allow him".
   *Built:* every Power Armour sergeant's Armoury offers Artificer Armour for +15 (counts towards the 50-pt cap). Sergeants whose entry already lists it cheaper (Adherent, Sanctifier: +10) keep their own +10 option. Sergeants with no Armoury access (Sanctifier Sergeant) do not get the +15 one.
   *Question:* OK that it counts against the 50-point Armoury cap?

6. **Salamanders Mantle - who may buy it.** L52: "One Salamanders Independent Character in the army may purchase a Salamanders Mantle for +35 points."
   *Built:* Praetor and Centurion (all Consuls) Armoury, counting towards the 100-pt cap; an error appears if two Mantles (incl. Numeon's and Nomus' Mantle of the Elder Drake) are in the army.
   *Question:* Does the Mantle count towards the Armoury points cap, or is it bought on top?

7. **Reinforced Ceramite.** L104-105.
   *Built:* every Armoured Ceramite option on non-Land Raider / non-Spartan vehicles and Dreadnoughts costs +10 (where it was +20). Land Raiders and Spartans keep their price.
   *Question:* None unless some vehicle had a price other than +20 that should also become +10.

8. **Proscribed Munitions.** L110.
   *Built:* every Phosphex Bomb / Discharger / Canister Shot option is hidden and set to max 0 in this catalogue (no Salamanders entry grants one).

## Units

9. **Numeon's Firedrake retinue - Firedrake Master upgrade.** L997: "One Firedrake in that unit may be upgraded to a Firedrake Master at no additional points cost."
   *Built:* the Firedrake Terminator Squad already contains a Firedrake Master (L369), so Numeon's retinue is the normal squad. No extra free Master.
   *Question:* Does this mean a *second* Firedrake Master (two characters in the squad), or is it just a reminder? If the former, should the second Master get the 50-pt Armoury too?

10. **Firedrakes and Transport Capacity.** L404: "Land Raider, Dreadclaw Drop Pod or Spartan Assault Tank where Transport Capacity permits."
    *Built:* Land Raider Phobos / Proteus, Dreadclaw and Spartan offered; capacity (Terminators count double) is not checked, same as the base Terminator Squad.
    *Question:* OK, or should the Land Raider / Dreadclaw options disappear above 5 models?

11. **"Land Raider" for Pyroclast, Infernus and Sanctifier Squads.** L543, L696, L947.
    *Built:* Land Raider Phobos and Land Raider Proteus.
    *Question:* Any other Land Raider pattern (e.g. Achilles) intended?

12. **Firedrake Storm Shield swap - two per five.** L397: "For every five models in the squad, up to two Firedrakes may replace their Dragonscale Storm Shield".
    *Built:* 2 swaps per full 5 models (5-9 models: 2, 10 models: 4).
    *Question:* Correct?

13. **Infernus Sergeant pistols.** L672-687: any model may replace either Hand Flamer with a Volkite Serpenta (+5) or Plasma Pistol (+15); the Sergeant may replace either with an Inferno Pistol (+10).
    *Built:* Sergeant: each Hand Flamer separately -> Volkite Serpenta +5, Plasma Pistol +15, Inferno Pistol +10. Destroyers: up to two swaps per model; a heavy weapon with Suspensor Web uses up one Hand Flamer.
    *Question:* Inferno Pistol at +10 here (Armoury price is +15) - intended?

14. **Infernus heavy weapons with Jump Packs.** L664-669: Heavy Flamer / Multi-Melta with Suspensor Web are allowed regardless of Jump Packs. Built that way. *Question:* intended?

15. **Sanctifier "replace his Bolter and Bolt Pistol".** L918-920.
    *Built:* one "replace Bolter" block per model (Second Bolt Pistol free, Rotor Cannon +10, Two Hand Flamers +10, Two Volkite Serpentae +10); the Bolt Pistol stays listed in the unit wargear even when the pair of pistols replaces it.
    *Question:* None (display limitation only).

16. **Pyroclast Warden / Adherent Sergeant Armoury and Salamanders Armoury.** L539, L802: "up to 50 points ... from the Space Marine Armoury and Salamanders Armoury."
    *Built:* Space Marine Armoury (incl. Inferno Pistol +15). Pyroclasts already wear Artificer Armour, so it is not offered. Salamanders Mantle is IC-only, so not offered.

17. **Cassian Dracos - Armoured Ceramite.** L1234-1235: "Cassian uses the normal Reinforced Ceramite rules." His wargear list (L1257-1263) has no Armoured Ceramite.
    *Built:* Armoured Ceramite is part of his fixed wargear (no cost).
    *Question:* Does he have it for free, or may he buy it for +10? (No options are printed for Cassian.)

18. **Cassian Dracos - Hull Points / Unit type.** Profile L1203-1219 has no Hull Points and he is "Vehicle (Walker, Character)" as a non-HQ Elites 0-1 choice. Built as printed (Elites, unique). *Question:* any Hull Points value to show?

## Characters

19. **Keeper of the Keys.** L1076-1077.
    *Built:* with Nomus Rhy'tan in the Detachment, one Legion Dreadnought or Legion Contemptor Dreadnought (max one per Detachment) can tick "Selected as HQ (Keeper of the Keys)": it becomes a non-compulsory HQ choice. Leviathan / Deredeo etc. are not included.
    *Question:* Correct that only those two Dreadnoughts qualify?

20. **Iron Halo on named characters.** Numeon and Nomus carry an Iron Halo (L1014, L1094). Built as their own wargear; they do not count against any one-Iron-Halo limit. *Question:* OK?

21. **Xiaphas Jurr is not a Master of the Legion** (L1182-1187 list no Master of the Legion). Built that way; he can be the compulsory HQ. *Question:* confirm.

22. **Jurr and The Awakening Fire.** L1160 "counts as a Legion Chaplain Consul for army construction requirements and Rites of War."
    *Built:* Nomus or Jurr in the Detachment satisfies "must include a Legion Chaplain Consul" (L234).

## Rites of War

23. **The Covenant of Fire - FA + HS limit.** L153.
    *Built:* an error when (Fast Attack + Heavy Support choices) > Troops choices in the Detachment, checked for up to 15 Troops choices. Units made Troops by the Rite (Pyroclasts, Infernus) count as Troops.
    *Question:* Do the Rite's Troops (Pyroclasts/Infernus) count as Troops for this limit? Do Dedicated Transports count? (Built: no, they are not FA/HS choices.)

24. **The Covenant of Fire - Deep Strike.** L152. *Built:* error if a Legion Drop Pod, Dreadclaw or Dreadnought Drop Pod is in the Detachment. Teleport Homers / Terminators deploying by Deep Strike are only covered by the text. *Question:* is Dreadclaw a "must Deep Strike" unit in your rules?

25. **The Awakening Fire - Fury of the Salamander.** L217. *Built:* a Librarian Consul in a Detachment with this Rite may take "Fury of the Salamander (Pyromancy)" as a free option. *Question:* does it replace one of his normal powers, or is it extra?

## Primarch

26. **Vulkan's Primarch's Chosen.** Vulkan uses the normal Primarch rules (2,000 pts, or 1,500 with Primarch's Chosen). Loyalist only (L1448) - error if the army is Traitor. *Question:* none.
