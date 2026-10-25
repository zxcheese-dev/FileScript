**FileScript interpreter**

<img width="200" height="200" alt="FileScript" src="https://github.com/user-attachments/assets/42b5cefe-0907-4132-a599-ee83d5b7c565" />

*FileScript is a simple programming language for more convenient work with files and the system*

*Added new function* ```always``` *it can ignore the skip stack for one command even if last element of stack is False*

*Also in latest update ```always``` is now not 1 function, this is block of code with ending* ```enough```

*Example:*

```go
always println

var msg "hello"
if msg == "hi"
    // we marked println with always so println ignores false if/endif
    println msg
endif

// enough means println will not ignore false if/endif
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
