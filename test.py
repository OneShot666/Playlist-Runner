# from math import *
from random import *
from time import *
# from copy import *
from os import *
import pygame
# import calendar

# calendar.setfirstweekday(calendar.SUNDAY)
# map & filter
# open (os)
"""   Méthode pour utiliser menu sur fenêtre   """


def use_menu():
    pygame.init()

    window = pygame.display.set_mode((500, 300))
    size = window.get_size()
    background = pygame.Surface(size)
    horloge = pygame.time.Clock()
    font = pygame.font.Font(f"fonts/CutiveMono-Regular.ttf", 20)
    color = (240, 240, 240)
    Playlist = get_playlist()
    run = True

    while run:
        horloge.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.blit(background, (0, 0))

        music = font.render(f"Artistes : ", True, color)
        music_size = music.get_size()
        window.blit(music, (int(size[0] * 0.5 - music_size[0] * 0.5), int(size[1] * 0.15)))

        for artist, song in Playlist:
            music = font.render(f"{artist} : {song}", True, color)
            music_size = music.get_size()
            window.blit(music, (int(size[0] * 0.5 - music_size[0] * 0.5), int(size[1] * 0.15)))

        pygame.display.flip()

    pygame.quit()
    exit()


"""   Méthode pour gestion dynamique images   """


def gerer_image_bouton():
    path1 = getcwd()
    Exceptions = ["icon", "fond", "anti-fond"]
    Images = [_ for _ in listdir(f"{path1}/images") if not _.startswith("anti-") and _.endswith(".jpg")
              and _[:-4] not in Exceptions]
    Anti_Images = [_ for _ in listdir(f"{path1}/images") if _.startswith("anti-") and _.endswith(".jpg")
                   and _[:-4] not in Exceptions]
    Images.sort()
    Anti_Images.sort()

    def modifier_button(nom_button, anti=False):
        new_name = obtenir_nom_variable(nom_button).removeprefix("button_") + ".jpg"
        if anti:
            new_name = "anti-" + new_name
            if new_name in Anti_Images:
                print("anti-image trouvée !")
                return new_name
        else:
            if new_name in Images:
                print("image trouvée !")
                return new_name
        return ""

    def obtenir_nom_variable(var):
        for nom_var, value in globals().items():
            if value is var:
                print("nom obtenu !")
                return nom_var
        return ""

    button_next = ""
    button_next = pygame.image.load(f"images/{modifier_button(button_next)}")
    button_next.set_colorkey((0, 0, 0))
    print(button_next)


"""   Méthode trouver touches enfoncées   """


def get_pressed():
    pygame.init()

    screen = pygame.display.set_mode((500, 300))
    background = pygame.Surface(screen.get_size())
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                print(f"{event.key}")

        screen.blit(background, (0, 0))

        pygame.display.flip()

    pygame.quit()


"""   Méthode mettre artiste + musiques et compter number musiques   """


def get_playlist():
    path2 = getcwd()
    song_list = [_ for _ in listdir(f"{path2}\Musiques") if _.endswith(".mp3")]  # Cherche fichiers musiques
    artists = []

    for song in song_list:
        artist = {"artist": "", "musics": []}
        for i in range(len(song)):
            if song[i] == "-":
                music = song[: i - 1]
                artist["artist"] = song[i + 2: - 4]
                break
        else:
            music = song[: - 4]

        artist["musics"].append(music)

        for group in artists:
            if artist["artist"] in group["artist"]:
                group["musics"].append(music)
                break
        else:
            artists.append(artist)

    artists.sort(key=lambda x: x["artist"])
    Playlist = artists

    return Playlist


"""   Méthode son arrondi à 5   """


def arrondi(arr=5):
    n = randint(0, 100)
    print(f"Ancien : {n}")
    sleep(1)
    print(f"Nouveau : {n - n % arr}\n")
    sleep(1)


"""   Méthode trouver nom artiste   """


def get_artist_name(music):  # Exemple : Gorgone - Blues
    auteur = ""
    for i in range(len(music)):
        if music[i] == "-":
            music_name = music[0:i - 1]
            auteur = music[i + 2:]
            break
    else:
        music_name = music

    return auteur, music_name


"""   Méthode créer message temporaire (en cours...)   """


def Temporary_message():
    pygame.init()

    window = pygame.display.set_mode((500, 300))
    horloge = pygame.time.Clock()
    font = pygame.font.SysFont(None, 150)

    background = pygame.Surface(window.get_size())
    ts, w, h, c1, c2 = 50, *window.get_size(), (128, 128, 128), (64, 64, 64)
    tiles = [((x * ts, y * ts, ts, ts), c1 if (x + y) % 2 == 0 else c2) for x in range((w + ts - 1) // ts) for y in
             range((h + ts - 1) // ts)]
    for rect, color in tiles:
        pygame.draw.rect(background, color, rect)

    transparence = 255 + 200  # max + 2 sec
    run = True

    while run:
        horloge.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        transparence -= 1
        window.blit(background, (0, 0))
        text_surf = font.render(f'Alpha {transparence}', True, (255, 0, 0))
        text_surf.set_alpha(transparence)
        window.blit(text_surf, text_surf.get_rect(center=window.get_rect().center))
        if transparence < 0:
            del text_surf
            run = False

        pygame.display.flip()

    pygame.quit()
    exit()


# gerer_image_bouton()
# get_pressed()
# get_playlist()
# arrondi()
# get_artist_name()
# Temporary_message()
# use_menu()

quit()
