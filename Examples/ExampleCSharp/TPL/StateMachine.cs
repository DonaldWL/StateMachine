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

      /* Used in ReturnValueDef. */
    public enum MO
    {
      Ok,                   /* ST OK */
      CodeBlockInvalid,     /* Code Block is invalid. */
      ExitedMainLoop,       /* Exited main while loop. */
      StateRValueInvalid,   /* State RValue is negative. */
      NoOtherWise,          /* No Otherwise defined and StateRValue out of range. */
      NextStateIndxInvalid  /* The state index from the table is out of range of */
                            /* the state table. */
    }

    public enum URValue
    {
      Ok,
      InDirErr,
      OutDirErr,
      InOutDirErr,
      NoFilesToProcess,
      InFileOpenError,
      OutFileOpenError,
      InFileReadError,
      OutFileWriteError,
      InFileCloseError,
      OutFileCloseError
    }

    /*
    * This is returned from ST_Run.
    *   MachineRValue
    *     Is the outcome from the state machine.  See
    *     enum MO for valid values
    *   Msg
    *     If not NULL is the message about the issue.
    *   UserRValue
    *     Is the user value that they wish to return.
    *     If the user code does not set this it will be
    *     -1.
    *   UserData
    *     Is the user date they wish to return.  This is
    *     a void pointer.  You will have to cast this.  If
    *     the user does not set this it will be NULL.
    */
    public struct ReturnValueDef
    {
      public MO MachineRValue;
      public string Msg;
      public URValue UserRValue;
      public string UserData;
    };
    public ReturnValueDef ReturnValue;

    private string InFileDir;
    private string OutFileDir;
    private bool ForceOverwrite;
    private StreamWriter TraceFh = null;
    private bool TraceFriendly;
    private StreamWriter LogFh = null;


    public CStateMachine(string _InFileDir, string _OutFileDir, bool _ForceOverwrite,
                         StreamWriter _TraceFh, bool _TraceFriendly, StreamWriter _LogFh)
    {
      InFileDir = _InFileDir;
      OutFileDir = _OutFileDir;
      ForceOverwrite = _ForceOverwrite;
      TraceFh = _TraceFh;
      TraceFriendly = _TraceFriendly;
      LogFh = _LogFh;
    }

    public int Run() {
      int CurStateIndx = CSMT.StartStateIndx;
      int PrevCurStateIndx = CSMT.StartStateIndx;
      int OtherWise = -1;
      int StateRValue = -1;
      bool ProcessStates = true;
      int FilesIndx = 0;
      string[] Files = { };
      string InFileName = "";
      string OutFileName = "";
      StreamReader InFileFh = null;
      StreamWriter OutFileFh = null;
      ReturnValue.MachineRValue = MO.Ok;
      ReturnValue.Msg = "";
      ReturnValue.UserRValue = URValue.Ok;
      ReturnValue.UserData = "";

      while (ProcessStates) {
        switch (CSMT.StateTable[CurStateIndx + (int) CSMT.STI.CBIdx]) {

            // StateRValue
            //   0 -> Ok
            //   1 -> InFileDir does not exist
            //        OutFileDir does not exist
            //        InFileDir and OutFileDir are the same
          case (int) CSMT.CB.StartMachine:
            StateRValue = 0;
            InFileDir = Path.GetFullPath(InFileDir);
            Log("Info", "InFileDir set to ", InFileDir);
            OutFileDir = Path.GetFullPath(OutFileDir);
            Log("Info", "OutFileDir set to ", OutFileDir);
            if (!Directory.Exists(InFileDir)) {
              StateRValue = 1;
              ReturnValue.UserData = Log("Error", "InFileDir (", InFileDir, 
                                         ") does not exist or is not a directory");
              ReturnValue.UserRValue = URValue.InDirErr;
            }
            if (!Directory.Exists(OutFileDir)) {
              StateRValue = 1;
              ReturnValue.UserData = Log("Error", "OutFileDir (", OutFileDir, 
                                         ") does not exist or is not a directory");
              ReturnValue.UserRValue = URValue.OutDirErr;
            }
            if (InFileDir == OutFileDir) {
              StateRValue = 1;
              ReturnValue.UserData = Log("Error", "InFileDir (", InFileDir, 
                                         ") is the same as OutFileDir (", OutFileDir, ")");
              ReturnValue.UserRValue = URValue.InOutDirErr;
            }
            break;

            // StateRValue
            //   0 -> Ok
            //   1 -> No files to process in InFileDir
          case (int) CSMT.CB.GetFiles:
            StateRValue = 0;
            FilesIndx = 0;
            Files = Directory.GetFiles(InFileDir, "*");
            Log("Info", "Number of files to process (", Files.Length, 
                ") from InFileDir (", InFileDir, ")");

            if (Files.Length == 0) {
              StateRValue = 1;
              ReturnValue.UserData = Log("Error", "No files found to process at InFileDir (", InFileDir, ")");
              ReturnValue.UserRValue = URValue.NoFilesToProcess;
            }
            break;

            // StateRValue
            //   0 -> Ok
            //   1 -> No more files to process
            //   2 -> Out file already exists and not in interactive mode
            //   3 -> Out File already exists and user stated overwrite the file
            //   4 -> User does not wish to overwrite file
            //   5 -> User wishes to skip file, or is a log file to skip.
          case (int) CSMT.CB.NextFile:
            StateRValue = 0;
            if (FilesIndx == Files.Length) {
              StateRValue = 1;
            } else {
              InFileName = Files[FilesIndx];

              if (LogFh != null) {
                if (LogFh.BaseStream is FileStream) {
                  FileStream fs = (FileStream) LogFh.BaseStream;
                  if (fs.Name == Files[FilesIndx]) {
                    // TODO: Add to other examples
                    Log("Info", "Skipping our LogFile (", fs.Name, ")");
                    StateRValue = 5;
                  }
                }
              }
              if (TraceFh != null) {
                if (TraceFh.BaseStream is FileStream) {
                  FileStream fs = (FileStream) TraceFh.BaseStream;
                  if (fs.Name == Files[FilesIndx]) {
                    // TODO: Add to other examples
                    Log("Info", "Skipping our TraceFile (", fs.Name, ")");
                    StateRValue = 5;
                  }
                }
              }

              FilesIndx++;
              if (StateRValue == 0) {
                // TODO: Handle 2-5
              }
            }
            break;

            // StateRValue
            //   0 -> Ok
            //   1 -> Unable to open in file
            //   2 -> Unable to open out file
          case (int) CSMT.CB.OpenFiles:
            StateRValue = 0;

            Log("Info", "Opening file InFile ", InFileName);
            try {
              InFileFh = new StreamReader(InFileName);
            } catch (IOException err) {
              ReturnValue.UserData = Log("Error", "Unable to open in file (", InFileName,
                                         ") => ", err.Message);
              ReturnValue.UserRValue = URValue.InFileOpenError;
              StateRValue = 1;
            }

            OutFileName = Path.Join(OutFileDir, Path.GetFileName(InFileName));
            Log("Info", "Opening file OutFile ", OutFileName);
            try {
              OutFileFh = new StreamWriter(OutFileName);
            } catch (IOException err) {
              StateRValue = 2;
              ReturnValue.UserData = Log("Error", "Unable to open out file (", OutFileName,
                                         ") => ", err.Message);
              ReturnValue.UserRValue = URValue.OutFileOpenError;
            }
            break;

            // StateRValue
            //   0 -> Ok
            //   1 -> Read error on InFile
            //   2 -> Write error on OutFile
          case (int) CSMT.CB.CopyFile:
            StateRValue = 0;
            string line;

            Log("Info", "Coping file (", InFileName, ") to (",
                OutFileName, ")");
            try {
              while ((line = InFileFh.ReadLine()) != null) {
                try { 
                  OutFileFh.WriteLine(line);
                } catch (IOException err) {
                  StateRValue = 2;
                  ReturnValue.UserData = Log("Error", "Unable to write out file (", OutFileName,
                      ") => ", err.Message);
                  ReturnValue.UserRValue = URValue.OutFileWriteError;
                }
              }
            } catch (IOException err) {
              StateRValue = 1;
              ReturnValue.UserData = Log("Error", "Unable to read in file (", InFileName,
                                         ") => ", err.Message);
              ReturnValue.UserRValue = URValue.InFileReadError;
            }
            break;

            // StateRValue
            //   0->Ok
            //   1->Unable to close in file
            //   2->Unable to close out file
          case (int)CSMT.CB.CloseFiles:
            StateRValue = 0;
            if (InFileFh != null) {
              Log("Info", "Closing file InFile ", InFileName);
              try { 
                InFileFh.Close();
              } catch (IOException err) {
                StateRValue = 1;
                ReturnValue.UserData = Log("Error", "Unable to close in file (", InFileName,
                                           ") => ", err.Message);
                ReturnValue.UserRValue = URValue.InFileCloseError;
              }
            }

            if (OutFileFh != null) {
              Log("Info", "Closing file OutFile ", OutFileName);
              try { 
                OutFileFh.Close();
              } catch (IOException err) {
                StateRValue = 2;
                ReturnValue.UserData = Log("Error", "Unable to close out file (", OutFileName,
                                           ") => ", err.Message);
                ReturnValue.UserRValue = URValue.OutFileCloseError;
              }
            }
            break;

          case (int) CSMT.CB.EndMachine:
            StateRValue = 0;
            ProcessStates = false;
            if (ReturnValue.UserData == "") {
              ReturnValue.UserData = "Ending State Machine";
            }
            Log("Info", ReturnValue.UserData);
            break;

          default:
            ReturnValue.MachineRValue = MO.CodeBlockInvalid;
            ReturnValue.Msg = "Invalid CodeBlock => State: " +
                              CSMT.StateNames[CSMT.StateTable[PrevCurStateIndx + (int) CSMT.STI.StateIdx]] +
                              "  CodeBlock: " +
                              CSMT.CodeBlockNames[CSMT.StateTable[PrevCurStateIndx + (int) CSMT.STI.CBIdx]] +
                              "  StateRValue: " + StateRValue;
            Log("Error", ReturnValue.Msg);
            ProcessStates = false;
            break;
        }

        if (StateRValue < 0) {
          ReturnValue.MachineRValue = MO.StateRValueInvalid;
          ReturnValue.Msg = "StateRValue is negative => State: " +
                             CSMT.StateNames[CSMT.StateTable[CurStateIndx + (int) CSMT.STI.StateIdx]] +
                             "  CodeBlock: " +
                             CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + (int) CSMT.STI.CBIdx]] +
                             "  StateRValue: " + StateRValue;
          Log("Error", ReturnValue.Msg);
          ProcessStates = false;
          break;
        }

        OtherWise = -1;
        if (StateRValue > CSMT.StateTable[CurStateIndx + (int)CSMT.STI.StateLenIdx])
        {
          OtherWise = CSMT.StateTable[CurStateIndx + (int) CSMT.STI.StateLenIdx + CSMT.StateTable[CurStateIndx + (int) CSMT.STI.StateLenIdx] + 1];
          if (OtherWise < 0) {
            ReturnValue.MachineRValue = MO.NoOtherWise;
            ReturnValue.Msg = "No Otherwise found => State: " +
                              CSMT.StateNames[CSMT.StateTable[CurStateIndx + (int) CSMT.STI.StateIdx]] +
                              "  CodeBlock: " +
                              CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + (int) CSMT.STI.CBIdx]] +
                              "  StateRValue: " + StateRValue;
            Log("Error", ReturnValue.Msg);
            ProcessStates = false;
            break;
          }
        }

        if (TraceFh != null) {
          if (TraceFriendly) {
            TraceFh.WriteLine("State Trace");
            TraceFh.WriteLine("  State:         {0}", 
                              CSMT.StateNames[CSMT.StateTable[CurStateIndx + (int) CSMT.STI.StateIdx]]);
            TraceFh.WriteLine("  CodeBlock:     {0}",
                              CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + (int) CSMT.STI.CBIdx]]);
            TraceFh.WriteLine("  StateRValue:   {0}\n", StateRValue);
          } else {
            TraceFh.WriteLine("{0}: {1},{2},{3}", DateTime.Now.ToString("yyyy-MM-dd HH:MM:ss"),
                              CSMT.StateNames[CSMT.StateTable[CurStateIndx + (int) CSMT.STI.StateIdx]],
                              CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + (int) CSMT.STI.CBIdx]],
                              StateRValue);
          }
        }

        PrevCurStateIndx = CurStateIndx;
        if (OtherWise > -1) {
          CurStateIndx = OtherWise;
        } else {
          CurStateIndx = CSMT.StateTable[CurStateIndx + (int) CSMT.STI.StatesIdx + StateRValue];
        }
        if (CurStateIndx > CSMT.STLen) {
          ReturnValue.MachineRValue = MO.NextStateIndxInvalid;
          ReturnValue.Msg = "Index into state table out of range => State: " +
                            CSMT.StateNames[CSMT.StateTable[PrevCurStateIndx + (int) CSMT.STI.StateIdx]] +
                            "  CodeBlock: " +
                            CSMT.CodeBlockNames[CSMT.StateTable[PrevCurStateIndx + (int) CSMT.STI.CBIdx]] +
                            "  StateRValue: " + StateRValue;
          Log("Error", ReturnValue.Msg);
          ProcessStates = false;
          break;
        }
      }

      if (ProcessStates) {
        ReturnValue.MachineRValue = MO.ExitedMainLoop;
        ReturnValue.Msg = "Exited the main loop => State: " +
                          CSMT.StateNames[CSMT.StateTable[CurStateIndx + (int) CSMT.STI.StateIdx]] +
                          "  CodeBlock: " +
                          CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + (int) CSMT.STI.CBIdx]] +
                          "  StateRValue: " + StateRValue;
        Log("Error", ReturnValue.Msg);
      }
      return 0;
    }

    private string Log(string _MsgType, params object[] list)
    {
      string Msg;
      string MsgBase = "";

      if (LogFh != null) {
        MsgBase = _MsgType + ": ";
        Msg = DateTime.Now.ToString("yyyy-MM-dd HH:MM:ss: ") + MsgBase;
        for (int i = 0; i < list.Length; i++) {
          Msg += list[i];
          MsgBase += list[i];
        }
        LogFh.WriteLine(Msg);
      }
      return MsgBase;
    }
  }
}
