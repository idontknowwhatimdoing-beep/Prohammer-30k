"""XX Legion - Alpha Legion (Forces of the Legions)."""
from itertools import combinations

from legions.common import *  # noqa: F401,F403
from legions.common import (PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry,
                            link, group, category_link, gs, L, L2, W, has, lacks, gear, per_model, rules_links,
                            unit_profile, slot, take, pool, transports, add_mods, add_to, foc, rite, rite_id,
                            RETINUE_SHARED, TROOPS, ELITES, FA, HQ, HS, model_swaps, model_takes, pa_armoury,
                            specials_decrement, register_data, unique, force_limit, option, named_character, primarch,
                            primarch_retinue, retinue_links, command_squad_for, add_armoury_items, required_choice,
                            choice_id, clone)

LEGION = "XX - Alpha Legion"
LR = "Legiones Astartes (Alpha Legion)"

MUTABLE = [("Counter-Attack", ["Counter-Attack"]), ("Furious Charge", ["Furious Charge"]),
           ("Infiltrate", ["Infiltrate"]), ("Move Through Cover", ["Move Through Cover"]),
           ("Siege Specialists", ["Siege Specialists"]), ("Tank Hunters", ["Tank Hunters"])]

RULES = {
    LR: ("Models with this rule belong to the XX Legion and use the Alpha Legion Legion special rules: Mutable Tactics, "
         "Martial Hubris and Infiltration Network."),
    "Mutable Tactics": (
        "An Alpha Legion army must select one of the following Veteran Skills at the point where Warlord Traits are "
        "selected for the game: Counter-Attack, Furious Charge, Infiltrate, Move Through Cover, Siege Specialists or Tank "
        "Hunters. It applies to all qualifying non-vehicle units in the Detachment with Legiones Astartes (Alpha Legion) "
        "for the duration of the game, does not count towards the number of Veteran Skills a unit may have, and all "
        "normal restrictions of the selected skill continue to apply."),
    "Siege Specialists": ("A unit using Siege Specialists receives +1 to Armour Penetration rolls against Fortifications, "
                          "Buildings, Bunkers and other immobile structures with an Armour Value."),
    "Martial Hubris": ("In a mission using Victory Points, compare the number of completely destroyed units of each "
                       "player at the end of the battle. If more Alpha Legion units than enemy units have been completely "
                       "destroyed, the opposing player receives an additional D3 x 50 Victory Points. No effect if both "
                       "players lost the same number of units."),
    "Infiltration Network": (
        "Legion Operative units may be selected as Troops choices in an Alpha Legion Detachment. Up to two Legion "
        "Operative units may be selected without occupying a Troops selection. Legion Operatives may not be chosen as "
        "compulsory Troops. They must still be paid for normally and count as units for Martial Hubris."),
    # armoury
    "Banestrike": "A natural To Wound roll of 6 made with Banestrike Ammunition is resolved at AP3.",
    "Banestrike Ammunition": (
        "Alpha Legion Seeker Squads, Legion Veteran Squads and Independent Characters equipped with a Bolter, Foeblaster "
        "Boltgun, Combi-Bolter or Combi-Weapon may purchase Banestrike Ammunition for +5 points per eligible model; every "
        "eligible model in a squad must purchase it or none may. Bolters fire the Banestrike Bolter profile. With a "
        "Foeblaster Boltgun, Combi-Bolter or the Bolter component of a Combi-Weapon, keep the weapon's normal number of "
        "shots and firing type but use 18\" range, AP4 and the Banestrike special rule. Seeker Squads keep their Special "
        "Issue Ammunition and may choose to fire Banestrike Ammunition instead. May not be combined with another "
        "ammunition type."),
    "Power Dagger": ("Any Alpha Legion Character with access to the Space Marine Armoury may purchase a Power Dagger for "
                     "+5 points. It counts as a Power Weapon with the Rending and Specialist Weapon special rules; "
                     "attacks with it are resolved at -1 Strength."),
    "Legion Saboteur": ("One Alpha Legion Seeker Sergeant in the army may be upgraded to a Legion Saboteur for +25 "
                        "points. The Saboteur retains the profile, weapons and equipment of the model he replaces."),
    "Coordinated Sabotage": ("After Mutable Tactics has been selected, the Saboteur's squad may select one additional "
                             "Veteran Skill from the Mutable Tactics list at no additional cost. A skill already granted "
                             "by Mutable Tactics may not be selected again."),
    "Pre-emptive Strike": (
        "After both armies have deployed but before the first turn begins, nominate one enemy unit (no range or line of "
        "sight required). A non-Vehicle unit suffers D6 Strength 5 hits (Armour Saves allowed); if at least one casualty "
        "is caused it must take a Pinning test at -1 Leadership. A Vehicle: roll a D6 - 1-3 no effect, 4-5 one Glancing "
        "Hit, 6 one Penetrating Hit."),
    "Teleportation Transponders": ("The model or unit gains the Deep Strike special rule and may deploy using Deep Strike "
                                   "even if the mission would not normally permit it. An Independent Character intending "
                                   "to Deep Strike as part of another unit must purchase Teleportation Transponders "
                                   "separately."),
    # units
    "Operative Cell": ("Before deployment, select one skill set for the unit at no cost: Scouts (Infiltrate and Move "
                       "Through Cover), Assassins (Infiltrate and Furious Charge) or Saboteurs (Infiltrate and Siege "
                       "Specialists)."),
    "Human Agents": ("Legion Operatives do not possess Legiones Astartes and do not benefit from Mutable Tactics or other "
                     "rules which specifically affect Alpha Legion Space Marines."),
    "All as Planned": ("After both armies have deployed but before the first turn begins, the Headhunter Kill Team may "
                       "make one Pre-emptive Strike (see Legion Saboteur)."),
    "Hydra's Wail": ("Enemy units with at least one model within 12\" of an Effrit Disruption Cadre suffer -1 Leadership "
                     "when taking Pinning tests. Enemy Nuncio Voxes and Teleport Homers may not be used while their "
                     "bearer is within 12\" of an Effrit model."),
    "Hydra's Resilience": "While Sheed Ranko remains alive, his Lernaean Terminator Squad has the Stubborn special rule.",
    "Sheed Ranko": ("Sheed Ranko may replace one model in a Lernaean Terminator Squad (total cost 110 points: +62 in "
                    "addition to the replaced Lernaean Terminator). He remains part of the squad, is not an Independent "
                    "Character and does not occupy a separate Force Organisation choice."),
    # characters
    "Command Squad (Armillus Dynat)": ("Dynat may be accompanied by a Legion Command Squad, Legion Terminator Command "
                                       "Squad or Lernaean Terminator Squad; they count as a single HQ selection."),
    "The Harrowing": ("Dynat and any unit he has joined gain Counter-Attack. Models in that unit add +1 to Armour "
                      "Penetration rolls against Vehicles in close combat."),
    "Weapon Mastery": ("Dynat may divide his close-combat attacks between his Power Weapon and Thunder Hammer in any "
                       "combination, including bonus Attacks for charging or two close-combat weapons."),
    "Hammerstrike Assault": ("Dynat may grant any unit he joins Teleportation Transponders for +10 points for the whole "
                             "unit, even if it would normally not have access to them. Dynat's own Teleportation "
                             "Transponders are included in his cost."),
    "Kraken Bolts (Headhunters)": (
        "Headhunters may fire Kraken Bolts (or Banestrike Ammunition) from any Bolter, including the Bolter component of "
        "a Combi-weapon. A model that replaces its Bolter with a special weapon loses access to Kraken Bolts."),
    "Lone Killer (Exodus)": ("Exodus may never join another unit and no Independent Character may join him. He may not "
                             "fulfil a compulsory HQ selection and may never be the army's Warlord."),
    "Execute the Mandate": ("If the enemy Warlord is slain by an attack made by Exodus, the Alpha Legion player receives "
                            "an additional 50 Victory Points."),
    "Delegatus (Autilon Skorr)": "Autilon Skorr counts as a Legion Delegatus Consul for all rules and restrictions.",
    "Desperate for Glory": ("Once per battle, at the beginning of any Alpha Legion turn, Skorr may invoke Desperate for "
                            "Glory: until the beginning of the next Alpha Legion turn, Skorr and any unit he has joined "
                            "gain Fearless and Feel No Pain (5+)."),
    "Command Squad (Ingo Pech)": ("Pech may be accompanied by a Legion Command Squad, Legion Terminator Command Squad, "
                                  "Lernaean Terminator Squad or Legion Seeker Squad; they count as a single HQ "
                                  "selection."),
    "Master of Deceit": ("An army containing Ingo Pech may use The Rewards of Treachery rule of The Coils of the Hydra "
                         "Rite of War even if it is not using that Rite. If it already uses The Coils of the Hydra, Pech "
                         "does not permit a second Rewards of Treachery unit."),
    "False Disposition": ("After both armies have deployed but before determining who takes the first turn, nominate "
                          "Herzog and one other friendly non-Vehicle Alpha Legion unit; both may be redeployed anywhere "
                          "following the rules for infiltrating. Units in Reserve are not eligible."),
    "Headhunter Commander": ("One Headhunter Kill Team may be selected without occupying an Elites choice in an army "
                             "containing Mathias Herzog. That unit remains an Elites unit for all other purposes."),
    # Alpharius
    "Master of Lies": ("After both armies have deployed but before the first turn begins, nominate one friendly Alpha "
                       "Legion unit. It may be redeployed anywhere it could legally have been deployed at the beginning "
                       "of the battle (normal deployment restrictions; it may not be placed into Reserve unless it was "
                       "already eligible to begin in Reserve)."),
    "The Hydra": (
        "Before either army deploys, secretly record one enemy unit as the Priority Target. It need not be revealed until "
        "the first time a friendly Alpha Legion unit attacks it. Once revealed, friendly units with Legiones Astartes "
        "(Alpha Legion) may re-roll To Hit rolls of 1 when attacking the Priority Target (shooting and close combat)."),
    "Sire of the Alpha Legion": ("Friendly units with Legiones Astartes (Alpha Legion) with at least one model within 12\" "
                                 "of Alpharius may use his Leadership when taking Morale or Pinning tests."),
    "I Am Alpharius": (
        "Alpharius is not deployed normally and does not begin in Reserve. At the beginning of any Alpha Legion turn, "
        "nominate one friendly Infantry model on the battlefield with Legiones Astartes (Alpha Legion); remove it (it "
        "counts as a casualty) and place Alpharius as close as possible to its position with his full Wounds, wargear and "
        "rules. If the model was part of a unit, Alpharius joins it; if it was in close combat, so is he. He may Move, "
        "Shoot and charge normally that turn; no Reserve roll is required. If he has not been revealed when the battle "
        "ends, he counts as slain for Victory Points, Slay the Warlord and Price of Failure."),
    "Alpharius' Primarch Retinue": (
        "Alpharius may select a Legion Honour Guard Squad, Legion Terminator Command Squad or Lernaean Terminator Squad "
        "as his Primarch Retinue (no additional Force Organisation selection). The retinue deploys normally without him; "
        "he may use I Am Alpharius to replace one of its models and then joins it. A Lernaean Terminator Squad selected "
        "this way does not count against the 0-1 limit on Lernaean Terminator Squads."),
    # Rites of War
    "The Coils of the Hydra": (
        "EFFECTS - Subterfuge: before determining who takes the first turn, choose +1 to the roll for the first turn or "
        "a re-roll of a failed attempt to Seize the Initiative (before any dice are rolled). Signal Corruption: enemy "
        "Reserve rolls suffer -1 (not units entering play automatically on a specified turn). The Rewards of Treachery: "
        "the Detachment may include one Legion-specific unit normally available only to another Space Marine Legion (not "
        "a Primarch, named Character, Independent Character or Unique unit); it is an Elites choice paid for normally, "
        "keeps its profile, wargear, options and unit rules, but has Legiones Astartes (Alpha Legion) instead of its own "
        "Legion's rule.\nLIMITATIONS - One additional compulsory Troops choice (three in total). Every Infantry unit must "
        "have Infiltrate or Deep Strike, or have access to and purchase a Dedicated Transport (if a unit relies on Mutable "
        "Tactics, Infiltrate must be the army's Mutable Tactic). No more than one Centurion upgraded to a Consul "
        "(Vigilator Consuls do not count). No Fortification or Allied Detachment drawn from another Space Marine Legion."),
    "Headhunter Leviathal": (
        "EFFECTS - Headhunter Elite: Headhunter Kill Teams may be selected as Troops choices and must be used to fulfil "
        "the compulsory Troops selections; additional Headhunter Kill Teams may also be selected as Troops. Sudden "
        "Strike: the Alpha Legion player may re-roll the dice to determine who takes the first turn (the entire result; "
        "the second must be accepted). False Flags: during the first Game Turn, an enemy unit declaring a shooting attack "
        "against an Alpha Legion unit must first pass a Leadership test unless it has already been fired upon by an "
        "Alpha Legion unit during the current player turn; if failed it may not make that attack (not Overwatch, Return "
        "Fire or Stand & Shoot). Leave No Head upon the Serpent: if the enemy Warlord survives the battle, the opponent "
        "gains an additional D3 x 50 Victory Points (Victory Point missions only).\nLIMITATIONS - Every Alpha Legion "
        "Vehicle must begin the battle in Reserve unless the mission prohibits it. No Allied Detachment."),
}

