import re
from datetime import timedelta
from pathlib import Path
from typing import Optional

from app import cache
from data import single_speaker

srtdir = Path("./data/subtitles/")


def td_to_milliseconds(td: timedelta) -> int:
    return int(td.total_seconds() * 1000)


def milliseconds_to_td(ms: int) -> timedelta:
    return timedelta(milliseconds=ms)


def episode_speaker(series_title: str, episode: int) -> Optional[str]:
    try:
        series = single_speaker[series_title]
    except KeyError:
        return "?"
    if episode in series:
        return series[episode]
    return None


title_regex = re.compile(r"Ep(?:is|si)ode (\d+)")


def title_to_episodenumber(title: str, video_number: int) -> int:
    print(title)
    try:
        match = title_regex.search(title)
        if not match:
            if "Hit Points for Level 12" in title:
                return 99
            elif "Hit Points for Level 15" in title:
                return 136
            else:
                raise ValueError("No episode number found in title")
        return int(match.group(1))
    except ValueError:
        if title == "Campaign 1":  # one-shots at the end of campaign 1
            return video_number - 3
        elif "Exandria" in title:
            return 1
        else:
            raise


def pretty_title(title: str) -> str:
    if "|" in title:
        return title.split("|")[0].strip()
    if "Handbooker Helper:" in title:
        return title.replace("Handbooker Helper:", "").strip()
    if "Critical Role RPG Show" in title:
        return title.split("-")[0].strip()
    else:
        return title.strip()


def clear_cache() -> None:
    cache.clear()
