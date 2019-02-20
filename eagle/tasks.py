from .storage import get_storage, Task
from .groups import group_exist, add_group
from .tools import err_print

from datetime import datetime, date, timedelta


def add_task(tasks):
    """
    Creates new task.

    1. place takes the task name.
    2. place takes date/frequency [optional] - or "-".
    3. place takes group [optional].

    Frequency might be "@dd/mm/yyyy" or "@dd/mm" or just:

    * Xd - i.e.: 1d (every day)
    * Xw - i.e.: 1w (every week)
    * Xm - i.e.: 1m (every month)
    * Xy - i.e.: 1y (every year)

    or

    +X - X is number of days in future

    or magic names:

    * today
    * tomorrow

    :param list groups: List of lists of task params(task, frequency, group).
    """

    def parse_frequency(f):

        # 1. specific date.
        if f.startswith("@"):

            # Try (D)D/(M)M/YYYY
            # or fallback to (D)D/(M)M where year will be the current one.
            try:
                return datetime.strptime(f[1:], "%d/%m/%Y")
            except ValueError:
                d = datetime.strptime(f[1:], "%d/%m")

                return d.replace(year=date.today().year)

        # 2. Magic date name
        if "today" == f:
            return datetime.now()

        if "tomorrow" == f:
            return datetime.now() + timedelta(days=1)

        # 3. +XY days
        # Handles the "+X" days - like "+5".
        # If cannot parse days number fallbacks to "today".
        if f.startswith("+"):
            try:
                days = int(f[1:])
            except:
                days = 0

            return datetime.now() + timedelta(days=days)

        # 4. X(d|w|m|y) - i.e. "2w".
        if 2 <= len(f) and f[-1] in ["d", "w", "m", "y"]:
            return f

        # 5. No date at all - fallback.
        if "-" == f:
            return None

        # No frequecy has been recognized.
        err_print("No known frequency recognized. Task added without frequency.")

    # Append new task to the todo list.
    with get_storage() as s:
        for t in tasks:

            # Check if group was mentioned.
            if 3 == len(t) and not group_exist(t[2]):
                add_group([[t[2]]])

            # If a frequency was given "t" variable has 2 items.
            s["tasks"].append(Task(
                t[0],
                parse_frequency(t[1]) if 1 < len(t) else None,
                t[2] if 3 == len(t) else None,
                datetime.now()
            ))


def delete_task(index_list):
    """
    Deletes a task from storage by index.

    :param list index: List of lists of task indexes to be deleted.
    """

    # Sort the IDs descending so while we pop item by item
    # the task indexes remains the same.
    to_delete = sorted([i[0] for i in index_list], reverse=True)

    with get_storage() as s:

        for i in to_delete:
            try:
                s["tasks"].pop(int(i) - 1)
            except IndexError:
                print(f"Cannot delete {i}")
