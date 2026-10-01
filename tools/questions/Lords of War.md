# Lords of War - questions for the author

Source: `/home/claude/src/Lords_of_War.txt` (line numbers below).
Module: `tools/armies/lords_of_war.py`.

## Unclear / missing points

1. **Which army may take which unit (L587, L1749, L1960).** The book only groups the entries under "Legiones Astartes", "Talons of the Emperor" and "Exercitus et Mechanicus". Built: every unit carries an "Available to: ..." rule; "Exercitus et Mechanicus" is described as Solar Auxilia, Exercitus Imperialis and Mechanicum. New Recruit cannot check across catalogues which army takes a Lords of War unit. Question: exactly which armies form "Exercitus et Mechanicus"? Is the Ordinatus Mechanicum-only? May The Lost and the Damned, Questoris Households or Daemons take any of these?

2. **How the units are added to an army.** This is its own catalogue. Built: a "Lords of War Detachment" force (exactly one Lords of War choice, no compulsory HQ/Troops) that is added to the roster next to the main army. The one-Lords-of-War-per-army limit of the main Force Organisation chart is therefore not checked against this extra Detachment. Question: OK, or should the Lords of War entries be copied into each army catalogue (needs a shared change)?

3. **Allegiance.** No allegiance restriction is stated anywhere in the book, so none is enforced. Question: are the Talons of the Emperor craft (Orion, Ares) Loyalist only, or any Lords of War Traitor/Loyalist restricted?

4. **Orion Assault Dropship and Ares Gunship have no Structure Points (L1790-1793, L1900-1903).** The table has no SP column. Built: profile says "Structure Points not listed" (L54: "Structure Points are determined normally according to the ProHammer Core Rules"). Question: how many Structure Points do they have?

5. **Ares Gunship type "Transport" (L1919)** but no Transport Capacity or Access Points. Built: no transport profile. Question: is the Ares a transport?

6. **Two Stormhammer entries (L2645-2715 and L2752-2823).** They differ: unit type "Vehicle (Super-heavy)" vs "Vehicle (Tank, Super-heavy)"; "Any Multi-laser" vs "Any Sponson-mounted Multi-laser" may be replaced; "Pintle-mounted Multi-laser or Heavy Flamer" vs two separate pintle options. Built: one unit from the second entry (Tank; only the six sponson Multi-lasers may be swapped; one pintle weapon, Multi-laser or Heavy Flamer +10). Question: which is correct; may the Co-axial Multi-laser be replaced; may it take both pintle weapons?

7. **Duplicate rows in the weapons table (L394-399).** Stormhammer Cannon and Dual Battlecannon are printed twice (identical). Built once.

8. **Weapon profiles not in this book.** Built with the Legiones Astartes / Solar Auxilia profiles: Heavy Bolter, Twin-linked Heavy Bolter, Quad Heavy Bolter, Heavy Flamer, Twin-linked Heavy Flamer, Twin-linked Bolter, Multi-Melta, Havoc Launcher, Hunter-Killer Missile, Lascannon, Twin-linked Lascannon, Autocannon, Twin-linked Autocannon, Multi-laser (and Co-axial Multi-laser), Volkite Culverin (45" S6 AP5 Heavy 4, Rending - note this book defines Deflagrate, which other volkite profiles may use), Demolisher Cannon and "Demolisher Siege Cannon" (Fellblade; built as the Demolisher Cannon 24" S10 AP2 Ordnance 1, Large Blast). Question: confirm these profiles, especially the Fellblade's Demolisher Siege Cannon and the Volkite Culverin.

9. **Combi-weapon** (pintle option, several entries): the secondary weapon is not specified. Built: Bolter profile + rule text "secondary weapon fired once per battle". Question: which combi-weapons are allowed?

10. **Laser Destroyer (L381)** is 36" S9 AP1 Ordnance 1, Twin-linked here, while the Legiones Astartes list has a Laser Destroyer 48" S10 AP1 Heavy 1, Twin-linked. Built as printed in this book. Question: intended?

11. **Hellstrike Missile (L397)** is 72" S8 AP2 Heavy 1, Sunder, One Use here (Solar Auxilia: AP3 Ordnance 1). Built as printed here.

