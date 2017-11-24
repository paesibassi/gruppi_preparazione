import json
import itertools
import random
import datetime
import calendar


class AllMembers:
    """
    Class that holds the names of the members, passed as json data file, and
    can return group compositions.
    """
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
                member = members_list.pop(random.randrange(len(members_list)))
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

    def print_groups(self, members_per_group=4, weekday=None):
        """
        Pretty printing of groups.
        :param members_per_group: integer
        :param weekday: day of the week, as string
        :return: 0, prints groups to the console as side effect
        """
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
        return 0


class WeekdaysFinder:
    def __init__(self):
        self.days = {x[1]: x[0] for x in enumerate(calendar.day_name)}
        self.months = {x[1]: x[0] for x in enumerate(calendar.month_name)}

    def get_next_weekday(self, weekday, startdate=None):
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

        if type(weekday) is str:
            weekday = self.days.get(weekday.capitalize())

        if startdate is None:
            dt = datetime.date.today()
        else:
            try:
                assert isinstance(startdate, str)
                startdate = [i for i in map(int, startdate.split('-'))]
                assert len(startdate) == 3
                dt = datetime.date(startdate[0], startdate[1], startdate[2])
            except AssertionError:
                raise ValueError('Startdate must be a string in the form yyyy-mm-d')

        while dt.weekday() != weekday:
            dt += datetime.timedelta(1)

        return dt

    def generator_weekday(self, weekday, startdate=None, howmany=1000):
        """
        This method is a generator, it will yield all the future dates
        of a specific weekday.
        :param weekday: weekday, as a string or integer value (base 0 for Monday)
        :param startdate: starting date, format yyyy-mm-dd
        :param howmany: optional max limit to the number of items generated
        :return: generator of dates
        """
        try:
            assert isinstance(weekday, (str, int))
            assert weekday != ''
            assert weekday is not None
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

        num, dt = 0, startdate
        while num < howmany:
            while dt.weekday() != weekday:
                dt += datetime.timedelta(1)
            yield dt
            num += 1
            dt += datetime.timedelta(1)

    def full_calendar(self, groups, month,
                      weekdays=(('wednesday', 4), ('saturday', 3))):
        """
        Returns a calendar for the full month
        :param groups:
        :param month:
        :param weekdays:
        :return:
        """
        try:
            assert isinstance(month, (str, int))
        except AssertionError:
            raise ValueError('Month is accepted as either string or integer value')

        if type(month) is str:
            month = self.months.get(month.capitalize())

        current_year = datetime.date.today().year  # get current year
        startdate = '-'.join([str(current_year), str(month), str(1)])

        wds = {day: member for (day, member) in weekdays}

        combo = {day: (self.generator_weekday(day, startdate=startdate),
                       groups.get_groups_list(members, day)
                       ) for day, members in wds.items()}

        result_dict = {}
        for weekday, value in combo.items():
            dates, groups = value
            result_dict[weekday] = ['{wday} {date}: '.format(wday=weekday.capitalize(), date=date) +
                                    ', '.join(group) for (date, group) in zip(dates, groups)]

        days = {x: x for x in wds.keys()}
        for key in days:
            days[key] = self.get_next_weekday(key, startdate=startdate)
        sorted_days = sorted(days, key=days.get)
        sorted_lists = [result_dict[day] for day in sorted_days]
        result = [item for pair in itertools.zip_longest(*sorted_lists, fillvalue='No more members') for item in pair]

        return result


def main():
    # grs = AllMembers('../persone.json').get_groups_list(4, 'wednesday')
    # gen = WeekdaysFinder().generator_weekday('wednesday')
    # for date, group in zip(gen, grs):
    #     print('Wednesday {d}: {g}'.format(d=date, g=', '.join(group)))
    wk = WeekdaysFinder()
    for x in wk.full_calendar(AllMembers('tests/members_example.json'), 'september'):
        print(x)


if __name__ == '__main__':
    main()
