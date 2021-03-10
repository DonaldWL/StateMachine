//@@C@@
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

  Double Linked list
-----------------------------------------------------------------------------
*/
#pragma once

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {DLIST_FIFO, DLIST_LIFO} DListTypeDef;

typedef struct DListNode {
  struct DListNode *Prev;
  struct DListNode *Next;
  void *UserData;
} DListNodeDef;

typedef struct {
  DListTypeDef Type;
  int Cnt;
  DListNodeDef *CurNode;
  DListNodeDef *FirstNode;
} DListDef;

extern DListDef *InitDList(DListTypeDef _type);

extern DListDef *DropDList(DListDef *_dList, void(*_UserItemDel)(void *));

extern DListNodeDef *DropNode(DListDef *_dList, DListNodeDef *_node, void(*_UserItemDel)(void *));
extern DListNodeDef *DropNodeNoCheck(DListDef *_dList, DListNodeDef *_node, void(*_UserItemDel)(void *));

extern inline void *PopDList(DListDef *_dList);

extern inline void *PopDListBottom(DListDef *_dList);
extern DListNodeDef *PopDListBottomNode(DListDef *_dList);

extern inline void *PopDListTop(DListDef *_dList);
extern DListNodeDef *PopDListTopNode(DListDef *_dList);

extern inline DListNodeDef *PushDList(DListDef *_dList, void *_userData);
extern DListNodeDef *PushDListBottom(DListDef *_dList, void *_userData);
extern DListNodeDef *PushDListTop(DListDef *_dList, void *_userData);

extern inline void *ReadDList(DListDef *_dList);
extern struct DListNode *ReadDListNode(DListDef *_dList);

#ifdef __cplusplus
}
#endif
