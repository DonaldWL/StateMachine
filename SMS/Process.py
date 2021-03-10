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

  This is the main entry for the SMS package.  The class in the module is
  use to process an SMS file.  You create an instance of the class and
  then tell it process the SMS files by using the method Process.
-----------------------------------------------------------------------------
Update History:
  Feb 22, 2022 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''
from collections import namedtuple
import os
import sys

from PythonLib.Base.CodeTimer import CCodeTimer
from PythonLib.Base.StringHandlers import (GetString, SkipWhiteSpace)

from StateMachine.SMS.Definitions import (StateRecDef, StateTransRecDef, CodeBlockDef, 
                                          SingleCmdDef, MultiParamCmdDef, 
                                          SMSFILEVERSIONMAJOR, LanguagesSupported)
from StateMachine.SMS.Exceptions import (SMSSyntaxError, SMSFileVersionError)
from StateMachine.SMS.Results import CSMSResults
from StateMachine.SMS._BuildResults import BuildResutls

  # Definition of each entry in the internal table self._ExecCmd in
  # Libs.StateMachine.SMS.Process.CSMSProcess.  This table is used to define all the
  # commands and how to process them.  The table is a dictionary, the
  # key is the command and the item is _ExecRecDef.
  #
  #   namedtuple('ExecRec', ['Method', 'Variable'])
  #     Method
  #       Is the method to execute for the command.  This is not
  #       a string, it is the method without calling.  Example
  #       of this is self._SetCmdWithParam.
  #     Variable
  #       This is a string that is the variable to use to store
  #       the commands results into.  Not all commands use this.
  #       The reason for this is to allow sharing of code with
  #       commands that have the same structure.
  #
  # Example of an entry:
  #   '@Author': _ExecRecDef(self._SetCmdWithParam, 'Author')
  #
  #     The above creates an entry for the command @Author.  This
  #     command will use self._SetCmdWithParam to process the command
  #     and use the variable self._Results.Author
_ExecRecDef = namedtuple('ExecRec', ['Method', 'Variable'])

  #  When a line is processed and it contains a command this record is produced
  #  for other parts of the processing to use.  The method CSMSProcess._GetCmd
  #  returns this.
  #
  #    namedtuple('CmdRec', ['OutCome', 'Cmd', 'CmdOffset', 'Params',
  #                          'LineNo', 'Line', 'LineLen'])
  #      OutCome
  #        If no command found then False else True.
  #      Cmd
  #        Is the command found, i.e., @Author....
  #      CmdOffset
  #        Is the offset in Line that the command was found
  #      Params
  #        Is a list _ParamRecDef.  Each param for the command has an entry.
  #      Line
  #        Is the line that was processed
  #      LineLen
  #        Is the length of the line that was processed
_CmdRecDef = namedtuple('CmdRec', ['OutCome', 'Cmd', 'CmdOffset', 'Params',
                                   'LineNo', 'Line', 'LineLen'])

  # Each param for a command has this layout, see _CmdRecDef.Params for the list
  # of these items.
  #
  #   namedtuple('ParamRec', ['Offset', 'Param'])
  #     Offset
  #       Is the offet in _CmdRecDef.Line that the param was found
  #     Param
  #       Is the param
_ParamRecDef = namedtuple('ParamRec', ['Offset', 'Param'])

  # Is the allowed names for Code Blocks
_CodeBlockTypes = ('Code', 'Method')

  # The white space to use that will separate the words in the line
  # that is being processed.
_WHITESPACE = (' ', '\t')

  #--------------------------------------------------------------------------
