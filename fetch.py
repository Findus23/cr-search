import argparse
import hashlib
import os
from datetime import datetime
from pathlib import Path
from shutil import move
from subprocess import run

import requests
import youtube_dl
from peewee import DoesNotExist

from data import series_data
from models import Episode, Series, Line, Phrase
from utils import srtdir, pretty_title, title_to_episodenumber, clear_cache

static_path = Path("static")


def main(args) -> None:
    os.nice(15)
    for series in series_data:
        name = series.name
        playlist_id = series.playlist_id
        is_campaign = "Campaign" in name
        try:
            s = Series.select().where(Series.title == name).get()
        except DoesNotExist:
            s = Series()
            s.title = name

        s.is_campaign = is_campaign
        s.single_speaker = series.single_speaker
        s.slug = series.slug
        s.save()
        ydl_opts = {
            'extract_flat': True
        }
        if series.playlist_id:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                playlist = ydl.extract_info("https://www.youtube.com/playlist?list=" + playlist_id, download=False)
                videos = playlist["entries"]

            urls = [v["url"] for v in videos]
        else:
            urls = series.videos
        ydl_opts_download = {
            "writesubtitles": True,
            "subtitleslangs": ["en", "en-US"],
            "skip_download": True,
        }

        for nr, url in enumerate(urls, 1):
            changed = False
            try:
                e = Episode.select().where((Episode.youtube_id == url)).get()
                if args.skip_existing and e.downloaded:
                    continue
            except DoesNotExist:
                e = Episode()
                e.series = s
                e.video_number = nr
                changed = True
            e.youtube_id = url
            video_info = ydl.extract_info(f'https://www.youtube.com/watch?v={e.youtube_id}', download=False)
            if nr == 1:
                file = static_path / f"{s.slug}.webp"
                if not file.exists():
                    r = requests.get(f"https://i.ytimg.com/vi_webp/{e.youtube_id}/maxresdefault.webp")
                    r.raise_for_status()
                    with file.open("wb")as f:
                        f.write(r.content)
            e.upload_date = datetime.strptime(video_info["upload_date"], "%Y%m%d")
            e.title = video_info["title"]
            e.pretty_title = pretty_title(video_info["title"])
            if s.is_campaign or "Exandria" in e.title:
                if e.series.id == 1 and ("One-Shot" in e.title or "Search For Bob" in e.title):
                    continue
                e.episode_number = title_to_episodenumber(e.title, e.video_number)
            else:
                e.episode_number = e.video_number
            e.save()
            print(e.series.id, e.episode_number, e.pretty_title)

            vttfile = srtdir / str(e.id)
            ydl_opts_download["outtmpl"] = str(vttfile)
            with youtube_dl.YoutubeDL(ydl_opts_download) as ydl:
                ydl.download([f'https://www.youtube.com/watch?v={e.youtube_id}'])
            if vttfile.with_suffix(".en-US.vtt").exists():
                # few videos have en-US as language code instead of en
                move(vttfile.with_suffix(".en-US.vtt"), vttfile.with_suffix(".en.vtt"))
            output = run(
                ["ffmpeg", "-y", "-i", vttfile.with_suffix(".en.vtt"), vttfile.with_suffix(".srt")],
                capture_output=True
            )
            e.downloaded = True
            try:
                vttfile.with_suffix(".en.vtt").unlink()
                with vttfile.with_suffix(".srt").open("rb") as f:
                    file_hash = hashlib.sha256()
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        file_hash.update(chunk)
                if e.subtitle_hash != file_hash.hexdigest():
                    print("subtitle hash changed, deleting imported data")
                    Line.delete().where(Line.episode == e)
                    Phrase.delete().where(Phrase.episode == e)
                    e.phrases_imported = False
                    e.text_imported = False
                    e.subtitle_hash = file_hash.hexdigest()
                    e.last_updated = datetime.now()
                    changed = True
            except FileNotFoundError:
                e.downloaded = False
            e.save()
            if changed:
                clear_cache()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="fetch episode data from YouTube")
    parser.add_argument("--skip-existing", dest="skip_existing", action="store_true",
                        help="don't check for update on existing videos")
    args = parser.parse_args()
    main(args)
