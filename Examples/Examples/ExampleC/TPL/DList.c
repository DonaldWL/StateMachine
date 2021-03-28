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

  Double linked list
-----------------------------------------------------------------------------
*/
#include <stdlib.h>

#include "DList.h"

DListDef *InitDList(DListTypeDef _type)
{
  DListDef *DList = malloc(sizeof(DListDef));

  DList->Type = _type;
  DList->Cnt = 0;
  DList->FirstNode = NULL;
  DList->CurNode = NULL;

  return DList;
}

DListDef *DropDList(DListDef *_dList, void (*_UserItemDel)(void *))
{
  if (_dList != NULL) {
    while (_dList->Cnt) {
      if (_UserItemDel != NULL) (*_UserItemDel)(_dList->FirstNode->UserData);
      PopDListTop(_dList);
    }
    free(_dList);
  }

  return NULL;
}

DListNodeDef *DropNodeNoCheck(DListDef *_dList, DListNodeDef *_node, void(*_UserItemDel)(void *))
{
  DListNodeDef *SavedNode;

  if (_UserItemDel != NULL) (*_UserItemDel)(_node->UserData);

  // Lets delete it.
  if (_node == _dList->FirstNode) {
    PopDListTopNode(_dList);
  } else {
    SavedNode = _dList->FirstNode;
    _dList->FirstNode = _node;
    PopDListTopNode(_dList);
    _dList->FirstNode = SavedNode;
  }
  _node->Prev = _node->Next = NULL;
  return NULL;
}

DListNodeDef *DropNode(DListDef *_dList, DListNodeDef *_node, void(*_UserItemDel)(void *))
{
  DListNodeDef *SavedNode;
  DListNodeDef *Node = NULL;

  if (_node != NULL) {
    if (_dList->Cnt == 0) return _node;

      // Make sure the passed in node is in _dList;
    SavedNode = _dList->CurNode;
    _dList->CurNode = NULL;
    while ((Node = ReadDListNode(_dList)) != NULL) {
      if (Node == _node) break;
    }
    _dList->CurNode = SavedNode;
    if (Node == NULL) return _node;

    Node = DropNode(_dList, _node, _UserItemDel);
    
  }
  return Node;
}

inline void *PopDList(DListDef *_dList) 
{ 
  return PopDListTop(_dList); 
}

inline void *PopDListBottom(DListDef *_dList)
{
  DListNodeDef *Node;
  void *UserData = NULL;

  Node = PopDListBottomNode(_dList);
  if (Node != NULL) {
    UserData = Node->UserData;
    free(Node);
  }
  return UserData;
}

DListNodeDef *PopDListBottomNode(DListDef *_dList)
{
  DListNodeDef *LastNode = NULL;

  if (_dList->Cnt) {
    LastNode = _dList->FirstNode->Prev;
    if (_dList->Cnt == 1) {
      _dList->Cnt = 0;
      _dList->FirstNode = NULL;
      _dList->CurNode = NULL;
    } else {
      LastNode->Prev->Next = LastNode->Next;
      LastNode->Next->Prev = LastNode->Prev;
      _dList->Cnt--;

      if (_dList->CurNode == LastNode) {
        _dList->CurNode = NULL;
      }
    }
    LastNode->Prev = LastNode->Next = NULL;
  }

  return LastNode;
}

inline void *PopDListTop(DListDef *_dList)
{
  DListNodeDef *Node;
  void *UserData = NULL;

  Node = PopDListTopNode(_dList);
  if (Node != NULL) {
    UserData = Node->UserData;
    free(Node);
  }
  return UserData;
}

DListNodeDef *PopDListTopNode(DListDef *_dList)
{
  DListNodeDef *FirstNode = NULL;

  if (_dList->Cnt) {
    FirstNode = _dList->FirstNode;
    if (_dList->Cnt == 1) {
      _dList->Cnt = 0;
      _dList->FirstNode = NULL;
      _dList->CurNode = NULL;
    } else {
      _dList->FirstNode = FirstNode->Next;
      FirstNode->Prev->Next = FirstNode->Next;
      FirstNode->Next->Prev = FirstNode->Prev;
      _dList->Cnt--;
      if (_dList->CurNode == FirstNode) {
        _dList->CurNode = NULL;
      }
    }
    FirstNode->Prev = FirstNode->Next = NULL;
  }

  return FirstNode;
}

inline DListNodeDef *PushDList(DListDef *_dList, void *_userData)
{
  if (_dList->Type == DLIST_FIFO) return PushDListBottom(_dList, _userData);
  else return PushDListTop(_dList, _userData);
}

DListNodeDef *PushDListBottom(DListDef *_dList, void *_userData)
{
  DListNodeDef *NewNode = (DListNodeDef *) malloc(sizeof(DListNodeDef));

  if (_dList->Cnt == 0) {
    NewNode->Prev = NewNode;
    NewNode->Next = NewNode;
    _dList->FirstNode = NewNode;
  } else {
    NewNode->Prev = _dList->FirstNode->Prev;
    NewNode->Next = _dList->FirstNode;
    NewNode->Prev->Next = NewNode;
    _dList->FirstNode->Prev = NewNode;
  }
  NewNode->UserData = _userData;
  _dList->Cnt++;
  return NewNode;
}

DListNodeDef *PushDListTop(DListDef *_dList, void *_userData)
{
  DListNodeDef *NewNode = (DListNodeDef *) malloc(sizeof(DListNodeDef));

  if (_dList->Cnt == 0) {
    NewNode->Prev = NewNode;
    NewNode->Next = NewNode;
    _dList->FirstNode = NewNode;
  } else {
    NewNode->Prev = _dList->FirstNode->Prev;
    NewNode->Next = _dList->FirstNode;
    _dList->FirstNode->Prev = NewNode;
    NewNode->Prev->Next = NewNode;
    _dList->FirstNode = NewNode;
  }
  NewNode->UserData = _userData;
  _dList->Cnt++;
  return NewNode;
}

inline void *ReadDList(DListDef *_dList)
{
  DListNodeDef *Node = ReadDListNode(_dList);

  if (Node == NULL) return NULL;
  return Node->UserData;
}

DListNodeDef *ReadDListNode(DListDef *_dList)
{
  DListNodeDef *Node = NULL;

  if (_dList->Cnt != 0) {
    if (_dList->CurNode == NULL) {
      _dList->CurNode = _dList->FirstNode;
      Node = _dList->CurNode;
    } else {
      if (_dList->CurNode->Next != _dList->FirstNode) {
        Node = _dList->CurNode->Next;
        _dList->CurNode = Node;
      } else {
        _dList->CurNode = NULL;
      }
    }
  }

  return Node;
}
