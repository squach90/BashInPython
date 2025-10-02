import time

username = "TEST"
filesystem = {
    username: {
        "Documents": {},
        "Games": {
            "InsideGames": {}
        },
    },
}

CurrentDir = "~"
current_folder = filesystem[username]
path = [username]

print(r"""   ___       __ _          _ _ 
  / _ \_   _/ _\ |__   ___| | |
 / /_)/ | | \ \| '_ \ / _ \ | |
/ ___/| |_| |\ \ | | |  __/ | |
\/     \__, \__/_| |_|\___|_|_|
       |___/
        pyshell-0.0.2 
      by Louis Lesniak
""")


# ----------------- Commands ------------------

def cd(cdPath):
    global current_folder, path, CurrentDir

    parts = cdPath.split("/")
    temp_path = path.copy()
    temp_folder = filesystem
    valid = True

    for p in temp_path:
        temp_folder = temp_folder[p]

    for part in parts:
        if part == "..":
            if len(temp_path) > 1:
                temp_path.pop()
                temp_folder = filesystem
                for p in temp_path:
                    temp_folder = temp_folder[p]
            else:
                temp_path = [username]
                temp_folder = filesystem[username]
        elif part in temp_folder and isinstance(temp_folder[part], dict):
            temp_folder = temp_folder[part]
            temp_path.append(part)
        else:
            print("pyshell: cd: " + cdPath + ": No such file or directory")
            valid = False
            break

    if valid:
        current_folder = temp_folder
        path = temp_path

    if path == [username]:
        CurrentDir = "~"
    else:
        CurrentDir = "~/" + "/".join(path[1:])


def clear():
    print("\n" * 100)


def echo(text, return_output=False):
    if return_output:
        return text
    else:
        print(text)


def exitPS():
    print("Bye " + username + " (^^)/" if username else "Bye (^^)/")
    time.sleep(1)
    exit()


def help_cmd():
    cmds = list(commands.keys())
    print("Commandes disponibles (Entrée = continuer, q = quitter):")
    for i, cmd in enumerate(cmds, 1):
        print(" -", cmd)
        if i % 10 == 0 and i != len(cmds):
            user_input = input("-- more -- ")
            if user_input.lower() == "q":
                break


def mkdir(name):
    if name not in current_folder:
        current_folder[name] = {}
    else:
        print("mkdir: cannot create directory: File exists")


def ls(directory=None):
    if directory:
        parts = directory.split("/")
        temp_folder = current_folder
        valid = True
        for part in parts:
            if part in temp_folder and isinstance(temp_folder[part], dict):
                temp_folder = temp_folder[part]
            else:
                print("pyshell: ls: cannot access " + directory + ": No such file or directory")
                valid = False
                break
        if not valid:
            return
    else:
        temp_folder = current_folder

    if not temp_folder:
        print("(empty)")
    else:
        for name, item in temp_folder.items():
            if isinstance(item, dict):
                print(name + "/", end=" ")
            else:
                print(name, end=" ")
        print()


def touch(filename):
    if not filename:
        print("touch: missing file operand")
    elif filename not in current_folder:
        current_folder[filename] = ""
    else:
        print("touch: cannot create file: File exists")


def cat(filename):
    if filename in current_folder:
        if isinstance(current_folder[filename], str):
            print(current_folder[filename], end="")
        else:
            print("cat: " + {filename} + ": Is a directory")
    else:
        print("cat: " + {filename} + ": No such file")


def pwd():
    if path == [username]:
        print("~")
    else:
        print("~/" + "/".join(path[1:]))


# ------------- Command dictionary -----------------

commands = {
    "clear": lambda args, ro=False: clear(),
    "help": lambda args, ro=False: help_cmd(),
    "exit": lambda args, ro=False: exitPS(),
    "pwd": lambda args, ro=False: pwd(),
    "echo": lambda args, ro=False: echo(args, ro),
    "cd": lambda args, ro=False: cd(args),
    "mkdir": lambda args, ro=False: mkdir(args),
    "touch": lambda args, ro=False: touch(args),
    "ls": lambda args, ro=False: ls(args),
    "cat": lambda args, ro=False: cat(args),
}


# ------------- Main loop -----------------

while True:
    if path == [username]:
        CurrentDir = "~"
    else:
        CurrentDir = "~/" + "/".join(path[1:])

    UserEntry = input(CurrentDir + "> ").strip()
    if not UserEntry:
        continue

    # handle redirection
    if ">" in UserEntry:
        if ">>" in UserEntry:
            command_part, filename = UserEntry.split(">>", 1)
            append = True
        else:
            command_part, filename = UserEntry.split(">", 1)
            append = False

        command_part = command_part.strip()
        filename = filename.strip()

        parts = command_part.split(" ", 1)
        cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if cmd in commands:
            output = commands[cmd](args, ro=True)
            if output is not None:
                if append and filename in current_folder:
                    current_folder[filename] += output + "\n"
                else:
                    current_folder[filename] = output + "\n"
        else:
            print("Commande inconnue: " + cmd)
        continue

    # normal execution
    parts = UserEntry.split(" ", 1)
    cmd = parts[0]
    args = parts[1] if len(parts) > 1 else ""

    if cmd in commands:
        commands[cmd](args)
    else:
        print("Commande inconnue: " + cmd)
