Tutorial
========

Install
-------

You need Python 3 to use ``climactic``. See the instructions
for your platform at http://python.org. It is a good idea to
update your pip::

    pip3 install -U setuptools pip

It is recommended that you also run climactic in a virtual
environment (optional)::

    python3 -m venv climactic_venv
    source climactic_venv/bin/activate

Now install ``climactic``::

    pip install climactic


Write Some Tests
----------------

Create a file called test_hello.yml with the following
contents::

    ---
    # A very simple test!

    - !run >
        echo Hello world!

    - !assert-output >
        Hello world!

Now let's go through each part. The first line identifies
the beginning of a YAML document::

    ---

Lines that start with # are comments::

    # A very simple test!

A test consists of a list of commands. The dash means a list
item in YAML. First we're going to run the ``echo`` command::

    - !run >
        echo Hello world!

.. note:: ``- !run`` and ``- run:`` both indicate a climactic
          command. e.g., this is equivalent::

              - run: >
                  echo Hello world!

          This works for any command. This behavior may evolve
          in future versions.

Then we will use an assert command to check that the output
of the echo was correct::

    - !assert-output >
        Hello world!

Run the Test Runner
-------------------

Save the file, and run climactic::

    (climactic)bjorgensen$ climactic
    .
    ----------------------------------------------------------------------
    Ran 1 tests in 0.035s

    OK

.. note:: If you also have ``py.test`` installed, ``climactic``
          provides a plugin::

                (climactic)bjorgensen$ py.test
                =========== test session starts ============
                platform darwin -- Python 3.4.2 -- py-1.4.28 -- pytest-2.7.1
                rootdir: /Users/brjorgensen/PycharmProjects/climactic, inifile: pytest.ini
                plugins: climactic
                collected 1 items

                ../examples/test_hello.yml .

                ========= 1 passed in 0.01 seconds =========

          Installing ``py.test`` is as easy as::

                (climactic)bjorgensen$ pip install pytest


Make a Test Fail
----------------

Create a file called test_hello2.yml with the following
contents::

    ---
    # A very simple test!

    - !run >
        echo Hello world!

    - !assert-output >
        Goodbye world!

Note that the assert-output specifies a different string
than the echo.
