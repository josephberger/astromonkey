import random
class Monster:

    def __init__(self, type, name=None):
        with open("data/enemies/1/alien/pictures.txt","r") as file:
            pictures = file.read().split("-----------------")
        with open("data/enemies/1/alien/names.txt","r") as file:
            names = file.read().split("\n")

        length = (len(pictures) - 1)
        self.picture = pictures[random.randint(0,length)]

        if name:
            self.name = name
        else:
            length = (len(names) - 1)
            self.name = names[random.randint(0,length)]

        self.health = 5
        self.type = type
        self.damage = 5
        self.accuracy = 15

    def __str__(self):

        return f"Monster-{self.type} - Name:{self.name} Health:{self.health}"

    def __repr__(self):

        return f"Monster-{self.type} - Name:{self.name} Health:{self.health}"