# XX - Alpha Legion: questions for the author

Source: `/home/claude/src/legions_v4/XX_Alpha_Legion.txt`. Module: `tools/legions/xx_alpha_legion.py`.

## Open questions

1. **Rewards of Treachery units: which version of the other Legion's rules?** (l.112-115: "It retains its normal
   profile, equipment, options and unit-specific special rules, but replaces its original Legion-specific version of
   Legiones Astartes with Legiones Astartes (Alpha Legion).")
   Built: the 43 units you listed are copied from their own Legion's catalogue as Elites choices named
   "<unit> (Rewards of Treachery)", shown only with The Coils of the Hydra or Ingo Pech, one per Detachment. Options
   that in their own Legion depend on that Legion's Rites of War, characters or Legion-wide choices (e.g. "Troops under
   Rite X", "0-1 unless Character Y") are treated as if that Rite/character is never present; their Troops/other slot
   changes are removed (always Elites). Wargear and rules that share a name with an Alpha Legion/base rule show the
   Alpha Legion/base text. Q: OK, or should any of these units keep an option that depends on its own Legion's choices?

## Shown as text only (not enforced by the builder)

2. **The Coils of the Hydra limitations** (l.120-124): every Infantry unit must have Infiltrate / Deep Strike / a
   purchased Dedicated Transport; no Fortification or Allied Detachment from another Legion. Enforced: three
   compulsory Troops (l.120) and the one-Consul limit (l.123, Vigilator excepted; Autilon Skorr does not count).
3. **Headhunter Leviathal limitations** (l.156-157): Vehicles start in Reserve; no Allied Detachment.
4. **Kraken Bolts** (l.343): usable from any Bolter or the Bolter component of a Combi-weapon; a Headhunter that swaps
   to a special weapon loses them. The Kraken Bolts profile stays on the unit (no per-model removal); the rule is
   explained in "Kraken Bolts (Headhunters)".
5. In-game rules shown as text: Martial Hubris, Siege Specialists, Subterfuge, Signal Corruption, Sudden Strike, False
   Flags, Leave No Head upon the Serpent, Pre-emptive Strike / All as Planned, Coordinated Sabotage (choice offered,
   duplicate of the Mutable Tactic hidden), Operative Cell (choice built), Human Agents, Hydra's Wail, The Harrowing,
   Weapon Mastery, Execute the Mandate, Desperate for Glory, False Disposition, Hydra's Resilience, Master of Lies,
   The Hydra, Sire of the Alpha Legion, I Am Alpharius, Exodus never being the Warlord. The Rewards of Treachery units
   do not lose rules their own Legion module put on them that come from that Legion's core rules (if any).
