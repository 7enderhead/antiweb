.. default-domain:: python

.. highlight:: python
   :linenothreshold: 6


#####
Usage
#####


.. code-block:: none

   > python antiweb.py [options] SOURCEFILE

Tangles a source code file to a rst file.

**Options**

  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o OUTPUT, --output=OUTPUT
                        The output file name
  -t TOKEN, --token=TOKEN
                        defines a token, usable by @if directives
  -w, --warnings        suppresses warnings


*******
Example
*******

See the :ref:`antiweb` source as an advanced example.


**********
Directives
**********

``@start(text block name)``
======================================

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


``@rstart(text block name)``
=====================================

   The ``@rstart`` directive works like the ``@start``
   directive. While ``@start`` removes it's block completely
   from the containing block. ``@rstart`` replaces the lines
   with a ``<<name>>`` - Sentinel.


``@cstart(text block name)``
======================================

   The ``@cstart(name)`` directive is a replacement for

   ::

      @rstart(name)
      @code


``@[(text block name)]``
=====================================

   The end (``@``) directive ends a text block.


``@code``
====================

   The ``@code`` directive starts a code block. All
   lines following ``@code`` will be displayed as source code.

   A ``@code`` directive ends,
     * if the text block ends
     * if an ``@edoc`` occurs.

   The content of the special macro ``__codeprefix__`` is inserted
   before each code block. ``__codeprefix__`` is empty by default
   and can be defined by a ``@define`` directive.
  


``@edoc``
====================

   The ``@edoc`` directive ends a previously started ``@code`` directive

``@include(text block name[, file])``
==============================================

   The ``@include`` directive inserts the contents of the 
   text block with the same name. The lines have the same
   indentation as the ``@include`` directive.

   The directive can have a second *file* argument. If given
   the directive inserts the text block of the specified file.



``@RInclude(text block name)``
=========================================

   The ``@rinclude(text block name)`` directive is a is a replacement for::

      .. _text block name:

      **<<text block name>>**

      @include(text block name)



``@indent spaces``
======================================

   The ``@indent`` directive changes the indentation of the
   following lines. For example a  call ``@indent -4``
   dedents the following lines by 4 spaces.


``@define(identifier[, substitution])``
================================================

   The ``@define`` directive defines a macro, that can be used
   with a ``@subst`` directive. If a ``substitution``
   argument is given, the macro defines an inline substitution.
   Otherwise the ``@define`` has to be ended by an ``@enifed``
   directive.


``@enifed(identifier)``
======================================

   The ``@enifed`` directive ends a macro defined by the
   ``@define`` directive.


``@subst(identifier)``
======================================

   The ``@subst`` directive is replaced by the substitution,
   defined by a ``@define`` directive. There are two predefined
   macros:

    ``__line__``
         Define the current line within the source code. The
         ``@subst`` can also handle operation with ``__line__``
         like ``__line__ + 2``.

    ``__file__``
        Defines the current source file name.



``@if(token name)``
======================================

   The ``@if`` directive is used for conditional weaving.
   The content of an ``@if``, ``@fi`` block is waved if the
   named token argument of ``@if``, is defined in the command line
   by the ``--token`` option.


``@fi(token name)``
======================================

   The ``@fi`` ends an ``@if`` directive


``@ignore``
======================================

   The ``@ignore`` directive ignores the line in the
   documentation output. It can be used for commentaries.
  


