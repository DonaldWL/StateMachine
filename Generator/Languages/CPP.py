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

  This supports the C and CPP language
-----------------------------------------------------------------------------
Update History:
  Author: Donald W. Long (Donald.W.Long@gmail.com)
  Date:   Feb 18, 2021
    Released
-----------------------------------------------------------------------------
'''
from collections import namedtuple

from StateMachine.Generator.Languages.Base import _CBase


  #--------------------------------------------------------------------------
class _CCPP(_CBase):
  '''
  See _CBase class for details.
  '''

  def __init__(self, Language, TPLDir, STMDir, OverWrite, LogFh, SMSResult):  
    _CBase.__init__(self, Language, TPLDir, STMDir, OverWrite, LogFh, SMSResult)
    
    if Language not in ('CPP', 'C'):
      raise AttributeError('_CCPP only supports generation of CPP or C code, language passed in ({0})'.format(Language))
    
      # Setup the calls for each command.
    self._CmdExec['RemoveLine'] = None
    self._CmdExec['ReplaceLine'] = self.CmdExecDef(self._ReplaceLine, None)
    self._CmdExec['CreationDate'] = self.CmdExecDef(self._CreationDate, None)
    self._CmdExec['SMSUserAuthor'] = self.CmdExecDef(self._CmdReplacement, self._SMSResult.Author.Value)
    self._CmdExec['SMSUserDate'] = self.CmdExecDef(self._CmdReplacement, self._SMSResult.Date.Value)
    self._CmdExec['SMSUserVersion'] = self.CmdExecDef(self._CmdReplacement, self._SMSResult.Version.Value)
    self._CmdExec['SMSFileVersion'] = self.CmdExecDef(self._CmdReplacement, self._SMSResult.SMSFileVersion.Value)
    self._CmdExec['CodeBlocks'] = self.CmdExecDef(self._CodeBlocks, None)
    self._CmdExec['CodeBlockNames'] = self.CmdExecDef(self._CodeBlockNames, None)
    self._CmdExec['StateNames'] = self.CmdExecDef(self._StateNames, None)
    self._CmdExec['StateTable'] = self.CmdExecDef(self._StateTable, None)
    self._CmdExec['StartState'] = self.CmdExecDef(self._StartState, None)
    self._CmdExec['StartStateValue'] = self.CmdExecDef(self._StartStateValue, None)
    self._CmdExec['EndState'] = self.CmdExecDef(self._EndState, None)
    self._CmdExec['EndStateValue'] = self.CmdExecDef(self._EndStateValue, None)

    if Language == 'CPP':
      self._CmdExec['ClassDefinition'] = self.CmdExecDef(self._ClassDefinition, None)
      self._CmdExec['ClassName'] = self.CmdExecDef(self._CmdReplacement, self._SMSResult.StateMachineName.Value)

  #--------------------------------------------------------------------------
  def _StartState(self):
    '''
    StartState tag
    '''
    StartStateId = self._SMSResult.StateNames.index(self._SMSResult.States.StartState.Param)
    self._STMFileFh.write((' ' * self._ForcedOffset) + 'const int StartState = ' + str(StartStateId) + ';\n')
    
    #--------------------------------------------------------------------------
  def _EndState(self):
    '''
    EndState tag
    '''
    EndStateId = -1
    if self._SMSResult.States.EndState is not None:
      EndStateId = self._SMSResult.StateNames.index(self._SMSResult.States.EndState.Param)
    self._STMFileFh.write((' ' * self._ForcedOffset) + 'const int EndState = ' + str(EndStateId) + ';\n')

    #--------------------------------------------------------------------------
  def _ClassDefinition(self):
    '''
    ClassDefinition tag
    '''
    STplLine = self._TplLine
    self._TplLine = (' ' * self._ForcedOffset) + 'class @@ClassName@@\n'
    self._CmdReplacement()
    self._TplLine = STplLine

    #--------------------------------------------------------------------------
  def _StateTable(self):
    '''
    StateTable tag.  Creates the state table and all its required variables.
    '''
    StateInfoDef = namedtuple('StateInfo', ['Indx', 'OtherWise', 'CodeBlockName', 'TransStates'])
    StateInfo = {}        # Holds all the State infor, key is StatName, item is StateInfoDef
    STLen = 0             # Is the final length of the state table.  Also used to figure out the
                          # Indx in StateInfo
    StartStateIndx = 0    # Contains the Indx for the start state
    EndStateIndx = -1     # Contains the Indx for the end state.  If -1 then no end state defined.
    MaxTranLen = 0        # Maximum length of trans.  Used to position the comment after each
                          # enty of the state table.

      # Generate the Info for each state.
    for StateName in self._SMSResult.StateNames:
      if StateName == self._SMSResult.States.StartState.Param:
        StartStateIndx = STLen
      elif StateName == self._SMSResult.States.EndState.Param:
        EndStateIndx = STLen
        
      StateRec = self._SMSResult.States.StateList[StateName]
      StateTransRec = StateRec.Transitions
      _ListRValues = list(StateTransRec.keys())
      OtherWiseState = ''
      if 'OtherWise' in _ListRValues:
        OtherWiseState = StateTransRec['OtherWise'].State
        _ListRValues.remove('OtherWise')
      StateInfo[StateName] = StateInfoDef(STLen, OtherWiseState, 
                                          self._SMSResult.States.StateList[StateName].CodeBlock, [])

      _ListRValues = list(range(0, max(list(map(int, _ListRValues))) + 1))
      for Idx in range(0, len(_ListRValues)):
        if str(Idx) in StateTransRec.keys():
          StateInfo[StateName].TransStates.append(StateTransRec[str(Idx)].State)
        else:
          StateInfo[StateName].TransStates.append(OtherWiseState)
      STLen += len(StateInfo[StateName].TransStates) + 4

      # Get MaxTranLen for comment at end of each table entry.
    for StateName, xStateInfo in StateInfo.items():
      TLen = len(xStateInfo.CodeBlockName) + 5
      TLen += len(StateName) + 5
      TLen += len(str(len(xStateInfo.TransStates))) + 2
      
      for TranState in xStateInfo.TransStates:
        if TranState in StateInfo.keys():
          TLen += len(str(StateInfo[TranState].Indx)) + 2
        else:
          TLen += 3
      if StateInfo[StateName].OtherWise:
        TLen += len(str(StateInfo[StateInfo[StateName].OtherWise].Indx)) + 2
      else:
        TLen += 3
      MaxTranLen = max(MaxTranLen, TLen)
    MaxTranLen += 1

      # Create the table.
    if self._FileLanguage == 'CPP':
      Line = (' ' * self._ForcedOffset) + 'static const int STLen = ' + str(STLen) + ';\n'
    else:
      Line = (' ' * self._ForcedOffset) + '#define STLen ' + str(STLen) + '\n'
    self._STMFileFh.write(Line)
    Line = ' ' * self._ForcedOffset + 'const int StateTable[STLen] = {'
    tLine = ''
    LineIndent = ' ' * len(Line)
    StateName = ''
    for StateName in self._SMSResult.StateNames:
      tLine = ('CB_' + StateInfo[StateName].CodeBlockName + ', ST_' + StateName + ', ' + 
               str(len(StateInfo[StateName].TransStates)) + ', ')
      for TStateName in StateInfo[StateName].TransStates:
        tLine += str(StateInfo[TStateName].Indx) + ', '
      if StateInfo[StateName].OtherWise: 
        tLine += str(StateInfo[StateInfo[StateName].OtherWise].Indx)
      else:
        tLine += '-1'
        
      if (len(self._SMSResult.StateNames) - 1) == self._SMSResult.StateNames.index(StateName):
        break

      tLine += ', '
      TOtherWise = '-1'
      if StateInfo[StateName].OtherWise: 
        TOtherWise = StateInfo[StateName].OtherWise
      tLine += ' ' * abs((MaxTranLen - len(tLine)))
      Line += tLine + '// {0} ({1}), {2}\n'.format(StateInfo[StateName].Indx,
                                                   ", ".join(StateInfo[StateName].TransStates), 
                                                   TOtherWise)
      self._STMFileFh.write(Line) 
      Line = LineIndent

      # Add the last line
    TOtherWise = '-1'
    if StateInfo[StateName].OtherWise: 
      TOtherWise = StateInfo[StateName].OtherWise
    Line += tLine + '};' 
    Line += ' ' * (abs(MaxTranLen - len(tLine)) - 2)
    Line += '// {0} ({1}), {2}\n'.format(StateInfo[StateName].Indx,
                                         ", ".join(StateInfo[StateName].TransStates), 
                                         TOtherWise)
    self._STMFileFh.write(Line) 

      # Start and Stop Indx's
    Line = (' ' * self._ForcedOffset) + 'const int StartStateIndx = ' + str(StartStateIndx) + ';\n'
    self._STMFileFh.write(Line) 
    Line = (' ' * self._ForcedOffset) + 'const int EndStateIndx = ' + str(EndStateIndx) + ';\n'
    self._STMFileFh.write(Line) 
      
    #--------------------------------------------------------------------------
  def _CodeBlocks(self):
    '''
    CodeBlocks tag.  Creates the code blocks within the switch statement
    '''
    FirstCase = True
    for CodeBlockName in self._SMSResult.CodeBlockNames:
      CodeBlock = self._SMSResult.CodeBlocks[CodeBlockName]
      Line = ' ' * self._ForcedOffset
      if not FirstCase:
        Line = '\n' + Line
      FirstCase = False
      Line += 'case ' + CodeBlockName + ':\n'
      self._STMFileFh.write(Line)
      
      for CodeLine in CodeBlock.CodeLines:
        self._STMFileFh.write(' ' * self._ForcedOffset + '  ' + CodeLine.Line + '\n')
      self._STMFileFh.write(' ' * self._ForcedOffset + '  break;\n')

    #--------------------------------------------------------------------------
  def _CodeBlockNames(self): 
    '''
    CodeBlockNames tag.  Creates the CodeBlock names array
    '''
    
      # Create the CBLen variables
    if self._FileLanguage == 'CPP':
      Line = (' ' * self._ForcedOffset) + 'static const int CBLen = ' + str(len(self._SMSResult.CodeBlockNames)) + ';\n'
    else:
      Line = (' ' * self._ForcedOffset) + '#define CBLen ' + str(len(self._SMSResult.CodeBlockNames)) + '\n'
    self._STMFileFh.write(Line)
    
      # Create the CodeBlockNames variables
    Line = ' ' * self._ForcedOffset + 'const char *CodeBlockNames[CBLen] = {'
    LineIndent = ' ' * len(Line)
    for Indx in range(0, len(self._SMSResult.CodeBlockNames)):
      Line += '"' + self._SMSResult.CodeBlockNames[Indx]
      if Indx != len(self._SMSResult.CodeBlockNames) - 1:
        Line += '",\n'
      else:
        Line += '"};\n'  
      self._STMFileFh.write(Line)
      Line = LineIndent

      # Create the enum. enum CB {
    LineIndent = (' ' * self._ForcedOffset) + (' ' * self._ForcedOffset)
    Line = '\n' + (' ' * self._ForcedOffset) + 'enum CB {\n'
    if self._ForcedOffset == 0:
      LineIndent = '  '
    for Indx in range(0, len(self._SMSResult.CodeBlockNames)):
      Line += '{0}CB_{1} = {2},\n'.format(LineIndent, 
                                          self._SMSResult.CodeBlockNames[Indx],
                                          Indx)
    Line = Line[0:-2] + ('\n' + ' ' * self._ForcedOffset) + '};\n'
    self._STMFileFh.write(Line)

    #--------------------------------------------------------------------------
  def _StateNames(self):
    '''
    StateNames tag.  Creates the StateNames array
    '''
      # Create the SNLen variables
    if self._FileLanguage == 'CPP':
      Line = (' ' * self._ForcedOffset) + 'static const int SNLen = ' + str(len(self._SMSResult.StateNames)) + ';\n'
    else:
      Line = (' ' * self._ForcedOffset) + '#define SNLen ' + str(len(self._SMSResult.StateNames)) + '\n'
    self._STMFileFh.write(Line)
    
      # Create the StateNames variables
    Line = ' ' * self._ForcedOffset + 'const char *StateNames[SNLen] = {'
    LineIndent = ' ' * len(Line)
    for Indx in range(0, len(self._SMSResult.StateNames)):
      Line += '"' + self._SMSResult.StateNames[Indx]
      if Indx != len(self._SMSResult.StateNames) - 1:
        Line += '",\n'
      else:
        Line += '"};\n'  
      self._STMFileFh.write(Line)
      Line = LineIndent
 
      # Create the enum.
    LineIndent = (' ' * self._ForcedOffset) + (' ' * self._ForcedOffset)
    Line = '\n' + (' ' * self._ForcedOffset) + 'enum ST {\n'
    if self._ForcedOffset == 0:
      LineIndent = '  '
    for Indx in range(0, len(self._SMSResult.StateNames)):
      Line += '{0}ST_{1} = {2},\n'.format(LineIndent, 
                                          self._SMSResult.StateNames[Indx],
                                          Indx)
    Line = Line[0:-2] + ('\n' +  ' ' * self._ForcedOffset) + '};\n'
    self._STMFileFh.write(Line)
