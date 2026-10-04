"""Daemons of the Ruinstorm (Age of Darkness army list for ProHammer Classic).

Source: /home/claude/src/v4/Daemons_of_the_Ruinstorm.txt
Questions: tools/questions/Daemons of the Ruinstorm.md
"""
from armies.common import *  # noqa: F401,F403
from armies.common import (k, unit, model, upgrade, unique, config, allegiance, error_if, catalogue, start,
                           register_data, LOW, COMMANDER, LINE)
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
from legiones import W, has, lacks, gear, rules_links, unit_profile, psychic_powers
import psychic_powers as PSY
from legiones2 import take, pool, choice, add_mods, add_to, model_swaps, TROOPS, ELITES, FA, HQ, HS

ARMY = "Daemons of the Ruinstorm"

# ======================================================================= rules
MV_TEXT = ("Manifestation Value determines the earliest Battle Round in which the unit may first enter play from "
           "Reserve and how much Manifestation Capacity it uses when it Manifests through a Warp Portal (see The Veil "
           "Thins and Manifestation Capacity). Battle Round 1: MV 1 only, special Reserve roll of 4+. Battle Round 2: "
           "MV 1-2, normal Reserve rolls. Battle Round 3+: all MVs. A unit with models of different MVs uses the highest. "
           "MV 1 = typically Lesser Daemons, Swarms, Beasts; MV 2 = Cavalry, Brutes, Chosen, Shrikes, Greater Daemon "
           "Beasts; MV 3 = Greater Daemons, Daemon Lords, Behemoths, Arch-Daemons.")

