import re
from subprocess import run

import youtube_dl

from models import Episode
from utils import srtdir

campaign_playlists = {
    1: "https://www.youtube.com/playlist?list=PL1tiwbzkOjQz7D0l_eLJGAISVtcL7oRu_",
    2: "https://www.youtube.com/playlist?list=PL1tiwbzkOjQxD0jjAE7PsWoaCrs0EkBH2"
}

skip_download = True


def main():
    for campaign in range(1, 3):
        ydl_opts = {
            'extract_flat': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            playlist = ydl.extract_info(campaign_playlists[campaign], download=False)
            videos = playlist["entries"]

        print(v["url"] for v in videos)

        ydl_opts = {
            "writesubtitles": True,
            "subtitleslangs": ["en"],
            "skip_download": True,
        }
        regex = re.compile(r"Ep(?:is|si)ode (\d+)")

        for nr, video in enumerate(videos, 1):
            vttfile = srtdir / f"C{campaign}E{nr}"
            ydl_opts["outtmpl"] = str(vttfile)
            if Episode.select().where((Episode.season == campaign) & (Episode.video_number == nr)).count() == 1:
                print(f"already imported {vttfile}")
                continue
            e = Episode()
            e.season = campaign
            e.video_number = nr
            try:
                match = regex.search(video["title"])
                e.episode_number = int(match.group(1))
            except AttributeError:
                if campaign == 1:  # one-shots at the end of campaign 1
                    e.episode_number = e.video_number - 3
                else:
                    raise
            e.youtube_id = video["url"]
            e.save()
            if skip_download:
                continue
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'https://www.youtube.com/watch?v={e.youtube_id}'])
                run(["ffmpeg", "-i", vttfile.with_suffix(".en.vtt"), vttfile.with_suffix(".srt")])
                vttfile.with_suffix(".en.vtt").unlink()


if __name__ == '__main__':
    main()
