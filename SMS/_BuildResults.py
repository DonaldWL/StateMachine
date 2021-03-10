'''
Created:   Feb 22, 2021
Author:    Donald W. Long (Donald.W.Long@gmail.com)
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

  Used to build the results in SMS.Results.CSMSResult.  After BuildResutls 
  is called the CSMSResult will be filled in.  This is only used in 
  SMS.Process.CSMSProcess._Validate and should not be called outside of the
  SMS package.
-----------------------------------------------------------------------------
Update History:
  Feb 22, 2021 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''

  #--------------------------------------------------------------------------
def BuildResutls(Result, LineCnt):
  '''
  Used to build the results in CSMSResult.

  (UndefStates, UndefCodeBlock) = BuildResutls(Result, LineCnt)
    UndefStates
      Dictionary of undefined states.  The key is the name of the
      state that is not defined.  The item is a list of states that
      this undefined state is found in.
    UndefCodeBlock
      Dictionary of undefined code blocks.  The key is the name of the
      block that is not defined.  The item is a list of state names that
      reference the code block.
    Result
      Instance of SMS.Results.CSMSResult
    LineCnt
      Number of lines processed in the SMS file.
  '''
  UndefStates = {}
  UndefCodeBlock = {}

  Result.StateNames = list(Result.States.StateList)
  Result.StateNames.sort()
  Result.UnusedStates = list(Result.States.StateList)
  Result.UnusedStates.sort()
  Result.CodeBlockNames = list(Result.CodeBlocks)
  Result.CodeBlockNames.sort()
  Result.UnusedCodeBlocks = list(Result.CodeBlocks)
  Result.UnusedCodeBlocks.sort()

  Result.Stats['LinesProcessed'] = LineCnt
  Result.Stats['ProcessingTime'] = Result.CaptureTimer.Took
  Result.Stats['StateCnt'] = len(Result.StateNames)
  Result.Stats['UnusedStateCnt'] = 0
  Result.Stats['CodeBlockCnt'] = len(Result.CodeBlocks.keys())
  Result.Stats['UnusedCodeBlockCnt'] = 0
  Result.Stats['NumStateTransCnt'] = 0

    # Put the correct code type with each code block
  for codeBlockName in Result.CodeBlockNames:
    if Result.CodeBlocks[codeBlockName].Type is None:
      Result.CodeBlocks[codeBlockName] = Result.CodeBlocks[codeBlockName]._replace(Type = Result.CodeBlockType.Value)

  Result.UnusedStates.remove(Result.States.StartState.Param)
  for stateName, stateRec in Result.States.StateList.items():
    transCnt = len(stateRec.Transitions)
    Result.Stats['NumStateTransCnt'] += transCnt
    if Result.States.StateList[stateName].CodeBlock in Result.CodeBlockNames:
      try:
        Result.UnusedCodeBlocks.remove(Result.States.StateList[stateName].CodeBlock)
      except ValueError:
        pass
    else:
      UndefCodeBlock.setdefault(Result.States.StateList[stateName].CodeBlock, [])
      UndefCodeBlock[Result.States.StateList[stateName].CodeBlock].append(stateName)
    Result.CodeBlockUsage.setdefault(Result.States.StateList[stateName].CodeBlock, [])
    Result.CodeBlockUsage[Result.States.StateList[stateName].CodeBlock].append(stateName)

    for RValue, TranRec in stateRec.Transitions.items():  # pylint: disable=unused-variable
      if TranRec.State == Result.States.EndState.Param and not stateName in Result.StatesWithEnd:
        Result.StatesWithEnd.append(stateName)
      if TranRec.State in Result.StateNames:
        try:
          Result.UnusedStates.remove(TranRec.State)
        except ValueError:
          pass
      else:
        UndefStates.setdefault(TranRec.State, [])
        if not stateName in UndefStates[TranRec.State]:
          UndefStates[TranRec.State].append(stateName)

  Result.Stats['UnusedStateCnt'] = len(Result.UnusedStates)
  Result.Stats['UnusedCodeBlockCnt'] = len(Result.UnusedCodeBlocks)
  Result.CodeBlockNames.sort()

  return (UndefStates, UndefCodeBlock)
