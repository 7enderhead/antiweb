///@start()

///<summary>
///		this code file was created for testing the CSharpReader
///</summary>

///<summary>The <c>DocumentationSample</c> type
///demonstrates code comments.</summary>
///<remarks>
///    <para>
///        The <c>DocumentationSample</c> type
///        provides no real functionality;
///        however, it does provide examples of
///        using the most common, built in
///        <c>C#</c> code comment xml tags.
///    </para>
///    <para><c>DocumentationSample</c> types are not
///          safe for access by concurrent threads.</para>
///</remarks>

/// <summary>Causes something happen.</summary>
/// <param name="someValue">A <see cref="String"/>
///  type representing some value.</param>
/// <exception cref="ArgumentNullException">
///     if <paramref name="someValue"/> is <c>null</c>.
/// </exception>
/// <exception cref="ArgumentException">
///     if <paramref name="someValue"/> is <c>empty</c>.
/// </exception>
/// <returns><paramref name="someValue"/> as passed in.
/// </returns>

/*
        testcomment
*/

//@include(intro)
//@include(test_area)

/// @start(intro)
/// <summary>
/// <para>Blub</para>
/// </summary>
///
/// @(intro)

//@start(test_area)
///a new start block
//the following xml comment block should be indented


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

