from game import Game
from pygame.time import Clock
from pygame.event import get
from pygame import init, quit, display, QUIT, KEYDOWN, K_ESCAPE
from menus import MainMenu
from pygame.mouse import set_visible


init()

clock = Clock()

menu = MainMenu()
game = 0


start = 2
flag = 1
start_timer = timer = 240
while 1:
    if game:
        if start == 2:
            game.run()
            start = 1
        elif start:
            if start_timer:
                start_timer -= 1
            else:
                start = 0
                set_visible(False)
        elif flag:
            flag = game.run()
        else:
            if timer:
                timer -= 1
            else:
                menu = MainMenu()
                game = 0
                flag = 1
                start = 2
                start_timer = timer = 240
    else:
        if player := menu.run():
            game = Game(player)

    for event in get():
        if event.type == QUIT:
            quit()
            exit()
        # elif event.type == KEYDOWN:
        #     if event.key == K_ESCAPE:

    display.update()
    clock.tick(120)