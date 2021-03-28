# StateMachine

  State Machine generator with a program to generate you state machine
  and examples in C, CPP, and Python.  Look at all the help files in
  'HelpFiles'.
 
  The program that can be used to generate the state machines for the
  examples is 'Gen.py'.  It also has the ability to display all the
  help files under 'HelpFiles'.

## Required Libraries

  You will need the repository that contains PythonLib.  You can find
  this at https://github.com/DonaldWL/PythonLib

## Packages And Files

  The StateMachine library contains a few packages and examples and 
  support files.  You should review all these files before you use
  this system.
 
  You will find a lot of text files under 'HelpFiles'  You should
  review these to understand how to use this packages.

## Contact (Questions, Issues or Recommendations)  
  If you have any questions, issues or recommendations feel free to send
  me an email at 'Donald.W.Long@gmail.com'.  I review my email every few
  days.
  
  I created this really as an example on how to create a simple state
  machine, but decided to create a way to do generate some of the tables
  and the like, to make it easer.
  
  I have used state machine in the past for doing communication protocols
  for Excel Exchange.  I also created a simple generate for the tables.  This
  one is a bit more and is in 'Python'.  It does not generate your code, you
  have to write that.  I did play with this a bit and removed it.
  
## General Layout

  You have two main packages that make up the generator for the state machine.
  'SMS' and "Generator'.  The 'SMS' package processes what is called the 'sms'
  file.  This file is used to define your state machine.  The 'SMS' does not
  generate anything.  It just creates all the data you need to generate your
  state machine.  The 'Generator' package is used to take the results of 'SMS'
  and generate the code that you need for your state machine.  It requires
  templates. 
  
  You will find a directory called 'Templates'.  This contains templates for 
  a few languages.  Currently C, CPP, CSharp, Java, and Python are supported.
  
  You will also find a directory called 'Examples'.  Each language has examples
  for you.  Under the 'Examples' directory you will find a program called 
  'BuildExamples.py'.  Run this and it will create a directory called 'Results'
  under the 'Examples' directory of all the examples that have been ran thru
  'Gen.py'.
  
  In the root directory of 'StateMachine' you will find a program called 'Gen.py'.
  It can be used to take your templates and generate your state machine skeleton.
  
  Remember to read all the text files under 'HelpFiles'.  This will help you 
  understand how to use this beast.
  
  Have fun.  This is a good way to learn state machines without having to build
  your own tables.  You should still learn how these tables work and how the code
  accesses the tables.  All the languages are the same except 'Python'.  So if you
  learn how the table work for C you also understand how the work for CPP, Java,
  and CSharp.
   
## TODO

  I have not completed the Linux side of the examples.  I currently do
  not have access to a Linux machine.  Thus, the C and CPP examples have
  not been compiled under Linux.  The basic state machine should not have
  an issue, but some of the other files to support the user side of the
  state machine need to be coded up and tested.
  
  If you have a Linux machine feel free to finish this.  I have retired and
  I am living in an RV and only have my laptop, that is running Windows.  Thus,
  no Linux box.
  