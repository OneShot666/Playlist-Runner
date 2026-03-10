from src.ui.button import Button
from src.settings import SCREEN_SIZE
import pygame


# . Adapt color buttons + texts to theme
# . Make it a sidebar (can close and open -> display names or just icons)
# ! Move rotate text function from test.py to here (for open button)
# ! Add writing functions (+ set font) on screen
class MenuManager:
    def __init__(self):
        # Boolean data
        self.is_open: bool = True                                               # Open by default
        # Menus data
        self.MenuItems = [("Profil", "profil.png"), ("Lector", "lector.png"),
            ("Artists", "artists.png"), ("Playlists", "playlists.png"),
            ("Themes", "themes.png"), ("Settings", "settings.png"), ("Quit", "quit.png")]
        self.current_menu_index: int = 1                                        # Lector page by default
        self.current_selected_index: int = 1
        self.bg_color = (64, 64, 64, 200)
        self.line_color = (128, 128, 128)
        # Animation data
        self.menu_position_percent: tuple[float, float] = (0.02, 0.2)
        self.width_percent_open: float = 0.25                                   # Menu width
        self.width_percent_close: float = 0.05
        self.menu_height_percent: float = 0.9 / len(self.MenuItems)
        self.target_width_percent = self.width_percent_open if self.is_open else self.width_percent_close
        self.current_width_percent = self.width_percent_open if self.is_open else self.width_percent_close
        self.animation_speed: float = 0.2
        self.padding: int = 15
        # Buttons data
        self.Buttons: list[Button] = []
        self.toggle_button = None                                               # To open/close menu
        self.button_height_percent: float = 0.08
        self.padding_percent: float = 0.02
        # Init function
        self.create_interface()

    def create_interface(self):
        self.Buttons = []

        w, h = SCREEN_SIZE
        height = int(h * self.button_height_percent)
        padding = int(h * self.padding_percent)
        start_pos = [int(w * self.menu_position_percent[0]), int(h * self.menu_position_percent[1])]
        size = [int(h * self.button_height_percent), int(h * self.button_height_percent)]

        self.toggle_button = Button(None, ">", start_pos, size, action=self.toggle_menu)    # Create toggle button

        for i, (name, icon_name) in enumerate(self.MenuItems):
            y_pos = start_pos[1] + (i * (height + padding))
            btn = Button(icon_name, name, (start_pos[0], y_pos), (int(w * self.width_percent_open), size[1]),
                action=lambda idx=i: self.set_current_menu(idx))
            btn.set_layout(icon_side="left", text_offset=50)
            self.Buttons.append(btn)

    def get_current_menu_name(self):
        return self.MenuItems[self.current_menu_index][0]

    def get_icon_by_name(self, searched_name):
        for name, icon_name in self.MenuItems:
            if name == searched_name:
                return icon_name
        return None

    def set_current_menu(self, new_index):
        self.current_menu_index = min(max(new_index, 0), len(self.MenuItems) - 1)
        print(f"[MenuManager] Current menu : {self.MenuItems[new_index][0]}")   # !!!

    def previous_menu(self):
        self.current_menu_index = (self.current_menu_index - 1) % len(self.MenuItems)

    def next_menu(self):
        self.current_menu_index = (self.current_menu_index + 1) % len(self.MenuItems)

    @staticmethod
    def draw_rectangle(screen: pygame.Surface, color, pos_percent, width: int = 0, radius_percent: float = 0.1):
        size = screen.size
        pos = [int(size[0] * pos_percent[0]), int(size[1] * pos_percent[1]),
               int(size[0] * pos_percent[2]), int(size[1] * pos_percent[3])]
        radius = int(min(pos[2], pos[3]) * radius_percent)
        pygame.draw.rect(screen, color, pos, width, radius)

    def update_layout(self):                                                    # Redo button based on screen size
        self.create_interface()

    def toggle_menu(self):
        self.is_open = not self.is_open
        self.target_width_percent = self.width_percent_open if self.is_open else self.width_percent_close
        # L Rotate toggle button text

    def update(self):                                                           # Manage animation
        diff = self.target_width_percent - self.current_width_percent

        if abs(diff) > 0.001:
            self.current_width_percent += diff * self.animation_speed
        else:
            self.current_width_percent = self.target_width_percent

        num = self.current_width_percent - self.width_percent_close
        den = self.width_percent_open - self.width_percent_close
        opened_amount = 0 if den == 0 else num / den
        opened_amount = min(max(opened_amount, 0), 1)

        for btn in self.Buttons:
            btn.update_truncation(opened_amount)

    def display_buttons(self, screen):
        current_pixel_width = int(SCREEN_SIZE[0] * self.current_width_percent)
        menu_surface = pygame.Surface((current_pixel_width, SCREEN_SIZE[1]))
        menu_surface.set_alpha(min(max(self.bg_color[3], 0), 255))              # Half transparent background
        menu_surface.fill(self.bg_color[:3])
        pos = [int(self.menu_position_percent[0] * SCREEN_SIZE[0]), int(self.menu_position_percent[1] * SCREEN_SIZE[1])]
        screen.blit(menu_surface, pos)

        pygame.draw.line(screen, self.line_color, (current_pixel_width, 0), (current_pixel_width, SCREEN_SIZE[1]), 2)

        self.toggle_button.draw(screen)

        bg_rect = pygame.Rect(0, 0, current_pixel_width, SCREEN_SIZE[1])
        for button in self.Buttons:
            button.draw(screen, clip_rect=bg_rect)
