"""VI Legion - Space Wolves (Forces of the Legions)."""
from legions.common import *  # noqa: F401,F403
from legions.common import (unique, force_limit, allegiance_only, upgrade, retinue_links, command_squad_for,
                            named_character, primarch, primarch_retinue, required_choice, add_consul, forbid_items,
                            add_armoury_items, min_points_error, add_group, add_entry, LOW, TRAITOR, LOYALIST)
from bsx import PTS, uid, el, wrap, cond, any_of, all_of, modifier, repeat, constraint, rule, entry, link, group
import gamesystem as gs
import legiones as L
import legiones2 as L2
from legiones import W, has, lacks, gear, per_model, rules_links, unit_profile, has_tda, no_tda
from legiones2 import (slot, take, pool, transports, add_mods, add_to, foc, rite_id, rite, walker_profile, TROOPS,
                       ELITES, FA, HQ, HS, model_swaps, model_takes, pa_armoury, tda_armoury, specials_decrement)
from legiones_wargear import ARMY_RULES, WEAPON_PROFILES, WEAPONS, WEAPON_RULES, WARGEAR

LEGION = "VI - Space Wolves"
LR = "Legiones Astartes (Space Wolves)"

RULES = {
    LR: ("Models with this rule belong to the VI Legion and use the Space Wolves Legion special rules: Hunters of "
         "Fenris, No Matter the Odds, Blood Feud and the Space Wolves Legion Organisation."),
    "Hunters of Fenris": ("All non-vehicle units with the Legiones Astartes (Space Wolves) special rule gain the "
                          "Counter-Attack and Acute Senses special rules."),
    "No Matter the Odds": ("Space Wolves units ignore negative Leadership modifiers applied to Break Tests caused by "
                           "losing close combat. Other Leadership modifiers apply normally."),
    "Blood Feud": (
        "Space Wolves models always hit Dark Angels and Thousand Sons models on a 3+ in close combat unless they would "
        "normally hit on a better result. Dark Angels and Thousand Sons models likewise always hit Space Wolves models on "
        "a 3+ in close combat unless they would normally hit on a better result."),
    "Legion Organisation (Space Wolves)": (
        "A Space Wolves Detachment must include one HQ selection for every full or partial 750 points in the army: up to "
        "750 points 1 HQ; 751-1,500 points 2 HQ; 1,501-2,250 points 3 HQ; 2,251-3,000 points 4 HQ. This replaces the "
        "normal minimum and maximum number of HQ selections. The normal restriction on models with Master of the Legion "
        "still applies. Space Wolves may not select Legion Chaplain Consuls or Legion Librarian Consuls; their roles are "
        "instead fulfilled by Wolf Priests and Rune Priests."),
    # Armoury
    "Frost Weapon": (
        "Any Space Wolves Character with access to the Space Marine Armoury may purchase a Frost Weapon for +20 points. A "
        "model already equipped with a Power Weapon may exchange it for a Frost Weapon for +5 points. A model may take a "
        "Frost Weapon or a Power Weapon, not both. May be represented "
        "by a sword, axe, claw or similar Fenrisian weapon; its appearance has no rules effect."),
    "Great Frost Blade": (
        "A Space Wolves Independent Character with access to the Space Marine Armoury may purchase a Great Frost Blade for "
        "+35 points. A model using a Great Frost Blade suffers -1 Initiative during that Assault phase."),
    "Wolf Pelt": ("Any Space Wolves Character may purchase a Wolf Pelt for +5 points. When the bearer's unit successfully "
                  "uses the Counter-Attack special rule, the bearer receives +2 Attacks instead of the normal +1 Attack "
                  "granted by Counter-Attack. This bonus applies only to the bearer."),
    "Wolf Tooth Necklace": ("Any Space Wolves Character may purchase a Wolf Tooth Necklace for +10 points. The bearer "
                            "always hits enemy models on a 3+ in close combat, regardless of comparative Weapon Skill. No "
                            "effect if the bearer would normally hit on a better result."),
    "Wolf Tail Talisman": (
        "Any Space Wolves Character may purchase a Wolf Tail Talisman for +5 points. Whenever an enemy psychic power "
        "directly affects the bearer or a unit he has joined, roll a D6 after the power has been successfully invoked and "
        "any normal attempt to Deny the Witch has been resolved. On a 6 the bearer is unaffected by that psychic power; "
        "the remainder of his unit is affected normally."),
    "Runic Armour": (
        "A Space Wolves Independent Character wearing Power Armour may replace it with Runic Armour for +25 points. Runic "
        "Armour grants a 2+ Armour Save and the Adamantium Will special rule. It counts as Artificer Armour for all other "
        "rules and restrictions. A model wearing Runic Armour may carry a Wolf Tail Talisman normally."),
    # Consuls
    "Wolf Priest": (
        "A Space Wolves Legion Centurion may be upgraded to a Wolf Priest for +35 points (a Space Wolves army may not "
        "select a Legion Chaplain Consul). Replaces the Chainsword with a Fang of Morkai and gains a Rosarius. Special "
        "rules: Rites of Battle, Oath of the Slayer."),
    "Fang of Morkai": "The Fang of Morkai counts as a Power Weapon.",
    "Rites of Battle": "The Wolf Priest and any Space Wolves unit he has joined may re-roll failed Morale checks.",
    "Oath of the Slayer": (
        "Before deployment, nominate one enemy unit. The Wolf Priest and any Space Wolves unit he has joined may re-roll "
        "failed To Hit rolls in close combat against the nominated enemy unit. The oath lasts for the duration of the "
        "battle."),
    "Rune Priest": (
        "A Space Wolves Legion Centurion may be upgraded to a Rune Priest for +25 points (a Space Wolves army may not "
        "select a Legion Librarian Consul). Replaces the Chainsword with a Runic Force Weapon and gains a Wolf Tail "
        "Talisman. Psyker (Mastery Level 1), Legion Support Officer; knows Mystic Winds of Fenris. May purchase a Psychic "
        "Hood from the Space Marine Armoury as normal."),
    "Runic Force Weapon": "A Runic Force Weapon counts as a Force Weapon.",
    "Master of Runes": (
        "A Rune Priest may be upgraded to a Master of Runes for +25 points: Psychic Mastery Level 2, and he may select one "
        "additional psychic power from the disciplines normally available to a Legion Librarian."),
    "Mystic Winds of Fenris": (
        "Blessing - friendly Space Wolves unit within 6\". If the Psychic Test is passed, nominate the Rune Priest or one "
        "friendly Space Wolves unit with at least one model within 6\". Until the beginning of the next Space Wolves turn "
        "the nominated unit receives a 5+ Cover Save. If the unit already has a Cover Save, improve that save by 1, to a "
        "maximum of 4+."),
    # Rites of War
    "The Pale Hunters": (
        "EFFECTS - The Great Hunt: add +1 to Reserve rolls made for Space Wolves units in this Detachment. Hunters Without "
        "Peer: all non-vehicle Space Wolves units gain Hit & Run provided the unit contains no model wearing any form of "
        "Terminator Armour; a unit with Hit & Run from this Rite moves 2D6\" after successfully disengaging instead of "
        "3D6\". The Killing Blow: during an Assault phase in which a Space Wolves unit successfully charged, models in "
        "that unit gain one additional Attack (in addition to the normal +1 for charging; not for a Disordered Charge or a "
        "unit which would otherwise receive no charging bonus). Pack Hunters: when two or more friendly Space Wolves units "
        "are engaged with the same enemy unit, each participating Space Wolves unit adds +1 to its combat-resolution "
        "score (not cumulative regardless of how many Space Wolves units are involved).\n"
        "LIMITATIONS - The army may include no more than one Heavy Support choice. The army may not include Legion "
        "Artillery Tank Squadrons, Rapier Weapons Batteries, Drop Pods, Dreadnought Drop Pods or Dreadclaw Drop Pods. A "
        "model wearing any form of Terminator Armour does not gain Hit & Run from this Rite."),
    "The Bloodied Claws": (
        "EFFECTS - Break the Line: Space Wolves units add +1 to their combat-resolution score while at least half of the "
        "models in the unit are within the enemy deployment zone (not cumulative with itself). Howl of the Death Wolf: "
        "once per battle, at the beginning of a Space Wolves turn, the Warlord may unleash the Howl; until the end of that "
        "player turn Space Wolves units may re-roll their Advance roll (the re-rolled result must be accepted) and their "
        "normal charge distance is increased from 6\" to 7\". Unstoppable Violence: during an Assault phase in which a "
        "Space Wolves unit charges an enemy unit already engaged by another friendly Space Wolves unit, the charging unit "
        "gains Furious Charge for that Assault phase. Bloodied Claws: Grey Slayer Squads and Legion Assault Squads must "
        "declare a charge during the Assault phase if an enemy unit is within their legal charge distance (the Space "
        "Wolves player chooses which if several).\n"
        "LIMITATIONS - No Prey Left Unhunted: Grey Slayer Squads must fulfil compulsory Troops selections when using "
        "this Rite. No Path of Retreat: units in this Detachment may not "
        "voluntarily withdraw from close combat; if a Space Wolves unit wins a close combat and an enemy unit retreats, the "
        "Space Wolves must Pursue whenever able. The Breaking of the Line: the Detachment may not include Artillery units, "
        "units with Slow and Purposeful, Immobile units or Fortifications, and may not include an Allied Detachment "
        "belonging to another Space Marine Legion."),
    # Units
    "True Grit": (
        "A model with True Grit which is equipped with both a Bolter and a Close-combat weapon counts as fighting with two "
        "close-combat weapons and receives +1 Attack in close combat. However, that model does not receive the normal +1 "
        "Attack for charging."),
    "Pack Assault": (
        "If a Grey Slayer Pack charges an enemy unit which was already engaged with another friendly Space Wolves unit at "
        "the beginning of that Assault phase, every Grey Slayer gains +1 Attack during that Assault phase."),
    "Grey Stalker Transport": (
        "A pack of ten models or fewer may select a Rhino, Drop Pod or Dreadclaw Drop Pod. A Grey Stalker Pack embarked "
        "upon a Transport may only use Infiltrate if that Transport is itself permitted to deploy using Infiltrate."),
    "Behind Enemy Lines": (
        "Instead of deploying normally, the Wolf Scout Squad may begin the battle in Reserve, even in a mission which does "
        "not normally permit Reserves. When the squad becomes available, nominate any table edge and roll a D6: on a 1 the "
        "opposing player chooses the table edge from which the Wolf Scouts enter; on a 2-6 the Space Wolves player "
        "chooses. The squad enters play from the chosen edge using the normal rules for units arriving from Reserve. A "
        "Wolf Scout Squad entering play using Behind Enemy Lines may shoot normally, but may not charge during the same "
        "turn."),
    "Dreams of Death": (
        "If a Deathsworn model is slain during an Assault phase before it has made its close-combat attacks, do not remove "
        "it immediately. At Initiative 1 that model may make its normal close-combat attacks as though it were still "
        "alive, provided at least one other model from its Deathsworn Pack is still alive. After these attacks have been "
        "resolved, remove the slain model."),
    "Scouring Tempest": (
        "Once per battle, before the Jorlund Hunter Pack shoots, the controlling player may declare a Scouring Tempest. "
        "Until the end of that Shooting phase, models in the pack may re-roll failed To Wound rolls made with Hand Flamers "
        "and Flamers."),
    "Glory Seekers": (
        "At the beginning of each Assault phase, if the Varagyr are engaged with one or more enemy Independent Characters, "
        "nominate one such character. Any Varagyr able to direct attacks against that character must do so. Each Varagyr "
        "attacking the nominated character may re-roll one failed To Hit roll during that Assault phase."),
    "Chosen of the Jarl": (
        "A Space Wolves Praetor equipped with Terminator Armour may select one Varagyr Wolf Guard Terminator Pack instead "
        "of a Legion Terminator Command Squad. The Varagyr do not occupy a separate Force Organisation slot and the "
        "Praetor and Varagyr count as a single HQ selection."),
    "Pack Hunters (Fenrisian Wolves)": (
        "A Fenrisian Wolf Pack must declare a charge against an enemy unit whenever it is legally able to do so. If the "
        "pack wins a close combat and an enemy unit Retreats, the Fenrisian Wolf Pack must Pursue if legally permitted."),
    "Wolf Retinue": (
        "In addition to a normal Retinue, an Independent Character may take a Retinue of 2 Fenrisian Wolves for 24 points, "
        "in addition to any Retinue squad or alone. They may never leave his side."),
    # Characters
    "Command Retinue (Hvarl Red-Blade)": (
        "Hvarl may select either a Legion Terminator Command Squad or a Varagyr Wolf Guard Terminator Pack as his "
        "retinue. Hvarl and his retinue occupy a single HQ selection."),
    "The Red-Blade": ("A Two-Handed Power Weapon which adds +2 to Hvarl's Strength. When attacking with the Red-Blade, "
                      "Hvarl suffers -1 Initiative."),
    "The Headsman": (
        "At the beginning of each Assault phase, if Hvarl is engaged with one or more enemy Independent Characters, "
        "nominate one of them. Hvarl must direct all of his attacks against the nominated character if able to do so. "
        "Hvarl may re-roll failed To Wound rolls against enemy Independent Characters."),
    "The Fell-Hand": "Counts as a Master-crafted Lightning Claw which adds +1 to Geigor's Strength.",
    "Preferred Enemy (Independent Characters)": "This model has the Preferred Enemy special rule against Independent "
                                                "Characters.",
    "Old and Wise": (
        "If the mission requires a dice roll to determine which player takes the first turn, a Space Wolves army "
        "containing Bjorn may re-roll that roll once. The second result must be accepted."),
    "Hard to Kill": (
        "Whenever Bjorn suffers a Glancing or Penetrating Hit and a result is rolled on the Vehicle Damage table, the Space "
        "Wolves player may force the opponent to re-roll that Vehicle Damage roll. The second result must be accepted."),
    "Command Retinue (Ohthere Wyrdmake)": "Ohthere may select a Legion Command Squad as his retinue.",
    "Runic Staff": "Ohthere's Runic Staff counts as both a Force Weapon and a Psychic Hood.",
    "Living Lightning": (
        "A Witchfire psychic power used during the Shooting phase. If successfully invoked, resolve it using the Living "
        "Lightning profile (24\", S5, AP4, Assault D6)."),
    # Leman Russ
    "Armour Elavagar": (
        "Counts as Primarch Armour. Whenever an enemy psychic power directly affects Leman Russ, after the power has been "
        "successfully invoked and any normal attempt to Deny the Witch has been resolved, roll a D6: on a 5+ Leman Russ is "
        "unaffected by that psychic power. If Russ has joined a unit, the remainder of the unit is affected normally."),
    "Mjalnar, the Sword of Balenight": (
        "A Master-crafted Power Weapon. Attacks made with it are resolved at +1 Strength and have the Shred special rule."),
    "Axe of Helwinter": "A Power Weapon. Attacks made with it are resolved at +2 Strength and have Armourbane.",
    "Krakenmaw": ("A Two-Handed Power Weapon. Attacks made with it are resolved at +2 Strength and have the Shred and "
                  "Rending special rules."),
    "Rending Claws and Fangs": "Count as a single Close Combat Weapon with the Rending special rule.",
    "The Emperor's Executioner": (
        "Before deployment, nominate one enemy Primarch, Independent Character or Monstrous Creature as Russ' Prey. Leman "
        "Russ may re-roll To Hit and To Wound rolls of 1 when making attacks against his Prey."),
    "Preternatural Senses": (
        "Leman Russ has the Night Vision special rule. In addition, enemy units deploying using Infiltrate may never be "
        "deployed within 18\" of Leman Russ or a unit he has joined, regardless of line of sight."),
    "The Wolf King": (
        "Friendly Space Wolves units with at least one model within 12\" of Leman Russ may re-roll failed Break Tests. In "
        "addition, they may re-roll failed Leadership Tests made when using the Counter-Attack special rule. The second "
        "result must be accepted."),
    "Bring Me the Traitor": (
        "If Russ' nominated Prey is within 12\" of him at the beginning of the Space Wolves Movement phase, Leman Russ may "
        "immediately move D6\" towards that model before making his normal move. This is a bonus move and does not "
        "prevent Russ from moving, shooting or charging normally later in the turn. Russ must end this bonus move closer "
        "to his Prey than he began it."),
    "The Wolves of the Wolf King": (
        "Freki and Geri begin the battle as part of Leman Russ' unit and may never voluntarily leave him. They do not "
        "prevent Leman Russ from using his Independent Character rules or joining another friendly unit; whenever Russ "
        "joins or leaves a unit, Freki and Geri accompany him. If Russ selects a Primarch Retinue, Freki and Geri are also "
        "part of that unit. For Transport Capacity, Freki and Geri each count as two models."),
    "Freki the Fierce": ("During an Assault phase in which Freki charged, he gains +1 Attack in addition to the normal "
                         "bonus for charging."),
    "Geri the Cunning": (
        "During each Assault phase, when Geri directs his attacks against an enemy Independent Character or Monstrous "
        "Creature, he may re-roll one failed To Hit roll OR one failed To Wound roll. The second result must be "
        "accepted."),
    "Primarch Retinue (Leman Russ)": (
        "Leman Russ may select a Legion Honour Guard Squad or a Legion Terminator Command Squad as his Primarch Retinue. "
        "It does not occupy an additional Force Organisation selection and otherwise follows the normal Primarch Retinue "
        "rules. Freki and Geri accompany Leman Russ regardless of which Primarch Retinue is selected."),
    "Leman Russ Restrictions": ("Leman Russ may only be selected for a Loyalist Space Wolves army. He otherwise follows "
                                "all normal rules and restrictions for Primarchs."),
}

