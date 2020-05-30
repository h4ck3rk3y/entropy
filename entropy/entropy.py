r"""
entropy is a command line friend that helps you reduce entropy
in your life

Usage:
    entropy journal add
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


TODAY = datetime.today()
JOURNAL_PATH = Path.expanduser(PosixPath("~/.entropy/journal"))
STATUS_PATH = Path.expanduser(PosixPath("~/.entropy/status.txt"))
TODAYS_FOLDER_TO_SAVE = str(JOURNAL_PATH) + "/" + \
    str(TODAY.year) + "/" + \
    TODAY.strftime("%B")


QUESTIONS = [
    ("I am grateful for", 1),
    ("What would make today great?", 3),
    ("Daily affirmations. I am", 1),
    ("Amazing thing that happened yesterday", 1)
]

__version__ = '0.1.0'


def print_to_screen(status, wasted, well, none):
    init()
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


def get_journal_path(journal_date):
    journal_path = str(JOURNAL_PATH) + "/" + \
        str(journal_date.year) + "/" + \
        journal_date.strftime("%B") + \
        "/" + journal_date.strftime("%Y-%m-%d") + ".txt"
    return journal_path


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
    if status_exists_for_date(TODAY):
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
    status, wasted, well, none = None, None, None, None
    with open(STATUS_PATH, 'r') as status_file:
        config.read_file(status_file)
        data = config["DEFAULT"]._options()
        if arguments["today"]:
            today_ = today()
            if today_ not in data:
                print("Today isn't set")
            elif data[today_] == 'True':
                print("Today was good")
            else:
                print("Today was a failure")
        elif arguments["yesterday"]:
            yesterday_ = yesterday()
            if yesterday_ not in data:
                print("Yesterday isn't set")
            elif data[yesterday_] == 'True':
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


def parse_date(input_date):
    try:
        date = datetime.strptime(input_date, "%Y-%m-%d")
        return date
    except:
        print(Fore.RED, "Invalid, try something like entropy view journal YYYY-mm-dd")
        return False


def handle_view_journal(arguments):
    journal_date = None
    if arguments["today"]:
        journal_date = TODAY
    elif arguments["yesterday"]:
        journal_date = TODAY - timedelta(days=1)
    elif arguments["<date>"]:
        journal_date = parse_date(arguments["<date>"])
        if not journal_date:
            return
    display_journal(journal_date)


def file_exits(path):
    return Path(path).exists()


def is_a_question(line):
    for question_ in QUESTIONS:
        question = question_[0]
        if question in line:
            return True
    return False


def display_journal(journal_date):
    journal_path = get_journal_path(journal_date)
    if not file_exits(journal_path):
        print(Fore.RED, "Sorry we don't have an entry for this date")
        return
    with open(journal_path, 'r') as journal_file:
        for line in journal_file.readlines():
            if is_a_question(line):
                print(Fore.BLUE, line, end="")
            else:
                print(Fore.GREEN, line, end="")


def save_journal(journal, day=TODAY):
    Path(TODAYS_FOLDER_TO_SAVE).mkdir(exist_ok=True, parents=True)
    with open(get_journal_path(day), 'w') as journal_file:
        for (question, responses) in journal:
            print(question, file=journal_file)
            if len(responses) > 1:
                for index, response in enumerate(responses):
                    print("  {}. ".format(index+1) +
                          response, file=journal_file)
            else:
                print(responses[0], file=journal_file)
    print(Fore.CYAN, "Journal entry saved at {}.\n Tweak it if you want to make edits".format(
        get_journal_path(day)))


def handle_add_journal(arguments):
    journal = []
    if file_exits(get_journal_path(TODAY)):
        print(Fore.RED, "Journal entry already exits at:\n {}.\n Please edit it to make changes.".format(
            get_journal_path(TODAY)))
        return
    for item in QUESTIONS:
        question = item[0]
        times = item[1]
        response = []
        print(Fore.BLUE, question)
        if times > 1:
            print(Fore.YELLOW, "You will be asked to add {} points".format(times))
            for time in range(times):
                response.append(input(Fore.GREEN + "{}. ".format(time+1)))
        else:
            response.append(input(Fore.GREEN + "> "))
        journal.append((question, response))
    save_journal(journal)


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
        journal(arguments)
    elif arguments["status"]:
        status(arguments)
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
