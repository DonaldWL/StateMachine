import sys
import os
import shutil
import subprocess
from enum import (IntEnum, unique)

  # Make our default path to our file location.
os.chdir(os.path.dirname(__file__))

  # Make sure our PythonLib and StateMachine are in the path.
  # We assume that PythonLib and StateMachine are at the same 
  # level.  If not you will have to change this.
BasePath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BasePath)

from PythonLib.Base.CodeTimer import (CCaptureTimer, CCodeTimer)


@unique
class ExitCodes(IntEnum):
  OK                = 0
  UNABLETOREMDIR    = 3
  ISNOTADIR         = 4
  UNABLETOCREATEDIR = 5
  ERRORONGENPROGRAM = 6
  INVALIDARGS       = 7

ExampleBaseDir = os.path.abspath(os.path.join(BasePath, 'Results'))
TPLExampleBaseDir = os.path.abspath('./')

Examples = {'ExampleC':              ['Language', 'C', 'SMSReport', 'Gen', 'OverWrite'],
            'ExampleOptimizeC':      ['Language', 'C', 'SMSReport', 'Gen', 'OverWrite', 'Optimize'],
            'ExampleCPP':            ['Language', 'CPP', 'SMSReport', 'Gen', 'OverWrite'],
            'ExampleOptimizeCPP':    ['Language', 'CPP', 'SMSReport', 'Gen', 'OverWrite', 'Optimize'],
            'ExampleCSharp':         ['Language', 'CSharp', 'SMSReport', 'Gen', 'OverWrite'],
            'ExampleOptimizeCSharp': ['Language', 'CSharp', 'SMSReport', 'Gen', 'OverWrite', 'Optimize'],
            'ExampleJava':           ['Language', 'Java', 'SMSReport', 'Gen', 'OverWrite'],
            'ExampleOptimizeJava':   ['Language', 'Java', 'SMSReport', 'Gen', 'OverWrite', 'Optimize'],
            'ExamplePython':         ['Language', 'Python', 'SMSReport', 'Gen', 'OverWrite']}

CaptureTimer = CCaptureTimer()
RunScons = False
RemoveOldDirs = False

if __name__ == '__main__':
  if len(sys.argv) > 3:
    print("Error: Invalid arguments, only RunScons and/or RemoveOldDirs allowed")
    sys.exit(ExitCodes.INVALIDARGS)
    
  for i in range(1, len(sys.argv)):
    if 'RunScons' == sys.argv[i]:
      RunScons = True
    elif 'RemoveOldDirs' == sys.argv[i]:
      RemoveOldDirs = True
    else:
      print("Error: Invalid arguments, only RunScons and/or RemoveOldDirs allowed")
      sys.exit(ExitCodes.INVALIDARGS)
  
    # Remove the example dir
  if RemoveOldDirs:
    if os.path.exists(ExampleBaseDir):
      if os.path.isdir(ExampleBaseDir):
        try:
          shutil.rmtree(ExampleBaseDir)
        except (OSError, IOError) as err:
          print("Error: {0}: {1}".format(ExampleBaseDir, str(err)))
          sys.exit(ExitCodes.UNABLETOREMDIR)
      else:
        print("Error: {0}: Is not a directory".format(ExampleBaseDir))
        sys.exit(ExitCodes.ISNOTADIR)
      
    # Make the example dir
  try:  
    if not os.path.exists(ExampleBaseDir):
      os.mkdir(ExampleBaseDir)
  except (OSError, IOError) as err:
    print("Error: {0}: {1}".format(ExampleBaseDir, str(err)))
    sys.exit(ExitCodes.UNABLETOCREATEDIR)

    # Make all the required directories
  ExampleDir = ''
  ExampleSrcDir = ''
  ProcessDir = ''
  with CCodeTimer("BuildExamples", CaptureTimer):
    for Example in Examples:
      print("Processing {0}".format(Example))
      try:  
        ProcessDir = ExampleDir = os.path.abspath(os.path.join(ExampleBaseDir, Example))
        if not os.path.exists(ProcessDir):
          os.mkdir(ProcessDir)
        ProcessDir = ExampleSrcDir = os.path.join(ExampleDir, 'Src')
        if os.path.exists(ProcessDir):
          try:
            shutil.rmtree(ProcessDir)
          except (OSError, IOError) as err:
            print("Error: {0}: {1}".format(ExampleBaseDir, str(err)))
            sys.exit(ExitCodes.UNABLETOREMDIR)
        os.mkdir(ProcessDir)
      except (OSError, IOError) as err:
        print("Error: {0}: {1}".format(ProcessDir, str(err)))
        sys.exit(ExitCodes.UNABLETOCREATEDIR)
      
      SMSFile = os.path.join(TPLExampleBaseDir, 'Example.sms')
      TPLDir = os.path.abspath(os.path.join(TPLExampleBaseDir, Example, 'TPL'))
      PopenArgs = ['python', '../Gen.py', SMSFile, TPLDir, ExampleSrcDir] + Examples[Example]
      print('+' * 50)
      print("Info: {0}".format(' '.join(PopenArgs)))
      print('+' * 50)
      process = subprocess.Popen(PopenArgs, 
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout, stderr = process.communicate()
      lines = stdout.decode("utf-8")
      if lines:
        for line in lines.split('\n'):
          print(line, end='')
      if lines:
        for line in lines.split('\n'):
          print(line, end='')
      if (process.returncode):
        lines = stderr.decode("utf-8")
        print("Error: Unable to process example {0}: RCode: {1}".format(Example, process.returncode))
        sys.exit(ExitCodes.ERRORONGENPROGRAM)
        
      SConstructFile = os.path.join(ExampleSrcDir, 'SConstruct')
      if os.path.exists(SConstructFile):
        if Example in ('ExampleCSharp', 'ExampleOptimizeCSharp'):
          CSharpDir = os.path.join(ExampleDir, 'csharp')
          if os.path.exists(CSharpDir):
            shutil.rmtree(CSharpDir)
          os.mkdir(CSharpDir)
          shutil.copytree(os.path.join(TPLDir, 'csharp'), CSharpDir, dirs_exist_ok=True)
          
        if (os.path.exists(os.path.join(ExampleDir, 'SConstruct'))):
          os.remove(os.path.join(ExampleDir, 'SConstruct'))
        shutil.move(SConstructFile, ExampleDir)
        if RunScons:
          os.chdir(ExampleDir)
          process = subprocess.Popen(['scons'], 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          stdout, stderr = process.communicate()
          lines = stdout.decode("utf-8")
          if lines:
            for line in lines.split('\n'):
              print(line, end='')
          if lines:
            for line in lines.split('\n'):
              print(line, end='')
          if (process.returncode):
            lines = stderr.decode("utf-8")
            print("Error: Unable to process example scons issue {0}: RCode: {1}".format(Example, process.returncode))
            sys.exit(ExitCodes.ERRORONGENPROGRAM)
          os.chdir(os.path.dirname(__file__))

  print('\n' + '+' * 50)
  print("Total Build took: {0}ms".format(CaptureTimer.Took))
  print('+' * 50)
  sys.exit(ExitCodes.OK)
