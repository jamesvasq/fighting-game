import random

playerName = "Adventurer"
playerChoiceYes = ('yes', 'y', '1', 'sure', 'ok', 'okay,' 'of course', 'yep')
playerChoiceNo = ('no', 'nope', '2', 'negative', 'nah')
playerMovement = ('move forward', 'go', 'move', 'advance', 'go forward', 'run', 'escape')
playerAttack = ('attack', 'slice', 'cut', 'kill', 'swing', 'fight')
playerHeal = ('heal', 'restore', 'health')
enemyTypes = ('Skeleton', 'Spider', 'Zombie', 'Goblin', 'Dragon')


# Keys are flavor text. Values are then multiplied by the health and damage stats in the 'enemy' object
enemyModifiers = {
  "Weak": 1,
  "Normal": 1.5,
  "Strong": 2,
  "Master": 2.5,
  "Mythic": 2.75,
  "Legendary": 3
}


class HostileMob:
    def __init__(self, level, modifier, type, name, health, damage):
        self.level = level
        self.modifier = modifier
        self.type = type
        self.name = name
        self.health = health
        self.damage = damage

    def __str__(self):
        return f"{self.modifier}{self.health}{self.damage}{self.level}"


class PlayerCharacter:
    def __init__(self, name, health, damage, level):
        self.name = name
        self.health = health
        self.damage = damage
        self.level = level

    def __str__(self):
        return f"{self.health}{self.damage}{self.level}"


def player_combat():
    global enemy
    while enemy.health >= 0 and player.health >= 0:
        print("You are engaged in combat with " + enemy.name + ". You can attack or try to escape.")
        playerchoice = input()
        if playerchoice in playerAttack:
            x = random.randint(0, 100)
            if x >= 60:
                print("You hit the " + enemy.name + " for " + str(player.damage) + " damage.")
                enemy.health = enemy.health - player.damage
                if enemy.health <= 0:
                    print("The " + enemy.name + " is eliminated.")
                    player_update_status()
                    break
                else:
                    print("It now has " + str(enemy.health) + " hit points.")
                    enemy_attack()
            else:
                print("You miss the " + enemy.name + ". It has " + str(enemy.health) + " hit points.")
                enemy_attack()
        elif playerchoice in playerMovement:
            x = random.randint(0, 100)
            if x <= 60:
                print("You've escaped.")
                player_update_status()
                break
            else:
                print("You've failed to escape.")
                enemy_attack()
        else:
            print("Response not recognized.")


def game_over():
    print("You have perished to " + enemy.name + ". Restart the game to try again.")


def get_player_name():
    global playerChoiceYes
    global player
    player = PlayerCharacter("undef", 50, 20, 1)
    x = 0
    while x == 0:
        player.name = input("What is your name?")
        response = input("Are you sure you want to be called " + player.name + "?")
        if response in playerChoiceYes:
            x = 1
        elif response in playerChoiceNo:
            x = 0
        else:
            print("Response not recognized.")


def player_update_status():
    playerchoice = input("You are in a dungeon. You are level " + str(player.level) + ". You can heal or move forward.")
    if playerchoice in playerMovement:
        player_move()
    elif playerchoice in playerHeal:
        player.health = 50
        print(player.name + " was healed to full health.")
        player_update_status()
    else:
        print("Response not recognized.")
        player_update_status()


def player_move():
    spawn_enemy_mob()
    print("You encounter " + enemy.name + "! You can attack or try to escape.")
    player_combat()


# random encounter player movement system // disabled for ease of testing
# def player_move():
#    x = random.randint(0, 100)
#    print("You move forward.")
#    if x < 30:
#        spawn_enemy_mob()
#        print("You encounter " + enemy.name + "! You can attack or try to escape.")
#        player_combat()
#    else:
#        player_update_status()


# random enemy generator. picks a mob type and then multiplies stats by randomly selected modifier
def spawn_enemy_mob():
    global enemy
    modifier = random.choice(list(enemyModifiers.items()))
    enemy = HostileMob(1, modifier[0], random.choice(enemyTypes), "mob", 20, 8)
    enemy.name = enemy.modifier + " " + enemy.type
    enemy.health = enemy.health * modifier[1]
    enemy.damage = enemy.damage * modifier[1]


def enemy_attack():
    x = random.randint(0, 100)
    if x >= 50:
        print("The " + enemy.name + " hits you for " + str(enemy.damage) + '.')
        player.health = player.health - enemy.damage
        print("You have " + str(player.health) + " hit points.")
        if player.health <= 0:
            game_over()
    else:
        print("The " + enemy.name + " misses its attack. You have " + str(player.health) + " hit points.")


player = PlayerCharacter("Adventurer", 50, 25, 1)
print("Welcome " + player.name)
get_player_name()


playerchoice = input("Welcome " + player.name + ", to version 1 of my text based fighting game.\nStart?")
if playerchoice in playerChoiceYes:
    player_move()
else:
    player_update_status()