WEAPONS = {
    "Power Dagger": ("-", "-1", "-", "Power Weapon, Rending, Specialist Weapon"),
    "Laspistol": ('12"', "3", "-", "Pistol"),
    "Autopistol": ('12"', "3", "-", "Pistol"),
    "Rime-shard": ("-", "+2", "-", "Power Weapon, Master-crafted, Two-Handed"),
    "Pale Spear": ("-", "User", "-", "Power Weapon, Two-Handed, Armourbane; Massive Wound (D3) vs non-Primarchs"),
    "Hydra's Spite": ('18"', "7", "2", "Assault 2, Gets Hot"),
}
MULTI = {
    "Banestrike Ammunition": {"Banestrike Bolter": ('18"', "4", "4", "Rapid Fire, Banestrike")},
    # Headhunter wargear: the Kraken Bolts profile of the base Special Issue Ammunition (no own profile in the book)
    "Kraken Bolts": {"Kraken Bolts": ('30"', "4", "4", "Rapid Fire")},
    "The Instrument": {"The Instrument - Rapid Shot": ('36"', "5", "4", "Salvo 2/3, Rending"),
                       "The Instrument - Execution Shot": ('36"', "6", "3",
                                                           "Heavy 1, Rending, Massive Wounds, Ignores Cover")},
}
WEAPON_RULES = {
    "Power Dagger": ["Power Dagger", "Rending"],
    "Banestrike Ammunition": ["Banestrike"],
    "The Instrument": ["Rending", "Ignores Cover"],
    "Rime-shard": ["Master-Crafted", "Two-Handed"],
    "Pale Spear": ["Two-Handed", "Armourbane"],
    "Hydra's Spite": ["Gets Hot"],
}
WARGEAR = {
    "Banestrike Ammunition": RULES["Banestrike Ammunition"],
    "Venom Spheres": ("The bearer gains the Hammer of Wrath special rule.", ["Hammer of Wrath"]),
    "Teleportation Transponders": (RULES["Teleportation Transponders"], ["Deep Strike"]),
    "Rime-shard": ("Counts as a Master-crafted Power Weapon; attacks are resolved at +2 Strength. Two-handed: no bonus "
                   "Attack for two close-combat weapons.", []),
    "Pale Spear": ("A Two-Handed Power Weapon resolved at Alpharius' normal Strength with Armourbane. Any unsaved Wound "
                   "it inflicts on a model without the Primarch special rule becomes a Massive Wound and inflicts D3 "
                   "Wounds instead of one.", []),
    "Pythian Scales": ("Count as Primarch Armour (1+ Armour Save, 4+ Invulnerable Save).", []),
}

