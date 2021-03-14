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

  Contains many global variables that are used thru out the program.

    SMSVERSIONMAJOR
      Major version of the SMS package

    SMSVERSIONMINOR
      Minor version of the SMS package

    SMSVERSION = "{0}.{1}".format(SMSVERSIONMAJOR, SMSVERSIONMINOR)
      Version string of the SMS package. Format is <major>.<minor>

    SMSFILEVERSIONMAJOR
      Major version of the SMS file that is supported.  These must
      match the SMS processor

    SMSFILEVERSIONMINOR
      Minor version of the SMS file that is supported.  This does not
      matter, this can change and the file can still be processed.

    SMSFILEVERSION = "{0}.{1}".format(SMSFILEVERSIONMAJOR, SMSFILEVERSIONMINOR)
      Version string for SMS file.  Format is <major>.<minor>

    StateTableDef
      Defines the CResult.Stats table.  The states table is set to this
      namedtuple.

        namedtuple('StateTable', ['StartState', 'EndState', 'BLineNo', 'ELineNo', 'StateList'])
          StartState
            Is the state that we will start the state machine at
          EndState
            Is the state that will end the state machine.  Returns from the 'Run'
            method.  May be None, an end state is not required.
          BLineNo
            Is the line number that @BeginStates was encountered on.
          ELineNo
            Is the line number that @EndStates was encountered on.
          StateList
            Is a dictionary of StateRecDef.  The key is the StateRValue.

        BNF of table:
          <StateTable>  ::= {StartState, EndState, BLineNo, ELineNo, StateList}
          <StateList>   ::= {<State>, <State>, ...}
          <State>       ::= {LineNo, CodeBlock, <Transitions>}
          <Transitions> ::= {<Transition>, <Transitions>, ...}
          <Transition>  ::= {LineNo, StateRValue, State}

    StateRecDef
      Defines each record in the StateList from StateTableDef.  Each state that
      is processed will have an entry in this list with this format.

        namedtuple('StateRec', ['LineNo', 'CodeBlock', 'Transitions'])
          LineNo
            Is the line number that the state was found at
          CodeBlock
            Is the name of the code block assigned to this state
          Transitions
            Is a list of all the transitions for the state, see StateTransRecDef.

    StateTransRecDef
      Defines each transition for a state.  It is stored in Transitions from
      StateRecDef.  This is a dictionary with the key being StateRValue.

        namedtuple('StateTransRec', ['LineNo', 'State'])
          LineNo
            Is the line number that the transition occurred at in the SMS file
          State
            Is the name of the state to transition to.  This can be @End.  This
            means end the state machine.

    CodeBlockDef
      Each code block in Libs.StateMachine.SMS.Result.CSMSResults.CodeBlocks uses
      as the item of the dictionary.  The dictionary key is the CodeBlock name.

        namedtuple('CodeBLock', ['LineNo', 'Type'])
          LineNo
            Line number that the Code block command was processed
          Type
            Type of code block, either 'Code' or 'Method'.  What
            types are supported will change based on the language
            that is being generated.

    SingleCmdDef
      Many commands use this to store the data of the command in.  The
      commands that use this are the ones that are single line with
      one parameter.

        namedtuple('SingleCmd', ['LineNo', 'Value'])
          LineNo
            Line number that the command occurred at in the SMS file
          Value
            Is the value that was retrieved from the command.  An example
            of a command would be @Author <yourname>.  <yourname> would
            be the Value.
            
    MultiParamCmdDef
      For commands that support nth number of params.
        
        namedtuple('MultiParamCmd', ['LineNo', 'Params'])
          LineNo
            Line number that the command occurred at in the SMS file
          Params
            A list of parameters
        
    LanguagesSupported
      Are the current languages that are supported.  This is a tuple of
      names.
-----------------------------------------------------------------------------
Update History:
  Feb 22, 2022 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''

from collections import namedtuple

  # SMS Version information.
SMSVERSIONMAJOR = "1"
SMSVERSIONMINOR = "0"
SMSVERSION = "{0}.{1}".format(SMSVERSIONMAJOR, SMSVERSIONMINOR)

  # SMS File Version information
SMSFILEVERSIONMAJOR = "1"
SMSFILEVERSIONMINOR = "0"
SMSFILEVERSION = "{0}.{1}".format(SMSFILEVERSIONMAJOR, SMSFILEVERSIONMINOR)

  # Used for the state table.  See module documentation for details
StateTableDef = namedtuple('StateTable', ['StartState', 'EndState', 'BLineNo', 'ELineNo', 'StateList'])
StateRecDef = namedtuple('StateRec', ['LineNo', 'CodeBlock', 'Transitions'])
StateTransRecDef = namedtuple('StateTransRec', ['LineNo', 'State'])

  # Each code block found has this.
CodeBlockDef = namedtuple('CodeBLock', ['LineNo', 'Type'])

  # If the line number is set to 0 then was never set, Value will be None.
  # TODO: Make them all MultiParamCmdDef, its simpler
SingleCmdDef = namedtuple('SingleCmd', ['LineNo', 'Value'])

  # If the line number is set to 0 then was never set, Params will be an
  # empty list.
MultiParamCmdDef = namedtuple('MultiParamCmd', ['LineNo', 'Params'])

  # Languages supported
LanguagesSupported = ('Python', 'CPP', 'C', 'CSharp')
