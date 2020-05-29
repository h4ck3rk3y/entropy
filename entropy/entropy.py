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
from datetime import datetime, timedelta
import configparser


JOURNAL_PATH = Path.expanduser(PosixPath("~/.entropy/journal"))
STATUS_PATH = Path.expanduser(PosixPath("~/.entropy/status.txt"))

__version__ = '0.1.0'


def today():
    today = datetime.today()
    return today.strftime("%Y-%m-%d")


def yesterday():
    yesterday = datetime.today() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def week():
    today_ = datetime.today()
    week = [(today_ + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0 - today_.weekday(), 7 - today_.weekday())]
    return week

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
        if day in data:
            if data[day]:
                well+=1
            else:
                wasted+=1
            status.append((day, data[day]))
        else:
            none+=1
            status.append((day, None))
    return status, wasted, well, none

def handle_status_view(arguments):
    config = configparser.ConfigParser()
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
            data = config["DEFAULT"]._options()
            status, wasted, well, none = get_statistics_for_timerange(week(), data)



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
