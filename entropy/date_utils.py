from datetime import datetime, timedelta, date

TODAY = datetime.today()
YESTERDAY = TODAY - timedelta(days=1)


def today():
    return TODAY.strftime("%Y-%m-%d")


def yesterday():
    return YESTERDAY.strftime("%Y-%m-%d")


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


def life(data):
    days = [datetime.strptime(day, "%Y-%m-%d") for day in data]
    return days


def parse_date(input_date):
    try:
        date = datetime.strptime(input_date, "%Y-%m-%d")
        return date
    except:
        return False
