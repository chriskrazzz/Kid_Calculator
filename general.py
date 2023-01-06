import pandas as pd
from typing import Iterable

#   LISTS
stat_list = ['HP', 'Str', 'Mag', 'Skl', 'Spd', 'Lck', 'Def', 'Res']
games = ['Awakening', 'Fates', 'Genealogy']
ava_games = ['Awakening', 'Fates']

fates_talents = ['Cavalier', 'Ninja', 'Fighter', 'Oni Savage', 'Sky Knight', 'Wyvern Rider', 'Outlaw', 'Archer',
                 'Knight', 'Mercenary', 'Samurai', 'Spear Fighter', 'Apothecary', 'Dark Mage', 'Diviner', 'Troubadour',
                 'Monk', 'Shrine Maiden']
fates_special1 = ['Songstress']  # only for azura
fates_special2 = ['Kitsune', 'Wolfskin', 'Nohr Prince(ss)', 'Villager']  # only inherited, no friend/partner seals
fates_dlc = ['Lodestar', 'Vanguard', 'Grandmaster', 'Great Lord', 'Dread Fighter', 'Ballistician', 'Witch',
             'Dark Falcon']

awa_regular = ['Cavalier', 'Myrmidon', 'Archer', 'Thief', 'Mage', 'Dark Mage', 'Knight',
               'Mercenary', 'Wyvern Rider']
awa_male = ['Barbarian', 'Fighter', 'Priest']
awa_female = ['Troubadour', 'Pegasus Knight', 'Cleric']
awa_special1 = ['Villager']
awa_special2 = ['Taguel', 'Manakete']  # only morgan can inherit
awa_special3 = ['Dancer', 'Conqueror']

three_classes = ['Swordmaster', 'Assassin', 'Fortress Knight', 'Paladin', 'Sniper', 'Wyvern Lord', 'Mortal Savant',
                 'Great Knight', 'Bow Knight', 'Dark Knight', 'Holy Knight', 'Trickster', 'War Cleric']
three_classes_male = ['Hero', 'Warlock', 'Dark Bishop', 'Bishop', 'War Master']
three_classes_female = ['Warrior', 'Falcon Knight', 'Gremory', 'Dark Flier', 'Valkyrie']

new_mystery_gender = ['Myrmidon', 'Cavalier', 'Archer', 'Mage']

#   DICTS

# fates classes
fates_gender_class = {
    'Monk': 'Shrine Maiden',
    'Shrine Maiden': 'Monk',
    'Troubadour F': 'Troubadour M',
    'Troubadour M': 'Troubadour F',
    'Maid': 'Butler',
    'Butler': 'Maid'
}

parallel_class = {
    'Nohr Prince(ss)': None,
    'Cavalier': 'Ninja',
    'Knight': 'Spear Fighter',
    'Fighter': 'Oni Savage',
    'Mercenary': 'Samurai',
    'Outlaw': 'Archer',
    'Samurai': 'Mercenary',
    'Oni Savage': 'Fighter',
    'Spear Fighter': 'Knight',
    'Diviner': 'Dark Mage',
    'Monk': None,
    'Shrine Maiden': None,
    'Sky Knight': 'Wyvern Rider',
    'Archer': 'Outlaw',
    'Wyvern Rider': 'Sky Knight',
    'Ninja': 'Cavalier',
    'Apothecary': None,
    'Dark Mage': 'Diviner',
    'Troubadour F': None,
    'Troubadour M': None,
    'Wolfskin': 'Outlaw',
    'Kitsune': 'Apothecary',
    'Songstress': 'Troubadour',
    'Villager': 'Apothecary'
}

