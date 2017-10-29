import json
import random
import datetime
import calendar


class AllMembers:
    def __init__(self, members=None):
        try:
            with open(members) as data_file:
                data = json.load(data_file)
                self.__name = data['name']
                self.__members = self.__build_tuple_list(data['members'])
                self.__exclusions = {k: self.__build_tuple_list(data['exclusions'].get(k)) for k in data['exclusions']}
        except TypeError:
            print('Must provide a file path, returning empty list')
            self.__members, self.__exclusions = [], {}
        except (NameError, FileNotFoundError):
            print('Could not find the file, returning empty list')
            self.__members, self.__exclusions = [], {}

    @staticmethod
    def __build_tuple_list(data):
        return [tuple([y.strip() for y in x.split('&')]) for x in data]

    def get_members(self, weekday=None):
        if weekday is None:
            return self.__members
        elif weekday in self.__exclusions.keys():
            to_remove = self.__exclusions.get(weekday)
        else:
            raise ValueError('Weekday not specified in json data file.')

        members = self.__members[:]
        for nome in to_remove:
            members.remove(nome)
        return members

    def __get_members_list(self, weekday):
        members = self.get_members(weekday)
        members_list = [(x, len(x)) for x in members]
        return members_list

    def get_groups(self, members_per_group=4, weekday=None):
        members_list = self.__get_members_list(weekday)
        groups = []
        while len(members_list) > 0:
            group, people = [], 0
            while people < members_per_group and len(members_list) > 0:
                member = members_list.pop(random.randrange(len(members_list)))
                people += member[1]
                group.append(member[0])
            groups.append(group)
        return groups

    def print_groups(self, members_per_group=4, weekday=None):
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


class WeekdaysFinder:
    def __init__(self):
        self.days = {x[1]: x[0] for x in enumerate(calendar.day_name)}

    def get_next_weekday(self, weekday):
        """
        This method accepts as argument a weekday
        Returns the next date of the corresponding weekday
        """
        try:
            assert isinstance(weekday, (str, int))
            assert weekday != ''
        except AssertionError:
            raise ValueError('Weekday is accepted as either string or integer value')

        if type(weekday) is str:
            weekday = self.days.get(weekday.capitalize())

        dt = datetime.date.today()
        while dt.weekday() != weekday:
            dt += datetime.timedelta(1)

        return dt

    def generator_weekday(self, weekday, startdate=None, howmany=4):
        try:
            assert isinstance(weekday, (str, int))
            assert weekday != ''
        except AssertionError:
            raise ValueError('Weekday is accepted as either string or integer value')

        if type(weekday) is str:
            weekday = self.days.get(weekday.capitalize())

        if startdate is None:
            startdate = datetime.date.today()
        else:
            try:
                assert isinstance(startdate, str)
                startdate = [i for i in map(int, startdate.split('-'))]
                assert len(startdate) == 3
                startdate = datetime.date(startdate[0], startdate[1], startdate[2])
            except AssertionError:
                raise ValueError('Startdate must be a string in the form yyyy-mm-d')

        num, dt = 0, startdate + datetime.timedelta(1)
        while num < howmany:
            while dt.weekday() != weekday:
                dt += datetime.timedelta(1)
            yield dt
            num += 1
            dt += datetime.timedelta(1)


def main():
    days = WeekdaysFinder()
    print([y for y in days.generator_weekday('saturday', '2017-10-29', 5)])


if __name__ == '__main__':
    main()
