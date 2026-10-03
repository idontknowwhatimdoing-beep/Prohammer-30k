"""V Legion - White Scars (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, allegiance_only, option, upgrade, clone, retinue_links,
                            command_squad_for, named_character, primarch, required_choice, add_consul, add_group,
                            add_entry, LOW, TRAITOR, LOYALIST)
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile, has_tda, no_tda
from legiones2 import (slot, take, pool, transports, add_mods, add_to, foc, rite_id, rite, TROOPS, ELITES, FA, HQ,
                       model_swaps, pa_armoury, _negate)
from legiones_wargear import ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR

LEGION = "V - White Scars"
LR = "Legiones Astartes (White Scars)"
# "he may select one psychic power from the normal Psychic Powers list" (kept as built before: four disciplines)
YESUGEI_DISCIPLINES = ["Biomancy", "Divination", "Pyromancy", "Telepathy"]

RULES = {
    LR: ("Models with this rule belong to the V Legion and use the White Scars Legion special rules: Swift Advance, "
         "Born in the Saddle and Mounted Brotherhoods."),
    "Swift Advance": (
        "A White Scars Infantry unit composed entirely of models in Power Armour, Artificer Armour or Recon Armour may "
        "make a Swift Advance: in its Shooting phase it may forgo shooting and instead move an additional D6\". It may "
        "move even if it made a Normal Move in the preceding Movement phase, is not slowed by Difficult Terrain during "
        "this move, may not move within 1\" of an enemy model and may not charge in the same player turn. Models in any "
        "form of Terminator Armour or Hardened Armour may not use Swift Advance."),
    "Born in the Saddle": (
        "White Scars models mounted on Bikes or Jetbikes gain Skilled Rider. Legion Bike Squadrons and Legion Sky Hunter "
        "Jetbike Squadrons gain Hit & Run; the unit may only use it if every model, including any attached Independent "
        "Character, is mounted on a Bike or Jetbike. Legion Attack Bike Squadrons do not gain Hit & Run from this rule."),
    "Mounted Brotherhoods": (
        "In a White Scars Detachment Legion Bike Squadrons are always Troops choices and may fulfil the army's compulsory "
        "Troops selections. They are otherwise identical to the Legion Bike Squadron entry."),
    # Armoury
    "Power Glaive": (
        "Any White Scars Character able to select a Power Weapon may instead select a Power Glaive for the cost of a Power "
        "Weapon for that unit or model +10 points; a model with a Power Weapon as part of its basic wargear may exchange it "
        "for +10 points. At the beginning of each Assault "
        "phase the bearer chooses how it is wielded (One-Handed: User, Power Weapon; Two-Handed: User +1, Power Weapon, "
        "Two-Handed) for the rest of that Assault phase."),
    "Cavalry Lance": (
        "During the first round of a close combat in which the bearer charged, it receives +1 Initiative; during any round "
        "of close combat in which it did not charge it suffers -1 Initiative. A Chogorian Warlance is a one-handed weapon. "
        "Only White Scars models with access to the Space Marine Armoury mounted on a Bike or Jetbike may purchase it "
        "(+15 points); it does not count towards the Space Marine Armoury points limit."),
    "Cyber-hawk": (
        "At the beginning of each White Scars turn place the Cyber-hawk marker anywhere on the battlefield (it may be moved "
        "at the beginning of each later White Scars turn). When a White Scars Infantry unit attacks an enemy unit with at "
        "least one model within 6\" of the marker it may re-roll To Hit rolls of 1 with shooting attacks, and its charge "
        "distance against that unit is 7\" instead of 6\". The marker cannot be attacked, does not block movement or line "
        "of sight and has no characteristics. One White Scars Praetor may purchase a Cyber-hawk for +10 points."),
    "Horsetail Talisman": (
        "One White Scars Independent Character may purchase it (+25 points); only one per army. Once per battle, at the "
        "beginning of the White Scars Shooting phase, the bearer and every friendly White Scars non-vehicle unit (including "
        "Bikes and Jetbikes) with a model within 6\" may move D6\" instead of shooting. Such a unit may not move within 1\" "
        "of an enemy model, must keep coherency and may not charge that player turn. Units Falling Back, embarked or locked "
        "in close combat may not benefit."),
    # Stormseer
    "Stormseer": (
        "A White Scars Legion Centurion may be upgraded to a Stormseer Consul for +35 points (a White Scars army may not "
        "select the normal Librarian Consul). Replaces the Chainsword with a Force Weapon. Psyker (Mastery Level 1), "
        "Adamantium Will, Legion Support Officer. Knows Unseen Bolt. May purchase a Psychic Hood (+25); all other equipment "
        "is selected normally from the Space Marine Armoury."),
    "Unseen Bolt": (
        "Psychic shooting power (36\", S6, AP4, Assault 1, Blast, Pinning), used in the Shooting phase instead of firing "
        "another weapon. Take a Psychic test using the normal ProHammer psychic rules; if successful resolve the attack. "
        "May not be invoked during Return Fire, Overwatch or Stand & Shoot."),
    "Epistolary (Stormseer)": (
        "A Stormseer may be upgraded to Mastery Level 2 for +25 points and then selects one additional psychic power from "
        "Divination, Biomancy, Telepathy or Pyromancy."),
    # Rites of War
    "Chogorian Brotherhood": (
        "EFFECTS - Ride Like the Wind: Legion Sky Hunter Jetbike Squadrons may be Troops; Legion Bike Squadrons and Sky "
        "Hunter Squadrons may fulfil compulsory Troops. Lightning Encirclement: White Scars Bike, Sky Hunter, Attack Bike, "
        "Land Speeder and Javelin squadrons gain Outflank; White Scars Infantry units gain Outflank if no model wears "
        "Terminator Armour or carries a Heavy weapon (a Dedicated Transport may enter play with its unit). Master of the "
        "Hunt: the White Scars player may re-roll Reserve rolls (successful or failed) for units in this Detachment; the "
        "second result stands. Strike and Vanish: a White Scars Bike or Jetbike unit that successfully uses Hit & Run rolls "
        "one additional D6 for its Hit & Run move and discards the lowest.\n"
        "While this Rite is chosen, a Praetor or Centurion mounted on a Space Marine Bike may upgrade it to a Jetbike for "
        "+5 points.\n"
        "LIMITATIONS - The Warlord must be mounted on a Space Marine Bike or a Jetbike. The compulsory Troops must be Legion "
        "Bike Squadrons or Legion Sky Hunter Jetbike Squadrons. No more than one Heavy Support choice. If every Bike and "
        "Jetbike unit in the Detachment has been completely destroyed by the end of the battle, the enemy receives an "
        "additional 150 Victory Points (Victory Point missions only)."),
    "The Sagyar Mazan": (
        "LOYALIST ONLY.\nEFFECTS - Death Seekers: whenever a non-vehicle White Scars unit from this Detachment is "
        "completely destroyed and would award Victory Points, roll a D6: 1-3 resolve normally; 4-5 it awards no Victory "
        "Points; 6 it awards none and the White Scars player gains 50 Victory Points. The Serpent's Eye: during the first "
        "round of any close combat non-vehicle White Scars units from this Detachment are Fearless. Not Yet Dead: "
        "non-vehicle White Scars units gain Feel No Pain (6+), or improve an existing Feel No Pain by one step (max 4+). "
        "Ebon Keshig: Ebon Keshig units may be Troops and may fulfil compulsory Troops.\n"
        "LIMITATIONS - No unit may voluntarily begin the battle in Reserve; units required by their own rules to begin in "
        "Reserve may not be selected. Units may not voluntarily withdraw from close combat and must Pursue whenever able. "
        "Only a Loyalist White Scars Detachment; may not include Jaghatai Khan; no Fortification; never more Vehicle units "
        "than non-vehicle Infantry units."),
    # Units
    "Dragon Dao": (
        "A Power Weapon. At the beginning of each Assault phase the bearer may wield it with both hands: +2 Strength and "
        "-2 Initiative for that Assault phase, and no bonus Attack for two close-combat weapons."),
    "Sabotage (Falcon's Claws)": (
        "After both armies have deployed but before the first game turn, nominate one enemy unit, Vehicle or Fortification "
        "(an Independent Character only if part of another unit). It suffers D6 Strength 5 AP6 hits (against the lowest "
        "Armour Value for Vehicles or Fortifications). Casualties do not cause Morale or Pinning tests."),
    # Characters
    "The Tails of the Dragon": (
        "A pair of Power Weapons; the bonus Attack for two close-combat weapons is included in Qin Xa's profile. At the "
        "beginning of each Assault phase choose a form: Swift Form (+1 Strength) or Sundering Form (+3 Strength and "
        "Unwieldy)."),
    "Master of the Keshig": (
        "Qin Xa may select one Ebon Keshig squad or Legion Terminator Command Squad as his retinue. It does not occupy a "
        "separate Force Organisation slot; Qin Xa and his retinue count as a single HQ selection."),
    "Chief Stormseer": (
        "Yesugei knows Unseen Bolt and may select one psychic power from the normal Psychic Powers list. He otherwise "
        "follows all normal rules for Psykers of Mastery Level 2."),
    "Brotherhood of the Storm": (
        "Shiban Khan has Fleet. Any White Scars unit he has joined also gains Fleet while he remains part of it."),
    "Command Retinue (White Scars Khans)": (
        "The character may select one Legion Command Squad (Hibou Khan and Hasik Noyan-Khan: or one Legion Veteran Squad) "
        "as his retinue; it does not occupy a separate Force Organisation slot. If the character is mounted on a Bike or "
        "Jetbike, every model in the retinue may purchase a Space Marine Bike for +20 points per model; if the character "
        "is mounted on a Jetbike, the retinue may instead purchase Jetbikes (+25 points per model). A retinue mounted on "
        "Bikes or Jetbikes may not take Jump Packs or a Dedicated Transport."),
    "Breath of the Storm": (
        "A Master-crafted Power Weapon: +2 Strength during an Assault phase in which Hibou Khan charged, +1 Strength during "
        "any other Assault phase."),
    "The Seeker of Atonement": (
        "If Hibou Khan and his unit win a close combat and at least one enemy unit is destroyed or Retreats as a result, "
        "they gain Fearless until the end of the following White Scars player turn."),
    "Lord of the Horde": (
        "While Hasik is part of a White Scars unit, that unit has Stubborn and may re-roll failed Morale tests (the second "
        "result stands)."),
    "Jetbike (White Scars)": (
        "A character mounted on a Space Marine Bike may upgrade it to a Jetbike for +5 points; the model follows the normal "
        "ProHammer rules for Jetbikes."),
    # Jaghatai
    "Wildfire Panoply": "Counts as Primarch Armour.",
    "White Tiger Dao": "A Master-crafted Power Weapon; attacks with it are resolved at +1 Strength.",
    "Master of the Hunt (Jaghatai)": (
        "Jaghatai Khan and any Bike or Jetbike unit he has joined gain Hit & Run. If the unit already has Hit & Run, the "
        "controlling player may re-roll the dice for its Hit & Run move (the second result stands)."),
    "Lightning Strike": "During an Assault phase in which Jaghatai Khan charged, his Strength is increased by +1.",
    "Sire of the White Scars": (
        "Friendly White Scars Bike and Jetbike units with at least one model within 12\" of Jaghatai Khan may re-roll "
        "failed Dangerous Terrain tests and failed Hit & Run tests."),
    "Ride Beyond the Horizon": (
        "Once per battle, at the beginning of the White Scars Movement phase, if Jaghatai Khan is mounted on the Sojutsu "
        "Pattern Voidbike and has joined a Bike or Jetbike unit, remove him and that unit from the battlefield and place "
        "them into Ongoing Reserves. They automatically return during the following White Scars turn and must enter play "
        "using Outflank; no Reserve roll is required."),
    "Sojutsu Pattern Voidbike": (
        "Jaghatai Khan's Unit Type becomes Jetbike and he follows all normal ProHammer rules for Jetbikes (+40 points)."),
    "Primarch Retinue (Jaghatai Khan)": (
        "Jaghatai Khan may select a Legion Honour Guard Squad or a Golden Keshig Squadron as his Primarch Retinue (no "
        "additional Force Organisation selection). If he is mounted on the Sojutsu Pattern Voidbike, a Legion Honour Guard "
        "Squad selected this way may equip every model with a Jetbike for +35 points per model (all models must take it)."),
}

WEAPONS_ = {
    "Chogorian Warlance": ("-", "User", "-", "Power Weapon, Cavalry Lance"),
    "Unseen Bolt": ('36"', "6", "4", "Assault 1, Blast, Pinning (psychic)"),
    "Breath of the Storm": ("-", "User +2/+1", "-", "Power Weapon, Master-crafted (+2 S when charging, else +1 S)"),
    "White Tiger Dao": ("-", "User +1", "-", "Power Weapon, Master-crafted"),
    "Storm's Voice": ('12"', "6", "4", "Pistol 2, Rending, Concussive, Master-crafted"),
}
MULTI = {
    "Power Glaive": {"Power Glaive - One-Handed": ("-", "User", "-", "Power Weapon"),
                     "Power Glaive - Two-Handed": ("-", "User +1", "-", "Power Weapon, Two-Handed")},
    "Dragon Dao": {"Dragon Dao - One-Handed": ("-", "User", "-", "Power Weapon"),
                   "Dragon Dao - Two-Handed": ("-", "User +2", "-", "Power Weapon, -2 Initiative, no bonus Attack")},
    "The Tails of the Dragon": {
        "Tails of the Dragon - Swift Form": ("-", "User +1", "-", "Power Weapon, paired (bonus Attack included)"),
        "Tails of the Dragon - Sundering Form": ("-", "User +3", "-", "Power Weapon, Unwieldy, paired (bonus Attack "
                                                                       "included)")},
}
WEAPON_RULES_ = {
    "Power Glaive": ["Power Glaive"], "Chogorian Warlance": ["Cavalry Lance"], "Unseen Bolt": ["Unseen Bolt", "Pinning"],
    "Dragon Dao": ["Dragon Dao"], "The Tails of the Dragon": ["The Tails of the Dragon", "Unwieldy"],
    "Breath of the Storm": ["Breath of the Storm", "Master-Crafted"],
    "White Tiger Dao": ["White Tiger Dao", "Master-Crafted"],
    "Storm's Voice": ["Rending", "Concussive", "Master-Crafted"],
}
WARGEAR_ = {
    "Cyber-hawk": RULES["Cyber-hawk"],
    "Horsetail Talisman": RULES["Horsetail Talisman"],
    "Wildfire Panoply": ("Counts as Primarch Armour.", ["Primarch Armour"]),
    "Sojutsu Pattern Voidbike": RULES["Sojutsu Pattern Voidbike"],
    "Jetbike": "The model is mounted on a Jetbike and follows the normal ProHammer rules for Jetbikes.",
    "Iron Halo (Named Character)": (
        "Grants a 4+ Invulnerable Save. Part of this named character's own wargear; not counted towards the army's normal "
        "limit of one Iron Halo."),
}


def register():
    ARMY_RULES.update(RULES)
    register_data(weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_, multi_profile=MULTI)
    # Scimitar Jetbike of the Golden Keshig: Heavy Bolter with Hellfire Rounds
    WEAPONS["Scimitar Jetbike with Heavy Bolter and Hellfire Rounds"] = ["Heavy Bolter", "Heavy Bolter - Hellfire Round"]
    WEAPON_RULES["Scimitar Jetbike with Heavy Bolter and Hellfire Rounds"] = ["Hellfire"]
    WEAPONS.setdefault("M.40 Stalker Bolter", ["M.40 Stalker Bolter"])
    # Rites of War changing the compulsory Troops
    for n in ["Legion Tactical Squad", "Legion Assault Squad", "Legion Breacher Siege Squad"]:
        L2.NOT_LINE_UNDER[n].append("Chogorian Brotherhood")
    L2.TROOP_RITES["Legion Sky Hunter Jetbike Squadron"].append("Chogorian Brotherhood")


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


def character_variant(roots, base, new, extra, skip_names=()):
    """'Any Character able to select <base> may instead select <new>': adds <new> next to every <base> option
    inside a Character model's own weapon groups, for the <base> price in that list + extra (author: always the
    Power Weapon price +10, so +10 where the Power Weapon is basic wargear). Returns the number of links added."""
    base_id = W(base)
    done = set()
    n = 0
    for r in roots:
        for e in r.iter("selectionEntry"):
            if not is_character(e) or e.get("name") in skip_names:
                continue
            for g in e.iter("selectionEntryGroup"):
                if id(g) in done or "Servo-automata" in (g.get("name") or ""):
                    continue
                done.add(id(g))
                links = g.find("entryLinks")
                if links is None:
                    continue
                for lk in list(links):
                    if lk.get("targetId") != base_id:
                        continue
                    cs = lk.find("costs")
                    cost = float(cs[0].get("value")) if cs is not None and len(cs) else 0
                    nid = uid(lk.get("id"), "variant", new)
                    cons = []
                    if any(c.get("type") == "max" for c in lk.iter("constraint")):
                        cons = [constraint(uid(nid, "max"), "max", 1, auto=True)]
                    new_l = link(nid, W(new), new, cost=int(cost + extra) or None,
                                 constraints=cons)
                    if g.get("defaultSelectionEntryId") is not None:
                        new_l.set("sortIndex", str(int(lk.get("sortIndex") or 1) + 100))
                    links.append(new_l)
                    n += 1
    return n


def add_links(grp, key, items, hide=None):
    """Add shared items [(name, pts)] to a group, each max 1; hide: conditions that hide and forbid them."""
    links = grp.find("entryLinks")
    if links is None:
        links = el("entryLinks")
        grp.append(links)
    for n, p in items:
        lid = uid("link", grp.get("id"), key, n)
        mods = []
        if hide:
            g = [or_group([c for c in hide if c.tag == "condition"], [c for c in hide if c.tag != "condition"])]
            mods = [modifier("set", "hidden", "true", groups=g), modifier("set", uid(lid, "max"), 0, groups=g)]
        links.append(link(lid, W(n), n, cost=p or None, mods=mods,
                          constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))


def or_group(conds=(), groups=()):
    """An 'or' condition group that may contain nested condition groups."""
    return el("conditionGroup", {"type": "or"}, [wrap("conditions", list(conds)), wrap("conditionGroups", list(groups))])


def block(e, max_id, conds=(), groups=()):
    """Hide an entry/link and set its max to 0 while any of conds/groups is true."""
    g = [or_group(conds, groups)]
    add_mods(e, [modifier("set", "hidden", "true", groups=g), modifier("set", max_id, 0, groups=g)])


def parent_of(root, child):
    for p in root.iter():
        for c in p:
            if c is child:
                return p
    return None


def owner_entry(root, node):
    """The nearest selectionEntry that contains node."""
    p = parent_of(root, node)
    while p is not None and p.tag != "selectionEntry":
        p = parent_of(root, p)
    return p


def warlance_beside_armoury(root, key, hide=None):
    """Chogorian Warlance (+15) for every model of root that has a Space Marine Armoury group; outside the points cap."""
    for g in [g for g in root.iter("selectionEntryGroup") if (g.get("name") or "").startswith("Space Marine Armoury")]:
        owner = owner_entry(root, g)
        if owner is None:
            continue
        ng = group(uid("grp", key, owner.get("id"), "ws-warlance"), "White Scars Wargear")
        add_links(ng, "ws", [("Chogorian Warlance", 15)], hide=hide)
        add_group(owner, ng)


def find_group(e, name):
    for g in e.iter("selectionEntryGroup"):
        if g.get("name") == name:
            return g
    return None


def ic_wargear_group(e):
    """The 'Additional Wargear' group inside a Praetor/Centurion's 100-point Armoury."""
    arm = find_group(e, "Space Marine Armoury (max 100 pts)")
    return find_group(arm, "Additional Wargear")


