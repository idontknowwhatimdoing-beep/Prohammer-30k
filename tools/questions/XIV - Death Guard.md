# XIV - Death Guard: questions for the author

Source: `/home/claude/src/legions/XIV_Death_Guard.txt` (line numbers refer to that file).
Module: `tools/legions/xiv_death_guard.py`.

## Legion rules

1. **Footslogging Killers - which units count?** L18-19: "A Death Guard army may take only 0-1 selection in total from
   the following units: Land Speeder Squadron, Attack Bike Squadron, Bike Squadron."
   *Built:* an army-wide error when the roster holds more than one of Legion Land Speeder / Attack Bike / Bike
   Squadrons together. Sky Hunter Jetbike Squadrons, Javelins and Seekers are not limited.
   *Question:* Should Sky Hunter Jetbike Squadrons (and Javelin Squadrons) count towards the 0-1 as well?

2. **Rules shown only as text (not enforced):** Steady Assault / True Grit / Move Through Cover (L5-10), Resilience of
   Barbarus (L13-14). They are listed on the Legion entry; the builder does not add them to each Infantry unit.

## Armoury

3. **Manreaper - who may buy it.** L57: "Any Death Guard Sergeant or Character permitted to select weapons from the
   Space Marine Armoury may purchase a Manreaper."
   *Built:* +20 pts, counts towards the Armoury cap, in the Praetor/Centurion 100-pt Armoury and in every Sergeant /
   Champion 50-pt Armoury that offers weapons (Tactical Sergeant, Terminator Sergeant, Command/Terminator Command Squad
   specialists, Chem-master, Poison-master). Sergeants whose Armoury in this builder is wargear-only (e.g. Veteran,
   Destroyer, Heavy Support, Assault Sergeants) do not get it.
   *Question:* Is that the intended group? It is a purchase (an extra weapon), not a replacement - correct?
4. **Manreaper profile.** L58 only says "Two-Handed Power Weapon". *Built:* Range -, S User, AP -, Power Weapon,
   Two-Handed. *Question:* no Strength bonus intended?
5. **Alchem Flamer - which models.** L62: "A Death Guard model equipped with a Flamer or Heavy Flamer may replace it with
   an Alchem Flamer at no additional cost."
   *Built:* wherever a non-vehicle unit can choose a Flamer, Heavy Flamer or Heavy Flamer with Suspensor Web, an Alchem
   Flamer is offered for the same points (Tactical/Veteran/Seeker/Breacher specials, Terminator heavy weapons, Attack Bike
   heavy flamer, Bike Squadron flamers, Command Squads, Servo-automata ...). Vehicles and Dreadnoughts (hull, sponson,
   pintle and arm Heavy Flamers) do not get it. Combi-Alchem Flamer is offered wherever a Combi-flamer can be chosen
   (Combi-flamer price +4).
   *Question:* Should vehicles / Dreadnoughts / Attack Bikes be able to take Alchem Flamers too? A Heavy Flamer with
   Suspensor Web replaced this way loses the Suspensor Web - OK?

## Rites of War

6. **The Reaping - Superior Firepower** (L118-119). *Built:* with this Rite Legion Veteran Squads and Legion Heavy Support
   Squads become Troops choices that do NOT count as compulsory Troops. OK?
7. **The Reaping - Dark Arsenal** (L128 "Any Death Guard Character or Independent Character may purchase Rad Grenades
   for +10 points"). *Built:* every model with a "(Character)" unit type (Praetor, Centurion, named characters,
   Sergeants, Champions, Chem-master, Techmarines ...) gets a "Rad Grenades (The Reaping)" option (+10) that is only
   visible with this Rite; models that already have Rad Grenades and Primarchs are skipped.
   *Question:* Are Sergeants meant (they are Characters), or only Independent Characters? Does the Rad Grenade affect the
   whole unit (normal rule) - i.e. is buying it on one Sergeant enough?
