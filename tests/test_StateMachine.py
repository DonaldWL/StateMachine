import os
import random
import unittest

from Libs.Base.CreationInfo import CCreationInfo
from Libs.Base.TraceFile import CTraceFile
from Libs.StateMachine.StateMachine import (CStateMachine, CodeBlockEntryDef ,
                                            StateTableEntryDef, StateMachineError)


class CMyTraceFile(CTraceFile):

  def __init__(self):
    CTraceFile.__init__(self)

    self._Output = ""

  def write(self, data):
    if data is not None:
      self._Output = self._Output + str(data)

  def writeline(self, data):
    if data is not None:
      self._Output = self._Output + str(data) + "\n"

  @property
  def GetLines(self):
    return self._Output


class CMyStateMachine(CStateMachine):

  def __init__(self, TraceFile = None):
    CStateMachine.__init__(self, TraceFile)

    self.Globals = globals()
    self.Locals = locals()
    self.ModuleFileName = os.path.basename(CCreationInfo().CreationFile)
    self.CodeBlockTable = (CodeBlockEntryDef("EndRun", compile(self.EndRun, self.ModuleFileName, "exec")),
                           CodeBlockEntryDef("CodeBlock1", compile(self.CodeBlock1, self.ModuleFileName, "exec")),
                           CodeBlockEntryDef("CodeBlock2", compile(self.CodeBlock2, self.ModuleFileName, "exec")),
                           CodeBlockEntryDef("CodeBlock3", compile(self.CodeBlock3, self.ModuleFileName, "exec")),
                           CodeBlockEntryDef("CodeBlock4", compile(self.CodeBlock4, self.ModuleFileName, "exec")),
                           CodeBlockEntryDef("CodeBlock5", compile(self.CodeBlock5, self.ModuleFileName, "exec")),
                           CodeBlockEntryDef("CodeBlock6", compile(self.CodeBlock6, self.ModuleFileName, "exec")),
                           CodeBlockEntryDef("CodeBlock7", compile(self.CodeBlock7, self.ModuleFileName, "exec")),
                           CodeBlockEntryDef("CodeBlock8", compile(self.CodeBlock8, self.ModuleFileName, "exec")))

      # We will Change the table in the test
      # methods.  This is not normal, but it
      # does make is easer for testing.
    self.StateTable = None

    self.StateNames = ("EndRun",
                       "State1",
                       "State2",
                       "State3",
                       "State4",
                       "State5",
                       "State6",
                       "State7",
                       "State8",
                       "State9")

      # We will use this to change what values
      # EndRun returns in each test.
    self.EndRunRValue = -1

  def GetCodeBlockName(self, CBIndex):
    return self.CB(self.CodeBlockTable[CBIndex].CBIndx).name
  
  def GetStateName(self, SNIndex):
    return self.StateNames[SNIndex]

  EndRun = "self.StateRValue = self.EndRunRValue"
  CodeBlock1 = "self.StateRValue = random.randint(0, 8)"
  CodeBlock2 = "self.StateRValue = random.randint(0, 2)"
  CodeBlock3 = "self.StateRValue = random.randint(0, 2)"
  CodeBlock4 = "self.StateRValue = random.randint(0, 10)"
  CodeBlock5 = "self.StateRValue = 0"
  CodeBlock6 = "self.StateRValue = 'me'"
  CodeBlock7 = "pass"
  CodeBlock8 = "self.StateRValue = -11"


  # Our state machine for testing
SM = CMyStateMachine()


