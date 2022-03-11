from random import randint
from pygame.display import set_mode, quit as disp_quit, set_caption
from pygame.transform import flip
from pygame.mouse import set_visible
from pygame.event import set_grab
from pygame import FULLSCREEN
from bullets import Bullet
from ships import Enemy, Star
from settings import window_h, window_w


class Game:
    def __init__(self, player, restart=0):

        self.player = player
        self.p_bullets = []

        self.enemy_ship = flip(self.player.image, 0, 1)

        self.bullet_speed = 8
        self.bullet_size = 2, 16

        self.enemies = [Enemy(self.enemy_ship, window_w // 2, -80),
                        Enemy(self.enemy_ship, window_w // 2, -80),
                        Enemy(self.enemy_ship, window_w // 2, -80)]
        self.enemy_bullets = []

        self.stars = [Star(window_w, window_h) for _ in range(window_w // 15)]
        if not restart:
            disp_quit()
        self.screen = set_mode((window_w, window_h))
        self.set_caption()

    @staticmethod
    def set_caption():
        set_caption("Space Ships")

    def run(self, not_paused):
        self.screen.fill((0, 0, 0))

        for i, star in enumerate(self.stars.copy(), -len(self.stars)):
            if not_paused:
                if star.update():
                    del self.stars[i]
                    self.stars.append(Star(window_w, window_h, 0))
            star.draw(self.screen)

        # player --------------------------------------------------------
        if not_paused:
            set_visible(False)
            set_grab(True)
            self.player.update(window_w, window_h)

            if fire := self.player.fire():
                self.p_bullets.extend([
                    Bullet(*fire, self.bullet_size, self.bullet_speed),
                    Bullet(fire[0] - 6, fire[1], self.bullet_size, self.bullet_speed),
                    Bullet(fire[0] + 6, fire[1], self.bullet_size, self.bullet_speed)
                ])
        else:
            set_visible(True)
            set_grab(False)

        for i, bullet in enumerate(self.p_bullets.copy(), -len(self.p_bullets)):
            if not_paused:
                bullet.update()
                if (index := bullet.rect.collidelist(self.enemies)) != -1:
                    del self.p_bullets[i]
                    self.enemies[index].hp -= self.player.damage
                    if self.enemies[index].hp <= 0:
                        del self.enemies[index]
                        self.enemies.append(
                            Enemy(self.enemy_ship, randint(35, window_w - 35), 0, randint(1, 100), randint(1, 20)))
                elif not bullet.rect.colliderect((0, 0, window_w, window_h)):
                    del self.p_bullets[i]
            bullet.draw(self.screen)
        # ---------------------------------------------------------------

        # enemy ---------------------------------------------------------
        for i, enemy in enumerate(self.enemies.copy(), -len(self.enemies)):
            if not_paused:
                if enemy.update(window_w, window_h, self.player.rect.y) != -1:
                    # if collides with player ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    if enemy.rect.colliderect(self.player.rect):
                        self.player.hp -= self.enemies[i].hp
                        del self.enemies[i]
                        self.enemies.append(
                            Enemy(self.enemy_ship, randint(35, window_w - 35), -80, randint(1, 100), randint(1, 20)))
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # enemy.draw(self.screen)
                    if fire := enemy.fire():
                        self.enemy_bullets.append(Bullet(*fire, self.bullet_size, -self.bullet_speed, enemy.damage))
                else:
                    del self.enemies[i]
                    self.enemies.append(Enemy(self.enemy_ship, randint(35, window_w - 35), -80, damage=randint(1, 20)))
            if enemy.hp_coords[1] + 6 > 0:
                enemy.draw(self.screen)

        for i, bullet in enumerate(self.enemy_bullets.copy(), -len(self.enemy_bullets)):
            if not_paused:
                bullet.update()
                if bullet.rect.colliderect(self.player):
                    del self.enemy_bullets[i]
                    self.player.hp -= bullet.damage
            elif not bullet.rect.colliderect((0, 0, window_w, window_h)):
                del self.enemy_bullets[i]
            bullet.draw(self.screen)
        # ---------------------------------------------------------------

        # hp check ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if not_paused and self.player.hp <= 0:
            self.player.hp = 0
            self.player.draw(self.screen)
            return 0
        self.player.draw(self.screen)
        return 1
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~