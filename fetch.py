import re
from subprocess import run

import youtube_dl

from models import Episode
from utils import srtdir

campaign_playlists = {2: "https://www.youtube.com/playlist?list=PL1tiwbzkOjQxD0jjAE7PsWoaCrs0EkBH2"}

campaign = 2
ydl_opts = {
    'extract_flat': True
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])

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
    e = Episode()
    e.season = campaign
    e.video_number = nr
    match = regex.search(video["title"])
    e.episode_number = int(match.group(1))
    e.youtube_id = video["url"]
    e.save()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={e.youtube_id}'])
        run(["ffmpeg", "-i", vttfile.with_suffix(".en.vtt"), vttfile.with_suffix(".srt")])
        vttfile.with_suffix(".en.vtt").unlink()
