from peewee import PostgresqlDatabase, Model, IntegerField, CharField, BooleanField, ForeignKeyField
from playhouse.postgres_ext import TSVectorField

from config import dbauth

db = PostgresqlDatabase(**dbauth)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Episode(BaseModel):
    season = IntegerField()
    episode_number = IntegerField()
    video_number = IntegerField()
    youtube_id = CharField(max_length=11)

    class Meta:
        indexes = ((("season", "video_number"), True),)

    @property
    def name(self) -> str:
        return f"C{self.season}E{self.episode_number:03d}"


class Person(BaseModel):
    name = CharField(unique=True)
    color = CharField(null=True)


FULL_TEXT_SEARCH = '''SELECT id, text, ts_rank_cd(search_text, query) AS rank
FROM line,
     to_tsquery('english', %s) query
WHERE search_text @@ query
ORDER BY rank DESC
'''


class Line(BaseModel):
    text = CharField()
    search_text = TSVectorField()
    person = ForeignKeyField(Person, backref="lines", null=True)
    isnote = BooleanField(default=False)
    ismeta = BooleanField(default=False)
    starttime = IntegerField()
    endtime = IntegerField()
    episode = ForeignKeyField(Episode, backref="lines")
    order = IntegerField()

    class Meta:
        indexes = ((("episode", "order"), True),)

    @classmethod
    def full_text_search(cls, query_string: str):
        cursor = cls._meta.database.execute_sql(
            FULL_TEXT_SEARCH,
            (query_string,)
        )
        result = cursor.fetchall()
        cursor.close()
        return result


class Phrase(BaseModel):
    text = CharField()
    count = IntegerField()
    episode = ForeignKeyField(Episode, backref="phrase")

    class Meta:
        indexes = ((("text", "episode"), True),)
