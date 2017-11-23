import pytest
import random
import datetime
import collections
import gruppi_preparazione.classes as gr


def test_allmembers_init(capsys):
    gr.AllMembers()
    out, err = capsys.readouterr()
    assert out == 'Must provide a file path, returning empty list\n'

    gr.AllMembers('notfound')
    out, err = capsys.readouterr()
    assert out == 'Could not find the file, returning empty list\n'


def test_allmembers_members():
    path = './members_example.json'
    allmembers = gr.AllMembers(path)

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
    path = './members_example.json'
    allmembers = gr.AllMembers(path)

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
    path = './members_example.json'
    allmembers = gr.AllMembers(path)

    random.seed(12345)

    assert isinstance(allmembers.get_groups_list(), list)
    assert isinstance(allmembers.get_groups_list(5), list)
    m = allmembers.get_groups_list(3, 'wednesday')
    assert isinstance(m, list)
    assert ['Stephen & Lyda', 'Zena'] in m
    assert len(m) == 6
    n = allmembers.get_groups_list(5, 'saturday')
    assert len(n) == 3
    assert ['Melissia', 'Stephen & Lyda', 'Jose & Dionne'] in n


def test_weekdays_finder():
    pass


def test_get_next_weekday():
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

    assert days.get_next_weekday('wednesday').weekday() == 2
    assert days.get_next_weekday('saturday').weekday() == 5


def test_generator_weekday():
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

def test_full_calendar():
    wk = gr.WeekdaysFinder()

    #TODO: implement unit tests for wk.full_calendar()
    # assert isinstance(wk.full_calendar('november'), list)