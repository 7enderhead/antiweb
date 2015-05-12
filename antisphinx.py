#@start()
"""
.. default-domain:: python

.. highlight:: python
   :linenothreshold: 6

##########
antisphinx
##########

This sphinx extension modifies the syntax highlight mechanism to handle
<<textblock>> abbreviations in source code.
Additionally it makes them linking to the referring source block.

The primary technique is:

1. Extend the basic pygments language lexer with a new *Heading* token.
2. Filter the html output of pygment lexing process: Replacing the 
   heading's ``<span>`` tag  by an ``<a>`` tag,  referencing the 
   a block.

***********
File Layout
***********

@include(file layout)
@include(imports)
@include(Lexers)
@include(Filter Output)

"""
#@

#@start(file layout)
#@code

#@rstart(imports)
'''
<<imports>>
===========
'''
#@code
import sphinx.highlighting as shighlighting
import pygments.lexers as plexers
import pygments
import re
from pygments.token import Token
#@(imports)
#@rstart(Lexers)
'''
<<Lexers>>
==========
'''
#@code

class CHeaderLexer(plexers.CLexer):
    tokens = plexers.CLexer.tokens.copy()
    tokens["whitespace"] = [ (r'(?m)^\s*<<.+>>\s*$', Token.Generic.Heading), ]\
                           + plexers.CLexer.tokens["whitespace"]
    
CHeaderLexer._tokens = CHeaderLexer.process_tokendef('', CHeaderLexer.tokens)


class PythonHeaderLexer(plexers.PythonLexer):
    tokens = plexers.PythonLexer.tokens.copy()
    tokens["root"] = [ (r'^\s*<<.+>>\s*$', Token.Generic.Heading), ]\
                     + plexers.PythonLexer.tokens["root"]
    
PythonHeaderLexer._tokens = PythonHeaderLexer.process_tokendef('', PythonHeaderLexer.tokens)

#replace the sphinx lexers by the new Lexers
shighlighting.lexers["c"] = CHeaderLexer()
shighlighting.lexers["python"] = PythonHeaderLexer()

#@(lexers)
#@rstart(Filter Output)
'''
<<Filter Output>>
=================
'''
#@code
re_html_heading = re.compile('<span class="gh">(.*?)</span>')

def highlight(code, lexer, formatter, outfile=None):
    #@cstart(make anchor)
    def make_anchor(mo):
        indented_name = mo.group(1)
        indent = len(indented_name)-len(indented_name.lstrip())
        name = indented_name.strip()

        #mangle the textblock name to satisfy the sphinx anchor names.
        href = name.replace("&lt;", "").replace("&gt;", "")\
               .replace(" ", "-").replace(":", "-").replace("+", "-")

        if "." in href:
            path = href.split(".")
            href = path[0] + "." + ".".join(path[1:]).lower()
        else:
            href = href.replace("_", "-").lower()

        if href.startswith("-"):
            href = href[1:]

        phref = None
        while phref != href:
            phref = href
            href = href.replace("--", "-")

        return '<span class="gh">%s<a href="#%s">%s</a></span>' \
               % (indented_name[:indent], href, name)
    #@
  
    output = pygments.highlight(code, lexer, formatter, outfile)
    output, noc = re_html_heading.subn(make_anchor, output)
    return output

#monkey path the original sphinx highlighting
shighlighting.highlight = highlight
shighlighting.parser = None


def setup(app):
    #is needed for sphinx extension mechanism
    pass

#@edoc
#@rinclude(make anchor)

#@(Filter Output)
#@(file layout)
