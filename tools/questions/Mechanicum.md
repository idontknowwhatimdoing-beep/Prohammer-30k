# Mechanicum - questions for the author

Source: `/home/claude/src/v4/Mechanicum.txt` (line numbers below) and the Combined Armoury
(`/home/claude/src/v4/Mechanicum_Armoury.txt`, used for all wargear access and costs). Module:
`tools/armies/mechanicum.py`. All earlier questions are settled (answers applied).

## Structure of the catalogue

- One common army list (the book says it is a single list, L148). A **Mechanicum Army** configuration entry (one per
  Detachment) carries the army rules, adds +1 HQ to the game system's chart (Mechanicum HQ 1-3, L160-163) and holds
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

1. **Weapons Platform profile (L2586-2645)**: you answered "normal artillery rules", but the book prints no profile
   for the platform itself. Built: Weapons Platform = Artillery, T7 W2 Sv 3+ (the Rapier Carrier values used in the
   other lists), crew = 3 Artillery Servitors per platform with Laspistol and Close Combat Weapon (L2622; L2623 still
   says "three Servitors armed with autopistols"). New weapons Photon Thruster and Plasma Caster (+40 per platform,
   L2638-2639; Plasma Caster 36" S7 AP2 Heavy 2, Blast, Gets Hot from L12655) added. Are T7 / W2 / 3+ right, and is
   it Laspistol or autopistol for the crew?
2. **Typos still in the new text (your answer to the earlier Q23 was "deleted and fixed")**: only the editorial note
   was removed. Still printed and built as printed: Vorax A "2(3)" (L4933), Ursarax Point-Blank Blast AP "Power
   Weapon" and the rule name "Prisoned" (L4746-4747), Maxima Bolter 12" Assault 3 (L12618), Earthshaker Cannon
   36-120" (L7156; the Legion list has 36-240"), Possessed Power Claw AP "Power Weapon" (L8993). Please correct them
   in the book if they are typos (or confirm).
3. **Archimandrite (L7788)**: "The army's Warlord must be an Archmagos." Kelbor-Hal, Kane and Decima count as
   Archmagos. Lukas Chrom and Anacharis Scoria now satisfy the "Archmagos or Magos Dominus" requirement of the Orders
   (your answer), but do they also count as an Archmagos for Archimandrite? Built: yes (no error for them; only a
   Magos Dominus Warlord gives an error).

## Rules shown as text only (not enforced)

Programmed Behaviour, Cortex Controller ranges, Cybertheurgy and all rites, Battlesmith, all Order bonuses
(Legion of Steel, Ruthless Assault, Great Hunt, Doctrina, Binaric Command Network, Omnissian Engines, Organic
Resilience, etc.), Warlord abilities of the Orders, Legio Cybernetica FA/HS order, Secutarii Titan requirement,
Archimandrite Warlord must be an Archmagos (only hidden for the Magos Dominus and an error), Archimandrite "vehicles
with Blessed Autosimulacra as standard lose it", Thallax Ferrox "may not replace Lightning Guns" (option hidden),
Scyllax / Karkinos / Praetorian Servitor Protocols, Paragon of Metal effects, Fleshcraft table, Reclamation Vats,
Scrapcode tables, Scrapcode / Ruinous Edicts, Overload Protocols, Unstable tests, all vehicle wargear effects,
characteristic changes from Abeyant, Machinator Array, Augments, Reconstructions and Warp-Wings (only the Adjutant
specialisations change the profile). Protector Squad: at most two Servo-Arms and two Mechanicum Axes are enforced,
not that they are carried by the same two Protectors. Power Armour bought by a Skitarii Primus / Adjutant /
Tech-Priest replaces War Plate (War Plate stays listed). Dark Invocation: 1 power at Mastery Level 1, 2 at Mastery
Level 2, Possession only at Mastery Level 2 (enforced); Psychic Tests at Leadership 7 is text.
