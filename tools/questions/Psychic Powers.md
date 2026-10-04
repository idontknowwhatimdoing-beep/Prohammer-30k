# Psychic Powers: questions for the author

Author's decision: "Spells should be pickable with effects and such also included - makes it easier for tracking."

Sources: core rules `/home/claude/src/core.txt` (C), Legiones Astartes list `/home/claude/src/legiones_v5.txt` (LA),
Legion texts `/home/claude/src/legions_v4/<Legion>.txt`. Data: `tools/data/psychic_powers.py`; helper:
`legiones.psychic_powers()`.

**What was built:** every psyker has a "Psychic Powers" group. Each power is an entry with its full rule text, a link
to its power type rule (Blessing, Malediction, Conjuration, Witchfire, Beam, Focused, Nova, Maelstrom) and, for
shooting powers with a profile, a weapon profile. The number of powers is the psyker's Mastery Level (Epistolary /
Master of Runes / Mastery Level 2 upgrades add one). Too few powers shows an error ("Choose N psychic powers") -
New Recruit does not pick for the player; more than allowed is blocked. Powers a psyker always knows are included
automatically. Thousand Sons psykers pick a Discipline (or use their Cult's Discipline) and only see that Discipline's powers;
psykers with a single extra power (Burning Lore, Stormseer Epistolary, Master of Runes, Yesugei) pick it directly.

1. **Thousand Sons Techmarine Cult.** XV L7: "All Thousand Sons Independent Characters are Psykers"; author: the
   Techmarine "chooses the spells like one with the cult restriction". *Built:* every Legion Techmarine in a Thousand
   Sons Techmarine Covenant is a Psyker (Mastery Level 1) and selects one power from the Discipline of the Covenant's
   Prosperine Cult. The Cult is chosen once for the whole Covenant (up to three Techmarines). *Question:* OK, or should
   each Techmarine (an Independent Character) choose his own Cult?
