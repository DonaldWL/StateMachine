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

from PythonLib.Base.CodeTimer import (CCaptureTimer, CCodeTimer)
from TheStateMachine import CTheStateMachine

if __name__ == "__main__":
  
    # Setup a log file
  LogFileName = os.path.join(os.getcwd(), 'StateMachine.log')
  LogFileFh = open(LogFileName, 'w')

    # Make sure our copy dir exists and it empty.
  CPFDir = '../CopiedFiles'
  if os.path.exists(CPFDir):
    if not os.path.isdir(CPFDir):
      print("CopiedFiles exists and is not a directory")
      sys.exit(5)
      
    for file in [os.path.join(CPFDir, f) for f in os.listdir(CPFDir) 
                   if os.path.isfile(os.path.join(CPFDir, f)) and f[0] != '.']:
      os.remove(file)
  else:
    os.mkdir(CPFDir)

    # Create State Machine
  StateMachine = CTheStateMachine(InFileDir = '../',
                                  OutFileDir = CPFDir,
                                  ForceOverwrite = False,
                                  TraceFile = LogFileFh, 
                                  FriendlyTrace = False)
  CaptureTimer = CCaptureTimer()
  rvalue = 0
  
    # Run state machine and get how log it took
  print("-" * 50)
  with CCodeTimer("StateRun", CaptureTimer):
    rvalue = StateMachine.Run()

  LogFileFh.close()
  
  print("\nState machine ended with ({0})".format(rvalue))
  print("State machine states processed ({0})".format(StateMachine.StatesProcessed))
  print("State machine duration ({0}ms)".format(CaptureTimer.Took))
  print("-" * 50)
  
  sys.exit(0)
