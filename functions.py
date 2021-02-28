import random
from classes import Artifact
from dictionaries import *

global inventory
inventory = {}

# convert numStats list to int
def listToInt(num):
    s = ''.join(map(str, num))
    return int(s)

# options menu
def menu():
    print('\n----------- GENSHIN ARTIFACT SIMULATOR -----------\n'
          '|              1. FARM ARTIFACTS                 |\n'
          '|              2. ENHANCE ARTIFACTS              |\n'
          '|              3. VIEW INVENTORY                 |\n'
          '|              4. EXIT SIMULATOR                 |\n'
          '--------------------------------------------------\n')

    while True:
        try:
            option = int(input('Select an option: '))
        except (ValueError, TypeError, KeyError, IndexError):
            print('\nPlease enter a valid option.\n')
        else:
            if option in range(1, 5):
                if option == 1:
                    farm_artifact()
                elif option == 2:
                    enhance_artifact()
                elif option == 3:
                    view_artifacts()
                    menu()
                else:
                    exit()
            else:
                print('\nPlease enter a valid option.\n')

# roll artifact set, type
def artifact_roll(domain):
    sets = artifact_sets.get(domain).split(',')
    artifact_set = random.choice(sets)
    artifact_type = random.choice(artifact_types)
    return [artifact_set, artifact_type]

# roll mainstat
def mainstat_roll(artifactType):
    possible_main = mainstat_dict.get(artifactType).split(',')
    return random.choice(possible_main)

# roll 4 substats
def substats_roll():
    roll_list = []
    numStats = random.choices([3, 4], [0.8, 0.2])
    noOfStats = listToInt(numStats)
    stats_rolled = random.sample([*substats_dict.keys()], int(noOfStats))

    for stat in stats_rolled:
        roll_values = substats_dict.get(stat).split(',')
        value = random.choice(roll_values)
        roll = stat + ": " + value
        roll_list.append(roll)

    return roll_list

# generates the artifact for the respective domain
def artifact_gen(domain):
    artifact_index = len(inventory) + 1
    artifactPiece = artifact_roll(str(domain))
    mainStat = mainstat_roll(artifactPiece[1])
    mainStatValue = mainStat_upgrades.get(mainStat).split(',')[0]
    subStats = substats_roll()
    artifact = Artifact(artifactPiece[0], artifactPiece[1], mainStat, mainStatValue, subStats)

    inventory[str(artifact_index)] = artifact

    print('\n' + artifact.name +
          "\nSlot: " + str(artifact.slot) +
          "\nMain Stat: " + str(artifact.mainStat))
    print(*[i for i in artifact.subStat], sep='\n')
    continue_farm(domain)

# prompts to continue farming
def continue_farm(domain):
    artifact_index = len(inventory) + 1
    try:
        print('\n=========== OPTIONS ===========: '
              '\n1. Continue Farming this Domain'
              '\n2. Farm Another Domain'
              '\n3. Return to Menu')
        continueFarm = str(input("\nSelect an Option: "))
    except (ValueError, TypeError, KeyError, IndexError):
        print('\nPlease enter a valid option.\n')
    else:
        if continueFarm == '1':
            artifact_index += 1
            artifact_gen(domain)
        elif continueFarm == '2':
            farm_artifact()
        else:
            print('\nYou have exited the domain!')
            menu()

# consolidated function for artifacts farming
def farm_artifact():
    while True:
        print('\nAvailable Artifact Domains:\n'
              '1. Midsummer Courtyard (TF, TS)\n'
              '2. Valley of Remembrance (VV, MB)\n'
              '3. Domain of Guyun (AP, RB)\n'
              '4. Hidden Palace of Zhou Formula (CW, LW)\n'
              '5. Clear Pool and Mountain Cavern (NO, BsC)\n'
              '6. Peak of Vindagnyr (BS, HoD)\n')

        try:
            domain = int(input("Which domain no. would you like to farm?: "))
        except (ValueError, TypeError, KeyError, IndexError):
            print('\nPlease enter a valid option.\n')
        else:
            if domain in range(1, 7):
                artifact_gen(domain)
                continue_farm(domain)
            else:
                print('\nPlease enter a valid option.\n')

# view artifact inventory
def view_artifacts():
    if bool(inventory) == False:
        print('\nYour inventory is empty!')
    else:
        index = 1
        for artifact in inventory.values():
            print(str(index) + '. ' + str(artifact))
            index += 1

# enhance selected artifact
def enhance_artifact():
    view_artifacts()

    while True:
        try:
            select_artifact = int(input('\nSelect which artifact you wish to enhance: '))
        except (ValueError, TypeError, KeyError, IndexError):
            print('\nPlease enter a valid option.\n')
        else:
            for key in inventory:
                if str(select_artifact) == key:
                    artifact = inventory.get(key)
                    while True:
                        artifact.enhance()
                        print('\n=========== OPTIONS ===========: '
                              '\n1. Continue Enhancing this Artifact'
                              '\n2. Enhance Another Artifact'
                              '\n3. Return to Menu')
                        try:
                            continueEnhance = int(input('\nSelect an option: '))
                        except (ValueError, TypeError, KeyError, IndexError):
                            print('\nPlease enter a valid option.\n')
                        else:
                            if int(continueEnhance) == 1:
                                continue
                            elif int(continueEnhance) == 2:
                                enhance_artifact()
                            else:
                                menu()
