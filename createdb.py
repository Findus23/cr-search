from sys import argv

from models import db, Series, Phrase, Episode, Person, Line


def confirm(message: str) -> None:
    if "y" not in input(message):
        raise ValueError("abort")


if len(argv) < 2:
    raise ValueError("select mode")
mode = argv[1]

if mode == "all":
    confirm("Delete all Data? ")
    db.drop_tables([Series, Episode, Person, Line, Phrase])
    db.create_tables([Series, Episode, Person, Line, Phrase])
elif mode == "phrases":
    confirm("Delete all Phrases? ")
    db.drop_tables([Phrase])
    db.create_tables([Phrase])

if mode in ["all", "phrases"]:
    db.execute_sql("CREATE INDEX phrases_text_index ON phrase USING gin (text gin_trgm_ops)")
