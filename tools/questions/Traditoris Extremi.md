# Traditoris Extremi: questions for the author

Source: `/home/claude/src/Traditoris_Extremi.txt` (line numbers refer to that file).
Module: `tools/armies/traditoris_extremi.py`.

## How the supplement is built

1. **A supplement that modifies another list.** L43: "This List is to be Used with the regular Legiones Astartes army list and the forces of the Legions Army books. Certain FoC spaces will be changed and certain Unit Upgrades may be applied."
   *Built:* New Recruit cannot let one catalogue change another catalogue's Force Organisation or add options to its units. So this is a small separate catalogue, "Traditoris Extremi", with Traitor as the only Allegiance (fixed by default). It contains the additional units (for now only the Daemon Prince). The supplement's general text is a rule ("Traditoris Extremi") linked from the Allegiance entry. To use it, the player adds a second Detachment of this catalogue next to the Legion Detachment.
   *Downside:* the Daemon Prince sits in its own Detachment, so it does not use the Legion Detachment's HQ slots and New Recruit does not check that both Detachments are the same Legion.
   *Alternative:* once the supplement is finished, its units and upgrades could be added straight into the Traitor Legion catalogues (III, IV, VIII, XII, XIV, XV, XVI, XVII, XX). There they could be hidden unless a "Traditoris Extremi" configuration option is chosen, and the FOC changes and unit upgrades could then be enforced properly.
   *Question:* Do you want the separate catalogue for now, or should the units go into the Legion catalogues behind a "Traditoris Extremi" switch?

2. **Force Organisation changes and unit upgrades.** L43 says these exist, but the text does not list any.
   *Built:* nothing; only mentioned in the rule text.
   *Question:* Which FOC spaces change, and what are the upgrades (units, costs, effects)?

## Daemon Prince (L51-98)

3. **Force Organisation slot.** The entry gives no battlefield role.
   *Built:* HQ. It counts towards the compulsory HQ choice. No 0-1 limit.
   *Question:* Is HQ right? Can it be the compulsory HQ or Warlord? Is it limited (e.g. 0-1, or one per X points, or does it replace a Praetor)?

4. **Daemonic Aura** (L87, "Deamonic Aura"). No rule text is given.
   *Built:* a wargear item whose text says its rules are not yet defined.
   *Question:* What does Daemonic Aura do?

5. **Demonic Weapon** (L85): "counts as Power Weapon".
   *Built:* weapon profile Range -, Strength User, AP -, "Counts as a Power Weapon (Ignores Armour Saves)".
   *Question:* Is that right? Monstrous Creatures already ignore armour in close combat. Should the weapon add anything else (e.g. +1 Strength, a god-specific effect)?

6. **Save "3+/ 5+"** (L60) and the "Deamon" rule (L97).
   *Built:* save shown as "3+/5++". Linked the core "Daemon" rule (5+ invulnerable save, causes Fear), which matches the 5+.
   *Question:* Is the 5+ only from the Daemon rule, or is it Daemonic Aura?

7. **Named Legiones Astartes rule** (L93). The model has Legiones Astartes, so it needs a named Legion version.
   *Built:* a required, free "Legion" choice listing the Traitor Legions (III, IV, VIII, XII, XIV, XV, XVI, XVII, XX). It is only a label: Legion rules from the Legion catalogues are not linked.
   *Question:* Does the Daemon Prince gain its Legion's rules? Is the Alpha Legion a valid choice?

8. **Chaos patron / Marks.** The introduction (L41, L53) speaks of Daemon Princes bound to their patron god, but there is no option for it.
   *Question:* Should a Daemon Prince choose a patron (Khorne, Nurgle, Slaanesh, Tzeentch, Undivided), and what would each one give? Should it have options (wings, psychic powers, other weapons)?

9. **Monstrous Creature with Power Armour and Independent Character** (L77-95).
   *Built:* as listed. The core Independent Character rule says ICs may not join units that contain Monstrous Creatures; it does not say whether a Monstrous Creature IC can join units.
   *Question:* Can the Daemon Prince join Legion units?

## Rules shown only as text (not enforced)

- Traditoris Extremi (supplement use with the Legiones Astartes list; FOC changes; unit upgrades).
- Same-Legion check between the Daemon Prince and the Legion Detachment.
- Legiones Astartes (named Legion rule): label only.
- Daemonic Aura (no rules yet).
