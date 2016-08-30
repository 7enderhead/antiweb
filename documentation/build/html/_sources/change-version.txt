.. default-domain:: python

.. highlight:: python3
   :linenothreshold: 4

#####################
Change Version Number
#####################

This standalone script, called `change-version.py`, will search for all occurences of version statements and replace them with a new version number. This is needed because we
have a handful of different meta and config files  which contain version statements.

Normally you would have to search through all files manually and change the version number in every single file. With this script we can
save time by letting it search and replace the version number for us.

Usage
======

The usage of `change-version.py` is quite simple:


::

        change-version.py new_version (e.g., 0.3.3)


.. py:method:: main()

    The `main()` function contains the recursive search for files and the replacement of the old version number.


We set the arguments coming from the command line. If there is not exactly one argument, print the usage and exit.


::

    
    def main(argv):
    
        if not len(argv) == 2: # own script name and first argument
            print("Usage: change-version.py new_version (e.g., 0.3.3)")
            sys.exit(1)
    
        new_version_number = argv[1]
    
        own_script_name = os.path.basename(argv[0])
    

The regex search pattern is defined as follows:

    * Search for occurences of the word `version`, followed by any number of any character.
    * That sequence is then consolidated as the first group.
    * It must then be followed by a digit, dot, digit, dot, digit (e.g., 0.3.3).
    * The digit/dot sequence is consolidated as the second group.
    * The whole pattern is NOT case sensitive and takes place in a single line.


::

    
        pattern = re.compile(r'(version.*)(\d+\.\d+\.\d+)', re.IGNORECASE)
    

The directories in which we do not want to search for occurences of the version number are defined.
This is needed, because there are generated files in the directory that raise an encoding error when being read.


::

    
        excluded_dirs = set(['.git', '__pycache__', 'dist', 'doctrees', 'build'])
    
    
        for root, dirs, filenames in os.walk(os.getcwd(), topdown=True):
            dirs[:] = [directory
                           for directory in dirs
                               if directory not in excluded_dirs]
    
            for filename in filenames:
                absolute_path = os.path.join(root, filename)
    
Our tool would also find and replace the version number in our documentation files and the changelog, we do
not want to change those and therefore exclude `.rst` files. We also exclude the script itself, `change-version.py`,
because we do not want it to be changed.

::

    
                if os.path.isfile(absolute_path) and \
                    not absolute_path.endswith('.rst') and \
                    not filename == own_script_name:
    
                    with open(absolute_path, "r", encoding="utf8") as input_file:
    
                        lines = input_file.read()
    

If there is a line that matches our criteria, we save that `match`. The user then gets notified that there
is a matching line in a file.

::

    
                        match = re.search(pattern, lines)
    
                        if match:
                            old_version = match.group(2)
                            print(absolute_path, old_version, "-->", new_version_number)
    

When substituting the old version number, we replace the whole match (e.g., __version__ = 0.3.3) and
re-use the first group (e.g., __version__ = ) to combine it with the new version number.

::

    
                            with open(absolute_path, "w") as output_file:
                                new_version = r'\g<1>' + new_version_number
                                output_file.write(re.sub(pattern, new_version, lines))
    






Examples
========

Running the following command:


::

        antiweb_work> change-version.py 0.3.4

Gives the following output:


::

        antiweb_work/PKG-INFO 0.3.3 --> 0.3.4
        antiweb_work/README.md 0.3.3 --> 0.3.4
        antiweb_work/setup.py 0.3.3 --> 0.3.4
        antiweb_work/antiweb.egg-info/PKG-INFO 0.3.3 --> 0.3.4
        antiweb_work/documentation/source/conf.py 0.3.3 --> 0.3.4


Errors
======

When no version statements are found, `change-version.py` does not raise an error but runs without touching any files
or giving any output in the command line.

When the user provides not exactly one argument, `change-version.py` shows the following usage message:


::

        Usage: change-version.py new_version (e.g., 0.3.3)



