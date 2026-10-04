# Exercitus Imperialis - questions for the author

Catalogue: `Exercitus Imperialis.cat`, module `tools/armies/exercitus_imperialis.py`.
Line numbers refer to the current book text `v4/Exercitus_Imperialis.txt`.

## How the catalogue is structured

- **Configuration entries.** There are two: Allegiance, and "Muster of Worlds: Provenances of War". The Provenances entry holds all 19 Provenances. You can pick up to two, and Companions of the Ten Thousand appears once Paragons of Humanity is chosen. The Provenance points are paid on this entry, not added to the Force Commander. The total cost comes out the same.
- **What is enforced on the Provenances entry:**
  - Every incompatible pair is an error.
  - Mechanised Regiments must be chosen alone.
  - Cult Horde and Undying Horde are Traitor only.
  - A Force Commander or a named Lord Commander must be present.
  - Paragons of Humanity needs a Veteran Squad or a Gene-Trooper Squad.
  - Imperial Navy Battalion needs a Naval Officer.
- **Provenance options on units.** Options that come from a Provenance are hidden until that Provenance is chosen in the same Detachment. The Provenance name is shown in brackets in the option title.
- **The Armoury.** Every character with Armoury access has one group "Exercitus Imperialis Armoury: <section> (max N pts)": a ranged weapon exchange, a close combat weapon exchange and Additional Wargear, with the section's allowance (100 / 50 / 25 / 25 / 25 / 50) as a points limit on the group. Items in the model's starting wargear are not offered again. Individual Provenance purchases sit inside the same group, so they count towards the allowance (Force Commander: Mounted, Jump Pack, Boarding Shield, Blade and Fury; Discipline Master: Jump Pack). Whole-squad upgrades hide the Sergeant's own Melta Bombs / Krak / Frag Grenades. Vehicles have "Vehicle Upgrades (Exercitus Imperialis Armoury)" with the General Vehicle Upgrades items they qualify for (Dozer Blade and pintle weapons on Tanks, Extra Armour not on super-heavies, Armoured Crew Compartment on Open-topped vehicles, no items they already carry); Sentinels and Land Speeders use their own sections.
- **Terminator Weapons.** A Force Commander in Terminator Armour gets the Terminator close combat weapons in his close combat slot. A Veteran or Gene-Trooper Squad in Terminator Armour gets two "any model" blocks (one ranged and one close combat exchange per model); a Pair of Lightning Claws uses up both.
- **Clanhold industrial weapons.** Any model in a unit with Mining Equipment may swap its close combat weapon for a Powered Mining Pick or Lascutter. The Fire Support Team's Mining Laser is in its normal heavy-weapon list, and the Combat Engineers' Mining Laser (one) is in their special-weapon pool.
- **Psykers.** Every psychic power is picked individually with its rules: Cult Leader (1 Telepathy power), Prophet (1 Divination), Rogue Psyker (Telepathy or Malefic Daemonology, +20 each), Necromancer Demagogue (Force Commander with Undying Horde: 1 Biomancy power plus Raise the Dead).
- **"Selected as Troops" toggles.** A toggle appears on Combat Engineers (Clanholds, or Engineer Corps with a limit of 2), Ogryn Brutes (Workdivision, limit 3), Cavalry (Horse Lords) and Jump Assault Squads (Drop Assault). Switching it on moves the unit to Troops and lets it fill a compulsory Troops choice.
- **Who can fill compulsory Troops:**
  - Reconnaissance Squads can with Frontier Marksmen.
  - With Survivors of the Dark Age, only Grenadier Squads can.
  - Inducted Levy Squads cannot with Warrior Elite, Survivors of the Dark Age or Paragons of Humanity.
- **Attached Advisors are shared entries.** They are linked from the units they may join. Any number of Advisors may join one unit; each Advisor's own 0-1 / 0-n limit counts across the Detachment.
  - Force Commander and named Lords: Navigator, Master of the Fleet, Memorator, Company Cook, Personal Aide, Scribe Historicus, Lotara Sarrin, Ilya Ravallion.
  - Platoon Command Cadre: the same list without the Personal Aide and Scribe Historicus.
  - Troops units: Psyker Attaché (Cult Leader or Prophet, 0-4 in total), Jester, Locus Scribii, Cartographica Adept (0-2).
  - The Field Officers Bronzi and Soneka are linked from the Veteran, Gene-Trooper and Reconnaissance Squads they may join.
