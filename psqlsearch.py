import logging
from datetime import datetime

from peewee import SQL, fn, Alias
from psycopg2._psycopg import cursor

from models import Line, Person, Episode, db
from utils import milliseconds_to_td

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

terms = "where a bunch of us nerdy-ass actors"
start_time = datetime.now()
a = Alias(fn.ts_rank(Line.search_text, fn.plainto_tsquery('english', terms)), "rank")

results = Line.select(Line, Person, Episode, a).where(
    (Line.search_text.match(terms, language="english", plain=True))
    &
    (Episode.episode_number <= 100)
    &
    (Episode.season == 2)
).order_by(SQL("rank DESC")).join(Person).switch(Line).join(Episode).limit(100)
end_time = datetime.now()
print(end_time - start_time)
# results = Line.full_text_search(terms)
if len(results) == 0:
    result: cursor = db.execute_sql("select plainto_tsquery('english',%s)", [terms])
    parsed = result.fetchone()[0]
    if not parsed:
        raise ValueError("only stop words were used")
    else:
        print(parsed)
for line in results:
    print(line.episode.name, milliseconds_to_td(line.starttime), line.rank, line.person.name + ": " + line.text)
