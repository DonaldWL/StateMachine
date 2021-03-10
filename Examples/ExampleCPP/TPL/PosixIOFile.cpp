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

  The posix implementationfor IOFile
-----------------------------------------------------------------------------
*/
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <filesystem>

int GetFullPath1(std::filesystem::path *Path) {
  char buffer[PATH_MAX + 1];
  char *ptr;

  ptr = realpath(Path->c_str(), buffer);
  if (ptr != nullptr) {
    *Path = ptr;
    return 0;
  }
  return 1;
}

bool IsAtty(FILE *Fh)
{
  if (!isatty(Fh)) {
    return false;
  }
  return true;
}
