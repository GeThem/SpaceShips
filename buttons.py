from pygame import Rect
from pygame.mouse import get_pos, get_pressed
from pygame.draw import rect
from pygame.font import Font
from pygame import Surface


class Button:
    def __init__(self, x, y, width, height, on_button_indication):
        self.rect = Rect(x, y, width, height)
        self.obi = on_button_indication
        self.was_pressed = 0


class TextButton(Button):
    def __init__(self, x, y, width, height, on_button_activation, text, size, alpha=255):
        super().__init__(x, y, width, height, on_button_activation)

        font = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', size)

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

    def draw(self, screen):
        if self.rect.collidepoint(*get_pos()):
            if get_pressed(3)[0]:
                self.was_pressed = 1
                screen.blit(self.but_pressed, self.rect)
            elif self.was_pressed:
                self.was_pressed = 0
                screen.blit(self.but_pressed, self.rect)
                return 1
            elif self.obi:
                screen.blit(self.but_active, self.rect)
        else:
            screen.blit(self.but_inact, self.rect)
            self.was_pressed = 0


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
            rect(screen, (170, 170, 170), self.rect)
        elif self.obi and self.collides:
            rect(screen, (130, 130, 130), self.rect)
        else:
            rect(screen, (100, 100, 100), self.rect)