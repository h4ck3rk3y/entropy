from pathlib import Path
from colorama import Fore

from .date_utils import TODAY
from .file_utils import file_exists

JOURNAL_PATH = Path.expanduser(Path("~/.entropy/journal"))
TODAYS_FOLDER_TO_SAVE = str(JOURNAL_PATH) + "/" + \
    str(TODAY.year) + "/" + \
    TODAY.strftime("%B")
QUESTIONS = [
    ("I am grateful for", 1),
    ("What would make today great?", 3),
    ("Daily affirmations. I am", 1),
    ("Amazing thing that happened yesterday", 1)
]


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


def display_journal(journal_date):
    if not journal_exists_for_date(journal_date):
        print(Fore.RED, "Sorry we don't have an entry for this date")
        return
    journal_path = get_journal_path(journal_date)
    with open(journal_path, 'r') as journal_file:
        for line in journal_file.readlines():
            if is_a_question(line):
                print(Fore.BLUE, line, end="")
            else:
                print(Fore.GREEN, line, end="")


def journal_exists_for_date(day):
    journal_path = get_journal_path(day)
    return file_exists(journal_path)


def is_a_question(line):
    for question_ in QUESTIONS:
        question = question_[0]
        if question in line:
            return True
    return False


def get_journal_path(journal_date):
    journal_path = str(JOURNAL_PATH) + "/" + \
        str(journal_date.year) + "/" + \
        journal_date.strftime("%B") + \
        "/" + journal_date.strftime("%Y-%m-%d") + ".txt"
    return journal_path
