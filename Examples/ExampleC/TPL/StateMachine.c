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

  The State machine
-----------------------------------------------------------------------------
*/

#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
#include <stdbool.h> 
#include <ctype.h>
#include <time.h>

#include "String.h"
#include "DList.h"
#include "FileInfo.h"
#include "StateMachine.h"
#include "StateMachineTables.h"


static char *BuildMsg(const char *MsgT, int CurStateIndx, int StateRValue);
static bool StoreFile(const char *_fileName);
static bool PrintError(char *ErrMsg);
static bool PrintWarning(char *WarningMsg);

ReturnValueDef *ST_Run(const char *_InFileDir, const char *_OutFileDir, bool _ForceOverwrite,
                       FILE *_TraceFh, bool _TraceFriendly) 
{
  char *InFileDir = NULL;      // Free memory
  PathDef *InFilePath = NULL;  // Free memory
  FILE *InFileFh = NULL;       // Close file   
  char *OutFileDir = NULL;     // Free memory
  PathDef *OutFilePath = NULL; // Free memory
  FILE *OutFileFh = NULL;      // Close File
  DListDef *DFileList = NULL;  // Free memroy
  bool ForceOverwrite = _ForceOverwrite;
  FILE *TraceFh = _TraceFh;
  bool TraceFriendly = _TraceFriendly;
  ReturnValueDef *ReturnValue = malloc(sizeof(ReturnValueDef)); // Do not free, its returned

  int CurStateIndx = StartStateIndx;
  int PrevCurStateIndx = CurStateIndx;
  int OtherWise = -1;
  int StateRValue = -1;
  bool ProcessStates = true;
  bool LoopError = true;

  ReturnValue->MachineRValue = MO_Ok;
  ReturnValue->Msg = NULL;
  ReturnValue->UserRValue = -1;
  ReturnValue->UserData = NULL;

  while (ProcessStates) {
    switch (StateTable[CurStateIndx + STI_CBIdx]) {

      // StateRValue
      //   0 -> Ok
      //   1 -> InFileDir does not exist
      //        OutFileDir does not exist
      //        InFileDir and OutFileDir are the same
      case CB_StartMachine:
        StateRValue = 0;
        if (_InFileDir != NULL) {
          InFileDir = RealPath(_InFileDir);
        } else {
          InFileDir = CurDir();
        }

        if (_OutFileDir != NULL) {
          OutFileDir = RealPath(_OutFileDir);
        } else {
          OutFileDir = CurDir();
        }

        if (!FileExist(InFileDir) || !IsDir(InFileDir)) {
          StateRValue = 1;
        } else if (!FileExist(OutFileDir) || !IsDir(OutFileDir)) {
          StateRValue = 1;
        } else if (OutFileDir == InFileDir) {
          StateRValue = 1;
        }
        break;

        // StateRValue
        //   0 -> Ok
        //   1 -> No files to process in InFileDir
      case CB_GetFiles:
        StateRValue = 0;
        DFileList = ListFromDir(InFileDir, StoreFile);
        if (DFileList == NULL) StateRValue = 1;
        break;

        // StateRValue
        //   0 -> Ok
        //   1 -> No more files to process
        //   2 -> Out file already exists and not in interactive mode
        //   3 -> Out File already exists and user stated overwrite the file
        //   4 -> User does not wish to overwrite file
        //   5 -> User wishes to skip file
      case CB_NextFile:
        {
          StateRValue = 0;
          char *FileName = (char *)ReadDList(DFileList);
          if (FileName == NULL) StateRValue = 1;
          else {
            FileName = JoinPath(InFileDir, FileName);
            InFilePath = SplitPath(FileName, false);
            free(FileName);

            FileName = JoinPath(OutFileDir, InFilePath->FileName);
            OutFilePath = SplitPath(FileName, false);
            free(FileName);
            if (FileExist(OutFilePath->FullPath)) {
              char *Msg;
              if (!IsAtty(stdin)) {
                Msg = StringBuild(NULL, 3, "Out File (", OutFilePath->FullPath,
                                  ") exists and not in interactive mode");
                PrintError(Msg);
                ReturnValue->UserRValue = 1;
                StateRValue = 2;
              } else {
                char YesNo[20];
                while (true) {
                  Msg = StringBuild(NULL, 3, "Out File (", OutFilePath->FullPath,
                                    ") exists, overwrite (Y|N|S)? ");
                  printf(Msg);
                  free(Msg);
                  fgets(YesNo, 20, stdin);
                  char *p = YesNo;
                  for (; *p; ++p) *p = tolower(*p);
                  if (strcmp(YesNo, "y") == 0) {
                    Msg = StringBuild(NULL, 2, "Overwriting file (", OutFilePath->FullPath);
                    PrintWarning(Msg);
                    StateRValue = 3;
                  } else if (strcmp(YesNo, "n") == 0) {
                    Msg = StringBuild(NULL, 3, "User does not wont to overwrite file (", OutFilePath->FullPath,
                                      ") ending program");
                    PrintWarning(Msg);
                    StateRValue = 4;
                    break;
                  } else if (strcmp(YesNo, "s") == 0) {
                    StateRValue = 5;
                    break;
                  }
                  Msg = StringBuild(NULL, 3, "\nInvalid response to question (", YesNo,
                                    ")  must be (Y|N|S)\n");
                  printf(Msg);
                  free(Msg);
                }
              }
            }
          } 
        }
        break;

        // StateRValue
        //   0 -> Ok
        //   1 -> Unable to open in file
        //   2 -> Unable to open out file
      case CB_OpenFiles:
        {
          StateRValue = 0;
          InFileFh = NULL;
          errno_t err = fopen_s(&InFileFh, InFilePath->FullPath, "r");
          if (err == 0) {
            OutFileFh = NULL;
            err = fopen_s(&OutFileFh, OutFilePath->FullPath, "w");
            if (err != 0) {
              char *Msg;
              char ErrText[1024];
              strerror_s(ErrText, 1024, errno);

              Msg = StringBuild(NULL, 4, "Unable to open out file (", OutFilePath->FullPath,
                                ") => ", ErrText);
              PrintError(Msg);
              ReturnValue->UserRValue = 1;
              StateRValue = 2;
            }
          } else {
            char *Msg;
            char ErrText[1024];
            strerror_s(ErrText, 1024, errno);

            Msg = StringBuild(NULL, 4, "Unable to open in file (", InFilePath->FullPath,
                              ") => ", ErrText);
            PrintError(Msg);
            ReturnValue->UserRValue = 1;
            StateRValue = 1;
          }
        }
        break;

        // StateRValue
        //   0 -> Ok
        //   1 -> Read error on InFile
        //   2 -> Write error on OutFile
      case CB_CopyFile:
        {
          StateRValue = 0;
          char Line[1028];
          char *xLine;
          int LineCnt;
          while (!feof(InFileFh)) {
            xLine = fgets(Line, 1024, InFileFh);
            if (xLine == NULL) continue;  // No more data.
            if (ferror(InFileFh)) {
              char *Msg;
              char ErrText[1024];
              strerror_s(ErrText, 1024, errno);

              Msg = StringBuild(NULL, 4, "Unable to read in file (", InFilePath->FullPath,
                                ") => ", ErrText);
              PrintError(Msg);
              ReturnValue->UserRValue = 1;
              StateRValue = 1;
              break;
            }

            LineCnt = fprintf(OutFileFh, Line);
            if (LineCnt < 0) {
              char *Msg;
              char ErrText[1024];
              strerror_s(ErrText, 1024, errno);

              Msg = StringBuild(NULL, 4, "Unable to write out file (", OutFilePath->FullPath,
                                ") => ", ErrText);
              PrintError(Msg);
              ReturnValue->UserRValue = 1;
              StateRValue = 2;
              break;
            }
          }
        }
        break;

        // StateRValue
        //   0->Ok
        //   1->Unable to close in file
        //   2->Unable to close out file
      case CB_CloseFiles:
        StateRValue = 0;
        if (InFileFh != NULL) fclose(InFileFh);
        InFilePath = SplitPathClean(InFilePath);
        if (OutFileFh != NULL) fclose(OutFileFh);
        OutFilePath = SplitPathClean(OutFilePath);

        InFileFh = NULL;
        OutFileFh = NULL;
        break;

        // End the state machine.  We return from this.
      case CB_EndMachine:
        ReturnValue->UserRValue = 0;
        ReturnValue->UserData = (void *) StringBuild(NULL, 1, "We Did It");
        ProcessStates = false;
        LoopError = false;
        break;

      default:
        ReturnValue->MachineRValue = MO_CodeBlockInvalid;
        ReturnValue->Msg = BuildMsg("Invalid CodeBlock => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                                    PrevCurStateIndx, StateRValue);
        ProcessStates = false;
        LoopError = false;
        break;
    }

    if (StateRValue < 0) {
      ReturnValue->MachineRValue = MO_StateRValueInvalid;
      ReturnValue->Msg = BuildMsg("StateRValue is negative => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                                  CurStateIndx, StateRValue);
      ProcessStates = false;
      LoopError = false;
      break;
    }

    OtherWise = -1;
    if (StateRValue > StateTable[CurStateIndx + STI_StateLenIdx]) {
      OtherWise = StateTable[CurStateIndx + STI_StateLenIdx + StateTable[CurStateIndx + STI_StateLenIdx] + 1];
      if (OtherWise < 0) {
        ReturnValue->MachineRValue = MO_NoOtherWise;
        ReturnValue->Msg = BuildMsg("No Otherwis found => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                                    CurStateIndx, StateRValue);
        ProcessStates = false;
        LoopError = false;
        break;
      }
    }

    if (TraceFh != NULL) {
      if (TraceFriendly) {
        char *Msg;
        char RValue[20];

        _itoa_s(StateRValue, RValue, 20, 10);
        Msg = StringBuild(NULL, 9, "State Trace\n  State:         ",
                          StateNames[StateTable[CurStateIndx + STI_StateIdx]], "\n",
                           "  CodeBlock:     ",
                           CodeBlockNames[StateTable[CurStateIndx + STI_CBIdx]], "\n",
                           "  StateRValue:   ", RValue, "\n\n");
        fprintf(TraceFh, Msg);
        free(Msg);
      } else {
        char *Msg;
        struct tm newtime;
        char tDataTime[30];

        time_t now = time(NULL);
        localtime_s(&newtime, &now);
        strftime(tDataTime, 30, "%F %T: ", &newtime);
        char RValue[20];
        _itoa_s(StateRValue, RValue, 20, 10);

          // Format is yyyy-mm-dd HH:MM:SS: <statename>,<codeblockname>,<StateRValue>
        Msg = StringBuild(NULL, 7, tDataTime, StateNames[StateTable[CurStateIndx + STI_StateIdx]], ",",
                          CodeBlockNames[StateTable[CurStateIndx + STI_CBIdx]], ",",
                          RValue, "\n");
        fprintf(TraceFh, Msg);
        free(Msg);
      }
    }

    PrevCurStateIndx = CurStateIndx;
    if (OtherWise > -1) {
      CurStateIndx = OtherWise;
    } else {
      CurStateIndx = StateTable[CurStateIndx + STI_StatesIdx + StateRValue];
    }
    if (CurStateIndx > STLen) {
      ReturnValue->MachineRValue = MO_NextStateIndxInvalid;
      ReturnValue->Msg = BuildMsg("Index into state table out of range => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                                  PrevCurStateIndx, StateRValue);
      ProcessStates = false;
      LoopError = false;
      break;
    }
  }

    // Make sure the files are closed.
  if (InFileFh != NULL) fclose(InFileFh);
  if (OutFileFh != NULL) fclose(OutFileFh);

    // Free all the required memory.
  if (InFileDir != NULL) free(InFileDir);
  if (OutFileDir != NULL) free(OutFileDir);
  SplitPathClean(InFilePath);
  SplitPathClean(OutFilePath);
  DropDList(DFileList, FileDListDeleter);

  if (LoopError) {
    ReturnValue->MachineRValue = MO_ExitedMainLoop;
    ReturnValue->Msg = BuildMsg("Exited the main loop => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                                CurStateIndx, StateRValue);
  }

  return ReturnValue;
}

ReturnValueDef *ST_CleanReturnValue(ReturnValueDef *_ReturnValue) 
{
  if (_ReturnValue != NULL) {
    if (_ReturnValue->Msg != NULL) free(_ReturnValue->Msg);
    if (_ReturnValue->UserData != NULL) free(_ReturnValue->UserData);
    free(_ReturnValue);
  }
  return NULL;
}

static bool PrintError(char *ErrMsg) {
  char *Msg = StringBuild(NULL, 3, "ERROR: ", ErrMsg, "\n");
  free(ErrMsg);
  printf(Msg);
  free(Msg);
  return true;
}

static bool PrintWarning(char *WarningMsg) {
  char *Msg = StringBuild(NULL, 3, "WARNING: ", WarningMsg, "\n");
  free(WarningMsg);
  printf(Msg);
  free(Msg);
  return true;
}

static char *BuildMsg(const char *MsgT, int CurStateIndx, int StateRValue)
{
  char *Msg = NULL;
  char TMsg[101] = "";
  size_t TMsgLen = 0;
  char Cmd[101] = "";
  size_t MsgTLen = strlen(MsgT);
  size_t MsgIndx = 0;

  Msg = StringBuild(Msg, 1, "ERROR: ");

  for (size_t i = 0; i < MsgTLen; i++) {
    if (MsgT[i] == '{') {
      size_t StrtCmd = i + 1;
      size_t ii;
      for (i += 1, ii = 0; i < MsgTLen && MsgT[i] != '}' && ii < 100; i++, ii++) {
        Cmd[ii] = MsgT[i];
      }
      Cmd[ii + 1] = '\0';
      if (MsgT[i] == '}' && ii < 100) {
        if (TMsgLen != 0) {
          TMsg[TMsgLen] = '\0';
          Msg = StringBuild(Msg, 1, TMsg);
          TMsgLen = 0;
        }
        if (!strcmp(Cmd, "SN")) {
          Msg = StringBuild(Msg, 1, StateNames[StateTable[CurStateIndx + STI_StateIdx]]);
        } else if (!strcmp(Cmd, "BN")) {
          Msg = StringBuild(Msg, 1, CodeBlockNames[StateTable[CurStateIndx + STI_StateIdx]]);
        } else if (!strcmp(Cmd, "RV")) {
          char StateRValueString[100];
          _itoa_s(StateRValue, StateRValueString, 100, 10);
          Msg = StringBuild(Msg, 1, StateRValueString);
        } else {
          TMsg[TMsgLen] = '{';
          TMsgLen++;
          i = StrtCmd - 1;
        }
      } else {
        if (TMsgLen != 0) {
          TMsg[TMsgLen] = '\0';
          Msg = StringBuild(Msg, 1, TMsg);
          TMsgLen = 0;
        }
        Msg = StringBuild(Msg, 1, &MsgT[StrtCmd - 1]);
        break;
      }
    } else {
      if (TMsgLen == 100) {
        TMsg[TMsgLen] = '\0';
        Msg = StringBuild(Msg, 1, TMsg);
        TMsgLen = 0;
      }
      TMsg[TMsgLen] = MsgT[i];
      TMsgLen++;
    }
  }

  if (TMsgLen != 0) {
    TMsg[TMsgLen] = '\0';
    Msg = StringBuild(Msg, 1, TMsg);
  }
  return Msg;
}

static bool StoreFile(const char *_fileName) 
{
  if (IsFile(_fileName) && _fileName[0] != '.') return true;
  return false;
}
