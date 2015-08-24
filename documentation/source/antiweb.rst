.. default-domain:: python

.. highlight:: python
   :linenothreshold: 6



#######
antiweb
#######

************
Installation
************

The most important parts of the system are Python 3, Sphinx and antiweb. Because of incompatibility with Python 2 you can't create 
documentaries of Python 2 programs.


   * Install Python 3.4
   * After installing Python, run below commands in cmd (you can add the directories to the PATH or navigate to the directories [I would prefer the first option])
   
   
   ::
   
       pip install sphinx 
   
   * :py:class:`IMPORTANT`: If you get a connection error the reason is most likely your proxy. You then have to use a tool like "cntlm" and add a proxy flag when running pip, example:
   
   
   ::
   
       pip install sphinx --proxy http://localhost:8123
   
   * The pre-installed version of babel doesn't work with Python 3, so we need to install an updated version from GitHub. Start the Git Shell and enter this command:
   
   
   ::
   
       pip install git+https://github.com/jun66j5/babel.git [options]

   * Run sphinx-quickstart.exe and follow the steps to configure sphinx as you like it (however, say yes to all extensions suggested during the process). The sphinx quickstart created a project folder for you, open the conf.py which is in that folder

   * You should find something like this: 

           
           ::
           
               extensions = [
               'sphinx.ext.autodoc',
               'sphinx.ext.doctest',
               'sphinx.ext.intersphinx',
               'sphinx.ext.todo',
               'sphinx.ext.coverage',
               'sphinx.ext.mathjax',
               'sphinx.ext.ifconfig',
               'sphinx.ext.viewcode',
               ]

    * Add 'sphinx.ext.graphviz' at the end and it will look like this:

           
           ::
           
               extensions = [
               'sphinx.ext.autodoc',
               'sphinx.ext.doctest',
               'sphinx.ext.intersphinx',
               'sphinx.ext.todo',
               'sphinx.ext.coverage',
               'sphinx.ext.mathjax',
               'sphinx.ext.ifconfig',
               'sphinx.ext.viewcode',
               'sphinx.ext.graphviz',
               ]

   * Download the Graphviz msi installer from here: http://www.graphviz.org/Download_windows.php 
   * Add the bin folder inside the Graphviz directory to the PATH


Preparing the .rst files
========================

   * Copy the ``antiweb.py`` file from my GitHub repository into the ``Python34`` folder
   
    * You can now begin creating a .rst file out of a C, C++, C# and py file. To do that, simply use following command:
   
   
   ::
   
       python antiweb.py "PATH TO THE FILE/DIRECTORY" [options]
   
   * You will then find a new file which is called ``Filename.rst`` -> This file will be used in Sphinx to generate the documentation
   
   * antiweb can also create/edit a file called "index.rst" if you add the -i option when executing antiweb. In that index all processed files for documentation with sphinx are included
   
   * When you don't use the -i option you have to edit the file manually (sphinx-quickstart created it):

   
   ::
   
    Welcome to Antiweb's documentation!
    ===================================
    
    Contents:
    
       .. toctree::
          :maxdepth: 2
    
          filename #without file extension!
    

   * You can add multiple files, they will then be listed in the generated index of your html project
   * It is also possible to use Graphviz for graph visualizatin. A proper graph should look like this:
   
   ::
   
       .. digraph:: name
    
        "bubble 1" -> "bubble 2" -> "bubble 3" -> "bubble 1";

   * The output from above code would look like this:

   .. digraph:: test

    "bubble 1" -> "bubble 2" -> "bubble 3" -> "bubble 1";

   * For more informatin on Graphviz visit http://www.graphviz.org/
   * When you have included the rst file in the index file, you can run Sphinx to finally create your documentation, here is an example:
   
   ::
   
       sphinx-build.exe -b html sphinx\source sphinx\source -D graphviz_dot=dot.exe
   
   * The ``-b`` flag indicates the builder to use
   * ``sphinx\source`` indicates the path to the index.rst
   * ``sphinx\source`` indicates the output path (you can change your output path to every path where you want the final documentation)
   * ``-D graphviz_dot=dot.exe`` indicates the path for the graphviz virtualizer dot.exe (which you already copied to the Scripts folder)
   
   * After sphinx has finished you will find some .html files in the output path. This is your finished documentation. 




   
   
   
           
           
   
   
   
   

***************
Getting Started
***************

   Every @ directive in antiweb has to be a comment in order to be accepted by antiweb. However, antiweb will still recognize but not accept directives which aren't comments, 
   so for the examples here :py:class:`I will leave 1 free space between the @ and the directive name` but you should NOT do so in your file.
   
   
