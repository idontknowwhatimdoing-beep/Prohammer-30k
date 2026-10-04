"""Psychic powers and disciplines (ProHammer Classic core rules + Forces of the Legions).

One place for every power a psyker can select or knows. Used by legiones.psychic_powers(), which gives a psyker a
"Psychic Powers" selection group whose entries carry these rule texts (and weapon profiles for shooting powers).

Sources: core.txt "PSYCHIC DISCIPLINES" (line ~2374) and "POWER TYPES" (line ~2294); Legion powers from
legions_v4/<Legion>.txt (line numbers in the comments).

POWERS: {power name: dict(discipline=..., type=..., text=..., profile=(range, S, AP, type) or None)}
  discipline: a core discipline name, or None for a Legion-specific power (known by a named psyker / unit).
  type:       the power type rule linked from the power (key of POWER_TYPES).
"""

DISCIPLINES = ["Biomancy", "Divination", "Pyromancy", "Telekinesis", "Telepathy",
               "Daemonology (Sanctic)", "Daemonology (Malefic)"]
# "The Librarian selects psychic powers from the Psychic Power list except any form of Daemonology."
LIBRARIAN = ["Biomancy", "Divination", "Pyromancy", "Telekinesis", "Telepathy"]
# Thousand Sons: Sorcerers of Prospero
THOUSAND_SONS = ["Biomancy", "Divination", "Pyromancy", "Telekinesis", "Telepathy"]

# core.txt "POWER TYPES" (lines 2294-2372), summarised faithfully
POWER_TYPES = {
    "Blessing": (
        "Blessings target a friendly unit and confer some benefit. Invoked at any time during the psyker's Movement phase "
        "unless otherwise noted. Duration: until the start of the psyker's own next turn. Blessings with the same effects "
        "stack if they are differently named powers; exact copies (same name) cannot be stacked on the same unit. "
        "Characteristics cannot be modified above 10 or below 1. If a psyker with an active blessing is removed from "
        "play, its blessings are immediately cancelled."),
    "Malediction": (
        "Maledictions weaken and hinder opposing units. Invoked during the psyker's Movement phase unless otherwise noted. "
        "Duration: until the start of the psyker's own next turn. Maledictions with the same effects stack if they are "
        "differently named powers; exact copies (same name) cannot be stacked on the same unit. Characteristics cannot be "
        "modified above 10 or below 1. If a psyker with an active malediction is removed from play, its maledictions are "
        "immediately cancelled."),
    "Conjuration": (
        "Conjurations summon outside forces onto the battlefield. Invoked at the start of the psyker's Movement phase "
        "unless otherwise noted. A unit using a conjuration may not perform any other actions that turn (no movement, "
        "shooting, other psychic powers, charging, etc.). Any doubles rolled on the psychic test inflict Perils of the "
        "Warp, whether or not the conjuration succeeded. Can only summon daemons matching the psyker's Chaos mark; a psyker without a Chaos mark (e.g. a Legiones "
        "Astartes Esoterist or Zardu Layak) may summon any of the daemons listed in the power. Summoned units are not "
        "bought or recorded in the roster. Each "
        "psyker may only successfully cast a selected conjuration once per game. Summoned psykers may not select "
        "conjuration powers. Summoned units arrive following the Deep Strike rules; the centre model must be placed "
        "within the power's range."),
    "Witchfire": (
        "Witchfire powers are ranged attacks and count as a shooting attack for the model (it may not make other ranged "
        "attacks unless normally allowed more than one). Invoked during the psyker's Shooting phase. Treated as Assault "
        "weapons unless otherwise specified. After invoking the power the psyker must still roll To Hit, with line of "
        "sight and range as normal; a witchfire power with no weapon/attack profile does not roll To Hit unless otherwise "
        "specified. A psyker may only invoke one witchfire power per turn, unless the model may shoot more than one "
        "weapon AND knows two or more different witchfire powers. Psychic powers which count as a shooting attack are "
        "witchfire powers."),
    "Witchfire - Beam": (
        "A witchfire power (see Witchfire). Draw a line between the psyker and a chosen point within the power's range "
        "(the power may or may not require line of sight to that point). Each unit with a model in the path of the beam "
        "takes a number of hits equal to the number of its models under the path. Unsaved wounds may be given to any "
        "models in the unit with the same saving throw."),
    "Witchfire - Focused": (
        "A witchfire power (see Witchfire) that attacks a specific model in the target unit. If the psychic test roll "
        "was equal to or within two points below the psyker's Leadership, the opposing player chooses which model in the "
        "target unit is affected; otherwise the psyker's owner chooses."),
    "Witchfire - Nova": (
        "A witchfire power (see Witchfire) that automatically targets and hits all ENEMY units within the power's maximum "
        "range. Line of sight, being engaged in melee, intervening terrain, etc. are ignored unless otherwise specified."),
    "Witchfire - Maelstrom": (
        "A witchfire power (see Witchfire) that automatically hits all units (friendly or enemy) within the affected "
        "area (typically a maximum range centred on the psyker). Line of sight, being engaged in melee, intervening "
        "terrain, etc. are ignored unless otherwise specified. May include effects that are blessings or maledictions."),
    "Psychic Power": (
        "A psychic power with its own timing, described in the power's text. Invoked with a Psychic Test using the "
        "normal ProHammer psychic rules (Perils of the Warp, Deny the Witch, Disturbance in the Warp) unless its text "
        "says otherwise."),
}


