import os
import logging
import sys
from sys import platform as _platform

logger = logging.getLogger('antiweb')

#@start()
"""
############
Write Index
############

This file is resposible for all modifications around the index.rst file.
"""

#@include(create_out_file_name_index doc)
#@include(insert_filename_in_index_file doc)
#@include(replace_path_seperator doc)
#@include(write_static doc)
#@include(create_index_file doc)
#@include(search_for_generated_block doc)

#@cstart(write_static)

def _write_static(index_file, start_block, end_block):
#@start(write_static doc)
    """
.. py:method:: _write_static(index_file, start_of_block, end_of_block)

   Writes the static contents to the index file.

   :param index_file: Absolute path of the index file.
   :param start_block: String which contains the generated index block start definition.
   :param end_block: String which contains the generated index block end definition.
    """
#@include(write_static)
#@(write_static doc)

    index_generated = "   " + start_block +"\n   " + end_block
    write_option = "w"
    index_content = "Documentation\n=======================\nContents:\n\n.. toctree::\n   :maxdepth: 2\n\n" + index_generated

    try:
        os.makedirs(os.path.dirname(index_file), exist_ok=True)

        with open(index_file, write_option) as index_out:
            index_out.write(index_content)
    except IOError:
        logger.error("\nError: Index File: %s could not be created.",  index_file)
        sys.exit(1)

#@(write_static)

#@cstart(create_index_file)
def create_index_file(working_dir, directory, file_name, start_block, end_block):
#@start(create_index_file doc)
    """
.. py:method:: create_index_file(working_dir, directory, file_name, start_block, end_block)

   Creates the index file and writes the standard index file contents into the file.

   :param working_dir: Current working directory.
   :param directory: Output directory (may contain a directory path or a directory name)
   :param file_name: Filename of the index file.
   :param start_block: String which contains the generated index block start definition.
   :param end_block: String which contains the generated index block end definition.
   :return: The absolute path of the index file.
    """
#@include(create_index_file)
#@(create_index_file doc)

    index_file = os.path.join(working_dir, directory, file_name)
    index_file_absolute = os.path.abspath(index_file)

    #index file is overwritten if it already exists
    _write_static(index_file_absolute, start_block, end_block)

    return index_file
#@(create_index_file)

#@cstart(search_for_generated_block)
def _search_for_generated_block(index_rst, start_of_block, end_of_block):
#@start(search_for_generated_block doc)
    """
.. py:method:: _search_for_generated_block(index_rst, start_of_block, end_of_block)

    The index file is searched for the generated block. The content in the generated block gets deleted.

    :param index_rst: Absolute path to the index.rst file
    :param start_of_block: The opening directive for the generated block
    :param end_of_block: The closing directive for the generated block
    :return: The content of index.rst file and the linenumber of the end_of_block directive
    """
    #@include(search_for_generated_block)
    #@(search_for_generated_block doc)
    startline = None
    endline = None
    content = ""

    with open(index_rst, "r") as index_file:
        for num, line in enumerate(index_file):
            if start_of_block in line:
                startline = num
            if end_of_block in line:
                endline = num

            if startline and endline:
                index_file.seek(0, 0)
                content = index_file.readlines()
                #delete content of generated block
                del content[startline+1:endline]
                #set endline = old_endline - deleted lines
                endline = endline - (endline-(startline+1))
    return (content, endline)
#@(search_for_generated_block)

#@cstart(replace_path_seperator)

def _replace_path_seperator(file_path):
#@start(replace_path_seperator doc)
    """
.. py:method:: _replace_path_seperator(file_path)

   Replaces OS specific path seperator characters by '_'.

   :param file_path: The path to a file.
    """
#@include(replace_path_seperator)
#@(replace_path_seperator doc)
#Path seperator characters are replaced by "_" in the index file
    if _platform == "linux" or _platform == "linux2":
        file_path = file_path.replace("/","_")
    if _platform == "win32":
        file_path = file_path.replace("\\","_")
    return file_path
#@(replace_path_seperator)

#@cstart(insert_filename_in_index_file)

def insert_filename_in_index_file(out_file, working_dir, recursive, index_file, start_block, end_block):
#@start(insert_filename_in_index_file doc)
    """
.. py:method:: insert_filename_in_index_file(out_file, working_dir, recursive, index_file, start_block, end_block)

  Inserts the given file name into the generated block in the index file.

  :param file_name: The file name which should be inserted into the index file.
  :param index_file: Absolute path of the index file.
  :param start_block: String which contains the generated index block start definition.
  :param end_block: String which contains the generated index block end definition.
    """

#If the user added the -i flag, an index file (documentation base file) is created which contains all processed files.
#Between the :py:class:`start(generated)` and :py:class:`end(generated)` directives the names of the processed files are added.
#Read  :py:meth:`create_out_file_name_index` for more information about how the inserted file name is computed.
#Files can be manually added after the :py:class:`end(generated)` directive.

#@include(insert_filename_in_index_file)
#@(insert_filename_in_index_file doc)

    #We need to know how the file will be called inside of the index.rst file
    file_name = create_out_file_name_index(out_file, working_dir, recursive)

    #At first the position has to be found where the new file should be inserted.
    content, endline = _search_for_generated_block(index_file, start_block, end_block)

    #If the index file does not contain the generated block, it is appended.
    if not content:
        _write_static(index_file, start_block, end_block)
        content, endline = _search_for_generated_block(index_file, start_block, end_block)

    if endline:
        #The new file name is inserted into the index file contents.
        content.insert(endline, "   " + file_name + "\n")

    try:
        #The adapted index file contents are written out to the index file.
        with open(index_file, "w") as index_out:
            for item in content:
                index_out.write(item)
    except IOError:
        logger.error("\nError: Could not write to index file: %s",  index_file)
        sys.exit(1)

#@(insert_filename_in_index_file)

#@cstart(create_out_file_name_index)

def create_out_file_name_index(out_file, working_dir, recursive):
#@start(create_out_file_name_index doc)
    """
.. py:method:: create_out_file_name_index(out_file, working_dir, recursive)

  Creates the file name which should be inserted into the generated index file block.

  :param out_file: Absolute path of the output file.
  :param index_file: Absolute path of the index file.
  :param recursive: Boolean which indicates whether the recursive commandline options is used.
  :return: The file name which should be inserted in the generated index file block.
    """

#If the user added the -i flag, an index file (documentation base file) is created which contains all processed files.
#The names of the processed files are added between the :py:class:`start(generated)` and :py:class:`end(generated)` directives.
#The file names which are inserted into the index file are computed in the following way:

#When the recursive option is used the file name in the index file is a relative path without extension.
#Otherwise the index file will only contain the filename without extension.
#Path seperator characters are replaced by "_".

#| Non-recursive example with current processed file: *C:\\antiweb\\report.rst\\file.rst*:
#| :py:class:`start(generated)`
#| :py:class:`file`
#| :py:class:`end(generated)`
#|
#| Recursive example with current processed file: *C:\\antiweb\\report.rst\\file.rst*:
#| :py:class:`start(generated)`
#| :py:class:`report.rst_file`
#| :py:class:`end(generated)`
#|

#@include(create_out_file_name_index)
#@(create_out_file_name_index doc)

    #1) Obtain only the file name
    out_file_name_index = os.path.split(out_file)[1]
    #2) Remove the extension
    out_file_name_index = os.path.splitext(out_file_name_index)[0]
    if recursive:
        out_file_name_index = os.path.relpath(out_file_name_index, working_dir)
        out_file_name_index = _replace_path_seperator(out_file_name_index)

    return out_file_name_index

#@(create_out_file_name_index)
