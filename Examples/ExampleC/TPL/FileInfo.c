/*@@CopyFile@@*/
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

#include <sys/stat.h> 
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#if defined(_MSC_VER)
#include <windows.h>
#include <direct.h>
#include <io.h>
#define getcwd _getcwd
#define PATH_MAX _MAX_PATH
#define FILESEP '\\'
#elif defined(__GNUC__)
#include <limits.h> 
#include <unistd.h>
#define FILESEP '/'
#endif

#include "String.h"
#include "DList.h"
#include "FileInfo.h"

bool FileExist(const char *_path) {
  struct stat Stats;

  return (stat(_path, &Stats) == 0);
}

bool IsDir(const char *_path)
{
  struct stat Stats;

  if (stat(_path, &Stats) == 0 && Stats.st_mode & S_IFDIR) return true;
  return false;
}

bool IsFile(const char *_path)
{
  struct stat Stats;

  if (stat(_path, &Stats) == 0 && Stats.st_mode & S_IFREG) return true;
  return false;
}

char *CurDir(void) {
  char *Path;

  if ((Path = getcwd(NULL, 0)) == NULL) {
    return NULL;
  }
  return Path;
}

char *RealPath(const char *_path) {
  char buf[PATH_MAX];

#if defined(_MSC_VER)
  if (_fullpath(buf, _path, PATH_MAX) == NULL) return NULL;
#elif defined(__GNUC__)
  if (realpath(_path, buf) == NULL) return NULL;
#endif

  size_t fullLength = strlen(buf);
  char *ThePath = malloc(fullLength + 1);
  memcpy(ThePath, buf, fullLength + 1);
  return ThePath;
}

char *JoinPath(const char *_path, const char *_path1)
{
  if (_path[strlen(_path) - 1] == FILESEP) {
    if (_path[0] == '\0' || _path1[0] != FILESEP) return StringBuild(NULL, 2, _path, _path1);
    return StringBuild(NULL, 1, _path);
  } else {
    if (_path[0] == '\0' && _path1[0] == FILESEP) return StringBuild(NULL, 1, _path1);
    else if (_path1[0] == FILESEP) return StringBuild(NULL, 1, _path);
  }

  char FileSep[2];
  FileSep[0] = FILESEP;
  FileSep[1] = '\0';
  return StringBuild(NULL, 3, _path, FileSep, _path1);
}

PathDef *SplitPath(const char* _path, bool _qualify)
{
  char Buf[PATH_MAX];
  size_t BufLen = 0;
  size_t Indx = 0;
  char *Path;
  size_t PathLen;
  PathDef *PathInfo = malloc(sizeof(PathDef));

  if (_qualify == true) {
    PathInfo->FullPath = RealPath(_path);
    if (PathInfo->FullPath == NULL) {
      free(PathInfo);
      return NULL;
    }
    PathLen = strlen(PathInfo->FullPath);
  } else {
    PathLen = strlen(_path);
    PathInfo->FullPath = malloc(PathLen + 1);
    memcpy(PathInfo->FullPath, _path, PathLen + 1);
  }
  Path = PathInfo->FullPath;

  PathInfo->Path = NULL;
  PathInfo->FileName = NULL;
  PathInfo->File = NULL;
  PathInfo->Ext = NULL;

#if defined(_MSC_VER)
  PathInfo->Drive = NULL;
  if (PathLen > 1 && Path[1] == ':') {
    PathInfo->Drive = malloc(3);
    PathInfo->Drive[0] = Path[0];
    PathInfo->Drive[1] = Path[1];
    PathInfo->Drive[2] = '\0';
    Indx = 2;
  }
#endif

    // No filename.
  if (Path[PathLen - 1] == FILESEP) {
    PathInfo->Path = malloc((PathLen - Indx) + 1);
    memcpy(PathInfo->Path, &Path[Indx], (PathLen - Indx) + 1);
  } else while (Indx < PathLen) {
    size_t StartIndx = Indx;
    size_t FileSepIndx = FindChar(&Path[Indx], FILESEP);
    if (FileSepIndx != -1) {
      Indx += FileSepIndx + 1;
      memcpy(&Buf[BufLen], &Path[StartIndx], Indx - StartIndx);
      BufLen += Indx - StartIndx;
    } else {
      PathInfo->FileName = malloc((PathLen - Indx) + 1);
      memcpy(PathInfo->FileName, &Path[Indx], (PathLen - Indx) + 1);
      break;
    }
  }

  if (BufLen != 0) {
    PathInfo->Path = malloc(BufLen + 1);
    memcpy(PathInfo->Path, Buf, BufLen);
    PathInfo->Path[BufLen] = '\0';
  }

  if (PathInfo->FileName != NULL) {
    size_t LenFileName = strlen(PathInfo->FileName);
    size_t FileExtIndx = FindChar(PathInfo->FileName, '.');
    if (FileExtIndx != -1) {
      size_t LenExt = strlen(&PathInfo->FileName[FileExtIndx + 1]);

      PathInfo->File = malloc(LenFileName - LenExt);
      memcpy(PathInfo->File, PathInfo->FileName, (LenFileName - LenExt));
      PathInfo->File[(LenFileName - LenExt) -1] = '\0';

      PathInfo->Ext = malloc(LenExt + 1);
      memcpy(PathInfo->Ext, &PathInfo->FileName[FileExtIndx + 1], 
             LenExt);
      PathInfo->Ext[LenExt] = '\0';
    } else {
      PathInfo->File = malloc(LenFileName + 1);
      memcpy(PathInfo->File, PathInfo->FileName, LenFileName + 1);
    }
  }
  return PathInfo;
}

