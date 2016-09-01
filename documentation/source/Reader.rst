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

         @subst(_at_)cstart(foo)
         def foo(arg1, arg2):
            Foo's documentation
            code


   is replaced by::

         @subst(_at_)cstart(foo)
         def foo(arg1, arg2):
            @subst(_at_)start(foo doc)
            Foo's documentation
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
         Documentation

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
   
RstReader
=============
.. py:class:: RstReader

   A reader for rst code. This class inherits :py:class:`Reader`.
   
   ::
   
       class RstReader(Reader):
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
   
The Reader Dictionary
=====================
When writing a new reader, please register it in this dictionary with the according lexer name of the file. Please note that the Readername is the name of the class, not the file.

Format:


::

     "lexername" : Readername,


::

    
    readers = {
        "C" : CReader,
        "C++" : CReader,
        "C#" : CSharpReader,
        "Python" : PythonReader,
        "Clojure" : ClojureReader,
        "rst" : RstReader,
    }
    


