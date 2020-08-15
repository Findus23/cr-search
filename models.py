from datetime import datetime

from peewee import PostgresqlDatabase, Model, IntegerField, CharField, BooleanField, ForeignKeyField, DateTimeField
from playhouse.postgres_ext import TSVectorField

from config import dbauth

db = PostgresqlDatabase(**dbauth)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Series(BaseModel):
    title = CharField(max_length=100)
    is_campaign = BooleanField()
    single_speaker = BooleanField()


class Episode(BaseModel):
    series = ForeignKeyField(Series, backref="episodes")
    episode_number = IntegerField()
    video_number = IntegerField()
    youtube_id = CharField(max_length=11)
    title = CharField(max_length=100)
    pretty_title = CharField(max_length=100)
    downloaded = BooleanField(default=False)
    text_imported = BooleanField(default=False)
    phrases_imported = BooleanField(default=False)
    subtitle_hash = CharField(max_length=64, null=True)
    last_updated = DateTimeField(default=datetime.now)

    class Meta:
        indexes = ((("series", "video_number"), True),)

    @property
    def name(self) -> str:
        return f"C{self.season}E{self.episode_number:03d}"


class Person(BaseModel):
    name = CharField()
    color = CharField(null=True)
    series = ForeignKeyField(Series)

    class Meta:
        indexes = ((("name", "series"), True),)


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


class Phrase(BaseModel):
    text = CharField()
    count = IntegerField()
    episode = ForeignKeyField(Episode, backref="phrase")

    class Meta:
        indexes = ((("text", "episode"), True),)
