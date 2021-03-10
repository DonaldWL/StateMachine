//@@CopyFile@@
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
/*
SMS User Author:  Donald W. Long
SMS User Date:    01/22/2021
SMS User Version: 1.0
Creation Date:    03/07/21
SMS File Version: 1.0
TPL Date:         02/11/2021
TPL Author:       Donald W. Long (Donald.W.Long@gmail.com)
-----------------------------------------------------------------------------
Description:

  Some stuff to handle strings
-----------------------------------------------------------------------------
*/
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>

#include "String.h"

// This is how big each block length is.  When more
// memory is needed it is allocated in this increament.
#define STRINGBLOCKLEN 128

char *StringBuild(char *_msg, const int _stringCnt, ...)
{
  char *string;
  size_t stringLen;
  size_t MsgLen;
  size_t MsgBlockLen;
  size_t NewMsgBlockLen;

  va_list args;
  va_start(args, _stringCnt);

    // Setup the Msg.
  if (_msg == NULL) {
    _msg = malloc(STRINGBLOCKLEN);
    _msg[0] = '\0';
    MsgLen = 0;
    MsgBlockLen = STRINGBLOCKLEN;
  } else {
    MsgLen = strlen(_msg);
    MsgBlockLen = ((MsgLen / STRINGBLOCKLEN) + 1) * STRINGBLOCKLEN;
  }

    // Loop thru all the args
  for (int i = 0; i < _stringCnt; i++) {
    string = va_arg(args, char *);
    stringLen = strlen(string);

      // See if we need to increase are string size.
    NewMsgBlockLen = MsgBlockLen;
    for (; MsgLen + stringLen + 1 > NewMsgBlockLen; NewMsgBlockLen += STRINGBLOCKLEN);
    if (MsgLen + stringLen + 1 > MsgBlockLen) {
      char *NewMsg = malloc(NewMsgBlockLen);
      memcpy(NewMsg, _msg, MsgBlockLen);
      MsgBlockLen = NewMsgBlockLen;
      free(_msg);
      _msg = NewMsg;
    }

      // Concat the new string to the old string.
    memcpy(&_msg[MsgLen], string, stringLen);
    _msg[MsgLen + stringLen] = '\0';
    MsgLen += stringLen;
  }

  va_end(args);
  return _msg;
}

size_t FindChar(const char *_string, const char _char)
{
  size_t Len = strlen(_string);
  size_t Indx = 0;
  for (; Indx < Len && _string[Indx] != _char; Indx++);
  if (_string[Indx] != _char) return -1;
  return Indx;
}

int LSkipWhiteSpace(const char *_string, const char *_whiteSpace)
{
  const char DefaultWhiteSpace[] = " \t";
  const char *WhiteSpace = DefaultWhiteSpace;
  size_t StringLen = strlen(_string);
  size_t WhiteSpaceLen;
  int Indx = 0;

  if (_whiteSpace != NULL) WhiteSpace = _whiteSpace;
  WhiteSpaceLen = strlen(WhiteSpace);

  while (Indx < (int) StringLen) {
    int i;
    for (i = 0; i < (int) WhiteSpaceLen && _string[Indx] != WhiteSpace[i]; i++);
    if (i == WhiteSpaceLen) break;
    Indx++;
  }

  if (Indx == (int) StringLen) return -1;
  return Indx;
}

int RSkipWhiteSpace(const char *_string, const char *_whiteSpace)
{
  const char DefaultWhiteSpace[] = " \t";
  const char *WhiteSpace = DefaultWhiteSpace;
  size_t StringLen = strlen(_string);
  size_t WhiteSpaceLen;
  int Indx = (int) (StringLen - 1);

  if (_whiteSpace != NULL) WhiteSpace = _whiteSpace;
  WhiteSpaceLen = strlen(WhiteSpace);

  while (Indx != -1) {
    int i;
    for (i = 0; i < (int) WhiteSpaceLen && _string[Indx] != WhiteSpace[i]; i++);
    if (i == WhiteSpaceLen) break;
    Indx--;
  }

  return Indx;
}
