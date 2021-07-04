"""
replace common typos of names to unify them in the database
"""

typos = {
    "Matt": {"Mat", "Mattt", "\"Matt", "Matr", "Mtt"},
    "Sam": {"San", "Nott", "Sma", "Sasm", "Sm", "Ssam"},
    "Travis": {"Tarvis", "Travs", "Travia", "Traivs", "Tavis", "Trvis"},
    "Taliesin": {"Taiesin", "Talisin", "Talisen", "Taleisn", "Talisein", "Talieisin", "Talesin", "Talisan", "Taleisin",
                 "Talieisn", "Talisien", "Tailesin", "Tlaiesin", "Tlaiesin"},
    "Marisha": {"Beau", "Mariasha", "Maisha", "Marisa", "Marish", "Marihsa", "Marsha", "Marsisha", "Marishaa",
                "Marihsha", "\\Marisha", "Marisah", "Marissa", "Marirsha", "Marisaha", "Mairsha", "Marshia", "Marsiha",
                "Marishia", "Marsiah", "Matisha", "Mraisha", "Amrisha", "<Arisha"},
    "Laura": {"Lauda", "Lauren", "Larua", "Laur", "Lauar", "Vex", "Laira"},
    "Liam": {"Caleb", "Laim", "Vax"},
    "Ashley": {"Ashly", "Ashely", "Ashey", "Aslhey", "Ahsley"},
    "All": {"Everyone", "Everybody"},
    "Mark": {"Marik"},
    "Brian": {"Brain", "\"Brian"},
    "Joe": {"Jroe"},
    "Man Off-Camera": {"Man Off Camera"},
    "Off-Screen": {"Offscreen"},
    "Anjali": {"Anajli"},
    "H. Michael": {"H Michael", "H.Michael"},
    "Allura": {"Alura"},
    "Krystina": {"Krystin"},
    "Michelle":{"Michlle"},
    "Alicia":{"Alica"}
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
