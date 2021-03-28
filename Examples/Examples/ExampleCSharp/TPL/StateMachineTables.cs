/*@@CSharp@@*/
/*
SMS User Author:  @@SMSUserAuthor@@
SMS User Date:    @@SMSUserDate@@
SMS User Version: @@SMSUserVersion@@
Creation Date:    @@CreationDate@@
SMS File Version: @@SMSFileVersion@@  
TPL Date:         02/11/2021
TPL Author:       Donald W. Long (Donald.W.Long@gmail.com)
-----------------------------------------------------------------------------
CopyRight:

    Copyright (C) 2020-2021  Donald W. Long (Donald.W.Long@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-----------------------------------------------------------------------------
Description:

  An example state machine that copies the files from one dir to another.
  This is all the generated variables and tables for the state machine.
-----------------------------------------------------------------------------
*/
using System;
using System.Collections.Generic;
using System.Text;

namespace ExampleCSharp
{
  class CSMT
  {
    //@@CodeBlockNames:4@@
    
    //@@CodeBlockValues:4@@
    public static readonly int CBLen = 7; //@@RemoveLine@@
    public static readonly string[] CodeBlockNames = { "CloseFiles", "CopyFile" }; //@@RemoveLine@@
    public enum CB { CloseFiles = 0, CopyFile = 1 }; //@@RemoveLine@@

    //@@StateNames:4@@
    
    //@@StateValues:4@@
    public static int SNLen = 8; //@@RemoveLine@@
    public static string[] StateNames = { "CloseFiles", "CloseFilesError" }; //@@RemoveLine@@
    public enum ST { CloseFiles = 0, CloseFilesError = 1 }; //@@RemoveLine@@
    public static readonly int CB_CloseFiles = 0; //@@RemoveLine@@
    public static readonly int CB_CopyFile = 1; //@@RemoveLine@@

    //@@STIValues:4@@

    //@@StateTable:4@@
    
    //@@StartState:4@@
    //@@EndState:4@@
    public static int STLen = 55; //@@RemoveLine@@
    public static int[] StateTable = { (int) CB.CloseFiles, (int) ST.CloseFiles, 3, 32, 21, 21, -1 }; //@@RemoveLine@@
    public static int StartStateIndx = 49; //@@RemoveLine@@
    public static int EndStateIndx = 21; //@@RemoveLine@@
  }
}