def hide_consul(ctx, name):
    cen = ctx.unit("Legion Centurion")
    cid = L.consul_id(name)
    for e in cen.iter("selectionEntry"):
        if e.get("id") == cid:
            add_mods(e, [modifier("set", "hidden", "true"), modifier("set", uid(cid, "max"), 0)])


def consul_replaces_chainsword(ctx, cid):
    cen = ctx.unit("Legion Centurion")
    gid = uid("slot", "centurion", "Chainsword")
    for g in cen.iter("selectionEntryGroup"):
        if g.get("id") == gid:
            c = [has(cid, L.CENTURION)]
            add_mods(g, [modifier("set", uid(gid, "min"), 0, conds=c), modifier("set", uid(gid, "max"), 0, conds=c),
                         modifier("set", "hidden", "true", conds=c)])


def consul_unlocks_psyker_items(ctx, cid, items=("Psychic Hood",)):
    """Let a Legion-specific psyker Consul take Armoury items reserved for psykers (e.g. the Psychic Hood)."""
    cen = ctx.unit("Legion Centurion")
    targets = {W(n) for n in items}
    psy = {L.consul_id(c) for c in L.PSYKER_CONSULS}
    for lk in cen.iter("entryLink"):
        if lk.get("targetId") not in targets:
            continue
        seen = set()
        for g in lk.iter("conditionGroup"):
            if id(g) in seen or g.get("type") != "and":
                continue
            seen.add(id(g))
            cs = g.find("conditions")
            if cs is not None and cs and all(c.get("childId") in psy for c in cs):
                cs.append(lacks(cid, L.CENTURION))


