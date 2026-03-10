from time import sleep, strftime, gmtime
from random import randint, choice
from mutagen.mp3 import MP3
from os import getcwd, path
from pathlib import Path
from glob import glob
import subprocess
import pygame

""" Documentation
creator : One Shot
name : Playlist Runner
year of creation : 2020
version : 2.0.3
language : python
purpose : Music lector made to play musics in a specific directory and with a specific name (optional).
          All arguments are optional, the programm can be run without any argument enter.
arguments : (6)
    - name_music : Default value = None. A part of the artist or the title of a song wanted. The programm will
      then create a playlist with all the file that match the value. The playlist need to be activate for that (next
      argument). If no matching file is found, the programm will just play any random music it find.
    - with_playlist : Default value = False. Ask the programm to create a playlist. If a name of one or several file is
      given, it will fill the playlist based on those.
    - sound_gap : Default value = 0.01. The gap of the sound : 1% each time volume sound button is press.
    - randomly : Default value = True. Make the random mode for playlist lecture : Playlist Runner will choose a music 
      to play randomly.
    - mute : Default value = False. Mute the volume (set it to 0%) if activated.
    - theme : Default value = False. Change the theme of the Playlist Runner : black by default, can be white.
requirements : libraries 'pygame', 'mutagen', 'random', 'time' , 'copy' and 'os'.
"""


