#!/usr/bin/env python3

# from .structs import Task

import pickle
import argparse
from datetime import datetime, date
from collections import namedtuple
from contextlib import contextmanager
import os
import sys


Task = namedtuple("Task", "title frequency created")


def get_conf_file(file):
    """
    Returns path to file placed in user's config
    directory.
    Also checkes if the config directory exists and if not
    creates it.

    :param str file: File name.
    :return: Absolute path to the file.
    :rtype: str
    """

    conf_path = os.path.join(os.path.expanduser("~"), ".config", "eagle")

    if not os.path.exists(conf_path):
        os.makedirs(conf_path, mode=0o755)

    return os.path.join(conf_path, file)


@contextmanager
def get_storage():
    """
    Context manager for storage.
    On enter reads storage content and yields it out.
    On exit serializes and saved storage back to storage file.

    Storage file: storage.dat
    """

    filename = get_conf_file("storage.dat")
    f = None

    # Try to open existing file and pickle the
    # content.
    try:
        f = open(filename, "rb+")

        # If file is empty set up the storage
        # as empty list.
        if not os.stat(filename).st_size:
            storage = []
        else:
            storage = pickle.load(f)
            f.close()

    except FileNotFoundError:
        storage = []

    yield storage

    # Persist the storage.
    pickle.dump(storage, open(filename, "wb"))

    # Close file if previously opened.
    if f:
        f.close()


def clear():
    """
    Clears todo list - removes all tasks.
    """

    with get_storage() as s:
        s.clear()

    print("\nYour list has been cleared out.\n")


def parse_arguments():
    """
    Parses CLI arguments and returns Namespace object.

    :return: Namespace object with parsed params.
    :rtype: Namespace
    """

    parser = argparse.ArgumentParser()

    # -a, --add
    h = (
        "Add task like: -a \"make yo bed\" 1d or -a \"make yo sis bed\" @20/1/2050. "
        "You can also add tasks with a dash instead of a specific date like : -a \"get a life\" -. "
        "For recurring tasks you can use \"d\", \"w\", \"m\", \"y\" for days, weeks, months, years."
    )
    parser.add_argument("-a", "--add", nargs=2, help=h)

    # -d, --delete
    h = "Removes an item from todo list. Cannot be undone."
    parser.add_argument("-d", "--delete", nargs=1, help=h)

    # -c, --clear
    h = "Clears todo list - removes all the tasks. Cannot be undone."
    parser.add_argument("-c", "--clear", action="store_true", help=h)

    ns = parser.parse_args()

    return ns


def add_task(title, frequency):
    """
    Adds task to the list.

    Frequency might be "@dd/mm/yyyy" or just:

    * Xd - i.e.: 1d (every day)
    * Xw - i.e.: 1w (every week)
    * Xm - i.e.: 1m (every month)
    * Xy - i.e.: 1y (every year)

    :param str title: Title of the task.
    :param str frequency: Frequency string.
    """

    def parse_frequency(f):

        if "-" == f:
            return None

        if f.startswith("@"):
            return datetime.strptime(f[1:], "%d/%m/%Y")

        return f

    # Append new task to the todo list.
    with get_storage() as s:
        s.append(Task(title, parse_frequency(frequency), datetime.now()))


def delete_task(index):
    """
    Deletes a task from storage by index.

    :param int index: Index of task to be deleted.
    """

    with get_storage() as s:

        try:
            s.pop(int(index) - 1)
        except IndexError:
            pass


def get_printable_freq(freq):

    # Display the frequency properly.
    if isinstance(freq, datetime):
        return freq.strftime("%d/%m/%Y")
    else:
        return freq


def print_list():
    """
    Prints today and other tasks.
    """

    def is_today_task(task):
        """
        Checks if the task is placed on today (in case of dated tasks)
        or is recurring on this day (in case of recurring tasks).
        """

        # Check for hypen.
        if task.frequency is None:
            return False

        # Check for specific date.
        if isinstance(task.frequency, datetime):
            if task.frequency.date() == date.today():
                return True

            return False

        # Parse frequency.
        number = int(task.frequency[:-1])
        period = task.frequency[-1:]

        delta = (date.today() - task.created.date()).days

        # Day.
        if "d" == period and 0 == delta % number:
            return True

        # Week.
        if "w" == period and 0 == delta % (number * 7):
            return True

        # Month.
        if "m" == period and 0 == delta % (number * 30):
            return True

        # Year
        if "y" == period and 0 == delta % (number * 365):
            return True

    def print_today_tasks(tasks):
        """
        Prints today tasks in numbered list.
        The item number is +1 of index from storage index.

        :param dict tasks: Task dict where key is task index and val Task instance.
        """

        print("\nToday:")

        for i, t in tasks.items():

            freq = get_printable_freq(t.frequency)

            print(f"\t{i + 1}. {t.title} ({freq})")

        print("")

    def print_other_tasks(tasks):
        """
        Prints other (besides today) tasks in numbered list.
        The item number is +1 of index from storage index.

        :param dict tasks: Task dict where key is task index and val Task instance.
        """

        print("\nYour list:")

        for i, t in tasks.items():

            if t.frequency:
                freq = get_printable_freq(t.frequency)
                print(f"\t{i + 1}. {t.title} ({freq})")
            else:
                print(f"\t{i + 1}. {t.title}")

        print("\n")

    with get_storage() as s:

        today_tasks = {}
        other_tasks = {}

        for i, t in enumerate(s):

            if is_today_task(t):
                today_tasks[i] = t
            else:
                other_tasks[i] = t

        if today_tasks:
            print_today_tasks(today_tasks)

        if other_tasks:
            print_other_tasks(other_tasks)


def eagle():

    if 1 < len(sys.argv):

        args = parse_arguments()

        # Add.
        if args.add:
            add_task(*args.add)
            print_list()

        # Delete.
        if args.delete:
            delete_task(*args.delete)
            print_list()

        # Clear.
        if args.clear:
            clear()

    else:
        print_list()


if "__main__" == __name__:
    eagle()
