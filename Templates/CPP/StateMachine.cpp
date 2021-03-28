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

  An example state machine that copies the files from one dir to another.
-----------------------------------------------------------------------------
*/
#include <stdarg.h>
#include <filesystem>

#include "StateMachine.h"

#define STRINGBLOCKLEN 128  // Size of our memeory for strings to allocate.


void CStateMachine::Run(void)
{
  int CurStateIndx = @@StartStateValue@@;
  int PrevCurStateIndx = CurStateIndx;
  int OtherWise = -1;
  int StateRValue = -1;
  bool ProcessStates = true;

  while (ProcessStates) {
    switch (StateTable[CurStateIndx + STI_CBIdx]) {

      @@CodeBlocks@@

      default:
        char *Msg = BuildMsg("Invalid CodeBlock => State: {SN}  CodeBlock: {BN}  StateRValue: {RV}",
                             PrevCurStateIndx, StateRValue);
        Log("Error", 1, Msg);
        free(Msg);
        ProcessStates = false;
        break;
    };

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
      struct tm newtime;
      time_t now = time(0);
      char buffer[30];
      localtime_s(&newtime, &now);
      strftime(buffer, 30, "%F %T: ", &newtime);

        // Format is yyyy-mm-dd HH:MM:SS: <statename>,<codeblockname>,<StateRValue>
      *TraceFh << buffer << StateNames[StateTable[CurStateIndx + STI_StateIdx]] << "," <<
                  CodeBlockNames[StateTable[CurStateIndx + STI_CBIdx]] << "," <<
                  StateRValue << std::endl;
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

std::string CStateMachine::Log(const char *_MsgType, int _ArgCnt, ...)
{
  std::string Msg;
  std::string MsgBase;
  struct tm newtime;
  char tDateTime[30];


  if (LogFileFh != nullptr) {
    va_list args;
    va_start(args, _ArgCnt);

    time_t now = time(NULL);
    localtime_s(&newtime, &now);
    strftime(tDateTime, 30, "%F %T: ", &newtime);

    Msg = tDateTime;
    Msg += _MsgType;
    MsgBase = _MsgType;
    Msg += ": ";
    MsgBase += ": ";

    for (int i = 0; i < _ArgCnt; i++) {
      char *arg = va_arg(args, char *);
      Msg += arg;
      MsgBase += arg;
    }
    *LogFileFh << Msg << std::endl;
    MsgBase += '\n';
    va_end(args);
  }
  return MsgBase;
}

char *CStateMachine::BuildMsg(const char *MsgT, int CurStateIndx, int StateRValue)
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

char *CStateMachine::StringBuild(char *_msg, const int _stringCnt, ...)
{
  va_list args;
  va_start(args, _stringCnt);
  _msg = StringBuildVaList(_msg, _stringCnt, args);
  va_end(args);
  return _msg;
}

char *CStateMachine::StringBuildVaList(char *_msg, const int _stringCnt, va_list args)
{
  char *string;
  size_t stringLen;
  size_t MsgLen;
  size_t MsgBlockLen;
  size_t NewMsgBlockLen;


    /* Setup the Msg. */
  if (_msg == NULL) {
    _msg = (char *) malloc(STRINGBLOCKLEN);
    _msg[0] = '\0';
    MsgLen = 0;
    MsgBlockLen = STRINGBLOCKLEN;
  } else {
    MsgLen = strlen(_msg);
    MsgBlockLen = ((MsgLen / STRINGBLOCKLEN) + 1) * STRINGBLOCKLEN;
  }

    /* Loop thru all the args */
  for (int i = 0; i < _stringCnt; i++) {
    string = va_arg(args, char *);
    stringLen = strlen(string);

      /* See if we need to increase are string size. */
    NewMsgBlockLen = MsgBlockLen;
    for (; MsgLen + stringLen + 1 > NewMsgBlockLen; NewMsgBlockLen += STRINGBLOCKLEN);
    if (MsgLen + stringLen + 1 > MsgBlockLen) {
      char *NewMsg = (char *) malloc(NewMsgBlockLen);
      memcpy(NewMsg, _msg, MsgBlockLen);
      MsgBlockLen = NewMsgBlockLen;
      free(_msg);
      _msg = NewMsg;
    }

      /* Concat the new string to the old string. */
    memcpy(&_msg[MsgLen], string, stringLen);
    _msg[MsgLen + stringLen] = '\0';
    MsgLen += stringLen;
  }

  va_end(args);
  return _msg;
}
