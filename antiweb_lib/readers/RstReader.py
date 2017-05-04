__author__ = "Michael Reithinger, Philipp Rathmanner, Lukas Tanner, Philipp Grandits, and Christian Eitner"
__copyright__ = "Copyright 2017, antiweb team"
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "antiweb team"
__email__ = "antiweb@freelists.org"

from pygments.token import Token

from antiweb_lib.readers.Reader import Reader

#@cstart(RstReader)
class RstReader(Reader):
    #@start(RstReader doc)
    #RstReader
    #=============
    """
    .. py:class:: RstReader

       A reader for rst code. This class inherits :py:class:`Reader`.
    """
    #@indent 3
    #@include(RstReader)
    #@(RstReader doc)
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
