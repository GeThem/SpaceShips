from pygame import Rect
from pygame.mouse import get_pos, get_pressed
from pygame.draw import rect


class Button:
    def __init__(self, x, y, width, height, on_button_indication):
        self.rect = Rect(x, y, width, height)
        self.obi = on_button_indication
        self.was_pressed = 0

    def draw(self, screen):
        if self.rect.collidepoint(*get_pos()):
            if get_pressed(3)[0]:
                self.was_pressed = 1
                rect(screen, (0, 250, 0), self.rect)
            elif self.was_pressed:
                return 1
            elif self.obi:
                rect(screen, (250, 0, 0), self.rect)
        else:
            rect(screen, (100, 100, 100), self.rect)
            self.was_pressed = 0
