from datetime import datetime, timedelta, date

TODAY = datetime.today()


def today():
    return TODAY.strftime("%Y-%m-%d")


def yesterday():
    yesterday = TODAY - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def week():
    today_ = TODAY
    week = [(today_ + timedelta(days=i))
            for i in range(0 - today_.weekday(), 7 - today_.weekday())]
    return week


def month():
    today_ = TODAY
    year_ = today_.year
    month_ = today_.month
    days = [date(year_, month_, day) for day in range(1, today_.day+1)]
    return days


def year():
    today_ = TODAY
    year_ = today_.year
    day_of_year = today_.timetuple().tm_yday
    days = [date(year_, 1, 1) + timedelta(days=day)
            for day in range(1, day_of_year)]
    return days
