from pygame import Rect
from pygame.mouse import get_pos, get_pressed
from pygame.draw import rect
from pygame.font import Font


class Button:
    def __init__(self, x, y, width, height, on_button_indication):
        self.rect = Rect(x, y, width, height)
        self.obi = on_button_indication
        self.was_pressed = 0


class TextButton(Button):
    def __init__(self, x, y, width, height, on_button_activation, text, size):
        super().__init__(x, y, width, height, on_button_activation)
        self.text = text
        self.size = size

        font = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', size)
        self.text_inact = font.render(text, 1, (120, 120, 120))
        self.text_inact = (self.text_inact, self.text_inact.get_rect(center=self.rect.center))

        self.text_on_button = font.render(text, 1, (120, 120, 120))
        self.text_on_button = (self.text_on_button, self.text_on_button.get_rect(center=self.rect.center))

        self.text_active = font.render(text, 1, (120, 120, 120))
        self.text_active = (self.text_active, self.text_active.get_rect(center=self.rect.center))

    def draw(self, screen):
        if self.rect.collidepoint(*get_pos()):
            if get_pressed(3)[0]:
                self.was_pressed = 1
                rect(screen, (0, 250, 0), self.rect)
            elif self.was_pressed:
                self.was_pressed = 0
                rect(screen, (0, 250, 0), self.rect)
                return 1
            elif self.obi:
                rect(screen, (250, 0, 0), self.rect)
                screen.blit(*self.text_active)
        else:
            rect(screen, (100, 100, 100), self.rect)
            screen.blit(*self.text_inact)
            self.was_pressed = 0


class Switch(Button):
    def __init__(self, x, y, width, height, on_button_activation):
        super().__init__(x, y, width, height, on_button_activation)
        self.activated = 0
        self.collides = 0

    def update(self, click):
        if self.rect.collidepoint(*get_pos()) and click:
            self.activated = not self.activated

    def draw(self, screen):
        if self.activated:
            rect(screen, (170, 170, 170), self.rect)
        elif self.obi and self.collides:
            rect(screen, (130, 130, 130), self.rect)
        else:
            rect(screen, (100, 100, 100), self.rect)
