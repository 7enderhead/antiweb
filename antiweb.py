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

######################
Antiweb documentation
######################

If you just want to generate the documentation from a source file use 
the following function:

@include(generate doc)


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
   creates :ref:`directives <Directives>` objects for each found antiweb directive in the source
   code. The source code is split in text blocks which consists of several
   :py:class:`lines <Line>`. The :py:class:`document <Document>` process all
   :ref:`directives <Directives>`  to generate the output document.
   

.. _Directives:

**********
Directives
**********

@include(directive doc)
@include(NameDirective doc)
@include(Start doc)
@include(RStart doc)
@include(CStart doc)
@include(End doc)
@include(Include doc)
@include(RInclude doc)
@include(Code doc)
@include(Edoc doc)
@include(If doc)
@include(Fi doc)
@include(Ignore doc)
@include(Define doc)
@include(Enifed doc)
@include(Subst doc)
@include(Indent doc)


*******
Readers
*******

Readers are responsible for the language dependent
source parsing.

@include(Reader doc)
@include(CReader doc)
@include(CSharpReader doc)
@include(PythonReader doc)
@include(ClojureReader doc)
@include(GenericReader doc)
@include(rstReader doc)


********
Document
********

@include(Document doc)
@include(Line doc)


***********
File Layout
***********

@include(file layout)

@include(imports)

@include(management)

@include(directives)

@include(readers)

@include(document)


****************************************
Multi-File Processing and Sphinx Support
****************************************

antiweb supports Sphinx, which means that antiweb can provide you with an index.rst document that includes all processed files.
To use that feature you simple have to use the -i option. Additionally you can process multiple files at once with the -r option added. 
The needed parameter then can be empty to use the current directory or you provide the directory antiweb should use.

************************
How to add new languages
************************

New languages are added by writing a new Reader class
and registering it in the readers dictionary (see readers).
A simple Reader example is provides by :py:class:`CReader`
a more advances reader is :py:class:`PythonReader`.

#@include(comments doc)
#@include(get_comment_markers doc)


#####
Usage
#####


.. code-block:: none

   #> python antiweb.py [options] SOURCEFILE

Tangles a source code file to a rst file.

**Options**

  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o OUTPUT, --output=OUTPUT
                        The output file name
  -t TOKEN, --token=TOKEN
                        defines a token, usable by @if directives
  -w, --warnings        suppresses warnings
  -r, --recursive       Process every file in given directory
  -i, --index           Automatically write file(s) to Sphinx' index.rst

*******
Example
*******

See the :ref:`antiweb` source as an advanced example.


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
import pygments.lexers as pm
from pygments.token import Token
import bisect
import re
import logging
import sys
import os.path
import operator
import os
from sys import platform as _platform
from bs4 import BeautifulSoup,  Tag,  NavigableString

#@rstart(management)

#<<management>>
#==============

#@code

__version__ = "0.3.2"

logger = logging.getLogger('antiweb')

class WebError(Exception):
    def __init__(self, error_list):
        self.error_list = error_list

#@rstart(directives)

#<<directives>>
#==============

#@code

#@cstart(Directive)
class Directive(object):
    #@start(directive doc)
    """
    Directive
    =========
    """
    """
    .. py:class:: Directive(line[, mo])

       The base class of all directives. 
       Directives can be distinguished by the different tasks,
       they handle, these Task are generally:

         * identifying a text block (:py:meth:`collect_block`)
         
         * inserting text in the output (:py:meth:`process`)

         * modifying text in the output (:py:meth:`process`)

         * deleting text in the output (:py:meth:`process`)
              
       :param line: the line number the directive was found
       :param mo: a match object of an regular expression
    """
    #@indent 3
    #@include(Directive)
    #@include(Directive.expression doc)
    #@include(Directive.priority doc)
    #@include(Directive.line doc)
    #@include(Directive.__init__ doc)
    #@include(Directive.collect_block doc)
    #@include(Directive.process doc)
    #@include(Directive.match doc)
    #@include(Directive.__repr__ doc)
    #@
    #Attributes
    #@cstart(Directive.expression)
    expression = ""
    """
    .. py:attribute:: expression
    
       A regular expression defining the directive.
    """
    #@cstart(Directive.priority)
    priority = 10
    """
    .. py:attribute:: priority

       An integer process priority. Directives with a lower priority
       will be processed earlier.
    """
    #@cstart(Directive.line)
    line = None
    """
    .. py:attribute:: line

       A integer defining the original line number of the directive.
    """
    #@

    #Methods
    #@cstart(Directive.__init__)
    def __init__(self, line, mo=None):
        """
        .. py:method:: __init__(line[, mo])

           The constructor
        """
        self.line = line
        

    #@cstart(Directive.collect_block)
    def collect_block(self, document, index):
        """
        .. py:method:: collect_block(document, index)

           This method is called by :py:class:`Document`.
           If the directive is defining a text block. It
           retrieves the text lines of the block from the document
           and return them.
           
           :param document: the document calling the function.
           :type document: :py:class:`Document`
           :param integer index: the line index of the directive.

           :return: If the directive collects a block the return value
                    is a tuple ``(directive name, block of lines)``, or
                    ``None`` otherwise.
        """
        return None


    #@cstart(Directive.process)
    def process(self, document, block, index):
        """
        .. py:method:: process(document, block, index)

           This method is called by :py:class:`Document`.
           The directive should do whatever it is supposed to do.
                           
           :param document: the document calling the function.
           :type document: :py:class:`Document`
           :param block: The line block the directive is in.
           :param integer index: the line index of the directive
                                 within the block.
        """
        pass
    

    #@cstart(Directive.match)
    def match(self, lines):
        """
        .. py:method:: match(lines)
        
           This method is called by :py:class:`Document`.
           It gives the directive the chance to find and manipulate other
           directives.

           :param list lines: a list of all document lines.
        """
        pass


    #@cstart(Directive.__repr__)
    def __repr__(self):
        """
        .. py:method:: __repr__()

           returns a textual representation of the directive.
        """
        return "<%s at %i>" % (self.__class__.__name__, self.line)

    #@(Directive.__repr__)

#@cstart(NameDirective)
class NameDirective(Directive):
    #@start(NameDirective doc)
    #NameDirective
    #=============
    """
    .. py:class:: NameDirective(line, mo)

       The base class for directives with a name argument.
       It inherits :py:class:`Directive`.
       
       :param line: the line number the directive was found
       :param mo: a match object of an regular expression or
                  a string defining the name. 

       .. py:attribute:: name

          A string defining the argument of the directive.
    """
    #@indent 3
    #@include(NameDirective)
    #@
    def __init__(self, line, mo):
        super(NameDirective, self).__init__(line, mo)
        if isinstance(mo, str):
            self.name = mo
        else:
            self.name = mo.group(1)


    def __repr__(self):
        return "<%s(%s) %i>" % (self.__class__.__name__,
                                self.name, self.line)

    
#@cstart(Start)
class Start(NameDirective):
    #@start(Start doc)
    #Start
    #=====
    """
    .. py:class:: Start

       This class represents a ``@start`` directive. It inherits
       :py:class:`NameDirective`.
       
    """
    #@start(Start user)
    """
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
    """
    #@
    #@include(Start user)
    #@indent 3
    #@include(Start)
    #@include(Start.has_named_end doc)
    #@rinclude(Start.inherited attributes)
    #@include(Start.collect_block doc)
    #@include(Start.process doc) 
    #@include(Start._find_matching_end doc)
    #@(Start doc)
    #Attributes
    #@cstart(Start.has_named_end)
    has_named_end = False
    """
    .. py:attribute:: has_named_end
    
       A boolean value, signalizing if the directive is
       ended by a named end directive.
    """
    #@cstart(Start.inherited attributes)
    expression = re.compile(r"@start\((.*)\)")
    priority = 5
    #@
    
    #Methods
    #@cstart(Start._find_matching_end)
    def _find_matching_end(self, block):
        """
        .. py:method:: _find_matching_end(block)

           Finds the matching end for the text block.

           :param list block: A list of lines beginning with start
           :return: The line index of the found end.
        """
        if self.has_named_end:
            # ignore all other ending conditions and directly
            # find the matching end directive
            for j, l in enumerate(block[1:]):
                j += 1
                d = l.directive
                if isinstance(d, End) and d.name == self.name:
                    return j

        start_indent = block[0].indent
        for j, l in enumerate(block[1:]):
            j += 1

            lindent = l.indent
            d = l.directive

            if isinstance(d, End):
                if d.name is None and lindent == start_indent:
                    #case 4: An unnamed @ directive with the same indentation
                    #        as the @start directive.
                    return j

                if d.start_line <= self.line:
                    #case 5: A named @ directive closing this block
                    #        or an outer block.
                    return j

            if isinstance(d, Start) and lindent == start_indent:
                #case 3: Another @start directive with same indentation.
                return j

            if lindent < start_indent and l:
                #case 2: A line with a smaller indentation as the @start directive.
                #        (an empty line doesn't count)
                return j

        #case 1: The end of the file
        return len(block)

    #@cstart(Start.collect_block)
    def collect_block(self, document, index):
        """
        .. py:method:: collect_block(document, index)

           See :py:meth:`Directive.collect_block`.
           The returned lines are unindented to column 0.
        """
        end = self._find_matching_end(document.lines[index:])
        block = document.lines[index+1:index+end]
        
        reduce_block = list(filter(bool, block))
        if not reduce_block:
            document.add_error(self.line, "Empty '%s' block" % self.name)
            return None

        #unindent the block, empty lines may not count (filter(bool, block))
        indent_getter = operator.attrgetter("indent")
        min_indent = min(list(map(indent_getter, reduce_block)))
        block = [ l.clone().change_indent(-min_indent) for l in block ]
        return self.name, block


    #@cstart(Start.process)
    def process(self, document, block, index):
        """
        .. py:method:: process(document, block, index)

           See :py:meth:`Directive.process`.
           Removes all lines of the text block from
           the containing block.
        """
        end = self._find_matching_end(block[index:])
        del block[index:index+end]
    #@
    
