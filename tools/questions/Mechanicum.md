# Mechanicum - questions for the author

Source: `/home/claude/src/Mechanicum.txt` (line numbers below). Module: `tools/armies/mechanicum.py`.

## Structure of the catalogue

- One common army list (the book says it is a single list, L92). A **Mechanicum Army** configuration entry (one per
  Detachment) carries the army rules, adds +1 HQ to the game system's chart (Mechanicum HQ 1-3, L114-118) and holds
  an optional choice of **Order of High Techno-Arcana** (12) or **Dark Techno-Arcana** (4, Traitor only). Zagreus Kane
  raises the limit to two. Units, options and errors of an Order / Dark Techno-Arcana appear when it is chosen.
- A shared **Warlord** upgrade (one per army) exists on every HQ Independent Character. It drives Djinn-skein, the
  Myrmidax / Ordo Reductor / Genetor Warlord options, and the "must be Warlord" rules. Orders that require an
  Archmagos / Magos Dominus Warlord hide the Warlord option on the Adjutant, Marshal and Axiarch.
- "May be selected as Troops" Order rules (Myrmidax, Skitarii, Genetor, Macrotek) are a free toggle on the unit.
  Units that "do not use a slot" (Protector Retinue, Reductor Bodyguard, Decima's Guardian Retinue, Kaban Machine) get
  a "+1 slot" Force Org category.
- Dark Mechanicum units are only visible/allowed with the Dark Techno-Arcana named in their Availability line.

## Unclear / missing points

1. **Skitarii Primus armoury (L3010)**: "may select weapons and wargear from the Skitarii section of the Mechanicum
   Armoury". There is no such section. Built: Primus may replace the Radium Carabiner like the Skitarii Marshal
   (Galvanic Rifle +5, Volkite Charger +5, Arc Rifle +10, Graviton Gun +15), take one melee weapon (Taser Goad +5,
   Corposant Stave +5, Arc Maul +10, Power Fist +15) and Auspex/Omnispex/Infravisor +5. Question: what is the list?
2. **Missing profiles**: Battle Cannon (L5552) built as 72" S8 AP3 Ordnance 1, Large Blast; Vanquisher Battle Cannon
   uses the "Vanquisher Anti-Tank Shell" profile (L5524); Heavy Stubber (L6935) 36" S4 AP6 Heavy 3; Arc Pistol
   (L1410, L3112) 12" S6 AP5 Pistol, Haywire; Lasgun is listed but unused. Please confirm.
3. **Wargear without rules**: Purity Seals (L2972) - shown with "no rules given"; Carapace Armour (L2903) - built as
   4+ save; Force Shield (L2714) - 4+ invulnerable as in the profile. Please give rules.
4. **Battle-Automata Power Blades** has two profiles: Castellax (L3473: User, -, Melee, Specialist Weapon) and
   Vorax/Vultarax (L4191, L4402: Melee, Rending, Paired). Built as two items ("Two Battle-Automata Power Blades" for
   the Castellax). Which is right?
5. **Weapons Platform crew (L2233-2235)**: "Laspistol and Close Combat Weapon" vs "three Servitors armed with
   autopistols". Built Laspistol. The platform itself has no profile (built without one) - should it have T/W/Sv?
6. **Myrmidon Hosts (L1709, L1822, L1937)** have Sv 3+ but no armour in their wargear. Built without an armour item.
7. **Protector Squad (L1637)**: "Up to two Protectors may take: Servo-Arm, Mechanicum Axe" - built as at most two
   items in total. May one Protector take both / may two take both?
8. **Mechanicum Leman Russ Squadron (L5509)** has no headline cost; built with the per-type costs from the table
   (140/120/145/150/175) per tank, all tanks the same type. Each tank must take a hull weapon (HB +5 default).
9. **Krios Squadron (L5199, L5247)**: first tank 175, additional tanks +125 - built as such. Confirm.
10. **Electro-Priest Covenant**: Siphoned Vigour (L2690) is not in its Special Rules list - added anyway. Unit has
    no Iron and Machine - correct?
11. **Orders require an Archmagos or Magos Dominus (L6069)**. Kelbor-Hal, Kane and Decima count as Archmagos. Do Lukas
    Chrom or Anacharis Scoria qualify (not built)?
12. **Rule of the Archmagos (L735, L8504)**: unit entry says "per Detachment", general rule "per army". Built: 0-1
    per army (Kelbor-Hal / Kane / Decima count as Archmagos), and an error if an Archmagos is not the Warlord (also
    triggers in an Allied Detachment). Same "must be Warlord" error for Scoria and Decima. OK?
13. **Legio Cybernetica (L6079)**: built - other Troops lose compulsory status, a Castellax Maniple with 2+ models
    counts as compulsory Troops, error with fewer than two Castellax Maniples, error if the Archmagos Warlord lacks a
    Cortex Controller. The Fast Attack / Heavy Support ordering restriction is text only.
14. **Flesh-Mechanica "Harvest of Flesh" (L6535)** approximated: error unless the Detachment has a Tech-Thrall
    Covenant and at least three Troops. "No more than one Heavy Support choice with Cybernetica Cortex": only
    Conqueror Maniples are counted (Thanatars are banned; Kaban "is not treated as having Cybernetica Cortex").
15. **Secutarii Order (L6175)**: "must include at least one Titan" - text only (Titans are not in this catalogue).
16. **Explorator Void-Hardened Armour (L6152)**: built for all Infantry units with armour including HQ characters
    (+1, +5 with Abeyant), Thallax and Ursarax (Jet Pack / Jump Infantry, +3 as Bulky). Electro-Priests (no armour),
    robots and Bombots excluded. Correct?
17. **Infernal Siege Engine (L7473)** "may purchase Mechanicum Vehicle Wargear" - no costs given; used Rhino /
    Land Raider costs (Dozer 5, Extra Armour 5, HK 5, Pintle SB 10, Searchlight 1, Smoke 5, Autosimulacra 5,
    Armoured Ceramite 20).
18. **Kaban Machine (L7804)**: "does not occupy a Heavy Support choice but instead gets a free Slot" - built as a
    Heavy Support unit that adds +1 Heavy Support. Fine?
19. **Tech-Priest Auxilia** - built as eligible for the compulsory HQ (no rule says otherwise) and each Tech-Priest
    is equipped separately. Should an Auxilia unit be able to be the army's only HQ?
20. **Kelbor-Hal edicts (L8083)**: Daemonic / Fleshcraft Edicts unlock the option on all eligible units, with an
    error if more than one unit takes it. Scrapcode and Ruinous Edicts are text only.
21. **Genetor Rad-Alchemy**: the Warlord's Rad Furnace costs 20 (instead of 30) when he is the Warlord in a Genetor
    army - only the Archmagos / Magos Dominus have a Rad Furnace option. Adjutant Malagra (+25) is unchanged.
22. **Myrmidax Perfected Armament**: the Warlord's Master-crafted upgrade becomes free (the book says "ranged
    weapon"; the builder cannot check which weapon).
23. **Typos / oddities kept as printed**: Vorax A "2(3)" (L4117), Ursarax Point-Blank Blast AP "Power Weapon" and
    rule name "Prisoned" (L3998), Maxima Bolter 12" Assault 3 (L9450), Earthshaker Cannon 36-120" (L5949, the
    Legion list has 36-240"), Possessed Power Claw AP "Power Weapon" (L6655). An editorial note was left in the
    rules text at L8640 ("The full rule already exists later...").
24. **Ordinator Bombardment**: the Adjutant version (L1056) lacks Lance/Twin-linked, the Ordinator Order version
    (L6182) has them - built both as printed.
25. **Shattersphere Grenades**: the Marshal may buy them (+5) - the Axiarch has them as standard. Rad Poisoning only
    in their profile.
26. **Archimandrite**: Blessed Autosimulacra purchase options are hidden (error if taken); vehicles that have it as
    standard (Krios, Macrocarid, Minotaur) keep the item in the list - "loses it" is text only.
27. **Dark Mechanicum**: all units of the base list remain available; Dark armies are forced Traitor (error).
    "Dark Mechanicum and Order both" cannot happen except with Kane (Loyalist) - not separately checked.

## Rules shown as text only (not enforced)

Programmed Behaviour, Cortex Controller ranges, Cybertheurgy and all rites, Battlesmith, all Order bonuses
(Legion of Steel, Ruthless Assault, Great Hunt, Doctrina, Binaric Command Network, Omnissian Engines, Organic
Resilience, etc.), Warlord abilities of the Orders, Legio Cybernetica FA/HS order, Secutarii Titan requirement,
Archimandrite Warlord must be an Archmagos (only hidden for the Magos Dominus and an error), Thallax Ferrox
"may not replace Lightning Guns" (option hidden), Scyllax / Karkinos / Praetorian Servitor Protocols, Paragon of Metal
effects, Fleshcraft table, Reclamation Vats, Scrapcode tables, Overload Protocols, Unstable tests, all vehicle
wargear effects, characteristic changes from Abeyant, Machinator Array, Augments, Reconstructions and Warp-Wings
(only the Adjutant specialisations change the profile).