def model(u, name, cost, mn, mx, utype, stats, kit, groups=(), mods=(), rules_=(), cons_ids=None):
    mid = uid("model", u, name)
    mn_id, mx_id = uid(mid, "min"), uid(mid, "max")
    return entry(mid, name, typ="model", cost=cost, mods=list(mods),
                 constraints=[constraint(mn_id, "min", mn, auto=bool(mods)), constraint(mx_id, "max", mx, auto=bool(mods))],
                 profiles=[unit_profile(u, name, utype, *stats)], links=[gear(mid, k) for k in kit],
                 groups=list(groups), infolinks=rules_links(list(rules_), key=mid))


def strip_category_mods(e):
    """Remove category-changing modifiers from the top of a cloned unit (a retinue is never a Troops choice)."""
    ms = e.find("modifiers")
    if ms is None:
        return e
    for m in list(ms):
        if m.get("field") == "category":
            ms.remove(m)
    return e


def mobility_group(u):
    """Named Khans: Space Marine Bike (+35), then Jetbike upgrade (+5)."""
    jid = uid(u, "jetbike")
    no_bike = [lacks(W("Space Marine Bike"), u)]
    jet = entry(jid, "Upgrade Bike to Jetbike", cost=5,
                mods=[modifier("set", "hidden", "true", conds=no_bike), modifier("set", uid(jid, "max"), 0, conds=no_bike)],
                constraints=[constraint(uid(jid, "max"), "max", 1, auto=True)], links=[gear(jid, "Jetbike")],
                infolinks=rules_links(["Jetbike (White Scars)", "Skilled Rider"], key=jid))
    g = take(u, "Mobility", [("Space Marine Bike", 35)])
    add_to(g, "selectionEntries", [jet])
    return g


