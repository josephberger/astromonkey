def target_hit(battle):
    screen = []
    explo = [".","/","\",""-","*"]
    for i in range(1,8):
        frame = new_line("Energy " + "|" * battle.player.health)
        frame += new_line("Oxygen " + "|" * battle.player.oxygen)

        for index, enemy in enumerate(battle.location.enemies):
            if index == battle.target:

                frame += new_line(f"[{index}]{enemy.name} - TARGET")
                for line in enemy.picture.split("\n"):
                    if (i % 2) == 0:
                        frame += " " + new_line(line)
                    else:
                        frame +=  line[1:] +"\n"
                frame += new_line(f"Health: {'|' * enemy.health}")

            else:

                frame += new_line(f"[{index}]{enemy.name}")
        frame += new_line(battle.message)

        screen.append(frame)

    return screen

def enemy_killed(battle):

    screen = []

    with open("data/animations/explode.txt","r") as file:
        explode = file.read().split("-------------")

    for e in explode:

        frame = new_line("Energy " + "|" * battle.player.health)
        frame += new_line("Oxygen " + "|" * battle.player.oxygen)

        for index, enemy in enumerate(battle.location.enemies):

                frame += new_line(f"[{index}]{enemy.name}")

        frame += new_line(battle.message)
        frame += (new_line(e))
        screen.append(frame)

    return screen

def new_line(line):
    return (line + "\n")