#@cstart(RStart)
class RStart(Start):
    #@start(RStart doc)
    #RStart
    #======
    """
    .. py:class:: RStart

       This class represents a ``@rstart`` directive. It inherits
       :py:class:`Start`.
       
    """
    #@start(RStart user)
    """
       The ``@subst(_rstart_)`` directive works like the ``@subst(_at_)start``
       directive. While ``@start`` removes it's block completely
       from the containing block. ``@rstart`` replaces the lines
       with a ``<<name>>`` - Sentinel.
    """
    #@
    #@include(RStart user)
    #@indent 3
    #@include(RStart)
    #@(RStart doc)
    expression = re.compile(r"@rstart\((.*)\)")

    def process(self, document, block, index):
        end = self._find_matching_end(block[index:])
        line = block[index]
        block[index:index+end] = [ line.like("<<%s>>" % self.name) ]
        

#@cstart(CStart)
class CStart(RStart):
    #@start(CStart doc)
    #CStart
    #======
    """
    .. py:class:: CStart

       This class represents a ``@rstart`` directive. It inherits
       :py:class:`RStart`.
       
    """
    #@start(CStart user)
    """
       The ``@subst(_at_)cstart(name)`` directive is a replacement for

       ::

          @subst(_rstart_)(name)
          @subst(_at_)code
    """
    #@
    #@include(CStart user)
    #@indent 3
    #@include(CStart)
    #@(CStart doc)
    expression = re.compile(r"@cstart\((.*)\)")

    def collect_block(self, document, index):
        name_block = super(CStart, self).collect_block(document, index)

        if not name_block: return None

        name, block = name_block

        first = block[0]
        sd = [ Code(first.index) ]
        block.insert(0, first.like("@code").set(directives=sd, 
                                                index=first.index-1))
        
        return name, block

#@cstart(End)
class End(NameDirective):
    #@start(End doc)
    #End
    #===
    """
    .. py:class:: End

       This class represents an end directive. It inherits
       :py:class:`NameDirective`.
       
    """
    #@start(End user)
    """
       The end (``@``) directive ends a text block.
    """
    #@
    #@include(End user)
    #@indent 3
    #@include(End)
    #@(End doc)
    expression = re.compile(r"@(\((.*)\))?\s*$", re.M)

    def __init__(self, line, mo):
        super(NameDirective, self).__init__(line, mo)
        self.start_line = self.line
        
        if isinstance(mo, str):
            self.name = mo
        else:
            self.name = mo.group(2)

        
    def match(self, lines):
        if self.name is None: return

        #find the matching start and inform it for the named end
        for l in reversed(lines[:self.line]):
            for d in l.directives:
                if isinstance(d, Start) and d.name == self.name:
                    d.has_named_end = True
                    self.start_line = d.line
                    return


    def process(self, document, block, index):
        #completely remove the directive from the containing block
        del block[index]


#@cstart(Fi)   
class Fi(NameDirective):
    #@start(Fi doc)
    #Fi
    #===
    """
    .. py:class:: Fi

       This class represents a `@fi` directive. It inherits
       :py:class:`NameDirective`.
       
    """
    #@start(Fi user)
    """
       The ``@fi`` ends an ``@if`` directive
    """
    #@
    #@include(Fi user)
    #@indent 3
    #@include(Fi)
    #@(Fi doc)
    expression = re.compile(r"@fi\((.+)\)")

    def process(self, document, block, index):
        del block[index]


#@cstart(If)
class If(NameDirective):
    #@start(If doc)
    #If
    #===
    """
    .. py:class:: If

       This class represents an ``@if`` directive. It inherits
       :py:class:`NameDirective`.
       
    """
    #@start(If user)
    """
       The ``@if`` directive is used for conditional weaving.
       The content of an ``@if``, ``@fi`` block is waved if the
       named token argument of ``@if``, is defined in the command line
       by the ``--token`` option.
    """
    #@
    #@include(If user)
    #@indent 3
    #@include(If)
    #@(If doc)
    expression = re.compile(r"@if\((.+)\)")
    priority = 4

    def process(self, document, block, index):
        for j in range(index+1, len(block)):
            d = block[j].directive
            if isinstance(d, Fi) and d.name == self.name:
                break

        else:
            document.add_error(self.line, "No fi for if %s" % self.name)
            return

        if self.name in document.tokens:
            del block[index]

        else:
            del block[index:j]
    
#@cstart(Define)
class Define(NameDirective):
    #@start(Define doc)
    #Define
    #======
    """
    .. py:class:: Define

       This class represents an ``@define`` directive. It inherits
       :py:class:`NameDirective`.
       
    """
    #@start(Define user)
    """
       The ``@define`` directive defines a macro, that can be used
       with a ``@subst(_at_)subst`` directive. If a ``substitution``
       argument is given, the macro defines an inline substitution.
       Otherwise the ``@define`` has to be ended by an ``@enifed``
       directive.
    """
    #@
    #@include(Define user)
    #@indent 3
    #@include(Define)
    #@(Define doc)

    expression = re.compile(r"@define\((.+)\)")
    priority = 1

    def process(self, document, block, index):
        args = self.name.split(",")
        name = args.pop(0).strip()

        if args:
            #more than one argument ==> an inline substitution
            document.macros[name] = args[0].strip()
            return

        #search for the matching @enifed
        for j in range(index+1, len(block)):
            d = block[j].directive
            if isinstance(d, Enifed) and d.name == name:
                break

        else:
            document.add_error(self.line, "No enifed for define %s" % name)
            return
        
        document.macros[name] = [ l.clone() for l in block[index+1:j] ]
            
#@cstart(Enifed)
class Enifed(NameDirective):
    #@start(Enifed doc)
    #Enifed
    #======
    """
    .. py:class:: Enifed

       This class represents an ``@enifed`` directive. It inherits
       :py:class:`NameDirective`.
       
    """
    #@start(Enifed user)
    """
       The ``@enifed`` directive ends a macro defined by the
       ``@define`` directive.
    """
    #@
    #@include(Enifed user)
    #@indent 3
    #@include(Enifed)
    #@(Enifed doc)

    expression = re.compile(r"@enifed\((.+)\)")

    def process(self, document, block, index):
        del block[index]
    
#@cstart(Subst)
class Subst(NameDirective):
    #@start(Subst doc)
    #Subst
    #=====
    """
    .. py:class:: Subst

       This class represents a ``@subst`` directive. It inherits
       :py:class:`NameDirective`.
       
    """
    #@start(Subst user)
    """
       The ``@subst`` directive is replaced by the substitution,
       defined by a ``@define`` directive. There are two predefined
       macros:

        ``__line__``
             Define the current line within the source code. The
             ``@subst`` can also handle operation with ``__line__``
             like ``__line__ + 2``.

        ``__file__``
            Defines the current source file name.
    """
    #@
    #@include(Subst user)
    #@indent 3
    #@include(Subst)
    #@(Subst doc)
    expression = re.compile(r"@subst\((.+?)\)")
    priority = 2

    def process(self, document, block, index):
        line = block[index]

        #find the substitution
        if self.name.startswith("__line__"):
            expression = self.name.replace("__line__", str(self.line+1))
            subst = str(eval(expression))

        elif self.name not in document.macros:
            document.add_error(self.line, "No macro %s found" % self.name)
            return
        
        else:
            subst = document.macros[self.name]

        if isinstance(subst, str):
            #inline substitution
            l = line.clone()
            l.text = line.text.replace("@subst(%s)" % self.name, subst)
            block[index] = l
        else:
            ln = line.index
            block[index:index+1] = [ l.clone(self.line+j)\
                                         .change_indent(line.indent)\
                                         .set(index=ln+j)
                                     for j, l in enumerate(subst) ]

        
#@cstart(Include)
class Include(NameDirective):
    #@start(Include doc)
    #Include
    #=======
    """
    .. py:class:: Include

       This class represents an ``@include`` directive. It inherits
       :py:class:`NameDirective`.
       
    """
    #@start(Include user)
    """
       The ``@include`` directive inserts the contents of the 
       text block with the same name. The lines have the same
       indentation as the ``@include`` directive.

       The directive can have a second *file* argument. If given
       the directive inserts the text block of the specified file.
    """
    #@
    #@include(Include user)
    #@indent 3
    #@include(Include)
    #@(Include doc)
    expression = re.compile(r"@include\((.+)\)")


    def process(self, document, block, index):
        #check if the name contains 2 arguments
        args = self.name.split(",")
        name = args.pop(0).strip()

        document.blocks_included.add(name)

        if args:
            #a file name is given, fetch block from that file
            fname = args[0].strip()
            subdoc = document.get_subdoc(fname)
            if subdoc:
                include = subdoc.get_compiled_block(name)
            else:
                include = None
        else:
            include = document.get_compiled_block(name)
            
        if not include:
            #print "error include", self.line, name
            document.add_error(self.line,
                               "Cannot find text block: %s" % name)
            return

        #replace the directive with its content
        indent = block[index].indent
        include = [ l.clone().change_indent(indent) for l in include ]
        block[index:index+1] = include



#@cstart(RInclude)
class RInclude(Include):
    #@start(RInclude doc)
    #RInclude
    #========
    """
    .. py:class:: RInclude

       This class represents an ``@rinclude`` directive. It inherits
       :py:class:`Include`.
       
    """
    #@start(RInclude user)
    """
       The ``@subst(_at_)rinclude(text block name)`` directive is a is a replacement for::

          .. _text block name:

          **<<text block name>>**

          @subst(_at_)include(text block name)

    """
    #@
    #@include(RInclude user)
    #@indent 3
    #@include(RInclude)
    #@(RInclude doc)
    expression = re.compile(r"@rinclude\((.+)\)")

    def process(self, document, block, index):
        l = block[index]
        super(RInclude, self).process(document, block, index)

        block[index:index] = [ l.like(""),
                               l.like(".. _%s:" % self.name),
                               l.like(""),
                               l.like("**<<%s>>**" % self.name),
                               l.like("") ]


