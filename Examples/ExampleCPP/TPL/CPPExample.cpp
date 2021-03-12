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
#include <filesystem>
#include <iostream>
#include <fstream>
#include <chrono>

#include "StateMachine.h"

int main(int argc, const char* argv[]) {
  std::filesystem::path InFileDir = std::filesystem::absolute("../../StateMachine/Examples/ExampleC/STM");
  std::filesystem::path OutFileDir = std::filesystem::absolute("./CopiedFiles");
  std::filesystem::path TraceLogFileName = std::filesystem::absolute("./StateMachineTrace.log");
  std::filesystem::path LogFileName = std::filesystem::absolute("./StateMachine.log");
  std::ofstream TraceFh;
  std::ofstream LogFh;
  bool TraceFriendly = false;
  bool ForceOverwrite = false;


  if (std::filesystem::exists(OutFileDir) and not std::filesystem::is_directory(OutFileDir)) {
    std::cout << "CopiedFiles exists and is not a directory" << std::endl;
    exit(5);
  }

    // If we are not going to do a overwrite then lets clear it out
  if (!ForceOverwrite && std::filesystem::exists(OutFileDir)) {

      // Make sure we do not have dirs in this directory, if fail
    for (const auto & entry : std::filesystem::directory_iterator(OutFileDir)) {
      if (std::filesystem::is_directory(entry)) {
        std::cout << "Cannot remove " << OutFileDir << " because it contains a directory " << entry.path() << std::endl;
        exit(6);
      }
    }

      // No dirs, lets delete all the files
    for (const auto & entry : std::filesystem::directory_iterator(OutFileDir)) {
      std::filesystem::remove(entry.path());
    }
    std::filesystem::remove(OutFileDir);
  }

  if (!std::filesystem::exists(OutFileDir)) std::filesystem::create_directory(OutFileDir);

    // We should check for errors.
  LogFh.open(LogFileName);
  TraceFh.open(TraceLogFileName);

    // Create the state machine
  CStateMachine StateMachine(InFileDir, OutFileDir, ForceOverwrite, &TraceFh,
                             TraceFriendly, &LogFh);

  std::string SepLine;
  SepLine.insert(0, 50, '-');
  printf("%s\n", SepLine.c_str());

    // Run the state machine and capture how long it took
  auto t1 = std::chrono::high_resolution_clock::now();
  int rvalue = StateMachine.Run();
  auto t2 = std::chrono::high_resolution_clock::now();
  auto duration = std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count();

    // Close the log files
  TraceFh.close();
  LogFh.close();

  printf("State Machine RValue (%u)\n", StateMachine.ReturnValue.MachineRValue);
  printf("State machine Msg (%s)\n", StateMachine.ReturnValue.Msg.c_str());
  printf("State Machine User RValue (%u)\n", StateMachine.ReturnValue.UserRValue);
  printf("State machine User Msg (%s)\n", StateMachine.ReturnValue.UserData.c_str());
  printf("State machine duration (%I64d)\n", duration);
  printf("%s\n", SepLine.c_str());

  return 0;
}
