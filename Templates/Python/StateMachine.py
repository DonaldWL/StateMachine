'''
SMS User Author:  Donald W. Long
SMS User Date:    01/22/2021
SMS User Version: 1.0
Creation Date:    03/28/21
SMS File Version: 1.0  
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

  A simple state machine that copies one dir to theother.
-----------------------------------------------------------------------------
'''

import os
from enum import IntEnum
from datetime import datetime
from collections import namedtuple

from PythonLib.Base.CreationInfo import CCreationInfo

CBEntryDef = namedtuple('CBEntry', ['CBIndx', 'Code'])
STEntryDef = namedtuple('STEntry', ['CodeBlock', 'StateTransitions', 'Otherwise'])

MSGS_START_STATE_NON_INT = "Start State method returned a non integer: {0} => {1} => {2}"
MSGS_STATE_NON_INT = "State method returned a non integer: {0} => {1} => {2} :: Prev: {3} => {4} => {5}"
MSGS_START_STATE_NEG = "Start State method returned an integer less than 0: {0} => {1} => {2}"
MSGS_STATE_NEG = "State method returned an integer less than 0: {0} => {1} => {2} :: Prev: {3} => {4} => {5}"
MSGS_START_STATE_NOOTHERWISE = "Start State Transition did not have an otherwise: {0} => {1}"
MSGS_STATE_NOOTHERWISE = "State Transition did not have an otherwise: {0} => {1} :: Prev: {2} => {3} => {4}"
MSGS_STATE_INVALID_STATETABLE= "Invalid State Table: Prev State/Value: ({0}:{1}), State: ({2})"
MSGS_EXITEDMAINLOOP = 'Exited main loop'


