Eagle
=====

.. image:: https://gitlab.com/n1_/eagle/raw/master/logo.png
   :align: center

Eagle is a simple CLI todo tool. It's so simple it hurts my coding skills.

How does it work?
-----------------

::

   ~ eagle

   Today:
       4. brush yo teeth

   Your list:

      1. do the laundry (every week)
      2. buy some food (each other day)
      3. buy presents (on 24th December)
      4. do the homework [School]

How can I install it?
---------------------
Don't worry about the early version number 0.x. I tend to Semantic Versioning more
than to "Marketing Versioning". That means version 0.5 is quite solid piece of
software instead or having version 25 and still not-even-half-way there.

So:

::

   pip install eagle-cli

You might need to use ``pip3`` instead if you run Python 2 next to Python 3.

Requirements
------------
* Python 3.6+

Parameters (how to use it)
--------------------------
Tasks
~~~~~
**-a, --add**

Adds a task (can be used multiple times).

 1. place takes the task name.
 2. place takes date/frequency [optional].
 3. place takes group [optional].

Examples:

::

    ~ eagle -a "make yo bed"  # Adds a todo
    ~ eagle -a "make yo bed" today  # Adds a todo task for today
    ~ eagle -a "make yo bed" tomorrow  # Adds a todo task for tomorrow
    ~ eagle -a "make yo bed" 1d  # Adds todo for each day
    ~ eagle -a "make yo sis bed" @20/1/2050  # Adds todo on 20th January 2050
    ~ eagle -a "make yo sis bed" @20/1  # Adds todo on 20th January this year
    ~ eagle -a "make yo sis bed" +5  # Adds todo on 5th day from today
    ~ eagle -a "make yo dog bed ... someday" @20/1/2050 dog # Adds todo on 20th January 2050 to the "dog" group
    ~ eagle -a "make yo dog bed groupped" - dog # Adds todo to the "dog" group - notice the "-" as a date.

* subject ``whatever``
* frequency (optional)
   * no date/frequency/recurring: ``-``
   * recurring: ``1d``, ``1w``, ``1m``, ``1y``
   * on a specific date: ``@20/1/2050`` or just ``@20/1`` for current year
   * magical string representing a date
      * ``today``
      * ``tomorrow``
      * ``+X`` where ``X`` is number of days. For example ``+5`` means "in 5 days".
* group (optional) - if the group doesn't exist eagle creates it for you

If you wanna add a task with no date/frequency to a certain group
use ``-`` as date/frequency.

::

   eagle -a Task1 - group1

**-d, --del**

Deletes a task (can be used multiple times).

Example:

::

    ~ eagle -d 2
    ~ eagle

    Today:
        4. brush yo teeth

    Your list:

        1. do the laundry (every week)
        2. buy presents (on 24th December)
        3. brush yo teeth (every day)

- number of the record to be deleted

**-c, --clear**

Removes all tasks and groups.

Example:

::

    ~ eagle

    Today:
        4. brush yo teeth

    Your list:

        1. do the laundry (every week)
        2. buy presents (24/12/2019)
        3. brush yo teeth (every day)

    ~ eagle -c
    Todo list has been cleared out.


**-t, --today**

Lists only today's tasks.

Example:

::

    ~ eagle -t

    Today:
        4. brush yo teeth

Groups
~~~~~~
**-A, --add-group**

Adds a group (can be used multiple times).

Example:

::

    ~ eagle -A "School"

**-D, --delete-group**

Deletes a group with all attached tasks (can be used multiple times).

Example:

::

    ~ eagle

    Your list:

        1. do the laundry (every week)
        2. do the homework [School]
        3. set up project [School]

    ~ eagle -D "School"

    Your list:

        1. do the laundry (every week)

**-S, --soft-delete-group**

Deletes a group without deleting attached tasks (can be used multiple times).

Example:

::

    ~ eagle

    Your list:

        1. do the laundry (every week)
        2. do the homework [School]
        3. set up project [School]

    ~ eagle -S "School"

    Your list:

        1. do the laundry (every week)
        2. do the homework
        3. set up project

**-g, --groups**

Lists tasks filtered by a group name (can be used multiple times).

Example:

::

   ~ eagle

   Your list:

        1. do the laundry (every week)
        2. do the homework [School]
        3. set up project [School]

    ~ eagle -g "School"

    Your list:

        2. do the homework [School]
        3. set up project [School]

Print options
~~~~~~~~~~~~~
**--sort=[groups]**

Tasks are sorted by date and time they were created. You can override this
option in this parameter.

* ``groups`` - sorts alphabetically tasks by groups. First goes the tasks
  without any group.

Why CLI?
--------
CLI is the best UI ever invented. It's fast, clean, bloat free and you dont have to
invest massive effort to make your software looks good. Also you don't have to rewrite
or modernize each year (see web apps).

Also you can easily parse the output and chain that into your window manager widget if you
want to (i.e. AwesomeWM).

Why GitLab?
-----------
It's hard to explain. It's one of those "once you switch you don't look back" things.
Try it yourself.

Isn't this just another copycat?
--------------------------------
There is a few project around which are pretty good. For example `TaskWarrior <https://taskwarrior.org/>`_
which is robust and covers pretty much everything. For me it's too heavy and fancy with all
the charts and tables. I want something more quiet and more straightforward.

Why you don't use mypy?
-----------------------
From mypy FAQ:

::

   Will static typing make my programs run faster?

   Mypy only does static type checking and it does not improve
   performance. It has a minimal performance impact. In the
   future, there could be other tools that can compile statically
   typed mypy code to C modules or to efficient JVM bytecode, for
   example, but this is outside the scope of the mypy project.

So static typing is just for a developer not for a machine. Once it will also help
a machine to run Python code faster (Cython principle) I will definitely start using
that.


Can I contribute?
-----------------
Absolutely! I would be more than happy to accept any bug-report, improvement, pull request,
constructive criticism, etc.
