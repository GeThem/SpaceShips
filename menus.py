from pygame.mouse import set_visible
from pygame.display import set_mode, quit as disp_quit
from buttons import Button
from ships import PlayerKeyboard, PlayerMouse


class Menu:
    def __init__(self):
        set_visible(True)
        self. window_w, self.window_h = 900, 600
        disp_quit()
        self.screen = set_mode((self.window_w, self.window_h), 0, 32)


class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.button_1 = Button(self.window_w // 2 - 350, self.window_h // 3 - 50, 700, 100, 1)
        self.button_2 = Button(self.window_w // 2 - 350, self.window_h // 3 * 2 - 50, 700, 100, 1)

    def run(self):
        self.screen.fill((60, 60, 60))
        if self.button_1.draw(self.screen):
            return PlayerMouse(100, 15, (5, 4))
        if self.button_2.draw(self.screen):
            return PlayerKeyboard(100, 15,(5, 4))
        return 0