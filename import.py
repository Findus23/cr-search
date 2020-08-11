import os
import re
from html import unescape
from typing import List, Optional

from alive_progress import alive_bar
from peewee import fn
from srt import parse, Subtitle

from models import Person, Line, Episode, db, Series
from typo import fix_typo
from utils import td_to_milliseconds, srtdir, episode_speaker


def is_invalid_name(name: str) -> bool:
    for a in ["PS", "P.S.", "\"P.S", "II", "The US", "Metal Gear", "D&amp;D", "LARP", "D&D", "A", "B"]:
        if a.lower() in name.lower():
            return True
    return False


def add_to_text(text: str, add: str) -> str:
    if text:
        return text + " " + add
    return add


def insert_subtitle(text: str, person: str, subline: Subtitle, episode: Episode, order: int,
                    isnote: bool = False, ismeta: bool = False):
    dbline = Line()
    if not text:
        raise ValueError("empty lines are not allowed")
    text = text.replace("\n", " ")
    dbline.text = text
    dbline.search_text = fn.to_tsvector('english', text)
    dbline.person = person
    dbline.starttime = td_to_milliseconds(subline.start)
    dbline.endtime = td_to_milliseconds(subline.end)
    dbline.episode = episode
    dbline.isnote = isnote
    dbline.ismeta = ismeta
    dbline.order = order
    dbline.save()


def main():
    os.nice(15)
    all_people = set()
    for series in Series.select():
        for episode in Episode.select().where(
                (Episode.text_imported == False) & (Episode.series == series) & (Episode.downloaded)
        ):
            with open("names.txt", "w") as f:
                f.write("\n".join(sorted(p for p in all_people if "\n" not in p)))
            file = srtdir / f"{episode.id}.srt"
            strtext = file.read_text()
            subtitlelines: List[Subtitle] = list(parse(strtext))
            print(episode.video_number, episode.title)
            person: Optional[Person] = None
            with db.atomic():
                with alive_bar(len(subtitlelines)) as bar:
                    i = 0
                    text = ""
                    for subline in subtitlelines:
                        bar()
                        total_text = unescape(subline.content)
                        if series.single_speaker:
                            person_name = episode_speaker(series.title, episode.video_number)
                            person, created = Person.get_or_create(name=person_name, series=series)
                            insert_subtitle(total_text, person, subline, episode, order=i)
                            i += 1
                            continue

                        if text:
                            insert_subtitle(text, person, subline, episode, order=i)
                            i += 1
                            text = ""
                        for line in total_text.split("\n"):
                            if line.startswith("-") or line.startswith(":"):
                                line = line[1:]
                            if ":" not in line:
                                text = add_to_text(text, line)
                                continue
                            name, resttext = line.split(":", maxsplit=1)
                            if is_invalid_name(name) or not name[-1].isupper():
                                text = add_to_text(text, line)
                                continue

                            if text:
                                insert_subtitle(text, person, subline, episode, order=i)
                                i += 1
                                text = ""

                            if text.startswith("(") and text.endswith(")"):
                                text = add_to_text(text, line)
                                person = None
                                insert_subtitle(text, person, subline, episode, isnote=True, order=i)
                                i += 1
                                text = ""
                                continue

                            if text.startswith("[") and text.endswith("]"):
                                text = add_to_text(text, line)
                                person = None
                                insert_subtitle(text, person, subline, episode, ismeta=True, order=i)
                                text = ""
                                i += 1
                                continue

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
                            person, created = Person.get_or_create(name=formatted_name, series=series)
                            text = add_to_text(text, resttext.strip())
                            if text:
                                insert_subtitle(text, person, subline, episode, order=i)
                                text = ""
                                i += 1

            episode.text_imported = True
            episode.save()


if __name__ == '__main__':
    main()