#@cstart(Edoc)
class Edoc(Directive):
    #@start(Edoc doc)
    #Edoc
    #====
    """
    .. py:class:: Edoc

       This class represents an ``@subst(_at_)edoc`` directive. It inherits
       :py:class:`Directive`.
       
    """
    #@start(Edoc user)
    """
       The ``@subst(_at_)edoc`` directive ends a previously started ``@subst(_at_)code`` directive
    """
    #@
    #@include(Edoc user)
    #@indent 3
    #@include(Edoc)
    #@(Edoc doc)
    expression = re.compile(r"@edoc")

    def process(self, document, block, index):
        del block[index]
        
        
#@cstart(Code)
class Code(Directive):
    #@start(Code doc)
    #Code
    #====
    """
    .. py:class:: Code

       This class represents an ``@subst(_at_)code`` directive. It inherits
       :py:class:`Directive`.
       
    """
    #@start(Code user)
    """
       The ``@subst(_at_)code`` directive starts a code block. All
       lines following ``@subst(_at_)code`` will be displayed as source code.

       A ``@subst(_at_)code`` directive ends,
         * if the text block ends
         * if an ``@subst(_at_)edoc`` occurs.

       The content of the special macro ``__codeprefix__`` is inserted
       before each code block. ``__codeprefix__`` is empty by default
       and can be defined by a ``@subst(_at_)define`` directive.
      
    """
    #@
    #@include(Code user)
    #@indent 3
    #@include(Code)
    #@(Code doc)
    expression = re.compile(r"@code")

    def process(self, document, block, index):
        line = block[index]

        #change the indentation the code lines
        for j in range(index+1, len(block)):
            l = block[j]

            if isinstance(l.directive, Edoc):
                break

            block[j] = l.clone().change_indent(4).set(type='c')
            
        #insert the rst prefix
        sd = [Subst(self.line, "__codeprefix__")]
        new_block = [
            line.like("@subst(__codeprefix__)").set(directives=sd), 
            line.like("::"),
            line.like("")
            ]

        block[index:index+1] = new_block
        block.append(line.like(""))


#@cstart(Ignore)
class Ignore(Directive):
    #@start(Ignore doc)
    #Ignore
    #======
    """
    .. py:class:: Ignore

       This class represents an ``@subst(_at_)ignore`` directive. It inherits
       :py:class:`Directive`.
       
    """
    #@start(Ignore user)
    """
       The ``@subst(_at_)ignore`` directive ignores the line in the
       documentation output. It can be used for commentaries.
      
    """
    #@
    #@include(Ignore user)
    #@indent 3
    #@include(Ignore)
    #@(Ignore doc)
    expression = re.compile("@ignore")

    def process(self, document, block, index):
        del block[index]
    
#@cstart(Indent)
class Indent(Directive):
    #@start(Indent doc)
    #Indent
    #======
    """
    .. py:class:: Indent

       This class represents an ``@indent`` directive. It inherits
       :py:class:`Directive`.
       
    """
    #@start(Indent user)
    """
       The ``@indent`` directive changes the indentation of the
       following lines. For example a  call ``@subst(_at_)indent -4``
       dedents the following lines by 4 spaces.
    """
    #@
    #@include(Indent user)
    #@indent 3
    #@include(Indent)
    #@(Indent doc)
    expression = re.compile("@indent\s+([+-]?\d+)")

    def __init__(self, line, mo):
        super(Indent, self).__init__(line, mo)
        self.indent = int(mo.group(1))

        
    def process(self, document, block, index):
        lines = [ l.clone().change_indent(self.indent)
                  for l in block[index+1:] ]
        block[index:] = lines
        

#@(Indent)

directives = {
    "start" : Start,
    "rstart" : RStart,
    "cstart" : CStart,
    "edoc" : Edoc,
    "end" : End,
    "include" : Include,
    "code" : Code,
    "ignore" : Ignore,
    "indent" : Indent,
    "if" : If,
    "fi" : Fi,
    "define" : Define,
    "enifed" : Enifed,
    "subst" : Subst,
    "rinclude" : RInclude,
    }

#@(directives)
#@rstart(readers)
#.. _readers:
#

#<<readers>>
#===========

#@code

#@cstart(Reader)

re_line_start = re.compile("^", re.M) #to find the line start indices


class Reader(object):
    #@start(Reader doc)
    #Reader
    #=============
    """
    .. py:class:: Reader(lexer)

       This is the base class for all readers. The public functions
       exposed to :py:class:`Document` are :py:meth:`process`,
       and :py:meth:`filter_output`.

       The main tasks for a reader is:

         * Recognize lines that can contain directives. (comment lines or doc strings).
         * Modify the source for language specific optimizations.
         * Filter the processed output.
       
       :param lexer: A pygments lexer for the specified language
    """
    #@
    #@indent 3
    #@include(Reader)
    #@include(Reader.__init__ doc)
    #@include(Reader.process doc)
    #@include(Reader.filter_output doc)
    #@include(Reader._handle_token doc)
    #@include(Reader._cut_comment doc)
    #@include(Reader._post_process doc)
    #@include(Reader._accept_token doc)
    #@(Reader doc)
    #Public Methods
    #@cstart(Reader.__init__)
    def __init__(self, lexer, single_comment_markers, block_comment_markers):
        """
        .. py:method:: __init__(lexer, single_comment_markers, block_comment_markers)
            
           The constructor initialises the language specific pygments lexer and comment markers. 
           
           :param Lexer lexer: The language specific pygments lexer.
           :param string[] single_comment_markers: The language specific single comment markers.
           :param string[] block_comment_markers: The language specific block comment markers.
        """
        self.lexer = lexer
        self.single_comment_markers = single_comment_markers
        self.block_comment_markers = block_comment_markers

    #@cstart(Reader.process)
    def process(self, fname, text):
        """
        .. py:method:: process(fname, text)

           Reads the source code and identifies the directives.
           This method is call by :py:class:`Document`.

           :param string fname: The file name of the source code
           :param string text: The source code
           :return: A list of :py:class:`Line` objects.
        """
        text = text.replace("\t", " "*8)
        starts = [ mo.start() for mo in re_line_start.finditer(text) ]
        lines = [ Line(fname, i, l) for i, l in enumerate(text.splitlines()) ]

        self.lines = lines    # A list of lines
        self.starts = starts  # the start indices of the lines

        tokens = self.lexer.get_tokens_unprocessed(text)
        for index, token, value in tokens:
            self._handle_token(index, token, value)
        self._post_process(fname, text)
        return self.lines


    #@cstart(Reader.filter_output)
    def filter_output(self, lines):
        """
        .. py:method:: filter_output(lines)

           This method is call by :py:class:`Document` and gives
           the reader the chance to influence the final output.
        
        """
        return lines
        
    #@
    
    #Protected Methods
    #@cstart(Reader._accept_token)
    def _accept_token(self, token):
        """
        .. py:method:: _accept_token(token)

           Checks if the token type may contain a directive.

           :param token: A pygments token
           :return: ``True`` if the token may contain a directive.
                    ``False`` otherwise.
        """
        return True


    #@cstart(Reader._post_process)
    def _post_process(self, fname, text):
        """
        .. py:method:: _post_process(fname, text)

           Does some post processing after the directives where found.
        """

        #correct the line attribute of directives, in case there have
        #been lines inserted or deleted by subclasses of Reader
        for i, l in enumerate(self.lines):
            for d in l.directives:
                d.line = i

        #give the directives the chance to match
        for l in self.lines:
            for d in l.directives:
                d.match(self.lines)


    #@cstart(Reader._handle_token)
    def _handle_token(self, index, token, value):
        """
        .. py:method:: _handle_token(index, token, value)

           Find antiweb directives in valid pygments tokens.

           :param integer index: The index within the source code
           :param token: A pygments token.
           :param string value: The token value.
		"""
		
        if not self._accept_token(token): return
        cvalue = self._cut_comment(index, token, value)
        offset = value.index(cvalue)
        for k, v in list(directives.items()):
            for mo in v.expression.finditer(cvalue):
                li = bisect.bisect(self.starts, index+mo.start()+offset)-1
                line = self.lines[li]
                line.directives = list(line.directives) + [ v(line.index, mo) ]
         

    #@cstart(Reader._cut_comment)
    def _cut_comment(self, index, token, text):
        """
        .. py:method:: _cut_comment(index, token, value)

           Cuts of the comment identifiers.

           :param integer index: The index within the source code
           :param token: A pygments token.
           :param string value: The token value.
           :return: value without comment identifiers.
        """
        return text

#@cstart(CReader)

class CReader(Reader):
    #@start(CReader doc)
    
    #CReader
    #=============
    """
    .. py:class:: CReader

       A reader for C/C++ code. This class inherits :py:class:`Reader`.
    """
    #@indent 3
    #@include(CReader)
    #@(CReader doc)

    def __init__(self, lexer,  single_comment_markers,  block_comment_markers):
        super(CReader, self).__init__(lexer,  single_comment_markers,  block_comment_markers)
        #For C/C++ exists only one type of single and block comment markers.
        #The markers are retrieved here in order to avoid iterating over the markers every time they are used.
        self.single_comment_marker = single_comment_markers[0]
        self.block_comment_marker_start = block_comment_markers[0]   
        self.block_comment_marker_end = block_comment_markers[1]

    def _accept_token(self, token):
        return token in Token.Comment
    
    def _cut_comment(self, index, token, text):
        if text.startswith(self.block_comment_marker_start):
            text = text[2:-2]
    
        elif text.startswith(self.single_comment_marker):
            text = text[2:]

        return text
		
    def filter_output(self, lines):
        """
        .. py:method:: filter_output(lines)

           See :py:meth:`Reader.filter_output`.
        """
        print(lines)
        for l in lines:
            if l.type == "d":
                #remove comment chars in document lines
                stext = l.text.lstrip()

                if stext == self.block_comment_marker_start or stext == self.block_comment_marker_end:
                    #remove /* and */ from documentation lines
                    #see the l.text.lstrip()! if the lines ends with a white space
                    #the quotes will be kept! This is feature, to force the quotes
                    #in the output
                    continue
                
                if stext.startswith(self.single_comment_marker):
                    l.text = l.indented(stext[2:])
                            
            yield l
