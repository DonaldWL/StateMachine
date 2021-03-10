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
    unsigned long long StatesProcessed = 0;

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
    bool Error = false;

    CStateMachine(std::filesystem::path InFileDir, std::filesystem::path OutFileDir, bool ForceOverwrite = false,
                  std::ostream *TraceFh = nullptr, bool TraceFriendly = false) :
                    InFileDir(InFileDir), OutFileDir(OutFileDir), ForceOverwrite(ForceOverwrite),
                    TraceFh(TraceFh), TraceFriendly(TraceFriendly) {};

  int Run(void);

  int CloseFiles(void) {
    if (InFileFh.is_open()) {
      InFileFh.close();
    }
    if (OutFileFh.is_open()) {
      OutFileFh.close();
    }
    return(0);
  }

  void PrintError(std::string &ErrMsg) {
    Error = true;
    std::cout << "ERROR: " << ErrMsg << std::endl;
  }

  void PrintWarning(std::string &WarningMsg) {
    std::cout << "WARNING: " << WarningMsg << std::endl;
  }

private:
  CStateMachine();

//@@CodeBlockNames@@

//@@StateNames@@

    // Used to index into each entry in the StateTable.
  enum STI {
    STI_CBIdx = 0,
    STI_StateIdx = 1,
    STI_StateLenIdx = 2,
    STI_StatesIdx = 3
  };

//@@StateTable@@
};
