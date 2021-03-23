'''
Created:   Feb 18, 2021
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

  This supports the Python language.
-----------------------------------------------------------------------------
Update History:
  Author: Donald W. Long (Donald.W.Long@gmail.com)
  Date:   Feb 18, 2021
    Released
-----------------------------------------------------------------------------
'''

from StateMachine.Generator.Languages.Base import _CBase


  #--------------------------------------------------------------------------
class _CPythonLan(_CBase):
  '''
  See the _CBase class for details.
  '''
  def __init__(self, Language, TPLDir, STMDir, OverWrite, LogFh, SMSResult, Optimize):  
    _CBase.__init__(self, Language, TPLDir, STMDir, OverWrite, LogFh, SMSResult, Optimize)
    
    if Language != 'Python':
      raise AttributeError('_CPython only supports generation of python code, language passed in ({0})'.format(Language))
    
      # Setup the calls for each command.
    self._CmdExec['RemoveLine'] = None
    self._CmdExec['ReplaceLine'] = self.CmdExecDef(self._ReplaceLine, None)
    self._CmdExec['CreationDate'] = self.CmdExecDef(self._CreationDate, None)
    self._CmdExec['ClassDefinition'] = self.CmdExecDef(self._ClassDefinition, None)
    self._CmdExec['SMSUserAuthor'] = self.CmdExecDef(self._CmdReplacement, self._SMSResult.Author.Value)
    self._CmdExec['SMSUserDate'] = self.CmdExecDef(self._CmdReplacement, self._SMSResult.Date.Value)
    self._CmdExec['SMSUserVersion'] = self.CmdExecDef(self._CmdReplacement, self._SMSResult.Version.Value)
    self._CmdExec['ClassName'] = self.CmdExecDef(self._CmdReplacement, self._SMSResult.StateMachineName.Value)
    self._CmdExec['SMSFileVersion'] = self.CmdExecDef(self._CmdReplacement, self._SMSResult.SMSFileVersion.Value)
    self._CmdExec['CodeBlocks'] = self.CmdExecDef(self._CodeBlocks, None)
    self._CmdExec['CodeBlockNames'] = self.CmdExecDef(self._CodeBlockNames, None)
    self._CmdExec['StateNames'] = self.CmdExecDef(self._StateNames, None)
    self._CmdExec['StateTable'] = self.CmdExecDef(self._StateTable, None)
    self._CmdExec['StartState'] = self.CmdExecDef(self._StartState, None)
    self._CmdExec['StartStateValue'] = self.CmdExecDef(self._StartStateValue, None)
    self._CmdExec['EndState'] = self.CmdExecDef(self._EndState, None)
    self._CmdExec['EndStateValue'] = self.CmdExecDef(self._EndStateValue, None)
    self._CmdExec['CodeBlockTable'] = self.CmdExecDef(self._CodeBlockTable, None)

    #--------------------------------------------------------------------------
  def _StartState(self):
    '''
    StartState tag.
    '''
    StartStateId = self._SMSResult.StateNames.index(self._SMSResult.States.StartState.Param)
    self._STMFileFh.write((' ' * self._ForcedOffset) + 'self.StartStateIdx = ' + str(StartStateId) + '\n')
    
    #--------------------------------------------------------------------------
  def _EndState(self):
    '''
    EndState tag.
    '''
    EndStateId = -1
    if self._SMSResult.States.EndState is not None:
      EndStateId = self._SMSResult.StateNames.index(self._SMSResult.States.EndState.Param)
    self._STMFileFh.write((' ' * self._ForcedOffset) + 'self.EndStateIdx = ' + str(EndStateId) + '\n')
    
    #--------------------------------------------------------------------------
  def _ClassDefinition(self):
    '''
    ClassDefinition tag.
    '''
    STplLine = self._TplLine
    self._TplLine = (' ' * self._ForcedOffset) + 'class @@ClassName@@(CStateMachine):\n'
    self._CmdReplacement()
    self._TplLine = STplLine
    
    #--------------------------------------------------------------------------
  def _StateTable(self):
    '''
    StateTable tag.  Creates the state table.
    '''
    
      # Write Out the STT enum class
    IndentSpaces = ' ' * self._ForcedOffset
    Line = IndentSpaces + 'class STT(IntEnum):\n'
    IndentSpaces += '  '
    self._STMFileFh.write(Line)
    for StateId in range(0, len(self._SMSResult.StateNames)):
      Line = "{0}{1} = {2}\n".format(IndentSpaces, 
                                     self._SMSResult.StateNames[StateId],
                                     StateId)
      self._STMFileFh.write(Line)
    self._STMFileFh.write('\n')
    
    IndentSpaces = ' ' * self._ForcedOffset
    Line = (' ' * self._ForcedOffset) + 'self.StateTable = ('
    IndentSpaces = ' ' * len(Line)
    for StateName in self._SMSResult.StateNames:
      Line += 'STEntryDef(CBB.{0}, ('.format(self._SMSResult.States.StateList[StateName].CodeBlock)
      
      OtherWiseStateName = '-1'
      _ListRValues = list(self._SMSResult.States.StateList[StateName].Transitions.keys())
      if 'OtherWise' in _ListRValues:
        _ListRValues.remove('OtherWise')
        OtherWiseStateName = self._SMSResult.States.StateList[StateName].Transitions['OtherWise'].State
      _ListRValues.sort()
      _ListRValues = list(range(0, max(list(map(int, _ListRValues))) + 1))
      for StateRValue in _ListRValues:
        if str(StateRValue) in self._SMSResult.States.StateList[StateName].Transitions.keys():
          Line += 'STT.{0}, '.format(self._SMSResult.States.StateList[StateName].Transitions[str(StateRValue)].State)
        else:
          Line += '{0}{1}, '.format('STT.' if OtherWiseStateName != '-1' else '',
                                    OtherWiseStateName) 
      if len(_ListRValues) != 1:
        Line = Line[0:-2]
      Line += '), '
        
      Line += '{0}{1}),\n'.format('STT.' if OtherWiseStateName != '-1' else '',
                                  OtherWiseStateName)
      Line += IndentSpaces
      
    Line = Line.rstrip(' ')
    Line = Line[0:-2] + ')'
    
    MaxLineLen = 0
    CLine = ''
    for xline in Line.split('\n'):
      MaxLineLen = max(MaxLineLen, len(xline))
    StdIndx = 0
    for xLine in Line.split('\n'):
      CLine += '{0}{1} # {2}\n'.format(xLine, (' ' * abs(MaxLineLen - len(xLine))),
                                       self._SMSResult.StateNames[StdIndx])
      StdIndx += 1
    
    self._STMFileFh.write(CLine)
      
    #--------------------------------------------------------------------------
  def _CodeBlockTable(self):
    '''
    CodeBlockTable tag.  Creates the CodeBlock Table.
    '''
      # Write Out the CB enum class
    IndentSpaces = ' ' * self._ForcedOffset
    Line = IndentSpaces + 'class CBB(IntEnum):\n'
    IndentSpaces += '  '
    self._STMFileFh.write(Line)
    for CodeBlockId in range(0, len(self._SMSResult.CodeBlockNames)):
      Line = "{0}{1} = {2}\n".format(IndentSpaces, 
                                     self._SMSResult.CodeBlockNames[CodeBlockId],
                                     CodeBlockId)
      self._STMFileFh.write(Line)
    self._STMFileFh.write('\n')
    
    IndentSpaces = ' ' * self._ForcedOffset
    Line = (' ' * self._ForcedOffset) + 'self.CodeBlockTable = ('
    IndentSpaces = ' ' * len(Line)
    for CodeBlockName in self._SMSResult.CodeBlockNames:
      if self._SMSResult.CodeBlocks[CodeBlockName].Type == 'Method':
        CBEntry = 'CBEntryDef(CBB.{0}, compile(self.__{0}__, MFName, "exec")),\n'.format(CodeBlockName)
      else:
        CBEntry = 'CBEntryDef(CBB.{0}, compile(self.{0}, MFName, "exec")),\n'.format(CodeBlockName)
      Line += CBEntry + IndentSpaces
      
    Line = Line.rstrip(' ')
    Line = Line[0:-2] + ')\n'
    self._STMFileFh.write(Line)

    #--------------------------------------------------------------------------
  def _CodeBlockNames(self):
    '''
    CodeBlockNames tag.
    '''
    Line = (' ' * self._ForcedOffset) + 'self.CodeBlockNames  = ('
    IndentSpaces = ' ' * len(Line)
    for CodeBlockName in self._SMSResult.CodeBlockNames:
      Line += "'{0}',\n".format(CodeBlockName)
      Line += IndentSpaces
    Line = Line[0:-(len(IndentSpaces) + 2)] + ')\n'
    self._STMFileFh.write(Line)
    
    #--------------------------------------------------------------------------
  def _CodeBlocks(self):
    '''
    CodeBlocks tag.  Creates all the code blocks that are needed for the 
    code block table.
    '''
    # TODO: Only create the Code ones not the Method ones.  
    CBCnt = 0
    for CodeBlockName, CodeBlock in self._SMSResult.CodeBlocks.items():
      CBCnt += 1
      Line = ' ' * self._ForcedOffset

      if CodeBlock.Type == 'Method':
        Line = ' ' * self._ForcedOffset + '__' + CodeBlockName + '__ = \'self.' + CodeBlockName + '()\'\n'
        if CBCnt != len(self._SMSResult.CodeBlocks.keys()):
          Line += "\n"
        self._STMFileFh.write(Line)
      else:
        self._STMFileFh.write("'''\n\n")

    #--------------------------------------------------------------------------
  def _StateNames(self):
    '''
    StateNames tag.  Creates the StateNames table.
    '''
    Line = (' ' * self._ForcedOffset) + 'self.StateNames = ('
    IndentSpaces = ' ' * len(Line)
    self._STMFileFh.write(Line + "'" + self._SMSResult.StateNames[0] + '\',\n')
    Index = 1

    while Index < len(self._SMSResult.StateNames):
      Line = IndentSpaces + "'" + self._SMSResult.StateNames[Index]
      if Index + 1 == len(self._SMSResult.StateNames):
        Line += '\')\n'
      else:
        Line += '\',\n'
      self._STMFileFh.write(Line)
      Index += 1
