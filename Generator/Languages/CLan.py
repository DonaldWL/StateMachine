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

  This supports the C
-----------------------------------------------------------------------------
Update History:
  Author: Donald W. Long (Donald.W.Long@gmail.com)
  Date:   Feb 18, 2021
    Released
-----------------------------------------------------------------------------
'''
from StateMachine.Generator.Languages.Base import _CBase


  #--------------------------------------------------------------------------
class _CCLan(_CBase):
  '''
  See _CBase class for details.
  '''

  def __init__(self, Language, TPLDir, STMDir, OverWrite, LogFh, SMSResult, Optimize):  
    _CBase.__init__(self, Language, TPLDir, STMDir, OverWrite, LogFh, SMSResult, Optimize)
    
    if Language != 'C':
      raise AttributeError('_CLan only supports C Code, language passed in ({0})'.format(Language))
    
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
    self._CmdExec['CodeBlockValues'] = self.CmdExecDef(self._CodeBlockValues, None)
    self._CmdExec['StateNames'] = self.CmdExecDef(self._StateNames, None)
    self._CmdExec['StateValues'] = self.CmdExecDef(self._StateValues, None)
    self._CmdExec['STIValues'] = self.CmdExecDef(self._STIValues, None)
    self._CmdExec['StateTable'] = self.CmdExecDef(self._StateTable, None)
    self._CmdExec['StartState'] = self.CmdExecDef(self._StartState, None)
    self._CmdExec['EndState'] = self.CmdExecDef(self._EndState, None)
    self._CmdExec['StartStateValue'] = self.CmdExecDef(self._StartStateValue, None)
    self._CmdExec['EndStateValue'] = self.CmdExecDef(self._EndStateValue, None)

    #--------------------------------------------------------------------------
  def _StartState(self):
    '''
    StartState tag
    '''
    self._STMFileFh.write((' ' * self._ForcedOffset) + 'const int StartStateIndx = ' + str(self._StartStateIndx) + ';\n')
    
    #--------------------------------------------------------------------------
  def _EndState(self):
    '''
    EndState tag
    '''
    self._STMFileFh.write((' ' * self._ForcedOffset) + 'const int EndStateIndx = ' + str(self._EndStateIndx) + ';\n')

    #--------------------------------------------------------------------------
  def _STIValues(self):
    LineIndent = (' ' * self._ForcedOffset) + '  '
    Line = (' ' * self._ForcedOffset) + 'enum STI {\n'
    if self._ForcedOffset == 0:
      LineIndent = '  '
    Line += LineIndent + 'STI_CBIdx = 0,\n' 
    if self._Optimize:
      Line += LineIndent + 'STI_StatesIdx = 1\n' 
    else:
      Line += LineIndent + 'STI_StateIdx = 1,\n' 
      Line += LineIndent + 'STI_StateLenIdx = 2,\n' 
      Line += LineIndent + 'STI_StatesIdx = 3\n' 
    
    Line += (' ' * self._ForcedOffset) + '};\n'
    self._STMFileFh.write(Line)
    
    #--------------------------------------------------------------------------
  def _StateTable(self):
    '''
    StateTable tag.  Creates the state table and all its required variables.
    '''

      # Create the table.
    Line = (' ' * self._ForcedOffset) + '#define STLen ' + str(self._STLen) + '\n'
    self._STMFileFh.write(Line)
    Line = ' ' * self._ForcedOffset + 'const int StateTable[STLen] = {'
    tLine = ''
    LineIndent = ' ' * len(Line)
    StateName = ''
    for StateName in self._SMSResult.StateNames:
      if self._Optimize:
        tLine = ('CB_' + self._StateInfo[StateName].CodeBlockName + ', ')
      else:
        tLine = ('CB_' + self._StateInfo[StateName].CodeBlockName + ', ST_' + StateName + ', ' + 
                 str(len(self._StateInfo[StateName].TransStates)) + ', ')
      for TStateName in self._StateInfo[StateName].TransStates:
        tLine += str(self._StateInfo[TStateName].Indx) + ', '
      if not self._Optimize:
        if self._StateInfo[StateName].OtherWise: 
          tLine += str(self._StateInfo[self._StateInfo[StateName].OtherWise].Indx) + ', '
        else:
          tLine += '-1, '
        
      if (len(self._SMSResult.StateNames) - 1) == self._SMSResult.StateNames.index(StateName):
        break

      TOtherWise = '-1'
      if not self._Optimize and self._StateInfo[StateName].OtherWise: 
        TOtherWise = self._StateInfo[StateName].OtherWise
      tLine += ' ' * abs((self._MaxTranLen - len(tLine)))
      if self._Optimize:
        Line += tLine + '/* {0} {2} ({1}) */\n'.format(self._StateInfo[StateName].Indx,
                                                       ", ".join(self._StateInfo[StateName].TransStates),
                                                       StateName) 
      else:
        Line += tLine + '/* {0} ({1}), {2} */\n'.format(self._StateInfo[StateName].Indx,
                                                        ", ".join(self._StateInfo[StateName].TransStates), 
                                                        TOtherWise)
      self._STMFileFh.write(Line) 
      Line = LineIndent

      # Add the last line
    TOtherWise = '-1'
    if not self._Optimize and self._StateInfo[StateName].OtherWise: 
      TOtherWise = self._StateInfo[StateName].OtherWise
    Line += tLine[0:-2] + '};' 
    Line += ' ' * (abs(self._MaxTranLen - len(tLine)) - 2)
    if self._Optimize:
      Line += '  /* {0} {2} ({1}) */\n'.format(self._StateInfo[StateName].Indx,
                                               ", ".join(self._StateInfo[StateName].TransStates),
                                               StateName) 
    else:
      Line += '  /* {0} ({1}), {2} */\n'.format(self._StateInfo[StateName].Indx,
                                                ", ".join(self._StateInfo[StateName].TransStates), 
                                                TOtherWise)
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
  def _CodeBlockValues(self):
    '''
    Create the code block enum.
    ''' 
    LineIndent = (' ' * self._ForcedOffset) + '  '
    Line = (' ' * self._ForcedOffset) + 'enum CB {\n'
    if self._ForcedOffset == 0:
      LineIndent = '  '
    for Indx in range(0, len(self._SMSResult.CodeBlockNames)):
      Line += '{0}CB_{1} = {2},\n'.format(LineIndent, 
                                          self._SMSResult.CodeBlockNames[Indx],
                                          Indx)
    Line = Line[0:-2] + ('\n' + ' ' * self._ForcedOffset) + '};\n'
    self._STMFileFh.write(Line)

    #--------------------------------------------------------------------------
  def _CodeBlockNames(self): 
    '''
    CodeBlockNames tag.  Creates the CodeBlock names array
    '''
    
      # Create the CBLen variables
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

    #--------------------------------------------------------------------------
  def _StateValues(self):
    '''
    Create the enum for states.
    '''
    LineIndent = (' ' * self._ForcedOffset) + '  '
    Line = (' ' * self._ForcedOffset) + 'enum ST {\n'
    if self._ForcedOffset == 0:
      LineIndent = '  '
    for Indx in range(0, len(self._SMSResult.StateNames)):
      Line += '{0}ST_{1} = {2},\n'.format(LineIndent, 
                                          self._SMSResult.StateNames[Indx],
                                          Indx)
    Line = Line[0:-2] + ('\n' +  ' ' * self._ForcedOffset) + '};\n'
    self._STMFileFh.write(Line)

    #--------------------------------------------------------------------------
  def _StateNames(self):
    '''
    StateNames tag.  Creates the StateNames array
    '''
      # Create the SNLen variables
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
