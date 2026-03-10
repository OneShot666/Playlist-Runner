from src.settings import ASSETS_DIR, FONTS_DIR
import pygame
import os


class ResourceLoader:                                                           # Manage resources of program
    def __init__(self):
        self.assets_path = ASSETS_DIR                                           # Only gather resources from assets folder
        # Dictionnaries to stock resources (use lazy-loading)
        self._images = {}
        self._fonts = {}
        self._sounds = {}

    def get_image(self, name, subfolder="images", size=None):                   # Load from asset path
        key = (subfolder, name)                                                 # Create unique key

        if name == "" or name is None:
            return self._get_default_image()

        if key in self._images:
            return self._images[key]                                            # Return already builded image

        try:
            name = name + ".png" if not name.endswith(".png") else name
            path = os.path.join(subfolder, name) if ASSETS_DIR in subfolder else \
                os.path.join(self.assets_path, subfolder, name)              # Build path
            image = pygame.image.load(path)
            image = image.convert_alpha() if image.get_alpha() else image.convert() # Convert optimisation
            if size is not None:
                image = pygame.transform.scale(image, size)

            self._images[key] = image                                           # Add in list (cache)
            return image
        except (FileNotFoundError, pygame.error) as e:                          # If can't load image
            return self._get_default_image()

    def get_font(self, name, size):
        key = (name, size)                                                      # Size matter (no dad joke please)

        if key in self._fonts:
            return self._fonts[key]

        try:
            path = os.path.join(FONTS_DIR, name)
            font = pygame.font.Font(path, size)
        except (FileNotFoundError, OSError):
            font = pygame.font.SysFont("Arial", size)                           # If font name not found, use default font

        self._fonts[key] = font
        return font

    def get_sound(self, name):
        if name in self._sounds:
            return self._sounds[name]

        try:
            path = os.path.join(self.assets_path, "sounds", name)
            sound = pygame.mixer.Sound(path)
            self._sounds[name] = sound
            return sound
        except (FileNotFoundError, pygame.error) as e:
            return None                                                         # Sound not found

    @staticmethod
    def _get_default_image():
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255))                                                # L Magenta for debug
        return surf


resources = ResourceLoader()                                                    # Instance imported by other classes
