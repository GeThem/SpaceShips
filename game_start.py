from game import Game
from menus import MainMenu, InGameMenu
from pygame import init as pg_init, quit, display, QUIT, KEYDOWN, K_ESCAPE
from pygame.time import Clock
from pygame.event import get, set_grab
from pygame.mouse import set_visible

pg_init()

clock = Clock()

menu = MainMenu()
in_game_menu = 0
game = 0
game_flag = 0

start = 2
game_is_going = 1
start_timer = timer = 240
while 1:
    if game_flag:
        if start == 2:
            game.run()
            start = 1
        elif start:
            if start_timer:
                start_timer -= 1
            else:
                start = 0
                set_visible(False)
                set_grab(True)
        elif game_is_going:
            game_is_going = game.run()
        else:
            if timer:
                timer -= 1
            else:
                menu = MainMenu()
                game = game_flag = 0
                game_is_going = 1
                start = 2
                start_timer = timer = 240
    else:
        if in_game_menu:
            if (contin := in_game_menu.run()) == 1:
                in_game_menu = 0
                game_flag = 1
                start = 2
                start_timer = 180
                game.init_display()
            elif contin:
                game_flag = 1
                start = game_is_going = timer = in_game_menu = 0

        elif player := menu.run():
            game = Game(player)
            game_flag = 1

    for event in get():
        if event.type == QUIT:
            quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE and not in_game_menu:
                in_game_menu = InGameMenu()
                game_flag = 0

    display.update()
    clock.tick(120)