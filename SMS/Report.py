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

  Generates a report about the SMS file processing.  It outputs statistics
  and all the information about the state machine.  You should review this
  report at least at the end of your development.  It will show you unused
  states and unused code blocks.
-----------------------------------------------------------------------------
Update History:
  Feb 22, 2022 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''

import sys

from StateMachine.SMS.Results import CSMSResults

  #--------------------------------------------------------------------------
def SMSReport(SMSResult, OutPutVersion, OutFile):
  '''
  Used to generate the SMS report.  The report contains statistics and information
  about the SMS file that was processed.

  SMSReport(SMSResult, OutPutVersion, OutFile)
    SMSResult  => CSMSResults from Libs.StateMachine.SMS.Results
      This is generated by CSMSProcess from Libs.StateMachine.SMS.Process.  After
      the CProccess has completed get the instance of CSmsResult and pass it into
      this function. If a syntax error occurred in the processing the CSMSResults
      will not be valid.
    OutPutVersion => bool
      If True then output SMSVersion and SMSCurrentFileVersion
    OutFile  => Any class instance that has a method called write
      Used to output the report.  Normally you pass in sys.stdout, but it can be
      any instance of a class that supports a method write.  The write method
      must take in a string and not add a new line.  No validation is done on
      this argument.  If not passed in or set to None will default to sys.stdout.

  Exceptions:
    AttributeError
      SMSResult is not an instance of CSMSResults
      OutPutVersion is not a bool
  '''

  if not isinstance(SMSResult, CSMSResults):
    raise AttributeError("SMSResult is not an instance of CSMSResults")

  if not isinstance(OutPutVersion, bool):
    raise AttributeError("OutPutVersion must be a bool (True, False)")

  if OutFile is None:
    OutFile = sys.stdout

  OutFile.write(('=' * 60) + '\n')
  if OutPutVersion:
    OutFile.write('Versions\n')
    OutFile.write('  SMSVersion:            {0}\n'.format(SMSResult.SMSVersion))
    OutFile.write('  SMSCurrentFileVersion: {0}\n'.format(SMSResult.SMSCurrentFileVersion))
    OutFile.write(('-' * 60) + '\n')

  _Stats(SMSResult, OutFile)
  OutFile.write(('-' * 60) + '\n')
  _General(SMSResult, OutFile)
  OutFile.write(('-' * 60) + '\n')
  _SimpleList('StateNames', SMSResult.StateNames, 4, OutFile)
  OutFile.write(('-' * 60) + '\n')
  _SimpleList('StatesWithEnd', SMSResult.StatesWithEnd, 4, OutFile)
  OutFile.write(('-' * 60) + '\n')
  _UnusedStates(SMSResult, OutFile)
  OutFile.write(('-' * 60) + '\n')
  _States(SMSResult, OutFile)
  OutFile.write(('-' * 60) + '\n')
  _SimpleList('CodeBlockNames', SMSResult.CodeBlockNames, 4, OutFile)
  OutFile.write(('-' * 60) + '\n')
  _UnusedCodeBlocks(SMSResult, OutFile)
  OutFile.write(('-' * 60) + '\n')
  _CodeBLockUsage(SMSResult, OutFile)
  OutFile.write(('-' * 60) + '\n')
  _CodeBlocks(SMSResult, OutFile)
  OutFile.write(('=' * 60) + '\n')

  #--------------------------------------------------------------------------
def _NameList(Names, Offset, OutFile):
  lines = ''
  loc = 0
  pad = 0
  for Name in Names:
    if pad < len(Name):
      pad = len(Name)
  while loc < len(Names):
    lines = lines + ' ' * Offset
    for Name in Names[loc:loc + 5]:
      lines = lines + Name + ' '
      lines = lines + ' ' * (pad - len(Name))
    lines = lines + '\n'
    loc += 5
  OutFile.write(lines)

  #--------------------------------------------------------------------------
def _Stats(SMSResult, OutFile):
  OutFile.write("Stats\n")
  StatNames = list(SMSResult.Stats.keys())
  StatNames.sort()
  for key in StatNames:
    if key == 'ProcessingTime':
      OutFile.write("  {0}: {1}ms\n".format(key, SMSResult.Stats[key]))
    else:
      OutFile.write("  {0}: {1}\n".format(key, SMSResult.Stats[key]))

  #--------------------------------------------------------------------------
