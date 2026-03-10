# --- Settings ---
import pygame
import os

# Screen
SCREEN_SIZE = [700, 600]
FPS = 60

# Paths
CURRENT_PATH =  os.getcwd()
ASSETS_DIR =        'assets'
FONTS_DIR =             ASSETS_DIR + '/fonts'
FONT_FILE =                 FONTS_DIR + 'Monitorica/Monitorica.ttf'
FONT_FILE_NAME =            'Monitorica/Monitorica.ttf'
IMAGES_DIR =            ASSETS_DIR + '/images'
IMAGES_GRADIENT_DIR =       IMAGES_DIR + '/gradients'
ICONS_MENU_DIR =            IMAGES_DIR + '/menu'
ICONS_VOLUME_DIR =          IMAGES_DIR + '/volume'
ICON_FILE_NAME =            'icon.png'
MUSICS_DIR =            ASSETS_DIR + '/musics'
TEST_MUSIC_FILE =           MUSICS_DIR + '/test.mp3'

CREDITS_FILE =          ASSETS_DIR + '/credits.txt'

LOGS_DIR =          'logs'

OLD_LECTOR_DIR =    'old'
OLD_LECTOR_FILE =       OLD_LECTOR_DIR + '/old_main.py'

DEFAULT_MUSIC_PATH = "C:\\Users\\\\Documents\\Music"
PERSO_MUSIC_PATH = "C:\\Musics"

# COLORS
ALL_COLORS = pygame.color.THECOLORS

# UI
DEFAULT_FONT_SIZE = 20
ICON_SIZE = 32
