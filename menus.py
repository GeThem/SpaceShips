from pickle import load as bin_load
from pygame import quit, Rect, Surface, FULLSCREEN
from pygame.display import set_mode, set_caption, quit as disp_quit
from pygame.draw import rect
from pygame.font import Font
from buttons import TextButton, Switch
from ships import PlayerKeyboard, PlayerMouse


class Menu:
    def __init__(self, caption, set_screen, resolution=None, fullscreen=None):
        if set_screen == 1:
            disp_quit()
            self.window_w, self.window_h = resolution
            if fullscreen:
                self.screen = set_mode(resolution, FULLSCREEN)
            else:
                self.screen = set_mode(resolution)
        else:
            self.screen = set_screen
            self.window_w, self.window_h = set_screen.get_size()
        set_caption(caption)


class MainMenu(Menu):
    def __init__(self, set_screen, resolution=(900, 600), fullscreen=0):
        super().__init__("Main Menu", set_screen, resolution, fullscreen)
        self.b_start = TextButton(self.window_w // 2 - 350, self.window_h // 2 - 230, 700, 100, 1, "Start", 54)
        self.b_recs = TextButton(self.window_w // 2 - 350, self.window_h // 2  - 110, 700, 100, 1, "Records", 54)
        self.b_setts = TextButton(self.window_w // 2 - 350, self.window_h // 2 + 10, 700, 100, 1, "Settings", 54)
        self.b_quit = TextButton(self.window_w // 2 - 350, self.window_h // 2 + 130, 700, 100, 1, "Quit", 54)

    def run(self):
        self.screen.fill((60, 60, 60))
        if self.b_start.update():
            with open('data/settings.bin', 'rb') as file:
                *controls, mode, _ = bin_load(file)
            if mode:
                return PlayerMouse(100, 15, (5, 4))
            return PlayerKeyboard(100, 15, (5, 4), controls)

        if self.b_recs.update():
            return 2
        if self.b_setts.update():
            return 1
        if self.b_quit.update():
            quit()
            exit()

        self.b_start.draw(self.screen)
        self.b_recs.draw(self.screen)
        self.b_setts.draw(self.screen)
        self.b_quit.draw(self.screen)

        return 0


class InGameMenu():
    def __init__(self, screen, caption):
        self.screen = screen
        self.window_w, self.window_h = screen.get_size()
        set_caption(caption)
        self.surf = Surface((self.window_w, self.window_h))  # the size of your rect
        self.surf.set_alpha(150)  # alpha level
        self.surf.fill((60, 60, 60))  # this fills the entire surface

    def run(self):
        self.screen.blit(self.surf, (0, 0))


class Pause(InGameMenu):
    def __init__(self, screen):
        super().__init__(screen, "Pause")
        self.b_continue = TextButton(self.window_w // 2 - 225, self.window_h // 2 - 190, 450, 80, 1, "Continue", 44, 200)
        self.b_restart = TextButton(self.window_w // 2 - 225, self.window_h // 2 - 60, 450, 80, 1, "Restart", 44, 200)
        self.b_back = TextButton(self.window_w // 2 - 225, self.window_h // 2 + 150, 450, 80, 1, "Go to Menu", 44, 200)

    def run(self):
        super().run()
        if self.b_continue.update():
            return 1
        if self.b_back.update():
            return 2
        if self.b_restart.update():
            return 3

        self.b_continue.draw(self.screen)
        self.b_back.draw(self.screen)
        self.b_restart.draw(self.screen)
        return 0


class DeathScreen(InGameMenu):
    def __init__(self, screen, score, combo):
        super().__init__(screen, "The end")
        self.b_restart = TextButton(self.window_w // 2 - 225, self.window_h // 2 - 120, 450, 80, 1, "Restart", 44, 200)
        self.b_back = TextButton(self.window_w // 2 - 225, self.window_h // 2 + 40, 450, 80, 1, "Go to Menu", 44, 200)
        font = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', 50)
        self.score_img1 = font.render(f'Final score:', 1, (200, 200, 200))
        self.score_img1 = self.score_img1, self.score_img1.get_rect(center=(self.window_w // 2, self.window_h // 6 - 30))
        
        self.score_img2 = font.render(str(score), 1, (200, 200, 200))
        self.score_img2 = self.score_img2, self.score_img2.get_rect(center=(self.window_w // 2, self.window_h // 6 + 30))

        self.combo_img = font.render(f'Max combo: x{combo}', 1, (200, 200, 200))
        self.combo_img = self.combo_img, self.combo_img.get_rect(center=(self.window_w // 2, self.window_h // 5 + 90))

    def run(self):
        super().run()
        if self.b_back.update():
            return 2
        if self.b_restart.update():
            return 3

        self.screen.blit(*self.combo_img)
        self.screen.blit(*self.score_img1)
        self.screen.blit(*self.score_img2)
        self.b_back.draw(self.screen)
        self.b_restart.draw(self.screen)
        return 0


class SettingsMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.window_w, self.window_h = screen.get_size()
        set_caption("Settings")
        self.fullscreen_switch = Switch(self.window_w // 2 - 310, self.window_h // 2 - 260, 30, 30, 1)
        self.mouse_controls = Switch(self.window_w // 2 - 310, self.window_h // 2 - 210, 30, 30, 1)
        self.keyboard_controls = Switch(self.window_w // 2 - 310, self.window_h // 2 - 160, 30, 30, 1)

        self.overlay = Surface((600, 250))
        self.overlay.set_alpha(150)
        self.overlay.fill((60, 60, 60))
        self.overlay_pos = self.window_w // 2 - 300, self.window_h // 2 - 110

        font = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', 24)
        self.fullscreen_text = font.render("Fullscreen", 1, (150, 150, 150))
        self.fullscreen_text = self.fullscreen_text, self.fullscreen_switch.rect.move(50, 0)

        self.mouse_text = font.render("Mouse control", 1, (150, 150, 150))
        self.mouse_text = self.mouse_text, self.mouse_controls.rect.move(50, 0)

        self.keyboard_text = font.render("Keyboard control", 1, (150, 150, 150))
        self.keyboard_text = self.keyboard_text, self.keyboard_controls.rect.move(50, 0)

        self.warning_text = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', 16).render("Changes will apply after leaving this menu", 1, (150, 150, 150))
        self.warning_text = self.warning_text, self.warning_text.get_rect(center=(self.window_w // 2, self.window_h // 2 + 270))
        self.draw_warning = False

        self.buttons = (
        	[TextButton(self.window_w // 2 - 235, self.window_h // 2 - 110, 220, 54, 1, "Move left", 34)],
            [TextButton(self.window_w // 2 - 235, self.window_h // 2 - 46, 220, 54, 1, "Move right", 34)],
            [TextButton(self.window_w // 2 - 235, self.window_h // 2 + 18, 220, 54, 1, "Move up", 34)],
            [TextButton(self.window_w // 2 - 235, self.window_h // 2 + 82, 220, 54, 1, "Move down", 34)]
            )
        self.button_back = TextButton(self.window_w // 2 - 315, self.window_h  // 2 + 175, 300, 74, 1, "Back", 54)
        self.button_save = TextButton(self.window_w // 2 + 15, self.window_h  // 2 + 175, 300, 74, 1, "Save", 54)
        *self.controls, self.mouse_controls.activated, self.fullscreen_switch.activated = settings
        self.keyboard_controls.activated = not self.mouse_controls.activated
        for i, (button, ) in enumerate(self.buttons):
            self.buttons[i].append(button.rect.move(button.rect.width + 30, 0))

    def run(self, click):
        result = -1
        self.screen.fill((60, 60, 60))

        self.fullscreen_switch.update(click)

        self.fullscreen_switch.draw(self.screen)
        self.keyboard_controls.draw(self.screen)
        self.mouse_controls.draw(self.screen)
        self.button_save.draw(self.screen)
        self.button_back.draw(self.screen)

        for i, (key, button) in enumerate(zip(self.controls, self.buttons)):
            rect(self.screen, (30, 30, 30), button[1])
            self.screen.blit(key, key.get_rect(center=button[1].center))
            if self.keyboard_controls.activated:
                if button[0].update():
                    result = i
            button[0].draw(self.screen)

        if self.keyboard_controls.activated:
            self.mouse_controls.update(click)
            if self.mouse_controls.activated:
                self.keyboard_controls.activated = 0

        elif self.mouse_controls.activated:
            self.keyboard_controls.update(click)
            if self.keyboard_controls.activated:
                self.mouse_controls.activated = 0
            else:
                self.screen.blit(self.overlay, self.overlay_pos)

        if self.button_save.update():
            result = 5
            self.draw_warning = True
        if self.button_back.update():
            result = 4

        self.screen.blit(*self.fullscreen_text)
        self.screen.blit(*self.mouse_text)
        self.screen.blit(*self.keyboard_text)
        if self.draw_warning:
        	self.screen.blit(*self.warning_text)


        return result, self.mouse_controls.activated, self.fullscreen_switch.activated


class Records:
    def __init__(self, screen):
        self.screen = screen
        set_caption("Records")
        self.window_w, self.window_h = screen.get_size()

        self.b_back = TextButton(self.window_w // 2 - 150, self.window_h // 2 + 175, 300, 74, 1, "Back", 54)

        with open('data/records.bin', 'rb') as file:
            self.records = bin_load(file)


        font = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', 35)
        colors = ((255, 224, 23), (224, 224, 224), (148, 86, 0), (150, 150, 150), (150, 150, 150))
        self.mn_text = font.render('Date     Score' + ' ' * 11 + 'Max combo', 1, (200, 200, 200))
        self.records = [font.render(text[0] + '  ' + text[1] + ' ' * (24 - sum(map(len, text[1:]))) + f'x{text[2]}', 1, color) for i, (text, color) in enumerate(zip(self.records, colors), 1)]

    def run(self):
        if self.b_back.update() == 1:
            return 1

        self.screen.fill((60, 60, 60))

        for i, record in enumerate(self.records):
            self.screen.blit(record, record.get_rect(center=(self.window_w // 2, self.window_h // 2 - 130 + 53 * i)))

        self.screen.blit(self.mn_text, self.mn_text.get_rect(center=(self.window_w // 2 + 30, self.window_h // 2 - 200)))
        self.b_back.draw(self.screen)
        return 0