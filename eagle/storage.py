import pickle
from contextlib import contextmanager
from collections import namedtuple
import os
# import pprint
from datetime import datetime, date


# Main structures.
Task = namedtuple("Task", "title frequency group created")
Group = namedtuple("Group", "title created")


def is_today_task(self):
    """
    Checks if the task is placed on today (in case of dated tasks)
    or is recurring on this day (in case of recurring tasks).
    """

    # Check for hypen.
    if self.frequency is None:
        return False

    # Check for specific date.
    if isinstance(self.frequency, datetime):
        if self.frequency.date() == date.today():
            return True

        return False

    # Parse frequency - for example "1d".
    number = int(self.frequency[:-1])
    period = self.frequency[-1:]

    delta = (date.today() - self.created.date()).days

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

Task.is_today_task = is_today_task


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


def serialize_structures(storage):
    """
    Serializes storage structures into dict.

    :param dict storage: Storage dict.
    :return: Serialized storage.
    :rtype: dict
    """

    return {
        "tasks": [list(t._asdict().values()) for t in storage["tasks"]],
        "groups": [list(g._asdict().values()) for g in storage["groups"]],
    }


def deserialize_structures(storage):
    """
    Deserializes storage structures into named tuples.

    :param dict storage: Storage dict.
    :return: Deserialized storage.
    :rtype: dict
    """

    return {
        "tasks": [Task._make(t) for t in storage.get("tasks", [])],
        "groups": [Group._make(g) for g in storage.get("groups", [])],
    }


@contextmanager
def get_storage():
    """
    Context manager for storage.
    On enter reads storage content and yields it out.
    On exit serializes and saved storage back to storage file.

    Storage file: storage.dat
    """

    def get_empty_storage():

        return {
            "groups": [],
            "tasks": [],
        }

    if hasattr(get_storage, "storage"):
        yield get_storage.storage

        return

    filename = get_conf_file("storage.dat")
    f = None

    # Try to open existing file and pickle the
    # content.
    try:
        f = open(filename, "rb+")

        # If file is empty set up the storage.
        if not os.stat(filename).st_size:
            get_storage.storage = get_empty_storage()
        else:
            get_storage.storage = deserialize_structures(pickle.load(f))
            f.close()

    except FileNotFoundError:
        get_storage.storage = get_empty_storage()

    # print("Storage:", pprint.pprint(get_storage.storage))

    yield get_storage.storage

    # Persist the storage.
    pickle.dump(serialize_structures(get_storage.storage), open(filename, "wb"))

    # Close file if previously opened.
    if f:
        f.close()
        del get_storage.storage
