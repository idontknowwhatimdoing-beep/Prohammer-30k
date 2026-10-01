# Exercitus Imperialis - questions for the author

Catalogue: `Exercitus Imperialis.cat`, module `tools/armies/exercitus_imperialis.py`.
Line numbers refer to `Exercitus_Imperialis.txt`.

## How the catalogue is structured

- **Configuration entries.** There are two: Allegiance, and "Muster of Worlds: Provenances of War". The Provenances entry holds all 19 Provenances. You can pick up to two, and Companions of the Ten Thousand appears once Paragons of Humanity is chosen. The Provenance points are paid on this entry, not added to the Force Commander. The total cost comes out the same.
- **What is enforced on the Provenances entry:**
  - Every incompatible pair is an error.
  - Mechanised Regiments must be chosen alone.
  - Cult Horde and Undying Horde are Traitor only.
  - A Force Commander or a named Lord Commander must be present.
  - Paragons of Humanity needs a Veteran Squad or a Gene-Trooper Squad.
  - Imperial Navy Battalion needs a Naval Officer.
- **Provenance options on units.** Options that come from a Provenance are hidden until that Provenance is chosen in the same Detachment. The Provenance name is shown in brackets in the option title. Examples: Frenzon, Blade and Fury, Discipline Collars, Cameleoline, Mining Equipment, Grav-chutes, Void-Hardened Armour, Advanced Weapons, Heavy Panoplies, Exemplar Guard, Mounted Command, Airborne Command, Blighted Ogryns, Hive Fighters, Razorwire and Industrial Carapace.
- **"Selected as Troops" toggles.** A toggle appears on Combat Engineers (Clanholds, or Engineer Corps with a limit of 2), Ogryn Brutes (Workdivision, limit 3), Cavalry (Horse Lords) and Jump Assault Squads (Drop Assault). Switching it on moves the unit to Troops and lets it fill a compulsory Troops choice.
- **Who can fill compulsory Troops:**
  - Reconnaissance Squads can with Frontier Marksmen.
  - With Survivors of the Dark Age, only Grenadier Squads can.
  - Inducted Levy Squads cannot with Warrior Elite, Survivors of the Dark Age or Paragons of Humanity.
- **Attached Advisors are shared entries.** They are linked from the units they may join, and only one Advisor is allowed per unit.
  - Force Commander and named Lords: Navigator, Master of the Fleet, Memorator, Company Cook, Personal Aide, Scribe Historicus, Lotara Sarrin, Ilya Ravallion.
  - Platoon Command Cadre: the same list without the Personal Aide and Scribe Historicus, plus the Discipline Master.
  - Troops units: Psyker Attaché (Cult Leader or Prophet, 0-4 in total), Jester, Locus Scribii, Cartographica Adept (0-2), Discipline Master.
  - Other Infantry: Discipline Master only (0-5 in total; this stands in for the "Cadre").
  - The Field Officers Bronzi and Soneka are linked from the Veteran, Gene-Trooper and Reconnaissance Squads they may join.
- **Remembrancer Circle.** It can also fight as its own unit, so it is a root entry. It goes in the HQ slot with the "Force Org: +1 HQ" category, so it never uses up an HQ choice.
- **Infantry Platoon.** This is one Troops entry: 1 Platoon Command Cadre plus 2-5 Infantry Squads, each squad equipped separately. It can take a Gorgon.
- **Tank Commander upgrades.** The Militia Tank Commander, Tyana Kourion and Aika 73 are upgrades on eligible tanks. The Tank Commander is limited to 0-1 per army and the other two are Unique.

## Questions

1. **The Armoury sections and their costs are missing.**
   - What the book says: units refer to the "Senior Officer" (l.530), "Junior Officer" (l.1468), "Advisor" (l.1562, 1655), "Militia Sergeant" (l.2680 etc.), "Ogryn Bone 'ead" (l.2395), "Enginseer" (l.2514), "Terminator Weapons" (l.904), "Sentinel" (l.4221), "Land Speeder" (l.4279) and general vehicle upgrade sections of the Armoury. But the Armoury summary (l.6699-6816) only lists items, with "As entry" as the cost.
   - What I built: my own lists for each section, with proposed costs, all in `ARMOURY` / `VEHICLE_UPGRADES` / `TERMINATOR_WEAPONS` in the module. Some examples:
     - Senior Officer: Power Weapon 10, Power Fist 15, Plasma Pistol 10, Iron Halo 15.
     - Militia Sergeant: Bolt Pistol 2, Hellpistol 2, Hand Flamer 5, Plasma Pistol 10, Boltgun 2, Power Weapon 10, Power Fist 15, Melta Bombs 5, Refractor Field 10.
     - Vehicles: Hunter-Killer 10, Dozer Blade 5, Extra Armour 10, Smoke Launchers 5, Improved Comms 15.
   - Question: please provide the real section lists and costs. Is there a points cap per section?
