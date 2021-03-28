//@@CPP@@
#pragma once
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

#include <iostream>
#include <filesystem>
#include <fstream>
#include <list>

//===================================================================
// Main class for the statemachine.  
//
//  @@ClassName@@ StateMachine();
//
//    Run(std::ostream &TraceFh, bool Trace = true, bool TraceFriendly = false)
//      Runs the state macnine.  All the exceptions can be thrown
//      by this method.
//
//      TraceFh
//        Is a std::ostream to write the trace data to.  Trace
//        must be true
//      Trace
//        If true then trace the state machine.  This will create
//        a lot of data to the TraceFh.
//
//      TraceFriendly
//        If true will output the trace in a more readable layout.
//        This will create a lot of data in your trace file.
//
//        Non Friendly
//          Each line in your TraceFh file will have the following.
//          This is better if you wish to process the data with
//          another program or keep the file as small as possible.
//
//            <StateName>,<StateIndx>,<CodeBlockName>,<StateRValue>,<OtherWise>
//  
//        Friendly
//          Each trace of the state will produce many lines in your
//          TraceFh file.
//
//            State Trace
//              State:         <StateName>
//              StateTableIdx: <StateIndx>
//              CodeBlock:     <CodeBlockName>
//              StateRValue:   <StateRValue>
//              OtherWiseUsed: <OtherWise>
//===================================================================

class CStateMachine
{
public:
  std::filesystem::path InFileDir;
  std::filesystem::path InFileName;
  std::ifstream InFileFh;
  std::filesystem::path OutFileDir;
  std::filesystem::path OutFileName;
  std::ofstream OutFileFh;
  bool ForceOverwrite;
  std::ostream *TraceFh;
  bool TraceFriendly;
  std::list <std::filesystem::path> Files;
  std::ostream *LogFileFh;
  bool Error = false;

    // Used in ReturnValueDef.
  enum MO {
    MO_Ok = 0,                   // ST OK
    MO_CodeBlockInvalid = 1,     // Code Block is invalid.
    MO_ExitedMainLoop = 2,       // Exited main while loop.
    MO_StateRValueInvalid = 3,   // State RValue is negative.
    MO_NoOtherWise = 4,          // No Otherwise defined and StateRValue out of range.
    MO_NextStateIndxInvalid = 5  // The state index from the table is out of range of
                                 // the state table.
  };

    // This is returned from Run.
    //   MachineRValue
    //     Is the outcome from the state machine.  See
    //     enum MO for valid values
    //   Msg
    //     If not NULL is the message about the issue.
    //   UserRValue
    //     Is the user value that they wish to return.
    //     If the user code does not set this it will be
    //     -1.
    //   UserData
    //     Is the user date they wish to return.  This is
    //     a void pointer.  You will have to cast this.  If
    //     the user does not set this it will be NULL.
  struct {
    enum MO MachineRValue;
    std::string Msg;
    int UserRValue;
    std::string UserData;
  } ReturnValue;

  // Constructor for the class.
  //
  //   _InFileDir
  //     Is the directory to copy from.  Does not have to be fully qualified
  //   _OutFileDir
  //     Is the directory to copy to.  Does not have to be fully qualified
  //   _ForcOverwrite
  //     If true write over the _OutFileDir files without prompting.
  //   _TraceFh
  //     If not equal to NULL then trace the state machine.
  //   _TraceFriendly
  //     If true will outpu a friendly type trace, but takes up a lot of
  //     space.  For log files recommend this to be false.
  //   _LogFh
  //     If not equal to NULL then log what the user code is doing.
  CStateMachine(std::filesystem::path InFileDir, std::filesystem::path OutFileDir, bool ForceOverwrite,
                std::ostream *TraceFh, bool TraceFriendly, std::ostream *LogFileFh) :
                  InFileDir(InFileDir), OutFileDir(OutFileDir), ForceOverwrite(ForceOverwrite),
                  TraceFh(TraceFh), TraceFriendly(TraceFriendly), LogFileFh(LogFileFh) {};

    // This is how you run the statemachine.  When it returns you need to validate
    // its outcome.  To check its results, see ReturnValue
  int Run(void);

private:
  CStateMachine();

  std::string Log(const char *_MsgType, int _ArgCnt, ...);

  //@@CodeBlockNames:2@@

  //@@CodeBlockValues:2@@

  //@@StateNames:2@@
  //@@StateValues:2@@

  //@@STIValues:2@@

  //@@StateTable:2@@

  //@@StartState:2@@
  //@@EndState:2@@
};
