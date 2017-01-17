import os
import logging
import sys
import pygments.lexers as pm

from antiweb_lib.readers.Reader import Reader

from antiweb_lib.document import Document, WebError, get_comment_markers

from antiweb_lib.readers.config import readers

logger = logging.getLogger('antiweb')

#@start()
"""
######
Write
######

This module is the mediator for all writing-related classes and modules

"""

#@include(write_documentation)
#@include(_create_out_file_name doc)
#@include(_create_doc_directory doc)
#@include(_process_file doc)
#@include(write_file doc)
#@include(create_write_string doc)

#@cstart(_create_out_file_name)

def _create_out_file_name(directory, input_file):
#@start(_create_out_file_name doc)
    """
.. py:method:: _create_out_file_name(working_dir, input_file)

  Computes the absolute path of the output file name. The input file name suffix is replaced by
  ".rst". If the input file name ends with ".rst" the string "_docs" is added before the suffix.
  The output file name consists of the combination of the directory and the input file name.

  :param directory: The absolute path of the documentation directory.
  :param input_file: The absolute path to the file which should be processed.
  :return: The absolute path of the output file.
    """

#.. csv-table::
#   :header: "Directory", "Input_File_Name", "Output_File_Name"

#   *C:\\antiweb\\doc*, *C:\\antiweb\\testing.py* , *C:\\antiweb\\doc\\testing.rst*
#   *C:\\antiweb\\*, *C:\\antiweb\\testing.py* , *C:\\antiweb\\testing.rst*
#   *C:\\antiweb\\doc*, *C:\\antiweb\\testing.rst* , *C:\\antiweb\\doc\\testing_docs.rst*
#   *C:\\antiweb\\doc*, *testing.py* , *C:\\antiweb\\doc\\testing.rst*

#@include(_create_out_file_name)
#@(_create_out_file_name doc)

    docs = "_docs"
    rst_suffix = ".rst"
    out_file_path = os.path.splitext(input_file)[0]

    if input_file.endswith(rst_suffix):
        out_file_path =  out_file_path + docs

    out_file_path =  out_file_path + rst_suffix

    out_file_name = os.path.split(out_file_path)[1]

    #If directory contains an absolute path, the working directory is ignored.
    out_file = os.path.join(directory, out_file_name)
    out_file = os.path.abspath(out_file)
    return out_file

#@(_create_out_file_name)

#@cstart(generate)
def generate(fname, tokens, show_warnings=False):
    """
    ..  py:function:: generate(fname, tokens, warnings)

        Generates a rst file from a source file.

        :param string fname: The path to the source file.
        :param list tokens: A list of string tokens, used for @if directives.
        :param bool show_warnings: Warnings will be written
                                   via the logging module.
    """
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
    reader = readers.get(lexer.name, Reader)(lexer, single_comment_markers, block_comment_markers)

    document = Document(text, reader, fname, tokens)
    return document.process(show_warnings, fname)
#@(generate)

#@cstart(_create_doc_directory)

def _create_doc_directory(out_file):
#@start(_create_doc_directory doc)
    """
.. py:method:: _create_doc_directory(out_file)

   Creates the documentation directory if it does not yet exist.
   If an error occurs, the program exits.

   :param out_file: The path to the output file.
    """
#@include(_create_doc_directory)
#@(_create_doc_directory doc)
    try:
        out_file_directory = os.path.split(out_file)[0]
        if not os.path.exists(out_file_directory):
            os.makedirs(out_file_directory)
    except IOError:
        logger.error("\nError: Documentation Directory: %s could not be created", out_file_directory)
        sys.exit(1)
#@(_create_doc_directory)

#@cstart(_process_file)
def _process_file(in_file, out_file, token, warnings):
#@start(_process_file doc)
    """
.. py:method:: _process_file(in_file, out_file, token, warnings)

    If no output name was declared, the input name will be given.

    :param in_file: The path to the input file.
    :param out_file: The path to the output file.
    :param token: Passes on the tokens which the user set.
    :return: The boolean could_write indicates if the file could be written.
    """
#@include(_process_file)
#@(_process_file doc)

#The output text will be written in the output file. If there is an output text, the function returns could_write as True.

    could_write = False
    try:
        text_output = generate(in_file, token, warnings)
        if text_output:
            with open(out_file, "w") as f:
                f.write(text_output)
            could_write = True
    except WebError as e:
        logger.error("\nErrors:")
        for l, d in e.error_list:
            logger.error("  in line %i(%s): %s", l.index+1, l.fname, d)
            logger.error("      %s", l.text)

    return could_write
#@(_process_file)

#@start(write_documentation)

#Writing the documentation files
#===============================

#From the given file a .rst file will be created if it contains an antiweb :py:class:`start() directive`.
#The following function is called for the creation of the documentation files.

#@include(write doc)
#@include(write_body)
#@(write_documentation)

