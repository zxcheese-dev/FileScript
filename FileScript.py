import sys
import os
import shlex
import shutil
import subprocess
import re
import time
import winreg

variables = {}
skip = []
fncs = {}
fncreate = []

def num_check(arg):
    try:
        return int(arg) if arg.isdigit() else float(arg)
    except ValueError:
        return None

def tokenise(value, is_string=False):
    if is_string:
        return value

    if value in variables:
        return variables[value]
    
    try:
        if '.' in value: return float(value)
        return int(value)
    except ValueError:
        pass

    if value.lower() == "true": return True
    if value.lower() == "false": return False

    if value in commands:
        commands[value]()

    raise NameError(f"Name '{value}' not defined")

def compare(a, b, op):
    if op == "==": return a == b
    if op == "!=": return a != b
    if op == "<":  return a < b
    if op == ">":  return a > b
    if op == "<=": return a <= b
    if op == ">=": return a >= b
    raise SyntaxError(f"Unknown operator '{op}'")


def count(num, op, num2):
    if not skip or skip[-1]:
        if num in variables or num2 in variables:
            try:
                if num in variables and not num2 in variables:
                    if op == "+": return variables[num] + num_check(num2)
                    if op == "-": return variables[num] - num_check(num2)
                    if op == "*": return variables[num] * num_check(num2)
                    if op == "/": return variables[num] / num_check(num2)
                    if op == "^": return variables[num] ^ num_check(num2)
                elif num2 in variables and not num in variables:
                    if op == "+": return num_check(num) + variables[num2]
                    if op == "-": return num_check(num) - variables[num2]
                    if op == "*": return num_check(num) * variables[num2]
                    if op == "/": return num_check(num) / variables[num2]
                    if op == "^": return num_check(num) ^ variables[num2]
                else:
                    if op == "+": return variables[num] + variables[num2]
                    if op == "-": return variables[num] - variables[num2]
                    if op == "*": return variables[num] * variables[num2]
                    if op == "/": return variables[num] / variables[num2]
                    if op == "^": return variables[num] ^ variables[num2]
            except (ValueError):
                raise ValueError("count cannot provide arguments that not number")
        else:
            try:
                if op == "+": return num_check(num) + num_check(num2)
                if op == "-": return num_check(num) - num_check(num2)
                if op == "*": return num_check(num) * num_check(num2)
                if op == "/": return num_check(num) / num_check(num2)
            except (ValueError):
                raise ValueError("count cannot provide arguments that not number")

def returnabe(*args):
    if not skip or skip[-1]:
        if len(args) >= 1:
            if args[0] in commands:
                return commands[args[0]](args[1:])
            elif args[0] in variables:
                return variables[args[0]]
            else:
                raise NameError(f"Name '{args[0]}' is not defined")
        else:
            raise SyntaxError("Return requires 1 argument")

def ls(path, type=None):
    if not skip or skip[-1]:
        files = []
        if type == "file":
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                
                if os.path.isfile(full_path):
                    files.append(item)
        elif type == "dir":
            for item in os.listdir(path):
                full_path = os.path.join(path, item)

                if os.path.isdir(full_path):
                    files.append(item)
        elif type == None:
            if path in variables:
                for item in os.listdir(variables[path]):
                    full_path = os.path.join(variables[path], item)

                    if os.path.isdir(full_path):
                        files.append(f"[DIR] {item}")
                    elif os.path.isfile(full_path):
                        files.append(f"[FILE] {item}")
            else:
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)

                    if os.path.isdir(full_path):
                        files.append(f"[DIR] {item}")
                    elif os.path.isfile(full_path):
                        files.append(f"[FILE] {item}")

        else:
            raise IndexError(f"Argument '{type}' is not defined")

        return files

