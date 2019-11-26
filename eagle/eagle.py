import argparse
import sys
from datetime import datetime

from .groups import add_group, delete_group, soft_delete_group
from .meta import CONFIG
from .storage import get_storage
from .tasks import add_task, delete_task, edit_task, prune


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

    parser = argparse.ArgumentParser(
        prog=CONFIG["package_name"], description=CONFIG["description"]
    )

    # 1. Task
    # -a, --add
    h = (
        'Creates a task like: -a "do the right thing" or -a "make yo bed" 1d or -a "make yo sis bed" @20/1/2050. '
        'For recurring tasks you can use "d", "w", "m", "y" for days, weeks, months, years.'
    )
    meta = ("TASK", "FREQUENCY (and GROUP)")
    parser.add_argument("-a", "--add", nargs="+", action="append", metavar=meta, help=h)

    # -d, --delete
    h = "Removes an item from todo list. Cannot be undone."
    meta = "TASK"
    parser.add_argument(
        "-d", "--delete", nargs=1, type=int, action="append", metavar=meta, help=h
    )

    # -c, --clear
    h = "Clears todo list - removes all the tasks. No undo."
    parser.add_argument("--clear", action="store_true", help=h)

    # --prune
    h = "Removes all overdue tasks."
    parser.add_argument("--prune", action="store_true", help=h)

    # 2. Group
    # -A, --add-group
    h = "Creates a group which can be used for managing tasks."
    meta = "GROUP"
    parser.add_argument(
        "-A", "--add-group", nargs=1, action="append", metavar=meta, help=h
    )

    # -D, --delete-group
    h = "Removes a group and tasks attached to the group."
    meta = "GROUP"
    parser.add_argument(
        "-D", "--delete-group", nargs=1, action="append", metavar=meta, help=h
    )

    # -S, --soft-delete-group
    h = "Removes a group and tasks attached to the group are pulled out."
    meta = "GROUP"
    parser.add_argument(
        "-S", "--soft-delete-group", nargs=1, action="append", metavar=meta, help=h
    )

    # -e
    h = "Edits a task."
    meta = "TASK"
    parser.add_argument("-e", "--edit", nargs=1, type=int, metavar=meta, help=h)

    # 3. List
    # -g, --group
    h = "Filters tasks by group."
    parser.add_argument("-g", "--group", nargs=1, action="append", help=h)

    # --overdue
    h = "Filters overdue tasks."
    parser.add_argument("--overdue", action="store_true", help=h)

    # --today
    h = "Filters today's tasks."
    parser.add_argument("--today", action="store_true", help=h)

    # --upcoming
    h = "Filters upcoming tasks (up to 3 days starting from today)."
    parser.add_argument("--upcoming", action="store_true", help=h)

    # --search
    h = "Searches tasks."
    meta = "QUERY"
    parser.add_argument("--search", nargs=1, action="append", metavar=meta, help=h)

    # --others
    h = "Filters others tasks."
    parser.add_argument("--others", action="store_true", help=h)

    # --sort
    h = 'Sort tasks by the given flag. Possible options are: "groups".'
    parser.add_argument("--sort", choices=["groups"], help=h)

    # --version
    # parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    h = "Shows version and other useful informations."
    parser.add_argument("--version", action="store_true", help=h)

    return parser.parse_args()


