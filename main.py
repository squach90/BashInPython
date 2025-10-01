import time

username = "TEST"
filesystem = {
    username: {
        "Documents":{},
        "Games":{
            "InsideGames":{}
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
        pyshell-0.0.1 
      by Louis Lesniak
      """)

def cd(cdPath):
    global current_folder, path, CurrentDir

    parts = cdPath.split("/")
    temp_path = path.copy()
    temp_folder = filesystem
    valid = True

    # rebuild temp_folder from current path
    for p in temp_path:
        temp_folder = temp_folder[p]

    for part in parts:
        if part == "..":
            if len(temp_path) > 1:  # stay inside user's home
                temp_path.pop()
                temp_folder = filesystem
                for p in temp_path:
                    temp_folder = temp_folder[p]
            else:
                # already at ~ (username root)
                temp_path = [username]
                temp_folder = filesystem[username]
        elif part in temp_folder and isinstance(temp_folder[part], dict):
            temp_folder = temp_folder[part]
            temp_path.append(part)
        else:
            print("pyshell: cd: " + cdPath + ": No such file or directory",)
            valid = False
            break

    if valid:
        current_folder = temp_folder
        path = temp_path

    # build CurrentDir like bash (~ instead of showing username)
    if path == [username]:
        CurrentDir = "~"
    else:
        CurrentDir = "~/" + "/".join(path[1:])


def clear():
    print("\n" * 100)

def config():
    clear()
    username = input("Enter your username: ")
    # TODO: create the config

def echo(text):
    print(text)

def exitPS():
    print("Bye " + username + " (^^)/" if username else "Bye (^^)/")
    time.sleep(3)
    print("(U can close the program)")

def help_cmd():
    print("Commandes disponibles:")
    for cmd in commands:
        print(" -", cmd)

def mkdir(name):
    if name not in current_folder:
        current_folder[name] = {}
    else:
        print("mkdir: cannot create directory: File exists")

def ls():
    if not current_folder:
        print("(empty)")
    else:
        for name, item in current_folder.items():
            if isinstance(item, dict):
                print(name + "/", end=" ")
            else:
                print(name, end=" ")
        print()

def touch(filename):
    if not filename:
        print("touch: missing file operand")
    if filename not in current_folder:
        current_folder[filename] = ""
    else:
        print("touch: cannot create directory: File exists")



def pwd():
    if path == [username]:
        print("~/ (User Folder)")
    else:
        print("~/" + "/".join(path[1:]))

def test():
    global current_folder, path, CurrentDir
    # Vérifier que "Games" existe dans le dossier de l'utilisateur
    if "Games" in filesystem["home"][username] and isinstance(filesystem["home"][username]["Games"], dict):
        current_folder = filesystem["home"][username]["Games"]
        path = [username, "Games"]  # inclure l'utilisateur dans le chemin
        CurrentDir = "~/" + "/".join(path)
        print("Dossier " + CurrentDir + " ouvert !")
    else:
        print("Le dossier 'Games' n'existe pas !") 


# Dictionnaire des commandes
commands = {
    "clear": lambda args: clear(),
    "help": lambda args: help_cmd(),
    "exit": lambda args: exitPS(),
    "pwd": lambda args: pwd(),
    "test": lambda args: test(),
    "echo": lambda args: echo(args),   
    "cd": lambda args: cd(args),   
    "mkdir": lambda args: mkdir(args),  
    "touch": lambda args: touch(args),   
    "config": lambda args: config(), 
    "ls": lambda args: ls(), 
}



while True:
    if path == [username]:
        CurrentDir = "~ "
    else:
        CurrentDir = "~/" + "/".join(path[1:])
    UserEntry = input(CurrentDir + "> ").strip()
    if not UserEntry:
        continue

    parts = UserEntry.split(" ", 1)
    cmd = parts[0]
    args = parts[1] if len(parts) > 1 else ""

    # exécuter la commande si elle existe
    if cmd in commands:
        commands[cmd](args)
    else:
        print("Commande inconnue: " + cmd)