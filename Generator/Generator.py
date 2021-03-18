'''
Created:   Feb 11, 2021
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

  This is the main module for the Generator package.  Is requires the 
  results from the SMS package.  You have to give it your location of
  TPL files and a location to place the results from the TPL files.  The
  result dir is called STM.
  
  The files that process each language are:
  
    Languages.CPP
      Processes C, CPP and CSharp (C#).  The reason for this is most
      of the code is the same for all of them.  Just a few if statements
      and it supports all three.
    Languages.Python
      Process Python
  
  See the Gen.py program for an example on how to use this class.
-----------------------------------------------------------------------------
Update History:
  Author: Donald W. Long (Donald.W.Long@gmail.com)
  Date:   Feb 11, 2021
    Released
-----------------------------------------------------------------------------
'''
import os
import sys

from PythonLib.Base.CodeTimer import CCaptureTimer
from PythonLib.Base.CodeTimer import CCodeTimer
from StateMachine.SMS.Definitions import LanguagesSupported
from StateMachine.Generator.Languages.Python import _CPython
from StateMachine.Generator.Languages.CPP import _CCPP

  #--------------------------------------------------------------------------
class CGenerator(object):
  '''
  Main class for the Generator.  Create an instance and then call 'Process'.
  
  CGenerator(Language, TPLDir, STMDir, OverWrite, LogFh, SMSResult)
  
    Language
      Is a string containing the language you are processing.  See 
      SMS.Definitions.LanguagesSupported for a list of the langauges
      that SMS and Generator support.
    TPLDir
      Is the directory that contains all the TPL files.
    STMDir
      Is a directory that the results of the run from the TPL files 
      will be placed.
    OverWrite
      If True, then overwrite any file that already exists in the
      STM directory.
    LogFh
      Instance of any class that has a 'write' method.  The method
      should not append an EOL.
    SMSResult
      Is the result from SMS package.
      
  Exceptions:
    AttributeError
      One of the attributes is invalid.
    GenException
      The exception of the Generator package.  Something went wrong.
      Any exception besides AttributeError will be this exception.
  '''
  def __init__(self, Language, TPLDir, STMDir, OverWrite, LogFh, SMSResult):
    self._Language = Language
    self._TPLDir = TPLDir
    self._STMDir = STMDir
    self._OverWrite = OverWrite
    self._LogFh = LogFh
    self._SMSResult = SMSResult
    self._CaptureTimer = CCaptureTimer()
    
    if self._LogFh is None:
      self._LogFh = sys.stdout
    if not hasattr(self._LogFh, 'write'):
      raise AttributeError('LogFh must have a method (write)')
      
    if not isinstance(OverWrite, bool):
      raise AttributeError("OverWrite must be a bool")
    
    if TPLDir is None:
      raise AttributeError('TPLDir can not be None')
    
    self._TPLDir = os.path.abspath(os.path.expanduser(os.path.expandvars(TPLDir)))
    if not os.path.exists(self._TPLDir):
      raise AttributeError('TPLDir ({0}) does not exist'.format(self._TPLDir))
    if not os.path.isdir(self._TPLDir):
      raise AttributeError('TPLDir ({0}) is not a directory'.format(self._TPLDir))
    
    self._STMDir = os.path.abspath(os.path.expanduser(os.path.expandvars(STMDir)))
    if not os.path.exists(self._STMDir):
      try:
        os.mkdir(self._STMDir)
      except (OSError, IOError) as err:
        raise AttributeError('Unable to create STMDir ({0}) - {1}'.format(self._STMDir, str(err))) from err
    elif not os.path.isdir(self._STMDir):
      raise AttributeError('STMDir ({0}) is not a directory'.format(self._STMDir))
    
    if not isinstance(Language, str):
      raise AttributeError('Language must be a string')
    
    if not Language in LanguagesSupported:
      raise AttributeError('Language {0} is not supported ({1})'.format(Language, ','.join(LanguagesSupported)))
    
    #--------------------------------------------------------------------------
  def Process(self):
    '''
    Process the TPL files and create the STM files.
    
      Process()
    '''
    ClassToProcess = None
    if self._Language == 'Python':
      ClassToProcess = _CPython
    else:   # 'CPP', 'C', 'CSharp', 'Java'
      ClassToProcess = _CCPP

    with CCodeTimer('TPL/STM', self._CaptureTimer):
      ClassToProcess(Language = self._Language, 
                     TPLDir = self._TPLDir, 
                     STMDir = self._STMDir,
                     OverWrite = self._OverWrite,
                     LogFh = sys.stdout,
                     SMSResult = self._SMSResult).Process()

    #--------------------------------------------------------------------------
  @property
  def ProcessingTime(self):
    '''
    A CCodeTimer is created and used before calling processing the TPL files.
    It is used to capture how long it took to do the TPL=>STM conversion.  This
    is a property that will return an instance of PythonLib.Base.CodeTimer.CCaptureTimer.
    
    See PythonLib.Base.Converters if you wish to break up the milliseconds into
    days, hours.....
    '''
    return self._CaptureTimer
  