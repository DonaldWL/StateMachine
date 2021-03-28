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
import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

public class JavaExample {
	
	public static final int ECodes_OK = 0;
	public static final int ECodes_OpenErrorOnLogFile = 1;
	public static final int ECodes_OpenErrorOnTraceFile = 2;
	public static final int ECodes_OutFileDirError = 3;
	public static final int ECodes_OutFileDirContainsDirs = 4;
	public static final int ECodes_CanNotDeleteAFile = 5;
	public static final int ECodes_CanNotDeleteDir = 6;
	public static final int ECodes_CanNotCreateDir = 7;
	
  public static void main(String[] args) throws IOException {
    String InFileDir = "../Src";
    String OutFileDir = "../CopyFiles";
    boolean  ForceOverwrite = false;
    String TraceFileName = "../StateMachineTrace.log";
    boolean  TraceFriendly = false;
    String LogFileName = "../StateMachine.log";

    Path t = Paths.get(System.getProperty("user.dir"));
    InFileDir = Paths.get(t.toString(), InFileDir).toString();
    OutFileDir = Paths.get(t.toString(), OutFileDir).toString();
    File xOutFile = new File(OutFileDir);
    if (xOutFile.exists() && !xOutFile.isDirectory()) {
			System.out.format("OutFileDir exists and is not a directory (%s)\n", OutFileDir);
      System.exit(ECodes_OutFileDirError);
    }
    if (xOutFile.isDirectory()) {
      String files[] = xOutFile.list();
      for(int i=0; i<files.length; i++) {
        Path filePath = Paths.get(OutFileDir, files[i]);          
        File tFile = new File(filePath.toString());
        if (tFile.isDirectory()) {
    			System.out.format("Cannot remove %s because it contains a directory %s\n", OutFileDir, files[i]);
          System.exit(ECodes_OutFileDirContainsDirs);
        }
      }    	
      for(int i=0; i<files.length; i++) {
        Path filePath = Paths.get(OutFileDir, files[i]);          
        File tFile = new File(filePath.toString());
        if (tFile.exists()) {
        	if (!tFile.delete()) {
      			System.out.format("Cannot remove file %s\n", files[i]);
            System.exit(ECodes_CanNotDeleteAFile);
        	}
        }
      }
      if (!xOutFile.delete()) {
  			System.out.format("Cannot remove OutFileDir %s\n", OutFileDir);
        System.exit(ECodes_CanNotDeleteDir);
      }
    }
    if (!xOutFile.exists()) {
    	if (!xOutFile.mkdir()) {
  			System.out.format("Cannot create OutFileDir %s\n", OutFileDir);
        System.exit(ECodes_CanNotCreateDir);
    	}
    }

			// Create instance of state machine
		StateMachine MyStateMachine = new StateMachine(InFileDir, OutFileDir, ForceOverwrite,
				                                           new File(TraceFileName), TraceFriendly, 
				                                           new File(LogFileName));

    String SepLine = "";
    for (int i = 0; i < 50; i++) SepLine += "-";
    System.out.format("%s\n", SepLine);
    
		long startTime = System.currentTimeMillis();
		MyStateMachine.Run();
		long stopTime = System.currentTimeMillis();
		
		System.out.format("State Machine RValue (%d)\n", MyStateMachine.ReturnValue.MachineRValue);
		System.out.format("State machine Msg (%s)\n", MyStateMachine.ReturnValue.Msg);
		System.out.format("State Machine User RValue (%d)\n", MyStateMachine.ReturnValue.UserRValue);
		System.out.format("State machine User Msg (%s)\n", MyStateMachine.ReturnValue.UserData);
		System.out.format("State machine duration (%dms)\n", stopTime-startTime);
    System.out.format("%s\n", SepLine);
		
	  System.exit(ECodes_OK);
  }
}
