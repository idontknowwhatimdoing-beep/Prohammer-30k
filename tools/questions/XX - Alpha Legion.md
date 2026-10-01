# XX - Alpha Legion: questions for the author

Source: `/home/claude/src/legions/XX_Alpha_Legion.txt`. Module: `tools/legions/xx_alpha_legion.py`.

## Ambiguities / decisions

1. **Mutable Tactics: when is the skill chosen?** (l.4: "must select one of the following Veteran Skills at the point
   where Warlord Traits are selected for the game")
   Built as an *optional* "Mutable Tactics" choice on the Legion entry (no error if left empty), because it is chosen at
   game time. Coordinated Sabotage and the Coils of the Hydra Infiltrate check read this choice if it is made.
   Q: Should the roster force the choice when the list is built?

2. **Kraken Bolts on the Headhunter Kill Team** (l.343: wargear "Kraken Bolts") - no profile is printed in the Legion
   text. I linked the existing Kraken Bolts profile of the base Special Issue Ammunition (30", S4, AP4, Rapid Fire).
   Q: Is that the intended profile? Do Headhunters fire them from the Bolter as an alternative to Banestrike (and what
   happens when a Headhunter swaps his Bolter for a Combi-weapon or special weapon)?

3. **Deadshot (Exodus)** (l.798: listed under Special Rules) - no rule text exists anywhere in the Legion text.
   Shown as a placeholder rule. Q: What does Deadshot do?

4. **Exodus is not an Independent Character / Master of the Legion** (l.792-799). Built as a unique HQ with no IC, no
   Master of the Legion and not eligible for the compulsory HQ (Lone Killer, l.760). The "never the army's Warlord"
   part is text only. Q: Correct? Does he still occupy an HQ slot (built: yes)?

5. **Banestrike Ammunition "all or none"** (l.43). Seeker and Veteran Squads get one squad-wide entry costing +5 per
   model, minus 5 for each model carrying a non-bolter special/heavy weapon (those models are not "eligible").
   Praetor/Centurion get it for +5 in their Armoury "Additional Wargear" (counts towards the 100-pt cap), only while
   they carry a Bolter, Foeblaster Boltgun, Combi-Bolter or Combi-weapon. Q: Is that the intended reading, and do Legion
   Armoury purchases count against the Armoury caps?

6. **Power Dagger / Venom Spheres for "Characters with access to the Space Marine Armoury"** (l.62, l.68).
   Added to the Praetor/Centurion 100-pt Armoury and to every "Space Marine Armoury (max 50 pts)" group (Sergeants and
   also Champions/other unit-upgrade characters). Headhunter Prime / Effrit Principal buy them only from their own
   option lists (no double purchase). Q: Should Venom Spheres be restricted to true Sergeants and ICs only ("squad
   Sergeant", l.68)?

7. **Teleportation Transponders (+15 per unit)** (l.87: "Any Alpha Legion unit composed entirely of models wearing any
   form of Terminator Armour"). Added to Legion Terminator Squads, Legion Terminator Command Squads (all retinue copies)
   and Lernaean Terminator Squads; +10 for a Praetor/Centurion in Terminator Armour. Q: Any other units (e.g.
   Dreadnoughts, which do not wear "Terminator Armour") meant to be included?

8. **Hammerstrike Assault (Armillus Dynat)** (l.706: "+10 points for the whole Unit"). Offered as a +10 option on each
   of Dynat's retinue choices (Command Squad, Terminator Command Squad, Lernaean); the normal +15 Terminator option is
   removed there so it cannot be bought twice. Units he joins in-game are not covered. Q: Does he also pay for his own
   Transponders (he already has them in his wargear, l.720)?

9. **Legion Operatives: Laspistol or Autopistol** (l.207). Built as a required squad-wide choice. Q: Per model or per
   unit? Do they differ in rules (both given the same 12" S3 AP- Pistol profile - no profile is printed)?

10. **Operative Leader armoury** (l.228: "up to 10 points of weapons from the Space Marine Armoury"). Built as optional
    extra weapons (all Armoury weapons costing <= 10 pts, plus Power Dagger) capped at 10 pts. Q: Are these
    additions or replacements for the Close-combat weapon / pistol?

11. **Infiltration Network** (l.26-28). Legion Operatives are Troops; each unit can tick "does not occupy a Troops
    selection" (max two per Detachment). They never count towards the compulsory Troops. Q: OK? Does the free slot need
    to be "used" by the first two units automatically?

12. **Lernaean Terminator Squad weapons** (l.445: "Power weapon or Power fist"; l.456 Chainfist +5; l.460 Combi-weapon
    "at the normal Armoury cost"). Built: default Power Weapon, swap to Power Fist (free) or Chainfist (+5); Combi-weapons
    at the Armoury costs (Combi-Bolter 5, Flamer/GL/Volkite 10, Melta/Plasma 15). Heavy swaps ("replace their ranged
    weapon", l.463) take the Volkite Charger. Q: Is a Chainfist available directly instead of the Power Weapon (built:
    yes, +5)? Are the Armoury combi costs right?

13. **Lernaean Dedicated Transport** (l.471: "a Land Raider, Dreadclaw Drop Pod or Spartan Assault Tank"). Offered:
    Land Raider Phobos, Land Raider Proteus, Anvillus Pattern Dreadclaw Drop Pod, Legion Spartan Assault Tank. No
    capacity check. Q: Which Land Raider variants count, and can Terminators really ride a Dreadclaw?

14. **Sheed Ranko** (l.1045). Built as an upgrade model inside the Lernaean Terminator Squad (110 pts, replaces one
    Lernaean Terminator, so +62 net); one per army across all Lernaean copies (Elites, Dynat/Pech/Alpharius retinues).
    Q: Can he be taken in a Lernaean squad that is a character's retinue?

15. **Command Squads for Autilon Skorr and Mathias Herzog** - their entries give no retinue. Both are Master of the
    Legion, so each may take a Legion Command Squad by the general Master of the Legion rule (built). Q: Correct?

16. **Autilon Skorr = Delegatus Consul** (l.880). Built: error if the Detachment also has a Legion Praetor (Delegated
    Authority). Under The Coils of the Hydra he counts as the one allowed Consul: error if a Centurion in the Detachment
    is also a (non-Vigilator) Consul. Q: Does he count for that Coils restriction (he is not a Centurion)?

17. **Ingo Pech: Legion Seeker Squad retinue** (l.924). Built as a copy of the Legion Seeker Squad (incl. Banestrike and
    Saboteur options). Q: Fine?

18. **Headhunter Leviathal Troops** (l.134-135). Headhunter Kill Teams become Troops (0-1 limit lifted) and Tactical /
    Assault / Breacher Squads no longer count as compulsory Troops. Q: May other Troops units (e.g. Legion Operatives)
    still be taken as non-compulsory Troops (built: yes)?

19. **Headhunter Commander (Herzog)** (l.1000). One Headhunter Kill Team can tick "does not occupy an Elites choice"
    while Herzog is in the army (max one per army; hidden under Headhunter Leviathal, where they are Troops anyway).

20. **Alpharius' Primarch Retinue** (l.1294-1300). Honour Guard, Terminator Command Squad or a Lernaean Terminator
    Squad (the retinue copy is outside the 0-1 limit). Points: 490 (l.1117), Sv 1+ with Primarch Armour 4++.

## Shown as text only (not enforced by the builder)

21. **The Rewards of Treachery** (l.113-116) and **Master of Deceit** (Ingo Pech, l.928): the catalogue only contains
    the Alpha Legion's own units, so another Legion's unique units cannot be selected. Q: Should specific units be
    copied into this catalogue (which ones)? This would need a shared-file change.
22. **The Coils of the Hydra limitations** (l.121-124): every Infantry unit must have Infiltrate / Deep Strike / a
    purchased Dedicated Transport; no Fortification or Allied Detachment from another Legion. Text only. Enforced: three
    compulsory Troops (l.120) and the one-Consul limit (l.123, Vigilator excepted).
23. **Headhunter Leviathal limitations** (l.156-157): Vehicles start in Reserve; no Allied Detachment. Text only.
24. In-game rules shown as text: Martial Hubris, Siege Specialists, Subterfuge, Signal Corruption, Sudden Strike, False
    Flags, Leave No Head upon the Serpent, Pre-emptive Strike / All as Planned, Coordinated Sabotage (choice offered,
    duplicate of the Mutable Tactic hidden), Operative Cell (choice built), Human Agents, Hydra's Wail, The Harrowing,
    Weapon Mastery, Execute the Mandate, Desperate for Glory, False Disposition, Hydra's Resilience, Master of Lies,
    The Hydra, Sire of the Alpha Legion, I Am Alpharius.
