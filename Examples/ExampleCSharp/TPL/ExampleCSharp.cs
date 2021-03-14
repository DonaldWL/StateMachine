/*@@CSharp@@*/
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
using System;
using System.Diagnostics;
using System.IO;

namespace ExampleCSharp
{
  class CExampleCSharp
  {
    static int Main(string[] args)
    {
      string InFileDir = Path.GetFullPath("../../../");
      string OutFileDir = Path.GetFullPath("../../../../CopyFiles");
      bool ForceOverwrite = false;
      string TraceFileName = Path.GetFullPath("../../../../StateMachineTrace.log");
      StreamWriter TraceFh = null;
      bool TraceFriendly = false;
      string LogFileName = Path.GetFullPath("../../../../StateMachine.log");
      StreamWriter LogFileFh = null;


      if (File.Exists(OutFileDir)) {
        Console.WriteLine("CopiedFiles exists and is not a directory");
        return (5);
      }

      if (Directory.Exists(OutFileDir)) {
        string[] files = Directory.GetFiles(OutFileDir, "*");
        for (int i = 0; i < files.Length; i++) {
          if (Directory.Exists(files[i])) {
            Console.WriteLine("Cannot remove %s because it contains a directory %s\n", OutFileDir, files[i]);
            return(6);
          }
        }
        for (int i = 0; i < files.Length; i++) {
          if (File.Exists(files[i])) {
            try {
              File.Delete(files[i]);
            } catch (IOException err) {
              Console.WriteLine("Cannot remove %s because %s\n", files[i], err.Message);
              return(7);
            }
          }
        }
        try {
          Directory.Delete(OutFileDir);
        } catch (IOException err) {
          Console.WriteLine("Cannot remove %s because %s\n", OutFileDir, err.Message);
          return (7);
        }
      }
      if (!Directory.Exists(OutFileDir)) {
        try {
          Directory.CreateDirectory(OutFileDir);
        } catch (IOException err) {
          Console.WriteLine("Cannot create %s because %s\n", OutFileDir, err.Message);
          return (7);
        }
      }

      TraceFh = new StreamWriter(TraceFileName);
      LogFileFh = new StreamWriter(LogFileName);

      // TODO: Create instance of state machine
      CStateMachine StateMachine = new CStateMachine(InFileDir, OutFileDir, ForceOverwrite,
                                                     TraceFh, TraceFriendly, LogFileFh);
      Stopwatch sw = new Stopwatch();
      sw.Restart();
      int RValue = StateMachine.Run();
      sw.Stop();

      // TODO: Output info
      Console.WriteLine("State machine duration ({0}ms)", sw.ElapsedMilliseconds);

      TraceFh.Close();
      LogFileFh.Close();

      return 0;
    }
  }
}
