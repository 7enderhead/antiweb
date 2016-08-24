#####
Write
#####

This module is the mediator for all writing-related classes and modules



Writing the documentation files
===============================

From the given file a .rst file will be created if it contains an antiweb :py:class:`start() directive`.
The following function is called for the creation of the documentation files.

.. py:method:: write(working_dir, input_file, options, index_file, start_block, end_block)

   Creates the corresponding documention file and optionally adds the processed file to the index file.

   :param working_dir: Current working directory.
   :param input_file: Contains the absolute path of the currently processed file.
   :param options: Commandline options.
   :param index_file: Absolute path of the index file.
   :param start_block: String which contains the generated index block start definition.
   :param end_block: String which contains the generated index block end definition.

Before the input file is processed the name of the output file has to be computed.
How the output file name is created depends on the different commandline options.
When there is no output option given the output file name is created in the following way:

.. csv-table::
   :header: "Input File", "Output File"

   ``C:\antiweb\testing.cs``, *C:\\antiweb\\testing.rst*
   ``C:\antiweb\testing.rst``, *C:\\antiweb\\testing_docs.rst*


::

    def write(working_dir, input_file, options, index_file, start_block, end_block):
    
        output = options.output
        recursive = options.recursive
    
        if not output:
            out_file = create_out_file_name(working_dir, "", input_file)
    

If there is an output given, we have to distinguish between the recursive and non-recursive option.
When the recursive option is used in combination with the output option, the output parameter is treated as the documentation directory:

.. csv-table::
   :header: "Input File", "Output File"

   ``C:\antiweb\ -r -o report.rst``,*C:\\antiweb\\report.rst\\file.rst*
   ``C:\antiweb\ -r -o report``,*C:\\antiweb\\report\\file.rst*
   ``C:\antiweb\ -r -o C:\antiweb\report.rst``,*C:\\antiweb\\report.rst\\file.rst*
   ``C:\antiweb\ -r -o \..\report.rst``,*C:\\report.rst\\file.rst*


::

        else:
            if recursive:
                #The output parameter is treated as a directory.
                #If it is a relative path it is combined with the current working directory.
                directory = output
                out_file = create_out_file_name(working_dir,directory,input_file)

When the output option is used without the recursive option the output file name is computed in the following way:

.. csv-table::
   :header: "Input File", "Output File"

   ``C:\antiweb\testing.cs -o report.rst``,*C:\\antiweb\\report.rst*
   ``C:\antiweb\testing.cs -o report``,*C:\\antiweb\\report\\testing.rst*
   ``C:\antiweb\testing.cs -o \..\report``,*C:\\report\\testing.rst*
   ``C:\antiweb\testing.cs -o report\report.rst``,*C:\\antiweb\\report\\report.rst*
   ``C:\antiweb\testing.cs -o report\report.rst\``,*C:\\antiweb\\report\\report.rst\\testing.rst*
   ``C:\antiweb\testing.cs -o C:\report\report.rst``,*C:\\report\\report.rst*


::

            else:
                #Get the file extension from output parameter
                file_extension = os.path.splitext(output)[1]
    
                if file_extension:
                    #If there is a file extension the last part of the output parameter is treated as the output file name.
                    path_tokens = os.path.split(output)
                    directory = path_tokens[0]
                    file_name = path_tokens[1]
    
                    #If directory contains an absolute path the working directory will be ignored,
                    #otherwise all three parameters will be joined
                    out_file = os.path.join(working_dir, directory, file_name)
                    out_file = os.path.abspath(out_file)
                else:
                    #If there is no file extension the whole output parameter is treated as the report directory.
                    directory = output
                    out_file = create_out_file_name(working_dir, directory, input_file)
    
        #Create the documentation directory. If it can't be created the program exits.
        create_doc_directory(out_file)

Now the input file is processed and the corresponding documentation file is created.
If processing is successful, ''could_process'' is set to ''True''.


::

    
        could_process = process_file(input_file, out_file, options.token, options.warnings)
    

If the file was processed successfully and the index option is used, the file name which should be inserted
in the generated index file block has to be computed first. Afterwards the file name is inserted into the
index file (see :py:meth:`insert_filename_in_index_file`).


::

        if options.index and could_process:
            insert_filename_in_index_file(out_file, working_dir, recursive, index_file, start_block, end_block)





.. py:method:: create_out_file_name(working_dir, directory, input_file)

  Computes the absolute path of the output file name. The input file name suffix is replaced by
  ".rst". If the input file name ends with ".rst" the string "_docs" is added before the suffix.
  If directory contains a relative path, then the paths of the working_dir and the directory
  are combined with the input file name. Otherwise, the directory is combined with the
  input file name.

  :param working_dir: Absolute path of the current working directory.
  :param directory: The documentation directory (absolute or relative)
  :param input_file: The absolute path to the file which should be processed.
  :return: The path of the output file.

.. csv-table::
   :header: "Working_Dir", "Directory", "Input_File_Name", "Output_File_Name"

   *C:\\antiweb\\*,doc, *C:\\antiweb\\testing.py* , *C:\\antiweb\\doc\\testing.rst*
   *C:\\antiweb\\* , , *C:\\antiweb\\testing.py* , *C:\\antiweb\\testing.rst*
   *C:\\antiweb\\* ,*C:\\doc\\* , *testing.py*, *C:\\doc\\testing.rst*
   *C:\\antiweb\\*,doc, *C:\\antiweb\\testing.rst* , *C:\\antiweb\\doc\\testing_docs.rst*


::

    
    def create_out_file_name(working_dir, directory, input_file):
    
        docs = "_docs"
        rst_suffix = ".rst"
        out_file_path = os.path.splitext(input_file)[0]
    
        if input_file.endswith(rst_suffix):
            out_file_path =  out_file_path + docs
    
        out_file_path =  out_file_path + rst_suffix
    
        out_file_name = os.path.split(out_file_path)[1]
    
        #If directory contains an absolute path, the working directory is ignored.
        out_file = os.path.join(working_dir, directory, out_file_name)
        out_file = os.path.abspath(out_file)
        return out_file
    

.. py:method:: create_doc_directory(out_file)

   Creates the documentation directory if it does not yet exist.
   If an error occurs, the program exits.

   :param out_file: The path to the output file.

::

    
    def create_doc_directory(out_file):
        try:
            out_file_directory = os.path.split(out_file)[0]
            if not os.path.exists(out_file_directory):
                os.makedirs(out_file_directory)
        except IOError:
            logger.error("\nError: Documentation Directory: %s could not be created",  out_file_directory)
            sys.exit(1)

.. py:method:: process_file(in_file, out_file, token, warnings)

    If no output name was declared, the input name will be given.

    :param in_file: The path to the input file.
    :param out_file: The path to the output file.
    :param token: Passes on the tokens which the user set.
    :return: The boolean could_write indicates if the file could be written.

::

    def process_file(in_file, out_file, token, warnings):
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
        
        parser.add_option("-i", "--index", dest="index",
                          action="store_true", help="Automatically write file(s) to Sphinx' index.rst")
    
        options, args = parser.parse_args()
        
        #There is no argument given, so we assume the user wants to use the current directory.
        if not args:
            args.append(os.getcwd())
        # parsing() returns the selected options, arguments (the filepath/folderpath) and the parser
        return (options, args, parser)

