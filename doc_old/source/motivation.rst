**************************************
Why another literate programming tool?
**************************************

Over the years I tried out several literate programming tools (cweb, funnelweb, leo and many more).
But all these tools suffer from several problems which are caused by 
the *book* approach: `web`_ was built to write primary a book and secondly
to get a program.  Donald Knuth is a professor who is used to publish papers,
from that point of view `web`_ is the perfect tool.

For a software developer the primary goal is a working, optimized program.
The second goal is good documentation for the fellow programmers to be able to
extend and maintain the code.

Most of the time a software developer spends for the following two tasks
(the *main development cycle*):

  * Test and debug program.
  * Adapt the code and start again testing.

And while `web`_ is a cool *top down* design tool. It is quite annoying to use it
during the *main development cycle*, because it needs several extra steps compared
to non literate programing: 

In non literate python programming the *main development cycle* is very fast: 
  * Start the program and test.
  * Find the bug.
  * Change the code.
  * Start the program again.

In literate python programming there are several more steps:
  * Start the program and test.
  * Find the bug in the tangled code.
  * Identify the buggy code in the web document.
  * Change the web document.
  * Tangle the new source code.
  * Start the program again.

The unnecessary extra steps slow down the productivity, which is probably
the cause that literate programming didn't become broadly accepted in 
professional computer programming. 

Another personal reason for my web dislike is: The tangled source code is not "mine",
but some canned text, which is polluted by sentinels. Most of my time during
the *main development cycle* I was spending with ugly generated code.


Why are document extractors like doxygen not sufficient?
========================================================

The results of doxygen, epidoc, etc. are like the tangle source code of
`web`_: It is a canned piece of text. But source code is a complex material.
Describing and explaining it cannot by done using a cookie cutter approach.



Features of antiweb
===================

Antiweb weaves restructured code from source code.

   * The source is partitioned in text blocks that can
     be freely arranged to generate the source.
   * Simple support for macros
   * Support for conditional weaving (i.e. base on the
     audience you can generate different outputs)
   * Supported languages: python, C/C++
   * Python doc string are supported.



.. _web: http://en.wikipedia.org/wiki/WEB

.. _sphinx document generator: http://sphinx.pocoo.org


