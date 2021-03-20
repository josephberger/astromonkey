import yaml
from models.location import Location

class Area:

    def __init__(self, id):

        self.locations = []
        self.id = id
        with open(f"data/map/areas/{id}/info.yaml","r") as file:
            info = yaml.full_load(file.read())

        self.name = info['name']
        self.description = info['description']

        with open(f"data/map/areas/{id}/locations.yaml","r") as file:
            yaml_locations = yaml.full_load(file.read())

        location_row = []

        for l in yaml_locations:
            if len(location_row) < int(info['length']):
                location_row.append(Location(**l))
            else:
                self.locations.append(location_row)
                location_row = []
                location_row.append(Location(**l))

        self.locations.append(location_row)

        self.location_index = [0,0]

    def goto(self, new_location):

        found = False

        for index1, row in enumerate(self.locations):
            for index2, location in enumerate(row):
                if new_location.upper() == location.name.upper():
                    found = True
                    if self.locations[index1][index2] in self.check_adj_locations():
                        if self.locations[index1][index2].blocked:
                            self.message = (f"{new_location} is not accessable.")
                            break
                        else:
                            self.location_index[0] = index1
                            self.location_index[1] = index2
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

        self.locations[self.location_index[0]][self.location_index[1]] = location
        return True

    def check_adj_locations(self):

        adj_locations = []
        for index1, row in enumerate(self.locations):
            for index2, location in enumerate(row):
                if index1 == self.location_index[0] and index2 == self.location_index[1]:
                    pass
                else:
                    dif1 = abs((index1) - (self.location_index[0]))
                    dif2 = abs((index2) - (self.location_index[1]))

                    if dif1 <= 1 and dif2 <= 1:
                        adj_locations.append(location)

        return adj_locations

    def __check_item(self, item):

        for index, location_item in enumerate(self.locations[self.location_index[0]][self.location_index[1]].items):
            if item == location_item.name:
                return self.locations[self.location_index[0]][self.location_index[1]].items[index]

        return False

    def add_item(self, item):

        self.locations[self.location_index[0]][self.location_index[1]].items.append(item)

    def remove_item(self, item):

        location_item = self.__check_item(item)

        if location_item:

            self.locations[self.location_index[0]][self.location_index[1]].items.remove(location_item)
            self.message = f"Removed {item}"
            return location_item

        else:
            self.message = f"I dont see a {item} to take."
            return False

    def get_current_location(self):

        return self.locations[self.location_index[0]][self.location_index[1]]

    def display_map(self):

        rows = []
        for index1, row in enumerate(self.locations):
            tiles = []
            for index2, location in enumerate(row):
                tile = ""
                if index2 == 0:
                    tile += "| "
                if index1 == self.location_index[0] and index2 == self.location_index[1]:
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
                tile += block + " | "
                tiles.append(tile)
            rows.append(tiles)

        self.message = "-" * (len(rows[0])*33+1) + "\n"

        for row in rows:
            for tile in row:
                self.message += tile
            self.message +="\n"

        self.message += "-" * (len(rows[0])*33+1) + "\n"

        return True

    def dump_info(self):

        info = {}
        info['id'] = self.id
        info['name'] = self.name
        info['location_index'] = self.location_index
        info['locations'] = []
        for index1, row in enumerate(self.locations):
            info['locations'].append([])
            for index2, location in enumerate(row):
                info['locations'][index1].append(location.dump_info())

        return info


    def __str__(self):
        location_count = 0
        for loc in self.locations:
            for l in loc:
                location_count += 1

        return f"Area{self.id} - Name:{self.name}, Location Count:{location_count}"

    def __repr__(self):
        location_count = 0
        for loc in self.locations:
            for l in loc:
                location_count += 1

        return f"Area{self.id} - Name:{self.name}, Location Count:{location_count}"
