#!python

"""
Name: antiweb
Version: 0.3.3
Summary: antiweb literate programming tool
Home-page: http://packages.python.org/antiweb/
Author: Michael Reithinger, Philipp Rathmanner, Lukas Tanner, Philipp Grandits, Christian Eitner
Author-email: antiweb@freelists.org
License: GPL
"""

#@start()
"""
.. default-domain:: python

.. highlight:: python3
   :linenothreshold: 4

########
antiweb
########

If you just want to generate the documentation from a source file use
the following function:

@include(generate doc, antiweb_lib\write.py)


*******
Objects
*******

.. compound::

   The graph below show the main objects of antiweb:

   .. digraph:: collaboration

      document [shape=box, label="document"]
      reader   [shape=box, label="reader"]
      directives [shape=box, label="directive" ]
      blocks [shape=box]
      lines [shape=box]

      document -> reader [label="uses"]
      reader -> directives [label="creates"]
      document -> directives [label="uses"]
      document -> blocks [label="contains"]
      directives -> blocks [label="prepare"]
      blocks -> lines [label="contains"]
      lines -> directives [label="contains"]


   The :py:class:`document <Document>` manages the complete transformation: It uses a
   :py:class:`reader <Reader>`  to parse source code. The :py:class:`reader <Reader>`
   creates :py:class:`directives <Directives>` objects for each found antiweb directive in the source
   code. The source code is split in text blocks which consists of several
   :py:class:`lines <Line>`. The :py:class:`document <Document>` process all
   :py:class:`directives <Directives>`  to generate the output document.




***********
File Layout
***********

@include(file layout)

@include(imports)

@include(management)

@include(parsing doc)

****************************************
Multi-File Processing and Sphinx Support
****************************************

antiweb creates .rst files which can be further processed by documentation systems like Sphinx.
Additionally you can process multiple files at once with the -r option added.
The optional directory parameter then can be empty to use the current directory, or you provide the directory antiweb should use.

************************
How to add new languages
************************

New languages are added by writing a new Reader class
and registering it in the readers dictionary (see readers).
A simple Reader example is provides by :py:class:`CReader`
a more advanced reader is :py:class:`PythonReader`.

#@include(comments doc, antiweb_lib\document.py)
#@include(get_comment_markers doc, antiweb_lib\document.py)

*******
Example
*******

See the antiweb source as an advanced example.

@if(usage)
**********
Directives
**********

``@subst(_at_)start(text block name)``
======================================

@include(Start user)


``@subst(_rstart_)(text block name)``
=====================================

@include(RStart user)


``@subst(_cstart_)(text block name)``
======================================

@include(CStart user)


``@subst(_end_)[(text block name)]``
=====================================

@include(End user)


``@subst(_at_)code``
====================

@include(Code user)


``@subst(_at_)edoc``
====================

@include(Edoc user)

``@subst(_include_)(text block name[, file])``
==============================================

@include(Include user)



``@subst(_at_)RInclude(text block name)``
=========================================

@include(RInclude user)


``@subst(_indent_) spaces``
======================================

@include(Indent user)


``@subst(_define_)(identifier[, substitution])``
================================================

@include(Define user)


``@subst(_enifed_)(identifier)``
======================================

@include(Enifed user)


``@subst(_subst_)(identifier)``
======================================

@include(Subst user)



``@subst(_if_)(token name)``
======================================

@include(If user)


``@subst(_fi_)(token name)``
======================================

@include(Fi user)


``@subst(_at_)ignore``
======================================

@include(Ignore user)


@fi(usage)

"""
#@

#@start(file layout)
#@code

#@rstart(imports)

#<<imports>>
#===========
#@code
from optparse import OptionParser
import logging
import sys
import os.path
import os

from antiweb_lib.write import write
#@rstart(management)

#<<management>>
#==============

#@code

__version__ = "0.3.3"

logger = logging.getLogger('antiweb')

#@cstart(parsing)
def parsing():
#@start(parsing doc)
    """
.. py:method:: def parsing()

   All possible input options are being defined, as well as their help-message, type and variable the values are stored in.
   If no arguments are given (the user did not provide a filepath), the current directory is set as the argument.
    """
#@include(parsing)
#@(parsing doc)
    parser = OptionParser("usage: %prog [options] SOURCEFILE",
                          description="Tangles a source code file to a rst file.",
                          version="%prog " + __version__)

    parser.add_option("-o", "--output", dest="output", default="",
                      type="string", help="The output filename")

    parser.add_option("-t", "--token", dest="token", action="append",
                      type="string", help="defines a token, usable by @if directives")

    parser.add_option("-w", "--warnings", dest="warnings",
                      action="store_false", help="suppresses warnings")

    parser.add_option("-r", "--recursive", dest="recursive",
                      action="store_true", help="Process every file in given directory")

    options, args = parser.parse_args()

    #There is no argument given, so we assume the user wants to use the current directory.
    if not args:
        args.append(os.getcwd())
    # parsing() returns the selected options, arguments (the filepath/folderpath) and the parser
    return (options, args, parser)
#@(parsing)

def main():

    options, args, parser = parsing()

    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    if options.warnings is None:
        options.warnings = True

    if not args:
        parser.print_help()
        sys.exit(0)

#@edoc

#The program checks if a -r flag was given and if so, save the current directory and change it to the given one.

#@code

    previous_dir = os.getcwd()

    #The user input (respectively the input antiweb sets when none is given) can be relative,
    #so we grab the absolute path to work with.
    absolute_path = os.path.abspath(args[0])

    if options.recursive:
        directory = absolute_path

        #Check if the given path refers to an existing directory.
        #The program aborts if the directory does not exist or if the path refers to a file.
        #A file is not allowed here because the -r option requires a directory.
        if not os.path.isdir(directory):
            logger.error("directory not found: %s", directory)
            sys.exit(1)

        os.chdir(directory)

#@edoc

#The program walks through the given directory and all subdirectories. The absolute file names
#are retrieved. Only files with the allowed extensions are processed.

#@code

        #Only files with the following extensions will be processed
        ext_tuple = (".cs",".cpp",".py",".cc", ".rst")

        for root, dirs, files in os.walk(directory, topdown=False):
            for filename in files:
                fname = os.path.join(root, filename)

                if os.path.isfile(fname) and fname.endswith(ext_tuple):
                    write(directory, fname, options)

#@edoc

#This else will take place when the -r flag is not given.

#@code

    else:
        absolute_file_path = absolute_path

        #Check if the given path refers to an existing file.
        #The program aborts if the file does not exist or if the path refers to a directory.
        #A directory is not allowed here because a directory can only be used with the -r option.
        if not os.path.isfile(absolute_file_path):
            logger.error("file not found: %s", absolute_file_path)
            sys.exit(1)

        directory = os.path.split(absolute_file_path)[0]

        if directory:
            os.chdir(directory)

        write(os.getcwd(), absolute_file_path, options)

    os.chdir(previous_dir)
    return True
#@edoc

#@(file layout)

if __name__ == "__main__":
    main()

"""
@start(__macros__)
@define(__codeprefix__)

@ignore The code begins in file @subst(__file__) at line @subst(__line__-1):
@enifed(__codeprefix__)
@end(__macros__)

@define(_rstart_, @rstart)
@define(_cstart_, @cstart)
@define(_end_, @)
@define(_if_, @if)
@define(_fi_, @fi)
@define(_include_, @include)
@define(_indent_, @indent)
@define(_define_, @define)
@define(_enifed_, @enifed)
@define(_subst_, @subst)
@define(_at_, @)
@define(triple, ''')
"""
