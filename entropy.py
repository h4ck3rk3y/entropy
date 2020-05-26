r"""
entropy is a command friend that helps you reduce entropy
in your life

Usage:
    entropy journal add <filename>
    entropy journal view
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

__version__ = '0.1.0'


def status(arguments):
    if arguments['add']:

def main():
    '''entropy helps you lower entropy in your life'''
    
    arguments = docopt(__doc__, version=__version__)

    if arguments["journal"]:
        print(arguments)
    elif arguments["status"]:
        status(arguments['status'])
    else:
        print(__doc__)

if __name__ == '__main__':
    main()