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

  Some converters.
-----------------------------------------------------------------------------
*/
#include <time.h>
#include <stdlib.h>
#include <stdbool.h> 
#include <stdint.h>

#include "Converters.h"

CvtrValueDef *ConvertMilliseconds(const clock_t _milliseconds, bool _week)
{
  CvtrValueDef *CvtrValue = malloc(sizeof(CvtrValueDef));

  CvtrValue->seconds = (_milliseconds / 1000) % 60;
  CvtrValue->minutes = (_milliseconds / (1000 * 60)) % 60;
  CvtrValue->hours = (_milliseconds / (1000 * 60 * 60)) % 24;
  if (_week) {
    CvtrValue->days = (_milliseconds / (1000 * 60 * 60 * 24)) % 7;
    CvtrValue->weeks = _milliseconds / (1000 * 60 * 60 * 24 * 7);
    CvtrValue->milliseconds = _milliseconds - ((CvtrValue->seconds * 1000) + (CvtrValue->minutes * (60 * 1000)) +
      (CvtrValue->hours * (1000 * 60 * 60)) + (CvtrValue->days * (1000 * 60 * 60 * 24)) +
                                               (CvtrValue->weeks * (1000 * 60 * 60 * 24 * 7)));

  } else {
    CvtrValue->days = _milliseconds / (1000 * 60 * 60 * 24);
    CvtrValue->weeks = 0;
    CvtrValue->milliseconds = _milliseconds - ((CvtrValue->seconds * 1000) + (CvtrValue->minutes * (60 * 1000)) +
      (CvtrValue->hours * (1000 * 60 * 60)) + (CvtrValue->days * (1000 * 60 * 60 * 24)));
  }

  return CvtrValue;
}

CvtrValue64Def *ConvertMilliseconds64(const int64_t _milliseconds, bool _week)
{
  CvtrValue64Def *CvtrValue = malloc(sizeof(CvtrValue64Def));

  CvtrValue->seconds = (_milliseconds / 1000) % 60;
  CvtrValue->minutes = (_milliseconds / (1000 * 60)) % 60;
  CvtrValue->hours = (_milliseconds / (1000 * 60 * 60)) % 24;
  if (_week) {
    CvtrValue->days = (_milliseconds / (1000 * 60 * 60 * 24)) % 7;
    CvtrValue->weeks = _milliseconds / (1000 * 60 * 60 * 24 * 7);
    CvtrValue->milliseconds = _milliseconds - ((CvtrValue->seconds * 1000) + (CvtrValue->minutes * (60 * 1000)) +
                              (CvtrValue->hours * (1000 * 60 * 60)) + (CvtrValue->days * (1000 * 60 * 60 * 24)) +
                              (CvtrValue->weeks * (1000 * 60 * 60 * 24 * 7)));

  } else {
    CvtrValue->days = _milliseconds / (1000 * 60 * 60 * 24);
    CvtrValue->weeks = 0;
    CvtrValue->milliseconds = _milliseconds - ((CvtrValue->seconds * 1000) + (CvtrValue->minutes * (60 * 1000)) +
                              (CvtrValue->hours * (1000 * 60 * 60)) + (CvtrValue->days * (1000 * 60 * 60 * 24)));
  }

  return CvtrValue;
}
