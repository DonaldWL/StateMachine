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

from PythonLib.Base.CreationInfo import CCreationInfo
from StateMachine.PythonBase import (CodeBlockEntryDef as CBEntryDef, # pylint: disable=unused-import
                                     CStateMachine,
                                     StateTableEntryDef as STEntryDef,
                                     StateMachineError)

class CTheStateMachine(CStateMachine):

  def __init__(self, InFileDir, OutFileDir, ForceOverwrite = False,  
               TraceFileFh = None, FriendlyTrace = False, LogFileFh = None):
    CStateMachine.__init__(self, TraceFileFh, FriendlyTrace)
    
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
    
    self.StateRValue = -1
    
      # You must capture the globals and locals for the exec
      # If you wish to control the exec you can set this to what you
      # wish the block of code to have access to.
    self.Globals = globals()
    self.Locals = locals()    

      # Get our module name    
    MFName = os.path.basename(CCreationInfo().CreationFile) #pylint: disable=unused-variable

    class CBB(IntEnum): T = 0 # @@RemoveLine@@ pylint: disable=multiple-statements 
#   @@CodeBlockTable@@
    self.CB = CBB # Used to allow access outside of __init__
    
#   @@StartState@@
#   @@EndState@@
  
    class STT(IntEnum): T = 0 # @@RemoveLine@@ pylint: disable=multiple-statements
#   @@StateTable@@
    self.ST = STT  # Used to allow access outside of __init__
    
    self.StateNames = ('a', ) # @@RemoveLine@@
#   @@StateNames@@

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
    
  def EndMachine(self):
    '''
    End the state machine.
    '''
    self.CloseFiles()
    self.StateRValue = not self._Error
    self.Log("Info", "Ending State Machine")

  def Log(self, MsgType, *argv):
    if MsgType == "Error": 
      self._Error = True
    if self._LogFileFh is not None:
      Msg = datetime.now().strftime('%Y-%m-%d %H:%M:%S: ') + MsgType + ": "
      for arg in argv:
        Msg += str(arg)
      print(Msg, file=self._LogFileFh)  
      
    # Overrides from base class, this is standard
  def GetCodeBlockName(self, CBIndex):
    return self.CB(self.CodeBlockTable[CBIndex].CBIndx).name

  def GetStateName(self, SNIndex):
    return self.StateNames[SNIndex]

# @@CodeBlocks@@
