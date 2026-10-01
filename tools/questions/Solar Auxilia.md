# Solar Auxilia - questions for the author

Source: `/home/claude/src/Solar_Auxilia.txt` (line numbers below).
Module: `tools/armies/solar_auxilia.py`.

## Unclear / missing points

1. **Infantry Tercio structure (L1654-1694).** Built: "Auxilia Infantry Tercio" is a Troops unit (0 pts) holding 1-3 Section sub-units (Lasrifle / Veletaris / Flamer; Achmiris and Eidis only under their Doctrines). Each Section has its own Dracosan option. Errors: Flamer (or Pioneer Eidis) Section without a Lasrifle Section; more than one Troop Master per Tercio. Question: is this the intended structure?

2. **Tercio of only Veletaris (L1658 vs Veletaris Assault Cohort L5058).** The normal Tercio says "any combination", so a Veletaris-only Tercio is already legal; the Doctrine says it "does not require an Auxilia Lasrifle Section". Built: no Lasrifle requirement except for Support Sections. Question: does a normal Tercio need a Lasrifle Section unless the Veletaris Assault Cohort is used? "Veletaris Storm Sections may fulfil the compulsory Troops selections" - they already do inside a Tercio; what does this change?

3. **Auxilia Tank Commander (L790).** "55 points + cost of tank". Built: an HQ unit (55 pts, Support Officer, not compulsory HQ) with a required "Commanded Vehicle" choice and a required Tank Ace ability; the tank is bought separately in its own slot. A warning appears if no eligible vehicle is in the Detachment (Baneblade etc. come from Engines of War and cannot be checked). Question: does the tank take its own Force Organisation slot (as built)? Does "Malcador" include the Malcador Infernus (built: yes)?

4. **Life Ward Retinue (L806-934).** Built as a retinue (1-6 Life Wards, 15 pts each) linked from the Legate Commander, Ireton MaSade and Aevos Jovan (the Solar Auxilia Independent Characters). The "only one Life Ward in the Detachment may select Power Fist / Inferno Pistol" limit is checked inside one retinue only. Question: may one retinue be split between several Characters? Is the Strategos (not an Independent Character) eligible?

5. **Cohort Attaches (L960-1035).** Built as one "Cohort Attaches" entry (max one per Detachment, 1-3 Attaches, each type once) selectable from the Legate Commander or the Tactical Command Section; assignment to a unit is text. Question: OK? Should the Attaches also be selectable from the Life Ward Retinue / MaSade?

6. **Mechanicum Liaison Adept (L1029)** unlocks "Thallax Cohorts and Castellax Battle-automata Maniples where permitted by the Solar Auxilia army list" - this list has no such entries. Also the Power Axe has no profile; built as a Power Weapon (User, -, Melee, Power Weapon). Question: where do Thallax/Castellax come from, and what is the Power Axe profile?

7. **Heavy Bolter profile missing.** Used by Leman Russ, Tarantula, Servo-automata, artillery pintles, but not in the weapon tables (L4683-4887). Built: 36" S5 AP4 Heavy 3 (Twin-linked version for Tarantula). Question: confirm.

8. **Eidis Engineer Section cost (L1442).** 25 points for 5 models (Prime + 4 Engineers), +5 per additional Eidii, +10 to upgrade an Engineer. Built as printed. Question: is 25 correct (Lasrifle Section 100 for 20)?

9. **Eidis weapon swaps (L1543).** Built: one choice for all Engineers and one for all Eidii (per model cost); the Prime has an optional slot with the same three weapons. Question: must the Prime's weapon match one of the Section's choices (not enforced)?

10. **Hades Breaching Drill availability.** The Eidis entry already allows the Hades (L1598-1604) and the Void & Siege Cohort grants it again (L5064). Built: always available. Question: is the Hades meant to be Void & Siege only?

11. **"Breaching Charges for free" (Void & Siege, L5064).** Built: a free option on an Eidis Section (one per Detachment, error otherwise) linking Breaching Charge. Question: does every model in that Section get a Breaching Charge, or only the Prime?

12. **Veletaris / Lykis weapon swaps (L1956-1962, L2926-2932).** Fixed 9 models, so built as one choice: "Rotor Cannons (Veletarii)" / "(Veletarii and Prime)" free, "Power Weapons" +45/+50; Lykis Rending +36/+40, Power +45/+50. Question: OK?

