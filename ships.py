from math import ceil
from random import randint
from itertools import cycle
from pygame.draw import rect
from pygame.mouse import get_pos
from pygame.key import get_pressed
from pygame.image import load
from settings import window_w, window_h


class Ship:
    def __init__(self, image, x, y, health, damage, movespeed):
        self.image = image
        self.rect = image.get_rect(midbottom=(x, y))
        self.hp = self.hp_const = health
        self.hp_coords = [self.rect.centerx - health // 2, y + 5]
        self.damage = damage
        self.ms_h, self.ms_v = movespeed

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        rect(surface, (250, 0, 0), (*self.hp_coords, self.hp_const, 6), border_radius=2)
        if self.hp:
            rect(surface, (0, 250, 0), (*self.hp_coords, self.hp, 6), border_radius=2)


class PlayerMouse(Ship):
    def __init__(self, health, damage, movespeed):
        super().__init__(load("data/images/ship.png"), window_w // 2, window_h - 15, health, damage, movespeed)
        self.firerate = cycle(range(40, -1, -1))

    def restart(self):
        self.rect.midbottom = window_w // 2, window_h - 15
        self.hp = self.hp_const
        self.hp_coords = [self.rect.centerx - self.hp // 2, self.rect.bottom + 5]

    def change_firerate(self, firerate):
        self.firerate = cycle(range(firerate, -1, -1))

    def fire(self):
        if not self.firerate.__next__():
            return self.rect.midtop

    def update(self, window_w, window_h):
        mx, my = get_pos()

        if mx != self.rect.centerx:
            direction = 1 if mx > self.rect.centerx else -1
            move = min(abs(mx - self.rect.centerx), self.ms_h) * direction
            if self.rect.x + move > 0 and self.rect.right + move < window_w:
                self.rect.x += move
                self.hp_coords[0] += move

        if my != self.rect.center[1]:
            direction = 1 if my > self.rect.centery else -1
            move = min(abs(my - self.rect.centery), self.ms_v) * direction
            if self.rect.y + move > 0 and self.rect.bottom + move < window_h:
                self.rect.y += move
                self.hp_coords[1] += move


class PlayerKeyboard(PlayerMouse):
    def __init__(self, health, damage, movespeed, controls):
        super().__init__(health, damage, movespeed)
        self.l, self.r, self.u, self.d = controls

    def update(self, window_w, window_h):
        keys = get_pressed()
        x = self.ms_h * (-keys[self.l] + keys[self.r])
        y = self.ms_v * (-keys[self.d] + keys[self.u])
        # if x and y:
        #     scale = sqrt(x * x + y * y) / abs(x)
        #     x = int(x / scale)
        #     y = int(y / scale)
        if self.rect.x + x > 0 and self.rect.right + x < window_w:
            self.rect.x += x
            self.hp_coords[0] += x
        if self.rect.y - y > 0 and self.rect.bottom - y < window_h:
            self.rect.y -= y
            self.hp_coords[1] -= y


class Enemy(Ship):
    def __init__(self, image, x, y, health=15, damage=5, proximity=50):
        super().__init__(image, x, y, health, damage, (randint(1, 4), randint(1, 2)))
        self.counterx = self.countery = 0
        self.proximity = proximity

    def fire(self):
        if not randint(0, 120):
            return self.rect.midbottom
        return 0

    def update(self, window_w, window_h, playery, moves=1):
        if not self.counterx:
            self.counterx = randint(10, window_w)
            self.ms_h *= -1

        if not self.countery:
            self.countery = randint(10, window_h)
            self.ms_v *= -1

        if self.rect.bottom >= playery - self.proximity and self.ms_v > 0:
            self.ms_v *= -1

        if self.rect.y < 0 and self.ms_v < 0:
            self.ms_v *= -1

        self.rect.y += self.ms_v * moves
        self.hp_coords[1] += self.ms_v * moves
        self.countery -= 1

        # self.rect.y += self.ms_v * moves
        # if self.rect.y > window_h:
        #     return -1
        # self.hp_coords[1] += self.ms_v * moves

        if self.rect.x + self.ms_h > 0 and self.rect.right + self.ms_h < window_w:
            self.rect.x += self.ms_h
            self.hp_coords[0] += self.ms_h
            self.counterx -= 1
        else:
            self.counterx = 0


class Star():
    def __init__(self, window_w, window_h, randy=1):
        self.window_w, self.window_h = window_w, window_h
        self.speed = randint(1, 6) / 2
        self.x, self.y = randint(0, window_w - 1), randint(0, window_h - 1) * randy
        self.size = ceil(self.speed), ceil(self.speed)

    def update(self):
        self.y += self.speed
        if self.y > self.window_h:
            return 1
        return 0

    def draw(self, screen):
        rect(screen, (250, 250, 250), (self.x, round(self.y), *self.size))