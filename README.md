# FileScript Interpreter

## Overview

FileScript is a simple custom scripting language interpreter written in Python and packaged as a standalone executable.

It supports variables, file operations, conditionals, and basic input/output.

FileScript is being developed as an idea for the more convenient language for working with files, focusing on simplicity, readability, and fast scripting for file-based tasks.

---

## How to run

### Run a script file

```bash
FileScript.exe script.filesc
```

or

```bash
./FileScript.exe script.filesc
```

---

### Interactive mode (REPL)

If you run the program without arguments:

```bash
FileScript.exe
```

You can type commands directly:

```
> var x 10
> println x
```

---

## File format

Only `.filesc` files are supported.

Example:
```
script.filesc
```

---

## Features

### Variables

```
var name value
println name
```

---

### Input

```
input name
```

Stores user input into a variable.

---

### Conditionals

```
if a b
...
endif
```

Compares variable `a` with string `b`.  
If the condition is false, the block is skipped.

---

### File operations

**Read file**
```
open file.txt varname
```

**Write file (overwrite)**
```
write file.txt text
```

**Append to file**
```
add file.txt text
```

**Create file**
```
create file file.txt content
```

**Create directory**
```
create dir dirname
```

**Remove file or directory**
```
remove path
```

---

## Errors

- `SyntaxError` — invalid command usage  
- `FileNotFoundError` — file not found  
- `FileExistsError` — file already exists  
- `PermissionError` — access denied  
- `NameError` — unknown command  

---

## Build

If built using PyInstaller:

```bash
pyinstaller --onefile your_script.py
```

Output:
```
dist/filescript.exe
```

---

## Notes

- No external dependencies required at runtime
- Variables are stored in memory only
- All values are treated as strings
- No functions or loops yet
- Designed as an educational scripting language focused on file operations and simplicity
```
