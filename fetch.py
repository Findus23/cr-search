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
    ids = [v["url"] for v in playlist["entries"]]

print(ids)

ydl_opts = {
    "writesubtitles": True,
    "subtitleslangs": ["en"],
    "skip_download": True,
}
for nr, id in enumerate(ids, 1):
    vttfile = srtdir / f"C{campaign}E{nr}"
    ydl_opts["outtmpl"] = str(vttfile)
    e = Episode()
    e.season = campaign
    e.episode_number = nr
    e.youtube_id = id
    e.save()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={id}'])
        run(["ffmpeg", "-i", vttfile.with_suffix(".en.vtt"), vttfile.with_suffix(".srt")])
        vttfile.with_suffix(".en.vtt").unlink()
