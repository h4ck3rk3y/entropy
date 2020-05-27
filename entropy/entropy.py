r"""
entropy is a command friend that helps you reduce entropy
in your life

Usage:
    entropy journal add <filename>
    entropy journal view today
    entropy journal view yesterday
    entropy journal view <date>
    entropy status add
    entropy status day
    entropy status week
    entropy status month
    entropy status life

Options:
    -h --help Show this screen
    --version Shows the version
"""

from docopt import docopt
from pathlib import Path, PosixPath
from datetime import datetime
import configparser


JOURNAL_PATH=Path.expanduser(PosixPath("~/.entropy/journal"))
STATUS_PATH=Path.expanduser(PosixPath("~/.entropy/status.txt"))
CONF=Path.expanduser(PosixPath("~/.entropy/entropy.conf"))

SET_UNSET_DAYS_TO_BAD=True

__version__ = '0.1.0'


def parse_conf():
    config = configparser.ConfigParser()
    config.read(CONF)
    if config.has_section("DEFAULT"):
        SET_UNSET_DAYS_TO_BAD = config["DEFAULT"].get(SET_UNSET_DAYS_TO_BAD, False)

def initial_setup():
    Path(JOURNAL_PATH).mkdir(parents=True, exist_ok=True)


def create_today():
    today = datetime.now()
    Path(JOURNAL_PATH + "/" + today.year + "/" + today.month + "/" + today.day).mkdir(parents=True, exist_ok=True)


def add_status_for_today(good=False):
    with open(STATUS_PATH, 'a') as status_file:
        status_file.write("{0}={1}".format(datetime.today().strftime("%Y-%m-%d"), good))


def handle_add_status(arguments):
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
    pass

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
    parse_conf()

    arguments = docopt(__doc__, version=__version__)

    if arguments["journal"]:
        print(arguments)
    elif arguments["status"]:
        status(arguments)
    else:
        print(__doc__)

if __name__ == '__main__':
    main()