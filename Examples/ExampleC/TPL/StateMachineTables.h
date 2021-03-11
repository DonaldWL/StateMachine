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

  Tables for the state machine
-----------------------------------------------------------------------------
*/
#pragma once

#ifdef __cplusplus
extern "C" {
#endif

//*@@CodeBlockNames:0@@*/

//*@@StateNames:0@@*/

  /* Used to index into each entry in the StateTable. */
enum STI {
  STI_CBIdx = 0, STI_StateIdx = 1, STI_StateLenIdx = 2, STI_StatesIdx = 3
};

/*@@StateTable:0@@*/

#ifdef __cplusplus
}
#endif
