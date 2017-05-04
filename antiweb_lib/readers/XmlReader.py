__author__ = "Michael Reithinger, Philipp Rathmanner, Lukas Tanner, Philipp Grandits, and Christian Eitner"
__copyright__ = "Copyright 2017, antiweb team"
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "antiweb team"
__email__ = "antiweb@freelists.org"

from pygments.token import Token

from antiweb_lib.readers.Reader import *


# @cstart(XmlReader)

class XmlReader(Reader):
    # @start(XmlReader doc)

    #XmlReader
    #=============
    """
    .. py:class:: XmlReader

       A reader for XML. This class inherits :py:class:`Reader`.

       Whitespaces and comment tokens are removed from text blocks that are defined on single comment lines.
       If a text block should be indented, define it on multiple lines and indent the include statement.
       Examples of how to define text blocks with and without indentation (without '_'):

       .. code-block:: xml

            <!--
                @_include(comments2)
                @_include(comments3)
            -->

            <!--    @_start(comments2)    -->
            <!--    comments2             -->
            <!--    @_(comments2)         -->

            <!--    @_start(comments3)
                    comments3
                    _(comments3)          -->

            will be resolved as:

            comments2
                comments3


       Here you can see an overview of the XmlReader class and its methods.


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
