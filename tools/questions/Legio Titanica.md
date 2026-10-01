# Legio Titanica - questions for the author

Source: `/home/claude/src/Legio_Titanica.txt` (line numbers below).
Module: `tools/armies/legio_titanica.py`.

## How the list is built

Every Titan (Warhound, Reaver, Warlord) is a root unit in the **Lords of War** slot (not compulsory-eligible), with its book cost. The single model uses the game system's **Walker** profile (WS, BS, S, Front, Side, Rear, I, A); Structure Points and Void Shields are written into the Unit Type ("Vehicle (Walker, Super-heavy, Titan); Structure Points 3; Void Shields 2"), and each Void Shield is also linked as a "Void Shield" wargear item (with the armoury rule text). The catalogue also has the usual Allegiance configuration (Loyalist / Traitor), which carries the army-wide Titan rules.

## Unclear / missing points

1. **Who may field Titans / FOC slot (whole book)**: the list never says which armies may take Titans or in which slot. The Questoris Households book says a Household "may select an eligible engine from the Collegia Titanica army list as its Lord of War".
   Built: every Titan is a Lords of War choice, with a rule "Fielding Titans" explaining this. Question: are Titans always Lords of War (one per army), or is there a Titan detachment / own Force Organisation chart (e.g. a Legio Maniple), and which armies may include them (all Imperial/Traitor armies, only Mechanicum/Knights)? Is there any points/size limit (e.g. Lords of War max 25% of points)?

2. **No Super-heavy Walker / Titan profile (L74-88, L350-352)**: the game system has no profile with a Structure Points (SP) column and nothing for Void Shields.
   Built: Walker profile + SP and Void Shields in the Unit Type text; Void Shields as N wargear items. Question: should a Super-heavy Walker/Titan profile type (with SP and Void Shields) be added to the game system (shared change)?

3. **Super-heavy Vehicle rules "presented earlier in this book" (L74, L88)**: Structure Points, Massive Firepower, Catastrophic Destruction / Apocalyptic Explosion are referenced but not contained in this list.
   Built: short "Super-heavy Walker" and "Structure Points" rules that point to the normal Super-heavy rules; Massive Firepower and Catastrophic Destruction are only mentioned by name. Question: please supply (or point to) the Super-heavy Vehicle rules text so it can be added.

4. **Void Shield source (L118 vs L247)**: L118 says Void Shields use "the normal Void Shield rules from the Lords of War Armoury", but the Collegia Titanica Armoury (L247) gives its own Void Shield rule.
   Built: the Collegia Titanica Armoury text. Question: are these the same rule?

5. **Weapon choices without a default (Warhound L377-389, Reaver L471-497)**: weapons are "chosen independently from the following list", no costs and no default.
   Built: each mount is a required, free choice; the first listed weapon is preselected (Warhound both arms: Turbo-laser Destructor; Reaver carapace: Turbo-laser Destructor, arms: Gatling Blaster). Both arms may take the same weapon. Question: is that correct (all choices free, duplicates allowed)?

6. **Saturnyne Lascutter (L599)** and **Incinerator Missile Bank (L621)**: Warlord options with no profile in the weapon table.
   Built: weapon entries with "?" for Range/S/AP and the note "No profile given in the army list". Question: what are their profiles and special rules?

7. **Warlord option names that differ from the weapon table (L583-623)**:
   - "Ardex-defensor Mauler Bolt Cannon Turrets" -> built as Defensor Bolt Cannon;
   - "Ardex-defensor Twin-linked Lascannon Turrets" -> Defensor Lascannon (its profile already says Twin-linked);
   - "Arioch Titan Power Claw" -> Arioch Power Claw;
   - "Titan Plasma Blastguns", "Reaver Laser Blasters / Melta Cannons / Gatling Blasters" -> Plasma Blastgun, Laser Blaster, Melta Cannon, Gatling Blaster;
   - "Vortex Missile Banks" -> Vortex Support Missile profile (one per bank, One Use);
   - "Two Twin-linked Vulcan Mega-bolters" -> a new entry "Twin-linked Vulcan Mega-bolter" (Vulcan Mega-bolter profile + Twin-linked).
   Question: are these all the same weapons? Is a Vortex Missile Bank really one Vortex Support Missile (One Use), or does a bank hold several?

8. **Warlord carapace pairs (L607-623)**: "Both carapace-mounted Apocalypse Missile Launchers may be replaced with one of the following pairs".
   Built: one required choice "Carapace-mounted weapons" (default: Two Apocalypse Missile Launchers); each pair costs its listed price once (not per weapon). Question: is the cost per pair (as built)?

9. **Warlord carapace minimum range (L639)**: the Warlord's carapace weapons may not target units within 24" (L639, Towering Monstrosity), while the Apocalypse Missile Launcher already has a 24" minimum range in its profile. Only rule text, no question unless you want a different interaction.

10. **Agile - "Primary Weapon" (L399)**: the Warhound may "fire one Primary Weapon and move D6"", but no Warhound weapon is called a Primary Weapon.
    Built: rule text as printed. Question: does "Primary Weapon" mean any one of its arm weapons?

11. **Three different "Towering Monstrosity" rules (L102-110, L512, Warlord rule box)**: the general Titan rule, the Reaver's and the Warlord's have different texts.
    Built: "Towering Monstrosity" (general, on every Titan), "Towering Monstrosity (Reaver)" and "Towering Monstrosity (Warlord)". The Warhound gets only the general rule and so has no minimum range. Question: is that intended (the Warhound has no listed minimum range and no Towering Monstrosity in its entry)?

12. **Weapon special rules not defined anywhere in this list or the core USR list**: Ordnance, Large Blast, Barrage, One Use, Sunder, Instant Death, Melee, Hellstorm.
    Built: printed in the weapon Type only (no rule link). Melta, Ignores Cover, Concussive, Armourbane, Twin-linked are linked to the core USRs. Question: should any of these get their own rule text (e.g. Sunder)?

13. **Legio / allegiance**: the book has no Legio choice, traits or allegiance restrictions.
    Built: the standard Allegiance configuration (Loyalist or Traitor, no effect). Question: are there Legio traits (e.g. Legio Mortis, Legio Ignatum) or other army-wide choices to add?

## Rules shown as text only (not enforced)

- Super-heavy Walker movement (12"), Massive Firepower, Titan Weapon Mounts / firing arcs, all minimum ranges (Reaver carapace 18", Warlord carapace 24").
- Towering Monstrosity (all three versions), Immense Machine, Reactor Meltdown, Void Shields, Reinforced Structure, World Burner, Agile.
- All weapon special rules (Apocalypse Missile Launcher, Inferno Gun, Plasma Blastgun profile choice, Vortex, Ardex-defensor, Reactor Overload, Titan Close Combat Weapons, Massive Blast, Apocalyptic Blast, Apocalyptic Barrage (X), Titan Killer, Machine Destroyer), Armoured Ceramite.
- Lords of War being permitted only by mission / agreement and any per-army Lords of War limit (the game system's Force Organisation chart controls the slot count).
