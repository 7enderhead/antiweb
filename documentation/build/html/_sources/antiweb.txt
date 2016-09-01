.. default-domain:: python

.. highlight:: python3
   :linenothreshold: 4

#######
antiweb
#######

If you just want to generate the documentation from a source file use
the following function:

..  py:function:: generate(fname, tokens, warnings)

    Generates a rst file from a source file.

    :param string fname: The path to the source file.
    :param list tokens: A list of string tokens, used for @if directives.
    :param bool show_warnings: Warnings will be written
                               via the logging module.
    
    ::
    
        def generate(fname, tokens, show_warnings=False):
            try:
                with open(fname, "r") as f:
                    text = f.read()
            except IOError:
                logger.error("file not found: %s", fname)
                sys.exit(1)
        
            lexer = pm.get_lexer_for_filename(fname)
            #get the language specific comment markers based on the pygments lexer name
            single_comment_markers,  block_comment_markers = get_comment_markers(lexer.name)
            #initialise a new Reader based on the pygments lexer name
            reader = readers.get(lexer.name, Reader)(lexer, single_comment_markers,  block_comment_markers)
        
            document = Document(text, reader, fname, tokens)
            return document.process(show_warnings, fname)
    


*******
Objects
*******

.. compound::

   The graph below show the main objects of antiweb:

   .. digraph:: collaboration

      document [shape=box, label="document"]
      reader   [shape=box, label="reader"]
      directives [shape=box, label="directive" ]
      blocks [shape=box]
      lines [shape=box]

      document -> reader [label="uses"]
      reader -> directives [label="creates"]
      document -> directives [label="uses"]
      document -> blocks [label="contains"]
      directives -> blocks [label="prepare"]
      blocks -> lines [label="contains"]
      lines -> directives [label="contains"]


   The :py:class:`document <Document>` manages the complete transformation: It uses a
   :py:class:`reader <Reader>`  to parse source code. The :py:class:`reader <Reader>`
   creates :py:class:`directives <Directives>` objects for each found antiweb directive in the source
   code. The source code is split in text blocks which consists of several
   :py:class:`lines <Line>`. The :py:class:`document <Document>` process all
   :py:class:`directives <Directives>`  to generate the output document.




***********
File Layout
***********


::

    
    <<imports>>
    <<management>>
    <<parsing>>
    
    def main():
    
        options, args, parser = parsing()
    
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
    
        if options.warnings is None:
            options.warnings = True
    
        if not args:
            parser.print_help()
            sys.exit(0)
    

The program checks if a -r flag was given and if so, save the current directory and change it to the given one.


::

    
        previous_dir = os.getcwd()
    
        #The user input (respectively the input antiweb sets when none is given) can be relative,
        #so we grab the absolute path to work with.
        absolute_path = os.path.abspath(args[0])
    
        if options.recursive:
            directory = absolute_path
    
            #Check if the given path refers to an existing directory.
            #The program aborts if the directory does not exist or if the path refers to a file.
            #A file is not allowed here because the -r option requires a directory.
            if not os.path.isdir(directory):
                logger.error("directory not found: %s", directory)
                sys.exit(1)
    
            os.chdir(directory)
    

The program walks through the given directory and all subdirectories. The absolute file names
are retrieved. Only files with the allowed extensions are processed.


::

    
            #Only files with the following extensions will be processed
            ext_tuple = (".cs",".cpp",".py",".cc", ".rst")
    
            for root, dirs, files in os.walk(directory, topdown=False):
                for filename in files:
                    fname = os.path.join(root, filename)
    
                    if os.path.isfile(fname) and fname.endswith(ext_tuple):
                        write(directory, fname, options)
    

This else will take place when the -r flag is not given.


::

    
        else:
            absolute_file_path = absolute_path
    
            #Check if the given path refers to an existing file.
            #The program aborts if the file does not exist or if the path refers to a directory.
            #A directory is not allowed here because a directory can only be used with the -r option.
            if not os.path.isfile(absolute_file_path):
                logger.error("file not found: %s", absolute_file_path)
                sys.exit(1)
    
            directory = os.path.split(absolute_file_path)[0]
    
            if directory:
                os.chdir(directory)
    
            write(os.getcwd(), absolute_file_path, options)
    
        os.chdir(previous_dir)
        return True







<<imports>>
===========

::

    from optparse import OptionParser
    import logging
    import sys
    import os.path
    import os
    
    from antiweb_lib.write import write



<<management>>
==============


::

    
    __version__ = "0.3.3"
    
    logger = logging.getLogger('antiweb')
    


.. py:method:: def parsing()

   All possible input options are being defined, as well as their help-message, type and variable the values are stored in.
   If no arguments are given (the user did not provide a filepath), the current directory is set as the argument.

::

    def parsing():
        parser = OptionParser("usage: %prog [options] SOURCEFILE",
                              description="Tangles a source code file to a rst file.",
                              version="%prog " + __version__)
    
        parser.add_option("-o", "--output", dest="output", default="",
                          type="string", help="The output filename")
    
        parser.add_option("-t", "--token", dest="token", action="append",
                          type="string", help="defines a token, usable by @if directives")
    
        parser.add_option("-w", "--warnings", dest="warnings",
                          action="store_false", help="suppresses warnings")
    
        parser.add_option("-r", "--recursive", dest="recursive",
                          action="store_true", help="Process every file in given directory")
    
        options, args = parser.parse_args()
    
        #There is no argument given, so we assume the user wants to use the current directory.
        if not args:
            args.append(os.getcwd())
        # parsing() returns the selected options, arguments (the filepath/folderpath) and the parser
        return (options, args, parser)


****************************************
Multi-File Processing and Sphinx Support
****************************************

antiweb creates .rst files which can be further processed by documentation systems like Sphinx.
Additionally you can process multiple files at once with the -r option added.
The optional directory parameter then can be empty to use the current directory, or you provide the directory antiweb should use.

************************
How to add new languages
************************

New languages are added by writing a new Reader class
and registering it in the readers dictionary (see readers).
A simple Reader example is provides by :py:class:`CReader`
a more advanced reader is :py:class:`PythonReader`.

Language specific comment markers
====================================
If a new language is added, its comment markers also have to be registered in the following map.
The map contains the definition of all language specific comment markers.

The comment markers of a language are defined in the format:
``"language" : ([single_comment_tokens],[start_block_token, end_block_token])``

Multiple single and block comment markers can be defined.


::

    comments = {
    "C" : (["//"],(["/*","*/"])),
    "C++" : (["//"],(["/*","*/"])),
    "C#" : (["//"],(["/*","*/"])),
    "Python" : (["#"],(["'''","'''"],["\"\"\"","\"\"\""])),
    }

From the map above the comment markers are retrieved via the following method:

..  py:function:: get_comment_markers(lexer_name)

    Retrieves the language specific comment markers from the comments map.
    The comment markers of C serves as the default comment markers if the lexer name cannot be found.

    :param string lexer_name: The name of the pygments lexer.
    :return: The single and comment block markers defined by the language
    
    ::
    
        
        def get_comment_markers(lexer_name):
            comment_markers = comments.get(lexer_name, comments["C"])
            single_comment_markers = comment_markers[0]
            block_comment_markers = comment_markers[1]
            return single_comment_markers,  block_comment_markers
    

*******
Example
*******

See the antiweb source as an advanced example.

