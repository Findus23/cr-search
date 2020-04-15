from data import colors_c2
from models import Person

p: Person
for p in Person.select():
    print(p)
    if p.name in colors_c2.keys() and p.season == 2:
        print(p.name)
        p.color = colors_c2[p.name]
        p.save()
