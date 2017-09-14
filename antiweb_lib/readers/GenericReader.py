__author__ = "Michael Reithinger, Philipp Rathmanner, Lukas Tanner, Philipp Grandits, and Christian Eitner"
__copyright__ = "Copyright 2017, antiweb team"
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "antiweb team"
__email__ = "antiweb@freelists.org"

from pygments.token import Token

from antiweb_lib.readers.Reader import Reader

#@cstart(GenericReader)
class GenericReader(Reader):
    #@start(GenericReader doc)
    #GenericReader
    #=============
    """
    .. py:class:: GenericReader

       A generic reader for languages with single line and block comments.
       This class inherits :py:class:`Reader`.
    """
    #@indent 3
    #@include(GenericReader)
    #@(GenericReader doc)
    def __init__(self, lexer, single_comment_markers, block_comment_markers):
        super(GenericReader, self).__init__(lexer, single_comment_markers, block_comment_markers)
        self.single_comment_marker = single_comment_markers[0]
        self.block_comment_marker_start = block_comment_markers[0]
        self.block_comment_marker_end = block_comment_markers[1]

    def _accept_token(self, token):
        return token in Token.Comment
    
    def _cut_comment(self, index, token, text):
        if text.startswith(self.block_comment_marker_start):
            text = text[len(self.block_comment_marker_start):-len(self.block_comment_marker_end)]
    
        elif text.startswith(self.single_comment_marker):
            text = text[len(self.single_comment_marker):]

        return text

    def filter_output(self, lines):

        for l in lines:
            if l.type == "d":
                #remove comment chars in document lines
                stext = l.text.lstrip()

                if stext == self.block_comment_marker_start or stext == self.block_comment_marker_end:
                    #remove the block comment characters from documentation lines
                    #see the l.text.lstrip()! if the lines ends with a white space
                    #the quotes will be kept! This is feature, to force the quotes
                    #in the output
                    continue

                if stext.startswith(self.single_comment_marker):
                    l.text = l.indented(stext[len(self.single_comment_marker):])
                            
            yield l