RULES = {
    # ---------------------------------------------------------------- army
    "Daemons of the Ruinstorm": (
        "Army list for the Daemonic hosts of the Ruinstorm (ProHammer Classic). FORCE ORGANISATION: HQ 1-2, Troops 2-6, "
        "Elites 0-3, Fast Attack 0-3, Heavy Support 0-3; at least 1 HQ and 2 Troops are compulsory. Units with the "
        "Support Unit rule occupy their slot but may not fill a compulsory selection. Lords of War and Fortifications are "
        "not part of the chart: they may only be included where the mission permits or both players agree, and no army "
        "may contain more than one Lord of War selection. Daemons do not normally construct Fortifications; Warp Portals "
        "are not Fortifications. ALLEGIANCE: Traitor; a Ruinstorm Detachment may not normally be included in a Loyalist "
        "army (missions/campaigns may override this). MULTIPLE DETACHMENTS: each Detachment fulfils its own compulsory "
        "selections, selects its own Aetheric Dominion and generates its own Warp Portals; rules of one Detachment do not "
        "affect another unless stated. ALTERNATIVE FORCE ORGANISATION: unit entries or special rules may change a unit's "
        "battlefield role, let it be taken without a slot, stop it filling a compulsory slot or change slot numbers; these "
        "are not Formations."),
    "The Army's Warlord": (
        "One eligible Character in the Primary Detachment must be nominated as Warlord. If the Primary Detachment "
        "contains a Ruinstorm Daemon Lord, it must be the Warlord; otherwise another eligible HQ Character may be chosen "
        "normally. A Ruinstorm Daemon Lord may not be selected in a Ruinstorm Allied Detachment. The Warlord selects a "
        "Warlord Trait using the normal ProHammer Classic rules."),
    "Allied Forces (Ruinstorm)": (
        "A Daemons of the Ruinstorm army may use Allied Detachments normally; an Allied Detachment may not fulfil the "
        "compulsory selections of the Primary Detachment. Unless stated otherwise: Aetheric Dominion rules only affect "
        "models of the Ruinstorm Detachment; allied models gain no Dominions, Emanations or Manifestation Values and may "
        "not Manifest through Ruinstorm Warp Portals; rules of an Allied Detachment do not affect Ruinstorm Daemons and "
        "vice versa; Independent Characters from another Detachment may not join Daemon units of a Ruinstorm Detachment "
        "and Ruinstorm Daemon Independent Characters may not join units of another Detachment; the Allegiance of any "
        "Allied Detachment must be compatible with the Traitor Allegiance."),
    "Ruinstorm Allied Detachment": (
        "A Traitor army may include a Daemons of the Ruinstorm Allied Detachment: HQ 1 (compulsory), Troops 1-2 (1 "
        "compulsory), Elites 0-1, Fast Attack 0-1, Heavy Support 0-1. It may not include a Ruinstorm Daemon Lord, a Lord "
        "of War or a Fortification. Support Units may not fulfil the compulsory Troops selection. It selects an Aetheric "
        "Dominion normally and receives one Warp Portal for every full 750 points spent on the Allied Detachment itself "
        "(points of the Primary Detachment do not count)."),
    "Malefic Daemonology and Summoned Daemons": (
        "Daemons summoned through Malefic Daemonology are not selected from this list; use the Chaos Daemons army list. "
        "They are not part of a Ruinstorm Detachment and gain no Aetheric Dominion, Favoured Archetype status, "
        "Emanations, Daemonic Forms, Greater Manifestations, Manifestation Value or access to Ruinstorm Warp Portals."),
    "Daemonic Archetypes": (
        "Units represent broad categories of Daemonic entity and may be modelled in any appropriate form. A unit's entry "
        "determines its characteristics, unit type, Manifestation Value, wargear, available Emanations, Daemonic Forms, "
        "Daemonic Weapons and special rules; appearance does not alter its rules. Daemons use the normal ProHammer Classic "
        "unit type rules. Models with the Daemon special rule possess the Invulnerable Save and Fear rules. Daemons do "
        "not automatically possess Deep Strike unless their unit type, Daemonic Form or another rule grants it."),
    # ------------------------------------------------------------ general
    "Daemonic Instability": (
        "Whenever a unit with Daemonic Instability would normally take a Morale, Break or Pinning test, it instead takes "
        "a Daemonic Instability test: roll 2D6 against the unit's Leadership, applying any modifiers that would have "
        "applied to the replaced test. If passed, no effect. If failed, the unit suffers one Wound for each point by "
        "which the test was failed; these Wounds allow no Armour, Cover or Invulnerable Saves and may not be ignored by "
        "Feel No Pain. The unit does not Fall Back, become Broken or become Pinned as a result. If the unit contains "
        "models with different Leadership, use the highest Leadership normally available to the unit."),
    "Manifestation Value 1": "Manifestation Value 1. " + MV_TEXT,
    "Manifestation Value 2": "Manifestation Value 2. " + MV_TEXT,
    "Manifestation Value 3": "Manifestation Value 3. " + MV_TEXT,
    "Aetheric Dominion": (
        "Every Daemons of the Ruinstorm Detachment must select one Aetheric Dominion when the army is chosen. Unless "
        "otherwise stated every model with the Daemon special rule in that Detachment possesses the rules of the chosen "
        "Dominion, and the same Dominion is used by every unit in the Detachment. Ruinstorm Possessed and other units "
        "stated not to possess an Aetheric Dominion receive no benefit from it."),
    "Favoured Archetype": (
        "Each Aetheric Dominion lists Favoured Archetypes. A Favoured unit may select Dominion Emanations where "
        "permitted, benefits from rules that affect Favoured Archetypes and gains special deployment or Manifestation "
        "options where specifically stated. Being Favoured does not by itself grant Deep Strike, Infiltrate, Outflank or "
        "any other deployment rule. Daemon Characters and Daemon Lords always count as Favoured Archetypes for their "
        "chosen Dominion."),
    "Support Unit": (
        "A Support Unit occupies its normal Force Organisation choice but may not be used to fulfil a compulsory "
        "selection of that type."),
    "Daemonic Emanations": (
        "A unit entry states how many Emanations the unit or model may select. Each Emanation counts as one selection "
        "and may not be selected more than once. If a unit of more than one model selects an Emanation, every model "
        "purchases it; the listed cost is paid per model using the unit's Emanation Cost Class (Lesser: Lesser Daemons, "
        "Daemon Swarms, Daemon Cavalry; Greater: Daemon Beasts, Daemon Brutes, Daemon Chosen; Monstrous: Daemon Shrikes, "
        "Greater Daemon Beasts, Greater Daemons, Daemon Lords, Daemon Behemoths, Arch-Daemons). Models which later join "
        "another unit and Retinues purchase their Emanations separately. General Emanations may be selected by any unit "
        "whose entry allows it; Dominion Emanations only by Favoured Archetypes of the appropriate Dominion and they count "
        "towards the normal maximum number of Emanations."),
    "Daemonic Forms": (
        "Where a unit entry permits it a model may purchase a Daemonic Form. A model may normally possess only one Form; "
        "Forms do not count towards the maximum number of Emanations. A Form changes the model's Unit Type and the model "
        "gains all rules of its new Unit Type; it does not alter characteristics unless stated."),
    "Greater Manifestations": (
        "Each Aetheric Dominion includes one Greater Manifestation. Only models listed as eligible receive it, and only "
        "that of their own Dominion, automatically and at no points cost. It does not count towards the maximum number "
        "of Emanations and a model may never possess more than one Greater Manifestation."),
    "Daemonic Weapons": (
        "Daemonic Melee Weapons: a model may normally select only one; it replaces the Close Combat Weapon. Daemonic "
        "Ranged Weapons: a model may normally select only one; it does not replace the Close Combat Weapon. If a unit of "
        "more than one model selects a Daemonic Weapon, every model takes the same weapon and pays the cost (per model, "
        "using the Emanation Cost Class). Daemon Swarms and Ruinstorm Possessed may not select Daemonic Weapons. Weapon "
        "names are descriptive only. Monstrous Creatures already treat their normal close combat attacks as Power Weapon "
        "attacks, so a Monstrous cost class model may not select a Warp Blade."),
    "Armour Save -1": ("Warp Maul: the armour save of a model wounded by this weapon is worsened by 1 (e.g. a 3+ "
                       "save becomes 4+)."),
    "Crushing": ("Attacks made with this weapon are always resolved at Initiative 1. This applies even if the bearer is "
                 "a Monstrous Creature."),
    # ------------------------------------------------------- warp portals
    "Warp Portals": (
        "Warp Portals are optional. A Ruinstorm Detachment receives 1 Warp Portal for every full 750 points spent on "
        "models of that Detachment (0-749: 0, 750-1,499: 1, 1,500-2,249: 2, 2,250-2,999: 3, 3,000-3,749: 4); points of "
        "another Detachment do not count. Portals cost no points, use no Force Organisation slot, are not Fortifications "
        "and belong only to the Detachment that generated them. THE PORTAL: a 60mm round base (its entire rules "
        "footprint); stationary, Impassable Terrain, does not block line of sight or give cover by itself, cannot control "
        "or contest Objectives, cannot normally be targeted, attacked or destroyed; models may move into base contact but "
        "not onto or across it. PLACING: after both armies have deployed but before Infiltrators deploy and before Scout "
        "moves; entirely on the battlefield, more than 18\" from the enemy Deployment Zone, more than 12\" from any enemy "
        "model and from another Portal, not in Impassable Terrain. Distances are measured to the edge of its base. If both "
        "players have Portals, roll off and alternate placing them, winner first."),
    "Aetheric Reserves": (
        "Any unit of a Ruinstorm Detachment with a Manifestation Value may always be placed in Reserve and counts as "
        "having a special Reserve rule for how much of the army may start in Reserve. It is not assigned to a Portal; when "
        "eligible it may Manifest through an active Warp Portal, enter from its own table edge, Deep Strike or Outflank if "
        "it has those rules, or use any other Reserve method granted to it. All Ruinstorm Daemons remain subject to their "
        "Manifestation Value whatever method they use."),
    "The Veil Thins": (
        "Battle Round 1: MV 1 units only, special Reserve roll of 4+. Battle Round 2: MV 1-2, normal Reserve roll. Battle "
        "Round 3+: all MVs, normal Reserve roll. A unit may not enter play before its MV permits, even with Deep Strike, "
        "Outflank or another Reserve rule, unless a rule explicitly allows it to Manifest earlier. Units with mixed MVs use "
        "the highest. MV only restricts a unit's first arrival; a unit later entering Ongoing Reserves is not restricted "
        "again."),
    "Manifestation Capacity": (
        "Each active Warp Portal has a Manifestation Capacity of 3 in each friendly Movement Phase, tracked separately per "
        "Portal; unused Capacity is lost. A unit Manifesting consumes Capacity equal to its Manifestation Value (the "
        "highest in the unit; the number of models does not matter) and may not use a Portal without sufficient Capacity "
        "left. MANIFESTING: choose an active Portal with sufficient Capacity, place one model in base contact with the "
        "Portal and the rest in coherency, none within 1\" of an enemy, in Impassable Terrain, on the Portal or off the "
        "battlefield; the unit does not scatter. If the whole unit cannot be placed it may not use that Portal (use "
        "another Portal or Reserve method, or remain in Reserve). A unit that Manifests counts as having moved, may not "
        "make a further Normal Move or Advance, may shoot and use Psychic Powers normally, but may not charge unless a "
        "rule states otherwise. Manifesting counts as entering play from Reserves for all rules (e.g. Interceptor)."),
    "Sealing a Warp Portal": (
        "At the start of its Movement Phase an enemy Psyker in base contact with an active Portal may attempt to Seal the "
        "Rift: it forgoes all other Psychic Powers that player turn and takes a Psychic Test; if passed the Portal is "
        "Sealed (Perils resolved normally). A model with Psychic Anathema may attempt it with a Leadership test instead "
        "and does not suffer Perils. A Sealed Portal remains on the battlefield as Impassable Terrain (60mm footprint) but "
        "cannot be used, provides no Capacity and cannot normally be reopened. Sealing awards no Victory Points unless "
        "the mission states otherwise. IF THE RIFTS ARE CLOSED: if a Detachment began the battle with one or more Portals "
        "and all have been Sealed, from that Detachment's next player turn all of its Ruinstorm Daemon units still in "
        "Reserve gain Outflank for entering play (MV restrictions still apply; units with another legal method may use "
        "it). This does not apply to a Detachment that began with no Portals."),
    # ------------------------------------------------------ unit rules
    "Lord of the Ruinstorm": (
        "If the Primary Detachment contains a Ruinstorm Daemon Lord, that model must be selected as the army's Warlord, "
        "unless another rule specifically requires a different model to be the Warlord. A Ruinstorm Daemon Lord may not "
        "be selected as part of a Ruinstorm Allied Detachment. Ka'Bandha (Lord of Murder) takes precedence: an army "
        "including Ka'Bandha may not include a Ruinstorm Daemon Lord (author's ruling)."),
    "Shepherd of Malign Intent": (
        "Before deployment, nominate one enemy category: Infantry, Jump Infantry, Bikes and Cavalry, or Monstrous "
        "Creatures. The Daemon Chosen and any Daemon unit it joins may re-roll natural To Hit rolls of 1 in close combat "
        "against models of the nominated type."),
    "Daemon Brute Retinue": (
        "A single unit of Ruinstorm Daemon Brutes may be taken as a Retinue for a Ruinstorm Daemon Lord. It does not occupy "
        "an Elites choice, is selected and paid for normally, forms a single unit with the Daemon Lord at the start of the "
        "battle and may not voluntarily leave the Daemon Lord. A Daemon Lord with the Winged Daemonic Form may not select a "
        "Daemon Brute Retinue. The Retinue purchases its Emanations separately from the Lord. The unit uses the highest "
        "Manifestation Value in it (3)."),
    "Slaves to Darkness": (
        "Ruinstorm Possessed are mortal vessels: they do not have the Daemon or Daemonic Instability rules, do not possess "
        "an Aetheric Dominion and cannot select Emanations, do not use Manifestation or Warp Portals and deploy normally. "
        "Independent Characters may not join a Ruinstorm Possessed unit. Ruinstorm Possessed may not control or contest "
        "Objectives. Support Unit: may not fulfil any compulsory Troops selection."),
    "Unstoppable": (
        "If an attack would inflict Instant Death upon this model, it instead inflicts D3 Wounds. Any effect which would "
        "otherwise remove the model from play outright without inflicting Wounds instead inflicts D3 Wounds. Saves and "
        "other methods of preventing Wounds are resolved normally unless the original attack or effect states otherwise."),
    "Apex Manifestation": (
        "An Arch-Daemon always counts as Favoured for its Aetheric Dominion (it may select Dominion Emanations normally) "
        "and always counts as an eligible model for the Greater Manifestation of its chosen Dominion, regardless of the "
        "Archetypes normally listed. It gains it automatically at no points cost and it does not count towards its maximum "
        "number of Emanations."),
    # -------------------------------------------------- named characters
    "Preferred Enemy (Characters)": "The model has the Preferred Enemy special rule against models with the Character type.",
    "Preferred Enemy (Sanguinius)": "The model has the Preferred Enemy special rule against Sanguinius.",
    "Feel No Pain (5+)": "The model has the Feel No Pain special rule with a 5+ roll.",
    "Feel No Pain (6+)": "The model has the Feel No Pain special rule with a 6+ roll.",
    "Born of Murder": (
        "Whenever a model with the Character type is slain while Samus is in Reserve, place a marker where it was "
        "removed. When Samus next becomes available from Reserve, he may instead enter play by Deep Strike with the centre "
        "of his base over one of these markers; he does not scatter. Remove the marker after Samus has entered play. Born "
        "of Murder does not allow Samus to enter play before his Manifestation Value permits."),
    "Samus (Aetheric Dominion)": (
        "Samus may only be selected in a Ruinstorm Detachment using the Suffocating Dread Aetheric Dominion. He possesses "
        "all Core Dominion Rules of Suffocating Dread, always counts as a Favoured Archetype, possesses the Dread Visage "
        "Dominion Emanation at no additional cost and does not receive the Avatar of Despair Greater Manifestation. Samus "
        "is selected as a Lord of War and is Unique."),
    "Psyker (Kyriss the Perverse)": (
        "Psyker (Mastery Level 2). Kyriss knows the Telepathy powers Dominate and Hallucination (ProHammer Classic) and may "
        "not exchange them or select powers from another Psychic Discipline."),
    "Kyriss (Aetheric Dominion)": (
        "Kyriss may only be selected in a Ruinstorm Detachment using the Lurid Onslaught Aetheric Dominion. Kyriss "
        "possesses all Core Dominion Rules of Lurid Onslaught, always counts as a Favoured Archetype, possesses the "
        "Quicksilver Grace and Transfixing Presence Dominion Emanations at no additional cost and does not receive the "
        "Flickering Gait Greater Manifestation. Kyriss is selected as a Lord of War and is Unique."),
    "Psyker (Cor'bax Utterblight)": (
        "Psyker (Mastery Level 2). Cor'bax may select two powers from the Biomancy Psychic Discipline (ProHammer Classic) "
        "and may not select powers from any other Psychic Discipline."),
    "Noisome Tide of Flesh": (
        "Cor'bax automatically passes Dangerous Terrain tests. When Cor'bax charges he inflicts D3 Hammer of Wrath attacks "
        "instead of one. When Cor'bax is destroyed, before removing the model centre the Large Blast marker over his base: "
        "every non-Daemon model touched suffers a Strength 4 AP4 hit with Poison (4+); models with the Daemon rule are "
        "unaffected. Then remove Cor'bax."),
    "Cor'bax (Aetheric Dominion)": (
        "Cor'bax may only be selected in a Ruinstorm Detachment using the Creeping Scourge Aetheric Dominion. He possesses "
        "all Core Dominion Rules of Creeping Scourge, always counts as a Favoured Archetype, possesses the Miasma of "
        "Feebleness Dominion Emanation (renamed from Miasma of Decay) and the Crushing Limbs General Emanation at no additional cost and does not receive the "
        "Pestilent Monolith Greater Manifestation. Cor'bax is selected as a Lord of War and is Unique."),
    "Psyker (Madail the Undivided)": (
        "Psyker (Mastery Level 3). Madail knows the Telepathy powers Psychic Shriek, Hallucination and Invisibility "
        "(ProHammer Classic) and may not exchange them or select powers from another Psychic Discipline."),
    "The Undivided": (
        "Madail may be selected in a Ruinstorm Detachment using any Aetheric Dominion. He possesses the Core Dominion "
        "Rules of that Dominion, always counts as a Favoured Archetype, does not receive its Greater Manifestation and "
        "possesses the Horned Crown General Emanation at no additional cost. Madail is selected as a Lord of War and is "
        "Unique."),
    "Lord of Murder": ("If Ka'Bandha is included in the army's Primary Detachment, it must be the army's Warlord. "
                      "Ka'Bandha takes precedence over a Ruinstorm Daemon Lord: an army including Ka'Bandha may not "
                      "include a Ruinstorm Daemon Lord (author's ruling)."),
    "Miasma of Rage": (
        "Ka'Bandha and all friendly Crimson Fury Daemon units within 12\" gain Rage (6th-7th Edition). A model which "
        "already possesses Rage also gains the Rampage special rule while it remains within 12\" of Ka'Bandha."),
    "Scythe of Hatred": (
        "At the end of any Assault phase in which Ka'Bandha inflicted one or more unsaved Wounds with close combat attacks, "
        "nominate one enemy unit within 6\": it suffers a number of automatic Strength 6 AP- hits equal to the unsaved "
        "Wounds Ka'Bandha inflicted in close combat that phase. These Wounds do not count towards Combat Resolution."),
    "Eternal Rivalry": (
        "If the opposing army includes Sanguinius, Ka'Bandha gains Preferred Enemy (Sanguinius). Sanguinius also gains "
        "Preferred Enemy (Ka'Bandha)."),
    "Ka'Bandha (Aetheric Dominion)": (
        "Ka'Bandha may only be selected in a Ruinstorm Detachment using the Crimson Fury Aetheric Dominion. It possesses "
        "all Core Dominion Rules of Crimson Fury, always counts as a Favoured Archetype, possesses the Molten Blood and "
        "Horned Crown General Emanations at no additional cost and does not receive the Avatar of Slaughter Greater "
        "Manifestation. Ka'Bandha is selected as a Lord of War and is Unique."),
    # ------------------------------------------------- Aetheric Dominions
    "Crimson Fury": (
        "Daemons of rage and slaughter. CORE DOMINION RULES: Fury Incarnate, Unending Slaughter. FAVOURED ARCHETYPES: "
        "Lesser Daemons, Daemon Beasts (and Greater Daemon Beasts), Daemon Cavalry, Daemon Brutes (plus all Daemon "
        "Characters and Daemon Lords). GREATER MANIFESTATION: Avatar of Slaughter (Greater Daemons and Daemon Behemoths). "
        "DOMINION EMANATIONS: Blood Frenzy, Reaping Blows, Brass-bound Rage."),
    "Fury Incarnate": "Models with this Dominion have the Furious Charge special rule.",
    "Unending Slaughter": ("Units with this Dominion may re-roll their Sweeping Advance roll. If able to pursue a "
                           "defeated enemy, they must do so."),
    "Creeping Scourge": (
        "Decay made manifest. CORE DOMINION RULES: Unnatural Resilience, Miasma of Decay. FAVOURED ARCHETYPES: Lesser "
        "Daemons, Daemon Swarms, Daemon Brutes, Daemon Behemoths (plus all Daemon Characters and Daemon Lords). GREATER "
        "MANIFESTATION: Pestilent Monolith (Greater Daemons and Daemon Behemoths). DOMINION EMANATIONS: Corpulent Horror, "
        "Pestilent Touch, Miasma of Feebleness."),
    "Unnatural Resilience": ("Models with this Dominion have Feel No Pain (6+). If a model already possesses a better Feel "
                             "No Pain save, use the better value."),
    "Miasma of Decay": ("Enemy models in base contact with one or more models with this Dominion suffer -1 Initiative, "
                        "to a minimum of 1."),
    "Maddening Swarms": (
        "Impossible change, fractured possibility and sorcerous power. CORE DOMINION RULES: Born of Sorcery, Flickering "
        "Reality. FAVOURED ARCHETYPES: Lesser Daemons, Daemon Swarms, Daemon Beasts (and Greater Daemon Beasts), Greater "
        "Daemons (plus all Daemon Characters and Daemon Lords). GREATER MANIFESTATION: Oracle of Chaos (Greater Daemons "
        "only). DOMINION EMANATIONS: Sorcerous Conduit, Iridescent Form, Fate-touched."),
    "Born of Sorcery": ("Psykers with this Dominion may re-roll one failed Psychic Test per player turn. The second result "
                        "must be accepted."),
    "Flickering Reality": ("Models with this Dominion may re-roll Invulnerable Save rolls of 1. A unit with this Dominion "
                           "which already possesses Deep Strike may also re-roll the distance rolled for Scatter when "
                           "arriving by Deep Strike. The second result must be accepted."),
    "Lurid Onslaught": (
        "Obsession, excess and predatory desire. CORE DOMINION RULES: Preternatural Grace, Unnatural Swiftness. FAVOURED "
        "ARCHETYPES: Lesser Daemons, Daemon Beasts (and Greater Daemon Beasts), Daemon Cavalry, Daemon Chosen (plus all "
        "Daemon Characters and Daemon Lords). GREATER MANIFESTATION: Flickering Gait (Greater Daemons and Daemon "
        "Behemoths). DOMINION EMANATIONS: Quicksilver Grace, Transfixing Presence, Impossible Perfection."),
    "Preternatural Grace": "Models with this Dominion have Fleet.",
    "Unnatural Swiftness": ("When a unit with this Dominion Runs, roll 2D6 and use the highest result for the distance "
                            "moved. A unit with this Dominion which already possesses Outflank may re-roll the result used "
                            "to determine which table edge it enters from. The second result must be accepted."),
    "Mirror of Hatred": (
        "Spite given independent existence. CORE DOMINION RULES: Spite Incarnate, Refusal of the Warp. FAVOURED "
        "ARCHETYPES: Daemon Brutes, Daemon Chosen, Greater Daemons, Daemon Behemoths (plus all Daemon Characters and "
        "Daemon Lords). GREATER MANIFESTATION: Inimitable Recursion (Greater Daemons only). DOMINION EMANATIONS: Anathema "
        "Aura, Reflected Malice, Soul-rending Hatred."),
    "Spite Incarnate": "Models with this Dominion have Hatred (Psykers) and Hatred (Daemons).",
    "Refusal of the Warp": ("Units with this Dominion may re-roll failed attempts to resist Psychic Powers which directly "
                            "affect them. A Psyker suffering an unsaved wound from a model with this Dominion in close "
                            "combat suffers -1 Leadership until the end of the following player turn."),
    "Suffocating Dread": (
        "Mortal terror, despair and the certainty of death. CORE DOMINION RULES: Pall of Terror, Unreasoning Horror. "
        "FAVOURED ARCHETYPES: Lesser Daemons, Daemon Swarms, Daemon Beasts (and Greater Daemon Beasts), Daemon Cavalry, "
        "Greater Daemons (plus all Daemon Characters and Daemon Lords). GREATER MANIFESTATION: Avatar of Despair (Greater "
        "Daemons and Daemon Behemoths). DOMINION EMANATIONS: Dread Visage, Oppressive Presence, Soul-chilling Howl."),
    "Pall of Terror": ("Enemy units within 12\" of one or more models with this Dominion suffer -1 Leadership; enemy units "
                       "within 6\" instead suffer -2 Leadership. These penalties are not cumulative with themselves."),
    "Unreasoning Horror": (
        "Enemy Infantry, Jump Infantry, Bikes and Cavalry within 6\" of one or more models with this Dominion suffer -1 "
        "Ballistic Skill when shooting at a unit with this Dominion, even if Fearless, automatically passing Morale tests "
        "or otherwise ignoring Leadership-based effects. Vehicles, Daemons and models explicitly mindless or immune to "
        "psychological effects are unaffected."),
    # ---------------------------------------------- Greater Manifestations
    "Avatar of Slaughter": (
        "Crimson Fury Greater Manifestation (Greater Daemons and Daemon Behemoths only). Friendly Crimson Fury units within "
        "6\" of the model gain +1 to their Combat Resolution. Whenever the model destroys an enemy model in close combat it "
        "gains one additional Attack for the remainder of that Assault phase, to a maximum of +3 Attacks."),
    "Pestilent Monolith": (
        "Creeping Scourge Greater Manifestation (Greater Daemons and Daemon Behemoths only). The model improves its Feel No "
        "Pain save by one step. Non-Daemon enemy units within 6\" suffer -1 Toughness for the purpose of resolving Poisoned "
        "attacks only (not for Instant Death or other effects)."),
    "Oracle of Chaos": (
        "Maddening Swarms Greater Manifestation (Greater Daemons only). While this model is on the battlefield the "
        "controlling player may re-roll Reserve rolls for friendly Daemon units and may re-roll the result used to "
        "determine the table edge from which a friendly Outflanking Daemon unit enters. The second result must be "
        "accepted."),
    "Flickering Gait": (
        "Lurid Onslaught Greater Manifestation (Greater Daemons and Daemon Behemoths only). Friendly Lurid Onslaught units "
        "within 6\" always count their Run roll as at least 4\", add +1\" to their charge movement and may re-roll "
        "Sweeping Advance rolls."),
    "Inimitable Recursion": (
        "Mirror of Hatred Greater Manifestation (Greater Daemons only). When the model loses its last Wound roll a D6: on a "
        "6 remove it from play instead of treating it as destroyed and place it into Ongoing Reserves with D3 Wounds "
        "restored; otherwise it is destroyed normally. A model may only successfully return in this manner once per "
        "battle."),
    "Avatar of Despair": (
        "Suffocating Dread Greater Manifestation (Greater Daemons and Daemon Behemoths only). The model's Pall of Terror "
        "ranges increase to 18\" (-1 Leadership) and 9\" (-2 Leadership). Fearless living units within 9\" remain immune "
        "to Morale and Pinning tests but suffer -1 Weapon Skill and -1 Ballistic Skill while within the aura."),
    # --------------------------------------------------- General Emanations
    "Warp-scaled Hide": "The model gains a 3+ Armour Save. This does not replace or modify its Invulnerable Save.",
    "Sundering Fangs": ("The model's normal close combat attacks gain Rending. This does not confer Rending upon attacks "
                        "made with another special melee weapon unless that weapon already possesses the rule."),
    "Flensing Talons": "The model may re-roll To Wound rolls of 1 in close combat.",
    "Crushing Limbs": ("The model gains +2 Strength when making its normal close combat attacks. When using this "
                       "Emanation, the model suffers -2 Initiative, to a minimum of 1."),
    "Horned Crown": ("Daemon Characters only. The model gains +1 Leadership, to a maximum of 10. If the model already has "
                     "Leadership 10, friendly Daemon units within 6\" may use its Leadership when taking Daemonic "
                     "Instability tests."),
    "Molten Blood": ("Whenever the model suffers an unsaved Wound in close combat, the enemy unit which inflicted the Wound "
                     "suffers one Strength 4 hit. Wounds caused by Molten Blood do not count towards Combat Resolution."),
    "Shroud of Darkness": ("The model gains Stealth. If the model already possesses Stealth, it gains Shrouded instead. "
                           "Stealth and Shrouded do not stack."),
    "Unnatural Vigour": "The model gains +1 Wound. This Emanation may only be selected once.",
    "Preternatural Speed": "The model gains +1 Initiative. This Emanation may only be selected once.",
    "Monstrous Strength": "The model gains +1 Strength. This Emanation may only be selected once.",
    "Daemonic Resilience": ("The model gains Feel No Pain (6+). If the model already possesses Feel No Pain, improve its "
                            "Feel No Pain value by one step instead, to a maximum of Feel No Pain (4+). This Emanation may "
                            "only be selected once."),
    "Malevolent Presence": ("Enemy units within 6\" suffer -1 Leadership when taking Morale or Pinning tests caused by "
                            "casualties inflicted by this model or a unit it has joined. This effect is not cumulative "
                            "with itself."),
    # -------------------------------------------------- Dominion Emanations
    "Blood Frenzy": ("Crimson Fury Dominion Emanation. A model with Blood Frenzy gains +1 Attack in any Assault phase in "
                     "which it charged."),
    "Reaping Blows": ("Crimson Fury Dominion Emanation. For each natural roll of 6 To Hit in close combat, the model "
                      "immediately generates one additional hit. Additional hits cannot themselves generate further "
                      "hits."),
    "Brass-bound Rage": "Crimson Fury Dominion Emanation. The model gains the Counter-attack special rule.",
    "Corpulent Horror": ("Creeping Scourge Dominion Emanation. The model gains +1 Toughness and -1 Initiative (to a "
                         "minimum of 1). This Emanation may only be selected once."),
    "Pestilent Touch": ("Creeping Scourge Dominion Emanation. The model's normal close combat attacks gain Poisoned (4+). "
                        "This does not confer Poisoned upon attacks made with another special melee weapon unless "
                        "specifically stated otherwise."),
    "Miasma of Feebleness": ("Creeping Scourge Dominion Emanation. Enemy models in base contact with a model possessing "
                             "this Emanation suffer -1 Weapon Skill, to a minimum of 1. This effect is not cumulative "
                             "with itself."),
    "Sorcerous Conduit": (
        "Maddening Swarms Dominion Emanation. Daemon Characters and Monstrous Creatures only. The model becomes a Psyker "
        "with Mastery Level 1 and may select one power from the Ruinstorm Psychic Powers. If the model is already a Psyker, "
        "increase its Mastery Level by 1 instead, to the maximum permitted by its army list entry."),
    "Iridescent Form": ("Maddening Swarms Dominion Emanation. Improve the model's Invulnerable Save by one step, to a "
                        "maximum of 4+. This Emanation may only be selected once."),
    "Fate-touched": ("Maddening Swarms Dominion Emanation. Once per player turn, the model or unit may re-roll one failed "
                     "To Hit, To Wound or Saving Throw. The second result must be accepted."),
    "Quicksilver Grace": "Lurid Onslaught Dominion Emanation. The model gains the Hit & Run special rule.",
    "Transfixing Presence": ("Lurid Onslaught Dominion Emanation. Enemy models in base contact with a model possessing "
                             "this Emanation suffer -1 Attack, to a minimum of 1. This effect is not cumulative with "
                             "itself."),
    "Impossible Perfection": ("Lurid Onslaught Dominion Emanation. The model gains +1 Weapon Skill. This Emanation may "
                              "only be selected once."),
    "Anathema Aura": ("Mirror of Hatred Dominion Emanation. Enemy Psykers within 12\" suffer -1 Leadership when taking "
                      "Psychic Tests. This effect is not cumulative with itself."),
    "Reflected Malice": ("Mirror of Hatred Dominion Emanation. Whenever the model or its unit successfully resists a "
                         "Psychic Power which directly targets it, the enemy Psyker responsible immediately suffers a "
                         "Strength 4 AP- hit. This hit does not itself trigger any further effects from Reflected "
                         "Malice."),
    "Soul-rending Hatred": ("Mirror of Hatred Dominion Emanation. When attacking a Psyker or a model with the Daemon "
                            "special rule in close combat, re-roll To Wound rolls of 1, and Wounds inflicted by the model "
                            "may not be ignored by Feel No Pain."),
    "Dread Visage": ("Suffocating Dread Dominion Emanation. Enemy units taking a Fear test caused by this model or its unit "
                     "suffer an additional -1 Leadership."),
    "Oppressive Presence": ("Suffocating Dread Dominion Emanation. Enemy models in base contact with a model possessing "
                            "this Emanation suffer -1 Weapon Skill, to a minimum of 1. This effect is not cumulative with "
                            "itself."),
    "Soul-chilling Howl": ("Suffocating Dread Dominion Emanation. Once per game, at the start of one of the controlling "
                           "player's Assault phases, the model may unleash its Soul-Chilling Howl: every enemy unit "
                           "within 6\" must immediately take a Pinning test. Units normally immune to Pinning remain "
                           "immune."),
    "Ruinstorm Psychic Powers": (
        "Ruinstorm Psychic Powers follow all normal rules for Psychic Powers (Blessings, Maledictions, Witchfire). A Psyker "
        "selects a number of powers equal to its Mastery Level unless its entry states otherwise; powers are chosen when "
        "the army is selected, not generated randomly. Models with Sorcerous Conduit may select powers from this list."),
}