RETINUE_JETBIKE_COST = 25


def jetbike_option(key, unit_id, char_id):
    """Khan on a Jetbike: the retinue may purchase Jetbikes (entire squad) instead of Space Marine Bikes."""
    name = "Jetbikes (entire squad)"
    e = per_model(key, name, RETINUE_JETBIKE_COST, unit_id, ["Jetbike"])
    block(e, uid(uid("squadwide", key, name), "max"), conds=[lacks(uid(char_id, "jetbike"), char_id)])
    return e


def bike_option(key, unit_id, char_id):
    """'If the character is mounted on a Bike or Jetbike, every model in the retinue may purchase a Space Marine Bike
    for +20 points per model.' (Jetbike Khans: Jetbikes instead)"""
    name = "Space Marine Bikes (entire squad)"
    e = per_model(key, name, 20, unit_id, ["Space Marine Bike"])
    block(e, uid(uid("squadwide", key, name), "max"),
          conds=[lacks(W("Space Marine Bike"), char_id), has(uid(char_id, "jetbike"), char_id)])
    return e


def mounted_blocks(squad, mounted_ids):
    """Bikes/Jetbikes exclude Jump Packs and a Dedicated Transport (and Jump Packs exclude the mounts)."""
    sid = squad.get("id")
    on = [has(m, sid) for m in mounted_ids]
    tr = find_group(squad, "Dedicated Transport")
    block(tr, uid_of_max(tr), conds=on)
    for e in squad.iter("selectionEntry"):
        if e.get("name") == "Jump Packs (entire squad)":
            block(e, uid_of_max(e), conds=on)
            for m in mounted_ids:
                for x in squad.iter("selectionEntry"):
                    if x.get("id") == m:
                        block(x, uid_of_max(x), conds=[has(e.get("id"), sid)])