BOLTERS = ["Bolter", "Foeblaster Boltgun", "Combi-Bolter", "Combi-Flamer", "Combi-Grenade Launcher", "Combi-Meltagun",
           "Combi-Plasma Gun", "Combi-Volkite Charger", "Combi-Weapon"]
COMBIS5 = [("Combi-Flamer", 5), ("Combi-Grenade Launcher", 5), ("Combi-Volkite Charger", 5), ("Combi-Meltagun", 10),
           ("Combi-Plasma Gun", 10)]
ARMOURY_COMBIS = [("Combi-Bolter", 5), ("Combi-Flamer", 10), ("Combi-Grenade Launcher", 10), ("Combi-Meltagun", 15),
                  ("Combi-Plasma Gun", 15), ("Combi-Volkite Charger", 10)]


def register():
    register_data(rules=RULES, weapons=WEAPONS, weapon_rules=WEAPON_RULES, wargear=WARGEAR, multi_profile=MULTI)
    # Headhunter Leviathal: the compulsory Troops must be Headhunter Kill Teams
    for n in ["Legion Tactical Squad", "Legion Assault Squad", "Legion Breacher Siege Squad"]:
        L2.NOT_LINE_UNDER[n].append("Headhunter Leviathal")


# ------------------------------------------------------------------ local helpers
def all_entries(ctx):
    seen, out = set(), []
    for e in ctx.all_entries():
        if id(e) not in seen:
            seen.add(id(e))
            out.append(e)
    return out


