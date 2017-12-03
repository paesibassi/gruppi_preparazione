#!/usr/local/bin/python3

import calendar
from argparse import ArgumentParser
from datetime import date, timedelta
from json import load
from random import randrange
from itertools import zip_longest


class ArgParser:
    """
    Argument parser to read command line arguments passed to the script
    """
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('output_type', type=str, choices=['groups', 'month'],
                                 help="""Specify either 'groups' for one set of groups for a weekday,
                                 or 'month' for full calendar month""")
        self.parser.add_argument('members_json', type=str,
                                 help='Specify the path to the list of members (json)')
        self.parser.add_argument('-n', '--number', type=int, default=4,
                                 help='Specify how many members per group, default 4')
        self.parser.add_argument('-w', '--weekday', type=str, default='saturday',
                                 help='Specify weekday to remove members, default saturday')
        self.parser.add_argument('-m', '--month', type=str, default=self.default_month(),
                                 help='Specify month to build full calendar, default next month')
        self.parser.add_argument('-v', '--verbose', action='store_true',
                                 help='Verbose output')
        self.args = vars(self.parser.parse_args())
        self.args_dict = dict((k, self.args[k]) for k in self.args if self.args[k] is not None)  # deletes None values

    @staticmethod
    def default_month():
        return (1 if date.today().month == 12 else date.today().month+1)

    def _print_options(self, options):  # pragma: no cover
        output_type, path, members_per_group, weekday, month = options
        print('='*70)
        print('Verbose option is ON')
        print('Read the members data from the file at {p}'.format(p=path))
        if output_type == 'month':
            print('Generate groups for the month of {m}'.format(m=calendar.month_name[month]))
        elif output_type == 'groups':
            print('Generating groups of {n} people'.format(n=members_per_group))
            print('Generating groups excluding members for weekday: {w}'.format(w=weekday))
        print('='*70)

    def get_arguments(self):
        output_type = self.args_dict.get('output_type')
        path = self.args_dict.get('members_json')
        members_per_group = self.args_dict.get('number')
        weekday = self.args_dict.get('weekday')
        month = self.args_dict.get('month')
        options = output_type, path, members_per_group, weekday, month
        if self.args_dict.get('verbose', False):
            self._print_options(options)
        return options


class AllMembers:
    """
    Class that holds the names of the members, passed as json data file, and
    returns group combinations.
    """
    def __init__(self, members=None):
        try:
            with open(members) as data_file:
                data = load(data_file)  # using json.load
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
        """
        get-members method
        :param weekday: day of the week as string
        :return: all members as a list of tuples
        """
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
        """
        Returns groups of members as a list of lists of tuples.
        :param members_per_group: int
        :param weekday: string
        :return: list
        """
        members_list = self.__get_members_list(weekday)
        groups = []
        while len(members_list) > 0:
            group, people = [], 0
            while people < members_per_group and len(members_list) > 0:
                member = members_list.pop(randrange(len(members_list)))
                people += member[1]
                group.append(member[0])
            groups.append(group)
        return groups

    def get_groups_list(self, members_per_group=4, weekday=None):
        """
        Returns groups of members as a list of lists,
        with couples joined in strings with a '&'.
        :param members_per_group: int
        :param weekday: string
        :return: list
        """
        groups = self.get_groups(members_per_group, weekday)
        groups_list = [[' & '.join(member) for member in group] for group in groups]
        return groups_list

    def printable_groups(self, members_per_group=4, weekday=None):
        """
        Pretty printing of groups.
        :param members_per_group: integer
        :param weekday: day of the week, as string
        :return: 0, prints groups to the console as side effect
        """
        groups = self.get_groups_list(members_per_group, weekday)
        printable_list = [', '.join(group) for group in groups]
        return printable_list


