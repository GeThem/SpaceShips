from pygame import Rect
from pygame.draw import rect


class Bullet:
    def __init__(self, x, y, size, speed, damage=0):
        self.rect = Rect(x - 1, y, *size)
        self.speed = speed
        self.damage = damage

    def update(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        rect(surface, (200, 200, 0), self.rect)