8. **The Reaping - Deep Strike** (L135). *Built:* error if the Detachment contains a Legion Drop Pod, Dreadclaw or
   Dreadnought Drop Pod. Units that merely *can* Deep Strike are allowed (play restriction). Advance Moves / Flat Out
   (L133-134) and Implacable (L122-124) are text only.
9. **Creeping Death** (L166-169). *Built:* errors for a Loyalist army, for no Heavy Support Squad with a Siege Breaker
   Sergeant, and for a Fortification in the Detachment. Not enforced: "must be the Attacker" and "no Allied Detachment"
   (the builder cannot see Allied Detachments from inside the Detachment). All effects (L147-162) are text only.

## Units

10. **Deathshroud Terminators - size.** L218/249/269: 110 points for 2 models, "up to five additional ... +55 points per
    model". *Built:* 2-7 models, no Sergeant/Character. Cataphractii option sets the profile Save to 2+/4+ (L272-273).
11. **Deathshroud / Grave Warden transports - "Land Raider".** L281/L457. *Built:* Land Raider Phobos or Land Raider
    Proteus, Anvillus Dreadclaw Drop Pod, Legion Spartan Assault Tank. *Question:* both Land Raider patterns OK?
12. **Silent Retinue** (L243). *Built:* a Deathshroud Terminator Squad is added to the Legion Praetor's and Legion
    Centurion's retinue choice, visible only while the character wears any form of Terminator Armour (same condition as
    the Terminator Command Squad). Calas Typhon and Mortarion may also take it. *Question:* Should a character in Power
    Armour also be allowed Deathshroud?
13. **Grave Wardens.** L358-453. *Built:* 4-9 Grave Wardens (+50 each above 4) + 1 Chem-master; any model (including
    the Chem-master) may swap the Power fist for a Chainfist (+5); Chem-master: Grenade Harness (+10) and up to 50 pts
    from the Terminator column of the Armoury. "Shrouded in Death" (Defensive Grenades, L396) is text only (there is no
    Defensive Grenades item). *Question:* does the Chainfist option include the Chem-master ("Any model")?
14. **Mortus Poisoner Squad - no Dedicated Transport.** L520-606 list no Dedicated Transport (the Legion Destroyer Squad
    has Rhino / Drop Pod / Dreadclaw / Land Raider Phobos). *Built:* no normal transport; only the Rite-of-War transports
    (Orbital Assault / Armoured Spearhead) appear. *Question:* should they get the Destroyer Squad's transport list?
15. **Mortus Poisoners and Rites.** Should the Legion Destroyer Company Rite (Destroyers as Troops, extra Destroyer
    weapons) also apply to Mortus Poisoner Squads? *Built:* no.
16. **Mortus Phosphex Bombs** (L587). *Built:* one Phosphex Bomb (+10) per full five models in the squad (Poison-master
    counts towards the five). Poison-master: Chainsword swap (Rending +5 / Power weapon +10 / Power fist +15), Artificer
    Armour (+10), up to three Phosphex Bombs (+10 each), 50 pts of Armoury weapons and wargear.

## Characters

17. **Crysos Morturg and Nathaniel Garro are not Master of the Legion.** Their special-rules lists (L776-782,
    L996-998) do not include it, unlike Typhon, Rask and Grulgor. *Built:* not Master of the Legion (they cannot unlock
    a Rite of War). *Question:* intended?
18. **Morturg's psychic power** (L742 "one psychic power from the normal Legion Librarian Psychic Power list").
    *Built:* no selection in the builder - the base Legion Librarian has no power list either, so the power is picked
    at the table (rule text on Morturg). Master of Ambush and Destroyer Officer are text only (he is not given the
    Infiltrate rule). *Question:* should the builder offer a list of powers (which list / disciplines)?
19. **"Art of Destruction" name clash.** Durak Rask's rule (L826-827, Tank Hunters) has the same name as the Siege
    Breaker's rule in the Legiones Astartes list (+1 AP vs vehicles). *Built:* separate rule "Art of Destruction
    (Durak Rask)". *Question:* rename one of them?
