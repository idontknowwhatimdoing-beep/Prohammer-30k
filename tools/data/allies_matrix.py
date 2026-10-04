"""Allies Matrix - At the Height of the Heresy (Games in the Age of Darkness).

Copied verbatim from the Google Doc. Rows and columns use the document's abbreviations; a blank cell is a cell the
document leaves empty.
"""
MATRIX_TABLE = """
|  | DA | EC | WS | SW | IF | NL | BA | IH | WE | UM | DG | TS | SoH | WB | S | RG | AL | ME | Ex | Q | SA | D | BS |
| DA | A | S | A | C | A | S | A | A | S | A | S | S | S | S | A | A | S | A | A | A | A | S | C |
| EC | S | A | S | S | S | A | S | S | A |  | A | A | A | A | S | S | C | A | A | A | A | A | C |
| WS | A | S | A | A | A | S | A | A | S | A | S | S | S | S | A | A | S | A | A | A | A | S | C |
| SW | S | S | A | A | A | S | A | A | S | A | S | S | S | S | A | A | S | A | A | A | A | S | C |
| IF | A | S | A | A | A | S | A | A | S | A | S | S | S | S | A | A | S | A | A | A | A | S | C |
| NL | S | A | S | S | S | A | S | S | A | S | A | A | A | A | S |  | C | A | A | A | A | A | C |
| BA | A | S | A | A | A | S | A | A | S | A | S | S | S | S | A | A | S | A | A | A | A | S | C |
| IH | A | S | A | A | A | S | A | A | S | A | S | S | S | S | A | A | S | A | A | A | A | S | C |
| WE | S | A | S | S | S | A | S | S | A | S | A | A | A | A | S | S | C | A | A | A | A | A | C |
| UM | A | S | A | A | A | S | A | A | S | A | S | S | S | S | A | A | S | A | A | A | A | S | C |
| DG | S | A | S | S | S | A | S | S | A | S | A | S | A | S | S | S | C | A | A | A | A | C | C |
| TS | S | A | S | S | S | A | S | S | A | S | S | A | A | A | S | S | C | A | A | A | A | C | C |
| SoH | S | A | S | S | S | A | S | S | A | S | A | A | A | S | S | S | A | A | A | A | A | A | C |
| WB | S | A | S | S | S | A | S | S | A | S | S | A | S | A | S | S | C | A | A | A | A | A | C |
| S | A | S | A | A | A | S | A | A | S | A | S | S | S | S | A | A | S | A | A | A | A | S | C |
| RG | A | S | A | A | A | S | A | A | S | A | S | S | S | S | A | A | S | A | A | A | A | S | C |
| AL | S | C | S | S | S | C | S | S | C | S | C | C | A | C | S | S | A | A | A | A | A | A | C |
| ME | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | S | C |
| EX | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | S | C |
| Q | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | S | C |
| SA | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | A | S | C |
| D | S | A | S | S | S | A | S | S | A | S | C | C | A | A | S | S | A | S | S | S | S | A | C |
| BS | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | A |
"""

LEGEND = {
    "A": ("Allies and Brothers",
          "These forces cooperate freely on the battlefield. Units from both detachments count as friendly units when "
          "determining eligible targets for beneficial abilities, wargear and psychic powers.\nNon-faction-specific "
          "effects may benefit allied units, including applicable Signum and Nuncio-vox effects. All normal targeting, "
          "range and usage restrictions still apply.\nIndependent Characters may join allied units, and units may embark "
          "in allied transports, subject to the normal joining, capacity and transport restrictions.\nThis relationship "
          "does not grant or transfer Legion traits, army-specific rules, Rites of War or other faction-specific bonuses. "
          "An effect restricted to a particular Legion, faction, unit or detachment retains that restriction."),
    "C": ("Conditional Alliance",
          "These forces fight alongside one another but operate independently. Units from both detachments count as "
          "friendly units for movement and combat and cannot deliberately attack one another.\nNeither detachment may "
          "benefit from abilities, wargear, psychic powers or other bonuses provided by the other detachment. This "
          "includes beneficial auras, Leadership effects and shared equipment effects.\nIndependent Characters cannot "
          "join units from the other detachment, and units cannot embark in the other detachment\u2019s transports.\n"
          "Each detachment retains its own rules and bonuses, applying them only within that detachment."),
    "S": ("Sworn Enemies",
          "These forces cannot be included together in the same army. Neither may be selected as an allied detachment "
          "of the other.\nThis prohibition also applies when a third faction is present: a permitted alliance with "
          "another detachment does not allow Sworn Enemies to fight together."),
}
GENERAL = ("Apply the chart separately to every pair of detachments in the army. An alliance never overrides "
           "army-building restrictions, allegiance requirements or the specific wording of a unit, ability or item of "
           "wargear.")


def matrix():
    """{(row, col): 'A' | 'C' | 'S' | ''}"""
    rows = [r.strip().strip("|").split("|") for r in MATRIX_TABLE.strip().splitlines()]
    cols = [c.strip() for c in rows[0][1:]]
    out = {}
    for r in rows[1:]:
        name = r[0].strip()
        for c, v in zip(cols, r[1:]):
            out[(name, c)] = v.strip()
    return cols, out
