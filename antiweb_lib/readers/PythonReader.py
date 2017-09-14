__author__ = "Michael Reithinger, Philipp Rathmanner, Lukas Tanner, Philipp Grandits, and Christian Eitner"
__copyright__ = "Copyright 2017, antiweb team"
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "antiweb team"
__email__ = "antiweb@freelists.org"

from pygments.token import Token
import bisect

from antiweb_lib.readers.Reader import Reader
from antiweb_lib.directives import *

#@cstart(PythonReader)
class PythonReader(Reader):
    #@start(PythonReader doc)
    #PythonReader
    #============
    '''
    .. py:class:: PythonReader

       A reader for python code. This class inherits :py:class:`Reader`.
       To reduce the number of sentinels, the python reader does some more
       sophisticated source parsing:

       A construction like::

             @subst(_at_)cstart(foo)
             def foo(arg1, arg2):
                """
                Foo's documentation
                """
                code


       is replaced by::

             @subst(_at_)cstart(foo)
             def foo(arg1, arg2):
                @subst(_at_)start(foo doc)
                """
                Foo's documentation
                """
                @subst(_at_)include(foo)
                @subst(_at_)(foo doc)
                code


       The replacement will be done only:

         * If the doc string begins with """
         * If the block was started by a ``@rstart`` or ``@cstart`` directive
         * If there is no antiweb directive in the doc string.
         * Only a ``@cstart`` will insert the @include directive.


       Additionally the python reader removes all single line ``"""`` and ``@subst(triple)``
       from documentation lines. In the following lines::

             @subst(_at_)start(foo)
             """
             Documentation
             """

       The ``"""`` are automatically removed in the rst output. (see :py:meth:`filter_output`
       for details).

    '''

    #@indent 3
    #@include(PythonReader)
    #@include(PythonReader._post_process doc)
    #@include(PythonReader._accept_token doc)
    #@include(PythonReader.filter_output doc)
    #@include(PythonReader._cut_comment doc)
    #@(PythonReader doc)
    def __init__(self, lexer,  single_comment_markers,  block_comment_markers):
        super(PythonReader, self).__init__(lexer,  single_comment_markers,  block_comment_markers)
        self.doc_lines = []
        self.single_comment_marker = single_comment_markers[0]
        self.doc_string_marker = '"""'

    #@cstart(PythonReader._post_process)
    def _post_process(self, fname, text):
        """
        .. py:method:: _post_process(fname, text)

           See :py:meth:`Reader._post_process`.

           This implementation *decorates* doc strings
           with antiweb directives.
        """
        #from behind because we will probably insert some lines
        self.doc_lines.sort(reverse=True)

        #handle each found doc string
        for start_line, end_line in self.doc_lines:
            indents = set()

            #@cstart(no antiweb directives in doc string)
            #If antiweb directives are within the doc string,
            #the doc string will not be decorated!
            directives_between_start_and_end_line = False
            for l in self.lines[start_line+1:end_line]:
                if l:
                    #needed for <<insert additional include>>
                    indents.add(l.indent)

                if l.directives:
                    directives_between_start_and_end_line = True
                    break

            if directives_between_start_and_end_line: continue

            #@cstart(find the last directive before the doc string)
            last_directive = None
            for l in reversed(self.lines[:start_line]):
                if l.directives:
                    last_directive = l.directives[0]
                    break
            #@

            if isinstance(last_directive, RStart):
                #@cstart(decorate beginning and end)
                l = self.lines[start_line]
                start = Start(start_line, last_directive.name + " doc")
                l.directives = list(l.directives) + [start]

                l = self.lines[end_line]
                end = End(end_line, last_directive.name + " doc")
                l.directives = list(l.directives) + [end]
                #@

                if isinstance(last_directive, CStart):
                    #@cstart(insert additional include)
                    l = l.like("")
                    include = Include(end_line, last_directive.name)
                    l.directives = list(l.directives) + [include]
                    self.lines.insert(end_line, l)

                    #the include directive should have the same
                    #indentation as the .. py:function:: directive
                    #inside the doc string. (It should be second
                    #value of sorted indents)
                    indents = list(sorted(indents))
                    if len(indents) > 1:
                        l.change_indent(indents[1]-l.indent)
                    #@

        super(PythonReader, self)._post_process(fname, text)

    #@edoc
    #@rinclude(no antiweb directives in doc string)
    #@rinclude(find the last directive before the doc string)
    #@rinclude(decorate beginning and end)
    #@rinclude(insert additional include)

    #@cstart(PythonReader._accept_token)
    def _accept_token(self, token):
        """
        .. py:method:: _accept_token(token)

           See :py:meth:`Reader._accept_token`.
        """
        return token in Token.Comment or token in Token.Literal.String.Doc


    #@cstart(PythonReader._cut_comment)
    def _cut_comment(self, index, token, text):
        """
        .. py:method:: _cut_comment(index, token, text)

           See :py:meth:`Reader._cut_comment`.
        """
        if token in Token.Literal.String.Doc:
            if text.startswith(self.doc_string_marker):
                #save the start/end line of doc strings beginning with """
                #for further decoration processing in _post_process,
                start_line = bisect.bisect(self.starts, index)-1
                end_line = bisect.bisect(self.starts, index+len(text)-3)-1
                lines = list(filter(bool, text[3:-3].splitlines())) #filter out empty strings
                if lines:
                    self.doc_lines.append((start_line, end_line))

            text = text[3:-3]

        return text

    #@cstart(PythonReader.filter_output)
    def filter_output(self, lines):
        """
        .. py:method:: filter_output(lines)

           See :py:meth:`Reader.filter_output`.
        """
        for l in lines:
            if l.type == "d":
                #remove comment chars in document lines
                stext = l.text.lstrip()

                is_block_comment = False

                for block_start, block_end in self.block_comment_markers:
                    is_block_comment = is_block_comment or stext == block_start or stext == block_end

                if is_block_comment:
                    # remove """ and ''' from documentation lines
                    # see the l.text.lstrip()! if the lines ends with a white space
                    # the quotes will be kept! This is feature, to force the quotes
                    # in the output
                    continue

                if stext.startswith(self.single_comment_marker):
                    #remove comments but not chapters
                    l.text = l.indented(stext[1:])

            yield l
