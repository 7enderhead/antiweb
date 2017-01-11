from pygments.token import Token

from antiweb_lib.readers.Reader import *
from antiweb_lib.directives import *

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
