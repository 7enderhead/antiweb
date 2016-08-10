.. default-domain:: python

.. highlight:: python
   :linenothreshold: 6



############
Installation
############

The most important parts of the system are Python 3, Sphinx and antiweb. Because of incompatibility with Python 2 you can't create 
documentations of Python 2 programs.

***********************************
Overview of the installation steps:
***********************************

   * Python
   * antiweb
   * Graphviz (Optional)
   
Install Python
==============

   * Install Python 3.x
   * You should make sure that Python is added to your PATH environment-variable so you can access it from everywhere 
   
Install antiweb
===============
   * After installing Python, run below command in cmd to install antiweb (you can add the Scripts directory inside Python to the PATH or navigate to it [I would prefer the first option])
   
   
   ::
   
       pip install git+https://github.com/Yarmek/antiweb.git@work
   
   * :py:class:`IMPORTANT` If you get a connection error the reason is most likely your proxy. You then have to use a tool like `cntlm`_ and add a proxy flag when running pip, example:
   
   
   ::
   
       pip install git+https://github.com/Yarmek/antiweb.git@work --proxy http://localhost:8123
   

Install Graphviz (Optional)
===========================

   Graphviz can be used to generate graphs and images out of source code
   * Download the Graphviz msi installer from here: http://www.graphviz.org/Download_windows.php 
   * Add the bin folder inside the Graphviz directory to your PATH variable

Project setup
=============

   :py:class:`IMPORTANT` You have to repeat the following steps for each sphinx project you create

   * Run sphinx-quickstart from inside your project folder (you have to create a folder yourself) and follow the steps to configure sphinx as you like it (you should allow sphinx to create a make.bat and a Makefile, those two make life much easier). The sphinx quickstart then creates a project for you inside that folder.
   
   :py:class:`Optional` If you would like to use Graphviz, open the conf.py which is in the project folder.
   
   * You should find something like this: 

           
           ::
           
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

    Add 'sphinx.ext.graphviz' at the end and it will look like this:

           
           ::
           
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


Preparing the .rst files
========================
   
    * You can now begin creating a .rst file out of a C, C++, C# and py file. To do that, simply use following command:
   
   
   ::
   
       antiweb.py "PATH TO THE FILE/DIRECTORY" [options]
   
   * You will then find a new file which is called ``Filename.rst`` -> This file will be used in Sphinx to generate the documentation
   
   * antiweb can also create/edit a file called "index.rst" if you add the -i option when executing antiweb. In that index all processed files for documentation with sphinx are included
   
   * When you don't use the -i option you have to edit the file manually (sphinx-quickstart created it):

   
   ::
   
    Welcome to the Documentation!
    =============================
    
    Contents:
    
       .. toctree::
          :maxdepth: 2

          .. start(generated)
          filename #without file extension!
          filename 2
          .. (generated)
          extra_file

   * You can add multiple files, they will then be listed in the generated index of your html project
   * If you would like to add files that were not genereated by antiweb, simply add them outside of the `generated` directives
   * It is also possible to use Graphviz for graph visualizatin. A proper graph should look like this:
   
   ::
   
       .. digraph:: name
    
        "bubble 1" -> "bubble 2" -> "bubble 3" -> "bubble 1";

   * The output from above code would look like this:

   .. digraph:: test

    "bubble 1" -> "bubble 2" -> "bubble 3" -> "bubble 1";

   * For more informatin on Graphviz visit http://www.graphviz.org/
   
   
Creating the documentation
==========================

   * When you have included the rst file(s) in the index file, you can run Sphinx to finally create your documentation, here is an example:
   
   ::
   
       make builder
   
   * The ``builder`` flag indicates the builder to use. Replace it with html, latex, etc.
   
   * After sphinx has finished you will find some .html files in the output path. This is your finished documentation. 




   .. _cntlm : http://cntlm.sourceforge.net/
   
   
           
           
   
   
   
   