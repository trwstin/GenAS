import random
from dictionaries import *

class Artifact:
    def __init__(self, name, slot, mainStat, mainStatValue, subStat):
        self.name = name
        self.slot = slot
        self.mainStat = mainStat
        self.mainStatValue = mainStatValue
        self.subStat = subStat
        self.enhances = 0

    def enhance_counter(self):
        self.enhances += 4

    def upgrade_mainStat(self):
        for mainStat in mainStat_upgrades.keys():
            if self.mainStat == mainStat:
                index = round(self.enhances/4)
                mainStatValue = mainStat_upgrades.get(self.mainStat).split(',')[index]
                self.mainStatValue = '{:,.2f}'.format(mainStatValue)

    def add_stat(self):
        statList = [*substats_dict.keys()]
        currentStat = [i.split(':')[0] for i in self.subStat]
        newStat = random.choice([i for i in statList if i not in currentStat])
        newStatValue = random.choice(substats_dict.get(newStat).split(','))

        self.subStat.append(newStat + ': ' + newStatValue)
        self.enhance_counter()
        self.upgrade_mainStat()
        print(f"\nYour artifact has been enhanced with a new substat, {newStat}!\n"
              f"{self.subStat}")

    def upgrade_stat(self):
        index = 0
        upgradedStat = random.choice(self.subStat).split(':')[0]
        upgradedValue = random.choice(substats_dict.get(upgradedStat).split(','))

        for stat in self.subStat:
            statName = stat.split(':')[0]
            if upgradedStat == statName:
                oldStatValue = stat.split(': ')[1]
                newStatValue = round(float(oldStatValue.replace('%', ''))
                                     + float(upgradedValue.replace('%', '')), 1)
                enhancement = statName + ': ' + str(newStatValue).replace('.0', '')
                if '%' in statName:
                    enhancement += '%'
                self.subStat.insert(index, enhancement)
                self.subStat.pop(index + 1)
            index += 1

        self.enhance_counter()
        self.upgrade_mainStat()
        print(f"\nYour artifact\'s {upgradedStat} has been successfully enhanced!\n"
              f"{self.subStat}")

    def enhance(self):
        if self.enhances >= 20:
            print("\nThis artifact has reached the maximum number of enhancements.")
        elif len(self.subStat) == 3:
            self.add_stat()
        elif self.enhances < 20:
            self.upgrade_stat()

    def __repr__(self):
        return f'A +{self.enhances} {self.name} {self.slot}, ' \
               f'with {self.mainStat} Main Stat value of {self.mainStatValue} ' \
               f'and the following Sub Stats: {self.subStat}'