WEAPONS = {
    # Daemonic Melee Weapons (no AP column in the book)
    "Close Combat Weapon": ("-", "User", "-", "Melee"),
    "Daemonic Blade": ("-", "User", "-", "Melee, Rending"),
    "Warp Blade": ("-", "User", "-", "Melee, Power Weapon"),
    "Great Warp Blade": ("-", "+2", "-", "Melee, Power Weapon, Two-Handed, -2 Initiative"),
    "Daemonic Axe": ("-", "+1", "-", "Melee, Power Weapon, Two-Handed"),
    "Warp Maul": ("-", "+2", "-", "Melee, Armour Save -1, Concussive"),
    "Piercing Talons": ("-", "User", "-", "Melee, Rending, re-roll To Wound rolls of 1"),
    "Crushing Claw": ("-", "x2", "-", "Melee, Power Weapon, Specialist Weapon, Crushing"),
    "Aetheric Lash": ("-", "User", "-", "Melee, Rending, +1 Initiative"),
    # Daemonic Ranged Weapons
    "Spine Volley": ('18"', "4", "5", "Assault 3"),
    "Corrosive Vomit": ("Template", "4", "5", "Assault 1, Poison (4+)"),
    "Flaming Ichor": ("Template", "5", "4", "Assault 1"),
    "Bone Shard Harpoons": ('12"', "6", "4", "Assault 2"),
    "Rift Barb": ('18"', "5", "3", "Assault 1"),
    # Ruinstorm Possessed (standard ProHammer profiles - not printed in the book)
    "Lasgun": ('24"', "3", "-", "Rapid Fire"),
    "Laspistol": ('12"', "3", "-", "Pistol"),
    "Heavy Stubber": ('36"', "4", "6", "Heavy 3"),
    "Flamer": ("Template", "4", "5", "Assault 1"),
    "Plasma Gun": ('24"', "7", "2", "Rapid Fire, Gets Hot"),
    "Meltagun": ('12"', "8", "1", "Assault 1, Melta"),
    "Bolter": ('24"', "4", "5", "Rapid Fire"),
    "Bolt Pistol": ('12"', "4", "5", "Pistol"),
    "Power Weapon": ("-", "User", "-", "Ignores Armour Saves"),
    "Power Fist": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon"),
    "Lightning Claw": ("-", "User", "-", "Power Weapon, re-roll failed To Wound rolls, Specialist Weapon"),
    "Thunder Hammer": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Concussive"),
    # Named characters
    "Blades of Samus": ("-", "User", "-", "Melee, Power Weapon, Rending, Armourbane"),
    "Sword of Six Thousand Miseries": ("-", "User", "-", "Melee, Force Weapon, Rending"),
    "Noxious Maw": ("-", "User", "-", "Melee, Power Weapon, Instant Death on natural 5-6 To Hit vs Infantry/Jump "
                                      "Infantry/Bikes/Cavalry"),
    "Blade of the Undivided": ("-", "User", "-", "Melee, Force Weapon, Rending"),
}
MULTI = {
    "Grenade Launcher": {"Grenade Launcher - Frag": ('24"', "3", "6", "Assault 1, Blast"),
                         "Grenade Launcher - Krak": ('24"', "6", "4", "Assault 1")},
    "Armaments of Ka'Bandha": {
        "Armaments of Ka'Bandha - Close Combat": ("-", "10", "-", "Melee, Power Weapon, Tank Hunters (armour penetration)"),
        "Armaments of Ka'Bandha - Barbed Lash": ('6"', "6", "2", "Assault 7 (Shooting phase)"),
    },
}
WEAPON_RULES = {
    "Daemonic Blade": ["Rending"], "Great Warp Blade": ["Two-Handed"], "Daemonic Axe": ["Two-Handed"],
    "Warp Maul": ["Armour Save -1", "Concussive"], "Piercing Talons": ["Rending"], "Crushing Claw": ["Crushing"],
    "Aetheric Lash": ["Rending"], "Corrosive Vomit": ["Poison"], "Plasma Gun": ["Gets Hot"], "Meltagun": ["Melta"],
    "Power Fist": ["Unwieldy"], "Thunder Hammer": ["Unwieldy", "Concussive"],
    "Blades of Samus": ["Rending", "Armourbane"], "Sword of Six Thousand Miseries": ["Rending"],
    "Blade of the Undivided": ["Rending"], "Armaments of Ka'Bandha": ["Tank Hunters"],
}
WARGEAR = {
    "Power Armour": "A model wearing Power Armour has a 3+ Armour Save.",
    "Flak Armour": "A model wearing Flak Armour has a 5+ Armour Save.",
    # Daemonic Forms
    "Winged": ("Daemonic Form. If the model is Infantry its Unit Type becomes Jump Infantry; if it is a Monstrous "
               "Creature its Unit Type becomes Flying Monster. The model gains all rules associated with its new Unit "
               "Type, including Deep Strike where applicable. A Ruinstorm Daemon Lord with the Winged Daemonic Form may "
               "not select a Daemon Brute Retinue."),
    "Mounted": ("Daemonic Form. The model's Unit Type becomes Cavalry and it gains all rules associated with Cavalry."),
    "Beast Form": ("Daemonic Form. The model's Unit Type becomes Beast and it gains all rules associated with Beasts."),
    # Named character wargear texts
    "Blades of Samus": "Attacks made with the Blades of Samus count as Power Weapon attacks and have Rending and Armourbane.",
    "Sword of Six Thousand Miseries": ("Attacks made with the Sword of Six Thousand Miseries count as attacks made with a "
                                       "Force Weapon and have the Rending special rule."),
    "Noxious Maw": ("Attacks made with the Noxious Maw count as Power Weapon attacks. When attacking Infantry, Jump "
                    "Infantry, Bikes or Cavalry, natural To Hit rolls of 5 or 6 inflict Instant Death if the resulting "
                    "Wound is not saved. Models immune to Instant Death remain immune."),
    "Blade of the Undivided": ("Attacks made with the Blade of the Undivided count as attacks made with a Force Weapon "
                               "and have the Rending special rule."),
    "Armaments of Ka'Bandha": ("In close combat, attacks made with the Armaments of Ka'Bandha count as Power Weapon "
                               "attacks and are resolved at Strength 10; Ka'Bandha has Tank Hunters when making Armour "
                               "Penetration rolls with them. In the Shooting phase Ka'Bandha may strike with its barbed "
                               "lash: 6\", Strength 6, AP2, Assault 7."),
}

