from src.settings import ALL_COLORS
from src.data.theme import Theme


class ThemeManager:
    def __init__(self):
        self.Colors = ALL_COLORS
        self.Themes: list[Theme] = []
        self.current_theme_index = 0
        # Init function
        self.create_themes()

    def create_themes(self):
        monochrome =    Theme("Monochrome", "black", "white", "lightgrey", "darkgrey")
        reverse =       Theme("Monochrome", "white", "black", "darkgrey", "lightgrey")
        ocean =         Theme("Ocean", "darkblue", "wheat", "blue", "cyan")
        forest =        Theme("Forest", "forestgreen", "darkgreen", "chartreuse", "lime")
        ironman =       Theme("Iron man", "firebrick", "yellow", "gold", "cyan")
        street_art =    Theme("Hero", "purple", "gold", "orange", "green")
        halloween =     Theme("Halloween", "blueviolet", "darkorange", "black", "orange")
        christmas =     Theme("Christmas", "snow", "red", "green", "snow")
        valentine =     Theme("Valentine's Day", "deeppink", "mediumvioletred", "salmon", "tomato")
        self.Themes.append(monochrome)
        self.Themes.append(reverse)
        self.Themes.append(ocean)
        self.Themes.append(forest)
        self.Themes.append(ironman)
        self.Themes.append(street_art)
        self.Themes.append(halloween)
        self.Themes.append(christmas)
        self.Themes.append(valentine)

    def get_font_color(self):
        return self.Themes[self.current_theme_index].font_color

    def next_theme(self):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.Themes)    # !!
