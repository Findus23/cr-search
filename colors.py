from data import colors_c2, colors_c1
from models import Person, Series

campaign2 = Series.select().where(Series.title == "Campaign 2").get()
campaign1 = Series.select().where(Series.title == "Campaign 1").get()

p: Person
for p in Person.select():
    if p.name in colors_c1.keys() and p.series == campaign1:
        print(p.name)
        p.color = colors_c1[p.name]
        p.save()
    if p.name in colors_c2.keys() and p.series == campaign2:
        print(p.name)
        p.color = colors_c2[p.name]
        p.save()