class CSMSProcess(object):
  '''
  Used to process and SMS file.  This is the main entry for the SMS package.

  CSMSProcess(SMSFileName, OutFile = None, EchoLine = True, 
              ExeptionOnSyntaxError = False)
    SMSFileName
      Is the name of the SMS file.  Must be a file.
    OutFile = None
      Out file, used to echo the SMS file and write out syntax errors.  If not passed
      in or None will be sys.stdout
    EchoLine = True
      Echo the SMS lines to the OutFile
    ExeptionOnSyntaxError = False
      If True then on syntax error raise an exception.  Normally you do not need to
      do this.  You normally wont to just display the syntax error in text.  Like a
      normal compiler.

  Exceptions
    AttributeError
      One of the attributes is not valid
    SMSSyntaxError
      A syntax error has occurred in relation to the SMS file.  This
      exception can be imported at Libs.StateMachine.SMS.Exceptions and only
      occurs if you set ExeptionOnSyntaxError to True.  This is manly for
      debugging.
    SMSFileVersionError
      If the SMS file version not supported this will be raised.  This
      exception can be imported at Libs.StateMachine.SMS.Exceptions
  '''
  def __init__(self, SMSFileName, OutFile = None, EchoLine = True, 
               ExeptionOnSyntaxError = False):
    if SMSFileName is None or not isinstance(SMSFileName, str):
      raise AttributeError("SMSFileName must be a string")
    self._SMSFileName = SMSFileName.strip()
    if not self._SMSFileName:
      raise AttributeError("SMSFileName must contain a filename and not be empty")
    if not os.path.exists(self._SMSFileName):
      raise AttributeError("SMSFileName '{0}' does not exist".format(self._SMSFileName))
    if os.path.isdir(self._SMSFileName):
      raise AttributeError("SMSFileName is a directory and must be a file '{0}'".format(self._SMSFileName))
    if not os.path.isfile(self._SMSFileName):
      raise AttributeError("SMSFileName is a special file (socket, FIFO, device file) and must be a file '{0}'".format(self._SMSFileName))
    if os.path.splitext(self._SMSFileName)[1] != ".sms":
      raise AttributeError("SMSFileName file '{0}' must be of type sms".format(self._SMSFileName))

    self._OutFile = OutFile
    if OutFile is None:
      self._OutFile = sys.stdout
    if not hasattr(self._OutFile, 'write'):
      raise AttributeError("OutFile does not have an attribute of write")

    if not isinstance(EchoLine, bool):
      raise AttributeError("EchoLine must be a bool (True, False)")
    self.EchoLine = EchoLine

    if not isinstance(ExeptionOnSyntaxError, bool):
      raise AttributeError("ExeptionOnSyntaxError must be a bool (True, False)")
    self._ExeptionOnSyntaxError = ExeptionOnSyntaxError

    self._ProcessingStates = False
    self._SyntaxErrorOccurred = False

      # All tables and values captured are stored in this class
    self._Result = CSMSResults()

      # For details see _ExecRecDef in this file
    self._ExecCmd = {'@Author': _ExecRecDef(self._SetCmdWithParam, 'Author'),
                     '@Date': _ExecRecDef(self._SetCmdWithParam, 'Date'),
                     '@StateMachineName': _ExecRecDef(self._SetCmdWithParam, 'StateMachineName'),
                     '@Version': _ExecRecDef(self._SetCmdWithParam, 'Version'),
                     '@SMSFileVersion': _ExecRecDef(self._SetSMSFileVersion, 'SMSFileVersion'),
                     '@CodeBlockType': _ExecRecDef(self._CodeBlockTypeCmd, 'CodeBlockType'),
                     '@CodeBlocks': _ExecRecDef(self._CodeBlocksCmd, 'CodeBlocks'),
                     '@CodeBlock': _ExecRecDef(self._CodeBlockCmd, 'CodeBlocks'),
                     '@Language': _ExecRecDef(self._LanguageCmd, 'Language'),
                     '@BeginStates': _ExecRecDef(self._BeginStatesCmd, 'States'),
                     '@EndStates': _ExecRecDef(self._EndStatesCmd, 'States'),
                     '@State': _ExecRecDef(self._StateCmd, 'States')}

    #--------------------------------------------------------------------------
  def Process(self):
    '''
    This will process the SMS file.  If it fails it will return False
    else True.  If success then Libs.StateMachine.SMS.Results.CSMSResults can be used to process
    the results.

    A False is syntax error.  But if ExeptionOnSyntaxError is set to True when you create your
    instance then an exception will be raised.
    '''
    self._ProcessingStates = False
    self._SyntaxErrorOccurred = False

      # All tables and values captured are stored in this class
    self._Result = CSMSResults()

    _CmdRecord = None
    _Line = None
    _LineCnt = 0

    with CCodeTimer("SMS Processing", self._Result.CaptureTimer):
      with open(self._SMSFileName, 'r') as SmsFile:
        for _Line in SmsFile:
          _LineCnt += 1
          _Line = _Line.rstrip()

          if self.EchoLine:
            self._OutFile.write("{0:05d}  {1}\n".format(_LineCnt, _Line))

            # Handle line comment
          lineLen = len(_Line)
          strtLoc = SkipWhiteSpace(_Line)
          if (strtLoc < lineLen and _Line[strtLoc] == '#'):
            continue

            # Handle normal lines
          cmdRecord = self._GetCmd(_Line, _LineCnt)
          if cmdRecord.OutCome:  # Found a command
            self._ExecCmd[cmdRecord.Cmd].Method(cmdRecord, _CmdRecord)
            _CmdRecord = cmdRecord
          elif self._ProcessingStates:
            if _Line:
              self._StateCmdTransition(strtLoc, _Line, lineLen, _LineCnt, _CmdRecord)
          else:
            if _Line:
              if not self._ProcessingSyntaxError:
                self._SyntaxError('Line contains no command', strtLoc, self.EchoLine, _Line, _LineCnt)

          if self._SyntaxErrorOccurred:
            break

      # Validate the state machine
    if not self._SyntaxErrorOccurred:
      self._Validate(_Line, _LineCnt)

    return not self._SyntaxErrorOccurred

    #--------------------------------------------------------------------------
  def _SetCmdWithParam(self, CmdRecord, PrevCmdRecord, MaxParams = 1):
    '''
    Handles commands that have a param but are on one line only.  If MaxParams
    is equal to 1 then SingleCmdDef is used else MultiParamCmdDef is used.  No
    checking is done to make sure MaxParams is greater than zero, this would make
    no sense to pass a 0 or negative number to this method.  By default MaxParams
    is 1.
    '''
    if self._ProcessingStates:
      self._SyntaxError('Command not allowed in {0}'.format(PrevCmdRecord.Cmd),
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif getattr(self._Result, self._ExecCmd[CmdRecord.Cmd].Variable).LineNo != 0:
      LineNo = getattr(self._Result, self._ExecCmd[CmdRecord.Cmd].Variable).LineNo
      self._SyntaxError('Command Already found at {0}'.format(LineNo),
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif not CmdRecord.Params:
      self._SyntaxError('Missing required parameter, non given',
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif MaxParams != -1 and len(CmdRecord.Params) > MaxParams:
      self._SyntaxError('To many params only one is required',
                        CmdRecord.Params[1].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    else:
      if MaxParams == 1:
        setattr(self._Result, self._ExecCmd[CmdRecord.Cmd].Variable,
                SingleCmdDef(CmdRecord.LineNo, CmdRecord.Params[0].Param))
      else:
        setattr(self._Result, self._ExecCmd[CmdRecord.Cmd].Variable,
                MultiParamCmdDef(CmdRecord.LineNo, []))
        for Param in CmdRecord.Params:
          getattr(self._Result, self._ExecCmd[CmdRecord.Cmd].Variable).Params.append(Param)
      return True

    return False

    #--------------------------------------------------------------------------
  def _SetSMSFileVersion(self, CmdRecord, PrevCmdRecord):
    '''
    Handles the @SMSFileVersion command
    '''
    if self._SetCmdWithParam(CmdRecord, PrevCmdRecord):
      VerData = getattr(self._Result, self._ExecCmd[CmdRecord.Cmd].Variable).Value.split('.')
      if CmdRecord.LineNo != 1:
        self._SyntaxError('@SMSFileVersion must be the first line in the file',
                          CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
      if len(VerData) != 2:
        self._SyntaxError('Invalid version format should be major.minor, both are numeric values',
                          CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
      elif not VerData[0].isnumeric() or not VerData[1].isnumeric():
        self._SyntaxError('Invalid version format should be major.minor, both are numeric values',
                          CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
      elif VerData[0] != SMSFILEVERSIONMAJOR:
        try:
          self._SyntaxError('SMS File Version {0} not supported, requires {1}'.format(VerData[0], SMSFILEVERSIONMAJOR),
                            CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
        except SMSSyntaxError:
          raise SMSFileVersionError() from SMSSyntaxError
      else:
        return True

    return False

    #--------------------------------------------------------------------------
  def _LanguageCmd(self, CmdRecord, PrevCmdRecord):
    '''
    Handles the @Language command
    '''
    if self._SetCmdWithParam(CmdRecord, PrevCmdRecord, -1):
      for Param in self._Result.Language.Params:
        if not Param.Param in LanguagesSupported:
          self._SyntaxError('Invalid param {0} must be one of ({1})'.format(Param.Param, ', '.join(LanguagesSupported)),
                            CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
          return False
        
      if CmdRecord.LineNo != 2:
        self._SyntaxError('@Language must be the second line in the file',
                          CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
        return False
      
    return True

    #--------------------------------------------------------------------------
  def _CodeBlockTypeCmd(self, CmdRecord, PrevCmdRecord):
    '''
    Handles the @CodeBlockType command
    '''
    if self._SetCmdWithParam(CmdRecord, PrevCmdRecord):
      if not self._Result.CodeBlockType.Value in _CodeBlockTypes:
        self._SyntaxError('Invalid param must be one of {0}'.format(_CodeBlockTypes),
                          CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
      else:
        return True

    return False

    #--------------------------------------------------------------------------
  def _CodeBlocksCmd(self, CmdRecord, PrevCmdRecord):
    if not CmdRecord.Params:
      self._SyntaxError('No code block names, must at least have one',
                        CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
      return False
    
    TempCmdRecord = _CmdRecDef(CmdRecord.OutCome, CmdRecord.Cmd, 
                               CmdRecord.CmdOffset, [], CmdRecord.LineNo, 
                               CmdRecord.Line, CmdRecord.LineLen)
    for Param in CmdRecord.Params:
      TempCmdRecord.Params.clear()
      TempCmdRecord.Params.append(Param)
      self._CodeBlockCmd(TempCmdRecord, PrevCmdRecord)
      TempCmdRecord.Params.clear()
      
    return True
  
  def _CodeBlockCmd(self, CmdRecord, PrevCmdRecord):  #pylint: disable=unused-argument
    '''
    Handles the @CodeBlock command
    '''
    if (not CmdRecord.Params):
      self._SyntaxError('Missing required parameter, non given, need at lest the name of the code block.',
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif (len(CmdRecord.Params) > 2):
      self._SyntaxError('To many params only two are allowed and one is required, <codeblockname> [<codetype>]',
                        CmdRecord.Params[1].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif len(CmdRecord.Params) == 2 and CmdRecord.Params[1].Param not in _CodeBlockTypes:
      self._SyntaxError('Invalid param code block type must be {0}'.format(' or '.join(_CodeBlockTypes)),
                        CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif CmdRecord.Params[0].Param in self._Result.CodeBlocks.keys():
      self._SyntaxError('CodeBlock already defined at {0}'.format(self._Result.CodeBlocks[CmdRecord.Params[0].Param].LineNo),
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    else:
      CodeType = None
      if len(CmdRecord.Params) == 2:
        CodeType = CmdRecord.Params[1].Param      
      self._Result.CodeBlocks[CmdRecord.Params[0].Param] = CodeBlockDef(CmdRecord.LineNo, CodeType)
      return True
    
    return False

    #--------------------------------------------------------------------------
  def _BeginStatesCmd(self, CmdRecord, PrevCmdRecord):
    '''
    Handles the @BeginStates command
    '''
    if self._ProcessingStates:
      self._SyntaxError('Command not allowed in {0}'.format(PrevCmdRecord.Cmd),
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif self._Result.States.BLineNo != 0:
      self._SyntaxError('Command Already found at {0}'.format(self._Result.States.BLineNo),
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif not CmdRecord.Params:
      self._SyntaxError('Must at least enter the start state, end state is optional',
                        CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif len(CmdRecord.Params) > 2:
      self._SyntaxError('Only two parameters allows <startstate> and <endstate>',
                        CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    else:
      if len(CmdRecord.Params) == 1:
        self._Result.States = self._Result.States._replace(StartState = CmdRecord.Params[0],
                                                           BLineNo = CmdRecord.LineNo)
      else:
        self._Result.States = self._Result.States._replace(StartState = CmdRecord.Params[0],
                                                           EndState = CmdRecord.Params[1],
                                                           BLineNo = CmdRecord.LineNo)
      self._ProcessingStates = True
      return True

    return False

    #--------------------------------------------------------------------------
  def _EndStatesCmd(self, CmdRecord, PrevCmdRecord):
    '''
    Handles the @EndStates command
    '''
    if CmdRecord.Params:
      self._SyntaxError('No params are allowed',
                        CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif not self._ProcessingStates:
      self._SyntaxError('Found @EndStates without @BeginStates',
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif PrevCmdRecord.Cmd == '@State' and not self._Result.States.StateList[PrevCmdRecord.Params[0].Param].Transitions:
      msg = 'No State Transitions found for state {0} at line {1}'
      self._SyntaxError(msg.format(PrevCmdRecord.Params[0], self._Result.States.StateList[PrevCmdRecord.Params[0].Param].LineNo),
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    else:
      self._Result.States = self._Result.States._replace(ELineNo = CmdRecord.LineNo)
      self._ProcessingStates = False
      return True

    return False

    #--------------------------------------------------------------------------
  def _StateCmd(self, CmdRecord, PrevCmdRecord):
    '''
    Handles the @State command
    '''
    if not CmdRecord.Params:
      self._SyntaxError('Missing required parameter, non given (state codeblock)',
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif not CmdRecord.Params:
      self._SyntaxError('Missing required parameter codeblock)',
                        CmdRecord.Params[0].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif len(CmdRecord.Params) > 2:
      self._SyntaxError('To many params only two is required (state codeblock)',
                        CmdRecord.Params[2].Offset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif PrevCmdRecord.Cmd == '@State' and not self._Result.States.StateList[PrevCmdRecord.Params[0].Param].Transitions:
      msg = 'No State Transitions found for state {0} at line {1}'
      LineNo = self._Result.States.StateList[PrevCmdRecord.Params[0].Param].LineNo
      self._SyntaxError(msg.format(PrevCmdRecord.Params[0], LineNo),
                          CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    elif CmdRecord.Params[0].Param in self._Result.States.StateList.keys():
      LineNo = self._Result.States.StateList[CmdRecord.Params[0].Param].LineNo
      self._SyntaxError('State already defined at {0}'.format(LineNo),
                        CmdRecord.CmdOffset, self.EchoLine, CmdRecord.Line, CmdRecord.LineNo)
    else:
      self._Result.States.StateList[CmdRecord.Params[0].Param] = StateRecDef(CmdRecord.LineNo, CmdRecord.Params[1].Param, {})
      return True

    return False

    #--------------------------------------------------------------------------
  def _StateCmdTransition(self, StrtLoc, Line, LineLen, LineNo, CmdRecord):
    '''
    Handles state transition lines
    '''
    Params = []

    Offset = StrtLoc
    while Offset < LineLen:
      Offset += SkipWhiteSpace(Line[Offset:])
      paramOffset = Offset
      if Offset < LineLen:
        while Offset < LineLen:  # Get the param
          if Line[Offset] in _WHITESPACE:  # Found start of params
            break
          Offset += 1
        Params.append(_ParamRecDef(paramOffset, Line[paramOffset:Offset]))

      # Handle comment on line
    if len(Params) > 3:
      if Params[3].Param[0] == '#':
        Params = Params[0:3]

    if len(Params) != 3:
      self._SyntaxError('Invalid syntax for state transitions <StateRValue> => <State>',
                        StrtLoc, self.EchoLine, Line, LineNo)
    elif Params[0].Param != 'OtherWise' and (not Params[0].Param.isnumeric() or int(Params[0].Param) < 0):
      self._SyntaxError('<StateRValue must be a numeric and greater than -1',
                        Params[0].Offset, self.EchoLine, Line, LineNo)
    elif Params[1].Param != '->' and Params[1].Param != '=>':
      self._SyntaxError('Invalid syntax for state transitions <StateRValue> => <State>',
                        Params[1].Offset, self.EchoLine, Line, LineNo)
    else:
      if Params[0].Param in self._Result.States.StateList[CmdRecord.Params[0].Param].Transitions.keys():
        self._SyntaxError('StateRValue already defined for this state',
                          Params[0].Offset, self.EchoLine, Line, LineNo)
        return False

      self._Result.States.StateList[CmdRecord.Params[0].Param].Transitions[Params[0].Param] = StateTransRecDef(LineNo, Params[2].Param)
      return True

    return False

    #--------------------------------------------------------------------------
  def _Validate(self, Line, LineCnt):
    '''
    Validate the state machine
    '''
    if self._ProcessingStates:
      self._SyntaxError('No @EndStates encountered', 0, self.EchoLine, Line, LineCnt)
    elif self._Result.SMSFileVersion is None:
      self._SyntaxError('@SMSFileVersion is required, must be the first Line', 0, self.EchoLine, Line, LineCnt)
    elif not self._Result.CodeBlocks:
      self._SyntaxError('No code blocks defined', 0, self.EchoLine, Line, LineCnt)
    elif not self._Result.States:
      self._SyntaxError('No states defined', 0, self.EchoLine, Line, LineCnt)
    elif not self._Result.Language.Params:
      self._SyntaxError('Must set the language that you are using for the state machine', 0, self.EchoLine, Line, LineCnt)
    else:
      (UndefStates, UndefCodeBlock) = BuildResutls(self._Result, LineCnt)

      if '@EndState' in UndefStates.keys():
        if self._Result.States.EndState is None:
          self._SyntaxError('State Transitions contain @EndState but no Code Block defined as an End state',
                            0, self.EchoLine, Line, LineCnt)
        del UndefStates['@EndState']
      if '@StartState' in UndefStates.keys():
        del UndefStates['@StartState']

        # Dump all the states that do not exist
      msg = 'Undefined states|codeblocks\n'
      UndefStateNames = list(UndefStates.keys())
      UndefCodeBlockNames = list(UndefCodeBlock.keys())
      if UndefStateNames or UndefCodeBlockNames:
        if UndefStateNames:
          UndefStateNames.sort()
          msg += '           States:\n'
          for undefStateName in UndefStateNames:
            msg += '             {0}\n'.format(undefStateName)
            stateNames = UndefStates[undefStateName]
            stateNames.sort()
            for stateName in stateNames:
              msg += ('               {0:05d} {1}\n'.format(self._Result.States.StateList[stateName].LineNo,
                                                            stateName))

        if UndefCodeBlockNames:
          UndefCodeBlockNames.sort()
          msg += '           CodeBlocs:\n'
          for UndefCodeBlockName in UndefCodeBlockNames:
            msg += '             {0}\n'.format(UndefCodeBlockName)
            stateNames = UndefCodeBlock[UndefCodeBlockName]
            stateNames.sort()
            for stateName in stateNames:
              msg += ('               {0:05d} {1}\n'.format(self._Result.States.StateList[stateName].LineNo,
                                                            stateName))

        self._SyntaxError(msg, 0, self.EchoLine, Line, LineCnt)

    #--------------------------------------------------------------------------
  def _GetCmd(self, Line, LineNo):
    '''
    Processes a line looking for a cmd and its params.  If
    a valid command is fount OutCome in _CmdRecDef will be
    True else False.  _CmdRecDef is returned.
    '''
    _Cmd = None
    _CmdOffset = None
    _Params = []

    _LineLen = len(Line)
    _LineStrt = SkipWhiteSpace(Line)
    if Line and Line[_LineStrt] == '@':  # Got a cmd to process.
      _Cmd = Line[_LineStrt]
      _CmdOffset = _LineStrt
      offset = 0
      for offset in range(_LineStrt + 1, _LineLen):
        if Line[offset] in _WHITESPACE:  # End of Cmd
          break
        _Cmd += Line[offset]
      offset += 1

      while offset < _LineLen:
        offset = offset + SkipWhiteSpace(Line[offset:])

        if Line[offset] == '#':
          break
        if Line[offset] == '"':
          RString = GetString(Line[offset:])
          if not RString.OutCome:
            self._SyntaxError('String not terminated', offset, self.EchoLine, Line, LineNo)

          _Params.append(_ParamRecDef(offset, RString.String))
          offset += RString.CharConsumed
        else:
          paramOffset = offset
          if offset < _LineLen:
            while offset < _LineLen:  # Get the param
              if Line[offset] in _WHITESPACE:  # Found start of params
                break
              offset += 1
            _Params.append(_ParamRecDef(paramOffset, Line[paramOffset:offset]))

    return _CmdRecDef(bool(_Cmd), _Cmd, _CmdOffset, _Params, LineNo, Line, _LineLen)

    #--------------------------------------------------------------------------
  def _SyntaxError(self, Msg, ErrorOffset, EchoLine, Line, LineNo):
    '''
    Called when you have a syntax error.  If self._ExeptionOnSyntaxError
    is True then raised SMSSyntaxError.  Outputs the passed in message.
    If EchoLine is False, that means the caller is not echoing the SMS
    file to self._OutFile, so the passed in Line will be echoed before
    the write of the syntax issue.
    '''
    if not EchoLine:
      self._OutFile.write("{0:05d}  {1}\n".format(LineNo, Line))

    self._OutFile.write('{0}^ '.format(' ' * (ErrorOffset + 7)))
    self._OutFile.write(Msg + "\n")

    self._SyntaxErrorOccurred = True

    if self._ExeptionOnSyntaxError:
      raise SMSSyntaxError(self._SMSFileName, LineNo, ErrorOffset)

    #--------------------------------------------------------------------------
  @property
  def Result(self):
    '''
    Returns the Libs.StateMachine.SMS.Result.CSMSResults instance.
    '''
    return self._Result
