Starting
--------

#########
XmlTest:
#########

- enumeration
   - item 1

comments without indentation
comment line 1
comment line 2

comments with indentation 
  comment line 1
  comment line 2

Code included:
==============

::

    
    <?xml version="1.0" encoding="UTF-8"?>
    <!-- code comment -->
    <note>
    <to>Tove</to>
    <from>Jani</from> 
    <heading>Reminder</heading>
    <body>Don't forget me this weekend!</body>
    </note>
    


Comments without indentation:
=============================
Spot difference between the block definitions of comments2 and comments3.
Comments2 uses a separate comment line for each specification, hence all white-spaces
are stripped -> no indentation.
 
comments2
  comments3                        
        