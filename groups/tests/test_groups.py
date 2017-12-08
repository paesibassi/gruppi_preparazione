"""Unit tests for the groups module, using pytest)"""

import random
import datetime
import collections
import sys
import argparse
import pytest
sys.path.append('.')
import groups.groups as gr

PATH = 'groups/tests/members_example.json'

def test_allmembers_init(capsys):
    """Unit tests for the __init__ method in AllMembers()"""
    gr.AllMembers()
    out, _ = capsys.readouterr()
    assert out == 'Must provide a file path, returning empty list\n'

    gr.AllMembers('notfound')
    out, _ = capsys.readouterr()
    assert out == 'Could not find the file, returning empty list\n'


def test_allmembers_members():
    """Unit tests for the members method in AllMembers()"""
    allmembers = gr.AllMembers(PATH)

    assert len(allmembers.get_members()) == 14

    assert ('Stephen', 'Lyda') in allmembers.get_members()
    assert ('Delbert',) in allmembers.get_members()

    assert len(allmembers.get_members('wednesday')) == 13
    assert ('Patsy',) not in allmembers.get_members('wednesday')
    assert ('Delbert',) in allmembers.get_members('wednesday')
    assert ('Delbert',) not in allmembers.get_members('saturday')

    assert len(allmembers.get_members('sunday')) == 13
    assert ('Stephen', 'Lyda') not in allmembers.get_members('sunday')

    with pytest.raises(ValueError):
        allmembers.get_members('another')


def test_allmembers_groups():
    """Unit tests for the groups method in AllMembers()"""
    allmembers = gr.AllMembers(PATH)

    random.seed(12345)

    assert isinstance(allmembers.get_groups(), list)
    assert isinstance(allmembers.get_groups(5), list)
    assert isinstance(allmembers.get_groups(3, 'wednesday'), list)
    assert [('Stephen', 'Lyda'), ('Zena',)] in allmembers.get_groups(3)
    assert len(allmembers.get_groups(3)) == 6
    assert len(allmembers.get_groups(5, 'saturday')) == 3
    assert [('Melissia',), ('Jose', 'Dionne'), ('Emilio', 'Nieves')] in \
        allmembers.get_groups(5, 'saturday')


def test_get_groups_list():
    """Unit tests for the get_groups as list method in AllMembers()"""
    allmembers = gr.AllMembers(PATH)

    random.seed(12345)

    assert isinstance(allmembers.get_groups_list(), list)
    assert isinstance(allmembers.get_groups_list(5), list)
    each = allmembers.get_groups_list(3, 'wednesday')
    assert isinstance(each, list)
    assert ['Stephen & Lyda', 'Zena'] in each
    assert len(each) == 6
    them = allmembers.get_groups_list(5, 'saturday')
    assert len(them) == 3
    assert ['Melissia', 'Stephen & Lyda', 'Jose & Dionne'] in them


def test_printable_groups():
    """Unit tests for the printable groups method in AllMembers()"""
    allmembers = gr.AllMembers(PATH)

    random.seed(12345)

    assert isinstance(allmembers.printable_groups(), list)
    assert isinstance(allmembers.printable_groups(6), list)
    each = allmembers.printable_groups(3, 'wednesday')
    assert isinstance(each, list)
    assert 'Stephen & Lyda, Zena' in each
    assert len(each) == 6
    them = allmembers.printable_groups(5, 'saturday')
    assert len(them) == 3
    assert 'Melissia, Stephen & Lyda, Jose & Dionne' in them


def test_get_next_weekday():
    """Unit tests for the weekday iterator in WeekdaysFinder()"""
    days = gr.WeekdaysFinder()

    assert isinstance(days.get_next_weekday(3), datetime.date)
    assert isinstance(days.get_next_weekday('wednesday'), datetime.date)
    assert isinstance(days.get_next_weekday('monday'), datetime.date)
    assert isinstance(days.get_next_weekday('Saturday'), datetime.date)

    with pytest.raises(ValueError):
        days.get_next_weekday('')
        days.get_next_weekday(8)
        days.get_next_weekday('whatever')
        days.get_next_weekday('sunday')

        days.get_next_weekday('wednesday', '')
        days.get_next_weekday('wednesday', '2017')
        days.get_next_weekday('wednesday', 2017)

    assert days.get_next_weekday('wednesday').weekday() == 2
    assert days.get_next_weekday('saturday').weekday() == 5
    assert days.get_next_weekday('saturday', '2017-12-01') == datetime.date(2017, 12, 2)


def test_generator_weekday():
    """Unit tests for the weekday generator in WeekdaysFinder()"""
    days = gr.WeekdaysFinder()

    assert isinstance(days.generator_weekday('saturday'), collections.Generator)
    assert [y for y in days.generator_weekday('saturday', '2017-11-5', 4)] == \
           [datetime.date(2017, 11, 11),
            datetime.date(2017, 11, 18),
            datetime.date(2017, 11, 25),
            datetime.date(2017, 12, 2)]
    assert [y for y in days.generator_weekday('thursday', '2017-11-3', 1)] == \
           [datetime.date(2017, 11, 9)]
    with pytest.raises(ValueError):
        print([y for y in days.generator_weekday('thursday', 2017113, 4)])
        print([y for y in days.generator_weekday('thursday', '2017113', 4)])

    dates_gen = days.generator_weekday('saturday', '2017-11-22')
    assert next(dates_gen) == datetime.date(2017, 11, 25)
    assert next(dates_gen) == datetime.date(2017, 12, 2)


def test_class_monthcalendargroups(capsys):
    """Unit tests for the class MonthCalendarGroups()"""
    members = gr.AllMembers(PATH)

    nov = gr.MonthCalendarGroups(members, 'november').full_calendar
    assert isinstance(nov, list)
    jun = gr.MonthCalendarGroups(members, 'june')
    print(jun)
    out, _ = capsys.readouterr()
    assert 'Wednesday' in out
    assert 'Saturday' in out

def test_main(mocker, capsys):
    """Unit tests for the main() function in the groups module"""
    mocker.patch('argparse.ArgumentParser.parse_args',
                 return_value=argparse.Namespace(
                     output_type='groups',
                     members_json='groups/tests/members_example.json',
                     weekday='wednesday',
                     number=4))
    gr.main()
    out, _ = capsys.readouterr()
    assert 'Stephen & Lyda' in out

    mocker.patch('argparse.ArgumentParser.parse_args',
                 return_value=argparse.Namespace(
                     output_type='month',
                     members_json='groups/tests/members_example.json',
                     month='november'))
    gr.main()
    out, _ = capsys.readouterr()
    assert 'Wednesday' in out
