#!/usr/bin/env python3

from . import __package_name__, __version__, __description__
from .tasks import add_task, delete_task
from .groups import add_group, delete_group, soft_delete_group
from .storage import get_storage

import argparse
from datetime import datetime, date
import sys


def clear():
    """
    Clears todo list - removes all tasks.
    """

    with get_storage() as s:
        s["tasks"].clear()
        s["groups"].clear()

    print("\nYour list has been cleared out.\n")


def parse_arguments():
    """
    Parses CLI arguments and returns Namespace object.

    :return: Namespace object with parsed params.
    :rtype: Namespace
    """

    parser = argparse.ArgumentParser(prog=__package_name__, description=__description__)

    # 1. Task
    # -a, --add
    h = (
        "Creates a task like: -a \"do the right thing\" or -a \"make yo bed\" 1d or -a \"make yo sis bed\" @20/1/2050. "
        "For recurring tasks you can use \"d\", \"w\", \"m\", \"y\" for days, weeks, months, years."
    )
    parser.add_argument("-a", "--add", nargs="+", action="append", help=h)

    # -d, --delete
    h = "Removes an item from todo list. Cannot be undone."
    parser.add_argument("-d", "--delete", nargs=1, type=int, action="append", help=h)

    # -c, --clear
    h = "Clears todo list - removes all the tasks. No undo."
    parser.add_argument("-c", "--clear", action="store_true", help=h)

    # 2. Group
    # -A, --add-group
    h = "Creates a group which can be used for managing tasks."
    parser.add_argument("-A", "--add-group", nargs=1, action="append", help=h)

    # -D, --delete-group
    h = "Removes a group and tasks attached to the group."
    parser.add_argument("-D", "--delete-group", nargs=1, action="append", help=h)

    # -S, --soft-delete-group
    h = "Removes a group and tasks attached to the group are pulled out."
    parser.add_argument("-S", "--soft-delete-group", nargs=1, action="append", help=h)

    # --version
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    return parser.parse_args()


def get_printable_freq(freq):
    """
    Formats task frequency.

    :param datetime or str frequency: Frequency to be formatted.
    :return: Formatted frequency string.
    :rtype: str
    """

    # Display the frequency properly.
    if isinstance(freq, datetime):
        return freq.strftime("%m/%d/%Y")
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

    def print_task(number, task, freq=False):
        """
        Prints formatted task.

        :param int number: Order number of the task.
        :param Task task: Task object.
        :param str freq: Formatted task frequency.
        """

        group = ""

        # Format task group.
        if task.group:
            group = f" [{task.group}]"

        if freq:
            print(f"\t{number + 1}. {task.title} ({freq}){group}")
        else:
            print(f"\t{number + 1}. {task.title}{group}")

    def print_today_tasks(tasks):
        """
        Prints today tasks in numbered list.
        The item number is +1 of index from storage index.

        :param dict tasks: Task dict where key is task index and val Task instance.
        """

        print("\nToday:")

        for i, t in tasks.items():

            freq = get_printable_freq(t.frequency)

            # print(f"\t{i + 1}. {t.title} ({freq})")
            print_task(i, t, freq)

        # print("")

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
                # print(f"\t{i + 1}. {t.title} ({freq})")
                print_task(i, t, freq)
            else:
                # print(f"\t{i + 1}. {t.title}")
                print_task(i, t)

        print("")

    with get_storage() as s:

        today_tasks = {}
        other_tasks = {}

        for i, t in enumerate(s["tasks"]):

            if is_today_task(t):
                today_tasks[i] = t
            else:
                other_tasks[i] = t

        if today_tasks:
            print_today_tasks(today_tasks)

        if other_tasks:
            print_other_tasks(other_tasks)


def eagle():
    """
    Main app function. Spins up the wheel
    and delivers the output.
    """

    to_print = False

    if 1 < len(sys.argv):

        args = parse_arguments()
        # print(args)

        # Add task.
        if args.add:
            add_task(args.add)
            to_print = True

        # Delete task.
        if args.delete:
            delete_task(args.delete)
            to_print = True

        # Clear tasks.
        if args.clear:
            clear()

        # Add group.
        if args.add_group:
            add_group(args.add_group)
            to_print = True

        # Delete group.
        if args.delete_group:
            delete_group(args.delete_group)
            to_print = True

        # Soft delete group.
        if args.soft_delete_group:
            soft_delete_group(args.soft_delete_group)
            to_print = True

    else:
        to_print = True

    if to_print:
        print_list()


if "__main__" == __name__:
    eagle()
