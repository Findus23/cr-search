import os
import re
from html import unescape
from typing import List, Optional, Set

from alive_progress import alive_bar
from peewee import fn, chunked
from srt import parse, Subtitle

from models import Person, Line, Episode, db, Series
from typo import fix_typo
from utils import td_to_milliseconds, srtdir, episode_speaker


def is_invalid_name(name: str) -> bool:
    for substr in ["PS", "P.S.", "\"P.S", "II", "The US", "Metal Gear", "D&amp;D", "LARP", "D&D"]:
        if substr.lower() in name.lower():
            return True
    for string in ["A", "B"]:
        if string.lower() == name.lower():
            return True
    return False


def add_to_text(text: str, add: str) -> str:
    if text:
        return text + " " + add
    return add


def insert_subtitle(text: str, person: Optional[Person], subline: Subtitle, episode: Episode, order: int,
                    isnote: bool = False, ismeta: bool = False) -> Line:
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
    return dbline


def main() -> None:
    os.nice(15)
    all_people: Set[str] = set()
    for series in Series.select().order_by(Series.id):
        for episode in Episode.select().where(
                (Episode.text_imported == False) & (Episode.series == series) & (Episode.downloaded)
        ).order_by(Episode.video_number):
            with open("names.txt", "w") as f:
                f.write("\n".join(sorted(p for p in all_people if "\n" not in p)))
            file = srtdir / f"{episode.id}.srt"
            strtext = file.read_text()
            subtitlelines: List[Subtitle] = list(parse(strtext))
            print(episode.video_number, episode.pretty_title)
            person: Optional[Person] = None
            with db.atomic():
                dblines = []
                i = 0
                text = ""
                for subline in subtitlelines:
                    total_text = unescape(subline.content)
                    if series.single_speaker:
                        person_name = episode_speaker(series.title, episode.video_number)
                        person, created = Person.get_or_create(name=person_name, series=series)
                        dblines.append(insert_subtitle(total_text, person, subline, episode, order=i))
                        i += 1
                        continue

                    if text:
                        dblines.append(insert_subtitle(text, person, subline, episode, order=i))
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
                            dblines.append(insert_subtitle(text, person, subline, episode, order=i))
                            i += 1
                            text = ""

                        if text.startswith("(") and text.endswith(")"):
                            text = add_to_text(text, line)
                            person = None
                            dblines.append(insert_subtitle(text, person, subline, episode, isnote=True, order=i))
                            i += 1
                            text = ""
                            continue

                        if text.startswith("[") and text.endswith("]"):
                            text = add_to_text(text, line)
                            person = None
                            dblines.append(insert_subtitle(text, person, subline, episode, ismeta=True, order=i))
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
                            dblines.append(insert_subtitle(text, person, subline, episode, order=i))
                            text = ""
                            i += 1
                num_per_chunk = 100
                chunks = chunked(dblines, num_per_chunk)
                with alive_bar(len(dblines) // num_per_chunk + 1) as bar:
                    for chunk in chunks:
                        bar()
                        Line.bulk_create(chunk)

                episode.text_imported = True
                episode.save()


if __name__ == '__main__':
    main()
