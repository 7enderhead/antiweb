import re
import bisect

from antiweb_lib.directives import *
from antiweb_lib.readers.Line import Line

#@start()
"""
*******
Readers
*******

Readers are responsible for the language dependent
source parsing.

@include(Reader doc)
@include(CReader doc, CReader.py)
@include(CSharpReader doc, CSharpReader.py)
@include(PythonReader doc, PythonReader.py)
@include(ClojureReader doc, ClojureReader.py)
@include(GenericReader doc, GenericReader.py)
@include(RstReader doc, RstReader.py)
"""
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
