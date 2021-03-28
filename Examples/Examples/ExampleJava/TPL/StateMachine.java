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
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.Date;

public class StateMachine {
	
    /* Used in ReturnValueDef. */
	public static final int MO_Ok = 0;                   /* ST OK */
	public static final int MO_CodeBlockInvalid = 1;     /* Code Block is invalid. */
	public static final int MO_ExitedMainLoop = 2;       /* Exited main while loop. */
	public static final int MO_StateRValueInalid = 3;    /* State RValue is negative. */
	public static final int MO_NoOtherWise = 4;          /* No Otherwise defined and StateRValue out of range. */
	public static final int MO_NextStateIndxInvalid = 5; /* The state index from the table is out of range of */
                                                       /* the state table. */
	
	public static final int URValue_Ok = 0;
	public static final int URValue_InDirErr = 1;
	public static final int URValue_OutDirErr = 2;
	public static final int URValue_InOutDirErr = 3;
	public static final int URValue_NoFilesToProcess = 4;
	public static final int URValue_InFileOpenError = 5;
	public static final int URValue_OutFileOpenError = 6;
	public static final int URValue_InFileReadError = 7;
	public static final int URValue_OutFileWriteError = 8;
	public static final int URValue_InFileCloseError = 9;
	public static final int URValue_OutFileCloseError = 10;
	
	/*
	* This is returned from ST_Run.
	*   MachineRValue
	*     Is the outcome from the state machine.  See
	*     enum MO for valid values
	*   Msg
	*     If not NULL is the message about the issue.
	*   UserRValue
	*     Is the user value that they wish to return.
	*     If the user code does not set this it will be
	*     -1.
	*   UserData
	*     Is the user date they wish to return.  This is
	*     a void pointer.  You will have to cast this.  If
	*     the user does not set this it will be NULL.
	*/
	public class ReturnValueDef
	{
	  public int MachineRValue;
	  public String Msg;
	  public int UserRValue;
	  public String UserData;
	};
	public ReturnValueDef ReturnValue = new ReturnValueDef();

	private String InFileDir;
	private String OutFileDir;
	private boolean ForceOverwrite;
	private File TraceFile;
	private PrintWriter TraceFh =  null;
	private boolean TraceFriendly;
	private File LogFile;
	private PrintWriter LogFh = null;
	
  public StateMachine(String _InFileDir, String _OutFileDir, boolean _ForceOverwrite,
  		                File _TraceFile, boolean _TraceFriendly, File _LogFile)
	{
		InFileDir = _InFileDir;
		OutFileDir = _OutFileDir;
		ForceOverwrite = _ForceOverwrite;
		TraceFile = _TraceFile;
		TraceFriendly = _TraceFriendly;
		LogFile = _LogFile;
		
  }