#@start(write)
def write(working_dir, input_file, options):
#@start(write doc)
    """
.. py:method:: write(working_dir, input_file, options)

   Creates the corresponding documentation file.

   :param working_dir: Current working directory.
   :param input_file: Contains the absolute path of the currently processed file.
   :param options: Commandline options.
   :return: a tuple of type <boolean, string>: the first value indicates if the documentation file could be generated and
            the second paramater contains the absolute path of the output file
    """
#@(write doc)

#@start(write_body)

#Before the input file is processed the name of the output file has to be computed.
#How the output file name is created depends on the different commandline options.
#When there is no output option given the output file name is created in the following way:

#.. csv-table::
#   :header: "Input File", "Output File"

#   ``C:\antiweb\testing.cs``, *C:\\antiweb\\testing.rst*
#   ``C:\antiweb\testing.rst``, *C:\\antiweb\\testing_docs.rst*

#@code
#@include(write)

    #options.output is either an absolute path or None
    output = options.output
    recursive = options.recursive

    if not output:
        out_file = _create_out_file_name(working_dir, input_file)

#@edoc

#If there is an output given, we have to distinguish between the recursive and non-recursive option.
#When the recursive option is used in combination with the output option, the output parameter is treated as the documentation directory:

#.. csv-table::
#   :header: "Commandline", "Current Directory", "Output File"

#   ``C:\antiweb\ -r -o report.rst``, *C:\\dir*, *C:\\dir\\report.rst\\file.rst*
#   ``C:\antiweb\ -r -o report``, *C:\\dir*, *C:\\dir\\report\\file.rst*
#   ``C:\antiweb\ -r -o C:\report``, *C:\\dir*, *C:\\report\\file.rst*
#   ``C:\antiweb\ -r -o \..\report.rst``, *C:\\dir*, *C:\\report.rst\\file.rst*

#@code
    else:
        if recursive:
            #The output parameter is treated as a directory.
            directory = output
            out_file = _create_out_file_name(directory,input_file)
#@edoc

#When the output option is used without the recursive option the output file name is computed in the following way:

#.. csv-table::
#   :header: "Commandline", "Current Directory", "Output File"

#   ``C:\antiweb\testing.cs -o report.rst``, *C:\\dir*, *C:\\dir\\report.rst*
#   ``C:\antiweb\testing.cs -o report``, *C:\\dir*, *C:\\dir\\report\\testing.rst*
#   ``C:\antiweb\testing.cs -o \..\report``, *C:\\dir*, *C:\\dir\\report\\testing.rst*
#   ``C:\antiweb\testing.cs -o report\report.rst``, *C:\\dir*, *C:\\dir\\report\\report.rst*
#   ``C:\antiweb\testing.cs -o C:\report\report.rst``, *C:\\dir*, *C:\\report\\report.rst*


#@code
        else:
            #Get the file extension from output parameter
            file_extension = os.path.splitext(output)[1]

            if file_extension:
                #If there is a file extension the last part of the output parameter is treated as the output file name.
                path_tokens = os.path.split(output)
                directory = path_tokens[0]
                file_name = path_tokens[1]

                out_file = os.path.join(directory, file_name)
                out_file = os.path.abspath(out_file)
            else:
                #If there is no file extension the whole output parameter is treated as the report directory.
                directory = output
                out_file = _create_out_file_name(directory, input_file)

    #Create the documentation directory. If it can't be created the program exits.
    _create_doc_directory(out_file)
#@edoc

#Now the input file is processed and the corresponding documentation file is created.
#If processing is successful, ''could_write'' is set to ''True''.

#@code
    could_write = _process_file(input_file, out_file, options.token, options.warnings)

    return could_write, out_file

#@edoc

#@(write_body)

#@cstart(write_file)
def write_file(working_dir, input_file, options):
#@start(write_file doc)
    """
.. py:method:: write_file(working_dir, input_file, options)

    Creates the corresponding documentation file and prints a message whether the documentation file could be generated.

    :param working_dir: Current working directory.
    :param input_file: Contains the absolute path of the currently processed file.
    :param options: Commandline options.
    """
#@include(write_file)
#@(write_file doc)

    could_write, created_file = write(working_dir, input_file, options)
    out_string = create_write_string(could_write, input_file, created_file)
    print("\n"+out_string)

#@(write_file)

#@cstart(create_write_string)
def create_write_string(could_write, input_file, created_file):
#@start(create_write_string doc)
    """
.. py:method:: create_write_string(could_write, input_file, created_file)

    Creates a string based on the value of could_write.

    :param could_write: A boolean which indicates whether the documentation file could be generated.
    :param input_file: Contains the absolute path of the currently processed file.
    :param created_file: Contains the absolute path of the created documentation file.
    :return: A created string based on the value of could_write.
    """
#@include(create_write_string)
#@(create_write_string doc)

    if could_write:
        out_string = "Generated " + created_file + " from: " + input_file
    else:
        out_string = "Could not generate file: " + created_file

    return out_string

#@(create_write_string)