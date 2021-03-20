from models.game import Game
from os import system, name
import pickle
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

        elif game.mode == "normal":

            print("Energy " + "|" * game.player.health)
            print("Oxygen " + "|" * game.player.oxygen)
            print(f"Location: {game.area.get_current_location().name}")
            print(f"Adjacent Locations: ", end="")
            for location in game.check_adj_locations():
                print(f"{location.name}, ",end="")
            print()
            print(f"Areas Visited: {game.areas_visited}")
            print()
            print(game.message)
            if game.warning:
                print(game.warning)
                game.warning = None
            action = input(f"What should {game.player.name} do?\n")

            if action == "save":
                save_game(game)
            elif action == "load":
                game = load_game(game)
            else:
                result = game.parse_actions(action)
                clear()
        elif game.mode == "battle":

            print("Energy " + "|" * game.battle.player.health)
            print("Oxygen " + "|" * game.battle.player.oxygen)

            for index, enemy in enumerate(game.battle.location.enemies):
                if index == game.battle.target:

                    print(f"[{index}]{enemy.name} - TARGET")
                    print(enemy.picture)
                    print(f"Health: {'|' * enemy.health}")

                else:

                    print(f"[{index}]{enemy.name}")
            print(game.battle.message)
            action = input(f"What should {game.player.name} do?\n")
            result = game.parse_actions(action)
            clear()
def print_narrative(stage):

    with open(f"data/narrative/{stage}.txt","r") as file:
        narrative = file.read()

    print(narrative)
    input("Press Enter To Continue")

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
            print(f"Cannot load this game.  It is version {game.version} and the engine is version {current_game.version}")
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