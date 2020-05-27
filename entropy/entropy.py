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
from pathlib import Path
import datetime


JOURNAL_PATH="~/.entropy/journal"
STATUS_PATH="~/.entropy/status"

__version__ = '0.1.0'


def initial_setup():
    Path(JOURNAL_PATH).mkdir(parents=True, exist_ok=True)
    Path(STATUS_PATH).mkdir(parents=True, exist_ok=True)


def create_current_year(path):
    Path


def add_status_for_today(good=False):
    pass


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
    arguments = docopt(__doc__, version=__version__)

    if arguments["journal"]:
        print(arguments)
    elif arguments["status"]:
        status(arguments)
    else:
        print(__doc__)

if __name__ == '__main__':
    main()