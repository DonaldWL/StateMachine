import sys

from PythonLib.Help import (CHelp, TagInfoDef, TagTypes)
from StateMachine.SMS import LanguagesSupported

HelpFiles = './HelpFiles'

Tags = {'xTAG1': TagInfoDef(TagTypes.SINGLEWORD, "xFun fun fun"),
        'xTAG1x': TagInfoDef(TagTypes.SINGLEWORD, ("xFun", "In", "The",  "Sun")),
        'xTAG2': TagInfoDef(TagTypes.SENTENCE, ("xFun", "In", "The", "Sun")),
        'xTAG2x': TagInfoDef(TagTypes.SENTENCE, "xFun In The Sun"),
        'xTAG3': TagInfoDef(TagTypes.PARAGRAPH, "xFun In The Sun"),
        'xTAG3x': TagInfoDef(TagTypes.PARAGRAPH, ("xFun are the days", "In the life", "The day is short", "Sun is bright")),
        'LANGUAGE': TagInfoDef(TagTypes.SINGLEWORD, ', '.join(LanguagesSupported)),
        'LANGUAGELIST': TagInfoDef(TagTypes.PARAGRAPH, LanguagesSupported)}        
        
Help = CHelp(HelpDirs = HelpFiles, TopicSeperatorLine = None,
             PreTopic = None, PostTopic = None, TopicIndent = 0,
             OutFile = sys.stdout, Tags = Tags)
             
Help.Process(['Example'])
