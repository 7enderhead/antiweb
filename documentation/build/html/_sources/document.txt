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
       
           def process(self, show_warnings, fname):
               self.collect_blocks()
               
               # check if there are any lines in the file and add the according error message
               if not self.lines:
                   self.add_error(0, "empty file", fname)
                   self.check_errors()
               elif "" not in self.blocks and not fname.endswith(".rst"):
                   self.add_error(0, "no @start() directive found (I need one)")
                   self.check_errors()       
           
               try:
                   text = self.get_compiled_block("")
               finally:
                   self.check_errors()
           
               if show_warnings:
                   <<show warnings>>
               text = self.reader.filter_output(text)
               return_text = None
               if text:
                    return_text = "\n".join(map(operator.attrgetter("text"), text))
               return return_text
       
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
              # if sub doc has no macros insert mine
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
              single_comment_markers,  block_comment_markers = get_comment_markers(lexer.name)    
              reader = readers.get(lexer.name, Reader)(lexer, single_comment_markers,  block_comment_markers)
          
              doc = Document(text, reader, rpath, self.tokens)
              doc.collect_blocks()
              insert_macros(doc)
      
      
   .. py:method:: add_error(line, text)
   
      Adds an error to the list.
      :param integer line_number: The line number that causes the error.
      :param string text: An error text.
      :param string fname: name of currently processed file (needed if no data in self.lines)
      
      
      ::
      
          def add_error(self, line_number, text, fname=""):
              # determine if access to line_number is possible
              if line_number < len(self.lines):
                  line = self.lines[line_number]
              else:
                  # without a line in self.lines, antiweb would crash on appending it to the errors (errorlist)
                  # we add a 'fake line' to prevent that issue
                  line = Line(fname, -1, "")
                  
              self.errors.append((line, text))
          
          
      
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
      