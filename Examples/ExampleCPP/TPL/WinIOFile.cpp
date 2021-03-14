//@@CPP@@
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

  The windows implementation for IOFile.
-----------------------------------------------------------------------------
*/
#include <windows.h>
#include <io.h>
#include <stdio.h>
#include <filesystem>

constexpr auto BUFSIZE = 4096;

int GetFullPath(std::filesystem::path *Path)
{
  DWORD  retval = 0;
  TCHAR  buffer[BUFSIZE] = TEXT("");
  TCHAR** lppPart = { NULL };
  int LastError = 0;

  TCHAR * thepath = (TCHAR *)Path->c_str();

  retval = GetFullPathName(thepath, BUFSIZE, buffer, lppPart);
  LastError = GetLastError();
  if (retval != 0) {
    *Path = buffer;
    if (lppPart != NULL && *lppPart != 0) {
      *Path += *lppPart;
    }
  }

  return LastError;
}

bool IsAtty(FILE *Fh)
{
  if (!_isatty(_fileno(Fh))) {
    return false;
  }
  return true;
}
