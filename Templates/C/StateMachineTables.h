/*
SMS User Author:  Donald W. Long
SMS User Date:    01/22/2021
SMS User Version: 1.0
Creation Date:    03/23/21
SMS File Version: 1.0
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

  Tables for the state machine
-----------------------------------------------------------------------------
*/
#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#define CBLen 7
const char *CodeBlockNames[CBLen] = {"CloseFiles",
                                     "CopyFile",
                                     "EndMachine",
                                     "GetFiles",
                                     "NextFile",
                                     "OpenFiles",
                                     "StartMachine"};

enum CB {
  CB_CloseFiles = 0,
  CB_CopyFile = 1,
  CB_EndMachine = 2,
  CB_GetFiles = 3,
  CB_NextFile = 4,
  CB_OpenFiles = 5,
  CB_StartMachine = 6
};

#define SNLen 8
const char *StateNames[SNLen] = {"CloseFiles",
                                 "CloseFilesError",
                                 "CopyFile",
                                 "EndState",
                                 "GetFiles",
                                 "NextFile",
                                 "OpenFiles",
                                 "StartState"};

enum ST {
  ST_CloseFiles = 0,
  ST_CloseFilesError = 1,
  ST_CopyFile = 2,
  ST_EndState = 3,
  ST_GetFiles = 4,
  ST_NextFile = 5,
  ST_OpenFiles = 6,
  ST_StartState = 7
};

enum STI {
  STI_CBIdx = 0,
  STI_StateIdx = 1,
  STI_StateLenIdx = 2,
  STI_StatesIdx = 3
};

#define STLen 55
const int StateTable[STLen] = {CB_CloseFiles, ST_CloseFiles, 3, 32, 21, 21, -1,         /* 0 (NextFile, EndState, EndState), -1 */
                               CB_CloseFiles, ST_CloseFilesError, 3, 21, 21, 21, -1,    /* 7 (EndState, EndState, EndState), -1 */
                               CB_CopyFile, ST_CopyFile, 3, 0, 7, 7, -1,                /* 14 (CloseFiles, CloseFilesError, CloseFilesError), -1 */
                               CB_EndMachine, ST_EndState, 1, 21, -1,                   /* 21 (EndState), -1 */
                               CB_GetFiles, ST_GetFiles, 2, 32, 21, -1,                 /* 26 (NextFile, EndState), -1 */
                               CB_NextFile, ST_NextFile, 6, 42, 21, 21, 42, 21, 32, -1, /* 32 (OpenFiles, EndState, EndState, OpenFiles, EndState, NextFile), -1 */
                               CB_OpenFiles, ST_OpenFiles, 3, 14, 7, 7, -1,             /* 42 (CopyFile, CloseFilesError, CloseFilesError), -1 */
                               CB_StartMachine, ST_StartState, 2, 26, 21, -1};          /* 49 (GetFiles, EndState), -1 */

#ifdef __cplusplus
}
#endif