def uid_of_max(e):
    for c in e.iter("constraint"):
        if c.get("type") == "max" and c.get("field") == "selections":
            return c.get("id")
    raise KeyError(e.get("name"))


def veteran_retinue(key, char_id):
    vs = strip_category_mods(clone(L2.veteran_squad(), key))
    bk, jk = key + "bikes", key + "jetbikes"
    add_to(vs, "selectionEntries", [bike_option(bk, vs.get("id"), char_id), jetbike_option(jk, vs.get("id"), char_id)])
    add_to(vs, "infoLinks", rules_links(["Retinue"], key=key))
    mounted_blocks(vs, [uid("squadwide", bk, "Space Marine Bikes (entire squad)"),
                        uid("squadwide", jk, "Jetbikes (entire squad)")])
    return vs


def khan_command_squad(key, char_id):
    """Legion Command Squad for a Khan: its Space Marine Bikes become Jetbikes when the Khan rides a Jetbike."""
    jk = key + "-jetbikes"
    cs = command_squad_for(key, char_id)
    jet = jetbike_option(jk, cs.get("id"), char_id)
    add_to(cs, "selectionEntries", [jet])
    for e in cs.iter("selectionEntry"):
        if e.get("name") == "Space Marine Bikes":
            block(e, uid(e.get("id"), "max"), conds=[has(uid(char_id, "jetbike"), char_id)])
    tr = find_group(cs, "Dedicated Transport")
    block(tr, uid_of_max(tr), conds=[has(jet.get("id"), cs.get("id"))])
    return cs


def talisman_group(key):
    tid = uid("ws", "horsetail", key)
    return group(uid("grp", "ws-wargear", key), "White Scars Wargear", entries=[
        entry(tid, "Horsetail Talisman", cost=25, links=[gear(tid, "Horsetail Talisman")],
              constraints=[constraint(uid(tid, "max"), "max", 1, auto=True)])])


