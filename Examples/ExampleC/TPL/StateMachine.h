//*@@C@@*/
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

  The state machine
-----------------------------------------------------------------------------
*/
#pragma once

#include <stdbool.h> 

#ifdef __cplusplus
extern "C" {
#endif

  /* Used in ReturnValueDef. */
enum MO {
  MO_Ok = 0,                   /* ST OK */
  MO_CodeBlockInvalid = 1,     /* Code Block is invalid. */
  MO_ExitedMainLoop = 2,       /* Exited main while loop. */
  MO_StateRValueInvalid = 3,   /* State RValue is negative. */
  MO_NoOtherWise = 4,          /* No Otherwise defined and StateRValue out of range. */
  MO_NextStateIndxInvalid = 5  /* The state index from the table is out of range of */
                               /* the state table. */
};

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
typedef struct {
  enum MO MachineRValue;
  char *Msg;
  int UserRValue;
  char *UserData;
} ReturnValueDef;

  /* This is how you run the statemachine.  When it returns you need to validate
   * its outcome.  See the typedef struct ReturnValueDef.  The caller is
   * repsonsible to free this structure from memory.  Also if Msg is not NULL
   * then you must also free this memory.
   *
   *   _InFileDir
   *     Is the directory to copy from.  Does not have to be fully qualified
   *   _OutFileDir
   *     Is the directory to copy to.  Does not have to be fully qualified
   *   _ForcOverwrite
   *     If true write over the _OutFileDir files without prompting.
   *   _TraceFh
   *     If not equal to NULL then trace the state machine.
   *   _TraceFriendly
   *     If true will outpu a friendly type trace, but takes up a lot of
   *     space.  For log files recommend this to be false.
   *   _LogFh
   *     If not equal to NULL then log what the user code is doing.
   */
extern ReturnValueDef *ST_Run(const char *_InFileDir, const char *_OutFileDir, bool _ForceOverwrite,
                              FILE *_TraceFh, bool _TraceFriendly, FILE *_LogFh);

  /* Used to clean your ReturnValueDef that was returned from ST_Run.
   * It free's all the memory allocated for it and then returns NULL.
   * After you call this all the data within has been freed and also
   * the ReturnValueDef.  Keep in mind that the field 'UserData' just
   * is a simple free.  If you have created a complex structure then
   * you should free this and then set this value to NULL before you
   * call this function.
   */
extern ReturnValueDef *ST_CleanReturnValue(ReturnValueDef *_ReturnValue);

#ifdef __cplusplus
}
#endif