PathDef *SplitPathClean(PathDef *_pathInfo) {
  if (_pathInfo != NULL) {
#if defined(_MSC_VER)
    if (_pathInfo->Drive != NULL) free(_pathInfo->Drive);
#endif
    if (_pathInfo->FullPath != NULL) free(_pathInfo->FullPath);
    if (_pathInfo->Path != NULL) free(_pathInfo->Path);
    if (_pathInfo->FileName != NULL) free(_pathInfo->FileName);
    if (_pathInfo->File != NULL) free(_pathInfo->File);
    if (_pathInfo->Ext != NULL) free(_pathInfo->Ext);
    free(_pathInfo);
  }
  return NULL;
}

#if defined(_MSC_VER)
char *RemoveDir(const char *_fileName) {
  char *Msg = NULL;

  if (!RemoveDirectoryA(_fileName)) {
    char pBuffer[2048];
    DWORD dwErrorCode = GetLastError();

    DWORD cchMsg = FormatMessageA(FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
                                  NULL,  /* (not used with FORMAT_MESSAGE_FROM_SYSTEM) */
                                  dwErrorCode,
                                  MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
                                  pBuffer,
                                  2048,
                                  NULL);
   Msg = StringBuild(NULL, 1, pBuffer);
  }
  return Msg;
}
#elif defined(__GNUC__)
#endif

#if defined(_MSC_VER)
bool IsAtty(FILE *Fh)
{
  if (!_isatty(_fileno(Fh))) {
    return false;
  }
  return true;
}
#elif defined(__GNUC__)
bool IsAtty(FILE *Fh)
{
  if (!isatty(Fh)) {
    return false;
  }
  return true;
}
#endif

#if defined(_MSC_VER)
DListDef *ListFromDir(const char *_path, bool(*_storeFile)(const char *))
{
  WIN32_FIND_DATAA ffd;
  HANDLE hFind = INVALID_HANDLE_VALUE;
  DWORD dwError = 0;
  char *Dir = JoinPath(_path, "*");
  char *Msg = NULL;
  DListDef *DList = InitDList(DLIST_FIFO);

  hFind = FindFirstFileA(Dir, &ffd);
  dwError = GetLastError();
  if (dwError == ERROR_SUCCESS) {
    do {
      char *FileName = JoinPath(_path, ffd.cFileName);

      if (_storeFile == NULL || (*_storeFile)(FileName)) {
        PushDList(DList, FileName);
      } else free(FileName);

    } while (FindNextFileA(hFind, &ffd) != 0);
  }
  dwError = GetLastError();
  if (dwError != ERROR_NO_MORE_FILES) {
    DList = DropDList(DList, FileDListDeleter);
  }
  if (DList->Cnt == 0) {
    DList = DropDList(DList, FileDListDeleter);
  }

  FindClose(hFind);
  free(Dir);

  return DList;
}

#elif defined(__GNUC__)
DListDef *ListFilesFromDir(const char *_path, void(*_UserItemDel)(void *))
{
  return NULL;
}
#endif

void FileDListDeleter(void *_userData) {
  if (_userData != NULL) free(_userData);
}

#if defined(_MSC_VER)
bool CreateDir(const char *_fileName)
{
  return CreateDirectoryA(_fileName, NULL);
}
#elif defined(__GNUC__)
bool CreateDir(const char *_fileName)
{
  return false;
}
#endif
