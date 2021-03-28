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

  File access stuff, making it work on windows and linux.
-----------------------------------------------------------------------------
*/
#pragma once

#include <stdbool.h> 
#include <stdio.h>

#include "DList.h"

#ifdef __cplusplus
extern "C" {
#endif

  /* If the file exists it will return true.  Remember that
   * if it is not fully qualified it may not find it.
   */
extern bool FileExist(const char *_path);

  /* If the path exists and is a dir will return true.  Remember that
   * if it is not fully qualified it may not find it.
   */
extern bool IsDir(const char *_path);

  /* If the path exists and is a file will return true.  Remember that
   * if it is not fully qualified it may not find it.
   */
extern bool IsFile(const char *_path);

  /* Returns the current directory.  You must manage the memory,
   * free it when done.
   */
extern char *CurDir(void);

  /* Returns the fully qualified path name.  You must
   * manage the memory.  free it when done.  If NULL
   * is returned then failed.
   */
extern char *RealPath(const char *_path);

  /* Join the two paths together.  If path1 starts with
   * a file seperator and path is not empty then returns
   * path else it joins them for you.  If NULL is returned
   * then failed.
   */
extern char *JoinPath(const char *_path, const char *_path1);

  /* Is returned by SplitPath.  Contains all the data you need
   * for the file.  Keep in mind you need to manage the memory.
   * You can use SplitPathClean to clean up all the allocated
   * memory for this.  You need to check each field be for you
   * use it, if the field is NULL then it was not found in the
   * path.  Normally this can be Drive (for windows), FileName,
   * File and Ext.
   *
   *   FullPath
   *     Is the full path that was processed.  This is
   *     what you passed into SplitPath.  See SplitPath
   *     for how this can be changed by SplitPath.
   *   Drive
   *     If windows and drive is found will contain the
   *     drive letter and the ':'.
   *   Path
   *     If a path is found will contain the path.  This
   *     could be NULL if only a file name was passed in
   *     with no path.
   *   FileName
   *     Is the filename with the ext.  This can be NULL
   *     if no filename was found.  This only happend if
   *     the last character in the path you passed in is
   *     a file seperator.
   *   File
   *     Is the filename without the ext.  This can be NULL.
   *     See FileName for details on why.
   *   Ext
   *     Is the files ext without the '.'. This can be NULL
   *     because of two reasons.  One, see FileName.  The
   *     other is did not find an ext from FileName.
   */
typedef struct {
  char *FullPath;
#if defined(_MSC_VER)
  char *Drive;
#endif
  char *Path;
  char *FileName;
  char *File;
  char *Ext;
} PathDef;

  /* Splits a path up into all its components.  See PathDef
   * for details.  For deleting all the allocated memory see
   * SplitPathClean.
   *
   *   <PathDef> SplitPath(<Path>, <Qualify>);
   *
   *     <PathDef>
   *       Return of the typedef PathDef.  This is a pointer
   *       and you need to manage the memory allocated.
   *     <Path>
   *       Is the path to split into its components.  Make sure
   *       you have all the leading spaces and trailing spaces
   *       removed.  That will cause issues.
   *     <Qualify>
   *       If true will call RealPath for you and this will
   *       be stored in FullPath not what you passed in.
   */
extern PathDef *SplitPath(const char* _path, bool _qualify);

  /* Used to clean up the PathDef that was created by SplitPath.
   * This makes it real easy to free all the memory used in
   * PathDef and also to delete the PathDef.  It returns a NULL
   * that you can us to set your variable of PathDef to NULL in
   * one statement.
   *
   *   <RPathDef> SplitPathClean(<PathDef>);
   *
   *     <RPathDef>
   *       Returns NULL pointer for you.
   *     <PathDef>
   *       Is the PathDef to clean up.
   */
extern PathDef *SplitPathClean(PathDef *_pathInfo);

  /* Used to get a list of directors and files from a directory.
   * It returns a DListDef.  Remember you must manage this.  Use
   * the FileDListDeleter function when you are working with the
   * DList.  For more details on how DLists work see the DList
   * header file.
   */
extern DListDef *ListFromDir(const char *_path, bool(*_storeFile)(const char *));
extern void FileDListDeleter(void *_userData);

  /* Used to remove a directory.  If the directory is removed the string returned is
   * NULL else its a string that contains the error message one what failed.  You
   * must manage the returned string.
   */
extern char *RemoveDir(const char *_fileName);

  /* Used to see if FILE is atty. */
extern bool IsAtty(FILE *Fh);

  /* Used to create a directory.  If the diretory was created it will
   * return a true else false.
   */
extern bool CreateDir(const char *_fileName);

#ifdef __cplusplus
}
#endif