WEAPONS_ = {
    "Frost Weapon": ("-", "User +1", "-", "Power Weapon"),
    "Great Frost Blade": ("-", "User +2", "-", "Power Weapon, Two-Handed, Master-crafted, -1 Initiative"),
    "Fang of Morkai": ("-", "User", "-", "Power Weapon"),
    "Runic Force Weapon": ("-", "User", "-", "Power Weapon, Force"),
    "Runic Staff": ("-", "User", "-", "Power Weapon, Force (counts as Psychic Hood)"),
    "Living Lightning": ('24"', "5", "4", "Assault D6 (Witchfire psychic power)"),
    "The Red-Blade": ("-", "User +2", "-", "Power Weapon, Two-Handed, -1 Initiative"),
    "The Fell-Hand": ("-", "User +1", "-", "Lightning Claw, Master-crafted"),
    "Mjalnar, the Sword of Balenight": ("-", "User +1", "-", "Power Weapon, Master-crafted, Shred"),
    "Axe of Helwinter": ("-", "User +2", "-", "Power Weapon, Armourbane"),
    "Krakenmaw": ("-", "User +2", "-", "Power Weapon, Two-Handed, Shred, Rending"),
    "Scornspitter": ('12"', "4", "3", "Assault 3, Rending"),
    "Rending Claws and Fangs": ("-", "User", "-", "Close Combat Weapon, Rending"),
}
WEAPON_RULES_ = {
    "Frost Weapon": ["Frost Weapon"],
    "Great Frost Blade": ["Great Frost Blade", "Two-Handed", "Master-Crafted"],
    "Fang of Morkai": ["Fang of Morkai"],
    "Runic Force Weapon": ["Runic Force Weapon", "Force"],
    "Runic Staff": ["Runic Staff", "Force"],
    "Living Lightning": ["Living Lightning"],
    "The Red-Blade": ["The Red-Blade", "Two-Handed"],
    "The Fell-Hand": ["The Fell-Hand", "Master-Crafted"],
    "Mjalnar, the Sword of Balenight": ["Mjalnar, the Sword of Balenight", "Master-Crafted", "Shred"],
    "Axe of Helwinter": ["Axe of Helwinter", "Armourbane"],
    "Krakenmaw": ["Krakenmaw", "Two-Handed", "Shred", "Rending"],
    "Scornspitter": ["Rending"],
    "Rending Claws and Fangs": ["Rending Claws and Fangs", "Rending"],
}
WARGEAR_ = {
    "Wolf Pelt": RULES["Wolf Pelt"],
    "Wolf Tooth Necklace": RULES["Wolf Tooth Necklace"],
    "Wolf Tail Talisman": RULES["Wolf Tail Talisman"],
    "Runic Armour": (RULES["Runic Armour"], ["Adamantium Will"]),
    "Yimira Stasis Bombs": (
        "A Deathsworn Pack counts as being equipped with Defensive Grenades. In addition, when an enemy unit Retreats from "
        "a close combat involving a Deathsworn Pack, roll two dice for the D6 portion of its Retreat distance and use the "
        "lower result."),
    "Scout Armour (Wolf Scouts)": "Confers a 4+ Armour Save.",
    "Iron Halo (Named Character)": (
        "Grants a 4+ Invulnerable Save. Part of this named character's own wargear; not counted towards the army's normal "
        "limit of one Iron Halo."),
    "Armour Elavagar": (RULES["Armour Elavagar"], ["Primarch Armour"]),
}


