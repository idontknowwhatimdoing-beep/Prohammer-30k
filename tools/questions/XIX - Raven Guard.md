# XIX - Raven Guard: questions for the author

Source: `/home/claude/src/legions/XIX_Raven_Guard.txt`. Module: `tools/legions/xix_raven_guard.py`.

## Ambiguities / decisions

1. **Sniper Rifles for Independent Characters** (l.19: "Legion Reconnaissance Squads and Independent Characters may buy
   Sniper Rifles for 2 points instead of 5points or any price otherwise applicable.")
   Praetors/Centurions normally have no Sniper Rifle option at all. I read this as *granting* them the option: Sniper
   Rifle (2 pts) is added to their Armoury "Additional Wargear" (counts towards the 100-pt cap). Recon Squad Sniper Rifles
   (Recon Marines and Sergeant) now cost 2. Veteran Squads under Legion Recon Company still pay 5.
   Q: Should ICs get a Sniper Rifle option, and is it an additional weapon or a replacement (for what)?

2. **Legion Armoury items and the Armoury points caps** (l.49, 62, 68, 76, 87). Fulcrum Hand Cannon, Infravisor,
   Shroud Bombs, Cameleoline, Teleportation Transponders (IC) and the Sniper Rifle were put into the normal Space Marine
   Armoury of Praetors/Centurions (100-pt cap) and Sergeants (50-pt cap), so they count towards those caps.
   Q: Do Legion Armoury purchases count towards the Armoury caps, or are they on top?

3. **Fulcrum Hand Cannon: who is a "squad Sergeant with access to the Space Marine Armoury"** (l.49).
   I added it to every character model that has a Space Marine Armoury allowance and a Bolt Pistol (Sergeants, and also
   Command Squad Champion/Apothecary/Standard Bearer and Honour Guard Champion, Dark Fury Strike Leader, Mor Deythan
   Sergeant, Raptor Alpha). Destroyer Sergeants carry "Two Bolt Pistols" and did not get it.
   Q: Only true Sergeants, or any unit-upgrade character with Armoury access? May a Destroyer Sergeant replace one of
   his two Bolt Pistols?

4. **Infravisor for Terminator Sergeants** (l.62): added to every "Space Marine Armoury (max 50 pts)" group, including
   the Terminator-Sergeant armoury. Q: OK in Terminator Armour?

5. **Raven's Talons upgrade for Characters with a Pair of Lightning Claws (+5)** (l.43). Implemented wherever a Pair of
   Lightning Claws is chosen from a weapon list (IC/Sergeant armouries, Assault Sergeant). Where the pair is a squad
   "replace both" option (Bike/Sky Hunter Sergeants, Terminator models) it was not added.
   Also: Raven's Talons are a pair of *Rending* weapons, so upgrading from Lightning Claws (Power Weapons) for +5 is a
   downgrade. Q: Intended?

6. **Raven's Talons in the Veteran Squad** (l.41) replace Bolt Pistol *and* Chainsword. For Veterans this shares the
   per-model limit with the Chainsword swaps (a model can't take both). The Veteran models' fixed Bolt Pistol can't be
   removed per model in the builder (documentation only). For the Sergeant the Bolt Pistol is removed. A Sergeant that
   takes both Raven's Talons and a Fulcrum Hand Cannon (both replace the Bolt Pistol) is not blocked.

7. **Teleportation Transponders** (l.87): +15 added to Legion Terminator Squad, Legion Terminator Command Squad and
   Deliverer Terminator Squad (the units that are always entirely in Terminator Armour); +10 for Praetor/Centurion only
   while wearing Terminator Armour. Q: Any other unit (e.g. Contemptor/Leviathan are not "models wearing Terminator
   Armour")?

8. **Cameleoline for ICs** (l.76): available unless the IC wears Terminator Armour (ICs can't take Recon Armour).

9. **Dark Fury Assault Squad 0-1?** The unit's Force Organisation (l.343-344) shows only "Fast Attack" (no 0-1), but
   Agapito Nev (l.882) says "up to two Dark Fury Assault Squads rather than the normal 0-1".
   I made it 0-1 per Detachment, 0-2 if Agapito Nev is in the army. Q: Is the Dark Fury Assault Squad 0-1?

10. **Named characters replacing a Sergeant - cost** (Kaedes Nex l.720, Agapito Nev l.861, Sharrowkyn l.981: "Remove
    the normal Sergeant and include X for N points instead"). The Sergeant has no separate price (it is included in the
    squad's base cost), so I charged the full character price on top (+135 / +140 / +125) and removed the Sergeant.
    For comparison, Alpha Legion's Sheed Ranko (+62 = 110 - 48) subtracts the replaced model's cost.
    Q: Flat +N, or N minus the value of the Sergeant (e.g. Agapito +106 = 140 - 34)?

11. **Kaedes Nex unit type** (l.710-719): no unit type given. He carries a Jump Pack; I used "Jump Infantry
    (Character)". His Destroyer Squad may still buy Jump Packs for the whole squad (he already has one - does he pay for
    it?). The per-model Jump Pack / Krak / Melta costs currently count Nex as a model.

12. **"Dangerous Weaponry"** (l.735) is listed as a special rule of Kaedes Nex but no text is given. Shown as a
    placeholder. Q: What does it do?

13. **Branne Nev / Command Squad** (l.894-943): no retinue mentioned (Alvarex Maun explicitly gets a Command Squad).
    The general Master of the Legion rule says "may select a Legion Command Squad as a retinue where permitted", so I
    gave Branne Nev a Command Squad. Q: Correct?

14. **Branne Nev "Commander of the Survivors"** (l.938): implemented as a toggle on the Raptor Squad ("does not occupy
    an Elites choice"), visible only with Branne Nev in the army, once per army; it gives the Detachment +1 Elites slot.
    The Raptor Squad's 0-1 limit still applies. Q: Correct that the 0-1 limit is not lifted?

15. **Dark Fury as Praetor retinue** (l.391): offered in the Praetor's retinue choice, hidden unless the Praetor has a
    Jump Pack (error if chosen without one). Agapito Nev can be in any copy (root squad, Praetor retinue, Corax
    retinue), with an error if more than one Agapito is in the army.
    Q: Does a Dark Fury retinue count towards the Dark Fury 0-1 limit? (Currently: no.)

16. **Raptor Squad profile**: Strength 5 and Initiative 5 (l.576-595) are used as printed.

17. **Mor Deythan "Close-combat weapon"** (l.230) and Raptor wargear: modelled as "Close Combat Weapon" from the base
    list. No transport is given for Mor Deythan, Raptors or Dark Furies - none added. Q: Should Mor Deythan / Raptors
    have Dedicated Transport options?

18. **Mor Deythan heavy weapons** (l.252): "For every five models ... one Mor Deythan may replace his Sniper Rifle" -
    the Sergeant can't take them. The Sergeant's Sniper Rifle can take the combi-weapons (l.245 "Any model").

19. **Deliverer Chieftain / Deliverers heavy weapons** (l.520): "One Deliverer for every five models" - the Chieftain
    can't take them. "Land Raider" transport = Land Raider Phobos or Proteus.

20. **Deliverers "Pair of Raven's Talons +10"** (l.510) replaces the Power Weapon only (as printed), not the
    Combi-bolter.

21. **Corax - The Avenging Shadow** (l.1258): an optional 0-pt upgrade on Corax; it changes his save to 2+/4+ and adds
    Patchwork Panoply, Ghost of Istvaan (Shrouded instead of Stealth - the Stealth link stays on the entry, see rule
    text), Hater of Traitors (Hatred).

22. **Corax profile save** (l.1116: "1+"): shown as 1+/4+ because Primarch Armour grants a 4+ Invulnerable Save.

23. **Decapitation Strike - Fury From Above** (l.111): Drop Pod / Dreadclaw options appear in the Heavy Support Squad's
    transport choice with this Rite; an error is shown if the squad has neither. Q: "Legion Heavy Support Squads" only,
    or every Heavy Support choice?

24. **Liberation Force** (l.155-157): Loyalist-only is enforced (error if Traitor). "No units with Immobile or Slow and
    Purposeful" is enforced on every unit with those rules - this includes Legion Drop Pods and Dreadnought Drop Pods
    (Immobile). Q: Were Drop Pods meant to be excluded?

## Rules shown as text only (not enforced)

25. Surgical Strike, Rapid Reaction, Fatal Strike, Swooping Killers, Terran Veterans, Unstable Creation (joining
    restrictions), The Raven's Due, Executioner's Instinct, Master of Descent, Commander of the Talons (re-roll part),
    First Into the Fray, Hold Fast, Ghost in the Dark, Perfect Ambusher, Secret Deployment, Sire of the Raven Guard.
26. Decapitation Strike: no Fortification / no Allied Detachment from another Legion (no Fortifications or Allies in this
    catalogue). The "no more than one Consul" and "0-1 Heavy Support" limits ARE enforced.
27. Liberation Force: Imperialis Militia allies, no Fortification.
28. Limited Vehicles IS enforced (error when Heavy Support selections exceed Fast Attack selections; Dedicated
    Transports are not counted).
29. Shadow Masters IS enforced: Recon Squads lose Support Squad and count for the compulsory Troops (except under Rites
    that replace the compulsory Troops, e.g. Pride of the Legion - same as Tactical Squads).
