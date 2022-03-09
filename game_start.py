from pickle import dump, load as bin_load
from pygame import init as pg_init, quit, display
from pygame.event import get, set_grab
from pygame.key import name as key_name
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from pygame.mouse import set_visible
from pygame.time import Clock
from pygame.font import Font
from game import Game
from menus import MainMenu, InGameMenu, SettingsMenu

pg_init()

clock = Clock()

menu = MainMenu()

font = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', 34)

contin = change = key = 0
while 1:
    if menu:
        if isinstance(menu, MainMenu):
            if (player := menu.run()) == 1:
                with open('data/controlls.bin', 'rb') as file:
                    controlls = bin_load(file)
                    menu = SettingsMenu([font.render(key_name(text).upper(), 1, (100, 100, 100)) for text in controlls])
            elif player:
                paused = 2
                is_going = 1
                start_timer = timer = 240
                game = Game(player)
                menu = 0

        elif isinstance(menu, InGameMenu):
            if contin == 0:
                contin = menu.run()
            if contin == 1:
                contin = menu = 0
                paused = 2
                start_timer = 180
                game.init_display()
            elif contin:
                contin = 0
                menu = MainMenu()

        else:
            if change == 0:
                change = menu.run()
            if change:
                if change == 1:
                    change = 0
                    menu = MainMenu()
                elif change == 2:
                    with open('data/controlls.bin', 'wb') as file:
                        dump(controlls, file)
                    change = 0
                    menu = MainMenu()
                elif key:
                    for i in range(0, 4):
                        if change == i + 3:
                            controlls[i] = key
                            menu.controlls[i] = font.render(key_name(controlls[i]).upper(), 1, (100, 100, 100))
                            change = key = 0
                            break
    else:
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
                game = 0
                is_going = 1
                paused = 2
                start_timer = timer = 240

    for event in get():
        if event.type == QUIT:
            quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if isinstance(menu, SettingsMenu) and not change:
                    menu = MainMenu()
                elif isinstance(menu, InGameMenu):
                    contin = 1
                elif menu == 0:
                    menu = InGameMenu()
            elif change:
                key = event.key

    display.update()
    clock.tick(120)