def register():
    ARMY_RULES.update(RULES)
    register_data(weapons=WEAPONS_, weapon_rules=WEAPON_RULES_, wargear=WARGEAR_)
    # the Grey Slayer / Varagyr "Frost Blade or Frost Axe" is a Frost Weapon
    WEAPONS["Frost Blade or Frost Axe"] = ["Frost Weapon"]
    WEAPON_RULES["Frost Blade or Frost Axe"] = ["Frost Weapon"]
    # Bjorn's close-combat arm
    WEAPONS["Dreadnought Close Combat Weapon with built-in Heavy Flamer"] = ["Dreadnought Close Combat Weapon",
                                                                              "Heavy Flamer"]


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


def pts_above(n):
    return cond("any", "roster", "greaterThan", n, field=PTS, deep=False)


def pts_below(n):
    return cond("any", "roster", "lessThan", n, field=PTS, deep=False)


def hide_unless(eid, conds_hide):
    return [modifier("set", "hidden", "true", groups=[any_of(*conds_hide)]),
            modifier("set", uid(eid, "max"), 0, groups=[any_of(*conds_hide)])]


def model(u, name, cost, mn, mx, utype, stats, kit, groups=(), mods=(), rules_=(), auto=False):
    mid = uid("model", u, name)
    return mid, entry(mid, name, typ="model", cost=cost, mods=list(mods),
                      constraints=[constraint(uid(mid, "min"), "min", mn, auto=auto),
                                   constraint(uid(mid, "max"), "max", mx, auto=auto)],
                      profiles=[unit_profile(u, name, utype, *stats)], links=[gear(mid, k) for k in kit],
                      groups=list(groups), infolinks=rules_links(list(rules_), key=mid))