def lang(line):
    global commands

    commands = {
        "count": count,
        "return": returnabe,
        "ls": ls
    }

    if not line:
        return

    dump_split = line.split()
    parts = shlex.split(line)

    if not fncreate or not fncreate[-1]:
        if parts[0] == "println":
            if not skip or skip[-1]:
                if len(parts) >= 2:
                    if dump_split[1] in variables:
                        print(variables[dump_split[1]])
                    else:
                        raise NameError(f"Name '{dump_split[1]}' not defined")
                else:
                    raise SyntaxError("println requires 1 value")

        elif parts[0] == "var":
            if not skip or skip[-1]:
                if len(parts) >= 3:
                    if parts[2] in commands:
                        args = parts[3:]

                        variables[parts[1]] = commands[parts[2]](*args)
                    else:
                        raw_val = line.split(maxsplit=2)[2]
                        is_str = (raw_val.startswith('"') and raw_val.endswith('"')) or (raw_val.startswith("'") and raw_val.endswith("'"))

                        variables[parts[1]] = tokenise(parts[2], is_string=is_str)
                else:
                    raise SyntaxError("var requires 2 arguments")

        elif parts[0] == "input":
            if not skip or skip[-1]:
                if len(parts) == 2:
                    variables[parts[1]] = input()
                else:
                    raise SyntaxError("input requires 1 argument")

        elif parts[0] == "wait":
            if len(parts) >= 2:
                if parts[1] in commands:
                    args = parts[2:]

                    time.sleep(commands[parts[1]](*args))
                else:
                    if dump_split[1] in variables:
                        time.sleep(variables[dump_split[1]])
                    else:
                        try:
                            time.sleep(float(parts[1]))
                        except (ValueError):
                            if (dump_split[1][0][0] == '"' and dump_split[-1][-1][-1] == '"') or (dump_split[1][0][0] == "'" and dump_split[-1][-1][-1] == "'"):
                                raise ValueError(f"wait cannot use arguments like '{parts[1]}'")
                            else:
                                raise ValueError(f"Variable '{parts[1]}' is not defined")
            else:
                raise SyntaxError("wait requires 1 argument")

        elif parts[0] == "if":
            if not skip or not False in skip:
                match = re.match(r"if\s+(.+?)\s*(==|!=|<=|>=|<|>)\s*(.+)", line.strip())
                if match:
                    raw_left = match.group(1).strip()
                    op = match.group(2)
                    raw_right = match.group(3).strip()

                    left_clean = shlex.split(raw_left)[0]
                    right_clean = shlex.split(raw_right)[0]

                    left_is_str = (raw_left.startswith('"') and raw_left.endswith('"')) or (raw_left.startswith("'") and raw_left.endswith("'"))
                    right_is_str = (raw_right.startswith('"') and raw_right.endswith('"')) or (raw_right.startswith("'") and raw_right.endswith("'"))

                    left = tokenise(left_clean, is_string=left_is_str)
                    right = tokenise(right_clean, is_string=right_is_str)

                    cond = compare(left, right, op)

                    if len(skip) > 0 and skip[-1] == False:
                        skip.append(False)
                    else:
                        skip.append(cond)
                else:
                    raise SyntaxError("if requires 3 arguments")

        elif parts[0] == "endif":
            if skip:
                skip.pop()

        elif parts[0] == "open":
            if not skip or skip[-1]:
                if len(parts) >= 3:
                    try:
                        if dump_split[1:dump_split.index(parts[2])][0][0] == '"' and dump_split[1:dump_split.index(parts[2])][-1][-1] == '"':
                            with open(parts[1], 'r', encoding='utf-8') as f:
                                data = f.read()
                            variables[parts[2]] = data
                        else:
                            if parts[1] in variables:
                                with open(variables[parts[1]], 'r', encoding='utf-8') as f:
                                    data = f.read()
                                variables[parts[2]] = data
                            else:
                                raise NameError(f"Name '{parts[1]}' not defined")

                    except (FileNotFoundError):
                        raise FileNotFoundError(f"File {parts[1]} not found")
                else:
                    raise SyntaxError("open requires 2 arguments")

        elif parts[0] == "write":
            if not skip or skip[-1]:
                if len(parts) == 3:
                    with open(parts[1], 'w', encoding='utf-8') as f:
                        if dump_split[2:][0][0] == '"' and dump_split[2:][-1][-1] == '"':
                            f.write(parts[2])
                        else:
                            if parts[2] in variables:
                                f.write(variables[parts[2]])
                            else:
                                raise NameError(f"Name '{parts[2]}' not defined")
                else:
                    raise SyntaxError("write requires 2 arguments")

        elif parts[0] == "add":
            if not skip or skip[-1]:
                if len(parts) >= 3:
                    try:
                        with open(parts[1], 'a', encoding='utf-8') as f:
                            if dump_split[2:][0][0] == '"' and dump_split[2:][-1][-1] == '"':
                                f.write(parts[2])
                            else:
                                if parts[2] in variables:
                                    f.write(variables[parts[2]])
                                else:
                                    raise NameError(f"Name '{parts[2]}' not defined")

                    except (FileNotFoundError):
                        raise FileNotFoundError(f"File {parts[1]} not found")
                else:
                    raise SyntaxError("add requires 2 arguments")

        elif parts[0] == "create":
            if not skip or skip[-1]:
                try:
                    if parts[1] == "file":
                        if len(parts) == 4:
                            with open(parts[2], 'x', encoding='utf-8') as f:
                                if dump_split[3:][0][0] == '"' and dump_split[3:][-1][-1] == '"':
                                    f.write(parts[3])
                                else:
                                    if parts[3] in variables:
                                        f.write(variables[parts[3]])
                                    else:
                                        raise NameError(f"Name '{parts[3]}' not defined")
                        else:
                            raise SyntaxError("create requires 3 arguments for files")
                    elif parts[1] == "dir":
                        if len(parts) == 3:
                            if dump_split[2:][0][0] == '"' and dump_split[2:][-1][-1] == '"':
                                os.mkdir(parts[2])
                            else:
                                if parts[2] in variables:
                                    os.mkdir(variables[parts[2]])
                                else:
                                    raise NameError(f"Name '{parts[2]}' not defined")
                        else:
                            raise SyntaxError("create requires 2 arguments for dirs")

                except (FileExistsError):
                    raise FileExistsError(f"File {parts[1]} already exist")

        elif parts[0] == "remove":
            if not skip or skip[-1]:
                if len(parts) == 2:
                    if dump_split[1:][0][0] == '"' and dump_split[1:][-1][-1] == '"':
                        if os.path.isfile(parts[1]):
                            try:
                                os.remove(parts[1])
                            except (FileNotFoundError):
                                raise FileNotFoundError(f"File {parts[1]} not found")
                            except (PermissionError):
                                raise PermissionError(f"Script has no permission for {parts[1]}")
                        elif os.path.isdir(parts[1]):
                            shutil.rmtree(parts[1])
                    else:
                        if parts[1] in variables:
                            if os.path.isfile(variables[parts[1]]):
                                try:
                                    os.remove(variables[parts[1]])
                                except (FileNotFoundError):
                                    raise FileNotFoundError(f"File {parts[1]} not found")
                                except (PermissionError):
                                    raise PermissionError(f"Script has no permission for {parts[1]}")
                            elif os.path.isdir(variables[parts[1]]):
                                shutil.rmtree(variables[parts[1]])
                        else:
                            raise NameError(f"Name '{parts[1]}' not defined")
                else:
                    raise SyntaxError("remove requires 1 argument")
        
        elif parts[0] == "reboot":
            if not skip or skip[-1]:
                try:
                    if len(parts) == 2:
                        if dump_split[1] in variables:
                            os.system(f"shutdown /r /t {int(variables[parts[1]])}")
                        else:
                            os.system(f"shutdown /r /t {int(parts[1])}")
                    else:
                        raise SyntaxError("reboot requires 1 argument")
                except (ValueError):
                    if parts[1] in variables:
                        raise ValueError(f"Argument '{variables[parts[1]]}' cannot be integer")
                    else:
                        raise ValueError(f"Argument '{parts[1]}' cannot be integer")

        elif parts[0] == "root":
            if not skip or skip[-1]:
                if len(parts) == 3:
                    if parts[1] == "file":
                        if dump_split[2] in variables:
                            if os.path.isfile(variables[parts[2]]):
                                commands = [
                                    f'takeown /f "{variables[parts[2]]}"',
                                    f'icacls "{variables[parts[2]]}" /grant %username%:F',
                                    f'icacls "{variables[parts[2]]}" /grant Administrators:F'
                                ]
            
                                for cmd in commands:
                                    root = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
                                    if root.returncode != 0:
                                        raise RuntimeError(f"root returned {root.returncode}")
                            else:
                                raise FileNotFoundError(f"File '{variables[parts[2]]}' not found")
                        else:
                            if os.path.isfile(parts[2]):
                                commands = [
                                    f'takeown /f "{parts[2]}"',
                                    f'icacls "{parts[2]}" /grant %username%:F',
                                    f'icacls "{parts[2]}" /grant Administrators:F'
                                ]

                                for cmd in commands:
                                    root = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                                    if root.returncode != 0:
                                        raise RuntimeError(f"root returned {root.returncode}")
                            else:
                                raise FileNotFoundError(f"File '{parts[2]}' not found")

                    elif parts[1] == "dir":
                        if dump_split[2] in variables:
                            if os.path.isdir(variables[parts[2]]):
                                commands = [
                                    f'takeown /f "{variables[parts[2]]}" /r /d y',
                                    f'icacls "{variables[parts[2]]}" /grant %username%:F /t',
                                    f'icacls "{variables[parts[2]]}" /grant Administrators:F /t'
                                ]
            
                                for cmd in commands:
                                    root = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
                                    if root.returncode != 0:
                                        raise RuntimeError(f"root returned {root.returncode}")
                            else:
                                raise FileNotFoundError(f"Dir '{variables[parts[2]]}' not found")
                        else:
                            if os.path.isdir(parts[2]):
                                commands = [
                                    f'takeown /f "{parts[2]}" /r /d y',
                                    f'icacls "{parts[2]}" /grant %username%:F /t',
                                    f'icacls "{parts[2]}" /grant Administrators:F /t'
                                ]

                                for cmd in commands:
                                    root = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                                    if root.returncode != 0:
                                        raise RuntimeError(f"root returned {root.returncode}")
                            else:
                                raise FileNotFoundError(f"Dir '{parts[2]}' not found")

                    else:
                        raise IndexError(f"Argument '{parts[1]}' is not defined")
                else:
                    raise SyntaxError("root requires 2 arguments")

        elif parts[0] == "AutoReg":
            if not skip or skip[-1]:
                if len(parts) == 3:
                    app_name = parts[2]
                    if parts[1] == "self":
                        script_path = sys.argv[1]
                    else:
                        script_path = parts[1]

                    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

                    try:
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, script_path)
                        winreg.CloseKey(key)

                    except FileNotFoundError:
                        raise FileNotFoundError(f"Path '{script_path}' not found")
                else:
                    raise SyntaxError("AutoReg requires 2 arguments")

        elif parts[0] == "run":
            if not skip or skip[-1]:
                if len(parts) == 2:
                    if dump_split[1] in variables:
                        try:
                            os.startfile(variables[parts[1]])
                        except (FileNotFoundError):
                            raise FileNotFoundError(f"File '{variables[parts[1]]}' not found")
                    else:
                        try:
                            os.startfile(parts[1])
                        except (FileNotFoundError):
                            raise FileNotFoundError(f"File '{dump_split[1]}' not found")
                else:
                    raise SyntaxError("run requires 1 argument") 

        elif parts[0] == "import":
            if not skip or skip[-1]:
                if len(parts) == 2:
                    try:
                        run_file(parts[1])
                    except FileNotFoundError:
                        raise ModuleNotFoundError(f"Module '{parts[1]}' not found")
                else:
                    raise SyntaxError("import requires 1 argument")

        elif parts[0] == "fnc":
            if len(parts) >= 2:
                global fnc_name
                fncreate.append(True)
                fnc_name = parts[1]
                fnc_args = parts[2:]
                fncs[fnc_name] = []

                for line in fnc_args:
                    if line != "endfnc":
                        fncs[fnc_name].append(line)
                    else:
                        break

        elif parts[0] == "endfnc":
            fncreate.append(False)

        else:
            if parts[0] in fncs:
                for cmd in fncs[parts[0]]:
                    lang(cmd)
            else:
                raise NameError(f"Unknown command '{parts[0]}'")
    else:
        if parts[0] == "endfnc":
            fncreate.append(False)
        else:
            fncs[fnc_name].append(line)

def run_file(filename):
    if not filename.endswith(".fssc"):
        print("EndswithError: Only .fssc files are supported")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    lang(line)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        print("FileScript interpreter by zxcheese python developer")

        while True:
            line = input("> ")
            lang(line)

# FileScript interpreter Powered by zxcheese Python developer
