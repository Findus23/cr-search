"""
replace common typos of names to unify them in the database
"""

typos = {
    "Matt": {"Mat", "Mattt", "\"Matt", "Matr"},
    "Sam": {"San", "Nott", "Sma", "Sasm", "Sm"},
    "Travis": {"Tarvis", "Travs", "Travia", "Traivs"},
    "Taliesin": {"Taiesin", "Talisin", "Talisen", "Taleisn", "Talisein", "Talieisin", "Talesin", "Talisan", "Taleisin",
                 "Talieisn", "Talisien"},
    "Marisha": {"Beau", "Mariasha", "Maisha", "Marisa", "Marish", "Marihsa", "Marsha", "Marsisha", "Marishaa",
                "Marihsha", "\\Marisha", "Marisah", "Marissa"},
    "Laura": {"Lauda", "Lauren", "Larua", "Laur", "Lauar", "Vex", "Laira"},
    "Liam": {"Caleb", "Laim", "Vax"},
    "Ashley": {"Ashly", "Ashely", "Ashey"},
    "All": {"Everyone", "Everybody"},
    "Mark": {"Marik"},
    "Brian": {"Brain"},
}
replacements = {}
for correct, typoset in typos.items():
    for typo in typoset:
        replacements[typo] = correct


def fix_typo(text: str) -> str:
    try:
        if text[0] == "-":
            text = text[1:]
    except IndexError:
        return ""
    for search, replace in replacements.items():
        if text == search.lower():
            text = replace.lower()
    return text


if __name__ == '__main__':
    print(fix_typo("San"))
