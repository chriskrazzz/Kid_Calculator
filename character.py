import pandas as pd
from general import stat_list, games, blood_dict, fates_promotions, awakening_promotions, sacred_stones_promotions, \
    echoes_promotions, shadow_dragon_promotions, new_mystery_promotions


class Character:
    """Class for character, keeps track of their stats and possible pairings."""
    def __init__(self, name: str,  game: str) -> None:
        """Dad is the parent who will always be the parent of this child. If reverse, this is a parent of which
        you would not expect them to give children (e.g. females in fates / males in awakening) but do, like Azura.
        """
        self.name = name
        self.game = game
        self._stats = dict()
        self.dad = None
        self.pair = set()
        self.aptitude = False
        self.boon = ''
        self.bane = ''
        self.kid = []
        self.mom = None
        self.minor = []
        self.major = ''
        self.gender = ''
        self.swap = False
        self.class_set = []  # these are the 'set classes'
        self.available_classes = []  # classes that this child can have after inheritance from free parent, otherwise
        # equal to class set
        self.classes = []  # these are all the classes this character can have access to somehow
        self.promoted = []  # these are all promoted (or special) classes the character can have
        self.friends = []  # friends
        self.exclusive = []
        self.lord = False
        self.dancer = False

    def __str__(self):
        string = f"{self.name}:\n"
        for stat, value in self.stats.items():
            string = string + f"    {stat}: {value}\n"
        string = string[:-1]
        return string

    @property
    def summary(self):
        string = f"{self.name}:\n"
        for stat, value in self.stats.items():
            string = string + f"    {stat}: {value}\n"
        string = string[:-1]
        if self.dad:
            string = string + f"\n  Set parent: {self.dad.name}."
        if self.mom:
            string = string + f"\n  Free parent: {self.mom.name}."
        if self.grandpa:
            string = string + f"\n  {self.name} is a grandchild.\n  Set parent of {self.mom.name}: {self.grandpa.name}."
            string = string + f"\n  Free parent of {self.mom.name}: {self.grandma.name}."
        if self.aptitude:
            string = string + f"\n  {self.name} has aptitude."
        if self.boon and self.bane:
            string = string + f"\n  {self.name} is affected by the Avatar's boon and bane: {self.boon} and" \
                              f" {self.bane}."
        if self.minor:
            string = string + f"\n  {self.name} has the following minor blood: "
            for blood in self.minor:
                string = string + f"{blood}, "
            string = string[:-2] + '.'
        if self.major:
            string = string + f"\n  {self.name} has the following major blood: {self.major}."
        if self.pair:
            string = string + f"\n {self.name} can marry the following people:\n"
            for person in self.pair:
                string = string + person.name + ', '
            string = string[:-2]
        return string

    @property
    def grandpa(self):
        return self.mom.dad if self.mom else None

    @property
    def grandma(self):
        return self.mom.mom if self.mom else None

    @property
    def total(self):
        return sum(self.stats.values())

    @property
    def stats(self):
        result = self._stats.copy()
        if self.aptitude:
            if self.game == 'Awakening':
                for stat in result:
                    result[stat] += 20
            else:
                for stat in result:
                    result[stat] += 10
        if self.minor:
            for minor_blood in self.minor:
                for stat in result:
                    result[stat] += blood_dict[minor_blood][stat]
        if self.major:
            for stat in result:
                result[stat] += blood_dict[self.major][stat] * 2
        return result

    @stats.setter
    def stats(self, new_stats):
        self._stats = new_stats

    @property
    def true_stats(self):
        return self._stats

    def add_class(self, new_class) -> bool:
        if new_class not in self.class_set:
            self.class_set.append(new_class)
            self.add_available(new_class)
            return True
        else:
            return False

    def add_available(self, new_class):
        if new_class not in self.available_classes:
            self.available_classes.append(new_class)
            self.add_possible(new_class)
            return True
        else:
            return False

    def add_possible(self, new_class):
        if new_class not in self.classes:
            self.classes.append(new_class)
            self._add_promoted(new_class)
            return True
        else:
            return False

    def _add_promoted(self, new_class):
        try:
            match self.game:
                case 'Fates':
                    promotions = fates_promotions[new_class]
                case 'Awakening':
                    promotions = awakening_promotions[new_class]
                case 'Sacred Stones':
                    promotions = sacred_stones_promotions[new_class]
                case 'Echoes':
                    promotions = echoes_promotions[new_class]
                case 'Three Houses':
                    promotions = [new_class]
                case 'Shadow Dragon':
                    promotions = shadow_dragon_promotions[new_class]
                case 'New Mystery':
                    promotions = new_mystery_promotions[new_class]
                case _:
                    print('Warning: Unrecognized game')
                    promotions = [new_class]
        except KeyError:
            promotions = [new_class]
        for promotion in promotions:
            self._add_promotion(promotion)

    def _add_promotion(self, new_class):
        if new_class not in self.promoted:
            self.promoted.append(new_class)
            return True
        return False

    def add_friend(self, new_friend):
        if new_friend not in self.friends:
            self.friends.append(new_friend)
            return True
        return False

    @staticmethod
    def load_char(line: pd.DataFrame, game: str) -> 'Character':
        """Loads a character from a string line."""
        if not isinstance(line, pd.Series):
            raise TypeError

        if type(game) != str:
            raise TypeError
        elif game not in games:
            print(game)
            raise ValueError

        # extract name
        name = line['Name']

        # stat extraction
        stat_dict = dict()
        for stat in stat_list:
            stat_dict[stat] = line[stat]

        result = Character(name, game)
        result.stats = stat_dict

        # gender (more accurately, sex, but I don't want to write sex everytime I reference it.)
        result.gender = line['Gender']

        # temporary dad set to true if child, because that way the program can easily check if it is a child
        if not pd.isnull(line['Role']) and 'c' in line['Role']:
            # char is a child
            result.dad = True

        if game == 'Genealogy':
            if not pd.isnull(line['Minor']):
                result.minor = [line['Minor']]
            if not pd.isnull(line['Major']):
                result.major = line['Major']

            # check for Febail and Patty, their blood inheritance is swapped.
            if line['Swap'] == 'y':
                result.swap = True
        else:
            # aptitude check
            if line['Aptitude'] == 'y':
                result.aptitude = True

        return result


if __name__ == '__main__':
    pass
