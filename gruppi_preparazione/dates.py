import datetime


def find_next_weekday(weekday):
    """
    This function accepts as argument a weekday
    Returns the next date of the corresponding weekday
    """

    if type(weekday) is str:
        if weekday == 'wednesday':
            weekday = 2
        elif weekday == 'saturday':
            weekday = 6
        else:
            raise ValueError('Weekday string argument must be either "wednesday" or "saturday"')
    elif type(weekday) is int:
        if weekday not in (2, 6):
            raise ValueError('Weekday numeric argument must be 2 or 6')
    else:
        raise ValueError('Weekday is accepted as either string or numeric form')

    today = datetime.date.today()
    while today.weekday() != weekday:
        today += datetime.timedelta(1)

    return today

def main():
    print(find_next_weekday('saturday'))


if __name__ == '__main__':
    main()