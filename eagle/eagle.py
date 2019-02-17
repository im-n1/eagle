#!/usr/bin/env python3

from . import __package_name__, __description__, __author__, \
    __homepage__, __version__
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
    meta = ("TASK", "FREQUENCY (and GROUP)")
    parser.add_argument("-a", "--add", nargs="+", action="append", metavar=meta, help=h)

    # -d, --delete
    h = "Removes an item from todo list. Cannot be undone."
    meta = "TASK"
    parser.add_argument("-d", "--delete", nargs=1, type=int, action="append", metavar=meta, help=h)

    # -c, --clear
    h = "Clears todo list - removes all the tasks. No undo."
    parser.add_argument("-c", "--clear", action="store_true", help=h)

    # 2. Group
    # -A, --add-group
    h = "Creates a group which can be used for managing tasks."
    meta = "GROUP"
    parser.add_argument("-A", "--add-group", nargs=1, action="append", metavar=meta, help=h)

    # -D, --delete-group
    h = "Removes a group and tasks attached to the group."
    meta = "GROUP"
    parser.add_argument("-D", "--delete-group", nargs=1, action="append", metavar=meta, help=h)

    # -S, --soft-delete-group
    h = "Removes a group and tasks attached to the group are pulled out."
    meta = "GROUP"
    parser.add_argument("-S", "--soft-delete-group", nargs=1, action="append", metavar=meta, help=h)

    # 3. List
    # -g, --group
    h = "Filters tasks by group."
    parser.add_argument("-g", "--group", nargs=1, action="append", help=h)

    # -t, --today
    h = "Filters today's tasks."
    parser.add_argument("-t", "--today", action="store_true", help=h)

    # -o, --others
    h = "Filters others tasks."
    parser.add_argument("-o", "--others", action="store_true", help=h)

    # --sort
    h = "Sort tasks by the given flag. Possible options are: \"groups\"."
    parser.add_argument("--sort", choices=["groups"], help=h)

    # --version
    # parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    h = "Shows version and other useful informations."
    parser.add_argument("--version", action="store_true", help=h)

    return parser.parse_args()


def print_list(tasks=None, sort_by=None):
    """
    Prints today and other tasks.

    :param list tasks: List of already filtered tasks.
    :param str sort_by: Sort the task by given flag - choices: "groups"
    """

    def get_printable_freq(freq):
        """
        Formats task frequency.

        :param datetime or str frequency: Frequency to be formatted.
        :return: Formatted frequency string.
        :rtype: str
        """

        # Display the frequency properly.
        if isinstance(freq, datetime):
            return freq.strftime("%d/%m/%Y")
        else:
            return freq

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

        for i, t in tasks:

            freq = get_printable_freq(t.frequency)
            print_task(i, t, freq)

    def print_other_tasks(tasks):
        """
        Prints other (besides today) tasks in numbered list.
        The item number is +1 of index from storage index.

        :param dict tasks: Task dict where key is task index and val Task instance.
        """

        print("\nYour list:")

        for i, t in tasks:

            if t.frequency:
                freq = get_printable_freq(t.frequency)
                # print(f"\t{i + 1}. {t.title} ({freq})")
                print_task(i, t, freq)
            else:
                # print(f"\t{i + 1}. {t.title}")
                print_task(i, t)

        print("")

    def sort_tasks(tasks, flag):
        """
        Sorts tasks by the given flag.
        Choices are:
            * groups

        :param list tasks: List of tasks.
        :param str sort_by: The sort flag.
        """

        if "groups" == flag:
            return sorted(tasks, key=lambda t: t[1].group if t[1].group else "")

    # Load tasks.
    if tasks is None:
        with get_storage() as s:
            tasks = s["tasks"]

    today_tasks = []
    other_tasks = []
    tasks = zip(range(0, len(tasks)), tasks)

    # Gather tasks.
    for i, t in tasks:

        if t.is_today_task():
            today_tasks.append((i, t))
        else:
            other_tasks.append((i, t))

    # Sort tasks.
    if sort_by:
        if today_tasks:
            today_tasks = sort_tasks(today_tasks, sort_by)
        if other_tasks:
            other_tasks = sort_tasks(other_tasks, sort_by)

    if today_tasks:
        print_today_tasks(today_tasks)

    if other_tasks:
        print_other_tasks(other_tasks)


def filter_tasks_by_groups(tasks=None, groups=None):
    """
    Filters tasks by the given groups.

    :param list tasks: List of already filtered tasks.
    :param list groups: List of existing groups.
    :return: Narrowed list of tasks.
    :rtype: list
    """

    # Load tasks.
    if tasks is None:
        with get_storage() as s:
            tasks = s["tasks"]

    # Flatten group list.
    if groups:
        groups = [g for g_list in groups for g in g_list]
        tasks = list(filter(lambda t: t.group in groups, tasks))

    return tasks


def filter_today_tasks(tasks=None):
    """
    Filters today's tasks.

    :param list tasks: List of already filtered tasks.
    :return: Narrowed list of tasks.
    :rtype: list
    """

    # Load tasks.
    if tasks is None:
        with get_storage() as s:
            tasks = s["tasks"]

    return list(filter(lambda t: t.is_today_task(), tasks))


def filter_other_tasks(tasks=None):
    """
    Filters other tasks.

    :param list tasks: List of already filtered tasks.
    :return: Narrowed list of tasks.
    :rtype: list
    """

    # Load tasks.
    if not tasks:
        with get_storage() as s:
            tasks = s["tasks"]

    return list(filter(lambda t: not t.is_today_task(), tasks))


def eagle():
    """
    Main app function. Spins up the wheel
    and delivers the output.
    """

    to_print = False
    groups = None
    tasks = None
    args = None

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

        # Filter by group.
        if args.group:
            to_print = True
            tasks = filter_tasks_by_groups(tasks, args.group)

        # Filter today's tasks.
        if args.today:
            to_print = True
            tasks = filter_today_tasks(tasks)

        # Filter other tasks.
        if args.others:
            to_print = True
            tasks = filter_other_tasks(tasks)

        # Sort.
        if args.sort:
            to_print = True

        # Version.
        if args.version:
            print((
                f"{__package_name__} {__version__}\n"
                f"Author: {__author__}\n"
                f"Homepage: {__homepage__}"
            ))

    else:
        to_print = True

    if to_print:
        print_list(tasks, args.sort if args else None)


if "__main__" == __name__:
    eagle()
