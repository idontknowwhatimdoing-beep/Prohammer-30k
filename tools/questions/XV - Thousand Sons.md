# XV - Thousand Sons: questions for the author

Source: `/home/claude/src/legions/XV_Thousand_Sons.txt` (line numbers refer to that file).
Module: `tools/legions/xv_thousand_sons.py`.

Decisions already made by the author and kept: Praetors and Centurions must choose a Prosperine Cult; Techmarines
are not Psykers; the Sekhmet 0-1 is lifted under The Guard of the Crimson King; Cult / Discipline are picked by the
player (a missing choice shows an error, nothing is auto-picked).

## Legion rules

1. **Sorcerers of Prospero - Psyker Consuls.** L7-9: "All Thousand Sons Independent Characters are Psykers ... A Thousand
   Sons Praetor instead counts as Psyker (Mastery Level 2)." L18: "A Thousand Sons Librarian Consul follows these rules
   normally."
   *Built:* Praetor (ML2) and Centurion (ML1) get a required Psychic Discipline choice (Biomancy, Divination, Pyromancy,
   Telekinesis, Telepathy). Centurions with the Esoterist or Primus Nullificator Consul do not get the choice (they keep
   their own Consul powers); a Librarian Consul does get it.
   *Question:* Is that right for Esoterist / Primus Nullificator? Does a Librarian use the Thousand Sons disciplines
   instead of the normal Librarian powers?
2. **Which units may choose a Prosperine Cult?** L24: "Any Thousand Sons Infantry, Jump Infantry, Bike, Jetbike unit or
   Independent Character that is permitted by its unit entry to select a Prosperine Cult..."; L30: units not permitted do
   not gain one.
   *Built:* Cults only on Praetor / Centurion, on squads that buy Brotherhood of Psykers, on the unique Cabals and on
   Magnus' Brotherhood retinue. Ordinary Tactical, Assault, Veteran (without Brotherhood) etc. have no Cult.
   *Question:* Is any normal Legion unit meant to pick a Cult without being a Brotherhood?
3. **Price of Knowledge** (L112-121): +1 HQ, +1 Elites, -1 Fast Attack is built on the Detachment. Marking which units
   use the extra slots and the +50 VP are text only.
4. **Text only (not enforced):** one power per turn / one discipline (L16, L19), Cult Arcana / Mastery effects and "Cult
   is kept when joining" (L31-39), Brotherhood + IC separation (L107), Signs and Portents (L126-129).

## Armoury

5. **Do the Legion items count towards the Armoury caps?** L149-182 (Arcane Litanies 10, Asphyx Shells 10, Teleportation
   Transponders 10, Prosperine Aether-Disc 30).
   *Built:* a separate "Thousand Sons Wargear" group on Praetor / Centurion, outside the 100-pt Space Marine Armoury.
   *Question:* Should they count towards the 100-pt cap?
6. **Prosperine Force Weapon - where.** L143: "Any Thousand Sons model permitted to select a Power Weapon may upgrade
   that Power Weapon ... for +10 points."
   *Built:* wherever a Power Weapon is offered in a weapon list (characters, sergeants, Command / Honour Guard
   specialists, Veterans ...), a Prosperine Force Weapon is offered for Power Weapon cost +10. Activation rules (L145-146)
   are text. *Question:* also for non-Psyker squad models (e.g. Veterans without Brotherhood)? They can never activate it.
7. **Aether-fire Cannon** (L155-156): offered free wherever a Plasma Cannon can be chosen. "All or none in a unit" is not
   enforced. Profile as printed (L162-166).
8. **Asphyx Shells** L172: "may not be combined with Special Issue Ammunition" - not enforced (Seekers / Vigilators do
   not get Asphyx anyway). Built for Praetor / Centurion (+10), Veteran and Terminator Squads (+20).
