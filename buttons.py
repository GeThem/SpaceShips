from pygame import Rect, Surface
from pygame.mouse import get_pos, get_pressed
from pygame.draw import rect
from pygame.font import Font


class Button:
    def __init__(self, x, y, width, height, on_button_indication):
        self.rect = Rect(x, y, width, height)
        self.obi = on_button_indication
        self.was_pressed = 0


class TextButton(Button):
    def __init__(self, x, y, width, height, on_button_activation, text, size, alpha=255):
        super().__init__(x, y, width, height, on_button_activation)

        font = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', size)
        self.on_button = 0

        text_img = font.render(text, 1, (130, 130, 130))
        self.but_inact = Surface(self.rect.size)
        text_img_rect = text_img.get_rect(center=self.but_inact.get_rect().center)
        self.but_inact.fill((100, 100, 100))
        self.but_inact.blit(text_img, text_img_rect)
        self.but_inact.set_alpha(alpha)

        text_img = font.render(text, 1, (130, 130, 130))
        self.but_active = Surface(self.rect.size)
        text_img_rect = text_img.get_rect(center=self.but_active.get_rect().center)
        self.but_active.fill((250, 0, 0))
        self.but_active.blit(text_img, text_img_rect)

        text_img = font.render(text, 1, (130, 130, 130))
        self.but_pressed = Surface(self.rect.size)
        text_img_rect = text_img.get_rect(center=self.but_pressed.get_rect().center)
        self.but_pressed.fill((0, 250, 0))
        self.but_pressed.blit(text_img, text_img_rect)

        self.button = self.but_inact

    def update(self):
        is_pressed = get_pressed(3)[0]
        if self.rect.collidepoint(*get_pos()):
            if is_pressed:
                if self.on_button:
                    self.was_pressed = 1
                    self.button = self.but_pressed
                elif self.obi:
                    self.button = self.but_active
            elif self.was_pressed:
                self.was_pressed = 0
                self.button = self.but_pressed
                return 1
            else:
                if self.obi:
                    self.button = self.but_active
                self.on_button = 1
        else:
            if is_pressed and self.was_pressed:
                self.button = self.but_pressed
            else:
                self.button = self.but_inact
                self.was_pressed = self.on_button = 0

    def draw(self, screen):
        screen.blit(self.button, self.rect)


class Switch(Button):
    def __init__(self, x, y, width, height, on_button_activation):
        super().__init__(x, y, width, height, on_button_activation)
        self.activated = 0
        self.collides = 0

    def update(self, click):
        if self.rect.collidepoint(*get_pos()):
            self.collides = 1
            if click:
                self.activated = not self.activated
        else:
            self.collides = 0

    def draw(self, screen):
        if self.activated:
            rect(screen, (170, 170, 170), self.rect, border_radius=self.rect.width//2)
        elif self.obi and self.collides:
            rect(screen, (130, 130, 130), self.rect, border_radius=self.rect.width//2)
        else:
            rect(screen, (100, 100, 100), self.rect, border_radius=self.rect.width//2)