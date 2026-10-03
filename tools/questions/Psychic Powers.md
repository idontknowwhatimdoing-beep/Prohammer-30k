# Psychic Powers: questions for the author

Author's decision: "Spells should be pickable with effects and such also included - makes it easier for tracking."

Sources: core rules `/home/claude/src/core.txt` (C), Legiones Astartes list `/home/claude/src/legiones_v5.txt` (LA),
Legion texts `/home/claude/src/legions_v3/<Legion>.txt`. Data: `tools/data/psychic_powers.py`; helper:
`legiones.psychic_powers()`.

**What was built:** every psyker has a "Psychic Powers" group. Each power is an entry with its full rule text, a link
to its power type rule (Blessing, Malediction, Conjuration, Witchfire, Beam, Focused, Nova, Maelstrom) and, for
shooting powers with a profile, a weapon profile. The number of powers is the psyker's Mastery Level (Epistolary /
Master of Runes / Mastery Level 2 upgrades add one). Too few powers shows an error ("Choose N psychic powers") -
New Recruit does not pick for the player; more than allowed is blocked. Powers a psyker always knows are included
automatically. Where a psyker first picks a Discipline (Thousand Sons, Burning Lore, Stormseer Epistolary, Master of
Runes, Yesugei) only that Discipline's powers are shown.

1. **"Molton Beam".** C L2395: "MOLTON BEAM". *Built:* named "Molten Beam (Pyromancy)". *Question:* OK to fix the
   spelling?

2. **"Normal Psychic Power list" for named psykers.** XIII_Ultramarines L1073: "Titus Prayto selects two psychic
   powers from the normal Psychic Power list"; V_White_Scars L934: Yesugei "may select one psychic power from the
   normal Psychic Powers list". *Built:* Prayto chooses from the Librarian list (Biomancy, Divination, Pyromancy,
   Telekinesis, Telepathy - LA L302 "except any form of Demonology"); Yesugei keeps the four Disciplines the module
   already used (no Telekinesis, like the Stormseer Epistolary list in V_White_Scars L251-256). *Question:* Is
   the "normal list" the Librarian list (incl. Telekinesis) for both, or should Yesugei follow the Stormseer list?

3. **Discipline step for single extra powers.** Stormseer Epistolary, Master of Runes, Yesugei and Burning Lore
   (incl. Erebus / Kor Phaeron) already had a "Discipline" choice; it was kept, and the power list only shows that
   Discipline's powers. *Question:* These psykers pick only one power - should the separate Discipline choice be
   dropped (pick the power directly from the allowed Disciplines)?

4. **Possession (Daemonology Malefic) for Mastery Level 1.** C L2463: "MAY ONLY BE USED BY A PSYKER WITH MASTERY
   LEVEL 2 OR GREATER". *Built:* selectable by every psyker allowed Malefic Daemonology (Esoterist is Mastery Level 1;
   Zardu Layak is Mastery Level 2); the restriction is in the power text only. *Question:* Hide Possession for
   Mastery Level 1 psykers (Esoterist)?

5. **Conjurations for Legiones Astartes.** C L2318: "Can only summon daemons that match the psykers chaos mark."
   LA L325: "An Esoterist may select Malefic Daemonology powers regardless of his Legion or Allegiance." Legion
   psykers have no Chaos mark. *Built:* Summoning / Possession / Sacrifice / Incursion are selectable with their text;
   summoned units are not added to the roster. *Question:* Which daemons may a Legion psyker (Esoterist, Zardu Layak)
   summon, and should summoned units be bought/recorded in the roster?

6. **Thousand Sons Esoterist / Primus Nullificator.** XV L7-8: "All Thousand Sons Independent Characters are
   Psykers ... Mastery Level 1"; XV L10: Psykers "permitted to select a Psychic Discipline" choose one of five.
   *Built (as before):* a Thousand Sons Centurion picks a Discipline + 1 power (2 as Epistolary); with the Esoterist
   or Primus Nullificator Consul he only selects that Consul's power (Daemonology) - the Thousand Sons Discipline
   and its power are removed. The base Librarian Consul's own list is replaced by the Thousand Sons one (XV L18 "A
   Thousand Sons Librarian Consul follows these rules normally"). *Question:* Correct, or does a Thousand Sons
   Esoterist / Nullificator know a Daemonology power in addition to a Sorcerers of Prospero power?

