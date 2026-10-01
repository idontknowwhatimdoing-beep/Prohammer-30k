# Aeronautica Imperialis - questions for the author

Source: `/home/claude/src/Areonautica_Imperialis.txt` (line numbers below).
Module: `tools/armies/aeronautica_imperialis.py`.

## Unclear / missing points

1. **Which army takes an aircraft (L46, L58).** "Each aircraft may be selected by the army or armies indicated in its entry." Built: a separate "Aeronautica Imperialis" catalogue; every aircraft is a root unit in its stated slot and carries a rule "Available to: ..." with the armies. New Recruit cannot check across catalogues which army (Detachment) the aircraft belongs to, so this is not enforced. Question: OK as a separate catalogue, or should each army catalogue link these aircraft directly?

2. **Legiones Astartes aircraft have no "Available To" line (L346-862).** Built: Primaris-Lightning = Legiones Astartes, Imperial Army, Mechanicum (from L1251-1261); Xiphon, Storm Eagle, Fire Raptor, Caestus = Legiones Astartes only (from the section heading L307). The book names no aircraft for the Talons of the Emperor or any other army. Question: correct? Should any aircraft be available to the Talons of the Emperor / Legio Custodes / Sisters of Silence?

3. **Primaris-Lightning for Imperial Army / Mechanicum (L1251-1261).** "May select a Primaris-Lightning ... as a Fast Attack choice using the profile and options presented in the Legiones Astartes section." Built: one entry for all three armies (BS4 for everyone). Question: does the BS stay 4 for Imperial Army / Mechanicum?

4. **"Imperial Army" (L902).** "Imperial Army includes the Exercitus Imperialis and Solar Auxilia." Built as rule text. The Solar Auxilia list already has its own "Auxilia Arvus Lighter" as a Dedicated Transport; here the Arvus is a Fast Attack choice. Question: are both meant to exist (Dedicated Transport in Solar Auxilia, Fast Attack from this list)?

5. **Weapon table duplicated (L265-270).** The first five rows are printed a second time with identical values. Built once. Just a layout error?

6. **Weapon rules not defined in this book.** Crawling Fire and Deadly Cargo (Phosphex Bomb Cluster, L256) have no text anywhere in this list - built as profile text only, no rule link. One Use - built with a generic text ("may only be fired once per battle"). Rad-phage and Lingering Death - text taken from the Legiones Astartes list. Poisoned (3+) linked to the core Poison rule. Barrage / Blast / Large Blast / Melta are core weapon types. Question: please give the texts for Crawling Fire and Deadly Cargo and confirm One Use.

7. **Standard weapon profiles not printed (L242).** Built with the usual profiles: Lascannon 48" S9 AP2 Heavy 1; Autocannon 48" S7 AP4 Heavy 2; Multi-laser 36" S6 AP6 Heavy 3; Heavy Bolter 36" S5 AP4 Heavy 3; Multi-Melta 24" S8 AP1 Heavy 1, Melta; Missile Launcher Frag 48" S4 AP6 Heavy 1 Blast / Krak 48" S8 AP3 Heavy 1; Havoc Launcher 48" S5 AP5 Heavy 1, Blast, Twin-linked (from the Legiones Astartes list); twin-linked versions add "Twin-linked". Twin-linked Avenger Bolt Cannon (Fire Raptor) and Twin-linked Magna-Melta (Caestus) = table profile + Twin-linked. Question: confirm.

8. **Terminal Tracking (L301 vs L519).** The general rule says "including those gained through Evasion"; the Xiphon box says "including saves gained through Jink or Evasion". Built: general text with the Jink note. Question: which wording is correct?

9. **Primaris-Lightning Dual Hardpoint Mounts (L395-411).** Built: three separate optional mounts, each 0-1 of the seven options; the same option may be taken in several mounts; a mount may be left empty. Question: may a mount stay empty? May the same load-out be repeated? Is the base Twin-linked Lascannon separate from the three mounts (built: yes)?

10. **Rad Missiles (L428).** "+15 points per launcher." Built: a "Rad Missiles" upgrade inside each Twin-linked Missile Launcher mount, adding the Rad Missile profile (48" S4 AP3 Heavy 1, Blast, Fleshbane, Rad-phage) as a third firing mode. Question: is it an additional ammunition type (as built) and is it One Use?

11. **Bombs (L84-102, L1082).** "A Flyer may only use one Bomb weapon during each Movement phase." The Avenger's "Six Tactical Bombs" therefore drop one per Movement phase (each One Use). Built as text. Question: intended (six turns of bombing)?

12. **Unit composition / squadrons.** Every aircraft is "1 ..." (no squadrons), so numbered() was not needed. No 0-1 or per-points limits are printed. Question: confirm there are no squadron or 0-1 limits.

13. **Allegiance.** The book gives no Loyalist/Traitor restrictions; none built.

14. **Fire points (L601-615, L831-841).** Storm Eagle and Caestus give no Fire Points line (Arvus: "None"). Built: "-". Question: do they have none?

15. **Caestus Misericord (L862).** Passenger restriction (Power/Artificer/Terminator Armour only; Terminators count as one model) is text only.

16. **Arvus Lighter - Mechanicum only (L1236).** Built: a "Battle-automata Carriage (Mechanicum only)" upgrade (+20) with the rule text. That only a Mechanicum army may take it, and the Castellax / Vorax cargo, cannot be checked across catalogues. Question: does the Arvus (a Fast Attack choice) carry the automata from their own slots? Can the Arvus carry other units otherwise (no restriction printed)?

17. **Auxiliary Drive (L849).** Not defined in this book; built with the Legiones Astartes text (Immobilised: 4+ to remove one result).

18. **Thunderbolt costs (L977-983).** "Four Hellstrike Missiles ... Free" - built as free. Name "Auxilia Thunderbolt" but available to all of the Imperial Army - built as printed.

## Rules shown as text only (not enforced)

- Available to: ... (all aircraft) - which army takes the aircraft.
- Aeronautica Imperialis (using this list / Flyers), Air-to-Air Targeting, Agile, Bomb, Bomb X.
- Cluster Warhead, Heat Seeker, Sunder, Terminal Tracking, One Use, Rad-phage, Lingering Death.
- Armoury: Armoured Ceramite, Armoured Cockpit, Battle Servitor Control (links Tank Hunters), Chaff Launcher (once per battle), Ground-tracking Auguries (links Strafing Run), Ramjet Diffraction Grid, Flare Shield, Illum Flares, Infra-red Targeting (links Night Vision), Frag Assault Launchers, Auxiliary Drive.
- Special Ordnance - Rad Missiles, Independent Turret Fire, Caestus Ram, Misericord, Simulacra Repair, Combat Interdiction, Defensive Heavy Stubber (Avenger), Arvus Mechanicum-only automata carriage.
