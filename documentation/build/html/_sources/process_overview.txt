.. default-domain:: python

.. highlight:: python
   :linenothreshold: 6



################
Process overview
################

There are some steps one has to make to create a documentation from a project or single file. The following overview will explain how to successfully create a documentation.

.. csv-table::
   :header: "Common steps in order of execution"

   Use antiweb to create rst files and add them manually to Sphinx' index.rst
   Execute sphinx-quickstart to create a project
   Execute make html
   Enjoy the documentation

**********************************
Creating rst files through antiweb
**********************************

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

**************************************
Creating the documentation with Sphinx
**************************************

   Before you are able to use Sphinx to build your documentation, you have to set up a project.

Creating a new Sphinx project
=============================

   Navigate to the folder you want to be the root of your project. During the following steps, Sphinx will generate all necessary files
   and folders in here. To generate the project, type:

   ::

      sphinx-quickstart

   You will then be guided through the project setup. There are some important steps:

   .. csv-table::

      For the root path just accept the default value
      You should accept to seperate source and build
      Use ``.rst`` as the source file suffix
      Accept ``index`` as the master document
      Accept the creation of a Makefile
      Accept the creation of a Windows command file

   All other settings are up to you

Configuring the new project
===========================

Depending on what you would like to do with your project, there are many possibilities. In this example we will be including `Graphviz`_ digraphs.

To do that, we navigate to the conf.py file inside the source folder. Inside of that file, we add ``'sphinx.ext.graphviz'`` to the extensions list.
Given that your ``.rst`` documents contain Graphviz code, Sphinx should now interpret them correctly.

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
