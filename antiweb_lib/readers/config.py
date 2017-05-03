from antiweb_lib.readers.Reader import Reader
from antiweb_lib.readers.CReader import CReader
from antiweb_lib.readers.CSharpReader import CSharpReader
from antiweb_lib.readers.ClojureReader import ClojureReader
from antiweb_lib.readers.GenericReader import GenericReader
from antiweb_lib.readers.RstReader import RstReader
from antiweb_lib.readers.PythonReader import PythonReader
from antiweb_lib.readers.XmlReader import XmlReader

#@start(reader_dictionary doc)
#The Reader Dictionary
#=====================
'''
When writing a new reader, please register it in this dictionary with the according lexer name of the file. Please note that the Readername is the name of the class, not the file.

Format:

@code
 "lexername" : Readername,
@edoc
'''

#@code

readers = {
    "C" : CReader,
    "C++" : CReader,
    "C#" : CSharpReader,
    "Python" : PythonReader,
    "Clojure" : ClojureReader,
    "rst" : RstReader,
    "XML" : XmlReader
}

#@edoc

#@start(comments doc)
#Language specific comment markers
#====================================
'''
If a new language is added, its comment markers also have to be registered in the following map.
The map contains the definition of all language specific comment markers.

The comment markers of a language are defined in the format:
``"language" : ([single_comment_tokens],[start_block_token, end_block_token])``

Multiple single and block comment markers can be defined.
'''

#@code
comments = {
"C" : (["//"],(["/*","*/"])),
"C++" : (["//"],(["/*","*/"])),
"C#" : (["//"],(["/*","*/"])),
"Python" : (["#"],(["'''","'''"],["\"\"\"","\"\"\""])),
"XML" : ([], (["<!--","-->"]))
}
#@
