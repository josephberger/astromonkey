from models.objects.inventory import InvItem
from models.enemy import Monster
class Location:

    def __init__(self, items, name, description="", enemies=None):

        self.name = name
        self.description = description
        self.items = []
        for i in items:
            self.items.append(InvItem(**i))

        if enemies:
            self.enemies = []
            for e in enemies:
                self.enemies.append(Monster(e['type']))
        else:
            self.enemies = []

    def add_item(self,item):

        self.items.append(item)
