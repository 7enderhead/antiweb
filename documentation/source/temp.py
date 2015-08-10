#@start(installation)
"""
The most important parts of the system are Python 3, Sphinx and antiweb. Because of incompatibility with Python 2 you can't create 
documentaries of Python 2 programs.


    * Step 1: Install Python 3.4
    * Step 2: After installing Python, run below commands in cmd (you have to navigate to Python\\Scripts first)
   
    @code
    pip install sphinx #when necessary you can add flags e.g. --proxy "proxy"
    @edoc

    @code
     pip uninstall babel #uninstall it because of incompatibility
    @edoc
    
    @code 
    pip install babel==1.3 #install compatible version 
    @edoc

    * Run sphinx-quickstart.exe and follow the steps to configure sphinx as you like it. (However, say yes to all extensions suggested during the process)
    * The sphinx quickstart created a project folder for you, open the conf.py which is in that folder
    * You should find something like this: 

       @code
       extensions = [
       'sphinx.ext.autodoc',
       'sphinx.ext.doctest',
       'sphinx.ext.intersphinx',
       'sphinx.ext.todo',
       'sphinx.ext.coverage',
       'sphinx.ext.mathjax',
       'sphinx.ext.ifconfig',
       'sphinx.ext.viewcode',
       ]
       @edoc

    * Add 'sphinx.ext.graphviz' at the end and it will look like this:

       @code
       extensions = [
       'sphinx.ext.autodoc',
       'sphinx.ext.doctest',
       'sphinx.ext.intersphinx',
       'sphinx.ext.todo',
       'sphinx.ext.coverage',
       'sphinx.ext.mathjax',
       'sphinx.ext.ifconfig',
       'sphinx.ext.viewcode',
       'sphinx.ext.graphviz',
       ]
       @edoc

    * Download the Graphviz msi installer from here: http://www.graphviz.org/Download_windows.php
    * After installing Graphviz you will find a Graphviz folder inside your Program folder, open it
    * Copy the content of its bin folder to Python\\Scripts


    
    Preparing the .rst files
    ========================

    * Download antiweb from here https://github.com/Yarmek/antiweb and copy the antiweb.py file into the Python folder
    * You can now create a .rst file out of a C, C++, C# and py files.
    * To do that, simply use following command:
    @code
    python antiweb.py "PATH TO THE FILE"
    @edoc
   
    * You will then find a new file which is called "Filename".rst -> This file will be used in Sphinx to generate the documentation
    * Sphinx also created a index.rst file for you. Open it and add the filename of the rst file (without the file extension) to the toctree so it looks like this:
   
    @code
    .. toctree::
    :maxdepth: 2
   
    FILENAME
    @edoc

    * You can add multiple files, they will then be listed in the generated index of your project
    * It is also possible to use Graphviz for graph visualizatin. A proper graph should look like this:
    @code
    .. digraph:: name

     "bubble 1" -> "bubble 2" -> "bubble 3" -> "bubble 1";
    @edoc

    * The output from above code would look like this:

    .. digraph:: test

     "bubble 1" -> "bubble 2" -> "bubble 3" -> "bubble 1";

    * For more informatin on Graphviz visit http://www.graphviz.org/
    * When you have included the rst file in the index file, you can run Sphinx to finally create your documentation, here is an example:
    @code
    sphinx-build.exe -b html sphinx\source sphinx\source -D graphviz_dot=dot.exe
    @edoc
   
    * The ''-b'' flag indicates the builder to use
    * ''sphinx\\source'' indicates the path to the index.rst
    * ''sphinx\\source'' this one indicates the output path (you can change your ouput path to every path where you want the final documentation)
    * ''-D graphviz_dot=dot.exe'' indicates the path for the graphviz virtualizer dot.exe
   
    * After sphinx has finished you will find some .html files in the output path. This is your finished documentation. 




"""
#@(installation)