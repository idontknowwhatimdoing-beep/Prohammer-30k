# V - White Scars: questions for the author

Source: `/home/claude/src/legions/V_White_Scars.txt` (line numbers refer to that file).
Module: `tools/legions/v_white_scars.py`.

## Legion rules

1. **Mounted Brotherhoods is optional?** L29-30: "Legion Bike Squadrons may be selected as Troops choices ... Legion Bike Squadrons selected as Troops may fulfil the army's compulsory Troops selections."
   *Built:* each Legion Bike Squadron has a "Selected as Troops (Mounted Brotherhoods)" toggle. When it is ticked the squadron is a Troops choice and can fill a compulsory Troops slot. Without it the squadron stays Fast Attack.
   *Question:* Should a player be able to pick Troops or Fast Attack for each squadron (as built)? Or are Bike Squadrons always Troops in a White Scars army?

2. **Skilled Rider on characters.** L19: "White Scars models mounted on Bikes or Jetbikes gain the Skilled Rider special rule."
   *Built:* Skilled Rider is linked on Bike, Sky Hunter, Attack Bike and Golden Keshig units and on the named Khans' Jetbike upgrade. A Praetor or Centurion on a bike only gets it from the Legion rule text.
   *Question:* Is that enough, or should the builder show Skilled Rider on every character that takes a bike?

3. **Rules shown only as text (not enforced):** Swift Advance (L5-14), the Hit & Run condition that every model including an attached IC must be mounted (L23), Blood Feud-type play rules, all in-game effects of the Rites of War and characters.

## Armoury

4. **Power Glaive cost where a sergeant's own list sells a Power Weapon for +10.** L117: "Any White Scars Character able to select a Power Weapon may instead select a Power Glaive for +25 points. A model already equipped with a Power Weapon as part of its basic wargear may exchange it for a Power Glaive for +10 points."
   *Built:* wherever a Character can pick a Power Weapon, a Power Glaive is added beside it: +10 where the Power Weapon is free (basic wargear), +25 everywhere else. This includes sergeant lists where the Power Weapon costs +10 (e.g. Veteran Sergeant). Non-character models ("any model may replace" blocks) do not get it.
   *Question:* Is +25 right in lists where the Power Weapon itself costs +10? Or should the Glaive always cost the Power Weapon price +10?

5. **Chogorian Warlance - who and where.** L129: "Any White Scars model with access to the Space Marine Armoury that is mounted on a Bike or Jetbike may purchase a Chogorian Warlance for +15 points."
   *Built:* offered in the Space Marine Armoury (counts towards the 100/50-point cap) of:
   - Praetor and Centurion (only while they have a Space Marine Bike)
   - Legion Biker Sergeant and Sky Hunter Sergeant
   - Command Squad specialists (only while the squad has taken bikes)

   The named Khans have no Armoury access, so they cannot buy one.
   *Question:* Is that the intended list? Should the Warlance count towards the Armoury points cap?

6. **Cyber-hawk limit.** L140: "One White Scars Praetor may purchase a Cyber-hawk for +10 points."
   *Built:* a "White Scars Wargear" option on the Praetor, limited to one per army. It is outside the 100-point Armoury cap. Jaghatai's own Cyber-hawk does not count towards that limit.
   *Question:* Is that right? Can an army with Jaghatai also have a Praetor with a Cyber-hawk?

7. **Horsetail Talisman - which ICs.** L150-151: "One White Scars Independent Character may purchase a Horsetail Talisman for +25 points. Only one Horsetail Talisman may be included in an army."
   *Built:* offered to the Praetor and Centurion (outside the Armoury cap). An error appears if the army has more than one.
   *Question:* May the named characters (Shiban, Hibou, Hasik, Qin Xa, Yesugei) buy it too? Their entries have no Armoury access.

## Stormseer Consul

8. **Psychic Hood.** L261-262: "A Stormseer may purchase: Psychic Hood ... +25 points. All other equipment is selected normally from the Space Marine Armoury."
   *Built:* the Stormseer can take the Armoury's Psychic Hood (+25), the same as a Librarian. It counts towards the Centurion's 100-point Armoury cap.
   *Question:* Should the Hood count towards the cap?