class CStateMachine():

    #--------------------------------------------------------------------------
  def __init__(self, TraceFileFh = None, LogFileFh = None):
    self.TraceFileFh = TraceFileFh
    self._LogFileFh = LogFileFh
    self.StateRValue = -1
    self.ProcessStates = True
    self.CurStateIndx = -1

      # You must capture the globals and locals for the exec
      # If you wish to control the exec you can set this to what you
      # wish the block of code to have access to.
    self.Globals = globals()
    self.Locals = locals()    

      # Get our module name    
    MFName = os.path.basename(CCreationInfo().CreationFile) #pylint: disable=unused-variable

    class CBB(IntEnum):
      CloseFiles = 0
      CopyFile = 1
      EndMachine = 2
      GetFiles = 3
      NextFile = 4
      OpenFiles = 5
      StartMachine = 6

    self.CodeBlockNames  = ('CloseFiles',
                            'CopyFile',
                            'EndMachine',
                            'GetFiles',
                            'NextFile',
                            'OpenFiles',
                            'StartMachine')
    
    self.CodeBlockTable = (CBEntryDef(CBB.CloseFiles, compile(self.__CloseFiles__, MFName, "exec")),
                           CBEntryDef(CBB.CopyFile, compile(self.__CopyFile__, MFName, "exec")),
                           CBEntryDef(CBB.EndMachine, compile(self.__EndMachine__, MFName, "exec")),
                           CBEntryDef(CBB.GetFiles, compile(self.__GetFiles__, MFName, "exec")),
                           CBEntryDef(CBB.NextFile, compile(self.__NextFile__, MFName, "exec")),
                           CBEntryDef(CBB.OpenFiles, compile(self.__OpenFiles__, MFName, "exec")),
                           CBEntryDef(CBB.StartMachine, compile(self.__StartMachine__, MFName, "exec")))

    class STT(IntEnum):
      CloseFiles = 0
      CloseFilesError = 1
      CopyFile = 2
      EndState = 3
      GetFiles = 4
      NextFile = 5
      OpenFiles = 6
      StartState = 7

    self.StateTable = (STEntryDef(CBB.CloseFiles, (STT.NextFile, STT.EndState, STT.EndState), -1),                                           # CloseFiles
                       STEntryDef(CBB.CloseFiles, (STT.EndState, STT.EndState, STT.EndState), -1),                                           # CloseFilesError
                       STEntryDef(CBB.CopyFile, (STT.CloseFiles, STT.CloseFilesError, STT.CloseFilesError), -1),                             # CopyFile
                       STEntryDef(CBB.EndMachine, (STT.EndState, ), -1),                                                                     # EndState
                       STEntryDef(CBB.GetFiles, (STT.NextFile, STT.EndState), -1),                                                           # GetFiles
                       STEntryDef(CBB.NextFile, (STT.OpenFiles, STT.EndState, STT.EndState, STT.OpenFiles, STT.EndState, STT.NextFile), -1), # NextFile
                       STEntryDef(CBB.OpenFiles, (STT.CopyFile, STT.CloseFilesError, STT.CloseFilesError), -1),                              # OpenFiles
                       STEntryDef(CBB.StartMachine, (STT.GetFiles, STT.EndState), -1))                                                       # StartState

    self.StartStateIdx = 7
    self.EndStateIdx = 3
    
    self.StateNames = ('CloseFiles',
                       'CloseFilesError',
                       'CopyFile',
                       'EndState',
                       'GetFiles',
                       'NextFile',
                       'OpenFiles',
                       'StartState')

    #--------------------------------------------------------------------------
  def Run(self):
    '''
    Runs the state machine.  Will only return when end state is executed.  A
    state machine does not have to have an end state.  The end state can return
    anything it wishes.  So the definition of the return is up to the user.
    '''
    self.CurStateIndx = self.StartStateIdx
    self.StateRValue = -1
    _PrevState = -2
    _xPrevState = -2
    _PrevRStateValue = -1
    _xPrevRStateValue = -1
    _CodeExecute = None
    self.ProcessStates = True
    
    while self.ProcessStates:

        # Validate that our table is ok.
      try:
        _CodeExecute = self.CodeBlockTable[self.StateTable[self.CurStateIndx].CodeBlock].Code
      except IndexError:
        self.Log('Error', MSGS_STATE_INVALID_STATETABLE.format(_PrevState,
                                                               _PrevRStateValue,
                                                               self.CurStateIndx))
        self.ProcessStates = False
        continue

        # Execute the code block, and if state is 0 we end.
      exec(_CodeExecute, self.Globals, self.Locals)  # pylint: disable=exec-used
      if self.CurStateIndx == self.EndStateIdx:
        if self.TraceFileFh is not None:
          Line = '{0}: {1},{2},{3}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                             self.StateNames[self.CurStateIndx],
                                             self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                             self.StateRValue)
          self.TraceFileFh.write(Line)                              
        self.ProcessStates = False
        continue

      # Check for errors
      if not isinstance(self.StateRValue, int):
        if _PrevState == -2:
          self.Log('Error', MSGS_START_STATE_NON_INT.format(self.CurStateIndx,
                                                            self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                                            self.StateRValue))
        else:                                              
          self.Log('Error', MSGS_STATE_NON_INT.format(self.CurStateIndx,
                                                      self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                                      self.StateRValue,
                                                      self.CodeBlockNames[self.StateTable[_PrevState].CodeBlock],
                                                      _PrevState,
                                                      _PrevState))
        self.ProcessStates = False
        continue
        
      if self.StateRValue < 0:
        if _PrevState == -2:
          self.Log('Error', MSGS_START_STATE_NEG.format(self.CurStateIndx,
                                                        self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                                        self.StateRValue))
        else:
          self.Log('Error', MSGS_STATE_NEG.format(self.CurStateIndx,
                                                  self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                                  self.StateRValue,
                                                  self.CodeBlockNames[self.StateTable[_PrevState].CodeBlock],
                                                  _PrevState,
                                                  _PrevRStateValue))
        self.ProcessStates = False
        continue

      if self.TraceFileFh is not None:
        Line = '{0}: {1},{2},{3}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                           self.StateNames[self.CurStateIndx],
                                           self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                           self.StateRValue)
        self.TraceFileFh.write(Line)                              

        # Save the old data away
      _xPrevState = _PrevState
      _xPrevRStateValue = _PrevRStateValue

      _PrevState = self.CurStateIndx
      _PrevRStateValue = self.StateRValue

      # Process the state value that was returned.
      try:
        self.CurStateIndx = self.StateTable[self.CurStateIndx].StateTransitions[self.StateRValue]
      except IndexError:
        self.CurStateIndx = self.StateTable[self.CurStateIndx].Otherwise

      self.StateRValue = None

      # Validate the returned state
      if self.CurStateIndx < 0:
        if _xPrevState == -2:
          self.Log('Error', MSGS_START_STATE_NOOTHERWISE.format(_PrevState,
                                                                self.CodeBlockNames[self.StateTable[_PrevState].CodeBlock]))
        else:
          self.Log('Error', MSGS_STATE_NOOTHERWISE.format(_PrevState,
                                                          self.CodeBlockNames[self.StateTable[_PrevState].CodeBlock],
                                                          self.CodeBlockNames[self.StateTable[_xPrevState].CodeBlock],
                                                          _xPrevState,
                                                          _xPrevRStateValue))
        self.ProcessStates = False
        continue

    if self.ProcessStates:
      self.Log('Error', MSGS_EXITEDMAINLOOP)
    
    #--------------------------------------------------------------------------
  def StartMachine(self):
    print("StartMachine")
    self.StateRValue = 0

    #--------------------------------------------------------------------------
  def GetFiles(self):
    print("GetFiles")
    self.StateRValue = 0

    #--------------------------------------------------------------------------
  def NextFile(self):
    print("NextFile")
    self.StateRValue = 0

    #--------------------------------------------------------------------------
  def OpenFiles(self):
    print("OpenFiles")
    self.StateRValue = 0

    #--------------------------------------------------------------------------
  def CopyFile(self):
    print("CopyFile")
    self.StateRValue = 1

    #--------------------------------------------------------------------------
  def CloseFiles(self):
    print("CloseFiles")
    self.StateRValue = 0

    #--------------------------------------------------------------------------
  def EndMachine(self):
    print("EndMachine")
    self.StateRValue = 0
    self.ProcessStates = False

  __StartMachine__ = 'self.StartMachine()'

  __GetFiles__ = 'self.GetFiles()'

  __NextFile__ = 'self.NextFile()'

  __OpenFiles__ = 'self.OpenFiles()'

  __CopyFile__ = 'self.CopyFile()'

  __CloseFiles__ = 'self.CloseFiles()'

  __EndMachine__ = 'self.EndMachine()'

    #--------------------------------------------------------------------------
  def Log(self, MsgType, *argv):
    if self._LogFileFh is not None:
      Msg = datetime.now().strftime('%Y-%m-%d %H:%M:%S: ') + MsgType + ": "
      for arg in argv:
        Msg += str(arg)
      print(Msg, file=self._LogFileFh)  
