from pygame.display import set_mode, quit as disp_quit
from pygame.transform import rotate
from random import randint
from bullet import Bullet
from ships import Enemy


class Game:
    def __init__(self, player):
        self.window_w, self.window_h = 600, 900

        disp_quit()
        self.screen = set_mode((self.window_w, self.window_h), 0, 32)

        self.player = player

        self.enemy_ship = rotate(self.player.image, 180)

        self.p_bullets = []
        self.fire_speed = 1
        self.bullet_speed = 8
        self.bullet_size = 2, 16

        self.enemies = [Enemy(self.enemy_ship, self.window_w // 2, 0),
                        Enemy(self.enemy_ship, self.window_w // 2, 0),
                        Enemy(self.enemy_ship, self.window_w // 2, 0)]
        self.enemy_bullets = []

    def run(self):
        self.screen.fill((60, 60, 60))

        # player --------------------------------------------------------
        self.player.update(self.window_w, self.window_h)
        if (index := self.player.rect.collidelist(self.enemies)) != -1:
            self.player.hp -= self.enemies[index].hp
            del self.enemies[index]
            self.enemies.append(
                Enemy(self.enemy_ship, randint(0 + 70, self.window_w - 70), 0, randint(1, 100), randint(1, 20)))

        if self.fire_speed:
            self.fire_speed -= 1
        else:
            self.fire_speed = 40
            self.p_bullets.append(
                Bullet(self.player.rect.x + self.player.size[0] // 2, self.player.rect.y, self.bullet_size,
                       self.bullet_speed))
            self.p_bullets.append(
                Bullet(self.player.rect.x + self.player.size[0] // 2 - 6, self.player.rect.y, self.bullet_size,
                       self.bullet_speed))
            self.p_bullets.append(
                Bullet(self.player.rect.x + self.player.size[0] // 2 + 6, self.player.rect.y, self.bullet_size,
                       self.bullet_speed))

        for i, bullet in enumerate(self.p_bullets.copy(), -len(self.p_bullets)):
            bullet.update()
            if (index := bullet.rect.collidelist(self.enemies)) != -1:
                del self.p_bullets[i]
                self.enemies[index].hp -= self.player.damage
                if self.enemies[index].hp <= 0:
                    del self.enemies[index]
                    self.enemies.append(
                        Enemy(self.enemy_ship, randint(0 + 70, self.window_w - 70), 0, randint(1, 100), randint(1, 20)))
            elif bullet.rect.colliderect((0, 0, self.window_w, self.window_h)):
                bullet.draw(self.screen)
            else:
                del self.p_bullets[i]
        # ---------------------------------------------------------------

        # enemy ---------------------------------------------------------
        for i, enemy in enumerate(self.enemies.copy(), -len(self.enemies)):
            if enemy.update(self.window_w, self.window_h) != -1:
                enemy.draw(self.screen)
                if enemy.fire == 1:
                    self.enemy_bullets.append(
                        Bullet(enemy.rect.center[0], enemy.rect.bottom, self.bullet_size, -self.bullet_speed,
                               enemy.damage))
            else:
                del self.enemies[i]
                self.enemies.append(
                    Enemy(self.enemy_ship, randint(0 + 70, self.window_w - 70), 0, damage=randint(1, 20)))

        for i, bullet in enumerate(self.enemy_bullets.copy(), -len(self.enemy_bullets)):
            bullet.update()
            if bullet.rect.colliderect(self.player):
                del self.enemy_bullets[i]
                self.player.hp -= bullet.damage
            elif bullet.rect.colliderect((0, 0, self.window_w, self.window_h)):
                bullet.draw(self.screen)
            else:
                del self.enemy_bullets[i]
        # ---------------------------------------------------------------

        # hp check ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if self.player.hp <= 0:
            self.player.hp = 0
            self.player.draw(self.screen)
            return 0
        self.player.draw(self.screen)
        return 1
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~