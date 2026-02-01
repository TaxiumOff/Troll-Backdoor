import socket
from colorama import Fore, Style, init

init(autoreset=True)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))
server_socket.listen(1)

print(Fore.GREEN + "[+] Serveur en écoute...")

client_socket, client_address = server_socket.accept()
print(Fore.CYAN + f"[✓] Connexion de {client_address}")

while True:
    data = client_socket.recv(1024).decode()
    print(Fore.YELLOW + f"[CLIENT] {data}")

    command = input(
        Fore.RED + "troll@server " +
        Fore.WHITE + "➜ " +
        Fore.MAGENTA
    )

    client_socket.send(command.encode())

    if command == "close":
        print(Fore.RED + "[!] Connexion fermée")
        client_socket.close()
        break