#@edoc

#@cstart(CSharpReader)


class CSharpReader(CReader):
    #@start(CSharpReader doc)
    #CSharpReader
    #=============
    """
    .. py:class:: CSharpReader

       A reader for C# code. This class inherits :py:class:`CReader`.
       The CSharpReader is needed because C# specific output filtering is applied.
       Compared to C, C# uses XML comments starting with *///* which are reused
       for the final documentation. Here you can see an overview of the CSharpReader class
       and its methods.
       
    """
    
    #@indent 3
    #@include(CSharpReader)
    #@include(CSharpReader.strip_tags doc)
    #@include(CSharpReader.get_attribute_text doc)
    #@include(CSharpReader.get_stripped_xml_lines doc)
    #@include(CSharpReader.create_new_lines doc)
    #@include(CSharpReader.init_xml_block doc)
    #@include(CSharpReader.filter_output doc)
    #@(CSharpReader doc)
    
    default_xml_block_index = -1
    
    def __init__(self, lexer,  single_comment_markers,  block_comment_markers):
        #the call to the base class CReader is needed for initialising the comment markers
        super(CSharpReader, self).__init__(lexer,  single_comment_markers,  block_comment_markers)
            
    #@cstart(CSharpReader.strip_tags)
    def strip_tags(self,  tags):
        """
        .. py:method:: strip_tags(tags)

           Removes all C# XML tags. The tags are replaced by their attributes and contents.
           This method is called recursively. This is needed if the content of a tag also contains
           tags.
           
           Examples:
           
            * ``<param name="arg1">value</param>`` will be stripped to : *"arg1 value"*
            * ``<para>Start <see cref="(String)"/> end</para>`` will be stripped to : *"Start (String) end"*

           :param Tag tags: The parsed xml tags.
           :return: the XML tags replaced by their attributes and contents.
        """
        
        if isinstance(tags,  Tag) and not tags.contents:            
            return self.get_attribute_text(tags)
    
        for tag in tags.find_all(True):
            text = self.get_attribute_text(tag)
            
            #if the content is a Navigablestring the content is simply concatenated 
            #otherwise the contents of the content are recursively checked for xml tags
            for content in tag.contents:
                if not isinstance(content, NavigableString):
                    content = self.strip_tags(content)
                text += content
    
            tag.replaceWith(text)
    
        return tags
    #@edoc
    
    #@cstart(CSharpReader.get_attribute_text)
    def get_attribute_text(self,  tag):
        """
        .. py:method:: get_attribute_text(tag)

           Returns the values of all XML tag attributes seperated by whitespace.

           Examples:
            
            * ``<param name="arg1">parameterValue</param>`` returns : *"arg1 "*
            * ``<include file='file1' path='[@name="test"]/*' />`` returns: *"file1 [@name="test"]/* "*

           :param Tag tag: A BeautifulSoup Tag.
           :return: the values of all attributes concatenated
        """
        #collect all values of xml tag attributes
        attributes = tag.attrs
        attribute_text = ""
        for attribute, value in attributes.items():
            attribute_text = value + " "
        return attribute_text
    #@edoc
    
    #@cstart(CSharpReader.get_stripped_xml_lines)
    def get_stripped_xml_lines(self,  xml_lines_block):
        """
        .. py:method:: get_stripped_xml_lines(xml_lines_block)
        
           Removes all XML comment tags from the lines in the xml_lines_block.
           
           :param Line[] xml_lines_block: A list containing all Line object which belong to an XML comment block.
           :return: A list of all stripped XML lines.
        """
        #the xml_lines_block contains Line objects. As the xml parser expects a string 
        #the Line obects have to be converted to a string.
        xml_text = "\n".join(map(operator.attrgetter("text"), xml_lines_block))
        
        #the xml lines will be parsed and then all xml tags will be removed       
        xml_tags = BeautifulSoup(xml_text, "html.parser")
        self.strip_tags(xml_tags)
        stripped_xml_lines = xml_tags.text.splitlines()
        return stripped_xml_lines
    #@edoc
    
    #@cstart(CSharpReader.create_new_lines)
    def create_new_lines(self, stripped_xml_lines, index, initial_line):
        """
        .. py:method:: create_new_lines(stripped_xml_lines, index, initial_line)
        
           This method is called after all XML comment tags are stripped. For each new 
           line in the stripped_xml_lines a new Line object is created.
           
           :param string[] stripped_xml_lines: The comment lines were the XML tags have been stripped.
           :param int index: The starting index for the new line object.
           :param Line initial_line: The first line of the xml comment block. Its indentation will be used for all new created lines.
           :return: A generator containing the lines which have been created out of the stripped_xml_lines.
        """
        for line in stripped_xml_lines:
            new_line = Line(initial_line.fname,  index,  initial_line.indented(line.lstrip()))
            index += 1
            yield new_line
    #@edoc
   
    #@cstart(CSharpReader.init_xml_block)
    def init_xml_block(self):
        """
        .. py:method:: init_xml_block()
        
           Inits the variables which are needed for collecting an XML comment block.
        """
        xml_lines_block = []
        xml_start_index = self.default_xml_block_index
        return xml_lines_block,  xml_start_index
    #@edoc
    
    #@cstart(CSharpReader.filter_output)
    def filter_output(self, lines):
        """
        .. py:method:: filter_output(lines)
        
           Applies C# specific filtering for the final output.
           XML comment tags are replaced by their attributes and contents.

           See :py:meth:`Reader.filter_output`
           
           We have to handle four cases:
            1. The current line is a code line: The line is added to result.
            2. The current line is a block comment: The line can be skipped.
            3. The current line is an XML comment: The line is added to the xml_lines_block.
            4. The current line is a single comment line: Add the line to result. If the current line is the first
               line after an xml comment block, the comment block is processed and its lines are added to result.
           
           :param Line[] lines: All lines of a file. The directives have already been replaced.
           :return: A generator containing all lines for the final output.
        """
        #first the CReader filters the output
        #afterwards the CSharpReader does some C# specific filtering
        lines = super(CSharpReader, self).filter_output(lines)
         
        #the xml_lines_block collects xml comment lines
        #if the end of an xml comment block is identified, the collected xml lines are processed
        xml_lines_block, xml_start_index  = self.init_xml_block()
        
        for l in lines:
            if l.type == "d":
                #remove comment chars in document lines
                stext = l.text.lstrip()
                   
                if stext == self.block_comment_marker_start or stext == self.block_comment_marker_end:
                    #remove /* and */ from documentation lines. see the l.text.lstrip()!
                    #if the lines ends with a white space the quotes will be kept! 
                    #This is feature, to force the quotes in the output
                    continue

                if stext.startswith("/") and not stext.startswith(self.block_comment_marker_start):
                    l.text = l.indented(stext[1:])
                    
                    if(xml_start_index == self.default_xml_block_index):
                        #indicates that a new xml_block has started
                        xml_start_index = l.index
                        
                    xml_lines_block.append(l)
                    continue 
                elif not xml_start_index == self.default_xml_block_index:
                    #an xml comment block has ended, now the block is processed
                    #at first the xml tags are stripped, afterwards a new line object is created for each 
                    #stripped line and added to the final result generator
                    stripped_xml_lines = self.get_stripped_xml_lines(xml_lines_block)
                    
                    new_lines = self.create_new_lines(stripped_xml_lines, xml_start_index, xml_lines_block[0])
                    for line in new_lines:
                        yield line
                    
                    #reset the xml variables for the next block
                    xml_lines_block, xml_start_index  = self.init_xml_block()

            yield l
    #@edoc

#@cstart(ClojureReader)
class ClojureReader(Reader):
    #@start(ClojureReader doc)
    #ClojureReader
    #=============
    """
    .. py:class:: ClojureReader

       A reader for Clojure code. This class inherits :py:class:`Reader`.
    """
    #@indent 3
    #@include(ClojureReader)
    #@(ClojureReader doc)
    def _accept_token(self, token):
        return token in Token.Comment
    
    def _cut_comment(self, index, token, text):
        if text.startswith(";"):
            text = text[1:]
        return text
		
    def filter_output(self, lines):
        """
        .. py:method:: filter_output(lines)

           See :py:meth:`Reader.filter_output`.
        """
        for l in lines:
            if l.type == "d":
                #remove comment chars in document lines
                stext = l.text.lstrip()
		
        if stext.startswith(";"):
                    #remove comments but not chapters
                    l.text = l.indented(stext[1:])

        yield l
    #@edoc
    #@(ClojureReader)

#@cstart(GenericReader)
class GenericReader(Reader):
    #@start(GenericReader doc)
    #GenericReader
    #=============
    """
    .. py:class:: GenericReader

       A generic reader for languages with single line and block comments . 
       This class inherits :py:class:`Reader`.
    """
    #@indent 3
    #@include(GenericReader)
    #@(GenericReader doc)
    def __init__(self, single_comment_markers, block_comment_markers):
        self.single_comment_markers = single_comment_markers
        self.block_comment_markers = block_comment_markers

    def _accept_token(self, token):
        return token in Token.Comment
    
    def _cut_comment(self, index, token, text):
        if text.startswith("/*"):
            text = text[2:-2]
    
        elif text.startswith("//"):
            text = text[2:]

        return text

    def filter_output(self, lines):

        for l in lines:
            if l.type == "d":
                #remove comment chars in document lines
                stext = l.text.lstrip()
                for block_start, block_end in self.block_comment_markers: #comment layout: [("/*", "*/"),("#","@")]
                    if stext == block_start or stext == block_end:
                        #remove """ and ''' from documentation lines
                        #see the l.text.lstrip()! if the lines ends with a white space
                        #the quotes will be kept! This is feature, to force the quotes
                        #in the output
                        continue
                    for comment_start in self.single_comment_markers: #comment layout: ["//",";"]
                        if stext.startswith(comment_start):
                            #remove comments but not chapters
                            l.text = l.indented(stext[2:])
                            
            yield l


