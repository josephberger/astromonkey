from models.objects.inventory import InvItem
from models.enemy import Monster
class Tile:

    def __init__(self, items, name, description="", enemies=None, blocked=False, exit=False):

        self.name = name
        self.description = description
        self.items = []
        self.exit = exit
        for i in items:
            self.items.append(InvItem(**i))

        if enemies:
            self.enemies = []
            for e in enemies:
                self.enemies.append(Monster(**e))
        else:
            self.enemies = []

        if blocked:
            self.blocked = blocked
        else:
            self.blocked = False

    def dump_info(self):

        info = {}
        info['name'] = self.name
        info['description'] = self.description
        info['blocked'] = self.blocked
        info['items'] = []
        for item in self.items:
            info['items'].append(item.dump_info())

        return info

    def __str__(self):

        return f"Location - Name:{self.name}"

    def __repr__(self):

        return f"Location - Name:{self.name}"
