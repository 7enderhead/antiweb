from pygments.token import Token

from antiweb_lib.readers.Reader import *


# @cstart(XmlReader)

class XmlReader(Reader):
    # @start(XmlReader doc)

    # XmlReader
    # =============
    """
    .. py:class:: XmlReader

       A reader for XML. This class inherits :py:class:`Reader`.
    """

    # @indent 3
    # @include(XmlReader)
    # @(XmlReader doc)

    def __init__(self, lexer, single_comment_markers, block_comment_markers):
        super(XmlReader, self).__init__(lexer, single_comment_markers, block_comment_markers)
        self.block_comment_marker_start = block_comment_markers[0]
        self.block_comment_marker_end = block_comment_markers[1]

    def _accept_token(self, token):
        return token in Token.Comment

    def _cut_comment(self, index, token, text):
        if text.startswith(self.block_comment_marker_start):
            text = self.remove_block_comment_start(text)
            text = self.remove_block_comment_end(text)
        return text

    def filter_output(self, lines):
        """
        .. py:method:: filter_output(lines)

           See :py:meth:`Reader.filter_output`.
        """

        for l in lines:
            if l.type == "d":
                stext = l.text.strip()

                if stext == self.block_comment_marker_start or stext == self.block_comment_marker_end:
                    continue

                #the block comment markers should be removed for cases like: '<!-- asdasdasd -->'
                if stext.startswith(self.block_comment_marker_start):
                    stext = self.remove_block_comment_start(stext)
                    l.text = stext.strip()

                if stext.endswith(self.block_comment_marker_end):
                    stext = self.remove_block_comment_end(stext)
                    l.text = stext.strip()

            yield l

    def remove_block_comment_start(self, text):
        return text[len(self.block_comment_marker_start):]

    def remove_block_comment_end(self, text):
        return text[:-len(self.block_comment_marker_end)]

# @edoc