@ start
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
   
@ rstart
========
   The ``@rstart`` directive works like the ``@start`` directive. While ``@start`` removes it’s block completely from the containing block, 
   ``@rstart`` replaces the lines with a ``<<name>>`` - Sentinel.
   
   
   ::
   
       
       try:    
            with open(fname, "r") as f:
                text = f.read()
        except IOError:
          <<name>>
            sys.exit(1)
       
   <<Name>>
   
   ::
   
       logger.error("file not found: %s", fname)
   
@ cstart
========

   The ``@cstart`` directive can be used as a shortcut for:
   
   
   ::
   
       @ start(block)
       @ code

@ include
=========

   Once you have created a block  you can include it with the ``@include`` directive. The order in which your blocks will appear in the documentation is defined by the order of the ``@include`` directives
   
   
   ::
   
       
       @ include(Blockname)
       
   
@ code
======
   Of course you want parts of your source code in a Block in order to e.g. describe the function of it. You can do that by following this example, a code block starts and ends with those directives. The code in between will be normally recognized as code but also included in the documentation:
   
   
   ::
   
       
       @ code 
       #End of comment section
       
       Put your code here
       
       #Beginning of next comment section
       @ edoc 
       
   
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
       
   
@ indent
========
   You can indicate antiweb to make a manual indentation with the ``@indent spaces`` directive, replacing ``spaces`` by three would indent the text by three spaces
   
Indentation matters!
====================
   
   In sphinx and antiweb, the indentation matters. To effectively nest blocks, create sub headlines and more you have to keep the indentation in mind. To nest a block or headline you have to indent it farther than its parent. In addition, your documentation looks much cleaner when structured like this.
   
   
   
   
   
   


* :py:class:`This is the end of the basic introduction. For more information on antiweb simply read on.`


#####################
Antiweb documentation
#####################

If you just want to generate the documentation from a source file use 
the following function:

..  py:function:: generate(fname, tokens, warnings)

    Generates a rst file from a source file.

    :param string fname: The path to the source file.
    :param list tokens: A list of string tokens, used for @if directives.
    :param bool show_warnings: Warnings will be written 
                               via the logging module.
    
    ::
    
        def generate(fname, tokens, show_warnings=False):
            try:    
                with open(fname, "r") as f:
                    text = f.read()
            except IOError:
                logger.error("file not found: %s", fname)
                sys.exit(1)
            
            lexer = pm.get_lexer_for_filename(fname)
            reader = readers.get(lexer.name, Reader)(lexer)
           
            document = Document(text, reader, fname, tokens)
            return document.process(show_warnings)
        
        
    


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
               line = block[index]
       
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
               
       
   


*******
Readers
*******

Readers are responsible for the language dependent
source parsing.

Reader
======
.. py:class:: Reader(lexer)

   This is the base class for all readers. The public functions
   exposed to :py:class:`Document` are :py:meth:`process`,
   and :py:meth:`filter_output`.

   The main tasks for a reader is:

     * Recognize lines that can contain directives. (comment lines or doc strings).
     * Modify the source for language specific optimizations.
     * Filter the processed output.
   
   :param lexer: A pygments lexer for the specified language
   
   ::
   
       
       re_line_start = re.compile("^", re.M) #to find the line start indices
       
       class Reader(object):
           #Public Methods
           <<Reader.__init__>>
           <<Reader.process>>
           <<Reader.filter_output>>
           
           #Protected Methods
           <<Reader._accept_token>>
           <<Reader._post_process>>
           <<Reader._handle_token>>
           <<Reader._cut_comment>>
   
   .. py:method:: __init__(lexer)
   
      The constructor
      
      ::
      
          def __init__(self, lexer):
              self.lexer = lexer
          
          
      
   .. py:method:: process(fname, text)
   
      Reads the source code and identifies the directives.
      This method is call by :py:class:`Document`.
   
      :param string fname: The file name of the source code
      :param string text: The source code
      :return: A list of :py:class:`Line` objects.
      
      ::
      
          def process(self, fname, text):
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
          
          
      
   .. py:method:: filter_output(lines)
   
      This method is call by :py:class:`Document` and gives
      the reader the chance to influence the final output.
   
      
      ::
      
          def filter_output(self, lines):
              return lines
              
      
   .. py:method:: _handle_token(index, token, value)
   
      Find antiweb directives in valid pygments tokens.
   
      :param integer index: The index within the source code
      :param token: A pygments token.
      :param string value: The token value.
      
      ::
      
          def _handle_token(self, index, token, value):
                      
              if not self._accept_token(token): return
                   
              cvalue = self._cut_comment(index, token, value)
              offset = value.index(cvalue)
              found = False
              for k, v in list(directives.items()):
                  for mo in v.expression.finditer(cvalue):
                      li = bisect.bisect(self.starts, index+mo.start()+offset)-1
                      line = self.lines[li]
                      line.directives = list(line.directives) + [ v(line.index, mo) ]
               
          
      
   .. py:method:: _cut_comment(index, token, value)
   
      Cuts of the comment identifiers.
   
      :param integer index: The index within the source code
      :param token: A pygments token.
      :param string value: The token value.
      :return: value without comment identifiers.
      
      ::
      
          def _cut_comment(self, index, token, value):
              return text
          
          
      
   .. py:method:: _post_process(fname, text)
   
      Does some post processing after the directives where found.
      
      ::
      
          def _post_process(self, fname, text):
          
              #correct the line attribute of directives, in case there have
              #been lines inserted or deleted by subclasses of Reader
              for i, l in enumerate(self.lines):
                  for d in l.directives:
                      d.line = i
          
              #give the directives the chance to match
              for l in self.lines:
                  for d in l.directives:
                      d.match(self.lines)
          
          
      
   .. py:method:: _accept_token(token)
   
      Checks if the token type may contain a directive.
   
      :param token: A pygments token
      :return: ``True`` if the token may contain a directive.
               ``False`` otherwise.
      
      ::
      
          def _accept_token(self, token):
              return True
          
          
      
