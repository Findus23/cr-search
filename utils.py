from datetime import timedelta
from pathlib import Path

srtdir = Path("./data/subtitles/")


def td_to_milliseconds(td: timedelta) -> int:
    return int(td.total_seconds() * 1000)


def milliseconds_to_td(ms: int) -> timedelta:
    return timedelta(milliseconds=ms)


def get_filename(campaign: int, episode: int) -> Path:
    return srtdir / f"C{campaign}E{episode}.srt"
