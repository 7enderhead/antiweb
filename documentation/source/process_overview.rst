################
Process Overview
################

1. (once) setup sphinx documentation project with ``sphinx-quickstart``
#. create static content in reStructured Text (rst) files
#. let antiweb create dynamic content from source files into rst files
#. run sphinx to create documentation from rst sources

********************************
Bootstrap With sphinx-quickstart
********************************

- navigate to 
- ``sphinx-quickstart``
  
  - usually ok to accept default values

Optional: Add Graphviz Support
==============================

- edit ``conf.py`` in sphinx project's source folder
- add graphviz to the extensions list:

  .. code-block:: python
     
    extensions = ['...', 'sphinx.ext.graphviz']

***********************************
Create Dynamic Content with Antiweb
***********************************

   antiweb can process your :py:class:`Python`, :py:class:`C++`, :py:class:`C`, :py:class:`C#`, :py:class:`Clojure` and :py:class:`rst` files. If you would like to add other languages take a look at the `antiweb documentation`_.

Processing the files
====================

   You will most likely have a project consisting of more than one file. Fortunately that occasion is no problem for antiweb.

   ::

      antiweb.py /path/to/project -r

   This snippet will recursively process files in /path/to/project and put them into the directory you are currently working in.
   To put them in a seperate folder, use:

   ::

      antiweb.py /path/to/project -r -o foldername

   A folder will be created in your working directory and the processed files will be stored in there.


Final step: Create the documentation
====================================

Make sure all of your ``.rst`` files are stored inside the source folder and that they are registered inside the index.rst (which is also located inside your source folder)

The only thing to do now is to execute:

   ::

      make html

Sphinx should now be processing your files and put the finished documentation inside the ``build`` folder. From now on, only changed documents will be processed by Sphinx.
If you would like Sphinx to process all files everytime you run Sphinx, you have to edit the ``make.bat`` file and change:

   ::

      set ALLSPHINXOPTS= -d %BUILDDIR%/doctrees %SPHINXOPTS% source

to
   ::

      set ALLSPHINXOPTS=-E -d %BUILDDIR%/doctrees %SPHINXOPTS% source




   .. _antiweb documentation : antiweb.html#how-to-add-new-languages
   .. _Graphviz : installation.html#install-graphviz-optional