#@cstart(rstReader)
class rstReader(Reader):
    #@start(rstReader doc)
    #rstReader
    #=============
    """
    .. py:class:: rstReader

       A reader for rst code. This class inherits :py:class:`Reader`.
    """
    #@indent 3
    #@include(rstReader)
    #@(rstReader doc)
    def _accept_token(self, token):
        return token in Token.Comment
    
    def _cut_comment(self, index, token, text):
        if text.startswith(".. "):
            text = text[3:]

        return text

    def filter_output(self, lines):
        """
        .. py:method:: filter_output(lines)

           See :py:meth:`Reader.filter_output`.
        """
        for l in lines:
            if l.type == "d":
                #remove comment chars in document lines
                stext = l.text.lstrip()
                if stext == '.. ':
                    #remove """ and ''' from documentation lines
                    #see the l.text.lstrip()! if the lines ends with a white space
                    #the quotes will be kept! This is feature, to force the quotes
                    #in the output
                    continue
                
                if stext.startswith(".. "):
                    #remove comments but not chapters
                    l.text = l.indented(stext[3:])
                            
            yield l

#@cstart(PythonReader)
class PythonReader(Reader):
    #@start(PythonReader doc)
    #PythonReader
    #============
    '''
    .. py:class:: PythonReader

       A reader for python code. This class inherits :py:class:`Reader`.
       To reduce the number of sentinels, the python reader does some more 
       sophisticated source parsing:
       
       A construction like::
         
             @subst(_at_)cstart(foo)
             def foo(arg1, arg2):
                """ 
                Foo's documentation
                """ 
                code


       is replaced by::

             @subst(_at_)cstart(foo)
             def foo(arg1, arg2):
                @subst(_at_)start(foo doc)
                """ 
                Foo's documentation
                """ 
                @subst(_at_)include(foo)
                @subst(_at_)(foo doc)
                code


       The replacement will be done only:

         * If the doc string begins with """
         * If the block was started by a ``@rstart`` or ``@cstart`` directive
         * If there is no antiweb directive in the doc string.
         * Only a ``@cstart`` will insert the @include directive.


       Additionally the python reader removes all single line ``"""`` and ``@subst(triple)``
       from documentation lines. In the following lines::
         
             @subst(_at_)start(foo)
             """ 
             Documentation
             """ 

       The ``"""`` are automatically removed in the rst output. (see :py:meth:`filter_output`
       for details).

    '''

    #@indent 3
    #@include(PythonReader)
    #@include(PythonReader._post_process doc)
    #@include(PythonReader._accept_token doc)
    #@include(PythonReader.filter_output doc)
    #@include(PythonReader._cut_comment doc)
    #@(PythonReader doc)
    def __init__(self, lexer,  single_comment_markers,  block_comment_markers):
        super(PythonReader, self).__init__(lexer,  single_comment_markers,  block_comment_markers)
        self.doc_lines = []
            
    #@cstart(PythonReader._post_process)
    def _post_process(self, fname, text):
        """
        .. py:method:: _post_process(fname, text)

           See :py:meth:`Reader._post_process`.

           This implementation *decorates* doc strings
           with antiweb directives.
        """
        #from behind because we will probably insert some lines
        self.doc_lines.sort(reverse=True)

        #handle each found doc string
        for start_line, end_line in self.doc_lines:
            indents = set()

            #@cstart(no antiweb directives in doc string)
            #If antiweb directives are within the doc string,
            #the doc string will not be decorated!
            directives_between_start_and_end_line = False
            for l in self.lines[start_line+1:end_line]:
                if l:
                    #needed for <<insert additional include>>
                    indents.add(l.indent)
                    
                if l.directives:
                    directives_between_start_and_end_line = True
                    break

            if directives_between_start_and_end_line: continue
            
            #@cstart(find the last directive before the doc string)
            last_directive = None
            for l in reversed(self.lines[:start_line]):
                if l.directives:
                    last_directive = l.directives[0]
                    break
            #@

            if isinstance(last_directive, RStart):
                #@cstart(decorate beginning and end)
                l = self.lines[start_line]
                start = Start(start_line, last_directive.name + " doc")
                l.directives = list(l.directives) + [start]

                l = self.lines[end_line]
                end = End(end_line, last_directive.name + " doc")
                l.directives = list(l.directives) + [end]
                #@
                
                if isinstance(last_directive, CStart):
                    #@cstart(insert additional include)
                    l = l.like("")
                    include = Include(end_line, last_directive.name)
                    l.directives = list(l.directives) + [include]
                    self.lines.insert(end_line, l)

                    #the include directive should have the same 
                    #indentation as the .. py:function:: directive 
                    #inside the doc string. (It should be second 
                    #value of sorted indents)
                    indents = list(sorted(indents))
                    if len(indents) > 1:
                        l.change_indent(indents[1]-l.indent)
                    #@

        super(PythonReader, self)._post_process(fname, text)

    #@edoc
    #@rinclude(no antiweb directives in doc string)
    #@rinclude(find the last directive before the doc string)
    #@rinclude(decorate beginning and end)
    #@rinclude(insert additional include)
        
    #@cstart(PythonReader._accept_token)
    def _accept_token(self, token):
        """
        .. py:method:: _accept_token(token)

           See :py:meth:`Reader._accept_token`.
        """
        return token in Token.Comment or token in Token.Literal.String.Doc


    #@cstart(PythonReader._cut_comment)
    def _cut_comment(self, index, token, text):
        """
        .. py:method:: _cut_comment(index, token, text)

           See :py:meth:`Reader._cut_comment`.
        """
        if token in Token.Literal.String.Doc:
            if text.startswith('"""'):
                #save the start/end line of doc strings beginning with """
                #for further decoration processing in _post_process,
                start_line = bisect.bisect(self.starts, index)-1
                end_line = bisect.bisect(self.starts, index+len(text)-3)-1
                lines = list(filter(bool, text[3:-3].splitlines())) #filter out empty strings
                if lines:
                    self.doc_lines.append((start_line, end_line))
                
            text = text[3:-3]

        return text

    #@cstart(PythonReader.filter_output)
    def filter_output(self, lines):
        """
        .. py:method:: filter_output(lines)

           See :py:meth:`Reader.filter_output`.
        """
        for l in lines:
            if l.type == "d":
                #remove comment chars in document lines
                stext = l.text.lstrip()

                if stext == '"""' or stext == "'''":
                    #remove """ and ''' from documentation lines
                    #see the l.text.lstrip()! if the lines ends with a white space
                    #the quotes will be kept! This is feature, to force the quotes
                    #in the output
                    continue
                
                if stext.startswith("#"):
                    #remove comments but not chapters
                    l.text = l.indented(stext[1:])
                            
            yield l

# The keys are the lexer names of pygments
readers = {
    "C" : CReader,
    "C++" : CReader,
    "C#" : CSharpReader,
    "Python" : PythonReader,
    "Clojure" : ClojureReader,
    "rst" : CReader,
}

#@(readers)

#@start(comments doc)
#Language specific comment markers
#====================================
'''
If a new language is added, its comment markers also have to be registered in the following map.
The map contains the definition of all language specific comment markers.

The comment markers of a language are defined in the format:
``"language" : ([single_comment_tokens],[start_block_token, end_block_token])``

Multiple single and block comment markers can be defined.
'''

#@code
comments = {
"C" : (["//"],(["/*","*/"])),
"C++" : (["//"],(["/*","*/"])),
"C#" : (["//"],(["/*","*/"])),
"Python" : (["#"],(["'''","'''"],["\"\"\"","\"\"\""])),
}
#@

