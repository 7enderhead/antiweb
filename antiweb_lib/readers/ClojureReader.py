from pygments.token import Token

from antiweb_lib.readers.Reader import Reader

#@cstart(ClojureReader)
class ClojureReader(Reader):
    #@start(ClojureReader doc)
    #ClojureReader
    #=============
    """
    .. py:class:: ClojureReader

       A reader for Clojure code. This class inherits :py:class:`Reader`.
    """
    #@indent 3
    #@include(ClojureReader)
    #@(ClojureReader doc)
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
    #@edoc
    #@(ClojureReader)
