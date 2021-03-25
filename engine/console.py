from models.game import Game
from os import system, name
from .animations import target_hit, enemy_killed
import pickle
import sys
import time
from models.mechanics.battle import GroundBattle
from models.mechanics.ground import GroundMode


def start():
    clear()
    name = input("Monkey's name (JoJo): ")

    if name == "":
        name = "JoJo"

    clear()

    print_narrative('000-begining')

    game = Game(name)

    while True:
        clear()
        if game.warning:

            print(game.warning)
            input()
            game.warning = None

            if game.game_over:
                clear()
                sys.exit(1)

        elif type(game.mode) == GroundMode:

            # print("Energy " + "|" * game.mode.player.health)
            # print("Oxygen " + "|" * game.mode.player.oxygen)
            # print(f"Location: {game.mode.area.get_current_location().name}")
            # print(f"Adjacent Locations: ", end="")
            # for location in game.mode.area.check_adj_locations():
            #     print(f"{location.name}, ",end="")
            # print()
            # print(f"Areas Visited: {game.mode.areas_visited}")
            # print()
            # print(game.message)

            screen = ground_screen(game.mode)

            for frame in screen:
                clear()
                print(frame)
                if game.mode.animation:
                    time.sleep(.15)

            action = input(f"What should {game.mode.player.name} do?\n")

            if action == "save":
                save_game(game)
            elif action == "load":
                game = load_game(game)
            else:
                result = game.parse_actions(action)

        elif type(game.mode) == GroundBattle:

            screen = battle_screen(game.mode)

            for frame in screen:
                clear()
                print(frame)
                if game.mode.animation:
                    time.sleep(.15)

            if game.mode.animation:
                game.mode.animation = None

            action = input(f"What should {game.player.name} do?\n")
            game.parse_actions(action)


def print_narrative(stage):
    with open(f"data/narrative/{stage}.txt", "r") as file:
        narrative = file.read()

    print(narrative)
    input("Press Enter To Continue")


def ground_screen(mode):
    screen = []

    frame = ""
    frame += new_line("Energy " + "|" * mode.player.health)
    frame += new_line("Oxygen " + "|" * mode.player.oxygen)
    frame += new_line(f"Location: {mode.area.get_current_location().name}")
    frame += f"Adjacent Locations: "
    for location in mode.area.check_adj_locations():
        frame += f"{location.name}, "
    frame += "\n"
    frame += new_line(f"Areas Visited: {mode.areas_visited}")
    frame += "\n"
    frame += new_line(mode.message)

    screen.append(frame)

    return screen


def battle_screen(battle):
    if battle.animation == "target hit":
        return target_hit(battle)
    elif battle.animation == "enemy killed":
        return enemy_killed(battle)

    screen = []
    frame = new_line("Energy " + "|" * battle.player.health)
    frame += new_line("Oxygen " + "|" * battle.player.oxygen)

    for index, enemy in enumerate(battle.location.enemies):
        if index == battle.target:

            frame += new_line(f"[{index}]{enemy.name} - TARGET")
            frame += new_line(enemy.picture)
            frame += new_line(f"Health: {'|' * enemy.health}")

        else:

            frame += new_line(f"[{index}]{enemy.name}")
    frame += new_line(battle.message)
    screen.append(frame)

    return screen


def new_line(line):
    return (line + "\n")


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')


def save_game(game):
    name = input("Save Name?: ")
    with open(f"game_data/savegame/{name}.game", "wb") as file:
        pickle.dump(game, file)

    for area_id in game.areas_visited:
        with open(f"game_data/area/{area_id}.area", "rb") as file:
            area = pickle.load(file)

        with open(f"game_data/savegame/areas/{name}.{area_id}.area", "wb") as file:
            pickle.dump(area, file)

    input(f"Successfully saved {name}")


def load_game(current_game):
    name = input("Load Name?: ")
    with open(f"game_data/savegame/{name}.game", "rb") as file:
        game = pickle.load(file)

    try:
        if game.version != current_game.version:
            print(
                f"Cannot load this game.  It is version {game.version} and the engine is version {current_game.version}")
            input()
            return current_game
    except:
        print(f"Cannot load this game.  It is on an unknwon version and the engine is version {current_game.version}")
        input()
        return current_game

    for area_id in game.areas_visited:
        with open(f"game_data/savegame/areas/{name}.{area_id}.area", "rb") as file:
            area = pickle.load(file)

        with open(f"game_data/area/{area_id}.area", "wb") as file:
            pickle.dump(area, file)
    input(f"Loaded saved game {name}")
    return game