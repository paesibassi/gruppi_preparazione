import pytest
import random
import datetime
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


def test_Weekdays_finder():
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

