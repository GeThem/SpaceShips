from random import randint, choice
from pygame.draw import rect
from pygame.mouse import get_pos
from pygame.key import get_pressed
from pygame.image import load
from itertools import cycle
from pickle import load as bin_load


class Ship:
    def __init__(self, image, x, y, health, damage, movespeed):
        self.image = image
        self.rect = image.get_rect(bottomleft=(x, y))
        self.hp = health
        self.hp_const = health
        self.hp_coords = [self.rect.centerx - health // 2, y + 5]
        self.damage = damage
        self.ms_h, self.ms_v = movespeed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        rect(surface, (250, 0, 0), (*self.hp_coords, self.hp_const, 6))
        rect(surface, (0, 250, 0), (*self.hp_coords, self.hp, 6))


class PlayerMouse(Ship):
    def __init__(self, health, damage, movespeed):
        super().__init__(load("data/images/ship.png"), 265, 900, health, damage, movespeed)
        self.firerate = cycle(range(40, -1, -1))

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
    def __init__(self, health, damage, movespeed):
        super().__init__(health, damage, movespeed)
        with open('data/controlls.bin', 'rb') as file:
            self.l, self.r, self.u, self.d = bin_load(file)

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
    def __init__(self, image, x, y, health=15, damage=5):
        super().__init__(image, x, y, health, damage, (randint(1, 4), 1))
        self.counter = 0

    def fire(self):
        if not randint(0, 120):
            return self.rect.midbottom
        return 0

    def update(self, window_w, window_h, moves=1):
        if not self.counter:
            self.counter = randint(0, window_w)
            self.ms_h *= choice((-1, 1))

        self.rect.y += self.ms_v * moves
        if self.rect.y > window_h:
            return -1
        self.hp_coords[1] += self.ms_v * moves

        if self.rect.x + self.ms_h > 0 and self.rect.right + self.ms_h < window_w:
            self.rect.x += self.ms_h
            self.hp_coords[0] += self.ms_h
            self.counter -= 1
        else:
            self.counter = 0