def child_model(unit, name):
    for e in unit.find("selectionEntries"):
        if e.get("name") == name:
            return e
    raise KeyError(name)


def one_per_army(entries, name):
    ids = [e.get("id") for e in entries]
    for e in entries:
        others = [cond(i, "roster", "atLeast", 1) for i in ids if i != e.get("id")]
        if others:
            add_mods(e, [modifier("add", "error", f"{name} may only be included once in an army.",
                                  groups=[any_of(*others)], conds=[cond(e.get("id"), "roster", "atLeast", 1)])])


def consul_limit_group(exclude=()):
    ids = [L.consul_id(c) for c in L.CONSULS if c not in exclude]
    singles = [cond(i, "force", "atLeast", 2) for i in ids]
    pairs = [all_of(cond(a, "force", "atLeast", 1), cond(b, "force", "atLeast", 1)) for a, b in combinations(ids, 2)]
    return el("conditionGroup", {"type": "or"}, [wrap("conditions", singles), wrap("conditionGroups", pairs)])


def ic_wargear(ctx, items):
    """Legion Armoury items for the Praetor/Centurion 'Additional Wargear' (counts towards the 100-pt cap)."""
    for n in ("Legion Praetor", "Legion Centurion"):
        u = ctx.unit(n)
        for g in u.iter("selectionEntryGroup"):
            if g.get("name") != "Additional Wargear":
                continue
            links = g.find("entryLinks")
            for name, pts, forbid in items:
                lid = uid("link", g.get("id"), "al", name)
                links.append(link(lid, W(name), name, cost=pts, mods=L.forbid_mods(lid, forbid(u.get("id"))),
                                  constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))


def req_gear_choice(key, title, options):
    """Required squad-wide wargear choice: error (no auto-pick) until one option is chosen.
    options: [(name, [wargear])]."""
    gid = uid("grp", key, title)
    ents = [entry(uid("choice", key, title, n), n, links=[gear(uid("choice", key, title, n), k) for k in kit],
                  constraints=[constraint(uid("choice", key, title, n, "max"), "max", 1, auto=True)])
            for n, kit in options]
    none = all_of(*[cond(e.get("id"), "parent", "lessThan", 1) for e in ents])
    return group(gid, title, entries=ents, constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)],
                 mods=[modifier("add", "error", f"Choose: {title}.", groups=[none])])


def banestrike_squad(key, unit_id, not_eligible):
    """'+5 points per eligible model, all or none': +5 per model, -5 per model carrying a non-bolter weapon."""
    eid = uid("banestrike", key)
    mods = [modifier("increment", PTS, 5, repeats=[repeat("model", unit_id, 1)])]
    mods += [modifier("decrement", PTS, 5, repeats=[repeat(W(n), unit_id, 1)]) for n in not_eligible]
    return entry(eid, "Banestrike Ammunition (every eligible model)", cost=0, mods=mods,
                 constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                 links=[gear(eid, "Banestrike Ammunition")])


def dt_option(key, cost=15, title="Teleportation Transponders (entire squad)"):
    return option(key, title, cost, item="Teleportation Transponders")


# ------------------------------------------------------------------ units
OPERATIVES = uid("unit", "Legion Operatives")