fates_promotions = {
    'Nohr Prince(ss)': ['Nohr Noble', 'Hoshido Noble'],
    'Cavalier': ['Paladin', 'Great Knight'],
    'Knight': ['General', 'Great Knight'],
    'Fighter': ['Berserker', 'Hero'],
    'Mercenary': ['Hero', 'Bow Knight'],
    'Outlaw': ['Adventurer', 'Bow Knight'],
    'Wyvern Rider': ['Wyvern Lord', 'Malig Knight'],
    'Dark Mage': ['Dark Knight', 'Sorcerer'],
    'Troubadour F': ['Strategist', 'Maid'],
    'Troubadour M': ['Strategist', 'Butler'],
    'Wolfskin': ['Wolfssegner'],
    'Samurai': ['Swordmaster', 'Master of Arms'],
    'Villager': ['Master of Arms', 'Merchant'],
    'Apothecary': ['Merchant', 'Mechanist'],
    'Ninja': ['Master Ninja', 'Mechanist'],
    'Oni Savage': ['Oni Chieftain', 'Blacksmith'],
    'Spear Fighter': ['Spear Master', 'Basara'],
    'Diviner': ['Basara', 'Onmyoji'],
    'Monk': ['Onmyoji', 'Great Master'],
    'Shrine Maiden': ['Onmyoji', 'Priestess'],
    'Sky Knight': ['Falcon Knight', 'Kinshi Knight'],
    'Archer': ['Sniper', 'Kinshi Knight'],
    'Kitsune': ['Nine-Tails']
}

# awakening classes
awakening_gender_class = {
    'Priest': 'Cleric',
    'Cleric': 'Priest',
    'War Monk': 'War Cleric',
    'War Cleric': 'War Monk'
}

awakening_parallel_class = {
    'Avatar': {'Fighter': 'Pegasus Knight', 'Barbarian': 'Troubadour', 'Pegasus Knight': 'Fighter',
               'Troubadour': 'Barbarian'},
    'Vaike': {'Fighter': 'Knight', 'Barbarian': 'Mercenary'},
    'Gaius': {'Fighter': 'Pegasus Knight'},
    'Donnel': {'Villager': 'Pegasus Knight', 'Fighter': 'Troubadour'},
    'Gregor': {'Barbarian': 'Troubadour'},
    'Henry': {'Barbarian': 'Troubadour'},
    'Lissa': {'Pegasus Knight': 'Myrmidon', 'Troubadour': 'Barbarian'},
    'Miriel': {'Troubadour': 'Barbarian'},
    'Maribelle': {'Pegasus Knight': 'Cavalier', 'Troubadour': 'Priest'},
    'Olivia': {'Dancer': 'Mercenary', 'Pegasus Knight': 'Barbarian'},
    'Panne': {'Wyvern Rider': 'Barbarian'},
    'Cherche': {'Troubadour': 'Fighter'}
}

awakening_promotions = {
    'Lord': ['Great Lord'],
    'Tactician': ['Grandmaster'],
    'Cavalier': ['Paladin', 'Great Knight'],
    'Knight': ['General', 'Great Knight'],
    'Fighter': ['Warrior', 'Hero'],
    'Mercenary': ['Hero', 'Bow Knight'],
    'Thief': ['Trickster', 'Assassin'],
    'Wyvern Rider': ['Wyvern Lord', 'Griffon Rider'],
    'Dark Mage': ['Dark Knight', 'Sorcerer'],
    'Mage': ['Dark Knight', 'Sage'],
    'Cleric': ['War Cleric', 'Sage'],
    'Priest': ['War Monk', 'Sage'],
    'Troubadour': ['Valkyrie', 'War Cleric'],
    'Myrmidon': ['Swordmaster', 'Assassin'],
    'Barbarian': ['Berserker', 'Warrior'],
    'Pegasus Knight': ['Falcon Knight', 'Dark Flier'],
    'Archer': ['Sniper', 'Bow Knight'],
}

# other classes
sacred_stones_promotions = {
    'Lord': ['Great Lord'],
    'Cavalier': ['Paladin', 'Great Knight'],
    'Knight': ['General', 'Great Knight'],
    'Fighter': ['Warrior', 'Hero'],
    'Mercenary': ['Hero', 'Ranger'],
    'Thief': ['Rogue', 'Assassin'],
    'Wyvern Rider': ['Wyvern Lord', 'Wyvern Knight'],
    'Shaman': ['Druid', 'Summoner'],
    'Mage': ['Mage Knight', 'Sage'],
    'Monk': ['Bishop', 'Sage'],
    'Cleric': ['Valkyrie', 'Bishop'],
    'Priest': ['Bishop', 'Sage'],
    'Troubadour': ['Valkyrie', 'Mage Knight'],
    'Myrmidon': ['Swordmaster', 'Assassin'],
    'Pirate': ['Berserker', 'Warrior'],
    'Pegasus Knight': ['Falcon Knight', 'Wyvern Knight'],
    'Archer': ['Sniper', 'Ranger'],
}

