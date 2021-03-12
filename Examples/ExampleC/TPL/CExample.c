/*@@C@@*/
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
  char *InFileDir = RealPath("../../StateMachine/Examples/ExampleC/STM"); /* Free memory  */
  char *OutFileDir = RealPath("./CopiedFiles"); /* Free memory */
  char *TraceLogFileName = RealPath("./StateMachineTrace.log"); /* Free Memory */
  char *LogFileName = RealPath("./StateMachine.log"); /* Free Memory */
  FILE *TraceFh = NULL;
  FILE *LogFh = NULL;
  ReturnValueDef *ReturnValue;
  bool TraceFriendly = false;
  bool ForceOverwrite = false;

  if (FileExist(OutFileDir) && !IsDir(OutFileDir)) {
    printf_s("CopiedFiles exists and is not a directory");
    exit(5);
  }

    /* If we are not going to do a overwrite then lets clear it out */
  if (!ForceOverwrite && FileExist(OutFileDir)) {
    DListDef *DFileList = NULL;  /* Free memroy */
    DFileList = ListFromDir(OutFileDir, StoreFile);
    if (DFileList != NULL) {
      char *FileName;

        /* Make sure we do not have dirs in this directory, if fail */
      while ((FileName = (char *)ReadDList(DFileList)) != NULL) {
        if (IsDir(FileName)) {
          printf_s("Cannot remove %s because it contains a directory %s\n", OutFileDir, FileName);
          exit(6);
        }
      }

        /* No dirs, lets delete all the files */
      while ((FileName = (char *)ReadDList(DFileList)) != NULL) {
        int ret = remove(FileName);
        if (ret != 0) {
          char ErrText[1024];
          strerror_s(ErrText, 1024, errno);
          printf_s("Cannot remove %s because %s\n", FileName, ErrText);
          exit(7);
        }
      }
    }
    char *ErrText = RemoveDir(OutFileDir);
    if (ErrText != NULL) {
      printf_s("Cannot remove %s because %s\n", OutFileDir, ErrText);
      free(ErrText);
      exit(7);
    }

    DropDList(DFileList, FileDListDeleter);
  }

  if (!FileExist(OutFileDir)) CreateDir(OutFileDir);

    /* We should check the errors. */
  errno_t err = fopen_s(&TraceFh, TraceLogFileName, "w");
  err = fopen_s(&LogFh, LogFileName, "w");

  char SepLine[51];
  memset(SepLine, '-', 50*sizeof(char));
  SepLine[50] = '\0';
  printf("%s\n", SepLine);

    /* Lets do the run and capture how long it took */
  clock_t begin = clock();
  ReturnValue = ST_Run(InFileDir, OutFileDir, ForceOverwrite, TraceFh, TraceFriendly, LogFh);
  clock_t end = clock();

  printf("State Machine RValue (%u)\n", ReturnValue->MachineRValue);
  if (ReturnValue->Msg != NULL) {
    printf("State machine Msg (%s)\n", ReturnValue->Msg);
  } else {
    printf("State machine Msg ()\n");
  }
  printf("State Machine User RValue (%u)\n", ReturnValue->UserRValue);
  if (ReturnValue->UserData != NULL) {
    printf("State machine User Msg (%s)\n", ReturnValue->UserData);
  } else {
    printf("State machine User Msg ()\n");
  }
  printf("State machine duration (%u)\n", end-begin);
  printf("%s\n", SepLine);

    /* Close the log files */
  fclose(TraceFh);
  fclose(LogFh);

    /* This is not needed but good practice for C programming. */
  free(InFileDir);
  free(OutFileDir);
  free(TraceLogFileName);
  free(LogFileName);
  ST_CleanReturnValue(ReturnValue);
  return 0;
}
