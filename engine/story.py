from models.game import Game
from os import system, name

def start():
    clear()
    name = input("Monkey's name (JoJo): ")

    if name == "":
        name = "JoJo"

    clear()

    print_narrative('000-begining')

    game = Game(name)

    while True:
        if game.mode == "normal":
            clear()
            print("Energy " + "|" * game.player.food)
            print("Oxygen " + "|" * game.player.oxygen)
            print(f"Location: {game.location.name} - {game.location_index1}{game.location_index2}")
            print(f"Adjacent Locations: ", end="")
            for location in game.check_adj_locations():
                print(f"{location.name}, ",end="")
            print()

            action = input(f"What should {game.player.name} do?\n")

            result = game.parse_actions(action)
            input(game.message + "\nPress Enter")
            clear()
        elif game.mode == "battle":

            clear()
            for enemy in game.battle.enemies:
                print(enemy.picture)
                print(enemy.name)
                print(f"Health: {'|' * enemy.health}")
            action = input(f"What should {game.player.name} do?\n")
            result = game.parse_actions(action)
            input(game.battle.message + "\nPress Enter")
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