# ============================================================ cost tables
LESSER, GREATER, MONSTROUS = 0, 1, 2
CLS_NAME = ["Lesser", "Greater", "Monstrous"]

GENERAL_EMANATIONS = [  # name, (Lesser, Greater, Monstrous)
    ("Warp-scaled Hide", (5, 10, 20)),
    ("Sundering Fangs", (3, 5, 5)),
    ("Flensing Talons", (2, 4, 8)),
    ("Crushing Limbs", (3, 6, 15)),
    ("Horned Crown", (None, 5, 10)),
    ("Molten Blood", (3, 6, 10)),
    ("Shroud of Darkness", (4, 8, 15)),
    ("Unnatural Vigour", (10, 15, 30)),
    ("Preternatural Speed", (2, 3, 5)),
    ("Monstrous Strength", (3, 5, 10)),
    ("Daemonic Resilience", (5, 10, 25)),
    ("Malevolent Presence", (1, 3, 5)),
]

DOMINIONS = ["Crimson Fury", "Creeping Scourge", "Maddening Swarms", "Lurid Onslaught", "Mirror of Hatred",
             "Suffocating Dread"]
DOMINION_RULES = {
    "Crimson Fury": ["Fury Incarnate", "Unending Slaughter", "Furious Charge"],
    "Creeping Scourge": ["Unnatural Resilience", "Miasma of Decay", "Feel No Pain (6+)"],
    "Maddening Swarms": ["Born of Sorcery", "Flickering Reality"],
    "Lurid Onslaught": ["Preternatural Grace", "Unnatural Swiftness", "Fleet"],
    "Mirror of Hatred": ["Spite Incarnate", "Refusal of the Warp", "Hatred"],
    "Suffocating Dread": ["Pall of Terror", "Unreasoning Horror"],
}
DOMINION_EMANATIONS = {
    "Crimson Fury": [("Blood Frenzy", (3, 5, 10)), ("Reaping Blows", (4, 6, 10)), ("Brass-bound Rage", (2, 4, 8))],
    "Creeping Scourge": [("Corpulent Horror", (6, 12, 25)), ("Pestilent Touch", (3, 5, 8)),
                         ("Miasma of Feebleness", (2, 5, 10))],
    "Maddening Swarms": [("Sorcerous Conduit", (None, 15, 25)), ("Iridescent Form", (5, 10, 20)),
                         ("Fate-touched", (2, 4, 8))],
    "Lurid Onslaught": [("Quicksilver Grace", (3, 6, 10)), ("Transfixing Presence", (3, 6, 12)),
                        ("Impossible Perfection", (2, 4, 8))],
    "Mirror of Hatred": [("Anathema Aura", (3, 6, 10)), ("Reflected Malice", (3, 5, 10)),
                         ("Soul-rending Hatred", (2, 4, 8))],
    "Suffocating Dread": [("Dread Visage", (2, 4, 8)), ("Oppressive Presence", (3, 6, 10)),
                          ("Soul-chilling Howl", (4, 8, 15))],
}
GREATER_MANIFESTATION = {"Crimson Fury": "Avatar of Slaughter", "Creeping Scourge": "Pestilent Monolith",
                         "Maddening Swarms": "Oracle of Chaos", "Lurid Onslaught": "Flickering Gait",
                         "Mirror of Hatred": "Inimitable Recursion", "Suffocating Dread": "Avatar of Despair"}
