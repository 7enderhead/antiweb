import operator

#@cstart(Line)
class Line(object):
    #@start(Line doc)
    #Line
    #====
    """
    .. py:class:: Line(fname, index, text[, directives[, type]])

       This class represents a text line.
    """
    #@indent 3
    #@include(Line)
    #@include(Line._directives doc)
    #@include(Line.fname doc)
    #@include(Line.index doc)
    #@include(Line.text doc)
    #@include(Line.type doc)
    #@include(Line.indent doc)
    #@include(Line.sindent doc)
    #@include(Line.directives doc)
    #@include(Line.directive doc)
    #@include(Line.__init__ doc)
    #@include(Line.set doc)
    #@include(Line.like doc)
    #@include(Line.indented doc)
    #@include(Line.change_indent doc)
    #@include(Line.__len__ doc)
    #@include(Line.__repr__ doc)
    #@(Line doc)
    #Attributes
    #@cstart(Line._directives)
    _directives = ()
    """
    .. py:attribute:: _directives
    
       A list of :py:class:`Directive` objects, sorted
       by their priority.
    """
    #@cstart(Line.fname)
    fname = ""
    """
    .. py:attribute:: fname
    
       A string of the source's file name the line belongs to.
    """
    #@cstart(Line.index)
    index = 0
    """
    .. py:attribute:: index
    
       The integer line index of the directive within the current block.
    """
    #@cstart(Line.text)
    text = ""
    """
    .. py:attribute:: text
    
       A string containing the source line.
    """
    #@cstart(Line.type)
    type = "d"
    """
    .. py:attribute:: type
    
       A char representing the line type:

         * ``d`` stands for a document line
         * ``c`` stands for a code line
    """
    #@

    #Methods
    #@cstart(Line.__init__)
    def __init__(self, fname, index, text, directives=(), type='d'):
        """
        .. py:method:: __init__(name, index, text[, directives[, type]])

           The constructor.
        """
        self.fname = fname
        self.index = index
        self.text = text
        self.directives = directives
        self.type = type


    #@cstart(Line.set)
    def set(self, index=None, type=None, directives=None):
        """
        .. py:method:: set([index=None[, type=None[, directives=None]]])

           Changes the attributes :py:attr:`index`, :py:attr:`type`
           and :py:attr:`directives` at once.

           :param integer index: the line index.
           :param char type: Either ``'d'`` or ``'c'``.
           :param list directives: A list of :py:class:`DCirective` objects.
           :return: The :py:class:`Line` object ``self``.
        """
        if index is not None:
            self.index = index

        if type is not None:
            self.type = type

        if directives is not None:
            self.directives = directives

        return self


    
    def clone(self, dline=None):

        if dline is not None:
            for d in self.directives:
                d.line = dline

        return Line(self.fname, self.index, self.text,
                    self.directives[:], self.type)


    #@cstart(Line.like)
    def like(self, text):
        """
        .. py:method:: like(text)

           Clones the Line with a different text.
        """
        return Line(self.fname, self.index, self.indented(text))


    #@cstart(Line.indented)
    def indented(self, text):
        """
        .. py:method:: indented(text)

           Returns the text, with the same indentation as ``self``.
        """
        return self.sindent + text
    
    #@cstart(Line.change_indent)
    def change_indent(self, delta):
        """
        .. py:method:: change_indent(delta)

           Changes the lines indentation.
        """
        if delta < 0:
            delta = min(-delta, self.indent)
            self.text = self.text[delta:]

        elif delta > 0:
            self.text = " "*delta + self.text

        return self

    #@cstart(Line.__len__)
    def __len__(self):
        """
        .. py:method:: __len__()

           returns the length of the stripped :py:attr:`text`.
        """
        return len(self.text.strip())
        

    #@cstart(Line.__repr__)
    def __repr__(self):
        """
        .. py:method:: __repr__()

           returns a textual representation of the line.
        """
        return "Line(%i, %s, %s)" % (self.index, self.text, str(self.directives))
    #@

    #Properties
    #@cstart(Line.indent)
    @property
    def indent(self):
        """
        .. py:attribute:: indent

        An integer representing the line's indentation.
        """
        return len(self.text)-len(self.text.lstrip())


    #@cstart(Line.sindent)
    @property
    def sindent(self):
        """
        .. py:attribute:: sindent

        A string representation of the line's indentation.
        """
        return " "*self.indent


    #@cstart(Line.directives)
    @property
    def directives(self):
        """
        .. py:attribute:: directives

        A sorted sequence of :py:class:`Directive` objects.
        """
        return self._directives


    @directives.setter
    def directives(self, value):
        self._directives = value[:]
        if self._directives:
            self._directives.sort(key=operator.attrgetter("priority"))


    #@cstart(Line.directive)
    @property
    def directive(self):
        """
        .. py:attribute:: directive

           The first of the contained :py:class:`Directive` objects.
        """
        return self.directives and self.directives[0]
