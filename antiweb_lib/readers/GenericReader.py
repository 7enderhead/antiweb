from pygments.token import Token

from antiweb_lib.readers.Reader import Reader

#@cstart(GenericReader)
class GenericReader(Reader):
    #@start(GenericReader doc)
    #GenericReader
    #=============
    """
    .. py:class:: GenericReader

       A generic reader for languages with single line and block comments . 
       This class inherits :py:class:`Reader`.
    """
    #@indent 3
    #@include(GenericReader)
    #@(GenericReader doc)
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
