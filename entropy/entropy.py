r"""
entropy is a command friend that helps you reduce entropy
in your life

Usage:
    entropy journal add <filename>
    entropy journal view today
    entropy journal view yesterday
    entropy journal view <date>
    entropy status add
    entropy status today
    entropy status yesterday
    entropy status week
    entropy status month
    entropy status year
    entropy status life

Options:
    -h --help Show this screen
    --version Shows the version
"""

from docopt import docopt
from pathlib import Path, PosixPath
from datetime import datetime, timedelta, date
import calendar
import configparser
from colorama import init, Fore, Back
from time_to_object import get_message


JOURNAL_PATH = Path.expanduser(PosixPath("~/.entropy/journal"))
STATUS_PATH = Path.expanduser(PosixPath("~/.entropy/status.txt"))

__version__ = '0.1.0'


def print_to_screen(status, wasted, well, none):
    init()
    for item in status:
        if item[1] == 'True':
            print(Fore.GREEN, "✓", end="")
        elif item[1] == 'False':
            print(Fore.RED, "X", end="")
        elif item[1] == None:
            print(Fore.WHITE, "-", end="")
    print("")
    if well and well > 1:
        print(Fore.GREEN, "You did well on {} days".format(well))
    elif well:
        print(Fore.GREEN, "You did well on {} day".format(well))
    if wasted:
        if wasted > 1:
            print(Fore.RED, "You wasted {} days".format(wasted))
        else:
            print(Fore.RED, "You wasted {} day".format(wasted))
        print(Fore.MAGENTA, get_message(wasted), "in the time you wasted")
    if none:
        print(Fore.WHITE, "We have no information for {} day(s)".format(none))


def today():
    today = datetime.today()
    return today.strftime("%Y-%m-%d")


def yesterday():
    yesterday = datetime.today() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def week():
    today_ = datetime.today()
    week = [(today_ + timedelta(days=i))
            for i in range(0 - today_.weekday(), 7 - today_.weekday())]
    return week


def month():
    today_ = datetime.today()
    year_ = today_.year
    month_ = today_.month
    num_days = calendar.monthrange(year_, month_)[1]
    days = [date(year_, month_, day) for day in range(1, num_days+1)]
    return days


def year():
    today_ = datetime.today()
    year_ = today_.year
    day_of_year = today_.timetuple().tm_yday
    days = [date(year_, 1, 1) + timedelta(days=day)
            for day in range(1, day_of_year)]
    return days


def initial_setup():
    Path(JOURNAL_PATH).mkdir(parents=True, exist_ok=True)
    Path(STATUS_PATH).touch()


def create_today():
    now = datetime.now()
    Path(JOURNAL_PATH + "/" + now.year + "/" + now.month +
         "/" + now.day).mkdir(parents=True, exist_ok=True)


def status_exists_for_date(date):
    with open(STATUS_PATH, 'r') as status_file:
        config = configparser.ConfigParser()
        config.read_file(status_file)
        return config.has_option(None, today())


def add_status_for_today(good=False):
    config = configparser.ConfigParser()
    with open(STATUS_PATH, 'r') as status_file:
        config.read_file(status_file)
    with open(STATUS_PATH, 'w') as status_file:
        config.set("DEFAULT", today(), str(good))
        config.write(status_file)


def handle_add_status(arguments):
    if status_exists_for_date(datetime.today()):
        print("You have already added a status for today")
        return
    while True:
        response = input('Do you consider today succesful? [y/n]\n>')
        if response == 'y' or response == 'Y':
            add_status_for_today(True)
            break
        elif response == 'n' or response == 'N':
            add_status_for_today(False)
            break
        else:
            print('I didnt quite understand what you said')


def get_statistics_for_timerange(duration, data):
    status = []
    wasted = 0
    well = 0
    none = 0
    for day in duration:
        formatted_day = day.strftime("%Y-%m-%d")
        if formatted_day in data:
            if data[formatted_day] == 'True':
                well += 1
            else:
                wasted += 1
            status.append((formatted_day, data[formatted_day]))
        else:
            none += 1
            status.append((formatted_day, None))
    return status, wasted, well, none


def handle_status_view(arguments):
    config = configparser.ConfigParser()
    data = config["DEFAULT"]._options()
    status, wasted, well, none = None, None, None, None
    with open(STATUS_PATH, 'r') as status_file:
        config.read_file(status_file)
        if arguments["today"]:
            today_ = config.getboolean("DEFAULT", today())
            if today_ is None:
                print("Today isn't set")
            elif today_ is True:
                print("Today was good")
            else:
                print("Today was a failure")
        elif arguments["yesterday"]:
            yesterday_ = config.getboolean("DEFAULT", yesterday())
            if yesterday_ is None:
                print("Yesterday isn't set")
            elif yesterday_ is True:
                print("Yesterday was good")
            else:
                print("Yesterday was a failure")
        elif arguments["week"]:
            status, wasted, well, none = get_statistics_for_timerange(
                week(), data)
        elif arguments["month"]:
            status, wasted, well, none = get_statistics_for_timerange(
                month(), data)
        elif arguments["year"]:
            status, wasted, well, none = get_statistics_for_timerange(
                year(), data)
        elif arguments["life"]:
            life = [datetime.strptime(day, "%Y-%m-%d") for day in data]
            status, wasted, well, none = get_statistics_for_timerange(
                life, data)
        if status:
            print_to_screen(status, wasted, well, none)


def handle_view_journal(arguments):
    pass


def handle_add_journal(arguments):
    pass


def journal(arguments):
    if arguments["add"]:
        handle_add_journal(arguments)
    elif arguments["view"]:
        handle_view_journal(arguments)


def status(arguments):
    if arguments["add"]:
        handle_add_status(arguments)
    else:
        handle_status_view(arguments)


def main():
    '''entropy helps you lower entropy in your life'''

    initial_setup()

    arguments = docopt(__doc__, version=__version__)

    if arguments["journal"]:
        print(arguments)
    elif arguments["status"]:
        status(arguments)
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
