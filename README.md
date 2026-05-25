# FileScript Interpreter

## Overview

FileScript is a custom scripting language interpreter written in Python and packaged as a standalone executable.

It is designed as a simple but expanding language focused on **file operations**, **variable handling**, and **basic scripting logic**.

The main idea of FileScript is to evolve into a **convenient and minimal language for working with files**, making file automation as simple and readable as possible.

---

## How to run

### Run executable with a script

```bash
filescript.exe script.filesc
```

or

```bash
./filescript.exe script.filesc
```

---

### Interactive mode (REPL)

If no file is provided:

```bash
filescript.exe
```

You can type commands directly:

```
> var name "Hello"
> println name
```

---

## File format

Only `.filesc` files are supported.

Example:

```
script.filesc
```

---

## Language features

### Variables

```text
var name "Hello"
var name2 name
println name2
```

- Supports string values
- Supports variable-to-variable assignment
- Unknown variables cause `NameError`

---

### Output

```text
println value
```

Prints either:
- variable value (if exists)
- raw string otherwise

---

### Input

```text
input name
```

Stores user input into a variable.

---

### Conditionals

```text
if a == b
if a != b
...
endif
```

- Supports `==` and `!=`
- Compares variables or string literals
- Strict mode: undefined names raise errors

---

### File operations

#### Open file

```text
open path varname
```

Reads file content into a variable.

Supports:
- string path
- variable path

---

#### Write file

```text
write path content
```

Overwrites file content.

---

#### Append to file

```text
add path content
```

Appends data to file.

---

#### Create

```text
create file filename content
create dir dirname
```

---

#### Remove

```text
remove path
```

Deletes file or directory.

Supports:
- string paths
- variables containing paths

---

### Directory listing

```text
ls path
ls path file
ls path dir
```

Modes:
- default → shows `[DIR]` and `[FILE]`
- `file` → only files
- `dir` → only directories

Supports:
- string paths
- variable paths

---

## Errors

- `SyntaxError` — invalid command usage  
- `NameError` — unknown variable or command  
- `FileNotFoundError` — missing file  
- `FileExistsError` — file already exists  
- `PermissionError` — access denied  
- `IndexError` — invalid argument usage  
- `EndswithError` — invalid file extension  

---

## Build

If using PyInstaller:

```bash
pyinstaller --onefile your_script.py
```

Output:

```
dist/filescript.exe
```

---

## Notes

- Everything is string-based (no types yet)
- Variables can reference other variables
- Strict undefined-variable behavior
- Designed for file automation and scripting
- Actively evolving language
```