#@cstart(Line)
class Line(object):
    #@start(Line doc)
    #Line
    #====
    """
    .. py:class:: Line(fname, index, text[, directives[, type]])

       This class represents a text line.
    """
    #@indent 3
    #@include(Line)
    #@include(Line._directives doc)
    #@include(Line.fname doc)
    #@include(Line.index doc)
    #@include(Line.text doc)
    #@include(Line.type doc)
    #@include(Line.indent doc)
    #@include(Line.sindent doc)
    #@include(Line.directives doc)
    #@include(Line.directive doc)
    #@include(Line.__init__ doc)
    #@include(Line.set doc)
    #@include(Line.like doc)
    #@include(Line.indented doc)
    #@include(Line.change_indent doc)
    #@include(Line.__len__ doc)
    #@include(Line.__repr__ doc)
    #@(Line doc)
    #Attributes
    #@cstart(Line._directives)
    _directives = ()
    """
    .. py:attribute:: _directives
    
       A list of :py:class:`Directive` objects, sorted
       by their priority.
    """
    #@cstart(Line.fname)
    fname = ""
    """
    .. py:attribute:: fname
    
       A string of the source's file name the line belongs to.
    """
    #@cstart(Line.index)
    index = 0
    """
    .. py:attribute:: index
    
       The integer line index of the directive within the current block.
    """
    #@cstart(Line.text)
    text = ""
    """
    .. py:attribute:: text
    
       A string containing the source line.
    """
    #@cstart(Line.type)
    type = "d"
    """
    .. py:attribute:: type
    
       A char representing the line type:

         * ``d`` stands for a document line
         * ``c`` stands for a code line
    """
    #@

    #Methods
    #@cstart(Line.__init__)
    def __init__(self, fname, index, text, directives=(), type='d'):
        """
        .. py:method:: __init__(name, index, text[, directives[, type]])

           The constructor.
        """
        self.fname = fname
        self.index = index
        self.text = text
        self.directives = directives
        self.type = type


    #@cstart(Line.set)
    def set(self, index=None, type=None, directives=None):
        """
        .. py:method:: set([index=None[, type=None[, directives=None]]])

           Changes the attributes :py:attr:`index`, :py:attr:`type`
           and :py:attr:`directives` at once.

           :param integer index: the line index.
           :param char type: Either ``'d'`` or ``'c'``.
           :param list directives: A list of :py:class:`DCirective` objects.
           :return: The :py:class:`Line` object ``self``.
        """
        if index is not None:
            self.index = index

        if type is not None:
            self.type = type

        if directives is not None:
            self.directives = directives

        return self


    
    def clone(self, dline=None):

        if dline is not None:
            for d in self.directives:
                d.line = dline

        return Line(self.fname, self.index, self.text,
                    self.directives[:], self.type)


    #@cstart(Line.like)
    def like(self, text):
        """
        .. py:method:: like(text)

           Clones the Line with a different text.
        """
        return Line(self.fname, self.index, self.indented(text))


    #@cstart(Line.indented)
    def indented(self, text):
        """
        .. py:method:: indented(text)

           Returns the text, with the same indentation as ``self``.
        """
        return self.sindent + text
    
    #@cstart(Line.change_indent)
    def change_indent(self, delta):
        """
        .. py:method:: change_indent(delta)

           Changes the lines indentation.
        """
        if delta < 0:
            delta = min(-delta, self.indent)
            self.text = self.text[delta:]

        elif delta > 0:
            self.text = " "*delta + self.text

        return self

    #@cstart(Line.__len__)
    def __len__(self):
        """
        .. py:method:: __len__()

           returns the length of the stripped :py:attr:`text`.
        """
        return len(self.text.strip())
        

    #@cstart(Line.__repr__)
    def __repr__(self):
        """
        .. py:method:: __repr__()

           returns a textual representation of the line.
        """
        return "Line(%i, %s, %s)" % (self.index, self.text, str(self.directives))
    #@

    #Properties
    #@cstart(Line.indent)
    @property
    def indent(self):
        """
        .. py:attribute:: indent

        An integer representing the line's indentation.
        """
        return len(self.text)-len(self.text.lstrip())


    #@cstart(Line.sindent)
    @property
    def sindent(self):
        """
        .. py:attribute:: sindent

        A string representation of the line's indentation.
        """
        return " "*self.indent


    #@cstart(Line.directives)
    @property
    def directives(self):
        """
        .. py:attribute:: directives

        A sorted sequence of :py:class:`Directive` objects.
        """
        return self._directives


    @directives.setter
    def directives(self, value):
        self._directives = value[:]
        if self._directives:
            self._directives.sort(key=operator.attrgetter("priority"))


    #@cstart(Line.directive)
    @property
    def directive(self):
        """
        .. py:attribute:: directive

           The first of the contained :py:class:`Directive` objects.
        """
        return self.directives and self.directives[0]
     
#@rstart(document)

#<<document>>
#============

#@code

#@cstart(Document)
class Document(object):
    #@start(Document doc)
    #Document
    #========

    """
    .. py:class:: Document(text, reader, fname, tokens)

       This is the mediator communicating with all other classes
       to generate rst output.
       :param string text: the source code to parse.
       :param reader: An instance of :py:class:`Reader`.
       :param string fname: The file name of the source code.
       :param tokens: A sequence of tokens usable for the ``@if`` directive.
    """

    #@indent 3
    #@include(Document)
    #@include(Document.errors doc)
    #@include(Document.blocks doc)
    #@include(Document.blocks_included doc)
    #@include(Document.compiled_blocks doc)
    #@include(Document.sub_documents doc)
    #@include(Document.tokens doc)
    #@include(Document.macros doc)
    #@include(Document.fname doc)
    #@include(Document.reader doc)
    #@include(Document.lines doc)
    #@include(Document.__init__ doc)
    #@include(Document.process doc)
    #@include(Document.get_subdoc doc)
    #@include(Document.add_error doc)
    #@include(Document.check_errors doc)
    #@include(Document.collect_blocks doc)
    #@include(Document.get_compiled_block doc)
    #@include(Document.compile_block doc)
    #@(Document doc)
    #Attributes
    #@cstart(Document.errors)
    errors = []
    """
    .. py:attribute:: errors
    
       A list of errors found during generation.
    """
    #@cstart(Document.blocks)
    blocks = {}
    """
    .. py:attribute:: blocks
    
       A dictionary of all found blocks: Name -> List of Lines
    """
    #@cstart(Document.blocks_included)
    blocks_included = set()
    """
    .. py:attribute:: blocks_included
    
       A set containing all block names that have been included by
       an @include directive.
    """
    #@cstart(Document.compiled_blocks)
    compiled_blocks = set()
    """
    .. py:attribute:: compiled_blocks
    
       A set containing all block names that have been already
       compiled.
    """
    #@cstart(Document.sub_documents)
    sub_documents = {}
    """
    .. py:attribute:: sub_documents
    
       A cache dictionary of sub documents, referenced by
       ``@include`` directives: Filename -> Document
    """
    #@cstart(Document.tokens)
    tokens = set()
    """
    .. py:attribute:: tokens
    
       A set of token names that can be used for the ``@if`` directive.
    """
    #@cstart(Document.macros)
    macros = {}
    """
    .. py:attribute:: macros
    
       A dictionary containing the macros that can be used
       by the ``@subst`` directive: Macro name -> substitution.
    """
    #@cstart(Document.fname)
    fname = ""
    """
    .. py:attribute:: fname
    
       The file name of the document's source.
    """
    #@cstart(Document.reader)
    reader = None
    """
    .. py:attribute:: reader
    
       The instance of a :py:class:`Reader` object.
    """
    #@cstart(Document.lines)
    lines = []
    """
    .. py:attribute:: lines
    
       A list of :py:class:`Line` objects representing the whole documents
       split in lines.
    """
    #@
    
    #Methods
    #@cstart(Document.__init__)
    def __init__(self, text, reader, fname, tokens):
        """
        .. py:method:: __init__(text, reader, fname, tokens)

           The constructor.
        """
        self.errors = []
        self.blocks = {}
        self.blocks_included = set()
        self.compiled_blocks = set()
        self.sub_documents = {}
        self.tokens = set(tokens or [])
        self.macros = { "__file__" : os.path.split(fname)[-1],
                        "__codeprefix__" : "" }
        self.fname = fname
        self.reader = reader
        self.lines = self.reader.process(fname, text)
        

    #@cstart(Document.process)
    def process(self, show_warnings, fname):
        """
        .. py:method:: process(show_warnings)

           Processes the document and generates the output.
           :param bool show_warnings: If ``True`` warnings are emitted.
           :return: A string representing the rst output.
        """
        self.collect_blocks()
        #print("Blocks", fname,  self.blocks)
        if "" not in self.blocks and not fname.endswith(".rst"):
            self.add_error(0, "no @start() directive found (I need one)")
            self.check_errors()
        

        try:
            text = self.get_compiled_block("")
        finally:
            self.check_errors()

        if show_warnings:
            #@cstart(show warnings)
            self.blocks_included.add("")           #may not cause a warning
            self.blocks_included.add("__macros__") #may not cause a warning
            unincluded = set(self.blocks.keys())-self.blocks_included
            if unincluded:
                logger.warning("The following block were not included:")
                warnings = [ (self.blocks[b][0].index, b) for b in unincluded ]
                warnings.sort(key=operator.itemgetter(0))
                for l, w in warnings:
                    logger.warning("  %s(line %i)", w, l)
            #@
        text = self.reader.filter_output(text)
        return_text = None
        if text:
             return_text = "\n".join(map(operator.attrgetter("text"), text))
        return return_text
    #@edoc
    #@rinclude(show warnings)
    #@(Document.process)
    #@cstart(Document.get_subdoc)
    def get_subdoc(self, rpath):
        """
        .. py:method:: get_subdoc(rpath)

           Tries to compile a document with the relative path rpath.
           :param string rpath: The relative path to the root
           containing document.
           :return: A :py:class:`Document` reference to the sub document.
        """
        #@cstart(return from cache if possible)
        try:
            return self.sub_documents[rpath]
        except KeyError:
            pass

        #@cstart(insert macros function)
        def insert_macros(subdoc):
            #if sub doc has no macros insert mine
            if ("__macros__" not in subdoc.blocks
                and "__macros__" in self.blocks):
                file_ = subdoc.macros["__file__"] # preserve __file__
                subdoc.macros.update(self.macros)
                subdoc.macros["__file__"] = file_

        #@cstart(read the source file)
        head, tail = os.path.split(self.fname)
        fpath = os.path.join(head, rpath)

        try:
            #print "try open", fpath
            with open(fpath, "r") as f:
                text = f.read()
        except IOError:
            doc = None
            logger.error("Could not open: %s", fpath)

        else:
            #parse the file
            lexer = pm.get_lexer_for_filename(rpath)
            single_comment_markers,  block_comment_markers = get_comment_markers(lexer.name)    
            reader = readers.get(lexer.name, Reader)(lexer, single_comment_markers,  block_comment_markers)
    
            doc = Document(text, reader, rpath, self.tokens)
            doc.collect_blocks()
            insert_macros(doc)
        #@
            
        self.sub_documents[rpath] = doc
        return doc

    #@edoc
    #@rinclude(return from cache if possible)
    #@rinclude(insert macros function)
    #@rinclude(read the source file)
    #@(Document.get_subdoc)
    #@cstart(Document.add_error)
    def add_error(self, line, text):
        """
        .. py:method:: add_error(line, text)

           Adds an error to the list.
           :param integer line: The line number that causes the error.
           :param string text: An error text.
        """
        self.errors.append((self.lines[line], text))


    #@cstart(Document.check_errors)
    def check_errors(self):
        """
        .. py:method:: check_errors()

           Raises a ``WebError`` exception if error were found.
        """
        if self.errors:
            raise WebError(self.errors)

    #@cstart(Document.collect_blocks)
    def collect_blocks(self):
        """
        .. py:method:: collect_blocks()

           Collects all text blocks.
        """
        blocks = [ d.collect_block(self, i)
                   for i, l in enumerate(self.lines)
                   for d in l.directives ]
       
        self.blocks = dict(list(filter(bool, blocks)))

        if "__macros__" in self.blocks:
            self.get_compiled_block("__macros__")


    #@cstart(Document.get_compiled_block)
    def get_compiled_block(self, name):
        """
        .. py:method:: get_compiled_block(name)

           Returns the compiled version of a text block.
           Compiled means: all directives where processed.
           :param string name: The name of the text block:
           :return: A list of :py:class:`Line` objects representing
           the text block.
           
        """
        if name not in self.blocks:
            return None
        
        if name in self.compiled_blocks:
            return self.blocks[name]
            
        return self.compile_block(name, self.blocks[name])


    #@cstart(Document.compile_block)
    def compile_block(self, name, block):
        """
        .. py:method:: compile_block(name, block)

           Compiles a text block.
           :param string name: The name of the block
           :param block: A list of :py:class:`Line` objects representing
           the text block to compile.
           :return: A list of :py:class:`Line` objects representing
           the compiled text block.

        """
        #@cstart(find_next_directive)
        def find_next_directive(block):
            # returns the next available directive
            min_line = [ (l.directives[0].priority, i)
                         for i, l in enumerate(block) if l.directives ]
            if not min_line:
                return None

            prio, index = min(min_line)
            return block[index].directives.pop(0), index
        #@(find_next_directive)

        while True:
            directive_index = find_next_directive(block)
            if not directive_index: break
            directive, index = directive_index
            directive.process(self, block, index)

        self.compiled_blocks.add(name)
        return block
    #@edoc
    #@rinclude(find_next_directive)
    #@(Document.compile_block)


