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

  This is the base module for all the languages.  They inherit this class
  to process all the tags.  Many of the tags have shared code in this file.
  But if you need to override the method do so.
-----------------------------------------------------------------------------
Update History:
  Author: Donald W. Long (Donald.W.Long@gmail.com)
  Date:   Feb 18, 2021
    Released
-----------------------------------------------------------------------------
'''
from abc import ABC
import os
import datetime
from collections import namedtuple

from PythonLib.Base.StringHandlers import SkipWhiteSpace
from StateMachine.SMS.Definitions import LanguagesSupported


  #--------------------------------------------------------------------------
class GenException(Exception):
  pass

  #--------------------------------------------------------------------------
class _CBase(ABC):
  '''
  Base class for all languages.  Each specific language class inherits from
  this class to implement all the tags and processing of all the TPL files.
  
  All tags have the executing method stored in '_CmdExec'.  This is a 
  dictionary with the name of the tag as the key.  The item in the
  dictionary is of 'CmdExecDef'.  Lots of other variables are available
  for your use.  Just read the code, to many to doc.
  '''
  CmdExecDef = namedtuple('CmdExec', ['Method', 'Value'])
  
    # Each item in self._StateInfo. 
    #   Indx
    #     Is the indx in the state table for this state
    #   OtherWise
    #     Is the otherwise setting.  If optimize this will always
    #     be an empty string.
    #   CodeBlockName
    #     Is the name of the code block for this state entry
    #   TransStates
    #     Is a list of the transitions.  If optimize will not be filled.
  StateInfoDef = namedtuple('StateInfo', ['Indx', 'OtherWise', 'CodeBlockName', 'TransStates'])

  def __init__(self, Language, TPLDir, STMDir, OverWrite, LogFh, SMSResult, Optimize):  
    self._Language = Language
    self._TPLDir = TPLDir
    self._STMDir = STMDir
    self._OverWrite = OverWrite
    self._LogFh = LogFh
    self._SMSResult = SMSResult
    self._Optimize = Optimize

    self._TPLLineCnt = 0
    self._STMFileFh = None
    self._FileLanguage = None
    
    self._TplLine = None
    self._StrtCmdOffset = -1
    self._EndCmdOffset = -1
    self._ForcedOffset = -1
    self._Cmd = None
    self._TPLFileName = None
    self._STMFileName = None
    self._CmdExec = {}
    self._CmdExecEntry = None
    self._CopyFileOnly = False
    
    self._TPLFilesToProcess = [os.path.join(TPLDir, f) for f in os.listdir(self._TPLDir) 
                                if os.path.isfile(os.path.join(self._TPLDir, f)) and f[0] != '.']
    if not self._TPLFilesToProcess:
      raise AttributeError('No files found to process in TPLDir ({0})'.format(self._TPLDir))
    
    self._StateInfo = {}       # Holds all the State infor, key is StatName, item is StateInfoDef
    self._StartStateIndx = -1  # Index into the table for the start state
    self._EndStateIndx = -1    # Index into the table for end state.  This is really only needed
                               # for python
    self._STLen = 0            # Length of the state table.
    self._MaxTranLen = 0       # Maximum length of trans.  Used to position the comment after each
                               # enty of the state table.
                               
    self._BuildStateInfo()

    #--------------------------------------------------------------------------
  def Process(self):
    '''
    This is called to process all the TPL files.
    '''
    for self._TPLFileName in self._TPLFilesToProcess:
      self._CopyFileOnly = False
      self._STMFileName = os.path.join(self._STMDir, os.path.split(self._TPLFileName)[1])
      if os.path.exists(self._STMFileName):
        if not self._OverWrite:
          self._LogFh.write('Warning: Skipping STM File {0} OverWrite set to False\n'.format(self._STMFileName))
          continue
        self._LogFh.write('Warning: Overwriting STM File {0}\n'.format(self._STMFileName))
        
      self._LogFh.write('Message: Processing TPL File {0}\n'.format(self._TPLFileName))
      try:
        with open(self._TPLFileName, 'r') as TPLFileFh:
          self._LogFh.write('Message: Producing STM File {0}\n'.format(self._STMFileName))
          try:
            with open(self._STMFileName, 'w') as self._STMFileFh:
              self._TPLLineCnt = 0
              try:
                for self._TplLine in TPLFileFh:
                  try:
                    if self._CopyFileOnly:
                      self._STMFileFh.write(self._TplLine)
                    elif not self._ProcessLine():
                      break
                  except (IOError, SystemError) as err:
                    raise GenException("Write Error on STM {0} => {1}".format(self._STMFileName, str(err))) from err
              except (IOError, SystemError) as err:
                raise GenException("Read Error on TPL {0} => {1}".format(self._TPLFileName, str(err))) from err
          except (IOError, SystemError) as err:
            raise GenException("Open Error on STM {0} => {1}".format(self._STMFileName, str(err))) from err
      except (IOError, SystemError) as err:
        raise GenException("Open Error on TPL {0} => {1}".format(self._TPLFileName, str(err))) from err

    #--------------------------------------------------------------------------
  def _BuildStateInfo(self):
    '''
    Builds up the state info.  This is used to complete the state table.
    '''
    self._StateInfo = {}
    self._StartStateIndx = -1
    self._EndStateIndx = -1
    self._STLen = 0
    self._MaxTranLen = 0

    for StateName in self._SMSResult.StateNames:
      if StateName == self._SMSResult.States.StartState.Param:
        self._StartStateIndx = self._STLen
      elif StateName == self._SMSResult.States.EndState.Param:
        self._EndStateIndx = self._STLen
        
      StateRec = self._SMSResult.States.StateList[StateName]
      StateTransRec = StateRec.Transitions
      _ListRValues = list(StateTransRec.keys())
      OtherWiseState = ''
      
        # If otherwise is defined in the SMS file and we have optimize set
        # then error.  You can not use otherwise with optimize.
      if 'OtherWise' in _ListRValues and self._Optimize:
        raise AttributeError('If argument Optimize is true you can not have an otherwise ({0})'.format(StateName))

      if 'OtherWise' in _ListRValues:
        OtherWiseState = StateTransRec['OtherWise'].State
        _ListRValues.remove('OtherWise')
      self._StateInfo[StateName] = self.StateInfoDef(self._STLen, OtherWiseState, 
                                                     self._SMSResult.States.StateList[StateName].CodeBlock, [])

        # Fill in all the missing r values.  If the SMS file RValues are not
        # filled i.e., 0, 3, 5 then fill in with 0, 1, 2, 3, 4, 5.  
      _ListRValues = list(range(0, max(list(map(int, _ListRValues))) + 1))
      for Idx in range(0, len(_ListRValues)):
        if str(Idx) in StateTransRec.keys():
          self._StateInfo[StateName].TransStates.append(StateTransRec[str(Idx)].State)
        else:
          self._StateInfo[StateName].TransStates.append(OtherWiseState)

      if self._Optimize:
        if '' in self._StateInfo[StateName].TransStates:
          raise AttributeError('If argument Optimize is true you can not have return values that are not sequential ({0})'.format(StateName))
        self._STLen += len(self._StateInfo[StateName].TransStates) + 1
      else:
        self._STLen += len(self._StateInfo[StateName].TransStates) + 4
        
    self._CalcMaxTranLen()

    #--------------------------------------------------------------------------
  def _CalcMaxTranLen(self):
    '''
    Figure out the max trans length
    '''
      # Get MaxTranLen for comment at end of each table entry.
    for StateName, xStateInfo in self._StateInfo.items():
      TLen = len(xStateInfo.CodeBlockName) + 5
      if not self._Optimize:
        TLen += len(StateName) + 5
        TLen += len(str(len(xStateInfo.TransStates))) + 2
      else:
        TLen += len(str(len(xStateInfo.TransStates)))
      
      for TranState in xStateInfo.TransStates:
        if TranState in self._StateInfo.keys():
          TLen += len(str(self._StateInfo[TranState].Indx)) + 2
        else:
          TLen += 3
      if not self._Optimize:
        if self._StateInfo[StateName].OtherWise:
          TLen += len(str(self._StateInfo[self._StateInfo[StateName].OtherWise].Indx)) + 2
        else:
          TLen += 3
      self._MaxTranLen = max(self._MaxTranLen, TLen)
    if not self._Optimize:
      self._MaxTranLen += 1
        
    #--------------------------------------------------------------------------
  def _ProcessLine(self):
    '''
    Process each line from the TPL line.
    '''
    self._TPLLineCnt += 1
    self._Cmd = ''
    self._StrtCmdOffset = self._TplLine.find('@@')
    if self._StrtCmdOffset != -1:
      self._EndCmdOffset = self._TplLine.find('@@', self._StrtCmdOffset + 2)
      if self._EndCmdOffset != -1:
        self._EndCmdOffset += 2
        self._Cmd = self._TplLine[self._StrtCmdOffset + 2:self._EndCmdOffset - 2]
  
      # Make sure the language is valid
    if self._TPLLineCnt == 1:
      if self._Cmd == 'CopyFile':
        self._CopyFileOnly = True
        Msg = 'Warning: Copying File {0} no tag processing\n'
        self._LogFh.write(Msg.format(self._TPLFileName))
        return True
      if self._Cmd == 'SkipFile':
        Msg = 'Warning: Skipping file {0}\n'
        self._LogFh.write(Msg.format(self._TPLFileName))
        return False
      
      if self._Cmd not in LanguagesSupported:
        Msg = 'Error: The language {0} in TPL file {2} is not supported, validate entries are {1} Skipping file\n'
        self._LogFh.write(Msg.format(self._Cmd, LanguagesSupported, self._TPLFileName))
        return False
      
      ParamList = []
      for Param in self._SMSResult.Language.Params:
        ParamList.append(Param.Param)
      if self._Cmd not in ParamList:
        Msg = 'Error: Language {0} in TPL file {2} does not match the SMS file ({1}) Skipping file\n'
        self._LogFh.write(Msg.format(self._Cmd, ', '.join(ParamList), self._TPLFileName))
        return False
        
      if not self._Cmd == self._Language:
        raise GenException('Language {0} in TPL file is not {1}'.format(self._Cmd, self._Language))
      self._FileLanguage = self._Cmd
      return True
  
    if self._Cmd:
      self._ForcedOffset = self._StrtCmdOffset
      if ':' in self._Cmd:
        self._Cmd, self._ForcedOffset = self._Cmd.split(':')
        self._ForcedOffset = self._ForcedOffset.strip()
        try:
          self._ForcedOffset = abs(int(self._ForcedOffset))
        except ValueError:
          self._ForcedOffset = self._StrtCmdOffset

        # Execute the method stored in self._CmdExec.  If not found
        # then warning but continue.
      try:
        if self._CmdExec[self._Cmd] is not None:
          self._CmdExecEntry = self._CmdExec[self._Cmd]
          self._CmdExec[self._Cmd].Method()
      except KeyError:
        Msg = 'Warning: Unsupported Command {0} found in TPL file {1}\n'
        self._LogFh.write(Msg.format('@@' + self._Cmd + '@@', self._TPLFileName))
    else:
      self._STMFileFh.write(self._TplLine)
      
    return True

    #--------------------------------------------------------------------------
  def _CreationDate(self):
    '''
    CreateDate tag
    '''
    Date = datetime.datetime.now()
    SCmdExecEntry = self._CmdExecEntry
    self._CmdExecEntry = self.CmdExecDef(None, Date.strftime("%m/%d/%y"))
    self._CmdReplacement()
    self._CmdExecEntry = SCmdExecEntry

    #--------------------------------------------------------------------------
  def _StartStateValue(self):
    '''
    StartStateValue tag
    '''
    SCmdExecEntry = self._CmdExecEntry
    if self._Language == 'Python':
      StartStateId = self._SMSResult.StateNames.index(self._SMSResult.States.StartState.Param)
      self._CmdExecEntry = self.CmdExecDef(None, str(StartStateId))
    else:
      self._CmdExecEntry = self.CmdExecDef(None, str(self._StartStateIndx))
    self._CmdReplacement()
    self._CmdExecEntry = SCmdExecEntry

    #--------------------------------------------------------------------------
  def _EndStateValue(self):
    '''
    EndStateValue tag
    '''
    SCmdExecEntry = self._CmdExecEntry
    if self._Language == 'Python':
      EndStateId = -1
      if self._SMSResult.States.EndState is not None:
        EndStateId = self._SMSResult.StateNames.index(self._SMSResult.States.EndState.Param)
      self._CmdExecEntry = self.CmdExecDef(None, str(EndStateId))
    else:
      self._CmdExecEntry = self.CmdExecDef(None, str(self._EndStateIndx))
    self._CmdReplacement()
    self._CmdExecEntry = SCmdExecEntry

    #--------------------------------------------------------------------------
    # TODO: Remove
  def _CmdReplacement(self):
    '''
    A general command replacement.  Replaces the tag with the value in
    self._CmdExecEntry.Value
    '''
    if self._CmdExecEntry.Value is not None:
      self._STMFileFh.write(self._TplLine.replace('@@' + self._Cmd + '@@', self._CmdExecEntry.Value))
    else:
      pass # TODO: Error
      
  def _ReplaceLine(self):
    '''
    ReplaceLine tag.
    '''
    xOffset = SkipWhiteSpace(self._TplLine[self._EndCmdOffset:])
    xTplLine = self._TplLine[self._EndCmdOffset + xOffset:]
    xCmd = ''
    xStrtCmdOffset = xTplLine.find('@@')
    if xStrtCmdOffset != -1:
      xEndCmdOffset = xTplLine.find('@@', xStrtCmdOffset + 2)
      if xEndCmdOffset != -1:
        xEndCmdOffset += 2
        xCmd = xTplLine[xStrtCmdOffset + 2:xEndCmdOffset - 2]
        
        if xCmd in self._CmdExec.keys():
          xTplLine = (' ') * self._ForcedOffset + xTplLine
          sTplLine = self._TplLine
          sCmd = self._Cmd
          self._TplLine = xTplLine
          self._Cmd = xCmd
          sCmdExecEntry = self._CmdExecEntry

          self._CmdExecEntry = self._CmdExec[self._Cmd]
          self._CmdExec[self._Cmd].Method()
                  
          self._CmdExecEntry = sCmdExecEntry
          self._TplLine = sTplLine
          self._Cmd = sCmd
        else:    
          self._STMFileFh.write((' ' * self._ForcedOffset) + xTplLine)
    else:    
      self._STMFileFh.write((' ' * self._ForcedOffset) + xTplLine)
  