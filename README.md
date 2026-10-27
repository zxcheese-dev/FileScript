**FileScript interpreter**

<img width="200" height="200" alt="FileScript" src="https://github.com/user-attachments/assets/42b5cefe-0907-4132-a599-ee83d5b7c565" />

*FileScript is a simple programming language for more convenient work with files and the system*

*In the last update added new function* ```OpenLink``` *that can open links in your webbrowser*

*Added new function* ```always``` *it can ignore the skip stack for one command even if the last element of stack is False*

*Also in the latest update ```always``` is now not one function, this is block of code with ending* ```enough```

*Example:*

```go
always println

var msg "hello"
if msg == "hi"
    // we marked println with always so println executes even inside a false if block
    println msg
endif

// enough means println will no longer ignore false if block
enough println
```

*Finally, FileScript almost can support Linux in file ```FileScript-for-Linux.py```, edited commands* ```root``` ```AutoReg``` ```reboot``` *and* ```run``` *and edited winreg import (but unfortunatelly Linux support now need fix for more convenient work with linux)*

*FileScript instruction* ```input``` *now updated and can output text before input*

```go
// just input
input text

// input with text
input "type here your text: " text
```

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

Copyright © 2026 zxcheese-dev
