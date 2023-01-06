from __future__ import annotations
from copy import deepcopy
from random import shuffle, choice
import pandas as pd
from general import SetWithSubset, stat_cap, stat_list, games, ava_games, boons_dict, banes_dict, fates_talents, \
    fates_dlc, partner_seal, inherit_class_single, inherit_class_married, awa_regular, awa_male, \
    awa_female, awa_inherit_dad, awa_inherit_mom, friend_seal

from character import Character


class Database:
    """Class that stores all the information of the characters and calculates all possible pairs."""
    def __init__(self, char_dict) -> None:
        self.char = char_dict

        # all the attributes underneath are empty, simply defined such that they always exist
        self.game = None
        self.kids = SetWithSubset()
        self.boba = ('', '')
        self.ava_kid = None

    @staticmethod
    def load_file(game: str, boba: tuple[str, str] | None = None, gender: str | None = None, talent: str | None = None):
        version = None
        if type(game) != str:
            raise TypeError("Argument game should be a string.")
        game = game.capitalize()

        if game in ['Conquest', 'Revelations', 'Birthright']:
            version = game
            game = 'Fates'

        if game not in games:
            raise ValueError('f{game} not recognized')

        if game in ava_games:
            if type(boba) != tuple:
                raise TypeError("Argument boba should get a tuple of stats as input.")
            elif len(boba) != 2:
                raise ValueError('Argument boba should contain a tuple of 2 values.')
            else:
                try:
                    boba = (stat_cap(boba[0]), stat_cap(boba[1]))
                except ValueError as e:
                    raise ValueError('Argument boba should contain valid stats.') from e
                else:
                    if 'Tot' in boba:
                        raise ValueError('Argument boba should contain valid stats, Tot is not allowed.')
                    elif boba[0] == boba[1]:
                        raise ValueError('Argument boba should contain valid stats, the boon cannot be the same as '
                                         'the bane.')
            if gender != 'f' and gender != 'm':
                raise ValueError('Argument gender should be either m or f to indicate main character gender.')
            if game == 'Fates':
                if type(talent) != str:
                    raise TypeError('Talent should be a string.')
                elif talent not in fates_talents:
                    raise ValueError(f'Talent {talent} not recognized.')
                elif talent == 'Troubadour':
                    talent += (' ' + gender.capitalize())
                elif talent == 'Monk' and gender == 'f':
                    print('Warning: Monk is male only, Shrine Maiden used instead')
                    talent = 'Shrine Maiden'
                elif talent == 'Shrine Maiden' and gender == 'm':
                    print('Warning: Shrine Maiden is female only, Monk used instead')
                    talent = 'Monk'
                # see if revelations, birthright or conquest
                if version is None:
                    version = input('Are you playing Revelations, Birthright or Conquest?\n')
                    while version not in ['Conquest', 'Revelations', 'Birthright']:
                        print('Please put in valid response.')
                        version = input('Are you playing Revelations, Birthright or Conquest?\n')
            elif talent:
                raise ValueError('Awakening does not need talent')

        elif boba or gender or talent:
            raise ValueError('Genealogy does not need a boba, talent or gender argument.')

        # character dictionary, will contain most information about that character. Also kid set, which will be saved
        char_dict = dict()
        kids = SetWithSubset()
        kids.create_subset('males')
        kids.create_subset('females')
        ava_kid = ''

        # character sets, subdivide into groups for pairing later, not remembered by instance
        moms = set()
        dads = set()

        # fates and awakening sets
        nohr = SetWithSubset()
        nohr.create_subset('royals')
        hoshido = SetWithSubset()
        hoshido.create_subset('royals')
        ava = SetWithSubset()
        ava.create_subset('males')
        ava.create_subset('females')

        # this set is only for chrom and lissa
        siblings = set()

        # database initialization using pandas
        db = pd.read_csv(game.lower() + '_growths.csv')
        if version == 'Conquest':
            db = db.loc[~db['Role'].str.contains('h', na=False) & ~db['Group'].str.contains('h', na=False)]
        elif version == 'Birthright':
            db = db.loc[~db['Role'].str.contains('n', na=False) & ~db['Group'].str.contains('n', na=False)]
        elif version == 'Revelations':
            db = db.loc[~db['Role'].str.contains('u', na=False)]

        for i, row in db.iterrows():
            char_info = Database._load_char(char_dict, row['Name'], db, game)
            name = char_info.name

            # add children to child list
            for _, child in row.filter(regex='Child').items():
                if not pd.isnull(child):
                    child_char = Database._load_char(char_dict, child, db, game)
                    char_info.kid.append(child_char)

            ##########################################
            #              Role check                #
            ##########################################
            role = row['Role']
            if not pd.isnull(role) and 'c' in role:
                # char is a child
                dad_char = Database._load_char(char_dict, row['Parent'], db, game)
                char_info.dad = dad_char
                if char_info.gender == 'f':
                    kids.females.add(char_info)
                elif char_info.gender == 'm':
                    kids.males.add(char_info)
                elif char_info.gender == 'b':
                    if gender == 'm':
                        char_info.gender = 'f'
                    else:
                        char_info.gender = 'm'
                    kids.add(char_info)
                    ava_kid = char_info
                else:
                    raise ValueError(f'{gender} is not a gender for {role}.')

            elif not pd.isnull(role) and 'a' in role:
                # this character can only have a child with the avatar
                if char_info.gender == 'f':
                    ava.females.add(char_info)
                elif char_info.gender == 'm':
                    ava.males.add(char_info)
                else:
                    raise ValueError(f'{gender} is not a gender for {role}, {name}.')
            elif pd.isnull(role):
                if char_info.gender == 'm':
                    # this character is a dad
                    dads.add(char_info)
                elif char_info.gender == 'f':
                    # this character is a mom
                    moms.add(char_info)
                elif char_info.gender == 'b':
                    char_info.gender = gender
                    # this is the avatar, determined by user input
                    if gender == 'f':
                        moms.add(char_info)
                    elif gender == 'm':
                        dads.add(char_info)
                else:
                    ValueError(f'{char_info.gender} is not a valid gender for {name}.')
            else:
                raise ValueError(f'{role} is not a valid role for {name}.')

            if game in ava_games:
                # this is not a thing in genealogy, so that game can skip this part.
                ##########################################
                #             Group check                #
                ##########################################
                group = row['Group']
                if pd.isnull(group):
                    pass
                elif group == 'a':
                    nohr.add(char_info)
                    hoshido.add(char_info)
                elif 'n' in group:
                    if group == 'nr':
                        nohr.royals.add(char_info)
                    else:
                        nohr.add(char_info)
                elif 'h' in group:
                    if group == 'hr':
                        hoshido.royals.add(char_info)
                    else:
                        hoshido.add(char_info)
                elif group == 'r':
                    siblings.add(char_info)
                else:
                    raise ValueError(f"Undefined group: {group} for {name}.")

                # special pair addition, only in revelations
                if version == 'Revelations':
                    for _, pair_up in row.filter(regex='Pair').items():
                        if not pd.isnull(pair_up):
                            char_pair = Database._load_char(char_dict, pair_up, db, game)
                            char_info.pair.add(char_pair)

                # friend addition step 1: Hoshido & Rev:
                if version == 'Birthright' or version == 'Revelations':
                    for _, friend in row.filter(regex='Hoshido').items():
                        if not pd.isnull(friend):
                            if friend == 'Kana':
                                # special case because stupid
                                if gender == char_info.gender:
                                    # this means Kana has different gender, so no friends
                                    continue
                                else:
                                    # adds this character as friend for kana
                                    Database._load_char(char_dict, friend, db, game).add_friend(char_info)
                            char_friend = Database._load_char(char_dict, friend, db, game)
                            char_info.add_friend(char_friend)

                # friend addition step 1: Hoshido & Rev:
                if version == 'Conquest' or version == 'Revelations':
                    for _, friend in row.filter(regex='Nohr').items():
                        if not pd.isnull(friend):
                            if friend == 'Kana':
                                # special case because stupid
                                if gender == char_info.gender:
                                    # this means Kana has different gender, so no friends
                                    continue
                                else:
                                    # adds this character as friend for kana
                                    Database._load_char(char_dict, friend, db, game).add_friend(char_info)
                            char_friend = Database._load_char(char_dict, friend, db, game)
                            char_info.add_friend(char_friend)

                # special class addition
                if game == 'Fates':
                    for _, class_ in row.filter(regex='Class').items():
                        if not pd.isnull(class_):
                            if class_ == 'Troubadour':
                                class_ += (' ' + char_info.gender.capitalize())
                            char_info.add_class(class_)
                    if name == 'Avatar':
                        # this is the avatar
                        char_dict[name].add_class(talent)
                    elif char_info.dad:
                        new_class = inherit_class_single(char_info)
                        char_info.add_class(new_class)
                    for new_class in fates_dlc:
                        if new_class in ['Witch', 'Great Lord'] and char_info.gender == 'm':
                            continue
                        if new_class in ['Ballistician', 'Grandmaster'] and char_info.gender == 'f':
                            continue
                        char_info.add_class(new_class)
                else:
                    for _, class_ in row.filter(regex='Class').items():
                        if not pd.isnull(class_):
                            char_info.add_class(class_)
                    if name == 'Avatar':
                        for class_ in awa_regular:
                            char_info.add_class(class_)
                        if gender == 'm':
                            for class_ in awa_male:
                                char_info.add_class(class_)
                        else:
                            for class_ in awa_female:
                                char_info.add_class(class_)
                    elif char_info.dad:
                        to_add = awa_inherit_dad(char_info)
                        for class_ in to_add:
                            char_info.add_class(class_)

        # now, fill pair set for all characters
        for char in char_dict.values():
            if type(char) == dict:
                # this is a kid
                char = char['base']

            if char.name == 'Avatar':
                if char in moms:
                    char.pair.update(dads.union(kids['males'], ava['males']))
                    if game == 'Fates':
                        char.friends = list(moms)
                else:
                    char.pair.update(moms.union(kids['females'], ava['females']))
                    if game == 'Fates':
                        char.friends = list(dads)
            elif game == 'Genealogy':
                # At least this one is simple
                if char in moms:
                    char.pair.update(dads)
                elif char in dads:
                    char.pair.update(moms)
            elif game == 'Fates':
                if char in moms:
                    if char in hoshido['royals']:
                        # hoshidan royal
                        for dad in dads:
                            if dad in hoshido.union(nohr['royals']) and dad not in hoshido['royals']:
                                char.pair.add(dad)
                    elif char in nohr['royals']:
                        for dad in dads:
                            if dad in nohr.union(hoshido['royals']) and dad not in nohr['royals']:
                                char.pair.add(dad)
                    else:
                        if char in hoshido:
                            char.pair.update({dad for dad in hoshido if dad in dads})
                        if char in nohr:
                            char.pair.update({dad for dad in nohr if dad in dads})
                elif char in dads:
                    if char in hoshido['royals']:
                        # hoshidan royal
                        for mom in moms:
                            if mom in hoshido.union(nohr['royals']) and mom not in hoshido['royals']:
                                char.pair.add(mom)
                    elif char in nohr['royals']:
                        for mom in moms:
                            if mom in nohr.union(hoshido['royals']) and mom not in nohr['royals']:
                                char.pair.add(mom)
                    else:
                        if char in hoshido:
                            char.pair.update({mom for mom in hoshido if mom in moms})
                        if char in nohr:
                            char.pair.update({mom for mom in nohr if mom in moms})
                elif gender == 'f' and char in ava['males'].union(kids['males']):
                    char.pair.add(char_dict['Avatar'])
                elif gender == 'm' and char in ava['females'].union(kids['females']):
                    char.pair.add(char_dict['Avatar'])
            else:
                # now Awakening
                if char in moms:
                    if char in siblings:
                        for dad in dads:
                            if char in siblings and dad in siblings:
                                continue
                            char.pair.add(dad)
                    else:
                        char.pair.update(dads)
                elif char in dads:
                    if char in siblings:
                        for mom in moms:
                            if char in siblings and mom in siblings:
                                continue
                            char.pair.add(mom)
                    else:
                        char.pair.update(moms)
                elif gender == 'f' and char in ava['males'].union(kids['males']):
                    char.pair.add(char_dict['Avatar'])
                elif gender == 'm' and char in ava['females'].union(kids['females']):
                    char.pair.add(char_dict['Avatar'])

        # now all possible classes have to be added. Friends aren't implemented yet, so they don't work yet.
        if game == 'Fates':
            # first give all kids the third class
            for kid in kids:
                for mom in kid.dad.pair:
                    new_class = inherit_class_married(kid, mom)
                    kid.add_available(new_class)
            # now partner seals
            for name, char in char_dict.items():
                if type(char) == dict:
                    char = char['base']
                    # this is a kid
                # general non kids
                for char2 in char.pair:
                    new_class = partner_seal(char, char2)
                    if new_class is not None:
                        char.add_possible(new_class)
                # friends
                for char2 in char.friends:
                    new_class = friend_seal(char, char2)
                    if new_class is not None:
                        char.add_possible(new_class)

        elif game == 'Awakening':
            for kid in kids:
                for mom in kid.dad.pair:
                    to_add = awa_inherit_mom(kid, mom)
                    for new_class in to_add:
                        kid.add_available(new_class)

        # finishing touches
        if game in ava_games:
            boons = boons_dict[game]
            banes = banes_dict[game]
            new_stats = dict()
            for stat, value in char_dict['Avatar'].stats.items():
                new_stats[stat] = value + boons[boba[0]][stat] - banes[boba[1]][stat]

            char_dict['Avatar'].stats = new_stats
            char_dict['Avatar'].boon = boba[0]
            char_dict['Avatar'].bane = boba[1]

        # Now return a dataset
        result = Database(char_dict)
        result.game = game
        result.kids = kids
        if game in ava_games:
            result.ava_kid = ava_kid
            result.boba = boba
        return result

    @staticmethod
    def _load_char(char_dict: dict[str: Character | dict[str: Character]], name: str, db: pd.DataFrame
                   , game: str) -> Character:
        try:
            char = char_dict[name]
        except KeyError:
            char = Character.load_char(db[db.Name == name].squeeze(0), game)
            if char.dad:
                char_dict[name] = {'base': char}
            else:
                char_dict[name] = char
        else:
            if type(char) == dict:
                char = char['base']
        return char

    def give_kid(self, kid: str, mom: str, grandma: str | None = None) -> Character | str:
        try:
            kid = self.char[kid.capitalize()]['base']
        except KeyError:
            raise KeyError(f"{kid} does not exist as kid.")
        try:
            mom = self.char[mom.capitalize()]
        except KeyError:
            raise KeyError(f"{mom} does not exist as parent.")

        grand_kid = False

        if type(mom) == dict:
            mom = mom['base']
            grand_kid = True

        if kid == self.ava_kid and mom in self.kids and grandma is None:
            raise ValueError(f"For {kid.name} to have {mom.name} as their parent, a grandparent is required.")
        elif grandma is not None:
            if kid == self.ava_kid and grand_kid:
                try:
                    grandma = self.char[grandma]
                except KeyError:
                    raise KeyError(f"{grandma} does not exist as grandparent")
            else:
                raise ValueError(f"For {kid.name} with {mom.name} as their parent, a grandparent is not required.")

        if grand_kid:
            try:
                return self.char[kid.name][mom.name][grandma.name]
            except KeyError:
                try:
                    self._make_kid(kid, mom, grandma)
                except ValueError:
                    raise ValueError(f"{kid.name} cannot have {mom.name} as parent or {mom.name} cannot have "
                                     f"{grandma.name} as parent.")
                else:
                    return self.char[kid.name][mom.name][grandma.name]
        else:
            try:
                return self.char[kid.name][mom.name]
            except KeyError:
                try:
                    self._make_kid(kid, mom)
                except ValueError:
                    raise ValueError(f"{kid.name} cannot have {mom.name} as parent.")
                else:
                    return self.char[kid.name][mom.name]

    def _make_kid(self, kid: Character, mom: Character, grandma: Character | None = None) -> None:
        if kid not in self.kids:
            raise ValueError
        # finding out who the dad is
        dad = kid.dad
        if mom not in dad.pair:
            raise ValueError

        if grandma:
            grandpa = mom.dad
            if grandma not in grandpa.pair:
                raise ValueError
            try:
                mom = self.char[mom.name][grandma.name]
            except KeyError:
                self._make_kid(mom, grandma)
                mom = self.char[mom.name][grandma.name]

        if self.game == 'Fates':  # This is Fates, only mom and kid required
            new_stats = dict()
            for stat, value in kid.stats.items():
                new_stats[stat] = (value + mom.true_stats[stat]) // 2
            new_char = deepcopy(kid)
            new_char.dad = kid.dad
            new_char.pair = kid.pair
            new_char.stats = new_stats
            new_char.aptitude = any([mom.aptitude, dad.aptitude])
            new_char.mom = mom

            if mom.boon and mom.bane:
                new_char.boon = mom.boon
                new_char.bane = mom.bane

            if grandma:
                try:
                    self.char[kid.name][mom.name][grandma.name] = new_char
                except KeyError:
                    self.char[kid.name][mom.name] = {grandma.name: new_char}
            else:
                self.char[kid.name][mom.name] = new_char
        elif self.game == 'Awakening':  # This is awakening, dad also required
            new_stats = dict()
            for stat, value in kid.stats.items():
                new_stats[stat] = (value + mom.true_stats[stat] + dad.true_stats[stat]) // 3
            new_char = deepcopy(kid)
            new_char.dad = kid.dad
            new_char.pair = kid.pair
            new_char.stats = new_stats
            new_char.aptitude = any([mom.aptitude, dad.aptitude])
            new_char.mom = mom

            if mom.boon and mom.bane:
                new_char.boon = mom.boon
                new_char.bane = mom.bane
            elif dad.boon and dad.bane:
                new_char.boon = dad.boon
                new_char.bane = dad.bane

            if grandma:
                try:
                    self.char[kid.name][mom.name][grandma.name] = new_char
                except KeyError:
                    self.char[kid.name][mom.name] = {grandma.name: new_char}
            else:
                self.char[kid.name][mom.name] = new_char
        else:
            # this is genealogy
            new_stats = dict()
            if kid.gender == mom.gender:
                for stat in stat_list:
                    # this does not require the stats of the kids, since they don't have base stats
                    new_stats[stat] = mom.true_stats[stat] + dad.true_stats[stat] // 2
            else:
                for stat in stat_list:
                    # this does not require the stats of the kids, since they don't have base stats
                    new_stats[stat] = mom.true_stats[stat] // 2 + dad.true_stats[stat]
            new_char = deepcopy(kid)
            new_char.dad = kid.dad
            new_char.pair = kid.pair
            new_char.stats = new_stats
            new_char.mom = mom

            if mom.minor and mom.minor == dad.minor:
                new_char.major = mom.minor[0]
            else:
                new_char.minor += mom.minor + dad.minor

            if mom.major:
                if (mom.gender == new_char.gender) or new_char.swap:
                    new_char.major = mom.major
                else:
                    new_char.minor.append(mom.major)
            elif dad.major:
                if (dad.gender == new_char.gender) or new_char.swap:
                    new_char.major = dad.major
                else:
                    new_char.minor.append(dad.major)

            new_minor = []
            for blood in new_char.minor:
                if not blood == new_char.major and blood not in new_minor:
                    new_minor.append(blood)
            new_char.minor = new_minor

            self.char[kid.name][mom.name] = new_char

    def find_max(self, kid: str, unavailable: set, margin: int, bonus: list[str]
                 , *args) -> tuple[str, list[tuple[Character, int]]]:
        """ Calculates the best mom based on args given. Unavailable is a list of moms not available for this kid.
        Margin is how close the score can be to be included in the list. *args accepts stats and Tot as inputs.
        If args is empty, will use tot. Bonus is a string or tuple of strings, possible options are 'skill' or 'blood'.
        These allocate bonus points to skills and inherited blood.
        """
        kid = self.char[kid]['base']
        if kid not in self.kids:
            raise ValueError(f'{kid.name} does not exist as a kid.')

        if all(mom.name in unavailable for mom in kid.dad.pair):
            raise ValueError('No possible suitors left for parent.')

        skill = False
        blood = False
        if bonus:
            if type(bonus) != list:
                raise TypeError("bonus argument should be a list.")
            for i, item in enumerate(bonus):
                item = item.capitalize()
                if item == 'Skill':
                    skill = True
                elif item == 'Blood':
                    blood = True
                else:
                    raise ValueError('Bonuses can only be "Skill" or "Blood".')

        todo = [*args]
        if not todo:
            todo = ['Tot']

        mult = dict()
        for stat in stat_list:
            mult[stat] = 0

        end_string = f'The following stats were maximized for {kid.name}: '
        for stat in todo:
            stat = stat_cap(stat)
            if stat == 'Tot':
                for stat2 in stat_list:
                    mult[stat2] += 1
            else:
                mult[stat] += 1
            end_string += stat + ', '
        end_string = end_string[:-2]

        result = []
        high = 0
        for mom in kid.dad.pair:
            if mom.name in unavailable:
                continue
            score = 0
            if kid == self.ava_kid and mom in self.kids:
                grandma = self.find_max(mom.name, unavailable.union({kid.dad.name, kid.name}), 0, *args)[1][0][0].mom
                new_char = self.give_kid(kid.name, mom.name, grandma.name)
            else:
                new_char = self.give_kid(kid.name, mom.name)

            for stat in mult:
                score += mult[stat] * new_char.stats[stat]
            if skill:
                pass
            if blood:
                if new_char.major:
                    score += 40 * sum(mult.values())
                for _ in new_char.minor:
                    score += 20 * sum(mult.values())

            result.append((new_char, score))
            if score > high:
                high = score

        to_check = result.copy()
        for line in to_check:
            if line[1] < high - margin:
                result.remove(line)

        return end_string, result

    def max_all(self, order: list[str] | None = None, mode: str | None = None, unavailable=None, *args)\
            -> tuple[list[tuple[str, Character]], list[str]]:
        """Runs find_max() for all kids, in order given by order argument. If none
        given, will instead use default self.kids order. Possible modes are 'Tot' (leave mode as None), 'max_max' (max
        the 3 highest stats of the kid) or 'custom' (a list of tuples should be added for the kids in the order you
        want to give custom maximized values, if less than all kids, continues using max_max). Now 'blood_max' also
        supported, prioritizes holy blood.
        """
        if unavailable is None:
            unavailable = set()

        todolist = []
        todolist_copy = []
        todo = ()

        if order:
            if len(set(order)) != len(order):
                raise ValueError('There are duplicates in the order.')
            new_order = []
            for kid in order:
                # check for kids that are not in self.kids:
                try:
                    if self.char[kid]['base'] not in self.kids:
                        raise ValueError(f'{kid} does not exist as kid.')
                except TypeError:
                    raise ValueError(f'{kid} does not exist as kid.')
                new_order.append(self.char[kid]['base'])
            order = new_order
        elif order is None:
            order = list(self.kids)

        tail = [kid for kid in self.kids if kid not in order]
        order += tail

        max_max = False
        custom = False
        blood_max = False
        if mode is None:
            todo = ('Tot',)
        elif mode == 'max_max':
            max_max = True
        elif mode == 'custom':
            if not args:
                raise ValueError('Custom mode requires a list of tuples to work, at least 1 tuple should be given.')
            todolist = args[0]
            todolist_copy = todolist.copy()
            custom = True
        elif mode == 'blood_max' and self.game == 'Genealogy':
            blood_max = True
        else:
            raise ValueError(f'{mode} not recognized.')

        # create list to see who have been used already
        result = []
        leftover = []

        for kid in order:
            if custom:
                try:
                    todo = todolist.pop(0)
                except IndexError:
                    if self.game == 'Genealogy':
                        blood_max = True
                    else:
                        max_max = True
                    custom = False
            if max_max or blood_max:
                if self.game in ava_games:
                    # HP and Lck are not accounted for, because many have high Lck
                    # and HP.
                    kid_stats = kid.stats.copy()
                    kid_stats['HP'] = 0
                    kid_stats['Lck'] = 0

                    stat1 = max(kid_stats, key=kid_stats.get)
                    kid_stats[stat1] = 0
                    stat2 = max(kid_stats, key=kid_stats.get)
                    kid_stats[stat2] = 0
                    stat3 = max(kid_stats, key=kid_stats.get)
                    kid_stats[stat3] = 0

                    todo = (stat1, stat2, stat3)
                else:
                    # genealogy, every kid has 0 'base stats', so instead the set parent (always the mom here) will be
                    # used
                    kid_stats = kid.dad.stats.copy()
                    kid_stats['HP'] = 0
                    kid_stats['Lck'] = 0

                    stat1 = max(kid_stats, key=kid_stats.get)
                    kid_stats[stat1] = 0
                    stat2 = max(kid_stats, key=kid_stats.get)
                    kid_stats[stat2] = 0
                    stat3 = max(kid_stats, key=kid_stats.get)
                    kid_stats[stat3] = 0

                    todo = (stat1, stat2, stat3)

            # check if kid is a sibling of another who was already checked
            if kid.name in unavailable:
                continue
            try:
                if blood_max:
                    string, all_max = self.find_max(kid.name, unavailable, 0, ['Blood'], *todo)
                else:
                    string, all_max = self.find_max(kid.name, unavailable, 0, [], *todo)
            except ValueError:
                leftover.append(kid.name)
            else:
                to_add = all_max[0]
                if len(all_max) > 1:
                    for check in all_max:
                        if check[1] > to_add[1]:
                            to_add = check
                result.append((string, to_add[0]))
                temp_char = to_add[0]
                mom = temp_char.mom
                dad = temp_char.dad
                unavailable.add(dad.name)
                unavailable.add(mom.name)

                if kid == self.ava_kid and type(self.char[mom.name]) == dict:
                    grandma = temp_char.grandma
                    grandpa = temp_char.grandpa
                    unavailable.add(grandma.name)
                    unavailable.add(grandpa.name)
                    result.append((string, mom))
                    if grandma.kid:
                        for kid2 in grandma.kid:
                            result.append((string, self.give_kid(kid2.name, grandpa.name)))
                            unavailable.add(kid2.name)
                            # ensure that custom order does not get disrupted for custom mode
                            if custom:
                                i = order.index(kid2)
                                if i <= len(todolist_copy) - 1:
                                    diff = len(todolist_copy) - len(todolist)
                                    todolist.pop(i - diff)
                    elif grandpa.kid:
                        for kid2 in grandpa.kid:
                            if kid2 != mom and kid2.name:
                                result.append((string, self.give_kid(kid2.name, grandma.name)))
                                unavailable.add(kid2.name)
                                # ensure that custom order does not get disrupted for custom mode
                                if custom:
                                    i = order.index(kid2)
                                    if i <= len(todolist_copy) - 1:
                                        diff = len(todolist_copy) - len(todolist)
                                        todolist.pop(i - diff)
                elif mom.kid:
                    # other parent has a set child of her own, needs to be added to result and unavailable too. If
                    # dad is Avatar and mom is an avatar only character, it will not find anything, but that's fine.
                    for kid2 in mom.kid:
                        result.append((string, self.give_kid(kid2.name, dad.name)))
                        unavailable.add(kid2.name)
                        if custom:
                            i = order.index(kid2)
                            if i <= len(todolist_copy) - 1:
                                diff = len(todolist_copy) - len(todolist)
                                todolist.pop(i - diff)
                elif dad.kid:
                    for kid2 in dad.kid:
                        if kid2 != kid:
                            result.append((string, self.give_kid(kid2.name, mom.name)))
                            unavailable.add(kid2.name)
                            if custom:
                                i = order.index(kid2)
                                if i <= len(todolist_copy) - 1:
                                    diff = len(todolist_copy) - len(todolist)
                                    todolist.pop(i - diff)
            finally:
                unavailable.add(kid)

        return result, leftover

    def randomize_classes(self, mode: str = 'minimal') -> tuple[dict, list]:
        """mode is either 'minimal', then every class will be assigned to one character, or 'maximal', where every
        character gets a random class, which will cause duplicates (though it tries to avoid it). DLC classes will
        always be limited to 1"""
        if self.game == 'Fates':
            dlc = fates_dlc
        elif self.game == 'Awakening':
            dlc = []
        else:
            raise ValueError('No Genealogy Randomization')

        if mode not in ['minimal', 'maximal']:
            raise ValueError

        result = dict()
        leftover = []
        for char in self.char.values():
            if type(char) == dict:
                leftover.append(char['base'])
            else:
                leftover.append(char)

        shuffle(leftover)
        done = []
        i = 0
        while len(leftover) > i:
            added = False
            char = leftover[i]
            classes = char.promoted
            shuffle(classes)
            for class_ in classes:
                if class_ not in done:
                    done.append(class_)
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
                    while not no_dlc:
                        class_ = choice(classes)
                        if class_ not in dlc:
                            no_dlc = True
                    result[char.name] = class_
                    leftover.pop(i)
                    if class_ not in done:
                        done.append(classes[0])
        leftover = [char.name for char in leftover]
        return result, leftover


if __name__ == '__main__':
    # children are very difficult
    t = Database.load_file('Fates', ('Str', 'Lck'), 'm', 'Mercenary')
    s = Database.load_file('Awakening', ('Mag', 'Str'), 'm')
    r = Database.load_file('Genealogy')

    # print Kid
    # print(t.give_kid('Asugi', 'Kagero'))
    # print(t.give_kid('Midori', 'Kagero'))

    # Randomizer
    # result, leftover = t.randomize_classes('maximal')
    # for name, class_ in result.items():
    #     print(f"{name} should become a {class_}.")
    # for name in leftover:
    #     print(f"{name} was left over.")

    # Maximizer 1
    result = t.find_max('Rhajat', {'Mozu'}, 10, [], 'Str', 'Spd', 'Skl')

    print(result[0])
    for line in result[1]:
        print(line[0].summary)
        print(line[1])

    # Maximizer all
    # order = ['Kana', 'Midori', 'Mitama', 'Shigure', 'Nina', 'Velouria', 'Selkie', 'Soleil', 'Dwyer']
    # result, leftover = t.max_all(order=order, mode='max_max')

    # for line in result:
    #     print(line[0])
    #     print(line[1].summary)
    # print(f"These characters were left over: {leftover}.")