9. **Epistolary powers.** L250-255: Mastery Level 2 for +25 and "one additional Psychic Power from ... Divination, Biomancy, Telepathy, Pyromancy".
   *Built:* the Epistolary upgrade asks the player to choose one of those four disciplines. The builder has no list of individual powers.
   *Question:* Is choosing the discipline enough, or should each power be listed?

## Rites of War

10. **Chogorian Brotherhood - Bikes as Troops.** L277-278 and L303.
    *Built:* Sky Hunters become Troops automatically while the Rite is chosen, as with the base Sky Hunter Phalanx. Bike Squadrons still need the Mounted Brotherhoods toggle. Tactical, Assault and Breacher Squads stop counting as compulsory Troops.
    *Question:* Under this Rite, should Bike Squadrons become Troops automatically?

11. **Chogorian Brotherhood - Warlord on a Bike or Jetbike.** L300-302: "The army's Warlord must be mounted on either: a Space Marine Bike; or a Jetbike."
    *Built:* not enforced, because the builder does not track who the Warlord is. Praetors and Centurions can only upgrade a Bike to a Jetbike under the base Sky Hunter Phalanx Rite.
    *Question:* Should Independent Characters also get the +5 Jetbike upgrade under Chogorian Brotherhood?

12. **Chogorian Brotherhood - text only.**
    - Enforced: the 0-1 Heavy Support limit (L304).
    - Text only: Lightning Encirclement (Outflank, L282-288), Master of the Hunt, Strike and Vanish, and the 150 Victory Point penalty (L304).

13. **The Sagyar Mazan - enforced and not enforced.**
    - Enforced as errors: Loyalist only (L307, L343), no Jaghatai Khan, no Fortification.
    - Ebon Keshig automatically become Troops that can fill a compulsory slot (L330).
    - Not enforced: "The army may never contain more Vehicle units than non-vehicle Infantry units" (L343).
    - Not enforced: "Units which are required by their own rules to begin in Reserve may not be selected" (L335).

    *Question:* Which units are meant by L335? Can you list them so they can be forbidden?

14. **Ebon Keshig allegiance and limit.** L494-553 put no Allegiance restriction or 0-1 limit on the Ebon Keshig entry, although the Sagyar Mazan are Loyalist only.
    *Question:* Should Ebon Keshig be Loyalist only, or only available with this Rite?

## Units

15. **Golden Keshig Squadron (L416-489).**
    *Built:* 70 pts plus 55 per Golden Keshig (2-4), plus the Champion, so 180 for three models. It has Deep Strike and Skilled Rider but no Hit & Run (Born in the Saddle only names Bike and Sky Hunter squadrons).
    *Questions:*
    - Should it have Hit & Run?
    - Should it be 0-1?
    - Does the Champion get Space Marine Armoury access?
    - Can the Champion take one of the Jetbike weapon swaps (L486 says "one Golden Keshig")?

16. **Ebon Keshig transport.** L552: "A squad of five models may select a Land Raider, Dreadclaw Drop Pod or Spartan Assault Tank where Transport Capacity permits."
    *Built:* "Land Raider" is read as Phobos or Proteus. The transport choice disappears when the squad has more than five models, even for the Spartan (capacity 25).
    *Question:* Should a squad of 6-10 be able to take a Spartan?

17. **Dragon Dao profile.** L520-524 gives no profile table.
    *Built:* two profiles: One-Handed (User, Power Weapon) and Two-Handed (User +2, -2 Initiative, no bonus Attack).
    *Question:* Is that correct?

18. **Dark Sons of Death - points.** L555 and L619: 200 points for 5 models, but extra models cost +35.
    *Built:* 60 pts plus 35 per Dark Son, plus the Death Speaker.
    *Question:* Please confirm the 200 base price.

