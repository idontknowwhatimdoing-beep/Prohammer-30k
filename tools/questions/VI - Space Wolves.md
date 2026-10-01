# VI - Space Wolves: questions for the author

Source: `/home/claude/src/legions/VI_Space_Wolves.txt` (line numbers refer to that file).
Module: `tools/legions/vi_space_wolves.py`.

## Legion rules and Legion Organisation

1. **HQ count above 3,000 points.** L23-27: "one HQ selection for every full or partial 750 points ... 2,251–3,000 points: 4 HQ". The table stops at 3,000.
   *Built:* the HQ maximum goes up with the points (2 -> 3 above 1,500, 4 above 2,250). Errors require **exactly** 1/2/3/4 HQ in the four bands. I continued the rule to 4,500 points (5 HQ up to 3,750, 6 up to 4,500). Above 4,500 there is only a warning to check the count by hand.
   *Question:* Does the rule go on past 3,000 points like this? Is "exactly n HQ" right, given that L28 says it "replaces the normal minimum and maximum"?

2. **What counts as an HQ selection.** *Built:* every unit with the HQ slot counts: Praetor, Centurion (also a Consul / Legion Support Officer), Hvarl, Geigor, Ohthere and Björn. Retinues (Varagyr, Command Squads, Wolf Retinue) do not count. Leman Russ is a Lord of War and does not count.
   *Question:* Should Legion Support Officers (Rune Priest, Ohthere) and Björn count towards the required HQ number?

3. **Chaplain and Librarian Consuls** (L28, L224, L252) are hidden on the Legion Centurion. Wolf Priest and Rune Priest are added instead.

4. **Text only (not enforced):** Hunters of Fenris (L7; Counter-Attack and Acute Senses appear only on the Legion entry, not on every unit), No Matter the Odds (L12), Blood Feud (L18).

## Armoury

5. **Frost Weapon cost.** L118: "+20 points. A model already equipped with a Power Weapon may exchange it for a Frost Weapon for +5 points."
   *Built:* wherever a Character can pick a Power Weapon, a Frost Weapon is added next to it. It costs +5 where the Power Weapon is free (basic wargear) and +20 everywhere else (Praetor, Centurion, Huscarls, Thegn, Command Squad characters...). Its profile is User +1, Power Weapon.
   *Question:* Is +20 right in lists where the Power Weapon itself costs +15? The Wolf Priest's Fang of Morkai counts as a Power Weapon (L238), but I did **not** let him swap it for a Frost Weapon. Should he be able to?

6. **Great Frost Blade** (L127-134). *Built:* +35, only for Praetor and Centurion (Independent Characters). It is offered in both of their weapon slots (Bolt Pistol / Chainsword). Profile: User +2, Power Weapon, Two-Handed, Master-crafted, -1 Initiative. Deathsworn can also take it from their own list (+10, L872).

7. **Wolf Pelt / Wolf Tooth Necklace / Wolf Tail Talisman - "Any Space Wolves Character"** (L138, L143, L149).
   *Built:* these are added to the Praetor/Centurion 100-pt Armoury and to every 50-pt Sergeant/Huscarl/Thegn Armoury, and they count towards those caps. Named characters cannot buy them, because they have no Armoury access.
   *Question:* Should they count towards the Armoury cap? Should named characters be able to buy them?

8. **Runic Armour** (L155-158). *Built:* +25 as an option in the Armour group of the Praetor and Centurion (it replaces Power Armour). It is hidden for the Forge Lord and Primus Nullificator Consuls, because those cannot take Artificer Armour either. The profile save is not changed automatically.

## Consuls

9. **Wolf Priest** (L223-246). *Built:* +35. He gets a Fang of Morkai in place of the Chainsword, plus a Rosarius, Rites of Battle and Oath of the Slayer. Like the base Chaplain, he cannot also buy a Refractor Field or Iron Halo. The Wolf Priest is still a normal Centurion: not a Support Officer, and he can fill the compulsory HQ.
   *Question:* Is that right?

10. **Rune Priest / Master of Runes** (L251-282). *Built:* +25. He gets a Runic Force Weapon in place of the Chainsword, a Wolf Tail Talisman (the Armoury Talisman is hidden for him), Psyker ML1, Legion Support Officer and Mystic Winds of Fenris. He may buy a Psychic Hood. Master of Runes is +25 (ML2) and must choose one discipline from Biomancy, Divination, Pyromancy, Telekinesis or Telepathy (no Daemonology, as for the base Librarian).
   *Question:* Is that the right discipline list?

## Units

11. **Grey Slayer / Grey Stalker / Jorlund Hunter Packs as compulsory Troops.** L390: "Grey Slayer Squads may fulfil compulsory Troops selections when using this Rite."
   *Built:* all three packs are Troops choices, but they do **not** fill the compulsory Troops normally. Grey Slayer Packs do so only under The Bloodied Claws.
   *Question:* Is that right? Without that Rite, a Space Wolves army still needs 2 Tactical/Assault/Breacher squads.

12. **Unit names.** L385/L390/L391 say "Grey Slayer Squads", but the unit is the "Grey Slayer Pack" (L408). I treated them as the same unit.

13. **Grey Slayer Combat Shield** (L478): "Any model may replace its Bolter with a Combat Shield +3". *Built:* for the Huscarl too (+3 in his Bolter slot; his normal Armoury Combat Shield stays +5). The Combat Shield, the special weapons and the Bolter swaps together are limited to one per model.

