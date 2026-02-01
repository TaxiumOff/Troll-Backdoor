import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))
server_socket.listen(1)

print("Serveur en écoute...")

client_socket, client_address = server_socket.accept()
print(f"Connexion de {client_address}")

while True:
    data = client_socket.recv(1024).decode()
    print(f"{data}")

    command = input("/> ")

    client_socket.send(command.encode())

    if command == "close":
        print("Connexion fermée")
        client_socket.close()
        break
