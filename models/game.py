from .characters import JoJo
from models.location import Location
from models.mechanics.battle import GroundBattle
import yaml

class Game:

    def __init__(self, player_name="JoJo"):

        self.player = JoJo(player_name)
        self.message = ""
        self.focus = "player"

        self.locations = []

        with open("data/map/01.yaml","r") as file:
            yaml_locations = yaml.full_load(file.read())

        location_row = []

        for l in yaml_locations:
            row_tracker = 0
            if len(location_row) < 3:
                location_row.append(Location(**l))
            else:
                self.locations.append(location_row)
                location_row = []
                location_row.append(Location(**l))

        self.locations.append(location_row)

        self.location = self.locations[0][0]
        self.location_index1 = 0
        self.location_index2 = 0
        self.mode = "normal"
        self.battle = None

    def parse_actions(self, action):

        if self.focus == "player":
            actions = action.split()
            missing = 6 - len(actions)
            for i in range(missing):
                actions.append(None)
            self.parse_player_actions(actions)

        if self.focus == "battle":
            actions = action.split()
            missing = 6 - len(actions)
            for i in range(missing):
                actions.append(None)
            self.battle_actions(actions)

    def battle_actions(self, action):

        self.battle.player_action(action)
        if self.battle.over:
            self.focus = "player"
            self.mode = "normal"
            self.location.enemies = self.battle.enemies
            self.player = self.battle.player
            self.location.enemies = self.battle.enemies

    def parse_player_actions(self, action):

        if action[0] == "fart":

            self.player.fart()
            self.message = self.player.message

        elif action[0] == "go":
            if action[1] == "to":
                if action[2]:
                    self.goto(new_location=action[2])
            else:
                self.message = f"Can't go {action[1]}"

        elif action[0] == "display":
            if action[1] == "map":
                self.display_map()
            else:
                self.message = f"Can't dsplay {action[1]}"

        elif action[0] == "poop":

            poop = self.player.poop()

            if poop:
                self.message = self.player.message
                self.location.add_item(poop)
            else:
                self.message = self.player.message

        elif action[0] == "check":

            if action[1] == "inventory":
                if action[2] == "detail":
                    self.message = f"\n{self.player.name}'s Inventory:\n"
                    if len(self.player.inventory) < 1:
                        self.message += "nothing in inventory"
                    else:
                        total_weight = 0
                        for i in self.player.inventory:
                            total_weight += i.weight
                            self.message += (i.name + " - " + i.description + " Weight:" + str(i.weight) + "\n")
                        self.message += f"\nTotal Weight: {total_weight}lbs"
                else:
                    self.message = f"\n{self.player.name}'s Inventory:\n"
                    if len(self.player.inventory) < 1:
                        self.message += "nothing in inventory"
                    else:
                        for i in self.player.inventory:
                            self.message += (i.name + "\n")

            elif action[1] == "location":
                self.message = self.location.description + "\n\n"

                if len(self.location.enemies) > 0:
                    self.message += "Enemies!\n"
                    for e in self.location.enemies:
                        self.message += e.type + "\n"

                else:
                    for item in self.location.items:
                        self.message += item.name + "\n"

            elif action[1] == None:
                self.message = "Specify somehting to check"
            else:
                self.message = f"Cant check {action[1]}"

        elif action[0] == "drop":

            if action[1]:
                dropped_item = self.player.drop(action[1])
                if dropped_item:
                    self.location.add_item(dropped_item)
                    self.message = self.player.message
                else:
                    self.message = self.player.message
            else:
                self.message = "Specify something to drop"

        elif action[0] == "take":

            for index,item in enumerate(self.location.items):
                if action[1] == item.name:
                    if self.validate_add_inventory(self.location.items[index]):
                        self.location.items.remove(self.location.items[index])
                        self.message = f"{item.name} taken!"
                    else:
                        self.message = "You are carying too much!  Throw some things out!"
                    return

            self.message = f"Cant seem to take {action[1]}"

        elif action[0] == None:
            self.message = "no input..."
        else:
            self.message = f"{self.player.name} cant do that!"

    def validate_add_inventory(self, item):

        if (self.player.check_inv_weight() + item.weight) > self.player.carry_weight:
            return False
        else:
            self.player.inventory.append(item)
            return True

    def goto(self, new_location):

        found = False

        for index1, row in enumerate(self.locations):
            for index2, location in enumerate(row):
                if new_location.upper() == location.name.upper():
                    found = True
                    if self.locations[index1][index2] in self.check_adj_locations():
                        self.locations[self.location_index1][self.location_index2] = self.location
                        self.location = self.locations[index1][index2]
                        self.location_index1 = index1
                        self.location_index2 = index2
                        self.message = (f"Changing location to {new_location}.")
                        if len(self.location.enemies) > 0:
                            self.focus = "battle"
                            self.mode = "battle"
                            self.message += ".. ENEMIES!  ENTERING BATTLE MODE!"
                            self.battle = GroundBattle(self.player, self.location.enemies)
                    else:
                        self.message = (f"{new_location} is not adjacent to current location.")
                    break
            if found:
                break

        if found:
            pass
        else:
            self.message = f"Can't go to {new_location}"

    def check_adj_locations(self):

        adj_locations = []
        for index1, row in enumerate(self.locations):
            for index2, location in enumerate(row):
                if index1 == self.location_index1 and index2 == self.location_index2:
                    pass
                else:
                    dif1 = abs((index1) - (self.location_index1))
                    dif2 = abs((index2) - (self.location_index2))

                    if dif1 <= 1 and dif2 <= 1:
                        adj_locations.append(location)

        return adj_locations

    def display_map(self):

        self.message = "-" * 100 + "\n"

        for index1, row in enumerate(self.locations):
            for index2, location in enumerate(row):
                if index2 == 0:
                    self.message += "| "
                if index1 == self.location_index1 and index2 == self.location_index2:
                    block = location.name + "*"
                else:
                    block = location.name
                alternator = True
                while len(block) < 30:
                    if alternator:
                        block += " "
                        alternator = False
                    else:
                        block = " " + block
                        alternator = True
                self.message += block + " | "
            self.message += "\n" + "-" * 100 + "\n"