class Lecteur:
    def __init__(self, name_music=None, with_playlist=False, sound_gap=0.01,
            randomly=True, is_mute=False, theme=False, oneshot=False):
        pygame.init()                                                           # ! Améliorer fond transparent (HP)
        pygame.mixer.init()
        # Main data
        self.creator = "One Shot"
        self.version = "v2.0.3"
        self.name = "old Playlist Runner"
        print(f"\nBienvenue sur {self.name}.")
        # Boolean data
        self.running = True
        self.musicOn = True
        self.theme0n = theme
        self.endlessOn = not randomly
        self.randomOn = randomly
        self.endAfterOn = oneshot
        self.with_playlist = with_playlist
        self.muteOn = is_mute
        # Gameplay data
        self.path = Path(getcwd()) / "old"                                      # Get actual position of self
        self.path_music = "C:/Musics"
        self.pressed = pygame.key.get_pressed()                                 # Pressed keys
        self.horloge = pygame.time.Clock()                                      # Manage the fps
        # Screen data
        self.height = 500
        self.width = 300
        self.size = [self.height, self.width]
        self.screen = pygame.display.set_mode(self.size)                        # Display window with bg image size
        # Icon data
        pygame.display.set_caption(self.name)                                   # Lector name
        self.icon = pygame.image.load(Path(self.path) / "images" / "icon.jpg")
        self.icon.set_colorkey((255, 255, 255))                                 # Remove white background
        self.icon = pygame.transform.scale(self.icon, (32, 32))
        pygame.display.set_icon(self.icon)                                      # Lector icon
        # Button data
        self.button_bg =            pygame.Surface((0, 0))                      # Background of the lector
        self.button_play =          pygame.Surface((0, 0))                      # Display if the song is running
        self.button_pause =         pygame.Surface((0, 0))                      # Display if the song is paused
        self.button_next =          pygame.Surface((0, 0))                      # Play the next song
        self.button_previous =      pygame.Surface((0, 0))                      # Play the previous song
        self.button_after =         pygame.Surface((0, 0))                      # Move forward in the song
        self.button_before =        pygame.Surface((0, 0))                      # Move backward in the song
        self.button_restart =       pygame.Surface((0, 0))                      # Restart the song from the beginning
        self.button_random =        pygame.Surface((0, 0))                      # Play a random song
        self.button_endless =       pygame.Surface((0, 0))                      # Play the same song endlessly
        self.button_sound_loud =    pygame.Surface((0, 0))                      # Display if the sound is loud (>66)
        self.button_sound_middle =  pygame.Surface((0, 0))                      # Display if the sound is middle (66>x>33)
        self.button_sound_low =     pygame.Surface((0, 0))                      # Display if the sound is low (33>)
        self.button_sound_mute =    pygame.Surface((0, 0))                      # Display if the sound is muted
        self.Exceptions = ["icon"]                                              # Exceptions for the images' name file
        # self.Images = [_ for _ in listdir(f"{self.path}/images") if not _.startswith("anti-") and _.endswith(".jpg")
        #                and _[:-4] not in self.Exceptions]
        self.Images = [f for f in glob(f"{self.path}/images/*.jpg") if not path.basename(f).startswith("anti-")
            and path.basename(f)[:-4] not in self.Exceptions]
        self.Images.sort()
        # self.Anti_Images = [_ for _ in listdir(f"{self.path}/images") if _.startswith("anti-") and _.endswith(".jpg")
        #                     and _[:-4] not in self.Exceptions]
        self.Anti_Images = [f for f in glob(f"{self.path}/images/*.jpg") if path.basename(f).startswith("anti-")
            and path.basename(f)[:-4] not in self.Exceptions]
        self.Anti_Images.sort()
        # Font data
        # self.Fonts = [_ for _ in listdir(f"{self.path}/fonts") if _.endswith(".ttf")]  # Get fonts
        self.Fonts = glob(f"{self.path}/fonts/**/*.ttf", recursive=True)
        self.police = choice(self.Fonts)                                        # Choose random font
        self.title_font =   pygame.font.Font(self.police, 25)                   # Load the different fonts type
        self.default_font = pygame.font.Font(self.police, 20)
        self.artist_font =  pygame.font.Font(self.police, 15)
        # Playlist data
        self.artists = []
        self.current_artist = ""
        self.character_forbidden = ". mp3"                                      # Check if name_music correct
        # self.Song_list = [_ for _ in listdir(f"{self.path_music}") if _.endswith(".mp3")]  # Get mp3 files
        self.Song_list = glob(f"{self.path_music}/*.mp3")
        self.Song_list.sort()
        self.Playlist = []
        self.place = self.set_place(name_music)                                 # Look for asked sons and make the playlist
        self.Playlist.sort()
        self.song_name = self.path_music + f"/{self.Song_list[self.place]}"     # Get full song name
        self.Historic = [self.place]                                            # Use to play previous songs
        # Music data
        self.repeat =   -1 if self.endlessOn else 0                             # Manage l'endless mode
        self.sound =     0 if self.muteOn else 0.5                              # Manage sound volume (% / 100)
        self.old_sound = 0 if self.muteOn else 0.5                              # Save previous volume (for mute)
        self.sound_gap = sound_gap                                              # Sound gap (used in set_volume)
        self.timelapse = 10                                                     # Time gap (used in set_position_in_music)
        self.current_time = 0                                                   # Current time since the song start (in sec)
        self.music_offset = 0                                                   # Manage movements in song duration
        # Color data
        self.color = (240, 240, 240)                                            # Manage theme and font color
        self.message_alpha = 255
        self.Run()

    def Run(self):                      # Letters uses : arrows, A, C, E, H, I, J, K, L, M, O, P, Q, T, W
        nb_zik = len(self.Playlist) if self.with_playlist else len(self.Song_list)
        self.Historic = self.Song_list[self.place] if len(self.Historic) <= 0 else self.Historic
        print(f"Lancement de la musique n°{self.place} / {nb_zik}")
        print(f"Historique ({len(self.Historic)}) : {self.Historic}")
        self.set_theme()
        self.play_song()

        while self.running:
            self.update()
            self.horloge.tick(20)
            self.pressed = pygame.key.get_pressed()

            if self.pressed[pygame.K_c]:
                self.show_commandes()

            if self.pressed[pygame.K_UP]:
                self.set_volume(+ self.sound_gap)
            elif self.pressed[pygame.K_DOWN]:
                self.set_volume(- self.sound_gap)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_lector()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.pause()

                    if event.key == pygame.K_RETURN:
                        self.next_song(1)

                    if event.key == pygame.K_LEFT:
                        self.set_position(- self.timelapse)
                    elif event.key == pygame.K_RIGHT:
                        self.set_position(+ self.timelapse)

                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        self.set_position(percent=0)
                    elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        self.set_position(percent=0.1)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        self.set_position(percent=0.2)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        self.set_position(percent=0.3)
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        self.set_position(percent=0.4)
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        self.set_position(percent=0.5)
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        self.set_position(percent=0.6)
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        self.set_position(percent=0.7)
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        self.set_position(percent=0.8)
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        self.set_position(percent=0.9)

                    if event.key == pygame.K_a:
                        self.show_artists()

                    if event.key == pygame.K_e:
                        self.change_end_after()

                    if event.key == pygame.K_h:
                        self.rewind()

                    if event.key == pygame.K_i:
                        self.random_mode()

                    if event.key == pygame.K_j:
                        self.next_song(-1)
                    elif event.key == pygame.K_l:
                        self.next_song(1)

                    if event.key == pygame.K_k:
                        self.pause()

                    if event.key == pygame.K_m:
                        self.mute_mode()

                    if event.key == pygame.K_o:
                        self.endless_mode()

                    if event.key == pygame.K_p:
                        self.with_playlist = not self.with_playlist

                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.close_lector()

                    if event.key == pygame.K_t:
                        self.set_theme()

                    if event.key == pygame.K_w:
                        self.switch_to_new_version()

    def set_place(self, name_music=None):                                       # Check if music ask exist
        if name_music:                                                          # If specific name requested
            Characters = self.character_forbidden.split()
            for char in Characters:                                             # Remove forbidden characters
                name_music = name_music.replace(char, "")

            if self.with_playlist and len(name_music) > 1:                      # If using playlist (and name_music ok)
                Name_musics = name_music.split()
                for index, _ in enumerate(Name_musics):
                    for song in self.Song_list:
                        if not Name_musics[index].startswith("-"):              # If requested
                            if Name_musics[index].lower() in song.lower() and song not in self.Playlist:
                                self.Playlist.append(song)
                        else:                                                   # If not requested (start with "-")
                            if Name_musics[index][1:].lower() not in song.lower() and song not in self.Playlist:
                                self.Playlist.append(song)

                if len(self.Playlist) <= 0:                                     # If no music found
                    message = f"No song found with title or artist "
                    for name in Name_musics:
                        message += f"or '{name}'" if name == Name_musics[-1] else f"'{name}', "
                    message += " !"
                    print(message)
                    place = randint(0, len(self.Song_list) - 1) if self.randomOn else 0  # Choice random music
                    self.with_playlist = False
                elif len(self.Playlist) == 1:
                    place = self.Song_list.index(self.Playlist[0])
                    print(f"Unique song found : '{self.Song_list[place][:-4]}'")
                    print(f"Activation of endless mode...")
                    print(f"Canceling playlist usage...")
                    self.endlessOn = True
                    self.randomOn = False
                    self.with_playlist = False
                else:                                                           # If more than one music found
                    print(f"Playlist created ! ({len(self.Playlist)} songs added)")
                    place = randint(0, len(self.Playlist) - 1) if self.randomOn else 0
            else:                                                               # If no playlist asked
                Musics = []
                for song in self.Song_list:                                     # Add founded music
                    if name_music.lower() in song.lower():
                        Musics.append(song)

                if len(Musics) <= 0:
                    print(f"No song found with title or artist '{name_music}' !")
                    place = randint(0, len(self.Song_list) - 1) if self.randomOn else 0
                elif len(Musics) == 1:
                    place = Musics[0]
                    print(f"Song found : '{self.Song_list[place][:-4]}'")
                else:
                    place = -1
                    print(f"Multiples songs found : ({len(Musics)})")
                    for zik in Musics:
                        print(f"{zik} - '{self.Song_list[zik][:-4]}'")
                    while place not in Musics:
                        place = int(input("What song would you like to listen (index) ? "))
        else:                                                                   # Si pas de requête
            place = randint(0, len(self.Song_list) - 1) if self.randomOn else 0
            self.with_playlist = False

        return place

    def set_theme(self):                                                        # Change theme of lector
        self.theme0n = not self.theme0n

        if self.theme0n:                                                       # Theme obscur (by default)
            anti = False
            color = (0, 0, 0)
            self.color = (240, 240, 240)
        else:                                                                  # Theme clair
            anti = True
            color = (255, 255, 255)
            self.color = (15, 15, 15)

        self.button_bg = pygame.image.load(self.button_modifier('fond', anti))
        self.button_bg = pygame.transform.scale(self.button_bg, (self.height, self.width))
        self.button_play = pygame.image.load(self.button_modifier('play', anti))
        self.button_play.set_colorkey(color)
        self.button_play = pygame.transform.scale(self.button_play, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_pause = pygame.image.load(self.button_modifier('pause', anti))
        self.button_pause.set_colorkey(color)
        self.button_pause = pygame.transform.scale(self.button_pause, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_next = pygame.image.load(self.button_modifier('suivant', anti))
        self.button_next.set_colorkey(color)
        self.button_next = pygame.transform.scale(self.button_next, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_previous = pygame.image.load(self.button_modifier('precedent', anti))
        self.button_previous.set_colorkey(color)
        self.button_previous = pygame.transform.scale(self.button_previous, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_after = pygame.image.load(self.button_modifier('after', anti))
        self.button_after.set_colorkey(color)
        self.button_after = pygame.transform.scale(self.button_after, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_before = pygame.image.load(self.button_modifier('before', anti))
        self.button_before.set_colorkey(color)
        self.button_before = pygame.transform.scale(self.button_before, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_restart = pygame.image.load(self.button_modifier('restart', anti))
        self.button_restart.set_colorkey(color)
        self.button_restart = pygame.transform.scale(self.button_restart, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_random = pygame.image.load(self.button_modifier('random', anti))
        self.button_random.set_colorkey(color)
        self.button_random = pygame.transform.scale(self.button_random, (self.size[1] * 0.1, self.size[1] * 0.1))
        self.button_endless = pygame.image.load(self.button_modifier('endless', anti))
        self.button_endless.set_colorkey(color)
        self.button_endless = pygame.transform.scale(self.button_endless, (self.size[1] * 0.1, self.size[1] * 0.1))
        self.button_sound_loud = pygame.image.load(self.button_modifier('sound_loud', anti))
        self.button_sound_loud.set_colorkey(color)
        self.button_sound_loud = pygame.transform.scale(self.button_sound_loud, (self.size[1] * 0.1, self.size[1] * 0.1))
        self.button_sound_middle = pygame.image.load(self.button_modifier('sound_middle', anti))
        self.button_sound_middle.set_colorkey(color)
        self.button_sound_middle = pygame.transform.scale(self.button_sound_middle, (self.size[1] * 0.1, self.size[1] * 0.1))
        self.button_sound_low = pygame.image.load(self.button_modifier('sound_low', anti))
        self.button_sound_low.set_colorkey(color)
        self.button_sound_low = pygame.transform.scale(self.button_sound_low, (self.size[1] * 0.1, self.size[1] * 0.1))
        self.button_sound_mute = pygame.image.load(self.button_modifier('sound_mute', anti))
        self.button_sound_mute.set_colorkey(color)
        self.button_sound_mute = pygame.transform.scale(self.button_sound_mute, (self.size[1] * 0.1, self.size[1] * 0.1))

    def play_song(self):
        self.current_time = 0
        self.music_offset = 0
        name_list = self.Playlist if self.with_playlist else self.Song_list
        self.song_name = name_list[self.place]
        pygame.mixer.music.load(self.song_name)                                # Erase last loaded file !
        pygame.mixer.music.play(self.repeat)                                   # Play endlessly : -1 ; Play once : 0

        if not self.musicOn:
            self.pause()

    def update(self):
        self.screen.blit(self.button_bg, (0, 0))
        pygame.mixer.music.set_volume(self.sound)

        self.current_time = pygame.mixer.music.get_pos() / 1000 + self.music_offset # Current position in music (in seconds)
        song_mutagen = MP3(self.song_name)                                      # Load file
        duration = song_mutagen.info.length                                     # Get music duration (in seconds)
        self.current_time = min(max(0, self.current_time), duration)

        time_format = '%H:%M:%S' if duration >= 3600 else '%M:%S'               # If music longer than 1h
        current_time_format = strftime(time_format, gmtime(self.current_time))
        song_lenght_format = strftime(time_format, gmtime(duration))

        current_song_time = self.default_font.render(f"{current_time_format}", True, self.color)
        current_song_time_size = current_song_time.get_size()
        self.screen.blit(current_song_time, (self.size[0] * 0.1 - current_song_time_size[0] * 0.5,
                                             self.size[1] * 0.9))               # Current position text
        pygame.draw.rect(self.screen, self.color, [int(self.size[0] * 0.2), int(self.size[1] * 0.9),
            int(self.size[0] * 0.6), int(self.size[1] * 0.05)],
            border_radius=int(self.size[1] * 0.05))                             # Music duration bar (bg)
        pygame.draw.rect(self.screen, (128, 128, 128), [self.size[0] * 0.2, self.size[1] * 0.9,
            self.current_time / duration * self.size[0] * 0.6, self.size[1] * 0.05],
            border_radius=int(self.size[1] * 0.05))                             # Current position in music bar
        current_song_lenght = self.default_font.render(f"{song_lenght_format}", True, self.color)
        current_song_lenght_size = current_song_lenght.get_size()
        self.screen.blit(current_song_lenght, (self.size[0] * 0.9 - current_song_lenght_size[0] * 0.5,
                                               self.size[1] * 0.9))             # Music duration text

        if self.current_time >= duration:                                       # if music end, play next one
            pygame.time.delay(1000)                                             # Wait a second !
            self.next_song(1)

        play_size = self.button_play.get_size()
        self.screen.blit(self.button_next, (self.size[0] * 0.7 - play_size[0] * 0.5, self.size[1] * 0.7))
        self.screen.blit(self.button_after, (self.size[0] * 0.6 - play_size[0] * 0.5, self.size[1] * 0.7))
        if self.musicOn:                                                        # Display Play/Pause image
            self.screen.blit(self.button_play, (self.size[0] * 0.5 - play_size[0] * 0.5, self.size[1] * 0.7))
        else:
            self.screen.blit(self.button_pause, (self.size[0] * 0.5 - play_size[0] * 0.5, self.size[1] * 0.7))
        self.screen.blit(self.button_before, (self.size[0] * 0.4 - play_size[0] * 0.5, self.size[1] * 0.7))
        self.screen.blit(self.button_previous, (self.size[0] * 0.3 - play_size[0] * 0.5, self.size[1] * 0.7))
        self.screen.blit(self.button_restart, (self.size[0] * 0.2 - play_size[0] * 0.5, self.size[1] * 0.7))

        if self.randomOn:                                                       # Manage random button
            self.screen.blit(self.button_random, (self.size[0] * 0.05, self.size[1] * 0.05))

        if self.endlessOn:                                                      # Manage endless button
            self.screen.blit(self.button_endless, (self.size[0] * 0.15, self.size[1] * 0.05))

        sound_max = self.size[1] * 0.7 - self.sound * self.size[1] * 0.4        # Display icon based on volume
        if self.muteOn or self.sound == 0:
            sound_image = self.button_sound_mute
        elif self.sound >= 0.66:
            sound_image = self.button_sound_loud
        elif 0.66 > self.sound > 0.33:
            sound_image = self.button_sound_middle
        else:
            sound_image = self.button_sound_low
        size = sound_image.get_size()
        self.screen.blit(sound_image, (self.size[0] * 0.82, sound_max - size[1] * 0.5))
        current_sound = self.default_font.render(f"{int(self.sound * 100)}", True, self.color)
        current_sound_size = current_sound.get_size()
        self.screen.blit(current_sound, (self.size[0] * 0.90, sound_max - current_sound_size[1] * 0.5))

        commande = self.default_font.render(f"C : Commands", True, self.color)
        commande_size = commande.get_size()
        self.screen.blit(commande, (int(self.size[0] * 0.5 - commande_size[0] * 0.5), int(self.size[1] * 0.0)))

        song_name = path.basename(self.song_name)                               # Remove path
        song_name, _ = path.splitext(song_name)                                 # Remove format

        parts = song_name.split(" - ", 1)
        if len(parts) == 2:
            title, artist = parts
        else:
            title = song_name.capitalize()
            artist = ""

        title = self.title_font.render(f"{title}", True, self.color)
        music_size = title.get_size()
        self.screen.blit(title, (int(self.size[0] * 0.5 - music_size[0] * 0.5), int(self.size[1] * 0.35)))
        artist = self.title_font.render(f"{artist}", True, self.color)
        artist_size = artist.get_size()
        self.screen.blit(artist, (int(self.size[0] * 0.5 - artist_size[0] * 0.5), int(self.size[1] * 0.5)))

        if not pygame.mixer.music.get_busy() and self.musicOn:                 # If music stop but isn't paused...
            self.next_song(1)                                                  # ... launch next music

        pygame.display.flip()

    def write_message(self, content, position_x=0.5, position_y=0.1, duration=1):
        self.message_alpha = 0
        alpha_max = duration * 1000

        while self.message_alpha < alpha_max:
            message = self.default_font.render(f"{content}", True, self.color)
            message.set_alpha(self.message_alpha)
            message_size = message.get_size()
            self.screen.blit(message, (int(self.size[0] * position_x - message_size[0] * 0.5), int(self.size[1] * position_y)))
            self.message_alpha += 1

            pygame.display.flip()
            # self.update()                                                    # ! Pb with Lector (redundancies)
            # sleep(0.01)                                                      # Quick pause

        del message

    def show_commandes(self):                                                   # Display commands (? use commandes())
        sound_max = self.size[1] * 0.7 - self.sound * self.size[1] * 0.4        # Manage messages around sound

        artist = self.default_font.render(f"A : Artists", True, self.color)
        artist_size = artist.get_size()
        self.screen.blit(artist, (int(self.size[0] * 0.5 - artist_size[0] * 0.5), int(self.size[1] * 0.2)))
        debut = self.default_font.render(f"H", True, self.color)
        debut_size = debut.get_size()
        self.screen.blit(debut, (int(self.size[0] * 0.2 - debut_size[0] * 0.5), int(self.size[1] * 0.65)))
        aleatoire = self.default_font.render(f"I", True, self.color)
        self.screen.blit(aleatoire, (int(self.size[0] * 0.07), int(self.size[1] * 0.0)))
        precedent_text = self.default_font.render(f"J", True, self.color)
        precedent_size = precedent_text.get_size()
        self.screen.blit(precedent_text, (int(self.size[0] * 0.3 - precedent_size[0] * 0.5), int(self.size[1] * 0.65)))
        avant = self.default_font.render(f"<-", True, self.color)
        avant_size = avant.get_size()
        self.screen.blit(avant, (int(self.size[0] * 0.4 - avant_size[0] * 0.5), int(self.size[1] * 0.65)))
        pause_text = self.default_font.render(f"K", True, self.color)
        pause_size = pause_text.get_size()
        self.screen.blit(pause_text, (int(self.size[0] * 0.5 - pause_size[0] * 0.5), int(self.size[1] * 0.65)))
        apres = self.default_font.render(f"->", True, self.color)
        apres_size = apres.get_size()
        self.screen.blit(apres, (int(self.size[0] * 0.6 - apres_size[0] * 0.5), int(self.size[1] * 0.65)))
        suivant_text = self.default_font.render(f"L", True, self.color)
        suivant_size = suivant_text.get_size()
        self.screen.blit(suivant_text, (int(self.size[0] * 0.7 - suivant_size[0] * 0.5), int(self.size[1] * 0.65)))
        muet = self.default_font.render(f"M", True, self.color)
        muet_size = muet.get_size()
        self.screen.blit(muet, (int(self.size[0] - muet_size[0] * 1.1), int(sound_max - muet_size[1] * 0.5)))
        infini = self.default_font.render(f"O", True, self.color)
        self.screen.blit(infini, (int(self.size[0] * 0.17), int(self.size[1] * 0.0)))
        monter = self.default_font.render(f"Up", True, self.color)
        monter_size = monter.get_size()
        self.screen.blit(monter, (int(self.size[0] * 0.9 - monter_size[0] * 0.5), int(sound_max - monter_size[1] * 1.6)))
        baisser = self.default_font.render(f"Down", True, self.color)
        baisser_size = baisser.get_size()
        self.screen.blit(baisser, (int(self.size[0] * 0.9 - baisser_size[0] * 0.5), int(sound_max + baisser_size[1] * 0.6)))
        theme = self.default_font.render(f"T : Theme", True, self.color)
        theme_size = theme.get_size()
        self.screen.blit(theme, (int(self.size[0] * 0.5 - theme_size[0] * 0.5), int(self.size[1] * 0.1)))
        quitter = self.default_font.render(f"Q", True, self.color)
        quitter_size = quitter.get_size()
        self.screen.blit(quitter, (int(self.size[0] * 0.97 - quitter_size[0]), int(self.size[1] * 0.0)))
        older = self.default_font.render(f"W", True, self.color)
        older_size = older.get_size()
        self.screen.blit(older, (int(self.size[0] * 0.1 - older_size[0]), int(self.size[1] * 0.8)))

        pygame.display.flip()
        sleep(1)

    def button_modifier(self, image_name, anti=False):
        if not image_name.endswith(".jpg"):
            image_name += ".jpg"

        if anti:
            image_name = "anti-" + image_name
            for path in self.Anti_Images:
                if image_name in path:
                    return str(path)
        else:
            for path in self.Images:
                if image_name in path:
                    return str(path)

        return Path(self.path) / "images" / "icon.jpg"

    def get_artists(self):
        self.artists = []

        name_list = self.Playlist if self.with_playlist else self.Song_list
        for song in name_list:
            artist = {"artist": "", "musics": []}

            name = song[:-4] if song.endswith(".mp3") else song                 # Find title and artist
            parts = name.split(" - ", 1)
            artist["artist"] = parts[1] if len(parts) > 1 else ""
            title = parts[0]
            artist["musics"].append(title)

            for group in self.artists:                                          # Update artists list
                if artist["artist"] in group["artist"]:
                    group["musics"].append(title)
                    break
            else:
                self.artists.append(artist)
        self.artists.sort(key=lambda x: x["artist"])

    def show_artists(self):
        if not self.artists:                                                   # if list not initiated
            self.get_artists()

        titre = None
        titre_size = None
        position = 0
        while position < len(self.artists) - 1:                                # Display elements by list of 10
            titre = self.artist_font.render(f"Artists : ({len(self.artists)})", True, self.color)
            titre_size = titre.get_size()
            self.screen.blit(titre, (int(self.size[0] * 0.2 - titre_size[0] * 0.5), int(self.size[1] * 0.2)))

            for i in range(10):
                try:
                    element = self.artist_font.render(
                        f"{self.artists[position]['artist']} (x{len(self.artists[position]['musics'])})",
                        True, self.color)
                    element_size = element.get_size()
                    self.screen.blit(element, (int(self.size[0] * 0.2 - element_size[0] * 0.5),
                                               int(self.size[1] * 0.25 + element_size[1] * 0.75 * i)))
                except IndexError:
                    break

                position += 1
                pygame.display.update()
                sleep(0.2)
                del element, element_size

            sleep(3)
            self.update()
        if titre is not None and titre_size is not None:
            del titre, titre_size

    def get_song_list(self):
        print("Musics : ")
        for song in self.Song_list:
            print(f"- {song}")
            sleep(0.1)

    def get_playlist(self):
        print("Playlist : ")
        for song in self.Playlist:
            print(f"- {song}")
            sleep(0.1)

    def endless_mode(self):
        self.endlessOn = not self.endlessOn

        if self.endlessOn:
            self.write_message("Endless mode activated")
            self.repeat = - 1
            # pygame.mixer.music.queue(self.song_name)                          # Load current music ?
            if self.randomOn:
                self.random_mode()
        else:
            self.write_message("Endless mode desactivated")
            self.repeat = 0

    def set_volume(self, gap: float):
        if self.muteOn: self.mute_mode()

        self.sound = min(max(0, round((self.sound + gap) * 100) / 100), 1)

        self.old_sound = self.sound

    def set_position(self, timelapse=0, percent=None):
        song_mutagen = MP3(self.song_name)
        duration = song_mutagen.info.length                                     # In seconds

        if percent is not None:
            self.music_offset = duration * percent
        else:
            self.music_offset = self.current_time + timelapse
        self.current_time = self.music_offset                                    # Time played in music (in seconds)

        if self.current_time < 0:
            self.current_time = 0
        elif self.current_time > duration:
            self.current_time = duration
        pygame.mixer.music.play(self.repeat, self.current_time)                 # play(repeat, start: en secs)

        if not self.musicOn:                                                    # Unpause after offset
            self.pause()

    def change_end_after(self):
        self.endAfterOn = not self.endAfterOn
        self.write_message("Closing after song" if self.endAfterOn else "Running after song")

    def next_song(self, direction=0):
        if self.endAfterOn:
            self.close_lector()
        else:
            name_list = self.Playlist if self.with_playlist else self.Song_list
            if self.endlessOn:
                pass
            elif self.randomOn:
                if direction < 0:
                    self.write_message("Previous")
                    place = -1 if len(self.Historic) < 2 else -2
                    self.place = self.Historic[place]
                elif direction > 0:
                    self.write_message("Next")
                    self.place = randint(0, len(name_list) - 1)
                    if len(self.Historic) >= len(name_list):                    # If played all musics
                        self.Historic = []
                    while self.place in self.Historic:                          # Prevent from replaying same musics
                        self.place = randint(0, len(name_list) - 1)
                    self.Historic.append(self.place)                            # Save music's index
            else:
                if direction < 0:
                    self.write_message("Previous")
                    self.place -= 1
                    if self.place < 0:
                        self.place = len(name_list) - 1
                    self.Historic.append(self.place)
                elif direction > 0:
                    self.write_message("Next")
                    self.place += 1
                    if self.place > len(name_list) - 1:
                        self.place = 0
                    self.Historic.append(self.place)                            # Save music's index
            if len(self.Historic) > 100:                                        # Remove first element if list too long
                self.Historic.pop(0)
            print(f"Historic ({len(self.Historic)}) : {self.Historic}")

            self.play_song()

    def pause(self):
        self.musicOn = not self.musicOn

        if self.musicOn:                                                        # Resume music where it stopped
            self.write_message("Play")
            pygame.mixer.music.unpause()
        else:                                                                   # Pause current music
            self.write_message("Pause")
            pygame.mixer.music.pause()

    def mute_mode(self):
        self.muteOn = not self.muteOn

        if self.muteOn:
            self.write_message("Mute mode activated")
            self.sound = 0
        else:
            self.write_message("Mute mode desactivated")
            self.sound = self.old_sound

    def random_mode(self):
        self.randomOn = not self.randomOn

        if self.randomOn:
            self.write_message("Random mode activated")
            if self.endlessOn:
                self.endless_mode()
        else:
            self.write_message("Random mode desactivated")

    def rewind(self):                                                           # Replay music from start (without interruption)
        self.write_message("Rewind")
        self.play_song()

    def switch_to_new_version(self):                                            # Launch new version
        self.close_lector()
        subprocess.run(["python", "main.py"])
        quit()

    def close_lector(self):                                                     # Properly close old Playlist Runner
        self.write_message(f"Closing {self.name}")
        self.running = False
        pygame.mixer.quit()
        pygame.quit()

if __name__ == "__main__":
    lecteur = Lecteur(name_music="", with_playlist=True, is_mute=False, oneshot=False)

"""           Format          """
# ogg : compressed
# wav : quality
# mp3 : read by music (but not by mixer)
