'''
Created:   Feb 22, 2021
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

  Used to build the results in Libs.StateMachine.SMS.Results.CSMSResult.
  After BuildResutls is called the CSMSResult will be filled in.  This is
  only used in Libs.StateMachine.SMS.Process.CSMSProcess._Validate
-----------------------------------------------------------------------------
Description:

  Is a program that you can use to generate your state machine.  For how
  to use this "Gen.py -h".  If you wish to see the exit codes for this
  program "Gen.py -e".
  
  See the file BuildExamples.cmd on how to build the examples.  It does not
  compile the C or CPP it just using Gen.py to generate the state machine.
  
  Also see the help files for SMS, Generator, PythonBase for more details
  on how to use this system.  The best you can do is look at the examples.
  
  You should review this file, if you are going to use the SMS and Generator
  package in your own code, this will give you a good example on how to
  use them.  What you need to understand starts at around line 160.
-----------------------------------------------------------------------------
Update History:
  Feb 22, 2021 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''
import sys
import os
from enum import (IntEnum, unique)

from PythonLib.Help import (CHelp, TagInfoDef, TagTypes)
from PythonLib.Base.Converters import ConvertMillisecondsDays  
from StateMachine.SMS import (CSMSProcess, SMSReport, LanguagesSupported)
from StateMachine.Generator import CGenerator

@unique
class ExitCodes(IntEnum):
  OK           = 0
  HELP         = 2
  INVALIDARGS  = 3
  SMSERROR     = 4
  FILENOTFOUND = 5
  ISDIR        = 6
  ISNOTDIR     = 7
  
MYMODULEDIR = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
MYHELPFILEDIR = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/HelpFiles')
PROGRAMNAME = 'gen'
MAJORVESION = "1"
MINORVERSION = "0"
VERSION = "{0}.{1}".format(MAJORVESION, MINORVERSION)
RELEASEYEAR = "2021"
RELEASEMONTH = "03"
RELEASEDAY = "09"
RELEASEDATE = "{0}-{1}-{2}".format(RELEASEMONTH, RELEASEDAY, RELEASEYEAR)

COPYRIGHT = '''
  Copyright (C) 2020-2021  Donald W. Long (Donald.W.Long@gmail.com)

  This program comes with ABSOLUTELY NO WARRANTY; for details type
  `gen --help w[arranty]'.  This is free software, and you are welcome to
  redistribute it under certain conditions; type `gen --help c[opyright]'
  for details.
