'''
Created:   Feb 21, 2021
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

  Is a state machine engine.  This allows you to define your state machine and
  use the class to execute your state machine.  You inherit the state machine
  class and fill in the tables and define your code blocks.  A code block
  relates to states.  Each state has to execute a code block.  More than
  one state can execute the same code block.

  For further details see the help file for this module.
-----------------------------------------------------------------------------
Exceptions:

  Python Exceptions
    AttributeError
      The passed in parameter was not valid type.

  MyStateMachine Defined Exceptions
    StateMachineError
      If any error occurs with the state machine this is the
      exception that will be raised.  Index errors from RStateValue,
      index errors from State, invalid return values from methods and
      invalid state table.
-----------------------------------------------------------------------------
Required Libraries:

  Python
    from abc import (ABCMeta, abstractmethod)
    from collections import namedtuple
-----------------------------------------------------------------------------
Update History:
  Feb 21, 2021 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''
from abc import (ABCMeta, abstractmethod)
from collections import namedtuple
from datetime import datetime

  #--------------------------------------------------------------------------
class StateMachineError(Exception):
  '''
  If an error occurs in accessing the state table this will be raised.
  This has overriding the Exception class and the first argument must
  be an int that is the message number to use.  You pass all values for
  the message after message number.  See the code for a list of message
  numbers.
  '''

  MSGS_START_STATE_NON_INT = 0
  MSGS_STATE_NON_INT = 1
  MSGS_START_STATE_NEG = 2
  MSGS_STATE_NEG = 3
  MSGS_START_STATE_NOOTHERWISE = 4
  MSGS_STATE_NOOTHERWISE = 5
  MSGS_STATE_INVALID_STATETABLE = 6

  MSGS = ("Start State method returned a non integer: {0} => {1} => {2}",
          "State method returned a non integer: {0} => {1} => {2} :: Prev: {3} => {4} => {5}",
          "Start State method returned an integer less than 0: {0} => {1} => {2}",
          "State method returned an integer less than 0: {0} => {1} => {2} :: Prev: {3} => {4} => {5}",
          "Start State Transition did not have an otherwise: {0} => {1}",
          "State Transition did not have an otherwise: {0} => {1} :: Prev: {2} => {3} => {4}",
          "Invalid State Table: Prev State/Value: ({0}:{1}), State: ({2})")

  def __init__(self, MessageNo, *args):
    Exception.__init__(self, "StateMachineError: " + self.MSGS[MessageNo].format(*args))


  # Define the tuple used in the CodeBlockTable.
CodeBlockEntryDef = namedtuple('CodeBlockEntry', ['CBIndx', 'Code'])

  # Define the tuple used in the StateTable.
StateTableEntryDef = namedtuple('StateTableEntry', ['CodeBlock', 'StateTransitions', 'Otherwise'])

  #--------------------------------------------------------------------------
class CStateMachine(metaclass=ABCMeta):
  '''
  This is the base class for the state machine.  You should inherit this class and fill in all
  the tables and create your code blocks.  For details on how to implement this state machine
  see the documenation of the file.

  CStateMachine(TraceFileFh = None, FriendlyTrace = False)
    TraceFileFh
      This is either None, no tracing or an instance of CTraceFile.  See Libs.Base.TraceFileFh
      for details on how to use TraceFileFh.
    FriendlyTrace
      If True output a nicer trace for usable reading, but is very verbose.  Same data just
      displayed easer for a person to read.
  '''

  def __init__(self, TraceFileFh = None, FriendlyTrace = False):
    object.__init__(self)

    self.TraceFileFh = TraceFileFh
    self.FriendlyTrace = FriendlyTrace
    self.StateRValue = -1
    self.StartState = -1
    self.EndState = -1
    self.CodeBlockTable = ()
    self.StateTable = ()
    self.StateNames = ()
    self.Globals = globals()
    self.Locals = locals()
    
    if not isinstance(FriendlyTrace, bool):
      raise AttributeError('FriendlyTrace must be a bool')

    #--------------------------------------------------------------------------
  @abstractmethod
  def GetCodeBlockName(self, CBIndex):
    '''
    Must be overriding.  This returns the CodeBlock name from the index.
    '''
    pass # pylint: disable=unnecessary-pass
  
    #--------------------------------------------------------------------------
  @abstractmethod
  def GetStateName(self, SNIndex):
    '''
    Must be overriding.  This returns the State name from the index.
    '''
    pass # pylint: disable=unnecessary-pass

    #--------------------------------------------------------------------------
  def Run(self):
    '''
    Runs the state machine.  Will only return when end state is executed.  A
    state machine does not have to have an end state.  The end state can return
    anything it wishes.  So the definition of the return is up to the user.
    '''
    _StateCmd = self.StartState
    self.StateRValue = -1
    _PrevState = -2
    _xPrevState = -2
    _PrevRStateValue = -1
    _xPrevRStateValue = -1
    _CodeExecute = None
    
    while True:

        # Validate that our table is ok.
      try:
        _CodeExecute = self.CodeBlockTable[self.StateTable[_StateCmd].CodeBlock].Code
      except IndexError:
        raise StateMachineError(StateMachineError.MSGS_STATE_INVALID_STATETABLE,
                                _PrevState,
                                _PrevRStateValue,
                                _StateCmd) from IndexError

        # Execute the code block, and if state is 0 we end.
      exec(_CodeExecute, self.Globals, self.Locals)  # pylint: disable=exec-used
      if _StateCmd == self.EndState:
        if self.TraceFileFh is not None:
          StateTableEntry = self.StateTable[_StateCmd]
  
          PrevStateTableEntry = None
          if _PrevState > -1:
            PrevStateTableEntry = self.StateTable[_PrevState]
          self.TraceStates(StateTableEntry, _StateCmd, self.StateRValue, PrevStateTableEntry,
                           _PrevState, _PrevRStateValue)
        return self.StateRValue

      # Check for errors
      if not isinstance(self.StateRValue, int):
        if _PrevState == -2:
          raise StateMachineError(StateMachineError.MSGS_START_STATE_NON_INT,
                                  _StateCmd,
                                  self.GetCodeBlockName(self.StateTable[_StateCmd].CodeBlock),
                                  self.StateRValue)

        raise StateMachineError(StateMachineError.MSGS_STATE_NON_INT,
                                _StateCmd,
                                self.GetCodeBlockName(self.StateTable[_StateCmd].CodeBlock),
                                self.StateRValue,
                                self.GetCodeBlockName(self.StateTable[_PrevState].CodeBlock),
                                _PrevState,
                                _PrevState)

      if self.StateRValue < 0:
        if _PrevState == -2:
          raise StateMachineError(StateMachineError.MSGS_START_STATE_NEG,
                                  _StateCmd,
                                  self.GetCodeBlockName(self.StateTable[_StateCmd].CodeBlock),
                                  self.StateRValue)

        raise StateMachineError(StateMachineError.MSGS_STATE_NEG,
                                _StateCmd,
                                self.GetCodeBlockName(self.StateTable[_StateCmd].CodeBlock),
                                self.StateRValue,
                                self.GetCodeBlockName(self.StateTable[_PrevState].CodeBlock),
                                _PrevState,
                                _PrevRStateValue)

      if self.TraceFileFh is not None:
        StateTableEntry = self.StateTable[_StateCmd]

        PrevStateTableEntry = None
        if _PrevState > -1:
          PrevStateTableEntry = self.StateTable[_PrevState]
        self.TraceStates(StateTableEntry, _StateCmd, self.StateRValue, PrevStateTableEntry,
                         _PrevState, _PrevRStateValue)

        # Save the old data away
      _xPrevState = _PrevState
      _xPrevRStateValue = _PrevRStateValue

      _PrevState = _StateCmd
      _PrevRStateValue = self.StateRValue

      # Process the state value that was returned.
      try:
        _StateCmd = self.StateTable[_StateCmd].StateTransitions[self.StateRValue]
      except IndexError:
        _StateCmd = self.StateTable[_StateCmd].Otherwise

      self.StateRValue = None

      # Validate the returned state
      if _StateCmd < 0:
        if _xPrevState == -2:
          raise StateMachineError(StateMachineError.MSGS_START_STATE_NOOTHERWISE,
                                  _PrevState,
                                  self.GetCodeBlockName(self.StateTable[_PrevState].CodeBlock))

        raise StateMachineError(StateMachineError.MSGS_STATE_NOOTHERWISE,
                                _PrevState,
                                self.GetCodeBlockName(self.StateTable[_PrevState].CodeBlock),
                                self.GetCodeBlockName(self.StateTable[_xPrevState].CodeBlock),
                                _xPrevState,
                                _xPrevRStateValue)

    #--------------------------------------------------------------------------
  def TraceStates(self, StateTableEntry, State, RStateValue, PrevStateTableEntry, # pylint: disable=unused-argument
                  PrevState, PrevRStateValue):                                    # pylint: disable=unused-argument
    '''
    Outputs trace data without previous state info.

    TraceStates(StateTableEntry, State, RStateValue,
                PrevStateTableEntry, PrevState, PrevRStateValue)

      StateTableEntry
        This is the entry in the state table that was just executed.  For details
        of this entry see the definition of the state table.

      State
        This is the state that was just executed.

      RStateValue
        This is the return value from the method of the state.

      PrevStateTableEntry
        This is the entry in the state table that was previously executed.  For
        details of this entry see the definition of the state tab.e

      PrevState
        This is the previous state that was executed.  If -2 then State is the
        start state and we do not have a prev state.

      PrevRStateValue
        This is the return value from the method of the previous state.
    '''
    Line = ''
    Statetxt = '-1'
    if State > -1:
      Statetxt = self.StateNames[State]
    StateTableEntrytxt = ""

    if StateTableEntry is not None:
      TransLine = '('
      for Trans in StateTableEntry.StateTransitions:
        if Trans != -1:
          TransLine += str(Trans).split('.')[1] + ', '
        else:
          TransLine += '-1, '
      if len(StateTableEntry.StateTransitions) != 1:
        TransLine = TransLine[0:-2]
      TransLine += ')'
      OtherWise = '-1'
      if StateTableEntry.Otherwise != -1:
        OtherWise = self.GetStateName(StateTableEntry.Otherwise) 
      StateTableEntrytxt = "{0}, {1}, {2}".format(self.GetCodeBlockName(StateTableEntry.CodeBlock),
                                                  TransLine,
                                                  OtherWise)

    Line = ''
    if self.FriendlyTrace:
      Line = 'State:             {0}\nState RValue:      {1}\nState Entry:       {2}\n'.format(Statetxt,
                                                                                               RStateValue,
                                                                                               StateTableEntrytxt)
    else:
      Line = '{3}: {0}, {1}, {2}'.format(Statetxt, RStateValue, StateTableEntrytxt,
                                         datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 

    Line += '\n'
    self.TraceFileFh.write(Line)
