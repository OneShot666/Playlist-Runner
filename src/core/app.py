from tkinter import filedialog                                                  # To select folders
from src.core.resource_loader import resources                                  # Local files
from src.ui.menu_manager import MenuManager
from src.theme_manager import ThemeManager
from src.audio_manager import AudioManager
from src.data.playlist import Playlist
from src.ui.painter import Painter
from src.ui.button import Button
from src.data.theme import Theme
from src.ui.label import Label
from src.settings import *
import tkinter as tk
import subprocess
import pygame


# ... Making menu as a sidebar -> require text that disappear gradually
# . Display data once playlist is chosen and loaded
# ! Sidebar for menu (lector, playlists, themes, settings, quit)
# L Add 'Update' button -> reload all musics in a folder
# L Add fade in and out options (in settings.py)
# L Add filter buttons (format of file, length of music, music name, style of music)
# L Can create its own theme
# L Create json files to save themes
# L Create local json save files (personal playlists, personal theme)
# L Can switch to old version -> add button on old version to switch to new
# L Add notification messages on window
# L Add """messages""" under functions (description)
# L Add credits option
# L Make project an app
class PlaylistRunner:
    def __init__(self):
        # Initializers
        pygame.init()
        pygame.mixer.init()
        # Project data
        self.creator =          "One Shot"
        self.project_name =     "Playlist Runner"
        self.date_of_rebirth =  "25/10/2025"
        self.version =          "v0.0.6"
        # Boolean data
        self.is_running =           True
        self.is_show_ui =           True                                        # ! Unused yet
        self.is_design_soundbar =   False                                       # ! Unused yet (make True by default)
        # Path data
        self.current_path =     CURRENT_PATH
        self.image_path =       IMAGES_DIR
        self.fonts_path =       FONTS_DIR
        self.music_path =       MUSICS_DIR
        self.playlist_path =    PERSO_MUSIC_PATH                                # L Check if other path, then check if path exists then load
        self.old_runner =       OLD_LECTOR_FILE
        # Game data
        self.pressed = pygame.key.get_pressed()                                 # Pressed keys
        self.horloge = pygame.time.Clock()                                      # Manage the fps
        self.fps = FPS                                                          # ? Change if playing or pause
        # Screen data
        self.screen = pygame.display.set_mode(SCREEN_SIZE)                      # Create screen
        pygame.display.set_caption(self.project_name)
        # Icon data
        self.icon_size = ICON_SIZE
        self.icon = resources.get_image(ICON_FILE_NAME, "images", [self.icon_size, self.icon_size])
        pygame.display.set_icon(self.icon)
        # Fonts data
        self.fonts_path = FONTS_DIR
        self.font_file =  FONT_FILE                                             # L Allow user to choose font name
        self.font_size =  DEFAULT_FONT_SIZE
        self.title_font = resources.get_font(self.font_file, self.font_size + 20)
        self.text_font =  resources.get_font(self.font_file, self.font_size)
        self.descr_font = resources.get_font(self.font_file, max(self.font_size - 10, 1))
        # Labels data
        self.Labels = []
        self.label_title =      None
        self.label_artist =     None
        self.label_volume =     None
        self.label_position =   None                                            # Position in music
        self.label_duration =   None                                            # Total duration in music
        # Audio Manager
        self.audio_manager =    None
        self.MusicsHistoric = []                                                # ? Move in audio manager
        self.historic_size = 100
        # Playlists data
        self.current_playlist_index = None                                      # L Move in PlaylistManager
        self.current_playlist_path =  None
        self.Playlists = []
        # Menu data
        self.menu_manager =     None
        # Buttons data
        self.button_play = Button()                                             # ? Move in MenuManager()
        # Theme data
        self.theme_manager =    None
        self.font_color = "black"
        self.painter = Painter()
        # Main function
        self.Initializers()
        self.run()

    def Initializers(self):
        # Create menu
        # Load player's data
        # Load playlists
        self.load_managers()
        self.create_texts()
        self.launch_music()                                                     # When program is loaded, play test music

    def load_managers(self):
        self.audio_manager =    AudioManager()
        self.menu_manager =     MenuManager()
        self.theme_manager =    ThemeManager()
        self.font_color = self.theme_manager.get_font_color()

    def create_texts(self):
        music = self.audio_manager.current_music
        self.label_title =  Label(music.title, (0.55, 0.35), color=self.font_color)
        self.Labels.append(self.label_title)
        self.label_artist = Label(music.artist, (0.55, 0.45), color=self.font_color)
        self.Labels.append(self.label_artist)

        volume_pos = [0.98, 0.25, 0.005, 0.33]
        volume = self.audio_manager.current_volume
        height = round((1 - volume) * volume_pos[3], 3)
        self.label_volume = Label(f"{int(volume * 100)}%", (0.95, volume_pos[1] + height), color=self.font_color)
        self.Labels.append(self.label_volume)

        current = music.get_duration_text(self.audio_manager.current_position)  # Pos in music
        self.label_position = Label(current, (0.3, 0.95), color=self.font_color)
        self.Labels.append(self.label_position)
        duration_text = music.get_duration_text()
        self.label_duration = Label(duration_text, (0.8, 0.95), color=self.font_color)
        self.Labels.append(self.label_duration)

    def launch_music(self):
        if self.audio_manager.is_loaded():
            self.audio_manager.change_endless_mode()
            self.audio_manager.play()
            self.MusicsHistoric.append(self.audio_manager.current_music)        # Add current music to historic

    def get_current_theme(self) -> Theme:
        return self.theme_manager.Themes[self.theme_manager.current_theme_index]

    def run(self):
        while self.is_running:
            self.input_manager()

            self.update_manager()                                               # Logic of program

            self.display_manager()

            self.horloge.tick(self.fps)

    def input_manager(self):                                                    # Handle keys input
        self.pressed = pygame.key.get_pressed()

        if self.pressed[pygame.K_UP]:
            self.audio_manager.increase_volume()
        elif self.pressed[pygame.K_DOWN]:
            self.audio_manager.decrease_volume()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_program()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if self.audio_manager.is_playing: self.audio_manager.pause()
                    else: self.audio_manager.resume()

                if event.key == pygame.K_RETURN:
                    self.next_song(1)

                # L Use TAB to enter selection mode (rect around selection)
                # L And ECHAP to exit selection mode

                if event.key == pygame.K_LEFT:
                    self.audio_manager.move_backward()
                elif event.key == pygame.K_RIGHT:
                    self.audio_manager.move_forward()

                if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                    self.audio_manager.set_percent(0)
                elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    self.audio_manager.set_percent(0.1)
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    self.audio_manager.set_percent(0.2)
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    self.audio_manager.set_percent(0.3)
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    self.audio_manager.set_percent(0.4)
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    self.audio_manager.set_percent(0.5)
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    self.audio_manager.set_percent(0.6)
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    self.audio_manager.set_percent(0.7)
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    self.audio_manager.set_percent(0.8)
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    self.audio_manager.set_percent(0.9)

                if event.key == pygame.K_a:
                    self.open_artists_menu()

                if event.key == pygame.K_b:
                    self.select_folder()

                if event.key == pygame.K_e:
                    self.open_profil_menu()

                if event.key == pygame.K_h:
                    self.audio_manager.rewind()

                if event.key == pygame.K_i:
                    self.random_mode()

                if event.key == pygame.K_j:
                    self.next_song(-1)
                elif event.key == pygame.K_l:
                    self.next_song(1)

                if event.key == pygame.K_k:
                    self.audio_manager.pause()

                if event.key == pygame.K_m:
                    self.audio_manager.change_mute_mode()

                if event.key == pygame.K_o:
                    self.audio_manager.change_endless_mode()

                if event.key == pygame.K_p:
                    self.open_playlist_menu()

                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    self.exit_program()
                    quit()

                if event.key == pygame.K_r:
                    self.open_lector_menu()

                if event.key == pygame.K_s:
                    self.open_settings_menu()

                if event.key == pygame.K_t:
                    self.open_theme_menu()
                    self.theme_manager.next_theme()                             # L Use another key (or add button to change theme)

                if event.key == pygame.K_w:
                    self.switch_to_old_version()

    def update_manager(self):
        self.audio_manager.update()
        if self.audio_manager.is_finish():
            self.audio_manager.next_music()

    def display_manager(self):                                                  # ! Make function for each paragraph
        self.screen.fill(self.get_current_theme().background_color)

        self.display_menu_buttons()

        self.display_current_music_info()

        self.display_current_music_bar()

        self.display_volume_bar()

        pygame.display.flip()

    def display_menu_buttons(self):
        self.menu_manager.display_buttons(self.screen)

    def display_current_music_info(self):
        if self.audio_manager.is_loaded():
            self.label_title.draw(self.screen)
            self.label_artist.draw(self.screen)

    def display_current_music_bar(self):
        if self.audio_manager.is_loaded():
            music = self.audio_manager.current_music

            current = music.get_duration_text(self.audio_manager.current_position)  # Pos in music
            self.label_position.set_text(current)
            self.label_position.draw(self.screen)

            duration_text = music.get_duration_text()
            self.label_duration.set_text(duration_text)
            self.label_duration.draw(self.screen)

            music_pos = [0.35, 0.94, 0.4, 0.01]
            self.menu_manager.draw_rectangle(self.screen, self.get_current_theme().button_color, music_pos, 0, 0.5)
            music_pos[2] = round((self.audio_manager.current_position / max(1, music.duration)) * music_pos[2], 3)
            self.menu_manager.draw_rectangle(self.screen, self.get_current_theme().border_color, music_pos, 0, 0.5)

    def display_volume_bar(self):
        volume_pos = [0.98, 0.25, 0.005, 0.33]
        volume = self.audio_manager.current_volume
        height = round((1 - volume) * volume_pos[3], 3)
        self.label_volume.set_text(f"{int(volume * 100)}%")
        self.label_volume.set_position_percent((0.95, volume_pos[1] + height))
        self.label_volume.draw(self.screen)

        self.menu_manager.draw_rectangle(self.screen, self.get_current_theme().border_color, volume_pos, 0, 0.5)
        volume_pos[3] = height
        self.menu_manager.draw_rectangle(self.screen, self.get_current_theme().button_color, volume_pos, 0, 0.5)

    def select_folder(self):
        root = tk.Tk()                                                          # Create tkinter window
        root.withdraw()                                                         # Hide window
        folder = filedialog.askdirectory()                                      # Ask user to select a folder
        root.destroy()                                                          # Close window
        playlist = Playlist(folder)
        self.audio_manager.set_playlist(playlist)

    def next_theme(self):
        self.theme_manager.next_theme()
        self.font_color = self.theme_manager.get_font_color()
        for label in self.Labels:
            label.set_color(self.font_color)

    def open_profil_menu(self):
        self.menu_manager.set_current_menu(0)

    def open_lector_menu(self):
        self.menu_manager.set_current_menu(1)

    def open_artists_menu(self):
        self.menu_manager.set_current_menu(2)

    def open_playlist_menu(self):
        self.menu_manager.set_current_menu(3)

    def open_theme_menu(self):
        self.menu_manager.set_current_menu(4)

    def open_settings_menu(self):
        self.menu_manager.set_current_menu(5)

    def save_data(self):
        pass

    def switch_to_old_version(self):                                            # L Add similar option in old version
        self.exit_program()
        subprocess.run(["python", self.old_runner])                             # Launch old version
        quit()

    def exit_program(self):                                                     # L Add confirm message
        self.save_data()
        # L Stop all musics and running tasks
        self.is_running = False
        pygame.mixer.quit()
        pygame.quit()
