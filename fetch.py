import hashlib
import os
from datetime import datetime
from shutil import move
from subprocess import run

import youtube_dl
from peewee import DoesNotExist

from data import series_data
from models import Episode, Series, Line, Phrase
from utils import srtdir, pretty_title, title_to_episodenumber


def main() -> None:
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
        s.save()
        ydl_opts = {
            'extract_flat': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            playlist = ydl.extract_info("https://www.youtube.com/playlist?list=" + playlist_id, download=False)
            videos = playlist["entries"]

        print(v["url"] for v in videos)

        ydl_opts_download = {
            "writesubtitles": True,
            "subtitleslangs": ["en", "en-US"],
            "skip_download": True,
        }

        for nr, video in enumerate(videos, 1):
            try:
                e = Episode.select().where((Episode.series == s) & (Episode.video_number == nr)).get()
                # if (e.series.id == 1) or (e.series.id == 2 and e.video_number < 90):
                #     continue
                # if e.downloaded:
                #     continue
            except DoesNotExist:
                e = Episode()
                e.series = s
                e.video_number = nr
            e.title = video["title"]
            e.pretty_title = pretty_title(video["title"])
            if s.is_campaign:
                if e.series.id == 1 and "One-Shot" in e.title:
                    continue
                e.episode_number = title_to_episodenumber(e.title, e.video_number)
            else:
                e.episode_number = e.video_number
            e.youtube_id = video["url"]
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
            except FileNotFoundError:
                e.downloaded = False
            e.save()


if __name__ == '__main__':
    main()
