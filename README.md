StateMachine

  State Machine generator with a program to generate you state machine
  and examples in C, CPP, and Python.  Look at all the help files in
  'HelpFiles'.
 
  The program that can be used to generate the state machines for the
  examples is 'Gen.py'.  It also has the ability to display all the
  help files under 'HelpFiles'.

Required Libraries

  You will need the repository that contains PythonLib.  You can find
  this at https://github.com/DonaldWL/PythonLib

TODO

  I have not completed the Linux side of the examples.  I currently do
  not have access to a Linux machine.  Thus, the C and CPP examples have
  not been compiled under Linux.  The basic state machine should not have
  an issue, but some of the other files to support the user side of the
  state machine need to be coded up and tested.

Packages And Files

  The StateMachine library contains a few packages and examples and 
  support files.  You should review all these files before you use
  this system.
  
Examples

  Contains all the examples for C, CPP, and Python.  See the help files.
    
    HelpFiles
      Example.help
      ExampleC.help
      ExampleCPP.help
      ExamplePython.help

Generator

  This package is used to generate the state machine from your TPL files.  See the help files.
    
    HelpFiles
      Generotr.help

HelpFiles

  This directory contains all the help files.  This is based on 'PythonLib.Help'.

PythonBase

  This package is used to create python based state machines.  See the help files
    
    HelpFiles
       PythonBase.help

SMS

  This package is used to process your SMS file.  The SMS file is used to define your 
  state machine.  See the help files
  
    HelpFiles
      SMS.help

Gen.py

  This is a program that can be used to generate your state machine using your SMS
  files and your TPL files.  Instead of reading the help files you can use the program
  with the '-h' command to get help on the sytnax of the command line and on all its
  topics.
