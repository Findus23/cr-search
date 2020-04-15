import json

from models import Series

series_list = []

for series in Series.select():
    series_list.append({"title": series.title, "id": series.id})

with open("web/data.json", "w") as f:
    json.dump({
        "series": series_list
    }, f, indent=2)
