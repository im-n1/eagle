from .storage import get_storage, Task
from .groups import group_exist, add_group

from datetime import datetime


def add_task(tasks):
    """
    Creates new task.

    Frequency might be "@dd/mm/yyyy" or just:

    * Xd - i.e.: 1d (every day)
    * Xw - i.e.: 1w (every week)
    * Xm - i.e.: 1m (every month)
    * Xy - i.e.: 1y (every year)

    :param list groups: List of lists of task params(task, frequency, group).
    """

    def parse_frequency(f):

        if f.startswith("@"):
            return datetime.strptime(f[1:], "%d/%m/%Y")

        return f

    # Append new task to the todo list.
    with get_storage() as s:
        for t in tasks:

            # Check if group was mentioned.
            if 3 == len(t) and not group_exist(t[2]):
                add_group([[t[2]]])

            # If a frequency was given "t" variable has 2 items.
            s["tasks"].append(Task(
                t[0],
                parse_frequency(t[1]) if 2 <= len(t) and "-" != t[1] else None,  # Also handles the "-" date as None.
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
