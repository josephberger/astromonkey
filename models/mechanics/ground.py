
from models.objects.inventory import InvItem
from models.area import Area
import pickle

class GroundMode:

    def __init__(self, player):

        self.player = player
        self.message = ""

        self.area = Area("spaceship")
        self.areas_visited = []
        self.areas_visited.append(self.area.id)
        self.dump_area()
        self.available_areas = ['01','spaceship']
        self.change_mode = False
        self.over = False

        self.animation = None

    def run(self, action):

        self.message = ""
        self.player_action(action)

        self.status_check()

    def player_action(self, action):

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
                self.area.display_map()
                self.message = self.area.message
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
                item = self.area.check_item(action[1])
                if item:
                    if self.player.add_item(item):
                        self.area.remove_item(item)
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

    def goto(self, new_location):

        self.area.goto(new_location)
        self.message = self.area.message
        if len(self.area.get_current_location().enemies) > 0:
            self.change_mode = "battle"
        return

    def status_check(self):

        if self.player.health <=0:
            self.over = True

        if self.player.oxygen <=0:
            self.overr = True

    def new_area(self, id):

        self.areas_visited.append(id)
        self.area = Area(id)

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