12. **Cerberus "Twin-linked Neutron Laser Battery" (L654)** - the Neutron Laser Battery profile is already Twin-linked. Built as the one weapon "Neutron Laser Battery". "Ordnance D3" kept as printed.

13. **Side sponsons (Baneblade family, Legion Stormblade).** "Up to two pairs of side sponsons, each containing one Lascannon and one Twin-linked Heavy Bolter, +50 per pair" - built as: each pair = two sponsons = 2 Lascannons + 2 Twin-linked Heavy Bolters, 0-2 pairs at +50. Where Twin-linked Heavy Bolters may become Twin-linked Heavy Flamers (Legion Stormblade, Stormlord) a pair can be taken as HB/HB, HB/HF or HF/HF. Question: is a pair one Lascannon + one TL Heavy Bolter in total, or per sponson (as built)?

14. **Targeters (Shadowsword, Stormblade - L2388, L2594)** "Two sponson Lascannons may be fitted with Targeters, free" - built as a free option (error if no sponsons are taken). The +1 BS is text only. Question: two Lascannons in total or per pair?

15. **Space Marine Legion Crew / Stormhammer Targeters (BS4)** change the profile BS to 4 (enforced). Space Marine Legion Crew on Falchion/Legion Stormblade/Fellblade only.

16. **Neutron Wave Capacitor (Falchion, L919-929)** - built as an upgrade with the rule text and links to Shock Pulse and Feedback.

17. **Sokar Stormbird Macro-bomb Cluster Payload (L1725)** "replace all six Dreadstrike Missiles with Macro-bomb Cluster Payload" - built as one Macro-bomb Cluster (Bomb 1, One Use). Question: one bomb or several?

18. **"Anabaric Claw" (L2029, L2082)** spelled "Anbaric Claw" in the armoury (L326). Built as Anbaric Claw.

19. **Super-heavy Command Tank cost** is +20 on the Mastodon and +25 elsewhere - built as printed. The rule affects "Friendly Infantry units" (all armies) - text only.

20. **Stormlord "All Power to Weapons!" (L2308)** is printed in a box but not in the Special Rules list (the Stormlord has no Special Rules section). Built as a special rule of the Stormlord.

21. **Searchlight, Smoke Launchers, Extra Armour, Power of the Machine Spirit** are not described in this book - linked to the ProHammer core rules.

22. **Thunderhawk Gunship "Six Hellstrike Missiles" → "Six Thunderhawk Cluster Bombs" (+60)** - each Cluster Bomb is Bomb 6, One Use; built as six weapons. Question: six bombs each of Bomb 6, or one Bomb 6 payload?

23. **Orion "may transport a single Custodes Contemptor-Achillus or Contemptor-Galatus Dreadnought" (L1849)** - text in the transport profile; not checked.

## Rules shown as text only (not enforced)

- All Super-heavy Vehicle rules (Structure Points, Massive Firepower, Lumbering War Engine, Super-heavy Tank Shock, Crushing Advance, Immense Machine, Catastrophic Destruction) - the Structure Points are shown in the profile's Unit Type.
- Super-heavy Command Tank, Ordinatus Reactor Meltdown, Reinforced Ordinatus Chassis, Bomb / Bomb X, all weapon special rules (Massive/Apocalyptic Blast, Apocalyptic Barrage, Titan Killer, Machine Destroyer, Divert Power, Stone Burner, Exoshock, Heavy Beam, Deflagrate, Heliothermic Detonation, Sunder, Indirect Only, Shock Pulse, Feedback, Ulator Sonic Wave).
- All armoury items (Armoured Ceramite, Flare Shield, Void Shield, Chaff Launcher, Armoured Cockpit, Illum Flares, Ramjet Diffraction Grid, Eclipse Shield, Macro Arae-shrike, Blessed Autosimulacra, Anbaric Claw, Ordinatus Dispersion Shield, Auxiliary Drive, Dual Void Shield Generator, Command Vox Relay).
- Unit rules: Reactor Blast, Crushing Weight, Enhanced Defensive Fire, Reinforced Shell, Loading/Unloading Vehicles, Shield Projection, Reinforced Structure, Grav-backwash, Exposed Arachnus Capacitors, All Power to Weapons!.
- Void-crafted Hull: Rear Armour 12 is enforced in the profile; Transport capacities and allowed passengers are text in the transport profiles.
- "Available to" (which army may take a unit) - text only, see question 1.