def _General(SMSResult, OutFile):
  OutFile.write('  {0:05d} SMSFileVersion: {1}\n'.format(SMSResult.SMSFileVersion.LineNo, SMSResult.SMSFileVersion.Value))
  ParamList = []
  for Param in SMSResult.Language.Params:
    ParamList.append(Param.Param)
  OutFile.write('  {0:05d} Language: ({1})\n'.format(SMSResult.Language.LineNo, ', '.join(ParamList)))
  OutFile.write('  {0:05d} Author: {1}\n'.format(SMSResult.Author.LineNo, SMSResult.Author.Value))
  OutFile.write('  {0:05d} Date: {1}\n'.format(SMSResult.Date.LineNo, SMSResult.Date.Value))
  OutFile.write('  {0:05d} StateMachineName: {1}\n'.format(SMSResult.StateMachineName.LineNo, SMSResult.StateMachineName.Value))
  OutFile.write('  {0:05d} Version: {1}\n'.format(SMSResult.Version.LineNo, SMSResult.Version.Value))
  OutFile.write('  {0:05d} CodeBlockType: {1}\n'.format(SMSResult.CodeBlockType.LineNo, SMSResult.CodeBlockType.Value))
  OutFile.write('  {0:05d} StartState: {1}\n'.format(SMSResult.States.BLineNo,
                                                   'None' if SMSResult.States.StartState is None else SMSResult.States.StartState.Param))
  OutFile.write('  {0:05d} EndState: {1}\n'.format(SMSResult.States.BLineNo,
                                                   'None' if SMSResult.States.EndState is None else SMSResult.States.EndState.Param))

  #--------------------------------------------------------------------------
def _SimpleList(Name, List, Offset, OutFile):
  OutFile.write('  {0}\n'.format(Name))
  x = List
  x.sort()
  _NameList(x, Offset, OutFile)

  #--------------------------------------------------------------------------
def _UnusedStates(SMSResult, OutFile):
  OutFile.write('  UnusedStates\n')
  x = SMSResult.UnusedStates
  x.sort()
  for stateName in x:
    OutFile.write('    {0:05d} {1}\n'.format(SMSResult.States.StateList[stateName].LineNo,
                                             stateName))

  #--------------------------------------------------------------------------
def _States(SMSResult, OutFile):
  OutFile.write('  States started at {0:05d} ended at {1:05d}\n'.format(SMSResult.States.BLineNo, SMSResult.States.ELineNo))
  x = list(SMSResult.States.StateList.keys())
  x.sort()
  for stateName in x:
    OutFile.write('    {0:05d} {1} {2}\n'.format(SMSResult.States.StateList[stateName].LineNo,
                                                 stateName,
                                                 SMSResult.States.StateList[stateName].CodeBlock))
    for RValue, TranRec in SMSResult.States.StateList[stateName].Transitions.items():
      OutFile.write('      {0:05d} {1} => {2}\n'.format(TranRec.LineNo, RValue, TranRec.State))

  #--------------------------------------------------------------------------
def _UnusedCodeBlocks(SMSResult, OutFile):
  OutFile.write('  UnusedCodeBlocks\n')
  UnusedCBNames = SMSResult.UnusedCodeBlocks
  UnusedCBNames.sort()
  for codeBlockName in UnusedCBNames:
    OutFile.write("    {0:05d} {1}\n".format(SMSResult.CodeBlocks[codeBlockName].LineNo,
                                             codeBlockName))

  #--------------------------------------------------------------------------
def _CodeBLockUsage(SMSResult, OutFile):
  OutFile.write('  CodeBlockUsage\n')
  x = list(SMSResult.CodeBlockUsage.keys())
  x.sort()
  for codeBlockName in x:
    OutFile.write('    {0}\n'.format(codeBlockName))
    x1 = SMSResult.CodeBlockUsage[codeBlockName]
    x1.sort()
    _NameList(x1, 6, OutFile)

  #--------------------------------------------------------------------------
def _CodeBlocks(SMSResult, OutFile):
  OutFile.write('  CodeBlocks\n')
  x = list(SMSResult.CodeBlocks.keys())
  x.sort()
  for codeBlockName in x:
    OutFile.write('    {0:05d} {1} ({2})\n'.format(SMSResult.CodeBlocks[codeBlockName].LineNo,
                                                   codeBlockName,
                                                   SMSResult.CodeBlocks[codeBlockName].Type))

  #--------------------------------------------------------------------------
def _SimpleBlock(Name, Variable, OutFile):
  OutFile.write('  {0} at {1:05d}\n'.format(Name, Variable.LineNo))
  for blockLine in Variable.BlockLines:
    OutFile.write('    {0:05d} {1}\n'.format(blockLine.LineNo, blockLine.Line))
