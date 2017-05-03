

this code file was created for testing the CSharpReader

The DocumentationSample type
demonstrates code comments.


The DocumentationSample type
provides no real functionality;
however, it does provide examples of
using the most common, built in
C# code comment xml tags.

DocumentationSample types are not
safe for access by concurrent threads.

Causes something happen.
someValue A String 
type representing some value.
ArgumentNullException 
if someValue  is null.

ArgumentException 
if someValue  is empty.

someValue  as passed in.


        testcomment


Blub


a new start block
the following xml comment block should be indented



::

    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    //starting namespace
    
    namespace Siemens.Simatic.HwConfiguration.Basics.Browsing.MetaMagic
    {
        /// <summary>
        /// describes a line in an iniFile
        /// by the LineContent and the LineNumber
        /// </summary>
        class Line
        {
            /*
                    another comment line
            */
            public string LineContent { get; set; }
    
            public int LineNumber { get; set; }
        }
    }

