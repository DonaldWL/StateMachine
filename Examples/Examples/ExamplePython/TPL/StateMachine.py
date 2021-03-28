#@@Python@@
'''
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

  A simple state machine that copies one dir to theother.
-----------------------------------------------------------------------------
'''

import os
import sys
from enum import IntEnum
from datetime import datetime
# @@Imports:0@@

from PythonLib.Base.CreationInfo import CCreationInfo

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

#@@CollectionDefs:0@@

class CStateMachine():

  def __init__(self, InFileDir, OutFileDir, ForceOverwrite = False,  
               TraceFileFh = None, FriendlyTrace = False, LogFileFh = None):
    self.TraceFileFh = TraceFileFh
    self.StateRValue = -1
    self.StartStateIdx = -1
    self.EndStateIdx = -1
    self.CurStateIndx = -1
    self.CodeBlockTable = ()
    self.StateTable = ()
    self.StateNames = ()
    self.CodeBlockNames = ()
    self.Globals = globals()
    self.Locals = locals()

    self._InFileDir = InFileDir
    self._OutFileDir = OutFileDir
    self._Files = None
    self._InFileName = None
    self._InFileFh = None
    self._OutFileName = None
    self._OutFileFh = None
    self._ForceOverwrite = ForceOverwrite
    self._LogFileFh = LogFileFh
    self._Error = False
    self._FriendlyTrace = FriendlyTrace
    
    if not isinstance(FriendlyTrace, bool):
      raise AttributeError('FriendlyTrace must be a bool')
    self.FriendlyTrace = FriendlyTrace

    self.StateRValue = -1
    
      # You must capture the globals and locals for the exec
      # If you wish to control the exec you can set this to what you
      # wish the block of code to have access to.
    self.Globals = globals()
    self.Locals = locals()    

      # Get our module name    
    MFName = os.path.basename(CCreationInfo().CreationFile) #pylint: disable=unused-variable

#   @@CodeBlockNames@@
    
    class CBB(IntEnum): T = 0 # @@RemoveLine@@
    self.CB = CBB # @@RemoveLine@@
#   @@CodeBlockValues@@
    
#   @@CodeBlocks@@

#   @@CodeBlockTable@@
    
    class STT(IntEnum): T = 0 # @@RemoveLine@@
    self.ST = STT  # @@RemoveLine@@
#   @@StateValues@@

#   @@StateTable@@

#   @@StartState@@
#   @@EndState@@
    