20. **Typhon** (L651-709). *Built:* Traitor only, error below 1,500 points, Master of the Legion, retinue Deathshroud or
    Terminator Command Squad. Latent Psyker / Aura of Pestilence are text only.
21. **Allegiance** of Grulgor and Rask (Traitor), Morturg and Garro (Loyalist): error if the army has the other
    Allegiance.

## Primarch

22. **The Reaper's Advance** is described (L1258-1259) but not in Mortarion's Special Rules list (L1146-1151).
    *Built:* included. OK?
23. **Mortarion's retinue** (L1272-1275). *Built:* only a Deathshroud Terminator Squad (no Honour Guard / Terminator
    Command Squad).
24. **Mortarion's Allegiance.** None given. *Built:* both Allegiances allowed.
25. **Mortarion, Prince of Decay - Allegiance.** Not stated (L1370-1371). *Built:* Traitor only (as for the other Daemon
    Primarchs), never together with the mortal Mortarion, 2,000-point Primarch rule, Lord of War.
26. **"Daemonic Barbaran Plate"** (L1351) is not defined. *Built:* text: 2+ Armour Save and 4+ Invulnerable Save as in
    the profile ("2+/4++", L1335). *Question:* any further effect (e.g. Primarch Armour-like rules)?
27. **"Poison Resistance"** (L1360) is not defined anywhere. *Built:* placeholder text. *Question:* what does it do (Poison
    Cannot Kill Death? Resilience of Barbarus?)
28. **Daemon Lantern has no Armourbane** (L1456 vs L1238). *Built:* as printed (two different Lantern profiles).
    Intended?
29. **Prince of Decay has no Legiones Astartes (Death Guard) rule** in his list (L1354-1367). *Built:* as printed (he
    does not get it). OK?
30. **Sons of the Plague Father** (L1497-1504). *Built:* while Mortarion, Prince of Decay is in the roster, every unit
    whose models are all Infantry wearing Power Armour or Artificer Armour gets a "Plague Marines (entire unit)" option
    (+7 pts per model) that also raises the models' Toughness in the profile by 1. This covers Tactical, Veteran,
    Destroyer, Heavy Support, Seeker, Mortus Poisoner, Command and Honour Guard Squads. Not covered: Assault Squads (Jump
    Infantry), Breacher Siege Squads (Hardened Power Armour), Recon Squads, single characters (Praetor, Centurion, named
    characters - their armour is a choice). The "no Move Through Cover / 5\" charge" effects are text only.
    *Question:* Should Jump Infantry, Breachers (Hardened Power Armour) or Independent Characters be able to take it?
    Should an IC who joins a Plague Marine unit have to be upgraded too?

## Rules shown only as text (not enforced)

31. All in-game effects: Steady Assault, True Grit, Resilience of Barbarus, Manreaper attacks, Rite of War effects and
    play limitations (Advance, Flat Out, Attacker, Allied Detachment), Silent Retinue's "single HQ selection", Shrouded
    in Death, Destroyer Cadre / Destroyer Officer joining limits, Latent Psyker, Aura of Pestilence, Master of Ambush,
    Art of Destruction, The Eater of Lives, Libertas, Aquila Imperator, all Mortarion and Prince of Decay rules
    (Witch-Spite, Toxic Miasma, Poison Cannot Kill Death, Burdened Wings incl. "may never join / be joined", The Reaper's
    Miasma, Reluctant Sorcerer and his three powers), Plague Marine movement/charge limits.

## Additional

32. **Prince of Decay and the universal Primarch rules.** L1354-1367 do not list "Primarch"; the Daemon Primarchs rule
    says he "uses only its own rules, but counts as a Primarch". *Built:* Lord of War, Primarch category (one Primarch
    per army, 2,000-point check, Primarch's Chosen interaction), but none of the universal Primarch rules (Sire of the
    Legion, Clash of Demigods, Price of Failure, Transports...) are linked. *Question:* should those apply to him?
