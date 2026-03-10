from random import choice
# from os import listdir
from glob import glob
from src.data.music import Music                                                     # Local files


# L Save all folders name/path of playlists in json files
class Playlist:
    def __init__(self, path=None):
        self.folder_path = path                                                 # Folder of playlist
        self.current_music_index = None                                         # Last played music in this playlist
        self.Musics = []
        self.Artists = []
        self.set_playlist_path(path)

    def get_playlist_path(self):
        return self.folder_path

    def set_playlist_path(self, new_path):
        self.folder_path = new_path
        self.load_playlist()

    def get_current_music(self):
        return None if len(self.Musics) <= 0 else self.Musics[self.current_music_index]

    def set_music_index(self, new_index):
        if type(new_music_index) == int:
            self.current_music_index = new_index

    def choose_next_music(self, is_random: bool = False):
        self.set_music_index(choice(self.Musics) if is_random else
            (self.current_music_index + 1) % len(self.Musics))

    def load_playlist(self):
        if self.folder_path:
            self.Musics.clear()
            self.Artists.clear()
            for file_path in glob(f"{self.folder_path}/*.mp3"):
                music = Music(file_path)
                if music.artist and music.artist not in self.Artists:
                    self.Artists.append(music.artist)
                self.Musics.append(music)
