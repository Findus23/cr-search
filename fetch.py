import re
from subprocess import run

import youtube_dl
from peewee import DoesNotExist

from models import Episode, Series
# https://www.youtube.com/playlist?list=
from utils import srtdir

series_data = [
    {
        "name": "Campaign 1",
        "playlist_id": "PL1tiwbzkOjQz7D0l_eLJGAISVtcL7oRu_",
    },
    {
        "name": "Campaign 2",
        "playlist_id": "PL1tiwbzkOjQxD0jjAE7PsWoaCrs0EkBH2"

    },
    {
        "name": "Handbooker Helper",
        "playlist_id": "PL1tiwbzkOjQyr6-gqJ8r29j_rJkR49uDN",
        "single_speaker": True
    }
]


def main():
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
            "subtitleslangs": ["en"],
            "skip_download": True,
        }
        regex = re.compile(r"Ep(?:is|si)ode (\d+)")

        for nr, video in enumerate(videos, 1):
            # if Episode.select().where((Episode.season == campaign) & (Episode.video_number == nr)).count() == 1:
            #     print(f"already imported {vttfile}")
            #     continue
            try:
                e = Episode.select().where((Episode.series == s) & (Episode.video_number == nr)).get()
            except DoesNotExist:
                e = Episode()
                e.series = s
                e.video_number = nr
            e.title = video["title"]
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
            vttfile = srtdir / str(e.id)
            ydl_opts["outtmpl"] = str(vttfile)
            if e.downloaded:
                continue
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'https://www.youtube.com/watch?v={e.youtube_id}'])
                run(["ffmpeg", "-i", vttfile.with_suffix(".en.vtt"), vttfile.with_suffix(".srt")])
                e.downloaded = True
                try:
                    vttfile.with_suffix(".en.vtt").unlink()
                except FileNotFoundError:
                    e.downloaded = False
                e.save()


if __name__ == '__main__':
    main()