GM_ELIGIBLE = {  # archetype -> dominions whose Greater Manifestation it receives
    "Greater Daemon": DOMINIONS,
    "Daemon Behemoth": ["Crimson Fury", "Creeping Scourge", "Lurid Onslaught", "Suffocating Dread"],
    "Arch-Daemon": DOMINIONS,
}
FAVOURED = {  # archetype -> dominions that favour it
    "Lesser Daemons": ["Crimson Fury", "Creeping Scourge", "Maddening Swarms", "Lurid Onslaught", "Suffocating Dread"],
    "Daemon Beasts": ["Crimson Fury", "Maddening Swarms", "Lurid Onslaught", "Suffocating Dread"],
    "Daemon Cavalry": ["Crimson Fury", "Lurid Onslaught", "Suffocating Dread"],
    "Daemon Brutes": ["Crimson Fury", "Creeping Scourge", "Mirror of Hatred"],
    "Daemon Swarms": ["Creeping Scourge", "Maddening Swarms", "Suffocating Dread"],
    "Daemon Behemoths": ["Creeping Scourge", "Mirror of Hatred"],
    "Greater Daemon Beasts": ["Crimson Fury", "Maddening Swarms", "Lurid Onslaught", "Suffocating Dread"],
    "Daemon Shrikes": [],
    "Character": DOMINIONS,
}

MELEE = [  # name, (Lesser, Greater, Monstrous)
    ("Daemonic Blade", (3, 5, 5)),
    ("Warp Blade", (5, 10, None)),
    ("Great Warp Blade", (10, 15, 20)),
    ("Daemonic Axe", (8, 12, 10)),
    ("Warp Maul", (6, 10, 12)),
    ("Piercing Talons", (5, 8, 8)),
    ("Crushing Claw", (15, 20, 25)),
    ("Aetheric Lash", (5, 8, 8)),
]
RANGED = [
    ("Spine Volley", (4, 6, 10)),
    ("Corrosive Vomit", (4, 6, 10)),
    ("Flaming Ichor", (5, 8, 12)),
    ("Bone Shard Harpoons", (6, 10, 15)),
    ("Rift Barb", (5, 8, 10)),
]
RUINSTORM_DISC = "Ruinstorm"
# Ruinstorm Psychic Powers (L4374-4481), same entry shape as tools/data/psychic_powers.py; added to PSY.POWERS in build()
RUINSTORM_POWERS = {
    "Aetheric Bolt": dict(discipline=RUINSTORM_DISC, type="Witchfire", profile=('18"', "6", "3", "Witchfire, Assault 2"),
                          text="Ruinstorm Psychic Power. Witchfire - range 18\", S6, AP3, Assault 2."),
    "Unmaking Gaze": dict(discipline=RUINSTORM_DISC, type="Witchfire - Focused",
                          profile=('12"', "7", "2", "Focused Witchfire, Assault 1"),
                          text=("Ruinstorm Psychic Power. Focused Witchfire - range 12\". If successfully invoked, resolve "
                                "a single ranged attack against the target unit with the profile 12\", S7, AP2, Assault 1. "
                                "As a Focused Witchfire, the normal rules for determining which model in the target unit "
                                "is affected apply.")),
    "Veil of Unreality": dict(discipline=RUINSTORM_DISC, type="Blessing", profile=None,
                              text=("Ruinstorm Psychic Power. Blessing - friendly Daemon unit within 12\". Until the start "
                                    "of the Psyker's next turn, enemy models suffer -1 Ballistic Skill when firing at the "
                                    "affected unit from more than 12\" away; Ballistic Skill may never be reduced below 1 "
                                    "by this power. No effect upon attacks which do not use Ballistic Skill.")),
    "Warp Mutation": dict(discipline=RUINSTORM_DISC, type="Blessing", profile=None,
                          text=("Ruinstorm Psychic Power. Blessing - friendly Daemon unit within 12\". When successfully "
                                "invoked choose: Predatory Mutation (the unit gains +1 Strength) or Quicksilver Mutation "
                                "(the unit gains +1 Initiative), until the start of the Psyker's next turn. The same "
                                "characteristic may not be increased more than once by Warp Mutation.")),
    "Delirium of the Immaterium": dict(discipline=RUINSTORM_DISC, type="Malediction", profile=None,
                                       text=("Ruinstorm Psychic Power. Malediction - enemy unit within 18\". Until the "
                                             "start of the Psyker's next turn the unit suffers -1 Weapon Skill and -1 "
                                             "Ballistic Skill; neither may be reduced below 1.")),
    "Impossible Geometry": dict(discipline=RUINSTORM_DISC, type="Blessing", profile=None,
                                text=("Ruinstorm Psychic Power. Blessing - friendly Daemon unit within 12\". Until the "
                                      "start of the Psyker's next turn the unit ignores penalties to Movement caused by "
                                      "Difficult Terrain and may move through it as though it were open ground, but must "
                                      "still take Dangerous Terrain tests where normally required. Models may not move "
                                      "through impassable terrain, enemy models or other locations they could not "
                                      "normally occupy. Grants no additional Movement and does not allow a charge that "
                                      "would otherwise be impossible.")),
}

