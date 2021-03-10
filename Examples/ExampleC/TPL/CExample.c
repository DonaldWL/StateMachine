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

  Simple State machine program.
-----------------------------------------------------------------------------
*/
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "StateMachine.h"
#include "FileInfo.h"
#include "Converters.h"
#include "DList.h"

static bool StoreFile(const char *_fileName)
{
  if (IsFile(_fileName) && _fileName[0] != '.') return true;
  return false;
}

static void FileDListDeleter(void *_userData) {
  if (_userData != NULL) free(_userData);
}

int main()
{
  char *InFileDir = RealPath(".\\");               // Free memory
  char *OutFileDir = RealPath(".\\CopiedFiles\\"); // Free memory
  char *LogFileName = RealPath("..\\StateMachine.log\\"); // Free Memory
  FILE *TraceFh = NULL;
  CvtrValueDef *CvtrValues;                        // Free memory
  ReturnValueDef *ReturnValue;

  if (FileExist(OutFileDir) && !IsDir(OutFileDir)) {
    printf_s("CopiedFiles exists and is not a directory");
    exit(5);
  }

  if (FileExist(OutFileDir)) {
    DListDef *DFileList = NULL;  // Free memroy
    DFileList = ListFromDir(OutFileDir, StoreFile);
    char *FileName;
    while ((FileName = (char *)ReadDList(DFileList)) != NULL) {
      char *FullFileName = JoinPath(OutFileDir, FileName);
      if (IsDir(FullFileName)) {
        printf_s("Cannot remove %s because it contains a directory %s\n", OutFileDir, FileName);
        exit(6);
      }
      free(FullFileName);
    }
    while ((FileName = (char *)ReadDList(DFileList)) != NULL) {
      char *FullFileName = JoinPath(OutFileDir, FileName);
      int ret = remove(FullFileName);
      if (ret != 0) {
        char ErrText[1024];
        strerror_s(ErrText, 1024, errno);
        printf_s("Cannot remove %s because %s\n", FullFileName, ErrText);
        exit(7);
      }
      free(FullFileName);
    }
    char *ErrText = RemoveDir(OutFileDir);
    if (ErrText != NULL) {
      printf_s("Cannot remove %s because %s\n", OutFileDir, ErrText);
      free(ErrText);
      exit(7);
    }

    DropDList(DFileList, FileDListDeleter);
  }

  CreateDir(OutFileDir);

  errno_t err = fopen_s(&TraceFh, LogFileName, "w");

  clock_t begin = clock();
  ReturnValue = ST_Run(InFileDir, OutFileDir, false, TraceFh, true);
  clock_t end = clock();
  CvtrValues = ConvertMilliseconds(end - begin, true);
  printf("%uw %ud %uh %um %us %ums\n", CvtrValues->weeks, CvtrValues->days, CvtrValues->hours,
         CvtrValues->minutes, CvtrValues->seconds, CvtrValues->milliseconds);

    // This is not needed but good practice for C programming.
  free(InFileDir);
  free(OutFileDir);
  free(LogFileName);
  free(CvtrValues);
  ST_CleanReturnValue(ReturnValue);
  return 0;
}
