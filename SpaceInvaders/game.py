import pygame as pg
from random import randint, choice
from itertools import cycle  # for animations
from math import sqrt

class Ship:
    def __init__(self, image, x, y, health, damage, movespeed):
        self.image = image
        self.size = image.get_size()
        self.rect = image.get_rect(bottomleft=(x, y))
        self.hp = health
        self.hp_const = health
        self.hp_coords = [x + (self.size[0] - health) // 2, y + 5]
        self.damage = damage
        self.ms_h, self.ms_v = movespeed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pg.draw.rect(surface, (250, 0, 0), (*self.hp_coords, self.hp_const, 6))
        pg.draw.rect(surface, (0, 250, 0), (*self.hp_coords, self.hp, 6))


class PlayerMouse(Ship):
    def __init__(self, image, x, y, health, damage, movespeed):
        super().__init__(image, x, y, health, damage, movespeed)

    def update(self):
        mx, my = pg.mouse.get_pos()
        if mx != self.rect.center[0]:
            direction = 1 if mx > self.rect.center[0] else -1
            move = min(abs(mx - self.rect.center[0]), self.ms_h)
            self.rect.x += move * direction
            self.hp_coords[0] += move * direction
        if my != self.rect.center[1]:
            direction = 1 if my > self.rect.center[1] else -1
            move = min(abs(my - self.rect.center[1]), self.ms_v)
            self.rect.y += move * direction
            self.hp_coords[1] += move * direction


class PlayerKeyboard(Ship):
    def __init__(self, image, x, y, health, damage, movespeed):
        super().__init__(image, x, y, health, damage, movespeed)

    def update(self):
        x, y = (xd_l + xd_r), (yd_d + yd_u)
        # if x and y:
        #     scale = sqrt(x * x + y * y) / abs(x)
        #     x = int(x / scale)
        #     y = int(y / scale)
        if self.rect.x + x > 0 and self.rect.x + x + self.size[0] < window_w:
            self.rect.x += x
            self.hp_coords[0] += x
        if self.rect.y - y > 0 and self.rect.y - y + self.size[1] < window_h:
            self.rect.y -= y
            self.hp_coords[1] -= y
        print(x, y)


class Enemy(Ship):
    def __init__(self, image, x, y, health=15, damage=5):
        super().__init__(image, x, y, health, damage, (randint(1, 4), 1))
        self.counter = 0
        self.fire = 0

    def update(self, moves=1):
        if not self.counter:
            self.counter = randint(0, window_w)
            self.ms_h *= choice((-1, 1))

        self.rect.y += self.ms_v * moves
        if self.rect.y > window_h:
            return -1
        self.hp_coords[1] += self.ms_v * moves

        if self.rect.x + self.ms_h > 0 and self.rect.x + self.ms_h + self.size[0] < window_w:
            self.rect.x += self.ms_h
            self.hp_coords[0] += self.ms_h
            self.counter -= 1
        else:
            self.counter = 0

        self.fire = randint(0, 60 * multiplier)


class Bullet:
    def __init__(self, x, y, size, speed, damage=0):
        self.rect = pg.Rect(x - 1, y, *size)
        self.speed = speed
        self.damage = damage

    def update(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        pg.draw.rect(surface, (200, 200, 0), self.rect)


pg.init()
clock = pg.time.Clock()
pg.mouse.set_visible(False)  # visibility of cursor

window_w, window_h = 600, 900

screen = pg.display.set_mode((window_w, window_h), 0, 32)

player_ship = pg.image.load("data/images/ship.png")
enemy_ship = pg.transform.rotate(player_ship, 180)

multiplier = 2

m_speed = 6 // multiplier
player = PlayerKeyboard(player_ship, (window_w - player_ship.get_size()[0]) // 2, window_h - 20, 100, 15, (5, 4))
p_bullets = []
fire_speed = 0
bullet_speed = 16 / multiplier
bullet_size = 2, 16
xd_l = xd_r = yd_d = yd_u = 0

enemies = [Enemy(enemy_ship, window_w // 2, 0),
           Enemy(enemy_ship, window_w // 2, 0),
           Enemy(enemy_ship, window_w // 2, 0)]
enemy_bullets = []

flag = 1
timer = 120 * 2
while 1:
    if flag:
        screen.fill((60, 60, 60))

        # player --------------------------------------------------------
        player.update()
        if (index := player.rect.collidelist(enemies)) != -1:
            player.hp -= enemies[index].hp
            del enemies[index]
            enemies.append(Enemy(enemy_ship, randint(0 + 70, window_w - 70), 0, randint(1, 100), randint(1, 20)))
        if player.hp <= 0:
            flag = 0
            player.hp = 0
            # pg.quit()
            # exit()
        player.draw(screen)

        if fire_speed:
            fire_speed -= 1
        else:
            fire_speed = 20 * multiplier
            p_bullets.append(Bullet(player.rect.x + player.size[0] // 2, player.rect.y, bullet_size,  bullet_speed))
            p_bullets.append(Bullet(player.rect.x + player.size[0] // 2 - 6, player.rect.y, bullet_size,  bullet_speed))
            p_bullets.append(Bullet(player.rect.x + player.size[0] // 2 + 6, player.rect.y, bullet_size,  bullet_speed))

        for i, bullet in enumerate(p_bullets.copy(), -len(p_bullets)):
            bullet.update()
            if (index := bullet.rect.collidelist(enemies)) != -1:
                del p_bullets[i]
                enemies[index].hp -= player.damage
                if enemies[index].hp <= 0:
                    del enemies[index]
                    enemies.append(Enemy(enemy_ship, randint(0 + 70, window_w - 70), 0, randint(1, 100), randint(1, 20)))
            elif bullet.rect.colliderect((0, 0, window_w, window_h)):
                bullet.draw(screen)
            else:
                del p_bullets[i]
        # ---------------------------------------------------------------

        # enemy ---------------------------------------------------------
        for i, enemy in enumerate(enemies.copy(), -len(enemies)):
            if enemy.update() != -1:
                enemy.draw(screen)
                if enemy.fire == 1:
                    enemy_bullets.append(Bullet(enemy.rect.x + enemy.size[0] // 2, enemy.rect.y + enemy.size[1], bullet_size, -bullet_speed, enemy.damage))
            else:
                del enemies[i]
                enemies.append(Enemy(enemy_ship, randint(0 + 70, window_w - 70), 0, damage=randint(1, 20)))

        for i, bullet in enumerate(enemy_bullets.copy(), -len(enemy_bullets)):
            bullet.update()
            if bullet.rect.colliderect(player):
                del enemy_bullets[i]
                player.hp -= bullet.damage
            elif bullet.rect.colliderect((0, 0, window_w, window_h)):
                bullet.draw(screen)
            else:
                del enemy_bullets[i]
        # ---------------------------------------------------------------
    else:
        if timer:
            timer -= 1
        else:
            pg.quit()
            exit()


    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                xd_l = -player.ms_h
            elif event.key == pg.K_RIGHT:
                xd_r = player.ms_h
            elif event.key == pg.K_UP:
                yd_u = player.ms_v
            elif event.key == pg.K_DOWN:
                yd_d = -player.ms_v
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                xd_l = 0
            elif event.key == pg.K_RIGHT:
                xd_r = 0
            elif event.key == pg.K_UP:
                yd_u = 0
            elif event.key == pg.K_DOWN:
                yd_d = 0

    pg.display.update()
    clock.tick(60 * multiplier)