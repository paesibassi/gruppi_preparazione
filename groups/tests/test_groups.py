"""Unit tests for the groups module, using pytest)"""

import random
import datetime
import collections
import sys
import argparse
import pytest
sys.path.append('.')
import groups.groups as gr

@pytest.fixture
def allmembers():
    """Test fixture to set seed and instantiate an AllMembers obj"""
    random.seed(12345)
    return gr.AllMembers('groups/tests/members_example.json')

def test_allmembers_init(capsys):
    """Unit tests for the __init__ method in AllMembers()"""
    gr.AllMembers()
    out, _ = capsys.readouterr()
    assert out == 'Must provide a file path, returning empty list\n'

    gr.AllMembers('notfound')
    out, _ = capsys.readouterr()
    assert out == 'Could not find the file, returning empty list\n'


@pytest.mark.parametrize(
    ("number_of_members", "weekday"),
    [(22, None),
     (20, 'wednesday'),
     (19, 'sunday')
    ])
def test_number_of_members_in_allmembers(allmembers, number_of_members, weekday):
    """Unit tests for the members method in AllMembers()"""
    assert number_of_members == len(allmembers.get_members(weekday))


@pytest.mark.parametrize(
    ("members", "weekday"),
    [(('Stephen', 'Lyda'), None),
     (('Delbert',), None),
     (('Delbert',), 'wednesday')
    ])
def test_members_in_allmembers(allmembers, members, weekday):
    """Unit tests for the members method in AllMembers()"""
    assert members in allmembers.get_members(weekday)


@pytest.mark.parametrize(
    ("members", "weekday"),
    [(('Patsy',), 'wednesday'),
     (('Delbert',), 'saturday'),
     (('Stephen', 'Lyda'), 'sunday')
    ])
def test_members_not_in_allmembers(allmembers, members, weekday):
    """Unit tests for the members method in AllMembers()"""
    assert members not in allmembers.get_members(weekday)


def test_error_if_missing_member_in_allmembers(allmembers):
    with pytest.raises(ValueError):
        allmembers.get_members('another')


def test_allmembers_groups(allmembers):
    """Unit tests for the groups method in AllMembers()"""
    assert isinstance(allmembers.get_groups(), list)
    assert isinstance(allmembers.get_groups(5), list)
    assert isinstance(allmembers.get_groups(3, 'wednesday'), list)
    assert [('Stephen', 'Lyda'), ('Alfonso',)] in allmembers.get_groups(3)
    assert len(allmembers.get_groups(3)) == 10
    assert len(allmembers.get_groups(5, 'saturday')) == 5
    assert [('Corina',), ('Charles', 'Vivienne'), ('Mark', 'Alysha')] in \
        allmembers.get_groups(5, 'saturday')


def test_get_groups_list(allmembers):
    """Unit tests for the get_groups as list method in AllMembers()"""
    assert isinstance(allmembers.get_groups_list(), list)
    assert isinstance(allmembers.get_groups_list(5), list)
    each = allmembers.get_groups_list(3, 'wednesday')
    assert isinstance(each, list)
    assert ['Tod & Kenya', 'Stephen & Lyda'] in each
    assert len(each) == 9
    them = allmembers.get_groups_list(5, 'saturday')
    assert len(them) == 5
    assert ['Mark & Alysha', 'Anthony & Cheryl', 'Olivier'] in them


def test_printable_groups(allmembers):
    """Unit tests for the printable groups method in AllMembers()"""
    assert isinstance(allmembers.printable_groups(), list)
    assert isinstance(allmembers.printable_groups(6), list)
    each = allmembers.printable_groups(3, 'wednesday')
    assert isinstance(each, list)
    assert 'Melissia, Shaq & Ouida' in each
    assert len(each) == 9
    them = allmembers.printable_groups(5, 'saturday')
    assert len(them) == 5
    assert 'Mark & Alysha, Anthony & Cheryl, Olivier' in them

@pytest.fixture
def days():
    """Test fixture to instantiate a WeekdaysFinder obj"""
    return gr.WeekdaysFinder()

def test_get_next_weekday(days):
    """Unit tests for the weekday iterator in WeekdaysFinder()"""
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


def test_generator_weekday(days):
    """Unit tests for the weekday generator in WeekdaysFinder()"""
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


def test_class_monthcalendargroups(capsys, allmembers):
    """Unit tests for the class MonthCalendarGroups()"""
    nov = gr.MonthCalendarGroups(allmembers, 'november').full_calendar
    assert isinstance(nov, list)
    jun = gr.MonthCalendarGroups(allmembers, 'june')
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
