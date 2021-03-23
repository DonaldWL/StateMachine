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

  /*
   * This is returned from ST_Run.
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
   *   _LogFh
   *     If not equal to NULL then log what the user code is doing.
   */
extern ReturnValueDef *ST_Run(const char *_InFileDir, const char *_OutFileDir, bool _ForceOverwrite,
                              FILE *_TraceFh, FILE *_LogFh);

#ifdef __cplusplus
}
#endif
