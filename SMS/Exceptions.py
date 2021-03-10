'''
Created:   Feb 22, 2021
Author:    Donald W. Long (Donald.W.Long@gmail.com)
-----------------------------------------------------------------------------
Description:

  All the custom exceptions for the SMS Package
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

  Module contains all the custom exceptions for SMS.
-----------------------------------------------------------------------------
Update History:
  Feb 22, 2021 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''

  #--------------------------------------------------------------------------
class SMSSyntaxError(Exception):
  '''
  If a syntax error occurred while processing the SMS file.  This will
  be raised, assuming that when you created the CSMSProcess you set the
  argument ExeptionOnSyntaxError to True.  Otherwise this exception
  should never be raised.  It is manly used for debugging.  Normally
  you do not configure SMS to raise this exception.
  '''
  def __init__(self, SmsFileName, LineNo, Column):
    msg = 'Syntax Error in SmsFile {0} at line {1} column {2}'
    Exception.__init__(self, msg.format(SmsFileName, LineNo, Column))

  #--------------------------------------------------------------------------
class SMSFileVersionError(Exception):
  '''
  If the SMS file is not a version that is supported by the SMS package
  that you are using then this will be raised.
  '''
  def __init__(self):
    Exception.__init__(self, 'StateMachineGenerator: SMS File version not supported')
