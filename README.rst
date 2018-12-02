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
Don't worry about the early version number 0.x. I tend to Semantic Verioning more
than to "Marketing Versioning". That means version 0.5 is quite solid piece of
software instead or having version 25 and still not-even-half-way there.

So:

::

   pip install eagle-cli

You might need to use ``pip3`` instead if you run Python 2 next to Python 3.

Requirements
------------
* Python 3.6+

Parameters
----------
Tasks
~~~~~
**-a, --add**

Example:

::

    ~ eagle -a "make yo bed" 1day  # Adds todo for each day
    ~ eagle -a "make yo sis bed" @20/1/2050  # Adds todo on 20th January 2050
    ~ eagle -a "make yo dog bed" # Adds todo without specific deadline or recurring
    ~ eagle -a "make yo dog bed ... someday" @20/1/2050 dog # Adds todo on 20th January 2050 to the "dog" group
    ~ eagle -a "make yo dog bed groupped" - dog # Adds todo to the "dog" group - notice the "-" as a date.

* subject ``whatever``
* frequency (optional)
    * no frequency/recurring: ``-``
    * recurring: ``1d``, ``1w``, ``1m``, ``1y``
    * on a specific date: ``@20/1/2050``

**-d, --del**

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

Example:

::

    ~ eagle

    Today:
        4. brush yo teeth

    Your list:

        1. do the laundry (every week)
        2. buy presents (on 24th December)
        3. brush yo teeth (every day)

   ~ eagle -c
   Todo list has been cleared out.

Groups
~~~~~~
**-A, --add-group**

Example:

::

    ~ eagle -A "School"

**-D, --delete-group**

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

Can I contribute?
-----------------
Absolutely! I would be more than happy to accept any bug-report, improvement, pull request,
constructive criticism, etc.
