set PYTHONPATH=..\

Gen.py .\Examples\Example.sms .\Examples\ExampleC\TPL .\Examples\ExampleC\STM Language C SMSReport Gen OverWrite

Gen.py .\Examples\Example.sms .\Examples\ExampleCPP\TPL .\Examples\ExampleCPP\STM Language CPP SMSReport Gen OverWrite

Gen.py .\Examples\Example.sms .\Examples\ExamplePython\TPL .\Examples\ExamplePython\STM Language Python SMSReport Gen OverWrite

Gen.py .\Examples\Example.sms .\Examples\ExampleCSharp\TPL .\Examples\ExampleCSharp\STM Language CSharp SMSReport Gen OverWrite

Gen.py .\Examples\Example.sms .\Examples\ExampleJava\TPL .\Examples\ExampleJava\STM Language Java SMSReport Gen OverWrite

xcopy .\Examples\ExampleCSharp\STM\* ..\Examples\ExampleCSharp /q /Y

xcopy .\Examples\ExampleJava\STM\* ..\JavaExample /q /Y