def add_links(grp, key, items, hide=None):
    """Add shared items [(name, pts)] to a group, each max 1; hide: conditions that hide and forbid them."""
    links = grp.find("entryLinks")
    if links is None:
        links = el("entryLinks")
        grp.append(links)
    for n, p in items:
        lid = uid("link", grp.get("id"), key, n)
        mods = hide_unless(lid, hide) if hide else []
        links.append(link(lid, W(n), n, cost=p or None, mods=mods,
                          constraints=[constraint(uid(lid, "max"), "max", 1, auto=True)]))


_EXCL_DONE = set()


def _exclusive_power_weapon(e):
    """Author: a model takes a Frost Weapon or a Power Weapon, never both. Shown as an error on the model (a
    max-0 modifier would also hide the Frost Weapon in single-choice groups whose default is the Power Weapon)."""
    if id(e) in _EXCL_DONE:
        return
    _EXCL_DONE.add(id(e))
    add_mods(e, [modifier("add", "error", f"{e.get('name')}: a model may take a Frost Weapon or a Power Weapon, "
                                          "not both.",
                          groups=[all_of(has(W("Power Weapon"), "self"), has(W("Frost Weapon"), "self"))])])


def frost_variants(roots):
    """Frost Weapon: wherever a Character model may choose a Power Weapon, it may choose a Frost Weapon instead
    (+5 where the Power Weapon is a free default/basic wargear, +20 otherwise). A Character with a fixed Power Weapon
    gets a 'Replace Power Weapon' choice (Frost Weapon +5). Author: a model picks a Frost Weapon or a Power Weapon,
    never both (an error on the model if it has both)."""
    base_id = W("Power Weapon")
    done = set()
    n = 0
    for r in roots:
        for e in list(r.iter("selectionEntry")):
            if not is_character(e) or id(e) in done:
                continue
            done.add(id(e))
            own = e.find("entryLinks")
            if own is not None:
                for lk in list(own):
                    if lk.get("targetId") == base_id:
                        own.remove(lk)
                        add_to(e, "selectionEntryGroups", [slot(uid(e.get("id"), "sw-frost"), "Replace Power Weapon",
                                                                "Power Weapon", [("Frost Weapon", 5)])])
                        n += 1
            for g in list(e.iter("selectionEntryGroup")):
                if id(g) in done or "Servo-automata" in (g.get("name") or ""):
                    continue
                done.add(id(g))
                links = g.find("entryLinks")
                if links is None or any(lk.get("targetId") == W("Frost Weapon") for lk in links):
                    continue
                for lk in list(links):
                    if lk.get("targetId") != base_id:
                        continue
                    cs = lk.find("costs")
                    cost = float(cs[0].get("value")) if cs is not None and len(cs) else 0
                    nid = uid(lk.get("id"), "variant", "Frost Weapon")
                    cons = [constraint(uid(nid, "max"), "max", 1, auto=True)]
                    new_l = link(nid, W("Frost Weapon"), "Frost Weapon", cost=5 if cost == 0 else 20, constraints=cons)
                    _exclusive_power_weapon(e)
                    if g.get("defaultSelectionEntryId") is not None:
                        new_l.set("sortIndex", str(int(lk.get("sortIndex") or 1) + 100))
                    links.append(new_l)
                    n += 1
    return n


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
            return
    raise KeyError("centurion chainsword slot")


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
            if cs is not None and len(cs) and all(c.get("childId") in psy for c in cs):
                cs.append(lacks(cid, L.CENTURION))


def wolf_retinue(key):
    """'An Independent Character may take a Retinue of 2 Wolves for 24 pts' (in addition to any retinue squad)."""
    eid = uid("sw-wolf-retinue", key)
    return entry(eid, "Wolf Retinue (2 Fenrisian Wolves)", cost=24,
                 constraints=[constraint(uid(eid, "max"), "max", 1, auto=True)],
                 profiles=[unit_profile(eid, "Fenrisian Wolf", "Cavalry", 4, 0, 4, 4, 1, 4, 2, 8, "6+")],
                 infolinks=rules_links(["Wolf Retinue", "Pack Hunters (Fenrisian Wolves)"], key=eid))


# ------------------------------------------------------------------ units
GREY_SLAYERS = uid("unit", "Grey Slayer Pack")
GREY_STALKERS = uid("unit", "Grey Stalker Pack")
WOLF_SCOUTS = uid("unit", "Wolf Scout Squad")
DEATHSWORN = uid("unit", "Deathsworn Pack")
JORLUND = uid("unit", "Jorlund Hunter Pack")
VARAGYR = uid("unit", "Varagyr Wolf Guard Terminators")
FENRISIAN = uid("unit", "Fenrisian Wolf Pack")
SPECIALS = [("Flamer", 5), ("Meltagun", 10), ("Plasma Gun", 15)]


