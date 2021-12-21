# An RPG text based adventure. Created for fun by Justice R. Brinston. Much thanks to the many online resources

# Required imports
import random
import math
import os
import shutil
import sys
import time

# Asset lists
town_names = ["Cariva", "Baronbell", "Zelbridge"]
path_names = ["Prairie Path", "Mountain Path", "Old Path", "Forest Path"]
town_locations = ["Town Hall", "Elder", "Graveyard", "Field", "Doctor",
                  "Church", "House", "Shop", "Cellar", "Blacksmith", "School"]
path_locations = ["Path", "Trees", "Bushes"]


# Clear screen function
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def regiongen(r_amt):
    """Random region generation"""

    # Blank lists
    region = [None] * r_amt

    # Even (+0) become town names
    region[::2] = random.sample(town_names, k=(math.ceil(r_amt / 2)))
    # Odd become path names
    region[1::2] = random.sample(path_names, k=(math.floor(r_amt / 2)))
    # Region Directory numbers
    regions = dict(zip(range(1, r_amt + 1), region))
    return regions


def localgen(r_amt, l_amt, regions):
    """Random location generator for each region"""

    # Blank list of lists
    location = []
    for i in range(r_amt):
        location.append([None] * (l_amt + 1))

    # Populate internal lists
    for i in range(r_amt):
        if (i % 2 == 0) or 0:
            even = i
            # Town Buildings
            location[even] = random.sample(town_locations, k=9)

            # Town Exits
            location[even][1::2] = random.sample(path_names, k=4)

        elif i % 2 != 0:
            odd = i
            # Path Buildings
            location[odd][::1] = random.choices(path_locations, k=9)

            location[odd][3::2] = random.sample(town_names, k=3)
            # print(location)

        # Assign directory number for each location within a region
        location[i] = dict(zip(range(1, l_amt + 1), location[i]))

        # Label each with region name
        location[i][0] = regions[i + 1]

    # Assign Directory number for each regions location list
    for i in range(1, r_amt + 1):
        result = dict(zip(regions, location))

        return result


def worldmaps(world, regions, r_amt):
    for i in range(1, r_amt + 1):
        result = {
            "Regions": regions}
        for x in range(1, r_amt + 1):
            result.update({f"{regions [x]}": world[regions[x]]})

        return result


compass = {
    "north": ["", "2", "3", "4"],
    "center": ["", "9", "1", "5"],
    "south": ["", "8", "7", "6"]
}

NS = ["", "south", "center", "north"]
EW = ["", "1", "2", "3"]


# Displays map
# noinspection PyTypeChecker
def mapview(worldmap):
    """Creates the map for player viewing/movement"""

    # Needed for centering
    width = shutil.get_terminal_size().columns

    # Map Variables

    current_region = worldmap['Regions'][Player['Region']]

    player_location = int(compass[NS[Player["NS"]]][Player["EW"]])

    local_name = worldmap[current_region][player_location]

    center = worldmap[current_region][1]
    nw = worldmap[current_region][2]
    north = worldmap[current_region][3]
    ne = worldmap[current_region][4]
    east = worldmap[current_region][5]
    se = worldmap[current_region][6]
    south = worldmap[current_region][7]
    sw = worldmap[current_region][8]
    west = worldmap[current_region][9]

    # Map Generation
    print("\n" + "=" * width)
    print(f"Region: {current_region}\n".center(width))
    print(f"|Location: {local_name}|".center(width))
    print("-" * width)

    # Top Legend
    print(f"||{'North West': <13}||{'Due North': ^25}||{'North East': >13}||".center(width))
    print("=" * width)

    # NW -> NE
    print(f"||{nw: <13}||{north: ^25}||{ne: >13}||".center(width))
    print("-" * width)

    # West -> East
    print(f"||{west: <13}||{center: ^25}||{east: >13}||".center(width))
    print("-" * width)

    # SW -> SE
    print(f"||{sw: <13}||{south: ^25}||{se: >13}||".center(width))
    print("=" * width)
    # Bottom Legend
    print(f"||{'South West': <13}||{'Due South': ^25}||{'South East': >13}||".center(width))
    print("-" * width)


