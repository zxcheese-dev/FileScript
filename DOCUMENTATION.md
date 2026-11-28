# FileScript interpreter Documentation
###### 27 November 2026.

*FileScript - is a scripting language for more convenient work with files and operating system*

*FileScript has really simple syntax and simple understandable commands*

# Output
*Output in FileScript has specific syntax that needs ```variable definition and output```*

```
var msg "hello world"
println msg
```
*In this example used 2 commands: var and println, here is they syntax:*

```var <name> <value>```

```println <variable>```

**IMPORTANT**
*println doesn't allow to outputting a value directly like ```println "hello world"```*

# Types of data
*FileScript has 4 types of data: ```int``` (integer), ```float```, ```string```, ```bool```*

*Also you can use same name functions*

```
$ this is a string
var num "10"

$ convertation to int
int num num
```

*Now variable 'num' has integer, not string*

# Input
*You can input your text with command ```input```:*

```
input text
```

*This code requires input from user and user input will be placed in variable ```text```.*

*Also if you need the input to be preceded by text you can type ```input "Your text: " text``` and even use variable for your text:*

```
var msg "Input text: "
input msg text

$ Output of this code: Input text:
$ It will require an input from user
```

*Syntax of this command:*

```input <text'> <name>```
* Where ' means that this argument not necessary.*

*Of course, you also can use this variable after inputing, for example ```println text``` or another.*

# Mathematics in FileScript

*For simple math calculations FileScript has command ```count```, you can use it for variables or output.*

```
$ Case 1
var res count 10 + 15
println res

$ Case 2
println count 10 + 15
```

*Also count can work with variables*

```
var num1 10
var num2 15

println count num1 + num2
```

*Also, count doesn't have only +, it also has operations * (multiply), / (divide) and - (subtraction)*
