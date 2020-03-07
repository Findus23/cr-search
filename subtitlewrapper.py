from datetime import timedelta

from pyvtt import WebVTTItem, from_string, WebVTTTime
from srt import Subtitle as SrtSubtitle
from srt import parse


class SubtitleList:
    def __init__(self, text: str, srt: bool):
        self.srt = srt
        self.list = []
        if srt:
            data = parse(text)
            d: SrtSubtitle
            for d in data:
                self.list.append(Subtitle(srt=d))
        else:
            data = from_string(text)
            i = 0
            v: WebVTTItem
            for v in data:
                i += 1
                self.list.append(Subtitle(vtt=v, i=i))

    def __iter__(self):
        yield from self.list


class Subtitle:
    def __init__(self, srt: SrtSubtitle = None, vtt: WebVTTItem = None, i: int = None):
        if srt:
            self.is_srt = True
            self.srt = srt
        else:
            self.is_srt = False
            self.vtt = vtt
            self.i = i

    @staticmethod
    def vtttime_to_td(vt: WebVTTTime) -> timedelta:
        return timedelta(hours=vt.hours, minutes=vt.minutes, seconds=vt.seconds, milliseconds=vt.milliseconds)

    @property
    def content(self) -> str:
        if self.is_srt:
            return self.srt.content
        else:
            return self.vtt.text

    @property
    def index(self) -> int:
        if self.is_srt:
            return self.srt.index
        else:
            return self.i

    @property
    def start(self) -> timedelta:
        if self.is_srt:
            return self.srt.start
        else:
            return self.vtttime_to_td(self.vtt.start)

    @property
    def end(self) -> timedelta:
        if self.is_srt:
            return self.srt.end
        else:
            return self.vtttime_to_td(self.vtt.end)
