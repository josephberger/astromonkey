from .characters import JoJo
from models.area import Area
from models.mechanics.battle import GroundBattle
from models.objects.inventory import InvItem
import yaml
import pickle

class Game:

    def __init__(self, player_name="JoJo"):

        self. version = "0.1"
        self.player = JoJo(player_name)
        self.message = ""
        self.focus = "player"

        self.mode = "normal"
        self.battle = None
        self.warning = None

        self.area = Area("spaceship")
        self.areas_visited = []
        self.areas_visited.append(self.area.id)
        self.dump_area()
        self.available_areas = ['01','spaceship']

    def parse_actions(self, action):

        if self.focus == "player":
            actions = action.split()
            missing = 6 - len(actions)
            for i in range(missing):
                actions.append(None)
            self.parse_player_actions(actions)

        elif self.focus == "battle":
            actions = action.split()
            missing = 6 - len(actions)
            for i in range(missing):
                actions.append(None)
            self.battle_actions(actions)

    def battle_actions(self, action):

        self.battle.run(action)
        if self.battle.over:
            self.focus = "player"
            self.mode = "normal"
            self.area.update_location(self.battle.location)
            self.player = self.battle.player
            self.warning = self.battle.get_battle_stats()

    def parse_player_actions(self, action):

        if action[0] == "fart":

            self.player.fart()
            self.message = self.player.message
        elif action[0] == "change":
            if self.area.get_current_location().exit:
                if action[1] == "area":
                    if action[2] in self.available_areas:
                        if action[2] in self.areas_visited:
                            self.dump_area()
                            self.load_area(action[2])
                        else:
                            self.dump_area()
                            self.new_area(action[2])
                    else:
                        self.message = f"Area '{action[2]}' not available"
            else:
                self.message = "You cannt exit from this location."
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
                self.area.add_item(poop)
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

                cur_loc = self.area.get_current_location()
                self.message = cur_loc.description + "\n\n"

                if len(cur_loc.enemies) > 0:
                    self.message += "Enemies!\n"
                    for e in cur_loc.enemies:
                        self.message += e.type + "\n"

                else:
                    for item in cur_loc.items:
                        self.message += item.name + "\n"

            elif action[1] == None:
                self.message = "Specify somehting to check"
            else:
                self.message = f"Cant check {action[1]}"

        elif action[0] == "drop":

            if action[1]:
                dropped_item = self.player.drop(action[1])
                if dropped_item:
                    self.area.add_item(dropped_item)
                    self.message = self.player.message
                else:
                    self.message = self.player.message
            else:
                self.message = "Specify something to drop"

        elif action[0] == "take":

            if action[1]:
                item = self.area.remove_item(action[1])
                if item:
                    if self.player.add_item(item):
                        self.message = f"{action[1]} taken."
                        return
                    else:
                        self.message = self.player.message
                        return
                else:
                    self.message = self.area.message
                    return
            else:
                self.message = "NO ITEM SPECIFIED"
                return

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

        self.area.goto(new_location)
        self.message = self.area.message
        if len(self.area.get_current_location().enemies) > 0:
            self.focus = "battle"
            self.mode = "battle"
            self.warning = ".. ENEMIES!  ENTERING BATTLE MODE!"
            self.battle = GroundBattle(self.player, self.area.get_current_location())
        return

    def check_adj_locations(self):

        return self.area.check_adj_locations()

    def display_map(self):

        self.area.display_map()
        self.message = self.area.message

        return
    def new_area(self, id):

        self.areas_visited.append(id)
        self.area = Area("01")

    def dump_area(self):

        if self.area.id in self.areas_visited:
            pass
        else:
            self.areas_visited.append(self.area.id)

        with open(f"game_data/area/{self.area.id}.area","wb") as file:
            pickle.dump(self.area, file)

    def load_area(self,id):

        with open(f"game_data/area/{id}.area", "rb") as file:
            self.area = pickle.load(file)
