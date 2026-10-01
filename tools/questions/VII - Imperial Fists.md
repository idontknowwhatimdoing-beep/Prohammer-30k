# VII - Imperial Fists: questions for the author

Source: `/home/claude/src/legions/VII_Imperial_Fists.txt` (line numbers refer to that file).
Module: `tools/legions/vii_imperial_fists.py`.

## Legion rules

1. **Legion rules are only text.** L5-27: Disciplined Fire, Fortification Masters (incl. "they may place D3 additional 6\" sections of razor wire or tank traps", L20) and Blind to the Risk.
   *Built:* all three are shown on the Legion entry, with no builder effect. Nothing in the text changes the Force Organisation, adds Consuls or changes existing units, so none of that was built.
   *Question:* Is it right that the VII Legion has no Consul and no changes to existing units?

## Armoury

2. **Solarite Power Gauntlet: cost and profile.** L120: "Any Imperial Fists Character with access to the Space Marine Armoury may purchase a Solarite Power Gauntlet for +30 points. A model already equipped with a Power Fist may exchange it for a Solarite Power Gauntlet for +5 points."
   *Built:* wherever a Character model can pick a Power Fist (Praetor/Centurion Armoury, sergeant/champion option lists, Terminator sergeants, Huscarl Captain, Templar Champion, Warder Sergeant...), a Solarite Power Gauntlet appears next to it. It costs +5 where the Power Fist is free and +30 everywhere else, including lists where the Power Fist itself is only +10/+15. Named characters cannot take it. The profile has no AP in the book; it is built as `- / 10 / - / Power Weapon, Unwieldy, Specialist Weapon`.
   *Question:* Should the Gauntlet always be +30, or "Power Fist price +5" in sergeant lists where the Fist is cheaper than 25?

3. **Vigil Pattern Storm Shield.** L131-134: "An Imperial Fists Independent Character may purchase a Vigil Pattern Storm Shield for +25 points. The bearer may carry no more than one weapon in addition to the shield."
   *Built:* +25 in the "Additional Wargear" of the Praetor and Centurion Armoury. It counts towards the 100-point Armoury cap. The "only one other weapon" rule and stacking with Iron Halo / Refractor Field / Combat or Boarding Shield are not enforced (text only). Named characters cannot buy it; Polux has one as fixed wargear.
   *Question:* Does it count towards the 100-point Armoury cap ("in addition to the normal Space Marine Armoury", L116)? Should the builder stop combining it with other invulnerable-save wargear, or with two weapons?

4. **Teleportation Transponders: who may buy them.** L142-144 (TDA units +15, TDA Independent Characters +10) and L213-215 (Hammerfall: any Infantry unit +15, any Independent Character +10).
   *Built:*
   - Always available: Legion Terminator Squad, every Legion Terminator Command Squad, every Huscarl Terminator Retinue, and the Praetor/Centurion while wearing Terminator Armour. Evander Garrius (Cataphractii) always has the option too.
   - Hammerfall Strike Force only: every other unit whose models are all Infantry (Tactical, Breacher, Veteran, Destroyer, Recon, Seeker, Heavy Support, Command/Honour Guard retinues, Templars, Warders, Techmarine Covenant). Also the Praetor/Centurion without Terminator Armour, and Sigismund, Rann, Polux and Diaz.
   - Jump Infantry (Legion Assault Squad) never gets it. Rogal Dorn never gets it (a Primarch may not buy wargear).
   *Question:* Do named characters get Transponders (all of them under Hammerfall, Garrius always)? Does "Infantry" include Jump Infantry? Should Rogal Dorn be able to buy them? See 8: without them he can never be Warlord in a Hammerfall army.

## Rites of War

5. **The Stone Gauntlet: compulsory Troops.** L161-163 and L185-187.
   *Built:* under this Rite, Phalanx Warder Squads become Troops and count for compulsory Troops. Legion Breacher Siege Squads still count. Legion Tactical and Assault Squads no longer count for compulsory Troops; they can still be taken as normal Troops. Max one Fast Attack is enforced.
   *Question:* Is this the intended reading of "compulsory Troops choices must be selected from" (non-compulsory Tactical Squads still allowed)?