9. **Teleportation Transponders - which units.** L176: "Any Thousand Sons unit composed entirely of models wearing any
   form of Terminator Armour may purchase ... +15 points per unit."
   *Built:* Legion Terminator Squad, Legion Terminator Command Squad, Sekhmet Terminator Cabal (+15); Praetor / Centurion
   only while in Terminator Armour (+10). *Question:* any other all-Terminator unit (e.g. a Command Squad bought in
   Terminator Armour, or Magnus' Terminator Command Squad retinue - not built)?
10. **Prosperine Aether-Disc** L182, L189: hidden while the character has Terminator Armour, a Jump Pack or a Bike (the
    Sky Hunter Jetbike upgrade needs a Bike). Aetheric Evasion is text.

## Rites of War

11. **The Axis of Dissolution - limitations.** L214: "Every Troops choice ... at its maximum permitted unit size." L215:
    no more Tank/Flyer Vehicles than Infantry units.
    *Built:* only the "no Fortification" error (L216). Max unit size and the Tank/Flyer count are text only (New Recruit
    has no unit-type categories to count). Effects (L198-210) are text.
12. **The Guard of the Crimson King - Troops.** L245: "Sekhmet Terminator Cabals may be selected as Troops choices and must
    fulfil the Detachment's compulsory Troops selections."
    *Built:* Sekhmet become Troops and the only compulsory-Troops-eligible unit (Tactical / Assault / Breacher Squads lose
    compulsory eligibility but may still be taken); Sekhmet 0-1 lifted (max 6 per Detachment).
    *Question:* May other Troops be taken in addition, once the compulsory Troops are Sekhmet?
13. **Guard - Transponders for characters.** L239-240: units "entirely in Terminator Armour gain Teleportation
    Transponders at no additional points cost"; "Independent Characters may purchase ... for +10 regardless of armour".
    *Built:* squads in Terminator Armour (and Sekhmet) get them for 0 pts; Praetor / Centurion pay +10 in any armour.
    *Question:* Is a character in Terminator Armour free (he is a unit "entirely in Terminator Armour") or +10?
14. **Guard - limitations.** L253-256. *Built:* the ML3 upgrade (+25, L254) is offered on every Praetor while the rite is
    chosen (the builder can't see who is Warlord); "no Fortification" is an error. Warlord restriction, vehicles vs
    Thousand Sons units and "no Allied Detachment" are text only. Astral Warfare / Wreathed in Lightning effects are text.
15. **The Fellowships of Prospero - Tactical Brotherhood discipline.** L267: a 20-model Tactical Squad "selects one psychic
    power from the normal Psychic Disciplines available to Thousand Sons Psykers" (not its Cult's discipline as in L98).
    *Built:* Cult + free Discipline choice for the Tactical Brotherhood (only visible with the rite and 20 models);
    Veteran / Terminator Brotherhoods use their Cult's discipline and cost 15 under the rite.
    *Question:* intended difference?
16. **Fellowships - counting Brotherhoods.** L287: "at least two Psychic Brotherhoods." *Built:* an error counting
    Brotherhood Veteran / Terminator / Tactical Squads, Sekhmet, Khenetai, Ammitara (also as Amon's / Sanakht's
    retinue), Ahriman's Cabal and Magnus' Brotherhood retinue. *Question:* Do retinue Brotherhoods count?
    0-1 Fast Attack is built. Warlord must be a Psyker (L286), Order of the Cults (L282), Magister Templi and "no Allied
    Detachment" are text only.

## Unique units

17. **Sekhmet weapons.** L408: "Any model may replace its Foeblaster Boltgun with a Combi-weapon at the normal Space
    Marine Armoury cost." L411: "For every five models ... up to two Sekhmet may replace their Foeblaster Boltgun".
    *Built:* Combi-Flamer 10, Combi-Grenade Launcher 10, Combi-Volkite Charger 10, Combi-Meltagun 15, Combi-Plasma Gun 15
    (Armoury prices); squad-level blocks for the Terminators, own slots for the Inceptor; heavy weapons as a squad pool of
    2 per 5 models. *Question:* prices OK?
18. **Sekhmet transport.** L430: "a Land Raider, Dreadclaw Drop Pod or Spartan Assault Tank". *Built:* Land Raider Phobos,
    Land Raider Proteus, Dreadclaw, Spartan. *Question:* any other Land Raider pattern?
19. **Khenetai Blademaster Armoury.** L552: "up to 50 points of permitted weapons and wargear ... may not replace his
    Paired Prosperine Force Blades." *Built:* 50-pt Armoury of wargear only (nothing to replace). *Question:* may he add
    extra weapons (e.g. a pistol) on top of his blades?
20. **Ammitara.** L680: "Any model may replace his Sniper Rifle" - built as one squad-level block for Intercessors and the
    Fate (Meltagun / Plasma Gun swaps reduce it). L702: the Fate's 50-pt Armoury can replace his Bolt Pistol and Combat
    Blade. Discipline limited to Divination / Telepathy (L642-644).
21. **Castellax-Achea.** L773 "Two Dreadnought Close Combat Weapons" - shown as 2x DCCW. Aetheric Command Matrix and
    Psychic Conduit are text.
22. **Contemptor-Osiron.** L928: "Automatic Shielding may not prevent this hit" - read as Atomantic Shielding. The Osiron
    Force Blade profile is not printed; built as Dreadnought Close Combat Weapon + Force. *Question:* profile OK?
23. **Numerologist Cabal.** L1038: "For every five models in the Cabal, one Life Ward may replace his Bolt pistol" - the
    Numerologist counts towards the five. *Question:* correct?

## Named characters

24. **Psyker levels / fixed Cults** are shown as rules (Ahriman ML3, Phosis / Amon / Hathor ML2, Sanakht ML1 with only
    Mindsong of Blades). Ahriman and Amon have the 1,500-point check (L1117, L1330); Sanakht is not Master of the Legion.
    Krak grenades +2 on each.
25. **Ahriman's Cabal** L1138-1148: the Command Squad retinue may buy Ahriman's Cabal (+50); while it does, each Prosperine
    Force Weapon in the squad costs Power Weapon +5 instead of +10. The two Divination powers are text.
26. **Black Staff of Ahriman / Blade of Ahn-Nunurta / Aetheric Blade** have no printed profiles. *Built:* User strength
    (Aetheric Blade S7), AP -, Power Weapon, Force, Master-crafted (+Two-Handed for the Blade). *Question:* AP values?

## Magnus

27. **Deny the Witch range.** L1879 (The Crimson King): "within 24\" of Magnus"; L1886 (The Warp Bends to Magnus): "Magnus
    may also attempt to deny the witch at 18” around him." *Built:* both texts as written. *Question:* which range?
28. **Magnus' save.** L1808 prints "1+"; built as "1+/4+" because Horned Raiment counts as Primarch Armour (L1839).
29. **Magnus powers / Cults** (L1854-1860, Psychic Supremacy L1863-1867): text only (5 powers from at least two
    disciplines; counts as every Cult for army selection, e.g. Order of the Cults).
30. **Magnus' retinue.** L1918-1927: Honour Guard, Terminator Command Squad or Sekhmet; Honour Guard / Terminator Command
    Squad may buy Brotherhood of Psykers (+25) with Cult and any discipline. The Bidding of the Crimson King (L249): mortal
    Magnus becomes HQ and fulfils the compulsory HQ.
31. **Magnus, Shard - Primarch status.** L2010-2023 do not list "Primarch" (no Supreme Commander, Fielding a Primarch,
    Clash of Demigods, retinue). *Built:* Lord of War, Master of the Legion, Primarch category, Daemon Primarchs rule, 2,000-pt
    check (1,500 with Primarch's Chosen), never together with mortal Magnus (L2027);
    no retinue (Incorporeal Will). Not usable as HQ under The Guard of the Crimson King.
    *Question:* Should the Shard follow the Fielding a Primarch rules (2,000 pts, must be Warlord)? Is it Traitor-only
    (no Allegiance restriction is built for either form)?
