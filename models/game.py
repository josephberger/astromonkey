from .characters import JoJo
from models.area import Area
from models.mechanics.battle import GroundBattle
from models.mechanics.ground import GroundMode
import pickle

class Game:

    def __init__(self, player_name="JoJo"):

        self. version = "0.2"
        self.player = JoJo(player_name)
        self.message = ""

        self.mode = GroundMode(self.player)
        self.warning = None
        self.game_over = False

        #variables for the "ground mode"
        self.ground = None
        self.battle = None

        self.game_over = False

        with open("data/warnings/battlemode.txt","r") as file:
            self.battle_banner = file.read()

    def parse_actions(self, action):

        actions = action.split()
        missing = 6 - len(actions)
        for i in range(missing):
            actions.append(None)
        self.mode.run(actions)

        self.message = self.mode.message

        self.status_check()

        if self.mode.change_mode:
            self.change_mode()

    def change_mode(self):

        if self.mode.change_mode == "battle":
            self.warning = ".. ENEMIES!  ENTERING BATTLE MODE!" + "\n" + self.battle_banner
            self.mode.change_mode = None
            self.ground = self.mode
            self.mode = GroundBattle(self.mode.player, self.mode.area.get_current_location())
        elif self.mode.change_mode == "ground":
            self.warning = self.mode.message
            self.mode.change_mode = None
            self.battle = self.mode
            self.mode = self.ground
            self.mode.player = self.battle.player
            self.mode.area.update_location(self.battle.location)


    def status_check(self):

        if self.mode.player.health <=0:
            self.game_over = True

        if self.mode.player.oxygen <=0:
            self.game_over = True

        if self.game_over:
            if self.warning:
                self.warning += "GAME OVER "
            else:
                self.warning = "GAME OVER"

