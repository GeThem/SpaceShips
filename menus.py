from pickle import load as bin_load
from pygame import quit, Rect, Surface
from pygame.display import set_mode, set_caption
from pygame.draw import rect
from pygame.font import Font
from buttons import TextButton, Switch
from ships import PlayerKeyboard, PlayerMouse


class Menu:
    def __init__(self, caption, window_w=900, window_h=600):
        self.window_w, self.window_h = window_w, window_h
        self.screen = set_mode((self.window_w, self.window_h))


class MainMenu(Menu):
    def __init__(self):
        super().__init__("Main Menu")
        self.b_start = TextButton(self.window_w // 2 - 350, self.window_h // 5 - 50, 700, 100, 1, "Start", 54)
        # self.b_2 = TextButton(self.window_w // 2 - 350, self.window_h // 5 * 2 - 50, 700, 100, 1, "Records", 54)
        self.b_setts = TextButton(self.window_w // 2 - 350, self.window_h // 5 * 3 - 50, 700, 100, 1, "Controls", 54)
        self.b_exit = TextButton(self.window_w // 2 - 350, self.window_h // 5 * 4 - 50, 700, 100, 1, "Exit", 54)

    def run(self):
        self.screen.fill((60, 60, 60))
        if self.b_start.draw(self.screen):
            with open('data/controls.bin', 'rb') as file:
                *controls, mode = bin_load(file)
            if mode:
                return PlayerMouse(100, 15, (5, 4))
            return PlayerKeyboard(100, 15, (5, 4), controls)

        # if self.b_2.draw(self.screen):
        #     return
        if self.b_setts.draw(self.screen):
            return 1
        if self.b_exit.draw(self.screen):
            quit()
            exit()
        return 0


class InGameMenu():
    def __init__(self, screen):
        self.screen = screen
        self.window_w, self.window_h = screen.get_size()
        set_caption("Menu")
        self.surf = Surface((self.window_w, self.window_h))  # the size of your rect
        self.surf.set_alpha(150)  # alpha level
        self.surf.fill((60, 60, 60))  # this fills the entire surface

        self.b_continue = TextButton(self.window_w // 2 - 225, self.window_h * 2 // 6 - 40, 450, 80, 1, "Continue", 44, 200)
        self.b_restart = TextButton(self.window_w // 2 - 225, self.window_h * 3 // 6 - 40, 450, 80, 1, "Restart", 44, 200)
        self.b_back = TextButton(self.window_w // 2 - 225, self.window_h * 4 // 6 - 40, 450, 80, 1, "Go to Menu", 44, 200)

    def run(self):
        self.screen.blit(self.surf, (0, 0))
        if self.b_continue.draw(self.screen):
            return 1
        if self.b_back.draw(self.screen):
            return 2
        if self.b_restart.draw(self.screen):
            return 3
        return 0


class SettingsMenu(Menu):
    def __init__(self, controls):
        super().__init__("Controls")
        self.mouse_controls = Switch(self.window_w // 4 - 85, self.window_h // 7 - 15, 30, 30, 1)
        self.keyboard_controls = Switch(self.window_w // 4 - 85, self.window_h * 2 // 7 - 37, 30, 30, 1)

        font = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', 24)
        self.mouse_text = font.render("Mouse control", 1, (150, 150, 150))
        self.mouse_text = self.mouse_text, Rect(self.mouse_controls.rect.move(50, 0))
        self.keyboard_text = font.render("Keyboard control", 1, (150, 150, 150))
        self.keyboard_text = self.keyboard_text, Rect(self.keyboard_controls.rect.move(50, 0))

        self.buttons = (
            [TextButton(self.window_w // 3 - 85, self.window_h * 2 // 7 - 37, 220, 64, 1, "Move left", 34)],
            [TextButton(self.window_w // 3 - 85, self.window_h * 3 // 7 - 37, 220, 64, 1, "Move right", 34)],
            [TextButton(self.window_w // 3 - 85, self.window_h * 4 // 7 - 37, 220, 64, 1, "Move up", 34)],
            [TextButton(self.window_w // 3 - 85, self.window_h * 5 // 7 - 37, 220, 64, 1, "Move down", 34)]
                        )
        self.button_back = TextButton(self.window_w // 3 - 165, self.window_h * 6 // 7 - 37, 300, 74, 1, "Back", 54)
        self.button_save = TextButton(self.window_w * 2 // 3 - 135, self.window_h * 6 // 7 - 37, 300, 74, 1, "Save", 54)
        *self.controls, self.mouse_controls.activated = controls
        self.keyboard_controls.activated = not self.mouse_controls.activated
        for i, (button, ) in enumerate(self.buttons):
            self.buttons[i].append(button.rect.move(button.rect.width + 30, 0))

    def run(self, click):
        result = 0
        self.screen.fill((60, 60, 60))

        if self.keyboard_controls.activated:
            self.mouse_controls.update(click)
            if self.mouse_controls.activated:
                self.keyboard_controls.activated = 0
            else:
                for i, (key, button) in enumerate(zip(self.controls, self.buttons), 3):
                    rect(self.screen, (30, 30, 30), button[1])
                    self.screen.blit(key, key.get_rect(center=button[1].center))
                    if button[0].draw(self.screen):
                        result = i

        elif self.mouse_controls.activated:
            self.keyboard_controls.update(click)
            if self.keyboard_controls.activated:
                self.mouse_controls.activated = 0
            else:
                self.screen.blit(*self.keyboard_text)

        self.keyboard_controls.draw(self.screen)
        self.mouse_controls.draw(self.screen)
        self.screen.blit(*self.mouse_text)

        if self.button_save.draw(self.screen):
            result = 2
        if self.button_back.draw(self.screen):
            result = 1
        return result, self.mouse_controls.activated