#@cstart(generate)
def generate(fname, tokens, show_warnings=False):
    """
    ..  py:function:: generate(fname, tokens, warnings)

        Generates a rst file from a source file.

        :param string fname: The path to the source file.
        :param list tokens: A list of string tokens, used for @if directives.
        :param bool show_warnings: Warnings will be written 
                                   via the logging module.
    """
    try:    
        with open(fname, "r") as f:
            text = f.read()
    except IOError:
        logger.error("file not found: %s", fname)
        sys.exit(1)
    
    lexer = pm.get_lexer_for_filename(fname)
    #get the language specific comment markers based on the pygments lexer name
    single_comment_markers,  block_comment_markers = get_comment_markers(lexer.name)
    #initialise a new Reader based on the pygments lexer name 
    reader = readers.get(lexer.name, Reader)(lexer, single_comment_markers,  block_comment_markers)
       
    document = Document(text, reader, fname, tokens)
    return document.process(show_warnings, fname)
#@(generate)

#@cstart(get_comment_markers)

def get_comment_markers(lexer_name):
    #@start(get_comment_markers doc)
    #From the map above the comment markers are retrieved via the following method:
    
    """
    ..  py:function:: get_comment_markers(lexer_name)

        Retrieves the language specific comment markers from the comments map.
        The comment markers of C serves as the default comment markers if the lexer name cannot be found.

        :param string lexer_name: The name of the pygments lexer.
        :return: The single and comment block markers defined by the language                           
    """
    #@indent 4
    #@include(get_comment_markers)
    #@(get_comment_markers doc)
    comment_markers = comments.get(lexer_name, comments["C"])
    single_comment_markers = comment_markers[0]
    block_comment_markers = comment_markers[1]
    return single_comment_markers,  block_comment_markers  

#@(document)

#@start(process_file)
#process_file
#============

#If no output name was declared, the input name will be given

#@code

def process_file(in_file, out_file, token, warnings):

#@edoc

#The output text will be written in the output file. If there is an output text, the function returns could_write as True.

#@code
    could_write = False
    try:
        text_output = generate(in_file, token, warnings)
        
        if text_output:
            with open(out_file, "w") as f:
                f.write(text_output)
            could_write = True
    except WebError as e:
        logger.error("\nErrors:")
        for l, d in e.error_list:
            logger.error("  in line %i(%s): %s", l.index+1, l.fname, d)
            logger.error("      %s", l.text)

    return could_write
#@edoc

#@start(search_for_generated_block)
#search_for_generated_block
#============================

#The index file is searched for the generated block. The contents in the generated block are deleted.
#Afterwards the whole file content and the endline of the generated block are returned.

#@code

def search_for_generated_block(index_rst, start_of_block, end_of_block):
    
    startline = None
    endline = None
    content = ""

    with open(index_rst, "r") as index_file:
        for num, line in enumerate(index_file):
            if start_of_block in line:
                startline = num
            if end_of_block in line:
                endline = num

            if startline and endline:
                index_file.seek(0, 0)
                content = index_file.readlines()
                #delete content of generated block
                del content[startline+1:endline]
                #set endline = old_endline - deleted lines
                endline = endline - (endline-(startline+1))
    return (content, endline)
#@edoc

#@start(write_documentation)

#Writing the documentation files
#===============================

#From the given file a .rst file will be created if it contains an antiweb :py:class:`start() directive`.
#The following function is called for the creation of the documentation files.

#@include(write doc)
#@include(write_body)
#@(write_documentation) 

#@start(write)
def write(working_dir, input_file, options, index_file, start_block, end_block):
#@start(write doc)
    """
.. py:method:: write(working_dir, input_file, options, index_file, start_block, end_block)
    
   Creates the corresponding documention file and optionally adds the processed file to the index file.
           
   :param working_dir: Current working directory.
   :param input_file: Contains the absolute path of the currently processed file.
   :param options: Commandline options.
   :param index_file: Absolute path of the index file.
   :param start_block: String which contains the generated index block start definition.
   :param end_block: String which contains the generated index block end definition.
    """
#@(write doc) 

#@start(write_body)

#Before the input file is processed the name of the output file has to be computed. 
#How the output file name is created depends on the different commandline options.
#When there is no output option given the output file name is created in the following way:

#.. csv-table::
#   :header: "Input File", "Output File"

#   ``C:\antiweb\testing.cs``, *C:\\antiweb\\testing.rst*
#   ``C:\antiweb\testing.rst``, *C:\\antiweb\\testing_docs.rst*

#@code
#@include(write)

    output = options.output
    recursive = options.recursive
    
    if not output:
        out_file = create_out_file_name(working_dir, "", input_file)

#@edoc

#If there is an output given, we have to distinguish between the recursive and non-recursive option.
#When the recursive option is used in combination with the output option, the output parameter is treated as the documentation directory:

#.. csv-table::
#   :header: "Input File", "Output File"

#   ``C:\antiweb\ -r -o report.rst``,*C:\\antiweb\\report.rst\\file.rst*
#   ``C:\antiweb\ -r -o report``,*C:\\antiweb\\report\\file.rst*
#   ``C:\antiweb\ -r -o C:\antiweb\report.rst``,*C:\\antiweb\\report.rst\\file.rst*
#   ``C:\antiweb\ -r -o \..\report.rst``,*C:\\report.rst\\file.rst*

#@code
    else:           
        if recursive:
            #The output parameter is treated as a directory.
            #If it is a relative path it is combined with the current working directory.
            directory = output
            out_file = create_out_file_name(working_dir,directory,input_file)
#@edoc    

#When the output option is used without the recursive option the output file name is computed in the following way: 

#.. csv-table::
#   :header: "Input File", "Output File"

#   ``C:\antiweb\testing.cs -o report.rst``,*C:\\antiweb\\report.rst*
#   ``C:\antiweb\testing.cs -o report``,*C:\\antiweb\\report\\testing.rst*
#   ``C:\antiweb\testing.cs -o \..\report``,*C:\\report\\testing.rst*
#   ``C:\antiweb\testing.cs -o report\report.rst``,*C:\\antiweb\\report\\report.rst*
#   ``C:\antiweb\testing.cs -o report\report.rst\``,*C:\\antiweb\\report\\report.rst\\testing.rst*
#   ``C:\antiweb\testing.cs -o C:\report\report.rst``,*C:\\report\\report.rst*

#@code       
        else:
            #Get the file extension from output parameter
            file_extension = os.path.splitext(output)[1]
            
            if file_extension:
                #If there is a file extension the last part of the output parameter is treated as the output file name.
                path_tokens = os.path.split(output)
                directory = path_tokens[0] 
                file_name = path_tokens[1]
                
                #If directory contains an absolute path the working directory will be ignored,
                #otherwise all three parameters will be joined
                out_file = os.path.join(working_dir, directory, file_name)
                out_file = os.path.abspath(out_file)
            else:
                #If there is no file extension the whole output parameter is treated as the report directory.
                directory = output
                out_file = create_out_file_name(working_dir, directory, input_file)
    
    #Create the documentation directory. If it can't be created the program exits.
    create_doc_directory(out_file)
#@edoc

#Now the input file is processed and the corresponding documentation file is created.
#If processing is successful, ''could_process'' is set to ''True''.

#@code

    could_process = process_file(input_file, out_file, options.token, options.warnings)
    
#@edoc

#If the file was processed successfully and the index option is used, the file name which should be inserted
#in the generated index file block has to be computed first. Afterwards the file name is inserted into the 
#index file (see :py:meth:`insert_filename_in_index_file`).

#@code
    if options.index and could_process:
        out_file_name_index = create_out_file_name_index(out_file, working_dir, recursive)
        insert_filename_in_index_file(out_file_name_index, index_file, start_block, end_block)
