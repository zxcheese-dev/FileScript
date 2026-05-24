import sys
import os
import shlex
import shutil

variables = {}
skip = []

def lang(line):
    if not line:
        return

    parts = shlex.split(line)

    if parts[0] == "println":
        if not skip or skip[-1]:
            if len(parts) == 2:
                value = parts[1]

                if value in variables:
                    print(variables[value])
                else:
                    print(value)

            else:
                print("SyntaxError: println requires 1 value")
                return

    elif parts[0] == "var":
        if not skip or skip[-1]:
            if len(parts) >= 3:
                name = parts[1]
                value = parts[2]

                variables[name] = value

            else:
                print("SyntaxError: var name value")
                return

    elif parts[0] == "input":
        if not skip or skip[-1]:
            if len(parts) == 2:
                input_name = parts[1]
                val = input()

                variables[input_name] = val
            else:
                print("SyntaxError: input must have 1 argument")

    elif parts[0] == "if":
        if not skip or not False in skip:
        	cond = variables[parts[1]] == parts[2]

        if len(parts) >= 3:
            if len(skip) > 0 and skip[-1] == False:
                skip.append(False)
            else:
                skip.append(cond)

        else:
            print("if: if requires 2 value")
            return

    elif parts[0] == "endif":
        skip.pop()

    elif parts[0] == "open":
        if not skip or skip[-1]:
            if len(parts) >= 3:
                try:
                    with open(parts[1], 'r', encoding='utf-8') as f:
                        data = f.read()
                    variables[parts[2]] = data

                except (FileNotFoundError):
                    print(f"FileNotFoundError: File {parts[1]} not found")
                    return
            else:
                print("SyntaxError: open requires 2 arguments")
                return

    elif parts[0] == "write":
        if not skip or skip[-1]:
            if len(parts) >= 3:
                with open(parts[1], 'w', encoding='utf-8') as f:
                    f.write(parts[2])
            else:
                print("SyntaxError: write requires 2 arguments")
                return

    elif parts[0] == "add":
        if not skip or skip[-1]:
            if len(parts) >= 3:
                try:
                    with open(parts[1], 'a', encoding='utf-8') as f:
                        f.write(parts[2])

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
                            f.write(parts[3])
                    else:
                        print("SyntaxError: create requires 3 arguments for files")
                        return
                elif parts[1] == "dir":
                    if len(parts) == 3:
                        os.mkdir(parts[2])
                    else:
                        print("SyntaxError: create requires 2 arguments for dirs")
                        return

            except (FileExistsError):
                print(f"FileExistError: File {parts[2]} already exist")
                return

    elif parts[0] == "remove":
        if not skip or skip[-1]:
            if len(parts) >= 2:
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
                print("SyntaxError: remove requires 2 arguments")
                return

    else:
        print(f"NameError: Unknown command {parts[0]}")
        return

def run_file(filename):
    if not filename.endswith(".filesc"):
        print("Error: only .filesc files are supported")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    lang(line)
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        print("FileScript interpreter")

        while True:
            line = input("> ")
            lang(line)