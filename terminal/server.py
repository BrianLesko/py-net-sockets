# Brian Lesko 12/16/2023

import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))  # Replace '0.0.0.0' with the server's IP address
server.listen()

print("Waiting for connection...")
client_socket, client_address = server.accept()
print(f"Connected to {client_address}")

while True:
    message = client_socket.recv(1024).decode()
    if not message:
        break
    print(f"Client: {message}")
    reply = input("Reply: ")
    client_socket.send(reply.encode())

client_socket.close()
server.close()