DOM = {}          # dominion name -> config option id (set in build)
LORD_CAT = None   # category of the Ruinstorm Daemon Lord (barred from the Allied Detachment)


def dom_on(d):
    return cond(DOM[d], "force", "atLeast", 1)


def dom_off(d):
    return cond(DOM[d], "force", "lessThan", 1)


# ============================================================ option blocks
def _cost(eid, pts, unit_id, multi):
    """(cost, mods) - flat for single-model entries, per model for units."""
    if multi:
        return 0, [modifier("increment", PTS, pts, repeats=[repeat("model", unit_id, 1)])]
    return pts, []


def emanations(key, unit_id, cls, n, archetype, multi, character=False, conduit=False, general_only=False):
    """Daemonic Emanations group (General + Dominion Emanations of the Dominions favouring this archetype).
    Returns (group, conduit entry id or None)."""
    gid = uid("grp", key, "emanations")
    ents, conduit_id = [], None

    def add(name, pts, dom=None):
        eid = uid(key, "emanation", name)
        cost, mods = _cost(eid, pts, unit_id, multi)
        mx = uid(eid, "max")
        if dom:
            mods += [modifier("set", "hidden", "true", conds=[dom_off(dom)]), modifier("set", mx, 0, conds=[dom_off(dom)])]
        ents.append(entry(eid, name, cost=cost, mods=mods, constraints=[constraint(mx, "max", 1, auto=True)],
                          infolinks=rules_links([name], key=eid)))
        return eid

    for name, costs in GENERAL_EMANATIONS:
        if name == "Horned Crown" and not character:
            continue
        if costs[cls] is not None:
            add(name, costs[cls])
    if not general_only:
        doms = DOMINIONS if character else FAVOURED[archetype]
        for d in doms:
            for name, costs in DOMINION_EMANATIONS[d]:
                if name == "Sorcerous Conduit" and not conduit:
                    continue
                if costs[cls] is None:
                    continue
                eid = add(name, costs[cls], dom=d)
                if name == "Sorcerous Conduit":
                    conduit_id = eid
    kind = "General Emanations" if general_only else "Daemonic Emanations"
    title = f"{kind} (up to {n}, {CLS_NAME[cls]} cost{', per model' if multi else ''})"
    g = group(gid, title, entries=ents, constraints=[constraint(uid(gid, "max"), "max", n, auto=True)])
    return g, conduit_id


def psychic_group(key, unit_id, conduit_id):
    """One Ruinstorm Psychic Power (one per unit, like a Brotherhood of Psykers), only with Sorcerous Conduit."""
    return psychic_powers(uid(key, "conduit"), unit_id, 1, [RUINSTORM_DISC], hide=[lacks(conduit_id, unit_id)],
                          title="Psychic Powers (Sorcerous Conduit: one Ruinstorm Psychic Power)")


def melee_choice(key, unit_id, cls, multi):
    opts = [("Close Combat Weapon", 0, False, ["Close Combat Weapon"], [])]
    opts += [(n, c[cls], multi, [n], []) for n, c in MELEE if c[cls] is not None]
    return choice(key, f"Daemonic Melee Weapon ({CLS_NAME[cls]} cost{', entire unit, per model' if multi else ''})",
                  opts, unit_id=unit_id, required=True, default="Close Combat Weapon")


def ranged_choice(key, unit_id, cls, multi):
    opts = [(n, c[cls], multi, [n], []) for n, c in RANGED]
    return choice(key, f"Daemonic Ranged Weapon ({CLS_NAME[cls]} cost{', entire unit, per model' if multi else ''})",
                  opts, unit_id=unit_id)


def manifestation_group(key, archetype):
    """Greater Manifestation of the chosen Dominion, added automatically for eligible models."""
    gid = uid("grp", key, "gm")
    ents = []
    for d in GM_ELIGIBLE[archetype]:
        n = GREATER_MANIFESTATION[d]
        eid = uid(key, "gm", n)
        mn, mx = uid(eid, "min"), uid(eid, "max")
        ents.append(entry(eid, f"Greater Manifestation: {n}", hidden=True,
                          mods=[modifier("set", "hidden", "false", conds=[dom_on(d)]),
                                modifier("set", mn, 1, conds=[dom_on(d)]), modifier("set", mx, 1, conds=[dom_on(d)])],
                          constraints=[constraint(mn, "min", 0, auto=True), constraint(mx, "max", 0, auto=True)],
                          infolinks=rules_links([n, "Greater Manifestations"], key=eid)))
    return group(gid, "Greater Manifestation (automatic, free)", entries=ents)


def daemon_groups(key, unit_id, cls, n_eman, archetype, multi, character=False, conduit=False, general_only=False,
                  melee=True, ranged=True):
    gs_ = []
    eg, cid = emanations(key, unit_id, cls, n_eman, archetype, multi, character, conduit, general_only)
    gs_.append(eg)
    if cid:
        gs_.append(psychic_group(key, unit_id, cid))
    if melee:
        gs_.append(melee_choice(key, unit_id, cls, multi))
    if ranged:
        gs_.append(ranged_choice(key, unit_id, cls, multi))
    return gs_


def dominion_text_rules():
    return ["Aetheric Dominion"]


# ================================================================== units
def single_daemon(name, cost, slot_cat, slot_name, stats, unit_type, mv, n_eman, archetype, rules_=(), forms=(),
                  gm=None, character=True, conduit=True, extra_groups=(), entries=(), mods=(), constraints=(),
                  extra_cats=(), compulsory=True, kit_extra=()):
    u = k("unit", name)
    prof = unit_profile(u, name, unit_type, *stats)
    m = model(u, name, 1, 1, 0, prof)
    groups = daemon_groups(u, u, MONSTROUS if "Monstrous" in unit_type or "Flying" in unit_type else GREATER, n_eman,
                           archetype, False, character=character, conduit=conduit)
    if forms:
        groups.append(take(u, "Daemonic Form", list(forms), max_total=1))
    if gm:
        groups.append(manifestation_group(u, gm))
    groups += list(extra_groups)
    rl = ["Daemon", "Daemonic Instability", f"Manifestation Value {mv}", "Aetheric Dominion", "Favoured Archetype",
          "Daemonic Emanations", "Daemonic Weapons", *rules_]
    if forms:
        rl.append("Daemonic Forms")
    return unit(name, cost, slot_cat, slot_name, models=[m], kit=list(kit_extra), rules_=rl, groups=groups,
                entries=list(entries), mods=list(mods), constraints=list(constraints), key=u,
                extra_cats=list(extra_cats), compulsory=compulsory)


def squad_daemon(name, slot_cat, slot_name, model_name, mn, mx, per, stats, unit_type, mv, cls, n_eman, archetype,
                 rules_=(), melee=True, ranged=True, compulsory=True, key=None, root=True, base_cost=0):
    u = key or k("unit", name)
    prof = unit_profile(u, model_name, unit_type, *stats)
    kit = [] if melee else ["Close Combat Weapon"]
    m = model(u, model_name, mn, mx, per, prof, kit=kit)
    groups = daemon_groups(u, u, cls, n_eman, archetype, True, melee=melee, ranged=ranged,
                           conduit=archetype in ("Greater Daemon Beasts",))
    rl = ["Daemon", "Daemonic Instability", f"Manifestation Value {mv}", "Aetheric Dominion", "Favoured Archetype",
          "Daemonic Emanations", *rules_]
    if melee or ranged:
        rl.append("Daemonic Weapons")
    if root:
        return unit(name, base_cost, slot_cat, slot_name, models=[m], rules_=rl, groups=groups, key=u,
                    compulsory=compulsory)
    return entry(u, name, typ="unit", cost=base_cost, infolinks=rules_links(rl, key=u), entries=[m], groups=groups)


# ---------------------------------------------------------------- HQ
def brutes(root=True):
    if root:
        return squad_daemon("Ruinstorm Daemon Brutes", ELITES, "Elites", "Ruinstorm Daemon Brute", 3, 6, 45,
                            (5, 3, 5, 5, 3, 4, 3, 8, "5++"), "Infantry", 2, GREATER, 2, "Daemon Brutes",
                            rules_=["Bulky", "Daemon Brute Retinue"])
    return squad_daemon("Ruinstorm Daemon Brute Retinue", None, None, "Ruinstorm Daemon Brute", 1, 3, 45,
                        (5, 3, 5, 5, 3, 4, 3, 8, "5++"), "Infantry", 2, GREATER, 2, "Daemon Brutes",
                        rules_=["Bulky", "Daemon Brute Retinue"], key=k("unit", "brute-retinue"),
                        root=False)


