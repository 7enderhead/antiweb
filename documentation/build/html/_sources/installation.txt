.. default-domain:: python

.. highlight:: python
   :linenothreshold: 6

############
Installation
############

.. note:: antiweb cannot create documentation for Python 2.x programs

Overview of Installation Steps
==============================

- *Python* 3.x
- *antiweb*
- (optional) *graphviz* for graphics
   
Python Installation
===================

- install `Python 3.x <https://www.python.org/downloads/>`_
- add python and the python *scripts* folder to your path
   
antiweb Installation
====================

- install antiweb
- choose

  - latest official package from PyPI:
    
    - ``pip install antiweb``
  
  - latest stable development branch:
    
    - ``pip install git+https://github.com/7enderhead/antiweb.git@master``
  
  - latest cutting-edge unstable development branch:
    
    - ``pip install git+https://github.com/7enderhead/antiweb.git@work``

- antiweb also installs `Sphinx <http://www.sphinx-doc.org/>`_ as a dependency

.. note:: use a program like `cntlm <http://cntlm.sourceforge.net>`_ when you are in a corporate environment with centralized proxy infrastructure: `pip install [...] --proxy http://localhost:8123` or set your http_proxy environment variable

Graphviz Installation
=====================

- install `graphviz <http://www.graphviz.org>`_
- add the graphviz bin folder to your path
