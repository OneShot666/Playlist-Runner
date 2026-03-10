# from src.settings import ALL_COLORS


# L Can create its own gradient and save them to use them after -> look in Suika Fruit
# L Add themes based on current date (holidays)
class Theme:                                                                    # Modify program ambiance
    def __init__(self, name="Theme", bg_color=(0, 0, 0), f_color=(0, 0, 0), e_color=(0, 0, 0), b_color=(0, 0, 0)):
        self.theme_name = name
        # Colors data
        # L self.Colors = ALL_COLORS
        self.background_color = bg_color                                            # L Add image/gradient attribut
        self.font_color = f_color
        self.border_color = e_color
        self.button_color = b_color
        # L self.selection_color = s_color

    def set_background_color(self, color):
        self.background_color = color

    def set_font_color(self, color):
        self.font_color = color

    def set_border_color(self, color):
        self.border_color = color

    def set_button_color(self, color):
        self.button_color = color

    # def set_selection_color(self, color):
    #     self.selection_color = color