#@edoc
#@(write_body)

#@cstart(create_out_file_name)

def create_out_file_name(working_dir, directory, input_file):
#@start(create_out_file_name doc)
    """
.. py:method:: create_out_file_name(working_dir, directory, input_file)
   
  Computes the absolute path of the output file name. The input file name suffix is replaced by 
  ".rst". If the input file name ends with ".rst" the string "_docs" is added before the suffix.
  If directory contains a relative path, then the paths of the working_dir and the directory 
  are combined with the input file name. Otherwise, the directory is combined with the 
  input file name.
             
  :param working_dir: Absolute path of the current working directory.
  :param directory: The documentation directory (absolute or relative)
  :param input_file: The absolute path to the file which should be processed.
  :return: The path of the output file.
    """
    
#.. csv-table::
#   :header: "Working_Dir", "Directory", "Input_File_Name", "Output_File_Name"

#   *C:\\antiweb\\*,doc, *C:\\antiweb\\testing.py* , *C:\\antiweb\\doc\\testing.rst*
#   *C:\\antiweb\\* , , *C:\\antiweb\\testing.py* , *C:\\antiweb\\testing.rst*
#   *C:\\antiweb\\* ,*C:\\doc\\* , *testing.py*, *C:\\doc\\testing.rst*
#   *C:\\antiweb\\*,doc, *C:\\antiweb\\testing.rst* , *C:\\antiweb\\doc\\testing_docs.rst*

#@include(create_out_file_name) 
#@(create_out_file_name doc) 

    docs = "_docs"
    rst_suffix = ".rst"
    out_file_path = os.path.splitext(input_file)[0]
    
    if input_file.endswith(rst_suffix):
        out_file_path =  out_file_path + docs
        
    out_file_path =  out_file_path + rst_suffix

    out_file_name = os.path.split(out_file_path)[1]
    
    #If directory contains an absolute path, the working directory is ignored.
    out_file = os.path.join(working_dir, directory, out_file_name)
    out_file = os.path.abspath(out_file)
    return out_file
    
#@(create_out_file_name)

#@cstart(create_out_file_name_index)

def create_out_file_name_index(out_file, working_dir, recursive):
#@start(create_out_file_name_index doc)
    """
.. py:method:: create_out_file_name_index(out_file, working_dir, recursive)
   
  Creates the file name which should be inserted into the generated index file block.
  
  :param out_file: Absolute path of the output file.
  :param index_file: Absolute path of the index file.
  :param recursive: Boolean which indicates whether the recursive commandline options is used.
  :return: The file name which should be inserted in the generated index file block.
    """
    
#If the user added the -i flag, an index file (documentation base file) is created which contains all processed files.
#The names of the processed files are added between the :py:class:`start(generated)` and :py:class:`end(generated)` directives.
#The file names which are inserted into the index file are computed in the following way: 

#When the recursive option is used the file name in the index file is a relative path without extension. 
#Otherwise the index file will only contain the filename without extension. 
#Path seperator characters are replaced by "_".

#| Non-recursive example with current processed file: *C:\\antiweb\\report.rst\\file.rst*:
#| :py:class:`start(generated)`
#| :py:class:`file`
#| :py:class:`end(generated)`
#|
#| Recursive example with current processed file: *C:\\antiweb\\report.rst\\file.rst*:
#| :py:class:`start(generated)`
#| :py:class:`report.rst_file`
#| :py:class:`end(generated)`
#|

#@include(create_out_file_name_index)        
#@(create_out_file_name_index doc)     

    #1) Obtain only the file name
    out_file_name_index = os.path.split(out_file)[1]
    #2) Remove the extension
    out_file_name_index = os.path.splitext(out_file_name_index)[0]
    if recursive:
        out_file_name_index = os.path.relpath(out_file_name_index, working_dir)
        out_file_name_index = replace_path_seperator(out_file_name_index)
        
    return out_file_name_index
    
#@(create_out_file_name_index)


#@cstart(insert_filename_in_index_file)

def insert_filename_in_index_file(file_name, index_file, start_block, end_block):
#@start(insert_filename_in_index_file doc)
    """
.. py:method:: insert_filename_in_index_file(file_name, index_file, start_block, end_block)
   
  Inserts the given file name into the generated block in the index file.
  
  :param file_name: The file name which should be inserted into the index file.
  :param index_file: Absolute path of the index file.
  :param start_block: String which contains the generated index block start definition.
  :param end_block: String which contains the generated index block end definition.
    """

#If the user added the -i flag, an index file (documentation base file) is created which contains all processed files.
#Between the :py:class:`start(generated)` and :py:class:`end(generated)` directives the names of the processed files are added.
#Read  :py:meth:`create_out_file_name_index` for more information about how the inserted file name is computed.
#Files can be manually added after the :py:class:`end(generated)` directive.

#@include(insert_filename_in_index_file)        
#@(insert_filename_in_index_file doc) 
    
    #At first the position has to be found where the new file should be inserted.
    content, endline = search_for_generated_block(index_file, start_block, end_block)
    
    #If the index file does not contain the generated block, it is appended.
    if not content:
        write_static(index_file, start_block, end_block)
        content, endline = search_for_generated_block(index_file, start_block, end_block)

    if endline:
        #The new file name is inserted into the index file contents.
        content.insert(endline, "   " + file_name + "\n")

    try: 
        #The adapted index file contents are written out to the index file.
        with open(index_file, "w") as index_out:
            for item in content:
                index_out.write(item)
    except IOError:
        logger.error("\nError: Could not write to index file: %s",  index_file)
        sys.exit(1)

#@(insert_filename_in_index_file)

#@cstart(create_doc_directory)

def create_doc_directory(out_file):
#@start(create_doc_directory doc)
    """
.. py:method:: create_doc_directory(out_file)
    
   Creates the documentation directory if it does not yet exist.
   If an error occurs, the program exits.
           
   :param out_file: The path to the output file.
    """
#@include(create_doc_directory) 
#@(create_doc_directory doc)        
    try:
        out_file_directory = os.path.split(out_file)[0]       
        if not os.path.exists(out_file_directory):
            os.makedirs(out_file_directory)
    except IOError:
        logger.error("\nError: Documentation Directory: %s could not be created",  out_file_directory)
        sys.exit(1)
#@(create_doc_directory)


#@cstart(replace_path_seperator)

def replace_path_seperator(file_path):
#@start(replace_path_seperator doc)
    """
.. py:method:: replace_path_seperator(file_path)
    
   Replaces OS specific path seperator characters by '_'.
           
   :param file_path: The path to a file.
    """
#@include(replace_path_seperator) 
#@(replace_path_seperator doc)      
#Path seperator characters are replaced by "_" in the index file
    if _platform == "linux" or _platform == "linux2":
        file_path = file_path.replace("/","_")
    if _platform == "win32":
        file_path = file_path.replace("\\","_")      
    return file_path
#@(replace_path_seperator)


#@cstart(write_static)

def write_static(index_file, start_block, end_block):
#@start(write_static doc)
    """
.. py:method:: write_static(index_file, start_of_block, end_of_block)
    
   Writes the static contents to the index file.
           
   :param index_file: Absolute path of the index file.
   :param start_block: String which contains the generated index block start definition.
   :param end_block: String which contains the generated index block end definition.
    """
#@include(write_static) 
#@(write_static doc)      

    index_generated = "   " + start_block +"\n   " + end_block
    write_option = "w"
    index_content = "Documentation\n=======================\nContents:\n\n.. toctree::\n   :maxdepth: 2\n\n" + index_generated
    
    try:
        os.makedirs(os.path.dirname(index_file), exist_ok=True)
        
        with open(index_file, write_option) as index_out:
            index_out.write(index_content)
    except IOError:
        logger.error("\nError: Index File: %s could not be created.",  index_file)
        sys.exit(1)
        
#@(write_static)

#@cstart(create_index_file)
def create_index_file(working_dir, directory, file_name, start_block, end_block):
#@start(create_index_file doc)
    """
.. py:method:: create_index_file(working_dir, directory, file_name, start_block, end_block)
    
   Creates the index file and writes the standard index file contents into the file.
   
   :param working_dir: Current working directory. 
   :param directory: Output directory (may contain a directory path or a directory name)           
   :param file_name: Filename of the index file.
   :param start_block: String which contains the generated index block start definition.
   :param end_block: String which contains the generated index block end definition.
   :return: The absolute path of the index file.
    """
#@include(create_index_file) 
#@(create_index_file doc)      
    
    index_file = os.path.join(working_dir, directory, file_name)
    index_file_absolute = os.path.abspath(index_file)
    
    #index file is overwritten if it already exists
    write_static(index_file_absolute, start_block, end_block)
    
    return index_file
#@(create_index_file)   
 
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
    
    parser.add_option("-i", "--index", dest="index",
                      action="store_true", help="Automatically write file(s) to Sphinx' index.rst")

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

    index_rst = "index.rst"
    start_block = ".. start(generated)"
    end_block = ".. end(generated)"
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
                
        if options.index:
            index_rst = create_index_file(directory, options.output, index_rst, start_block, end_block)
                    
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
                    write(directory, fname, options, index_rst, start_block, end_block)

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
           
        if options.index:
            #check if output contains a directory or a file name
            index_rst = create_index_file(os.getcwd(), "", index_rst, start_block, end_block)    
                
        write(os.getcwd(), absolute_file_path, options, index_rst, start_block, end_block)
    
    os.chdir(previous_dir)
    return True
#@edoc

#@include(write_documentation)
#@include(create_out_file_name doc)
#@include(create_out_file_name_index doc)
#@include(insert_filename_in_index_file doc)
#@include(create_doc_directory doc)
#@include(replace_path_seperator doc)
#@include(write_static doc)
#@include(create_index_file doc)
#@include(process_file)
#@include(search_for_generated_block)
#@include(parsing doc)

if __name__ == "__main__":
    main()


#@(file layout)
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