13. **Achmiris special ammunition (L2820-2824).** "All models may purchase AT rounds / Volkite rounds +5 points each". Built: each as a whole-Section upgrade at +5 per model (both may be bought), hidden once the sniper rifles are exchanged. Question: may a Section buy both? Must all models buy it?

14. **Household Retinue Veletaris (L618).** Built: separate Elites unit "Veletaris Storm Section (Household Retinue)" (WS4 Veletarii, no Hold the Line, Preferred Enemy (Infantry), Dracosan or Arvus). Error if the Detachment has no Lord Marshal; "is the army's Warlord" is not checked.

15. **Lord Marshal (L543).** "One Legate Commander in the army" - built as max one per roster. Relic Blade, Grav-wave Generator and Displacer Matrix give an error without the Lord Marshal upgrade.

16. **Ireton MaSade (L3762).** "Must be the army's Warlord" conflicts with Disciplined Command (a Lord Marshal / Legate would outrank him) and the Armoured Cohort requirement. Built: text only. Question: does MaSade override Disciplined Command? Is Aevos Jovan restricted to an Allegiance (none stated, built unrestricted)?

17. **Vaskale Solar (L3934).** Built as an upgrade (+30) inside the Troop Master upgrade of a Lasrifle Sergeant, Loyalist only, one per army; the Sergeant profile changes to Troop Master / Vaskale stats. OK?

18. **Squadron Prime (Armoured Cohort, L5046).** Built as a squadron-level upgrade (+25, max one, only with three vehicles) for Leman Russ Strike/Assault, Artillery Batteries and Sentinel Squadrons. Question: which units count as "Vehicle Squadrons" (Sentinels with 4-5 models? Tarantulas?)

19. **Top Working Order (L5046).** Built for every vehicle with upgrades: Nuncio-vox +10 and Flare Shield +35. The Dracosan, Malcador and Arvus already have a Flare Shield option (+25/+20); for those only the Nuncio-vox is added. Question: correct?

20. **Infantry Cohort vehicle squadron limit (L5040).** Built: at most one of Leman Russ Strike Squadron / Armoured Sentinel Squadron (FA) and one of Leman Russ Assault Squadron / Artillery Tank Battery (HS). Question: do single-vehicle units (Malcador, Valdor) or Tarantulas count?

21. **Armoured Cohort (L5046).** Built: Strike Squadrons become Troops and count for compulsory Troops; Tercios no longer count for compulsory Troops; Assault Squadrons become Elites; errors for fewer than two Strike Squadrons, no Tank Commander, Fortifications, Tarantulas; Rolling Army error on every unit with a transport option that has none. Question: may Tercios still be taken as (non-compulsory) Troops?

22. **Void & Siege Reinforced Void Armour (L5064):** +2 per model built as +40 for the fixed 20-model Section.

23. **Artillery Tank Battery as Elites (Siege Train):** built as a toggle on the unit, only under Void & Siege.

24. **Arvus Lighter (L2248):** "Available To: Imperial Army" kept as a Solar Auxilia transport (TCS, Household Veletaris). Chaff Launcher, Armoured Cockpit and Illum Flares refer to Aeronautica Imperialis - only summary text given.

25. **Tactical Command Section (L705):** additional Veteran Auxiliaries cost only +5 each - built as printed.

26. **Typos:** "Life Ward Reteniue" (L934), "Areonautica" (L4556); Grav-wave generator rule (L4405) vs table. Displacer Matrix etc. as written.

## Rules shown as text only (not enforced)

- Warlord precedence (Disciplined Command), Doctrine Warlord requirements, MaSade "must be Warlord".
- Tercio deployment/reserves, Support Section across Detachments, Zone Mortalis split.
- Life Ward / Attache / Medicae Orderly / Jovan assignment to units; Achmiris Veiled Bodyguard joined to the Legate.
- Tank Commander assignment to a specific vehicle (warning only), Command Sentinel.
- Reconnaissance Cohort: Malcadors/Valdor start in Reserve; Void & Siege: no Outflank; Veletaris Furious Charge, Fury of the Auxilia, Amongst the Men, Prepared Positions and all other in-game Doctrine effects.
- Mechanicum Liaison unlock of Thallax/Castellax.
- Lords of War / Fortifications (in other army lists); the Super-heavy Command Tank rule is included as text only.
- All weapon, wargear and unit special rules (Hold the Line, High Command, Charger Burnout, Tunnelling, etc.).