# ------------------------------------------------------------------ units
def golden_keshig(key="Golden Keshig Squadron", root=True):
    name = "Golden Keshig Squadron"
    u = uid("unit", key)
    kit = ["Power Armour", "Scimitar Jetbike with Heavy Bolter and Hellfire Rounds", "Bolt Pistol", "Chogorian Warlance",
           "Frag Grenades"]
    keshig = model(u, "Golden Keshig", 55, 2, 4, "Jetbike", (5, 4, 4, 5, 1, 4, 2, 9, "2+"), kit)
    champ = model(u, "Golden Keshig Champion", 0, 1, 1, "Jetbike (Character)", (5, 4, 4, 5, 1, 4, 3, 10, "2+"), kit)
    jw, _ = pool(u, "Jetbike Weapons (1 per 3 models, replace Heavy Bolter with Hellfire Rounds)", u,
                 [("Multi-Melta", 10), ("Volkite Culverin", 10)], 0, every=3)
    return entry(u, name, typ="unit", cost=180 - 2 * 55, cats=[foc(FA, "Fast Attack", u)] if root else [],
                 infolinks=rules_links([LR, "Deep Strike", "Skilled Rider", "Hit & Run"] + ([] if root else ["Retinue"]), key=u),
                 entries=[champ, keshig, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[jw])


def ebon_keshig(key="Ebon Keshig", root=True):
    name = "Ebon Keshig"
    u = uid("unit", key)
    m = model(u, "Ebon Keshig", 45, 5, 10, "Infantry", (5, 4, 4, 4, 1, 5, 3, 9, "2+/5+"),
              ["Terminator Armour", "Dragon Dao"])
    tr = transports(u, u, ["Land Raider Phobos", "Land Raider Proteus", "Anvillus Pattern Dreadclaw Drop Pod",
                           "Legion Spartan Assault Tank"], orbital=False)
    # a squad of more than five may only take the Spartan (Transport Capacity)
    big = [cond("model", u, "greaterThan", 5)]
    for lk in tr.iter("entryLink"):
        if lk.get("name") != "Legion Spartan Assault Tank":
            mid_ = uid(lk.get("id"), "ws-max")
            add_to(lk, "constraints", [constraint(mid_, "max", 1, auto=True)])
            block(lk, mid_, conds=big)
    mods = []
    if root:
        sm = [rite("The Sagyar Mazan")]
        mods = [modifier("set-primary", "category", TROOPS, conds=sm), modifier("remove", "category", ELITES, conds=sm),
                modifier("add", "category", gs.CAT_LINE, conds=sm)]
    e = entry(u, name, typ="unit", cost=225 - 5 * 45, cats=[foc(ELITES, "Elites", u)] if root else [], mods=mods,
                 infolinks=rules_links([LR, "Fearless"] + ([] if root else ["Retinue"]), key=u),
                 entries=[m], groups=[tr])
    return allegiance_only(e, loyalist=True)


def dark_sons():
    name = "Dark Sons of Death"
    u = uid("unit", name)
    kit = ["Power Armour", "Two Bolt Pistols", "Power Glaive", "Frag Grenades", "Rad Grenades"]
    sons = model(u, "Dark Son", 35, 4, 9, "Infantry", (4, 4, 4, 4, 1, 4, 1, 9, "3+"), kit)
    sid = uid("model", u, "Death Speaker")
    speaker = model(u, "Death Speaker", 0, 1, 1, "Infantry (Character)", (5, 4, 4, 4, 1, 4, 2, 9, "3+"), kit,
                    groups=[take(sid, "Death Speaker Wargear", [("Artificer Armour", 10), ("Phosphex Bomb", 10, 3)]),
                            pa_armoury(sid, u, 10, skip=("Artificer Armour",))])
    weapons, wmx = pool(u, "Destroyer Weapons (1 per 5 models, 2 per 5 in a Destroyer Company; replace one Bolt Pistol)",
                        u, [("Volkite Serpenta", 5), ("Hand Flamer", 5), ("Plasma Pistol", 15),
                            ("Missile Launcher with Suspensor Web and Rad Missiles", 25)], 0, every=5)
    add_mods(weapons, [modifier("increment", wmx, 1, conds=[rite("Legion Destroyer Company")],
                                repeats=[repeat("model", u, 5)])])
    dc = [rite("Legion Destroyer Company")]
    role = [modifier("set-primary", "category", TROOPS, conds=dc), modifier("remove", "category", ELITES, conds=dc),
            modifier("add", "category", gs.CAT_LINE, conds=dc)]
    jp_id = uid("squadwide", u, "Jump Packs (entire squad)")
    return entry(u, name, typ="unit", cost=200 - 4 * 35, cats=[foc(ELITES, "Elites", u)], mods=role,
                 infolinks=rules_links([LR, "Counter-Attack", "Dual Pistols (Destroyers)", "Destroyer Cadre"], key=u),
                 entries=[speaker, sons, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"]),
                          per_model(u, "Jump Packs (entire squad)", 15, u, ["Jump Pack"])],
                 groups=[weapons, transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                                    "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos"],
                                             block_if=[has(jp_id, u)])])


