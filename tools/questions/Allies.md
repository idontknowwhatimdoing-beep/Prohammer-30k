# Allied Detachments and the Allies Matrix: questions for the author

Sources: Games in the Age of Darkness (GAD, Allies Matrix "At the Height of the Heresy" + legend), ProHammer Classic
core rules (C, "Multiple Detachments"), the army lists' Multiple Detachments / Allied Forces sections, Forces of the
Legions (FotL). Code: `tools/allies.py`, matrix copied into `tools/data/allies_matrix.py`, check `tools/check_allies.py`.

**What was built:** a roster has one force "Primary Detachment" (the old Standard chart, same id: old lists keep
working) and any number of "Allied Detachment" forces (same chart, each fulfils its own compulsory selections). Special
charts count as Allied Detachments: Ruinstorm Allied Detachment, Daemons of the Ruinstorm Covenant Detachment (Word
Bearers, new), Agents of the Sigillite. Every army's Allegiance entry carries an "Army: ..." marker and shows an "Allies
Matrix: <army>" rule listing its Allies and Brothers / Conditional Alliance / Sworn Enemies. Errors: Sworn Enemies in
the same roster (any two detachments, also through a third); more than one Primary Detachment; an Allied Detachment
without a Primary; Loyalist and Traitor detachments together; a second detachment of the same army list before the
Primary's 6 Troops slots are filled; a Primarch in an Allied Detachment; Rites of War that forbid Allied Detachments
(15 Legion Rites + Primarch's Chosen) or allies from another Legion; Vigil Opertii Mission needs an Exercitus
Imperialis allied detachment; The Emperor's Talons (Custodes in the Primary - no allies, except Exercitus with
Companions of the Ten Thousand); Blackshields Chymeriae / The Alien Brotherhood - no allies; Covenant only in a Word
Bearers army and then the army's only Allied Detachment. Conditional Alliance effects (no joining, no embarking, no
shared buffs) are shown as rule text only - New Recruit cannot check them.

1. **Asymmetric / blank matrix cells.** GAD matrix: row DA / column SW = "C" but row SW / column DA = "S"; row EC /
   column UM is blank but row UM / column EC = "S"; row NL / column RG is blank but row RG / column NL = "S". *Built:*
   a pair is Sworn Enemies if either cell says S (so DA + SW, EC + UM, NL + RG are all Sworn Enemies). *Question:* is
   Dark Angels + Space Wolves meant to be Conditional (C) or Sworn Enemies (S)? And are the two blanks S?

2. **Iron Warriors missing.** The matrix has 17 Legions; IV Iron Warriors has no row or column. *Built:* no alliance
   checks for Iron Warriors (only allegiance). *Question:* what are Iron Warriors' relations? (Probably like the other
   Traitor Legions: A with EC NL WE DG TS SoH WB, C with AL, S with the Loyalists?)

3. **Talons of the Emperor missing.** No row/column for Talons (Custodes / Sisters of Silence). *Built:* only its own
   rules (always Loyalist, The Emperor's Talons). *Question:* add Talons to the matrix (e.g. S with Daemons and the
   Traitor Legions)?

4. **Matrix vs declared allegiance.** The matrix is "At the Height of the Heresy" and treats Legions by their historic
   side, but a Legion may be fielded with either allegiance (LA "Allegiance"). *Built:* the matrix applies whatever the
   declared allegiance, plus an error whenever Loyalist and Traitor detachments are in the same army. *Question:* is
   that right (e.g. a Loyalist Sons of Horus detachment + Loyalist Ultramarines is still Sworn Enemies)? And do all
   detachments really have to share one allegiance (C and the army lists only say "compatible")?

5. **Mechanicum, Exercitus, Questoris, Solar Auxilia vs Daemons.** They are A with every Legion (Traitor ones too) and
   S only with Daemons. Fine as built - just confirming that e.g. a Traitor Mechanicum detachment with a Death Guard
   primary is Allies and Brothers.

6. **Blackshields (BS) = The Lost and the Damned catalogue.** *Built:* the BS row/column applies to the Blackshields
   force of The Lost and the Damned (C with everyone). Agents of the Sigillite (same catalogue) count as Allied
   Detachment but have no matrix row: only "alongside a Loyalist Primary Detachment" is checked. *Question:* OK?
   Shattered Legions has no catalogue of its own yet - see question 9.

7. **Allied Detachment size.** C gives no separate allied chart: an allied detachment uses the full Standard Force
   Organisation Chart (1-2 HQ, 2-6 Troops, ...) and no points limit. *Built:* exactly that. *Question:* do you want a
   smaller allied chart or a points cap (e.g. 25% / 50%) for allied detachments?

8. **Covenant Detachment 25% limit.** FotL Word Bearers: "The Covenant Detachment may cost no more than 25% of the
   army's total points limit". *Built:* the chart (HQ 0-1, Troops 1-3, Elites/FA/HS 0-1) and its restrictions; the 25%
   points cap is not checked (New Recruit cannot compare one force's points with the army's limit reliably) - it is in
   the rule text. With The Dark Brethren the Word Bearers may use the normal Ruinstorm Allied Detachment instead (both
   are available; using that one without the Rite is not flagged). OK?

9. **Shattered Legions.** L&D: "A Shattered Legions force is not a separate army list... modify a force chosen from the
   Legiones Astartes Army List and allow warriors from several different Legions to fight together within the same
   army." *Built:* nothing yet - each Legion is its own catalogue, so a Shattered Legions army can only be made today
   as a Primary + Allied Detachments of different Legions (with each detachment's own FOC). *Question:* is that an
   acceptable stand-in, or should Shattered Legions get its own catalogue (one FOC, units of 2-3 chosen Legions)?
   That is a big build (all Legion units in one catalogue).

10. **"Sworn Brothers" / "Desperate Allies" / "Fellow Warriors".** FotL Word Bearers (The Dark Brethren, Covenant)
    still use older ally levels that are not in the GAD legend (A / C / S). *Question:* which GAD level do they mean
    (Sworn Brothers = A, Desperate Allies = C?), and should the WB text be changed?