class StateMachine(unittest.TestCase):

  def test_Good(self):
    SM.StateTable = (StateTableEntryDef(0, None, None),  # State 0
                     StateTableEntryDef(1, (2, 3, 4, 4, 4, 6), 4),  # State 1
                     StateTableEntryDef(2, (3,), 2),  # State 2
                     StateTableEntryDef(3, (4,), 3),  # State 3
                     StateTableEntryDef(4, (0, 5, 6, 6, 6, 2, 6), 1),  # State 4
                     StateTableEntryDef(5, (1,), 3),  # State 5
                     StateTableEntryDef(2, (5,), 2)  # State 6
                     )

    SM.EndRunRValue = random.randint(0, 4)

    for cnt in range(0, 100):  # pylint: disable=unused-variable
      self.assertIn(SM.Run(), (0, 1, 2, 3, 4))

  def test_EmptyTables(self):
    SM.StateTable = (StateTableEntryDef(0, None, None),  # State 0
                     StateTableEntryDef(1, (1, 1, 2, 1, 2, 2), 0),  # State 1
                     StateTableEntryDef(2, (2,), 1),  # State 2
                     )

    for cnt in range(0, 100):  # pylint: disable=unused-variable
      SavedCodeBlockTable = SM.CodeBlockTable
      SavedStateTable = SM.StateTable
      try:
        SM.CodeBlockTable = ()
        self.assertRaises(StateMachineError, SM.Run)

        SM.CodeBlockTable = SavedCodeBlockTable
        SM.StateTable = ()
        self.assertRaises(StateMachineError, SM.Run)
      finally:
        SM.CodeBlockTable = SavedCodeBlockTable
        SM.StateTable = SavedStateTable

  def test_BadStateRValue(self):
    SM.StateTable = (StateTableEntryDef(0, None, None),  # State 0
                     StateTableEntryDef(7, (1, 1, 2, 1, 2, 2), 0),  # State 1
                     StateTableEntryDef(2, (2,), 1),  # State 2
                     )
    for cnt in range(0, 100):  # pylint: disable=unused-variable
      self.assertRaises(StateMachineError, SM.Run)

    SM.StateTable = (StateTableEntryDef(0, None, None),  # State 0
                     StateTableEntryDef(1, (2, 2, 2, 2, 2, 2), 2),  # State 1
                     StateTableEntryDef(7, (0,), 0),  # State 2
                     )
    for cnt in range(0, 100):  # pylint: disable=unused-variable
      self.assertRaises(StateMachineError, SM.Run)

    SM.StateTable = (StateTableEntryDef(0, None, None),  # State 0
                     StateTableEntryDef(8, (2, 2, 2, 2, 2, 2), 2),  # State 1
                     StateTableEntryDef(2, (0,), 0),  # State 2
                     )
    for cnt in range(0, 100):  # pylint: disable=unused-variable
      self.assertRaises(StateMachineError, SM.Run)

    SM.StateTable = (StateTableEntryDef(0, None, None),  # State 0
                     StateTableEntryDef(1, (2, 2, 2, 2, 2, 2), 2),  # State 1
                     StateTableEntryDef(8, (0,), 0),  # State 2
                     )
    for cnt in range(0, 100):  # pylint: disable=unused-variable
      self.assertRaises(StateMachineError, SM.Run)

  def test_StateNegative(self):
    SM.StateTable = (StateTableEntryDef(0, None, None),  # State 0
                     StateTableEntryDef(1, (-1, -1, -2, -1, -2, -2), -8),  # State 1
                     StateTableEntryDef(2, (2,), 1),  # State 2
                     )
    for cnt in range(0, 100):  # pylint: disable=unused-variable
      self.assertRaises(StateMachineError, SM.Run)

    SM.StateTable = (StateTableEntryDef(0, None, None),  # State 0
                     StateTableEntryDef(1, (2, 2, 2, 2, 2, 2), 2),  # State 1
                     StateTableEntryDef(1, (-1, -1, -2, -1, -2, -2), -8),  # State 1
                     )
    for cnt in range(0, 100):  # pylint: disable=unused-variable
      self.assertRaises(StateMachineError, SM.Run)

  def test_Trace(self):
    MyTraceFile = CMyTraceFile()
    xSM = CMyStateMachine(MyTraceFile)

    xSM.StateTable = (StateTableEntryDef(0, None, None),
                      StateTableEntryDef(5, (2,), 2),  # State 2
                      StateTableEntryDef(5, (0,), 0))

    TraceResults = "State:             1 (State1)\n"
    TraceResults = TraceResults + "State Entry:       (CodeBlock5: (2,), 2)\n"
    TraceResults = TraceResults + "State RValue:      0\n"
    TraceResults = TraceResults + "State:             2 (State2)\n"
    TraceResults = TraceResults + "State Entry:       (CodeBlock5: (0,), 0)\n"
    TraceResults = TraceResults + "State RValue:      0\n"
    TraceResults = TraceResults + "Prev State:        1 (State1)\n"
    TraceResults = TraceResults + "Prev State Entry:  (CodeBlock5: (2,), 2)\n"
    TraceResults = TraceResults + "Prev State RValue: 0\n"

      # Test that the lines are correct.  We are get`ting good trace info.
    self.maxDiff = None
    xSM.Run()
    self.assertEqual(MyTraceFile.GetLines, TraceResults)

      # Make sure that we have to set TraceFile to a CTraceFile
    with self.assertRaises(AttributeError):
      xSM.TraceFile = ""

      # Make sure that we handle bad statenames in the trace.
    xSM.StateNames = ()
    xSM.Run()


if __name__ == "__main__":
  # import sys;sys.argv = ['', 'Test.testName']
  unittest.main()