def falcons_claws():
    name = "Falcon's Claws"
    u = uid("unit", name)
    cid = uid("model", u, "Falcon's Claw")
    lid = uid("model", u, "Falcon's Claw Leader")
    swaps = [("Astartes Shotgun", 0), ("Sniper Rifle", 5)]
    claws = model(u, "Falcon's Claw", 22, 4, 9, "Infantry", (4, 5, 4, 4, 1, 4, 1, 9, "4+"),
                  ["Recon Armour", "M.40 Stalker Bolter", "Bolt Pistol", "Combat Blade", "Frag Grenades"])
    leader = model(u, "Falcon's Claw Leader", 0, 1, 1, "Infantry (Character)", (4, 5, 4, 4, 1, 4, 2, 9, "4+"),
                   ["Recon Armour", "Combat Blade", "Frag Grenades"],
                   groups=[slot(lid, "Replace M.40 Stalker Bolter", "M.40 Stalker Bolter", swaps),
                           pa_armoury(lid, u, 10, slots=["Bolt Pistol"])])
    return entry(u, name, typ="unit", cost=120 - 4 * 22, cats=[foc(FA, "Fast Attack", u)],
                 constraints=[force_limit(u, 1)],
                 infolinks=rules_links([LR, "Scouts", "Infiltrate", "Move Through Cover", "Acute Senses",
                                        "Sabotage (Falcon's Claws)"], key=u),
                 entries=[leader, claws, per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Cameleoline (entire squad)", 5, u, ["Cameleoline"])],
                 groups=[model_swaps(u, "Falcon's Claws: replace M.40 Stalker Bolter (any number)", u, [cid], swaps),
                         L.one_each(u, "Squad Equipment", [("Nuncio Vox", 10)])])


# ------------------------------------------------------------------ characters
def characters():
    out = []
    # Qin Xa
    q = uid("unit", "Qin Xa, Master of the Keshig")
    out.append(named_character(
        LR, "Qin Xa, Master of the Keshig", 180, (6, 4, 4, 4, 3, 5, 4, 10, "2+/4+"),
        ["Tartaros Terminator Armour", "Iron Halo (Named Character)", "The Tails of the Dragon"],
        ["Fearless", "Master of the Keshig"], extra_groups=[talisman_group("qinxa")],
        retinue=retinue_links("qinxa", [ebon_keshig("qinxa-ebon", root=False), L2.terminator_command_squad("qinxa")]),
        profile_name="Qin Xa"))
    # Targutai Yesugei (Legion Support Officer)
    y = uid("unit", "Targutai Yesugei")
    out.append(named_character(
        LR, "Targutai Yesugei", 195, (5, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Force Weapon", "Psychic Hood", "Bolt Pistol", "Frag Grenades"],
        ["Psyker", "Adamantium Will", "Legion Support Officer", "Chief Stormseer"], master=False, compulsory=False,
        extra_groups=[take(y, "Wargear", [("Krak Grenades", 2)]), talisman_group("yesugei"),
                      required_choice(y, "Psychic Discipline (one additional power)",
                                      [(d, []) for d in YESUGEI_DISCIPLINES]),
                      psychic_powers(y, y, 1, YESUGEI_DISCIPLINES, fixed=["Unseen Bolt"],
                                     filters={d: [choice_id(y, "Psychic Discipline (one additional power)", d)]
                                              for d in YESUGEI_DISCIPLINES})]))
    # Shiban Khan
    s = uid("unit", "Shiban Khan")
    out.append(named_character(
        LR, "Shiban Khan", 155, (6, 5, 4, 4, 3, 5, 3, 10, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Power Weapon", "Bolt Pistol", "Frag Grenades"],
        ["Fleet", "Brotherhood of the Storm", "Command Retinue (White Scars Khans)"],
        retinue=retinue_links("shiban", [khan_command_squad("shiban", s)]),
        extra_groups=[take(s, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)]), mobility_group(s),
                      talisman_group("shiban")]))
    # Hibou Khan
    h = uid("unit", "Hibou Khan")
    out.append(named_character(
        LR, "Hibou Khan", 155, (6, 5, 4, 4, 3, 5, 3, 10, "3+/4+"),
        ["Power Armour", "Iron Halo (Named Character)", "Breath of the Storm", "Bolt Pistol", "Frag Grenades"],
        ["The Seeker of Atonement", "Command Retinue (White Scars Khans)"],
        retinue=retinue_links("hibou", [khan_command_squad("hibou", h), veteran_retinue("hibou-vets", h)]),
        extra_groups=[take(h, "Wargear", [("Krak Grenades", 2)]), mobility_group(h), talisman_group("hibou")]))
    # Hasik Noyan-Khan (Traitor)
    k = uid("unit", "Hasik Noyan-Khan")
    out.append(named_character(
        LR, "Hasik Noyan-Khan", 175, (6, 5, 4, 4, 3, 5, 4, 10, "2+/4+"),
        ["Artificer Armour", "Iron Halo (Named Character)", "Power Weapon", "Bolt Pistol", "Frag Grenades"],
        ["Stubborn", "Lord of the Horde", "Command Retinue (White Scars Khans)"],
        retinue=retinue_links("hasik", [khan_command_squad("hasik", k), veteran_retinue("hasik-vets", k)]),
        extra_groups=[take(k, "Wargear", [("Krak Grenades", 2), ("Melta Bombs", 5)]), mobility_group(k),
                      talisman_group("hasik")],
        loyalist=False))
    return out


JAGHATAI = uid("unit", "Jaghatai Khan, the Warhawk")


def jaghatai():
    u = JAGHATAI
    hg = L2.honour_guard("jaghatai")
    jets = per_model("jaghatai-hg", "Jetbikes (entire squad, Sojutsu Voidbike)", 35, hg.get("id"), ["Jetbike"])
    no = [lacks(W("Sojutsu Pattern Voidbike"), u)]
    add_mods(jets, [modifier("set", "hidden", "true", conds=no),
                    modifier("set", uid(uid("squadwide", "jaghatai-hg", "Jetbikes (entire squad, Sojutsu Voidbike)"), "max"),
                             0, conds=no)])
    add_to(hg, "selectionEntries", [jets])
    ret = retinue_links("jaghatai", [hg, golden_keshig("jaghatai-gk", root=False)], title="Primarch Retinue")
    bike = option(u, "Sojutsu Pattern Voidbike", 40)
    e = primarch(LR, "Jaghatai Khan, the Warhawk", 490, (8, 6, 6, 6, 6, 9, 6, 10, "1+"),
                 ["Wildfire Panoply", "White Tiger Dao", "Storm's Voice", "Cyber-hawk", "Frag Grenades"],
                 ["Primarch Armour", "Master of the Hunt (Jaghatai)", "Lightning Strike", "Sire of the White Scars",
                  "Ride Beyond the Horizon", "Primarch Retinue (Jaghatai Khan)"],
                 retinue=ret, extra_entries=[bike], profile_name="Jaghatai Khan")
    prof = e.find("profiles")[0]
    prof.insert(0, wrap("modifiers", [modifier("set", gs.char_id("Unit", "Unit Type"), "Jetbike (Character)",
                                               conds=[has(W("Sojutsu Pattern Voidbike"), u)])]))
    return e


# ------------------------------------------------------------------ extend
def extend(ctx):
    ctx.legion_rules([LR, "Swift Advance", "Born in the Saddle", "Mounted Brotherhoods"])

    # Born in the Saddle / Mounted Brotherhoods
    bikes = ctx.unit("Legion Bike Squadron")
    bid = bikes.get("id")
    add_to(bikes, "infoLinks", rules_links(["Hit & Run", "Skilled Rider", "Mounted Brotherhoods"], key=bid + "ws"))
    # Mounted Brotherhoods: always Troops, may fill the compulsory Troops
    add_mods(bikes, [modifier("set-primary", "category", TROOPS), modifier("remove", "category", FA),
                     modifier("add", "category", gs.CAT_LINE)])
    sky = ctx.unit("Legion Sky Hunter Jetbike Squadron")
    add_to(sky, "infoLinks", rules_links(["Hit & Run", "Skilled Rider"], key=sky.get("id") + "ws"))
    ab = ctx.unit("Legion Attack Bike Squadron")
    add_to(ab, "infoLinks", rules_links(["Skilled Rider"], key=ab.get("id") + "ws"))

    # Stormseer Consul replaces the Librarian
    hide_consul(ctx, "Librarian")
    epi = uid("ws-stormseer", "epistolary")
    epi_disc = ["Divination", "Biomancy", "Telepathy", "Pyromancy"]
    epistolary = entry(epi, "Epistolary (Mastery Level 2)", cost=25,
                       constraints=[constraint(uid(epi, "max"), "max", 1, auto=True)],
                       infolinks=rules_links(["Epistolary (Stormseer)"], key=epi),
                       groups=[required_choice(epi, "Additional Psychic Power Discipline",
                                               [(d, []) for d in epi_disc])])
    # Unseen Bolt is always known; the Epistolary selects one more power from the Discipline picked above
    powers = psychic_powers(uid("ws-stormseer", "powers"), L.CENTURION, 0, epi_disc, fixed=["Unseen Bolt"],
                            more=[(1, has(epi, L.CENTURION))],
                            filters={d: [choice_id(epi, "Additional Psychic Power Discipline", d)] for d in epi_disc})
    cid = add_consul(ctx, "Stormseer", 35, ["Psyker", "Adamantium Will", "Legion Support Officer", "Stormseer"],
                     kit=["Force Weapon"], options=[epistolary], groups_=[powers], support_officer=True)
    consul_replaces_chainsword(ctx, cid)
    consul_unlocks_psyker_items(ctx, cid, ["Psychic Hood"])

    # new units
    ctx.add_units(golden_keshig(), ebon_keshig(), dark_sons(), falcons_claws(), *characters(), jaghatai())

    # Armoury: Power Glaive wherever a Character may choose a Power Weapon
    character_variant(ctx.all_entries(), "Power Weapon", "Power Glaive", 10)
    # Chogorian Warlance: models with the Armoury mounted on a Bike or Jetbike
    # (outside the Armoury points cap; Praetor/Centurion: in their White Scars Wargear group below)
    for n in ["Legion Bike Squadron", "Legion Sky Hunter Jetbike Squadron"]:
        warlance_beside_armoury(ctx.unit(n), "ws-" + n)
    for squad in ctx.retinues("Legion Command Squad") + ctx.retinues("Legion Veteran Squad"):
        sid = squad.get("id")
        mounts = [e.get("id") for e in squad.iter("selectionEntry")
                  if e.get("name") in ("Space Marine Bikes", "Space Marine Bikes (entire squad)",
                                       "Jetbikes (entire squad)")]
        if mounts:
            warlance_beside_armoury(squad, "ws-" + sid, hide=[all_of(*[lacks(m, sid) for m in mounts])])
    # Cyber-hawk (one Praetor) and Horsetail Talisman (one Independent Character)
    for n, uid_ in [("Legion Praetor", L.PRAETOR), ("Legion Centurion", L.CENTURION)]:
        e = ctx.unit(n)
        ents = []
        if n == "Legion Praetor":
            hid = uid("ws", "cyber-hawk")
            ents.append(entry(hid, "Cyber-hawk", cost=10, links=[gear(hid, "Cyber-hawk")],
                              constraints=[constraint(uid(hid, "max"), "max", 1, auto=True),
                                           constraint(uid(hid, "roster"), "max", 1, scope="roster", deep=True)]))
        lid = uid("ws", "warlance", n)
        ents.append(entry(lid, "Chogorian Warlance", cost=15, links=[gear(lid, "Chogorian Warlance")],
                          constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)],
                          mods=[modifier("set", "hidden", "true", conds=[lacks(W("Space Marine Bike"), uid_)]),
                                modifier("set", uid(lid, "max"), 0, conds=[lacks(W("Space Marine Bike"), uid_)])]))
        tid = uid("ws", "horsetail", n)
        ents.append(entry(tid, "Horsetail Talisman", cost=25, links=[gear(tid, "Horsetail Talisman")],
                          constraints=[constraint(uid(tid, "max"), "max", 1, auto=True)]))
        add_group(e, group(uid("grp", "ws-wargear", n), "White Scars Wargear", entries=ents))
    # only one Horsetail Talisman per army (shared item counted over the roster)
    legion = ctx.unit("Legion")
    add_mods(legion, [modifier("add", "error", "Only one Horsetail Talisman may be included in an army.",
                               conds=[cond(W("Horsetail Talisman"), "roster", "greaterThan", 1)])])

    # Chogorian Brotherhood: Praetor/Centurion on a Bike may upgrade to a Jetbike (as under Sky Hunter Phalanx)
    for key, n in [("praetor", "Legion Praetor"), ("centurion", "Legion Centurion")]:
        e = ctx.unit(n)
        jid = uid(key, "jetbike")
        for x in e.iter("selectionEntry"):
            if x.get("id") != jid:
                continue
            x.set("name", "Upgrade Bike to Jetbike (Sky Hunter Phalanx / Chogorian Brotherhood)")
            x.remove(x.find("modifiers"))
            no_rite = all_of(cond(rite_id("Sky Hunter Phalanx"), "force", "lessThan", 1),
                             cond(rite_id("Chogorian Brotherhood"), "force", "lessThan", 1))
            block(x, uid(jid, "max"), conds=[lacks(W("Space Marine Bike"), e.get("id"))], groups=[no_rite])

    # Rites of War
    ctx.add_rite("Chogorian Brotherhood", RULES["Chogorian Brotherhood"], limit_hs=True)
    ctx.add_rite("The Sagyar Mazan", RULES["The Sagyar Mazan"], errors=[
        ("only a Loyalist White Scars Detachment may use this Rite.", [cond(TRAITOR, "roster", "atLeast", 1)]),
        ("the Detachment may not include Jaghatai Khan.", [cond(JAGHATAI, "roster", "atLeast", 1)]),
        ("the army may not include a Fortification.", [cond(gs.cat("Fortification"), "roster", "atLeast", 1)]),
    ])
