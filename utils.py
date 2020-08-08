from datetime import timedelta
from pathlib import Path
from typing import Optional

from data import single_speaker

srtdir = Path("./data/subtitles/")


def td_to_milliseconds(td: timedelta) -> int:
    return int(td.total_seconds() * 1000)


def milliseconds_to_td(ms: int) -> timedelta:
    return timedelta(milliseconds=ms)


def episode_speaker(series_title: str, episode: int) -> Optional[str]:
    series = single_speaker[series_title]
    if episode in series:
        return series[episode]
    return None


def pretty_title(title: str) -> str:
    if "|" in title:
        return title.split("|")[0].strip()
    if "Handbooker Helper:" in title:
        return title.replace("Handbooker Helper:", "").strip()
    if "Critical Role RPG Show" in title:
        return title.split("-")[0].strip()
    else:
        return title.strip()