  public int Run() throws FileNotFoundException {
    int CurStateIndx = CSMT.StartStateIndx;
    int PrevCurStateIndx = CSMT.StartStateIndx;
    int OtherWise = -1;
    int StateRValue = -1;
    boolean ProcessStates = true;
    int FilesIndx = 0;
    String[] Files = { };
    File InFileName = null;
    File OutFileName = null;
    BufferedReader InFileFh = null;
    BufferedWriter OutFileFh = null;
    ReturnValue.MachineRValue = MO_Ok;
    ReturnValue.Msg = "";
    ReturnValue.UserRValue = URValue_Ok;
    ReturnValue.UserData = "";

	  	// Open log and trace files.
    if (LogFile != null) LogFh = new PrintWriter(LogFile);
   	if (TraceFile != null) TraceFh = new PrintWriter(TraceFile);
    
    while (ProcessStates) {
      switch (CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]) {

	        // StateRValue
	        //   0 -> Ok
	        //   1 -> InFileDir does not exist
	        //        OutFileDir does not exist
	        //        InFileDir and OutFileDir are the same
      	case CSMT.CB_StartMachine:
          StateRValue = 0;
          Log("Info", "InFileDir set to ", InFileDir);
          Log("Info", "OutFileDir set to ", OutFileDir);
          File xInFileDir = new File(InFileDir);
          if (xInFileDir.exists() && !xInFileDir.isDirectory()) {
	          StateRValue = 1;
	          ReturnValue.UserData = Log("Error", "InFileDir (", InFileDir, 
	                                     ") does not exist or is not a directory");
	          ReturnValue.UserRValue = URValue_InDirErr;
	        }
          File xOutFileDir = new File(OutFileDir);
          if (xOutFileDir.exists() && !xOutFileDir.isDirectory()) {
	          StateRValue = 1;
	          ReturnValue.UserData = Log("Error", "OutFileDir (", OutFileDir, 
	                                     ") does not exist or is not a directory");
	          ReturnValue.UserRValue = URValue_OutDirErr;
	        }
          
          if (xInFileDir.compareTo(xOutFileDir) == 0) {
	          StateRValue = 1;
	          ReturnValue.UserData = Log("Error", "InFileDir (", InFileDir, 
	                                     ") is the same as OutFileDir (", OutFileDir, ")");
	          ReturnValue.UserRValue = URValue_InOutDirErr;
          }
        	break;

          // StateRValue
          //   0 -> Ok
          //   1 -> No files to process in InFileDir
        case CSMT.CB_GetFiles:
          StateRValue = 0;
          FilesIndx = 0;
          File xInFile = new File(InFileDir);
          Files = xInFile.list();
          if (Files != null) {
	          Log("Info", "Number of files to process (", Integer.toString(Files.length), 
	              ") from InFileDir (", InFileDir, ")");

	          if (Files.length == 0) {
	            StateRValue = 1;
	            ReturnValue.UserData = Log("Error", "No files found to process at InFileDir (", InFileDir, ")");
	            ReturnValue.UserRValue = URValue_NoFilesToProcess;
	          }
          } else {
            StateRValue = 1;
            ReturnValue.UserData = Log("Error", "No files found to process at InFileDir (", InFileDir, ")");
            ReturnValue.UserRValue = URValue_NoFilesToProcess;
          }
        	break;

          // StateRValue
          //   0 -> Ok
          //   1 -> No more files to process
          //   2 -> Out file already exists and not in interactive mode
          //   3 -> Out File already exists and user stated overwrite the file
          //   4 -> User does not wish to overwrite file
          //   5 -> User wishes to skip file, or is a log file to skip.
        case CSMT.CB_NextFile:
          StateRValue = 0;
          if (FilesIndx == Files.length) {
            StateRValue = 1;
          } else {
            InFileName = new File(Files[FilesIndx]);
      			if (InFileName.isDirectory()) {
              Log("Info", "Skipping Directory (", InFileName.getAbsoluteFile().toString(), ")");
              StateRValue = 5;
      			} else if (InFileName.getName().charAt(0) == '.') {
              Log("Info", "Skipping file (", InFileName.getAbsoluteFile().toString(), ")");
              StateRValue = 5;
            }
            FilesIndx++;
            if (StateRValue == 0) {
              // TODO: Handle 2-5
            }
          }
        	break;

          // StateRValue
          //   0 -> Ok
          //   1 -> Unable to open in file
          //   2 -> Unable to open out file
        case CSMT.CB_OpenFiles:
          StateRValue = 0;

          InFileName = new File(Paths.get(InFileDir, InFileName.toString()).toString());
          Log("Info", "Opening file InFile ", InFileName.getAbsoluteFile().toString());
          try {
          	InFileFh = new BufferedReader(new FileReader(InFileName));
          	
            Path filePath = Paths.get(OutFileDir, InFileName.getName());          
            OutFileName = new File(filePath.toString());
            Log("Info", "Opening file OutFile ", InFileName.getAbsoluteFile().toString());
            try {
            	OutFileFh = new BufferedWriter(new FileWriter(OutFileName));
            } catch (IOException err) {
              StateRValue = 2;
              ReturnValue.UserData = Log("Error", "Unable to open out file (", OutFileName.getAbsoluteFile().toString(),
                                         ") => ", err.getMessage());
              ReturnValue.UserRValue = URValue_OutFileOpenError;
            }
          } catch (IOException err) {
            ReturnValue.UserData = Log("Error", "Unable to open in file (", InFileName.getAbsoluteFile().toString(),
                                       ") => ", err.getMessage());
            ReturnValue.UserRValue = URValue_InFileOpenError;
            StateRValue = 1;
          }
        	break;

          // StateRValue
          //   0 -> Ok
          //   1 -> Read error on InFile
          //   2 -> Write error on OutFile
        case CSMT.CB_CopyFile:
          StateRValue = 0;
          String line;

          Log("Info", "Coping file (", InFileName.toString(), ") to (",
              OutFileName.toString(), ")");
          try {
            while ((line = InFileFh.readLine()) != null) {
              try { 
                OutFileFh.write(line + "\n");
              } catch (IOException err) {
                StateRValue = 2;
                ReturnValue.UserData = Log("Error", "Unable to write out file (", OutFileName.toString(),
                    ") => ", err.getMessage());
                ReturnValue.UserRValue = URValue_OutFileWriteError;
              }
            }
          } catch (IOException err) {
            StateRValue = 1;
            ReturnValue.UserData = Log("Error", "Unable to read in file (", InFileName.toString(),
                                       ") => ", err.getMessage());
            ReturnValue.UserRValue = URValue_InFileReadError;
          }
        	break;

          // StateRValue
          //   0->Ok
          //   1->Unable to close in file
          //   2->Unable to close out file
        case CSMT.CB_CloseFiles:
          StateRValue = 0;
          if (InFileFh != null) {
            Log("Info", "Closing file InFile ", InFileName.toString());
            try { 
              InFileFh.close();
            } catch (IOException err) {
              StateRValue = 1;
              ReturnValue.UserData = Log("Error", "Unable to close in file (", InFileName.toString(),
                                         ") => ", err.getMessage());
              ReturnValue.UserRValue = URValue_InFileCloseError;
            }
          }

          if (OutFileFh != null) {
            Log("Info", "Closing file OutFile ", OutFileName.toString());
            try { 
              OutFileFh.close();
            } catch (IOException err) {
              StateRValue = 2;
              ReturnValue.UserData = Log("Error", "Unable to close out file (", OutFileName.toString(),
                                         ") => ", err.getMessage());
              ReturnValue.UserRValue = URValue_OutFileCloseError;
            }
          }
        	break;

          // End the state machine.  We setup to drop out of the main
          // processing loop and return to the calling program.
        case CSMT.CB_EndMachine:
          StateRValue = 0;
          ProcessStates = false;
          if (ReturnValue.UserData == "") {
            ReturnValue.UserData = "Ending State Machine";
          }
          Log("Info", ReturnValue.UserData);
        	break;

        default:
          ReturnValue.MachineRValue = MO_CodeBlockInvalid;
          ReturnValue.Msg = "Invalid CodeBlock => State: " +
                            CSMT.StateNames[CSMT.StateTable[PrevCurStateIndx + (int) CSMT.STI_StateIdx]] +
                            "  CodeBlock: " +
                            CSMT.CodeBlockNames[CSMT.StateTable[PrevCurStateIndx + (int) CSMT.STI_CBIdx]] +
                            "  StateRValue: " + StateRValue;
          Log("Error", ReturnValue.Msg);
          ProcessStates = false;
        	break;
      }

      if (StateRValue < 0) {
	      ReturnValue.MachineRValue = MO_StateRValueInalid;
	      ReturnValue.Msg = "StateRValue is negative => State: " +
	                         CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]] +
	                         "  CodeBlock: " +
	                         CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]] +
	                         "  StateRValue: " + StateRValue;
	      Log("Error", ReturnValue.Msg);
	      ProcessStates = false;
	      break;
      }

      OtherWise = -1;
      if (StateRValue > CSMT.StateTable[CurStateIndx + CSMT.STI_StateLenIdx])
      {
        OtherWise = CSMT.StateTable[CurStateIndx + CSMT.STI_StateLenIdx + CSMT.StateTable[CurStateIndx + CSMT.STI_StateLenIdx] + 1];
        if (OtherWise < 0) {
          ReturnValue.MachineRValue = MO_NoOtherWise;
          ReturnValue.Msg = "No Otherwise found => State: " +
                            CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]] +
                            "  CodeBlock: " +
                            CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]] +
                            "  StateRValue: " + StateRValue;
          Log("Error", ReturnValue.Msg);
          ProcessStates = false;
          break;
        }
      }

      if (TraceFh != null) {
        if (TraceFriendly) {
          TraceFh.write("State Trace\n");
          TraceFh.format("  State:         %s\n", 
                         CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]]);
          TraceFh.format("  CodeBlock:     %s\n",
                         CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]]);
          TraceFh.format("  StateRValue:   %d\n", StateRValue);
        } else {
          String pattern = "yyyy-MM-dd HH:MM:ss";
          SimpleDateFormat simpleDateFormat = new SimpleDateFormat(pattern);
          String date = simpleDateFormat.format(new Date());
          TraceFh.format("%s: %s,%s,%d\n", date,
                            CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]],
                            CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]],
                            StateRValue);
        }
      }

      PrevCurStateIndx = CurStateIndx;
      if (OtherWise > -1) {
        CurStateIndx = OtherWise;
      } else {
        CurStateIndx = CSMT.StateTable[CurStateIndx + CSMT.STI_StatesIdx + StateRValue];
      }
      if (CurStateIndx > CSMT.STLen) {
        ReturnValue.MachineRValue = MO_NextStateIndxInvalid;
        ReturnValue.Msg = "Index into state table out of range => State: " +
                          CSMT.StateNames[CSMT.StateTable[PrevCurStateIndx + CSMT.STI_StateIdx]] +
                          "  CodeBlock: " +
                          CSMT.CodeBlockNames[CSMT.StateTable[PrevCurStateIndx + CSMT.STI_CBIdx]] +
                          "  StateRValue: " + StateRValue;
        Log("Error", ReturnValue.Msg);
        ProcessStates = false;
        break;
      }
    }
    
    if (ProcessStates) {
      ReturnValue.MachineRValue = MO_ExitedMainLoop;
      ReturnValue.Msg = "Exited the main loop => State: " +
                        CSMT.StateNames[CSMT.StateTable[CurStateIndx + CSMT.STI_StateIdx]] +
                        "  CodeBlock: " +
                        CSMT.CodeBlockNames[CSMT.StateTable[CurStateIndx + CSMT.STI_CBIdx]] +
                        "  StateRValue: " + StateRValue;
      Log("Error", ReturnValue.Msg);
    }
    
    if (LogFile != null) LogFh.close();
   	if (TraceFile != null) TraceFh.close();
    return ReturnValue.UserRValue;
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
