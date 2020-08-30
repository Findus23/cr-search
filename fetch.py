import hashlib
import os
import re
from datetime import datetime
from shutil import move
from subprocess import run

import youtube_dl
from peewee import DoesNotExist

from data import series_data
from models import Episode, Series, Line, Phrase
from utils import srtdir, pretty_title


def main():
    os.nice(15)
    for series in series_data:
        name = series["name"]
        playlist_id = series["playlist_id"]
        is_campaign = "Campaign" in name
        try:
            s = Series.select().where(Series.title == name).get()
        except DoesNotExist:
            s = Series()
            s.title = name

        s.is_campaign = is_campaign
        s.single_speaker = "single_speaker" in series and series["single_speaker"]
        s.save()
        ydl_opts = {
            'extract_flat': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            playlist = ydl.extract_info("https://www.youtube.com/playlist?list=" + playlist_id, download=False)
            videos = playlist["entries"]

        print(v["url"] for v in videos)

        ydl_opts = {
            "writesubtitles": True,
            "subtitleslangs": ["en", "en-US"],
            "skip_download": True,
        }
        regex = re.compile(r"Ep(?:is|si)ode (\d+)")

        for nr, video in enumerate(videos, 1):
            try:
                e = Episode.select().where((Episode.series == s) & (Episode.video_number == nr)).get()
                # if e.downloaded:
                #     continue
            except DoesNotExist:
                e = Episode()
                e.series = s
                e.video_number = nr
            e.title = video["title"]
            e.pretty_title = pretty_title(video["title"])
            if s.is_campaign:
                try:
                    match = regex.search(video["title"])
                    e.episode_number = int(match.group(1))
                except AttributeError:
                    if s.title == "Campaign 1":  # one-shots at the end of campaign 1
                        e.episode_number = e.video_number - 3
                    else:
                        raise
            else:
                e.episode_number = e.video_number
            e.youtube_id = video["url"]
            e.save()
            print(e.series.id, e.episode_number, e.pretty_title)

            vttfile = srtdir / str(e.id)
            ydl_opts["outtmpl"] = str(vttfile)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'https://www.youtube.com/watch?v={e.youtube_id}'])
            if vttfile.with_suffix(".en-US.vtt").exists():
                # few videos have en-US as language code instead of en
                move(vttfile.with_suffix(".en-US.vtt"), vttfile.with_suffix(".en.vtt"))
            output = run(
                ["ffmpeg", "-y", "-i", vttfile.with_suffix(".en.vtt"), vttfile.with_suffix(".srt")],
                capture_output=True
            )
            if output.returncode:
                raise RuntimeError(output.stderr.decode())
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
            except FileNotFoundError:
                e.downloaded = False
            e.save()


if __name__ == '__main__':
    main()