def print_list(tasks, sort_by=None, all_tasks=False):
    """
    Prints overdue, today upcoming and other tasks.

    :param list tasks: List of already filtered tasks - enumerated.
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

    def print_overdue_tasks(tasks):
        """
        Prints overdue tasks in numbered list.
        The item number is +1 of index from storage index.

        :param dict tasks: Task dict where key is task index and val Task instance.
        """

        print("\nOverdue:")

        for i, t in tasks:

            freq = get_printable_freq(t.frequency)
            print_task(i, t, freq)

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

    def print_upcoming_tasks(tasks):
        """
        Prints upcoming tasks in numbered list.
        The item number is +1 of index from storage index.

        :param dict tasks: Task dict where key is task index and val Task instance.
        """

        print("\nUpcoming:")

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
                print_task(i, t, freq)
            else:
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
    if all_tasks:
        with get_storage() as s:
            tasks = enumerate(s["tasks"])

    overdue_tasks = []
    today_tasks = []
    other_tasks = []
    upcoming_tasks = []
    # tasks = zip(range(0, len(tasks)), tasks)

    # Gather tasks.
    for i, t in tasks:

        if t.is_overdue():
            overdue_tasks.append((i, t))
        elif t.is_today_task():
            today_tasks.append((i, t))
        elif t.is_upcoming():
            upcoming_tasks.append((i, t))
        else:
            other_tasks.append((i, t))

    # Sort tasks.
    if sort_by:
        if overdue_tasks:
            overdue_tasks = sort_tasks(overdue_tasks, sort_by)
        if today_tasks:
            today_tasks = sort_tasks(today_tasks, sort_by)
        if other_tasks:
            other_tasks = sort_tasks(other_tasks, sort_by)

    if overdue_tasks:
        print_overdue_tasks(overdue_tasks)

    if today_tasks:
        print_today_tasks(today_tasks)

    if upcoming_tasks:
        print_upcoming_tasks(upcoming_tasks)

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
    if not tasks:
        with get_storage() as s:
            tasks = s["tasks"]

    # Flatten group list.
    if groups:
        groups = [g for g_list in groups for g in g_list]
        tasks = list(filter(lambda t: t[1].group in groups, enumerate(tasks)))

    return tasks


def filter_today_tasks():
    """
    Filters today's tasks.

    :return: Narrowed list of tasks - enumerated.
    :rtype: list
    """

    # Load tasks.
    with get_storage() as s:
        tasks = s["tasks"]

    return list(filter(lambda t: t[1].is_today_task(), enumerate(tasks)))


def filter_overdue_tasks():
    """
    Filters overdue tasks.

    :return: Narrowed list of tasks - enumerated.
    :rtype: list
    """

    # Load tasks.
    with get_storage() as s:
        tasks = s["tasks"]

    return list(filter(lambda t: t[1].is_overdue(), enumerate(tasks)))


def filter_other_tasks():
    """
    Filters other tasks.

    :return: Narrowed list of tasks.
    :rtype: list
    """

    # Load tasks.
    with get_storage() as s:
        tasks = enumerate(s["tasks"])

    return list(
        filter(lambda t: not t[1].is_today_task() and not t[1].is_overdue(), tasks)
    )


def search_tasks(queries):
    """
    Search tasks.

    :param str queries: Query string to be searched in tasks.
    :return: Narrowed list of tasks.
    :rtype: list
    """

    filtered_tasks = []
    queries = [q for q_list in queries for q in q_list]

    # Load tasks.
    with get_storage() as s:
        tasks = s["tasks"]

    for query in queries:
        filtered_tasks.extend(
            list(
                filter(lambda t: query.lower() in t[1].title.lower(), enumerate(tasks))
            )
        )

    return filtered_tasks


def filter_upcoming_tasks():
    """
    Filters upcoming tasks.

    :return: Narrowed list of tasks.
    :rtype: list
    """

    # Load tasks.
    with get_storage() as s:
        tasks = s["tasks"]

    return list(filter(lambda t: t[1].is_upcoming(), enumerate(tasks)))


def eagle():
    """
    Main app function. Spins up the wheel
    and delivers the output.
    """

    to_print = False
    # groups = None
    tasks = []
    args = None
    all_tasks = False

    if 1 < len(sys.argv):

        args = parse_arguments()
        # print(args)

        # Add task.
        if args.add:
            add_task(args.add)
            to_print = True

        # Edit task.
        if args.edit:
            edit_task(args.edit)
            to_print = True

        # Delete task.
        if args.delete:
            delete_task(args.delete)
            to_print = True

        # Clear tasks.
        if args.clear:
            clear()

        if args.prune:
            prune()

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
            tasks.extend(filter_tasks_by_groups(tasks, args.group))

        # Filter today's tasks.
        if args.today:
            to_print = True
            tasks.extend(filter_today_tasks())

        # Filter overdue tasks.
        if args.overdue:
            to_print = True
            tasks.extend(filter_overdue_tasks())

        # Filter upcoming tasks.
        if args.upcoming:
            to_print = True
            tasks.extend(filter_upcoming_tasks())

        # Search tasks.
        if args.search:
            to_print = True
            tasks.extend(search_tasks(args.search))

        # Filter other tasks.
        if args.others:
            to_print = True
            tasks.extend(filter_other_tasks())

        # Sort.
        if args.sort:
            to_print = True

        # Version.
        if args.version:
            print(
                (
                    f"{CONFIG['package_name']} {CONFIG['version']}\n"
                    f"Author: {CONFIG['author']}\n"
                    f"Homepage: {CONFIG['homepage']}"
                )
            )

    else:
        to_print = True
        all_tasks = True

    if to_print:
        print_list(tasks, args.sort if args else None, all_tasks)
