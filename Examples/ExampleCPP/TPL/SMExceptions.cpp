//@@CopyFile@@
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

#include "SMExceptions.h"


SMException::SMException(const std::string State, const std::string CodeBlock) :
  State(State), CodeBlock(CodeBlock) {}

SMExitedMainLoop::SMExitedMainLoop(const std::string State, const std::string CodeBlock) :
  SMException::SMException(State, CodeBlock)
{
  msg = "Exited the main loop => State: " + this->State;
  msg = "  CodeBlock: " + this->CodeBlock;
}

SMNextStateIndxInvalid::SMNextStateIndxInvalid(const std::string State, const std::string CodeBlock,
                                               const int StateRValue, const int StateTableIdx,
                                               const int OtherWise, const int BadStateTableIdx) :
  SMException::SMException(State, CodeBlock),
  StateRValue(StateRValue),
  StateTableIdx(StateTableIdx),
  OtherWise(OtherWise),
  BadStateTableIdx(BadStateTableIdx)
{
  this->msg = "Next StateIndx Invalid => State: " + this->State;
  this->msg += "  CodeBlock: " + this->CodeBlock;
  this->msg += "  StateRValue: " + this->StateRValue;
  this->msg += "  StateTableIdx: " + this->StateTableIdx;
  this->msg += "  OtherWise: " + this->OtherWise;
  this->msg += "  BadStateTableIdx: " + this->BadStateTableIdx;
}

SMNoOtherWise::SMNoOtherWise(const std::string State, const std::string CodeBlock,
                             const int StateRValue, const int StateTableIdx) :
  SMException::SMException(State, CodeBlock),
  StateRValue(StateRValue),
  StateTableIdx(StateTableIdx)
{
  this->msg = "No OtherWise defined => State: " + this->State;
  this->msg += "  CodeBlock: " + this->CodeBlock;
  this->msg += "  StateRValue: " + this->StateRValue;
  this->msg += "  StateTableIdx: " + this->StateTableIdx;
}

SMStateRValueInvalid::SMStateRValueInvalid(const std::string State, const std::string CodeBlock,
                                           const int StateRValue, const int StateTableIdx) :
  SMException::SMException(State, CodeBlock),
  StateRValue(StateRValue),
  StateTableIdx(StateTableIdx)
{
  this->msg = "Invalid StateRValue => State: " + this->State;
  this->msg += "  CodeBlock: " + this->CodeBlock;
  this->msg += "  StateRValue: " + this->StateRValue;
  this->msg += "  StateTableIdx: " + this->StateTableIdx;
}

SMCodeBlockInvalid::SMCodeBlockInvalid(const std::string State, const int CodeBlockInt,
                                       const int StateRValue, const int StateTableIdx) :
  SMException::SMException(State, std::string("")),
  StateRValue(StateRValue),
  StateTableIdx(StateTableIdx)
{
  this->msg = "Invalid CodeBlock (might be bad state table) => State: " + this->State;
  this->msg += "  CodeBlockInt: " + this->CodeBlockInt;
  this->msg += "  StateRValue: " + this->StateRValue;
  this->msg += "  StateTableIdx: " + this->StateTableIdx;
}
