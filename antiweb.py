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
   creates :py:class:`directives <Directives>` objects for each found antiweb directive in the source
   code. The source code is split in text blocks which consists of several
   :py:class:`lines <Line>`. The :py:class:`document <Document>` process all
   :py:class:`directives <Directives>`  to generate the output document.

********
Document
********

@include(Document doc)
@include(Line doc, antiweb_lib\readers\Reader.py)


***********
File Layout
***********

@include(file layout)

@include(imports)

@include(management)

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

*******
Example
*******

See the :ref:`antiweb` source as an advanced example.

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
import pygments.lexers as pm
import logging
import sys
import os.path
import operator
import os
from sys import platform as _platform

from antiweb_lib.readers.Reader import Reader, Line
from antiweb_lib.readers.CReader import CReader
from antiweb_lib.readers.CSharpReader import CSharpReader
from antiweb_lib.readers.ClojureReader import ClojureReader
from antiweb_lib.readers.GenericReader import GenericReader
from antiweb_lib.readers.rstReader import rstReader
from antiweb_lib.readers.PythonReader import PythonReader

#@rstart(management)

#<<management>>
#==============

#@code

__version__ = "0.3.3"

logger = logging.getLogger('antiweb')

class WebError(Exception):
    def __init__(self, error_list):
        self.error_list = error_list

# The keys are the lexer names of pygments
readers = {
    "C" : CReader,
    "C++" : CReader,
    "C#" : CSharpReader,
    "Python" : PythonReader,
    "Clojure" : ClojureReader,
    "rst" : rstReader,
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
            # if sub doc has no macros insert mine
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
    def add_error(self, line_number, text, fname=""):
        """
        .. py:method:: add_error(line, text)

           Adds an error to the list.
           :param integer line_number: The line number that causes the error.
           :param string text: An error text.
           :param string fname: name of currently processed file (needed if no data in self.lines)
           
        """
        # determine if access to line_number is possible
        if line_number < len(self.lines):
            line = self.lines[line_number]
        else:
            # without a line in self.lines, antiweb would crash on appending it to the errors (errorlist)
            # we add a 'fake line' to prevent that issue
            line = Line(fname, -1, "")
            
        self.errors.append((line, text))


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
