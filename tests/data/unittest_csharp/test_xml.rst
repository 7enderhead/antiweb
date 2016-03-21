

this code file was created for testing the CSharpReader

parameter s parameterValue
returnvalue
Here's how you could make a second paragraph in a description. System.Console.WriteLine(System.String)  for information about output statements.
TestClass.Main 

testcomment

a new start block
the following xml comment block should be indented

    
    the complete comment block will be indented like the indentation of the first line in the block
    
    fileName the outputFileName
    on success: true, false otherwise
    See FileStream  for information about filestreams.


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

