.. default-domain:: python

.. highlight:: python
   :linenothreshold: 6



############
Installation
############

The most important parts of the system are Python 3, antiweb and Sphinx. (It will be automatically installed with antiweb). Because of incompatibility with Python 2 you can't create 
documentations of Python 2 programs.


Overview of the installation steps:
===================================

   * Python
   * antiweb
   * Graphviz (Optional)
   
Install Python
==============

   Install Python 3.x, you can use this `link`_ to do so
   
   You should make sure that Python AND the Scripts folder inside Python are added to your PATH environment-variable so you can access them from everywhere 
   
Install antiweb
===============
   * After installing Python, run below command in cmd to install antiweb
   
   
   ::
   
       pip install git+https://github.com/7enderhead/antiweb.git@work
   
   
   :py:class:`IMPORTANT` If you get a connection error the reason is most likely your proxy. You then have to use a tool like `cntlm`_ and add a proxy flag when running pip, example:
   
   
   ::
   
       pip install git+https://github.com/7enderhead/antiweb.git@work --proxy http://localhost:8123
   

Install Graphviz (Optional)
===========================

   Graphviz can be used to generate graphs and images out of source code
   
   * Download the Graphviz msi installer from `here`_ and install it
   * Add the bin folder inside the Graphviz directory to your PATH variable


   .. _cntlm : http://cntlm.sourceforge.net/
   .. _link : https://www.python.org/downloads/
   .. _here: http://www.graphviz.org/Download_windows.php
   
           
           
   
   
   
   