- **Discipline Master Cadre.** Bought on its own (0-1, 1-5 Discipline Masters, each equipped separately) and assigned before deployment. Like the Remembrancer Circle it sits in the HQ slot with the "Force Org: +1 HQ" category, so it never uses up an HQ choice and cannot fill the compulsory HQ.
- **Infantry Platoon.** The Infantry Squad exists only inside the Platoon: one Troops entry with 1 Platoon Command Cadre plus 2-5 Infantry Squads, each squad equipped separately. It can take a Gorgon.
- **Tank Commander upgrades.** The Militia Tank Commander, Tyana Kourion and Aika 73 are upgrades on eligible tanks. The Tank Commander is limited to 0-1 per army and the other two are Unique. A tank with a Command Tank cannot also buy Improved Comms.

## Questions

1. **Ilya Ravallion** (l.6624-6674) is an Attached Advisor with no host listed. I linked her from the Force Commander and Platoon Command Cadre. Where should she be able to join? (Your earlier reply had no answer text.)
2. **Stormhammer / Super-heavy Command Tank** (l.6271): Tyana Kourion can be put in a Stormhammer, which is not in the book. Deferred until the Lords of War are done, as agreed. Kourion is currently only offered on the Leman Russ and the Malcador, for both sides.
3. **Rogue Psyker powers: maximum and mixing.** "must purchase at least one Rogue Psyker psychic power for +20 points per power" (l.1872); "He selects powers from either Telepathy of Malefic Daemonology" (l.1883). I built: at least 1 and at most 3 powers, +20 each, and powers from both disciplines may be mixed. Is there a maximum (3?), and must all powers come from one of the two disciplines?
4. **Necromancer Demagogue for the named Traitor Lords.** Fayle and Egwu "count as a Force Commander for all rules". I gave them the Undying Horde psyker option (1 Biomancy power and Raise the Dead) as well. Is that right?
5. **Which purchases count towards the Force Commander's allowance?** "Equipment purchased through another Armoury section or an individual Provenance option counts towards the same allowance" (l.7158). Inside his 100-point limit I put the Mounted (+10), Jump Pack (+15), Boarding Shield (+5) and Blade and Fury (+10) options. I left the Naval Officer upgrade (+10) outside, as a rank upgrade. Is that right?
6. **Discipline Masters: one per unit?** You said the Cadre is bought and then assigned freely, and that is how it is built now. The book still says "Only one Discipline Master may be assigned to each unit" (l.1376). Should that sentence stay? It is shown as text only.

## Settled questions kept as notes (built as accepted)

- **Engineer Corps.** "One Combat Engineer Squad selected as Troops may be used to fulfil a compulsory Troops choice" (l.977). This is not enforced: both toggled squads count as compulsory. It is text only.
- **Survivors and Hive Platoons.** Advanced Weapons must be bought by every squad of a type if one buys it (l.624-). This is not enforced. Street-born (no Advanced Weapons) is enforced only for Grenadiers.
- **Malcador and Gorgon weapon swaps.** The replacements are shown as extra choices, and the standard autocannons stay listed in the profile. Treat a chosen replacement as replacing them.
- **Medicae Detachment.** Each Orderly is assigned to a unit (l.2322). This is only shown as text, because the Detachment is an Elites unit.
- **Cyber-Augmetics on Mutant Spawn.** Mutant Spawn has no Provenance rule, so it gets no Provenance options.

## Rules shown as text only (not enforced)

- Provenance characteristic changes: WS, S, T, I, Ld and saves.
- Feral Warriors: no more Vehicle units than Infantry units.
- Undying Horde: each Vehicle unit only once, and at most 3 Vehicle units.
- Mechanised Regiments: units must begin the battle embarked, and characters must have room in a transport.
- Grav-chute units may not begin the battle embarked.
- Who an Advisor, Discipline Master or Field Officer is assigned to, beyond which units offer them.
- Armoury: a Senior Officer may carry no more than two weapons, only one two-handed. A model with a Pair of Lightning Claws may not keep a pistol or basic ranged weapon (for the Force Commander the ranged slot may then be left empty; for squads this is text only). Terminator weapons bought for a squad Sergeant are not counted in his 25-point allowance.
- Warlord requirements.
- Lords of War and Fortifications: none are in the book.
