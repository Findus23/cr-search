from html import unescape

from peewee import fn
from srt import parse

from models import Person, Line, Episode, db
from typo import fix_typo
from utils import td_to_milliseconds, get_filename

campaign = 2

for episode_nr in range(1, 95):
    file = get_filename(campaign, episode_nr)
    text = file.read_text()
    subtitlelines = parse(text)
    print(episode_nr)
    person = None
    episode = Episode.get(season=campaign, episode_number=episode_nr)
    with db.atomic():
        i = 0
        for line in subtitlelines:
            i += 1
            assert i == line.index
            text = unescape(line.content)
            dbline = Line()
            if ":" in text:
                name, resttext = text.split(":", maxsplit=1)
                if name.isupper():
                    formatted_name = fix_typo(name.strip()).title()
                    if formatted_name == "San":
                        print(name.title())
                    person, created = Person.get_or_create(name=formatted_name)
                    text = resttext.strip()
            else:
                if text.startswith("(") and text.endswith(")"):
                    dbline.isnote = True
                    person = None
                elif text.startswith("[") and text.endswith("]"):
                    dbline.ismeta = True
                    person = None
            text = text.replace("\n", " ")
            dbline.text = text
            dbline.search_text = fn.to_tsvector('english', text)
            dbline.person = person
            dbline.starttime = td_to_milliseconds(line.start)
            dbline.endtime = td_to_milliseconds(line.end)
            dbline.episode = episode
            dbline.order = line.index
            dbline.save()