# noinspection PyTypeChecker
def travel(worldmap, r_amt):
    """Allows for player travel between regions"""

    # Travel Variables
    current_region = worldmap['Regions'][Player['Region']]

    player_location = int(compass[NS[Player["NS"]]][Player["EW"]])

    local_name = worldmap[current_region][player_location]

    if local_name in worldmap["Regions"].values():

        ask = input(f"Would you like to travel to {local_name}").lower()

        if ask in ["y", "yes"]:

            for i in range(1, r_amt + 1):

                try:

                    if worldmap["Regions"][i] is local_name:
                        Player["Region"] = i
                        cls()
                        time.sleep(.5)
                        print(f"Travelling to {local_name}")
                        time.sleep(2)
                        mapview(worldmap)

                except IndexError:
                    pass
        else:
            move(worldmap)


# Game Dictionaries
wpn_list = {"Sword": [1.125, 2], "Bow": [1.25, 1], "Dagger": [1.0625, 3]}
role_list = [["warrior", "w"], ["hunter", "h"], ["rogue", "r"]]
Player = {
    "Region": 1,
    "NS": 2,
    "EW": 2
}


# Hero creation
def new_hero():
    # Name selection
    Player["name"] = input("What is your name?")
    # Starting level
    Player["lvl"] = 1
    # Random starting health
    Player["hp"] = random.choice(random.sample(range(Player["lvl"] * 16, Player["lvl"] * 32), 4))
    # random.choice(random.sample(range(Player["lvl"] * 16, Player["lvl"] * 32), 4))
    # Needed for level up
    Player["maxhp"] = Player["hp"]
    Player['strength'] = 0
    Player['defense'] = 0
    Player['agility'] = 0
    roll = random.randint(4, 10)

    # Stat distribution
    while roll > 0:
        print(f"Strength: {Player ['strength']}, Defense: {Player ['defense']}, Agility: {Player ['agility']} ")

        choice = input(f"{roll} points available. Choose which attribute to increase.\n").lower()
        if choice in ["strength", "s", "defense", "d", "agility", "a"]:
            # Strength
            if choice in ["strength", "s"]:
                s_amt = int(input("Add how much strength?\n"))
                Player["strength"] += s_amt
                roll -= s_amt
            # Defense
            elif choice in ["defense", "d"]:
                d_amt = int(input("Add how much defense?\n"))
                Player["defense"] += d_amt
                roll -= d_amt
            # Agility
            elif choice in ["agility", "a"]:
                a_amt = int(input("Add how much agility?\n"))
                Player["agility"] += a_amt
                roll -= a_amt
            else:
                print("Select an attribute")

    Player["wpn"] = 1
    # Weapon choice
    while Player["wpn"] == 1:
        print("Name: Dmg Multiplier, Agility Modifier")
        print("Sword:   " + str(wpn_list["Sword"][0]) + "          " + str(wpn_list["Sword"][1]))
        print("Bow:     " + str(wpn_list["Bow"][0]) + "           " + str(wpn_list["Bow"][1]))
        print("Dagger:  " + str(wpn_list["Dagger"][0]) + "         " + str(wpn_list["Dagger"][1]))
        wpn_choice = input("Now, please choose a weapon. \n").lower()
        if wpn_choice in ["sword", "s", "bow", "b" "dagger", "d"]:
            if wpn_choice in ["sword", "s"]:
                Player["wpn"] = wpn_list["Sword"][0]
                Player["agility"] += wpn_list["Sword"][1]
            elif wpn_choice in ["bow", "b"]:
                Player["wpn"] = wpn_list["Bow"][0]
                Player["agility"] += wpn_list["Bow"][1]
            elif wpn_choice in ["dagger", "d"]:
                Player["wpn"] = wpn_list["Dagger"][0]
                Player["agility"] += wpn_list["Dagger"][1]

            else:
                print("Select a weapon")
    Player["exp"] = 0
    Player["lvlup"] = 5
    Player["alive"] = True
    return Player


