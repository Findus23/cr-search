from data import colors_c2
from models import Person, Series

p: Person
for p in Person.select():
    campaign2 = Series.select().where(Series.title == "Campaign 2")
    print(p)
    if p.name in colors_c2.keys() and p.series == campaign2:
        print(p.name)
        p.color = colors_c2[p.name]
        p.save()