class WeekdaysFinder:
    days = {x[1]: x[0] for x in enumerate(calendar.day_name)}
    months = {x[1]: x[0] for x in enumerate(calendar.month_name)}

    def get_next_weekday(self, weekday, start_date=None):
        """
        This method accepts as argument a weekday
        Returns the next date of the corresponding weekday
        """
        try:
            assert isinstance(weekday, (str, int))
            assert weekday != ''
            assert weekday is not None
        except AssertionError:
            raise ValueError('Weekday is accepted as either string or integer value')

        if isinstance(weekday, str):
            weekday = self.days.get(weekday.capitalize())

        if start_date is None:
            day_date = date.today()
        else:
            try:
                assert isinstance(start_date, str)
                start_date = [i for i in map(int, start_date.split('-'))]
                assert len(start_date) == 3
                day_date = date(start_date[0], start_date[1], start_date[2])
            except AssertionError:
                raise ValueError('Start date must be a string in the form yyyy-mm-d')

        while day_date.weekday() != weekday:
            day_date += timedelta(1)

        return day_date

    def generator_weekday(self, weekday, start_date=None, how_many=1000):
        """
        This method is a generator, it will yield all the future dates
        of a specific weekday.
        :param weekday: weekday, as a string or integer value (base 0 for Monday)
        :param start_date: starting date, format yyyy-mm-dd
        :param how_many: optional max limit to the number of items generated
        :return: generator of dates
        """
        try:
            assert isinstance(weekday, (str, int))
            assert weekday != ''
            assert weekday is not None
        except AssertionError:
            raise ValueError('Weekday is accepted as either string or integer value')

        if isinstance(weekday, str):
            weekday = self.days.get(weekday.capitalize())

        if start_date is None:
            start_date = date.today()
        else:
            try:
                assert isinstance(start_date, str)
                start_date = [i for i in map(int, start_date.split('-'))]
                assert len(start_date) == 3
                start_date = date(start_date[0], start_date[1], start_date[2])
            except AssertionError:
                raise ValueError('Start date must be a string in the form yyyy-mm-d')

        num, day_date = 0, start_date
        while num < how_many:
            while day_date.weekday() != weekday:
                day_date += timedelta(1)
            yield day_date
            num += 1
            day_date += timedelta(1)


class MonthCalendarGroups:
    """
    Returns a calendar for the full month
    :param members:
    :param month:
    :param weekdays:
    :return:
    """
    def __init__(self, members, month, weekdays=(('wednesday', 4), ('saturday', 3))):
        self.members = members
        self.wkd = WeekdaysFinder()

        if isinstance(month, str):
            month = self.wkd.months.get(month.capitalize())

        current_year = date.today().year if month != 1 else date.today().year+1  # get current year
        start_date = '-'.join([str(current_year), str(month), str(1)])

        wds = {day: member for (day, member) in weekdays}

        combo = {day: (self.wkd.generator_weekday(day, start_date=start_date),
                       self.members.get_groups_list(members, day)
                      ) for day, members in wds.items()}

        result_dict = {}
        for weekday, value in combo.items():
            dates, groups = value
            result_dict[weekday] = ['{wday} {date}: '.format(wday=weekday.capitalize(), date=day_date) +
                                    ', '.join(group) for (day_date, group) in zip(dates, groups)]

        days = {x: x for x in wds.keys()}
        for key in days:
            days[key] = self.wkd.get_next_weekday(key, start_date=start_date)
        sorted_days = sorted(days, key=days.get)
        sorted_lists = [result_dict[day] for day in sorted_days]
        zipped_list = zip_longest(*sorted_lists, fillvalue='No more groups for this weekday')
        result = [item for pair in zipped_list for item in pair]

        self.full_calendar = result

    def __str__(self):
        return '\n'.join(self.full_calendar)


def main():
    output_type, path, members_per_group, weekday, month = ArgParser().get_arguments()
    members = AllMembers(path)

    if output_type == 'groups':
        print(*members.printable_groups(members_per_group, weekday), sep='\n')
    elif output_type == 'month':
        print(MonthCalendarGroups(members, month))


if __name__ == '__main__':  # pragma: no cover
    main()
