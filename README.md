***FileScript interpreter***

*Simple FileScript programming language for more convenient work with files and the system*

*Now FileScript has function ```?exist``` making FileScript more comfortable for file operations*

*Example:*

```go
var file_exist ?exist "file.txt"
println file_exist
```

*Also ```println``` can print result of returnable functions and also it has comments ```//```*

*Example:*

```go
// counting 1 + 1
println count 1 + 1

// outputs existence of text.txt (True/False)
println ?exist "text.txt"
```
