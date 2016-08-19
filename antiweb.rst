.. default-domain:: python

.. highlight:: python3
   :linenothreshold: 4

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
            #get the language specific comment markers based on the pygments lexer name
            single_comment_markers,  block_comment_markers = get_comment_markers(lexer.name)
            #initialise a new Reader based on the pygments lexer name 
            reader = readers.get(lexer.name, Reader)(lexer, single_comment_markers,  block_comment_markers)
               
            document = Document(text, reader, fname, tokens)
            return document.process(show_warnings, fname)
    


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

*******
Readers
*******

Readers are responsible for the language dependent
source parsing.

Reader
=============
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
   
   .. py:method:: __init__(lexer, single_comment_markers, block_comment_markers)
       
      The constructor initialises the language specific pygments lexer and comment markers. 
      
      :param Lexer lexer: The language specific pygments lexer.
      :param string[] single_comment_markers: The language specific single comment markers.
      :param string[] block_comment_markers: The language specific block comment markers.
      
      ::
      
          def __init__(self, lexer, single_comment_markers, block_comment_markers):
              self.lexer = lexer
              self.single_comment_markers = single_comment_markers
              self.block_comment_markers = block_comment_markers
          
      
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
      
          def _cut_comment(self, index, token, text):
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
=============
.. py:class:: CReader

   A reader for C/C++ code. This class inherits :py:class:`Reader`.
   
   ::
   
       
       class CReader(Reader):
       
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
   
   
CSharpReader
=============
.. py:class:: CSharpReader

   A reader for C# code. This class inherits :py:class:`CReader`.
   The CSharpReader is needed because C# specific output filtering is applied.
   Compared to C, C# uses XML comments starting with *///* which are reused
   for the final documentation. Here you can see an overview of the CSharpReader class
   and its methods.
   

   
   ::
   
       
       
       class CSharpReader(CReader):
           
           default_xml_block_index = -1
           
           def __init__(self, lexer,  single_comment_markers,  block_comment_markers):
               #the call to the base class CReader is needed for initialising the comment markers
               super(CSharpReader, self).__init__(lexer,  single_comment_markers,  block_comment_markers)
                   
           <<CSharpReader.strip_tags>>
           <<CSharpReader.get_attribute_text>>
           <<CSharpReader.get_stripped_xml_lines>>
           <<CSharpReader.create_new_lines>>
           <<CSharpReader.init_xml_block>>
           <<CSharpReader.filter_output>>
   
   .. py:method:: strip_tags(tags)
   
      Removes all C# XML tags. The tags are replaced by their attributes and contents.
      This method is called recursively. This is needed if the content of a tag also contains
      tags.
      
      Examples:
      
       * ``<param name="arg1">value</param>`` will be stripped to : *"arg1 value"*
       * ``<para>Start <see cref="(String)"/> end</para>`` will be stripped to : *"Start (String) end"*
   
      :param Tag tags: The parsed xml tags.
      :return: the XML tags replaced by their attributes and contents.
      
      ::
      
          def strip_tags(self,  tags):
              
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
      
      
   .. py:method:: get_attribute_text(tag)
   
      Returns the values of all XML tag attributes seperated by whitespace.
   
      Examples:
       
       * ``<param name="arg1">parameterValue</param>`` returns : *"arg1 "*
       * ``<include file='file1' path='[@name="test"]/*' />`` returns: *"file1 [@name="test"]/* "*
   
      :param Tag tag: A BeautifulSoup Tag.
      :return: the values of all attributes concatenated
      
      ::
      
          def get_attribute_text(self,  tag):
              #collect all values of xml tag attributes
              attributes = tag.attrs
              attribute_text = ""
              for attribute, value in attributes.items():
                  attribute_text = value + " "
              return attribute_text
      
      
   .. py:method:: get_stripped_xml_lines(xml_lines_block)
   
      Removes all XML comment tags from the lines in the xml_lines_block.
      
      :param Line[] xml_lines_block: A list containing all Line object which belong to an XML comment block.
      :return: A list of all stripped XML lines.
      
      ::
      
          def get_stripped_xml_lines(self,  xml_lines_block):
              #the xml_lines_block contains Line objects. As the xml parser expects a string 
              #the Line obects have to be converted to a string.
              xml_text = "\n".join(map(operator.attrgetter("text"), xml_lines_block))
              
              #the xml lines will be parsed and then all xml tags will be removed       
              xml_tags = BeautifulSoup(xml_text, "html.parser")
              self.strip_tags(xml_tags)
              stripped_xml_lines = xml_tags.text.splitlines()
              return stripped_xml_lines
      
      
   .. py:method:: create_new_lines(stripped_xml_lines, index, initial_line)
   
      This method is called after all XML comment tags are stripped. For each new 
      line in the stripped_xml_lines a new Line object is created.
      
      :param string[] stripped_xml_lines: The comment lines were the XML tags have been stripped.
      :param int index: The starting index for the new line object.
      :param Line initial_line: The first line of the xml comment block. Its indentation will be used for all new created lines.
      :return: A generator containing the lines which have been created out of the stripped_xml_lines.
      
      ::
      
          def create_new_lines(self, stripped_xml_lines, index, initial_line):
              for line in stripped_xml_lines:
                  new_line = Line(initial_line.fname,  index,  initial_line.indented(line.lstrip()))
                  index += 1
                  yield new_line
      
      
   .. py:method:: init_xml_block()
   
      Inits the variables which are needed for collecting an XML comment block.
      
      ::
      
          def init_xml_block(self):
              xml_lines_block = []
              xml_start_index = self.default_xml_block_index
              return xml_lines_block,  xml_start_index
      
      
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
      
      ::
      
          def filter_output(self, lines):
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
           def __init__(self, lexer,  single_comment_markers,  block_comment_markers):
               super(PythonReader, self).__init__(lexer,  single_comment_markers,  block_comment_markers)
               self.doc_lines = []
                   
           <<PythonReader._post_process>>
           <<PythonReader._accept_token>>
           <<PythonReader._cut_comment>>
           <<PythonReader.filter_output>>
       # The keys are the lexer names of pygments
       readers = {
           "C" : CReader,
           "C++" : CReader,
           "C#" : CSharpReader,
           "Python" : PythonReader,
           "Clojure" : ClojureReader,
           "rst" : CReader,
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
                      
                      if stext.startswith("#"):
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
          
      
ClojureReader
=============
.. py:class:: ClojureReader

   A reader for Clojure code. This class inherits :py:class:`Reader`.
   
   ::
   
       class ClojureReader(Reader):
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
   
GenericReader
=============
.. py:class:: GenericReader

   A generic reader for languages with single line and block comments . 
   This class inherits :py:class:`Reader`.
   
   ::
   
       class GenericReader(Reader):
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
       
       
   
rstReader
=============
.. py:class:: rstReader

   A reader for rst code. This class inherits :py:class:`Reader`.
   
   ::
   
       class rstReader(Reader):
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
      


***********
File Layout
***********


::

    
    <<imports>>
    <<management>>
    <<readers>>
    
    
    <<Line>>
    <<document>>
    
    
    
    
    <<create_out_file_name>>
    
    <<create_out_file_name_index>>
    
    
    <<insert_filename_in_index_file>>
    
    <<create_doc_directory>>
    
    
    <<replace_path_seperator>>
    
    
    <<write_static>>
    
    <<create_index_file>>
     
    <<parsing>>
        
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

The program checks if a -r flag was given and if so, save the current directory and change it to the given one.


::

    
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
                        

The program walks through the given directory and all subdirectories. The absolute file names 
are retrieved. Only files with the allowed extensions are processed.


::

    
            #Only files with the following extensions will be processed
            ext_tuple = (".cs",".cpp",".py",".cc", ".rst")
    
            for root, dirs, files in os.walk(directory, topdown=False):
                for filename in files:
                    fname = os.path.join(root, filename)
            
                    if os.path.isfile(fname) and fname.endswith(ext_tuple):
                        write(directory, fname, options, index_rst, start_block, end_block)
    

This else will take place when the -r flag is not given.


::

    
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


Writing the documentation files
===============================

From the given file a .rst file will be created if it contains an antiweb :py:class:`start() directive`.
The following function is called for the creation of the documentation files.

.. py:method:: write(working_dir, input_file, options, index_file, start_block, end_block)
    
   Creates the corresponding documention file and optionally adds the processed file to the index file.
           
   :param working_dir: Current working directory.
   :param input_file: Contains the absolute path of the currently processed file.
   :param options: Commandline options.
   :param index_file: Absolute path of the index file.
   :param start_block: String which contains the generated index block start definition.
   :param end_block: String which contains the generated index block end definition.

Before the input file is processed the name of the output file has to be computed. 
How the output file name is created depends on the different commandline options.
When there is no output option given the output file name is created in the following way:

.. csv-table::
   :header: "Input File", "Output File"

   ``C:\antiweb\testing.cs``, *C:\\antiweb\\testing.rst*
   ``C:\antiweb\testing.rst``, *C:\\antiweb\\testing_docs.rst*


::

    def write(working_dir, input_file, options, index_file, start_block, end_block):
    
        output = options.output
        recursive = options.recursive
        
        if not output:
            out_file = create_out_file_name(working_dir, "", input_file)
    

If there is an output given, we have to distinguish between the recursive and non-recursive option.
When the recursive option is used in combination with the output option, the output parameter is treated as the documentation directory:

.. csv-table::
   :header: "Input File", "Output File"

   ``C:\antiweb\ -r -o report.rst``,*C:\\antiweb\\report.rst\\file.rst*
   ``C:\antiweb\ -r -o report``,*C:\\antiweb\\report\\file.rst*
   ``C:\antiweb\ -r -o C:\antiweb\report.rst``,*C:\\antiweb\\report.rst\\file.rst*
   ``C:\antiweb\ -r -o \..\report.rst``,*C:\\report.rst\\file.rst*


::

        else:           
            if recursive:
                #The output parameter is treated as a directory.
                #If it is a relative path it is combined with the current working directory.
                directory = output
                out_file = create_out_file_name(working_dir,directory,input_file)

When the output option is used without the recursive option the output file name is computed in the following way: 

.. csv-table::
   :header: "Input File", "Output File"

   ``C:\antiweb\testing.cs -o report.rst``,*C:\\antiweb\\report.rst*
   ``C:\antiweb\testing.cs -o report``,*C:\\antiweb\\report\\testing.rst*
   ``C:\antiweb\testing.cs -o \..\report``,*C:\\report\\testing.rst*
   ``C:\antiweb\testing.cs -o report\report.rst``,*C:\\antiweb\\report\\report.rst*
   ``C:\antiweb\testing.cs -o report\report.rst\``,*C:\\antiweb\\report\\report.rst\\testing.rst*
   ``C:\antiweb\testing.cs -o C:\report\report.rst``,*C:\\report\\report.rst*


::

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

Now the input file is processed and the corresponding documentation file is created.
If processing is successful, ''could_process'' is set to ''True''.


::

    
        could_process = process_file(input_file, out_file, options.token, options.warnings)
        

If the file was processed successfully and the index option is used, the file name which should be inserted
in the generated index file block has to be computed first. Afterwards the file name is inserted into the 
index file (see :py:meth:`insert_filename_in_index_file`).


::

        if options.index and could_process:
            out_file_name_index = create_out_file_name_index(out_file, working_dir, recursive)
            insert_filename_in_index_file(out_file_name_index, index_file, start_block, end_block)





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
    
.. csv-table::
   :header: "Working_Dir", "Directory", "Input_File_Name", "Output_File_Name"

   *C:\\antiweb\\*,doc, *C:\\antiweb\\testing.py* , *C:\\antiweb\\doc\\testing.rst*
   *C:\\antiweb\\* , , *C:\\antiweb\\testing.py* , *C:\\antiweb\\testing.rst*
   *C:\\antiweb\\* ,*C:\\doc\\* , *testing.py*, *C:\\doc\\testing.rst*
   *C:\\antiweb\\*,doc, *C:\\antiweb\\testing.rst* , *C:\\antiweb\\doc\\testing_docs.rst*


::

    
    def create_out_file_name(working_dir, directory, input_file):
    
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
        

.. py:method:: create_out_file_name_index(out_file, working_dir, recursive)
   
  Creates the file name which should be inserted into the generated index file block.
  
  :param out_file: Absolute path of the output file.
  :param index_file: Absolute path of the index file.
  :param recursive: Boolean which indicates whether the recursive commandline options is used.
  :return: The file name which should be inserted in the generated index file block.
    
If the user added the -i flag, an index file (documentation base file) is created which contains all processed files.
The names of the processed files are added between the :py:class:`start(generated)` and :py:class:`end(generated)` directives.
The file names which are inserted into the index file are computed in the following way: 

When the recursive option is used the file name in the index file is a relative path without extension. 
Otherwise the index file will only contain the filename without extension. 
Path seperator characters are replaced by "_".

| Non-recursive example with current processed file: *C:\\antiweb\\report.rst\\file.rst*:
| :py:class:`start(generated)`
| :py:class:`file`
| :py:class:`end(generated)`
|
| Recursive example with current processed file: *C:\\antiweb\\report.rst\\file.rst*:
| :py:class:`start(generated)`
| :py:class:`report.rst_file`
| :py:class:`end(generated)`
|


::

    
    def create_out_file_name_index(out_file, working_dir, recursive):
    
        #1) Obtain only the file name
        out_file_name_index = os.path.split(out_file)[1]
        #2) Remove the extension
        out_file_name_index = os.path.splitext(out_file_name_index)[0]
        if recursive:
            out_file_name_index = os.path.relpath(out_file_name_index, working_dir)
            out_file_name_index = replace_path_seperator(out_file_name_index)
            
        return out_file_name_index
        

.. py:method:: insert_filename_in_index_file(file_name, index_file, start_block, end_block)
   
  Inserts the given file name into the generated block in the index file.
  
  :param file_name: The file name which should be inserted into the index file.
  :param index_file: Absolute path of the index file.
  :param start_block: String which contains the generated index block start definition.
  :param end_block: String which contains the generated index block end definition.

If the user added the -i flag, an index file (documentation base file) is created which contains all processed files.
Between the :py:class:`start(generated)` and :py:class:`end(generated)` directives the names of the processed files are added.
Read  :py:meth:`create_out_file_name_index` for more information about how the inserted file name is computed.
Files can be manually added after the :py:class:`end(generated)` directive.


::

    
    def insert_filename_in_index_file(file_name, index_file, start_block, end_block):
        
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
    

.. py:method:: create_doc_directory(out_file)
    
   Creates the documentation directory if it does not yet exist.
   If an error occurs, the program exits.
           
   :param out_file: The path to the output file.

::

    
    def create_doc_directory(out_file):
        try:
            out_file_directory = os.path.split(out_file)[0]       
            if not os.path.exists(out_file_directory):
                os.makedirs(out_file_directory)
        except IOError:
            logger.error("\nError: Documentation Directory: %s could not be created",  out_file_directory)
            sys.exit(1)

.. py:method:: replace_path_seperator(file_path)
    
   Replaces OS specific path seperator characters by '_'.
           
   :param file_path: The path to a file.

::

    
    def replace_path_seperator(file_path):
    #Path seperator characters are replaced by "_" in the index file
        if _platform == "linux" or _platform == "linux2":
            file_path = file_path.replace("/","_")
        if _platform == "win32":
            file_path = file_path.replace("\\","_")      
        return file_path

.. py:method:: write_static(index_file, start_of_block, end_of_block)
    
   Writes the static contents to the index file.
           
   :param index_file: Absolute path of the index file.
   :param start_block: String which contains the generated index block start definition.
   :param end_block: String which contains the generated index block end definition.

::

    
    def write_static(index_file, start_block, end_block):
    
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
            

.. py:method:: create_index_file(working_dir, directory, file_name, start_block, end_block)
    
   Creates the index file and writes the standard index file contents into the file.
   
   :param working_dir: Current working directory. 
   :param directory: Output directory (may contain a directory path or a directory name)           
   :param file_name: Filename of the index file.
   :param start_block: String which contains the generated index block start definition.
   :param end_block: String which contains the generated index block end definition.
   :return: The absolute path of the index file.

::

    def create_index_file(working_dir, directory, file_name, start_block, end_block):
        
        index_file = os.path.join(working_dir, directory, file_name)
        index_file_absolute = os.path.abspath(index_file)
        
        #index file is overwritten if it already exists
        write_static(index_file_absolute, start_block, end_block)
        
        return index_file

process_file
============

If no output name was declared, the input name will be given


::

    
    def process_file(in_file, out_file, token, warnings):
    

The output text will be written in the output file. If there is an output text, the function returns could_write as True.


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



search_for_generated_block
============================

The index file is searched for the generated block. The contents in the generated block are deleted.
Afterwards the whole file content and the endline of the generated block are returned.


::

    
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


.. py:method:: def parsing()

   All possible input options are being defined, as well as their help-message, type and variable the values are stored in.
   If no arguments are given (the user did not provide a filepath), the current directory is set as the argument.

::

    def parsing():
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
    from sys import platform as _platform
    from bs4 import BeautifulSoup,  Tag,  NavigableString
    
    from antiweb.directives import *
    



<<management>>
==============


::

    
    __version__ = "0.3.2"
    
    logger = logging.getLogger('antiweb')
    
    class WebError(Exception):
        def __init__(self, error_list):
            self.error_list = error_list
    


.. _readers:


<<readers>>
===========


::

    
    <<Reader>>
    <<CReader>>
    <<CSharpReader>>
    <<ClojureReader>>
    
    <<GenericReader>>
    <<rstReader>>
    <<PythonReader>>



<<document>>
============


::

    
    <<Document>>
    <<generate>>
    
    <<get_comment_markers>>



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

Language specific comment markers
====================================
If a new language is added, its comment markers also have to be registered in the following map.
The map contains the definition of all language specific comment markers.

The comment markers of a language are defined in the format:
``"language" : ([single_comment_tokens],[start_block_token, end_block_token])``

Multiple single and block comment markers can be defined.


::

    comments = {
    "C" : (["//"],(["/*","*/"])),
    "C++" : (["//"],(["/*","*/"])),
    "C#" : (["//"],(["/*","*/"])),
    "Python" : (["#"],(["'''","'''"],["\"\"\"","\"\"\""])),
    }

From the map above the comment markers are retrieved via the following method:

..  py:function:: get_comment_markers(lexer_name)

    Retrieves the language specific comment markers from the comments map.
    The comment markers of C serves as the default comment markers if the lexer name cannot be found.

    :param string lexer_name: The name of the pygments lexer.
    :return: The single and comment block markers defined by the language                           
    
    ::
    
        
        def get_comment_markers(lexer_name):
            comment_markers = comments.get(lexer_name, comments["C"])
            single_comment_markers = comment_markers[0]
            block_comment_markers = comment_markers[1]
            return single_comment_markers,  block_comment_markers  
        
    

*******
Example
*******

See the :ref:`antiweb` source as an advanced example.