KABANDHA = None  # id of Ka'Bandha's unit (set in build)


def daemon_lord(retinue):
    u = k("unit", "Ruinstorm Daemon Lord")
    winged = has(W("Winged"), u)
    with_ret = has(retinue.get("id"), u)
    rgid = uid("grp", u, "retinue")
    ret_group = group(rgid, "Daemon Brute Retinue (1-3 Brutes, no Force Organisation slot)",
                      links=[link(uid("link", rgid, "brutes"), retinue.get("id"), retinue.get("name"))],
                      constraints=[constraint(uid(rgid, "max"), "max", 1, auto=True)],
                      mods=[modifier("set", "hidden", "true", conds=[winged]),
                            modifier("set", uid(rgid, "max"), 0, conds=[winged])])
    e = single_daemon("Ruinstorm Daemon Lord", 200, HQ, "HQ", (7, 4, 6, 6, 5, 5, 5, 10, "4++"),
                      "Monstrous Creature (Character)", 3, 3, "Character",
                      rules_=["Lord of the Ruinstorm", "The Army's Warlord", "Daemon Brute Retinue", "Daemonic Forms"],
                      extra_groups=[ret_group],
                      constraints=[unique(u, 1, "force")],
                      mods=[modifier("set", "hidden", "true", conds=[cond(KABANDHA, "roster", "atLeast", 1)]),
                            error_if("Ka'Bandha takes over as Warlord: an army including Ka'Bandha may not include a "
                                     "Ruinstorm Daemon Lord.", [cond(KABANDHA, "roster", "atLeast", 1)])],
                      extra_cats=[(LORD_CAT, "Ruinstorm Daemon Lord")])
    # Winged form (hidden while a Retinue is taken)
    tg = take(u, "Daemonic Form", [("Winged", 35)], max_total=1, hide=[with_ret])
    add_to(e, "selectionEntryGroups", [tg])
    return e


def greater_daemon():
    return single_daemon("Ruinstorm Greater Daemon", 150, HQ, "HQ", (6, 4, 6, 6, 4, 4, 4, 10, "4++"),
                         "Monstrous Creature (Character)", 3, 2, "Character", forms=[("Winged", 30)],
                         gm="Greater Daemon")


def daemon_chosen():
    return single_daemon("Ruinstorm Daemon Chosen", 55, HQ, "HQ", (5, 4, 5, 4, 2, 5, 3, 10, "5++"),
                         "Infantry (Character)", 2, 2, "Character",
                         rules_=["Independent Character", "Shepherd of Malign Intent"],
                         forms=[("Winged", 15), ("Mounted", 15), ("Beast Form", 15)])


# ---------------------------------------------------------------- Troops
def lesser_daemons():
    return squad_daemon("Ruinstorm Lesser Daemons", TROOPS, "Troops", "Ruinstorm Lesser Daemon", 5, 20, 13,
                        (4, 3, 4, 4, 1, 4, 2, 10, "5++"), "Infantry", 1, LESSER, 3, "Lesser Daemons")


def daemon_beasts():
    return squad_daemon("Ruinstorm Daemon Beasts", TROOPS, "Troops", "Ruinstorm Daemon Beast", 3, 10, 30,
                        (4, 3, 5, 5, 2, 4, 2, 10, "5++"), "Beast", 1, GREATER, 2, "Daemon Beasts")


def daemon_swarms():
    return squad_daemon("Ruinstorm Daemon Swarms", TROOPS, "Troops", "Ruinstorm Daemon Swarm", 3, 10, 20,
                        (3, 0, 3, 3, 3, 3, 3, 10, "5++"), "Infantry (Swarm)", 1, LESSER, 1, "Daemon Swarms",
                        rules_=["Swarms", "Support Unit"], melee=False, ranged=False, compulsory=False)


def possessed():
    name = "Ruinstorm Possessed"
    u = k("unit", name)
    aux = uid("model", u, "Possessed Auxiliary")
    leg = uid("model", u, "Possessed Legionary")
    upg = uid(u, "upgrade", "Possessed Legionaries")
    up = has(upg, u)
    not_up = lacks(upg, u)
    amin, amax, lmin, lmax = uid(aux, "min"), uid(aux, "max"), uid(leg, "min"), uid(leg, "max")
    aux_m = entry(aux, "Possessed Auxiliary", typ="model", cost=5,
                  mods=[modifier("set", amin, 0, conds=[up]), modifier("set", amax, 0, conds=[up]),
                        modifier("set", "hidden", "true", conds=[up])],
                  constraints=[constraint(amin, "min", 10), constraint(amax, "max", 20)],
                  profiles=[unit_profile(u, "Possessed Auxiliary", "Infantry", 3, 3, 3, 3, 1, 2, 1, 9, "5+")],
                  links=[gear(aux, "Close Combat Weapon"), gear(aux, "Flak Armour")])
    leg_m = entry(leg, "Possessed Legionary", typ="model", cost=10, hidden=True,
                  mods=[modifier("set", lmin, 10, conds=[up]), modifier("set", lmax, 20, conds=[up]),
                        modifier("set", "hidden", "false", conds=[up])],
                  constraints=[constraint(lmin, "min", 0), constraint(lmax, "max", 0)],
                  profiles=[unit_profile(u, "Possessed Legionary", "Infantry", 4, 4, 4, 4, 1, 3, 2, 9, "3+")],
                  links=[gear(leg, "Close Combat Weapon"), gear(leg, "Bolter"), gear(leg, "Power Armour")])
    upgrade_e = entry(upg, "Upgrade to Possessed Legionaries (+5 pts per model)",
                      constraints=[constraint(uid(upg, "max"), "max", 1, auto=True)],
                      rules=[rule(uid(upg, "rule"), "Possessed Legionaries",
                                  "The entire unit is upgraded to Possessed Legionaries for +5 points per model: remove "
                                  "the Possessed Auxiliaries and add the same number of Possessed Legionaries (10 points "
                                  "each).")])
    hide_aux = [modifier("set", "hidden", "true", conds=[up])]
    hide_leg = [modifier("set", "hidden", "true", conds=[not_up])]
    sidearm = choice(u, "Possessed Auxiliaries: Lasguns or Laspistols (entire unit)",
                     [("Lasguns", 0, False, ["Lasgun"], []), ("Laspistols", 0, False, ["Laspistol"], [])],
                     unit_id=u, required=False, default="Lasguns")
    sidearm_id = sidearm.get("id")
    smin = uid(sidearm_id, "min")
    add_to(sidearm, "constraints", [constraint(smin, "min", 1, auto=True)])
    add_mods(sidearm, [modifier("set", smin, 0, conds=[up]), modifier("set", uid(sidearm_id, "max"), 0, conds=[up]),
                       modifier("set", "hidden", "true", conds=[up])])
    aux_pool, _ = pool(u, "Possessed Auxiliaries: for every 5, one may replace its Lasgun", u,
                       [("Heavy Stubber", 10), ("Flamer", 10), ("Grenade Launcher", 10), ("Plasma Gun", 15),
                        ("Meltagun", 15)], 0, every=5, per_child=aux, extra_mods=hide_aux)
    leg_pool, _ = pool(u, "Possessed Legionaries: for every 5, one may replace its Bolter", u,
                       [("Flamer", 10), ("Plasma Gun", 15), ("Meltagun", 15)], 0, every=5, per_child=leg,
                       extra_mods=hide_leg)
    pistols = model_swaps(u, "Possessed Legionaries: exchange Bolter for Bolt Pistol (any model)", u, [leg],
                          [("Bolt Pistol", 0)], minus=[W("Flamer"), W("Plasma Gun"), W("Meltagun")])
    add_mods(pistols, hide_leg)
    ccw = take(u, "One Possessed Legionary may replace its Close Combat Weapon",
               [("Power Weapon", 10), ("Power Fist", 15), ("Lightning Claw", 15), ("Thunder Hammer", 20)],
               max_total=1, hide=[not_up])
    return unit(name, 0, TROOPS, "Troops", models=[aux_m, leg_m], rules_=["Slaves to Darkness", "Support Unit"],
                entries=[upgrade_e], groups=[sidearm, aux_pool, leg_pool, pistols, ccw], key=u, compulsory=False)


# -------------------------------------------------------- Fast Attack
def daemon_cavalry():
    return squad_daemon("Ruinstorm Daemon Cavalry", FA, "Fast Attack", "Ruinstorm Daemon Cavalry", 5, 10, 20,
                        (4, 3, 4, 4, 1, 5, 3, 10, "5++"), "Cavalry", 2, LESSER, 2, "Daemon Cavalry")


def daemon_shrike():
    name = "Ruinstorm Daemon Shrike"
    u = k("unit", name)
    prof = unit_profile(u, name, "Flying Monster", 5, 4, 6, 5, 4, 5, 4, 10, "5++")
    m = model(u, name, 1, 1, 0, prof)
    groups = daemon_groups(u, u, MONSTROUS, 2, "Daemon Shrikes", False, general_only=True)
    return unit(name, 160, FA, "Fast Attack", models=[m], groups=groups, key=u,
                rules_=["Daemon", "Daemonic Instability", "Manifestation Value 2", "Aetheric Dominion",
                        "Daemonic Emanations", "Daemonic Weapons"])


# ------------------------------------------------------- Heavy Support
def greater_daemon_beasts():
    return squad_daemon("Greater Ruinstorm Daemon Beasts", HS, "Heavy Support", "Greater Ruinstorm Daemon Beast", 1, 3,
                        100, (4, 3, 6, 6, 4, 3, 3, 10, "5++"), "Monstrous Creature", 2, MONSTROUS, 3,
                        "Greater Daemon Beasts")


