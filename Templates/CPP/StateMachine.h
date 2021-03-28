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

#include <stdarg.h>
#include <iostream>
//#include <filesystem>
//#include <fstream>
//#include <list>

class CStateMachine
{
public:
  std::ostream *TraceFh;
  std::ostream *LogFileFh;

  CStateMachine(std::ostream *TraceFh, std::ostream *LogFileFh) :
                TraceFh(TraceFh), LogFileFh(LogFileFh) {};

  void Run(void);

private:
  CStateMachine();

  std::string Log(const char *_MsgType, int _ArgCnt, ...);
  char *CStateMachine::BuildMsg(const char *MsgT, int CurStateIndx, int StateRValue);
  char *CStateMachine::StringBuild(char *_msg, const int _stringCnt, ...);
  char *CStateMachine::StringBuildVaList(char *_msg, const int _stringCnt, va_list args);
  
  //@@CodeBlockNames:2@@

  //@@CodeBlockValues:2@@

  //@@StateNames:2@@

  //@@StateValues:2@@

  //@@STIValues:2@@

  //@@StateTable:2@@
};
