///@start()

/*
testcomment
*/

//@include(test_area)

//@start(test_area)
///a new start block
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

