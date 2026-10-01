# XII - World Eaters: questions for the author

Source: `/home/claude/src/legions/XII_World_Eaters.txt` (line numbers below). Module: `tools/legions/xii_world_eaters.py`.

## Armoury

1. **Chainaxe - who is "eligible to carry a Close Combat Weapon"?** (L22 "Any World Eaters model eligible to carry a Close
   Combat Weapon may replace it with a Chainaxe for +4 points.")
   Done: every model carrying a Chainsword may swap it for a Chainaxe (+4): every choice that offers a Chainsword now also
   offers a Chainaxe (+4 on top of the Chainsword price), squads with fixed Chainswords get a "replace Chainsword with
   Chainaxe (any number)" block, characters with a fixed Chainsword get a replace slot. Not changed: the Tactical Squad's
   squad-wide "Chainswords" options, and the Techmarine's Servo-automata got it too.
   Question: is "Close Combat Weapon" meant as "Chainsword" (as done), or also the plain "Close Combat Weapon" item /
   Combat Blades? Should Servo-automata be excluded?
2. **Caedere Weapon profile.** L40-41 give "User +1, Rending"; the Rampager entry (L241) says "a Caedere Weapon counts as
   a Rending Weapon" (Rending Weapon = Strength User). Done: User +1, Rending everywhere. Question: which is right?
3. **Caedere Weapon - purchase or replacement?** (L34 "may purchase a Caedere Weapon for +15 points".) Done: an extra
   Armoury item (+15, counts towards the 100/50-point caps) for the Praetor, Centurion and every Sergeant/Champion 50-pt
   Armoury block (this also includes Terminator Sergeants). Question: should it replace a weapon (e.g. the Chainsword)?
   Should Terminator Sergeants have it?

## Rites of War

4. **Berserker Assault - "at least one compulsory Troops choice must be a Rampager Squad"** (L72). Done: Tactical,
   Breacher and Inductii Squads stop counting as compulsory Troops; Rampager Squads become Troops and count; an error is
   shown if the Detachment has no Rampager Squad. The builder cannot check that the Rampager is one of the two
   *compulsory* choices. OK?
5. **Weapons of the Pits** (L62, Chainaxe +2 per model in Assault / Rampager Squads). Done for Legion Assault Squad
   models and the Assault Sergeant. Rampagers already carry Chainaxes, so it does nothing for them. Is something else
   meant for Rampagers (e.g. their Champion)?
6. **Warlord weapon** (L73) is not checked (text only). **"No Fortification"** (L75, L113) is shown as an error when any
   Fortification is in the Detachment.
7. **The Crimson Path limitations** (L111-114). "No Immobile units": errors for Legion Drop Pods and Dreadnought Drop Pods
   (both have Immobile). Should Dreadclaws (Deep Strike, not Immobile) be allowed? "No Slow and Purposeful": no World
   Eaters unit has it, not checked. "No Allied Detachment from another Legion": cannot be checked (other catalogue).

## Units

8. **Rampager Squad** (L203-289): no Frag Grenades in the base wargear (only as +1/model option) - intended? The Champion
   has no chainaxe swap list of his own, only the 50-pt Armoury (done: his Bolt Pistol and Chainaxe can be exchanged from the
   Armoury). "Up to three Rampagers (six at ten models)" is a squad count (the Champion is not excluded by the builder).
9. **"Land Raider" as Dedicated Transport** (L289, L403, L583, L812, L937). Done like the base list: Power-Armour squads
   get the Land Raider Phobos, Terminator squads get Phobos or Proteus. Correct?
10. **Red Butcher Squad** (L340-403): no Frag/Krak Grenades or champion - intended? "0-1" (L367) done as 0-1 per Detachment.
11. **Red Hand Destroyer Mortalis Squad** (L478-583): the Sergeant has no Space Marine Armoury access (the base Destroyer
    Sergeant has) - intended? The "Missile Launcher with Suspensor Web and Rad Missiles" is listed as replacing "one Bolt
    pistol" (L543-548) - done as written. "For every five models" counts the Sergeant.
12. **Red Hand Destroyers and the Legion Destroyer Company Rite**: do Red Hand Squads count as Legion Destroyer Squads
    (Troops / compulsory Troops, Forbidden Arsenal second missile launcher)? Not done.
13. **Inductii Squad** (L592-675): the Sergeant "may replace his Chainaxe" (L668) but the wargear is a Chainsword (L645).
    Done: replaces the Chainsword (and may also take a Chainaxe via the Armoury rule). No Frag Grenades by default, no
    Armoury for the Sergeant - intended? The squad is compulsory-Troops eligible (no Support Squad rule) - correct?
14. **Devourer Terminator Squad** (L728-812) - no limit on how many; as Angron's retinue it takes no Elites slot. OK.
15. **Triarii Breacher Squad** (L861-937): spelled "Trarii" in the entry, "Triarii" at L933 and "Legion Trarii Breacher
    Squad" at L1371. Done: "Triarii Breacher Squad". L904 "The Rampager Champion is a Character" - done as the Triarii
    Champion. L922 "All Trarii Breacher may replace their Chainaxe" - done as ONE squad-wide exchange for all Breachers
    (not the Champion), paid per model. Should it be "any number"? The squad has no Hardened Armour / Breacher rules and may
    take a Rhino or Drop Pod although base Breachers may not (L937) - intended?

## Characters

16. **Khârn** (L998-1071): the Force Organisation line is empty in the header but "HQ" at L1039 - done as HQ, Master of the
    Legion, 1,500 points minimum. His Iron Halo counts towards the normal one-Iron-Halo-per-army limit - intended?
    Gorechild restriction (L1071): error if Khârn has Gorechild while mortal Angron keeps Gorefather & Gorechild.
17. **Shabran Darr** (L1078-1135): no "Master of the Legion" listed - done as not Master. He uses the Destroyer squads'
    "Dual Pistols" rule text.
18. **Gahlan Surlak** (L1140-1192) and **Kargos** (L1197-1255): the "Apothecary" special rule is not defined anywhere;
    done as "counts as an Apothecary". Surlak is a Legion Support Officer (not compulsory HQ); Kargos is not - correct?
    Neither is Master of the Legion.
19. **Captain Ehrlen** (L1276-1332): the Command Squad Jump Packs use the base Command Squad option (+15/model, whole squad,
    no transport) - same as the text.
20. **Delvarus** (L1339-1392): options say "Kargos may take" (L1390) - done as Delvarus. His Save is "3+" although he has a
    Boarding Shield (5+ Invulnerable) - should it read 3+/5+? Not Master of the Legion.

## Primarchs

21. **Angron** (L1417-1605): Save shown as 1+/4+ (Primarch Armour). Widowmaker exchange is free (L1592). No Allegiance
    restriction - correct?
22. **Angron, the Red Angel (Daemon Primarch)** (L1614-1790): same name as the mortal form - the builder entry is called
    "Angron, the Red Angel (Daemon Primarch)". No Allegiance is given; done as **Traitor only**. "Daemonic Armour" has no
    rule text - done as 2+/4+ from the profile. "Blades of the Red Angel" have no profile - done as User Strength, Power
    Weapon, Master-crafted. His profile does not list Legiones Astartes (World Eaters) - left out. Does the 2,000-point /
    Primarch's Chosen 1,500-point rule apply to him as to the mortal Angron (done: yes)?

## Rules shown as text only (not enforced)

Blood Frenzy; Rage after winning a combat; Headlong Assault; Blood Forward; Forlorn Hope; Unto Death; The Path Must End
in Blood; Ravening Madmen (including "never Scoring"); Nails-Broken; Destroyer Cadre joining limits (and Shabran Darr's
exception); The Bloody; Architect of the Nails; Warrior-Apothecary; Gladiator Champion; all Angron rules (The Red Angel,
Butcher's Nails, Sire of the World Eaters, The Nails Demand Blood); Daemon Angron's Blood Calls to Blood (never deployed,
summoning table), The Red Angel Descends, The Nails Sing (affects both armies), Daemonic Flight. Jump Packs do not
change the unit type shown in profiles.
