from colorama import Fore
from pathlib import Path
import configparser

from .date_utils import today, yesterday
from .time_to_object import get_message

STATUS_PATH = Path.expanduser(Path("~/.entropy/status.txt"))


def print_to_screen(status, wasted, well, none):
    for index, item in enumerate(status):
        if index and index % 31 == 0:
            print("")
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
    if wasted and wasted > 1:
        print(Fore.RED, "You wasted {} days".format(wasted))
        print(Fore.MAGENTA, get_message(wasted), "in this time")
    elif wasted:
        print(Fore.RED, "You wasted {} day".format(wasted))
        print(Fore.MAGENTA, get_message(wasted), "in this time")
    else:
        print(Fore.GREEN, "You have done well on all reported days!")
    if none and none > 1:
        print(Fore.WHITE, "We have no information for {} days".format(none))
    elif none:
        print(Fore.WHITE, "We have no information for {} day".format(none))


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


def print_today(data):
    print_one_date(today(), data, "Today")


def print_yesterday(data):
    print_one_date(yesterday(), data, "Yesterday")


def print_one_date(day, data, name):
    if day not in data:
        print("{} isn't set".format(name))
    elif data[day] == 'True':
        print("{} was good".format(name))
    else:
        print("{} was a failure".format(name))
