from datetime import datetime

from peewee import IntegerField, CharField, BooleanField, ForeignKeyField, DateTimeField, \
    DateField, TextField
from playhouse.postgres_ext import TSVectorField

from app import flask_db


class BaseModel(flask_db.Model):
    ...


class Series(BaseModel):
    title = CharField(max_length=100)
    slug = CharField(max_length=100)
    is_campaign = BooleanField()
    single_speaker = BooleanField()

    def __str__(self) -> str:
        return f"<Series: {self.title}>"


class Episode(BaseModel):
    series = ForeignKeyField(Series, backref="episodes", on_delete="CASCADE")
    episode_number = IntegerField()
    video_number = IntegerField()
    youtube_id = CharField(max_length=11)
    title = CharField(max_length=100)
    pretty_title = CharField(max_length=100)
    downloaded = BooleanField(default=False)
    text_imported = BooleanField(default=False)
    phrases_imported = BooleanField(default=False)
    subtitle_hash = CharField(max_length=64, null=True)
    upload_date = DateField()
    last_updated = DateTimeField(default=datetime.now)

    class Meta:
        indexes = ((("series", "video_number"), True),)

    @property
    def name(self) -> str:
        return f"C{self.season}E{self.episode_number:03d}"

    def __str__(self) -> str:
        return f"<Episode: {self.title}>"


class Person(BaseModel):
    name = CharField()
    color = CharField(null=True)
    series = ForeignKeyField(Series)

    class Meta:
        indexes = ((("name", "series"), True),)

    def __str__(self) -> str:
        return f"<Person: {self.name}>"


class Line(BaseModel):
    text = TextField()
    search_text = TSVectorField()
    person = ForeignKeyField(Person, backref="lines", null=True, on_delete="CASCADE")
    isnote = BooleanField(default=False)
    ismeta = BooleanField(default=False)
    starttime = IntegerField()
    endtime = IntegerField()
    episode = ForeignKeyField(Episode, backref="lines", on_delete="CASCADE")
    order = IntegerField()

    class Meta:
        indexes = ((("episode", "order"), True),)

    def __str__(self) -> str:
        if self.is_dirty():
            return f"<Line: {self.order} (dirty)>"
        return f"<Line: {self.id}>"


class Phrase(BaseModel):
    text = CharField()
    count = IntegerField()
    episode = ForeignKeyField(Episode, backref="phrase", on_delete="CASCADE")

    class Meta:
        indexes = ((("text", "episode"), True),)

    def __str__(self) -> str:
        return f"<Line: {self.text} ({self.pk})>"