def operatives():
    name = "Legion Operatives"
    u = OPERATIVES
    oid, lid = uid("model", u, "Legion Operative"), uid("model", u, "Operative Leader")
    omin, omax = uid(oid, "min"), uid(oid, "max")
    ops = entry(oid, "Legion Operative", typ="model", cost=6, mods=specials_decrement(oid, omin, omax, [lid], u),
                constraints=[constraint(omin, "min", 10, auto=True), constraint(omax, "max", 20, auto=True)],
                profiles=[unit_profile(u, "Operative", "Infantry", 3, 3, 3, 3, 1, 3, 1, 7, "6+")],
                links=[gear(oid, "Close Combat Weapon")])
    gid = uid("grp", lid, "armoury-weapons")
    wlinks = [link(uid("link", gid, n), W(n), n, cost=p,
                   constraints=[constraint(uid("link", gid, n, "max"), "max", 1, auto=True)])
              for n, p, *_ in L.PA_SGT_WEAPONS if p <= 10] + \
        [link(uid("link", gid, "Power Dagger"), W("Power Dagger"), "Power Dagger", cost=5,
              constraints=[constraint(uid("link", gid, "Power Dagger", "max"), "max", 1, auto=True)])]
    leader = entry(lid, "Operative Leader (+5)", typ="model", cost=11,
                   constraints=[constraint(uid(lid, "max"), "max", 1)],
                   profiles=[unit_profile(u, "Operative Leader", "Infantry (Character)", 3, 3, 3, 3, 1, 3, 2, 8, "6+")],
                   links=[gear(lid, "Close Combat Weapon")],
                   groups=[group(gid, "Space Marine Armoury weapons (max 10 pts)", links=wlinks,
                                 constraints=[constraint(uid(gid, "maxpts"), "max", 10, scope="self", field=PTS,
                                                         deep=True)])])
    tog = uid(u, "network")
    network = entry(tog, "Infiltration Network (does not occupy a Troops selection)",
                    constraints=[constraint(uid(tog, "max"), "max", 1, auto=True),
                                 constraint(uid(tog, "force"), "max", 2, scope="force", deep=True)],
                    infolinks=rules_links(["Infiltration Network"], key=tog))
    return entry(u, name, typ="unit", cost=60 - 10 * 6, cats=[foc(TROOPS, "Troops", u)],
                 mods=[modifier("add", "category", gs.FOC_PLUS["Troops"], conds=[cond(tog, "self", "atLeast", 1)])],
                 infolinks=rules_links(["Operative Cell", "Human Agents", "Infiltration Network"], key=u),
                 entries=[ops, leader, network,
                          per_model(u, "Frag Grenades (entire unit)", 1, u, ["Frag Grenades"]),
                          per_model(u, "Krak Grenades (entire unit)", 1, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire unit)", 2, u, ["Melta Bombs"])],
                 groups=[req_gear_choice(u, "Sidearms (entire unit)", [("Laspistols", ["Laspistol"]),
                                                                       ("Autopistols", ["Autopistol"])]),
                         required_choice(u, "Operative Cell", [
                             ("Scouts", ["Infiltrate", "Move Through Cover"]),
                             ("Assassins", ["Infiltrate", "Furious Charge"]),
                             ("Saboteurs", ["Infiltrate", "Siege Specialists"])])])


HERZOG = uid("unit", "Mathias Herzog")


def headhunters():
    name = "Headhunter Kill Team"
    u = uid("unit", name)
    hid, pid = uid("model", u, "Headhunter"), uid("model", u, "Headhunter Prime")
    kit = ["Power Armour", "Bolter", "Banestrike Ammunition", "Kraken Bolts", "Close Combat Weapon", "Frag Grenades",
           "Melta Bombs"]
    prime = entry(pid, "Headhunter Prime", typ="model",
                  constraints=[constraint(uid(pid, "min"), "min", 1), constraint(uid(pid, "max"), "max", 1)],
                  profiles=[unit_profile(u, "Headhunter Prime", "Infantry (Character)", 4, 5, 4, 4, 1, 4, 2, 9, "3+")],
                  links=[gear(pid, k) for k in kit],
                  groups=[slot(pid, "Replace Bolter", "Bolter", COMBIS5),
                          take(pid, "Headhunter Prime Wargear", [("Power Dagger", 5), ("Artificer Armour", 10),
                                                                 ("Venom Spheres", 5)]),
                          pa_armoury(pid, u, 10, slots=["Close Combat Weapon"],
                                     skip=("Artificer Armour", "Melta Bombs"))])
    hhs = entry(hid, "Headhunter", typ="model", cost=32,
                constraints=[constraint(uid(hid, "min"), "min", 4), constraint(uid(hid, "max"), "max", 9)],
                profiles=[unit_profile(u, "Headhunter", "Infantry", 4, 5, 4, 4, 1, 4, 1, 8, "3+")],
                links=[gear(hid, k) for k in kit])
    spec_opts = [("Heavy Flamer", 10), ("Meltagun", 10), ("Plasma Gun", 15), ("Multi-Melta", 25),
                 ("Heavy Bolter with Suspensor and Hellfire Rounds", 15)]
    specials, _ = pool(u, "Special Weapons (up to two Headhunters, replace Bolter)", u, spec_opts, 2)
    swaps = [model_swaps(u, "Headhunters: replace Bolter (any number)", u, [hid], COMBIS5,
                         minus=[W(n) for n, _ in spec_opts]),
             model_takes(u, "Headhunters: wargear (any number)", u, [hid], [("Power Dagger", 5)])]
    lev = [rite("Headhunter Leviathal")]
    tog = uid(u, "herzog")
    no_herzog = [cond(HERZOG, "roster", "lessThan", 1)]
    toggle = entry(tog, "Headhunter Commander (does not occupy an Elites choice)",
                   constraints=[constraint(uid(tog, "max"), "max", 1, auto=True),
                                constraint(uid(tog, "roster"), "max", 1, scope="roster", deep=True)],
                   mods=[modifier("set", "hidden", "true", groups=[any_of(no_herzog[0], *lev)]),
                         modifier("set", uid(tog, "max"), 0, groups=[any_of(no_herzog[0], *lev)])],
                   infolinks=rules_links(["Headhunter Commander"], key=tog))
    mods = [modifier("set-primary", "category", TROOPS, conds=lev),
            modifier("remove", "category", ELITES, conds=lev),
            modifier("add", "category", gs.CAT_LINE, conds=lev),
            modifier("increment", uid(u, "force-max"), 10, conds=lev),
            modifier("add", "category", gs.FOC_PLUS["Elites"], conds=[cond(tog, "self", "atLeast", 1)])]
    return entry(u, name, typ="unit", cost=160 - 4 * 32, cats=[foc(ELITES, "Elites", u)], mods=mods,
                 constraints=[force_limit(u)],
                 infolinks=rules_links([LR, "Infiltrate", "Move Through Cover", "All as Planned", "Pre-emptive Strike",
                                         "Kraken Bolts (Headhunters)"],
                                       key=u),
                 entries=[prime, hhs, toggle], groups=[*swaps, specials])


RANKO_ALL = []


def lernaeans(key="Lernaean Terminator Squad", root=True):
    name = "Lernaean Terminator Squad"
    u = uid("unit", key)
    tid, rid = uid("model", u, "Lernaean Terminator"), uid("model", u, "Sheed Ranko")
    tmin, tmax = uid(tid, "min"), uid(tid, "max")
    terms = entry(tid, "Lernaean Terminator", typ="model", cost=48, mods=specials_decrement(tid, tmin, tmax, [rid], u),
                  constraints=[constraint(tmin, "min", 5, auto=True), constraint(tmax, "max", 10, auto=True)],
                  profiles=[unit_profile(u, "Lernaean Terminator", "Infantry", 5, 5, 4, 4, 1, 3, 2, 9, "2+/4+")],
                  links=[gear(tid, k) for k in ["Cataphractii Terminator Armour", "Volkite Charger", "Power Weapon"]])
    ranko = entry(rid, "Sheed Ranko (replaces one Lernaean Terminator)", typ="model", cost=110,
                  constraints=[constraint(uid(rid, "max"), "max", 1, auto=True), unique(rid)],
                  profiles=[unit_profile(u, "Sheed Ranko", "Infantry (Character)", 5, 5, 4, 4, 2, 4, 3, 9, "2+/4+")],
                  infolinks=rules_links(["Sheed Ranko", "Hydra's Resilience"], key=rid),
                  links=[gear(rid, k) for k in ["Cataphractii Terminator Armour", "Combi-Plasma Gun", "Auspex",
                                                "Nuncio Vox"]] +
                  [link(uid("link", rid, "pw2"), W("Power Weapon"), "Power Weapon",
                        constraints=[constraint(uid("link", rid, "pw2", "min"), "min", 2),
                                     constraint(uid("link", rid, "pw2", "max"), "max", 2)])])
    RANKO_ALL.append(ranko)
    heavy_opts = [("Plasma Gun", 15), ("Plasma Cannon", 20), ("Conversion Beamer", 35)]
    heavy, _ = pool(u, "Heavy Weapons (up to two models, replace Volkite Charger)", u, heavy_opts, 2)
    swaps = [model_swaps(u, "Lernaean Terminators: Power Weapon or Power Fist (any number)", u, [tid],
                         [("Power Fist", 0), ("Chainfist (replaces a Power Fist)", 5)] if False else
                         [("Power Fist", 0), ("Chainfist", 5)]),
             model_swaps(u, "Lernaean Terminators: replace Volkite Charger with a Combi-weapon (any number)", u, [tid],
                         ARMOURY_COMBIS, minus=[W(n) for n, _ in heavy_opts])]
    cats, cons = ([foc(ELITES, "Elites", u)], [force_limit(u)]) if root else ([], [])
    return entry(u, name, typ="unit", cats=cats, constraints=cons,
                 infolinks=rules_links([LR], key=u),
                 entries=[terms, ranko, dt_option(u)],
                 groups=[*swaps, heavy,
                         transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                                    orbital=False)])


