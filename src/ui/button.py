from src.core.resource_loader import resources
from src.settings import IMAGES_DIR, SCREEN_SIZE
from src.ui.label import Label
import pygame
import os


# ... Checking code efficiency with Gemini
class Button:                                                                   # CSS and actions of program
    def __init__(self, image_name: str = None, text: str = "", pos=(0, 0), size=(0, 0), border_size=0,
            border_color="white", text_color="black", sub_path="", action=None, action_args=None):
        self.hovered = False
        # Button data
        self.image_name = image_name
        self.image: pygame.Surface = None
        self.sub_path = os.path.join(IMAGES_DIR, sub_path) if IMAGES_DIR not in sub_path else sub_path
        self.position: tuple[int, int] = pos
        self.size: tuple[int, int] = size
        self.rect: pygame.Rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.border_size: int = border_size
        # Icon data
        self.icon_surface = None
        self.icon_position = None
        if image_name:
            self.icon_surface = resources.get_image(image_name, sub_path, size)
        # Colors data
        self.border_color = border_color
        self.text_color = text_color
        # Label data
        self.original_text = text
        self.label: Label = Label(text, self.position, color=self.text_color)
        # Layout data
        self.icon_side = "left"
        self.text_offset = 10
        self.apply_layout()
        # Function data
        self.function = action
        self.args = action_args

    def set_position(self, pos: tuple[int, int]):
        self.position = pos

    def set_position_percent(self, pos: tuple[float, float]):
        self.position = (int(pos[0] * SCREEN_SIZE[0]), int(pos[1] * SCREEN_SIZE[1]))

    def set_size(self, size: tuple[int, int]):
        if size != self.size and self.image_name:
            self.size = size
            self.image = resources.get_image(self.image_name, self.sub_path, self.size)
            self.rect: pygame.Rect = self.image.get_rect(topleft=self.position) if self.image else (
                pygame.Rect(0, 0, self.size[0], self.size[1]))

    def set_size_percent(self, size: tuple[int, int]):
        self.size = (int(size[0] * SCREEN_SIZE[0]), int(size[1] * SCREEN_SIZE[1]))

    def set_text(self, text: str):
        self.label.set_text(text)

    def set_image(self, image: pygame.Surface):
        self.image = pygame.transform.scale(image, size) if image.size != self.size else image
        self.rect: pygame.Rect = self.image.get_rect(topleft=self.position) if self.image else None

    def set_theme(self, border_color=None, text_color=None):
        self.border_color = border_color
        self.text_color = text_color
        self.label.set_color(self.text_color)

    def set_layout(self, icon_side="left", text_offset=50):                     # How icon and text are placed
        self.icon_side = icon_side
        self.text_offset = text_offset
        self.apply_layout()

    def apply_layout(self):
        center_y = self.rect.centery
        start_x = self.rect.x

        if self.icon_side == "left":
            text_x = start_x + self.text_offset
            self.label.set_position((text_x, center_y))
            self.icon_position = (start_x + 10, center_y - (self.icon_surface.get_height() // 2) if self.icon_surface else 0)

    def update_truncation(self, ratio_open):
        total_chars = len(self.original_text)
        nb_chars = int(total_chars * ratio_open)

        sliced_text = self.original_text[:nb_chars]                             # Truncate text
        self.label.set_text(sliced_text)

    def draw(self, screen, clip_rect: pygame.Rect = None):
        if self.image:
            screen.blit(self.image, self.position)
        if self.border_size > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_size)
        self.label.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:                                    # If mouse hover button
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:                                # If click
            if event.button == 1 and self.hovered and self.function:
                self.function(self.args) if args else self.function()