'''
  
def Help(Topics):
  Tags = {'LANGUAGE': TagInfoDef(TagTypes.SINGLEWORD, ', '.join(LanguagesSupported)),
          'LANGUAGELIST': TagInfoDef(TagTypes.PARAGRAPH, LanguagesSupported)}
  
  HelpSys = CHelp(HelpDirs = [MYHELPFILEDIR, MYMODULEDIR],
                  TopicSeperatorLine = '\n',
                  PreTopic = 'usage',
                  PostTopic = None,
                  TopicIndent = 2,
                  CopyRight = COPYRIGHT,
                  OutFile = None,
                  Tags = Tags)
  HelpSys.Process(Topics)
  
if __name__ == '__main__':
  GenSTM = False
  OverWrite = False
  OutPutSMSReport = False
  Optimize = False

  print("{0} - {1} ({2})\n".format(PROGRAMNAME, VERSION, RELEASEDATE))
  
  if len(sys.argv) == 1:
    Help(['usagedetails'])
    sys.exit(2)
  else:
    if sys.argv[1] in ('-h', '--help'):
      Help(sys.argv[2:] if len(sys.argv) > 2 else ['usagedetails'])
      sys.exit(2)
    elif sys.argv[1] in ('-e', '--ecodes'):
      Help(['ExitCodes'])
      sys.exit(2)
        
  if len(sys.argv) < 6:
    print('****Error: Required arguments missing****\n')
    Help([])
    sys.exit(ExitCodes.INVALIDARGS)
    
  if len(sys.argv) > 6:
    for i in range(6, len(sys.argv)):
      if sys.argv[i] == 'SMSReport':
        OutPutSMSReport = True
      elif sys.argv[i] == 'Gen':
        GenSTM = True
      elif sys.argv[i] == 'OverWrite':
        OverWrite = True
      elif sys.argv[i] == 'Optimize':
        Optimize = True
      else:
        print('**** Error: Invalid argument {0}****\n'.format(sys.argv[i]))
        Help([])
        sys.exit(ExitCodes.INVALIDARGS)
        
  if not os.path.exists(sys.argv[1]):
    print('Error: SMS File {0} does not exist'.format(sys.argv[1]))
    sys.exit(ExitCodes.FILENOTFOUND)
  if os.path.isdir(sys.argv[1]):
    print('Error: SMS File {0} is a directory'.format(sys.argv[1]))
    sys.exit(ExitCodes.ISDIR)
    
  if not os.path.exists(sys.argv[2]):
    print('Error: TPL DIR {0} does not exist'.format(sys.argv[2]))
    sys.exit(ExitCodes.FILENOTFOUND)
  if not os.path.isdir(sys.argv[2]):
    print('Error: TPL DIR {0} is not a directory'.format(sys.argv[2]))
    sys.exit(ExitCodes.ISNOTDIR)

  if os.path.exists(sys.argv[3]) and not os.path.isdir(sys.argv[3]):
    print('Error: STM DIR {0} is not a directory'.format(sys.argv[3]))
    sys.exit(ExitCodes.ISNOTDIR)
    
  if sys.argv[4] != 'Language':
    print('Error: Required argument Language ({0})'.format(sys.argv[4]))
    sys.exit(ExitCodes.INVALIDARGS)
    
  if sys.argv[5] not in LanguagesSupported:
    print('Error: Language can only be {0}'.format(' or '.join(LanguagesSupported)))
    sys.exit(ExitCodes.INVALIDARGS)
      
  print('\nGen:')
  print('  Using SMS File:         {0}'.format(sys.argv[1]))
  print('  Using TPL Files from:   {0}'.format(sys.argv[2]))
  print('  Storing results STM at: {0}'.format(sys.argv[3]))
  print('  Language:               {0}'.format(sys.argv[5]))
  print('  Generating SMS Report:  {0}'.format('True' if OutPutSMSReport else 'False'))
  print('  Generating STM Files:   {0}'.format('True' if GenSTM else 'False'))
  print('  OverWriting STM Files:  {0}\n'.format('True' if OverWrite else 'False'))
  
  MySmsProcess = CSMSProcess(SMSFileName = sys.argv[1], 
                             OutFile = None,
                             EchoLine = False, 
                             ExeptionOnSyntaxError = True)
  if not MySmsProcess.Process():
    print('Error: Unable to Process SMS file, see above error')
    sys.exit(ExitCodes.SMSERROR)
    
  if OutPutSMSReport:
    SMSReport(SMSResult = MySmsProcess.Result, OutPutVersion = True, OutFile = None)
    
  if GenSTM:
    Generator = CGenerator(Language = sys.argv[5], 
                           TPLDir = sys.argv[2],
                           STMDir = sys.argv[3],  
                           OverWrite = OverWrite,
                           LogFh = sys.stdout,
                           SMSResult = MySmsProcess.Result,
                           Optimize = Optimize)
    Generator.Process()
    RunTimeGen = ConvertMillisecondsDays(Generator.ProcessingTime.Took)
    print('\nProcessing Time: {0}d {1}h {2}m {3}s {4}ms'.format(RunTimeGen.days, RunTimeGen.hours, RunTimeGen.minutes, 
                                                              RunTimeGen.seconds, RunTimeGen.milliseconds))

  sys.exit(ExitCodes.OK)
