import pytest
import gruppi_preparazione.dates as dt
import datetime


def test_find_next_weekday():
    with pytest.raises(ValueError):
        dt.find_next_weekday(1)
        dt.find_next_weekday(5)
        dt.find_next_weekday('whatever')
        dt.find_next_weekday('sunday')
        dt.find_next_weekday('')
        dt.find_next_weekday()

    assert type(dt.find_next_weekday(2)) == datetime.date
    assert type(dt.find_next_weekday('wednesday')) == datetime.date

    assert dt.find_next_weekday('wednesday').weekday() == 2
    assert dt.find_next_weekday('saturday').weekday() == 6