2. **Plasma Pistol has no profile.** It is an option on the Jump Assault Squad (l.4595), but the weapon tables have no profile for it. I used 12" S7 AP2 Pistol, Gets Hot. Is that right?
3. **Twin-linked weapon profiles are missing.** The twin-linked heavy stubber, heavy bolter, autocannon, lascannon and multi-laser are used but not listed. I used the base profile plus Twin-linked. The Exterminator uses the "Exterminator Autocannon" profile (Heavy 4, Twin-linked). Is that right?
4. **Boarding Shield rules are missing.** The book says its rules are "presented in the Exercitus Imperialis Armoury" (l.1296), but they are not there. It is currently shown as text, as +1 Armour Save in close combat. What are the rules?
5. **The Rogue Psyker powers list is missing** (l.1948). I built a counter, "Rogue Psyker psychic power", costing 20 points each, minimum 1 and maximum 3. What are the powers, and what is the maximum?
6. **Terminator Armour and Tainted Weapon costs for the Force Commander.**
   - Clanholds of the Deep Worlds lets the Force Commander "purchase Terminator Armour from the Armoury" (l.906), but no cost is given. I used 25.
   - Tainted Flesh's Tainted Weapon (l.755) has no cost either. I used the Cult Demagogue's +5.
7. **Platoon Command Cadre Bodyguard weapon costs** (l.1472-1484). The swaps are "All Militia Bodyguards may replace ... Laslocks +10, Boltguns +20, Heavy stubbers +35, Grenade launchers +70". I built these as flat costs for the whole squad. Are they per squad or per model?
8. **Infantry Squad: in a Platoon only, or also on its own?** The squad (l.3030) has no size options (it is a fixed 20 models for 80 points). The Infantry Platoon text (l.3018-3026) suggests squads come in Platoons, but the squad also has its own entry. I built both: the Platoon (one Troops choice) and a stand-alone Infantry Squad (Troops). Is the stand-alone squad allowed?
9. **Can a Platoon Command Cadre bought as an HQ fill the compulsory HQ?** The book only says a Force Commander can (l.286). I let the Platoon Command Cadre fill it too. Is that right?
10. **Do named Lords Commander count against the "0-1 Force Commander"?** Varvarus, Namatjira, Niborran, Fayle and Egwu "count as a Force Commander for all rules and army construction purposes". I treat them as counting against the 0-1 limit, so only one Force Commander or Lord per Detachment. They also get the Force Commander's Provenance options and Advisors, but not his Armoury, because their entries list no options. Is that right?
11. **Rapier Battery cost.** The battery costs 40 points for one team, but extra teams cost +50 each (l.4845, 4900). I built it as written (40/90/140). Is that right? The Rapier Carrier also has no profile in the book, so I used Artillery T7 W2 Sv3+.
12. **Sentinel Strength is missing** from its profile (l.4164). I used S5.
13. **Ogryn Bone 'ead.** The squad upgrade is +10 (l.2391), and it is free with Ogryn Workdivision. The Bone 'ead replaces one of the Brutes. Is that right?
14. **The Stormhammer is missing.** Tyana Kourion mentions a Stormhammer Super-heavy Assault Tank and a Super-heavy Command Tank upgrade (l.5922), but neither is in the book. Kourion is only offered on the Leman Russ and the Malcador. Kourion has no Allegiance listed, so she is allowed for both sides.
15. **Ilya Ravallion** (l.6198) is an Attached Advisor with no host listed. I linked her from the Force Commander and Platoon Command Cadre. Where should she be able to join?
16. **One Attached Advisor per unit** (l.6424). This is enforced, so the Force Commander can take only one of Aide, Scribe, Navigator and so on. Is that intended?
17. **The Discipline Master Cadre** (0-1, 1-5 models) is built as up to 5 Discipline Masters, each picked inside the unit it joins. That way the "one per unit" assignment is enforced.
18. **Mechanised Regiments.** Fire Support Squads, Reconnaissance Squads and Clone Cohorts normally have no transport. Under Mechanised they get a required Chimera. Is that right?
19. **Engineer Corps.** "Only one Combat Engineer Squad selected as Troops may fulfil a compulsory Troops choice" (l.1227). This is not enforced: both toggled squads count as compulsory. It is text only.
20. **Survivors and Hive Platoons.** Advanced Weapons must be bought by every squad of a type if one buys it (l.675). This is not enforced. Street-born (no Advanced Weapons) is enforced only for Grenadiers.
21. **Malcador and Gorgon weapon swaps.** The replacements are shown as extra choices, and the standard autocannons stay listed in the profile. Treat a chosen replacement as replacing them.
22. **Medicae Detachment.** Each Orderly is assigned to a unit. This is only shown as text, because the Detachment is an Elites unit.
23. **Cyber-Augmetics on Mutant Spawn.** Mutant Spawn has no Provenance rule, so it gets no Provenance options.

## Rules shown as text only (not enforced)

- Provenance characteristic changes: WS, S, T, I, Ld and saves.
- Feral Warriors: no more Vehicle units than Infantry units.
- Undying Horde: each Vehicle unit only once, and at most 3 Vehicle units.
- Mechanised Regiments: units must begin the battle embarked, and characters must have room in a transport.
- Grav-chute units may not begin the battle embarked.
- Who an Advisor or Field Officer is assigned to, beyond which units offer them.
- Warlord requirements.
- Lords of War and Fortifications: none are in the book.
- Iron Halo is limited to one per army (this one is enforced by the shared wargear).
- All in-game special rules.
