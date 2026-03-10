from src.data.playlist import Playlist
from src.data.music import Music
from os import path
import pygame


class AudioManager:
    def __init__(self, music_name=None):
        pygame.mixer.init()
        # Boolean data
        self.is_playing =       False
        self.is_endless_mode =  False
        self.is_random_mode =   False
        self.is_mute =          False
        # Music data
        self.current_music = Music()                                            # Empty instance
        self.current_playlist = None
        # Position
        self.current_position = 0
        self.position_offset = 0                                                # ! Use when change time
        self.position_gap = 5                                                   # In seconds
        # Volume data
        self.current_volume = 0.5                                               # Between 0-1
        self.volume_gap = 0.01                                                  # Move by 1%
        # Init function
        music_name = music_name if music_name else path.join("assets", "musics", "test.mp3")  # Default music
        self.load_music(music_name)

    def get_position(self):                                                     # In ms
        if not self.is_loaded(): return -1
        return pygame.mixer.music.get_pos() / 1000

    def set_position(self, new_pos=0):                                          # In current music
        if not self.is_loaded(): return

        self.position_offset = min(max(0, new_pos), self.current_music.duration)
        self.current_position = self.position_offset

        if not pygame.mixer.music.get_busy():
            self.play()
        pygame.mixer.music.play(-1 if self.is_endless_mode else 0, self.current_position)

        if not self.is_playing:
            self.pause()

    def set_percent(self, percent: float):                                      # Off current music
        if not self.is_loaded(): return
        percent = min(max(0, percent), 1)
        self.set_position(int(self.current_music.duration * percent))

    def is_loaded(self):
        return self.current_music.path

    def is_finish(self):
        return self.current_position >= self.current_music.duration or not pygame.mixer.music.get_busy()

    def move_forward(self):
        if not self.is_loaded(): return
        pos = min(self.current_position + self.position_gap, self.current_music.duration)
        self.set_position(pos)

    def move_backward(self):
        pos = max(0, self.current_position - self.position_gap)
        self.set_position(pos)

    def set_playlist(self, playlist: Playlist):
        self.current_playlist = playlist

    def set_volume(self, new_volume):
        self.current_volume = min(max(new_volume, 0), 1)
        pygame.mixer.music.set_volume(self.current_volume)

    def increase_volume(self):
        self.set_volume(self.current_volume + self.volume_gap)

    def decrease_volume(self):
        self.set_volume(self.current_volume - self.volume_gap)

    def print_music_data(self):
        self.current_music.print_data()

    def load_music(self, path_name):
        try:
            self.unload_music()
            self.current_music = Music(path_name)
            pygame.mixer.music.load(path_name)
        except Exception as e:
            print(f"[AudioManager] Error while loading file '{path_name}' : {e}")   # L Save errors as log

    def unload_music(self):
        self.current_music.unload_music()
        pygame.mixer.music.unload()

    def update(self):
        if self.is_loaded():
            self.current_position = self.get_position() + self.position_offset
            self.current_position = min(max(0, self.current_position), self.current_music.duration)

    def play(self):
        if self.is_loaded():
            self.current_position = 0
            self.position_offset = 0
            pygame.mixer.music.play(-1 if self.is_endless_mode else 0)
            self.is_playing = True

    def pause(self):
        if self.is_loaded():
            pygame.mixer.music.pause()
            self.is_playing = False

    def resume(self):
        if self.is_loaded():
            pygame.mixer.music.unpause()
            self.is_playing = True

    def rewind(self):
        self.set_position(0)
        self.load_music(self.current_music.path)
        self.play()

    def next_music(self):
        if self.is_endless_mode:                                                # Reload music
            self.rewind()
        elif self.current_playlist:
            pygame.time.wait(1000)                                              # Wait a second between musics
            self.current_playlist.choose_next_music(self.is_random_mode)
            self.load_music(self.current_playlist.get_current_music())
            self.play()

    def change_endless_mode(self):
        self.is_endless_mode = not self.is_endless_mode

    def change_random_mode(self):
        self.is_random_mode = not self.is_random_mode

    def change_mute_mode(self):
        self.is_mute = not self.is_mute
        if self.is_loaded():
            pygame.mixer.music.set_volume(0 if self.is_mute else self.current_volume)   # Don't modify current volume
