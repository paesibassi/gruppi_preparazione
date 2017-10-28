import json
import random


class AllMembers:
    def __init__(self, members=None):
        try:
            with open(members) as data_file:
                data = json.load(data_file)
                self.__name = data['name']
                self.__members = self.__build_tuple_list(data['members'])
                self.__wednesday = self.__build_tuple_list(data['wednesday'])
                self.__saturday = self.__build_tuple_list(data['saturday'])
        except TypeError:
            print('Must provide a file path, returning empty list')
            self.__members, self.__wednesday, self.__saturday = [],[],[]
        except (NameError, FileNotFoundError):
            print('Could not find the file, returning empty list')
            self.__members, self.__wednesday, self.__saturday = [], [], []

    def __build_tuple_list(self, data: object) -> list:
        return [tuple([y.strip() for y in x.split('&')]) for x in data]

    def get_members(self, weekday=None):
        if weekday is None:
            return self.__members
        elif weekday == 'wednesday': to_remove = self.__wednesday
        elif weekday == 'saturday': to_remove = self.__saturday
        else: raise ValueError('Weekday not yet supported.')

        members = self.__members[:]
        for nome in to_remove:
            members.remove(nome)
        return members

    def __get_members_list(self, members):
        members_list = [(x, len(x)) for x in members]
        return members_list

    def get_groups(self, members_per_group=4, weekday=None):
        members = self.get_members(weekday)
        members_list = self.__get_members_list(members)
        groups = []
        while len(members_list) > 0:
            group, people = [], 0
            while people < members_per_group and len(members_list) > 0:
                member = members_list.pop(random.randrange(len(members_list)))
                people += member[1]
                group.append(member[0])
            groups.append(group)
        return groups

    def get_groups_string(self, members_per_group=4, weekday=None):
        groups = self.get_groups(members_per_group, weekday)
        for g, group in enumerate(groups, start=1):
            print('Gruppo {g}: '.format(g=g), end='')
            components = len(group)
            for m, member in enumerate(group, start=1):
                num_pers = len(member)
                if num_pers == 1:
                    print(member[0], end='')
                elif num_pers == 2:
                    print(member[0], '&', member[1], end='')
                else:
                    raise ValueError('Only single members or couples are supported.')
                if m < components:
                    print(', ', end='')
            print('')
        return None
