import re
from html import unescape

from peewee import fn
from srt import parse

from models import Person, Line, Episode, db
from typo import fix_typo
from utils import td_to_milliseconds, get_filename


def is_invalid_name(name: str) -> bool:
    for a in ["PS", "P.S.", "II", "The US", "Metal Gear", "D&amp;D"]:
        if a.lower() in name.lower():
            return True
    return False


def main():
    all_people = set()
    for campaign in range(1, 3):
        for episode in Episode.select().where((Episode.text_imported == False) & (Episode.season == campaign)):
            with open("names.txt", "w") as f:
                f.write("\n".join(sorted(p for p in all_people if "\n" not in p)))
            file = get_filename(campaign, episode.video_number)
            text = file.read_text()
            subtitlelines = parse(text)
            print(episode.video_number, episode.episode_number)
            person = None
            with db.atomic():
                i = 0
                for line in subtitlelines:
                    i += 1
                    assert i == line.index
                    text = unescape(line.content)
                    dbline = Line()
                    if ":" in text:
                        name, resttext = text.split(":", maxsplit=1)
                        if name and name[-1].isupper() and not is_invalid_name(name):
                            people = []
                            name = name.lower()
                            for word in re.split('[,&/]|and| an ', name):
                                word = word.strip()
                                word = fix_typo(word).title()
                                word = word.strip()
                                if word:
                                    people.append(word)
                            all_people.update(people)
                            formatted_name = ", ".join(people)
                            person, created = Person.get_or_create(name=formatted_name, season=campaign)
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
            episode.text_imported = True
            episode.save()


if __name__ == '__main__':
    main()
