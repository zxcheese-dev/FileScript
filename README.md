<img width="200" height="200" alt="FileScript" src="https://github.com/user-attachments/assets/42b5cefe-0907-4132-a599-ee83d5b7c565" />
***FileScript interpreter***

*Simple FileScript programming language for more convenient work with files and the system*

*In last update you can do... absolutely nothing (added* ```pass```*)*

*Example:*

```go
var text "hello"

if text == "hello"
  // doing absolutely nothing
  pass
endif
```

(*Fixed stack* ```skip```)

*Now FileScript has function* ```?exist``` *making FileScript more comfortable for file operations*

*Example:*

```go
var file_exist ?exist "file.txt"
println file_exist
```

*Also* ```println``` *now can print result of returnable functions and also it has comments* ```//```

*Example:*

```go
// counting 1 + 1
println count 1 + 1

// outputs existence of text.txt (True/False)
println ?exist "text.txt"
```

*FileScript instruction* ```input``` *now updated and can output text before input*

```go
// just input
input text

// input with text
input "type here your text: " text
```
