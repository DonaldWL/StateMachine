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

#include "IOFile.h"
#include "StateMachine.h"
#include "SMExceptions.h"

int CStateMachine::Run(void)
{
  int CurStateIndx = StartStateIndx;
  int PrevCurStateIndx = CurStateIndx;
  int OtherWise = -1;
  int StateRValue = -1;
  bool ProcessStates = true;

  while (ProcessStates) {
    switch (StateTable[CurStateIndx + STI_CBIdx]) {

        // StateRValue
        //   0 -> Ok
        //   1 -> InFileDir does not exist
        //        OutFileDir does not exist
        //        InFileDir and OutFileDir are the same
      case CB_StartMachine:
        StateRValue = 0;
        InFileDir = std::filesystem::absolute(InFileDir);
        Log("Info", 2, "InFileDir set to ", InFileDir.string().c_str());
        OutFileDir = std::filesystem::absolute(OutFileDir);
        Log("Info", 2, "OutFileDir set to ", OutFileDir.string().c_str());
        if (!std::filesystem::exists(InFileDir) || !std::filesystem::is_directory(InFileDir)) {
          Log("Error", 3, "InFileDir (", InFileDir.string().c_str(), ") is does not exist or is not a directory");
          StateRValue = 1;
        } else if (!std::filesystem::exists(OutFileDir) || !std::filesystem::is_directory(OutFileDir)) {
          Log("Error", 3, "OutFileDir (", OutFileDir.string().c_str(), ") is does not exist or is not a directory");
          StateRValue = 1;
        } else if (OutFileDir == InFileDir) {
          Log("Error", 5, "InFileDir (", InFileDir.string().c_str(), ") is the same as OutFileDir (",
              OutFileDir.string().c_str(), ")");
          StateRValue = 1;
        }
        break;

        // StateRValue
        //   0 -> Ok
        //   1 -> No files to process in InFileDir
      case CB_GetFiles:
        StateRValue = 0;
        for (const auto &entry : std::filesystem::directory_iterator(InFileDir)) {
          if (!std::filesystem::is_directory(entry.path()) &&
              std::string{ entry.path().filename().u8string() }[0] != '.') {
            Files.push_front(entry.path());
          }
        }
        {
          char ANum[20];

          _itoa_s((int)Files.size(), ANum, 20, 10);
          Log("Info", 5, "Number of files to process (", ANum, ") from InFileDir (",
              InFileDir.string().c_str(), ")");
        }

        if (Files.empty()) {
          Log("Error", 3, "No files found to process at InFileDir (", InFileDir.string().c_str(), ")");
          StateRValue = 1;
        }
        break;

        // StateRValue
        //   0 -> Ok
        //   1 -> No more files to process
        //   2 -> Out file already exists and not in interactive mode
        //   3 -> Out File already exists and user stated overwrite the file
        //   4 -> User does not wish to overwrite file
        //   5 -> User wishes to skip file
      case CB_NextFile:
        StateRValue = 0;
        if (Files.empty()) {
          StateRValue = 1;
        } else {
          InFileName = Files.front();
          Files.pop_front();
          OutFileName = OutFileDir / InFileName.filename();
          if (std::filesystem::exists(OutFileName)) {
            std::string Msg;
            if (!IsAtty(stdin)) {
              Log("Error", 3, "Out File (", OutFileName.string().c_str(), ") exists and not in interactive mode");
              ReturnValue.UserRValue = 1;
              StateRValue = 2;
            } else {
              std::string YesNo;
              while (true) {
                std::cout << "Out File (" << OutFileName.string().c_str() << ") exists, overwrite (Y|N|S)? ";
                std::cin >> YesNo;
                transform(YesNo.begin(), YesNo.end(), YesNo.begin(), ::tolower);
                if (YesNo == "y") {
                  Msg = Log("Warning", 3, "Overwriting file (", OutFileName.string().c_str(), ")");
                  printf(Msg.c_str());
                  StateRValue = 3;
                  break;
                } else if (YesNo == "n") {
                  Msg = Log("Error", 3, "User does not wont to overwrite file (", OutFileName.string().c_str(),
                           ") ending program");
                  printf(Msg.c_str());
                  ReturnValue.UserRValue = 1;
                  StateRValue = 4;
                  break;
                } else if (YesNo == "s") {
                  Log("Info", 3, "User is skipping (", OutFileName.string().c_str(), ")");
                  StateRValue = 5;
                  break;
                }
                std::cout << std::endl << "Invalid response to question (" << YesNo <<
                             ")  must be (Y|N|S)" << std::endl;
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
        StateRValue = 0;
        Log("Info", 2, "Opening file InFile ", InFileName.string().c_str());
        InFileFh = std::ifstream(InFileName);
        if (!InFileFh.good()) {
          std::error_code err(errno, std::system_category());
          Log("Error", 4, "Unable to open in file (", InFileName.string().c_str(),
              ") => ", err.message());
          ReturnValue.UserRValue = 1;
          StateRValue = 1;
        }

        Log("Info", 2, "Opening file OutFile ", OutFileName.string().c_str());
        OutFileFh = std::ofstream(OutFileName);
        if (!OutFileFh.good()) {
          std::error_code err(errno, std::system_category());
          Log("Error", 4, "Unable to open out file (", OutFileName.string().c_str(),
              ") => ", err.message());
          ReturnValue.UserRValue = 1;
          StateRValue = 2;
        }
        break;

        // StateRValue
        //   0 -> Ok
        //   1 -> Read error on InFile
        //   2 -> Write error on OutFile
      case CB_CopyFile:
        StateRValue = 0;
        Log("Info", 4, "Coping file (", InFileName.string().c_str(), ") to (",
            OutFileName.string().c_str(), ")");
        {
          std::string Line;

            // Read the file in line by line
          while (std::getline(InFileFh, Line)) {
            if (!InFileFh.good()) {
              std::error_code err(errno, std::system_category());
              if (err.value() != 0) {
                Log("Error", 4, "Unable to read in file (", InFileName.string().c_str(),
                    ") => ", err.message());
                ReturnValue.UserRValue = 1;
                StateRValue = 1;
                break;
              }
            }

              // Write the line out.
            OutFileFh << Line << std::endl;
            if (!OutFileFh.good()) {
              std::error_code err(errno, std::system_category());
              Log("Error", 4, "Unable to write out file (", OutFileName.string().c_str(),
                  ") => ", err.message());
              ReturnValue.UserRValue = 1;
              StateRValue = 1;
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
        if (InFileFh.is_open()) {
          Log("Info", 2, "Closing file InFile ", InFileName.string().c_str());
          InFileFh.close();
        }
        if (OutFileFh.is_open()) {
          Log("Info", 2, "Closing file OutFile ", OutFileName.string().c_str());
          OutFileFh.close();
        }
        break;

        // End the state machine.  We return from this.
      case CB_EndMachine:
        StateRValue = 0;
        if (ReturnValue.UserData == "") {
          ReturnValue.UserRValue = 0;
          ReturnValue.UserData = "Ending State Machine";
        }
        Log("Info", 1, ReturnValue.UserData.c_str());
        ProcessStates = false;
        break;

      default:
        throw SMCodeBlockInvalid(StateNames[StateTable[CurStateIndx + STI_StateIdx]],
                                 StateTable[CurStateIndx + STI_CBIdx], StateRValue, CurStateIndx);
    };

    if (StateRValue < 0) {
      throw SMStateRValueInvalid(StateNames[StateTable[CurStateIndx + STI_StateIdx]],
                                 CodeBlockNames[StateTable[CurStateIndx + STI_CBIdx]],
                                 StateRValue, CurStateIndx);
    }

    OtherWise = -1;
    if (StateRValue > StateTable[CurStateIndx + STI_StateLenIdx]) {
      OtherWise = StateTable[CurStateIndx + STI_StateLenIdx + StateTable[CurStateIndx + STI_StateLenIdx] + 1];
      if (OtherWise < 0) {
        throw SMNoOtherWise(StateNames[StateTable[CurStateIndx + STI_StateIdx]],
                            CodeBlockNames[StateTable[CurStateIndx + STI_CBIdx]],
                            StateRValue, CurStateIndx);
      }
    }

    if (TraceFh != nullptr) {
      if (TraceFriendly) {
        *TraceFh << "State Trace" << std::endl;
        *TraceFh << "  State:         " << StateNames[StateTable[CurStateIndx + STI_StateIdx]] << std::endl;
        *TraceFh << "  CodeBlock:     " << CodeBlockNames[StateTable[CurStateIndx + STI_CBIdx]] << std::endl;
        *TraceFh << "  StateRValue:   " << StateRValue << std::endl << std::endl;
      } else {
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
    }

    PrevCurStateIndx = CurStateIndx;
    if (OtherWise > -1) {
      CurStateIndx = OtherWise;
    } else {
      CurStateIndx = StateTable[CurStateIndx + STI_StatesIdx + StateRValue];
    }
    if (CurStateIndx > STLen) {
      throw SMNextStateIndxInvalid(StateNames[StateTable[PrevCurStateIndx + STI_StateIdx]],
                                   CodeBlockNames[StateTable[PrevCurStateIndx + STI_CBIdx]],
                                   StateRValue, PrevCurStateIndx, OtherWise, CurStateIndx);
    }
  };

    // If the user did not set to exit the loop then error
  if (ProcessStates) {
    throw SMExitedMainLoop(StateNames[StateTable[CurStateIndx + STI_StateIdx]],
                           CodeBlockNames[StateTable[CurStateIndx + STI_CBIdx]]);
  }

  return ReturnValue.UserRValue;
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
