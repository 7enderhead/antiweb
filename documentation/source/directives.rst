**********
Directives
**********

Directive
=========

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
   
   ::
   
       class Directive(object):
           #Attributes
           <<Directive.expression>>
           <<Directive.priority>>
           <<Directive.line>>
       
           #Methods
           <<Directive.__init__>>
           <<Directive.collect_block>>
           <<Directive.process>>
           <<Directive.match>>
           <<Directive.__repr__>>
       
   
   .. py:attribute:: expression
   
      A regular expression defining the directive.
      
      ::
      
          expression = ""
      
   .. py:attribute:: priority
   
      An integer process priority. Directives with a lower priority
      will be processed earlier.
      
      ::
      
          priority = 10
      
   .. py:attribute:: line
   
      A integer defining the original line number of the directive.
      
      ::
      
          line = None
      
   .. py:method:: __init__(line[, mo])
   
      The constructor
      
      ::
      
          def __init__(self, line, mo=None):
              self.line = line
          
          
      
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
      
      ::
      
          def collect_block(self, document, index):
              return None
          
          
      
   .. py:method:: process(document, block, index)
   
      This method is called by :py:class:`Document`.
      The directive should do whatever it is supposed to do.
   
      :param document: the document calling the function.
      :type document: :py:class:`Document`
      :param block: The line block the directive is in.
      :param integer index: the line index of the directive
                            within the block.
      
      ::
      
          def process(self, document, block, index):
              pass
          
          
      
   .. py:method:: match(lines)
   
      This method is called by :py:class:`Document`.
      It gives the directive the chance to find and manipulate other
      directives.
   
      :param list lines: a list of all document lines.
      
      ::
      
          def match(self, lines):
              pass
          
          
      
   .. py:method:: __repr__()
   
      returns a textual representation of the directive.
      
      ::
      
          def __repr__(self):
              return "<%s at %i>" % (self.__class__.__name__, self.line)
          
      
NameDirective
=============
.. py:class:: NameDirective(line, mo)

   The base class for directives with a name argument.
   It inherits :py:class:`Directive`.

   :param line: the line number the directive was found
   :param mo: a match object of an regular expression or
              a string defining the name.

   .. py:attribute:: name

      A string defining the argument of the directive.
   
   ::
   
       class NameDirective(Directive):
           def __init__(self, line, mo):
               super(NameDirective, self).__init__(line, mo)
               if isinstance(mo, str):
                   self.name = mo
               else:
                   self.name = mo.group(1)
       
       
           def __repr__(self):
               return "<%s(%s) %i>" % (self.__class__.__name__,
                                       self.name, self.line)
       
       
   
Start
=====
.. py:class:: Start

   This class represents a ``@start`` directive. It inherits
   :py:class:`NameDirective`.

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
   
   ::
   
       class Start(NameDirective):
           #Attributes
           <<Start.has_named_end>>
           <<Start.inherited attributes>>
       
           #Methods
           <<Start._find_matching_end>>
           <<Start.collect_block>>
           <<Start.process>>
       
   
   .. py:attribute:: has_named_end
   
      A boolean value, signalizing if the directive is
      ended by a named end directive.
      
      ::
      
          has_named_end = False
      
   
   .. _Start.inherited attributes:
   
   **<<Start.inherited attributes>>**
   
   
   ::
   
       expression = re.compile(r"@start\((.*)\)")
       priority = 5
   
   .. py:method:: collect_block(document, index)
   
      See :py:meth:`Directive.collect_block`.
      The returned lines are unindented to column 0.
      
      ::
      
          def collect_block(self, document, index):
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
          
          
      
   .. py:method:: process(document, block, index)
   
      See :py:meth:`Directive.process`.
      Removes all lines of the text block from
      the containing block.
      
      ::
      
          def process(self, document, block, index):
              end = self._find_matching_end(block[index:])
              del block[index:index+end]
      
   .. py:method:: _find_matching_end(block)
   
      Finds the matching end for the text block.
   
      :param list block: A list of lines beginning with start
      :return: The line index of the found end.
      
      ::
      
          def _find_matching_end(self, block):
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
          
      
RStart
======
.. py:class:: RStart

   This class represents a ``@rstart`` directive. It inherits
   :py:class:`Start`.

   The ``@rstart`` directive works like the ``@start``
   directive. While ``@start`` removes it's block completely
   from the containing block. ``@rstart`` replaces the lines
   with a ``<<name>>`` - Sentinel.
   
   ::
   
       class RStart(Start):
           expression = re.compile(r"@rstart\((.*)\)")
       
           def process(self, document, block, index):
               end = self._find_matching_end(block[index:])
               line = block[index]
               block[index:index+end] = [ line.like("<<%s>>" % self.name) ]
       
       
   
CStart
======
.. py:class:: CStart

   This class represents a ``@rstart`` directive. It inherits
   :py:class:`RStart`.

   The ``@cstart(name)`` directive is a replacement for

   ::

      @rstart(name)
      @code
   
   ::
   
       class CStart(RStart):
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
       
   
End
===
.. py:class:: End

   This class represents an end directive. It inherits
   :py:class:`NameDirective`.

   The end (``@``) directive ends a text block.
   
   ::
   
       class End(NameDirective):
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
       
       
   
