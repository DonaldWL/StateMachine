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

  Is the results of the processing of the SMS File by CSMSProcess from
  Libs.StateMachine.SMS.Process.  If a syntax error occurs then the results
  are not valid.  You might get some but overall you should consider the data
  invalid.  You should look at the file Libs.StateMachine.SMS.Definitions.
  This contains all the structure definitions that are used.  Also review
  Libs.StateMachine.SMS.Report, it will show you how to access the data and
  process it for your needs.
-----------------------------------------------------------------------------
Update History:
  Feb 22, 2022 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''

from PythonLib.Base.CodeTimer import CCaptureTimer
from StateMachine.SMS.Definitions import (StateTableDef, SingleCmdDef, MultiParamCmdDef, 
                                          SMSVERSION, SMSFILEVERSION)

  #--------------------------------------------------------------------------
class CSMSResults(object):
  '''
  Used to hold data that can be retrieved by the user of CSMSProcess to
  dump the results of the run.

  The following are the variables available to you, it is assumed you
  understand the SMS file.

    Author => SingleCmdDef(0, None)
      From @Author, is not required.

    Date => SingleCmdDef(0, None)
      From @Date, is not required.

    StateMachineName = SingleCmdDef(0, None)
      From @StateMachineName, is required

    Version => SingleCmdDef(0, None)
      from @Version, is not required

    SMSFileVersion => SingleCmdDef(0, None)
      from @SMSFileVersion, is required

    SMSCurrentFileVersion => string
      Is the current supported SMS File version.

    SMSVersion => string
      Is the SMS package version

    CodeBlockType => SingleCmdDef(0, 'Code')
      from @CodeBlockType, is not required, default is Code

    CodeBlocks => {}
      from @BeginCodeBlock and @EndCodeBlock.  This is a
      dictionary and the key is the CodeBlock name.  Each
      item is of CodeBlockDef.

    States => StateTableDef(0, 0, {})
      Contains all the information about the states.  The
      dictionary is by state name.  Each item in the state
      name is StateRecDef.

    CaptureTimer => CCaptureTimer()
      This is how long it took to process the SMS file.
      This does not include validation, just reading in
      the file and processing the file.  See CCaptureTimer
      from Libs.Base.CodeTimer.

    Stats => {}
      Is a dictionary of statistics.  See below for a list, but you should
      dump the keys to make sure you see all of them.  This documentation
      might not be up to date.

        CodeBlockCnt        => Number of code block
        LinesProcessed      => Number of lines processed from SMS file
        NumStateTransCnt    => Number of state transitions
        ProcessingTime      => How long it took to process the SMS file in milliseconds
                               See Libs.Base.CodeTimer.  This is an instance of this.
                               If you wish to convert it see Libs.Base.Converters.
        StateCnt            => Number of states
        UnusedCodeBlockCnt  => Number of code blocks defined that are not referenced
        UnusedStateCnt      => Number of states defined that are not referenced

    StateNames => []
      Is a sorted list of all the State Name.

    StatesWithEnd => []
      Is a sorted list of all states that contain @End

    UnusedStates => []
      Is a sorted list of all states that are not referenced.

    CodeBlockNames => []
      Is a sorted list of code blocks.

    UnusedCodeBlocks => []
      Is a sorted list of unused code blocks

    CodeBlockUsage => {}
      Is a dictionary of code block usages.  They key is the code block name,
      the item is a list of states that reference the code block.
  '''

  def __init__(self):
    self.Author = SingleCmdDef(0, None)
    self.Date = SingleCmdDef(0, None)
    self.StateMachineName = SingleCmdDef(0, None)
    self.Language = MultiParamCmdDef(0, [])
    self.Version = SingleCmdDef(0, None)
    self.SMSFileVersion = SingleCmdDef(0, None)
    self.SMSCurrentFileVersion = SMSFILEVERSION
    self.SMSVersion = SMSVERSION
    self.CodeBlockType = SingleCmdDef(0, 'Code')
    self.CodeBlocks = {}
    self.States = StateTableDef(None, None, 0, 0, {})
    self.CaptureTimer = CCaptureTimer()

    self.Stats = {}
    self.StateNames = []
    self.StatesWithEnd = []
    self.UnusedStates = []
    self.CodeBlockNames = []
    self.UnusedCodeBlocks = []
    self.CodeBlockUsage = {}
