///@start()

///<summary>
///		this code file was created for testing the CSharpReader
///</summary>
///<param name="parameter s">parameterValue</param>
///<returns>returnvalue</returns>
/// <para>Here's how you could make a second paragraph in a description. <see cref="System.Console.WriteLine(System.String)"/> for information about output statements.</para>
/// <seealso cref="TestClass.Main"/>

/*
testcomment
*/

//@include(test_area)

//@start(test_area)
///a new start block
//the following xml comment block should be indented

    ///<summary>
///the complete comment block will be indented like the indentation of the first line in the block
///</summary>
///<param name="fileName">the outputFileName</param>
///<returns>on success: true, false otherwise</returns>
///<para>See <see cref="FileStream"/> for information about filestreams.</para>

//@code
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
//@edoc
//@(test_area)

