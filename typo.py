"""
replace common typos of names to unify them in the database
"""

typos = {
    "Matt": {"Mat", "Mattt", "\"Matt"},
    "Sam": {"San", "Nott", "Sma", "Sasm", "Sm"},
    "Travis": {"Tarvis", "Travs", "Travia", "Traivs"},
    "Taliesin": {"Taiesin", "Talisin", "Talisen", "Taleisn", "Talisein"},
    "Marisha": {"Beau", "Mariasha", "Maisha", "Marisa", "Marish", "Marihsa", "Marsha", "Marsisha", "Marishaa"},
    "Laura": {"Lauda", "Lauren", "Larua", "Laur"},
    "Liam": {"Caleb", "Laim"},
    "Ashley": {"Ashly", "Ashely", "Ashey"},
    "All": {"Everyone", "Everybody"},
    "Mark": {"Marik"},
    "Brian": {"Brain"}
}
replacements = {}
for correct, typoset in typos.items():
    for typo in typoset:
        replacements[typo] = correct


def fix_typo(text: str) -> str:
    for search, replace in replacements.items():
        if text == search.upper():
            text = replace.upper()
    return text


if __name__ == '__main__':
    print(fix_typo("San"))