def grey_slayers():
    u = GREY_SLAYERS
    gid, slayers = model(u, "Grey Slayer", 18, 4, 19, "Infantry", (4, 4, 4, 4, 1, 4, 1, 8, "3+"),
                         ["Power Armour", "Bolter", "Close Combat Weapon"])
    hid = uid("model", u, "Grey Slayer Huscarl")
    arm = pa_armoury(hid, u, 20, slots=["Bolter", "Close Combat Weapon"])
    # the Huscarl may also replace his Bolter with a Combat Shield (+3) like any other model of the pack
    add_links(find_group(arm, "Replace Bolter"), "sw", [("Combat Shield", 3)])
    _, huscarl = model(u, "Grey Slayer Huscarl", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 2, 9, "3+"),
                       ["Power Armour"], groups=[arm])
    ranged, _ = pool(u, "Special Weapons (1 per 5 models, replace Bolter)", u, SPECIALS, 0, every=5)
    melee, _ = pool(u, "Close-combat Weapons (1 per 5 models, replace Close-combat weapon)", u,
                    [("Power Weapon", 10), ("Frost Blade or Frost Axe", 15), ("Power Fist", 15)], 0, every=5)
    shields = model_swaps(u, "Grey Slayers: replace Bolter with Combat Shield (any number)", u, [gid],
                          [("Combat Shield", 3)], minus=[W(n) for n, _ in SPECIALS])
    return entry(u, "Grey Slayer Pack", typ="unit", cost=105 - 4 * 18,
                 cats=[foc(TROOPS, "Troops", u), category_link(gs.CAT_LINE, "Compulsory Troops Eligible", key=u)],
                 infolinks=rules_links([LR, "True Grit", "Pack Assault"], key=u),
                 entries=[huscarl, slayers,
                          per_model(u, "Frag Grenades (entire pack)", 1, u, ["Frag Grenades"]),
                          per_model(u, "Krak Grenades (entire pack)", 2, u, ["Krak Grenades"])],
                 groups=[shields, ranged, melee,
                         L.one_each(u, "Pack Equipment (each on a different model)",
                                    [("Legion Vexilla", 10), ("Nuncio Vox", 10)]),
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod", "Land Raider Phobos",
                                           "Land Raider Proteus"], max_models=10)])


