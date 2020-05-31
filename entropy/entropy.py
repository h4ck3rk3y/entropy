r"""
entropy is a command line friend that helps you reduce entropy
in your life

Usage:
    entropy journal add
    entropy journal view today
    entropy journal view yesterday
    entropy journal view <date>
    entropy status add
    entropy status view today
    entropy status view yesterday
    entropy status view week
    entropy status view month
    entropy status view year
    entropy status view life
    entropy status view <date>

Options:
    -h --help Show this screen
    --version Shows the version
"""

from docopt import docopt
from pathlib import Path
import configparser
from colorama import init, Fore

from .date_utils import TODAY, YESTERDAY, week, month, year, life, parse_date
from .status import STATUS_PATH, print_to_screen, print_today, print_yesterday, print_one_date, status_exists_for_date, add_status_for_today, get_statistics_for_timerange
from .journal import QUESTIONS, JOURNAL_PATH, display_journal, get_journal_path, save_journal, journal_exists_for_date
from .file_utils import file_exists

__version__ = '0.1.5'


def initial_setup():
    init()
    Path(JOURNAL_PATH).mkdir(parents=True, exist_ok=True)
    Path(STATUS_PATH).touch()


def handle_add_status(arguments):
    if status_exists_for_date(TODAY):
        print(Fore.RED, "You have already added a status for today")
        return
    if not journal_exists_for_date(TODAY):
        print(Fore.YELLOW, "You forgot to add a journal entry this morning!")
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


def handle_status_view(arguments):
    config = configparser.ConfigParser()
    status, wasted, well, none = None, None, None, None
    with open(STATUS_PATH, 'r') as status_file:
        config.read_file(status_file)
        data = config["DEFAULT"]._options()
        if arguments["today"]:
            print_today(data)
        elif arguments["yesterday"]:
            print_yesterday(data)
        elif arguments["<date>"]:
            day = parse_date(arguments["<date>"])
            if not day:
                print(
                    Fore.RED, "Invalid, try something like entropy view journal YYYY-mm-dd")
                return
            day = day.strftime("%Y-%m-%d")
            print_one_date(day, data, day)
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
            status, wasted, well, none = get_statistics_for_timerange(
                life(data), data)
        if status:
            print_to_screen(status, wasted, well, none)


def handle_view_journal(arguments):
    journal_date = None
    if arguments["today"]:
        journal_date = TODAY
    elif arguments["yesterday"]:
        journal_date = YESTERDAY
    elif arguments["<date>"]:
        journal_date = parse_date(arguments["<date>"])
        if not journal_date:
            print(Fore.RED, "Invalid, try something like entropy view journal YYYY-mm-dd")
            return
    display_journal(journal_date)


def handle_add_journal(arguments):
    if file_exists(get_journal_path(TODAY)):
        print(Fore.RED, "Journal entry already exits at:\n {}.\n Please edit it to make changes.".format(
            get_journal_path(TODAY)))
        return
    if not status_exists_for_date(YESTERDAY):
        print(Fore.YELLOW, "You forgot to add a status entry yesterday night!")
    journal = []
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


def handle_journal(arguments):
    if arguments["add"]:
        handle_add_journal(arguments)
    elif arguments["view"]:
        handle_view_journal(arguments)


def handle_status(arguments):
    if arguments["add"]:
        handle_add_status(arguments)
    else:
        handle_status_view(arguments)


def main():
    '''entropy helps you lower entropy in your life'''

    initial_setup()

    arguments = docopt(__doc__, version=__version__)

    if arguments["journal"]:
        handle_journal(arguments)
    elif arguments["status"]:
        handle_status(arguments)
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
