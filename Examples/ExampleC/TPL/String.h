//@@C@@
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

  Some stuff to handle strings
-----------------------------------------------------------------------------
*/
#pragma once

#ifdef __cplusplus
extern "C" {
#endif

  // Find a given charactor in a string.
  // 
  //   <Indx> = FindChar(<String>, <Char>);
  //
  //     <Indx>
  //       Is the index into the <string> that contains the
  //       charactor.  If -1 then <Char> was not found.
  //     <String>
  //       Is the string to scan.
  //     <Char>
  //       Is the charactor to scan for.
extern size_t FindChar(const char* _string, const char _char);

  // Builds up a string for you.  It allocates memory as needed.
  //   
  //   <Msg> = StringBuild(<Msg>, <StringCnt>, ...)
  //
  //     <Msg>
  //       Should be the return and the first param.  You should
  //       not allocate space for Msg.  The memory is managed
  //       by the function.  First time you call this function
  //       <Msg> should be NULL.  You are responsible to free 
  //       this memory when you are done.
  //     <StringCnt>
  //       Is the number of strings that you pass in after
  //       <StringCnt>.
  //
  //  Example:
  //   
  //    #include <stdlib.h>
  //    #include <stdio.h>
  //
  //    #include "String.h"
  //
  //    int main()
  //    {
  //      char *Msg = NULL;
  //
  //        // Prints the "Hello Wordl!\n"
  //      Msg = StringBuild(Msg, 1, "Hello Wordl!\n");
  //      printf(Msg);
  //
  //        // Prints "Hello Wordl!\nHello Worlds!\nabb   cc\n"
  //      Msg = StringBuild(Msg, 4, "a", "bb   ", "cc", "\n");
  //      printf(Msg);
  //
  //        // Done with Msg lets free it.
  //      free(Msg);
  //      Msg = NULL;
  //
  //      exit(0);
  //    }
extern char *StringBuild(char *_msg, const int _stringCnt, ...);

  // Skip the white space.  It returns an index into <String> of
  // the first character that is not in <WhiteSpace>.  Starts 
  // from the beging of <String>.
  //
  //   <Index> = LSkipWhiteSpace(<String>, <WhiteSpace>);
  //     
  //     <Index>
  //       Is the index of the first charactor in <String>
  //       that is not <WhiteSpace>
  //     <String>
  //       Is the string to scan.
  //     <WhiteSpace>
  //       Is the white space to look for.  If NULL then it will 
  //       be " \t".
extern int LSkipWhiteSpace(const char *_string, const char *_whiteSpace);

  // Skips the white space from the right, starts at end of string.
  // 
  //   <Index> = LSkipWhiteSpace(<String>, <WhiteSpace>);
  //     
  //     <Index>
  //       Is the index of the first charactor from the end <String>
  //       that is not <WhiteSpace>
  //     <String>
  //       Is the string to scan.
  //     <WhiteSpace>
  //       Is the white space to look for.  If NULL then it will 
  //       be " \t".
extern int RSkipWhiteSpace(const char *_string, const char *_whiteSpace);

#ifdef __cplusplus
}
#endif
