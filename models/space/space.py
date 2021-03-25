import yaml
from ..space.tile import Tile
import random

class SpaceMode:

    def __init__(self, id):

        self.tiles = []
        self.id = id
        self.name = "space"
        self.description = "The final frontier"

        with open(f"data/map/space/manditory.yaml","r") as file:
            manditory = yaml.full_load(file.read())
        with open(f"data/map/space/random.yaml","r") as file:
            common = yaml.full_load(file.read())

        tiles = []
        for tile in manditory:
            tiles.append(tile)
        for i in range (len(manditory), 36):
            index = random.randint(0,len(common)-1)
            tiles.append(common[index])

        tile_row = []

        while len(tiles) > 0:
            index = random.randint(1, len(tiles)) - 1
            if len(tile_row) < 6:
                tile_row.append(Tile(**tiles[index]))
                tiles.remove(tiles[index])
            else:
                self.tiles.append(tile_row)
                tile_row = []
                tile_row.append(Tile(**tiles[index]))
                tiles.remove(tiles[index])


        self.tiles.append(tile_row)

        self.tile_index = [0,0]

    def goto(self, new_location):

        found = False

        for index1, row in enumerate(self.tiles):
            for index2, location in enumerate(row):
                if new_location.upper() == location.name.upper():
                    found = True
                    if self.tiles[index1][index2] in self.check_adj_locations():
                        if self.tiles[index1][index2].blocked:
                            self.message = (f"{new_location} is not accessable.")
                            break
                        else:
                            self.tile_index[0] = index1
                            self.tile_index[1] = index2
                            self.message = (f"Changing location to {new_location}.")
                    else:
                        self.message = (f"{new_location} is not adjacent to current location.")
                    break
            if found:
                break

        if found:
            pass
        else:
            self.message = f"Can't go to {new_location}"

    def update_location(self,location):

        self.tiles[self.tile_index[0]][self.tile_index[1]] = location
        return True

    def check_adj_locations(self):

        adj_locations = []
        for index1, row in enumerate(self.tiles):
            for index2, location in enumerate(row):
                if index1 == self.tile_index[0] and index2 == self.tile_index[1]:
                    pass
                else:
                    dif1 = abs((index1) - (self.tile_index[0]))
                    dif2 = abs((index2) - (self.tile_index[1]))

                    if dif1 <= 1 and dif2 <= 1:
                        adj_locations.append(location)

        return adj_locations

    def check_item(self, item):

        for index, location_item in enumerate(self.tiles[self.tile_index[0]][self.tile_index[1]].items):
            if item == location_item.name:
                return self.tiles[self.tile_index[0]][self.tile_index[1]].items[index]

        return False

    def add_item(self, item):

        self.tiles[self.tile_index[0]][self.tile_index[1]].items.append(item)

    def remove_item(self, item):

        location_item = self.check_item(item)

        if location_item:

            self.tiles[self.tile_index[0]][self.tile_index[1]].items.remove(location_item)
            self.message = f"Removed {item}"
            return location_item

        else:
            self.message = f"I dont see a {item} to take."
            return False

    def get_current_location(self):

        return self.tiles[self.tile_index[0]][self.tile_index[1]]

    def display_map(self):

        rows = []
        for index1, row in enumerate(self.tiles):
            tiles = []
            for index2, location in enumerate(row):
                tile = ""
                if index2 == 0:
                    tile += "| "
                if index1 == self.tile_index[0] and index2 == self.tile_index[1]:
                    block = "*" + location.name
                else:
                    block = location.name

                if location.exit:
                    block += "+"

                alternator = True
                while len(block) < 16:
                    if alternator:
                        block += " "
                        alternator = False
                    else:
                        block = " " + block
                        alternator = True
                tile += block + " | "
                tiles.append(tile)
            rows.append(tiles)

        self.message = "-" * (len(rows[0])*19) + "-\n"

        for row in rows:
            for i in row:
                self.message += "|" + (" " * 18)
            self.message += "|\n"
            for tile in row:
                self.message += tile
            self.message +="\n"
            for i in row:
                self.message += "|" + (" " * 18)
            self.message += "|\n"
            self.message += "-" * (len(row)*19) + "-\n"
        self.message += "Lgend:\n+ Exit Location\n* Player Location"
        return True

    def __str__(self):
        location_count = 0
        for loc in self.tiles:
            for l in loc:
                location_count += 1

        return f"Area{self.id} - Name:{self.name}, Location Count:{location_count}"

    def __repr__(self):
        location_count = 0
        for loc in self.tiles:
            for l in loc:
                location_count += 1

        return f"Area{self.id} - Name:{self.name}, Location Count:{location_count}"
