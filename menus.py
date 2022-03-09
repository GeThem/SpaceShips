from pygame.mouse import set_visible
from pygame.display import set_mode, quit as disp_quit, set_caption
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
        set_caption("Main Menu")
        self.button_1 = Button(self.window_w // 2 - 350, self.window_h // 4 - 50, 700, 100, 1)
        self.button_2 = Button(self.window_w // 2 - 350, self.window_h // 4 * 2 - 50, 700, 100, 1)
        self.button_3 = Button(self.window_w // 2 - 350, self.window_h // 4 * 3 - 50, 700, 100, 1)

    def run(self):
        self.screen.fill((60, 60, 60))
        if self.button_1.draw(self.screen):
            return PlayerMouse(100, 15, (5, 4))
        if self.button_2.draw(self.screen):
            return PlayerKeyboard(100, 15,(5, 4))
        if self.button_3.draw(self.screen):
            return 1
        return 0


class InGameMenu(Menu):
    def __init__(self):
        super().__init__()
        set_caption("Menu")
        self.button_1 = Button(self.window_w // 2 - 350, self.window_h // 3 - 50, 700, 100, 1)
        self.button_2 = Button(self.window_w // 2 - 350, self.window_h // 3 * 2 - 50, 700, 100, 1)

    def run(self):
        self.screen.fill((60, 60, 60))
        if self.button_1.draw(self.screen):
            return 1
        if self.button_2.draw(self.screen):
            return 2
        return 0


class SettingsMenu(Menu):
    def __init__(self):
        super().__init__()
        set_caption("Settings")
        self.chosing = 0
        self.button_1 = Button(self.window_w // 3 - 100, self.window_h // 6 - 37, 200, 74, 1)
        self.button_2 = Button(self.window_w // 3 - 100, self.window_h * 2 // 6 - 37, 200, 74, 1)
        self.button_3 = Button(self.window_w // 3 - 100, self.window_h * 3 // 6 - 37, 200, 74, 1)
        self.button_4 = Button(self.window_w // 3 - 100, self.window_h * 4 // 6 - 37, 200, 74, 1)
        self.button_back = Button(self.window_w // 3 - 165, self.window_h * 6 // 7 - 37, 300, 74, 1)
        self.button_save = Button(self.window_w * 2 // 3 - 135, self.window_h * 6 // 7 - 37, 300, 74, 1)

    def run(self):
        self.screen.fill((60, 60, 60))
        if self.button_1.draw(self.screen):
            self.chosing = 1
            return 3
        if self.button_2.draw(self.screen):
            self.chosing = 1
            return 4
        if self.button_3.draw(self.screen):
            self.chosing = 1
            return 5
        if self.button_4.draw(self.screen):
            self.chosing = 1
            return 6
        if self.button_save.draw(self.screen):
            return 2
        return self.button_back.draw(self.screen)