7. **Other Thousand Sons Independent Characters.** XV L7: "All Thousand Sons Independent Characters are Psykers."
   *Built:* Praetor, Centurion and the named characters have powers; the Legion Techmarine (an Independent
   Character in the army list) does not. *Question:* Should a Thousand Sons Techmarine also be a Psyker (Mastery
   Level 1, one Discipline, one power)?

8. **Second power of the Osiron and the Sekhmet Cabal.** XV L926: Osiron "If upgraded to Mastery Level 2, it selects a
   second power from the same list"; XV L360: Sekhmet Cabal "knows one additional psychic power from the disciplines
   above". *Built:* both keep their one Psychic Discipline choice (XV L16: "a Psyker may select powers from only one
   Psychic Discipline"), so the second power comes from the same Discipline. *Question:* May the second power come
   from a different Discipline?

9. **Magnus' two Disciplines.** XV L1852-1856: five powers in total, "must select powers from at least two different
   psychic disciplines. He may not select all five powers from a single discipline. Infernal Phoenix and Strands of
   Fate are always known ... and count towards his five". The two fixed powers belong to no Discipline. *Built:*
   Infernal Phoenix and Strands of Fate are always included, Magnus chooses 3 more, and an error is shown if all 3
   come from one Discipline. Magnus, Shard of the Crimson King: both fixed + 6 chosen from any combination (XV
   L2073-2083, no Discipline restriction). *Question:* Is "the 3 chosen powers may not all be from one Discipline" the
   intended reading?

10. **Strands of Fate wording.** XV L1894-1904 (Magnus) and L2101-2110 (Shard) differ slightly ("may not attempt that
    type of action again during that phase" vs "that action is lost for that phase"). *Built:* one power entry with
    the Magnus (mortal) text for both forms. *Question:* OK, or should the Shard use its own text?

11. **Mortarion, Prince of Decay.** XIV L1466-1490: "Mortarion is a Mastery Level 2 Psyker ... knows the following
    powers:" Miasma of Pestilence, Curse of Decay, Nurgle's Rot (three powers). *Built:* all three always known, no
    choice. *Question:* Correct (three known, Mastery Level 2 only limits invoking to two per turn)?

12. **Ahriman's Divination powers.** XV L1128: "Ahriman knows every psychic power in the ProHammer Divination
    discipline." *Built:* all seven Divination powers always included. Ahriman's Cabal (XV L1144) selects two
    Divination powers inside the Cabal upgrade. No question - listed for checking.

13. **Powers without a profile.** C: Psychic Shriek (L~2493), Crush, Haemorrhage, Spontaneous Combustion and Purge Soul
    give no weapon profile (Crush rolls its Strength/AP; the others wound or hit through their text). *Built:* rule
    text only, no profile line. Witchfire powers with a printed profile (Smite, Life Leech, Flame Breath, Molten
    Beam, Sunburst, Inferno, Cleansing Flame, Vortex of Doom, Dark Flame, Infernal Gaze, Assail, Shockwave, Psychic
    Maelstrom, Unseen Bolt, Living Lightning, Infernal Phoenix, Fury of the Salamander) show a weapon profile.
    *Question:* Should Crush get a profile line (18", S 2D6, AP D6)?

**Shown as text only (not enforced by the builder):** Mastery Level limits on invoking (one / two powers per turn),
Warp Limit, Disturbance in the Warp, one Witchfire per turn, Deny the Witch, Perils of the Warp, per-character
Leadership for Psychic Tests (Sevatar Ld 7, Typhon Ld 7, Curze Ld 8, Jurr Ld 7, Mortarion Ld 8, Osiron / Sekhmet
Ld 9-10), Magnus' Psychic Supremacy / Lord of the Ether limits, the Sekhmet Cabal losing its second power when the
Inceptor dies, and the Salamanders' Fury of the Salamander only for Librarians in a Detachment with The Awakening
Fire (the option is only offered while that Rite of War is chosen).
