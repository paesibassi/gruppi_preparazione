import pytest
import random
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

    assert ('Federico', 'Teresa') in allmembers.get_members()
    assert ('Giancarlo',) in allmembers.get_members()

    assert len(allmembers.get_members('wednesday')) == 13
    assert ('Ana',) not in allmembers.get_members('wednesday')
    assert ('Giancarlo',) in allmembers.get_members('wednesday')
    assert ('Giancarlo',) not in allmembers.get_members('saturday')

    assert len(allmembers.get_members('sunday')) == 13
    assert ('Federico', 'Teresa') not in allmembers.get_members('sunday')

    with pytest.raises(ValueError):
        allmembers.get_members('another')


def test_allmembers_groups():
    path = './members_example.json'
    allmembers = gr.AllMembers(path)

    random.seed(12345)

    assert isinstance(allmembers.get_groups(), list)
    assert isinstance(allmembers.get_groups(5), list)
    assert isinstance(allmembers.get_groups(3, 'wednesday'), list)
    assert [('Federico', 'Teresa'), ('Philippe',)] in allmembers.get_groups(3)
    assert len(allmembers.get_groups(3)) == 6
    assert len(allmembers.get_groups(5, 'saturday')) == 3
    assert [('Maria',), ('Marcelo', 'Chantal'), ('Enrique', 'Concha')] in \
        allmembers.get_groups(5, 'saturday')