#   @@StateNames@@
    self.StateNames = ('a', ) # @@RemoveLine@@

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
    
    while True:

        # Validate that our table is ok.
      try:
        _CodeExecute = self.CodeBlockTable[self.StateTable[self.CurStateIndx].CodeBlock].Code
      except IndexError:
        raise StateMachineError(StateMachineError.MSGS_STATE_INVALID_STATETABLE,
                                _PrevState,
                                _PrevRStateValue,
                                self.CurStateIndx) from IndexError

        # Execute the code block, and if state is 0 we end.
      exec(_CodeExecute, self.Globals, self.Locals)  # pylint: disable=exec-used
      if self.CurStateIndx == self.EndStateIdx:
        if self.TraceFileFh is not None:
          Line = ''
          if self.FriendlyTrace:
            Line = 'State:             {0}\nCode Block:        {1}\nState Entry:       {2}\n'.format(self.StateNames[self.CurStateIndx],
                                                                                                     self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                                                                                     self.RStateValue)
          else:
            Line = '{0}: {1},{2},{3}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                               self.StateNames[self.CurStateIndx],
                                               self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                               self.StateRValue)
          self.TraceFileFh.write(Line)
        return self.StateRValue

      # Check for errors
      if not isinstance(self.StateRValue, int):
        if _PrevState == -2:
          raise StateMachineError(StateMachineError.MSGS_START_STATE_NON_INT,
                                  self.CurStateIndx,
                                  self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                  self.StateRValue)

        raise StateMachineError(StateMachineError.MSGS_STATE_NON_INT,
                                self.CurStateIndx,
                                self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                self.StateRValue,
                                self.CodeBlockNames[self.StateTable[_PrevState].CodeBlock],
                                _PrevState,
                                _PrevState)

      if self.StateRValue < 0:
        if _PrevState == -2:
          raise StateMachineError(StateMachineError.MSGS_START_STATE_NEG,
                                  self.CurStateIndx,
                                  self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                  self.StateRValue)

        raise StateMachineError(StateMachineError.MSGS_STATE_NEG,
                                self.CurStateIndx,
                                self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                self.StateRValue,
                                self.CodeBlockNames[self.StateTable[_PrevState].CodeBlock],
                                _PrevState,
                                _PrevRStateValue)

      if self.TraceFileFh is not None:
        Line = ''
        if self.FriendlyTrace:
          Line = 'State:             {0}\nCode Block:        {1}\nState Entry:       {2}\n'.format(self.StateNames[self.CurStateIndx],
                                                                                                   self.CodeBlockNames[self.StateTable[self.CurStateIndx].CodeBlock],
                                                                                                   self.RStateValue)
        else:
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
          raise StateMachineError(StateMachineError.MSGS_START_STATE_NOOTHERWISE,
                                  _PrevState,
                                  self.CodeBlockNames[self.StateTable[_PrevState].CodeBlock])

        raise StateMachineError(StateMachineError.MSGS_STATE_NOOTHERWISE,
                                _PrevState,
                                self.CodeBlockNames[self.StateTable[_PrevState].CodeBlock],
                                self.CodeBlockNames[self.StateTable[_xPrevState].CodeBlock],
                                _xPrevState,
                                _xPrevRStateValue)

    #--------------------------------------------------------------------------
  def StartMachine(self):
    '''
    StateRValue
      0 -> Ok
      1 -> InFileDir does not exist
           OutFileDir does not exist
           InFileDir and OutFileDir are the same
    '''
    self.StateRValue = 0
    
    self.Log("Info", "InFileDir set to ", self._InFileDir)
    self._InFileDir = os.path.abspath(os.path.expanduser(os.path.expandvars(self._InFileDir)))
    self.Log("Info", "OutFileDir set to ", self._OutFileDir)
    self._OutFileDir = os.path.abspath(os.path.expanduser(os.path.expandvars(self._OutFileDir)))
    if not os.path.exists(self._InFileDir) or not os.path.isdir(self._InFileDir):
      self.Log("Error", "InFileDir (", self._InFileDir, ") is does not exist or is not a directory")
      self.StateRValue = 1
    elif self._InFileDir == self._OutFileDir:
      self.Log("Error", "OutFileDir (", self._OutFileDir, ") is does not exist or is not a directory")
      self.StateRValue = 1
    elif not os.path.exists(self._OutFileDir) or not os.path.isdir(self._OutFileDir):
      self.Log("Error", "InFileDir (", self._InFileDir, ") is the same as OutFileDir (",
               self._OutFileDir, ")")
      self.StateRValue = 1
    
    #--------------------------------------------------------------------------
  def GetFiles(self):
    '''
    StateRValue
      0 -> Ok
      1 -> No files to process in InFileDir
    '''
    self.StateRValue = 0
    
    self._Files = [os.path.join(self._InFileDir, f) 
                     for f in os.listdir(self._InFileDir) 
                       if os.path.isfile(os.path.join(self._InFileDir, f)) and f[0] != '.']
    self.Log("Info", "Number of files to process (", len(self._Files), ") from InFileDir (",
             self._InFileDir, ")")
    if not self._Files:
      self.Log("Error", "No files found to process at InFileDir (", self._InFileDir, ")")
      self.StateRValue = 1
    
    #--------------------------------------------------------------------------
  def NextFile(self):
    '''
    StateRValue
      0 -> Ok
      1 -> No more files to process
      2 -> Out file already exists and not in interactive mode
      3 -> Out File already exists and user stated overwrite the file
      4 -> User does not wish to overwrite file
      5 -> User wishes to skip file
    '''
    self.StateRValue = 0

    if not self._Files:
      self.StateRValue = 1
    else:
      self._InFileName = self._Files.pop(0)
  
      self._OutFileName = os.path.join(self._OutFileDir, os.path.split(self._InFileName)[1])
      if os.path.exists(self._OutFileName):
        if not sys.stdin.isatty():
          self.Log("Error", "Out File (", self._OutFileName, ") exists and not in interactive mode")
          self.StateRValue = 2
        else:
          while True:
            YesNo = input('Out File ({0}) exists, overwrite (Y|N|S)? '.format(os.path.split(self._OutFileName)[1]))
            if YesNo.lower() == 'y':
              self.Log("Warning", "Overwriting file (", self._OutFileName, ")")
              print("Warning: Overwriting file ({0})".format(self._OutFileName))
              self.StateRValue = 3
              break
            if YesNo.lower() == 'n':
              self.Log("Error", "User does not wont to overwrite file (", self._OutFileName,
                  ") ending program")
              self.StateRValue = 4
              break
            if YesNo.lower() == 's':
              self.Log("Info", "User is skipping (", self._OutFileName, ")")
              print("Warning: Skipping file ({0})".format(self._OutFileName))
              self.StateRValue = 5
              break
            
            print("\nInvalid response to question ({0}) must be (Y|N|S)".format(YesNo))
    
    #--------------------------------------------------------------------------
  def OpenFiles(self):
    '''
    StateRValue
      0 -> Ok
      1 -> Unable to open in file
      2 -> Unable to open out file
    '''
    self.StateRValue = 0

    try:
      self.Log("Info", "Opening file InFile ", self._InFileName)
      self._InFileFh = open(self._InFileName, 'r')

      try:
        self.Log("Info", "Opening file OutFile ", self._OutFileName)
        self._OutFileFh = open(self._OutFileName, 'w')
      except (OSError, IOError) as err:
        self.Log("Error", "Unable to open out file (", self._OutFileName, ") => ", str(err))
        self.StateRValue = 2
    except (OSError, IOError) as err:
      self.Log("Error", "Unable to open in file (", self._InFileName, ") => ", str(err))
      self.StateRValue = 1
    
    #--------------------------------------------------------------------------
  def CopyFile(self):
    '''
    StateRValue
      0 -> Ok
      1 -> Read error on InFile
      2 -> Write error on OutFile
    '''
    self.StateRValue = 0

    try:
      self.Log("Info", "Coping file (", self._InFileName, ") to (", self._OutFileName, ")")
      for Line in self._InFileFh:
        try:
          self._OutFileFh.write(Line)
        except (OSError, IOError) as err:
          self.Log("Error", "Unable to write out file (", self._OutFileName, ") => ", str(err))
          self.StateRValue = 2
          break
    except (OSError, IOError) as err:
      self.Log("Error", "Unable to read in file (", self._InFileName, ") => ", str(err))
      self.StateRValue = 1
    
    #--------------------------------------------------------------------------
  def CloseFiles(self):
    '''
    StateRValue
      0 -> Ok
      1 -> Unable to close in file
      2 -> Unable to close out file
    '''
    self.StateRValue = 0
    
    if self._InFileFh is not None:
      try:
        self.Log("Info", "Closing file InFile ", self._InFileName)
        self._InFileFh.close()
      except (OSError, IOError) as err:
        self.StateRValue = 1
        self.Log("Error", "Unable to close in file (", self._InFileName, ") => ", str(err))
      self._InFileFh = None
      
    if self._OutFileFh is not None:
      try:
        self.Log("Info", "Closing file OutFile ", self._InFileName)
        self._OutFileFh.close()
      except (OSError, IOError) as err:
        self.StateRValue = 2 if self.StateRValue == 0 else self.StateRValue
        self.Log("Error", "Unable to close Out file (", self._OutFileName, ") => ", str(err))
      self._OutFileFh = None
    
    #--------------------------------------------------------------------------
  def EndMachine(self):
    '''
    End the state machine.
    '''
    self.CloseFiles()
    self.StateRValue = not self._Error
    self.Log("Info", "Ending State Machine")

    #--------------------------------------------------------------------------
  def Log(self, MsgType, *argv):
    if MsgType == "Error": 
      self._Error = True
    if self._LogFileFh is not None:
      Msg = datetime.now().strftime('%Y-%m-%d %H:%M:%S: ') + MsgType + ": "
      for arg in argv:
        Msg += str(arg)
      print(Msg, file=self._LogFileFh)  