19. **Dark Sons of Death - rules and weapons.**
    - Dual Pistols (L614): built as the Destroyer version ("Dual Pistols (Destroyers)").
    - Hand Flamer swap costs +5 here, but +10 in the normal Destroyer Squad. Please confirm.
    - L653 says "Rhino, Drop Pod, Dreadclaw,Drop Pod or Land Raider": read as Rhino, Drop Pod, Dreadclaw or Land Raider Phobos.

    *Questions:*
    - Do Dark Sons count as a Destroyer Squad for the Legion Destroyer Company Rite (2 weapons per 5, Troops)?
    - Should they be 0-1?

20. **Death Speaker armoury.** L645: "may select up to 50 points of permitted weapons and wargear from the Space Marine Armoury."
    *Built:* Armoury wargear only. His Two Bolt Pistols and Power Glaive have no swap slots, and Artificer Armour is only offered at the listed +10.
    *Question:* Which weapons should he be able to replace from the Armoury?

21. **Falcon's Claws (L672-760).**
    *Built:*
    - Force Organisation text is mixed with the Sabotage rule (L707-711); read as Fast Attack, 0-1 per Detachment.
    - 32 pts plus 22 per Falcon's Claw, plus the Leader, so 120 for five.
    - Sabotage uses its own rule entry; the text is identical to the Vigilator's.
    - The Leader's 50-point Armoury may replace his Bolt Pistol.

    *Question:* Is this correct?

## Characters

22. **Iron Halo army limit.** Qin Xa (L890), Hibou Khan (L1110) and Hasik (L1175) carry an Iron Halo. The base army list allows "normally no more than one Iron Halo" per army, and every Praetor has one.
    *Built:* their halos are a separate item, "Iron Halo (Named Character)", that does not count towards the limit.
    *Question:* Do named characters' Iron Halos count towards the one-per-army limit?

23. **Qin Xa retinue.** L878: "one Ebon Keshig squad or Legion Terminator Command Squad."
    *Built:* both are offered. Qin Xa is Master of the Legion and Fearless and has no options.
    *Question:* Should he have Krak Grenades or other options like the others?

24. **Yesugei's extra power.** L934: "he may select one psychic power from the normal Psychic Powers list."
    *Built:* he chooses a discipline from Biomancy, Divination, Pyromancy or Telepathy, the same list as the Stormseer.
    *Question:* Is Telekinesis (or any other discipline) allowed?

25. **Yesugei's HQ slot.** Yesugei has Legion Support Officer, so he cannot fill the compulsory HQ.
    *Question:* He has no retinue. Is that intended?

26. **Veteran Squad retinue (Hibou, Hasik).** L1097 and L1165.
    *Built:* the Veteran Squad retinue can buy "Space Marine Bikes (entire squad)" at +20 per model while the Khan has a Space Marine Bike. It keeps its own Jump Pack option and Dedicated Transport; neither is blocked when bikes are taken.
    *Question:* Should bikes exclude Jump Packs and a transport, as for the Command Squad?

27. **Jetbike Khans' retinue.** When a Khan upgrades to a Jetbike, his retinue may still only buy Space Marine Bikes (L1025 says "may purchase a Space Marine Bike").
    *Question:* Should they get Jetbikes instead?

28. **Breath of the Storm profile** (L1089). Shown as Strength "User +2/+1": +2 when Hibou charged, +1 otherwise.

## Jaghatai Khan

29. **Allegiance.** L1260 onward has no Allegiance restriction.
    *Built:* none.
    *Question:* Should he be Loyalist only?

30. **Primarch Retinue.** L1433-1436 lists only the Legion Honour Guard Squad and the Golden Keshig Squadron.
    *Built:* only those two; the Terminator Command Squad is not offered.
    - The Honour Guard may take "Jetbikes (entire squad)" at +35 per model, only while Jaghatai has the Sojutsu Pattern Voidbike.
    - With the Voidbike, his Unit Type changes to Jetbike (Character).

31. **Master of the Hunt name clash.** The Rite effect (L291) and Jaghatai's rule (L1404) are both called "Master of the Hunt".
    *Built:* the Primarch's rule is named "Master of the Hunt (Jaghatai)".
