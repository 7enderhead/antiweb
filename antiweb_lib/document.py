__author__ = "Michael Reithinger, Philipp Rathmanner, Lukas Tanner, Philipp Grandits, and Christian Eitner"
__copyright__ = "Copyright 2017, antiweb team"
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "antiweb team"
__email__ = "antiweb@freelists.org"

import os
import operator
import logging
import pygments.lexers as pm

from antiweb_lib.readers.config import readers, comments

from antiweb_lib.readers.Line import Line

from antiweb_lib.readers.Reader import Reader
from antiweb_lib.readers.CReader import CReader
from antiweb_lib.readers.CSharpReader import CSharpReader
from antiweb_lib.readers.ClojureReader import ClojureReader
from antiweb_lib.readers.GenericReader import GenericReader
from antiweb_lib.readers.RstReader import RstReader
from antiweb_lib.readers.PythonReader import PythonReader


logger = logging.getLogger('antiweb')

class WebError(Exception):
    def __init__(self, error_list):
        self.error_list = error_list


#@start()
"""
********
Document
********

@include(Document doc)
@include(Line doc, readers\Line.py)
"""
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
