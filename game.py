from random import randint
from pygame.display import set_mode, quit as disp_quit, set_caption
from pygame.transform import flip
from pygame.mouse import set_visible
from pygame.event import set_grab
from bullets import Bullet
from ships import Enemy, Star


class Game:
    def __init__(self, player, set_screen, resolution=(600, 900), restart=0):

        self.player = player

        self.p_bullets = []

        if set_screen == 1:
            disp_quit()
            self.window_w, self.window_h = resolution
            self.screen = set_mode((self.window_w, self.window_h))
        else:
            self.screen = set_screen
            self.window_w, self.window_h = set_screen.get_size()

        self.set_caption()

        self.player.set_pos(self.window_w // 2, self.window_h - 15)

        self.enemy_ship = flip(self.player.image, 0, 1)

        self.bullet_size = 2, 16
        self.bullet_speed = self.bullet_size[1] // 2

        enemy_num = self.window_w // 200
        self.enemies = [Enemy(self.enemy_ship, randint(35, self.window_w - 35), -80) for _ in range(enemy_num)]
        self.enemy_bullets = []

        self.stars = [Star(self.window_w, self.window_h) for _ in range(self.window_w // 15)]

        if restart:
            self.player.restart(self.window_w // 2, self.window_h - 15)


    @staticmethod
    def set_caption():
        set_caption("Space Ships")

    def run(self, not_paused):
        self.screen.fill((0, 0, 0))

        for i, star in enumerate(self.stars.copy(), -len(self.stars)):
            if not_paused:
                if star.update():
                    self.stars[i] = Star(self.window_w, self.window_h, 0)
            star.draw(self.screen)

        # player --------------------------------------------------------
        if not_paused:
            set_visible(False)
            set_grab(True)
            self.player.update(self.window_w, self.window_h)

            if fire := self.player.fire():
                self.p_bullets.extend([
                    Bullet(*fire, self.bullet_size, self.bullet_speed, self.player.damage),
                    Bullet(fire[0] - 15, fire[1] + 4, self.bullet_size, self.bullet_speed, self.player.damage - 7),
                    Bullet(fire[0] + 15, fire[1] + 4, self.bullet_size, self.bullet_speed, self.player.damage - 7)
                ])
        else:
            set_visible(True)
            set_grab(False)

        for i, bullet in enumerate(self.p_bullets.copy(), -len(self.p_bullets)):
            if not_paused:
                bullet.update()
                if (index := bullet.rect.collidelist(self.enemies)) != -1:
                    del self.p_bullets[i]
                    self.enemies[index].hp -= bullet.damage
                    if self.enemies[index].hp <= 0:
                        self.enemies[index] = Enemy(self.enemy_ship, randint(35, self.window_w - 35), 0,
                                                    randint(1, 100), randint(1, 20))
                elif not bullet.rect.colliderect((0, 0, self.window_w, self.window_h)):
                    del self.p_bullets[i]
            bullet.draw(self.screen)
        # ---------------------------------------------------------------

        # enemy ---------------------------------------------------------
        for i, enemy in enumerate(self.enemies, -len(self.enemies)):
            if not_paused:
                if enemy.update(self.window_w, self.window_h, self.player.rect.y) != -1:
                    # if collides with player ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    if enemy.rect.colliderect(self.player.rect):
                        self.player.hp -= self.enemies[i].hp
                        self.enemies[i] = Enemy(self.enemy_ship, randint(35, self.window_w - 35), -80,
                                                randint(1, 100), randint(1, 20))
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    if fire := enemy.fire():
                        self.enemy_bullets.append(Bullet(*fire, self.bullet_size, -self.bullet_speed, enemy.damage))
                else:
                    self.enemies[i] = Enemy(self.enemy_ship, randint(35, self.window_w - 35), -80,
                                                damage=randint(1, 20))
            if enemy.hp_coords[1] + 6 > 0:
                enemy.draw(self.screen)

        for i, bullet in enumerate(self.enemy_bullets.copy(), -len(self.enemy_bullets)):
            if not_paused:
                bullet.update()
                if bullet.rect.colliderect(self.player):
                    del self.enemy_bullets[i]
                    self.player.hp -= bullet.damage
                elif bullet.rect.y > self.window_h:
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