from data import colors
from models import Person, Series

campaign2 = Series.select().where(Series.title == "Campaign 2").get()
campaign1 = Series.select().where(Series.title == "Campaign 1").get()

p: Person
for p in Person.select().join(Series):
    if p.series.slug in colors:
        series_colors = colors[p.series.slug]
        if p.name in series_colors.keys():
            p.color=series_colors[p.name]
            p.save()

