from models import db, Episode, Person, Line, Phrase

# db.drop_tables([Episode, Person, Line, Phrase])
# db.create_tables([Episode, Person, Line, Phrase])
db.drop_tables([Phrase])
db.create_tables([Phrase])
