//@@CopyFile@@
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

  Converters
-----------------------------------------------------------------------------
*/
#pragma once
#include <time.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  clock_t weeks;
  clock_t days;
  clock_t hours;
  clock_t minutes;
  clock_t seconds;
  clock_t milliseconds;
} CvtrValueDef;
  
typedef struct {
  int64_t weeks;
  int64_t days;
  int64_t hours;
  int64_t minutes;
  int64_t seconds;
  int64_t milliseconds;
} CvtrValue64Def;

  // Converts milliseconds into CvtrValueDef.  It overflows at after
  // 3w 3d 20h 31m 23s 647ms.  If you need more than this then use
  // ConvertMilliseconds64.  You are responsible for the memory 
  // allocated that is returned.  When you are done free CvtrValueDef.
extern CvtrValueDef *ConvertMilliseconds(const clock_t _milliseconds, bool _week);

  // Converts milliseconds into CvtrValue64Def.  You are responsible for the
  // memory allocated that is returned.  When you are done free CvtrValue64Def. 
  // This one has less of a limitation because of the large 64bit number.
extern CvtrValue64Def *ConvertMilliseconds64(const int64_t _milliseconds, bool _week);

#ifdef __cplusplus
}
#endif
