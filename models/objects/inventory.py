import yaml

class InvItem:

    def __init__(self, name=None, type=None, description=None, weight=None, common_item=None, dmg=None):

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
                dmg = None

    def __load_common_item(self, name):

        with open("data/items/common_items.yaml","r") as file:
            common_items = yaml.full_load(file.read())

        for ci in common_items:
            if ci['name'] == name:
                self.name = ci['name']
                self.type = ci['type']
                self.description = ci['description']
                self.weight = ci['weight']