def effrits():
    name = "Effrit Disruption Cadre"
    u = uid("unit", name)
    did, pid = uid("model", u, "Effrit Disruptor"), uid("model", u, "Effrit Principal")
    kit = ["Power Armour", "Bolter", "Banestrike Ammunition", "Bolt Pistol", "Close Combat Weapon", "Frag Grenades"]
    principal = entry(pid, "Effrit Principal", typ="model",
                      constraints=[constraint(uid(pid, "min"), "min", 1), constraint(uid(pid, "max"), "max", 1)],
                      profiles=[unit_profile(u, "Effrit Principal", "Infantry (Character)", 4, 5, 4, 4, 1, 4, 2, 9,
                                             "3+")],
                      links=[gear(pid, k) for k in kit],
                      groups=[slot(pid, "Replace Bolter", "Bolter", COMBIS5),
                              take(pid, "Effrit Principal Wargear", [("Power Dagger", 5), ("Melta Bombs", 5),
                                                                     ("Artificer Armour", 10), ("Venom Spheres", 5)]),
                              pa_armoury(pid, u, 10, slots=["Bolt Pistol", "Close Combat Weapon"],
                                         skip=("Artificer Armour", "Melta Bombs"))])
    dis = entry(did, "Effrit Disruptor", typ="model", cost=25,
                constraints=[constraint(uid(did, "min"), "min", 4), constraint(uid(did, "max"), "max", 9)],
                profiles=[unit_profile(u, "Effrit Disruptor", "Infantry", 4, 5, 4, 4, 1, 4, 1, 8, "3+")],
                links=[gear(did, k) for k in kit])
    spec_opts = [("M.40 Targeter and Stalker Bolter", 10), ("Meltagun", 10), ("Plasma Gun", 15)]
    specials, _ = pool(u, "Special Weapons (1 per 5 models, replace Bolter)", u, spec_opts, 0, every=5)
    swaps = [model_swaps(u, "Effrit Disruptors: replace Bolter (any number)", u, [did], COMBIS5,
                         minus=[W(n) for n, _ in spec_opts]),
             model_takes(u, "Effrit Disruptors: wargear (any number)", u, [did], [("Power Dagger", 5),
                                                                                  ("Melta Bombs", 5)])]
    return entry(u, name, typ="unit", cost=145 - 4 * 25, cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links([LR, "Infiltrate", "Move Through Cover", "Hydra's Wail"], key=u),
                 entries=[principal, dis], groups=[*swaps, specials])