6. **The Stone Gauntlet: limitations not enforced.** L188: "The Detachment must include at least one Independent Character equipped with either a Boarding Shield or Vigil Pattern Storm Shield." L189: "No unit in the Detachment may voluntarily deploy using Deep Strike."
   *Built:* both are text only. The builder cannot tell a Centurion's Boarding Shield apart from the Boarding Shields of Breacher or Warder squads, so the IC check cannot be counted reliably. Teleportation Transponders stay purchasable.
   *Question:* OK as text only? Should Teleportation Transponders (and Drop Pods / Deep Strike transports) be hidden under this Rite?

7. **The Stone Gauntlet / Templar Assault effects are text only:** Shield Wall, Unyielding Line, The Hammer Behind the Shield (L166-181), Crusading Assault and Swords of the Legion (L252-261).

8. **Hammerfall Strike Force: Warlord with Transponders.** L235: "The army's Warlord must be equipped with Teleportation Transponders."
   *Built:* Independent Characters buy Transponders through one shared upgrade. While this Rite is chosen, the builder shows an error if no Independent Character in the Detachment has that upgrade (it cannot know which model is the Warlord). Because Rogal Dorn must be Warlord and cannot buy Transponders, an army with Dorn always shows this error.
   *Question:* Can Rogal Dorn be used with Hammerfall at all (e.g. may he purchase Transponders for +10)?

9. **Hammerfall: other limitations.** L236: "Every Vehicle in the Detachment must begin the battle in Reserve." (text only). L237: no Fortification (enforced).
   *Question:* Do Immobile Tarantula Sentry Guns also have to start in Reserve, and how would they arrive?