echoes_promotions = {
    'Villager M': ['Dread Fighter', 'Baron', 'Sage', 'Gold Knight', 'Bow Knight'],
    'Villager F': ['Saint', 'Priestess', 'Falcon Knight', 'Gold Knight'],
    'Soldier': ['Baron'],
    'Knight': ['Baron'],
    'Cavalier': ['Gold Knight'],
    'Paladin': ['Gold Knight'],
    'Pegasus Knight': ['Falcon Knight'],
    'Cleric': ['Saint'],
    'Archer': ['Bow Knight'],
    'Mercenary': ['Dread Fighter'],
    'Myrmidon': ['Dread Fighter'],
    'Mage M': ['Sage'],
    'Mage F': ['Priestess']
}

shadow_dragon_promotions = {
    'Cavalier': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Archer': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Mage': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Myrmidon': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Curate': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Knight': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Mercenary': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Fighter': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Hunter': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Pirate': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Dark Mage': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Pegasus Knight': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Cleric': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop']
}

shadow_dragon_promotion_max = {
    'Lord': 2,
    'Ballistician': 3,
    'Manakete': 4,
    'Thief': 3,
    'Freelancer': 2,
    'Paladin': 11,
    'Dracoknight': 6,
    'Sniper': 5,
    'Swordmaster': 4,
    'Sage': 5,
    'Bishop': 6,
    'General': 7,
    'Hero': 5,
    'Warrior': 5,
    'Horseman': 4,
    'Berserker': 2,
    'Sorcerer': 2
}

new_mystery_promotions = {
    'Cavalier M': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Archer M': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Mage M': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Myrmidon M': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Curate': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Dracoknight': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop'],
    'Knight': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Mercenary': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Fighter': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Hunter': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Pirate': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Dark Mage': ['General', 'Hero', 'Warrior', 'Horseman', 'Berserker', 'Sorcerer'],
    'Cavalier F': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop', 'Falcon Knight', 'General'],
    'Archer F': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop', 'Falcon Knight', 'General'],
    'Mage F': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop', 'Falcon Knight', 'General'],
    'Myrmidon F': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop', 'Falcon Knight', 'General'],
    'Cleric': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop', 'Falcon Knight', 'General'],
    'General': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop', 'Falcon Knight', 'General'],
    'Pegasus Knight': ['Paladin', 'Dracoknight', 'Sniper', 'Swordmaster', 'Sage', 'Bishop', 'Falcon Knight', 'General']
}

new_mystery_promotion_max = {
    'Lord': 2,
    'Manakete': 4,
    'Thief': 3,
    'Freelancer': 2,
    'Paladin': 15,
    'Dracoknight': 6,
    'Sniper': 6,
    'Swordmaster': 6,
    'Sage': 7,
    'Bishop': 5,
    'General': 7,
    'Hero': 5,
    'Warrior': 7,
    'Horseman': 7,
    'Berserker': 2,
    'Sorcerer': 2,
    'Falcon Knight': 2,
    'Dancer': 2
}

# other
boba = pd.read_csv('boons.csv', index_col=0) \
    .fillna(0) \
    .astype(int)

boons_fates = boba.loc['HP':'Res', 'FHP':'FRes']
boons_fates.columns = boons_fates.columns.str[1:]
boons_fates = boons_fates.to_dict(orient='index')

banes_fates = boba.loc['RHP':'RRes', 'FHP':'FRes']
banes_fates.columns = banes_fates.columns.str[1:]
banes_fates = banes_fates.transpose()
banes_fates.columns = banes_fates.columns.str[1:]
banes_fates = banes_fates.transpose()
banes_fates = banes_fates.to_dict(orient='index')

boons_awakening = boba.loc['HP':'Res', 'AHP':'ARes']
boons_awakening.columns = boons_awakening.columns.str[1:]
boons_awakening = boons_awakening.to_dict(orient='index')

