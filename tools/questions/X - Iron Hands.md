# X - Iron Hands: questions for the author

Source: `/home/claude/src/legions/X_Iron_Hands.txt` (line numbers refer to that file).
Module: `tools/legions/x_iron_hands.py`.

## Legion rules and Armoury

1. **Bionics cost for characters.** L19: "Iron Hands Characters and Veteran Sergeants may purchase Bionics for 5 points."
   *Built:* every character model that can buy Bionics now pays 5 points. Characters with no Bionics option get a "More Machine than Man" option for 5 points. Units made only of Infantry, Jump Infantry, Bikes and/or Jetbikes get "Bionics (entire unit)" for +3 points per model.
   *Question:* Does the unit-wide +3 option also cover the unit's sergeant? (As built, it does, because Bionics are given to the whole unit.)

2. **Servo-Arm, Albian Power Gladius and Mechadendrites: who can take them.** L29, L34, L60.
   *Built:*
   - Servo-Arm (+30) and Albian Power Gladius (+10): in every Space Marine Armoury (Praetor, Centurion, and all 50-point sergeant, champion and specialist armouries). Both count towards the Armoury points cap.
   - Servo-Arm is hidden while the model has a Jump Pack. It is also hidden for a Forge Lord Consul, who already has one.
   - Mechadendrites (+15): Praetor, Centurion and every model named "... Sergeant", plus the Gorgon Sergeant and the Morlock Captain.
   *Questions:*
   - Should Apothecaries, Champions and Standard Bearers ("Character with access to the Armoury") also get the Gladius? (As built, they do.)
   - Does the Morlock Captain count as a "Sergeant" for Mechadendrites?

3. **Splinter Bolts.** L54-56. *Built:* "+5 per unit" on every Infantry unit that has a bolter-type weapon. It is hidden, and an error is shown, if the unit also has Special Issue Ammunition. The Fury of the Legion restriction is text only.

4. **Dangerous Weaponry.** L39. *Built:* wherever a Flamer can be selected, a Graviton Gun is offered for +15. Squad caps that count Flamers also count the Graviton Gun.
   *Question:* Is the price always +15? Or should it be the Flamer's price in that list +15? (As built, it is always +15.)

5. **Iron Father's Iron Halo.** L83. *Built:* the Iron Father, Meduson, the Gorgon Sergeant and the Morlock Captain each carry an "Iron Halo (Iron Hands)" that does not count towards the normal one-Iron-Halo-per-army limit.
   *Question:* Is that correct, or should these count towards the limit?

## Rites of War

6. **The Head of the Gorgon limitations.** L121-123.
   *Built and enforced:*
   - 0-1 Fast Attack.
   - An error if the Detachment has more than one Consul other than Forge Lords.
   - Relics of War: Blessed Autosimulacra cost 0.
   - Scions of Iron: Land Raider Phobos and Land Raider Proteus are added to the Dedicated Transports of Infantry units that can take a Rhino. They are only shown while the unit has 10 models or fewer.
   *Not enforced:* "may not include an Allied Detachment drawn from another Space Marine Legion" (Allied Detachments are not modelled in this catalogue).
   *Question:* Is "Land Raider" for Scions of Iron limited to Phobos and Proteus as written? (Built so.)

7. **Company of Bitter Iron.** L133-153.
   *Enforced:*
   - Medusan Immortals become Compulsory Troops Eligible and lose their 0-1 limit.
   - Errors for a Traitor army, for Ferrus Manus, and for a Detachment with no Medusan Immortal Squad.
   *Not enforced:*
   - "No Allied Detachment".
   - The requirement that the Immortals fill one of the *compulsory* Troops slots (only "at least one Immortal Squad" is checked).
   *Question (L133 vs L207-208):* Immortals are already listed as "Troops, 0-1". So without the Rite, they are a Troops choice that cannot fill compulsory Troops. Is that correct?

## Units

8. **Medusan Immortals Dedicated Transport.** L262: "Rhino, Drop Pod, Dreadclaw Drop Pod or Land Raider". *Built:* Land Raider = Land Raider Phobos or Land Raider Proteus.
   *Question:* Are other Land Raider variants (e.g. Achilles) allowed?

9. **Venerable Forge Lord.** L571-572: the +1 Attack is not included in the profile. *Built:* the profile's Attacks change from 2 to 3 while both close-combat weapons are kept.
   - It has no Legiones Astartes (Iron Hands) rule (none is listed at L606-609).
   *Question:* Should it have that rule?

10. **Gorgon/Morlock Terminators: pair of Lightning Claws.** Gorgons (L396) have the pair option. Morlocks have none.
    *Question:* Should Morlocks have it too? (Not built.)

## Characters

11. **Castrmen Orth.** L842-858.
    *Built:*
    - A +50 upgrade on every Tank (one per army).
    - It sets the Vehicle's BS to 5.
    - It adds the HQ category and "Compulsory HQ Eligible" to the unit.
    *Not enforced:* "not a Vehicle already commanded by another named character"; Vehicles inside a multi-vehicle squadron are not excluded.
    *Questions:*
    - Can Orth's Vehicle fill the compulsory HQ slot?
    - Can he command a Tank that is part of a squadron?

12. **Allegiance.** Shadrak Meduson (Fury of the Survivors, L716), Gabriel Santar and Ferrus Manus have no allegiance restriction in the text. *Built:* no restriction.
    *Question:* Should any of them be Loyalist only?

13. **Gabriel Santar + Morlocks as one HQ selection** (L900). *Built:* the Morlocks are a retinue with no slot of their own. The 0-1 Morlock limit is only checked for Morlocks taken as a separate Elites choice.

14. **Ferrus Manus weapons.** L1110: he may fire up to two Carapace weapons per Shooting phase. *Built:* Forgebreaker = Thunder Hammer profile + Master-crafted + Armourbane. Living Metal Hands = S8 Power Weapon. The two-weapons limit is text only.

## Text-only rules (not enforced by the builder)

Wisdom of the Omnissiah, Inexorable Advance, the Bionics recovery on 5+, Mechadendrites, Blessed Autosimulacra repairs, Gorgon Field, Rites of Battle, Ground of Choice, Armoured Encirclement, Immortal Hatred, Bitter Duty, No Death Without Purpose, Old & Wise, Hard to Kill, Auto-Repair Simulacra, Fury of the Survivors, Battlesmith, Tank Hunters, The Gorgon, Master of the Forge, Forged for War.
