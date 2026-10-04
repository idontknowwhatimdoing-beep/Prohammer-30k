# Allied Detachments and the Allies Matrix: questions for the author

Built from the current Games in the Age of Darkness (GAD) matrix incl. Iron Warriors and Talons, the GAD Allied
Detachment Force Org Chart (HQ 1, Troops 1-2, Elites / Fast Attack / Heavy Support 0-1, max 25% of the army) and the
author's answers. A Legion fielded with the other allegiance swaps sides (Loyalist Sons of Horus + Ultramarines is
fine); all detachments of an army share one allegiance. Code: `tools/allies.py`, `tools/data/allies_matrix.py`.

1. **Iron Warriors vs Iron Warriors.** GAD row IW / column IW = "S". *Built:* ignored (two Iron Warriors detachments
   are not Sworn Enemies; the core "second detachment of the same list" rule still applies). *Question:* typo, or
   really S?

2. **Talons row vs Talons column.** The T row disagrees with the T column in some cells: T row says SoH C, WB C,
   Salamanders S, AL S; the SoH, WB, Salamanders and AL rows say T = S, S, C, S. *Built:* the other army's row wins
   (Talons + Salamanders = C; Talons + SoH / WB = S, which only matters for same-allegiance armies anyway). *Question:*
   is the T row shifted by one column?

3. **Lords of War / Fortifications in the Allied Detachment.** The new chart lists only HQ, Elites, Troops, Fast
   Attack, Heavy Support. *Built:* Lords of War 0, Fortification 0 in an Allied Detachment. OK?

4. **25% with several Allied Detachments.** *Built:* the points of all Allied Detachment units together may not exceed
   25% of the army (New Recruit can only sum them). Should it be 25% per detachment instead?

5. **Ruinstorm Allied Detachment and Covenant.** They keep their own charts (army book). The Covenant keeps its own
   25% (text); the Ruinstorm Allied Detachment has no points cap. OK?

6. **Word Bearers wording (your Q10: "Sworn Brothers").** Suggestion for the Word Bearers text in Forces of the
   Legions, to use the GAD levels:
   - Covenant: "Word Bearers and Covenant units are treated as **Allies and Brothers**. Independent Characters from one
     Detachment may not join units from the other." (was "Fellow Warriors")
   - The Dark Brethren / From Beyond: "This Allied Detachment is treated as **Allies and Brothers** with the Word
     Bearers." (was "Sworn Brothers")
   - The Dark Brethren limitation: "Any Allied Detachment other than Daemons of the Ruinstorm is treated as a
     **Conditional Alliance**." (was "Desperate Allies")
