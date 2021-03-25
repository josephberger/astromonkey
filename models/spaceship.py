from models.area import Area
from models.mechanics.battle import GroundBattle
import pickle

class SpaceShip:

    def __init__(self, player, area):

        self.player = player
        self.message = ""

        self.landed = True

    def blast_off(self):
        pass

    def land(self):
        pass