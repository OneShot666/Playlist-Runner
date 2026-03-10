from mutagen.id3 import TIT2, TPE1, TALB, TCOM, TCON, TIT1, TDRC, TIT3          # To change music files metadata
from mutagen.mp3 import MP3                                                     # For music files metadata
from pathlib import Path


class Music:
    def __init__(self, music_name=None):
        self.meta =     None
        self.path =     None
        self.title =    None
        self.artist =   None
        self.album =    None
        self.composer = None
        self.style =    None
        self.category = None
        self.subtitle = None
        self.year =     None
        self.tempo =    None
        self.format =   None
        self.duration = 0
        # Init function
        self.load_music(music_name)

    def set_title(self, new_title):
        if self.meta:
            self.meta.tags["TIT2"] = TIT2(encoding=3, text=new_title)           # '3': UTF-8
            self.meta.save()

    def set_artist(self, new_artist):
        if self.meta:
            self.meta.tags["TPE1"] = TPE1(encoding=3, text=new_artist)          # '3': UTF-8
            self.meta.save()

    def set_album(self, new_album):
        if self.meta:
            self.meta.tags["TALB"] = TALB(encoding=3, text=new_album)           # '3': UTF-8
            self.meta.save()

    def set_composer(self, new_composer):
        if self.meta:
            self.meta.tags["TCOM"] = TCOM(encoding=3, text=new_composer)        # '3': UTF-8
            self.meta.save()

    def set_style(self, new_style):
        if self.meta:
            self.meta.tags["TCON"] = TCON(encoding=3, text=new_style)           # '3': UTF-8
            self.meta.save()

    def set_category(self, new_category):
        if self.meta:
            self.meta.tags["TIT1"] = TIT1(encoding=3, text=new_category)        # '3': UTF-8
            self.meta.save()

    def set_recorder_year(self, new_year):
        if self.meta:
            self.meta.tags["TDRC"] = TDRC(encoding=3, text=new_year)            # '3': UTF-8
            self.meta.save()

    def set_subtitle(self, new_subtitle):
        if self.meta:
            self.meta.tags["TIT3"] = TIT3(encoding=3, text=new_subtitle)        # '3': UTF-8
            self.meta.save()

    def get_duration_text(self, duration=None):
        duration = duration if duration else self.duration
        h, m = divmod(duration, 3600)
        m, s = divmod(m, 60)
        h, m, s = int(h), int(m), int(s)
        return f"{h}h {m}m {s}s" if h else f"{m}m {s}s" if m else f"{s}s"

    def get_pseudo_title(self):
        if self.path:
            return Path(self.path).stem.split(" - ")[0].strip()
        return "[no title]"

    def get_pseudo_artist(self):
        if self.path:
            artist = Path(self.path).stem.split(" - ")[-1].strip()
            if artist != self.get_pseudo_title(): return artist
        return "[no artist]"

    def is_finish(self):
        return self.get_position() >= self.duration

    def print_data(self):                                                       # ? Make it getters
        if self.meta:
            print(f"{f"'{self.title}'" if self.title else "A music"} by "
                  f"{self.artist if self.artist else "no one important"}")
            if self.album: print(f"Album : {self.album}")
            if self.composer: print(f"Composed by : {self.composer}")
            if self.style or self.category: print(f"Style : {f"{self.style} and {self.category}" 
                if self.style and self.category else self.style if self.style else self.category}" +
                f" [{self.subtitle}]" if self.subtitle else "")
            if self.year: print(f"Year : {self.year}")
            if self.tempo: print(f"Average tempo : {self.tempo} bpm")
            print(f"Duration : {self.get_duration_text()}")
        else:
            print("No music loaded")

    def load_music(self, path_name):
        if path_name is None: return None
        try:
            self.path = path_name
            self.meta = MP3(path_name)
            self.title =    self.meta.tags.get("TIT2", self.get_pseudo_title())
            self.artist =   self.meta.tags.get("TPE1", self.get_pseudo_artist())
            self.album =    self.meta.tags.get("TALB", None)
            self.composer = self.meta.tags.get("TCOM", None)
            self.style =    self.meta.tags.get("TCON", None)
            self.category = self.meta.tags.get("TIT1", None)
            self.year =     self.meta.tags.get("TDRC", None)
            self.subtitle = self.meta.tags.get("TIT3", None)
            self.tempo =    self.meta.tags.get("TBPM", None)
            self.format =   self.meta.mime[0].replace("audio/", "")
            self.duration = self.meta.info.length
        except Exception as e:
            self.unload_music()
            print(f"Error while loading file's metadata '{path_name}' : {e}")   # L Write in logs

    def unload_music(self):
        self.__init__()
