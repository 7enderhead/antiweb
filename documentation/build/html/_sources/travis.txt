#########
Travis-CI
#########

******************
The Travis-CI file
******************

This file tells our external website for continuous integration, Travis-CI, how to perform the tests.

::

    # in which language the script was written
    language: python
    # on which operating systems the tests should be performed
    os:
      - linux
    # which Python releases to use
    python:
      - "3.4"
      - "3.5"
    # command to install dependencies and the script itself
    install: "python setup.py install"
    # command to run tests
    script: python -m unittest discover
