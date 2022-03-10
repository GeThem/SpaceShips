from pygame.display import set_mode, quit as disp_quit, set_caption
from pygame.transform import rotate
from random import randint
from bullets import Bullet
from ships import Enemy


class Game:
    def __init__(self, player):
        self.window_w, self.window_h = 600, 900

        self.player = player
        self.p_bullets = []

        self.enemy_ship = rotate(self.player.image, 180)

        self.bullet_speed = 8
        self.bullet_size = 2, 16

        self.enemies = [Enemy(self.enemy_ship, self.window_w // 2, 0),
                        Enemy(self.enemy_ship, self.window_w // 2, 0),
                        Enemy(self.enemy_ship, self.window_w // 2, 0)]
        self.enemy_bullets = []

        self.init_display()

    def init_display(self):
        disp_quit()
        set_caption("Space Ships")
        self.screen = set_mode((self.window_w, self.window_h))

    def run(self):
        self.screen.fill((60, 60, 60))

        # player --------------------------------------------------------
        self.player.update(self.window_w, self.window_h)

        if fire := self.player.fire():
            self.p_bullets.extend([
                Bullet(*fire, self.bullet_size, self.bullet_speed),
                Bullet(fire[0] - 6, fire[1], self.bullet_size, self.bullet_speed),
                Bullet(fire[0] + 6, fire[1], self.bullet_size, self.bullet_speed)
            ])

        for i, bullet in enumerate(self.p_bullets.copy(), -len(self.p_bullets)):
            bullet.update()
            if (index := bullet.rect.collidelist(self.enemies)) != -1:
                del self.p_bullets[i]
                self.enemies[index].hp -= self.player.damage
                if self.enemies[index].hp <= 0:
                    del self.enemies[index]
                    self.enemies.append(
                        Enemy(self.enemy_ship, randint(0, self.window_w - 70), 0, randint(1, 100), randint(1, 20)))
            elif bullet.rect.colliderect((0, 0, self.window_w, self.window_h)):
                bullet.draw(self.screen)
            else:
                del self.p_bullets[i]
        # ---------------------------------------------------------------

        # enemy ---------------------------------------------------------
        for i, enemy in enumerate(self.enemies.copy(), -len(self.enemies)):
            if enemy.update(self.window_w, self.window_h) != -1:
                # if collides with player ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if enemy.rect.colliderect(self.player.rect):
                    self.player.hp -= self.enemies[i].hp
                    del self.enemies[i]
                    self.enemies.append(
                        Enemy(self.enemy_ship, randint(0, self.window_w - 70), 0, randint(1, 100), randint(1, 20)))
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                enemy.draw(self.screen)
                if fire := enemy.fire():
                    self.enemy_bullets.append(Bullet(*fire, self.bullet_size, -self.bullet_speed, enemy.damage))
            else:
                del self.enemies[i]
                self.enemies.append(Enemy(self.enemy_ship, randint(0, self.window_w - 70), 0, damage=randint(1, 20)))

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
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~