def _p(discipline, typ, text, profile=None, name=None, rule=None):
    """name: displayed power name when it differs from the key (two versions of one power);
    rule: rule / profile name when it differs from the default '<name> (<discipline>)'."""
    return dict(discipline=discipline, type=typ, text=text, profile=profile, name=name, rule=rule)


B, D, P, TK, TP = "Biomancy", "Divination", "Pyromancy", "Telekinesis", "Telepathy"
SA, MA = "Daemonology (Sanctic)", "Daemonology (Malefic)"

POWERS = {
    # ---------------------------------------------------------------- BIOMANCY (core.txt 2378-2433)
    "Smite": _p(B, "Witchfire", "Witchfire. Range 18\", S4, AP2, Assault 4.", ('18"', "4", "2", "Witchfire, Assault 4")),
    "Iron Arm": _p(B, "Blessing", "Blessing - targets the psyker. Adds +2 to Strength and +1 Toughness."),
    "Enfeeble": _p(B, "Malediction", "Malediction - enemy unit within 24\". -1 to Strength and Toughness, and the unit "
                                     "treats all movement as difficult terrain."),
    "Life Leech": _p(B, "Witchfire", "Witchfire. Range 18\", S6, AP2, Assault 2. If it causes at least one unsaved "
                                     "wound, a model within 6\" of the psyker regains a wound.",
                     ('18"', "6", "2", "Witchfire, Assault 2")),
    "Warp Speed": _p(B, "Blessing", "Blessing - targets the psyker. Gains +3 Initiative and +3 Attacks, and gains Fleet."),
    "Endurance": _p(B, "Blessing", "Blessing - friendly unit within 24\". Models in the unit gain Eternal Warrior, Feel "
                                   "No Pain (5+) and Relentless."),
    "Haemorrhage": _p(B, "Witchfire - Focused", "Focused Witchfire - range 18\". The target model must pass two "
                      "Toughness tests or suffer a wound with no armour or cover saves. If a model is killed, select "
                      "another model within 2\", which must pass a single Toughness test or suffer a wound as well. "
                      "Repeat until a Toughness test is passed."),
    # ---------------------------------------------------------------- DIVINATION
    "Prescience": _p(D, "Blessing", "Blessing - friendly unit within 12\". The unit re-rolls all failed To Hit rolls."),
    "Foreboding": _p(D, "Blessing", "Blessing - targets the psyker. The psyker and any joined unit gain Counter-Attack "
                                    "and may fire reaction fire using the full number of allowed shots."),
    "Forewarning": _p(D, "Blessing", "Blessing - friendly unit within 12\". The unit gains a 4+ invulnerable save."),
    "Perfect Timing": _p(D, "Blessing", "Blessing - targets the psyker. The psyker and any joined unit ignore cover when "
                                        "shooting an enemy unit."),
    "Precognition": _p(D, "Blessing", "Blessing - targets the psyker. The psyker re-rolls all failed To Hit and To Wound "
                                      "rolls. The psyker model re-rolls failed saving throws."),
    "Misfortune": _p(D, "Malediction", "Malediction - enemy unit within 24\". All attacks against this unit count as "
                                       "Rending."),
    "Scrier's Gaze": _p(D, "Blessing", "Blessing - targets the psyker. While the power is in effect, one reserve each "
                                       "turn may automatically pass its reserve roll; other reserve and outflank rolls "
                                       "may be re-rolled. Mysterious objective rolls can be re-rolled."),
    # ---------------------------------------------------------------- PYROMANCY
    "Flame Breath": _p(P, "Witchfire", "Witchfire. Template, S5, AP4, Assault 1, Soul Blaze.",
                       ("Template", "5", "4", "Witchfire, Assault 1, Soul Blaze")),
    "Fiery Form": _p(P, "Blessing", "Blessing - targets the psyker. Gains a 4+ invulnerable save and all its melee "
                                    "attacks cause Soul Blaze. Re-rolls failed wounds inflicted by any other Pyromancy "
                                    "powers."),
    "Molten Beam": _p(P, "Witchfire - Beam", "Beam. Range 12\", S8, AP1, Assault 1, Melta.",
                      ('12"', "8", "1", "Witchfire - Beam, Assault 1, Melta")),
    "Fire Shield": _p(P, "Blessing", "Blessing - friendly unit within 24\". The unit gains a 4+ cover save and all enemy "
                                     "units within 6\" of it treat all terrain (even open ground) as dangerous terrain."),
    "Sunburst": _p(P, "Witchfire - Nova", "Nova. Range 9\", S4, AP5, Assault 2D6, Ignores Cover, causes Soul Blaze.",
                   ('9"', "4", "5", "Witchfire - Nova, Assault 2D6, Ignores Cover, Soul Blaze")),
    "Inferno": _p(P, "Witchfire", "Witchfire. Range 24\", S4, AP5, Assault 1, Ignores Cover, Large Blast, Soul Blaze.",
                  ('24"', "4", "5", "Witchfire, Assault 1, Ignores Cover, Large Blast, Soul Blaze")),
    "Spontaneous Combustion": _p(P, "Witchfire - Focused", "Focused Witchfire - range 18\". The target model suffers a "
                                 "S6 AP3 hit with Soul Blaze. If the model is slain, place a blast marker over the removed "
                                 "model: all models hit suffer a S5 AP4 hit that ignores cover and causes Soul Blaze."),
    # ---------------------------------------------------------------- DAEMONOLOGY (SANCTIC) (core.txt 2436-2483)
    "Banishment": _p(SA, "Malediction", "Malediction - enemy DAEMON unit within 24\". All models in the target unit "
                                        "suffer -1 to their invulnerable saves."),
    "Gate of Infinity": _p(SA, "Blessing", "Blessing - targets the psyker. Remove the psyker and any joined unit from "
                                           "the board and immediately re-deploy it using the Deep Strike rules."),
    "Hammerhand": _p(SA, "Blessing", "Blessing - targets the psyker. The psyker and any joined unit gain +2 Strength."),
    "Sanctuary": _p(SA, "Blessing", "Blessing - targets the psyker. The psyker and any joined unit receive +1 to their "
                                    "invulnerable saves (or gain a 6+ invulnerable save). Units with the Daemon special "
                                    "rule treat all terrain within 12\" of the psyker as dangerous terrain (even open "
                                    "ground)."),
    "Purge Soul": _p(SA, "Witchfire - Focused", "Focused Witchfire - range 24\". The psyker and the target model each "
                     "roll a D6 and add their Leadership. If the psyker's total is greater than or equal, the target "
                     "suffers an automatic wound with no armour or cover saves allowed."),
    "Cleansing Flame": _p(SA, "Witchfire - Nova", "Nova. Range 9\", S5, AP4, Assault 2D6, Ignores Cover, Soul Blaze.",
                          ('9"', "5", "4", "Witchfire - Nova, Assault 2D6, Ignores Cover, Soul Blaze")),
    "Vortex of Doom": _p(SA, "Witchfire", "Witchfire. Range 12\", S10, AP1, Assault 1, Blast, Vortex.",
                         ('12"', "10", "1", "Witchfire, Assault 1, Blast, Vortex")),
    # ---------------------------------------------------------------- DAEMONOLOGY (MALEFIC)
    "Summoning": _p(MA, "Conjuration", "Conjuration - range 12\". Summons one of the following: 8 Bloodletters, 9 Pink "
                                       "Horrors, 7 Plaguebearers, 6 Daemonettes, 4 Flesh Hounds, 3 Flamers, 4 Nurglings or "
                                       "6 Seekers."),
    "Cursed Earth": _p(MA, "Blessing", "Blessing - targets the psyker. All DAEMON models within 12\" of the psyker have "
                                       "+1 to their invulnerable saves. Deep striking daemons do not scatter when the "
                                       "centre model is placed within 12\" of the psyker."),
    "Dark Flame": _p(MA, "Witchfire", "Witchfire. Template, S4, AP5, Assault 1, Soul Blaze, Torrent.",
                     ("Template", "4", "5", "Witchfire, Assault 1, Soul Blaze, Torrent")),
    "Possession": _p(MA, "Conjuration", "Conjuration - range 6\". Summons 1 Bloodthirster, Lord of Change, Great Unclean "
                                        "One or Keeper of Secrets. If successful, the invoking psyker is removed as a "
                                        "casualty. MAY ONLY BE USED BY A PSYKER WITH MASTERY LEVEL 2 OR GREATER."),
    "Sacrifice": _p(MA, "Conjuration", "Conjuration - range 6\". Summons 1 Herald of Khorne / Tzeentch / Nurgle / "
                                       "Slaanesh with 30 pts of wargear (see Codex: Chaos Daemons). If successfully "
                                       "invoked, one friendly model within 6\" of the psyker takes a wound with no saves "
                                       "of any kind allowed."),
    "Incursion": _p(MA, "Conjuration", "Conjuration - range 12\". Summons 3 Bloodcrushers, 4 Screamers, 3 Plague Drones "
                                       "or 3 Fiends."),
    "Infernal Gaze": _p(MA, "Witchfire - Beam", "Beam. Range 18\", S3, AP4, Assault 1, Armourbane, Fleshbane.",
                        ('18"', "3", "4", "Witchfire - Beam, Assault 1, Armourbane, Fleshbane")),
    # ---------------------------------------------------------------- TELEKINESIS (core.txt 2486-2541)
    "Assail": _p(TK, "Witchfire - Beam", "Beam. Range 18\", S6, AP -, Assault 1, Strikedown.",
                 ('18"', "6", "-", "Witchfire - Beam, Assault 1, Strikedown")),
    "Crush": _p(TK, "Witchfire - Focused", "Focused Witchfire - range 18\". Roll 2D6: the target suffers a hit with "
                "Strength equal to the roll. Roll another D6 for the AP value.",
                ('18"', "2D6", "D6", "Witchfire - Focused")),
    "Objuration Mechanicum": _p(TK, "Malediction", "Malediction - enemy unit within 24\". All of the target unit's "
                                "ranged weapon attacks have the Gets Hot special rule. Vehicles suffer an immediate hit "
                                "with the Haywire effect."),
    "Shockwave": _p(TK, "Witchfire - Nova", "Nova. Range 9\", S4, AP -, Assault 2D6, Pinning.",
                    ('9"', "4", "-", "Witchfire - Nova, Assault 2D6, Pinning")),
    "Levitation": _p(TK, "Blessing", "Blessing - targets the psyker. The psyker and any joined unit may immediately move "
                                     "up to 12\" (cannot land on other models or impassable terrain). They cannot charge "
                                     "this turn and count as having moved."),
    "Telekine Dome": _p(TK, "Blessing", "Blessing - targets the psyker. The psyker and all friendly models within 12\" "
                                        "have a 5+ invulnerable save against shooting attacks."),
    "Psychic Maelstrom": _p(TK, "Witchfire", "Witchfire. Range 12\", S10, AP1, Assault 1, Barrage, Large Blast.",
                            ('12"', "10", "1", "Witchfire, Assault 1, Barrage, Large Blast")),
    # ---------------------------------------------------------------- TELEPATHY
    "Psychic Shriek": _p(TP, "Witchfire", "Witchfire - range 18\". Roll 3D6 and subtract the target's Leadership: the "
                                          "unit suffers wounds equal to the result, with no armour or cover saves."),
    "Dominate": _p(TP, "Malediction", "Malediction - enemy unit within 24\". The target unit must pass a Leadership test "
                                      "each time it attempts to move, advance, shoot, charge or use a psychic power."),
    "Mental Fortitude": _p(TP, "Blessing", "Blessing - friendly unit within 24\". If the target is falling back, it "
                                           "immediately regroups. The target gains Fearless."),
    "Terrify": _p(TP, "Malediction", "Malediction - enemy unit within 24\". The target unit has -1 Leadership and treats "
                                     "all opposing units as if they had Fear. It must take a casualty test at the end of "
                                     "the turn."),
    "Hallucination": _p(TP, "Malediction", "Malediction - enemy unit within 24\". Roll a D6 and the unit suffers the "
                                           "result: 1-2: the unit must take a Pinning test; 3-4: the unit suffers -1 WS, "
                                           "BS, Initiative and Attacks; 5-6: randomly select a model in the unit - it "
                                           "takes a hit for every other model in the unit, with Strength equal to the "
                                           "majority Strength in the unit."),
    "Invisibility": _p(TP, "Blessing", "Blessing - friendly unit within 24\". Opposing units suffer -1 To Hit when "
                                       "making ranged and melee attacks against the target unit."),
    "Shrouding": _p(TP, "Blessing", "Blessing - targets the psyker. All friendly models within 6\" of the psyker have "
                                    "the Shrouded special rule."),

    # ================================================================ Legion-specific powers
    # V White Scars (V_White_Scars.txt 232-247): Stormseer, Targutai Yesugei
    "Unseen Bolt": _p(None, "Witchfire", "Psychic shooting power, used during the psyker's Shooting phase instead of "
                      "firing another weapon. Range 36\", S6, AP4, Assault 1, Blast, Pinning. Take a Psychic test using "
                      "the normal ProHammer psychic rules; if successful, resolve the attack using this profile. Unseen "
                      "Bolt may not be invoked during Return Fire, Overwatch or Stand & Shoot.",
                      ('36"', "6", "4", "Witchfire, Assault 1, Blast, Pinning")),
    # VI Space Wolves (VI_Space_Wolves.txt 281-282, 1575-1590): Rune Priest, Ohthere Wyrdmake
    "Mystic Winds of Fenris": _p(None, "Blessing", "Blessing - friendly Space Wolves unit within 6\". If the Psychic "
                                 "Test is passed, nominate the Rune Priest or one friendly Space Wolves unit with at "
                                 "least one model within 6\". Until the beginning of the next Space Wolves turn, the "
                                 "nominated unit receives a 5+ Cover Save. If the unit already has a Cover Save, improve "
                                 "that save by 1, to a maximum of 4+."),
    "Living Lightning": _p(None, "Witchfire", "Witchfire psychic power used during the Shooting phase. If successfully "
                           "invoked, resolve it using the profile: Range 24\", S5, AP4, Assault D6.",
                           ('24"', "5", "4", "Witchfire, Assault D6")),
    # VIII Night Lords (VIII_Night_Lords.txt 753-761): Sevatar
    "Withering Gaze": _p(None, "Psychic Power", "Used during the Night Lords Shooting phase instead of Sevatar firing a "
                         "weapon. Choose one visible enemy unit within 12\" and take a Psychic Test (Sevatar uses "
                         "Leadership 7). If successful, until the beginning of the next Night Lords turn, that enemy unit "
                         "must pass a Leadership test before it may declare a charge against Sevatar or a unit he has "
                         "joined. If the test is failed, the unit may not declare that charge during that Assault phase, "
                         "but may declare a charge against another eligible target."),
    # XIV Death Guard (XIV_Death_Guard.txt 668-673, 1466-1490): Calas Typhon, Mortarion (Daemon Primarch)
    "Aura of Pestilence": _p(None, "Psychic Power", "At the beginning of either player's Assault phase, Typhon may "
                             "attempt to invoke Aura of Pestilence (Psychic Test on Leadership 7). If passed, every enemy "
                             "model within 2\" of Typhon suffers -1 Attack, to a minimum of 1, until the end of that "
                             "Assault phase. If failed, every friendly model within 2\" of Typhon instead suffers -1 "
                             "Attack, to a minimum of 1, until the end of that Assault phase. Typhon may fight normally "
                             "during an Assault phase in which Aura of Pestilence is used."),
    "Miasma of Pestilence": _p(None, "Psychic Power", "Phase: beginning of the enemy Assault phase. Range 12\". Choose "
                               "one enemy unit within range and take a Psychic Test. If successful, the unit suffers -1 "
                               "Initiative and -1 Attack, to a minimum of 1, until the end of the Assault phase."),
    "Curse of Decay": _p(None, "Psychic Power", "Phase: Mortarion's Shooting phase. Range 18\". Choose one enemy unit "
                         "within range and take a Psychic Test. If successful, the unit treats all terrain, including "
                         "open ground, as Difficult Terrain until the beginning of Mortarion's next turn."),
    "Nurgle's Rot": _p(None, "Psychic Power", "Phase: Mortarion's Shooting phase. Range 12\". Choose one enemy unit "
                       "within range and take a Psychic Test. If successful, the target suffers D6 Strength 4 AP4 hits "
                       "with Poisoned (3+)."),
    # XV Thousand Sons (XV_Thousand_Sons.txt 497-500, 975-976, 1887-1904, 2088-2110)
    "Mindsong of Blades": _p(None, "Blessing", "Blessing invoked at the beginning of an Assault phase. If successfully "
                             "invoked, until the end of that Assault phase models in the Psyker's unit gain +1 "
                             "Initiative and may re-roll close-combat To Hit rolls of 1."),
    "Psy-Synchronicity": _p(None, "Blessing", "Blessing invoked during the Thousand Sons Movement phase. If successfully "
                            "invoked, select up to two friendly Thousand Sons units with at least one model within 6\" of "
                            "the Numerologist. Until the end of the following Thousand Sons Shooting phase, models in "
                            "those units may re-roll shooting To Hit rolls of 1. The Numerologist may not fire a weapon "
                            "during a player turn in which he successfully invokes Psy-Synchronicity."),
    "Infernal Phoenix": _p(None, "Witchfire - Beam", "Witchfire - Beam. Range 24\", Strength 8, AP1, Melta. Resolve "
                           "using the normal rules for Beam psychic powers.",
                           ('24"', "8", "1", "Witchfire - Beam, Melta")),
    "Strands of Fate": _p(None, "Malediction", "Malediction. Choose one enemy non-Vehicle unit within 18\" and line of "
                          "sight. Until the beginning of Magnus' next turn, that unit must pass a Leadership Test each "
                          "time it attempts to move during the Movement phase, shoot during the Shooting phase or declare "
                          "a Charge. If the test is failed, the attempted action is lost and the unit may not attempt "
                          "that type of action again during that phase. A separate Leadership Test is required for each "
                          "different action attempted."),
    # Magnus, Shard of the Crimson King (XV_Thousand_Sons.txt 2101-2110): his own Strands of Fate text
    "Strands of Fate (Shard)": _p(None, "Malediction", "Malediction. Range 18\". Choose one enemy non-Vehicle unit "
                                  "within range and line of sight. Until the beginning of Magnus' next turn, the "
                                  "affected unit must pass a Leadership Test each time it wishes to: Move; Shoot; "
                                  "Charge. If the test is failed, that action is lost for that phase.",
                                  name="Strands of Fate", rule="Strands of Fate (Shard of the Crimson King)"),
    # XVIII Salamanders (XVIII_Salamanders.txt 216-232): The Awakening Fire, Xiaphas Jurr
    "Fury of the Salamander": _p(None, "Witchfire - Beam", "Witchfire - Beam. Range 18\", S5, AP1, Assault 1, Elemental "
                                 "Horror. Elemental Horror: if an enemy unit suffers one or more unsaved Wounds from Fury "
                                 "of the Salamander, it must immediately take a Morale test regardless of how many "
                                 "casualties were caused, with a Leadership penalty equal to the number of unsaved Wounds "
                                 "caused by Fury of the Salamander. (Counts as a Pyromancy power for Salamanders "
                                 "Librarians in a Detachment using The Awakening Fire.)",
                                 ('18"', "5", "1", "Witchfire - Beam, Assault 1, Elemental Horror")),
}


def in_discipline(d):
    return [n for n, p in POWERS.items() if p["discipline"] == d]
