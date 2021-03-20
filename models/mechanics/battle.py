import random
from models.objects.inventory import InvItem

class GroundBattle:

    def __init__(self, player, location):

        self.player = player
        self.location = location
        self.message = ""
        self.player_message = ""
        self.enemy_message = ""
        self.over = False
        self.target = -1
        self.action = []
        self.passive = False
        self.defeated_enemies = []

    def start(self):
        pass

    def run(self, action):

        self.message = ""
        self.player_message = ""
        self.enemy_message = ""
        self.player_action(action)

        if self.passive:
            self.message = f"Player actions: {self.player_message}\n"
        else:
            self.enemy_action()
            self.message = f"Player actions: {self.player_message}\n"
            self.message += f"Enemy actions:\n{self.enemy_message}\n"

        self.status_check()

    def player_action(self,action):

        if action[0] == "poop":

            self.player.poop()
            self.player_message = self.player.message
            self.passive = False

        elif action[0] == "target":

            if action[1]:
                try:
                    int(action[1])
                except:
                    self.player_message = f"{action[1]} is not an enemy ID"
                    return
                if int(action[1]) > len(self.location.enemies) -1:
                    self.player_message = f"No enemy with ID of {action[1]}"
                    return
                else:
                    self.target = int(action[1])
                    self.player_message = f"Targeted {self.location.enemies[self.target].name}"
                    self.passive = True

        elif action[0] == "throw":

            self.attack_target(at_method=action[0], at_object=action[1])
            self.passive = False

        else:
            self.player_message = f"Player did nothing"
            self.passive = False

    def attack_target(self, at_method, at_object):

        if self.target >= 0:
            pass
        else:
            self.player_message = ("You need to target something first!")
            return

        if at_method == "throw":
            thrown = self.player.throw(at_object)
            if thrown:
                self.location.enemies[self.target].health -= thrown.dmg
                self.player_message = f"{at_object} thrown at {self.location.enemies[self.target].name} for {thrown.dmg} damage!"
            else:
                self.player_message = self.player.message

    def enemy_action(self):

        for enemy in self.location.enemies:
            chance = random.randint(0, 100)
            if chance <= enemy.accuracy:

                self.player.health -= enemy.damage
                self.enemy_message += f"{enemy.name} did {enemy.damage} damage!\n"

            else:

                self.enemy_message += f"{enemy.name} missed!\n"

    def check_enemy(self, target):

        for index, enemy in enumerate(self.location.enemies):
            if target.upper() == enemy.name.upper():
                return enemy, index

    def status_check(self):

        for index, enemy in enumerate(self.location.enemies):
            if enemy.health < 1:
                if index == self.target:
                    self.target = -1
                self.message += f"{enemy.name} killed!\n"
                self.location.items.append(InvItem(common_item="banana"))
                self.defeated_enemies.append(self.location.enemies[index])
                self.location.enemies.remove(self.location.enemies[index])

        if len(self.location.enemies) == 0:
            self.over = True

    def get_battle_stats(self):

        stats = ("--- Battle Stats ---\n"
                 f"Defeated: {len(self.defeated_enemies)}\n")

        return stats