def grey_stalkers():
    u = GREY_STALKERS
    _, stalkers = model(u, "Grey Stalker", 17, 4, 14, "Infantry", (4, 4, 4, 4, 1, 4, 1, 8, "3+"),
                        ["Power Armour", "Bolter", "Close Combat Weapon"])
    hid = uid("model", u, "Stalker Huscarl")
    _, huscarl = model(u, "Stalker Huscarl", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 2, 9, "3+"),
                       ["Power Armour"], groups=[pa_armoury(hid, u, 15, slots=["Bolter", "Close Combat Weapon"])])
    ranged, _ = pool(u, "Special Weapons (1 per 5 models, replace Bolter)", u,
                     SPECIALS + [("Volkite Charger", 10)], 0, every=5)
    return entry(u, "Grey Stalker Pack", typ="unit", cost=100 - 4 * 17,
                 cats=[foc(TROOPS, "Troops", u), category_link(gs.CAT_LINE, "Compulsory Troops Eligible", key=u)],
                 infolinks=rules_links([LR, "Infiltrate", "Move Through Cover", "Night Vision",
                                        "Grey Stalker Transport"], key=u),
                 entries=[huscarl, stalkers,
                          per_model(u, "Frag Grenades (entire pack)", 1, u, ["Frag Grenades"]),
                          per_model(u, "Krak Grenades (entire pack)", 2, u, ["Krak Grenades"])],
                 groups=[ranged,
                         L.one_each(u, "Pack Equipment (each on a different model)",
                                    [("Legion Vexilla", 10), ("Nuncio Vox", 10)]),
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod"], max_models=10)])


SCOUT_SWAPS = [("Bolter", 0), ("Astartes Shotgun", 0), ("Sniper Rifle", 5)]


def wolf_scouts():
    u = WOLF_SCOUTS
    kit = ["Scout Armour (Wolf Scouts)", "Bolt Pistol", "Close Combat Weapon"]
    sid, scouts = model(u, "Wolf Scout", 14, 4, 9, "Infantry", (4, 4, 4, 4, 1, 4, 1, 8, "4+"), kit)
    hid = uid("model", u, "Wolf Scout Huscarl")
    arm = pa_armoury(hid, u, 10, slots=["Bolt Pistol", "Close Combat Weapon"])
    # Huscarl: 'any model may replace his Bolt pistol and Close-combat weapon with ...'
    hus_swap = take(hid, "Replace Bolt Pistol and Close-combat weapon", SCOUT_SWAPS, max_total=1)
    swapped = [has(W(n), hid) for n, _ in SCOUT_SWAPS]
    for d in ("Bolt Pistol", "Close Combat Weapon"):
        g = find_group(arm, f"Replace {d}")
        gid = g.get("id")
        add_mods(g, [modifier("set", uid(gid, "min"), 0, groups=[any_of(*swapped)]),
                     modifier("set", uid(gid, "max"), 0, groups=[any_of(*swapped)]),
                     modifier("set", "hidden", "true", groups=[any_of(*swapped)])])
    _, huscarl = model(u, "Wolf Scout Huscarl", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 2, 9, "4+"),
                       ["Scout Armour (Wolf Scouts)"], groups=[hus_swap, arm])
    heavy = [("Heavy Bolter", 10), ("Missile Launcher", 15)]
    hgid = uid("grp", u, "sw-heavy")
    heavy_g = group(hgid, "Heavy Weapon (one Wolf Scout, instead of a special weapon; replaces Bolt Pistol)",
                    links=[link(uid("link", hgid, n), W(n), n, cost=p) for n, p in heavy],
                    constraints=[constraint(uid(hgid, "max"), "max", 1, auto=True)])
    took_heavy = [has(W(n), u) for n, _ in heavy]
    stitle = "Special Weapons (up to two Wolf Scouts, one each; replaces Bolt Pistol)"
    scout_specials = SPECIALS + [("Plasma Pistol", 15), ("Power Weapon", 10)]
    specials, smx = pool(u, stitle, u, scout_specials, 2,
                         extra_mods=[modifier("decrement", uid(uid("grp", u, stitle), "max"), 1,
                                              groups=[any_of(*took_heavy)])])
    return entry(u, "Wolf Scout Squad", typ="unit", cost=85 - 4 * 14, cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links([LR, "Infiltrate", "Move Through Cover", "Behind Enemy Lines"], key=u),
                 entries=[huscarl, scouts,
                          per_model(u, "Frag Grenades (entire squad)", 1, u, ["Frag Grenades"]),
                          per_model(u, "Krak Grenades (entire squad)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire squad)", 5, u, ["Melta Bombs"])],
                 groups=[model_swaps(u, "Wolf Scouts: replace Bolt Pistol and Close-combat weapon (any number)", u,
                                     [sid], SCOUT_SWAPS,
                                     minus=[W(n) for n, _ in scout_specials + heavy]),
                         specials, heavy_g,
                         transports(u, u, ["Legion Rhino Armoured Carrier"], orbital=False, spearhead=False)])


def deathsworn():
    u = DEATHSWORN
    _, ds = model(u, "Deathsworn", 30, 5, 10, "Infantry", (4, 4, 4, 4, 1, 4, 2, 9, "2+"),
                  ["Artificer Armour", "Bolt Pistol", "Power Weapon", "Yimira Stasis Bombs", "Frag Grenades"])
    melee, _ = pool(u, "Close-combat Weapons (1 per 5 models, replace Power Weapon)", u,
                    [("Power Fist", 5), ("Great Frost Blade", 10), ("Thunder Hammer", 10)], 0, every=5)
    return entry(u, "Deathsworn Pack", typ="unit", cost=175 - 5 * 30, cats=[foc(ELITES, "Elites", u)],
                 infolinks=rules_links([LR, "Dreams of Death"], key=u),
                 entries=[ds, per_model(u, "Krak Grenades (entire pack)", 2, u, ["Krak Grenades"]),
                          per_model(u, "Melta Bombs (entire pack)", 5, u, ["Melta Bombs"])],
                 groups=[melee, transports(u, u, ["Legion Rhino Armoured Carrier", "Anvillus Pattern Dreadclaw Drop Pod",
                                                  "Land Raider Phobos", "Land Raider Proteus"])])


def jorlund():
    u = JORLUND
    _, hunters = model(u, "Jorlund Hunter", 18, 4, 9, "Infantry", (4, 4, 4, 4, 1, 4, 2, 8, "3+"),
                       ["Power Armour", "Hand Flamer", "Chainsword", "Frag Grenades"])
    hid = uid("model", u, "Hunt-master")
    _, master = model(u, "Hunt-master", 0, 1, 1, "Infantry (Character)", (4, 4, 4, 4, 1, 4, 3, 9, "3+"),
                      ["Power Armour", "Frag Grenades"],
                      groups=[pa_armoury(hid, u, 10, slots=["Hand Flamer", "Chainsword"])])
    flamers, _ = pool(u, "Pack Weapons (1 per 5 models, replace Hand Flamer)", u,
                      [("Flamer", 5), ("Volkite Serpenta", 5)], 0, every=5)
    return entry(u, "Jorlund Hunter Pack", typ="unit", cost=100 - 4 * 18, cats=[foc(TROOPS, "Troops", u)],
                 infolinks=rules_links([LR, "Scouring Tempest"], key=u),
                 entries=[master, hunters, per_model(u, "Krak Grenades (entire pack)", 2, u, ["Krak Grenades"])],
                 groups=[flamers, L.one_each(u, "Pack Equipment", [("Legion Vexilla", 10)]),
                         transports(u, u, ["Legion Rhino Armoured Carrier", "Legion Drop Pod",
                                           "Anvillus Pattern Dreadclaw Drop Pod"])])


VAR_RANGED = [("Foeblaster Boltgun", 5), ("Combi-Flamer", 10), ("Combi-Volkite Charger", 10), ("Combi-Meltagun", 15),
              ("Combi-Plasma Gun", 15)]
VAR_CC = [("Power Fist", 5), ("Chainfist", 10), ("Thunder Hammer", 10)]
VAR_HEAVY = [("Heavy Flamer", 10), ("Reaper Autocannon", 15), ("Assault Cannon", 20)]


def varagyr(key="Varagyr Wolf Guard Terminators", root=True):
    u = uid("unit", key)
    kit = ["Cataphractii Terminator Armour"]
    vkit = kit + ["Combi-Bolter", "Frost Blade or Frost Axe"]
    vid = uid("model", u, "Varagyr Terminator")
    tid = uid("model", u, "Varagyr Thegn")
    vmin, vmax = uid(vid, "min"), uid(vid, "max")
    _, terms = model(u, "Varagyr Terminator", 45, 5, 10, "Infantry", (5, 4, 4, 4, 1, 4, 2, 9, "2+/4+"), vkit,
                     mods=specials_decrement(vid, vmin, vmax, [tid], u), auto=True)
    thegn = entry(tid, "Varagyr Thegn (upgrade one Varagyr)", typ="model", cost=45 + 25,
                  constraints=[constraint(uid(tid, "max"), "max", 1)],
                  profiles=[unit_profile(u, "Varagyr Thegn", "Infantry (Character)", 5, 4, 4, 4, 2, 4, 3, 9, "2+/4+")],
                  links=[gear(tid, k) for k in kit],
                  groups=[slot(tid, "Replace Combi-bolter", "Combi-Bolter", VAR_RANGED),
                          slot(tid, "Replace Frost Blade or Frost Axe", "Frost Blade or Frost Axe", VAR_CC),
                          take(tid, "Thegn Wargear", [("Grenade Harness", 10)]),
                          tda_armoury(tid)])
    heavy, _ = pool(key, "Heavy Weapons (1 per 5 models, replace Combi-bolter)", u, VAR_HEAVY, 0, every=5)
    swaps = [model_swaps(key, "Varagyr: replace Combi-bolter (any number)", u, [vid], VAR_RANGED,
                         minus=[W(n) for n, _ in VAR_HEAVY]),
             model_swaps(key, "Varagyr: replace Frost Blade or Frost Axe (any number)", u, [vid], VAR_CC)]
    return entry(u, "Varagyr Wolf Guard Terminators", typ="unit", cost=250 - 5 * 45,
                 cats=[foc(ELITES, "Elites", u)] if root else [],
                 infolinks=rules_links([LR, "Fearless", "Glory Seekers", "Chosen of the Jarl"] +
                                       ([] if root else ["Retinue"]), key=u),
                 entries=[thegn, terms],
                 groups=[*swaps, heavy,
                         transports(key, u, ["Land Raider Phobos", "Land Raider Proteus",
                                             "Anvillus Pattern Dreadclaw Drop Pod", "Legion Spartan Assault Tank"],
                                    orbital=False)])


def fenrisian_wolves():
    u = FENRISIAN
    _, wolves = model(u, "Fenrisian Wolf", 12, 5, 10, "Cavalry", (4, 0, 4, 4, 1, 4, 2, 8, "6+"), [])
    return entry(u, "Fenrisian Wolf Pack", typ="unit", cost=60 - 5 * 12, cats=[foc(FA, "Fast Attack", u)],
                 infolinks=rules_links(["Pack Hunters (Fenrisian Wolves)"], key=u), entries=[wolves])


# ------------------------------------------------------------------ characters
HVARL = uid("unit", "Hvarl Red-Blade")
GEIGOR = uid("unit", "Geigor Fell-Hand")
BJORN = uid("unit", "Bjorn the Fell-Handed")
OHTHERE = uid("unit", "Ohthere Wyrdmake")
RUSS = uid("unit", "Leman Russ, the Wolf King")


WOLF_ITEMS = [("Wolf Pelt", 5), ("Wolf Tooth Necklace", 10), ("Wolf Tail Talisman", 5)]


def characters():
    out = []
    out.append(named_character(
        LR, "Hvarl Red-Blade", 195, (6, 5, 4, 4, 3, 5, 4, 10, "2+/4+"),
        ["Terminator Armour", "Iron Halo (Named Character)", "Heavy Bolter", "The Red-Blade"],
        ["The Headsman", "Command Retinue (Hvarl Red-Blade)"], min_points=1500,
        extra_groups=[take(HVARL, "Space Wolves Wargear", WOLF_ITEMS)],
        retinue=retinue_links("hvarl", [L2.terminator_command_squad("hvarl"), varagyr("hvarl-varagyr", root=False)]),
        extra_entries=[wolf_retinue("hvarl")]))
    out.append(named_character(
        LR, "Geigor Fell-Hand", 145, (6, 5, 4, 4, 3, 5, 3, 9, "2+/5+"),
        ["Artificer Armour", "Refractor Field", "Bolter", "Bolt Pistol", "The Fell-Hand", "Frag Grenades"],
        ["Preferred Enemy (Independent Characters)", "Preferred Enemy"], master=False,
        extra_groups=[take(GEIGOR, "Wargear", [("Krak Grenades", 2)] + WOLF_ITEMS)], extra_entries=[wolf_retinue("geigor")]))
    out.append(named_character(
        LR, "Ohthere Wyrdmake", 150, (5, 5, 4, 4, 3, 5, 3, 10, "2+"),
        ["Runic Armour", "Bolt Pistol", "Runic Staff", "Frag Grenades"],
        ["Psyker", "Legion Support Officer", "Command Retinue (Ohthere Wyrdmake)"], master=False, compulsory=False,
        retinue=retinue_links("ohthere", [command_squad_for("ohthere", OHTHERE)]),
        extra_groups=[take(OHTHERE, "Wargear", [("Krak Grenades", 2)] + WOLF_ITEMS),
                      psychic_powers(OHTHERE, OHTHERE, fixed=["Mystic Winds of Fenris", "Living Lightning"])],
        extra_entries=[wolf_retinue("ohthere")]))
    # Bjorn the Fell-Handed - a Dreadnought HQ
    u = BJORN
    out.append(entry(u, "Bjorn the Fell-Handed", typ="unit", cost=190,
                     cats=[foc(HQ, "HQ", u), category_link(gs.CAT_COMMANDER, "Compulsory HQ Eligible", key=u)],
                     constraints=[unique(u)],
                     profiles=[walker_profile(u, "Bjorn the Fell-Handed", 5, 5, 6, 12, 12, 10, 4, 3)],
                     infolinks=rules_links(["Old and Wise", "Hard to Kill", LR], key=u),
                     groups=[group(uid("grp", u, "transport"), "Dedicated Transport",
                                   links=[link(uid("link", uid("grp", u, "transport"), "dp"),
                                               L2.T["Legion Dreadnought Drop Pod"], "Legion Dreadnought Drop Pod")],
                                   constraints=[constraint(uid("grp", u, "transport", "max"), "max", 1, auto=True)])],
                     links=[gear(u, k) for k in ["Assault Cannon",
                                                 "Dreadnought Close Combat Weapon with built-in Heavy Flamer",
                                                 "Smoke Launchers", "Searchlight"]]))
    return out


def leman_russ():
    u = RUSS
    beasts = []
    for name, rl in [("Freki", "Freki the Fierce"), ("Geri", "Geri the Cunning")]:
        mid = uid("model", u, name)
        beasts.append(entry(mid, name, typ="model",
                            constraints=[constraint(uid(mid, "min"), "min", 1), constraint(uid(mid, "max"), "max", 1)],
                            profiles=[unit_profile(u, name, "Cavalry", 5, 0, 5, 5, 2, 5, 3, 10, "5+")],
                            links=[gear(mid, "Rending Claws and Fangs")],
                            infolinks=rules_links(["Fearless", "The Wolves of the Wolf King", rl], key=mid)))
    weapon = slot(u, "Weapon (choose one)", "Mjalnar, the Sword of Balenight",
                  [("Axe of Helwinter", 0), ("Krakenmaw", 0)])
    return primarch(LR, "Leman Russ, the Wolf King", 510, (8, 6, 6, 6, 6, 7, 6, 10, "1+"),
                    ["Armour Elavagar", "Scornspitter", "Frag Grenades"],
                    ["Primarch Armour", "The Emperor's Executioner", "Preternatural Senses", "Night Vision",
                     "The Wolf King", "Bring Me the Traitor", "Primarch Retinue (Leman Russ)", "Leman Russ Restrictions"],
                    retinue=primarch_retinue("russ"), loyalist=True, extra_groups=[weapon], extra_entries=beasts,
                    profile_name="Leman Russ")


# ------------------------------------------------------------------ Legion-wide changes
def legion_organisation(ctx):
    """One HQ per full or partial 750 points (replaces the normal 1-2 HQ). The book's table stops at 3,000 points;
    the rule ('every full or partial 750 points') is continued up to 4,500 points."""
    legion = ctx.unit("Legion")
    alleg = ctx.unit("Allegiance")
    plus = gs.FOC_PLUS["HQ"]
    # the standard chart allows 2 HQ; every selection carrying the '+1 HQ' category raises it by one. A category only
    # counts once per selection, so each step is put on a different configuration selection.
    add_mods(legion, [modifier("add", "category", plus, conds=[pts_above(1500)])])
    add_mods(alleg, [modifier("add", "category", plus, conds=[pts_above(2250)])])
    for e in legion.iter("selectionEntry"):
        if e.get("id") == ctx.legion_id:
            add_mods(e, [modifier("add", "category", plus, conds=[pts_above(3000)])])
    for e in alleg.iter("selectionEntry"):
        if e.get("id") in (L.LOYALIST, L.TRAITOR):
            add_mods(e, [modifier("add", "category", plus, conds=[pts_above(3750)])])
    mods = []
    for n in range(1, 7):
        lo, hi = 750 * (n - 1), 750 * n
        txt = (f"Space Wolves Legion Organisation: an army of {lo + 1:,}-{hi:,} points must include exactly {n} HQ "
               f"selection{'s' if n > 1 else ''}.")
        if n > 1:
            mods.append(modifier("add", "error", txt, conds=[pts_above(lo), pts_below(hi + 1),
                                                              cond(HQ, "force", "lessThan", n)]))
        mods.append(modifier("add", "error", txt, conds=[pts_above(lo), pts_below(hi + 1),
                                                          cond(HQ, "force", "greaterThan", n)]))
    mods.append(modifier("add", "error", "Space Wolves Legion Organisation: armies of more than 4,500 points need one "
                                         "HQ selection per full or partial 750 points - check the HQ count by hand.",
                         conds=[pts_above(4500)]))
    add_mods(legion, mods)


def armoury(ctx):
    # Wolf Pelt, Wolf Tooth Necklace, Wolf Tail Talisman: any Space Wolves Character with the Armoury
    add_armoury_items(ctx, [("Wolf Pelt", 5), ("Wolf Tooth Necklace", 10), ("Wolf Tail Talisman", 5)])
    for n, u in [("Legion Praetor", L.PRAETOR), ("Legion Centurion", L.CENTURION)]:
        e = ctx.unit(n)
        arm = find_group(e, "Space Marine Armoury (max 100 pts)")
        # Great Frost Blade: Independent Characters only
        for s in ("Replace Bolt Pistol", "Replace Chainsword"):
            add_links(find_group(arm, s), "sw", [("Great Frost Blade", 35)])
        # Runic Armour replaces Power Armour (counts as Artificer Armour)
        armour = None
        for g in e.find("selectionEntryGroups"):
            if g.get("name") == "Armour":
                armour = g
        hide = [has(L.consul_id(c), u) for c in ("Forge Lord", "Primus Nullificator")] if n == "Legion Centurion" \
            else None
        add_links(armour, "sw", [("Runic Armour", 25)], hide=hide)
        add_entry(e, wolf_retinue(n))


def consuls(ctx):
    hide_consul(ctx, "Chaplain")
    hide_consul(ctx, "Librarian")
    cen = ctx.unit("Legion Centurion")
    wp = add_consul(ctx, "Wolf Priest", 35, ["Wolf Priest", "Rites of Battle", "Oath of the Slayer"],
                    kit=["Fang of Morkai", "Rosarius"])
    consul_replaces_chainsword(ctx, wp)
    # a Rosarius does not combine with other invulnerable saves
    forbid_items(cen, ["Refractor Field", "Iron Halo"], [has(wp, L.CENTURION)])
    mor = uid("sw-rune-priest", "master-of-runes")
    lib = PSY.LIBRARIAN
    master = entry(mor, "Master of Runes (Mastery Level 2)", cost=25,
                   constraints=[constraint(uid(mor, "max"), "max", 1, auto=True)],
                   infolinks=rules_links(["Master of Runes"], key=mor))
    # Mystic Winds of Fenris is always known; a Master of Runes selects one more power directly from the allowed
    # Disciplines (offered only while the Master of Runes upgrade is taken)
    powers = psychic_powers(uid("sw-rune-priest", "powers"), L.CENTURION, 0, lib, fixed=["Mystic Winds of Fenris"],
                            more=[(1, has(mor, L.CENTURION))],
                            filters={d: [mor] for d in lib})
    rp = add_consul(ctx, "Rune Priest", 25, ["Psyker", "Legion Support Officer", "Rune Priest"],
                    kit=["Runic Force Weapon", "Wolf Tail Talisman"], options=[master], groups_=[powers],
                    support_officer=True)
    consul_replaces_chainsword(ctx, rp)
    consul_unlocks_psyker_items(ctx, rp, ["Psychic Hood"])
    # he already carries a Wolf Tail Talisman: hide the Armoury one
    for g in cen.iter("selectionEntryGroup"):
        if g.get("name") == "Additional Wargear":
            for lk in g.findall("entryLinks/entryLink"):
                if lk.get("targetId") == W("Wolf Tail Talisman"):
                    add_mods(lk, hide_unless(lk.get("id"), [has(rp, L.CENTURION)]))


def praetor_varagyr(ctx):
    """Chosen of the Jarl: a Praetor in Terminator Armour may take a Varagyr pack instead of a Terminator Command
    Squad."""
    praetor = ctx.unit("Legion Praetor")
    ret = find_group(praetor, "Retinue (no Force Organisation slot)")
    v = varagyr("praetor-varagyr", root=False)
    ctx.add_shared(v)
    lid = uid("link", ret.get("id"), v.get("id"))
    add_to(ret, "entryLinks", [link(lid, v.get("id"), v.get("name") + " (Chosen of the Jarl)",
                                    mods=[modifier("set", "hidden", "true", groups=[no_tda(L.PRAETOR)])])])
    add_mods(praetor, [modifier("add", "error", "Chosen of the Jarl: only a Praetor equipped with Terminator Armour may "
                                                "select a Varagyr Wolf Guard Terminator Pack.",
                                groups=[all_of(cond(v.get("id"), L.PRAETOR, "atLeast", 1),
                                               *[lacks(W(t), L.PRAETOR) for t in L.TDA])])])


def rites(ctx):
    T = L2.T
    art = ctx.unit("0-1 Legion Artillery Tank Squadron").get("id")
    rapier = ctx.unit("Legion Rapier Weapons Battery").get("id")
    pods = [("Drop Pods", T["Legion Drop Pod"]), ("Dreadnought Drop Pods", T["Legion Dreadnought Drop Pod"]),
            ("Dreadclaw Drop Pods", T["Anvillus Pattern Dreadclaw Drop Pod"])]
    ctx.add_rite("The Pale Hunters", RULES["The Pale Hunters"], limit_hs=True, errors=[
        ("the army may not include Legion Artillery Tank Squadrons.", [cond(art, "force", "atLeast", 1)]),
        ("the army may not include Rapier Weapons Batteries.", [cond(rapier, "force", "atLeast", 1)]),
    ] + [(f"the army may not include {n}.", [cond(i, "force", "atLeast", 1)]) for n, i in pods])
    bc = ctx.add_rite("The Bloodied Claws", RULES["The Bloodied Claws"], errors=[
        ("Grey Slayer Packs must fulfil the compulsory Troops selections (at least two Grey Slayer Packs).",
         [cond(GREY_SLAYERS, "force", "lessThan", 2)]),
        ("the Detachment may not include Artillery units (Rapier Weapons Batteries).",
         [cond(rapier, "force", "atLeast", 1)]),
        ("the Detachment may not include Fortifications.", [cond(gs.cat("Fortification"), "force", "atLeast", 1)]),
    ])
    # The Breaking of the Line: no units with the Immobile or Slow and Purposeful special rules
    bad = {L.rule_ref("Immobile")[0], L.rule_ref("Slow and Purposeful")[0]}
    done = set()
    for r_ in ctx.all_entries():
        for e in r_.iter("selectionEntry"):
            if e.get("type") != "unit" or e.get("id") in done:
                continue
            il = e.find("infoLinks")
            if il is not None and any(x.get("targetId") in bad for x in il):
                done.add(e.get("id"))
                add_mods(e, [modifier("add", "error", "The Bloodied Claws: the Detachment may not include Immobile "
                                                      "units or units with the Slow and Purposeful special rule.",
                                      conds=[cond(bc, "force", "atLeast", 1)])])


# ------------------------------------------------------------------ extend
def extend(ctx):
    ctx.legion_rules([LR, "Hunters of Fenris", "Counter-Attack", "Acute Senses", "No Matter the Odds", "Blood Feud",
                      "Legion Organisation (Space Wolves)"])
    legion_organisation(ctx)

    ctx.add_units(grey_slayers(), grey_stalkers(), jorlund(), wolf_scouts(), deathsworn(), varagyr(),
                  fenrisian_wolves(), *characters(), leman_russ())
    praetor_varagyr(ctx)
    ctx.finish()  # new retinues become shared entries before the Legion-wide changes below

    armoury(ctx)
    consuls(ctx)
    frost_variants(ctx.all_entries())
    rites(ctx)
