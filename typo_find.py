from difflib import SequenceMatcher
from itertools import combinations

from models import Person

people = set()
for p in Person.select():
    if "\n" not in p.name:
        if "," in p.name:
            names = [n.strip() for n in p.name.split(",")]
            people.update(names)
        else:
            people.add(p.name)
print(people)

for a, b in combinations(people, r=2):
    s = SequenceMatcher(None, a, b)
    ratio = s.ratio()
    if ratio < 0.8 or ratio == 1:
        continue
    print(a, "|", b)
    print(ratio)
