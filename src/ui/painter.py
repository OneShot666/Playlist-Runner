from PIL import Image
from pathlib import Path
from os import getcwd, path
from src.settings import SCREEN_SIZE
import pygame


class Painter:
    def __init__(self):
        self.save_path = path.join(getcwd(), "assets", "images", "gradients")
        self.ALL_COLORS = pygame.color.THECOLORS
        self.COLORS_NAMES = list(self.ALL_COLORS.keys())
        self.COLORS_VALUES = list(self.ALL_COLORS.values())
        self.Gradients = []
        # Init function
        self.create_gradients()

    def get_color_name(self, color):
        for value in self.COLORS_VALUES:
            if color == value: return value
        return color

    def create_gradient_name(self, color1, color2, name, orientation):
        name1, name2 = None, None

        if type(color1) == str:
            name1 = color1
            color1 = pygame.Color(color1)[:3]
        if type(color2) == str:
            name2 = color2
            color2 = pygame.Color(color2)[:3]

        if name is None:
            name1 = name1 if name1 else self.get_color_name(color1)
            name2 = name2 if name2 else self.get_color_name(color2)
            name = f"gradient_{orientation}_{name1}_to_{name2}.png"
        elif not name.endswith(".png"):
            name += ".png"

        return name, color1, color2

    def create_gradient(self, size, color1, color2, orientation=0, image_name=None):
        size = SCREEN_SIZE if size is None else size
        image_name, color1, color2 = self.create_gradient_name(color1, color2, image_name, orientation)
        image_path = path.join(self.save_path, image_name)

        if not Path(image_path).exists():
            img = Image.new("RGB", size, color1)
            pixels = img.load()

            for x in range(size[0]):
                for y in range(size[1]):
                    if orientation in ["hor", "horizontal", 0, 180]: t = x / (size[0] - 1)
                    elif orientation in ["ver", "vertical", 90, 270]: t = y / (size[1] - 1)
                    else: raise ValueError("Orientation doit être 'horizontal' ou 'vertical'.")

                    r = int(color1[0] + (color2[0] - color1[0]) * t)                # Gradient from color1 to color2
                    g = int(color1[1] + (color2[1] - color1[1]) * t)
                    b = int(color1[2] + (color2[2] - color1[2]) * t)

                    pixels[x, y] = (r, g, b)

            img.save(image_path, "PNG")
            self.Gradients.append(img)

    def create_gradients(self):
        self.create_gradient(None, "white", "black", "horizontal")
        self.create_gradient(None, "red", "yellow", 0)
        self.create_gradient(None, "orchid", "darkorchid", "hor")
        self.create_gradient(None, "crimson", "deeppink", "hor")
        self.create_gradient(None, "coral", "seagreen", "hor")
        self.create_gradient(None, "peachpuff", "lavender", "hor")
        self.create_gradient(None, "darkorange", "purple", "hor")
        self.create_gradient(None, "lime", "royalblue", "hor")
        self.create_gradient(None, "palegreen", "violet", "hor")

        self.create_gradient(None, "cyan", "purple", "vertical")
        self.create_gradient(None, "chartreuse", "forestgreen", 90)
        self.create_gradient(None, "orange", "gold", "ver")
        self.create_gradient(None, "aqua", "navy", "ver")
        self.create_gradient(None, "chocolate", "saddlebrown", "ver")
        self.create_gradient(None, "yellow", "yellowgreen", "ver")
        self.create_gradient(None, "plum", "palevioletred", "ver")
        self.create_gradient(None, "lightblue", "lightpink", "ver")
        self.create_gradient(None, "darkred", "slateblue", "ver")
