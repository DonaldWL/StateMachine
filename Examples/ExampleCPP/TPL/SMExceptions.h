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

  Exceptions that the state machine can throw.
-----------------------------------------------------------------------------
*/

#include <string>

//===================================================================
// Base exception for all exception
//===================================================================
class SMException : public std::exception
{
  public:
    std::string State;
    std::string CodeBlock;
    std::string msg;

    SMException(const std::string State, const std::string CodeBlock);
};

//===================================================================
// Some how we dropped out of the main loop in CStateMachine.Run.
// This should never happen.
//===================================================================
class SMExitedMainLoop : public SMException
{
  public:
    SMExitedMainLoop(const std::string State, const std::string CodeBlock);

    inline virtual const char* what() const throw () { return msg.c_str(); }
};

//===================================================================
// The transition from current state to the next state has created
// an index into the state table that is not valid.  This occurs
// when the index goes beyond the state table.
//===================================================================
class SMNextStateIndxInvalid : SMException
{
  public:
    int StateRValue;
    int StateTableIdx;
    int OtherWise;
    int BadStateTableIdx;

    SMNextStateIndxInvalid(const std::string State, const std::string CodeBlock,
                           const int StateRValue, const int StateTableIdx,
                           const int OtherWise, const int BadStateTableIdx);

    inline virtual const char* what() const throw () { return msg.c_str(); }
};

//===================================================================
// StateRValue does not have a state to tranistion to and no 
// OtherWise was defined for this state.
//
// TODO: Need to make a list of the transition and otherwise.
//===================================================================
class SMNoOtherWise : SMException
{
  public:
    int StateRValue;
    int StateTableIdx;

    SMNoOtherWise(const std::string State, const std::string CodeBlock,
                  const int StateRValue, const int StateTableIdx);


    inline virtual const char* what() const throw () { return msg.c_str(); }
};


//===================================================================
// StateRValue is not a valid number, must be 0 or greater.
//===================================================================
class SMStateRValueInvalid : SMException
{
  public:
    int StateRValue;
    int StateTableIdx;

    SMStateRValueInvalid(const std::string State, const std::string CodeBlock,
                         const int StateRValue, const int StateTableIdx);


    inline virtual const char* what() const throw () { return msg.c_str(); }
};

//===================================================================
// Looked for the codeblock name and the index was outside the
// list of code blocks.
//===================================================================
class SMCodeBlockInvalid : SMException
{
  public:
    int CodeBlockInt;
    int StateRValue;
    int StateTableIdx;

    SMCodeBlockInvalid(const std::string State, const int CodeBlockInt,
                       const int StateRValue, const int StateTableIdx);


    inline virtual const char* what() const throw () { return msg.c_str(); }
};