# Player Levelling
def level_up():
    while Player["exp"] >= Player["lvlup"]:
        print("You leveled up")

        # Player["lvlup"] -= Player["exp"]
        stats1 = random.choice([Player["strength"], Player["defense"], Player["agility"]])
        print("You gained 1 random stat point")
        stats1 += 1
        Player["maxhp"] = math.ceil(Player["maxhp"] * 1.125)
        Player["hp"] = Player["maxhp"]
        Player["exp"] -= Player["lvlup"]
        Player["lvlup"] *= 1.5
        Player["lvl"] += 1
        time.sleep(1)


# Mob Names
m_names = ["Goblin", "Minotaur", "Imp", "Rat", "Chimera", "Bandit"]


# Random Mob Generator
def create_mob():
    stats = {"name": random.choice(m_names), "lvl": random.randint(Player["lvl"], Player["lvl"] + 2)}
    stats["hp"] = random.choice(random.sample(range(stats["lvl"] * 8, stats["lvl"] * 12), 2))
    stats["strength"] = random.randint(math.ceil(stats["lvl"] / 2), math.ceil(stats["lvl"] * 1.5))
    stats["defense"] = random.randint(math.ceil(stats["hp"] / 25), math.ceil(stats["hp"] / 20))
    stats["agility"] = random.randint(math.ceil(stats["lvl"] / 4), math.ceil(stats["lvl"] / 2))
    stats["wpn"] = round(random.uniform(1, ((stats["lvl"] * 0.0625) + 1)), 2)

    return stats


def attack(self, target):
    accuracy = self["agility"] - target["agility"]
    hit = random.randint(1, 21) + accuracy
    # accuracy check
    if hit >= 10:
        dmg = random.randint(round((self["strength"] * 2) * self["wpn"]),
                             round((self["strength"] * 4) * self["wpn"]))
        dmg -= (target['defense'] / 2)
        # dmg is always at least 1
        if dmg <= 0:
            dmg = 1
            print(f"{self['name']} dealt {dmg} dmg")
            target['hp'] -= dmg

        # dmg is never more than hp
        elif dmg >= target["hp"]:
            dmg = target['hp']
            print(f"{self['name']} dealt {dmg} dmg")
            target["hp"] -= dmg
        else:
            print(f"{self['name']} dealt {dmg} dmg")
            target["hp"] -= dmg

    # If attack misses
    else:
        if self['name'] == Player['name']:
            print("You missed")
        else:
            print(f"{self['name']} missed")


def battle(hero, mob):
    width = shutil.get_terminal_size().columns
    print(f"{mob['name']} spots you")

    while hero["hp"] and mob["hp"] > 0:
        cmd = input("(R)un, or (F)ight?").lower()
        if cmd in ["f", "fight"]:

            # print(f"{Player['name']}: {Player['hp']} HP")
            print(f"{hero['name']}: {hero['hp']} HP  Level: {hero['lvl']} Exp: {hero['exp']}".center(width))
            attack(hero, mob)
            time.sleep(.5)
            print(f"{mob['name']}: {mob['hp']} HP Level: {mob['lvl']}".center(width))
            if mob["hp"] > 0:
                attack(mob, hero)
                print(f"{hero['name']}: {hero['hp']} HP  Level: {hero['lvl']} Exp: {hero['exp']}".center(
                    width))
                time.sleep(1)

            elif mob["hp"] <= 0:
                expgain = random.randrange(math.ceil(mob["lvl"] / 2), mob["lvl"] * 2, 1)
                hero["exp"] += expgain
                print(f"You gained {expgain} exp!")
                level_up()
                time.sleep(2)

            elif hero["hp"] <= 0:
                cls()
                print(f"{mob['name']} killed you, better luck next time")
                hero["alive"] = False
                sys.exit()

        elif cmd in ["r", "run"]:
            roll = random.randint(1, 20)
            if roll + hero["agility"] > 16:
                print("You got away")
                break

            print("You failed tp get away")
            attack(mob, hero)


