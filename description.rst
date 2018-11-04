Eagle
=====

.. image:: https://gitlab.com/n1_/eagle/raw/master/logo.png

Eagle is a simple CLI todo tool. It's so simple it hurts my coding skills.

How does it work?
-----------------

.. code-block:: text

   ~ eagle

   Today:
       4. brush yo teeth

   Your list:

      1. do the laundry (every week)
      2. buy some food (each other day)
      3. buy presents (on 24th December)

How can I install it?
---------------------
Don't worry about the early version number 0.x. I tend to Semantic Verioning more
than to "Marketing Versioning". That means version 0.5 is quite solid piece of
software instead or having version 25 and still not-even-half-way there.

So:

.. code-block:: text

   pip install eagle-todo

You might need to use ``pip3`` instead if you run Python 2 next to Python 3.

Requirements
------------
* Python 3.6+

Parameters
----------
**-a, --add**

Example:

.. code-block:: shell

   ~ eagle -a "make yo bed" 1day  # Adds todo for each day
   ~ eagle -a "make yo sis bed" @20/1/2050  # Adds todo on 20th January 2050
   ~ eagle -a "make yo dog bed" - # Adds todo without specific deadline or recurring

* subject `whatever`
* frequency
    * no frequency/recurring - `-`
    * recurring - `1d`, `1w`, `1m`, `1y`
    * on a specific date - `@20/1` or `@20/1/2050`
* whom `bro`

**-d, --del**

Example:

.. code-block:: text

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

.. code-block::

   ~ eagle

   Today:
      4. brush yo teeth

   Your list:

      1. do the laundry (every week)
      2. buy presents (on 24th December)
      3. brush yo teeth (every day)

   ~ eagle -c
   Todo list has been cleared out.
