**FileScript interpreter**

<img width="200" height="200" alt="FileScript" src="https://github.com/user-attachments/assets/42b5cefe-0907-4132-a599-ee83d5b7c565" />

*FileScript is a simple programming language for more convenient work with files and the system*

*In last update you can do... absolutely nothing (added* ```pass```*)*

*Example:*

```go
var text "hello"

if text == "hello"
  // doing absolutely nothing
  pass
endif
```

*Finally, FileScript almost can support Linux in file '''FileScript-for-Linux.py''', edited commands* '''root''' '''AutoReg''' '''reboot''' *and* '''run''' *and edited winreg import (but unfortunatelly Linux support now needs fix for more convenient work with operating system)*

*FileScript now can return errors with* ```error``` *function*

*Example:*

```go
error SyntaxError "invalid syntax"
```

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