Include
=======
.. py:class:: Include

   This class represents an ``@include`` directive. It inherits
   :py:class:`NameDirective`.

   The ``@include`` directive inserts the contents of the
   text block with the same name. The lines have the same
   indentation as the ``@include`` directive.

   The directive can have a second *file* argument. If given
   the directive inserts the text block of the specified file.
   
   ::
   
       class Include(NameDirective):
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
       
       
       
   
RInclude
========
.. py:class:: RInclude

   This class represents an ``@rinclude`` directive. It inherits
   :py:class:`Include`.

   The ``@rinclude(text block name)`` directive is a is a replacement for::

      .. _text block name:

      **<<text block name>>**

      @include(text block name)

   
   ::
   
       class RInclude(Include):
           expression = re.compile(r"@rinclude\((.+)\)")
       
           def process(self, document, block, index):
               l = block[index]
               super(RInclude, self).process(document, block, index)
       
               block[index:index] = [ l.like(""),
                                      l.like(".. _%s:" % self.name),
                                      l.like(""),
                                      l.like("**<<%s>>**" % self.name),
                                      l.like("") ]
       
       
   
Code
====
.. py:class:: Code

   This class represents an ``@code`` directive. It inherits
   :py:class:`Directive`.

   The ``@code`` directive starts a code block. All
   lines following ``@code`` will be displayed as source code.

   A ``@code`` directive ends,
     * if the text block ends
     * if an ``@edoc`` occurs.

   The content of the special macro ``__codeprefix__`` is inserted
   before each code block. ``__codeprefix__`` is empty by default
   and can be defined by a ``@define`` directive.

   
   ::
   
       class Code(Directive):
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
       
       
   
Edoc
====
.. py:class:: Edoc

   This class represents an ``@edoc`` directive. It inherits
   :py:class:`Directive`.

   The ``@edoc`` directive ends a previously started ``@code`` directive
   
   ::
   
       class Edoc(Directive):
           expression = re.compile(r"@edoc")
       
           def process(self, document, block, index):
               del block[index]
       
       
   
If
===
.. py:class:: If

   This class represents an ``@if`` directive. It inherits
   :py:class:`NameDirective`.

   The ``@if`` directive is used for conditional weaving.
   The content of an ``@if``, ``@fi`` block is waved if the
   named token argument of ``@if``, is defined in the command line
   by the ``--token`` option.
   
   ::
   
       class If(NameDirective):
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
       
   
Fi
===
.. py:class:: Fi

   This class represents a `@fi` directive. It inherits
   :py:class:`NameDirective`.

   The ``@fi`` ends an ``@if`` directive
   
   ::
   
       class Fi(NameDirective):
           expression = re.compile(r"@fi\((.+)\)")
       
           def process(self, document, block, index):
               del block[index]
       
       
   
Ignore
======
.. py:class:: Ignore

   This class represents an ``@ignore`` directive. It inherits
   :py:class:`Directive`.

   The ``@ignore`` directive ignores the line in the
   documentation output. It can be used for commentaries.

   
   ::
   
       class Ignore(Directive):
           expression = re.compile("@ignore")
       
           def process(self, document, block, index):
               del block[index]
       
   
Define
======
.. py:class:: Define

   This class represents an ``@define`` directive. It inherits
   :py:class:`NameDirective`.

   The ``@define`` directive defines a macro, that can be used
   with a ``@subst`` directive. If a ``substitution``
   argument is given, the macro defines an inline substitution.
   Otherwise the ``@define`` has to be ended by an ``@enifed``
   directive.
   
   ::
   
       class Define(NameDirective):
       
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
       
   
Enifed
======
.. py:class:: Enifed

   This class represents an ``@enifed`` directive. It inherits
   :py:class:`NameDirective`.

   The ``@enifed`` directive ends a macro defined by the
   ``@define`` directive.
   
   ::
   
       class Enifed(NameDirective):
       
           expression = re.compile(r"@enifed\((.+)\)")
       
           def process(self, document, block, index):
               del block[index]
       
   
Subst
=====
.. py:class:: Subst

   This class represents a ``@subst`` directive. It inherits
   :py:class:`NameDirective`.

   The ``@subst`` directive is replaced by the substitution,
   defined by a ``@define`` directive. There are two predefined
   macros:

    ``__line__``
         Define the current line within the source code. The
         ``@subst`` can also handle operation with ``__line__``
         like ``__line__ + 2``.

    ``__file__``
        Defines the current source file name.
   
   ::
   
       class Subst(NameDirective):
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
       
       
   
Indent
======
.. py:class:: Indent

   This class represents an ``@indent`` directive. It inherits
   :py:class:`Directive`.

   The ``@indent`` directive changes the indentation of the
   following lines. For example a  call ``@indent -4``
   dedents the following lines by 4 spaces.
   
   ::
   
       class Indent(Directive):
           expression = re.compile("@indent\s+([+-]?\d+)")
       
           def __init__(self, line, mo):
               super(Indent, self).__init__(line, mo)
               self.indent = int(mo.group(1))
       
       
           def process(self, document, block, index):
               lines = [ l.clone().change_indent(self.indent)
                         for l in block[index+1:] ]
               block[index:] = lines
       
       
   
import re
import operator
