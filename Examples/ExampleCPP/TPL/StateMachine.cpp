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
#include "IOFile.h"
#include "StateMachine.h"
#include "SMExceptions.h"

int CStateMachine::Run(void)
{
  int CurStateIndx = StartStateIndx;
  int PrevCurStateIndx = CurStateIndx;
  int OtherWise = -1;
  int StateRValue = -1;

  while (true) {
    StatesProcessed++;
    switch (StateTable[CurStateIndx + STI_CBIdx]) {

        // StateRValue
        //   0 -> Ok
        //   1 -> InFileDir does not exist
        //        OutFileDir does not exist
        //        InFileDir and OutFileDir are the same
      case CB_StartMachine:
        StateRValue = 0;
        GetFullPath(&InFileDir);
        GetFullPath(&OutFileDir);
        if (not std::filesystem::exists(InFileDir) or not std::filesystem::is_directory(InFileDir)) {
          StateRValue = 1;
        } else if (not std::filesystem::exists(OutFileDir) or not std::filesystem::is_directory(OutFileDir)) {
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
        for (const auto &entry : std::filesystem::directory_iterator(InFileDir)) {
          if (not std::filesystem::is_directory(entry.path()) &&
              std::string{ entry.path().filename().u8string() }[0] != '.') {
            Files.push_front(entry.path());
          }
        }

        if (Files.empty()) {
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
              Msg = "Out File (" + OutFileName.string() + ") exists and not in interactive mode";
              PrintError(Msg);
              StateRValue = 2;
            } else {
              std::string YesNo;
              while (true) {
                std::cout << "Out File (" << OutFileName.string() << ") exists, overwrite (Y|N|S)? ";
                std::cin >> YesNo;
                transform(YesNo.begin(), YesNo.end(), YesNo.begin(), ::tolower);
                if (YesNo == "y") {
                  Msg = "Overwriting file (" + OutFileName.string();
                  PrintWarning(Msg);
                  StateRValue = 3;
                  break;
                } else if (YesNo == "n") {
                  Msg = "User does not wont to overwrite of (" + OutFileName.string() + ") ending program";
                  PrintWarning(Msg);
                  StateRValue = 4;
                  break;
                } else if (YesNo == "s") {
                  Msg = "Skipping file (" + OutFileName.string() + ") ending program";
                  PrintWarning(Msg);
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
        InFileFh = std::ifstream(InFileName);
        if (!InFileFh.good()) {
          std::string Msg;
          std::error_code err(errno, std::system_category());
          Msg = "Unable to open in file (" + InFileName.string() + ") => " + err.message();
          PrintError(Msg);
          StateRValue = 1;
        }

        OutFileFh = std::ofstream(OutFileName);
        if (!OutFileFh.good()) {
          std::string Msg;
          std::error_code err(errno, std::system_category());
          Msg = "Unable to open out file (" + OutFileName.string() + ") => " + err.message();
          PrintError(Msg);
          StateRValue = 2;
        }
        break;

        // StateRValue
        //   0 -> Ok
        //   1 -> Read error on InFile
        //   2 -> Write error on OutFile
      case CB_CopyFile:
        StateRValue = 0;
        {
          std::string Line;

            // Read the file in line by line
          while (std::getline(InFileFh, Line)) {
            if (!InFileFh.good()) {
              std::string Msg;
              std::error_code err(errno, std::system_category());
              if (err.value() != 0) {
                Msg = "Unable to read in file (" + InFileName.string() + ") => " + err.message();
                PrintError(Msg);
                StateRValue = 1;
                break;
              }
            }

              // Write the line out.
            OutFileFh << Line << std::endl;
            if (!OutFileFh.good()) {
              std::string Msg;
              std::error_code err(errno, std::system_category());
              Msg = "Unable to write out file (" + OutFileName.string() + ") => " + err.message();
              PrintError(Msg);
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
        StateRValue = CloseFiles();
        break;

        // End the state machine.  We return from this.
      case CB_EndMachine:
        CloseFiles();
        return(!Error);

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

  throw SMExitedMainLoop(StateNames[StateTable[CurStateIndx + STI_StateIdx]],
                         CodeBlockNames[StateTable[CurStateIndx + STI_CBIdx]]);
}
