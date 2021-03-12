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
  InFileDir = os.path.join(os.getcwd(), ".")
  OutFileDir = os.path.join(os.getcwd(), "./CopiedFiles")
  TraceFileName = os.path.join(os.getcwd(), "../StateMachineTrace.log")
  LogFileName = os.path.join(os.getcwd(), "../StateMachine.log")
  TraceFileFh = None
  LogFileFh = None
  TraceFriendly = False
  ForceOverwrite = False
    
    # Setup the trace and logging, should do error handling
  TraceFileFh = open(TraceFileName, 'w')
  LogFileFh = open(LogFileName, 'w')

    # Make sure our copy dir exists and it empty.
  if os.path.exists(OutFileDir): 
    if not os.path.isdir(OutFileDir):
      print("OutFileDir exists and is not a directory")
      sys.exit(5)
      
      # If we are not going to do a overwrite then lets clear it out
    if (not ForceOverwrite and os.path.exists(OutFileDir)):
      for file in [os.path.join(OutFileDir, f) for f in os.listdir(OutFileDir) 
                     if os.path.isfile(os.path.join(OutFileDir, f)) and f[0] != '.']:
        os.remove(file)
      os.remdir(OutFileDir)
  os.mkdir(OutFileDir)

    # Create State Machine
  StateMachine = CTheStateMachine(InFileDir = InFileDir,
                                  OutFileDir = OutFileDir,
                                  ForceOverwrite = ForceOverwrite,
                                  TraceFileFh = TraceFileFh, 
                                  FriendlyTrace = TraceFriendly,
                                  LogFileFh = LogFileFh)
  CaptureTimer = CCaptureTimer()
  rvalue = 0
  
    # Run state machine and get how log it took
  print("-" * 50)
  with CCodeTimer("StateRun", CaptureTimer):
    rvalue = StateMachine.Run()

  TraceFileFh.close()
  
  print("\nState machine ended with ({0})".format(rvalue))
  print("State machine duration ({0}ms)".format(CaptureTimer.Took))
  print("-" * 50)
  
  sys.exit(0)
