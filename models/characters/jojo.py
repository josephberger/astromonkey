from models.objects.inventory import InvItem
class JoJo():

    def __init__(self, name="JoJo",):

        self.name = name
        self.health = 100
        self.inventory = [InvItem(common_item="turd"), InvItem(common_item="turd"), InvItem(common_item="turd")]
        self.oxygen = 100
        self.message = "Lets go!"
        self.carry_weight = 10

    def run(self):

        self.health -= 1

    def fart(self):

        self.health -= 1
        self.message = "FaaaAAAArrrRTTtttt!"

    def poop(self):

        self.health -= 5
        if self.add_item(InvItem(common_item="turd")):
            self.message = "I pooped!"
            return None
        else:
            self.message = "I pooped!  But iventory is full!"
            return InvItem(common_item="turd")

    def eat(self,health):

        pass

    def throw(self,item):

        for index,inv in enumerate(self.inventory):
            if inv.name == item:
                if self.inventory[index].weapon:
                    thrown = self.inventory[index]
                    self.inventory.remove(self.inventory[index])
                    self.message = f"{item} thrown!"
                    if item == "turd":
                        self.message += "  TURDS AWAY!"
                    return thrown
                else:
                    self.message = f"{item} cannot be thrown in battle!"
                    return False

        self.message = f"No {item}s in inventory to throw!"
        return False

    def drop(self,item):

        for index,inv in enumerate(self.inventory):
            if inv.name == item:
                dropped_item = self.inventory[index]
                self.inventory.remove(self.inventory[index])
                self.message = f"{item} dropped"
                return dropped_item

        self.message = f"No {item} in inventory"
        return None

    def add_item(self,item):

        if item.weight + self.check_inv_weight() < self.carry_weight:
            self.inventory.append(item)
            self.message = f"Added {item.name} to inventory."
            return True
        else:
            self.message = f"{item.name} is too heavy!"
            return False

    def check_inv_weight(self):

        weight = 0
        for item in self.inventory:
            weight += item.weight

        return weight


