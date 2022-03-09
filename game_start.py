from pickle import dump, load as bin_load

from keyboard import read_key
from pygame import init as pg_init, quit, display
from pygame.event import get, set_grab
from pygame.key import key_code
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from pygame.mouse import set_visible
from pygame.time import Clock

from game import Game
from menus import MainMenu, InGameMenu, SettingsMenu

pg_init()

clock = Clock()

menu = MainMenu()
game = 0
game_flag = 0

paused = 2
is_going = 1
start_timer = timer = 240
while 1:
    if game_flag:
        if paused == 2:
            game.run()
            paused = 1
        elif paused:
            if start_timer:
                start_timer -= 1
            else:
                paused = 0
                set_visible(False)
                set_grab(True)
        elif is_going:
            is_going = game.run()
        else:
            if timer:
                timer -= 1
            else:
                menu = MainMenu()
                game = game_flag = 0
                is_going = 1
                paused = 2
                start_timer = timer = 240
    else:
        if isinstance(menu, InGameMenu):
            if (contin := menu.run()) == 1:
                menu = 0
                game_flag = 1
                paused = 2
                start_timer = 180
                game.init_display()
            elif contin:
                game_flag = 1
                paused = is_going = timer = menu = 0

        elif isinstance(menu, SettingsMenu):
            if (change := menu.run()) == 1:
                menu = MainMenu()
            elif change == 2:
                with open('data/controlls.bin', 'wb') as file:
                    dump(controlls, file)
                menu = MainMenu()
            elif change == 3:
                controlls[0] = key_code(read_key())
            elif change == 4:
                controlls[1] = key_code(read_key())
            elif change == 5:
                controlls[2] = key_code(read_key())
            elif change == 6:
                controlls[3] = key_code(read_key())

        elif (player := menu.run()) == 1:
            menu = SettingsMenu()
            with open('data/controlls.bin', 'rb') as file:
                controlls = bin_load(file)

        elif player:
            game = Game(player)
            game_flag = 1
            menu = 0

    for event in get():
        if event.type == QUIT:
            quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if isinstance(menu, SettingsMenu):
                    menu = MainMenu()
                elif menu == 0:
                    menu = InGameMenu()
                    game_flag = 0

    display.update()
    clock.tick(120)