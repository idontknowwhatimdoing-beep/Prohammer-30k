"""III Legion - Emperor's Children (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, allegiance_only, upgrade, retinue_links, command_squad_for,
                            named_character, primarch, primarch_retinue, add_group, add_entry, LOW, TRAITOR,
                            LOYALIST)
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile
from legiones2 import (slot, take, pool, transports, add_mods, add_to, foc, rite_id, rite, walker_profile, TROOPS,
                       ELITES, FA, HQ, HS, model_swaps, model_takes, pa_armoury)
from legiones_wargear import ARMY_RULES, WEAPONS

LEGION = "III - Emperor's Children"
LR = "Legiones Astartes (Emperor's Children)"

RULES = {
    LR: ("Models with this rule belong to the III Legion and use the Emperor's Children Legion special rules: Exemplars "
         "of War, Purity Above All and Martial Pride."),
    "Exemplars of War": (
        "Emperor's Children units gain the Crusader special rule. In addition, during an Assault phase in which an "
        "Emperor's Children model charges, that model gains +1 Initiative until the end of that Assault phase. This bonus "
        "may be combined with other Initiative modifiers."),
    "Purity Above All": (
        "Any Legion Veteran Squad may upgrade its Legion Veteran Sergeant to an Apothecary for +25 points. In addition, up "
        "to one Legion Tactical Squad or Legion Assault Squad in the army may upgrade its Legion Sergeant to an Apothecary "
        "for +25 points. The Apothecary retains all weapons and wargear previously carried by the Sergeant and is "
        "additionally equipped with a Narthecium. It counts as an Apothecary for all rules and wargear restrictions and "
        "may purchase a Reductor for +5 points."),
    "Martial Pride": (
        "Emperor's Children units may not voluntarily withdraw from close combat. If an Emperor's Children unit wins a "
        "close combat and all enemy units it was engaged with retreat, it must Pursue if it is able to do so; it may not "
        "take a Restraint Test in order to Consolidate instead."),
    "Apothecary (Purity Above All)": (
        "This Sergeant has been upgraded to an Apothecary: he keeps all weapons and wargear previously carried, is "
        "additionally equipped with a Narthecium, counts as an Apothecary for all rules and wargear restrictions and may "
        "purchase a Reductor for +5 points."),
    # Armoury
    "Phoenix Strike": ("During the first round of each close combat, attacks made with a Phoenix Spear are resolved at +1 "
                       "Strength. After the first round, the weapon is resolved at the bearer's normal Strength."),
    "Phoenix Spear": (
        "Any Emperor's Children Independent Character or unit Character able to select a Power Weapon may instead select "
        "a Phoenix Spear instead for the cost of that Power Weapon +5 points. A model already equipped with a Power Weapon "
        "as part of its basic wargear may exchange it for a Phoenix Spear for +5 points. Named characters may not "
        "exchange their weapons for a Phoenix Spear."),
    "Digital Lasers": ("An Emperor's Children Independent Character may purchase Digital Lasers for +15 points. A model "
                       "equipped with Digital Lasers adds +1 to its Attacks characteristic. Digital Lasers may not be "
                       "combined with Terminator Honours. They count towards the Armoury points limit; named "
                       "Independent Characters may also purchase them."),
    "Sonic Shrieker": (
        "TRAITOR ONLY. An Emperor's Children Independent Character (including named Independent Characters, except Saul "
        "Tarvitz) may purchase a Sonic Shrieker for +10 points (other "
        "units may gain access through their unit entry or a Rite of War). During the first round of a close combat, an "
        "enemy model in base contact with a model equipped with a Sonic Shrieker suffers -1 Weapon Skill. If every model "
        "in an Emperor's Children unit is equipped with a Sonic Shrieker, every enemy model engaged with that unit "
        "suffers -1 Weapon Skill during the first round of close combat instead. This modifier is not cumulative. "
        "Fearless models are unaffected."),
    "Sonic Weaponry": (
        "TRAITOR ONLY. One Legion Heavy Support Squad in an Emperor's Children Detachment may select up to four Sonic "
        "Weapons (Sonic Blaster +15, Doom Siren +20, Blastmaster +35 points each); they may be mixed with weapons from its "
        "normal Heavy Weapon options, up to four Heavy and Sonic Weapons in total, and each replaces the Bolter of the "
        "model carrying it. In addition, one Emperor's Children Praetor or Centurion (including a Legion Consul) in the "
        "army may select a Sonic Blaster (+15) or a Doom Siren (+20); this does not count towards the Armoury points "
        "limit. A Character may carry no more than one Sonic Weapon."),
    "Perfect Cacophony (Armoury)": (
        "A Legion Heavy Support Squad equipped with at least two Sonic Weapons may purchase the Fearless special rule "
        "for +20 points per squad."),
    # Rites of War
    "The Maru Skara": (
        "EFFECTS - The Open Blade: all units deployed normally at the beginning of the battle form the Open Blade; the "
        "army's Warlord must form part of it and must begin the battle on the battlefield. The Hidden Blade: before "
        "deployment, nominate up to three Emperor's Children units from Legion Assault Squads, Legion Veteran Squads, "
        "Legion Terminator Squads, Palatine Blade Squads, Phoenix Terminator Squads, Legion Bike Squadrons and Legion Sky "
        "Hunter Jetbike Squadrons. An Independent Character may accompany a nominated unit normally; Dedicated Transports "
        "purchased for a nominated unit form part of the Hidden Blade with it. All units of the Hidden Blade must begin "
        "the battle in Reserve. Perfectly Timed Strike: after deployment zones are determined but before either army "
        "deploys, secretly record game turn 2 or 3 and the left or right side table edge. At the beginning of the chosen "
        "Emperor's Children turn reveal the choice: every surviving Hidden Blade unit becomes available automatically "
        "without a Reserve roll, enters play from the chosen side table edge and may act normally that turn. The Killing "
        "Stroke: during the player turn in which the Hidden Blade arrives, all Emperor's Children units may re-roll "
        "failed Advance rolls and failed Charge distance rolls (the second result must be accepted).\n"
        "LIMITATIONS - The army's Warlord must begin the battle as part of the Open Blade. The Hidden Blade may contain no "
        "more than three units, excluding attached Independent Characters and Dedicated Transports. The army may include "
        "no more than two Heavy Support choices. Immobile units (Fortifications) may not be selected."),
    "3rd Company Elite": (
        "TRAITOR ONLY.\nEFFECTS - Chosen of Vairosean: Kakophoni Squads may be selected as Troops choices and may then "
        "fulfil compulsory Troops selections. All Kakophoni Squads in the Detachment gain Relentless. Sonic Assault: any "
        "Emperor's Children Infantry unit composed entirely of models wearing Power Armour or Artificer Armour may "
        "purchase Sonic Shriekers for +2 points per model; every eligible model in the unit must purchase the upgrade "
        "(normal Sonic Shrieker rules). Armoury of Excess: up to two Legion Heavy Support Squads may select Sonic "
        "Weaponry. Perfect Cacophony: a unit in which every surviving model is equipped with either a Sonic Weapon or a "
        "Sonic Shrieker gains the Fear special rule.\n"
        "LIMITATIONS - Only a Traitor Emperor's Children Detachment. The army must include at least one Kakophoni Squad. "
        "The army's Warlord must be equipped with a Sonic Shrieker or a Doom Siren. The army may include no more than "
        "one Fortification."),
    "Selected as Troops (3rd Company Elite)": (
        "Under the 3rd Company Elite Rite of War this Kakophoni Squad is a Troops choice, may fulfil compulsory Troops "
        "selections and has the Relentless special rule."),
    "Sonic Assault (3rd Company Elite)": (
        "3rd Company Elite: this unit (every model wearing Power Armour or Artificer Armour) has purchased Sonic "
        "Shriekers for every model."),
    # Units
    "Duelists": ("When fighting an enemy unit containing one or more Characters or Independent Characters, models in "
                 "this squad may re-roll close-combat To Hit rolls of 1."),
    "Palatine Jump Packs": ("If equipped with Jump Packs the unit becomes Jump Infantry and follows the normal ProHammer "
                            "rules for Jump Infantry. It may not select a Dedicated Transport."),
    "Cacophony": ("If an enemy unit suffers one or more casualties from shooting attacks made by a Kakophoni Squad, it "
                  "must take a Pinning test after the squad has finished firing."),
    "Exemplary Marksmen": ("Once during each friendly Shooting phase, the Sun Killer Squad may re-roll one failed shooting "
                           "To Hit roll. The second result must be accepted."),
    "Energy Weapons (Sun Killers)": ("The entire squad may replace all of its Lascannons with Plasma Cannons (-5 points "
                                     "per model) or Volkite Culverins (-15 points per model). Every model in the squad "
                                     "must carry the same Heavy weapon."),
    # Characters
    "Thunderous Charge": (
        "During an Assault phase in which Eidolon charges, attacks made with his Thunder Hammer are resolved at Initiative "
        "5 instead of Initiative 1. This Initiative value already includes any Initiative bonus gained for charging and "
        "may not be further increased."),
    "Command Retinue (Eidolon)": (
        "Eidolon may select one Legion Honour Guard Squad. An Honour Guard Squad selected for Eidolon may purchase Jump "
        "Packs for +15 points per model; if it does so, the unit becomes Jump Infantry and may not select a Dedicated "
        "Transport. The Honour Guard does not occupy a separate Force Organisation slot and Eidolon and his Honour Guard "
        "count as a single HQ selection."),
    "Hardened Survivor": (
        "Saul Tarvitz and any unit he has joined improve any Cover Save they receive by 1, to a maximum of 4+. This rule "
        "does not grant a Cover Save to a unit which would not otherwise receive one. In addition, while Tarvitz and his "
        "unit are controlling an Objective, they have the Fearless special rule."),
    "Honour or Death (Lucius)": (
        "If Lucius is in base contact with one or more enemy Independent Characters, he must direct all of his "
        "close-combat attacks against one of those Characters. When attacking an enemy Independent Character in close "
        "combat, Lucius may re-roll failed To Hit and To Wound rolls."),
    "Command Retinue (Lucius)": (
        "Lucius may select one Legion Command Squad. The Command Squad does not occupy a separate Force Organisation slot. "
        "Lucius and the Command Squad count as a single HQ selection, but do not have to deploy together and operate as "
        "separate units during the battle."),
    "Enhanced Warriors": (
        "If an Emperor's Children army includes Fabius Bile, any number of Emperor's Children Infantry squads (including "
        "Jump Infantry, but not retinues) with the Legiones Astartes special rule may be enhanced for +3 points per model "
        "(units wearing Terminator Armour may not be enhanced). After deployment but before the first turn begins, roll a D6 separately for each enhanced squad: "
        "1 - Berserk Rage: make an Armour Save for every model in the squad, remove any model which fails as a casualty; "
        "the survivors gain +1 Strength for the remainder of the battle. 2-5 - Stable Mutation: every model gains +1 "
        "Strength and +1 Initiative for the remainder of the battle. 6 - Created a Monster: every model gains +1 Strength, "
        "+1 Initiative and +1 Attack for the remainder of the battle; however, in missions using Victory Points, every "
        "model from the squad which survives the battle counts as a casualty when calculating Victory Points."),
    "Ancient of Rites": (
        "Once per player turn, when Rylanor suffers a Glancing or Penetrating Hit which is not ignored by Atomantic "
        "Shielding, the Emperor's Children player may force the opponent to re-roll the resulting Vehicle Damage roll "
        "(the second result must be accepted). In addition, if the mission requires a dice roll to determine which player "
        "takes the first turn, an Emperor's Children army containing Rylanor may re-roll that roll once."),
    "Living Icon of the Legion": (
        "Friendly Emperor's Children units with at least one model within 6\" of Rylanor automatically pass Morale tests "
        "(this does not cause them to automatically pass Pinning tests). If Rylanor is destroyed, every friendly "
        "Emperor's Children unit with line of sight to him must immediately take a Pinning test at -1 Leadership."),
    "Dreadnought Drop Pod (Rylanor)": ("Rylanor may select a Legion Dreadnought Drop Pod as a Dedicated Transport like "
                                       "any other Dreadnought."),
    # Fulgrim
    "Gilded Panoply": ("Counts as Primarch Armour, except that Fulgrim has a 5+ Invulnerable Save against ranged attacks "
                       "and a 3+ Invulnerable Save against attacks made in close combat."),
    "Fireblade": "A Master-crafted Power Weapon. Attacks made with it are resolved at +1 Strength and have Shred.",
    "The Blade of the Laer": ("A Master-crafted, Two-Handed Power Weapon. Attacks made with it are resolved at Fulgrim's "
                              "normal Strength and have the Fleshbane special rule."),
    "Sublime Swordsman": ("When Fulgrim directs close combat attacks against an enemy model with Weapon Skill 6 or "
                          "higher, he may re-roll To Hit rolls of 1."),
    "Perfect Execution": ("During an Assault phase in which Fulgrim charged, increase his Initiative and Attacks "
                          "characteristics by +1 for that Assault phase."),
    "Sire of Perfection": (
        "Once during each player turn, when a friendly Emperor's Children unit within 12\" of Fulgrim is selected to shoot "
        "or fight in close combat, Fulgrim may invoke this rule. That unit may re-roll To Hit rolls of 1 for the remainder "
        "of that phase."),
    "Pride of the Phoenician": (
        "When Fulgrim fights an enemy Independent Character or Primarch in close combat, compare their Weapon Skill "
        "characteristics. For each point by which Fulgrim's Weapon Skill exceeds that model's Weapon Skill, Fulgrim gains "
        "+1 Attack when directing attacks against that model, to a maximum of +2 Attacks."),
    "Primarch Retinue (Fulgrim)": (
        "Fulgrim may select a Legion Honour Guard Squad, a Legion Terminator Command Squad or a Phoenix Terminator Squad "
        "as his Primarch Retinue. It does not occupy an additional Force Organisation selection and otherwise follows the "
        "normal Primarch Retinue rules."),
    # Fulgrim Transfigured
    "Wings (Fulgrim Transfigured)": ("Fulgrim may move up to 12\" during the Movement phase and may move over intervening "
                                     "models and terrain while doing so. Fulgrim may never join another unit and no "
                                     "model may join him."),
    "Blade of the Laer (Transfigured)": ("A Master-crafted Power Weapon. Fulgrim may re-roll To Wound rolls of 1 made "
                                         "with the Blade of the Laer."),
    "Daemon Spear": ("A Two-Handed Power Weapon which grants Fulgrim +2 Strength and Armourbane. Fulgrim chooses which "
                     "weapon he uses at the beginning of each Assault phase."),
    "The Stage is Set": (
        "Fulgrim may never begin the battle on the battlefield and must begin in Reserve. Beginning on Turn 2, roll for "
        "Fulgrim using the normal Reserve rules; if successful, Fulgrim must enter play that turn. If he has not "
        "previously arrived, he enters play automatically on Turn 4. When Fulgrim enters play he must move onto the "
        "battlefield from his controlling player's own table edge. He may not Deep Strike or Outflank."),
    "Only the Worthy": (
        "When Fulgrim attempts to declare a charge against a non-Vehicle unit, determine the highest Weapon Skill amongst "
        "the models in that unit: WS 4 or lower - Fulgrim may not charge the unit; WS 5 - on a 3+ Fulgrim may charge "
        "normally (if the roll fails he may attempt to charge another eligible unit); WS 6 or higher - Fulgrim may charge "
        "normally. If no enemy models with WS 5 or greater remain on the battlefield, Fulgrim ignores this rule for the "
        "remainder of the battle. This rule does not prevent enemy units from charging Fulgrim."),
    "The Phoenician's Pride": (
        "If Fulgrim is engaged with an enemy unit containing one or more Independent Characters, he must allocate all of "
        "his close-combat attacks against a single eligible Independent Character of his choice. Treat the chosen "
        "Independent Character as a separate target; Fulgrim uses that model's own Weapon Skill and Toughness when "
        "resolving his attacks. All Wounds caused must be allocated to that model; any excess Wounds are lost. Fulgrim may "
        "not divide his attacks between the Independent Character and the remainder of the unit. Enemy Independent "
        "Characters are not required to attack Fulgrim."),
    "A Perfect Victory": ("If Fulgrim personally slays an enemy Independent Character during the Assault phase and the "
                          "enemy subsequently Falls Back, Fulgrim may not Pursue. He may Consolidate normally."),
    "The Phoenician's Favour": (
        "If Fulgrim Transfigured is included in an Emperor's Children army, the following may purchase the Blessing of "
        "Slaanesh (Traitor only): Emperor's Children Infantry unit (including Jump Infantry and retinues) +25 points per "
        "unit; Emperor's Children Independent Character (including named Independent Characters) +20 points per model. Models with the Blessing of Slaanesh gain +1 Initiative (cumulative with other Initiative "
        "modifiers). Fulgrim himself does not gain this bonus."),
    "Blessing of Slaanesh": ("Models with the Blessing of Slaanesh gain +1 Initiative. This bonus is cumulative with other "
                             "Initiative modifiers. (Only while Fulgrim Transfigured is in the army.)"),
    "Fulgrim Transfigured Restrictions": (
        "Fulgrim Transfigured may only be selected for an Emperor's Children army. An army may not include both Fulgrim "
        "Transfigured and Fulgrim in his mortal form."),
}

WEAPONS_ = {
    "Phoenix Spear": ("-", "User", "-", "Power Weapon, Two-Handed, Phoenix Strike"),
    "Doom Siren": ("Template", "5", "4", "Assault 1"),
    "Blastmaster": ('48"', "8", "3", "Heavy 1, Blast"),
    "Master-crafted Thunder Hammer": ("-", "x2", "-", "Power Weapon, Unwieldy, Specialist Weapon, Concussive, "
                                                      "Master-crafted"),
    "Master-crafted Power Weapon": ("-", "User", "-", "Ignores Armour Saves, Master-crafted"),
    "Fireblade": ("-", "User +1", "-", "Power Weapon, Master-crafted, Shred"),
    "The Blade of the Laer": ("-", "User", "-", "Power Weapon, Master-crafted, Two-Handed, Fleshbane"),
    "Firebrand": ('15"', "5", "5", "Assault 2, Rending, Master-crafted"),
    "Blade of the Laer (Transfigured)": ("-", "User", "-", "Power Weapon, Master-crafted, re-roll To Wound rolls of 1"),
    "Daemon Spear": ("-", "User +2", "-", "Power Weapon, Two-Handed, Armourbane"),
}
MULTI = {
    "Sonic Blaster": {"Sonic Blaster - Assault": ('24"', "4", "5", "Assault 2"),
                      "Sonic Blaster - Heavy": ('24"', "4", "5", "Heavy 3")},
}
WEAPON_RULES_ = {
    "Phoenix Spear": ["Phoenix Strike", "Two-Handed"],
    "Master-crafted Thunder Hammer": ["Master-Crafted", "Concussive", "Unwieldy"],
    "Master-crafted Power Weapon": ["Master-Crafted"],
    "Fireblade": ["Fireblade", "Master-Crafted", "Shred"],
    "The Blade of the Laer": ["The Blade of the Laer", "Master-Crafted", "Two-Handed", "Fleshbane"],
    "Firebrand": ["Rending", "Master-Crafted"],
    "Blade of the Laer (Transfigured)": ["Blade of the Laer (Transfigured)", "Master-Crafted"],
    "Daemon Spear": ["Daemon Spear", "Two-Handed", "Armourbane"],
}
WARGEAR_ = {
    "Digital Lasers": RULES["Digital Lasers"],
    "Sonic Shrieker": RULES["Sonic Shrieker"],
    "The Chirurgeon": "The Chirurgeon grants Fabius Bile a 4+ Invulnerable Save.",
    "Gilded Panoply": (RULES["Gilded Panoply"], ["Primarch Armour"]),
    "Transfigured Panoply": ("Fulgrim Transfigured's armour: 2+ Armour Save and 4+ Invulnerable Save as shown in his "
                             "profile. The army book gives no further rules for it."),
}

# names of existing units used below
SONIC_ASSAULT_UNITS = ["Legion Tactical Squad", "Legion Assault Squad", "Legion Veteran Squad", "Legion Destroyer Squad",
                       "Legion Seeker Squad", "Legion Heavy Support Squad", "Legion Command Squad",
                       "Legion Honour Guard Squad", "Palatine Blade Squad", "Kakophoni Squad", "Sun Killer Squad"]
RETINUES = ["Legion Command Squad", "Legion Honour Guard Squad"]
ENHANCED_UNITS = [n for n in SONIC_ASSAULT_UNITS if n not in RETINUES] + ["Legion Breacher Siege Squad",
                                                                          "Legion Reconnaissance Squad"]
BLESSING_UNITS = ENHANCED_UNITS + RETINUES + ["Legion Terminator Squad", "Legion Terminator Command Squad",
                                              "Phoenix Terminator Squad"]


def register():
    ARMY_RULES.update(RULES)
    register_data(weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_, multi_profile=MULTI)
    WEAPON_RULES["Sonic Blaster"] = []
    # "Doom Siren and Bolt Pistol" for the Cacophonic Champion
    WEAPONS["Doom Siren and Bolt Pistol"] = ["Doom Siren", "Bolt Pistol"]


# ------------------------------------------------------------------ local helpers
def _unit_type(e):
    ps = e.find("profiles")
    if ps is None:
        return None
    for p in ps:
        if p.get("typeName") == "Unit":
            for c in p.iter("characteristic"):
                if c.get("name") == "Unit Type":
                    return c.text or ""
    return None


def is_character(e):
    t = _unit_type(e)
    return bool(t) and "Character" in t


def find_group(e, name):
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == name:
            return g
    return None


def find_entry(e, name):
    for x in e.iter("selectionEntry"):
        if x.get("name") == name:
            return x
    return None


def entries_named(ctx, name):
    return [e for e in ctx.all_entries() if e.get("name") == name]


def hide_unless(eid, conds_hide):
    """Hide an option entry and set its max to 0 while any of conds_hide is true."""
    return [modifier("set", "hidden", "true", groups=[any_of(*conds_hide)]),
            modifier("set", uid(eid, "max"), 0, groups=[any_of(*conds_hide)])]


def phoenix_spear_variant(roots, skip_names=()):
    """Phoenix Spear: next to every Power Weapon option of a Character model (Power Weapon cost +5; +5 where the
    Power Weapon is its basic wargear, i.e. a free default). Fixed Power Weapons of Character models become a 'Replace Power Weapon'
    choice offering the spear for +5."""
    base_id = W("Power Weapon")
    done = set()
    n = 0
    for r in roots:
        for e in list(r.iter("selectionEntry")):
            if not is_character(e) or e.get("name") in skip_names or id(e) in done:
                continue
            done.add(id(e))
            # fixed Power Weapon -> replaceable
            own = e.find("entryLinks")
            if own is not None:
                for lk in list(own):
                    if lk.get("targetId") == base_id:
                        own.remove(lk)
                        add_to(e, "selectionEntryGroups", [slot(uid(e.get("id"), "ec-spear"), "Replace Power Weapon",
                                                                "Power Weapon", [("Phoenix Spear", 5)])])
                        n += 1
            for g in list(e.iter("selectionEntryGroup")):
                if id(g) in done:
                    continue
                done.add(id(g))
                links = g.find("entryLinks")
                if links is None:
                    continue
                if any(lk.get("targetId") == W("Phoenix Spear") for lk in links):
                    continue
                for lk in list(links):
                    if lk.get("targetId") != base_id:
                        continue
                    cs = lk.find("costs")
                    cost = float(cs[0].get("value")) if cs is not None and len(cs) else 0
                    nid = uid(lk.get("id"), "variant", "Phoenix Spear")
                    cons = []
                    if any(c.get("type") == "max" for c in lk.iter("constraint")):
                        cons = [constraint(uid(nid, "max"), "max", 1, auto=True)]
                    new_l = link(nid, W("Phoenix Spear"), "Phoenix Spear", cost=int(cost) + 5,
                                 constraints=cons)
                    if g.get("defaultSelectionEntryId") is not None:
                        new_l.set("sortIndex", str(int(lk.get("sortIndex") or 1) + 100))
                    links.append(new_l)
                    n += 1
    return n


def model(u, name, cost, mn, mx, utype, stats, kit, groups=(), mods=(), rules_=(), prof_mods=()):
    mid = uid("model", u, name)
    prof = unit_profile(u, name, utype, *stats)
    if prof_mods:
        prof.insert(0, wrap("modifiers", list(prof_mods)))
    return mid, entry(mid, name, typ="model", cost=cost, mods=list(mods),
                      constraints=[constraint(uid(mid, "min"), "min", mn), constraint(uid(mid, "max"), "max", mx)],
                      profiles=[prof], links=[gear(mid, k) for k in kit],
                      groups=list(groups), infolinks=rules_links(list(rules_), key=mid))


def unit_type_mod(new_type, conds):
    return modifier("set", gs.char_id("Unit", "Unit Type"), new_type, conds=conds)


# ------------------------------------------------------------------ units
PALATINE = uid("unit", "Palatine Blade Squad")
PHOENIX = uid("unit", "Phoenix Terminator Squad")
KAKOPHONI = uid("unit", "Kakophoni Squad")
SUN_KILLERS = uid("unit", "Sun Killer Squad")


def palatine_blades():
    u = PALATINE
    jp_id = uid("squadwide", u, "Jump Packs (entire squad)")
    jp_on = [has(jp_id, u)]
    kit = ["Artificer Armour", "Frag Grenades"]
    bid, blades = model(u, "Palatine Blade", 30, 4, 9, "Infantry", (5, 4, 4, 4, 1, 4, 2, 9, "2+"),
                        kit + ["Bolt Pistol", "Rending Weapon"], prof_mods=[unit_type_mod("Jump Infantry", jp_on)])
    pid = uid("model", u, "Palatine Primus")
    _, primus = model(u, "Palatine Primus", 0, 1, 1, "Infantry (Character)", (5, 4, 4, 4, 1, 5, 3, 9, "2+"), kit,
                      prof_mods=[unit_type_mod("Jump Infantry (Character)", jp_on)],
                      groups=[take(pid, "Wargear", [("Combat Shield", 5), ("Melta Bombs", 5)]),
                              pa_armoury(pid, u, 10, slots=["Bolt Pistol", "Rending Weapon"],
                                         skip=("Combat Shield", "Melta Bombs", "Artificer Armour"))])
    return entry(u, "Palatine Blade Squad", typ="unit", cost=150 - 4 * 30, cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links([LR, "Duelists", "Palatine Jump Packs"], key=u),
                 entries=[primus, blades, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Jump Packs (entire squad)", 15, u, ["Jump Pack"])],
                 groups=[model_swaps(u, "Palatine Blades: replace Rending Weapon (any number)", u, [bid],
                                     [("Power Weapon", 10)]),
                         model_takes(u, "Palatine Blades: wargear (any number)", u, [bid],
                                     [("Combat Shield", 5), ("Melta Bombs", 5)]),
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos",
                                           "Land Raider Proteus"],
                                    block_if=jp_on)])


def phoenix_terminators(key="Phoenix Terminator Squad", root=True):
    u = uid("unit", key)
    kit = ["Tartaros Terminator Armour", "Phoenix Spear"]
    _, terms = model(u, "Phoenix Terminator", 45, 4, 9, "Infantry", (5, 4, 4, 4, 1, 5, 2, 9, "2+/5+"), kit)
    cid = uid("model", u, "Phoenix Champion")
    _, champ = model(u, "Phoenix Champion", 0, 1, 1, "Infantry (Character)", (5, 4, 4, 4, 1, 5, 3, 10, "2+/5+"), kit,
                     groups=[take(cid, "Champion Wargear", [("Grenade Harness", 10)])])
    return entry(u, "Phoenix Terminator Squad", typ="unit", cost=235 - 4 * 45,
                 cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links([LR, "Implacable Advance", "Stubborn"] + ([] if root else ["Retinue"]), key=u),
                 entries=[champ, terms],
                 groups=[take(u, "One Phoenix Terminator may take", [("Doom Siren", 15)]),
                         transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                                    orbital=False)])


def kakophoni():
    u = KAKOPHONI
    kit = ["Power Armour", "Frag Grenades"]
    kid, kak = model(u, "Kakophoni", 25, 5, 11, "Infantry", (4, 4, 4, 4, 1, 5, 1, 10, "3+"), kit + ["Sonic Blaster"])
    cid = uid("model", u, "Cacophonic Champion")
    siren = entry(uid(cid, "siren"), "Doom Siren and Bolt Pistol", links=[gear(uid(cid, "siren"), "Doom Siren"),
                                                                         gear(uid(cid, "siren"), "Bolt Pistol")])
    _, champ = model(u, "Cacophonic Champion", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 5, 2, 10, "3+"), kit,
                     groups=[slot(cid, "Replace Sonic Blaster", "Sonic Blaster", [(siren, None)]),
                             take(cid, "Champion Wargear", [("Power Weapon", 10), ("Power Fist", 15),
                                                            ("Melta Bombs", 5)])])
    blast, _ = pool(u, "Kakophoni: replace Sonic Blaster with Blastmaster (1 per 3 models)", u, [("Blastmaster", 15)],
                    0, every=3)
    on = [rite("3rd Company Elite")]
    e = entry(u, "Kakophoni Squad", typ="unit", cost=150 - 5 * 25, cats=[foc(HS, "Heavy Support", u)],
              mods=[modifier("set-primary", "category", TROOPS, conds=on),
                    modifier("remove", "category", HS, conds=on),
                    modifier("add", "category", gs.CAT_LINE, conds=on)],
              infolinks=rules_links([LR, "Fearless", "Cacophony", "Selected as Troops (3rd Company Elite)"], key=u),
              entries=[champ, kak, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
              groups=[blast, transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                               "Land Raider Phobos"], max_models=10)])
    return allegiance_only(e, loyalist=False)


def sun_killers():
    u = SUN_KILLERS
    kit = ["Power Armour", "Bolt Pistol", "Frag Grenades"]
    _, sk = model(u, "Sun Killer", 50, 4, 9, "Infantry", (4, 5, 4, 4, 1, 4, 1, 9, "3+"), kit)
    pid = uid("model", u, "Sun Killer Prefector")
    _, pref = model(u, "Sun Killer Prefector", 0, 1, 1, "Infantry (Character)", (4, 5, 4, 4, 1, 4, 2, 10, "3+"), kit,
                    groups=[take(pid, "Prefector Wargear", [("Artificer Armour", 10), ("Melta Bombs", 5)])])
    gid = uid("grp", u, "energy")
    ents = []
    for n, minus in [("Lascannon", 0), ("Plasma Cannon", 5), ("Volkite Culverin", 15)]:
        eid = uid("choice", u, "energy", n)
        mods = [modifier("decrement", PTS, minus, repeats=[repeat("model", u, 1)])] if minus else []
        ents.append(entry(eid, f"{n}s (every model)", mods=mods, links=[gear(eid, n)],
                          constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)]))
    heavy = group(gid, "Heavy Weapon (entire squad)", entries=ents, default=ents[0].get("id"),
                  constraints=[constraint(uid(gid, "min"), "min", 1, auto=True),
                               constraint(uid(gid, "max"), "max", 1, auto=True)])
    return entry(u, "Sun Killer Squad", typ="unit", cost=250 - 4 * 50, cats=[foc(HS, "Heavy Support", u)],
                 infolinks=rules_links([LR, "Exemplary Marksmen", "Energy Weapons (Sun Killers)"], key=u),
                 entries=[pref, sk, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
                 groups=[heavy, transports(u, u, ["Legion Rhino Armoured Carrier"])])


RYLANOR = uid("unit", "Rylanor the Unyielding")


def rylanor():
    u = RYLANOR
    dp = uid("grp", u, "transport")
    return entry(u, "Rylanor the Unyielding", typ="unit", cost=225, cats=[foc(ELITES, "Elites", u)],
                 constraints=[unique(u)],
                 profiles=[walker_profile(u, "Rylanor the Unyielding", 6, 5, 7, 13, 12, 10, 4, 3)],
                 infolinks=rules_links([LR, "Crusader", "Atomantic Shielding", "Fleet", "Ancient of Rites",
                                        "Living Icon of the Legion", "Dreadnought Drop Pod (Rylanor)"], key=u),
                 links=[gear(u, k) for k in ["Kheres Assault Cannon", "Dreadnought Close Combat Weapon", "Heavy Flamer",
                                             "Smoke Launchers", "Searchlight"]],
                 groups=[group(dp, "Dedicated Transport",
                               links=[link(uid("link", dp, "Legion Dreadnought Drop Pod"),
                                           L2.T["Legion Dreadnought Drop Pod"], "Legion Dreadnought Drop Pod")],
                               constraints=[constraint(uid(dp, "max"), "max", 1, auto=True)])])


# ------------------------------------------------------------------ characters
EIDOLON = uid("unit", "Lord Commander Eidolon")
TARVITZ = uid("unit", "Saul Tarvitz")
LUCIUS = uid("unit", "Captain Lucius")
BILE = uid("unit", "Fabius Bile")


def eidolon_honour_guard():
    hg = L2.honour_guard("eidolon")
    hid = hg.get("id")
    jp = per_model("eidolon-hg", "Jump Packs (entire squad)", 15, hid, ["Jump Pack"])
    jp_id = jp.get("id")
    add_to(hg, "selectionEntries", [jp])
    add_to(hg, "infoLinks", rules_links(["Command Retinue (Eidolon)"], key=hid + "ec"))
    tr = find_group(hg, "Dedicated Transport")
    mx = uid(tr.get("id"), "max")
    add_mods(tr, [modifier("set", mx, 0, conds=[has(jp_id, hid)]),
                  modifier("set", "hidden", "true", conds=[has(jp_id, hid)])])
    for p in list(hg.iter("profile")):
        types = [c.text for c in p.iter("characteristic") if c.get("name") == "Unit Type"]
        if types:
            p.insert(0, wrap("modifiers", [unit_type_mod("Jump " + types[0], [has(jp_id, hid)])]))
    return hg


def ic_extras(u, krak=True, shrieker=True):
    """Digital Lasers (+15) and, Traitor only, a Sonic Shrieker (+10) for a named Independent Character."""
    items = ([("Krak Grenades", 2)] if krak else []) + [("Digital Lasers", 15)]
    out = [take(u, "Wargear", items)]
    if shrieker:
        out.append(take(u, "Sonic Shrieker (Traitor only)", [("Sonic Shrieker", 10)],
                        hide=[cond(LOYALIST, "roster", "atLeast", 1)]))
    return out


def characters():
    out = []
    out.append(named_character(
        LR, "Lord Commander Eidolon", 225, (6, 5, 4, 4, 3, 5, 3, 10, "2+/4+"),
        ["Artificer Armour", "Iron Halo", "Jump Pack", "Master-crafted Thunder Hammer", "Doom Siren", "Bolt Pistol",
         "Krak Grenades"],
        ["Thunderous Charge", "Command Retinue (Eidolon)"],
        retinue=retinue_links("eidolon", [eidolon_honour_guard()]), unit_type="Jump Infantry (Character)",
        extra_groups=ic_extras(EIDOLON, krak=False)))
    out.append(named_character(
        LR, "Saul Tarvitz", 115, (5, 5, 4, 4, 2, 5, 3, 9, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Rending Weapon", "Sniper Rifle", "Frag Grenades"],
        ["Hardened Survivor"], master=False,
        extra_groups=ic_extras(TARVITZ, shrieker=False)))
    out.append(named_character(
        LR, "Captain Lucius", 130, (7, 5, 4, 4, 2, 5, 3, 9, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Master-crafted Power Weapon", "Bolt Pistol", "Frag Grenades"],
        ["Honour or Death (Lucius)", "Command Retinue (Lucius)"], master=False,
        retinue=retinue_links("lucius", [command_squad_for("lucius", LUCIUS)]),
        extra_groups=ic_extras(LUCIUS)))
    out.append(named_character(
        LR, "Fabius Bile", 125, (5, 4, 4, 4, 3, 4, 2, 9, "3+/4+"),
        ["Power Armour", "The Chirurgeon", "Rending Weapon", "Frag Grenades"],
        ["Enhanced Warriors"], master=False,
        extra_groups=ic_extras(BILE)))
    return out


FULGRIM = uid("unit", "Fulgrim, the Phoenician")
FULGRIM_T = uid("unit", "Fulgrim Transfigured")


def fulgrim():
    return primarch(LR, "Fulgrim, the Phoenician", 530, (8, 6, 6, 6, 6, 9, 6, 10, "1+"),
                    ["Gilded Panoply", "Firebrand"],
                    ["Primarch Armour", "Sublime Swordsman", "Perfect Execution", "Sire of Perfection",
                     "Pride of the Phoenician", "Primarch Retinue (Fulgrim)"],
                    retinue=primarch_retinue("fulgrim", extra=[phoenix_terminators("fulgrim-phoenix", root=False)]),
                    other=FULGRIM_T, profile_name="Fulgrim",
                    extra_groups=[slot(FULGRIM, "Sword (choose one)", "Fireblade", [("The Blade of the Laer", 0)])])


def fulgrim_transfigured():
    return primarch("Daemon Primarchs", "Fulgrim Transfigured", 600, (9, 6, 7, 7, 7, 9, 7, 10, "2+/4+"),
                    ["Blade of the Laer (Transfigured)", "Daemon Spear", "Transfigured Panoply"],
                    ["Daemon", "Fear", "Fearless", "Fleet", "Eternal Warrior", "Adamantium Will", "Master of the Legion",
                     "Wings (Fulgrim Transfigured)", "The Stage is Set", "Only the Worthy", "The Phoenician's Pride",
                     "A Perfect Victory", "The Phoenician's Favour", "Fulgrim Transfigured Restrictions"],
                    other=FULGRIM, unit_type="Monstrous Creature (Character)", loyalist=False, core=False,
                    profile_name="Fulgrim Transfigured")


# ------------------------------------------------------------------ Legion-wide options
def add_purity_above_all(ctx):
    """Apothecary upgrades for Veteran Sergeants (any number) and one Tactical/Assault Sergeant per army."""
    def apo_entry(eid, name, cons):
        return entry(eid, name, cost=25, typ="upgrade", constraints=cons,
                     links=[gear(eid, "Narthecium")],
                     infolinks=rules_links(["Apothecary (Purity Above All)"], key=eid),
                     groups=[take(eid, "Apothecary Wargear", [("Reductor", 5)])])

    vet = ctx.unit("Legion Veteran Squad")
    sgt = find_entry(vet, "Legion Veteran Sergeant")
    vid = uid("ec", "vet-apothecary")
    v = apo_entry(vid, "Upgrade to Apothecary (Purity Above All)", [constraint(uid(vid, "max"), "max", 1, auto=True)])
    add_to(sgt, "selectionEntries", [v])
    add_mods(sgt, [modifier("set", "name", "Legion Veteran Apothecary", conds=[has(vid, "self")])])

    # one Tactical or Assault Sergeant per army: one shared upgrade linked from both, limited over the roster
    sid = uid("ec", "line-apothecary")
    shared = apo_entry(sid, "Upgrade to Apothecary (Purity Above All, one per army)",
                       [constraint(uid(sid, "roster"), "max", 1, scope="roster", deep=True)])
    ctx.add_shared(shared)
    for unit, sname in [("Legion Tactical Squad", "Legion Tactical Sergeant"),
                        ("Legion Assault Squad", "Legion Assault Sergeant")]:
        s = find_entry(ctx.unit(unit), sname)
        lid = uid("link", s.get("id"), "ec-apothecary")
        add_to(s, "entryLinks", [link(lid, sid, shared.get("name"),
                                      constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])])
        add_mods(s, [modifier("set", "name", sname.replace("Sergeant", "Apothecary"), conds=[has(sid, "self")])])


def add_ic_wargear(ctx):
    """Digital Lasers, Sonic Shrieker (Traitor) in the Praetor/Centurion Armoury; one Sonic Weapon per army."""
    loyal = [cond(LOYALIST, "roster", "atLeast", 1)]
    # one Sonic Weapon for one Praetor or Centurion per army
    swid = uid("ec", "char-sonic")
    sgid = uid("grp", swid, "weapon")
    sonic = entry(swid, "Sonic Weapon (one Praetor, Centurion or Consul per army, Traitor only)", typ="upgrade",
                  constraints=[constraint(uid(swid, "roster"), "max", 1, scope="roster", deep=True)],
                  infolinks=rules_links(["Sonic Weaponry"], key=swid),
                  groups=[group(sgid, "Sonic Weapon", links=[
                      link(uid("link", sgid, n), W(n), n, cost=p) for n, p in [("Sonic Blaster", 15), ("Doom Siren", 20)]],
                      constraints=[constraint(uid(sgid, "min"), "min", 1, auto=True),
                                   constraint(uid(sgid, "max"), "max", 1, auto=True)])])
    ctx.add_shared(sonic)
    for name in ("Legion Praetor", "Legion Centurion"):
        e = ctx.unit(name)
        u = e.get("id")
        arm = find_group(e, "Space Marine Armoury (max 100 pts)")
        wg = find_group(arm, "Additional Wargear")
        links = wg.find("entryLinks")
        dl = uid("link", wg.get("id"), "ec", "Digital Lasers")
        ss = uid("link", wg.get("id"), "ec", "Sonic Shrieker")
        links.append(link(dl, W("Digital Lasers"), "Digital Lasers", cost=15,
                          mods=hide_unless(dl, [has(W("Terminator Honours"), u)]),
                          constraints=[constraint(uid(dl, "max"), "max", 1, auto=True)]))
        links.append(link(ss, W("Sonic Shrieker"), "Sonic Shrieker", cost=10, mods=hide_unless(ss, loyal),
                          constraints=[constraint(uid(ss, "max"), "max", 1, auto=True)]))
        for lk in links:
            if lk.get("targetId") == W("Terminator Honours"):
                add_mods(lk, [modifier("set", "hidden", "true", conds=[has(W("Digital Lasers"), u)])])
        add_mods(e, [modifier("add", "error", "Digital Lasers may not be combined with Terminator Honours.",
                              groups=[all_of(has(W("Digital Lasers"), u), has(W("Terminator Honours"), u))])])
        lid = uid("link", u, "ec-sonic")
        add_to(e, "entryLinks", [link(lid, swid, sonic.get("name"), mods=hide_unless(lid, loyal),
                                      constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])])


def cgroup(typ, conds=(), groups=()):
    """conditionGroup that may nest other condition groups (bsx.any_of/all_of only hold plain conditions)."""
    return el("conditionGroup", {"type": typ}, [wrap("conditions", list(conds)), wrap("conditionGroups", list(groups))])


def fewer_than_two(u, names):
    """True while unit u has fewer than two selections of the given items in total (for three item kinds)."""
    a, b, c = names
    lt = lambda k, v: cond(W(k), u, "lessThan", v)
    return cgroup("and", [lt(a, 2), lt(b, 2), lt(c, 2)],
                  [any_of(lt(a, 1), lt(b, 1)), any_of(lt(a, 1), lt(c, 1)), any_of(lt(b, 1), lt(c, 1))])


def add_sonic_weaponry(ctx):
    """Legion Heavy Support Squad: Sonic Weaponry toggle (one per Detachment, two with 3rd Company Elite)."""
    hs = ctx.unit("Legion Heavy Support Squad")
    u = hs.get("id")
    tid = uid("ec", "hs-sonic")
    fid = uid(tid, "force")
    loyal = [cond(LOYALIST, "roster", "atLeast", 1)]
    tog = entry(tid, "Sonic Weaponry (Traitor only)", typ="upgrade",
                mods=hide_unless(tid, loyal) + [modifier("increment", fid, 1, conds=[rite("3rd Company Elite")])],
                constraints=[constraint(uid(tid, "max"), "max", 1, auto=True),
                             constraint(fid, "max", 1, scope="force", deep=True)],
                infolinks=rules_links(["Sonic Weaponry"], key=tid))
    off = [lacks(tid, u)]
    sonic_names = ["Sonic Blaster", "Doom Siren", "Blastmaster"]
    sonic = take(u, "Sonic Weapons (replace Bolters; up to four Heavy and Sonic Weapons in total)",
                 [("Sonic Blaster", 15, 4), ("Doom Siren", 20, 4), ("Blastmaster", 35, 4)], max_total=4, hide=off)
    # Perfect Cacophony (Armoury): at least two Sonic Weapons in the squad
    pc = upgrade(u, "Perfect Cacophony (Fearless, at least two Sonic Weapons)", 20,
                 rules_=["Perfect Cacophony (Armoury)", "Fearless"])
    pcid = pc.get("id")
    off_pc = lambda: cgroup("or", [lacks(tid, u)], [fewer_than_two(u, sonic_names)])
    add_mods(pc, [modifier("set", "hidden", "true", groups=[off_pc()]),
                  modifier("set", uid(pcid, "max"), 0, groups=[off_pc()])])
    # Heavy and Sonic Weapons may be mixed, up to four in total
    heavy = find_group(hs, "Heavy Weapons (up to four models)")
    hmx = uid(heavy.get("id"), "max")
    add_mods(heavy, [modifier("decrement", hmx, 1, repeats=[repeat(W(k), u, 1)]) for k in sonic_names])
    add_to(hs, "selectionEntries", [tog, pc])
    add_to(hs, "selectionEntryGroups", [sonic])


def add_unit_options(ctx):
    """3rd Company Elite Sonic Shriekers, Fabius Bile's Enhanced Warriors, Fulgrim Transfigured's Blessing."""
    no_rite = [cond(rite_id("3rd Company Elite"), "force", "lessThan", 1)]
    no_bile = [cond(BILE, "roster", "lessThan", 1)]
    no_ft = [cond(FULGRIM_T, "roster", "lessThan", 1)]
    seen = set()
    for e in ctx.all_entries():
        n = e.get("name")
        if e.get("type") != "unit" or id(e) in seen:
            continue
        seen.add(id(e))
        u = e.get("id")
        new = []
        if n in SONIC_ASSAULT_UNITS:
            s = per_model(u + "ec", "Sonic Shriekers (every model, 3rd Company Elite)", 2, u, ["Sonic Shrieker"])
            add_mods(s, hide_unless(s.get("id"), no_rite))
            add_to(s, "infoLinks", rules_links(["Sonic Assault (3rd Company Elite)"], key=s.get("id")))
            new.append(s)
        if n in ENHANCED_UNITS:
            s = per_model(u + "ec", "Enhanced Warriors (Fabius Bile)", 3, u, [])
            add_mods(s, hide_unless(s.get("id"), no_bile))
            add_to(s, "infoLinks", rules_links(["Enhanced Warriors"], key=s.get("id")))
            new.append(s)
        if n in BLESSING_UNITS:
            new.append(upgrade(u + "ec", "Blessing of Slaanesh (Fulgrim Transfigured)", 25,
                               rules_=["Blessing of Slaanesh"], hide=no_ft))
        if n in ("Legion Praetor", "Legion Centurion") or u in (EIDOLON, TARVITZ, LUCIUS, BILE):
            new.append(upgrade(u + "ec", "Blessing of Slaanesh (Fulgrim Transfigured)", 20,
                               rules_=["Blessing of Slaanesh"], hide=no_ft))
        if new:
            add_to(e, "selectionEntries", new)


# ------------------------------------------------------------------ extend
def extend(ctx):
    ctx.legion_rules([LR, "Exemplars of War", "Crusader", "Purity Above All", "Martial Pride"])

    ctx.add_units(palatine_blades(), phoenix_terminators(), kakophoni(), sun_killers(), rylanor(), *characters(),
                  fulgrim(), fulgrim_transfigured())
    ctx.finish()  # new retinues become shared entries before the Legion-wide changes below

    add_purity_above_all(ctx)
    add_ic_wargear(ctx)
    add_sonic_weaponry(ctx)
    add_unit_options(ctx)
    phoenix_spear_variant(ctx.all_entries(), skip_names=("Captain Lucius", "Lord Commander Eidolon", "Saul Tarvitz",
                                                         "Fabius Bile", "Fulgrim, the Phoenician",
                                                         "Fulgrim Transfigured"))

    # Rites of War
    ctx.add_rite("The Maru Skara", RULES["The Maru Skara"], errors=[
        ("the army may include no more than two Heavy Support choices.", [cond(HS, "force", "greaterThan", 2)]),
        ("Immobile units (Fortifications) may not be selected.",
         [cond(gs.cat("Fortification"), "force", "atLeast", 1)]),
    ])
    ctx.add_rite("3rd Company Elite", RULES["3rd Company Elite"], errors=[
        ("only a Traitor Emperor's Children Detachment may use this Rite.", [cond(LOYALIST, "roster", "atLeast", 1)]),
        ("the army must include at least one Kakophoni Squad.", [cond(KAKOPHONI, "roster", "lessThan", 1)]),
        ("the army may include no more than one Fortification.",
         [cond(gs.cat("Fortification"), "roster", "greaterThan", 1)]),
    ])
