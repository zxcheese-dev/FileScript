import sys
import os
import shlex
import shutil
import subprocess
import re
import time
import winreg
import openpyxl

variables = {}
skip = []

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

    if value.lower() == "true": return True
    if value.lower() == "false": return False

    try:
        if '.' in value: return float(value)
        return int(value)
    except ValueError:
        pass

    raise NameError(f"Name '{value}' not defined")

def compare(a, b, op):
    if op == "==": return a == b
    if op == "!=": return a != b
    if op == "<":  return a < b
    if op == ">":  return a > b
    if op == "<=": return a <= b
    if op == ">=": return a >= b
    raise SyntaxError(f"Unknown operator '{op}'")

def lang(line):
    if not line:
        return

    dump_split = line.split()
    parts = shlex.split(line)

    if parts[0] == "println":
        if not skip or skip[-1]:
            if len(parts) == 2:
                if dump_split[1] in variables:
                    print(variables[dump_split[1]])
                else:
                    raise NameError(f"Name '{dump_split[1]}' not defined")
            else:
                raise SyntaxError("println requires 1 value")

    elif parts[0] == "var":
        if not skip or skip[-1]:
            if len(parts) >= 3:
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

    elif parts[0] == "count":
        if not skip or skip[-1]:
            if len(parts) == 4:
                if dump_split[1] in variables or dump_split[3] in variables:
                    try:
                        if dump_split[1] in variables and not dump_split[3] in variables:
                            if parts[2] == "+": print(variables[parts[1]] + num_check(parts[3]))
                            if parts[2] == "-": print(variables[parts[1]] - num_check(parts[3]))
                            if parts[2] == "*": print(variables[parts[1]] * num_check(parts[3]))
                            if parts[2] == "/": print(variables[parts[1]] / num_check(parts[3]))
                        elif dump_split[3] in variables and not dump_split[1] in variables:
                            if parts[2] == "+": print(num_check(parts[1]) + variables[parts[3]])
                            if parts[2] == "-": print(num_check(parts[1]) - variables[parts[3]])
                            if parts[2] == "*": print(num_check(parts[1]) * variables[parts[3]])
                            if parts[2] == "/": print(num_check(parts[1]) / variables[parts[3]])
                        else:
                            if parts[2] == "+": print(variables[parts[1]] + variables[parts[3]])
                            if parts[2] == "-": print(variables[parts[1]] - variables[parts[3]])
                            if parts[2] == "*": print(variables[parts[1]] * variables[parts[3]])
                            if parts[2] == "/": print(variables[parts[1]] / variables[parts[3]])
                    except (ValueError):
                        raise ValueError("count cannot provide arguments that not number")
                else:
                    try:
                        if parts[2] == "+": print(num_check(parts[1]) + num_check(parts[3]))
                        if parts[2] == "-": print(num_check(parts[1]) - num_check(parts[3]))
                        if parts[2] == "*": print(num_check(parts[1]) * num_check(parts[3]))
                        if parts[2] == "/": print(num_check(parts[1]) / num_check(parts[3]))
                    except (ValueError):
                        raise ValueError("count cannot provide arguments that not number")
            else:
                raise SyntaxError("count requires 3 arguments")

    elif parts[0] == "wait":
        if len(parts) == 2:
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

    elif parts[0] == "ls":
        if not skip or skip[-1]:
            if len(parts) >= 2:
                if len(parts) == 3:
                    if parts[2] == "file":
                        for item in os.listdir(parts[1]):
                            full_path = os.path.join(parts[1], item)
                            
                            if os.path.isfile(full_path):
                                print(item)
                    elif parts[2] == "dir":
                        for item in os.listdir(parts[1]):
                            full_path = os.path.join(parts[1], item)

                            if os.path.isdir(full_path):
                                print(item)
                    else:
                        raise IndexError(f"Argument '{parts[2]}' is not defined")
                    
                else:
                    if dump_split[1:][0][0] == '"' and dump_split[1:][-1][-1] == '"':
                        for item in os.listdir(parts[1]):
                            full_path = os.path.join(parts[1], item)

                            if os.path.isdir(full_path):
                                print(f"[DIR] {item}")
                            elif os.path.isfile(full_path):
                                print(f"[FILE] {item}")
                    else:
                        if parts[1] in variables:
                            for item in os.listdir(variables[parts[1]]):
                                full_path = os.path.join(variables[parts[1]], item)

                                if os.path.isdir(full_path):
                                    print(f"[DIR] {item}")
                                elif os.path.isfile(full_path):
                                    print(f"[FILE] {item}")
                        else:
                            raise NameError(f"Name '{parts[1]}' not defined")
            else:
                raise SyntaxError("ls requires 1 or 2 arguments")
    
    elif parts[0] == "reboot":
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
                raise FileNotFoundError("Path '{script_path}' not found")
        else:
            raise SyntaxError("AutoReg requires 2 arguments")

    elif parts[0] == "run":
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

    else:
        raise NameError(f"Unknown command '{parts[0]}'")

def run_file(filename):
    if not filename.endswith(".filesc"):
        print("EndswithError: Only .filesc files are supported")
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
        print("FileScript interpreter")

        while True:
            line = input("> ")
            lang(line)

# FileScript interpreter Powered by zxcheese python developer