banes_awakening = boba.loc['RHP':'RRes', 'AHP':'ARes']
banes_awakening.columns = banes_awakening.columns.str[1:]
banes_awakening = banes_awakening.transpose()
banes_awakening.columns = banes_awakening.columns.str[1:]
banes_awakening = banes_awakening.transpose()
banes_awakening = banes_awakening.to_dict(orient='index')


boons_dict = {'Fates': boons_fates, 'Awakening': boons_awakening}
banes_dict = {'Fates': banes_fates, 'Awakening': banes_awakening}

blood_dict = pd.read_csv('holy_blood.csv', index_col=0) \
    .fillna(0) \
    .astype(int) \
    .to_dict(orient='index')


class SetWithSubset(set):
    """Set should only be initialized with arguments if they should not be
    in a subset.
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.parent = None

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

    def add(self, element):
        super().add(element)
        if self.parent is not None:
            self.parent.add(element)

    def remove(self, element) -> None:
        super().remove(element)
        for key, subset in self.get_subsets().items():
            if element in subset:
                self.__getattribute__(key).remove(element)

    def create_subset(self, name, values=None):
        if values is None:
            values = []
        if name in self.get_subsets():
            raise ValueError(f"Subset with name '{name}' already exists.")
        self.update(values)
        self[name] = SetWithSubset(values)
        self[name].parent = self

    def get_subsets(self):
        result = vars(self).copy()
        result.pop('parent')
        return result

    def pop(self):
        result = super().pop()
        self.add(result)
        self.remove(result)
        return result

    def not_in_subset(self) -> set:
        result = set(self)
        for subset in self.get_subsets().values():
            for element in subset:
                try:
                    result.remove(element)
                except KeyError:
                    continue
        return result

    def copy(self) -> 'SetWithSubset':
        result = SetWithSubset()
        for tag, subset in self.get_subsets().items():
            result.create_subset(tag)
            for element in subset:
                result.__getattribute__(tag).add(element)
        for element in self.not_in_subset():
            result.add(element)
        return result

    def update(self, *s: Iterable) -> None:
        for t in s:
            if isinstance(t, SetWithSubset):
                for tag, subset in t.get_subsets().items():
                    try:
                        self.__getattribute__(tag).update(subset)
                    except AttributeError:
                        self.create_subset(tag, subset)

                for element in t.not_in_subset():
                    self.add(element)
            else:
                for element in t:
                    self.add(element)

    def union(self, *s: Iterable) -> 'SetWithSubset':
        result = self.copy()
        for t in s:
            if isinstance(t, SetWithSubset):
                for tag, subset in t.get_subsets().items():
                    try:
                        result.__getattribute__(tag).update(subset)
                    except AttributeError:
                        result.create_subset(tag, subset)
                for element in t.not_in_subset():
                    result.add(element)
            else:
                for element in t:
                    result.add(element)
        return result


def stat_cap(stat):
    """Function that ensures stats are capitalized correctly. Raises ValueError if not a recognized stat or 'Tot'"""
    check = stat.lower()

    if check == "tot":
        return "Tot"

    if check == "hp":
        return "HP"
    else:
        stat = stat.capitalize()
    if stat in stat_list:
        return stat
    else:
        raise ValueError(f"{stat} is not a valid stat.")


def partner_seal(char1, char2):
    """returns class that char1 would gain via partner seal with char2"""
    new_class = char2.class_set[0]
    if new_class in fates_special1 + fates_special2:
        # class can't be partner-sealed
        new_class = char2.class_set[1]
        if new_class == char1.class_set[0]:
            # secondary of partner is first of unit
            new_class = parallel_class[char2.class_set[0]]
            if new_class is None:
                # Corrin (Nohr Prince(ss)) does not have a parallel class, so parallel of secondary
                # is given instead
                new_class = parallel_class[char2.class_set[1]]
    elif new_class == char1.class_set[0]:
        # primary of partner is first of unit
        new_class = char2.class_set[1]
    if new_class in fates_gender_class and char1.gender != char2.gender:
        new_class = fates_gender_class[new_class]
    elif new_class == 'Troubadour':
        new_class += (' ' + char1.gender.capitalize())
    return new_class


def friend_seal(char1, char2):
    """returns class that char1 would gain via friend seal with char2"""
    new_class = char2.class_set[0]
    if new_class in fates_special1 + fates_special2:
        # class can't be partner-sealed
        new_class = char2.class_set[1]
        if new_class == char1.class_set[0]:
            # secondary of partner is first of unit
            new_class = parallel_class[char2.class_set[0]]
            if new_class is None:
                # Corrin (Nohr Prince(ss)) does not have a parallel class, so parallel of secondary
                # is given instead
                new_class = parallel_class[char2.class_set[1]]
    elif new_class == char1.class_set[0]:
        # primary of partner is first of unit
        new_class = char2.class_set[1]
    if new_class == 'Troubadour':
        new_class += (' ' + char1.gender.capitalize())
    return new_class


def inherit_class_single(char):
    """Gives kid first possible class, it will always have this, but there is a seperate function for 2 known parents,
    since it works differently then (looking at you azura).
    """
    dad = char.dad
    new_class = dad.class_set[0]
    if new_class in fates_special1:
        # class can't be inherited
        new_class = dad.class_set[1]
        if new_class == char.class_set[0]:
            # secondary of parent is first of unit
            new_class = parallel_class[dad.class_set[0]]
    elif new_class == char.class_set[0]:
        # primary of partner is first of unit
        new_class = dad.class_set[1]
    if new_class in fates_gender_class and char.gender != char.dad.gender:
        new_class = fates_gender_class[new_class]
    elif new_class == 'Troubadour':
        new_class += (' ' + char.gender.capitalize())
    return new_class


def inherit_class_married(char, mom):
    """Father passes down first, even for Azura. Returns third class for this character. Important: Shigure's second
    will always be troubadour, even if inherited from Azura"""
    dad = char.dad
    new_class = mom.class_set[0]
    if new_class in fates_special1:
        # class can't be inherited
        new_class = mom.class_set[1]
        if new_class == char.class_set[0]:
            # secondary of parent is first of unit
            new_class = parallel_class[mom.class_set[0]]
    elif new_class == char.class_set[0]:
        # primary of mom is first of unit
        new_class = mom.class_set[1]
    elif new_class == char.class_set[1]:
        # gets same class from both parents
        if mom.gender == 'f':
            # default behaviour
            new_class = mom.class_set[1]
        else:
            # Set parent is Azura or F!Corrin
            new_class = parallel_class[dad.class_set[1]]
    if new_class in fates_gender_class and char.gender != mom.gender:
        new_class = fates_gender_class[new_class]
    elif new_class == 'Troubadour':
        new_class += (' ' + char.gender.capitalize())
    return new_class


def awa_inherit_dad(char):
    result = []
    dad = char.dad
    for class_ in dad.class_set:
        if class_ in awa_special3:
            continue
        elif class_ in awa_special2 and dad.name == 'Avatar':
            result.append(class_)
        elif class_ in awa_special1 and char.gender == 'm':
            result.append(class_)
        elif char.gender != dad.gender and (class_ in awa_male + awa_female or (dad.name == 'Panne' and
                                            class_ == 'Wyvern Rider')):
            try:
                class_ = awakening_gender_class[class_]
            except KeyError:
                class_ = awakening_parallel_class[dad.name][class_]
            result.append(class_)
        else:
            result.append(class_)
    return result


def awa_inherit_mom(char, mom):
    result = []
    for class_ in mom.class_set:
        if class_ in awa_special3:
            continue
        elif class_ in awa_special2 and char.dad.name == 'Avatar':
            result.append(class_)
        elif class_ in awa_special1 and char.gender == 'm':
            result.append(class_)
        elif char.gender != mom.gender and (class_ in awa_male + awa_female or (mom.name == 'Panne' and
                                                                                class_ == 'Wyvern Rider')):
            try:
                class_ = awakening_gender_class[class_]
            except KeyError:
                class_ = awakening_parallel_class[mom.name][class_]
            result.append(class_)
        else:
            result.append(class_)
    return result


if __name__ == '__main__':
    A = SetWithSubset()
    A.create_subset("check")
    A.add(5)
    A.check.add(10)
    C = set(A)
    B = A.copy()
    D = SetWithSubset([4,6])
    D.create_subset('p', [10, 0, 1.1])
    print(A)
    print(D)
    print(A.union(D))
    print(A)
    A.update(D)
    print(A.p)
    print(set(A))
    print(A.check)
    print(B.check)

