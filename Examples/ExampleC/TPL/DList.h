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

  /* Used to create the DList.  The DListDef that is returned
   * must be managed by you.  See DropDList, it will delete all
   * the memory.  You need to select the Type, see DListTypeDef.
   * Based on the type will determine how items are push onto
   * the dlist.
   */
extern DListDef *InitDList(DListTypeDef _type);

  /* Used to drop the dlist.  It will delete all the memory it
   * has allocated.  To remove your memory you need to pass in
   * a method that will be called to free your user data.  If
   * you pass in NULL then it will not attempt to free your memory
   * just the nodes it created.
   *
   *   void _UserItemDel(void *_UserData)
   *     _UserData is the memory you passed into DList when you
   *     created the node.
   */
extern DListDef *DropDList(DListDef *_dList, void(*_UserItemDel)(void *));

  /* These two functions will drop a node.  the DropNode, validates that the
   * Node is in the DList, the DropNodeNoCheck does not validate it, its
   * faster as long as you are managing what you are doing.  Each function
   * is like DropDList, you can pass in the function that will delete your
   * user data.
   */
extern DListNodeDef *DropNode(DListDef *_dList, DListNodeDef *_node, void(*_UserItemDel)(void *));
extern DListNodeDef *DropNodeNoCheck(DListDef *_dList, DListNodeDef *_node, void(*_UserItemDel)(void *));

  /* Pops the first item of the top of the dlist and returns your user data.
   * If no more items return NULL.
   */
extern inline void *PopDList(DListDef *_dList);

  /* Pops from the bottom of the dlist.  One returns just the user data and
   * the other returns the node.  Keep in mind the node was allocated using
   * malloc.  So if you pop the node then you must manage that memory.
   */
extern inline void *PopDListBottom(DListDef *_dList);
extern DListNodeDef *PopDListBottomNode(DListDef *_dList);

  /* Pops from the top of the Dlist, just like PopDList.  This is just like
   * POpDListBottom and PopDListBottomNode.  You need to manage the node
   * data if you pop the node.
   */
extern inline void *PopDListTop(DListDef *_dList);
extern DListNodeDef *PopDListTopNode(DListDef *_dList);

  /* These functions allow you to push your user data onto the dlist.
   * PushDList may push to the top or bottom based on the type that
   * you selected when you created the dlist, see DListTypeDef.  If
   * you wish to control the push then select the top or bottom
   * function.
   */
extern inline DListNodeDef *PushDList(DListDef *_dList, void *_userData);
extern DListNodeDef *PushDListBottom(DListDef *_dList, void *_userData);
extern DListNodeDef *PushDListTop(DListDef *_dList, void *_userData);

  /* Reads the items from the dlist.  The first time it is called
   * it returns the first item, then the next... when it has finished
   * the dlist it return NULL.  If you modify the dlist during this
   * time it gets reset to the top.
   */
extern inline void *ReadDList(DListDef *_dList);
extern struct DListNode *ReadDListNode(DListDef *_dList);

#ifdef __cplusplus
}
#endif
