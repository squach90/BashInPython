import time

username = "TEST"
filesystem = {
    "home": {
        username: {
            "Documents":{},
            "Games":{},
        },   
    }
}


CurrentDir = "~"
current_folder = filesystem["home"]
path = ["home"]


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

    if cdPath == "..":
        # Remonter d'un dossier si possible
        if len(path) > 1:
            path.pop()
            # reconstruire current_folder depuis filesystem et path
            current_folder = filesystem["home"][path[0]]
            for p in path[1:]:
                current_folder = current_folder[p]
        else:
            print("Déjà à la racine !")
    else:
        # Vérifier que le dossier existe dans le dossier courant
        if cdPath in current_folder and isinstance(current_folder[cdPath], dict):
            path.append(cdPath)
            current_folder = current_folder[cdPath]
        else:
            print("pyshell: cd: " + cdPath + ": No such file or directory",)

    # Mettre à jour le prompt
    CurrentDir = "~/" + "/".join(path)


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


def pwd():
    print("~/" + "/".join(path))

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
    "echo": lambda args: echo(args),  # args = texte à afficher
    "cd": lambda args: cd(args),  # args = texte à afficher
    "config": lambda args: config(), 
}



while True:
    CurrentDir = "~/" + "/".join(path)
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