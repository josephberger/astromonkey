class GroundBattle:

    def __init__(self, player, enemies):

        self.player = player
        self.enemies = enemies
        self.message = f"There are {len(enemies)}!"
        self.over = False

    def player_action(self,action):

        if action[0] == "throw":

            if action[1]:
                if self.player.throw(action[1]) and action[2]:
                    if action[2] == "at":
                        if action[3]:
                            enemy, enemy_index = self.check_enemy(action[3])
                            if enemy:
                                self.message = f"{action[1]} thrown at {action[3]}"
                                self.over = True
                                self.enemies = []
                            else:
                                self.message = (self.player.message + f"... but {action[3]} is not an enemy!")
                    else:
                        self.message = "Throw what where who?"
                else:
                    self.message = "Throw what where who?"

            elif action[1]:
                self.message = "Throw what exactly?"

    def check_enemy(self, target):

        for index, enemy in enumerate(self.enemies):
            if target.upper() == enemy.name.upper():
                return enemy, index
