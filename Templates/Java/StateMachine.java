/*@@Java@@*/
/*
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

  An example state machine that copies the files from one dir to another.
-----------------------------------------------------------------------------
*/
import java.text.SimpleDateFormat;
import java.util.Date;
import java.io.File;
import java.io.PrintWriter;
import java.io.FileNotFoundException;

public class StateMachine {
	private File TraceFile;
	private PrintWriter TraceFh =  null;
	private File LogFile;
	private PrintWriter LogFh = null;
	
  public StateMachine(File _TraceFile, File _LogFile)
	{
		TraceFile = _TraceFile;
		LogFile = _LogFile;
  }

  public void Run() throws FileNotFoundException {
    int CurStateIndx = @@StartStateValue@@;
    int PrevCurStateIndx = @@StartStateValue@@;
    int OtherWise = -1;
    int StateRValue = -1;
    boolean ProcessStates = true;

	  	// Open log and trace files.
    if (LogFile != null) LogFh = new PrintWriter(LogFile);
   	if (TraceFile != null) TraceFh = new PrintWriter(TraceFile);
    
    while (ProcessStates) {
      switch (CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]) {

        @@CodeBlocks@@

        default:
          String Msg = "Invalid CodeBlock => State: " +
                       CSMT.StateNames[CSMT.StateTable[PrevCurStateIndx + (int) CSMT.STI_StateIdx]] +
                       "  CodeBlock: " +
                       CSMT.CodeBlockNames[CSMT.StateTable[PrevCurStateIndx + (int) CSMT.STI_CBIdx]] +
                       "  StateRValue: " + StateRValue;
          Log("Error", Msg);
          ProcessStates = false;
        	break;
      }

      if (StateRValue < 0) {
	      String Msg = "StateRValue is negative => State: " +
	                    CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]] +
	                    "  CodeBlock: " +
	                    CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]] +
	                    "  StateRValue: " + StateRValue;
	      Log("Error", Msg);
	      ProcessStates = false;
	      break;
      }

      OtherWise = -1;
      if (StateRValue > CSMT.StateTable[CurStateIndx + CSMT.STI_StateLenIdx])
      {
        OtherWise = CSMT.StateTable[CurStateIndx + CSMT.STI_StateLenIdx + CSMT.StateTable[CurStateIndx + CSMT.STI_StateLenIdx] + 1];
        if (OtherWise < 0) {
          String Msg = "No Otherwise found => State: " +
                       CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]] +
                       "  CodeBlock: " +
                       CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]] +
                       "  StateRValue: " + StateRValue;
          Log("Error", Msg);
          ProcessStates = false;
          break;
        }
      }

      if (TraceFh != null) {
        String pattern = "yyyy-MM-dd HH:MM:ss";
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat(pattern);
        String date = simpleDateFormat.format(new Date());
        TraceFh.format("%s: %s,%s,%d\n", date,
                        CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]],
                        CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]],
                        StateRValue);
      }

      PrevCurStateIndx = CurStateIndx;
      if (OtherWise > -1) {
        CurStateIndx = OtherWise;
      } else {
        CurStateIndx = CSMT.StateTable[CurStateIndx + CSMT.STI_StatesIdx + StateRValue];
      }
      if (CurStateIndx > CSMT.STLen) {
        String Msg = "Index into state table out of range => State: " +
                     CSMT.StateNames[CSMT.StateTable[PrevCurStateIndx + CSMT.STI_StateIdx]] +
                     "  CodeBlock: " +
                     CSMT.CodeBlockNames[CSMT.StateTable[PrevCurStateIndx + CSMT.STI_CBIdx]] +
                     "  StateRValue: " + StateRValue;
        Log("Error", Msg);
        ProcessStates = false;
        break;
      }
    }
    
    if (ProcessStates) {
      String Msg = "Exited the main loop => State: " +
                   CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]] +
                   "  CodeBlock: " +
                   CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]] +
                   "  StateRValue: " + StateRValue;
      Log("Error", Msg);
    }
    
    if (LogFile != null) LogFh.close();
   	if (TraceFile != null) TraceFh.close();
    return;
  }
  
    // Used to log messages.  Returns the message without the time stamp so
    // it can be used for something else.  The timestamp message is sent to 
    // the logger.
  private String Log(String _MsgType, String ... _Msg)
  {
    String Msg = "";
    String MsgBase = "";

    String pattern = "yyyy-MM-dd HH:MM:ss: ";
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat(pattern);
    String date = simpleDateFormat.format(new Date());
    
    Msg = date;
    Msg += _MsgType;
    Msg += ": ";
    		
    for (String xMsg: _Msg) {
      Msg += xMsg;
      MsgBase += xMsg;
    }
    Msg += "\n";
    if (LogFh != null) {
      LogFh.write(Msg);
    }
    return MsgBase;
  }
}
