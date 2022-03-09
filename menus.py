from pygame.mouse import set_visible
from pygame.event import set_grab
from pygame.display import set_mode, quit as disp_quit, set_caption
from pygame.draw import rect
from pygame import quit
from buttons import Button
from ships import PlayerKeyboard, PlayerMouse
from pygame.locals import Rect


class Menu:
    def __init__(self):
        set_visible(True)
        set_grab(False)
        self. window_w, self.window_h = 900, 600
        # disp_quit()
        self.screen = set_mode((self.window_w, self.window_h))


class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        set_caption("Main Menu")
        self.b_1 = Button(self.window_w // 2 - 350, self.window_h // 5 - 50, 700, 100, 1, "Start Via Mouse", 54)
        self.b_2 = Button(self.window_w // 2 - 350, self.window_h // 5 * 2 - 50, 700, 100, 1, "Start Via Keyboard", 54)
        self.b_3 = Button(self.window_w // 2 - 350, self.window_h // 5 * 3 - 50, 700, 100, 1, "Change Keybinds", 54)
        self.b_4 = Button(self.window_w // 2 - 350, self.window_h // 5 * 4 - 50, 700, 100, 1, "Exit", 54)

    def run(self):
        self.screen.fill((60, 60, 60))
        if self.b_1.draw(self.screen):
            return PlayerMouse(100, 15, (5, 4))
        if self.b_2.draw(self.screen):
            return PlayerKeyboard(100, 15, (5, 4))
        if self.b_3.draw(self.screen):
            return 1
        if self.b_4.draw(self.screen):
            quit()
            exit()
        return 0


class InGameMenu(Menu):
    def __init__(self):
        super().__init__()
        set_caption("Menu")
        self.b_1 = Button(self.window_w // 2 - 350, self.window_h // 3 - 50, 700, 100, 1, "Continue", 54)
        self.b_2 = Button(self.window_w // 2 - 350, self.window_h // 3 * 2 - 50, 700, 100, 1, "Back to Menu", 54)

    def run(self):
        self.screen.fill((60, 60, 60))
        if self.b_1.draw(self.screen):
            return 1
        if self.b_2.draw(self.screen):
            return 2
        return 0


class SettingsMenu(Menu):
    def __init__(self, controlls):
        super().__init__()
        set_caption("Settings")
        self.buttons = (
            [Button(self.window_w // 3 - 85, self.window_h // 6 - 37, 220, 74, 1, "Move left", 34)],
            [Button(self.window_w // 3 - 85, self.window_h * 2 // 6 - 37, 220, 74, 1, "Move right", 34)],
            [Button(self.window_w // 3 - 85, self.window_h * 3 // 6 - 37, 220, 74, 1, "Move up", 34)],
            [Button(self.window_w // 3 - 85, self.window_h * 4 // 6 - 37, 220, 74, 1, "Move down", 34)]
                        )

        self.button_back = Button(self.window_w // 3 - 165, self.window_h * 6 // 7 - 37, 300, 74, 1,
                                  "Back", 54)
        self.button_save = Button(self.window_w * 2 // 3 - 135, self.window_h * 6 // 7 - 37, 300, 74, 1,
                                  "Save", 54)
        self.controlls = controlls
        for i, (button, ) in enumerate(self.buttons):
            self.buttons[i].append(Rect(button.rect.right + 30, button.rect.y, *button.rect.size))

    def run(self):
        result = 0
        self.screen.fill((60, 60, 60))
        for i, (key, button) in enumerate(zip(self.controlls, self.buttons), 3):
            rect(self.screen, (30, 30, 30), button[1])
            self.screen.blit(key, key.get_rect(center=button[1].center))
            if button[0].draw(self.screen):
                result = i

        if self.button_save.draw(self.screen):
            result = 2
        if self.button_back.draw(self.screen):
            result = 1
        return result