CReader
=======
.. py:class:: CReader

   A reader for C/C++ code. This class inherits :py:class:`Reader`.
   
   ::
   
       class CReader(Reader):
           def _accept_token(self, token):
               return token in Token.Comment
           
           def _cut_comment(self, index, token, text):
               if text.startswith("/*"):
                   text = text[2:-2]
           
               elif text.startswith("//"):
                   text = text[2:]
       
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
       
                       if stext == '/*' or stext == "*/":
                           #remove """ and ''' from documentation lines
                           #see the l.text.lstrip()! if the lines ends with a white space
                           #the quotes will be kept! This is feature, to force the quotes
                           #in the output
                           continue
                       
                       if stext.startswith("//") and not stext.startswith("#####"):
                           #remove comments but not chapters
                           l.text = l.indented(stext[2:])
                                   
                   yield l
       
   
PythonReader
============
.. py:class:: PythonReader

   A reader for python code. This class inherits :py:class:`Reader`.
   To reduce the number of sentinels, the python reader does some more 
   sophisticated source parsing:
   
   A construction like::
     
         @cstart(foo)
         def foo(arg1, arg2):
            """ 
            Foo's documentation
            """ 
            code


   is replaced by::

         @cstart(foo)
         def foo(arg1, arg2):
            @start(foo doc)
            """ 
            Foo's documentation
            """ 
            @include(foo)
            @(foo doc)
            code


   The replacement will be done only:

     * If the doc string begins with """
     * If the block was started by a ``@rstart`` or ``@cstart`` directive
     * If there is no antiweb directive in the doc string.
     * Only a ``@cstart`` will insert the @include directive.


   Additionally the python reader removes all single line ``"""`` and ``'''``
   from documentation lines. In the following lines::
     
         @start(foo)
         """ 
         Documentation
         """ 

   The ``"""`` are automatically removed in the rst output. (see :py:meth:`filter_output`
   for details).


   
   ::
   
       class PythonReader(Reader):
           def __init__(self, lexer):
               super(PythonReader, self).__init__(lexer)
               self.doc_lines = []
                   
           <<PythonReader._post_process>>
           <<PythonReader._accept_token>>
           <<PythonReader._cut_comment>>
           <<PythonReader.filter_output>>
       # The keys are the lexer names of pygments
       readers = {
           "C" : CReader,
           "C++" : CReader,
           "C#" : CReader,
           "Python" : PythonReader,
       }
       
   
   .. py:method:: _post_process(fname, text)
   
      See :py:meth:`Reader._post_process`.
   
      This implementation *decorates* doc strings
      with antiweb directives.
      
      ::
      
          def _post_process(self, fname, text):
              #from behind because we will probably insert some lines
              self.doc_lines.sort(reverse=True)
          
              #handle each found doc string
              for start_line, end_line in self.doc_lines:
                  indents = set()
          
                  <<no antiweb directives in doc string>>
                  <<find the last directive before the doc string>>
          
                  if isinstance(last_directive, RStart):
                      <<decorate beginning and end>>
                      
                      if isinstance(last_directive, CStart):
                          <<insert additional include>>
          
              super(PythonReader, self)._post_process(fname, text)
          
      
      .. _no antiweb directives in doc string:
      
      **<<no antiweb directives in doc string>>**
      
      
      ::
      
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
          
      
      
      .. _find the last directive before the doc string:
      
      **<<find the last directive before the doc string>>**
      
      
      ::
      
          last_directive = None
          for l in reversed(self.lines[:start_line]):
              if l.directives:
                  last_directive = l.directives[0]
                  break
      
      
      .. _decorate beginning and end:
      
      **<<decorate beginning and end>>**
      
      
      ::
      
          l = self.lines[start_line]
          start = Start(start_line, last_directive.name + " doc")
          l.directives = list(l.directives) + [start]
          
          l = self.lines[end_line]
          end = End(end_line, last_directive.name + " doc")
          l.directives = list(l.directives) + [end]
      
      
      .. _insert additional include:
      
      **<<insert additional include>>**
      
      
      ::
      
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
      
          
      
   .. py:method:: _accept_token(token)
   
      See :py:meth:`Reader._accept_token`.
      
      ::
      
          def _accept_token(self, token):
              return token in Token.Comment or token in Token.Literal.String.Doc
          
          
      
   .. py:method:: filter_output(lines)
   
      See :py:meth:`Reader.filter_output`.
      
      ::
      
          def filter_output(self, lines):
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
                      
                      if stext.startswith("#") and not stext.startswith("#####"):
                          #remove comments but not chapters
                          l.text = l.indented(stext[1:])
                                  
                  yield l
          
      
   .. py:method:: _cut_comment(index, token, text)
   
      See :py:meth:`Reader._cut_comment`.
      
      ::
      
          def _cut_comment(self, index, token, text):
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
          
      


********
Document
********

Document
========

.. py:class:: Document(text, reader, fname, tokens)

   This is the mediator communicating with all other classes
   to generate rst output.
   :param string text: the source code to parse.
   :param reader: An instance of :py:class:`Reader`.
   :param string fname: The file name of the source code.
   :param tokens: A sequence of tokens usable for the ``@if`` directive.

   
   ::
   
       class Document(object):
           #Attributes
           <<Document.errors>>
           <<Document.blocks>>
           <<Document.blocks_included>>
           <<Document.compiled_blocks>>
           <<Document.sub_documents>>
           <<Document.tokens>>
           <<Document.macros>>
           <<Document.fname>>
           <<Document.reader>>
           <<Document.lines>>
           
           #Methods
           <<Document.__init__>>
           <<Document.process>>
           <<Document.get_subdoc>>
           <<Document.add_error>>
           <<Document.check_errors>>
           <<Document.collect_blocks>>
           <<Document.get_compiled_block>>
           <<Document.compile_block>>
       
       
   
   .. py:attribute:: errors
   
      A list of errors found during generation.
      
      ::
      
          errors = []
      
   .. py:attribute:: blocks
   
      A dictionary of all found blocks: Name -> List of Lines
      
      ::
      
          blocks = {}
      
   .. py:attribute:: blocks_included
   
      A set containing all block names that have been included by
      an @include directive.
      
      ::
      
          blocks_included = set()
      
   .. py:attribute:: compiled_blocks
   
      A set containing all block names that have been already
      compiled.
      
      ::
      
          compiled_blocks = set()
      
   .. py:attribute:: sub_documents
   
      A cache dictionary of sub documents, referenced by
      ``@include`` directives: Filename -> Document
      
      ::
      
          sub_documents = {}
      
   .. py:attribute:: tokens
   
      A set of token names that can be used for the ``@if`` directive.
      
      ::
      
          tokens = set()
      
   .. py:attribute:: macros
   
      A dictionary containing the macros that can be used
      by the ``@subst`` directive: Macro name -> substitution.
      
      ::
      
          macros = {}
      
   .. py:attribute:: fname
   
      The file name of the document's source.
      
      ::
      
          fname = ""
      
   .. py:attribute:: reader
   
      The instance of a :py:class:`Reader` object.
      
      ::
      
          reader = None
      
   .. py:attribute:: lines
   
      A list of :py:class:`Line` objects representing the whole documents
      split in lines.
      
      ::
      
          lines = []
      
   .. py:method:: __init__(text, reader, fname, tokens)
   
      The constructor.
      
      ::
      
          def __init__(self, text, reader, fname, tokens):
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
              
          
      
   .. py:method:: process(show_warnings)
   
      Processes the document and generates the output.
      :param bool show_warnings: If ``True`` warnings are emitted.
      :return: A string representing the rst output.
      
      ::
      
          def process(self, show_warnings):
              self.collect_blocks()
              if "" not in self.blocks:
                  self.add_error(0, "no @start() directive found (I need one)")
                  self.check_errors()
          
              try:
                  text = self.get_compiled_block("")
              finally:
                  self.check_errors()
          
              if show_warnings:
                  <<show warnings>>
          
              text = self.reader.filter_output(text)
              return "\n".join(map(operator.attrgetter("text"), text))
      
      .. _show warnings:
      
      **<<show warnings>>**
      
      
      ::
      
          self.blocks_included.add("")           #may not cause a warning
          self.blocks_included.add("__macros__") #may not cause a warning
          unincluded = set(self.blocks.keys())-self.blocks_included
          if unincluded:
              logger.warning("The following block were not included:")
              warnings = [ (self.blocks[b][0].index, b) for b in unincluded ]
              warnings.sort(key=operator.itemgetter(0))
              for l, w in warnings:
                  logger.warning("  %s(line %i)", w, l)
      
      
   .. py:method:: get_subdoc(rpath)
   
      Tries to compile a document with the relative path rpath.
      :param string rpath: The relative path to the root
      containing document.
      :return: A :py:class:`Document` reference to the sub document.
      
      ::
      
          def get_subdoc(self, rpath):
              <<return from cache if possible>>
              <<insert macros function>>
              <<read the source file>>
                  
              self.sub_documents[rpath] = doc
              return doc
          
      
      .. _return from cache if possible:
      
      **<<return from cache if possible>>**
      
      
      ::
      
          try:
              return self.sub_documents[rpath]
          except KeyError:
              pass
          
      
      
      .. _insert macros function:
      
      **<<insert macros function>>**
      
      
      ::
      
          def insert_macros(subdoc):
              #if sub doc has no macros insert mine
              if ("__macros__" not in subdoc.blocks
                  and "__macros__" in self.blocks):
                  file_ = subdoc.macros["__file__"] # preserve __file__
                  subdoc.macros.update(self.macros)
                  subdoc.macros["__file__"] = file_
          
      
      
      .. _read the source file:
      
      **<<read the source file>>**
      
      
      ::
      
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
              reader = readers.get(lexer.name, Reader)(lexer)
              doc = Document(text, reader, rpath, self.tokens)
              doc.collect_blocks()
              insert_macros(doc)
      
      
   .. py:method:: add_error(line, text)
   
      Adds an error to the list.
      :param integer line: The line number that causes the error.
      :param string text: An error text.
      
      ::
      
          def add_error(self, line, text):
              self.errors.append((self.lines[line], text))
          
          
      
   .. py:method:: check_errors()
   
      Raises a ``WebError`` exception if error were found.
      
      ::
      
          def check_errors(self):
              if self.errors:
                  raise WebError(self.errors)
          
      
   .. py:method:: collect_blocks()
   
      Collects all text blocks.
      
      ::
      
          def collect_blocks(self):
              blocks = [ d.collect_block(self, i)
                         for i, l in enumerate(self.lines)
                         for d in l.directives ]
             
              self.blocks = dict(list(filter(bool, blocks)))
          
              if "__macros__" in self.blocks:
                  self.get_compiled_block("__macros__")
          
          
      
   .. py:method:: get_compiled_block(name)
   
      Returns the compiled version of a text block.
      Compiled means: all directives where processed.
      :param string name: The name of the text block:
      :return: A list of :py:class:`Line` objects representing
      the text block.
      
      
      ::
      
          def get_compiled_block(self, name):
              if name not in self.blocks:
                  return None
              
              if name in self.compiled_blocks:
                  return self.blocks[name]
                  
              return self.compile_block(name, self.blocks[name])
          
          
      
   .. py:method:: compile_block(name, block)
   
      Compiles a text block.
      :param string name: The name of the block
      :param block: A list of :py:class:`Line` objects representing
      the text block to compile.
      :return: A list of :py:class:`Line` objects representing
      the compiled text block.
   
      
      ::
      
          def compile_block(self, name, block):
              <<find_next_directive>>
          
              while True:
                  directive_index = find_next_directive(block)
                  if not directive_index: break
                  directive, index = directive_index
                  directive.process(self, block, index)
          
              self.compiled_blocks.add(name)
              return block
      
      .. _find_next_directive:
      
      **<<find_next_directive>>**
      
      
      ::
      
          def find_next_directive(block):
              # returns the next available directive
              min_line = [ (l.directives[0].priority, i)
                           for i, l in enumerate(block) if l.directives ]
              if not min_line:
                  return None
          
              prio, index = min(min_line)
              return block[index].directives.pop(0), index
      
      
Line
====
.. py:class:: Line(fname, index, text[, directives[, type]])

   This class represents a text line.
   
   ::
   
       class Line(object):
           #Attributes
           <<Line._directives>>
           <<Line.fname>>
           <<Line.index>>
           <<Line.text>>
           <<Line.type>>
       
           #Methods
           <<Line.__init__>>
           <<Line.set>>
           <<Line.like>>
           <<Line.indented>>
           <<Line.change_indent>>
           <<Line.__len__>>
           <<Line.__repr__>>
       
           #Properties
           <<Line.indent>>
           <<Line.sindent>>
           <<Line.directives>>
           <<Line.directive>>
   
   .. py:attribute:: _directives
   
      A list of :py:class:`Directive` objects, sorted
      by their priority.
      
      ::
      
          _directives = ()
      
   .. py:attribute:: fname
   
      A string of the source's file name the line belongs to.
      
      ::
      
          fname = ""
      
   .. py:attribute:: index
   
      The integer line index of the directive within the current block.
      
      ::
      
          index = 0
      
   .. py:attribute:: text
   
      A string containing the source line.
      
      ::
      
          text = ""
      
   .. py:attribute:: type
   
      A char representing the line type:
   
        * ``d`` stands for a document line
        * ``c`` stands for a code line
      
      ::
      
          type = "d"
      
   .. py:attribute:: indent
   
   An integer representing the line's indentation.
   
   ::
   
       @property
       def indent(self):
           return len(self.text)-len(self.text.lstrip())
       
       
   
   .. py:attribute:: sindent
   
   A string representation of the line's indentation.
   
   ::
   
       @property
       def sindent(self):
           return " "*self.indent
       
       
   
   .. py:attribute:: directives
   
   A sorted sequence of :py:class:`Directive` objects.
   
   ::
   
       @property
       def directives(self):
           return self._directives
       
       
       @directives.setter
       def directives(self, value):
           self._directives = value[:]
           if self._directives:
               self._directives.sort(key=operator.attrgetter("priority"))
       
       
   
   .. py:attribute:: directive
   
      The first of the contained :py:class:`Directive` objects.
      
      ::
      
          @property
          def directive(self):
              return self.directives and self.directives[0]
          
          
      
   .. py:method:: __init__(name, index, text[, directives[, type]])
   
      The constructor.
      
      ::
      
          def __init__(self, fname, index, text, directives=(), type='d'):
              self.fname = fname
              self.index = index
              self.text = text
              self.directives = directives
              self.type = type
          
          
      
   .. py:method:: set([index=None[, type=None[, directives=None]]])
   
      Changes the attributes :py:attr:`index`, :py:attr:`type`
      and :py:attr:`directives` at once.
   
      :param integer index: the line index.
      :param char type: Either ``'d'`` or ``'c'``.
      :param list directives: A list of :py:class:`DCirective` objects.
      :return: The :py:class:`Line` object ``self``.
      
      ::
      
          def set(self, index=None, type=None, directives=None):
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
          
          
      
   .. py:method:: like(text)
   
      Clones the Line with a different text.
      
      ::
      
          def like(self, text):
              return Line(self.fname, self.index, self.indented(text))
          
          
      
   .. py:method:: indented(text)
   
      Returns the text, with the same indentation as ``self``.
      
      ::
      
          def indented(self, text):
              return self.sindent + text
          
      
   .. py:method:: change_indent(delta)
   
      Changes the lines indentation.
      
      ::
      
          def change_indent(self, delta):
              if delta < 0:
                  delta = min(-delta, self.indent)
                  self.text = self.text[delta:]
          
              elif delta > 0:
                  self.text = " "*delta + self.text
          
              return self
          
      
   .. py:method:: __len__()
   
      returns the length of the stripped :py:attr:`text`.
      
      ::
      
          def __len__(self):
              return len(self.text.strip())
              
          
      
   .. py:method:: __repr__()
   
      returns a textual representation of the line.
      
      ::
      
          def __repr__(self):
              return "Line(%i, %s, %s)" % (self.index, self.text, str(self.directives))
      


***********
File Layout
***********


::

    
    <<imports>>
    <<management>>
    <<directives>>
    <<readers>>
    
    
    <<Line>>
    <<document>>
    
    def write_static(input_type, index_rst, startblock, endblock):
        index_static = "Documentation\n=======================\nContents:\n\n.. toctree::\n   :maxdepth: 2\n\n   " + startblock +"\n   " + endblock
        index_out = open(os.path.join(input_type, index_rst), "w")
        index_out.write(index_static)
    
    def main():
        parser = OptionParser("usage: %prog [options] SOURCEFILE",
                              description="Tangles a source code file to a rst file.",
                              version="%prog " + __version__)
    
        parser.add_option("-o", "--output", dest="output", default="",
                          type="string", help="The output filename")
    
        parser.add_option("-t", "--token", dest="token", action="append",
                          type="string", help="defines a token, usable by @if directives")
    
        parser.add_option("-w", "--warnings", dest="warnings",
                          action="store_false", help="suppresses warnings")
        
    if __name__ == "__main__":
        main()
    
    
    



<<imports>>
===========

::

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
    import collections
    from sys import platform as _platform
    



<<management>>
==============


::

    
    __version__ = "0.3.1"
    
    logger = logging.getLogger('antiweb')
    
    class WebError(Exception):
        def __init__(self, error_list):
            self.error_list = error_list
    



<<directives>>
==============


::

    
    <<Directive>>
    <<NameDirective>>
    <<Start>>
    <<RStart>>
    <<CStart>>
    <<End>>
    <<Fi>>
    <<If>>
    <<Define>>
    <<Enifed>>
    <<Subst>>
    <<Include>>
    <<RInclude>>
    <<Edoc>>
    <<Code>>
    <<Ignore>>
    <<Indent>>
    
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
    


.. _readers:


<<readers>>
===========


::

    
    <<Reader>>
    <<CReader>>
    <<PythonReader>>



<<document>>
============


::

    
    <<Document>>
    <<generate>>



****************************************
Multi-File Processing and Sphinx Support
****************************************

There are two new flags in antiweb:

* The ''-r'' flag:
    * antiweb will search for all compatible files to process them

* The ''-i'' flag:
    * Sphinx' index.rst will be edited to contain all processed files (empty files will be ignored)


::

    
        parser.add_option("-r", "--recursive", dest="recursive",
                          action="store_true", help="Process every file in given directory")
        
        parser.add_option("-i", "--index", dest="index",
                          action="store_true", help="Automatically write file(s) to Sphinx' index.rst")
    

    options, args = parser.parse_args()

    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    if options.warnings is None:
        options.warnings = True
    
    if not args:
        parser.print_help()
        sys.exit(0)

    index_rst = "index.rst"
    replace_text = ""
    startblock = ".. @start(generated)"
    endblock = ".. @(generated)"
The program will check if a -r flag was given and if so, save the current directory and change it to the given one


::

    
        if options.recursive:
            previous_dir = os.getcwd()
            os.chdir(args[0])
            if options.output:
                os.makedirs(os.path.join(args[0], options.output), exist_ok=True)
            if options.index:
                if options.output:
                    in_type = os.path.join(args[0], options.output)
                    if not os.path.isfile(os.path.join(in_type, index_rst)):
                        write_static(in_type, index_rst, startblock, endblock)
    
                    content, startline = search_for_generate(options.output, index_rst, startblock, endblock)
    
                else:
                    in_type = args[0]
                    if not os.path.isfile(os.path.join(in_type, index_rst)):
                        write_static(in_type, index_rst, startblock, endblock)
    
                    content, startline = search_for_generate(os.getcwd(), index_rst, startblock, endblock)

The program lists all files in the directory and sub-directories to prepare them for the process


::

    
            for root, dirs, files in os.walk(args[0], topdown=False):
                for filename in files:
                    fname = os.path.join(root, filename)
    

If the found file is no folder nor a rst file, it will be put into the process


::

                    ext_tuple = (".cs",".cpp",".py",".cc")
                    if os.path.isfile(fname) and fname.endswith(ext_tuple):
                        if options.index:
                            write(os.getcwd(), fname, options.output, options.token, options.warnings, options.index, index_rst, options.recursive, content, startblock, endblock, startline)
                        else:
                            write(os.getcwd(), fname, options.output, options.token, options.warnings, options.index, index_rst, options.recursive, None, startblock, endblock, None)

This else will take place when the -r flag is not given.


::

    
        else:
            os.chdir(os.path.split(args[0])[0])
            if options.index:
                if not os.path.isfile(os.path.join(os.getcwd(), index_rst)):
                    write_static(os.getcwd(), index_rst, startblock, endblock)
                content, startline = search_for_generate(None, index_rst, startblock, endblock)
                write(os.getcwd(), args[0], options.output, options.token, options.warnings, options.index, index_rst, options.recursive, content, startblock, endblock, startline)
            else:
                write(os.getcwd(), args[0], options.output, options.token, options.warnings, options.index, index_rst, options.recursive, None, startblock, endblock, None)

Writing the index.rst file
==========================

From the given file a .rst file will be created if it contains an antiweb :py:class:`start() directive`


::

    
    def write(path, fname, output, token, warnings, index, index_rst, recursive, content, startblock, endblock, startline):
    

When there is no output given there are two possibilities: recursive or not recursive. The file path gets split up and put together so it can be processed by ''process_file''

::

    
            if not output:
                if recursive:
                    out_file_name = os.path.splitext(fname)[0] + ".rst"
                    out_file = out_file_name
                    out_file_name = os.path.relpath(out_file_name, path)
                else:
                    out_file = os.path.splitext(fname)[0] + ".rst"
                    out_file_name = os.path.split(out_file)[1]
    
There is an output given, so it can also be either recursive or not recursive. With the additional output parameter the file path gets split up and put together so it can be processed by ''process_file''. There is also a differentiation between Linux, Windows and OS X (because of the different paths in each operating system)

::

    
            else:
                if recursive:
                    rel_path = os.path.relpath(fname, path)
                    out_file_name = os.path.splitext(rel_path)[0] + ".rst"
                    if _platform == "linux" or _platform == "linux2":
                        out_file_name = out_file_name.replace("/","_")
                    if _platform == "win32":
                        out_file_name = out_file_name.replace("\\","_")
                    out_file = os.path.join(path, output, out_file_name)
                else:
                    out_file_name = output + ".rst"
                    out_file = os.path.join(path, out_file_name)
The prepared file path gets pushed to ''process file''. If the process is successful, ''could_process'' is set to ''True''.

::

    
            could_process = process_file(fname, out_file, token, warnings)
    


If the user added the -i flag, the file gets added to Sphinx' index.rst file. Between the :py:class:`start(generated)` and :py:class:`(generated)` directives is the space for automatic added files, you can manually add files below the @(generated) directive.


::

    
            if index:
                if could_process:
                    
                    if output and recursive:
                        replace_in_generated(startblock, endblock, out_file_name, path, output, index_rst, content, startline)
                    else:
                        replace_in_generated(startblock, endblock, out_file_name, path, None, index_rst, content, startline)






process_file
============

If no output name was declared, the input name will be given


::

    
    def process_file(in_file, out_file, token, warnings):
    

The output text will be written in the output file. If there is an output text, the function returns could_write as True


::

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



search_for_generated
====================

The line numbers of the :py:class:`start(generated)` and :py:class:`(generated)` directive are looked up and their content getting depleted


::

    
    def search_for_generate(output, index_rst, startblock, endblock):
    
        startline = None
        endline = None
        content = ""
        if not output:
            output = ""
    
        while startline == None or endline == None:
            path = os.path.join(os.getcwd(), output, index_rst)
            with open(path, "r") as index_file:
                for num, line in enumerate(index_file):
                    if startblock in line:
                        startline = num
                    if endblock in line:
                        endline = num
    
                if startline== None or endline== None:
                    write_static(os.path.join(os.getcwd(), output), index_rst, startblock, endblock)
                else:
                    index_file.seek(0, 0)
                    content = index_file.readlines()
                    del content[startline+1:endline]
        return (content, startline)


replace_in_generated
====================

The name of the generated files get added between the :py:class:`start(generated)` and :py:class:`(generated)` directives. Code before and after is left as is.


::

    
    def replace_in_generated(startblock, endblock, out_file_name, path, output, index_rst, content, startline):
    
        if startline:
            endline = startline+1
        
        index_var = os.path.splitext(out_file_name)[0]
        if startline and endline:
            content.insert(endline, "   " + index_var + "\n")
        if output:
            index_out = open(os.path.join(path, output, index_rst), "w")
        else:
            index_out = open(os.path.join(path, index_rst), "w")
        for item in content:
            index_out.write(item)
        index_out.close()
    









************************
How to add new languages
************************

New languages are added by writing a new Reader class
and registering it in the readers dictionary (see readers).
A simple Reader example is provides by :py:class:`CReader`
a more advances reader is :py:class:`PythonReader`.




