import pandas as pd
from random import choice, shuffle
from collections import Counter
from general import fates_talents, three_classes, three_classes_male, three_classes_female, shadow_dragon_promotion_max\
    , new_mystery_gender, new_mystery_promotion_max
from database import Database
from character import Character

fates_games = ['Conquest', 'Birthright', 'Revelations']
db_games = ['Awakening'] + fates_games
ava_games = db_games + ['New Mystery', 'Three Houses']
other_games = ['Echoes', 'Sacred Stones', 'Shadow Dragon', 'New Mystery'] + db_games
possible_games = db_games + other_games
versions = ['Silver Snow', 'Azure Moon', 'Crimson Flower', 'Verdant Wind']


class OtherDB:
    game: str
    gender: str
    char: dict
    """For non DB Games that only require minimal features."""
    def __init__(self, game):
        self.game = game

    @staticmethod
    def load_file(game: str, gender=None):
        """gender only for new mystery and Three Houses"""
        result = OtherDB(game)
        result.gender = gender
        char_dict = dict()

        version = None
        if game in versions:
            version = game
            game = 'Three Houses'
        path = game.lower().replace(' ', '_') + '.csv'

        db = pd.read_csv(path)
        match version:
            case 'Azure Moon':
                db = db.loc[db['Availability'].str.contains('a', na=False)]
            case 'Crimson Flower':
                db = db.loc[db['Availability'].str.contains('c', na=False)]
            case 'Verdant Wind':
                db = db.loc[db['Availability'].str.contains('v', na=False)]
            case 'Silver Snow':
                db = db.loc[db['Availability'].str.contains('s', na=False)]

        for i, row in db.iterrows():
            name = row['Name']
            char_info = Character(name, game)

            if game in ['Three Houses', 'New Mystery', 'Echoes']:
                char_info.gender = row['Gender']
                if char_info.gender == 'b':
                    # this is kris
                    match gender:
                        case 'f':
                            char_info.gender = 'f'
                            char_info.add_class('Pegasus Knight')
                        case 'm':
                            char_info.gender = 'm'
                            char_info.add_class(choice(['Mercenary', 'Cavalier M']))

            for _, class_ in row.filter(regex='Class').items():
                if not pd.isnull(class_):
                    if game == 'Echoes' and (class_ == 'Villager' or class_ == 'Mage'):
                        class_ += ' ' + char_info.gender.upper()
                    elif game == 'New Mystery' and class_ in new_mystery_gender:
                        class_ += ' ' + char_info.gender.upper()
                    char_info.add_class(class_)

            match game:
                case 'Echoes':
                    if not pd.isnull(row['Exclusive']):
                        char_info.exclusive = [row['Exclusive']]
                    elif row['Lord'] == 'y':
                        char_info.lord = True
                case 'Three Houses':
                    if row['Dancer'] == 'y':
                        char_info.add_class('Dancer')
                    match char_info.gender:
                        case 'f':
                            for class_ in three_classes + three_classes_female:
                                char_info.add_class(class_)
                        case 'm':
                            for class_ in three_classes + three_classes_male:
                                char_info.add_class(class_)
                case 'Shadow Dragon':
                    for _, char2 in row.filter(regex='Exclusive').items():
                        if not pd.isnull(char2):
                            char_info.exclusive.append(char2)

            char_dict[name] = char_info

        result.char = char_dict
        return result

    def randomize_classes(self, mode):
        """mode is either 'minimal', then every class will be assigned to one character, or 'maximal', where every
                character gets a random class, which will cause duplicates (though it tries to avoid it).
                DLC classes will always be limited to 1
                """
        dlc = False
        match self.game:
            case 'Three Houses':
                dlc = ['Dancer']
                # there can be only one
            case 'Echoes':
                j = 3
                possible_char = list(self.char.values())
                shuffle(possible_char)
                while j > 0:
                    """There is a small chance that both Sonya and Deen get it, which isn't possible"""
                    candidate = possible_char.pop()
                    if not candidate.lord and ('Villager M' not in candidate.classes)\
                            and ('Villager F' not in candidate.classes):
                        candidate.add_class('Villager' + ' ' + candidate.gender.upper())
                        j -= 1

        if mode not in ['minimal', 'maximal']:
            raise ValueError

        result = dict()
        leftover = []
        for char in self.char.values():
            leftover.append(char)

        shuffle(leftover)
        done = Counter()
        i = 0
        excluded = []
        while len(leftover) > i:
            added = False
            char = leftover[i]
            # currently only for Deen and Sonya
            if char.name in excluded:
                i += 1
                if i >= len(leftover):
                    break
                continue

            excluded += char.exclusive

            classes = char.promoted
            shuffle(classes)
            for class_ in classes:
                if class_ not in done:
                    done[class_] += 1
                    leftover.pop(i)
                    result[char.name] = class_
                    added = True
                    break
            if not added:
                if mode == 'minimal':
                    i += 1
                    if i >= len(leftover):
                        break
                elif mode == 'maximal':
                    no_dlc = False
                    class_ = None
                    if dlc:
                        while not no_dlc:
                            class_ = choice(classes)
                            if class_ not in dlc:
                                no_dlc = True
                    elif self.game == 'Shadow Dragon':
                        for _class in classes:
                            if done[_class] + 1 <= shadow_dragon_promotion_max[_class]:
                                class_ = _class
                                break
                    elif self.game == 'New Mystery':
                        for _class in classes:
                            if done[_class] + 1 <= new_mystery_promotion_max[_class]:
                                class_ = _class
                                break
                    else:
                        class_ = choice(classes)
                    result[char.name] = class_
                    leftover.pop(i)
                    done[class_] += 1
        leftover = [char.name for char in leftover]
        return result, leftover


class Randomizer:
    def __init__(self, game):
        while not game_check(game):
            game = input(f"{game} is not valid, please enter a valid game:\n")
        self.version = game
        if game in versions:
            game = 'Three Houses'

        self.game = game
        # for games with avatar gender is already randomized here
        self._load_db()

    def randomize(self, mode='maximal'):
        return self.db.randomize_classes(mode)  # returns a tuple: list of result and leftover

    def _load_db(self):
        if self.game in fates_games:
            gender = choice(['f', 'm'])
            talent = choice(fates_talents[:-1])
            if talent == 'Monk' and gender == 'f':
                talent = 'Shrine Maiden'
            self.db = Database.load_file(self.game, ('Skl', 'Lck'), gender, talent)
        elif self.game in db_games:
            gender = choice(['f', 'm'])
            self.db = Database.load_file(self.game, ('Skl', 'Lck'), gender)
        elif self.game in ava_games:
            gender = choice(['f', 'm'])
            self.db = OtherDB.load_file(self.version, gender)
        else:
            self.db = OtherDB.load_file(self.game)


def game_check(game):
    if game == 'Three Houses':
        return False
    elif game in versions:
        return True
    elif game in possible_games:
        return True
    return False


if __name__ == '__main__':
    t = Randomizer('New Mystery')

    result, leftover = t.randomize()

    for name, class_ in result.items():
        print(f"{name} should become a {class_}.")
    for name in leftover:
        print(f"{name} was left over.")

