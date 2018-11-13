from .storage import get_storage, Group, Task
from .tools import err_print

from datetime import datetime


def add_group(groups):
    """
    Creates new group. Group title has to be unique.

    :param list groups: List of lists of group titles.
    """

    # Flatten group list.
    groups = [g for g_list in groups for g in g_list]

    with get_storage() as s:
        for g in groups:
            if not group_exist(g):
                s["groups"].append(Group(g, datetime.now()))
            else:
                err_print(f"Group \"{g}\" already exists.")


def delete_group(groups):
    """
    Deletes groups from storage including belonging tasks.

    :param list groups: List of lists of groups.
    """

    # Flatten group list.
    groups = [g for g_list in groups for g in g_list]

    with get_storage() as s:

        # Delete in reverse order so no item are skipped
        # once pop() method is called on the storage.
        for i, t in sorted(enumerate(s["tasks"]), reverse=True):

            # Compare by group name.
            if t.group in groups:
                s["tasks"].pop(i)

        for i, g in enumerate(s["groups"]):

            # Compare by group name.
            if g.title in groups:
                s["groups"].pop(i)


def soft_delete_group(groups):
    """
    Deletes groups from storage and belonging
    tasks are ungrouped.

    :param list groups: List of lists of groups.
    """

    def ungroup_tasks(storage, group):
        """
        Removes given group from all tasks that uses it.

        :param dict storge: Storage object (dictionary).
        :param str group: Group title.
        """

        for i, t in enumerate(storage["tasks"]):
            if group == t.group:

                # Cannot modify existing task so let's create a new
                # one without group.
                storage["tasks"][i] = Task(t.title, t.frequency, None, t.created)

    # Flatten group list.
    groups = [g for g_list in groups for g in g_list]

    with get_storage() as s:
        for i, g in enumerate(s["groups"]):

            # Compare by group name.
            if g.title in groups:
                ungroup_tasks(s, g.title)
                s["groups"].pop(i)


def group_exist(title):
    """
    Checks uniqueness of group by comparing titles.

    :param str title: Group title.
    :return: True if the group title is already taken, False otherwise.
    :rtype: bool
    """

    with get_storage() as s:
        for i, g in enumerate(s["groups"]):
            if title == g.title:
                return True