def behemoth():
    return single_daemon("Ruinstorm Daemon Behemoth", 300, HS, "Heavy Support", (4, 3, 7, 7, 7, 2, 5, 10, "4++"),
                         "Monstrous Creature", 3, 3, "Daemon Behemoths", rules_=["Unstoppable"],
                         forms=[("Winged", 50)], gm="Daemon Behemoth", character=False, conduit=True)


# ------------------------------------------------------- Lords of War
LOW_LIMIT = None


def low_mods():
    return [error_if("No army may contain more than one Lord of War selection.",
                     [cond(LOW, "roster", "greaterThan", 1)])]


def arch_daemon():
    return single_daemon("Arch-Daemon", 450, LOW, "Lords of War", (8, 5, 7, 7, 7, 6, 6, 10, "4++"),
                         "Monstrous Creature (Character)", 3, 4, "Character", rules_=["Unstoppable", "Apex Manifestation"],
                         forms=[("Winged", 60)], gm="Arch-Daemon", mods=low_mods(), compulsory=False)


def named(name, short, cost, stats, unit_type, weapon, rules_, dominion=None, mods=(), powers=None):
    """powers: (count, [disciplines], [fixed powers]) for a psyker."""
    u = k("unit", name)
    prof = unit_profile(u, short, unit_type, *stats)
    m = model(u, short, 1, 1, 0, prof, kit=[weapon])
    mods = list(mods) + low_mods()
    if dominion:
        mods += [modifier("set", "hidden", "true", conds=[dom_off(dominion)]),
                 error_if(f"{short} may only be selected in a Detachment using the {dominion} Aetheric Dominion.",
                          [dom_off(dominion)])]
    rl = ["Daemon", "Daemonic Instability", "Manifestation Value 3", *rules_]
    if dominion:
        rl += [dominion] + [r for r in DOMINION_RULES[dominion]]
    groups = []
    if powers:
        n, discs, fixed = powers
        groups.append(psychic_powers(u, u, n, discs, fixed=fixed))
    return unit(name, cost, LOW, "Lords of War", models=[m], rules_=rl, mods=mods, constraints=[unique(u)], key=u,
                compulsory=False, groups=groups)


def named_characters():
    out = [
        named("Samus, The End and The Death", "Samus", 400, (9, 5, 8, 7, 7, 6, 6, 10, "3+/4++"),
              "Monstrous Creature (Character, Unique)", "Blades of Samus",
              ["Deep Strike", "Eternal Warrior", "It Will Not Die", "Preferred Enemy (Characters)", "Born of Murder",
               "Samus (Aetheric Dominion)", "Dread Visage"], dominion="Suffocating Dread"),
        named("Kyriss the Perverse", "Kyriss the Perverse", 400, (9, 5, 6, 6, 6, 9, 7, 10, "3+/4++"),
              "Monstrous Creature (Character, Unique)", "Sword of Six Thousand Miseries",
              ["Deep Strike", "Psyker", "Psyker (Kyriss the Perverse)", "Kyriss (Aetheric Dominion)",
               "Quicksilver Grace", "Hit & Run", "Transfixing Presence"], dominion="Lurid Onslaught",
              powers=(0, [], ["Dominate", "Hallucination"])),
        named("Cor'bax Utterblight Unbound", "Cor'bax Utterblight", 425, (6, 3, 7, 8, 8, 3, 5, 10, "4++"),
              "Monstrous Creature (Character, Unique)", "Noxious Maw",
              ["Eternal Warrior", "Feel No Pain (5+)", "Hammer of Wrath", "Psyker", "Psyker (Cor'bax Utterblight)",
               "Noisome Tide of Flesh", "Cor'bax (Aetheric Dominion)", "Miasma of Feebleness", "Crushing Limbs"],
              dominion="Creeping Scourge", powers=(2, ["Biomancy"], [])),
    ]
    # Madail: any Dominion
    u = k("unit", "Madail the Undivided")
    prof = unit_profile(u, "Madail", "Monstrous Creature (Character, Unique)", 8, 5, 7, 7, 7, 6, 6, 10, "3+/4++")
    m = model(u, "Madail", 1, 1, 0, prof, kit=["Blade of the Undivided"])
    out.append(unit("Madail the Undivided", 475, LOW, "Lords of War", models=[m], key=u, compulsory=False,
                    rules_=["Daemon", "Daemonic Instability", "Manifestation Value 3", "Deep Strike", "Eternal Warrior",
                            "Adamantium Will", "Psyker", "Psyker (Madail the Undivided)", "The Undivided",
                            "Aetheric Dominion", "Horned Crown"],
                    mods=low_mods(), constraints=[unique(u)],
                    groups=[psychic_powers(u, u, 0, [], fixed=["Psychic Shriek", "Hallucination", "Invisibility"])]))
    # Ka'Bandha
    lord = k("unit", "Ruinstorm Daemon Lord")
    out.append(named("Ka'Bandha, Daemon General of Signus", "Ka'Bandha", 550, (9, 5, 8, 7, 8, 6, 7, 10, "3+/4++"),
                     "Flying Monster (Character, Unique)", "Armaments of Ka'Bandha",
                     ["Eternal Warrior", "It Will Not Die", "Adamantium Will", "Rage (6th-7th Edition Codexes)",
                      "Lord of Murder", "Miasma of Rage", "Scythe of Hatred", "Eternal Rivalry",
                      "Preferred Enemy (Sanguinius)", "Ka'Bandha (Aetheric Dominion)", "Molten Blood", "Horned Crown"],
                     dominion="Crimson Fury",
                     mods=[error_if("Ka'Bandha takes over as Warlord: an army including Ka'Bandha may not include a "
                                    "Ruinstorm Daemon Lord.", [cond(lord, "roster", "atLeast", 1)])]))
    return out


# ============================================================ allied force
def allied_force():
    links = [category_link(gs.CAT_CONFIG, "Configuration", key=k("allied"))]
    for name, mn, mx in [("HQ", 1, 1), ("Troops", 1, 2), ("Elites", 0, 1), ("Fast Attack", 0, 1),
                         ("Heavy Support", 0, 1)]:
        cl = category_link(gs.cat(name), name, key=k("allied"))
        cl.append(wrap("constraints", [constraint(k("allied", "min", name), "min", mn),
                                       constraint(k("allied", "max", name), "max", mx)]))
        links.append(cl)
    for cid, name, mn in [(COMMANDER, "Compulsory HQ Eligible", 1), (LINE, "Compulsory Troops Eligible", 1)]:
        cl = category_link(cid, name, key=k("allied"))
        cl.append(wrap("constraints", [constraint(k("allied", "min", name), "min", mn)]))
        links.append(cl)
    cl = category_link(LORD_CAT, "Ruinstorm Daemon Lord", key=k("allied"))
    cl.append(wrap("constraints", [constraint(k("allied", "max", "lord"), "max", 0)]))
    links.append(cl)
    return el("forceEntry", {"id": k("force", "allied"), "name": "Ruinstorm Allied Detachment", "hidden": "false"},
              [wrap("categoryLinks", links)])


def traitor_only():
    """Allegiance (Traitor only). Daemons of the Ruinstorm - also as a Ruinstorm Allied Detachment - may only be part of
    a Traitor army: an error while the army (another catalogue's Detachment) has the Loyalist Allegiance."""
    e = allegiance(loyalist_ok=True, traitor_ok=True)
    # keep the (shared) Loyalist id in this catalogue so the check below resolves, but never selectable here
    for x in e.iter("selectionEntry"):
        if x.get("id") == L.LOYALIST:
            x.set("hidden", "true")
            for c in x.iter("constraint"):
                c.set("value", "0")
    for g in e.iter("selectionEntryGroup"):
        g.set("defaultSelectionEntryId", L.TRAITOR)
    add_mods(e, [error_if("A Daemons of the Ruinstorm Detachment (including a Ruinstorm Allied Detachment) may only be "
                          "included in a Traitor army.", [cond(L.LOYALIST, "roster", "atLeast", 1)])])
    return e


# ================================================================== build
def build():
    global LORD_CAT, KABANDHA
    start(ARMY)
    register_data(rules=RULES, weapons=WEAPONS, multi_profile=MULTI, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    PSY.POWERS.update(RUINSTORM_POWERS)
    LORD_CAT = k("cat", "Ruinstorm Daemon Lord")
    KABANDHA = k("unit", "Ka'Bandha, Daemon General of Signus")

    dom_entry, ids = config("dominion", "Aetheric Dominion",
                            [(d, [d] + DOMINION_RULES[d]) for d in DOMINIONS])
    DOM.update(ids)
    add_to(dom_entry, "infoLinks", rules_links(
        ["Daemons of the Ruinstorm", "Aetheric Dominion", "Favoured Archetype", "Greater Manifestations",
         "The Army's Warlord", "Allied Forces (Ruinstorm)", "Ruinstorm Allied Detachment",
         "Malefic Daemonology and Summoned Daemons", "Daemonic Archetypes", "Warp Portals", "Aetheric Reserves",
         "The Veil Thins", "Manifestation Capacity", "Sealing a Warp Portal", "Ruinstorm Psychic Powers"],
        key=dom_entry.get("id")))

    retinue = brutes(root=False)
    units = [
        traitor_only(),
        dom_entry,
        daemon_lord(retinue), greater_daemon(), daemon_chosen(),
        brutes(),
        lesser_daemons(), daemon_beasts(), daemon_swarms(), possessed(),
        daemon_cavalry(), daemon_shrike(),
        greater_daemon_beasts(), behemoth(),
        arch_daemon(), *named_characters(),
    ]
    root = catalogue(ARMY, units, [retinue], force_entries=[allied_force()])
    # the Daemon Lord category (used by the Allied Detachment to bar the Daemon Lord)
    cats = wrap("categoryEntries", [el("categoryEntry", {"id": LORD_CAT, "name": "Ruinstorm Daemon Lord",
                                                         "hidden": "false"})])
    idx = list(root).index(root.find("forceEntries"))
    root.insert(idx, cats)
    return root
