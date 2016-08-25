.. default-domain:: python

.. highlight:: python
   :linenothreshold: 6



###############
Getting Started
###############

   .. code-block:: none

      > python antiweb.py [options] SOURCEFILE

   Tangles a source code file to a rst file.

   Options

   ::

     --version                       show programs version number and exit
     -h, --help                      show this help message and exit
     -o OUTPUT, --output=OUTPUT      The output file/folder name
     -t TOKEN, --token=TOKEN         defines a token, usable by @if directives
     -w, --warnings                  suppresses warnings
     -r, --recursive                 Process every file in the given directory

   IMPORTANT: When combining certain flags, their behaviour may change.
   When combining the ``-o`` with the ``-r`` flag, ``-o`` defines the output folder, not the output file.

   Every @ directive in antiweb has to be a comment in order to be accepted by antiweb. However, antiweb will still recognize but not accept directives which aren't comments.


@start
=======

      The ``@start`` directive defines the beginning of
      a text block. It is called with an argument defining
      the name of the text block. There are two special text
      blocks:

         * ``()`` The empty one defining the main text block
         * ``(__macro__)`` defining a text block for implementing macros.

      There are several possibilities to end a text block.

         1) The end of the file

         2) A line with a smaller indentation as the ``@start`` directive.

         3) Another start directive with same indentation.

         4) An unnamed end (``@``) directive with the same indentation as
            the ``@start`` directive.

         5) A named end directive closing this block or an outer block.


      Text blocks defined by ``@start`` can be nested.

@rstart(text block name)
========================
   The ``@rstart`` directive works like the ``@start`` directive. While ``@start`` removes its block completely from the containing block,
   ``@rstart`` replaces the lines with a ``<<name>>`` - Sentinel.


@cstart(text block name)
========================

   The ``@cstart`` directive can be used as a shortcut for:


   ::

       @start(block)
       @code

@[(text block name)]
====================

   The end(``@``) directive ends a text block. Optional a specific text block can also be closed by defining its ``text block name``.

@include(text block name [, file])
==================================

   Once you have created a block  you can include it with the ``@include`` directive. The order in which your blocks will appear in the documentation is defined by the order of the ``@include`` directives


   ::


       @include(Blockname)

   The directive can have a second file argument. If given, the directive inserts the text block of the specified file.

@RInclude(text block name)
==========================

   The ``@rinclude(text block name)`` directive is a is a replacement for::

      .. _text block name:

      **<<text block name>>**

      @include(text block name)



@code
======

   Of course you want parts of your source code in a Block in order to e.g. describe the function of it. You can do that by following this example. The code in between the directives will be normally recognized as code but also included in the documentation:


   ::


       @code
       #End of comment section

       Put your code here

       #Beginning of next comment section
       @edoc

@edoc
=====

   The ``@edoc`` directive ends a previously started ``@code`` directive


Titles
======

   There are also different types of titles with different indentation in the index. antiweb wants the indication marks, e.g. #### to
   be exactly as long as the title. Creating a headline below a higher level headline makes it a sub-headline of the higher one, also
   shown in the index table

   ::



       #####
       Title #This is the top level headline
       #####

       *****
       Title #This is the mid level headline
       *****

       Title #This is the low level headline
       =====


@indent spaces
===============
   You can indicate antiweb to make a manual indentation with the ``@indent spaces`` directive, replacing ``spaces`` by three would indent the text by three spaces


@define(identifier[, substitution])
===================================

   The ``@define`` directive defines a macro, that can be used
   with a ``@subst`` directive. If a ``substitution``
   argument is given, the macro defines an inline substitution.
   Otherwise the ``@define`` has to be ended by an ``@enifed``
   directive.


@enifed(identifier)
===================

   The ``@enifed`` directive ends a macro defined by the
   ``@define`` directive.


@subst(identifier)
==================

   The ``@subst`` directive is replaced by the substitution,
   defined by a ``@define`` directive. There are two predefined
   macros:

    ``__line__``
         Define the current line within the source code. The
         ``@subst`` can also handle operation with ``__line__``
         like ``__line__ + 2``.

    ``__file__``
        Defines the current source file name.



@if(token name)
===============

   The ``@if`` directive is used for conditional weaving.
   The content of an ``@if``, ``@fi`` block is waved if the
   named token argument of ``@if``, is defined in the command line
   by the ``--token`` option.


@fi(token name)
===============

   The ``@fi`` ends an ``@if`` directive


@ignore
=======

   The ``@ignore`` directive ignores the line in the
   documentation output. It can be used for commentaries.

Indentation matters
===================

   In sphinx and antiweb, the indentation matters. To effectively nest blocks, create sub headlines and more you have to keep the indentation in mind. To nest a block or headline you have to indent it farther than its parent. In addition, your documentation looks much cleaner when structured like this.
