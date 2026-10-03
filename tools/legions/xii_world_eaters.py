"""XII Legion - World Eaters (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, allegiance_only, named_character, primarch, primarch_retinue,
                            retinue_links, command_squad_for, add_armoury_items, register_data, LOW)
from bsx import costs as bsx_costs
from bsx import PTS, uid, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, gear, per_model, rules_links, unit_profile
from legiones2 import slot, take, pool, transports, add_mods, add_to, walker_profile, foc, rite, rite_id, model_swaps
from legiones2 import TROOPS, ELITES, HQ, HS, RETINUE_SHARED

LEGION = "XII - World Eaters"
LR = "Legiones Astartes (World Eaters)"

RULES = {
    LR: ("Models with this special rule belong to the XII Legion and use the World Eaters Legion special rule Blood "
         "Frenzy."),
    "Blood Frenzy": (
        "World Eaters Infantry, Bike, Jump Infantry and Dreadnought models gain +1 Attack during an Assault phase in "
        "which they charged (first round of that close combat only). Whenever a World Eaters unit wins a close combat it "
        "gains the Rage special rule (ProHammer 3rd-5th Edition version) for the remainder of the battle. A World Eaters "
        "unit which wins a close combat must Pursue a retreating enemy whenever it is permitted to do so; if no Pursuit "
        "is possible because the enemy was completely destroyed, it must Consolidate as directly as possible towards the "
        "nearest enemy unit."),
    "World Eaters Armoury": (
        "Chainaxe (+4): any World Eaters model eligible to carry a Close Combat Weapon may replace it with a Chainaxe "
        "(not Servo-automata). Caedere Weapon (+15): any World Eaters Independent Character or squad Sergeant with access "
        "to the Space Marine Armoury may replace a Chainsword with a Caedere Weapon; it does not count towards the "
        "Armoury points limit and may not be taken by models in Terminator Armour (Rampager Squads gain access through "
        "their own entry)."),
    "Caedere Weapon": ("A Caedere Weapon counts as a one-handed close-combat weapon (Strength User +1, Rending). It does "
                       "not count as a Power Weapon."),
    # Rites of War
    "Berserker Assault": (
        "EFFECTS - The Red Hand: Rampager Squads may be selected as Troops and may fulfil compulsory Troops; Legion "
        "Assault Squads may fulfil compulsory Troops normally. Headlong Assault: World Eaters Infantry and Jump Infantry "
        "units gain Fleet (a unit with Fleet may charge after making an Advance move). Weapons of the Pits: models in "
        "Legion Assault Squads and Rampager Squads may purchase Chainaxes for +2 points per model instead of +4. Blood "
        "Forward: a non-Vehicle World Eaters unit must declare a charge if it is eligible and at least one enemy unit is "
        "within its current charge distance (the World Eaters player chooses between legal targets).\n"
        "LIMITATIONS - The compulsory Troops must be Legion Assault Squads or Rampager Squads, at least one of them a "
        "Rampager Squad. The Warlord must be equipped with a Chainaxe, Caedere Weapon, Rending Weapon, Power Weapon or "
        "another close-combat weapon. No more than one Heavy Support choice. No Fortification."),
    "The Crimson Path": (
        "EFFECTS - Forlorn Hope: World Eaters Infantry models gain Feel No Pain (5+) while within the enemy deployment "
        "zone (an existing Feel No Pain improves by one step, max 3+). Unto Death: World Eaters Independent Characters "
        "gain It Will Not Die while within the enemy deployment zone (with It Will Not Die already, they regain a Wound on "
        "4+ there). The Path Must End in Blood (Victory Point missions only): at the end of the battle the opponent gains "
        "+150 Victory Points if no surviving World Eaters non-Vehicle unit is at least partially within the enemy "
        "deployment zone, and +150 Victory Points if the opponent completely destroyed more World Eaters units than the "
        "World Eaters destroyed enemy units.\n"
        "LIMITATIONS - No units with Slow and Purposeful. No Immobile units (e.g. Drop Pods). No Fortification. No Allied "
        "Detachment drawn from another Space Marine Legion."),
    # units
    "Ravening Madmen": (
        "Red Butchers always hit models with a Weapon Skill on a 3+ in close combat, regardless of the Weapon Skill "
        "comparison, and enemy models likewise always hit Red Butchers on a 3+. Does not affect attacks against Vehicles "
        "or other targets without a Weapon Skill and does not override a rule allowing a better fixed result. Red "
        "Butchers never count as a Scoring Unit."),
    "Paired Power Weapons (Red Butchers)": ("The Attacks characteristic in the Red Butcher profile already includes the "
                                            "bonus Attack for fighting with two close-combat weapons."),
    "Nails-Broken": ("If an Inductii Squad is able to declare a charge during the Assault phase, it must do so. If more "
                     "than one enemy unit may legally be charged, the World Eaters player chooses the target normally."),
    "Devourers": ("0-1 Devourer Terminator Squad per Detachment. Angron may select one Devourer Terminator Squad as his retinue. If selected in this manner, the "
                  "Devourers do not occupy a separate Elites choice."),
    "Red Hand Assault Squad": ("If the entire squad takes Jump Packs it becomes Jump Infantry, is renamed a Red Hand "
                               "Destroyer Assault Squad and may not select a Dedicated Transport."),
    # characters
    "The Bloody": (
        "Whenever Kharn rolls a natural 1 To Hit in close combat, that attack instead hits the nearest friendly model "
        "within 6\" (opponent chooses if several are equally close), resolved with Kharn's current Strength and weapon; "
        "saves are allowed and the wounds do not count towards the combat result. If no friendly model is within 6\", "
        "the roll is simply a miss."),
    "Command Retinue (Kharn)": ("Kharn may select one Legion Command Squad or Rampager Squad as his retinue. It does not "
                                "occupy a separate Force Organisation slot."),
    "Gorechild (Kharn)": ("Gorechild may only be selected if Angron is not equipped with Gorechild (Gorefather & "
                          "Gorechild) in the same army."),
    "Master of Destroyers": (
        "Shabran Darr may join Legion Destroyer Squads and Red Hand Destroyer Squads despite Destroyer Cadre. He may "
        "select one Red Hand Destroyer Mortalis or Assault Squad as his retinue; it does not occupy a separate Force "
        "Organisation slot."),
    "Apothecary": ("This model is an Apothecary: it counts as an Apothecary for rules referring to Apothecaries and for "
                   "selecting restricted equipment."),
    "Architect of the Nails": (
        "After deployment but before the first turn, nominate one friendly World Eaters Infantry unit not wearing any form "
        "of Terminator Armour. It gains Furious Charge for the battle and must declare a charge whenever it is legally "
        "able to. Only one unit may be enhanced in this manner."),
    "Warrior-Apothecary": ("Kargos may use his Narthecium even while in base contact with an enemy model. All other "
                           "Narthecium restrictions still apply."),
    "Command Retinue (Kargos)": ("Kargos may select one Legion Command Squad as his retinue (no separate Force "
                                 "Organisation slot). If Kargos has a Jump Pack, the Command Squad may purchase Jump Packs "
                                 "normally."),
    "Command Retinue (Ehrlen)": (
        "Ehrlen may select one Legion Command Squad as his retinue (no separate Force Organisation slot). Every model in "
        "it may purchase a Jump Pack for +15 points per model; if so, every model must receive one and the squad may not "
        "select a Dedicated Transport."),
    "Gladiator Champion": "Any Trarii Breacher Squad joined by Delvarus becomes Stubborn and gains Furious Charge.",
    "Command Retinue (Delvarus)": ("Delvarus may select one Trarii Breacher Squad as his retinue. It does not occupy a "
                                   "separate Force Organisation slot."),
    # Angron
    "Armour of Mars": "The Armour of Mars counts as Primarch Armour (1+ Armour Save, 4+ Invulnerable Save).",
    "Gorefather & Gorechild": ("A matched pair of Power Weapons (count as two close-combat weapons). Attacks are resolved "
                               "at +1 Strength and have Shred and Armourbane."),
    "The Red Angel": (
        "If Angron is able to declare a charge during the Assault phase, he must do so. Angron and any unit he has joined "
        "may declare charges against enemy units up to 8\" away instead of 6\", and must charge the closest eligible enemy "
        "unit to Angron (World Eaters player chooses between equally close units). Difficult Terrain does not reduce this "
        "charge distance; Dangerous Terrain is resolved normally."),
    "Butcher's Nails": (
        "Angron has Furious Charge and may never voluntarily Withdraw from close combat. Whenever Angron rolls an "
        "unmodified 1 To Hit in close combat (not re-rollable), that attack instead strikes another friendly model in his "
        "unit (opponent chooses), resolved with Angron's current Strength and weapon rules; saves allowed, wounds do not "
        "count towards the combat result. If Angron is not accompanied by another friendly model, the roll is a miss."),
    "Sire of the World Eaters": ("Friendly World Eaters units with at least one model within 12\" of Angron add +1 to all "
                                 "Pursuit rolls and may re-roll failed Break Tests caused by losing a close combat (the "
                                 "second result must be accepted)."),
    "The Nails Demand Blood": ("Each time an enemy unit is completely destroyed during an Assault phase in a close combat "
                               "involving Angron, his Attacks increase by +1 for the rest of the battle (cumulative, max "
                               "+3, i.e. up to 9 Attacks)."),
    "Widowmaker": ("A Two-Handed Power Weapon. Attacks are resolved at Strength 10, have Armourbane and are made at -2 "
                   "Initiative."),
    "Primarch Retinue (Angron)": ("Angron may select a Legion Honour Guard Squad, Legion Terminator Command Squad or "
                                  "Devourer Terminator Squad as his Primarch Retinue."),
    # Angron, the Red Angel
    "Daemonic Flight": ("Angron may move up to 12\" in the Movement phase, moving over intervening models and terrain. He "
                        "may never join another unit and no model may join him."),
    "Blades of the Red Angel": (
        "The Blades of the Red Angel count as a pair of Master-crafted Power Weapons. Angron receives the normal +1 Attack "
        "for fighting with two close-combat weapons. Against Vehicles, attacks made with the Blades of the Red Angel have "
        "Armourbane. Against Monstrous Creatures and models with Toughness 6 or greater, Angron may re-roll failed To "
        "Wound rolls."),
    "Daemonic Armour": "Angron, the Red Angel has a 2+ Armour Save and a 4+ Invulnerable Save (as shown in his profile).",
    "Blood Calls to Blood": (
        "Angron never begins the battle on the battlefield and does not make normal Reserve rolls. Keep a cumulative "
        "total of unsaved Wounds actually inflicted on enemy models by friendly World Eaters models in close combat "
        "(excess Wounds and shooting/psychic shooting never count). At the end of each World Eaters Assault phase roll: "
        "0-9 - cannot be summoned; 10-19 - 6+; 20-29 - 5+; 30-39 - 4+; 40-49 - 3+; 50+ - 2+. If successful he arrives at "
        "the beginning of the controlling player's next turn. If not summoned before, he automatically arrives at the "
        "beginning of Turn 5."),
    "The Red Angel Descends": ("When Angron arrives, deploy him by Deep Strike without scattering. He may declare a "
                               "charge in the turn he arrives and keeps all bonus Attacks and other benefits for "
                               "charging."),
    "The Nails Sing": (
        "While Angron is on the battlefield, ALL units (friend and foe) gain +1 Attack during the first round of a close "
        "combat in which they charged, and any unit composed entirely of models in Power or Artificer Armour may charge "
        "up to 8\" instead of 6\". World Eaters additionally: Compulsory Charge (must charge the nearest eligible enemy "
        "unit within charge distance); No Restraint (a unit winning a combat must Pursue, overriding rules that would "
        "prevent it unless physically or mission-wise impossible); Bloodward Consolidation (if the enemy is destroyed and "
        "no Pursuit is possible, Consolidate as directly as possible towards the nearest enemy). The Attack is cumulative "
        "with the normal charge bonus and Blood Frenzy."),
    "Only one Angron": ("Angron, the Red Angel may only be selected for a World Eaters army. An army may not include both "
                        "Angron, the Red Angel and Angron in his mortal form."),
}

WEAPONS = {
    "Caedere Weapon": ("-", "User +1", "-", "Rending"),
    "The Cutter": ("-", "User +1", "-", "Power Weapon"),
    "Gorechild": ("-", "User +3", "-", "Power Weapon, Master-crafted, +D3 Attacks in the first round of each combat"),
    "Gorefather & Gorechild": ("-", "User +1", "-", "Power Weapon, Shred, Armourbane, pair (two close-combat weapons)"),
    "Spite Furnace": ('12"', "7", "2", "Pistol, Gets Hot, Master-crafted"),
    "Widowmaker": ("-", "10", "-", "Power Weapon, Two-Handed, Armourbane, -2 Initiative"),
    "Blades of the Red Angel": ("-", "User", "-", "Power Weapon, Master-crafted, pair (+1 Attack), Armourbane vs "
                                                  "Vehicles"),
}
WEAPON_RULES = {
    "Caedere Weapon": ["Caedere Weapon", "Rending"],
    "Gorechild": ["Master-Crafted"],
    "Gorefather & Gorechild": ["Gorefather & Gorechild", "Shred", "Armourbane"],
    "Spite Furnace": ["Gets Hot", "Master-Crafted"],
    "Widowmaker": ["Widowmaker", "Two-Handed", "Armourbane"],
    "Blades of the Red Angel": ["Blades of the Red Angel", "Master-Crafted", "Armourbane"],
}
WARGEAR = {
    "Armour of Mars": (RULES["Armour of Mars"], []),
    "Daemonic Armour": (RULES["Daemonic Armour"], []),
}

# rites that decide what the compulsory Troops are (a unit that is normally compulsory-eligible loses that)
RESTRICTING_RITES = ["Primarch's Chosen", "Pride of the Legion", "Legion Assault Company", "Legion Breacher Company",
                     "Legion Recon Company", "Legion Destroyer Company", "Fury of the Ancients", "Sky Hunter Phalanx",
                     "Legion Tactical Company", "Berserker Assault"]


def register():
    register_data(rules=RULES, weapons=WEAPONS, weapon_rules=WEAPON_RULES, wargear=WARGEAR)
    for n in ["Legion Tactical Squad", "Legion Breacher Siege Squad"]:
        L2.NOT_LINE_UNDER[n].append("Berserker Assault")
    # Red Hand Destroyer squads count as Legion Destroyer Squads (Legion Destroyer Company: Troops, compulsory Troops)
    L2.TROOP_RITES[RED_HAND_NAME] = list(L2.TROOP_RITES["Legion Destroyer Squad"])
    L2.NORMAL_ROLE[RED_HAND_NAME] = ELITES


# ------------------------------------------------------------------ helpers
def gear_n(key, name, n):
    """Fixed wargear link carried n times (e.g. two Power Weapons)."""
    lid = uid("link", key, name)
    return link(lid, W(name), name, constraints=[constraint(uid(lid, "min"), "min", n),
                                                 constraint(uid(lid, "max"), "max", n)])


def model(u, name, mn, mx, cost, stats, kit, unit_type="Infantry", groups=(), links=(), mods=()):
    mid = uid("model", u, name)
    return mid, entry(mid, name, typ="model", cost=cost, mods=list(mods),
                      constraints=[constraint(uid(mid, "min"), "min", mn), constraint(uid(mid, "max"), "max", mx)],
                      profiles=[unit_profile(u, name, unit_type, *stats)],
                      links=[gear(mid, k) for k in kit] + list(links), groups=list(groups))


def pool_upto(key, title, unit_id, options, base, at10):
    """'Up to N models may ...; if the squad numbers ten models, up to M'."""
    gid = uid("grp", key, title)
    mx = uid(gid, "max")
    g, _ = pool(key, title, unit_id, options, base,
                extra_mods=[modifier("increment", mx, at10 - base, conds=[cond("model", unit_id, "atLeast", 10)])])
    return g


def squad_swap(key, title, unit_id, model_id, options):
    """'All <models> may replace X with ...': one squad-wide choice paid per model of model_id."""
    gid = uid("grp", key, title)
    ents = []
    for n, pts in options:
        eid = uid("swap", key, title, n)
        ents.append(entry(eid, n, cost=0, mods=[modifier("increment", PTS, pts, repeats=[repeat(model_id, unit_id, 1)])],
                          constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)], links=[gear(eid, n)]))
    return group(gid, title, entries=ents, constraints=[constraint(uid(gid, "max"), "max", 1, auto=True)])


def not_line_mods():
    return [modifier("remove", "category", gs.CAT_LINE, groups=[any_of(*[rite(r) for r in RESTRICTING_RITES])])]


def fortification_error():
    return ("the Detachment may not include a Fortification.", [cond(gs.cat("Fortification"), "force", "atLeast", 1)])


# ------------------------------------------------------------------ units
RAMPAGER = uid("unit", "Rampager Squad")
RED_HAND_NAME = "Red Hand Destroyer Mortalis Squad"


def squad_prices_for_champion(champ, champ_id, prices):
    """The Champion's Armoury slots ('Replace <default>') also offer the squad's own exchanges at the squad price;
    those do not count towards his 50-point Armoury limit. prices: {default: [(item, pts)]}."""
    for cap in champ.iter("selectionEntryGroup"):
        cons = [c for c in cap.iter("constraint") if c.get("field") == PTS]
        if cap.get("name") != "Space Marine Armoury (max 50 pts)" or not cons:
            continue
        cap_mods = []
        for g in cap.iter("selectionEntryGroup"):
            name = g.get("name") or ""
            if not name.startswith("Replace "):
                continue
            for item, pts in prices.get(name[len("Replace "):], []):
                links = g.find("entryLinks")
                lk = next((x for x in links if x.get("targetId") == W(item)), None)
                if lk is None:
                    lid = uid("link", g.get("id"), "squad-price", item)
                    links.append(link(lid, W(item), item, cost=pts,
                                      constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))
                else:
                    c = lk.find("costs")
                    if c is not None and len(c):
                        c[0].set("value", str(pts))
                    else:
                        lk.append(bsx_costs(pts))
                cap_mods.append(modifier("increment", cons[0].get("id"), pts, conds=[has(W(item), champ_id)]))
        add_mods(cap, cap_mods)


def rampager(key="Rampager Squad", root=True):
    u = uid("unit", key)
    kit = ["Power Armour", "Bolt Pistol", "Chainaxe"]
    rid, ramp = model(u, "Rampager", 4, 9, 22, (4, 4, 4, 4, 1, 4, 2, 9, "3+"), kit)
    cid, champ = model(u, "Rampager Champion", 1, 1, 0, (4, 4, 4, 4, 1, 4, 3, 9, "3+"), ["Power Armour"],
                       unit_type="Infantry (Character)",
                       groups=[L2.pa_armoury(uid(key, "champ"), u, 10, slots=["Bolt Pistol", "Chainaxe"])])
    squad_prices_for_champion(champ, cid, {"Chainaxe": [("Caedere Weapon", 3), ("Power Weapon", 7)],
                                           "Bolt Pistol": [("Plasma Pistol", 10)]})
    jp_id = uid("squadwide", u, "Jump Packs (entire squad)")
    jp = per_model(u, "Jump Packs (entire squad)", 15, u, ["Jump Pack"])
    cats, mods, cons = [], [], []
    if root:
        cats = [foc(ELITES, "Elites", u)]
        br = [rite("Berserker Assault")]
        mods = [modifier("set-primary", "category", TROOPS, conds=br), modifier("remove", "category", ELITES, conds=br),
                modifier("add", "category", gs.CAT_LINE, conds=br)]
    return entry(u, "Rampager Squad", typ="unit", cost=110 - 4 * 22, cats=cats, mods=mods, constraints=cons,
                 infolinks=rules_links([LR, "Caedere Weapon"], key=u),
                 entries=[champ, ramp,
                          per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]), jp],
                 groups=[pool_upto(u, "Rampagers: replace Chainaxe (up to 3; 6 at ten models)", u,
                                   [("Caedere Weapon", 3), ("Power Weapon", 7)], 3, 6),
                         pool_upto(u, "Rampagers: replace Bolt Pistol (up to 3; 6 at ten models)", u,
                                   [("Plasma Pistol", 10)], 3, 6),
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos"],
                                    block_if=[has(jp_id, u)])])


def red_butchers():
    u = uid("unit", "Red Butcher Squad")
    bid = uid("model", u, "Red Butcher")
    b = entry(bid, "Red Butcher", typ="model", cost=60,
              constraints=[constraint(uid(bid, "min"), "min", 5), constraint(uid(bid, "max"), "max", 10)],
              profiles=[unit_profile(u, "Red Butcher", "Infantry", 3, 2, 4, 4, 2, 3, 4, 9, "2+/4+")],
              links=[gear(bid, "Cataphractii Terminator Armour"), gear_n(bid, "Power Weapon", 2)])
    return entry(u, "Red Butcher Squad", typ="unit", cost=300 - 5 * 60, cats=[foc(ELITES, "Elites", u)],
                 constraints=[force_limit(u)],
                 infolinks=rules_links([LR, "Fearless", "Ravening Madmen", "Paired Power Weapons (Red Butchers)"], key=u),
                 entries=[b],
                 groups=[model_swaps(u, "Red Butchers: replace one Power Weapon (any number)", u, [bid],
                                     [("Power Fist", 5), ("Chainfist", 10), ("Thunder Hammer", 10)]),
                         transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                                    orbital=False)])


def red_hand(key="Red Hand Destroyer Mortalis Squad", root=True):
    name = RED_HAND_NAME
    u = uid("unit", key)
    kit = ["Power Armour", "Two Bolt Pistols", "Chainaxe", "Frag Grenades", "Rad Grenades"]
    did, dests = model(u, "Red Hand Destroyer", 4, 9, 22, (4, 4, 4, 4, 1, 4, 2, 9, "3+"), kit)
    sid, sgt = model(u, "Red Hand Sergeant", 1, 1, 0, (4, 4, 4, 4, 1, 4, 3, 9, "3+"), kit,
                     unit_type="Infantry (Character)",
                     groups=[slot(uid(key, "sgt"), "Replace Chainaxe", "Chainaxe",
                                  [("Rending Weapon", 5), ("Power Weapon", 10), ("Power Fist", 15),
                                   ("Lightning Claw", 15), ("Thunder Hammer", 20)]),
                             take(uid(key, "sgt"), "Sergeant Wargear", [("Artificer Armour", 10),
                                                                         ("Phosphex Bomb", 10, 3)])])
    weapons, wmx = pool(u, "Red Hand Destroyers: replace one Bolt Pistol (1 per 5 models; 2 per 5 in a Destroyer "
                           "Company)", u,
                        [("Volkite Serpenta", 5), ("Hand Flamer", 5), ("Plasma Pistol", 15),
                         ("Missile Launcher with Suspensor Web and Rad Missiles", 25)], 0, every=5)
    # counts as a Legion Destroyer Squad: Forbidden Arsenal (Legion Destroyer Company) doubles the allowance
    add_mods(weapons, [modifier("increment", wmx, 1, conds=[rite("Legion Destroyer Company")],
                                repeats=[repeat("model", u, 5)])])
    bombs, _ = pool(u, "Red Hand Destroyers: Phosphex Bomb (1 per 5 models)", u, [("Phosphex Bomb", 10)], 0, every=5)
    jp_id = uid("squadwide", u, "Jump Packs (entire squad) - Red Hand Destroyer Assault Squad")
    jp = per_model(u, "Jump Packs (entire squad) - Red Hand Destroyer Assault Squad", 15, u, ["Jump Pack"])
    mods = [modifier("set", "name", "Red Hand Destroyer Assault Squad", conds=[has(jp_id, u)])]
    if root:
        mods += L2.troop_role_mods(name)
    return entry(u, name, typ="unit", cost=160 - 4 * 22, cats=[foc(ELITES, "Elites", u)] if root else [], mods=mods,
                 infolinks=rules_links([LR, "Counter-Attack", "Dual Pistols (Destroyers)", "Destroyer Cadre",
                                        "Rad Grenades", "Red Hand Assault Squad"], key=u),
                 entries=[sgt, dests, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]), jp],
                 groups=[weapons, bombs,
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos"],
                                    block_if=[has(jp_id, u)])])


def inductii():
    u = uid("unit", "World Eaters Inductii Squad")
    kit = ["Power Armour", "Bolt Pistol", "Chainsword"]
    iid, ind = model(u, "Inductii", 9, 19, 13, (4, 3, 4, 4, 1, 4, 1, 7, "3+"), kit)
    sid, sgt = model(u, "Inductii Sergeant", 1, 1, 0, (4, 3, 4, 4, 1, 4, 2, 8, "3+"), kit,
                     unit_type="Infantry (Character)",
                     groups=[slot(uid(u, "sgt"), "Replace Chainsword", "Chainsword",
                                  [("Rending Weapon", 5), ("Power Weapon", 10), ("Power Fist", 15)])])
    specials, _ = pool(u, "Inductii: replace Bolt Pistol (1 per 10 models)", u, [("Flamer", 5), ("Meltagun", 10)], 0,
                       every=10)
    return entry(u, "World Eaters Inductii Squad", typ="unit", cost=130 - 9 * 13, mods=not_line_mods(),
                 cats=[foc(TROOPS, "Troops", u), category_link(gs.CAT_LINE, "Compulsory Troops Eligible", key=u)],
                 infolinks=rules_links([LR, "Nails-Broken"], key=u),
                 entries=[sgt, ind, per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
                 groups=[specials, transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                                     "Anvillus Pattern Dreadclaw Drop Pod"], max_models=10)])


def devourers(key="Devourer Terminator Squad", root=True):
    u = uid("unit", key)
    kit = ["Cataphractii Terminator Armour", "Combi-Bolter", "Power Weapon"]
    did, dev = model(u, "Devourer", 4, 9, 45, (5, 4, 4, 4, 1, 4, 2, 9, "2+/4+"), kit)
    cid, chief = model(u, "Devourer Chieftain", 1, 1, 0, (5, 4, 4, 4, 1, 4, 3, 10, "2+/4+"), kit,
                       unit_type="Infantry (Character)")
    harness, _ = pool(u, "Grenade Harness (one model)", u, [("Grenade Harness", 10)], 1)
    return entry(u, "Devourer Terminator Squad", typ="unit", cost=225 - 4 * 45,
                 cats=[foc(ELITES, "Elites", u)] if root else [], constraints=[force_limit(u)] if root else [],
                 infolinks=rules_links([LR, "Stubborn", "Devourers"], key=u),
                 entries=[chief, dev],
                 groups=[model_swaps(u, "Any model: replace Combi-bolter (any number)", u, [did, cid],
                                     [("Foeblaster Boltgun", 5), ("Combi-Flamer", 10), ("Combi-Volkite Charger", 10),
                                      ("Combi-Meltagun", 15), ("Combi-Plasma Gun", 15)]),
                         model_swaps(u, "Any model: replace Power Weapon (any number)", u, [did, cid],
                                     [("Power Fist", 5), ("Lightning Claw", 5), ("Chainfist", 10),
                                      ("Thunder Hammer", 10)]),
                         harness,
                         transports(u, u, ["Land Raider Phobos", "Land Raider Proteus",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                                    orbital=False)])


def triarii(key="Triarii Breacher Squad", root=True):
    # ids keep the old "Triarii" key; the book now spells the unit "Trarii"
    u = uid("unit", key)
    kit = ["Power Armour", "Bolt Pistol", "Chainaxe", "Boarding Shield"]
    bid, br = model(u, "Trarii Breacher", 4, 9, 27, (4, 4, 4, 4, 1, 4, 2, 9, "3+"), kit)
    cid, champ = model(u, "Trarii Breacher Champion", 1, 1, 0, (4, 4, 4, 4, 1, 4, 3, 9, "3+"),
                       ["Power Armour", "Boarding Shield"],
                       unit_type="Infantry (Character)",
                       groups=[L2.pa_armoury(uid(key, "champ"), u, 10, slots=["Bolt Pistol", "Chainaxe"])])
    return entry(u, "Trarii Breacher Squad", typ="unit", cost=155 - 4 * 27,
                 cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links([LR, "Hardened Armour"], key=u),
                 entries=[champ, br, per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"])],
                 groups=[squad_swap(u, "All Trarii Breachers: replace Chainaxe", u, bid,
                                    [("Caedere Weapon", 5), ("Power Weapon", 10)])])


# ------------------------------------------------------------------ characters
ANGRON = uid("unit", "Angron, the Red Angel")
DAEMON_ANGRON = uid("unit", "Angron, the Red Angel (Daemon Primarch)")


def characters():
    out = []
    # Kharn
    k = uid("unit", "Khârn the Bloody")
    kharn = named_character(LR, "Khârn the Bloody", 180, (6, 5, 4, 4, 3, 5, 4, 9, "2+/4+"),
                            ["Artificer Armour", "Iron Halo", "Plasma Pistol", "The Cutter", "Frag Grenades"],
                            ["The Bloody", "Command Retinue (Kharn)", "Gorechild (Kharn)"],
                            retinue=retinue_links("kharn", [command_squad_for("kharn", k),
                                                            rampager("kharn-rampagers", root=False)]),
                            min_points=1500,
                            extra_groups=[take(k, "Wargear", [("Krak Grenades", 2), ("Jump Pack", 20)]),
                                          slot(k, "Replace The Cutter", "The Cutter", [("Gorechild", 55)])])
    add_mods(kharn, [modifier("add", "error", "Khârn may only take Gorechild if Angron is not equipped with Gorechild "
                                              "(Gorefather & Gorechild) in the same army.",
                              groups=[all_of(has(W("Gorechild"), k), cond(ANGRON, "roster", "atLeast", 1),
                                             cond(W("Widowmaker"), "roster", "lessThan", 1))])])
    out.append(kharn)
    # Shabran Darr
    d = uid("unit", "Shabran Darr")
    out.append(named_character(LR, "Shabran Darr", 150, (6, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
                               ["Artificer Armour", "Refractor Field", "Two Bolt Pistols", "Power Weapon",
                                "Frag Grenades", "Rad Grenades"],
                               ["Stubborn", "Dual Pistols (Destroyers)", "Master of Destroyers"],
                               retinue=retinue_links("darr", [red_hand("darr-red-hand", root=False)]),
                               master=False, loyalist=True,
                               extra_groups=[take(d, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]))
    # Gahlan Surlak (Legion Support Officer)
    s = uid("unit", "Gahlan Surlak")
    out.append(named_character(LR, "Gahlan Surlak", 125, (5, 5, 4, 4, 2, 4, 2, 9, "3+/5+"),
                               ["Power Armour", "Refractor Field", "Narthecium", "Reductor", "Bolt Pistol",
                                "Chainsword", "Frag Grenades"],
                               ["Architect of the Nails", "Legion Support Officer"],
                               master=False, compulsory=False,
                               extra_groups=[take(s, "Wargear", [("Krak Grenades", 2)])]))
    # Kargos
    kg = uid("unit", "Kargos, the Bloodspitter")
    out.append(named_character(LR, "Kargos, the Bloodspitter", 120, (5, 4, 4, 4, 3, 5, 3, 9, "3+"),
                               ["Power Armour", "Narthecium", "Reductor", "Chainaxe", "Bolt Pistol", "Frag Grenades"],
                               ["Apothecary", "Warrior-Apothecary", "Command Retinue (Kargos)"],
                               retinue=retinue_links("kargos", [command_squad_for("kargos", kg)]), master=False,
                               extra_groups=[take(kg, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5),
                                                                  ("Jump Pack", 20)])],
                               profile_name="Kargos"))
    # Captain Ehrlen
    e = uid("unit", "Captain Ehrlen")
    out.append(named_character(LR, "Captain Ehrlen", 95, (5, 5, 4, 4, 2, 5, 3, 9, "3+/5+"),
                               ["Power Armour", "Refractor Field", "Jump Pack", "Rending Weapon", "Bolt Pistol",
                                "Bionics", "Frag Grenades"],
                               ["Command Retinue (Ehrlen)"],
                               retinue=retinue_links("ehrlen", [command_squad_for("ehrlen", e)]), master=False,
                               loyalist=True, unit_type="Jump Infantry (Character)",
                               extra_groups=[take(e, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]))
    # Delvarus
    dv = uid("unit", "Delvarus")
    out.append(named_character(LR, "Delvarus", 120, (5, 4, 4, 4, 2, 5, 3, 9, "3+/5+"),
                               ["Power Armour", "Caedere Weapon", "Bolt Pistol", "Boarding Shield", "Frag Grenades"],
                               ["Gladiator Champion", "Command Retinue (Delvarus)"],
                               retinue=retinue_links("delvarus", [triarii("delvarus-triarii", root=False)]),
                               master=False,
                               extra_groups=[take(dv, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)])]))
    return out


def angron():
    return primarch(LR, "Angron, the Red Angel", 515, (9, 6, 7, 6, 6, 7, 6, 10, "1+/4+"),
                    ["Armour of Mars", "Gorefather & Gorechild", "Spite Furnace", "Frag Grenades"],
                    ["Primarch Armour", "The Red Angel", "Butcher's Nails", "Furious Charge", "Sire of the World Eaters",
                     "The Nails Demand Blood", "Primarch Retinue (Angron)"],
                    retinue=primarch_retinue("angron", extra=[devourers("angron-devourers", root=False)]),
                    other=DAEMON_ANGRON, profile_name="Angron", loyalist=False,
                    extra_groups=[slot(ANGRON, "Replace Gorefather & Gorechild", "Gorefather & Gorechild",
                                       [("Widowmaker", 0)])])


def daemon_angron():
    return primarch(LR, "Angron, the Red Angel (Daemon Primarch)", 650,
                    (9, 5, 8, 7, 8, 7, 8, 10, "2+/4+"),
                    ["Blades of the Red Angel", "Daemonic Armour"],
                    ["Daemon Primarchs", "Daemon", "Fear", "Fearless", "Fleet", "Furious Charge", "Eternal Warrior",
                     "Adamantium Will", "Master of the Legion", "Daemonic Flight", "Blood Calls to Blood",
                     "The Red Angel Descends", "The Nails Sing", "Only one Angron"],
                    other=ANGRON, unit_type="Monstrous Creature (Character)", loyalist=False, core=False,
                    profile_name="Angron, the Red Angel")


# ------------------------------------------------------------------ Legion-wide Chainaxe
def add_chainaxes(roots, pits_rite=None):
    """World Eaters Armoury: any model eligible to carry a Close Combat Weapon (Chainsword) may take a Chainaxe (+4).
    - every choice group offering a Chainsword also offers a Chainaxe for +4 (unless it already offers one);
    - every 'replace Chainsword (any number)' squad block gets a Chainaxe option;
    - units whose models carry a fixed Chainsword get a squad-level 'replace Chainsword with Chainaxe' block."""
    cs, ca = W("Chainsword"), W("Chainaxe")
    done = set()
    for r in roots:
        pits = pits_rite and r.get("name") in ("Legion Assault Squad", "Rampager Squad")
        # characters with a fixed Chainsword on the unit itself: turn it into a replaceable slot
        own = r.find("entryLinks")
        if r.get("type") == "unit" and own is not None:
            for lk in list(own):
                if lk.get("targetId") == cs:
                    own.remove(lk)
                    add_to(r, "selectionEntryGroups", [slot(uid(r.get("id"), "we-chainaxe"), "Replace Chainsword",
                                                            "Chainsword", [])])
        for g in list(r.iter("selectionEntryGroup")):
            if id(g) in done:
                continue
            done.add(id(g))
            if (g.get("name") or "").startswith("Servo-automata"):
                continue  # Servo-automata may not take Chainaxes
            links = g.find("entryLinks")
            if links is None:
                continue
            targets = [lk.get("targetId") for lk in links]
            if ca in targets:
                continue
            if cs in targets:
                for lk in list(links):
                    if lk.get("targetId") != cs:
                        continue
                    cost = 0
                    c = lk.find("costs")
                    if c is not None and len(c):
                        cost = float(c[0].get("value"))
                    new = link(uid(lk.get("id"), "we-chainaxe"), ca, "Chainaxe", cost=int(cost + 4),
                               mods=[modifier("set", PTS, int(cost + 2), conds=[rite(pits_rite)])] if pits else None)
                    if g.get("defaultSelectionEntryId") is not None:
                        new.set("sortIndex", "90")
                    links.append(new)
            elif "replace Chainsword" in (g.get("name") or ""):
                links.append(link(uid(g.get("id"), "we-chainaxe"), ca, "Chainaxe", cost=4))
        if r.get("type") != "unit":
            continue
        # squads: models with a fixed Chainsword
        has_block = any("replace Chainsword" in (g.get("name") or "") for g in r.iter("selectionEntryGroup"))
        mids = []
        for m in r.iter("selectionEntry"):
            if m.get("type") != "model" or m.get("name") == "Servo-automata":
                continue
            el_links = m.find("entryLinks")
            if el_links is not None and any(lk.get("targetId") == cs for lk in el_links):
                mids.append(m.get("id"))
        if mids and not has_block:
            opts = [("Chainaxe", 4, [modifier("set", PTS, 2, conds=[rite(pits_rite)])])] if pits else [("Chainaxe", 4)]
            add_to(r, "selectionEntryGroups", [model_swaps(uid(r.get("id"), "we-chainaxe"),
                                                           "World Eaters: replace Chainsword with Chainaxe (any number)",
                                                           r.get("id"), mids, opts)])


# ------------------------------------------------------------------ Caedere Weapon
CAEDERE_PTS = 15


def _pts_cap(g, parents):
    """The nearest enclosing group (or g itself) with a points cap: (group, constraint id) or (None, None)."""
    x = g
    while x is not None and x.tag.split("}")[-1] != "selectionEntry":
        if x.tag.split("}")[-1] == "selectionEntryGroup":
            cs = x.find("constraints")
            for c in (cs if cs is not None else []):
                if c.get("field") == PTS:
                    return x, c.get("id")
        x = parents.get(x)
    return None, None


def add_caedere(ctx):
    """Caedere Weapon (+15): Independent Characters (Praetor, Centurion) and squad Sergeants with access to the Space
    Marine Armoury may replace a Chainsword with it. Not counted towards the Armoury cap; never in Terminator Armour."""
    cs, cw = W("Chainsword"), W("Caedere Weapon")
    tda = {W(n) for n in L.TDA}
    done = set()
    count = 0
    for r in ctx.all_entries():
        parents = {c: p for p in r.iter() for c in p}
        for e in r.iter("selectionEntry"):
            if id(e) in done:
                continue
            gs_ = e.find("selectionEntryGroups")
            own_groups = list(gs_) if gs_ is not None else []
            is_ic = e.get("type") == "unit" and e.get("name") in ("Legion Praetor", "Legion Centurion")
            # squad Sergeants only (not Command Squad Apothecaries / Standard Bearers with their own Armoury access)
            is_sgt = "Sergeant" in (e.get("name") or "") and any(
                g.get("name") == "Space Marine Armoury (max 50 pts)" for g in own_groups)
            if not (is_ic or is_sgt):
                continue
            done.add(id(e))
            eid = e.get("id")
            fixed = e.find("entryLinks")
            if fixed is not None and any(lk.get("targetId") in tda for lk in fixed):
                continue  # Terminator Sergeants
            forbid = L.has_tda(eid, deep=False) if is_ic else []
            # fixed Chainsword on the model -> a replace slot (Chainaxe is added by add_chainaxes)
            if fixed is not None:
                for lk in list(fixed):
                    if lk.get("targetId") == cs:
                        fixed.remove(lk)
                        add_to(e, "selectionEntryGroups", [slot(uid(eid, "we-caedere"), "Replace Chainsword",
                                                                "Chainsword", [])])
            for g in list(e.iter("selectionEntryGroup")):
                links = g.find("entryLinks")
                if links is None or cw in [lk.get("targetId") for lk in links]:
                    continue
                cs_links = [lk for lk in links if lk.get("targetId") == cs]
                if not cs_links:
                    continue
                c = cs_links[0].find("costs")
                base = float(c[0].get("value")) if c is not None and len(c) else 0
                lid = uid(g.get("id"), "we-caedere")
                mods = []
                if forbid:
                    mods = [modifier("set", "hidden", "true", groups=[any_of(*forbid)]),
                            modifier("set", uid(lid, "max"), 0, groups=[any_of(*L.has_tda(eid, deep=False))])]
                new = link(lid, cw, "Caedere Weapon", cost=int(base + CAEDERE_PTS), mods=mods,
                           constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)])
                new.set("sortIndex", "91")
                links.append(new)
                count += 1
                # not counted towards the Armoury points cap
                capg, cap_id = _pts_cap(g, {**parents, **{c_: p for p in e.iter() for c_ in p}})
                if capg is not None:
                    add_mods(capg, [modifier("increment", cap_id, int(base + CAEDERE_PTS),
                                             conds=[L.own(cw, eid)] if is_ic else [has(cw, eid)])])
    return count


# ------------------------------------------------------------------ extend
def extend(ctx):
    ctx.legion_rules([LR, "Blood Frenzy", "World Eaters Armoury"])
    roots = [rampager(), red_butchers(), red_hand(), inductii(), devourers(), triarii(), *characters(), angron(),
             daemon_angron()]
    ctx.add_units(*roots)
    ctx.finish()  # new retinues become shared entries before the Legion-wide changes below

    # Rites of War
    ctx.add_rite("Berserker Assault", RULES["Berserker Assault"], limit_hs=True,
                 errors=[("the Detachment must include at least one Rampager Squad as a Troops choice.",
                          [cond(RAMPAGER, "force", "lessThan", 1)]),
                         fortification_error()])
    immobile = [L.TRANSPORTS["Legion Drop Pod"], L2.T["Legion Dreadnought Drop Pod"]]
    ctx.add_rite("The Crimson Path", RULES["The Crimson Path"],
                 errors=[("the Detachment may not include Immobile units (Legion Drop Pods, Dreadnought Drop Pods).",
                          [any_of(*[cond(i, "force", "atLeast", 1) for i in immobile])]),
                         fortification_error()])

    # Armoury: Caedere Weapon for Independent Characters and Sergeants with Armoury access; Chainaxes everywhere
    add_caedere(ctx)
    add_chainaxes(ctx.all_entries(), pits_rite="Berserker Assault")
