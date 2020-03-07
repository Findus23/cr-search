import logging

from sonic import SearchClient

from models import Line, Episode, Person
from utils import milliseconds_to_td

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

with SearchClient("127.0.0.1", 1491, "SecretPassword") as querycl:
    results = querycl.query("crsearch", "crsearch", "gnome", lang="eng")
    real_results = []
    for rs in results:
        r = int(rs)
        real_results.extend([r - 1, r, r + 1])
    lines = Line.select(Line, Person, Episode).where(Line.id << real_results).join(Person).switch(Line).join(Episode)
    for line in lines:
        print(line.episode.name, milliseconds_to_td(line.starttime), line.person.name + ": " + line.text)

    results = querycl.suggest("crsearch", "crsearch", "regular")
    print(results)
