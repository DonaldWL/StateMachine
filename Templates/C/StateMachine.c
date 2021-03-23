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

  The State machine
-----------------------------------------------------------------------------
*/

#include <stdio.h> 
/*
#include <stdlib.h>
#include <string.h>
#include <stdbool.h> 
#include <ctype.h>
#include <time.h>
#include <stdarg.h>
*/

#include "StateMachine.h"
#include "StateMachineTables.h"


  /* Used to build up messages for the state machine.  It is manly for
   * errors.
   */
static char *BuildMsg(const char *MsgT, int CurStateIndx, int StateRValue);

  /* Used to log what the user code is doing.  This has nothing to do with
   * tracing the state machine
   */
static void Log(const char *_MsgType, int _ArgCnt, ...);

  /* Is the log file handle to use for logging.  This has nothing to do with
   * tracing the state machine.
   */
static FILE *LogFh = NULL;

void ST_Run(FILE *_TraceFh, FILE *_LogFh)
{
  FILE *TraceFh = _TraceFh;
  LogFh = _LogFh;

  int CurStateIndx = @@StartStateValue@@;
  int PrevCurStateIndx = CurStateIndx;
  int OtherWise = -1;
  int StateRValue = -1;
  bool ProcessStates = true;

  while (ProcessStates) {
    switch (StateTable[CurStateIndx + STI_CBIdx]) {


      default:
        ReturnValue->MachineRValue = MO_CodeBlockInvalid;
        char *Msg = BuildMsg("Invalid CodeBlock => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                             PrevCurStateIndx, StateRValue);
        Log("Error", 1, Msg);
        free(Msg);
        ProcessStates = false;
        break;
    }

    if (StateRValue < 0) {
      char *Msg = BuildMsg("StateRValue is negative => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                           CurStateIndx, StateRValue);
      Log("Error", 1, Msg);
      free(Msg);
      ProcessStates = false;
      break;
    }

    OtherWise = -1;
    if (StateRValue > StateTable[CurStateIndx + STI_StateLenIdx]) {
      OtherWise = StateTable[CurStateIndx + STI_StateLenIdx + StateTable[CurStateIndx + STI_StateLenIdx] + 1];
      if (OtherWise < 0) {
        char *Msg = BuildMsg("No Otherwise found => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                             CurStateIndx, StateRValue);
        Log("Error", 1, Msg);
        free(Msg);
        ProcessStates = false;
        break;
      }
    }

    if (TraceFh != NULL) {
      char *Msg;
      struct tm newtime;
      char tDateTime[30];

      time_t now = time(NULL);
      localtime_s(&newtime, &now);
      strftime(tDateTime, 30, "%F %T: ", &newtime);
      char RValue[20];
      _itoa_s(StateRValue, RValue, 20, 10);

        // Format is yyyy-mm-dd HH:MM:SS: <statename>,<codeblockname>,<StateRValue>
      Msg = StringBuild(NULL, 7, tDateTime, StateNames[StateTable[CurStateIndx + STI_StateIdx]], ",",
                        CodeBlockNames[StateTable[CurStateIndx + STI_CBIdx]], ",",
                        RValue, "\n");
      fprintf(TraceFh, Msg);
      free(Msg);
    }

    PrevCurStateIndx = CurStateIndx;
    if (OtherWise > -1) {
      CurStateIndx = OtherWise;
    } else {
      CurStateIndx = StateTable[CurStateIndx + STI_StatesIdx + StateRValue];
    }
    if (CurStateIndx > STLen) {
      char *Msg = BuildMsg("Index into state table out of range => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                           PrevCurStateIndx, StateRValue);
      Log("Error", 1, Msg);
      free(Msg);
      ProcessStates = false;
      break;
    }
  }

    /* If the user did not set to exit the loop then error */
  if (ProcessStates) {
    char *Msg = BuildMsg("Exited the main loop => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                         CurStateIndx, StateRValue);
    Log("Error", 1, Msg);
    free(Msg);
  }
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

static void Log(const char *_MsgType, int _ArgCnt, ...)
{
  char *Msg = NULL;
  struct tm newtime;
  char tDateTime[30];


  if (LogFh != NULL) {
    va_list args;
    va_start(args, _ArgCnt);

    time_t now = time(NULL);
    localtime_s(&newtime, &now);
    strftime(tDateTime, 30, "%F %T: ", &newtime);

    Msg = StringBuild(Msg, 3, tDateTime, _MsgType, ": ");
    Msg = StringBuildVaList(Msg, _ArgCnt, args);
    Msg = StringBuild(Msg, 1, "\n");
    fprintf(LogFh, Msg);
    va_end(args);
    free(Msg);
  }
}
