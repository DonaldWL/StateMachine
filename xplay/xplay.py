import sys

from PythonLib.Help import (CHelp, TagInfoDef, TagTypes)

Tags = {'TAG1': TagInfoDef(TagTypes.SINGLEWORD, "Fun fun fun"),
        'TAG1x': TagInfoDef(TagTypes.SINGLEWORD, ("Fun", "In", "The",  "Sun")),
        'TAG2': TagInfoDef(TagTypes.SENTENCE, ("Fun", "In", "The", "Sun")),
        'TAG2x': TagInfoDef(TagTypes.SENTENCE, "Fun In The Sun"),
        'TAG3': TagInfoDef(TagTypes.PARAGRAPH, "Fun In The Sun"),
        'TAG3x': TagInfoDef(TagTypes.PARAGRAPH, ("Fun are the days", "In the life", "The day is short", "Sun is bright"))}

Help = CHelp(HelpDirs = './HelpFiles', TopicSeperatorLine = None,
             PreTopic = None, PostTopic = None, TopicIndent = 0,
             OutFile = sys.stdout, Tags = Tags)

Help.Process(['-h'])
