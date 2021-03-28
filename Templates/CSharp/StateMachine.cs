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
-----------------------------------------------------------------------------
*/
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace ExampleCSharp
{
  class CStateMachine
  {
    private StreamWriter TraceFh = null;
    private StreamWriter LogFh = null;


    public CStateMachine(StreamWriter _TraceFh, StreamWriter _LogFh)
    {
      TraceFh = _TraceFh;
      LogFh = _LogFh;
    }

    public void Run() {
      int CurStateIndx = @@StartStateValue@@;
      int PrevCurStateIndx = @@StartStateValue@@;
      int OtherWise = -1;
      int StateRValue = -1;
      bool ProcessStates = true;

      while (ProcessStates) {
        switch (CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]) {

          @@CodeBlocks@@

          default:
            string Msg = "Invalid CodeBlock => State: " +
                         CSMT.StateNames[CSMT.StateTable[PrevCurStateIndx + CSMT.STI_StateIdx]] +
                         "  CodeBlock: " +
                         CSMT.CodeBlockNames[CSMT.StateTable[PrevCurStateIndx + CSMT.STI_CBIdx]] +
                         "  StateRValue: " + StateRValue;
            Log("Error", Msg);
            ProcessStates = false;
            break;
        }

        if (StateRValue < 0) {
          string Msg = "StateRValue is negative => State: " +
                       CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]] +
                       "  CodeBlock: " +
                       CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]] +
                       "  StateRValue: " + StateRValue;
          Log("Error", Msg);
          ProcessStates = false;
          break;
        }

        OtherWise = -1;
        if (StateRValue > CSMT.StateTable[CurStateIndx + CSMT.STI_StateLenIdx])
        {
          OtherWise = CSMT.StateTable[CurStateIndx + CSMT.STI_StateLenIdx + CSMT.StateTable[CurStateIndx + CSMT.STI_StateLenIdx] + 1];
          if (OtherWise < 0) {
            string Msg = "No Otherwise found => State: " +
                         CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]] +
                         "  CodeBlock: " +
                         CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]] +
                         "  StateRValue: " + StateRValue;
            Log("Error", Msg);
            ProcessStates = false;
            break;
          }
        }

        if (TraceFh != null) {
          TraceFh.WriteLine("{0}: {1},{2},{3}", DateTime.Now.ToString("yyyy-MM-dd HH:MM:ss"),
                            CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]],
                            CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]],
                            StateRValue);
        }

        PrevCurStateIndx = CurStateIndx;
        if (OtherWise > -1) {
          CurStateIndx = OtherWise;
        } else {
          CurStateIndx = CSMT.StateTable[CurStateIndx + CSMT.STI_StatesIdx + StateRValue];
        }
        if (CurStateIndx > CSMT.STLen) {
          string Msg = "Index into state table out of range => State: " +
                       CSMT.StateNames[CSMT.StateTable[PrevCurStateIndx + CSMT.STI_StateIdx]] +
                       "  CodeBlock: " +
                       CSMT.CodeBlockNames[CSMT.StateTable[PrevCurStateIndx + CSMT.STI_CBIdx]] +
                       "  StateRValue: " + StateRValue;
          Log("Error", Msg);
          ProcessStates = false;
          break;
        }
      }

      if (ProcessStates) {
        string Msg = "Exited the main loop => State: " +
                     CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]] +
                     "  CodeBlock: " +
                     CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]] +
                     "  StateRValue: " + StateRValue;
        Log("Error", Msg);
      }
    }

    private string Log(string _MsgType, params object[] list)
    {
      string Msg;
      string MsgBase = "";

      MsgBase = _MsgType + ": ";
      Msg = DateTime.Now.ToString("yyyy-MM-dd HH:MM:ss: ") + MsgBase;
      for (int i = 0; i < list.Length; i++) {
        Msg += list[i];
        MsgBase += list[i];
      }
      if (LogFh != null) {
        LogFh.WriteLine(Msg);
      }
      return MsgBase;
    }
  }
}
