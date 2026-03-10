from src.settings import FONT_FILE_NAME, SCREEN_SIZE
from src.core.resource_loader import resources
import pygame


class Label:
    def __init__(self, text: str, pos: tuple[int, int], font_name: str = None, font_size: int = 20,
            color="white", anchor: str = "center"):
        """ :param anchor: "topleft", "center", "topright", etc. (same attributs as for rect) """
        if font_name is None: font_name = FONT_FILE_NAME
        self.font: pygame.Font = resources.get_font(font_name, font_size)       # Get Loader font
        self._text = str(text)
        self.position: tuple[int, int] = pos
        self.color = color
        self.anchor = anchor                                                    # Text placement in image
        self._image = None                                                      # surface to display
        self._rect = None
        # Init function
        self._render()

    def _render(self):
        """ Create text's image. Only use if text or position change """
        self._image = self.font.render(self._text, True, self.color)
        self._rect = self._image.get_rect()
        self.update_position()

    def get_text(self):
        return self._text

    def set_text(self, new_text):
        """ Modify text and regenerate image (if necessary) """
        if str(new_text) != self._text:
            self._text = str(new_text)
            self._render()

    def set_position(self, pos: tuple[int, int]):
        """ Modify and update position (if necessary) """
        if self.position != pos:
            self.position = pos
            self.update_position()

    def set_position_percent(self, pos: tuple[float, float]):
        """ Modify percent position and regenerate image (if necessary) """
        if self.position != pos:
            self.position = (int(pos[0] * SCREEN_SIZE[0]), int(pos[1] * SCREEN_SIZE[1]))
            self._render()

    def set_color(self, color):
        """ Modify font color and regenerate image (if necessary) """
        if color != self.color:
            self.color = color
            self._render()

    def is_text_null(self):
        return self._text in ["", None]

    def update_position(self):
        """ Move text """
        if self._rect:
            setattr(self._rect, self.anchor, self.position)

    def draw(self, screen):
        if self._image and not self.is_text_null():
            screen.blit(self._image, self._rect)