10. **Templar Assault: transports.** L265-268: a Templar Brethren Squad may take a Land Raider Phobos or Proteus; "A Templar Brethren Squad of a size which cannot be carried by either vehicle may instead select a Legion Spartan Assault Tank". L367 (the squad's own entry) already allows "a Rhino, Drop Pod, Dreadclaw Drop Pod or Land Raider".
   *Built:* the squad may always take Rhino, Drop Pod, Dreadclaw, Land Raider Phobos or Land Raider Proteus. The Spartan Assault Tank is shown only while Templar Assault is chosen, with no size check: the squad has at most 10 models, so it always fits in a Land Raider.
   *Question:* Which Land Raider variants does "Land Raider" in L367 mean? When can a Templar squad be too large for a Land Raider (only with attached characters)?

11. **Templar Assault: Warlord weapon and compulsory Troops.** L273, L276.
   *Built:* Templar Brethren Squads become Troops and count for compulsory Troops. Tactical, Assault and Breacher squads no longer count. The 0-1 limit is lifted, and max one Fast Attack and no Fortification are enforced. The Warlord's weapon requirement is text only.

## Units

12. **Templar Brethren Squad 0-1.** L315: "0–1".
   *Built:* 0-1 per Detachment as an Elites choice, lifted under Templar Assault. Templar squads taken as a retinue for Sigismund or Rogal Dorn do not count towards this limit.
   *Question:* Is the limit per Detachment or per army? Does a retinue Templar squad count towards it?

13. **Templar Brethren: power weapons and frag grenades.** L345: "Up to five models may replace their Rending Weapon with: Power weapon +10". L328-332: the wargear has no Frag Grenades; frag is bought for +1 per model (L350).
   *Built:* up to five Templar Brethren (not the Champion) may take a Power Weapon for +10. The Champion changes weapons through his 50-point Armoury, where the Bolt Pistol and Rending Weapon can be replaced (Combat Shield removed from his list, since he already has one).
   *Question:* Can the Champion be one of the five at +10? Is it right that the squad has no Frag Grenades by default (the same applies to Phalanx Warders, L458-462, who also have no Bolt Pistol)?

14. **Phalanx Warder Sergeant Armoury.** L497.
   *Built:* the Sergeant's 50-point Armoury may replace his Bolter and Power Weapon and add wargear (Combat Shield and Refractor Field removed because of the Boarding Shield). The "one per five models" special weapons are for Phalanx Warders only.

15. **Huscarl Terminator Retinue.** L540-626.
   *Built:*
   - Retinue only: for a Praetor in Terminator Armour (option hidden otherwise, error if the Praetor drops his Terminator Armour), Sigismund, Garrius and Rogal Dorn (no Terminator Armour needed for Dorn or Sigismund).
   - The Huscarl Captain's "50 points of permitted Terminator weapons and wargear" is built as replacement of his Combi-bolter / Power Weapon at Terminator-Sergeant Armoury prices, plus Bionics, Master-crafted Weapon and Purity Seals, capped at 50.
   - The book lists no Dedicated Transport, so the unit has none.
   - Teleportation Transponders +15 (see 4).
   *Question:* Should Huscarls be allowed a Land Raider / Spartan / Dreadclaw like other Terminator units? Can a Centurion in Terminator Armour take them?

16. **Tarantula Sentry Gun Battery.** L673-729: "Fast Attack • 0–2 Batteries", 1-3 guns at 20 points each.
   *Built:* Fast Attack, 0-2 per Detachment, each gun configured separately (Twin-linked Heavy Bolter or Twin-linked Lascannon +15). Firing Mode, Automated Targeting and Disposable Platform are text. The profile gives no Hull Points or crew; "Immobile" is linked from the base rules.
   *Question:* Does a Battery use one Fast Attack slot? (It counts as one under the Stone Gauntlet/Templar one-Fast-Attack limit.)

## Characters

17. **Sigismund.** L741-798.
   *Built:* HQ, Master of the Legion. His Iron Halo is a separate "Iron Halo (Named Character)" so it does not use up the army's single Iron Halo. The Black Sword profile is `User +2, Power Weapon, Two-Handed, Master-crafted`. "Massive Wound (D3)" (L766) is text only; it is not defined in the core rules list.
   *Question:* Should Sigismund's Iron Halo count towards the one-per-army limit? Where is Massive Wound defined?

18. **Fafnir Rann's weapons.** L850-851: the book gives no profiles for The Headsman and The Hunter.
   *Built:* two weapons, each `- / User / - / Power Weapon`.

19. **Alexis Polux.** L892-952: his Force Organisation block shows "HQ" (L925); his special rules include Master of the Legion. His Master-crafted Power Fist is built as `x2, Power Weapon, Unwieldy, Specialist Weapon, Master-crafted`. Teleport Transponder (his own rule) and The Crimson Fist are text only.

20. **Camba Diaz: Master of the Legion?** L1017-1021: his special rules do not include Master of the Legion (Sigismund, Rann, Polux and Garrius have it).
   *Built:* not a Master of the Legion, but he can fill the compulsory HQ slot.
   *Question:* Is that intended?

21. **Evander Garrius.** L1056-1057: Subjugator has no AP in the book; built `- / 10 / - / Power Weapon, Unwieldy, Specialist Weapon, Master-crafted`. Retinue: Huscarl Terminator Retinue or Legion Terminator Command Squad.

22. **Rogal Dorn: allegiance and profile.** L1108-1274.
   *Built:*
   - No Loyalist-only restriction, because the text does not state one.
   - Save shown as printed ("1+"); Auric Armour counts as Primarch Armour (4+ Invulnerable).
   - Storm's Teeth: `User +2, Power Weapon, Two-Handed, Shred, Rampage`. Voice of Terra: 24" S5 AP4 Salvo 3/5, Rending.
   - Primarch Retinue: Honour Guard, Terminator Command Squad, Huscarl Terminator Retinue or Templar Brethren Squad.
   *Question:* Is Rogal Dorn Loyalist-only?

## Shown as text only (not enforced by the builder)

23. Disciplined Fire, Fortification Masters, Blind to the Risk; Shield Wall / Unyielding Line / Hammer Behind the Shield; Blinding Luminescence; Crusading Assault; Swords of the Legion; the Stone Gauntlet IC-with-shield and no-Deep-Strike limits; Hammerfall vehicles in Reserve; the Templar Assault Warlord weapon; Righteous Zeal; Tarantula Firing Mode / Automated Targeting / Disposable Platform; Kingslayer, Black Sword, Headsman and Hunter, Executioner's Tax, Lord Seneschal, Polux's Teleport Transponder and Crimson Fist, Hold the Line, Tyrant of Cthonia; all of Rogal Dorn's special rules; the Vigil Pattern Storm Shield "one other weapon" rule.
