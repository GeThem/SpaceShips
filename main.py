from pickle import dump, load as bin_load
from pygame import init as pg_init, quit
from pygame.display import update as display_update, quit as disp_quit
from pygame.event import get
from pygame.key import name as key_name
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN
from pygame.time import Clock
from pygame.font import Font
from game import Game
from menus import MainMenu, Pause, DeathScreen, SettingsMenu, InGameMenu

pg_init()

clock = Clock()

menu = MainMenu()

font = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', 34)

contin = change = key = click = 0
while 1:
    if menu:
        if isinstance(menu, MainMenu):
            if (player := menu.run()) == 1:
                try:
                    with open('data/controls.bin', 'rb') as file:
                        *controls, mode = bin_load(file)
                except FileNotFoundError:
                    with open('data/controls.bin', 'wb') as file:
                        controls, mode = [97, 100, 119, 115], 1
                        dump(controls + [mode], file)
                menu = SettingsMenu([font.render(key_name(text).upper(), 1, (100, 100, 100)) for text in controls] + [mode])
            elif player:
                paused = is_going = 1
                start_timer = timer = 240
                game = Game(player)
                menu = 0

        elif isinstance(menu, InGameMenu):
            if contin == 0:
                game.run(0)
                contin = menu.run()
            elif contin in (1, 3):
                if contin == 3:
                    player.restart()
                    game = Game(player, 1)
                    is_going = 1
                game.set_caption()
                contin = menu = 0
                paused = 1
                start_timer = 60
            elif contin == 2:
                contin = 0
                disp_quit()
                menu = MainMenu()

        else:
            if change == 0:
                change, mode = menu.run(click)
            if change:
                if change == 1:
                    change = 0
                    menu = MainMenu()
                elif change == 2:
                    with open('data/controls.bin', 'wb') as file:
                        dump(controls + [mode], file)
                    change = 0
                    menu = MainMenu()
                elif key:
                    for i in range(0, 4):
                        if change == i + 3:
                            controls[i] = key
                            menu.controls[i] = font.render(key_name(controls[i]).upper(), 1, (100, 100, 100))
                            change = key = 0
                            break
    else:
        if paused:
            game.run(0)
            start_timer -= 1
            if start_timer == 0:
                paused = 0
        elif is_going:
            is_going = game.run(1)
        else:
            menu = DeathScreen(game.screen)

    click = 0
    for event in get():
        if event.type == QUIT:
            quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if isinstance(menu, SettingsMenu) and not change:
                    menu = MainMenu()
                elif isinstance(menu, Pause):
                    contin = 1
                elif isinstance(menu, DeathScreen):
                    contin = 0
                    disp_quit()
                    menu = MainMenu()
                elif menu == 0:
                    menu = Pause(game.screen)
            elif change:
                key = event.key
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = 1

    display_update()
    clock.tick(120)