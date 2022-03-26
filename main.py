from pickle import dump, load as bin_load
from pygame import init as pg_init, quit
from pygame.display import update as display_update, Info
from pygame.event import get
from pygame.key import name as key_name
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN
from pygame.time import Clock
from pygame.font import Font
from game import Game
from menus import MainMenu, Pause, DeathScreen, SettingsMenu, InGameMenu, Records


pg_init()

clock = Clock()

resolution = Info().current_w, Info().current_h

try:
    with open('data/settings.bin', 'rb') as file:
        *controls, mode, fullscreen = bin_load(file)
except FileNotFoundError:
    with open('data/settings.bin', 'wb') as file:
        *controls, mode, fullscreen = 97, 100, 119, 115, 1, 1
        dump(controls + [mode, fullscreen], file)

try:
    with open('data/records.bin', 'rb') as file:
        pass
except FileNotFoundError:
    with open('data/records.bin', 'wb') as file:
        dump([], file)

if fullscreen:
    menu = MainMenu(1, resolution, fullscreen)
else:
    menu = MainMenu(1)

font = Font('data/fonts/JetBrainsMono-ExtraBold.ttf', 34)

change = -1
contin = key = click = 0

while 1:
    if menu:
        if isinstance(menu, MainMenu):
            if (player := menu.run()) == 1:
                menu = SettingsMenu(menu.screen, [font.render(key_name(text).upper(), 1, (100, 100, 100)) for text in controls] + [mode, fullscreen])
            elif player == 2:
                menu = Records(menu.screen)
            elif player:
                paused = is_going = 1
                start_timer = timer = 240
                if fullscreen:
                    game = Game(player, menu.screen)
                else:
                    game = Game(player, 1)
                menu = 0

        elif isinstance(menu, InGameMenu):
            if contin == 0:
                game.run(0)
                contin = menu.run()
            elif contin in (1, 3):
                if contin == 3:
                    game = Game(player, game.screen, restart=1)
                    is_going = 1
                game.set_caption()
                contin = menu = 0
                # paused = 1
                # start_timer = 60
            elif contin == 2:
                contin = 0
                if fullscreen:
                    menu = MainMenu(game.screen)
                else:
                    menu = MainMenu(1)

        elif isinstance(menu, Records):
            if menu.run() == 1:
                menu = MainMenu(menu.screen)

        else:
            if change == -1:
                change, mode, fullscreen = menu.run(click)
            else:
                if change == 5:
                    with open('data/settings.bin', 'wb') as file:
                        dump(controls + [mode, fullscreen], file)
                    change = -1
                if change == 4:
                    with open('data/settings.bin', 'rb') as file:
                        *controls, mode, fullscreen = bin_load(file)
                    if fullscreen:
                        if menu.screen.get_size() != resolution:
                            menu = MainMenu(1, resolution, 1)
                        else:
                            menu = MainMenu(menu.screen)
                    else:
                        if menu.screen.get_size() == resolution:
                            menu = MainMenu(1)
                        else:
                            menu = MainMenu(menu.screen)
                    change = -1
                elif key:
                    controls[change] = key
                    menu.controls[change] = font.render(key_name(key).upper(), 1, (100, 100, 100))
                    change = -1
                    key = 0
    else:
        if paused:
            game.run(0)
            start_timer -= 1
            if start_timer == 0:
                paused = 0
        elif is_going:
            is_going, score, combo = game.run(1)
        else:
            menu = DeathScreen(game.screen, score, combo)
            with open('data/records.bin', 'rb') as file:
                scores = bin_load(file)

            if scores == [] or len(scores) < 5:
                scores.append([score, combo])
            elif int(scores[-1][0]) < int(score) or int(scores[-1][0]) == int(score) and int(scores[-1][1]) < int(combo):
                scores[-1] = [score, combo]
            scores = sorted(scores, key=lambda x: int(x[0]), reverse=1)

            with open('data/records.bin', 'wb') as file:
                dump(scores, file)

    click = 0
    for event in get():
        if event.type == QUIT:
            quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if isinstance(menu, SettingsMenu) and change == -1:
                    menu = MainMenu(menu.screen)
                elif isinstance(menu, Pause):
                    contin = 1
                elif isinstance(menu, DeathScreen):
                    contin = 0
                    if fullscreen:
                        menu = MainMenu(game.screen)
                    else:
                        menu = MainMenu(1)
                elif menu == 0:
                    menu = Pause(game.screen)
            elif change != -1:
                key = event.key
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = 1

    display_update()
    clock.tick(120)