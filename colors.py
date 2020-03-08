from models import Person

colors_c2 = {
    "Laura": "#59c3f9",
    "Marisha": "#00146e",
    "Liam": "#fe8413",
    "Taliesin": "#be1c0d",
    "Ashley": "#868984",
    "Sam": "#dae1dd",
    "Travis": "#076708",
    "Matt": "#471f0e"  # random color
}

p: Person
for p in Person.select():
    print(p)
    if p.name in colors_c2.keys() and p.season == 2:
        print(p.name)
        p.color = colors_c2[p.name]
        p.save()