def characters(ctx):
    out = []
    # Armillus Dynat
    d = uid("unit", "Armillus Dynat")
    ham = lambda k: option(k, "Teleportation Transponders (Hammerstrike Assault, whole unit)", 10,  # noqa: E731
                           item="Teleportation Transponders")
    cs = command_squad_for("dynat", d)
    tcs = L2.terminator_command_squad("dynat")
    lern = lernaeans("dynat-lernaean", root=False)
    # Hammerstrike Assault replaces the normal +15 Terminator Teleportation Transponders in Dynat's own retinue
    ents = lern.find("selectionEntries")
    for x in list(ents):
        if x.get("name") == "Teleportation Transponders (entire squad)":
            ents.remove(x)
    for r in (cs, tcs, lern):
        add_to(r, "selectionEntries", [ham(r.get("id"))])
    out.append(named_character(LR, "Armillus Dynat", 205, (6, 5, 4, 4, 3, 5, 3, 10, "2+/4+"),
                               ["Artificer Armour", "Iron Halo", "Power Weapon", "Thunder Hammer", "Bolt Pistol",
                                "Nuncio Vox", "Frag Grenades", "Krak Grenades", "Teleportation Transponders"],
                               ["Command Squad (Armillus Dynat)", "The Harrowing", "Weapon Mastery",
                                "Hammerstrike Assault"],
                               retinue=retinue_links("dynat", [cs, tcs, lern])))
    # Exodus (not an Independent Character, not Master of the Legion, not a compulsory HQ)
    x = uid("unit", "Exodus")
    ex = named_character(LR, "Exodus", 110, (5, 6, 4, 4, 3, 5, 2, 9, "3+"),
                         ["Power Armour", "The Instrument", "Bolt Pistol", "Combat Blade", "Cameleoline",
                          "Frag Grenades", "Krak Grenades"],
                         ["Infiltrate", "Move Through Cover", "Scout", "Lone Killer (Exodus)",
                          "Execute the Mandate"],
                         master=False, compulsory=False,
                         extra_groups=[take(x, "Options", [("Melta Bombs", 5), ("Power Dagger", 5),
                                                           ("Venom Spheres", 5)])])
    il = ex.find("infoLinks")
    for lk in list(il):
        if lk.get("name") == "Independent Character":
            il.remove(lk)
    out.append(ex)
    # Autilon Skorr (Traitor only, Delegatus)
    s = uid("unit", "Autilon Skorr")
    sk = named_character(LR, "Autilon Skorr", 135, (5, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
                         ["Artificer Armour", "Refractor Field", "Bolt Pistol", "Rime-shard", "Frag Grenades",
                          "Krak Grenades"],
                         ["Delegatus (Autilon Skorr)", "Delegated Authority", "Desperate for Glory"],
                         retinue=retinue_links("skorr", [command_squad_for("skorr", s)]), loyalist=False)
    add_mods(sk, [modifier("add", "error", "Autilon Skorr counts as a Delegatus: a Detachment containing him may not "
                                           "also contain a Legion Praetor.", conds=[cond(L.PRAETOR, "force", "atLeast", 1)])])
    out.append(sk)
    # Ingo Pech
    p = uid("unit", "Ingo Pech")
    seekers = clone(ctx.unit("Legion Seeker Squad"), "pech-seekers")
    RANKO_ALL  # (Lernaean copy below registers its Ranko)
    out.append(named_character(LR, "Ingo Pech", 175, (6, 5, 4, 4, 3, 5, 3, 10, "2+/4+"),
                               ["Artificer Armour", "Iron Halo", "Power Weapon", "Bolter", "Nuncio Vox",
                                "Frag Grenades", "Krak Grenades"],
                               ["Command Squad (Ingo Pech)", "Master of Deceit"],
                               retinue=retinue_links("pech", [command_squad_for("pech", p),
                                                              L2.terminator_command_squad("pech"),
                                                              lernaeans("pech-lernaean", root=False), seekers])))
    # Mathias Herzog (Command Squad per the general Master of the Legion rule - see questions)
    out.append(named_character(LR, "Mathias Herzog", 170, (6, 5, 4, 4, 3, 5, 3, 10, "2+/4+"),
                               ["Artificer Armour", "Iron Halo", "Bolter", "Banestrike Ammunition", "Bolt Pistol",
                                "Power Weapon", "Frag Grenades", "Krak Grenades"],
                               ["False Disposition", "Headhunter Commander"],
                               retinue=retinue_links("herzog", [command_squad_for("herzog", HERZOG)])))
    return out


def alpharius():
    ret = primarch_retinue("alpharius", extra=[lernaeans("alpharius-lernaean", root=False)])
    return primarch(LR, "Alpharius, the Hydra", 490, (7, 7, 6, 6, 5, 6, 5, 10, "1+/4+"),
                    ["Pythian Scales", "Pale Spear", "Hydra's Spite", "Frag Grenades"],
                    ["Primarch Armour", "Master of Lies", "The Hydra", "Sire of the Alpha Legion", "I Am Alpharius",
                     "Alpharius' Primarch Retinue"],
                    retinue=ret)


# ------------------------------------------------------------------ changes to existing units
SABOTEUR_ALL = []


def seeker_changes(ctx):
    sq = ctx.unit("Legion Seeker Squad")
    u = sq.get("id")
    sgt = child_model(sq, "Legion Seeker Sergeant")
    sid = uid("al-saboteur", u)
    skills = required_choice(sid, "Coordinated Sabotage (additional Veteran Skill)", MUTABLE, required=False)
    # a skill already granted by Mutable Tactics may not be selected again
    for e in skills.find("selectionEntries"):
        n = e.get("name")
        taken = [cond(choice_id("al-mutable", "Mutable Tactics", n), "roster", "atLeast", 1)]
        add_mods(e, [modifier("set", "hidden", "true", conds=taken),
                     modifier("set", uid(e.get("id"), "max"), 0, conds=taken)])
    sab = entry(sid, "Legion Saboteur", cost=25,
                constraints=[constraint(uid(sid, "max"), "max", 1, auto=True), unique(sid)],
                infolinks=rules_links(["Legion Saboteur", "Coordinated Sabotage", "Pre-emptive Strike"], key=sid),
                groups=[skills])
    add_to(sgt, "selectionEntries", [sab])
    SABOTEUR_ALL.append(sab)
    spec = ["Flamer", "Meltagun", "Plasma Gun", "M.40 Targeter and Stalker Bolter",
            "Heavy Bolter with Suspensor and Hellfire Rounds", "Volkite Charger", "Volkite Caliver"]
    add_to(sq, "selectionEntries", [banestrike_squad(u, u, spec)])


def veteran_changes(ctx):
    vet = ctx.unit("Legion Veteran Squad")
    u = vet.get("id")
    not_eligible = ["Sniper Rifle", "Rotor Cannon", "Flamer", "Meltagun", "Plasma Gun", "Volkite Charger",
                    "Volkite Caliver", "Heavy Flamer with Suspensor Web", "Heavy Bolter with Suspensor Web",
                    "Missile Launcher with Suspensor Web"]
    add_to(vet, "selectionEntries", [banestrike_squad(u, u, not_eligible)])


def sergeant_venom_spheres(ctx):
    """Venom Spheres (+5): only true squad Sergeants (author's answer), not Champions or other upgrade characters."""
    seen = set()
    for root in all_entries(ctx):
        for m in root.iter("selectionEntry"):
            if m.get("type") != "model" or "Sergeant" not in m.get("name", ""):
                continue
            for g in m.iter("selectionEntryGroup"):
                if g.get("name") != "Space Marine Armoury (max 50 pts)" or id(g) in seen:
                    continue
                seen.add(id(g))
                links = g.find("entryLinks")
                if links is None:
                    links = el("entryLinks")
                    g.append(links)
                lid = uid("link", g.get("id"), "legion", "Venom Spheres")
                links.append(link(lid, W("Venom Spheres"), "Venom Spheres", cost=5,
                                  constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
    return len(seen)


def armoury(ctx):
    add_armoury_items(ctx, [("Power Dagger", 5), ("Venom Spheres", 5)], who=("praetor", "centurion"))
    add_armoury_items(ctx, [("Power Dagger", 5)], who=("sergeants",))
    n = sergeant_venom_spheres(ctx)
    assert n, "no Sergeant armoury found for Venom Spheres"
    ic_wargear(ctx, [
        ("Banestrike Ammunition", 5, lambda u: [("group", all_of(*[lacks(W(n), u) for n in BOLTERS]))]),
        ("Teleportation Transponders", 10, lambda u: [("group", L.no_tda(u))]),
    ])
    for n in ("Legion Terminator Squad",):
        e = ctx.unit(n)
        add_to(e, "selectionEntries", [dt_option(e.get("id"))])
    for e in ctx.retinues("Legion Terminator Command Squad"):
        if any(x.get("name", "").startswith("Teleportation Transponders") for x in (e.find("selectionEntries") if e.find("selectionEntries") is not None else [])):
            continue    # Dynat's retinue: Hammerstrike Assault (+10) instead
        add_to(e, "selectionEntries", [dt_option(e.get("id"))])
    # Headhunter Prime / Effrit Principal buy Power Dagger and Venom Spheres from their own option lists
    for n in ("Headhunter Kill Team", "Effrit Disruption Cadre"):
        for g in ctx.unit(n).iter("selectionEntryGroup"):
            if g.get("name") != "Space Marine Armoury (max 50 pts)":
                continue
            links = g.find("entryLinks")
            for lk in list(links if links is not None else []):
                if lk.get("id") in {uid("link", g.get("id"), "legion", i) for i in ("Power Dagger", "Venom Spheres")}:
                    links.remove(lk)


def rites(ctx):
    rites_e = ctx.unit("Rite of War")
    coils = ctx.add_rite("The Coils of the Hydra", RULES["The Coils of the Hydra"],
                         errors=[("the Detachment must take three compulsory Troops choices.",
                                  [cond(gs.CAT_LINE, "force", "lessThan", 3)])])
    add_mods(rites_e, [modifier("add", "error", "The Coils of the Hydra: no more than one Centurion upgraded to a Consul "
                                                "(Vigilator Consuls do not count).",
                                conds=[cond(coils, "force", "atLeast", 1)],
                                groups=[consul_limit_group(exclude=("Vigilator",))])])
    # Autilon Skorr does not count towards this Coils of the Hydra Consul limit (author's answer)
    ctx.add_rite("Headhunter Leviathal", RULES["Headhunter Leviathal"])


def extend(ctx):
    ctx.legion_rules([LR, "Mutable Tactics", "Siege Specialists", "Martial Hubris", "Infiltration Network"])
    add_to(ctx.unit("Legion"), "selectionEntryGroups",
           [required_choice("al-mutable", "Mutable Tactics", MUTABLE)])
    seeker_changes(ctx)
    veteran_changes(ctx)
    chars = characters(ctx)     # after the Seeker changes (Ingo Pech's Seeker Squad is a copy)
    ctx.add_units(operatives(), headhunters(), lernaeans(), effrits(), *chars, alpharius())
    # every copy of Sheed Ranko / the Legion Saboteur: only one per army
    one_per_army(RANKO_ALL, "Sheed Ranko")
    sabs = [x for r in all_entries(ctx) for x in r.iter("selectionEntry")
            if x.get("name") == "Legion Saboteur"]
    one_per_army(sabs, "The Legion Saboteur")
    rites(ctx)
    armoury(ctx)