def move(worldmap):
    r_amt = len(worldmap["Regions"])
    '''Player movement function'''

    direction = input("Which direction?\n").lower()
    valid_direction = ["north", "south", "east", "west", "n", "s", "e", "w"]

    while direction not in valid_direction:
        direction = input("Which direction?\n").lower()

    if direction in valid_direction:
        # ---------------------------------------------------------#
        # North
        if direction in ["north", "n"]:
            try:
                Player["NS"] += 1
                cls()
                mapview(worldmap)

            except IndexError:
                Player["NS"] -= 1
                cls()
                mapview(worldmap)
                print("The town ends here")
                time.sleep(1)
        # ---------------------------------------------------------#
        # South
        elif direction in ["south", "s"]:
            try:
                Player["NS"] -= 1
                cls()
                mapview(worldmap)

            except KeyError:
                Player["NS"] += 1
                cls()
                mapview(worldmap)
                print("The town ends here")
                time.sleep(1)
        # --------------------------------------------------------#
        # East
        if direction in ["east", "e"]:
            try:
                Player["EW"] += 1
                cls()
                mapview(worldmap)
            except IndexError:
                Player["EW"] -= 1
                cls()
                mapview(worldmap)
                print("The town ends here")
                time.sleep(1)

        # --------------------------------------------------------#
        # West
        elif direction in ["west", "w"]:
            try:
                Player["EW"] -= 1
                if Player["EW"] == 0:
                    Player["EW"] += 1
                    cls()
                    mapview(worldmap)
                    print("The town ends here")
                    time.sleep(1)

                else:
                    cls()
                    mapview(worldmap)

            except KeyError:
                Player["EW"] += 1
                cls()
                mapview(worldmap)
                print("The town ends here")
                time.sleep(1)

    travel(worldmap, r_amt)


# --------------------------------------------------------#


def title():
    cls()
    width = shutil.get_terminal_size().columns
    print('''
    +_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_+
    |              New Game                 |
    |_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_|
    |              Continue                 |
    |_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_|
    |              Help                     |
    |_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_|
    |              Quit                     |
    |_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_|
    |          ©J.R. Brinston               |
    +_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_+'''.center(width))


def game_menu():
    cls()
    title()
    cmd = input("Please select an option\n")
    if cmd in ["new", "n", "continue", "c", "help", "h", "quit", "q"]:
        if cmd in ["new", "n"]:
            new_game()
        elif cmd in ["continue", "c"]:
            pass
        elif cmd in ["help", "h"]:
            cls()
            print("Enter input either by word or first letter")
            print("E.g. 'n' or 'new' for new game.\nTo move use cardinal directions, (North, East, South, West)")
            print("Good luck, try not to die!")
            print("Remember, you can always just use the first letter of any command")
            time.sleep(5)
            game_menu()

        elif cmd in ["quit", "q"]:
            sys.exit()
    else:
        cls()
        game_menu()


def game_loop(player, worldmap):
    steps = 0
    width = shutil.get_terminal_size().columns
    while player["alive"]:
        str(mapview(worldmap)).center(width)
        str(move(worldmap)).center(width)
        steps += 1
        if steps >= 3 and steps % 3 == 0:
            chance = random.randint(0, 10)
            if chance > 4:
                mob = create_mob()
                battle(player, mob)


def new_game():
    # World size
    r_amt = int(input("Region Amount (Default/Max: 6)") or 6)
    l_amt = int(input("Region size (Default/Max: 9)") or 9)
    regions = regiongen(r_amt)
    locations = localgen(r_amt, l_amt, regions)
    world = dict(zip(regions.values(), locations.values()))
    worldmap = worldmaps(world, regions, r_amt)
    player = new_hero()
    game_loop(player, worldmap)


if __name__ == 'main':
    game_menu()
