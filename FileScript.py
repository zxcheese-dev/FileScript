import sys
import os
import shlex
import shutil

variables = {}
skip = []

def lang(line):
    if not line:
        return

    dump_split = line.split()
    parts = shlex.split(line)

    if parts[0] == "println":
        if not skip or skip[-1]:
            if len(parts) == 2:
                value = parts[1]

                if value in variables:
                    print(variables[value])
                else:
                    print(f"NameError: Name '{parts[1]}' not defined")
                    return

            else:
                print("SyntaxError: println requires 1 value")
                return

    elif parts[0] == "var":
        if not skip or skip[-1]:
            if len(parts) >= 3:
                if dump_split[2:][0][0] == '"' and dump_split[2:][-1][-1] == '"':
                    name = parts[1]
                    value = parts[2]

                    variables[name] = value
                else:
                    if parts[2] in variables:
                        name = parts[1]
                        value = variables[parts[2]]

                        variables[name] = value
                    else:
                        print(f"NameError: Name '{parts[2]}' not defined")
                        return

            else:
                print("SyntaxError: var requires 2 arguments")
                return
        
    elif parts[0] == "input":
        if not skip or skip[-1]:
            if len(parts) == 2:
                input_name = parts[1]
                val = input()

                variables[input_name] = val
            else:
                print("SyntaxError: input requires 1 argument")

    elif parts[0] == "if":
        if not skip or not False in skip:
            if parts[2] == "==":
                if not parts[3] in variables:
                    if dump_split[3:][0][0] == '"' and dump_split[3:][-1][-1] == '"':
                        cond = variables[parts[1]] == parts[3]
                    else:
                        print(f"IndexError: Name '{parts[3]}' not defined")
                        return
                else:
                    cond = variables[parts[1]] == variables[parts[3]]

            elif parts[2] == "!=":
                if not parts[3] in variables:
                    if dump_split[3:][0][0] == '"' and dump_split[3:][-1][-1] == '"':
                        cond = variables[parts[1]] != parts[3]
                    else:
                        print(f"IndexError: Name '{parts[3]}' not defined")
                        return
                else:
                    cond = variables[parts[1]] != variables[parts[3]]

            if len(parts) >= 4:
                if len(skip) > 0 and skip[-1] == False:
                    skip.append(False)
                else:
                    skip.append(cond)

            else:
                print("SyntaxError: if requires 3 arguments")
                return

    elif parts[0] == "endif":
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
                            print(f"NameError: Name '{parts[1]}' not defined")
                            return

                except (FileNotFoundError):
                    print(f"FileNotFoundError: File {parts[1]} not found")
                    return
            else:
                print("SyntaxError: open requires 2 arguments")
                return

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
                            print(f"NameError: Name '{parts[2]}' not defined")
                            return
            else:
                print("SyntaxError: write requires 2 arguments")
                return

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
                                print(f"NameError: Name '{parts[2]}' not defined")
                                return

                except (FileNotFoundError):
                    print(f"FileNotFoundError: File {parts[1]} not found")
                    return
            else:
                print("SyntaxError: add requires 2 arguments")
                return

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
                                    print(f"NameError: Name '{parts[3]}' not defined")
                                    return
                    else:
                        print("SyntaxError: create requires 3 arguments for files")
                        return
                elif parts[1] == "dir":
                    if len(parts) == 3:
                        if dump_split[2:][0][0] == '"' and dump_split[2:][-1][-1] == '"':
                            os.mkdir(parts[2])
                        else:
                            if parts[2] in variables:
                                os.mkdir(variables[parts[2]])
                            else:
                                print(f"NameError: Name '{parts[2]}' not defined")
                                return
                    else:
                        print("SyntaxError: create requires 2 arguments for dirs")
                        return

            except (FileExistsError):
                print(f"FileExistError: File {parts[1]} already exist")
                return

    elif parts[0] == "remove":
        if not skip or skip[-1]:
            if len(parts) == 2:
                if dump_split[1:][0][0] == '"' and dump_split[1:][-1][-1] == '"':
                    if os.path.isfile(parts[1]):
                        try:
                            os.remove(parts[1])
                        except (FileNotFoundError):
                            print(f"FileNotFoundError: File {parts[1]} not found")
                            return
                        except (PermissionError):
                            print(f"PermissionError: Script has no permission for {parts[1]}")
                            return
                    elif os.path.isdir(parts[1]):
                        shutil.rmtree(parts[1])
                else:
                    if parts[1] in variables:
                        if os.path.isfile(variables[parts[1]]):
                            try:
                                os.remove(variables[parts[1]])
                            except (FileNotFoundError):
                                print(f"FileNotFoundError: File {parts[1]} not found")
                                return
                            except (PermissionError):
                                print(f"PermissionError: Script has no permission for {parts[1]}")
                                return
                        elif os.path.isdir(variables[parts[1]]):
                            shutil.rmtree(variables[parts[1]])
                    else:
                        print(f"NameError: Name '{parts[1]}' not defined")
                        return
            else:
                print("SyntaxError: remove requires 1 arguments")
                return

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
                        print(f"IndexError: Argument '{parts[2]}' is not defined")
                        return
                    
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
                            print(f"NameError: Name '{parts[1]}' not defined")
                            return
            else:
                print("SyntaxError: ls requires 1 or 2 arguments")
                return

    else:
        print(f"NameError: Unknown command {parts[0]}")
        return

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
        print(f"FileNotFoundError: File '{filename}' not found")
        return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        print("FileScript interpreter")

        while True:
            line = input("> ")
            lang(line)
