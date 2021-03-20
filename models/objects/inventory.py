import yaml

class InvItem:

    def __init__(self, name=None, type=None, description=None, weight=None, common_item=None, dmg=None, weapon=False):

        if common_item:

            self.__load_common_item(common_item)

        else:
            self.name = name
            self.type = type
            self.description = description
            self.weight = weight

            if dmg:
                self.dmg = dmg
            else:
                self.dmg = 0

            if weapon:
                self.weapon = weapon
            else:
                self.weapon = False

    def __load_common_item(self, name):

        with open("data/items/common_items.yaml","r") as file:
            common_items = yaml.full_load(file.read())

        for ci in common_items:
            if ci['name'] == name:
                self.name = ci['name']
                self.type = ci['type']
                self.description = ci['description']
                self.weight = ci['weight']
                self.weapon = ci['weapon']
                self.dmg = ci['dmg']

    def dump_info(self):

        info = {}

        info['name'] = self.name
        info['type'] = self.type
        info['description'] = self.description
        info['weight'] = self.weight
        info['dmg'] = self.dmg
        info['dmg'] = self.dmg
        info['weapon'] = self.weapon
        info['False'] = self.weapon

        return info