14. **Wolf Scout special/heavy weapons** (L752-762): "Up to two Wolf Scouts may each select ..." / "One Wolf Scout may instead take: Heavy Bolter / Missile Launcher".
   *Built:* up to two special weapons are **added** (nothing is replaced). A heavy weapon uses up one of the two places. The "any model may replace Bolt pistol and CCW" swap is separate.
   *Question:* Do the special/heavy weapons replace the Bolt pistol or CCW (or the Bolter/Shotgun/Sniper Rifle)? Is Scout Armour a 4+ save (as built, from the profile)?

15. **Yimira Stasis Bombs** (L834-837): "one Deathsworn may throw a Yimira Stasis Bomb instead of firing another weapon". No profile is given.
   *Question:* What is the thrown profile (range/S/AP/type)?

16. **Deathsworn Pack** has no character/leader (L844). Built that way: no Armoury.

17. **Varagyr Thegn** (L1179-1187): +25 upgrade of one Varagyr. *Built:* the Thegn (W2, A3) has his own Combi-bolter / Frost Weapon swaps, a Grenade Harness (+10) and a 50-pt Terminator Armoury. He cannot take one of the "1 per 5 models" heavy weapons.
   *Question:* May the Thegn take a heavy weapon? L1140 says "A Varagyr Thegn is a Character", but the composition (L1135) lists only Varagyr Terminators. Is the Thegn really optional?

18. **Chosen of the Jarl** (L1128). *Built:* the Varagyr appear in the Legion Praetor's retinue choice. They can be chosen only while the Praetor wears any Terminator Armour pattern (otherwise they are hidden and an error appears). Hvarl may also take them (L1324).

19. **Fenrisian Wolf Pack** (L1242-1289). It has no Legiones Astartes (Space Wolves) rule (none is listed), so it does not get Hunters of Fenris. Its special rule is called "Pack Hunters", which is also the name of a Pale Hunters effect (L346). In the builder it is called "Pack Hunters (Fenrisian Wolves)".

20. **Wolf Retinue** (L1289): "In addition to an Normal Retenue a Independent Character may take a Retinue of 2 Wolves for 24 pts".
   *Built:* a 24-pt upgrade "Wolf Retinue (2 Fenrisian Wolves)" with the Fenrisian Wolf profile. It is on the Praetor, Centurion (any Consul), Hvarl, Geigor and Ohthere. Leman Russ and Björn do not get it. The wolves are not separate model entries.
   *Questions:* Do the wolves have Pack Hunters (must charge)? Do they count for transport capacity? Should Legion Support Officers be able to take them too?

## Named characters

21. **Hvarl Red-Blade** (L1296-1351): HQ, Master of the Legion, only from 1,500 points (error), retinue Terminator Command Squad or Varagyr. OK as written.

22. **Geigor Fell-Hand** (L1406-1455): no Master of the Legion and no retinue are listed, so none were built. I left him able to fill the compulsory HQ.
   *Question:* Is that correct?

23. **Björn the Fell-Handed** (L1466-1513): HQ walker (190 pts), one per army. He has no Legiones Astartes rule and no options (no Dreadnought Drop Pod, no upgrades). He can fill the compulsory HQ.
   *Questions:* Can he fill the compulsory HQ? Does he count as an HQ for the Legion Organisation? Should he have the Legion rule or any vehicle upgrades / a drop pod?

24. **Ohthere Wyrdmake** (L1548-1625): HQ (L1597; the "Force Organisation" line at L1570 is empty), Legion Support Officer (so he cannot fill the compulsory HQ), Psyker ML2. He knows Mystic Winds of Fenris and Living Lightning (24", S5, AP4, Assault D6). He may take a Command Squad retinue and a Wolf Retinue.

## Leman Russ

25. **Weapon choice** (L1775): "Mjalnar, the Sword of Balenight, the Axe of Helwinter or Krakenmaw" was read as **three** choices, all free (Mjalnar = the Sword of Balenight, L1846). Default: Mjalnar.

26. Freki and Geri are fixed models in his unit. Russ is Loyalist only (error), with the normal Primarch checks (2,000 pts, one Primarch, Lord of War). His Primarch Retinue is an Honour Guard or Terminator Command Squad. The transport rule "Freki and Geri count as two models" is text only.

## Rites of War

27. **The Pale Hunters** (L327-358). *Built:* 0-1 Heavy Support (per Detachment), plus errors for Artillery Tank Squadrons, Rapier Batteries, Drop Pods, Dreadnought Drop Pods and Dreadclaws in the Detachment. L351 says "the army".
   *Question:* Does it apply to the whole army (allies too) or only to this Detachment (as built)?

28. **The Bloodied Claws** (L362-405). *Built:* Grey Slayer Packs can fill the compulsory Troops. There is an error if the Detachment has no Grey Slayer Pack. There are errors for Rapier Batteries (Artillery), Drop Pods and Dreadnought Drop Pods (treated as Immobile), and Fortifications.
   *Questions:* Are Drop Pods meant to count as "Immobile units"? Which units count as "Slow and Purposeful" (L402)? That restriction and "no Allied Detachment of another Space Marine Legion" (L405) are text only. "At least one compulsory Troops choice must be a Grey Slayer Squad" is checked as "at least one Grey Slayer Pack in the Detachment".

29. **Text only:** every in-game effect of both Rites (reserve bonus, Hit & Run, extra attacks, combat resolution, Howl of the Death Wolf, compulsory charges and Pursue), and all character and unit play rules.
